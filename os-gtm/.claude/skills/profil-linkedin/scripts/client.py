"""Client Unipile - profil d'un utilisateur LinkedIn (le sien ou celui d'un tiers).
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


def _request(method: str, path: str, params: dict | None = None) -> dict:
    url = f"{dsn()}{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        url = f"{url}?{qs}"
    headers = {"X-API-KEY": api_key(), "Accept": "application/json"}
    req = urllib.request.Request(url, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur {method} {path} : {e.read().decode()}")


def get_profile(account_id: str, identifier: str, full: bool = True) -> dict:
    """identifier : 'me' (compte connecte), un public_identifier (ex: 'jean-dupont'),
    ou un provider_id interne. full=True demande toutes les sections LinkedIn
    (experiences, formations, competences, langues, certifications, recommandations)."""
    params = {"account_id": account_id}
    if full:
        params["linkedin_sections"] = "*"
    return _request("GET", f"/api/v1/users/{identifier}", params=params)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <identifiant|me> [--light]")
        sys.exit(0)
    account_id, identifier = sys.argv[1], sys.argv[2]
    full = "--light" not in sys.argv
    profile = get_profile(account_id, identifier, full=full)
    print(json.dumps(profile, indent=2, ensure_ascii=False))
