"""Client Unipile - likers et commentateurs d'un post LinkedIn. Stdlib uniquement."""
from __future__ import annotations
import csv
import os
import re
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


def extract_post_id(url: str) -> str:
    m = re.search(r"(?:activity|share)[/:-](\d+)", url) or re.search(r"urn:li:ugcPost:(\d+)", url)
    if not m:
        raise ValueError(f"Impossible d'extraire l'id du post depuis : {url}")
    return m.group(1)


def list_reactions(account_id: str, post_id: str, max_pages: int = 10) -> list[dict]:
    items, cursor, page = [], None, 0
    while page < max_pages:
        params = {"account_id": account_id, "limit": 100} if cursor is None else {"cursor": cursor}
        data = _get(f"/api/v1/posts/{post_id}/reactions", params)
        page_items = data.get("items", [])
        items.extend(page_items)
        cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
        page += 1
        if not cursor or not page_items:
            break
    return items


def list_comments(account_id: str, post_id: str, max_pages: int = 10) -> list[dict]:
    items, cursor, page = [], None, 0
    while page < max_pages:
        params = {"account_id": account_id, "limit": 100}
        if cursor:
            params["cursor"] = cursor
        data = _get(f"/api/v1/posts/{post_id}/comments", params)
        page_items = data.get("items", [])
        items.extend(page_items)
        cursor = data.get("cursor") or (data.get("paging") or {}).get("cursor")
        page += 1
        if not cursor or not page_items:
            break
    return items


def normalize(item: dict, engagement_type: str) -> dict:
    author = item.get("author") or item.get("member") or item
    return {
        "name": author.get("name"),
        "headline": author.get("headline") or author.get("occupation"),
        "linkedin_url": author.get("profile_url") or author.get("public_profile_url"),
        "provider_id": author.get("id") or author.get("provider_id") or author.get("member_urn"),
        "engagement_type": engagement_type,
        "comment_text": item.get("text") if engagement_type == "comment" else None,
        "comment_id": item.get("id") if engagement_type == "comment" else None,
    }


def scrape_engagers(account_id: str, post_url: str, engagement_types: list[str] = None) -> list[dict]:
    engagement_types = engagement_types or ["reaction", "comment"]
    post_id = extract_post_id(post_url)
    rows_by_url: dict[str, dict] = {}

    if "reaction" in engagement_types:
        for r in list_reactions(account_id, post_id):
            n = normalize(r, "reaction")
            key = n["linkedin_url"] or n["name"]
            rows_by_url[key] = n

    if "comment" in engagement_types:
        for c in list_comments(account_id, post_id):
            n = normalize(c, "comment")
            key = n["linkedin_url"] or n["name"]
            if key in rows_by_url:
                rows_by_url[key]["engagement_type"] = "reaction+comment"
                rows_by_url[key]["comment_text"] = n["comment_text"]
                rows_by_url[key]["comment_id"] = n["comment_id"]
            else:
                rows_by_url[key] = n

    return list(rows_by_url.values())


def write_csv(rows: list[dict], out_path: Path) -> None:
    if not rows:
        Path(out_path).write_text("")
        return
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage : python client.py <account_id> <url_du_post> <sortie.csv> "
              "[--type both|reactions|comments]")
        sys.exit(0)
    account_id, post_url, out = sys.argv[1], sys.argv[2], sys.argv[3]
    type_map = {"both": ["reaction", "comment"], "reactions": ["reaction"], "comments": ["comment"]}
    engagement_types = type_map["both"]
    if "--type" in sys.argv:
        engagement_types = type_map[sys.argv[sys.argv.index("--type") + 1]]
    rows = scrape_engagers(account_id, post_url, engagement_types)
    write_csv(rows, Path(out))
    print(f"[+] {len(rows)} engagers trouves, ecrits dans {out}")
