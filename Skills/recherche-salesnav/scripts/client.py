"""Client Unipile - recherche LinkedIn / Sales Navigator. Stdlib uniquement."""
from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


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


def search_linkedin(account_id: str, api: str = "sales_navigator", category: str = "people",
                     url: str = None, keywords: str = None, max_results: int = 100) -> list[dict]:
    """api : 'sales_navigator' | 'classic' | 'recruiter'. category : 'people' | 'companies'.
    Fournir soit `url` (URL Sales Nav copiee du navigateur), soit `keywords` (recherche classique)."""
    all_items = []
    cursor = None
    hard_cap = max_results + 50
    iterations = 0
    page_cap = 50 if api == "classic" else 100
    while len(all_items) < max_results and iterations < hard_cap:
        iterations += 1
        body = {"api": api, "category": category, "limit": min(page_cap, max_results - len(all_items))}
        if url:
            body["url"] = url
        if keywords:
            body["keywords"] = keywords
        if cursor:
            body["cursor"] = cursor
        data = _request("POST", "/api/v1/linkedin/search", params={"account_id": account_id}, body=body)
        items = data.get("items", [])
        all_items.extend(items)
        cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
        if not cursor or not items:
            break
    return all_items[:max_results]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <url_sales_nav_ou_mot_cle> "
              "[--api sales_navigator|classic|recruiter] [--category people|companies] [--max 100]")
        sys.exit(0)
    account_id, target = sys.argv[1], sys.argv[2]
    api = "sales_navigator"
    category = "people"
    max_results = 100
    if "--api" in sys.argv:
        api = sys.argv[sys.argv.index("--api") + 1]
    if "--category" in sys.argv:
        category = sys.argv[sys.argv.index("--category") + 1]
    if "--max" in sys.argv:
        max_results = int(sys.argv[sys.argv.index("--max") + 1])
    is_url = target.startswith("http")
    results = search_linkedin(account_id, api=api, category=category,
                               url=target if is_url else None,
                               keywords=None if is_url else target,
                               max_results=max_results)
    print(json.dumps(results, indent=2))
    print(f"[+] {len(results)} resultats", file=sys.stderr)
