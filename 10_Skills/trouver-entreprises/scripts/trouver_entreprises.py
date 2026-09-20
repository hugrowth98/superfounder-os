"""trouver_entreprises : une liste d'entreprises par criteres, en CSV normalise.

Sources (--source) :
  google-maps  Apify compass/crawler-google-places : commerces et services locaux (recherche + lieu)
  linkedin     Apify harvestapi/linkedin-company-search : filtres LinkedIn (mots-cles, lieux, taille, secteur ids)
  base-large   Apify code_crafter/leads-finder : base large par secteur, mots-cles, taille, CA, financement
               (une ligne par entreprise, dedoublonnee par domaine, avec le dirigeant trouve en bonus)
  salesnav     Apify curious_coder/linkedin-sales-navigator-search-scraper : URL de recherche Sales Navigator
               "comptes" + cookies LinkedIn du .env (LINKEDIN_LI_AT, LINKEDIN_LI_A, LINKEDIN_USER_AGENT)
  unipile      Unipile : meme URL Sales Navigator (ou mots-cles) avec le compte LinkedIn de l'utilisateur
  crustdata    Crustdata POST /v1/companies/search (priorite api)
  prospeo      Prospeo POST /search-company : filtres exacts (industries, lieux et technos resolus par les suggestions gratuites),
               mots-cles, taille, CA, annee, levee, ICP inverse (--vend-a), clients cles, integrations, lookalike par domaine ou
               texte, actualites, postes ouverts ; 1 credit par page de 25 ; --total-seulement ; --filtres-json = payload du tableau de bord
  ocean        Ocean.io POST /v3/search/companies : recherche precise par filtres (secteurs exacts du referentiel, mots-cles sur la
               description, technos du site, taille, pays, villes, CA, annee de creation, levee, croissance, lookalikes) ; --lister-secteurs,
               --lister-technos, --lister-mots-cles, --lister-lieux pour trouver les libelles (gratuit) ; --total-seulement pour compter

Sans --source : linkedin si OUTILS.md dit priorite apify, crustdata sinon.

Exemples :
  python3 trouver_entreprises.py --source google-maps --recherche "cabinet d'expertise comptable" --lieu "Lyon, France" --max 100 --avec-site
  python3 trouver_entreprises.py --source linkedin --mots-cles "agence marketing" --lieu France --taille 11-50,51-200 --max 200
  python3 trouver_entreprises.py --source base-large --secteur "computer software" --pays france --taille 11-50 --max 300
  python3 trouver_entreprises.py --source salesnav --url "https://www.linkedin.com/sales/search/company?..." --max 500
  python3 trouver_entreprises.py --source crustdata --secteur "Software Development" --taille 11-50 --lieu France --max 50
  python3 trouver_entreprises.py --source prospeo --lister-secteurs software
  python3 trouver_entreprises.py --source prospeo --secteur "Software Development" --lieu "Paris, France" --taille 11-50,51-200 --vend-a "Head of Sales" --total-seulement
  python3 trouver_entreprises.py --source prospeo --icp-texte "agences de recrutement specialisees tech, 10 a 50 personnes, France" --max 100
  python3 trouver_entreprises.py --source ocean --lister-secteurs "logiciel RH"
  python3 trouver_entreprises.py --source ocean --secteur "Human Resources Software" --pays fr --taille 11-50,51-200 --mots-cles "SaaS,logiciel" --total-seulement
  python3 trouver_entreprises.py --source ocean --secteur "Human Resources Software" --pays fr --villes Paris:fr --taille 11-50,51-200 --max 200 --enregistrer
Ajoutez --dry-run pour voir l'input et le cout sans rien lancer. Sortie : Listes-prospection/trouver-entreprises_<sujet>_<date>.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (Crustdata, Ocean, Prospeo, Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie,  # noqa: E402
                        domaine, ecrire_csv, enregistrer_requete, env, lire_outils, norm_linkedin_url)
from apify_run import lancer, prix  # noqa: E402

VERBE = "trouver-entreprises"
TITRES_DIRIGEANTS = ["CEO", "Founder", "Co-Founder", "Owner", "Managing Director", "President",
                     "Directeur General", "Gerant", "Fondateur", "Dirigeant"]
TAILLES_LEADS_FINDER = {"1-10": ["1-10"], "11-50": ["11-20", "21-50"], "51-200": ["51-100", "101-200"],
                        "201-500": ["201-500"], "501-1000": ["501-1000"], "1001-5000": ["1001-2000", "2001-5000"],
                        "5001-10000": ["5001-10000"], "10001+": ["10001-20000", "20001-50000", "50000+"]}


def _g(d: dict, *cles, defaut=""):
    """Premiere valeur non vide parmi des cles (chemins pointes acceptes)."""
    for c in cles:
        cur = d
        for part in c.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur not in (None, "", [], {}):
            return cur
    return defaut


def _liste(s: str | None) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _base(source: str) -> dict:
    return {"source": source, "date_extraction": aujourd_hui()}


# ------------------------------------------------------------------ sources Apify

def google_maps(a) -> tuple[list[dict], str]:
    if not a.recherche or not a.lieu:
        arret("--recherche et --lieu sont requis pour google-maps (ex : --recherche \"cabinet comptable\" --lieu \"Lyon, France\")")
    entree = {"searchStringsArray": [a.recherche], "locationQuery": a.lieu, "maxCrawledPlacesPerSearch": a.max,
              "language": a.langue, "skipClosedPlaces": True, "scrapeContacts": a.contacts}
    if a.avec_site:
        entree["website"] = "withWebsite"
    actor = "compass/crawler-google-places"
    items, _ = lancer(actor, entree, label="google-maps", dry_run=a.dry_run, estimation=prix(actor, a.max))
    lignes = []
    for it in items:
        site = _g(it, "website")
        li = (it.get("linkedIns") or [""])[0] if isinstance(it.get("linkedIns"), list) else ""
        lignes.append({**_base(actor), "entreprise": _g(it, "title"), "domaine": domaine(site),
                       "linkedin_entreprise_url": norm_linkedin_url(li), "ville": _g(it, "city"),
                       "pays": _g(it, "countryCode"), "secteur": _g(it, "categoryName"),
                       "site_web": site, "telephone_entreprise": _g(it, "phone", "phoneUnformatted"),
                       "adresse": _g(it, "address"), "note_google": _g(it, "totalScore"),
                       "nb_avis": _g(it, "reviewsCount"), "url_google_maps": _g(it, "url"),
                       "email_entreprise": (it.get("emails") or [""])[0] if isinstance(it.get("emails"), list) else ""})
    return lignes, actor


def linkedin_search(a) -> tuple[list[dict], str]:
    entree = {"scraperMode": "full" if a.complet else "short", "maxItems": a.max}
    if a.mots_cles:
        entree["searchQuery"] = a.mots_cles
    if a.lieu:
        entree["locations"] = _liste(a.lieu)
    if a.taille:
        entree["companySize"] = _liste(a.taille)
    if a.industry_ids:
        entree["industryIds"] = _liste(a.industry_ids)
    if not (a.mots_cles or a.lieu or a.taille or a.industry_ids):
        arret("linkedin : donnez au moins --mots-cles, --lieu, --taille ou --industry-ids")
    actor = "harvestapi/linkedin-company-search"
    items, _ = lancer(actor, entree, label="linkedin-company-search", dry_run=a.dry_run, estimation=prix(actor, a.max))
    lignes = []
    for it in items:
        loc = (it.get("locations") or [{}])[0] if isinstance(it.get("locations"), list) else {}
        tranche = it.get("employeeCountRange") or {}
        industries = it.get("industries") if isinstance(it.get("industries"), list) else []
        secteur = _g(it, "industry") or (industries[0].get("name", "") if industries and isinstance(industries[0], dict) else "")
        lignes.append({**_base(actor), "entreprise": _g(it, "name"), "domaine": domaine(_g(it, "website")),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedinUrl")),
                       "ville": _g(loc, "parsed.city", "city"), "pays": _g(loc, "parsed.country", "country") or _g(it, "location.linkedinText"),
                       "secteur": secteur,
                       "effectif": _g(it, "employeeCount") or (f"{tranche.get('start', '')}-{tranche.get('end', '')}" if tranche else ""),
                       "site_web": _g(it, "website"), "abonnes": _g(it, "followerCount", "followers"),
                       "annee_creation": _g(it, "foundedOn.year"), "type": _g(it, "companyType"),
                       "description": (_g(it, "tagline", "summary", "description") or "")[:300]})
    return lignes, actor


def base_large(a) -> tuple[list[dict], str]:
    entree = {"fetch_count": int(a.max * 1.5), "file_name": f"gtm-os {a.sujet}",
              "contact_job_title": TITRES_DIRIGEANTS, "seniority_level": ["founder", "owner", "c_suite"],
              "email_status": ["validated", "not_validated", "unknown"]}
    if a.secteur:
        entree["company_industry"] = _liste(a.secteur)
    if a.mots_cles:
        entree["company_keywords"] = _liste(a.mots_cles)
    if a.pays:
        entree["contact_location"] = [p.lower() for p in _liste(a.pays)]
    if a.taille:
        tailles = []
        for t in _liste(a.taille):
            tailles += TAILLES_LEADS_FINDER.get(t, [t])
        entree["size"] = tailles
    if a.ca_min:
        entree["min_revenue"] = a.ca_min
    if a.ca_max:
        entree["max_revenue"] = a.ca_max
    if a.financement:
        entree["funding"] = _liste(a.financement)
    if not (a.secteur or a.mots_cles or a.taille):
        arret("base-large : donnez au moins --secteur, --mots-cles ou --taille")
    actor = "code_crafter/leads-finder"
    items, _ = lancer(actor, entree, label="leads-finder", dry_run=a.dry_run, estimation=prix(actor, entree["fetch_count"]))
    vus, lignes = set(), []
    for it in items:
        dom = domaine(_g(it, "company_domain", "company_website"))
        cle = dom or (_g(it, "company_name") or "").lower()
        if not cle or cle in vus:
            continue
        vus.add(cle)
        lignes.append({**_base(actor), "entreprise": _g(it, "company_name"), "domaine": dom,
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "company_linkedin")),
                       "ville": _g(it, "company_city"), "pays": _g(it, "company_country"), "secteur": _g(it, "industry"),
                       "effectif": _g(it, "company_size"), "site_web": _g(it, "company_website"),
                       "chiffre_affaires": _g(it, "company_annual_revenue_clean", "company_annual_revenue"),
                       "financement_total": _g(it, "company_total_funding_clean", "company_total_funding"),
                       "technos": _g(it, "company_technologies"), "annee_creation": _g(it, "company_founded_year"),
                       "telephone_entreprise": _g(it, "company_phone"),
                       "dirigeant_trouve": f"{_g(it, 'first_name')} {_g(it, 'last_name')} ({_g(it, 'job_title')})".strip(),
                       "dirigeant_linkedin_url": norm_linkedin_url(_g(it, "linkedin")),
                       "dirigeant_email": _g(it, "email"),
                       "description": (_g(it, "company_description") or "")[:300]})
        if len(lignes) >= a.max:
            break
    return lignes, actor


def cookies_linkedin() -> tuple[list[dict], str]:
    """Cookies pour l'actor Sales Navigator, depuis le .env (jamais depuis un skill)."""
    ua = env("LINKEDIN_USER_AGENT", aide="Ecrivez LINKEDIN_USER_AGENT dans .env (voir connecter-outils, etape 8).")
    fichier = env("LINKEDIN_COOKIES_FILE", obligatoire=False)
    if fichier and Path(fichier).exists():
        data = json.loads(Path(fichier).read_text(encoding="utf-8"))
        return (data if isinstance(data, list) else data.get("cookie", [])), ua
    li_at = env("LINKEDIN_LI_AT", aide="Ecrivez LINKEDIN_LI_AT (et LINKEDIN_LI_A pour Sales Navigator) dans .env.")
    cookies = [{"name": "li_at", "value": li_at, "domain": ".linkedin.com", "path": "/", "secure": True, "httpOnly": True}]
    li_a = env("LINKEDIN_LI_A", obligatoire=False)
    if li_a:
        cookies.append({"name": "li_a", "value": li_a, "domain": ".linkedin.com", "path": "/", "secure": True, "httpOnly": True})
    return cookies, ua


def salesnav_apify(a) -> tuple[list[dict], str]:
    actor = "curious_coder/linkedin-sales-navigator-search-scraper"
    if a.dry_run:
        cookies, ua = [{"name": "li_at", "value": "<depuis .env>"}], "<depuis .env>"
    else:
        cookies, ua = cookies_linkedin()
    entree = {"cookie": cookies, "userAgent": ua, "count": a.max, "deepScrape": False, "stopOnRateLimit": True,
              "minDelay": 5, "maxDelay": 30, "startPage": 1}
    if a.url:
        if "/sales/search/company" not in a.url and "/sales/search/account" not in a.url:
            afficher("  [attention] l'URL ne ressemble pas a une recherche Sales Navigator de comptes")
        entree["searchUrl"] = a.url
    else:
        if a.mots_cles:
            entree["accountsFilters.keywords"] = a.mots_cles
        if a.lieu:
            entree["accountsFilters.geography"] = _liste(a.lieu)
        if a.secteur:
            entree["accountsFilters.industry"] = _liste(a.secteur)
        if a.taille:
            entree["accountsFilters.companyHeadcount"] = [TAILLE_SALESNAV.get(t, t) for t in _liste(a.taille)]
        if len(entree) <= 8:
            arret("salesnav : donnez --url (recherche de comptes Sales Navigator) ou --mots-cles / --lieu / --secteur / --taille")
    items, _ = lancer(actor, entree, label="sales-navigator-comptes", dry_run=a.dry_run, estimation=prix(actor, a.max))
    lignes = []
    for it in items:
        lignes.append({**_base(actor), "entreprise": _g(it, "name", "companyName", "title"),
                       "domaine": domaine(_g(it, "website", "companyWebsite", "url")),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedinUrl", "companyUrl", "url", "salesNavigatorUrl")),
                       "ville": _g(it, "location", "headquarters", "geoRegion"), "secteur": _g(it, "industry"),
                       "effectif": _g(it, "employeeCount", "employees", "employeeCountRange", "companySize"),
                       "site_web": _g(it, "website", "companyWebsite"),
                       "description": (_g(it, "description", "summary") or "")[:300]})
    return lignes, actor


TAILLE_SALESNAV = {"self": "A", "1-10": "B", "11-50": "C", "51-200": "D", "201-500": "E", "501-1000": "F",
                   "1001-5000": "G", "5001-10000": "H", "10001+": "I"}


# ------------------------------------------------------------------ sources API

def unipile(a) -> tuple[list[dict], str]:
    if a.dry_run:
        bandeau_dry_run("Unipile recherche d'entreprises", [f"api : {'sales_navigator' if a.url else 'classic'}",
                                                            f"url ou mots-cles : {a.url or a.mots_cles}", f"max : {a.max}",
                                                            "cout : inclus dans l'abonnement Unipile (pas de credit)"])
        return [], "unipile"
    u = Unipile()
    items = u.recherche(api="sales_navigator" if a.url else "classic", categorie="companies", url=a.url,
                        mots_cles=None if a.url else a.mots_cles, max_resultats=a.max)
    if getattr(u, "dernier_total", None) is not None:
        afficher(f"[unipile] total de comptes correspondant a la recherche : {u.dernier_total}")
    lignes = []
    for it in items:
        lignes.append({**_base("unipile"), "entreprise": _g(it, "name", "company_name"), "secteur": _g(it, "industry"),
                       "ville": _g(it, "location", "headquarters"), "effectif": _g(it, "employee_count"),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedin_url", "company_url", "profile_url")),
                       "unipile_id": _g(it, "id"), "description": (_g(it, "summary", "description") or "")[:300]})
    return lignes, "unipile"


def crustdata(a) -> tuple[list[dict], str]:
    if a.dry_run:
        bandeau_dry_run("Crustdata /v1/companies/search", [f"secteur={a.secteur} taille={a.taille} lieu={a.lieu} mots-cles={a.mots_cles} limit={a.max}",
                                                           "cout : 1 credit par recherche (2 en mode live)"])
        return [], "crustdata"
    c = Crustdata()
    afficher(f"  [crustdata] solde : {c.credits()} credits")
    res = c.entreprises(industry=a.secteur, employee_range=a.taille, location=a.lieu, keywords=a.mots_cles, limit=a.max)
    lignes = []
    for it in res:
        lignes.append({**_base("crustdata"), "entreprise": _g(it, "name", "company_name"),
                       "domaine": domaine(_g(it, "website", "company_website_domain", "domain")),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedin_url", "linkedin_profile_url")),
                       "pays": _g(it, "hq_country"), "secteur": _g(it, "industry"),
                       "effectif": _g(it, "employee_count", "employee_count_range"), "type": _g(it, "company_type"),
                       "stade_financement": _g(it, "funding_stage", "last_funding_round"),
                       "annee_creation": _g(it, "year_founded", "founded_year"),
                       "description": (_g(it, "description", "linkedin_company_description") or "")[:300]})
    return lignes, "crustdata"


# ------------------------------------------------------------------ Ocean.io (recherche precise par filtres)

TAILLES_OCEAN = {"1-10": ["0-1", "2-10"], "11-50": ["11-50"], "51-200": ["51-200"], "201-500": ["201-500"], "501-1000": ["501-1000"],
                 "1001-5000": ["1001-5000"], "5001-10000": ["5001-10000"], "10001+": ["10001-50000", "50001-100000", "100001-500000", "500000+"]}


def _referentiel_exact(oc, cle: str, valeurs: list[str], libelle: str) -> list[str]:
    """Chaque valeur doit exister telle quelle dans le referentiel Ocean (sans casse) ; sinon on propose les candidats."""
    ref = oc.data_fields().get(cle) or []
    if isinstance(ref, dict):
        ref = list(ref.keys())
    noms = [v if isinstance(v, str) else (v.get("name") or v.get("title") or str(v)) for v in ref]
    par_cle = {n.lower(): n for n in noms}
    exacts = []
    for v in valeurs:
        if v.lower() in par_cle:
            exacts.append(par_cle[v.lower()])
            continue
        cands = oc.chercher_referentiel(cle, v, limite=12)
        if len(cands) == 1:
            afficher(f"  [ocean] {libelle} '{v}' -> {cands[0]}")
            exacts.append(cands[0])
        elif cands:
            arret(f"{libelle} '{v}' n'existe pas tel quel chez Ocean. Candidats : {', '.join(cands)}. Reprenez le libelle exact (ou --lister-secteurs \"{v}\").")
        else:
            arret(f"{libelle} '{v}' inconnu chez Ocean : --lister-secteurs \"{v}\" pour chercher, ou passez par --mots-cles.")
    return exacts


def filtres_ocean(a, oc=None) -> dict:
    """Traduit les options en companiesFilters Ocean (v3). Les referentiels (secteurs, technos) sont verifies si `oc` est donne."""
    f: dict = {}
    if a.lookalikes:
        f["lookalikeDomains"] = _liste(a.lookalikes)
        f["companyMatchingMode"] = "precise"
    if a.secteur:
        vals = _liste(a.secteur)
        f["industries"] = {"industries": _referentiel_exact(oc, "industries", vals, "secteur") if oc else vals, "mode": "anyOf"}
    if a.categorie:
        vals = _liste(a.categorie)
        f["industryCategories"] = {"industryCategories": _referentiel_exact(oc, "industryCategories", vals, "categorie") if oc else vals, "mode": "anyOf"}
    if a.industrie_linkedin:
        vals = _liste(a.industrie_linkedin)
        f["linkedinIndustries"] = _referentiel_exact(oc, "linkedinIndustries", vals, "industrie LinkedIn") if oc else vals
    if a.secteurs_exclus:
        f["excludeIndustries"] = _liste(a.secteurs_exclus)
    mc = {}
    if a.mots_cles:
        mc["anyOf"] = _liste(a.mots_cles)
    if a.mots_cles_tous:
        mc["allOf"] = _liste(a.mots_cles_tous)
    if a.mots_cles_exclus:
        mc["noneOf"] = _liste(a.mots_cles_exclus)
    if mc:
        f["keywords"] = mc
    loc = {}
    if a.pays:
        loc["includeCountries"] = [x.lower() for x in _liste(a.pays)]
    if a.pays_exclus:
        loc["excludeCountries"] = [x.lower() for x in _liste(a.pays_exclus)]
    if a.villes:
        villes = []
        for v in _liste(a.villes):
            ville, _, pays = v.partition(":")
            villes.append({"city": ville.strip(), "country": (pays or (a.pays or "fr").split(",")[0]).strip().lower()})
        loc["includeCities"] = villes
    if loc:
        f["primaryLocations"] = loc
    if a.taille:
        tailles = []
        for tr in _liste(a.taille):
            if tr in TAILLES_OCEAN:
                tailles += TAILLES_OCEAN[tr]
            elif tr in Ocean.TAILLES:
                tailles.append(tr)
            else:
                arret(f"taille inconnue '{tr}' : {', '.join(TAILLES_OCEAN)} (ou une tranche Ocean : {', '.join(Ocean.TAILLES)})")
        f["companySizes"] = tailles
    if a.ca:
        for c in _liste(a.ca):
            if c not in Ocean.CA:
                arret(f"tranche de CA inconnue '{c}' : {', '.join(Ocean.CA)}")
        f["revenues"] = _liste(a.ca)
    tech = {}
    if a.technos:
        tech["anyOf"] = _referentiel_exact(oc, "technologies", _liste(a.technos), "techno") if oc else _liste(a.technos)
    if a.technos_exclues:
        tech["noneOf"] = _liste(a.technos_exclues)
    if tech:
        f["technologies"] = {"apps": tech}
    if a.fondee:
        d, _, fin = a.fondee.partition("-")
        f["yearFounded"] = {k: int(v) for k, v in (("from", d), ("to", fin)) if v}
    if a.levee or a.levee_depuis or a.levee_min:
        fr = {}
        if a.levee:
            fr["types"] = _liste(a.levee)
        if a.levee_depuis:
            fr["date"] = {"from": a.levee_depuis}
        if a.levee_min:
            fr["raised"] = {"from": int(a.levee_min)}
        f["fundingRound"] = fr
    if a.croissance is not None:
        f["headcountGrowth"] = {"asPercentage": True, "growthRange": {"from": float(a.croissance) / 100}, "months": "Six months"}
    if a.relevance_min:
        f["minRelevance"] = a.relevance_min.upper()
    if a.exclure_domaines:
        f["excludeDomains"] = _liste(a.exclure_domaines)
    return f


def ocean(a) -> tuple[list[dict], str]:
    """Ocean.io POST /v3/search/companies : une recherche precise par filtres (secteurs exacts, mots-cles, technos, taille, pays,
    villes, CA, annee, levee, croissance, lookalikes). La reponse donne le total et les credits factures."""
    if a.lister_secteurs or a.lister_technos or a.lister_mots_cles or a.lister_lieux:
        oc = Ocean()
        if a.lister_secteurs:
            for cle, lib in (("industries", "secteur"), ("industryCategories", "categorie"), ("linkedinIndustries", "industrie LinkedIn")):
                for n in oc.chercher_referentiel(cle, a.lister_secteurs, limite=20):
                    print(f"{lib}\t{n}")
        if a.lister_technos:
            for n in oc.chercher_referentiel("technologies", a.lister_technos, limite=30):
                print(f"techno\t{n}")
        if a.lister_mots_cles:
            for k in oc.autocomplete("keywords", a.lister_mots_cles, limite=15):
                print(f"mot-cle\t{k if isinstance(k, str) else json.dumps(k, ensure_ascii=False)}")
        if a.lister_lieux:
            for k in oc.autocomplete("locations", a.lister_lieux, limite=15):
                print(f"lieu\t{k if isinstance(k, str) else json.dumps(k, ensure_ascii=False)}")
        return [], "ocean"
    if a.dry_run:
        f = filtres_ocean(a, None)
        if not f:
            arret("ocean : donnez au moins un filtre (--secteur, --mots-cles, --technos, --taille, --pays, --villes, --lookalikes...)")
        bandeau_dry_run("Ocean.io POST /v3/search/companies", [f"companiesFilters : {json.dumps(f, ensure_ascii=False)}",
                                                                f"size : {a.max}",
                                                                "cout : credits Ocean par entreprise renvoyee (la reponse affiche creditsUsed) ; "
                                                                "--total-seulement compte d'abord (apercu gratuit en Enterprise, sinon 1 entreprise)"])
        return [], "ocean"
    oc = Ocean()
    afficher(f"  [ocean] solde : {oc.solde()}")
    f = filtres_ocean(a, oc)
    if not f:
        arret("ocean : donnez au moins un filtre (--secteur, --mots-cles, --technos, --taille, --pays, --villes, --lookalikes...)")
    if a.total_seulement:
        total, comment = oc.total_entreprises(f)
        afficher(f"  [ocean] total : {total} entreprise(s) ({comment})")
        print(total)
        if a.enregistrer:
            enregistrer_requete(a.nom or a.sujet, "", json.dumps(f, ensure_ascii=False), commande_ocean(a), volume=total, notes="comptage seul")
        return [], "ocean"
    items, total, credits = oc.entreprises(f, max_resultats=a.max, taille_page=min(50, a.max))
    afficher(f"  [ocean] {len(items)} entreprise(s) prises sur {total} disponibles ; {credits} credit(s) factures")
    lignes = []
    for c in items:
        l = Ocean.normaliser_entreprise(c)
        if c.get("relevance"):
            l["pertinence"] = c["relevance"]
        lignes.append(l)
    if a.enregistrer:
        enregistrer_requete(a.nom or a.sujet, "", json.dumps(f, ensure_ascii=False), commande_ocean(a), volume=f"{len(lignes)} sur {total}")
    return lignes, "ocean"


def commande_ocean(a) -> str:
    """La commande a rejouer, reconstruite depuis les options renseignees."""
    parts = ["trouver_entreprises.py --source ocean"]
    for nom in ("secteur", "categorie", "industrie_linkedin", "secteurs_exclus", "mots_cles", "mots_cles_tous", "mots_cles_exclus", "pays", "pays_exclus",
                "villes", "taille", "ca", "technos", "technos_exclues", "fondee", "levee", "levee_depuis", "levee_min", "croissance", "relevance_min",
                "lookalikes", "exclure_domaines", "max"):
        v = getattr(a, nom, None)
        if v not in (None, "", False):
            parts.append(f"--{nom.replace('_', '-')} \"{v}\"")
    return " ".join(parts)


# ------------------------------------------------------------------ Prospeo (recherche d'entreprises, 1 credit par page de 25)

def filtres_prospeo(a, pr=None) -> dict:
    """Traduit les options en filtres Prospeo (search-company). Les valeurs qui ne se devinent pas (lieux, industries, technos)
    passent par les suggestions gratuites quand `pr` est donne ; sinon elles partent telles quelles (dry-run)."""
    if a.filtres_json:
        brut = a.filtres_json
        if Path(brut).exists():
            brut = Path(brut).read_text(encoding="utf-8")
        f = json.loads(brut)
        return f.get("filters", f)
    f: dict = {}
    if a.secteur:
        vals = _liste(a.secteur)
        f["company_industry"] = {"include": pr.resoudre("industry", vals, "secteur") if pr else vals}
    if a.secteurs_exclus:
        f.setdefault("company_industry", {})["exclude"] = _liste(a.secteurs_exclus)
    if a.lieu:
        vals = [x.strip() for x in a.lieu.split(";") if x.strip()]  # "Paris, France" garde sa virgule : plusieurs lieux se separent par ;
        f["company_location_search"] = {"include": pr.resoudre("location", vals, "lieu") if pr else vals}
    if a.taille:
        tailles = []
        for tr in _liste(a.taille):
            if tr in Prospeo.TAILLES_DEPUIS_MODULE:
                tailles += Prospeo.TAILLES_DEPUIS_MODULE[tr]
            elif tr in Prospeo.TAILLES:
                tailles.append(tr)
            else:
                arret(f"taille inconnue '{tr}' : {', '.join(Prospeo.TAILLES_DEPUIS_MODULE)} (ou une tranche Prospeo : {', '.join(Prospeo.TAILLES)})")
        f["company_headcount_range"] = tailles
    mc = {}
    if a.mots_cles:
        mc["include"] = _liste(a.mots_cles)
    if a.mots_cles_tous:
        mc["include"] = _liste(a.mots_cles_tous)
        mc["include_all"] = True
    if a.mots_cles_exclus:
        mc["exclude"] = _liste(a.mots_cles_exclus)
    if mc:
        f["company_keywords"] = mc
    if a.technos:
        vals = _liste(a.technos)
        f["company_technology"] = {"include": pr.resoudre("technology", vals, "techno") if pr else vals}
    if a.technos_exclues:
        f.setdefault("company_technology", {})["exclude"] = _liste(a.technos_exclues)
    if a.ca:
        vals = _liste(a.ca)
        for c in vals:
            if c not in Prospeo.CA:
                arret(f"tranche de CA inconnue '{c}' : {', '.join(Prospeo.CA)}")
        f["company_revenue"] = {"min": vals[0], "max": vals[-1], "include_unknown_revenue": False}
    if a.fondee:
        d, _, fin = a.fondee.partition("-")
        f["company_founded"] = {k: int(v) for k, v in (("min", d), ("max", fin)) if v}
    if a.levee or a.levee_depuis_jours or a.investisseurs:
        fr = {}
        if a.levee:
            fr["stage"] = _liste(a.levee)
        if a.levee_depuis_jours:
            j = int(a.levee_depuis_jours)
            if j not in Prospeo.JOURS:
                arret(f"--levee-depuis-jours accepte {', '.join(map(str, Prospeo.JOURS))}")
            fr["funding_date"] = j
        if a.investisseurs:
            fr["investors"] = _liste(a.investisseurs)
        f["company_funding"] = fr
    if a.vend_a or a.vend_a_tailles:
        icp = {}
        if a.vend_a:
            icp["titles_include"] = _liste(a.vend_a)
        if a.vend_a_tailles:
            icp["company_sizes"] = _liste(a.vend_a_tailles)
        f["company_icp"] = icp
    if a.clients_cles:
        f["company_key_customers"] = {"include": _liste(a.clients_cles)}
    if a.integrations:
        f["company_integrations"] = {"include": _liste(a.integrations)}
    if a.lookalike_domaine or a.icp_texte:
        la = {"minimum_tier": (a.lookalike_niveau or "T3").upper()}
        if a.lookalike_domaine:
            la["domain"] = domaine(a.lookalike_domaine)
        else:
            la["icp_text"] = a.icp_texte
        f["company_lookalike"] = la
    if a.actualites:
        cats = _liste(a.actualites)
        f["company_news"] = {"categories": cats, "timeframe_days": int(a.actualites_jours or 90)}
    if a.recrute:
        f["company_job_posting_hiring_for"] = {"include": _liste(a.recrute)}
    if a.exclure_domaines:
        f["company"] = {"websites": {"exclude": [domaine(d) for d in _liste(a.exclure_domaines)]}}
    return f


def commande_prospeo(a) -> str:
    parts = ["trouver_entreprises.py --source prospeo"]
    for nom in ("secteur", "secteurs_exclus", "lieu", "taille", "mots_cles", "mots_cles_tous", "mots_cles_exclus", "technos", "technos_exclues", "ca", "fondee",
                "levee", "levee_depuis_jours", "investisseurs", "vend_a", "vend_a_tailles", "clients_cles", "integrations", "lookalike_domaine", "icp_texte",
                "lookalike_niveau", "actualites", "actualites_jours", "recrute", "exclure_domaines", "filtres_json", "max"):
        v = getattr(a, nom, None)
        if v not in (None, "", False):
            parts.append(f"--{nom.replace('_', '-')} \"{v}\"")
    return " ".join(parts)


def prospeo(a) -> tuple[list[dict], str]:
    """Prospeo POST /search-company : 1 credit par page de 25 (gratuit si la page a deja ete payee dans les 30 jours).
    La page 1 donne le total : --total-seulement s'arrete la. Les libelles (lieux, industries, technos) sont resolus par les
    suggestions gratuites avant la recherche : une valeur devinee renvoie zero resultat sans erreur."""
    if a.lister_secteurs or a.lister_technos or a.lister_lieux or a.lister_titres:
        pr = Prospeo()
        for genre, mots, lib in (("industry", a.lister_secteurs, "secteur"), ("technology", a.lister_technos, "techno"),
                                 ("location", a.lister_lieux, "lieu"), ("job_title", a.lister_titres, "titre")):
            if mots:
                for s in pr.suggestions(genre, mots):
                    print(f"{lib}\t{s}")
        return [], "prospeo"
    if a.dry_run:
        f = filtres_prospeo(a, None)
        if not f:
            arret("prospeo : donnez au moins un filtre positif (--secteur, --lieu, --taille, --mots-cles, --technos, --vend-a, --clients-cles, --lookalike-domaine, --icp-texte, --filtres-json...)")
        bandeau_dry_run("Prospeo POST /search-company", [f"filters : {json.dumps(f, ensure_ascii=False)[:900]}",
                                                        f"pages : jusqu'a {max(1, -(-a.max // 25))} (25 par page, 1 credit par page avec resultats ; gratuit si deja payee sous 30 jours)",
                                                        "les lieux, industries et technos seront resolus par les suggestions gratuites au vrai run"])
        return [], "prospeo"
    pr = Prospeo()
    afficher(f"  [prospeo] {pr.solde()}")
    f = filtres_prospeo(a, pr)
    if not f:
        arret("prospeo : donnez au moins un filtre positif")
    if a.total_seulement:
        total, rep = pr.total("/search-company", f)
        afficher(f"  [prospeo] total : {total} entreprise(s) ({'page 1 gratuite' if rep.get('free') else '1 credit pour la page 1'})")
        print(total)
        if a.enregistrer:
            enregistrer_requete(a.nom or a.sujet, "", json.dumps(f, ensure_ascii=False), commande_prospeo(a), volume=total, notes="comptage seul")
        return [], "prospeo"
    items, total, pages = pr.entreprises(f, max_resultats=a.max)
    afficher(f"  [prospeo] {len(items)} entreprise(s) prises sur {total} disponibles ; {pages} page(s) facturee(s), soit {pages} credit(s)")
    lignes = [{**_base("prospeo"), **Prospeo.normaliser_entreprise(c)} for c in items]
    if a.enregistrer:
        enregistrer_requete(a.nom or a.sujet, "", json.dumps(f, ensure_ascii=False), commande_prospeo(a), volume=f"{len(lignes)} sur {total}")
    return lignes, "prospeo"


SOURCES = {"google-maps": google_maps, "linkedin": linkedin_search, "base-large": base_large,
           "salesnav": salesnav_apify, "unipile": unipile, "crustdata": crustdata, "ocean": ocean, "prospeo": prospeo}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=sorted(SOURCES))
    ap.add_argument("--sujet", default="", help="mot pour le nom du fichier (defaut : recherche ou mots-cles)")
    ap.add_argument("--recherche", help="google-maps : ce qu'on taperait dans Google Maps")
    ap.add_argument("--mots-cles", help="mots-cles (linkedin, base-large, salesnav, unipile, crustdata)")
    ap.add_argument("--lieu", help="lieu ou liste de lieux separes par des virgules (prospeo : libelles canoniques comme \"Paris, France\", plusieurs lieux separes par ;)")
    ap.add_argument("--pays", help="base-large : pays en anglais minuscule (france, belgium)")
    ap.add_argument("--secteur", help="secteur(s) : libelle Crustdata, industrie leads-finder, ou industrie Sales Nav")
    ap.add_argument("--industry-ids", help="linkedin : ids d'industrie LinkedIn separes par des virgules")
    ap.add_argument("--taille", help="tranches : 1-10,11-50,51-200,201-500,501-1000,1001-5000,5001-10000,10001+")
    ap.add_argument("--ca-min", help="base-large : 100K,500K,1M,5M,10M,25M,50M,100M,500M,1B")
    ap.add_argument("--ca-max")
    ap.add_argument("--financement", help="base-large : seed,series_a,series_b,...")
    ap.add_argument("--url", help="salesnav / unipile : URL d'une recherche Sales Navigator de comptes")
    ap.add_argument("--max", type=int, default=100)
    ap.add_argument("--langue", default="fr", help="google-maps : langue des resultats")
    ap.add_argument("--avec-site", action="store_true", help="google-maps : seulement les lieux avec site web (+0,001 $/lieu)")
    ap.add_argument("--contacts", action="store_true", help="google-maps : enrichir emails et reseaux depuis le site (+0,002 $/lieu)")
    ap.add_argument("--complet", action="store_true", help="linkedin : mode full (0,004 $) au lieu de short (0,002 $)")
    ap.add_argument("--out", help="chemin CSV de sortie (defaut : Listes-prospection/)")
    ap.add_argument("--dry-run", action="store_true")
    oc_ = ap.add_argument_group("ocean (recherche precise par filtres ; --secteur = industries Ocean exactes, --taille et --mots-cles communs)")
    oc_.add_argument("--categorie", help="ocean : categories d'industrie (libelles exacts du referentiel)")
    oc_.add_argument("--industrie-linkedin", help="ocean : industries LinkedIn (libelles exacts)")
    oc_.add_argument("--secteurs-exclus", help="ocean : industries a exclure")
    oc_.add_argument("--mots-cles-tous", help="ocean : mots-cles tous presents (allOf) ; --mots-cles = au moins un (anyOf)")
    oc_.add_argument("--mots-cles-exclus", help="ocean : mots-cles a exclure (noneOf)")
    oc_.add_argument("--pays-exclus", help="ocean : codes pays ISO a exclure")
    oc_.add_argument("--villes", help="ocean : villes du siege, Ville:pays separees par des virgules (Paris:fr,Lyon:fr)")
    oc_.add_argument("--ca", help="ocean : tranches de CA : " + ",".join(Ocean.CA))
    oc_.add_argument("--technos", help="ocean : technologies presentes sur le site (libelles exacts, au moins une)")
    oc_.add_argument("--technos-exclues", help="ocean : technologies a exclure")
    oc_.add_argument("--fondee", help="ocean : annee de creation, ex : 2015-2024 ou 2018-")
    oc_.add_argument("--levee", help="ocean : types de tour, ex : \"Seed,Series A\"")
    oc_.add_argument("--levee-depuis", help="ocean : date de tour minimale, YYYY-MM-DD")
    oc_.add_argument("--levee-min", help="ocean : montant leve minimal en dollars")
    oc_.add_argument("--croissance", type=float, help="ocean : croissance d'effectif minimale sur 6 mois, en pourcent (10 = +10 %%)")
    oc_.add_argument("--relevance-min", help="ocean : pertinence minimale A, B ou C (avec --lookalikes)")
    oc_.add_argument("--lookalikes", help="ocean : domaines de reference a combiner avec les filtres (10 max)")
    oc_.add_argument("--exclure-domaines", help="ocean : domaines a exclure (vos clients, vos concurrents)")
    oc_.add_argument("--total-seulement", action="store_true", help="ocean : compter seulement (apercu gratuit en Enterprise, sinon 1 entreprise facturee)")
    oc_.add_argument("--lister-secteurs", metavar="MOTS", help="ocean : cherche des libelles de secteur, categorie, industrie LinkedIn (gratuit)")
    oc_.add_argument("--lister-technos", metavar="MOTS", help="ocean : cherche des libelles de technologie (gratuit)")
    oc_.add_argument("--lister-mots-cles", metavar="MOTS", help="ocean : suggestions de mots-cles (autocomplete)")
    oc_.add_argument("--lister-lieux", metavar="MOTS", help="ocean : suggestions de lieux (autocomplete)")
    oc_.add_argument("--nom", help="nom de la requete pour le registre Ciblage/requetes-booleennes.md")
    oc_.add_argument("--enregistrer", action="store_true", help="ocean / prospeo : ajoute la requete (commande, filtres, volume) au registre")
    pr_ = ap.add_argument_group("prospeo (recherche par filtres exacts ; --secteur, --lieu, --taille, --mots-cles, --technos, --ca, --fondee, --levee, --total-seulement, --lister-* et --enregistrer sont communs avec ocean)")
    pr_.add_argument("--levee-depuis-jours", help="prospeo : dernier tour depuis N jours (30, 60, 90, 180, 270, 365)")
    pr_.add_argument("--investisseurs", help="prospeo : noms d'investisseurs (10 max)")
    pr_.add_argument("--vend-a", help="prospeo : ICP inverse, titres que l'entreprise vend a (ex : \"VP Sales,Head of Sales\") ; plan Growth")
    pr_.add_argument("--vend-a-tailles", help="prospeo : tailles des clients de l'entreprise : micro, smb, midmarket, enterprise, large_enterprise")
    pr_.add_argument("--clients-cles", help="prospeo : entreprises qui citent ces marques comme clients (100 max) ; plan Growth")
    pr_.add_argument("--integrations", help="prospeo : integrations citees sur le site (20 max) ; plan Growth")
    pr_.add_argument("--lookalike-domaine", help="prospeo : un domaine de reference (lookalike, mode domaine)")
    pr_.add_argument("--icp-texte", help="prospeo : description libre du client ideal (lookalike sans graine, 5 000 caracteres max)")
    pr_.add_argument("--lookalike-niveau", help="prospeo : T1 (le plus proche), T2, T3 (defaut)")
    pr_.add_argument("--actualites", help="prospeo : categories d'actualite : \"Funding & Investment\", \"Mergers & Acquisitions\", \"Product Launch\", Partnership, Expansion, \"Layoffs & Restructuring\", IPO, \"Leadership Change\"")
    pr_.add_argument("--actualites-jours", help="prospeo : 60, 90 (defaut), 180 ou 365")
    pr_.add_argument("--recrute", help="prospeo : intitules de postes ouverts (offres actives)")
    pr_.add_argument("--lister-titres", metavar="MOTS", help="prospeo : suggestions de titres de poste (gratuit)")
    pr_.add_argument("--filtres-json", help="prospeo : le JSON copie depuis le tableau de bord (bouton Search API), chaine ou chemin de fichier")
    a = ap.parse_args()

    if not a.source:
        a.source = "linkedin" if lire_outils().get("priorite", "apify") != "api" else "crustdata"
        afficher(f"  [source] {a.source} (d'apres OUTILS.md)")
    a.sujet = a.sujet or a.recherche or a.mots_cles or a.secteur or a.source
    lignes, outil = SOURCES[a.source](a)
    if a.dry_run or (a.source in ("ocean", "prospeo") and (a.total_seulement or a.lister_secteurs or a.lister_technos or a.lister_mots_cles or a.lister_lieux or a.lister_titres)):
        return
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, a.sujet)
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} entreprises ({outil}) -> {sortie}")


if __name__ == "__main__":
    main()
