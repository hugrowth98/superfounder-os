"""Client Unipile - lister les publications (posts) d'une entreprise LinkedIn.
Stdlib uniquement."""
from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_ENV = Path(__file__).resolve().parents[4] / ".env"


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


def _resolve_company_provider_id(account_id: str, name: str) -> str | None:
    """L'endpoint posts exige l'id numerique interne (pas le public_identifier) :
    on le recupere via une recherche entreprise."""
    body = {"api": "classic", "category": "companies", "keywords": name, "limit": 5}
    data = _request("POST", "/api/v1/linkedin/search", params={"account_id": account_id}, body=body)
    items = data.get("items", [])
    return str(items[0]["id"]) if items else None


def list_company_posts(account_id: str, company: str, max_results: int = 50) -> list[dict]:
    """company : id numerique interne connu, ou nom/public_identifier d'entreprise
    (resolution automatique par recherche dans ce dernier cas)."""
    provider_id = company if company.isdigit() else _resolve_company_provider_id(account_id, company)
    if not provider_id:
        raise RuntimeError(f"Entreprise introuvable : {company}")

    all_items, cursor = [], None
    while len(all_items) < max_results:
        params = {"account_id": account_id, "is_company": "true", "limit": min(50, max_results - len(all_items))}
        if cursor:
            params["cursor"] = cursor
        data = _request("GET", f"/api/v1/users/{provider_id}/posts", params=params)
        items = data.get("items", [])
        all_items.extend(items)
        cursor = data.get("cursor")
        if not cursor or not items:
            break
    return all_items[:max_results]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <id_entreprise|nom_entreprise> [--max 50]")
        sys.exit(0)
    account_id, company = sys.argv[1], sys.argv[2]
    max_results = 50
    if "--max" in sys.argv:
        max_results = int(sys.argv[sys.argv.index("--max") + 1])
    posts = list_company_posts(account_id, company, max_results=max_results)
    print(json.dumps(posts, indent=2, ensure_ascii=False))
    print(f"[+] {len(posts)} publication(s)", file=sys.stderr)
