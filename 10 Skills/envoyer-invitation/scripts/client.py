"""Envoi d'invitations LinkedIn (Unipile) avec garde-fou 30/jour en fichier local. Stdlib uniquement."""
from __future__ import annotations
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"
COUNTER_FILE = Path(__file__).parent / "compteur.json"
LIMITE_JOUR = 30


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


def send_invitation(account_id: str, provider_id: str, message: str = None) -> dict:
    if _today_count() >= LIMITE_JOUR:
        raise RuntimeError(
            f"Limite de {LIMITE_JOUR} invitations/jour atteinte. Reessayer demain "
            "(garde-fou anti-restriction LinkedIn, non contournable)."
        )
    url = f"{dsn()}/api/v1/users/invite"
    body = {"account_id": account_id, "provider_id": provider_id}
    if message:
        body["message"] = message
    data = json.dumps(body).encode()
    headers = {"X-API-KEY": api_key(), "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            result = json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur POST /api/v1/users/invite : {e.read().decode()}")
    _increment_counter()
    return result


def send_batch(account_id: str, contacts: list[dict], delay_s: float = 3.0) -> dict:
    """contacts : liste de dicts {provider_id, message?}. S'arrete a la limite du jour."""
    sent, skipped, errors = [], [], []
    for c in contacts:
        if remaining_today() <= 0:
            skipped.append({"provider_id": c["provider_id"], "raison": "limite quotidienne atteinte"})
            continue
        try:
            send_invitation(account_id, c["provider_id"], c.get("message"))
            sent.append(c["provider_id"])
            time.sleep(delay_s)
        except Exception as e:
            errors.append({"provider_id": c["provider_id"], "erreur": str(e)})
    return {"sent": sent, "skipped": skipped, "errors": errors, "remaining_today": remaining_today()}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or sys.argv[1] == "remaining":
        print(f"Invitations restantes aujourd'hui : {remaining_today()}/{LIMITE_JOUR}")
        sys.exit(0)
    print("Usage : python client.py remaining")
    print("Pour l'envoi en batch, importer send_batch() depuis un script appelant avec la liste de contacts.")
