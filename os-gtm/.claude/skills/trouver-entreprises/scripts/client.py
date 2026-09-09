"""Client Crustdata - recherche et enrichissement d'entreprises. Stdlib uniquement."""
from __future__ import annotations
import csv
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://api.crustdata.com"
ROOT_ENV = Path(__file__).resolve().parents[4] / ".env"


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


def search_companies(industry: str = None, employee_range: str = None, location: str = None,
                      keywords: str = None, limit: int = 50) -> list[dict]:
    body = {"limit": limit}
    if industry:
        body["industry"] = industry
    if employee_range:
        body["employee_range"] = employee_range
    if location:
        body["location"] = location
    if keywords:
        body["keywords"] = keywords
    res = _request("POST", "/v1/companies/search", body)
    return res.get("results", [])


def enrich_company(domain: str) -> dict:
    res = _request("GET", f"/screener/company?company_domain={domain}")
    if isinstance(res, list):
        return res[0] if res else {}
    return res


def normalize(item: dict) -> dict:
    return {
        "name": item.get("name") or item.get("company_name"),
        "website": item.get("website") or item.get("company_website") or item.get("domain"),
        "industry": item.get("industry"),
        "employee_count": item.get("employee_count") or item.get("employees"),
        "hq_country": item.get("hq_country"),
        "company_type": item.get("company_type"),
        "description": item.get("description") or item.get("linkedin_company_description"),
        "funding_stage": item.get("funding_stage") or item.get("last_funding_round"),
        "linkedin_url": item.get("linkedin_url") or item.get("linkedin_profile_url"),
        "year_founded": item.get("year_founded") or item.get("founded_year"),
    }


def get_credits() -> float:
    return _request("GET", "/user/credits")["credits"]


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
        print("Usage : python client.py search --keywords '...' --industry '...' "
              "--employee-range '...' --location '...' --limit 50 --out sortie.csv")
        sys.exit(0)
    args = sys.argv[2:]
    kwargs = {}
    out = "companies.csv"
    i = 0
    while i < len(args):
        if args[i] == "--out":
            out = args[i + 1]
            i += 2
            continue
        key = args[i].lstrip("-").replace("-", "_")
        kwargs[key] = args[i + 1]
        i += 2
    limit = int(kwargs.pop("limit", 50))
    results = search_companies(limit=limit, **kwargs)
    rows = [normalize(r) for r in results]
    write_csv(rows, Path(out))
    print(f"[+] {len(rows)} entreprises trouvees, ecrites dans {out}")
