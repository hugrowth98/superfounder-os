"""Client Unipile - profil d'une entreprise LinkedIn. Stdlib uniquement."""
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


def _resolve_company_identifier(account_id: str, name: str) -> str | None:
    """Cherche l'entreprise par nom et retourne son public_identifier (le plus fiable
    pour l'appel profil, l'id numerique interne fonctionne aussi si fourni)."""
    body = {"api": "classic", "category": "companies", "keywords": name, "limit": 5}
    data = _request("POST", "/api/v1/linkedin/search", params={"account_id": account_id}, body=body)
    items = data.get("items", [])
    if not items:
        return None
    top = items[0]
    url = top.get("profile_url", "")
    slug = url.rstrip("/").split("/")[-1] if url else None
    return slug or str(top.get("id"))


def get_company_profile(account_id: str, identifier: str) -> dict:
    """identifier : public_identifier LinkedIn (slug), id numerique interne, ou un nom
    d'entreprise en langage naturel (dans ce cas, resolution automatique via recherche)."""
    try:
        return _request("GET", f"/api/v1/linkedin/company/{identifier}", params={"account_id": account_id})
    except RuntimeError as e:
        if "404" not in str(e):
            raise
        resolved = _resolve_company_identifier(account_id, identifier)
        if not resolved:
            raise RuntimeError(f"Entreprise introuvable, meme via recherche : {identifier}") from e
        return _request("GET", f"/api/v1/linkedin/company/{resolved}", params={"account_id": account_id})


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <public_identifier|id|nom_entreprise>")
        sys.exit(0)
    account_id, identifier = sys.argv[1], sys.argv[2]
    profile = get_company_profile(account_id, identifier)
    print(json.dumps(profile, indent=2, ensure_ascii=False))
