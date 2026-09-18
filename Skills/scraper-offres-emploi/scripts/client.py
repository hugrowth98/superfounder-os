"""Detection de signal recrutement (Crustdata) - baseline stockee en JSON local, pas de DB."""
from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://api.crustdata.com"
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"
BASELINE_FILE = Path(__file__).parent / "baseline.json"


def load_api_key() -> str:
    key = os.environ.get("CRUSTDATA_API_KEY")
    if key:
        return key
    if ROOT_ENV.exists():
        for line in ROOT_ENV.read_text().splitlines():
            if line.strip().startswith("CRUSTDATA_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(f"CRUSTDATA_API_KEY introuvable (env ou {ROOT_ENV})")


def _get(path: str) -> dict:
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Token {load_api_key()}"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur GET {path} : {e.read().decode()}")


def enrich_company(domain: str) -> dict:
    res = _get(f"/screener/company?company_domain={domain}")
    return (res[0] if isinstance(res, list) and res else res) or {}


def _load_baselines() -> dict:
    if BASELINE_FILE.exists():
        return json.loads(BASELINE_FILE.read_text())
    return {}


def _save_baselines(data: dict) -> None:
    BASELINE_FILE.write_text(json.dumps(data, indent=2))


def check_hiring_signal(domain: str, threshold: int = 5) -> dict:
    company = enrich_company(domain)
    current = company.get("job_postings_count") or company.get("open_jobs") or 0

    baselines = _load_baselines()
    previous = baselines.get(domain, 0)
    delta = current - previous
    changed = delta >= threshold

    baselines[domain] = current
    _save_baselines(baselines)

    return {
        "domain": domain,
        "previous_count": previous,
        "current_count": current,
        "delta": delta,
        "signal": changed,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage : python client.py <domaine> [--threshold 5]")
        sys.exit(0)
    domain = sys.argv[1]
    threshold = 5
    if "--threshold" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--threshold") + 1])
    result = check_hiring_signal(domain, threshold)
    print(json.dumps(result, indent=2))
