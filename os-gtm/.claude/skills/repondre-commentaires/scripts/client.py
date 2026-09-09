"""Reponse a des commentaires LinkedIn (Unipile), pause de 2s entre chaque envoi. Stdlib uniquement."""
from __future__ import annotations
import os
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT_ENV = Path(__file__).resolve().parents[4] / ".env"
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scraper-post" / "scripts"))
import client as post_client  # extract_post_id, list_comments


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


def send_comment_reply(account_id: str, post_id: str, text: str, comment_id: str = None) -> dict:
    url = f"{dsn()}/api/v1/posts/{post_id}/comments"
    body = {"account_id": account_id, "text": text}
    if comment_id:
        body["comment_id"] = comment_id
    data = json.dumps(body).encode()
    headers = {"X-API-KEY": api_key(), "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur POST /api/v1/posts/{post_id}/comments : {e.read().decode()}")


def fetch_unanswered_comments(account_id: str, post_url: str, own_author_id: str) -> list[dict]:
    post_id = post_client.extract_post_id(post_url)
    comments = post_client.list_comments(account_id, post_id)
    return [c for c in comments if c.get("author_id") != own_author_id and not c.get("has_replied")]


def send_replies(account_id: str, post_url: str, replies: list[dict], delay_s: float = 2.0) -> dict:
    """replies : liste de dicts {comment_id, text}."""
    post_id = post_client.extract_post_id(post_url)
    sent, errors = [], []
    for r in replies:
        try:
            send_comment_reply(account_id, post_id, r["text"], r.get("comment_id"))
            sent.append(r["comment_id"])
            time.sleep(delay_s)
        except Exception as e:
            errors.append({"comment_id": r.get("comment_id"), "erreur": str(e)})
    return {"sent": sent, "errors": errors}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <url_du_post> [--own-author-id <id>]")
        sys.exit(0)
    account_id, post_url = sys.argv[1], sys.argv[2]
    own_author_id = None
    if "--own-author-id" in sys.argv:
        own_author_id = sys.argv[sys.argv.index("--own-author-id") + 1]
    unanswered = fetch_unanswered_comments(account_id, post_url, own_author_id)
    print(json.dumps(unanswered, indent=2))
    print(f"[+] {len(unanswered)} commentaire(s) sans reponse", file=sys.stderr)
