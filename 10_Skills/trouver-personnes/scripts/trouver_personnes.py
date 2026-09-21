"""trouver_personnes : des decisionnaires par titre, seniorite, lieu ou entreprise, en CSV normalise.

Sources (--source) :
  profils     Apify harvestapi/linkedin-profile-search : filtres LinkedIn (titres, lieux, taille, entreprises), sans cookies
  employes    Apify harvestapi/linkedin-company-employees : depuis un CSV d'entreprises (colonne linkedin_entreprise_url)
  salesnav    Apify curious_coder/linkedin-sales-navigator-search-scraper : URL de recherche Sales Navigator "leads"
              + cookies LinkedIn du .env (LINKEDIN_LI_AT, LINKEDIN_LI_A, LINKEDIN_USER_AGENT)
  unipile     Unipile : URL Sales Navigator (ou mots-cles) avec le compte LinkedIn de l'utilisateur (secours)
  prospeo     Prospeo POST /search-person : titres (contient, similaires, ou --booleen), seniorites, departements, lieux canoniques,
              entreprises par domaine (--in ou --domaines, 500 max), --par-entreprise ; 1 credit par page de 25 ; --reveler obtient les
              emails verifies en lot (1 credit chacun), --reveler-mobile les mobiles (10 credits) ; --changement-poste = 90 jours
  ocean       Ocean.io POST /v3/search/people : decisionnaires d'entreprises precises (--in avec domaine, ou --domaines) ou d'une cible
              (--secteur exact, --taille, --lieu = codes pays), par --titres, --seniorites, --departements ; --par-entreprise (2 par defaut
              avec des domaines) ; --changement-poste = arrives depuis 90 jours
  crustdata   Crustdata /screener/persondb/search/ (priorite api)
  google      Apify apify/google-search-scraper : sans compte LinkedIn ni outil API. Par entreprise (--in, --entreprise, --domaines) :
              une requete Google ("titres" OR ...) "entreprise" site:linkedin.com/in, 0,0025 $ par entreprise ; par cible : titres,
              lieu, mots-cles, jusqu'a 10 pages. Le moins precis : confiance par ligne (haute = entreprise et titre confirmes)

Sans --source (auto) : la cascade "le plus puissant de ce qui est branche" : prospeo > crustdata > ocean (outils API) > salesnav
(Apify + cookies LinkedIn, avec --url ou des filtres) > employes ou profils (Apify LinkedIn) > google (Apify). Chaque source
saute si sa cle manque ou si l'entree ne lui convient pas ; le script dit laquelle il prend et pourquoi.
  --in accepte un CSV d'entreprises avec linkedin_entreprise_url, domaine ou seulement entreprise (nom) : employes resout
  les URLs manquantes par Google (0,0025 $ par entreprise), profils cherche par lots de 10 noms (currentCompanies).

Exemples :
  python3 trouver_personnes.py --source profils --titres "CEO,Fondateur,Directeur Général" --lieu France --taille 11-50,51-200 --max 100
  python3 trouver_personnes.py --source employes --in Listes-prospection/trouver-entreprises_x.csv --titres "DRH,Responsable recrutement" --par-entreprise 2
  python3 trouver_personnes.py --source salesnav --url "https://www.linkedin.com/sales/search/people?..." --max 500
  python3 trouver_personnes.py --source prospeo --in entreprises.csv --dirigeants --par-entreprise 2 --email-verifie --reveler --format large
  python3 trouver_personnes.py --source prospeo --titres "Head of Sales" --titres-similaires --lieu "France" --taille 11-50,51-200 --total-seulement
  python3 trouver_personnes.py --source ocean --in entreprises.csv --dirigeants --par-entreprise 2 --format large
  python3 trouver_personnes.py --source employes --in entreprises.csv --dirigeants --strict-titre --par-entreprise 2 --format large
  python3 trouver_personnes.py --source crustdata --titres "Head of Sales,VP Sales" --seniorites "vp,head" --lieu France --max 100
  python3 trouver_personnes.py --in entreprises.csv --dirigeants --par-entreprise 2 --format large        (auto : la cascade choisit)
  python3 trouver_personnes.py --source google --in entreprises.csv --dirigeants --par-entreprise 2 --format large
  python3 trouver_personnes.py --source profils --in entreprises.csv --dirigeants --par-entreprise 3     (lots de 10 noms, currentCompanies)
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
from gtm_common import (Crustdata, Ocean, Prospeo, Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, domaine,  # noqa: E402
                        ecrire_csv, enregistrer_requete, env, fraicheur, lire_csv, lire_outils, norm_linkedin_url, norm_texte,
                        seniorite_depuis_titre)
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
    actor = "harvestapi/linkedin-profile-search"
    noms = noms_entreprises(a) if (a.entree or a.entreprise) and not a.entreprises_urls else []
    if noms:
        # des noms d'entreprises : par lots de 10 dans currentCompanies (LinkedIn les combine en OU), 3 profils par entreprise
        par = a.par_entreprise or 3
        lots = [noms[i:i + 10] for i in range(0, len(noms), 10)]
        pages = sum(max(1, -(-(par * len(lot)) // 25)) for lot in lots)
        estimation = f"{len(lots)} lot(s) de 10 entreprises, {pages} page(s) de 25 x 0,10 $ = environ {pages * 0.10:.2f} $"
        lignes = []
        for n, lot in enumerate(lots, 1):
            e = {**entree, "currentCompanies": lot, "maxItems": par * len(lot)}
            items, _ = lancer(actor, e, label=f"profile-search lot {n}/{len(lots)}", dry_run=a.dry_run, estimation=estimation if n == 1 else "(compris ci-dessus)")
            for it in items:
                l = ligne_harvest(it, actor)
                cible = entreprise_correspondante(l.get("entreprise", ""), lot)
                if not cible:
                    continue  # anti faux positif : l'entreprise actuelle doit correspondre a un nom du lot
                l["entreprise_cible"] = cible
                lignes.append(l)
        if not a.dry_run:
            afficher(f"  [profils] {len(lignes)} profils dont l'entreprise actuelle correspond a un nom demande")
        return lignes, actor
    if len(entree) <= 2:
        arret("profils : donnez au moins --titres, --mots-cles, --lieu, --entreprises-urls, --in (noms d'entreprises) ou --seniorites")
    pages = max(1, -(-a.max // 25))
    estimation = f"{pages} page(s) de 25 x 0,10 $ = environ {pages * 0.10:.2f} $" + (f" + {a.max} x 0,004 $ (mode Full)" if a.complet else "")
    items, _ = lancer(actor, entree, label="profile-search", dry_run=a.dry_run, estimation=estimation)
    return [ligne_harvest(it, actor) for it in items], actor


def mots_significatifs(nom: str) -> set:
    stop = {"sas", "sarl", "sa", "eurl", "sasu", "group", "groupe", "france", "inc", "ltd", "llc", "gmbh", "the", "and", "les", "des"}
    return {m for m in norm_texte(nom).replace("-", " ").split() if len(m) >= 4 and m not in stop}


def entreprise_correspondante(trouvee: str, noms: list[str]) -> str:
    """Le nom demande qui correspond a l'entreprise trouvee : un mot significatif (4 lettres et plus) en commun, ou un nom court
    contenu dans l'autre. Rend '' si aucune (faux positif)."""
    nt = norm_texte(trouvee)
    if not nt:
        return ""
    mt = mots_significatifs(trouvee)
    for n in noms:
        nn = norm_texte(n)
        if nn and (nn in nt or nt in nn):
            return n
        if mt & mots_significatifs(n):
            return n
    return ""


NOMS_FORCES: list[str] = []  # second passage Google : seulement les entreprises restees sans decisionnaire


def noms_entreprises(a) -> list[str]:
    """Les noms d'entreprises de --entreprise, du CSV --in (colonne entreprise, sinon domaine) ou de --domaines."""
    if NOMS_FORCES:
        return list(NOMS_FORCES)
    noms = []
    if a.entreprise:
        noms.append(a.entreprise.strip())
    if a.entree:
        for l in lire_csv(a.entree):
            n = (l.get("entreprise") or l.get("nom") or l.get("company") or "").strip()
            if not n and (l.get("domaine") or l.get("site_web")):
                n = domaine(l.get("domaine") or l.get("site_web")).split(".")[0]
            if n and n not in noms:
                noms.append(n)
    if a.domaines and not noms:
        noms = [d.split(".")[0] for d in _liste(a.domaines)]
    return noms


def urls_entreprises_par_google(noms: list[str], a) -> dict:
    """site:linkedin.com/company "<nom>" pour chaque nom sans URL : rend {nom: url}. 0,0025 $ par entreprise."""
    actor = "apify/google-search-scraper"
    requetes = [f"site:linkedin.com/company \"{n}\"" for n in noms]
    entree = {"queries": "\n".join(requetes), "maxPagesPerQuery": 1, "countryCode": "fr", "languageCode": "fr",
              "saveHtml": False, "saveHtmlToKeyValueStore": False, "includeIcons": False}
    items, _ = lancer(actor, entree, label=f"google-company ({len(noms)} entreprises sans URL)", dry_run=a.dry_run, estimation=prix(actor, len(noms)))
    out = {}
    for it in items:
        term = ((it.get("searchQuery") or {}).get("term") or "")
        nom = next((n for n in noms if norm_texte(n) in norm_texte(term)), "")
        for r in it.get("organicResults") or []:
            u = r.get("url") or ""
            if "linkedin.com/company/" in u and nom and entreprise_correspondante(r.get("title") or "", [nom]):
                out[nom] = norm_linkedin_url(u.split("?")[0].rstrip("/"))
                break
    return out


def employes(a):
    if not a.entree and not a.entreprises_urls:
        arret("employes : --in <csv d'entreprises> (linkedin_entreprise_url, ou juste le nom : l'URL est cherchee par Google) ou --entreprises-urls")
    toutes = lire_csv(a.entree) if a.entree else [{"entreprise": u, "linkedin_entreprise_url": u} for u in _liste(a.entreprises_urls)]
    sans_url = [l for l in toutes if not norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url") or "")
                and (l.get("entreprise") or l.get("nom"))]
    if sans_url:
        noms = []
        for l in sans_url:
            n = (l.get("entreprise") or l.get("nom")).strip()
            if n not in noms:
                noms.append(n)
        afficher(f"  [employes] {len(noms)} entreprise(s) sans URL LinkedIn : recherche Google site:linkedin.com/company (0,0025 $ chacune)")
        trouvees = urls_entreprises_par_google(noms, a)
        for l in sans_url:
            u = trouvees.get((l.get("entreprise") or l.get("nom")).strip())
            if u:
                l["linkedin_entreprise_url"] = u
        if not a.dry_run:
            afficher(f"  [employes] {len(trouvees)} URL(s) trouvee(s) sur {len(noms)}" + (f" ; sans URL : {', '.join(n for n in noms if n not in trouvees)}" if len(trouvees) < len(noms) else ""))
    entreprises = [l for l in toutes if norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url") or "")]
    urls = []
    for l in entreprises:
        u = norm_linkedin_url(l.get("linkedin_entreprise_url") or l.get("linkedin_url"))
        if u not in urls:
            urls.append(u)
    if not urls:
        if a.dry_run and sans_url:
            urls = [f"<url de {n}>" for n in (l.get("entreprise") or l.get("nom") for l in sans_url)]
        else:
            arret("aucune URL LinkedIn d'entreprise (ni trouvee par Google) : passez par enrichir-entreprise, ou --source profils avec les noms")
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


DIRIGEANTS = ["General Manager", "Gérant", "Gerant", "Président", "President", "Presidente", "Présidente", "Directeur Général",
              "Directrice Générale", "Fondateur", "Fondatrice", "Founder", "Co-founder", "Cofounder", "Co-fondateur", "CEO",
              "Chief Executive Officer", "DG", "PDG", "Dirigeant"]  # 20 titres, le plafond des actors harvestapi
DEPARTEMENTS_OCEAN = ["Accounting and Finance", "Board", "Business Support", "Customer Relations", "Design", "Editorial Personnel", "Engineering",
                      "Founder/Owner", "Healthcare", "HR", "Legal", "Management", "Manufacturing", "Marketing and Advertising", "Operations",
                      "PR and Communications", "Procurement", "Product", "Quality Control", "R&D", "Sales", "Security", "Supply Chain", "Other", "Education"]


def ocean(a):
    """Ocean.io POST /v3/search/people : les personnes d'entreprises precises (domaines du CSV ou --domaines), ou d'une cible
    (secteurs exacts, taille, pays), par titres, seniorites, departements ; peoplePerCompany plafonne par entreprise ;
    changedPositionAfter pour les arrivees recentes. Rend linkedinUrl, jobTitle, seniorites, entreprise, domaine."""
    pf: dict = {}
    if a.titres:
        pf["jobTitleKeywords"] = {"anyOf": _liste(a.titres)}
    if a.titres_exclus:
        pf.setdefault("jobTitleKeywords", {})["noneOf"] = _liste(a.titres_exclus)
    if a.seniorites:
        sen = []
        for s in _liste(a.seniorites):
            if s.lower() not in Ocean.SENIORITES:
                arret(f"seniorite inconnue '{s}' pour Ocean : {', '.join(sorted(set(Ocean.SENIORITES)))}")
            sen.append(Ocean.SENIORITES[s.lower()])
        pf["seniorities"] = sorted(set(sen))
    if a.departements:
        deps = []
        for d in _liste(a.departements):
            m = next((x for x in DEPARTEMENTS_OCEAN if x.lower() == d.lower()), None)
            if not m:
                arret(f"departement inconnu '{d}' : {', '.join(DEPARTEMENTS_OCEAN)}")
            deps.append(m)
        pf["departments"] = {"departments": deps, "mode": "anyOf"}
    if a.lieu:
        pf["countries"] = [x.strip().lower() for x in _liste(a.lieu) if len(x.strip()) == 2] or None
        if not pf["countries"]:
            arret("ocean : --lieu attend des codes pays ISO (fr,be), pas des villes")
    if a.changement_poste:
        from datetime import date, timedelta
        pf["changedPositionAfter"] = (date.today() - timedelta(days=90)).strftime("%Y-%m")
    cf: dict = {}
    doms = []
    if a.entree:
        for l in lire_csv(a.entree):
            d = domaine(l.get("domaine") or l.get("site_web") or "")
            if d and d not in doms:
                doms.append(d)
    doms += [domaine(d) for d in _liste(a.domaines) if domaine(d) and domaine(d) not in doms]
    if doms:
        cf["includeDomains"] = doms
    if a.secteur:
        cf["industries"] = {"industries": _liste(a.secteur), "mode": "anyOf"}
    if a.taille:
        from_module = {"1-10": ["0-1", "2-10"], "10001+": ["10001-50000", "50001-100000", "100001-500000", "500000+"]}
        tailles = []
        for tr in _liste(a.taille):
            tailles += from_module.get(tr, [tr])
        cf["companySizes"] = tailles
    if a.mots_cles:
        cf["keywords"] = {"anyOf": _liste(a.mots_cles)}
    if not pf and not cf:
        arret("ocean : donnez des entreprises (--in ou --domaines) et/ou des criteres (--titres, --seniorites, --departements, --secteur, --taille, --lieu)")
    if not doms and not (pf.get("seniorities") or pf.get("jobTitleKeywords") or pf.get("departments")):
        arret("ocean : sans liste d'entreprises, precisez au moins --titres, --seniorites ou --departements")
    par = a.par_entreprise or (2 if doms else None)
    if a.dry_run:
        bandeau_dry_run("Ocean.io POST /v3/search/people", [f"peopleFilters : {json.dumps(pf, ensure_ascii=False)}",
                                                            f"companiesFilters : {json.dumps(cf, ensure_ascii=False)[:600]}" + (f" ({len(doms)} domaines)" if doms else ""),
                                                            f"peoplePerCompany : {par or 'illimite'} ; size : {a.max}",
                                                            "cout : credits Ocean par personne renvoyee (la reponse affiche creditsUsed)"])
        return [], "ocean"
    oc = Ocean()
    afficher(f"  [ocean] solde : {oc.solde()}")
    items, total, credits = oc.personnes(pf, cf or None, max_resultats=a.max, taille_page=min(50, a.max), par_entreprise=par)
    afficher(f"  [ocean] {len(items)} personne(s) prises sur {total} disponibles ; {credits} credit(s) factures")
    lignes = [{**_base("ocean"), **Ocean.normaliser_personne(p)} for p in items]
    if a.changement_poste:
        for l in lignes:
            l["signal_type"] = l.get("signal_type") or "changement_poste"
    return lignes, "ocean"


# ------------------------------------------------------------------ Prospeo (personnes, 1 credit par page de 25, revelation en lot)

def filtres_prospeo_personnes(a, pr=None) -> dict:
    if a.filtres_json:
        brut = a.filtres_json
        if Path(brut).exists():
            brut = Path(brut).read_text(encoding="utf-8")
        f = json.loads(brut)
        return f.get("filters", f)
    f: dict = {}
    if a.booleen:
        f["person_job_title"] = {"boolean_search": a.booleen}
    elif a.titres:
        jt = {"include": _liste(a.titres), "match_mode": "SIMILAR" if a.titres_similaires else "CONTAINS"}
        if a.titres_similaires:
            jt["smart_intensity"] = (a.intensite or "NORMAL").upper()
        if a.titres_exclus:
            jt["exclude"] = _liste(a.titres_exclus)
        f["person_job_title"] = jt
    if a.seniorites:
        sen = []
        for s in _liste(a.seniorites):
            if s.lower() not in Prospeo.SENIORITES:
                arret(f"seniorite inconnue '{s}' pour Prospeo : {', '.join(sorted(set(Prospeo.SENIORITES)))}")
            sen.append(Prospeo.SENIORITES[s.lower()])
        f["person_seniority"] = {"include": sorted(set(sen))}
    if a.departements:
        f["person_department"] = {"include": _liste(a.departements)}
    if a.lieu:
        vals = [x.strip() for x in a.lieu.split(";") if x.strip()]
        f["person_location_search"] = {"include": pr.resoudre("location", vals, "lieu") if pr else vals}
    if a.changement_poste:
        f["person_job_change"] = {"timeframe_days": 90, "only_new_company": True}
    cd = {}
    if a.email_verifie:
        cd["email"] = ["VERIFIED"]
    if a.mobile_verifie:
        cd["mobile"] = ["VERIFIED"]
    if cd or a.cacher_deja_reveles:
        cd.setdefault("operator", "AND" if (a.email_verifie and a.mobile_verifie) else "OR")
        cd["hide_people_with_details_already_revealed"] = bool(a.cacher_deja_reveles)
        f["person_contact_details"] = cd
    doms = []
    if a.entree:
        for l in lire_csv(a.entree):
            d = domaine(l.get("domaine") or l.get("site_web") or "")
            if d and d not in doms:
                doms.append(d)
    doms += [domaine(d) for d in _liste(a.domaines) if domaine(d) and domaine(d) not in doms]
    if doms:
        if len(doms) > 500:
            arret(f"prospeo : 500 domaines max par recherche ({len(doms)} donnes) : decoupez le fichier")
        f["company"] = {"websites": {"include": doms}}
    if a.secteur:
        vals = _liste(a.secteur)
        f["company_industry"] = {"include": pr.resoudre("industry", vals, "secteur") if pr else vals}
    if a.taille:
        tailles = []
        for tr in _liste(a.taille):
            tailles += Prospeo.TAILLES_DEPUIS_MODULE.get(tr, [tr])
        f["company_headcount_range"] = tailles
    if a.mots_cles:
        f["company_keywords"] = {"include": _liste(a.mots_cles)}
    par = a.par_entreprise or (2 if doms else None)
    if par:
        f["max_person_per_company"] = int(par)
    return f


def prospeo(a):
    """Prospeo POST /search-person : titres (contient, similaire avec expansion, ou booleen), seniorites, departements, lieux
    canoniques, entreprises par domaine (500 max), filtres d'entreprise ; max_person_per_company plafonne ; la recherche
    ne revele ni email ni mobile (statut VERIFIED visible) : --reveler les obtient en lot (1 credit par email, 10 par mobile)."""
    if a.lister_titres or a.lister_lieux:
        pr = Prospeo()
        for genre, mots, lib in (("job_title", a.lister_titres, "titre"), ("location", a.lister_lieux, "lieu")):
            if mots:
                for s in pr.suggestions(genre, mots):
                    print(f"{lib}\t{s}")
        return [], "prospeo"
    if a.dry_run:
        f = filtres_prospeo_personnes(a, None)
        if not f or all(k in ("max_person_per_company", "person_contact_details") for k in f):
            arret("prospeo : donnez des entreprises (--in ou --domaines) et/ou des criteres (--titres, --booleen, --seniorites, --departements, --lieu, --secteur, --taille)")
        bandeau_dry_run("Prospeo POST /search-person", [f"filters : {json.dumps(f, ensure_ascii=False)[:900]}",
                                                       f"pages : jusqu'a {max(1, -(-a.max // 25))} (25 par page, 1 credit par page avec resultats)",
                                                       "revelation : " + (f"--reveler{' --reveler-mobile' if a.reveler_mobile else ''} : 1 credit par email trouve, 10 par mobile, 0 sinon" if (a.reveler or a.reveler_mobile) else "aucune (emails et mobiles masques, statuts visibles)")])
        return [], "prospeo"
    pr = Prospeo()
    afficher(f"  [prospeo] {pr.solde()}")
    f = filtres_prospeo_personnes(a, pr)
    if a.total_seulement:
        total, rep = pr.total("/search-person", f)
        statuts = [((r.get("person") or {}).get("email") or {}).get("status") for r in rep.get("results") or []]
        verif = sum(1 for s in statuts if s == "VERIFIED")
        afficher(f"  [prospeo] total : {total} personne(s) ; sur la page 1, {verif}/{len(statuts)} avec un email verifie")
        print(total)
        return [], "prospeo"
    items, total, pages = pr.personnes(f, max_resultats=a.max)
    afficher(f"  [prospeo] {len(items)} personne(s) prises sur {total} disponibles ; {pages} page(s) facturee(s)")
    lignes = [{**_base("prospeo"), **Prospeo.normaliser_personne(r)} for r in items]
    if a.changement_poste:
        for l in lignes:
            l["signal_type"] = l.get("signal_type") or "changement_poste"
    if a.reveler or a.reveler_mobile:
        cibles = [l for l in lignes if l.get("prospeo_person_id") and not l.get("email")]
        data = [{"identifier": l["prospeo_person_id"], "person_id": l["prospeo_person_id"]} for l in cibles]
        if data:
            trouves, non, cout = pr.enrichir_personnes(data, email_verifie_seulement=not a.emails_non_verifies, mobile=bool(a.reveler_mobile))
            for l in cibles:
                m = trouves.get(l["prospeo_person_id"])
                if not m:
                    continue
                n = Prospeo.normaliser_personne(m)
                for k in ("email", "email_statut", "telephone"):
                    if n.get(k) and not l.get(k):
                        l[k] = n[k]
            afficher(f"  [prospeo] revelation : {len(trouves)} trouve(s), {len(non)} sans resultat, {cout} credit(s) factures")
    return lignes, "prospeo"


# ------------------------------------------------------------------ Google (le dernier recours)

TITRES_GOOGLE_DIRIGEANTS = ["CEO", "PDG", "Directeur Général", "Directrice Générale", "Fondateur", "Fondatrice", "Founder", "Co-founder",
                            "Président", "Gérant", "General Manager", "Dirigeant"]


def _decouper_titre_google(titre: str) -> tuple[str, str, str, str]:
    """'Prenom Nom - Titre - Entreprise | LinkedIn' -> (prenom, nom, titre, entreprise). Tolere les tirets longs de Google."""
    tt = titre.replace(" | LinkedIn", "").replace("| LinkedIn", "")
    for sep in (" \u2013 ", " \u2014 ", " - "):
        tt = tt.replace(sep, " | ")
    parts = [x.strip() for x in tt.split(" | ") if x.strip()]
    nom_complet = parts[0] if parts else ""
    prenom, nom = _split_nom(nom_complet)
    poste = parts[1] if len(parts) > 1 else ""
    entreprise = parts[2] if len(parts) > 2 else ""
    return prenom, nom, poste, entreprise


def google(a):
    """apify/google-search-scraper : des profils LinkedIn par requete Google. Par entreprise (--in, --entreprise, --domaines) : une requete
    (titres OR ...) "entreprise" site:linkedin.com/in ; par cible : titres + lieu + mots-cles, jusqu'a 10 pages. Aucun compte, aucun outil
    API ; le moins precis des chemins : chaque ligne porte une confiance (haute : entreprise et titre confirmes, moyenne : l'un des deux)."""
    actor = "apify/google-search-scraper"
    titres = _liste(a.titres)
    titres_q = (TITRES_GOOGLE_DIRIGEANTS if (a.dirigeants or not titres) else titres)[:10]
    groupe = "(" + " OR ".join(f'"{x}"' for x in titres_q) + ")"
    noms = noms_entreprises(a)
    if noms:
        requetes = [f'{groupe} "{n}" site:linkedin.com/in' for n in noms]
        pages_par = 1
    else:
        if not (titres or a.mots_cles):
            arret("google : donnez des entreprises (--in, --entreprise, --domaines) ou une cible (--titres, --lieu, --mots-cles)")
        q = groupe + (f' "{a.lieu}"' if a.lieu else "") + (f" {a.mots_cles}" if a.mots_cles else "") + " site:linkedin.com/in"
        requetes, pages_par = [q], min(10, max(1, -(-a.max // 10)))
    entree = {"queries": "\n".join(requetes), "maxPagesPerQuery": pages_par, "countryCode": a.pays, "languageCode": a.pays if a.pays in ("fr", "en", "de", "es", "it") else "en",
              "saveHtml": False, "saveHtmlToKeyValueStore": False, "includeIcons": False}
    items, _ = lancer(actor, entree, label=f"google-personnes ({len(requetes)} requete(s) x {pages_par} page(s))", dry_run=a.dry_run,
                      estimation=prix(actor, len(requetes) * pages_par))
    lignes = []
    voulus = [norm_texte(x) for x in titres_q]
    for it in items:
        term = ((it.get("searchQuery") or {}).get("term") or "")
        cible = next((n for n in noms if f'"{norm_texte(n)}"' in norm_texte(term) or norm_texte(n) in norm_texte(term)), "") if noms else ""
        for r in it.get("organicResults") or []:
            u = r.get("url") or ""
            if "linkedin.com/in/" not in u:
                continue
            pi = r.get("personalInfo") or {}
            prenom, nom, poste, ent = _decouper_titre_google(r.get("title") or "")
            poste = pi.get("jobTitle") or poste
            ent = pi.get("companyName") or ent
            texte = norm_texte(f"{r.get('title') or ''} {r.get('description') or ''} {pi.get('rawText') or ''}")
            ent_ok = bool(cible) and (bool(entreprise_correspondante(ent, [cible])) or norm_texte(cible) in texte)
            titre_ok = any(v in norm_texte(poste) or v in texte for v in voulus)
            if noms and not ent_ok:
                continue  # sans l'entreprise confirmee, la ligne est un faux positif probable
            if not titre_ok and not a.garder_faibles:
                continue
            conf = "haute" if (ent_ok and titre_ok) or (not noms and titre_ok and ent) else "moyenne"
            lignes.append({**_base(actor), "prenom": prenom, "nom": nom, "titre": poste, "seniorite": seniorite_depuis_titre(poste),
                           "entreprise": ent or cible, "entreprise_cible": cible, "linkedin_url": norm_linkedin_url(u.split("?")[0]),
                           "headline": (r.get("title") or "").replace(" | LinkedIn", ""), "confiance": conf, "google_requete": term})
    if not a.dry_run:
        afficher(f"  [google] {len(lignes)} profil(s) retenu(s) ({sum(1 for l in lignes if l['confiance'] == 'haute')} en confiance haute)")
    return lignes, actor


SOURCES = {"profils": profils, "employes": employes, "salesnav": salesnav, "unipile": unipile, "crustdata": crustdata, "ocean": ocean,
           "prospeo": prospeo, "google": google}


def _cle(nom: str) -> bool:
    return bool(env(nom, obligatoire=False))


def choisir_source(a) -> tuple[str, str]:
    """La cascade : le plus puissant de ce qui est branche, pour l'entree donnee. Rend (source, raison)."""
    par_entreprise = bool(a.entree or a.entreprise or a.domaines or a.entreprises_urls)
    domaines = bool(a.domaines) or (bool(a.entree) and any(domaine(l.get("domaine") or l.get("site_web") or "") for l in lire_csv(a.entree)))
    cookies = bool(env("LINKEDIN_USER_AGENT", obligatoire=False)) and (bool(env("LINKEDIN_LI_AT", obligatoire=False)) or bool(env("LINKEDIN_COOKIES_FILE", obligatoire=False)))
    apify = _cle("APIFY_TOKEN")
    etapes = []
    if _cle("PROSPEO_API_KEY"):
        if not par_entreprise or domaines or a.entreprise:
            return "prospeo", "outil API branche (recherche par filtres exacts, emails verifies)"
        etapes.append("prospeo saute : il cherche par domaine, le CSV n'en a pas (ajoutez une colonne domaine, ou enrichir-entreprise)")
    else:
        etapes.append("prospeo non branche")
    if _cle("CRUSTDATA_API_KEY"):
        if not par_entreprise or domaines or a.entreprise:
            return "crustdata", "outil API branche"
        etapes.append("crustdata saute : il cherche par domaine ou par nom unique")
    else:
        etapes.append("crustdata non branche")
    if _cle("OCEAN_API_KEY"):
        if (par_entreprise and domaines) or a.secteur:
            return "ocean", "outil API branche (decisionnaires par domaine)"
        etapes.append("ocean saute : il faut des domaines ou --secteur")
    else:
        etapes.append("ocean non branche")
    if apify and cookies and (a.url or not par_entreprise):
        return "salesnav", "Apify + cookies LinkedIn du .env (Sales Navigator)"
    if a.url and _cle("UNIPILE_API_KEY") and _cle("UNIPILE_ACCOUNT_ID"):
        return "unipile", "URL Sales Navigator sans cookies Apify : le compte Unipile"
    if apify:
        if par_entreprise:
            return "employes", "Apify LinkedIn (employes des entreprises ; URLs manquantes cherchees par Google)"
        return "profils", "Apify LinkedIn (recherche de profils par filtres, sans cookies)"
    etapes.append("apify non branche")
    arret("aucune source disponible : connectez au moins Apify (connecter-outils), ou Prospeo, Crustdata, Ocean.io ; cascade : " + " ; ".join(etapes))


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


def format_large(lignes: list[dict], titres: list[str]) -> list[dict]:
    """Une ligne par entreprise avec d1 (le decisionnaire principal) et d2 (le second), choisis par l'ordre des titres demandes
    (CEO avant fondateur avant DG...), puis par seniorite."""
    from collections import OrderedDict
    voulus = [norm_texte(x) for x in titres]

    def rang(l):
        tt = norm_texte(l.get("titre") or "")
        pos = next((i for i, v in enumerate(voulus) if v in tt), len(voulus))
        return (pos, {"fondateur": 0, "c_level": 1, "vp": 2, "directeur": 3, "head": 4, "manager": 5}.get(l.get("seniorite"), 9))
    groupes: "OrderedDict[str, list]" = OrderedDict()
    for l in lignes:
        cle = norm_texte(l.get("linkedin_entreprise_url") or l.get("domaine") or l.get("entreprise") or "")
        groupes.setdefault(cle, []).append(l)
    sortie = []
    for cle, grp in groupes.items():
        grp = sorted(grp, key=rang)[:2]
        base = {"entreprise": grp[0].get("entreprise", ""), "domaine": grp[0].get("domaine", ""),
                "linkedin_entreprise_url": grp[0].get("linkedin_entreprise_url", ""), "source": grp[0].get("source", ""), "date_extraction": aujourd_hui()}
        for n, l in enumerate(grp, 1):
            base.update({f"d{n}_prenom": l.get("prenom", ""), f"d{n}_nom": l.get("nom", ""), f"d{n}_titre": l.get("titre", ""), f"d{n}_linkedin_url": l.get("linkedin_url", "")})
        sortie.append(base)
    return sortie


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
    ap.add_argument("--signal", help="etiquette de signal a poser sur chaque ligne (URL Sales Navigator a filtre) : visite_profil, "
                                     "abonne_entreprise, a_publie, changement_poste ; ecrit signal_type, signal_date (aujourd'hui), signal_detail, fraicheur")
    ap.add_argument("--par-entreprise", type=int, help="garder N contacts max par entreprise (defaut 3 pour employes, 2 pour ocean avec des domaines, illimite sinon)")
    ap.add_argument("--dirigeants", action="store_true", help="prend les 20 titres de dirigeants (CEO, fondateur, DG, gerant...) comme --titres")
    ap.add_argument("--titres-exclus", help="titres a exclure (ocean : noneOf ; autres sources : filtre local avec --strict-titre)")
    ap.add_argument("--strict-titre", action="store_true", help="ne garde que les lignes dont le titre actuel contient un des titres demandes (anti faux positifs)")
    ap.add_argument("--format", choices=["long", "large"], default="long", help="large : en plus du CSV, un fichier _decisionnaires.csv avec une ligne par entreprise (d1_*, d2_*)")
    ap.add_argument("--domaines", help="ocean : domaines d'entreprises separes par des virgules (ou --in avec une colonne domaine)")
    ap.add_argument("--secteur", help="ocean : industries Ocean exactes (voir trouver_entreprises.py --source ocean --lister-secteurs)")
    ap.add_argument("--departements", help="ocean : departements (Management, Sales, Marketing and Advertising, HR, Engineering, Founder/Owner...)")
    pr_ = ap.add_argument_group("prospeo")
    pr_.add_argument("--booleen", help="prospeo : booleen de titres, ex : \"(CEO OR CTO) AND !intern\" (remplace --titres)")
    pr_.add_argument("--titres-similaires", action="store_true", help="prospeo : elargit chaque titre aux titres voisins (match_mode SIMILAR)")
    pr_.add_argument("--intensite", help="prospeo : LOOSE, NORMAL (defaut) ou STRICT avec --titres-similaires")
    pr_.add_argument("--email-verifie", action="store_true", help="prospeo : seulement les personnes avec un email verifie")
    pr_.add_argument("--mobile-verifie", action="store_true", help="prospeo : seulement les personnes avec un mobile verifie")
    pr_.add_argument("--cacher-deja-reveles", action="store_true", help="prospeo : exclut les contacts deja reveles par votre compte (jamais payer deux fois)")
    pr_.add_argument("--reveler", action="store_true", help="prospeo : revele les emails en lot apres la recherche (1 credit par email trouve)")
    pr_.add_argument("--reveler-mobile", action="store_true", help="prospeo : revele aussi les mobiles (10 credits par mobile, email compris)")
    pr_.add_argument("--emails-non-verifies", action="store_true", help="prospeo : accepter aussi les emails non verifies a la revelation")
    pr_.add_argument("--total-seulement", action="store_true", help="prospeo : page 1 seulement (1 credit) : total et part d'emails verifies")
    pr_.add_argument("--lister-titres", metavar="MOTS", help="prospeo : suggestions de titres (gratuit)")
    pr_.add_argument("--lister-lieux", metavar="MOTS", help="prospeo : suggestions de lieux canoniques (gratuit)")
    pr_.add_argument("--filtres-json", help="prospeo : le JSON copie depuis le tableau de bord (Search API), chaine ou fichier")
    ap.add_argument("--nom", help="nom de la requete pour le registre Ciblage/requetes-booleennes.md")
    ap.add_argument("--enregistrer", action="store_true", help="ajoute ou met a jour la requete (URL ou commande, volume) dans le registre")
    ap.add_argument("--max", type=int, default=100)
    ap.add_argument("--complet", action="store_true", help="profils : mode Full (+0,004 $ par profil)")
    ap.add_argument("--pays", default="fr", help="google : pays de la recherche (code ISO, defaut fr)")
    ap.add_argument("--garder-faibles", action="store_true", help="google : garder aussi les profils dont le titre n'est pas confirme")
    ap.add_argument("--sans-google", action="store_true", help="employes / profils : pas de second passage Google pour les entreprises restees sans personne")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.source:
        a.source, raison = choisir_source(a)
        afficher(f"  [source] {a.source} : {raison} (cascade : prospeo > crustdata > ocean > salesnav > employes ou profils > google ; --source pour forcer)")
    if a.dirigeants:
        a.titres = ",".join(DIRIGEANTS)
    a.sujet = a.sujet or ("dirigeants" if a.dirigeants else (a.titres or a.mots_cles or a.source)).split(",")[0]
    lignes, outil = SOURCES[a.source](a)
    if a.source in ("employes", "profils") and not a.sans_google and (a.entree or a.entreprise):
        # second passage : les entreprises demandees restees sans personne passent par Google (le dernier recours de la cascade)
        noms = noms_entreprises(a)
        couverts = {norm_texte(l.get("entreprise_cible") or entreprise_correspondante(l.get("entreprise", ""), noms)) for l in lignes}
        restants = [n for n in noms if norm_texte(n) not in couverts]
        if restants and (lignes or a.dry_run):
            afficher(f"  [google] {len(restants)} entreprise(s) sans decisionnaire par {a.source} : second passage Google ({', '.join(restants[:8])}{'...' if len(restants) > 8 else ''})")
            NOMS_FORCES[:] = restants
            complement, _ = google(a)
            NOMS_FORCES.clear()
            lignes.extend(complement)
    if a.dry_run or (a.source == "prospeo" and (a.total_seulement or a.lister_titres or a.lister_lieux)):
        return
    if a.strict_titre and a.titres:
        voulus = [norm_texte(x) for x in _liste(a.titres)]
        exclus = [norm_texte(x) for x in _liste(a.titres_exclus)]
        avant = len(lignes)
        lignes = [l for l in lignes if any(v in norm_texte(l.get("titre") or "") for v in voulus)
                  and not any(x in norm_texte(l.get("titre") or "") for x in exclus)]
        afficher(f"  [strict-titre] {avant} -> {len(lignes)} lignes (titre actuel contenant un des titres demandes)")
    if a.signal:
        detail = {"visite_profil": "a consulte votre profil (Sales Navigator, vues de profil recentes)",
                  "abonne_entreprise": "suit votre page entreprise (Sales Navigator)",
                  "a_publie": "a publie sur LinkedIn dans les 30 derniers jours (Sales Navigator)",
                  "changement_poste": "a change de poste dans les 90 derniers jours (Sales Navigator, date a confirmer par enrichir-personne)"}
        for l in lignes:
            l["signal_type"] = a.signal
            l["signal_date"] = aujourd_hui()
            l["signal_detail"] = detail.get(a.signal, f"filtre Sales Navigator {a.signal}")
            l["fraicheur"] = fraicheur(l["signal_date"])
        afficher(f"  [signal] {a.signal} pose sur {len(lignes)} lignes (signal_date = {aujourd_hui()} : la date du run, pas celle de l'action)")
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
    if a.format == "large":
        large = format_large(uniques, _liste(a.titres))
        sortie_large = sortie.with_name(sortie.stem + "_decisionnaires.csv")
        ecrire_csv(large, sortie_large, colonnes_extra=["d1_prenom", "d1_nom", "d1_titre", "d1_linkedin_url", "d2_prenom", "d2_nom", "d2_titre", "d2_linkedin_url"])
        afficher(f"{len(large)} entreprise(s), 2 decisionnaires max chacune -> {sortie_large}")
    if a.enregistrer or a.url:
        from gtm_common import maj_volume_requete
        ref = a.url or f"trouver_personnes.py --source {a.source}" + "".join(
            f" --{k} \"{getattr(a, k.replace('-', '_'))}\"" for k in ("titres", "seniorites", "lieu", "taille", "mots-cles", "departements", "domaines", "secteur")
            if getattr(a, k.replace("-", "_"), None))
        # une URL deja enregistree par construire-requete-salesnav recoit son volume ; --enregistrer ajoute la ligne sinon
        if not maj_volume_requete(ref, len(uniques)) and a.enregistrer:
            enregistrer_requete(a.nom or a.sujet, "", a.titres or a.seniorites or "", ref, volume=len(uniques))


if __name__ == "__main__":
    main()
