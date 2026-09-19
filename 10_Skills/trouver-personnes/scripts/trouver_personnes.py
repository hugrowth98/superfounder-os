"""trouver_personnes : des decisionnaires par titre, seniorite, lieu ou entreprise, en CSV normalise.

Sources (--source) :
  profils     Apify harvestapi/linkedin-profile-search : filtres LinkedIn (titres, lieux, taille, entreprises), sans cookies
  employes    Apify harvestapi/linkedin-company-employees : depuis un CSV d'entreprises (colonne linkedin_entreprise_url)
  salesnav    Apify curious_coder/linkedin-sales-navigator-search-scraper : URL de recherche Sales Navigator "leads"
              + cookies LinkedIn du .env (LINKEDIN_LI_AT, LINKEDIN_LI_A, LINKEDIN_USER_AGENT)
  unipile     Unipile : URL Sales Navigator (ou mots-cles) avec le compte LinkedIn de l'utilisateur (secours)
  crustdata   Crustdata /screener/persondb/search/ (priorite api)

Sans --source : profils si OUTILS.md dit priorite apify (employes si --in est fourni), crustdata sinon.

Exemples :
  python3 trouver_personnes.py --source profils --titres "CEO,Fondateur,Directeur Général" --lieu France --taille 11-50,51-200 --max 100
  python3 trouver_personnes.py --source employes --in Listes-prospection/trouver-entreprises_x.csv --titres "DRH,Responsable recrutement" --par-entreprise 2
  python3 trouver_personnes.py --source salesnav --url "https://www.linkedin.com/sales/search/people?..." --max 500
  python3 trouver_personnes.py --source crustdata --titres "Head of Sales,VP Sales" --seniorites "vp,head" --lieu France --max 100
--par-entreprise N garde les N meilleurs contacts par entreprise (ordre des --titres, puis seniorite). --dry-run : input + cout.
Sortie : Listes-prospection/trouver-personnes_<sujet>_<date>.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (Crustdata, Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, domaine,  # noqa: E402
                        ecrire_csv, env, lire_csv, lire_outils, norm_linkedin_url, norm_texte, seniorite_depuis_titre)
from apify_run import lancer, prix  # noqa: E402

VERBE = "trouver-personnes"
SENIORITE_IDS = {"owner": "320", "fondateur": "320", "cxo": "310", "c_level": "310", "vp": "300", "director": "220",
                 "directeur": "220", "manager": "210", "senior": "120"}
TAILLE_IDS = {"self": "A", "1-10": "B", "11-50": "C", "51-200": "D", "201-500": "E", "501-1000": "F",
              "1001-5000": "G", "5001-10000": "H", "10001+": "I"}
CRUSTDATA_SENIORITES = {"owner": "Owner", "fondateur": "Founder", "c_level": "C-level", "cxo": "C-level", "partner": "Partner",
                        "vp": "VP", "head": "Head", "director": "Director", "directeur": "Director", "manager": "Manager", "senior": "Senior"}


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


def _base(source):
    return {"source": source, "date_extraction": aujourd_hui()}


def _split_nom(nom: str) -> tuple[str, str]:
    nom = (nom or "").strip()
    parts = nom.split(" ", 1)
    return (parts[0], parts[1]) if len(parts) > 1 else (nom, "")


def ligne_harvest(it: dict, source: str) -> dict:
    pos = (it.get("currentPositions") or it.get("currentPosition") or [{}])
    pos = pos[0] if isinstance(pos, list) and pos else (pos if isinstance(pos, dict) else {})
    titre = _g(pos, "title", "position") or _g(it, "headline")
    return {**_base(source), "prenom": _g(it, "firstName"), "nom": _g(it, "lastName"), "titre": titre,
            "seniorite": seniorite_depuis_titre(titre), "entreprise": _g(pos, "companyName"),
            "linkedin_url": norm_linkedin_url(_g(it, "linkedinUrl")),
            "linkedin_entreprise_url": norm_linkedin_url(_g(pos, "companyLinkedinUrl")),
            "ville": _g(it, "location.parsed.city"), "pays": _g(it, "location.parsed.country") or _g(it, "location.linkedinText"),
            "headline": _g(it, "headline"), "email": _g(it, "email") if isinstance(it.get("email"), str) else ""}


# ------------------------------------------------------------------ Apify

def profils(a):
    entree = {"profileScraperMode": "Full" if a.complet else "Short", "maxItems": a.max}
    if a.mots_cles:
        entree["searchQuery"] = a.mots_cles
    if a.titres:
        entree["currentJobTitles"] = _liste(a.titres)
    if a.lieu:
        entree["locations"] = _liste(a.lieu)
    if a.taille:
        entree["companyHeadcount"] = [TAILLE_IDS.get(t, t) for t in _liste(a.taille)]
    if a.seniorites:
        entree["seniorityLevelIds"] = [SENIORITE_IDS.get(s, s) for s in _liste(a.seniorites)]
    if a.entreprises_urls:
        entree["currentCompanies"] = _liste(a.entreprises_urls)
    if a.changement_poste:
        entree["recentlyChangedJobs"] = True
    if a.industry_ids:
        entree["industryIds"] = _liste(a.industry_ids)
    if len(entree) <= 2:
        arret("profils : donnez au moins --titres, --mots-cles, --lieu, --entreprises-urls ou --seniorites")
    actor = "harvestapi/linkedin-profile-search"
    pages = max(1, -(-a.max // 25))
    estimation = f"{pages} page(s) de 25 x 0,10 $ = environ {pages * 0.10:.2f} $" + (f" + {a.max} x 0,004 $ (mode Full)" if a.complet else "")
    items, _ = lancer(actor, entree, label="profile-search", dry_run=a.dry_run, estimation=estimation)
    return [ligne_harvest(it, actor) for it in items], actor


def employes(a):
    if not a.entree:
        arret("employes : --in <csv d'entreprises avec linkedin_entreprise_url> est requis")
    entreprises = [l for l in lire_csv(a.entree) if norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url") or "")]
    urls = []
    for l in entreprises:
        u = norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url"))
        if u not in urls:
            urls.append(u)
    if not urls:
        arret("aucune colonne linkedin_entreprise_url remplie dans le CSV : passez d'abord par enrichir-entreprise")
    titres = _liste(a.titres)[:20]
    par = a.par_entreprise or 3
    entree = {"companies": urls, "profileScraperMode": "Short ($4 per 1k)", "companyBatchMode": "one_by_one",
              "maxItemsPerCompany": par * 2, "maxItems": par * 2 * len(urls)}
    if titres:
        entree["jobTitles"] = titres
    if a.lieu:
        entree["locations"] = _liste(a.lieu)
    if a.seniorites:
        entree["seniorityLevelIds"] = [SENIORITE_IDS.get(s, s) for s in _liste(a.seniorites)]
    actor = "harvestapi/linkedin-company-employees"
    estimation = f"{entree['maxItems']} profils max x 0,003 $ + {len(urls)} requetes x 0,02 $ = environ {entree['maxItems'] * 0.003 + len(urls) * 0.02:.2f} $"
    items, _ = lancer(actor, entree, label=f"employees ({len(urls)} entreprises)", dry_run=a.dry_run, estimation=estimation)
    lignes = []
    par_url = {u: l for l in entreprises for u in [norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url"))]}
    for it in items:
        ligne = ligne_harvest(it, actor)
        q = _g(it, "_meta.query.currentCompanies")
        cible = norm_linkedin_url(q[0]) if isinstance(q, list) and q else ""
        src = par_url.get(cible) or par_url.get(ligne["linkedin_entreprise_url"]) or {}
        if src:
            ligne["entreprise"] = ligne["entreprise"] or src.get("entreprise", "")
            ligne["linkedin_entreprise_url"] = ligne["linkedin_entreprise_url"] or cible
            for c in ("domaine", "secteur", "effectif", "score_icp", "tier"):
                if src.get(c) and not ligne.get(c):
                    ligne[c] = src[c]
        lignes.append(ligne)
    return lignes, actor


def cookies_linkedin():
    ua = env("LINKEDIN_USER_AGENT", aide="Ecrivez LINKEDIN_USER_AGENT dans .env (connecter-outils, etape 8).")
    fichier = env("LINKEDIN_COOKIES_FILE", obligatoire=False)
    if fichier and Path(fichier).exists():
        data = json.loads(Path(fichier).read_text(encoding="utf-8"))
        return (data if isinstance(data, list) else data.get("cookie", [])), ua
    li_at = env("LINKEDIN_LI_AT", aide="Ecrivez LINKEDIN_LI_AT et LINKEDIN_LI_A dans .env.")
    cookies = [{"name": "li_at", "value": li_at, "domain": ".linkedin.com", "path": "/", "secure": True, "httpOnly": True}]
    li_a = env("LINKEDIN_LI_A", obligatoire=False)
    if li_a:
        cookies.append({"name": "li_a", "value": li_a, "domain": ".linkedin.com", "path": "/", "secure": True, "httpOnly": True})
    return cookies, ua


def salesnav(a):
    actor = "curious_coder/linkedin-sales-navigator-search-scraper"
    cookies, ua = ([{"name": "li_at", "value": "<depuis .env>"}], "<depuis .env>") if a.dry_run else cookies_linkedin()
    entree = {"cookie": cookies, "userAgent": ua, "count": a.max, "deepScrape": False, "stopOnRateLimit": True,
              "minDelay": 5, "maxDelay": 30, "startPage": 1}
    if a.url:
        entree["searchUrl"] = a.url
    else:
        if a.titres:
            entree["peopleFilters.currentTitles"] = _liste(a.titres)
        if a.lieu:
            entree["peopleFilters.geography"] = _liste(a.lieu)
        if a.taille:
            entree["peopleFilters.companyHeadcount"] = [TAILLE_IDS.get(t, t) for t in _liste(a.taille)]
        if a.seniorites:
            entree["peopleFilters.seniorityLevel"] = [SENIORITE_IDS.get(s, s) for s in _liste(a.seniorites)]
        if a.mots_cles:
            entree["peopleFilters.keywords"] = a.mots_cles
        if a.changement_poste:
            entree["peopleFilters.changedJobs"] = True
        if len(entree) <= 8:
            arret("salesnav : donnez --url (recherche Sales Navigator de leads) ou --titres / --lieu / --taille / --seniorites")
    items, _ = lancer(actor, entree, label="sales-navigator-leads", dry_run=a.dry_run, estimation=prix(actor, a.max))
    lignes = []
    for it in items:
        prenom, nom = _g(it, "firstName", "first_name"), _g(it, "lastName", "last_name")
        if not prenom and _g(it, "name", "fullName"):
            prenom, nom = _split_nom(_g(it, "name", "fullName"))
        titre = _g(it, "title", "currentTitle", "headline", "currentPosition.title")
        lignes.append({**_base(actor), "prenom": prenom, "nom": nom, "titre": titre,
                       "seniorite": seniorite_depuis_titre(titre),
                       "entreprise": _g(it, "companyName", "company", "currentCompany", "currentPosition.companyName"),
                       "linkedin_url": norm_linkedin_url(_g(it, "linkedinUrl", "profileUrl", "url", "salesNavigatorUrl")),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "companyLinkedinUrl", "companyUrl", "currentPosition.companyLinkedinUrl")),
                       "ville": _g(it, "location", "geoRegion", "locationText"), "headline": _g(it, "headline", "summary")})
    return lignes, actor


# ------------------------------------------------------------------ API

def unipile(a):
    if a.dry_run:
        bandeau_dry_run("Unipile recherche de personnes", [f"api : {'sales_navigator' if a.url else 'classic'}",
                                                          f"url ou mots-cles : {a.url or a.mots_cles or a.titres}", f"max : {a.max}",
                                                          "cout : abonnement Unipile, pas de credit (mais des vues de profil sur le compte LinkedIn)"])
        return [], "unipile"
    u = Unipile()
    items = u.recherche(api="sales_navigator" if a.url else "classic", categorie="people", url=a.url,
                        mots_cles=None if a.url else (a.mots_cles or a.titres), max_resultats=a.max)
    lignes = []
    for it in items:
        prenom, nom = _g(it, "first_name"), _g(it, "last_name")
        if not prenom:
            prenom, nom = _split_nom(_g(it, "name"))
        pos = it.get("current_positions") or it.get("current_position") or {}
        pos = pos[0] if isinstance(pos, list) and pos else (pos if isinstance(pos, dict) else {})
        titre = _g(pos, "role", "title") or _g(it, "headline")
        url = _g(it, "profile_url", "public_profile_url") or (f"https://www.linkedin.com/in/{it['public_identifier']}" if it.get("public_identifier") else "")
        lignes.append({**_base("unipile"), "prenom": prenom, "nom": nom, "titre": titre, "seniorite": seniorite_depuis_titre(titre),
                       "entreprise": _g(it, "company") or _g(pos, "company"), "linkedin_url": norm_linkedin_url(url),
                       "ville": _g(it, "location"), "headline": _g(it, "headline"),
                       "provider_id": _g(it, "id", "provider_id", "member_urn"), "degre_relation": _g(it, "network_distance")})
    return lignes, "unipile"


def crustdata(a):
    titres, sen = _liste(a.titres), [CRUSTDATA_SENIORITES.get(s.lower(), s) for s in _liste(a.seniorites)]
    if a.dry_run:
        bandeau_dry_run("Crustdata /screener/persondb/search/", [f"titres={titres} seniorites={sen} region={a.lieu} entreprise={a.entreprise} limit={a.max}",
                                                                 f"cout : 3 credits par tranche de 100 resultats (environ {max(3, -(-a.max // 100) * 3)} credits)"])
        return [], "crustdata"
    c = Crustdata()
    afficher(f"  [crustdata] solde : {c.credits()} credits")
    doms = []
    if a.entree:
        doms = [domaine(l.get("domaine") or l.get("site_web") or "") for l in lire_csv(a.entree)]
        doms = [d for d in doms if d]
    res = c.personnes(entreprise=a.entreprise, titres=titres or None, seniorites=sen or None, region=a.lieu,
                      domaines=doms or None, limit=a.max)
    lignes = []
    for p in res.get("profiles", []):
        emp = (p.get("current_employers") or [{}])[0]
        prenom, nom = _split_nom(_g(p, "name"))
        titre = _g(emp, "title") or _g(p, "headline")
        lignes.append({**_base("crustdata"), "prenom": prenom, "nom": nom, "titre": titre,
                       "seniorite": seniorite_depuis_titre(titre) if not _g(emp, "seniority_level") else norm_texte(_g(emp, "seniority_level")).replace(" ", "_"),
                       "entreprise": _g(emp, "name"), "domaine": domaine(_g(emp, "company_website_domain")),
                       "linkedin_url": norm_linkedin_url(_g(p, "linkedin_profile_url")), "ville": _g(p, "region"),
                       "headline": _g(p, "headline")})
    afficher(f"  [crustdata] {len(lignes)} profils sur {res.get('total_count', '?')} disponibles")
    return lignes, "crustdata"


SOURCES = {"profils": profils, "employes": employes, "salesnav": salesnav, "unipile": unipile, "crustdata": crustdata}


def plafonner(lignes: list[dict], par: int, titres: list[str]) -> list[dict]:
    """Garde les `par` meilleurs contacts par entreprise : d'abord l'ordre des titres demandes, puis la seniorite."""
    ordre_sen = {"fondateur": 0, "c_level": 1, "vp": 2, "directeur": 3, "head": 4, "manager": 5, "senior": 6, "autre": 7, "": 8}
    normes = [norm_texte(t) for t in titres]

    def rang(l):
        t = norm_texte(l.get("titre"))
        idx = next((i for i, n in enumerate(normes) if n and n in t), len(normes))
        return (idx, ordre_sen.get(l.get("seniorite", ""), 8))

    groupes = defaultdict(list)
    for l in lignes:
        groupes[norm_texte(l.get("linkedin_entreprise_url") or l.get("entreprise") or l.get("linkedin_url"))].append(l)
    out = []
    for cle, grp in groupes.items():
        out.extend(sorted(grp, key=rang)[:par])
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=sorted(SOURCES))
    ap.add_argument("--sujet", default="")
    ap.add_argument("--in", dest="entree", help="CSV d'entreprises (employes : linkedin_entreprise_url ; crustdata : domaine)")
    ap.add_argument("--titres", help="titres separes par des virgules, du plus au moins prioritaire (20 max pour employes)")
    ap.add_argument("--seniorites", help="owner,c_level,vp,director,manager,senior (ids LinkedIn ou libelles Crustdata)")
    ap.add_argument("--lieu", help="lieu(x) LinkedIn ou region Crustdata")
    ap.add_argument("--taille", help="tranches d'effectif : 1-10,11-50,51-200,201-500,501-1000,1001-5000,5001-10000,10001+")
    ap.add_argument("--mots-cles")
    ap.add_argument("--entreprise", help="crustdata : nom d'une entreprise precise")
    ap.add_argument("--entreprises-urls", help="profils : URLs LinkedIn d'entreprises separees par des virgules")
    ap.add_argument("--industry-ids", help="profils : ids d'industrie LinkedIn")
    ap.add_argument("--url", help="salesnav / unipile : URL d'une recherche Sales Navigator de leads")
    ap.add_argument("--changement-poste", action="store_true", help="profils / salesnav : seulement les gens qui ont change de poste recemment")
    ap.add_argument("--par-entreprise", type=int, help="garder N contacts max par entreprise (defaut 3 pour employes, illimite sinon)")
    ap.add_argument("--max", type=int, default=100)
    ap.add_argument("--complet", action="store_true", help="profils : mode Full (+0,004 $ par profil)")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.source:
        prio = lire_outils().get("priorite", "apify")
        a.source = "crustdata" if prio == "api" else ("employes" if a.entree else "profils")
        afficher(f"  [source] {a.source} (d'apres OUTILS.md)")
    a.sujet = a.sujet or (a.titres or a.mots_cles or a.source).split(",")[0]
    lignes, outil = SOURCES[a.source](a)
    if a.dry_run:
        return
    if a.par_entreprise:
        avant = len(lignes)
        lignes = plafonner(lignes, a.par_entreprise, _liste(a.titres))
        afficher(f"  [plafond] {avant} -> {len(lignes)} lignes ({a.par_entreprise} max par entreprise)")
    vus, uniques = set(), []
    for l in lignes:
        cle = l.get("linkedin_url") or f"{l.get('prenom')} {l.get('nom')} {l.get('entreprise')}".lower()
        if cle in vus:
            continue
        vus.add(cle)
        uniques.append(l)
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, a.sujet)
    ecrire_csv(uniques, sortie)
    afficher(f"{len(uniques)} personnes ({outil}) -> {sortie}")


if __name__ == "__main__":
    main()
