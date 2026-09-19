"""Client Apify commun : lancer un actor, attendre la fin, lire le dataset. API REST, `requests` uniquement.

Importe par tous les scripts Apify du module GTM :

    from apify_run import lancer, verifier_actor, prix, PRIX

Usage direct (runner generique) :
    python3 apify_run.py <utilisateur/actor> --input entree.json [--out sortie.json] [--timeout 900] [--dry-run]
    python3 apify_run.py --verifier <utilisateur/actor>        (existence + prix, gratuit)
    python3 apify_run.py --moi                                  (teste APIFY_TOKEN, gratuit)

Cle : APIFY_TOKEN dans le .env a la racine du module GTM.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gtm_common import afficher, arret, bandeau_dry_run, env, http  # noqa: E402

API = "https://api.apify.com/v2"

# Prix verifies le 2026-09-19 sur le Store (palier BRONZE, en dollars). Sert aux estimations
# affichees avant tout run. (libelle, prix unitaire, frais de depart par run)
PRIX = {
    "compass/crawler-google-places": ("par lieu (+0,001 $ par filtre applique)", 0.003, 0.0),
    "harvestapi/linkedin-company-search": ("par entreprise (short 0,002 / full 0,004)", 0.004, 0.001),
    "code_crafter/leads-finder": ("par lead", 0.002, 0.02),
    "curious_coder/linkedin-sales-navigator-search-scraper": ("par resultat", 0.005, 0.0005),
    "harvestapi/linkedin-profile-search": ("par page de 25 profils (mode Short)", 0.10, 0.0),
    "harvestapi/linkedin-company-employees": ("par profil (Short) ; 0,02 $ de depart par requete", 0.003, 0.02),
    "harvestapi/linkedin-profile-scraper": ("par profil", 0.004, 0.0),
    "harvestapi/linkedin-company": ("par entreprise", 0.004, 0.0),
    "signalbase/signalbase-api": ("par resultat", 0.04, 0.0),
    "tagadanar/linkedin-jobs-scraper": ("par offre (+0,0018 $ si details)", 0.0018, 0.001),
    "borderline/indeed-scraper": ("par offre", 0.005, 0.0),
    "harvestapi/linkedin-post-comments": ("par commentaire", 0.002, 0.0),
    "harvestapi/linkedin-post-reactions": ("par reaction", 0.002, 0.0),
    "scrapemint/website-tech-stack-detector": ("par domaine avec au moins une detection", 0.01, 0.0),
    "curious_coder/facebook-ads-library-scraper": ("par pub", 0.00075, 0.0),
    "s-r/linkedin-ads-library": ("par pub", 0.005, 0.0),
}


def token() -> str:
    return env("APIFY_TOKEN", aide="Token sur https://console.apify.com/settings/integrations")


def actor_path(actor: str) -> str:
    return actor.replace("/", "~")


def prix(actor: str, n: int) -> str:
    """Phrase d'estimation pour n resultats."""
    lib, unit, depart = PRIX.get(actor, ("par resultat (prix non verifie)", 0.0, 0.0))
    return f"{n} x {unit:.4f} $ {lib} + {depart:.3f} $ = environ {n * unit + depart:.2f} $"


def _req(methode: str, url: str, body=None, params=None):
    params = dict(params or {})
    params["token"] = token()
    st, corps = http(methode, url, params=params, json_body=body, timeout=120)
    if st == 402:
        arret("Apify : credit epuise (HTTP 402). Rechargez le compte sur console.apify.com.")
    if st >= 400:
        raise RuntimeError(f"Apify HTTP {st} sur {url.split('?')[0]} : {str(corps)[:400]}")
    return corps


def moi() -> dict:
    """Teste le token (gratuit)."""
    return _req("GET", f"{API}/users/me").get("data", {})


def verifier_actor(actor: str) -> dict:
    """Existence de l'actor (gratuit). Renvoie {name, username, title, pricing}."""
    d = _req("GET", f"{API}/acts/{actor_path(actor)}").get("data", {})
    return {"nom": f"{d.get('username')}/{d.get('name')}", "titre": d.get("title"),
            "modele_prix": (d.get("pricingInfos") or [{}])[-1].get("pricingModel") if d.get("pricingInfos") else None}


def dataset_items(dataset_id: str, limite: int | None = None) -> list[dict]:
    items, offset, page = [], 0, 1000
    while True:
        lot = _req("GET", f"{API}/datasets/{dataset_id}/items",
                   params={"clean": "true", "format": "json", "limit": page, "offset": offset})
        items.extend(lot)
        if len(lot) < page or (limite and len(items) >= limite):
            break
        offset += page
    return items[:limite] if limite else items


def lancer(actor: str, entree: dict, timeout_s: int = 900, poll_s: int = 5, memoire_mb: int | None = None,
           label: str = "", dry_run: bool = False, estimation: str = "") -> tuple[list[dict], dict]:
    """Lance l'actor, attend la fin, renvoie (items du dataset, infos du run).
    En dry-run : affiche l'input et l'estimation, ne lance rien, renvoie ([], {})."""
    if dry_run:
        bandeau_dry_run(f"actor {actor}" + (f" ({label})" if label else ""),
                        [f"input : {json.dumps(entree, ensure_ascii=False)[:1500]}",
                         f"cout estime : {estimation or 'voir PRIX dans apify_run.py'}"])
        return [], {}
    params = {"timeout": timeout_s}
    if memoire_mb:
        params["memory"] = memoire_mb
    run = _req("POST", f"{API}/acts/{actor_path(actor)}/runs", body=entree, params=params)["data"]
    run_id, dataset_id = run["id"], run["defaultDatasetId"]
    afficher(f"  [apify] {label or actor} : run {run_id} lance (https://console.apify.com/actors/runs/{run_id})")
    t0 = time.time()
    statut = run.get("status")
    while statut not in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
        time.sleep(poll_s)
        statut = _req("GET", f"{API}/actor-runs/{run_id}")["data"]["status"]
        if time.time() - t0 > timeout_s + 120:
            raise RuntimeError(f"Run {run_id} ne termine pas ({statut})")
    if statut != "SUCCEEDED":
        raise RuntimeError(f"Run {run_id} termine en {statut} : https://console.apify.com/actors/runs/{run_id}")
    items = dataset_items(dataset_id)
    infos = _req("GET", f"{API}/actor-runs/{run_id}")["data"]
    cout = (infos.get("usageTotalUsd") or 0)
    afficher(f"  [apify] {label or actor} : termine en {int(time.time() - t0)} s, {len(items)} items, "
             f"cout facture {cout:.3f} $")
    return items, infos


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("actor", nargs="?", help="utilisateur/actor, ex : harvestapi/linkedin-company")
    ap.add_argument("--input", help="fichier JSON d'input de l'actor")
    ap.add_argument("--out", help="fichier JSON de sortie (items du dataset)")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--dry-run", action="store_true", help="affiche ce qui serait lance, sans appel")
    ap.add_argument("--verifier", metavar="ACTOR", help="verifie qu'un actor existe (gratuit)")
    ap.add_argument("--moi", action="store_true", help="teste le token (gratuit)")
    a = ap.parse_args()

    if a.moi:
        d = moi()
        afficher(f"Token OK : utilisateur {d.get('username')} (plan {(d.get('plan') or {}).get('tier', '?')})")
        return
    if a.verifier:
        afficher(json.dumps(verifier_actor(a.verifier), ensure_ascii=False, indent=2))
        return
    if not a.actor or not a.input:
        ap.error("actor et --input sont requis (ou --verifier / --moi)")
    entree = json.loads(Path(a.input).read_text(encoding="utf-8"))
    items, _ = lancer(a.actor, entree, timeout_s=a.timeout, dry_run=a.dry_run)
    if a.dry_run:
        return
    sortie = Path(a.out) if a.out else Path(a.input).with_suffix(".sortie.json")
    sortie.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    afficher(f"{len(items)} items ecrits dans {sortie}")


if __name__ == "__main__":
    main()
