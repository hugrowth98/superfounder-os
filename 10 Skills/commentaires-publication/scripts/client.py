"""Client Unipile - lister les commentaires (et leurs reponses) d'une publication
LinkedIn. Stdlib uniquement."""
from __future__ import annotations
import re
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


def normalize_post_id(post_url_or_id: str) -> str:
    """Accepte une URL de post LinkedIn ou directement un social_id (urn:li:...)."""
    if post_url_or_id.startswith("urn:li:"):
        return post_url_or_id
    m = re.search(r"(?:activity|share)[/:-](\d+)", post_url_or_id)
    if m:
        return f"urn:li:activity:{m.group(1)}"
    raise ValueError(f"Impossible d'extraire un social_id depuis : {post_url_or_id}")


def _list_page(account_id: str, post_id: str, comment_id: str | None, max_pages: int) -> list[dict]:
    items, cursor, pages = [], None, 0
    while pages < max_pages:
        pages += 1
        params = {"account_id": account_id, "limit": 100}
        if cursor:
            params["cursor"] = cursor
        if comment_id:
            params["comment_id"] = comment_id
        data = _request("GET", f"/api/v1/posts/{post_id}/comments", params=params)
        page_items = data.get("items", [])
        items.extend(page_items)
        cursor = data.get("cursor")
        if not cursor or not page_items:
            break
    return items


def list_comments(account_id: str, post_id: str, include_replies: bool = True, max_pages: int = 10) -> list[dict]:
    """Retourne les commentaires de premier niveau. Si include_replies=True, les
    reponses a chaque commentaire (reply_counter > 0) sont recuperees et ajoutees
    dans une cle 'replies' sur le commentaire parent."""
    comments = _list_page(account_id, post_id, comment_id=None, max_pages=max_pages)
    if include_replies:
        for c in comments:
            if c.get("reply_counter", 0) > 0:
                c["replies"] = _list_page(account_id, post_id, comment_id=c["id"], max_pages=max_pages)
    return comments


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage : python client.py <account_id> <url_post_ou_social_id> [--no-replies]")
        sys.exit(0)
    account_id, raw_post = sys.argv[1], sys.argv[2]
    post_id = normalize_post_id(raw_post)
    include_replies = "--no-replies" not in sys.argv
    comments = list_comments(account_id, post_id, include_replies=include_replies)
    print(json.dumps(comments, indent=2, ensure_ascii=False))
    total_replies = sum(len(c.get("replies", [])) for c in comments)
    print(f"[+] {len(comments)} commentaire(s) de premier niveau, {total_replies} reponse(s)", file=sys.stderr)
