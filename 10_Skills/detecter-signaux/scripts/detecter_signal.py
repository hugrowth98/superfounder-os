"""detecter_signal : levees, acquisitions, recrutements, changements de poste, investisseurs, entreprises,
via l'actor Apify signalbase/signalbase-api (0,04 $ par resultat). Sortie CSV normalisee.

Usage :
  python3 detecter_signal.py --type funding --pays FR --periode last_30d --round "Seed,Series A" --limite 100
  python3 detecter_signal.py --type job-changes --pays FR --positions "ceo,vp of sales" --periode last_14d --limite 50
  python3 detecter_signal.py --type hiring --pays FR --search "SDR" --departements sales --periode last_7d --limite 100
  python3 detecter_signal.py --type acquisitions --pays FR,BE --periode last_90d --limite 50
  python3 detecter_signal.py --type job-changes --liste-suivie 05_Departements/Go-to-Market/Signaux/comptes-suivis.csv --periode last_30d --limite 100
  python3 detecter_signal.py --type job-changes --liste-suivie comptes.csv --par-cible     (une requete par entreprise suivie)
Ajoutez --dry-run pour voir l'input et le cout. --pages N enchaine N pages de --limite resultats.

Mode "liste suivie" : --liste-suivie <csv> lit les colonnes linkedin_entreprise_url, domaine, entreprise et linkedin_url
du fichier et ne garde que les signaux qui concernent ces entreprises ou ces personnes (filtre apres coup, donc le
cout est celui du run complet). --par-cible (job-changes) lance une requete exacte par entreprise suivie a la place.
Sortie : 05_Departements/Go-to-Market/Signaux/detecter-signaux_<type>-<source>-<sujet>_<date>.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (PredictLeads, TheirStack, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, dossier_gtm, domaine, ecrire_csv, fraicheur, lire_csv,  # noqa: E402
                        norm_linkedin_url, norm_texte, seniorite_depuis_titre)
from apify_run import lancer, prix  # noqa: E402

VERBE = "detecter-signaux"
ACTOR = "signalbase/signalbase-api"
TYPES = ["funding", "acquisitions", "hiring", "job-changes", "investors", "companies", "events", "intent"]
# valeur canonique de signal_type par type demande (docs/conventions-gtm.md section 8)
SIGNAL_TYPE_CANON = {"funding": "levee", "acquisitions": "acquisition", "hiring": "offre_emploi", "job-changes": "changement_poste",
                     "investors": "investisseur", "companies": "profil_entreprise", "intent": "intent"}
# quelle source sait faire quel type
SOURCES_PAR_TYPE = {
    "signalbase": ["funding", "acquisitions", "hiring", "job-changes", "investors", "companies"],
    "predictleads": ["funding", "events", "hiring"],
    "theirstack": ["hiring", "intent"],
}
# categories d'evenements PredictLeads utiles a la prospection (news_events)
CATEGORIES_EVENTS = ("expands_offices_to,expands_offices_in,opens_new_location,expands_facilities,increases_headcount_by,"
                     "hires,promotes,leaves,partners_with,integrates_with,launches,is_developing,receives_award,recognized_as,"
                     "signs_new_client,invests_into,acquires,merges_with,goes_public,spins_off_company,spins_off_division")
# la liste complete des categories PredictLeads (news_events) : acquires, merges_with, sells_assets_to, loses_client,
# signs_new_client, declares_bankruptcy, files_suit_against, has_issues_with, closes_offices_in, decreases_headcount_by,
# attends_event, expands_facilities, expands_offices_in, expands_offices_to, increases_headcount_by, opens_new_location,
# goes_public, has_earnings, has_revenue, has_valuation, invests_into, invests_into_assets, receives_financing, hires,
# leaves, promotes, retires_from, integrates_with, is_developing, launches, ends_partnership_with, partners_with,
# receives_award, recognized_as, identified_as_competitor_of, spins_off_company, spins_off_division
PERIODES = ["today", "yesterday", "last_7d", "last_14d", "last_30d", "last_60d", "last_90d", "last_6m", "last_1y", "last_2y",
            "this_week", "this_month", "this_quarter", "this_year", "last_week", "last_month", "last_quarter", "last_year"]


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


def _split_nom(nom: str):
    nom = (nom or "").strip()
    parts = nom.split(" ", 1)
    return (parts[0], parts[1]) if len(parts) > 1 else (nom, "")


def _montant(v) -> str:
    """L'API compte en cents de dollar : on rend des dollars."""
    try:
        n = float(v)
    except (TypeError, ValueError):
        return ""
    return f"{n / 100:.0f}"


def _date(*vals) -> str:
    for v in vals:
        if v:
            return str(v)[:10]
    return ""


def normaliser(it: dict, typ: str) -> dict:
    base = {"source": ACTOR, "date_extraction": aujourd_hui(), "signal_type": SIGNAL_TYPE_CANON.get(typ, typ), "signal_id": _g(it, "signalId", "id")}
    if typ == "funding":
        inv = it.get("investors") or []
        inv = ", ".join((i.get("name") if isinstance(i, dict) else str(i)) for i in inv[:4])
        montant = _montant(it.get("amount"))
        return {**base, "entreprise": _g(it, "companyName"), "domaine": domaine(_g(it, "companyWebsite")),
                "linkedin_entreprise_url": norm_linkedin_url(_g(it, "companyLinkedin", "companyLinkedinUrl")),
                "pays": _g(it, "companyCountry"), "secteur": _g(it, "companyIndustry"), "effectif": _g(it, "companyEmployeeCount"),
                "signal_date": _date(it.get("announcedDate"), it.get("occurredAt")),
                "signal_detail": f"levee {_g(it, 'roundType') or '?'} {montant + ' $' if montant else ''}".strip() + (f" ({inv})" if inv else ""),
                "round": _g(it, "roundType"), "montant_usd": montant, "devise_annoncee": _g(it, "currency"), "investisseurs": inv,
                "verification": _g(it, "verificationStatus"), "url_source": _g((it.get("sources") or [{}])[0] if isinstance(it.get("sources"), list) else {}, "url"),
                "annee_creation": _g(it, "companyFoundedYear"), "description": (_g(it, "companyDescription") or "")[:300]}
    if typ == "acquisitions":
        montant = _montant(it.get("amount"))
        return {**base, "entreprise": _g(it, "companyName"), "domaine": domaine(_g(it, "companyWebsite")),
                "linkedin_entreprise_url": norm_linkedin_url(_g(it, "companyLinkedin", "companyLinkedinUrl")),
                "pays": _g(it, "companyCountry"), "secteur": _g(it, "companyIndustry"), "effectif": _g(it, "companyEmployeeCount"),
                "signal_date": _date(it.get("announcedDate"), it.get("occurredAt")),
                "signal_detail": f"rachetee par {_g(it, 'acquiringCompanyName') or '?'}" + (f" ({montant} $)" if montant else ""),
                "acquereur": _g(it, "acquiringCompanyName"), "acquereur_domaine": domaine(_g(it, "acquiringCompanyWebsite")),
                "acquereur_linkedin_url": norm_linkedin_url(_g(it, "acquiringCompanyLinkedin")), "montant_usd": montant,
                "url_source": _g((it.get("sources") or [{}])[0] if isinstance(it.get("sources"), list) else {}, "url")}
    if typ == "hiring":
        return {**base, "entreprise": _g(it, "companyName"), "domaine": domaine(_g(it, "companyWebsite")),
                "ville": _g(it, "city"), "pays": _g(it, "country", "companyCountry"), "secteur": _g(it, "companyIndustry"),
                "effectif": _g(it, "companyEmployeeCount"), "signal_date": _date(it.get("datePosted"), it.get("createdAt")),
                "signal_detail": f"offre : {_g(it, 'title')} ({_g(it, 'location') or _g(it, 'city')})",
                "poste": _g(it, "title"), "url_offre": _g(it, "jobUrl"), "seniorite_offre": _g(it, "seniorityLevel"),
                "fonction": _g(it, "jobFunction"), "type_contrat": _g(it, "employmentType"), "nb_candidats": _g(it, "numApplicants")}
    if typ == "job-changes":
        prenom, nom = _split_nom(_g(it, "personName"))
        titre = _g(it, "newRole")
        return {**base, "prenom": prenom, "nom": nom, "titre": titre, "seniorite": seniorite_depuis_titre(titre),
                "entreprise": _g(it, "companyName"), "domaine": domaine(_g(it, "companyWebsite")),
                "linkedin_url": norm_linkedin_url(_g(it, "personLinkedinUrl")),
                "linkedin_entreprise_url": norm_linkedin_url(_g(it, "companyLinkedinUrl")),
                "pays": _g(it, "companyCountry"), "secteur": _g(it, "companyIndustry"), "effectif": _g(it, "companyEmployeeCount"),
                "signal_date": _date(it.get("occurredAt"), it.get("discoveredAt")),
                "signal_detail": f"{_g(it, 'personName')} devient {titre or '?'} chez {_g(it, 'companyName')}",
                "post_annonce": (_g(it, "postContent") or "")[:300]}
    if typ == "investors":
        return {**base, "entreprise": _g(it, "name"), "domaine": domaine(_g(it, "website")),
                "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedinUrl")), "pays": ", ".join(it.get("countries") or []),
                "ville": _g(it, "headquarters"), "signal_date": _date(it.get("createdAt")),
                "signal_detail": f"investisseur {_g(it, 'type')} ticket {_g(it, 'ticketSizeMin')}-{_g(it, 'ticketSizeMax')} $",
                "type_investisseur": _g(it, "type")}
    return {**base, "entreprise": _g(it, "name"), "domaine": domaine(_g(it, "website")),
            "linkedin_entreprise_url": norm_linkedin_url(_g(it, "linkedinUrl")), "pays": _g(it, "headquartersCountry"),
            "secteur": _g(it, "industry"), "effectif": _g(it, "employeeCount"), "signal_date": _date(it.get("updatedAt"), it.get("createdAt")),
            "signal_detail": (_g(it, "description") or "")[:200], "annee_creation": _g(it, "foundedYear"),
            "mots_cles": ", ".join(it.get("keywords") or [])[:200]}


def sortie_signaux(nom: str) -> Path:
    """Les runs de signaux vont dans 05_Departements/Go-to-Market/Signaux/."""
    d = dossier_gtm() / "Signaux"
    d.mkdir(parents=True, exist_ok=True)
    return d / chemin_sortie(VERBE, nom).name


def _pl_base(it: dict) -> dict:
    """Champs entreprise communs a tous les datasets PredictLeads (company_lite fusionne par aplatir)."""
    return {"entreprise": _g(it, "company_company_name", "company_friendly_company_name"),
            "domaine": _g(it, "company_domain"),
            "linkedin_entreprise_url": _g(it, "company_linkedin_url"),
            "pays": _g(it, "company_location", "company_country"),
            "effectif": _g(it, "company_size", "company_employee_count"),
            "source": "predictleads", "signal_id": f"pl-{_g(it, '_id')}"}


def normaliser_predictleads(it: dict, typ: str) -> dict:
    l = _pl_base(it)
    d = _date(_g(it, "first_seen_at"), _g(it, "found_at"), _g(it, "date"))
    if typ == "funding":
        l.update({"signal_type": "levee", "signal_date": d, "round": _g(it, "financing_type_normalized", "financing_type"),
                  "montant_usd": _g(it, "amount_normalized", "amount"), "url_source": _g(it, "article_url", "url"),
                  "signal_detail": f"{_g(it, 'financing_type')} {_g(it, 'amount')} {_g(it, 'currency')} ({d})".strip()})
    elif typ == "events":
        cat = _g(it, "category")
        l.update({"signal_type": f"evenement:{cat}" if cat else "evenement", "signal_date": d, "categorie": cat,
                  "url_source": _g(it, "article_url", "url"), "signal_detail": _g(it, "summary", "title", "article_title")[:300]})
    elif typ == "hiring":
        l.update({"signal_type": "offre_emploi", "signal_date": d, "poste": _g(it, "title"), "url_offre": _g(it, "url"),
                  "seniorite_offre": _g(it, "seniority"), "ville": _g(it, "location"),
                  "signal_detail": f"{_g(it, 'title')}, {_g(it, 'location')} ({d})"})
    return l


def normaliser_theirstack(it: dict, typ: str) -> dict:
    c = it.get("company_object") or it.get("company") or {}
    if not isinstance(c, dict):
        c = {}
    l = {"entreprise": _g(c, "name") or _g(it, "company_name", "name"), "domaine": _g(c, "domain") or _g(it, "domain"),
         "linkedin_entreprise_url": _g(c, "linkedin_url") or _g(it, "linkedin_url"), "pays": _g(c, "country_code") or _g(it, "country_code"),
         "effectif": _g(c, "employee_count") or _g(it, "employee_count"), "secteur": _g(c, "industry") or _g(it, "industry"),
         "source": "theirstack", "signal_id": f"ts-{_g(it, 'id')}"}
    if typ == "hiring":
        d = _date(_g(it, "date_posted"), _g(it, "discovered_at"))
        l.update({"signal_type": "offre_emploi", "signal_date": d, "poste": _g(it, "job_title"), "url_offre": _g(it, "url", "final_url"),
                  "seniorite_offre": _g(it, "seniority"), "ville": _g(it, "location", "short_location"),
                  "technos_offre": "|".join(it.get("technology_slugs") or []),
                  "signal_detail": f"{_g(it, 'job_title')}, {_g(it, 'location')} ({d})"})
    else:  # intent : entreprise avec techno cible et offres ouvertes
        techs = it.get("technology_slugs") or [x.get("slug") if isinstance(x, dict) else x for x in (it.get("technologies") or [])]
        l.update({"signal_type": "intent", "signal_date": aujourd_hui(), "nb_offres": _g(it, "num_jobs_found", "num_jobs"),
                  "technos": "|".join([x for x in techs if x][:30]),
                  "signal_detail": f"{_g(it, 'num_jobs_found', 'num_jobs')} offre(s) ouverte(s), technos : {', '.join([x for x in techs if x][:6])}"})
    return l


def lancer_predictleads(a) -> list[dict]:
    dataset = {"funding": "financing_events", "events": "news_events", "hiring": "job_openings"}[a.type]
    params = {}
    if a.du:
        params["first_seen_at_from" if a.type != "hiring" else "found_at_from"] = a.du
    if a.au and a.type != "hiring":
        params["first_seen_at_until"] = a.au
    if a.pays:
        params["company_location"] = {"FR": "France", "BE": "Belgium", "CH": "Switzerland", "LU": "Luxembourg", "US": "United States", "GB": "United Kingdom", "DE": "Germany", "ES": "Spain", "IT": "Italy"}.get(a.pays.split(",")[0].upper(), a.pays)
    if a.taille_equipe:
        params["company_sizes"] = a.taille_equipe
    if a.type == "funding" and a.round:
        params["financing_types_normalized"] = ",".join(r.strip().lower().replace(" ", "_") for r in a.round.split(","))
    if a.type == "events":
        params["categories"] = a.categories.replace("|", ",") if a.categories else CATEGORIES_EVENTS
    if a.type == "hiring":
        if a.search:
            params["title"] = a.search
        if a.ville or a.pays:
            params["location"] = a.ville or params.get("company_location", "")
        params["active_only"] = "true"
        if a.seniorites:
            params["seniority"] = a.seniorites
    if a.dry_run:
        bandeau_dry_run("PredictLeads discover " + dataset, [f"params : {params}", f"pages : {a.pages} x limit {a.limite}",
                                                            "cout : compte sur le quota mensuel de requetes de l'abonnement, pas de credit par resultat"])
        return []
    pl = PredictLeads()
    items = []
    for p in range(1, a.pages + 1):
        lot = pl.discover(dataset, params, page=p, limit=a.limite)
        items += lot
        if len(lot) < a.limite:
            break
    return [normaliser_predictleads(it, a.type) for it in items]


def lancer_theirstack(a) -> list[dict]:
    if a.type == "hiring":
        body = {"posted_at_max_age_days": {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_60d": 60, "last_90d": 90}.get(a.periode or "", 30),
                "order_by": [{"field": "date_posted", "desc": True}]}
        if a.pays:
            body["job_country_code_or"] = [c.strip().upper() for c in a.pays.split(",")]
        if a.search:
            body["job_title_pattern_or"] = [s.strip() for s in a.search.split(",")]
        if a.seniorites:
            body["job_seniority_or"] = [s.strip() for s in a.seniorites.split(",")]
        if a.effectif_min:
            body["min_employee_count"] = a.effectif_min
        if a.effectif_max:
            body["max_employee_count"] = a.effectif_max
        if a.technos:
            body["job_technology_slug_or"] = [s.strip() for s in a.technos.split(",")]
        chemin = "/jobs/search"
    else:  # intent
        body = {"min_num_jobs_found": a.nb_offres_min or 1, "order_by": [{"field": "num_jobs_found", "desc": True}]}
        if a.pays:
            body["company_country_code_or"] = [c.strip().upper() for c in a.pays.split(",")]
        if a.technos:
            body["company_technology_slug_or"] = [s.strip() for s in a.technos.split(",")]
        if a.effectif_min:
            body["min_employee_count"] = a.effectif_min
        if a.effectif_max:
            body["max_employee_count"] = a.effectif_max
        if a.secteur:
            body["industry_or"] = [s.strip() for s in a.secteur.split(",")]
        chemin = "/companies/search"
    import os
    if a.dry_run and not os.environ.get("THEIRSTACK_API_KEY"):
        from gtm_common import load_env
        load_env()
    if a.dry_run and not os.environ.get("THEIRSTACK_API_KEY"):
        bandeau_dry_run("TheirStack " + chemin, [f"body : {body}", f"pages : {a.pages} x limit {a.limite}",
                                                 f"cout : au plus {a.limite * a.pages} credit(s) (1 par resultat) ; cle absente, comptage impossible"])
        return []
    ts = TheirStack()
    total = ts.compter(chemin, body)
    afficher(f"  [theirstack] {total} resultat(s) disponibles ; {min(total, a.limite * a.pages)} seront factures (1 credit chacun)")
    if a.dry_run:
        bandeau_dry_run("TheirStack " + chemin, [f"body : {body}", f"pages : {a.pages} x limit {a.limite}", f"cout : {min(total, a.limite * a.pages)} credit(s)"])
        return []
    items = []
    for p in range(a.pages):
        lot = ts.jobs(body, a.limite, p) if a.type == "hiring" else ts.entreprises(body, a.limite, p)
        items += lot
        if len(lot) < a.limite:
            break
    return [normaliser_theirstack(it, a.type) for it in items]



def construire_input(a) -> dict:
    e = {"signalType": a.type, "limit": min(a.limite, 100), "sort_order": "desc"}
    if a.periode:
        e["date_preset"] = a.periode
    if a.du:
        e["dateFrom"] = a.du
    if a.au:
        e["dateTo"] = a.au
    for cle, val in (("countries", a.pays), ("round", a.round), ("positions", a.positions), ("seniorities", a.seniorites),
                     ("departments", a.departements), ("search", a.search), ("industry", a.secteur), ("categories", a.categories),
                     ("subcategories", a.sous_categories), ("company_name", a.entreprise), ("investor_name", a.investisseur),
                     ("city", a.ville), ("team_size", a.taille_equipe), ("type", a.type_investisseur), ("round_flavor", a.round_flavor)):
        if val:
            e[cle] = val
    if a.montant_min:
        e["amount_min"] = int(float(a.montant_min) * 100)
    if a.montant_max:
        e["amount_max"] = int(float(a.montant_max) * 100)
    if a.effectif_min:
        e["employee_count_min"] = a.effectif_min
    if a.effectif_max:
        e["employee_count_max"] = a.effectif_max
    if a.personne_linkedin_url:
        e["personLinkedinUrl"] = a.personne_linkedin_url
    if a.entreprise_linkedin_url:
        e["companyLinkedinUrl"] = a.entreprise_linkedin_url
    if getattr(a, "verification", None):
        e["verification_status"] = a.verification
    return e


def charger_suivis(chemin: str) -> dict:
    urls_e, doms, noms, urls_p = set(), set(), set(), set()
    for l in lire_csv(chemin):
        u = norm_linkedin_url(l.get("linkedin_entreprise_url"))
        if u:
            urls_e.add(u)
        d = domaine(l.get("domaine") or l.get("site_web") or "")
        if d:
            doms.add(d)
        if l.get("entreprise"):
            noms.add(norm_texte(l["entreprise"]))
        p = norm_linkedin_url(l.get("linkedin_url"))
        if p:
            urls_p.add(p)
    return {"urls_e": urls_e, "doms": doms, "noms": noms, "urls_p": urls_p}


def concerne(ligne: dict, suivis: dict) -> bool:
    return bool((ligne.get("linkedin_entreprise_url") and ligne["linkedin_entreprise_url"] in suivis["urls_e"])
                or (ligne.get("domaine") and ligne["domaine"] in suivis["doms"])
                or (ligne.get("entreprise") and norm_texte(ligne["entreprise"]) in suivis["noms"])
                or (ligne.get("linkedin_url") and ligne["linkedin_url"] in suivis["urls_p"]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", choices=TYPES, required=True)
    ap.add_argument("--source", choices=["signalbase", "predictleads", "theirstack"], default="signalbase",
                    help="signalbase (Apify, defaut), predictleads (levees, events, offres), theirstack (offres, intent)")
    ap.add_argument("--technos", help="theirstack : slugs de technos, ex : hubspot,salesforce")
    ap.add_argument("--nb-offres-min", type=int, help="intent (theirstack) : nombre minimum d'offres ouvertes")
    ap.add_argument("--pays", help="codes ISO separes par des virgules : FR,BE,CH")
    ap.add_argument("--periode", choices=PERIODES, help="fenetre relative (prime sur --du/--au)")
    ap.add_argument("--du", help="YYYY-MM-DD")
    ap.add_argument("--au", help="YYYY-MM-DD")
    ap.add_argument("--round", help="funding : Pre-Seed,Seed,Series A,Series B,...")
    ap.add_argument("--round-flavor", help="funding : bridge,extension,secondary")
    ap.add_argument("--montant-min", help="funding : montant minimum en dollars (converti en cents pour l'API)")
    ap.add_argument("--montant-max")
    ap.add_argument("--positions", help="job-changes : ceo,cto,cfo,coo,vp of sales,vp of marketing,head of growth,founder,...")
    ap.add_argument("--seniorites", help="founder,c_level,vp,director,head,lead,manager")
    ap.add_argument("--departements", help="hiring : marketing,sales,engineering,product,operations,finance,people,growth,...")
    ap.add_argument("--search", help="texte libre (nom, secteur, intitule)")
    ap.add_argument("--secteur", help="industry : noms exacts separes par des virgules")
    ap.add_argument("--categories", help="Technology|Healthcare (separateur |)")
    ap.add_argument("--sous-categories", help="ai,saas,fintech,marketing,sales,...")
    ap.add_argument("--entreprise", help="filtre company_name (partiel)")
    ap.add_argument("--investisseur", help="funding : investor_name (partiel)")
    ap.add_argument("--ville", help="hiring : ville")
    ap.add_argument("--taille-equipe", help="hiring : 1-10,11-50,51-200,201-1000,1000-plus")
    ap.add_argument("--type-investisseur", help="investors : vc,angel,pe,corporate,accelerator,...")
    ap.add_argument("--effectif-min", type=int)
    ap.add_argument("--effectif-max", type=int)
    ap.add_argument("--personne-linkedin-url", help="job-changes : URL exacte d'une personne")
    ap.add_argument("--entreprise-linkedin-url", help="job-changes : URL exacte d'une entreprise")
    ap.add_argument("--verification", help="signalbase : verified,unverified,pending (verification_status)")
    ap.add_argument("--limite", type=int, default=50, help="resultats par page (max 100)")
    ap.add_argument("--pages", type=int, default=1, help="nombre de pages a enchainer")
    ap.add_argument("--liste-suivie", help="CSV d'entreprises ou de personnes : ne garder que les signaux qui les concernent")
    ap.add_argument("--par-cible", action="store_true", help="job-changes : une requete exacte par entreprise (linkedin_entreprise_url) et par personne (linkedin_url) de la liste suivie")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.type not in SOURCES_PAR_TYPE[a.source]:
        arret(f"--type {a.type} n'existe pas chez {a.source}. Sources possibles pour ce type : "
              + ", ".join(s for s, ts in SOURCES_PAR_TYPE.items() if a.type in ts))
    suivis = charger_suivis(a.liste_suivie) if a.liste_suivie else None
    if a.source != "signalbase":
        lignes = lancer_predictleads(a) if a.source == "predictleads" else lancer_theirstack(a)
        if a.dry_run:
            return
        vus, garde = set(), []
        for l in lignes:
            l["fraicheur"] = fraicheur(l.get("signal_date"))
            cle = l.get("signal_id") or f"{l.get('entreprise')}|{l.get('signal_date')}|{l.get('signal_detail')}"
            if cle in vus or (suivis and not concerne(l, suivis)):
                continue
            vus.add(cle)
            garde.append(l)
        sujet = a.sujet or (a.pays or "") + ("-" + (a.search or a.technos or "").split(",")[0] if (a.search or a.technos) else "")
        sortie = Path(a.out) if a.out else sortie_signaux(f"{a.type}-{a.source}-{sujet}" if sujet else f"{a.type}-{a.source}")
        ecrire_csv(garde, sortie)
        afficher(f"{len(garde)} signal(aux) {a.type} via {a.source}" + (" (liste suivie)" if suivis else "") + f" -> {sortie}")
        return
    entrees = []
    if a.par_cible:
        if a.type != "job-changes" or not suivis:
            arret("--par-cible ne vaut que pour --type job-changes avec --liste-suivie (colonnes linkedin_entreprise_url ou linkedin_url)")
        for u in sorted(suivis["urls_e"]):
            a.entreprise_linkedin_url, a.personne_linkedin_url = u, None
            entrees.append(construire_input(a))
        for u in sorted(suivis.get("urls_p", set())):
            a.entreprise_linkedin_url, a.personne_linkedin_url = None, u
            entrees.append(construire_input(a))
        if not entrees:
            arret("aucune linkedin_entreprise_url ni linkedin_url dans la liste suivie")
    else:
        base = construire_input(a)
        for p in range(1, a.pages + 1):
            e = dict(base)
            if p > 1:
                e["page"] = p
            entrees.append(e)
    total_max = sum(e["limit"] for e in entrees)
    estimation = prix(ACTOR, total_max)
    afficher(f"  [signalbase] {len(entrees)} requete(s), jusqu'a {total_max} resultats : {estimation}")

    vus, lignes = set(), []
    for n, e in enumerate(entrees, 1):
        items, _ = lancer(ACTOR, e, label=f"{a.type} {n}/{len(entrees)}", dry_run=a.dry_run, estimation=prix(ACTOR, e["limit"]))
        if a.dry_run and n >= 2:
            if len(entrees) > 2:
                afficher(f"  [dry-run] ... {len(entrees) - 2} autre(s) requete(s) identique(s) sur d'autres cibles ou pages")
            break
        for it in items:
            ligne = normaliser(it, a.type)
            ligne["fraicheur"] = fraicheur(ligne.get("signal_date"))
            cle = ligne.get("signal_id") or f"{ligne.get('entreprise')}|{ligne.get('signal_date')}|{ligne.get('signal_detail')}"
            if cle in vus:
                continue
            vus.add(cle)
            if suivis and not a.par_cible and not concerne(ligne, suivis):
                continue
            lignes.append(ligne)
    if a.dry_run:
        return
    sujet = a.sujet or (a.pays or "") + ("-" + (a.search or a.round or a.positions or "").split(",")[0] if (a.search or a.round or a.positions) else "")
    sortie = Path(a.out) if a.out else sortie_signaux(f"{a.type}-signalbase-{sujet}" if sujet else f"{a.type}-signalbase")
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} signal(aux) {a.type}" + (" (liste suivie)" if suivis else "") + f" -> {sortie}")


if __name__ == "__main__":
    main()
