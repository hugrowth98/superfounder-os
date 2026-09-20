#!/usr/bin/env python3
"""trouver_url_linkedin : retrouve l'URL LinkedIn d'une ou plusieurs personnes a partir du prenom, du nom et de l'entreprise.

Sources (--source) :
  unipile   recherche de personnes avec le compte LinkedIn de l'utilisateur (abonnement, pas de credit) ; defaut si Unipile est branche
  google    Apify apify/google-search-scraper : une requete Google "Prenom Nom" Entreprise site:linkedin.com/in par personne,
            0,0025 $ par page + 0,001 $ par run, sans compte LinkedIn ; defaut sinon, ou --source google
Sans --source : unipile si les cles sont dans .env, google sinon.

Entree : --in <csv> (colonnes prenom, nom, entreprise ; les lignes avec linkedin_url deja rempli sont sautees) ou --nom "Prenom Nom" [--entreprise X].
Sortie : le meme CSV avec linkedin_url, linkedin_confiance (haute, moyenne, faible, aucune), linkedin_entreprise_match (oui, partiel, non),
linkedin_titre_trouve, linkedin_source. Une confiance faible se relit a la main avant tout usage.

Exemples :
  python3 trouver_url_linkedin.py --nom "Hugo Dollfus" --entreprise "Growth Hiring"
  python3 trouver_url_linkedin.py --in contacts.csv --dry-run
  python3 trouver_url_linkedin.py --in contacts.csv --source google --pays fr
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (Unipile, afficher, aujourd_hui, arret, bandeau_dry_run, chemin_sortie, ecrire_csv, env, lire_csv,  # noqa: E402
                        norm_linkedin_url, norm_texte, sujet_depuis_fichier)
from apify_run import lancer, prix  # noqa: E402

VERBE = "trouver-url-linkedin"
ACTOR = "apify/google-search-scraper"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def personnes_depuis(a) -> list[dict]:
    if a.nom:
        prenom, _, nom = a.nom.strip().partition(" ")
        return [{"prenom": prenom, "nom": nom, "entreprise": a.entreprise or ""}]
    if not a.entree:
        arret("donnez --nom \"Prenom Nom\" (et --entreprise) ou --in <csv avec prenom, nom, entreprise>")
    return lire_csv(a.entree)


def a_traiter(lignes: list[dict], forcer: bool) -> list[int]:
    return [i for i, l in enumerate(lignes) if (l.get("prenom") or "").strip() and (l.get("nom") or "").strip()
            and (forcer or not (l.get("linkedin_url") or "").strip())]


def confiance(prenom: str, nom: str, entreprise: str, texte: str, entreprise_trouvee: str) -> tuple[str, str]:
    """(confiance, match entreprise) : haute si prenom et nom sont dans le texte du resultat, moyenne si un seul, faible sinon."""
    t = _norm(texte)
    tokens = [x for x in _norm(f"{prenom} {nom}").split() if len(x) > 1]
    trouves = [x for x in tokens if x in t]
    conf = "haute" if len(tokens) >= 2 and len(trouves) == len(tokens) else ("moyenne" if trouves else "faible")
    ent = _norm(entreprise)
    match = ""
    if ent:
        toks = [x for x in ent.split() if len(x) > 2]
        cible = _norm(entreprise_trouvee) + " " + t
        if toks and all(x in cible for x in toks):
            match = "oui"
        elif toks and any(x in cible for x in toks):
            match = "partiel"
        else:
            match = "non"
    return conf, match


def poser(l: dict, url: str, conf: str, match: str, titre: str, source: str) -> None:
    l["linkedin_url"] = norm_linkedin_url(url) if url else ""
    l["linkedin_confiance"] = conf if url else "aucune"
    l["linkedin_entreprise_match"] = match if url else ""
    l["linkedin_titre_trouve"] = (titre or "")[:150]
    l["linkedin_source"] = source
    l["date_extraction"] = l.get("date_extraction") or aujourd_hui()


# ------------------------------------------------------------------ Unipile

def via_unipile(lignes: list[dict], idx: list[int], a) -> None:
    if a.dry_run:
        bandeau_dry_run("Unipile recherche de personnes (classique)", [f"{len(idx)} personne(s), une recherche chacune : \"Prenom Nom Entreprise\"",
                                                                       "cout : abonnement Unipile, pas de credit"])
        return
    u = Unipile()
    for n, i in enumerate(idx, 1):
        l = lignes[i]
        mots = f"{l['prenom']} {l['nom']} {l.get('entreprise') or ''}".strip()
        try:
            items = u.recherche(api="classic", categorie="people", mots_cles=mots, max_resultats=5)
        except Exception as e:  # noqa: BLE001
            poser(l, "", "", "", f"erreur : {e}"[:120], "unipile")
            continue
        meilleur, best = None, ("", "")
        for it in items:
            nom_complet = it.get("name") or f"{it.get('first_name', '')} {it.get('last_name', '')}"
            pos = it.get("current_positions") or []
            pos = pos[0] if isinstance(pos, list) and pos else {}
            texte = f"{nom_complet} {it.get('headline') or ''} {pos.get('company') or ''}"
            conf, match = confiance(l["prenom"], l["nom"], l.get("entreprise") or "", texte, pos.get("company") or "")
            score = {"haute": 2, "moyenne": 1, "faible": 0}[conf] * 2 + {"oui": 2, "partiel": 1}.get(match, 0)
            if meilleur is None or score > meilleur[0]:
                url = it.get("profile_url") or it.get("public_profile_url") or (f"https://www.linkedin.com/in/{it['public_identifier']}" if it.get("public_identifier") else "")
                meilleur, best = (score, url, texte), (conf, match)
        if meilleur and meilleur[1]:
            poser(l, meilleur[1], best[0], best[1], meilleur[2], "unipile")
        else:
            poser(l, "", "", "", "", "unipile")
        if n % 20 == 0:
            afficher(f"  [unipile] {n}/{len(idx)}")


# ------------------------------------------------------------------ Google (Apify)

def via_google(lignes: list[dict], idx: list[int], a) -> None:
    requetes = []
    for i in idx:
        l = lignes[i]
        ent = (l.get("entreprise") or "").strip()
        requetes.append(f"\"{l['prenom'].strip()} {l['nom'].strip()}\"" + (f" {ent}" if ent else "") + " site:linkedin.com/in")
    entree = {"queries": "\n".join(requetes), "maxPagesPerQuery": 1, "countryCode": a.pays, "languageCode": a.pays if a.pays in ("fr", "en", "de", "es", "it") else "en",
              "saveHtml": False, "saveHtmlToKeyValueStore": False, "includeIcons": False}
    items, _ = lancer(ACTOR, entree, label=f"google-linkedin ({len(requetes)} requetes)", dry_run=a.dry_run, estimation=prix(ACTOR, len(requetes)))
    if a.dry_run:
        return
    par_requete = {}
    for it in items:
        term = ((it.get("searchQuery") or {}).get("term") or "").strip()
        par_requete[_norm(term)] = it
    for i, q in zip(idx, requetes):
        l = lignes[i]
        it = par_requete.get(_norm(q))
        if it is None:
            it = next((v for k, v in par_requete.items() if _norm(f"{l['prenom']} {l['nom']}") in k), None)
        premier = None
        for r in (it or {}).get("organicResults") or []:
            if "linkedin.com/in" in (r.get("url") or ""):
                premier = r
                break
        if not premier:
            poser(l, "", "", "", "", ACTOR)
            continue
        pi = premier.get("personalInfo") or {}
        texte = f"{premier.get('title') or ''} {premier.get('description') or ''} {pi.get('rawText') or ''} {' '.join(premier.get('emphasizedKeywords') or [])} {premier.get('url')}"
        conf, match = confiance(l["prenom"], l["nom"], l.get("entreprise") or "", texte, pi.get("companyName") or "")
        poser(l, premier.get("url") or "", conf, match, premier.get("title") or "", ACTOR)


SOURCES = {"unipile": via_unipile, "google": via_google}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", help="CSV avec prenom, nom, entreprise")
    ap.add_argument("--nom", help="une seule personne : \"Prenom Nom\"")
    ap.add_argument("--entreprise", help="avec --nom : son entreprise")
    ap.add_argument("--source", choices=sorted(SOURCES), help="unipile (compte LinkedIn) ou google (Apify) ; defaut : unipile si branche, sinon google")
    ap.add_argument("--pays", default="fr", help="google : pays de la recherche (code ISO, defaut fr)")
    ap.add_argument("--force", action="store_true", help="refaire aussi les lignes qui ont deja une linkedin_url")
    ap.add_argument("--max", type=int, help="nombre de lignes a traiter au plus")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = personnes_depuis(a)
    idx = a_traiter(lignes, a.force)
    if a.max:
        idx = idx[:a.max]
    if not idx:
        arret("aucune ligne a traiter : il faut prenom et nom, et pas de linkedin_url deja remplie (ou --force)")
    source = a.source
    if not source:
        source = "unipile" if (env("UNIPILE_API_KEY", obligatoire=False) and env("UNIPILE_ACCOUNT_ID", obligatoire=False)) else "google"
        afficher(f"  [source] {source} ({'Unipile branche' if source == 'unipile' else 'pas de compte Unipile dans .env'})")
    afficher(f"  [cibles] {len(idx)} personne(s) a chercher sur {len(lignes)}")
    SOURCES[source](lignes, idx, a)
    if a.dry_run:
        return
    trouves = sum(1 for i in idx if lignes[i].get("linkedin_url"))
    hautes = sum(1 for i in idx if lignes[i].get("linkedin_confiance") == "haute")
    afficher(f"  [resultat] {trouves}/{len(idx)} URL trouvees, dont {hautes} en confiance haute")
    if a.nom:
        l = lignes[0]
        print(l.get("linkedin_url") or "(aucune URL trouvee)", "|", l.get("linkedin_confiance"), "|", l.get("linkedin_titre_trouve"))
        return
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet))
    ecrire_csv(lignes, sortie, colonnes_extra=["linkedin_confiance", "linkedin_entreprise_match", "linkedin_titre_trouve", "linkedin_source"])
    afficher(f"{len(lignes)} lignes -> {sortie}")


if __name__ == "__main__":
    main()
