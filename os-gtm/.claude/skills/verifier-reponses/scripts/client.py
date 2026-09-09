"""Client Unipile - liste des conversations et detection des reponses recues. Stdlib uniquement."""
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


def _get(path: str, params: dict) -> dict:
    qs = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    url = f"{dsn()}{path}?{qs}"
    headers = {"X-API-KEY": api_key(), "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur GET {path} : {e.read().decode()}")


def list_chats(account_id: str, limit: int = 100) -> list[dict]:
    data = _get("/api/v1/chats", {"account_id": account_id, "limit": limit})
    return data.get("items", data if isinstance(data, list) else [])


def get_messages(chat_id: str, limit: int = 50) -> list[dict]:
    data = _get(f"/api/v1/chats/{chat_id}/messages", {"limit": limit})
    return data.get("items", data if isinstance(data, list) else [])


def has_replied(account_id: str, chat_id: str, own_provider_id: str) -> bool:
    """True si le dernier message du chat ne vient pas de nous (donc du prospect)."""
    messages = get_messages(chat_id)
    if not messages:
        return False
    last = messages[-1]
    sender = last.get("sender_id") or last.get("from") or (last.get("sender") or {}).get("id")
    return sender != own_provider_id


def list_repliers(account_id: str, own_provider_id: str) -> list[dict]:
    """Retourne les chats ou le prospect a repondu, avec son dernier message."""
    repliers = []
    for chat in list_chats(account_id):
        chat_id = chat.get("id")
        if not chat_id:
            continue
        messages = get_messages(chat_id)
        if not messages:
            continue
        last = messages[-1]
        sender = last.get("sender_id") or last.get("from") or (last.get("sender") or {}).get("id")
        if sender != own_provider_id:
            repliers.append({
                "chat_id": chat_id,
                "attendee_provider_id": chat.get("attendee_provider_id") or sender,
                "last_message": last.get("text"),
            })
    return repliers


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <own_provider_id>")
        sys.exit(0)
    account_id, own_id = sys.argv[1], sys.argv[2]
    result = list_repliers(account_id, own_id)
    print(json.dumps(result, indent=2))
    print(f"[+] {len(result)} conversation(s) avec reponse", file=sys.stderr)
