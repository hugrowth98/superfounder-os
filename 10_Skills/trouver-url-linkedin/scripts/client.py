"""Client Unipile - trouver l'URL LinkedIn d'une personne a partir de son nom (et
optionnellement son entreprise). Stdlib uniquement."""
from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"

DISTANCE_RANK = {
    "SELF": 0,
    "FIRST_DEGREE": 1,
    "DISTANCE_1": 1,
    "DISTANCE_2": 2,
    "DISTANCE_3": 3,
    "OUT_OF_NETWORK": 4,
}


def _load(var: str) -> str:
    val = os.environ.get(var)
    if val:
        return val
    if ROOT_ENV.exists():
        for line in ROOT_ENV.read_text().splitlines():
            if line.strip().startswith(f"{var}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(f"{var} introuvable (env ou {ROOT_ENV})")


def dsn() -> str:
    return _load("UNIPILE_DSN")


def api_key() -> str:
    return _load("UNIPILE_API_KEY")


def _request(method: str, path: str, params: dict | None = None, body: dict | None = None) -> dict:
    url = f"{dsn()}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        url = f"{url}?{qs}"
    data = json.dumps(body).encode() if body else None
    headers = {"X-API-KEY": api_key(), "Accept": "application/json"}
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur {method} {path} : {e.read().decode()}")


def _clean_url(profile_url: str) -> str:
    return profile_url.split("?")[0] if profile_url else profile_url


def _search_people(account_id: str, keywords: str, limit: int) -> list[dict]:
    body = {"api": "classic", "category": "people", "keywords": keywords, "limit": limit}
    data = _request("POST", "/api/v1/linkedin/search", params={"account_id": account_id}, body=body)
    return data.get("items", [])


def find_linkedin_url(account_id: str, name: str, company: str | None = None, max_results: int = 5) -> list[dict]:
    """Cherche une personne par nom (+ entreprise si fournie). Si 0 resultat avec le nom
    et l'entreprise combines, retente avec le nom seul (une entreprise mal orthographiee
    ou un raccourci peut faire echouer la recherche exacte)."""
    keywords = f"{name} {company}".strip() if company else name
    items = _search_people(account_id, keywords, max_results)
    fallback_used = False
    if not items and company:
        items = _search_people(account_id, name, max_results)
        fallback_used = True

    results = []
    for it in items:
        results.append({
            "name": it.get("name"),
            "headline": it.get("headline"),
            "location": it.get("location"),
            "network_distance": it.get("network_distance"),
            "public_identifier": it.get("public_identifier"),
            "linkedin_url": _clean_url(it.get("profile_url") or it.get("public_profile_url") or ""),
        })
    results.sort(key=lambda r: DISTANCE_RANK.get(r["network_distance"], 9))
    if fallback_used:
        for r in results:
            r["fallback_recherche_nom_seul"] = True
    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> \"<nom>\" [--entreprise \"<entreprise>\"] [--max 5]")
        sys.exit(0)
    account_id, name = sys.argv[1], sys.argv[2]
    company = None
    max_results = 5
    if "--entreprise" in sys.argv:
        company = sys.argv[sys.argv.index("--entreprise") + 1]
    if "--max" in sys.argv:
        max_results = int(sys.argv[sys.argv.index("--max") + 1])
    results = find_linkedin_url(account_id, name, company=company, max_results=max_results)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"[+] {len(results)} resultat(s)", file=sys.stderr)
