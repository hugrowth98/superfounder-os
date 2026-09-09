"""Export d'une recherche Sales Navigator ou LinkedIn classique en CSV. Stdlib uniquement."""
from __future__ import annotations
import csv
import re
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "recherche-salesnav" / "scripts"))
import client as search_client

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]+", flags=re.UNICODE
)


def normalize_person(item: dict) -> dict:
    name = EMOJI_RE.sub("", item.get("name", "")).strip()
    parts = name.split(" ", 1)
    first_name, last_name = (parts[0], parts[1]) if len(parts) > 1 else (name, "")

    profile_url = item.get("profile_url") or item.get("public_profile_url") or ""
    if not profile_url and item.get("public_identifier"):
        profile_url = f"https://www.linkedin.com/in/{item['public_identifier']}"
    slug_match = re.search(r"/in/([^/?#]+)", profile_url)

    pos = item.get("current_positions") or item.get("current_position") or {}
    if isinstance(pos, list):
        pos = pos[0] if pos else {}

    return {
        "first_name": first_name,
        "last_name": last_name,
        "headline": item.get("headline") or pos.get("role") or pos.get("title"),
        "company": item.get("company") or pos.get("company"),
        "location": item.get("location"),
        "linkedin_url": profile_url,
        "linkedin_slug": slug_match.group(1) if slug_match else None,
        "provider_id": item.get("id") or item.get("provider_id") or item.get("member_urn"),
        "network_distance": item.get("network_distance"),
    }


def normalize_company(item: dict) -> dict:
    return {
        "name": item.get("name") or item.get("company_name"),
        "industry": item.get("industry"),
        "location": item.get("location") or item.get("headquarters"),
        "employee_count": item.get("employee_count"),
        "linkedin_url": item.get("linkedin_url") or item.get("company_url"),
    }


def write_csv(rows: list[dict], out_path: Path) -> None:
    if not rows:
        Path(out_path).write_text("")
        return
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage : python client.py <account_id> <url_ou_mot_cle> <sortie.csv> "
              "[--api sales_navigator|classic|recruiter] [--category people|companies] [--max 100]")
        sys.exit(0)
    account_id, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
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
    results = search_client.search_linkedin(
        account_id, api=api, category=category,
        url=target if is_url else None,
        keywords=None if is_url else target,
        max_results=max_results,
    )
    normalize = normalize_person if category == "people" else normalize_company
    rows = [normalize(r) for r in results]
    write_csv(rows, Path(out))

    raw_path = Path(out).with_suffix(".raw.json")
    raw_path.write_text(json.dumps(results, indent=2))
    print(f"[+] {len(rows)} resultats exportes dans {out} (brut : {raw_path})")
