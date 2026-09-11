"""Envoi de messages directs LinkedIn (Unipile) avec garde-fou quotidien local. Stdlib uniquement."""
from __future__ import annotations
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

ROOT_ENV = Path(__file__).resolve().parents[4] / ".env"
COUNTER_FILE = Path(__file__).parent / "compteur.json"
LIMITE_JOUR = 100


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


def _today_count() -> int:
    if not COUNTER_FILE.exists():
        return 0
    data = json.loads(COUNTER_FILE.read_text())
    return data.get(str(date.today()), 0)


def _increment_counter() -> None:
    data = json.loads(COUNTER_FILE.read_text()) if COUNTER_FILE.exists() else {}
    key = str(date.today())
    data[key] = data.get(key, 0) + 1
    COUNTER_FILE.write_text(json.dumps(data, indent=2))


def remaining_today() -> int:
    return max(0, LIMITE_JOUR - _today_count())


def send_dm(account_id: str, attendee_provider_id: str, text: str) -> dict:
    if _today_count() >= LIMITE_JOUR:
        raise RuntimeError(f"Limite de {LIMITE_JOUR} DM/jour atteinte. Reessayer demain.")
    url = f"{dsn()}/api/v1/chats"
    body = {"account_id": account_id, "attendees_ids": [attendee_provider_id], "text": text}
    data = json.dumps(body).encode()
    headers = {"X-API-KEY": api_key(), "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            result = json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur POST /api/v1/chats : {e.read().decode()}")
    _increment_counter()
    return result


def send_batch(account_id: str, contacts: list[dict], already_replied_ids: set = None, delay_s: float = 3.0) -> dict:
    """contacts : liste de dicts {provider_id, message}. already_replied_ids : provider_id a
    exclure imperativement (issus de verifier-reponses)."""
    already_replied_ids = already_replied_ids or set()
    sent, skipped, errors = [], [], []
    for c in contacts:
        if c["provider_id"] in already_replied_ids:
            skipped.append({"provider_id": c["provider_id"], "raison": "a deja repondu, jamais de relance"})
            continue
        if remaining_today() <= 0:
            skipped.append({"provider_id": c["provider_id"], "raison": "limite quotidienne atteinte"})
            continue
        try:
            send_dm(account_id, c["provider_id"], c["message"])
            sent.append(c["provider_id"])
            time.sleep(delay_s)
        except Exception as e:
            errors.append({"provider_id": c["provider_id"], "erreur": str(e)})
    return {"sent": sent, "skipped": skipped, "errors": errors, "remaining_today": remaining_today()}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or sys.argv[1] == "remaining":
        print(f"DM restants aujourd'hui : {remaining_today()}/{LIMITE_JOUR}")
        sys.exit(0)
    print("Usage : python client.py remaining")
