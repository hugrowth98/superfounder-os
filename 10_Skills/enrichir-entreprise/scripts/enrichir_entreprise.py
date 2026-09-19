"""enrichir_entreprise : complete un CSV d'entreprises (firmographique, site, LinkedIn, effectif, secteur).

Sources (--source) :
  unipile     page entreprise LinkedIn via le compte de l'utilisateur (GET /api/v1/linkedin/company/{id}) ; par defaut
  crustdata   GET /screener/company?company_domain= (1 credit cache / 4 temps reel) ; ajoute nb_offres_emploi, CA estime
  apify       harvestapi/linkedin-company (0,004 $ par entreprise) : par URL LinkedIn, ou par nom si l'URL manque
  Les sources se cumulent : --source unipile,crustdata enchaine les deux (chacune ne remplit que ce qui est vide).

Usage :
  python3 enrichir_entreprise.py --in liste.csv [--source unipile,crustdata] [--max 100] [--force] [--dry-run]
Entree : CSV avec `entreprise` et si possible `linkedin_entreprise_url` ou `domaine`.
Sortie : Listes-prospection/enrichir-entreprise_<sujet>_<date>.csv (l'entree n'est jamais ecrasee).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (Crustdata, Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, domaine,  # noqa: E402
                        ecrire_csv, lire_csv, lire_outils, norm_linkedin_url, norm_texte, slug_linkedin, sujet_depuis_fichier)
from apify_run import lancer, prix  # noqa: E402

VERBE = "enrichir-entreprise"


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


def _tranche(d: dict) -> str:
    t = d.get("employeeCountRange") or d.get("employee_count_range") or d.get("staff_count_range") or {}
    if isinstance(t, dict):
        return f"{t.get('start', t.get('min', ''))}-{t.get('end', t.get('max', ''))}".strip("-")
    return str(t) if t else ""


def fusion(ligne: dict, d: dict, source: str) -> None:
    industries = d.get("industries") if isinstance(d.get("industries"), list) else []
    secteur = _g(d, "industry", "linkedin_industry") or (industries[0].get("name", "") if industries and isinstance(industries[0], dict) else (industries[0] if industries else ""))
    locs = d.get("locations") if isinstance(d.get("locations"), list) else []
    siege = next((l for l in locs if isinstance(l, dict) and l.get("headquarter")), locs[0] if locs and isinstance(locs[0], dict) else {})
    maj = {
        "entreprise": _g(d, "name", "company_name"), "domaine": domaine(_g(d, "website", "company_website_domain", "company_website")),
        "linkedin_entreprise_url": norm_linkedin_url(_g(d, "linkedinUrl", "linkedin_profile_url", "linkedin_url", "public_url")),
        "ville": _g(siege, "parsed.city", "city") or _g(d, "headquarters.city", "hq_city"),
        "pays": _g(siege, "parsed.country", "country") or _g(d, "headquarters.country", "hq_country"),
        "secteur": secteur, "effectif": _g(d, "employeeCount", "employee_count", "linkedin_headcount", "headcount") or _tranche(d),
        "effectif_tranche": _tranche(d), "site_web": _g(d, "website", "company_website"),
        "abonnes": _g(d, "followerCount", "followers_count", "follower_count", "linkedin_followers"),
        "annee_creation": _g(d, "foundedOn.year", "founded_year", "year_founded"), "type": _g(d, "companyType", "type", "company_type"),
        "specialites": " | ".join(d.get("specialities") or d.get("specialties") or [])[:300],
        "telephone_entreprise": _g(d, "phone.number", "phone"), "tagline": _g(d, "tagline"),
        "description": (_g(d, "description", "linkedin_company_description") or "")[:400],
        "nb_offres_emploi": _g(d, "job_postings_count", "open_jobs", "job_openings"),
        "chiffre_affaires_estime": _g(d, "estimated_revenue_lower_bound_usd", "revenue", "estimated_revenue"),
        "stade_financement": _g(d, "last_funding_round_type", "funding_stage", "last_funding_round"),
        "unipile_id": _g(d, "id") if source == "unipile" else "",
    }
    for k, v in maj.items():
        if v and not (ligne.get(k) or "").strip():
            ligne[k] = v
    ligne["date_enrichissement_entreprise"] = aujourd_hui()
    ligne["source"] = (ligne.get("source") or "") + (f"+{source}" if ligne.get("source") else source)


def cibles(lignes: list[dict], forcer: bool, maximum: int | None) -> list[int]:
    idx = [i for i, l in enumerate(lignes) if (forcer or not l.get("date_enrichissement_entreprise"))
           and (l.get("entreprise") or l.get("linkedin_entreprise_url") or l.get("domaine"))]
    return idx[:maximum] if maximum else idx


POSTS = False


def via_unipile(lignes, idx, dry_run, pause):
    if dry_run:
        bandeau_dry_run("Unipile GET /api/v1/linkedin/company/{id}", [f"{len(idx)} entreprise(s), une requete par entreprise (recherche par nom si pas d'URL)",
                                                                      "cout : abonnement Unipile"])
        return 0
    u, ok = Unipile(), 0
    for n, i in enumerate(idx, 1):
        l = lignes[i]
        ident = slug_linkedin(l.get("linkedin_entreprise_url")) or l.get("entreprise")
        try:
            fusion(l, u.entreprise(ident), "unipile")
            if POSTS:
                l["posts_recents"] = " || ".join(u.posts(slug_linkedin(l.get("linkedin_entreprise_url")) or l.get("unipile_id") or ident, entreprise=True))
            ok += 1
        except Exception as e:
            l["erreur_enrichissement_entreprise"] = str(e)[:120]
        if n % 10 == 0:
            afficher(f"  [unipile] {n}/{len(idx)}")
        time.sleep(pause)
    return ok


def via_crustdata(lignes, idx, dry_run, pause):
    doms = [(i, domaine(lignes[i].get("domaine") or lignes[i].get("site_web"))) for i in idx]
    doms = [(i, d) for i, d in doms if d]
    if dry_run:
        bandeau_dry_run("Crustdata GET /screener/company?company_domain=", [f"{len(doms)} entreprise(s) avec un domaine ({len(idx) - len(doms)} sans domaine, ignorees)",
                                                                             f"cout : 1 credit par entreprise en cache (4 en temps reel), soit environ {len(doms)} credits"])
        return 0
    c, ok = Crustdata(), 0
    afficher(f"  [crustdata] solde : {c.credits()} credits")
    for n, (i, d) in enumerate(doms, 1):
        try:
            res = c.entreprise(d)
            if res:
                fusion(lignes[i], res, "crustdata")
                ok += 1
        except Exception as e:
            lignes[i]["erreur_enrichissement_entreprise"] = str(e)[:120]
        time.sleep(pause)
    return ok


def via_apify(lignes, idx, dry_run, pause):
    urls = {i: norm_linkedin_url(lignes[i].get("linkedin_entreprise_url")) for i in idx}
    par_url = [u for u in urls.values() if u]
    par_nom = [lignes[i].get("entreprise") for i, u in urls.items() if not u and lignes[i].get("entreprise")]
    entree = {}
    if par_url:
        entree["companies"] = sorted(set(par_url))
    if par_nom:
        entree["searches"] = sorted(set(par_nom))
    if not entree:
        arret("apify : aucune URL LinkedIn ni nom d'entreprise dans les lignes a traiter")
    actor = "harvestapi/linkedin-company"
    items, _ = lancer(actor, entree, label="linkedin-company", dry_run=dry_run, estimation=prix(actor, len(par_url) + len(par_nom)))
    if dry_run:
        return 0
    by_url = {norm_linkedin_url(_g(it, "linkedinUrl")): it for it in items}
    by_q = {norm_texte(_g(it, "originalQuery.search")): it for it in items if _g(it, "originalQuery.search")}
    ok = 0
    for i in idx:
        it = by_url.get(urls[i]) or by_q.get(norm_texte(lignes[i].get("entreprise")))
        if it:
            fusion(lignes[i], it, actor)
            ok += 1
        else:
            lignes[i]["erreur_enrichissement_entreprise"] = "non trouvee par l'actor"
    return ok


SOURCES = {"unipile": via_unipile, "crustdata": via_crustdata, "apify": via_apify}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--source", help="unipile, crustdata, apify, ou plusieurs separes par des virgules (defaut selon OUTILS.md)")
    ap.add_argument("--max", type=int)
    ap.add_argument("--pause", type=float, default=1.0)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--techno", action="store_true", help="enchainer la detection de la stack technique (scripts/detecter_techno.py)")
    ap.add_argument("--pubs", action="store_true", help="enchainer les pubs actives Meta et LinkedIn (scripts/scraper_pubs.py)")
    ap.add_argument("--sans-base", action="store_true", help="sauter l'enrichissement de base, ne faire que --techno et/ou --pubs")
    ap.add_argument("--cherche", help="avec --techno : technos a reperer, separees par des virgules")
    ap.add_argument("--diff", action="store_true", help="avec --techno : comparer au dernier run")
    ap.add_argument("--plateforme", default="les-deux", help="avec --pubs : meta, linkedin ou les-deux")
    ap.add_argument("--techno-source", choices=["apify", "predictleads"], default="apify", help="avec --techno : apify (photo + diff) ou predictleads (detections datees)")
    ap.add_argument("--recentes-jours", type=int, help="avec --techno-source predictleads : une ligne techno_ajout par techno vue depuis N jours")
    ap.add_argument("--posts", action="store_true", help="ajouter posts_recents (5 derniers posts de la page, Unipile)")
    a = ap.parse_args()

    global POSTS
    POSTS = a.posts
    if a.sans_base and not (a.techno or a.pubs):
        arret("--sans-base n'a de sens qu'avec --techno et/ou --pubs")
    if a.sans_base:
        _options(a, Path(a.entree))
        return
    sources = [s.strip() for s in (a.source or "").split(",") if s.strip()]
    if not sources:
        sources = ["unipile"] if lire_outils().get("priorite", "apify") != "api" else ["unipile", "crustdata"]
        afficher(f"  [source] {', '.join(sources)} (d'apres OUTILS.md)")
    for s in sources:
        if s not in SOURCES:
            arret(f"source inconnue : {s} (unipile, crustdata, apify)")
    lignes = lire_csv(a.entree)
    idx = cibles(lignes, a.force, a.max)
    afficher(f"  [cibles] {len(idx)} entreprise(s) a enrichir sur {len(lignes)}")
    for s in sources:
        ok = SOURCES[s](lignes, idx, a.dry_run, a.pause)
        if not a.dry_run:
            afficher(f"  [{s}] {ok} entreprise(s) enrichie(s)")
    if a.dry_run:
        _options(a, Path(a.entree))
        return
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet))
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} lignes -> {sortie}")
    _options(a, sortie)


def _options(a, csv_source: Path) -> None:
    """Enchaine les options --techno et --pubs sur le CSV enrichi (ou l'entree en dry-run / --sans-base)."""
    import subprocess
    ici = Path(__file__).resolve().parent
    if a.techno:
        cmd = [sys.executable, str(ici / "detecter_techno.py"), "--in", str(csv_source), "--sujet", a.sujet or sujet_depuis_fichier(csv_source)]
        if a.cherche:
            cmd += ["--cherche", a.cherche]
        if a.diff:
            cmd.append("--diff")
        if a.techno_source != "apify":
            cmd += ["--source", a.techno_source]
        if a.recentes_jours:
            cmd += ["--recentes-jours", str(a.recentes_jours)]
        if a.dry_run:
            cmd.append("--dry-run")
        afficher("  [option techno] " + " ".join(cmd[2:]))
        subprocess.run(cmd, check=False)
    if a.pubs:
        cmd = [sys.executable, str(ici / "scraper_pubs.py"), "--in", str(csv_source), "--plateforme", a.plateforme, "--sujet", a.sujet or sujet_depuis_fichier(csv_source)]
        if a.dry_run:
            cmd.append("--dry-run")
        afficher("  [option pubs] " + " ".join(cmd[2:]))
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
