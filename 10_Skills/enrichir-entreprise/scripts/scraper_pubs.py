"""scraper_pubs : les publicites actives d'une entreprise (concurrent, prospect) dans la bibliotheque de pubs Meta
et dans celle de LinkedIn, une ligne par pub : date de debut, texte, lien.

Plateformes (--plateforme) :
  meta       Apify curious_coder/facebook-ads-library-scraper (0,00075 $ par pub) : recherche par nom, ou URL de page Facebook
  linkedin   Apify s-r/linkedin-ads-library (0,005 $ par pub) : recherche par nom d'annonceur, filtre pays et periode
  les-deux   les deux a la suite (defaut)

Usage :
  python3 scraper_pubs.py --entreprise "Acme" --pays FR --max 50
  python3 scraper_pubs.py --entreprises "Acme,Beta,Gamma" --plateforme meta --max 30 --dry-run
  python3 scraper_pubs.py --in liste.csv --plateforme linkedin --periode last-30-days     (colonne entreprise, et facebook_url si connue)
Meta : seules les pubs actives sont demandees. LinkedIn ne dit pas si une pub tourne encore : --periode (last-30-days par
defaut) sert de filtre "en cours". Sortie : Listes-prospection/scraper-pubs_<sujet>_<date>.csv
"""
from __future__ import annotations

import argparse
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import afficher, arret, aujourd_hui, chemin_sortie, ecrire_csv, fraicheur, lire_csv, norm_texte, sujet_depuis_fichier  # noqa: E402
from apify_run import lancer, prix  # noqa: E402

VERBE = "scraper-pubs"
ACTOR_META = "curious_coder/facebook-ads-library-scraper"
ACTOR_LINKEDIN = "s-r/linkedin-ads-library"


def _g(d, *cles, defaut=""):
    for c in cles:
        cur = d
        for part in c.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur not in (None, "", [], {}):
            return cur
    return defaut


def _liste(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _date_unix(v) -> str:
    try:
        return datetime.utcfromtimestamp(int(v)).date().isoformat()
    except (TypeError, ValueError, OSError):
        return str(v or "")[:10]


def cibles_depuis(a) -> list[dict]:
    cibles = []
    if a.entree:
        for l in lire_csv(a.entree):
            if l.get("entreprise"):
                cibles.append({"entreprise": l["entreprise"], "facebook_url": l.get("facebook_url", ""), "src": l})
    for n in _liste(a.entreprises) + ([a.entreprise] if a.entreprise else []):
        cibles.append({"entreprise": n, "facebook_url": "", "src": {}})
    if a.page_url:
        cibles.append({"entreprise": a.entreprise or a.page_url, "facebook_url": a.page_url, "src": {}})
    if not cibles:
        arret("donnez --entreprise, --entreprises, --in <csv> ou --page-url")
    return cibles


def meta(cibles: list[dict], a) -> list[dict]:
    urls = []
    for c in cibles:
        if c["facebook_url"]:
            urls.append({"url": c["facebook_url"]})
        else:
            q = urllib.parse.quote(c["entreprise"])
            urls.append({"url": f"https://www.facebook.com/ads/library/?active_status={'all' if a.toutes else 'active'}&ad_type=all&country={a.pays}&q={q}&search_type=keyword_unordered&media_type=all"})
    entree = {"urls": urls, "limitPerSource": a.max, "scrapePageAds.activeStatus": "all" if a.toutes else "active",
              "scrapePageAds.countryCode": a.pays, "scrapePageAds.sortBy": "most_recent", "scrapeAdDetails": False}
    items, _ = lancer(ACTOR_META, entree, label=f"meta ads ({len(urls)} cibles)", dry_run=a.dry_run, estimation=prix(ACTOR_META, a.max * len(urls)))
    lignes = []
    for it in items:
        snap = it.get("snapshot") or {}
        texte = _g(snap, "body.text") or _g(it, "body") or ""
        debut = _g(it, "start_date_formatted") or _date_unix(it.get("start_date"))
        lignes.append({"entreprise": _g(it, "page_name", "snapshot.page_name", "advertiser.ad_library_page_info.page_info.page_name"),
                       "source": ACTOR_META, "date_extraction": aujourd_hui(), "signal_type": "pub_active" if it.get("is_active", True) else "pub_arretee",
                       "signal_date": str(debut)[:10], "signal_detail": f"pub Meta depuis le {str(debut)[:10]} : {texte[:160]}".replace("\n", " "),
                       "plateforme": "meta", "active": "oui" if it.get("is_active", True) else "non",
                       "date_debut": str(debut)[:10], "date_fin": _g(it, "end_date_formatted") or (_date_unix(it.get("end_date")) if it.get("end_date") else ""),
                       "titre": _g(snap, "title"), "texte": texte.replace("\n", " ")[:1000], "cta": _g(snap, "cta_text"),
                       "lien": _g(snap, "link_url"), "url_pub": _g(it, "ad_library_url", "url"), "format": _g(snap, "display_format"),
                       "canaux": " | ".join(it.get("publisher_platform") or []), "pays": a.pays, "id_pub": _g(it, "ad_archive_id"),
                       "nb_variantes": _g(it, "collation_count"), "page_id": _g(it, "page_id")})
    return lignes


def linkedin(cibles: list[dict], a) -> list[dict]:
    lignes = []
    for n, c in enumerate(cibles, 1):
        entree = {"search": c["entreprise"], "max_ads": a.max, "sort": "NEWEST"}
        if a.pays:
            entree["country"] = a.pays
        if a.periode:
            entree["date_range"] = a.periode
        items, _ = lancer(ACTOR_LINKEDIN, entree, label=f"linkedin ads {n}/{len(cibles)} ({c['entreprise']})", dry_run=a.dry_run,
                          estimation=prix(ACTOR_LINKEDIN, a.max))
        if a.dry_run and n >= 2:
            if len(cibles) > 2:
                afficher(f"  [dry-run] ... {len(cibles) - 2} autre(s) entreprise(s)")
            break
        for it in items:
            if _g(it, "result_type") == "total":
                continue
            texte = _g(it, "body_text") or ""
            plage = _g(it, "date_range")
            lignes.append({"entreprise": _g(it, "advertiser_name") or c["entreprise"], "source": ACTOR_LINKEDIN, "date_extraction": aujourd_hui(),
                           "signal_type": "pub_active", "signal_date": str(plage)[:10] if plage and plage[:4].isdigit() else "",
                           "signal_detail": f"pub LinkedIn ({_g(it, 'ad_type')}) {plage} : {(_g(it, 'headline') or texte)[:160]}".replace("\n", " "),
                           "plateforme": "linkedin", "active": "", "date_debut": str(plage), "titre": _g(it, "headline"),
                           "texte": texte.replace("\n", " ")[:1000], "lien": _g(it, "deeplink"), "url_pub": _g(it, "deeplink", "source_url"),
                           "format": _g(it, "creative_type", "ad_type"), "pays": _g(it, "country") or a.pays, "id_pub": _g(it, "ad_id"),
                           "porte_parole": " ".join(x for x in [_g(it, "person_name"), _g(it, "person_title")] if x),
                           "total_pubs_annonceur": _g(it, "total_ads_in_search", "total_ads")})
    return lignes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plateforme", choices=["meta", "linkedin", "les-deux"], default="les-deux")
    ap.add_argument("--entreprise", help="nom d'une entreprise ou d'une page")
    ap.add_argument("--entreprises", help="plusieurs noms separes par des virgules")
    ap.add_argument("--in", dest="entree", help="CSV avec entreprise (et facebook_url)")
    ap.add_argument("--page-url", help="meta : URL d'une page Facebook (https://www.facebook.com/<page>)")
    ap.add_argument("--pays", default="FR", help="code ISO pour les deux bibliotheques (ALL pour Meta monde)")
    ap.add_argument("--periode", default="last-30-days", choices=["last-30-days", "current-month", "current-year", "last-year", ""], help="linkedin")
    ap.add_argument("--toutes", action="store_true", help="meta : pubs actives et arretees")
    ap.add_argument("--max", type=int, default=50, help="pubs max par entreprise et par plateforme")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cibles = cibles_depuis(a)
    lignes = []
    if a.plateforme in ("meta", "les-deux"):
        lignes += meta(cibles, a)
    if a.plateforme in ("linkedin", "les-deux"):
        lignes += linkedin(cibles, a)
    if a.dry_run:
        return
    for l in lignes:
        l["fraicheur"] = fraicheur(l.get("signal_date"))
    lignes.sort(key=lambda l: (norm_texte(l.get("entreprise")), l.get("plateforme", ""), l.get("signal_date", "")), reverse=False)
    sujet = a.sujet or (sujet_depuis_fichier(a.entree) if a.entree else (cibles[0]["entreprise"] if len(cibles) == 1 else "concurrents"))
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(lignes, sortie)
    par_ent: dict = {}
    for l in lignes:
        k = f"{l.get('entreprise')} ({l.get('plateforme')})"
        par_ent[k] = par_ent.get(k, 0) + 1
    for k, v in sorted(par_ent.items()):
        afficher(f"  {k} : {v} pub(s)")
    afficher(f"{len(lignes)} pub(s) -> {sortie}")


if __name__ == "__main__":
    main()
