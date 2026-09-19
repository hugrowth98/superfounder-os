"""scraper_offres_emploi : les offres ouvertes d'un marche ou d'entreprises, une ligne par offre + un agrege par
entreprise (nombre d'offres, delta depuis le dernier run). Apify uniquement.

Sources (--source) :
  linkedin    tagadanar/linkedin-jobs-scraper : mots-cles x lieux, depuis 24h/week/month, ou ids d'entreprises (0,0018 $ par offre)
  indeed      borderline/indeed-scraper : requete + lieu + rayon + jours, pays fr par defaut (0,005 $ par offre)
  signalbase  signalbase/signalbase-api signalType=hiring : un marche entier avec filtres departements, seniorites (0,04 $ par resultat)

Pipeline commun (herite du traitement Indeed) : brut -> filtre "titre exact" (tous les fragments du mot-cle dans le titre,
desactivable par --sans-filtre-titre) -> classement des entreprises : client_final / a_verifier / exclu (cabinets de
recrutement, interim, ESN, ecoles ; liste connue dans intermediaires-exclus.csv, enrichie par --exclure) -> agregat.

Usage :
  python3 scraper_offres_emploi.py --source linkedin --mots-cles "SDR,Business Developer" --lieu Paris --depuis week --max 200
  python3 scraper_offres_emploi.py --source indeed --mots-cles "responsable comptable" --lieu "Lyon" --rayon 25 --jours 7 --max 200
  python3 scraper_offres_emploi.py --source linkedin --entreprises-ids 1441,10667 --max 100      (ids numeriques LinkedIn, f_C= dans l'URL jobs)
  python3 scraper_offres_emploi.py --source signalbase --pays FR --search "SDR" --departements sales --periode last_7d --limite 100
  python3 scraper_offres_emploi.py --source indeed ... --exclure "Cabinet X,Interim Y"       ajoute des intermediaires a la liste connue
Sorties : Listes-prospection/scraper-offres-emploi_<sujet>_<date>.csv (une ligne par offre, toutes, avec statut_entreprise)
          Listes-prospection/scraper-offres-emploi_<sujet>_<date>_par-entreprise.csv (agregat, delta vs historique_offres.json)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (afficher, aujourd_hui, arret, chemin_sortie, domaine, ecrire_csv, fraicheur,  # noqa: E402
                        norm_linkedin_url, norm_texte)
from apify_run import lancer, prix  # noqa: E402

VERBE = "scraper-offres-emploi"
ICI = Path(__file__).resolve().parent
INTERMEDIAIRES = ICI / "intermediaires-exclus.csv"
HISTORIQUE = ICI / "historique_offres.json"
STOPWORDS = {"de", "du", "des", "d", "la", "le", "les", "l", "et", "en", "h", "f", "hf", "x", "a", "au", "aux", "of", "the"}
MOTS_INTERMEDIAIRE = ["recrut", "interim", "staffing", "talents", "talent ", "rh ", " rh", "-rh", "search", "headhunt", "chasseur",
                      "portage", "freelance", "temps partage", "job ", "emploi", "carriere", "career", "cfa", "alternance", "ecole",
                      "formation", "campus", "academy", "esn", "consulting", "conseil"]


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


def stems(mot: str, n: int = 6) -> list[str]:
    return [w[:n] for w in norm_texte(mot).split() if w not in STOPWORDS and len(w) > 1]


def titre_match(titre: str, mots_cles: list[str]) -> bool:
    t = norm_texte(titre)
    return any(all(s in t for s in stems(m)) for m in mots_cles if stems(m))


def charger_intermediaires() -> dict:
    if not INTERMEDIAIRES.exists():
        return {}
    with open(INTERMEDIAIRES, encoding="utf-8-sig", newline="") as fh:
        return {norm_texte(r["entreprise"]): r for r in csv.DictReader(fh) if r.get("entreprise")}


def ajouter_intermediaires(noms: list[str], raison: str) -> int:
    connus = charger_intermediaires()
    lignes = list(connus.values())
    ajoutes = 0
    for n in noms:
        if n and norm_texte(n) not in connus:
            lignes.append({"entreprise": n, "type": "exclu", "raison": raison})
            connus[norm_texte(n)] = lignes[-1]
            ajoutes += 1
    with open(INTERMEDIAIRES, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["entreprise", "type", "raison"])
        w.writeheader()
        w.writerows(sorted(lignes, key=lambda r: norm_texte(r["entreprise"])))
    return ajoutes


def classer(entreprise: str, secteur: str, connus: dict) -> tuple[str, str]:
    n = norm_texte(entreprise)
    if not n:
        return "exclu", "annonce sans nom d'entreprise"
    padded = f" {n} "
    for k, r in connus.items():
        if k == n or (len(k) >= 4 and f" {k} " in padded):
            return "exclu", f"intermediaire connu : {r.get('type', '')} ({r.get('entreprise', '')})"
    if "staffing" in norm_texte(secteur) or "human resources" in norm_texte(secteur):
        return "exclu", f"secteur {secteur}"
    for mot in MOTS_INTERMEDIAIRE:
        m = norm_texte(mot)
        if m and ((f" {m} " in padded) if len(m) <= 3 else (m in n)):
            return "a_verifier", f"suspect : contient '{m}'"
    return "client_final", ""


# ------------------------------------------------------------------ sources

def source_linkedin(a) -> tuple[list[dict], str]:
    actor = "tagadanar/linkedin-jobs-scraper"
    entree = {"maxResults": a.max, "postedSince": a.depuis, "sortBy": "recent", "scrapeDetails": bool(a.details),
              "workType": a.teletravail or "any", "experienceLevel": a.niveau or "any"}
    if a.url:
        entree["searchUrls"] = _liste(a.url)
    else:
        if a.mots_cles:
            entree["keywords"] = _liste(a.mots_cles)
        if a.lieu:
            entree["location"] = _liste(a.lieu)
        if a.entreprises_ids:
            entree["companyIds"] = _liste(a.entreprises_ids)
        if not (a.mots_cles or a.entreprises_ids):
            arret("linkedin : donnez --mots-cles (et --lieu), --entreprises-ids ou --url")
    items, _ = lancer(actor, entree, label="linkedin-jobs", dry_run=a.dry_run, estimation=prix(actor, a.max))
    lignes = []
    for it in items:
        lignes.append({"plateforme": "linkedin", "poste": _g(it, "title", "jobTitle"), "entreprise": _g(it, "companyName", "company.name", "company"),
                       "linkedin_entreprise_url": norm_linkedin_url(_g(it, "companyUrl", "companyLinkedinUrl", "company.linkedinUrl", "company.url")),
                       "secteur": _g(it, "companyIndustry", "company.industry", "industries"), "ville": _g(it, "location", "jobLocation"),
                       "signal_date": str(_g(it, "postedAt", "postedDate", "listedAt", "datePosted", "publishedAt"))[:10],
                       "url_offre": _g(it, "url", "jobUrl", "link", "applyUrl"), "type_contrat": _g(it, "employmentType", "jobType"),
                       "teletravail": _g(it, "workType", "workplaceType"), "niveau": _g(it, "seniorityLevel", "experienceLevel"),
                       "nb_candidats": _g(it, "applicants", "applicantsCount", "numApplicants"), "source": actor})
    return lignes, actor


def source_indeed(a) -> tuple[list[dict], str]:
    actor = "borderline/indeed-scraper"
    if not a.mots_cles or not a.lieu:
        arret("indeed : --mots-cles et --lieu sont requis")
    urls = []
    for mot in _liste(a.mots_cles):
        params = {"q": mot, "l": a.lieu, "radius": a.rayon}
        if a.jours:
            params["fromage"] = a.jours
        urls.append(f"https://{a.pays_indeed}.indeed.com/jobs?" + urllib.parse.urlencode(params))
    entree = {"urls": urls, "maxRowsPerUrl": a.max, "country": a.pays_indeed, "enableUniqueJobs": True, "includeSimilarJobs": False}
    items, _ = lancer(actor, entree, label="indeed", dry_run=a.dry_run, estimation=prix(actor, a.max * len(urls)))
    lignes = []
    for it in items:
        lignes.append({"plateforme": "indeed", "poste": _g(it, "title"), "entreprise": _g(it, "companyName"),
                       "domaine": domaine(_g(it, "companyLinks.corporateWebsite")), "secteur": _g(it, "companyIndustry"),
                       "effectif": _g(it, "companyNumEmployees"), "ville": _g(it, "location.formattedAddressShort", "location.city"),
                       "signal_date": str(_g(it, "datePublished"))[:10], "url_offre": _g(it, "jobUrl"),
                       "type_contrat": _g(it, "jobType"), "teletravail": "oui" if it.get("isRemote") else "",
                       "salaire": _g(it, "salary.salaryText"), "url_entreprise_indeed": _g(it, "companyUrl"), "source": actor})
    return lignes, actor


def source_signalbase(a) -> tuple[list[dict], str]:
    actor = "signalbase/signalbase-api"
    entree = {"signalType": "hiring", "limit": min(a.limite, 100), "sort_order": "desc"}
    for cle, val in (("countries", a.pays), ("date_preset", a.periode), ("search", a.search), ("departments", a.departements),
                     ("seniorities", a.seniorites), ("city", a.lieu), ("team_size", a.taille_equipe), ("industry", a.secteur)):
        if val:
            entree[cle] = val
    items, _ = lancer(actor, entree, label="signalbase-hiring", dry_run=a.dry_run, estimation=prix(actor, entree["limit"]))
    lignes = []
    for it in items:
        lignes.append({"plateforme": "signalbase", "poste": _g(it, "title"), "entreprise": _g(it, "companyName"),
                       "domaine": domaine(_g(it, "companyWebsite")), "secteur": _g(it, "companyIndustry"),
                       "effectif": _g(it, "companyEmployeeCount"), "ville": _g(it, "city") or _g(it, "location"), "pays": _g(it, "country", "companyCountry"),
                       "signal_date": str(_g(it, "datePosted", "createdAt"))[:10], "url_offre": _g(it, "jobUrl"),
                       "type_contrat": _g(it, "employmentType"), "niveau": _g(it, "seniorityLevel"), "nb_candidats": _g(it, "numApplicants"),
                       "source": actor})
    return lignes, actor


SOURCES = {"linkedin": source_linkedin, "indeed": source_indeed, "signalbase": source_signalbase}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=sorted(SOURCES), required=True)
    ap.add_argument("--sujet", default="")
    ap.add_argument("--mots-cles", help="intitules separes par des virgules (un par recherche)")
    ap.add_argument("--lieu", help="ville, region ou pays (linkedin : plusieurs, separes par des virgules)")
    ap.add_argument("--depuis", choices=["any", "24h", "week", "month"], default="week", help="linkedin")
    ap.add_argument("--teletravail", choices=["on-site", "remote", "hybrid"], help="linkedin")
    ap.add_argument("--niveau", choices=["internship", "entry", "associate", "mid-senior", "director", "executive"], help="linkedin")
    ap.add_argument("--entreprises-ids", help="linkedin : ids numeriques d'entreprises (f_C= dans l'URL jobs)")
    ap.add_argument("--url", help="linkedin : URL(s) de recherche jobs copiee(s) du navigateur")
    ap.add_argument("--details", action="store_true", help="linkedin : description complete (+0,0018 $ par offre)")
    ap.add_argument("--rayon", default="25", help="indeed : km")
    ap.add_argument("--jours", default="7", help="indeed : offres publiees depuis N jours (1,3,7,14 ; vide = toutes)")
    ap.add_argument("--pays-indeed", default="fr", help="indeed : domaine pays (fr, be, ch, uk, us)")
    ap.add_argument("--pays", help="signalbase : codes ISO (FR,BE)")
    ap.add_argument("--periode", default="last_7d", help="signalbase : last_7d, last_30d, ...")
    ap.add_argument("--search", help="signalbase : texte libre")
    ap.add_argument("--departements", help="signalbase : sales,marketing,engineering,product,operations,finance,people,growth")
    ap.add_argument("--seniorites", help="signalbase : founder,c_level,vp,director,head,lead,manager")
    ap.add_argument("--taille-equipe", help="signalbase : 1-10,11-50,51-200,201-1000,1000-plus")
    ap.add_argument("--secteur", help="signalbase : industry")
    ap.add_argument("--limite", type=int, default=100, help="signalbase : resultats (max 100)")
    ap.add_argument("--max", type=int, default=200, help="linkedin / indeed : offres max")
    ap.add_argument("--sans-filtre-titre", action="store_true", help="garder toutes les offres, pas seulement le titre exact")
    ap.add_argument("--exclure", help="noms d'intermediaires a ajouter a la liste connue, separes par des virgules")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.exclure:
        afficher(f"  [intermediaires] {ajouter_intermediaires(_liste(a.exclure), 'ajoute a la main')} ajoute(s) a {INTERMEDIAIRES.name}")
    lignes, actor = SOURCES[a.source](a)
    if a.dry_run:
        return
    sujet = a.sujet or (a.mots_cles or a.search or a.entreprises_ids or a.source).split(",")[0]
    mots = _liste(a.mots_cles) + _liste(a.search)
    total = len(lignes)
    if mots and not a.sans_filtre_titre and a.source != "signalbase":
        lignes = [l for l in lignes if titre_match(l.get("poste", ""), mots)]
    connus = charger_intermediaires()
    for l in lignes:
        st, raison = classer(l.get("entreprise", ""), l.get("secteur", ""), connus)
        l.update({"statut_entreprise": st, "raison_statut": raison, "signal_type": "recrutement",
                  "signal_detail": f"offre : {l.get('poste')} ({l.get('ville') or '?'})", "date_extraction": aujourd_hui(),
                  "fraicheur": fraicheur(l.get("signal_date"))})
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(lignes, sortie)

    # agregat par entreprise + delta vs historique
    hist = json.loads(HISTORIQUE.read_text(encoding="utf-8")) if HISTORIQUE.exists() else {}
    groupes = defaultdict(list)
    for l in lignes:
        if l["statut_entreprise"] != "exclu":
            groupes[norm_texte(l.get("entreprise"))].append(l)
    agreg = []
    for cle, grp in groupes.items():
        if not cle:
            continue
        prev = hist.get(cle, {})
        nb = len(grp)
        postes = sorted({g.get("poste", "") for g in grp})
        agreg.append({"entreprise": grp[0].get("entreprise"), "domaine": next((g.get("domaine") for g in grp if g.get("domaine")), ""),
                      "linkedin_entreprise_url": next((g.get("linkedin_entreprise_url") for g in grp if g.get("linkedin_entreprise_url")), ""),
                      "ville": grp[0].get("ville"), "secteur": grp[0].get("secteur"), "effectif": grp[0].get("effectif"),
                      "source": actor, "date_extraction": aujourd_hui(), "signal_type": "recrutement",
                      "signal_date": max((g.get("signal_date") or "" for g in grp), default=""),
                      "signal_detail": f"{nb} offre(s) : " + " | ".join(postes)[:200], "fraicheur": fraicheur(max((g.get("signal_date") or "" for g in grp), default="")),
                      "nb_offres": nb, "nb_offres_precedent": prev.get("nb", ""), "delta": (nb - prev["nb"]) if prev else "",
                      "premiere_vue": "" if prev else "oui", "dernier_run": prev.get("date", ""),
                      "statut_entreprise": grp[0]["statut_entreprise"], "raison_statut": grp[0]["raison_statut"]})
        hist[cle] = {"nb": nb, "date": aujourd_hui(), "entreprise": grp[0].get("entreprise")}
    agreg.sort(key=lambda r: (-(r["delta"] if isinstance(r["delta"], int) else 0), -r["nb_offres"]))
    sortie2 = sortie.with_name(sortie.stem + "_par-entreprise.csv")
    ecrire_csv(agreg, sortie2)
    HISTORIQUE.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    excl = sum(1 for l in lignes if l["statut_entreprise"] == "exclu")
    verif = sum(1 for l in lignes if l["statut_entreprise"] == "a_verifier")
    afficher(f"{total} offres brutes, {len(lignes)} au titre exact, {excl} chez des intermediaires exclus, {verif} a verifier -> {sortie}")
    afficher(f"{len(agreg)} entreprises (delta calcule contre {HISTORIQUE.name}) -> {sortie2}")


if __name__ == "__main__":
    main()
