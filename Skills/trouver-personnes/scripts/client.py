"""Client Crustdata - recherche et enrichissement de personnes. Stdlib uniquement."""
from __future__ import annotations
import csv
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://api.crustdata.com"
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


def load_api_key() -> str:
    key = os.environ.get("CRUSTDATA_API_KEY")
    if key:
        return key
    if ROOT_ENV.exists():
        for line in ROOT_ENV.read_text().splitlines():
            if line.strip().startswith("CRUSTDATA_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(f"CRUSTDATA_API_KEY introuvable (env ou {ROOT_ENV})")


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {
        "Authorization": f"Token {load_api_key()}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur {method} {path} : {e.read().decode()}")


def _condition(column: str, value, op_type: str = "[.]") -> dict:
    if isinstance(value, list):
        return {"column": column, "type": "in", "value": value}
    return {"column": column, "type": op_type, "value": value}


def search_people(company_name: str = None, titles: list[str] = None,
                   seniority_levels: list[str] = None, location: str = None,
                   limit: int = 100, cursor: str = None) -> dict:
    """titles/seniority_levels : listes de valeurs (combinees en OR entre elles,
    combinees en AND avec les autres criteres)."""
    conditions = []
    if company_name:
        conditions.append(_condition("current_employers.name", company_name))
    if titles:
        conditions.append({"op": "or", "conditions": [
            _condition("current_employers.title", t) for t in titles
        ]})
    if seniority_levels:
        conditions.append(_condition("current_employers.seniority_level", seniority_levels))
    if location:
        conditions.append(_condition("region", location))

    if not conditions:
        raise ValueError("Au moins un critere est requis (entreprise, titre, seniorite ou localisation)")
    filters = conditions[0] if len(conditions) == 1 else {"op": "and", "conditions": conditions}

    body = {"filters": filters, "limit": min(limit, 1000)}
    if cursor:
        body["cursor"] = cursor
    return _request("POST", "/screener/persondb/search/", body)


def enrich_person(linkedin_url: str = None, first_name: str = None, last_name: str = None,
                   domain: str = None, company_name: str = None) -> dict:
    params = []
    if linkedin_url:
        params.append(f"linkedin_url={linkedin_url}")
    else:
        params += [f"first_name={first_name}", f"last_name={last_name}"]
        params.append(f"domain={domain}" if domain else f"company_name={company_name}")
    return _request("GET", f"/screener/person/enrich/?{'&'.join(params)}")


def normalize(profile: dict) -> dict:
    emp = (profile.get("current_employers") or [{}])[0]
    return {
        "name": profile.get("name"),
        "headline": profile.get("headline"),
        "title": emp.get("title"),
        "company": emp.get("name"),
        "company_domain": emp.get("company_website_domain"),
        "seniority_level": emp.get("seniority_level"),
        "region": profile.get("region"),
        "linkedin_url": profile.get("linkedin_profile_url"),
    }


def write_csv(rows: list[dict], out_path: Path) -> None:
    if not rows:
        Path(out_path).write_text("")
        return
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or sys.argv[1] != "search":
        print("Usage : python client.py search --titles 'CEO,Founder' --location 'France' "
              "--company-name '...' --seniority-levels 'director,vp' --limit 100 --out sortie.csv")
        sys.exit(0)
    args = sys.argv[2:]
    kwargs = {}
    out = "personnes.csv"
    i = 0
    while i < len(args):
        if args[i] == "--out":
            out = args[i + 1]
            i += 2
            continue
        key = args[i].lstrip("-").replace("-", "_")
        val = args[i + 1]
        if key in ("titles", "seniority_levels"):
            val = [v.strip() for v in val.split(",")]
        kwargs[key] = val
        i += 2
    limit = int(kwargs.pop("limit", 100))
    res = search_people(limit=limit, **kwargs)
    rows = [normalize(p) for p in res.get("profiles", [])]
    write_csv(rows, Path(out))
    print(f"[+] {len(rows)} personnes trouvees (total disponible : {res.get('total_count')}), ecrites dans {out}")
