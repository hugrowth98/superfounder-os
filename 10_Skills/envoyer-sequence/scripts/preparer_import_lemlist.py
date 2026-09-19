"""preparer_import_lemlist : transforme un CSV normalise en fichier d'import Lemlist (email, firstName, lastName,
companyName, jobTitle, linkedinUrl, phone, icebreaker + variables personnalisees), en ecartant ce qui ne doit pas partir.

Ecarte : exclu = oui, ne_plus_contacter = oui, email vide, email_statut INVALID / INVALID_DOMAIN / NOT_FOUND,
CATCH_ALL sauf --avec-catch-all, statuts non verifies (LINKEDIN_1ER_DEGRE, APIFY_NON_VERIFIE, vide) sauf --sans-verification.
Les colonnes qui commencent par var_ deviennent des variables Lemlist (var_preuve -> preuve). --colonne-message indique
la colonne qui contient le message personnalise (variable icebreaker par defaut).

Usage :
  python3 preparer_import_lemlist.py --in liste.csv --colonne-message icebreaker [--avec-catch-all] [--sujet x]
Sortie : Listes-prospection/envoyer-sequence_<sujet>_<date>_lemlist.csv + apercu de 3 lignes (a montrer avant l'import).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import afficher, arret, chemin_sortie, lire_csv, norm_linkedin_url, sujet_depuis_fichier  # noqa: E402

VERBE = "envoyer-sequence"
FIABLES = {"DELIVERABLE", "HIGH_PROBABILITY"}
INVALIDES = {"INVALID", "INVALID_DOMAIN", "NOT_FOUND", "BOUNCE", "BOUNCED"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--colonne-message", default="icebreaker", help="colonne du message personnalise (variable Lemlist du meme nom)")
    ap.add_argument("--avec-catch-all", action="store_true")
    ap.add_argument("--sans-verification", action="store_true", help="accepter les emails non verifies (deconseille)")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    gardees, raisons = [], {}
    for l in lignes:
        email = (l.get("email") or "").strip().lower()
        statut = (l.get("email_statut") or "").strip().upper()
        raison = ""
        if (l.get("exclu") or "").lower() == "oui":
            raison = "exclu"
        elif (l.get("ne_plus_contacter") or "").lower() == "oui":
            raison = "ne plus contacter"
        elif not email or "@" not in email:
            raison = "sans email"
        elif statut in INVALIDES:
            raison = f"email {statut.lower()}"
        elif statut == "CATCH_ALL" and not a.avec_catch_all:
            raison = "catch-all"
        elif statut not in FIABLES and statut != "CATCH_ALL" and not a.sans_verification:
            raison = "email non verifie"
        if raison:
            raisons[raison] = raisons.get(raison, 0) + 1
            continue
        ligne = {"email": email, "firstName": l.get("prenom", ""), "lastName": l.get("nom", ""), "companyName": l.get("entreprise", ""),
                 "jobTitle": l.get("titre", ""), "linkedinUrl": norm_linkedin_url(l.get("linkedin_url")), "phone": l.get("telephone", ""),
                 "companyDomain": l.get("domaine", ""), "tier": l.get("tier", ""), "signal": l.get("signal_detail", "")}
        if a.colonne_message in l:
            ligne["icebreaker"] = l.get(a.colonne_message, "")
        for k, v in l.items():
            if k.startswith("var_") and v:
                ligne[k[4:]] = v
        gardees.append(ligne)
    if not gardees:
        arret("aucune ligne importable : " + ", ".join(f"{k} {v}" for k, v in raisons.items()))
    cols = list(dict.fromkeys(k for g in gardees for k in g))
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet), suffixe="lemlist")
    with open(sortie, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(gardees)
    afficher(f"{len(gardees)} leads importables sur {len(lignes)} -> {sortie}")
    for k, v in sorted(raisons.items(), key=lambda x: -x[1]):
        afficher(f"  ecartes : {v:4d}  {k}")
    sans_msg = sum(1 for g in gardees if a.colonne_message and not g.get("icebreaker"))
    if a.colonne_message and sans_msg:
        afficher(f"  [attention] {sans_msg} lead(s) sans message dans la colonne {a.colonne_message}")
    afficher("Apercu (a montrer a l'utilisateur avant l'import) :")
    for g in gardees[:3]:
        afficher(f"  - {g['firstName']} {g['lastName']} <{g['email']}> ({g['companyName']}) : {(g.get('icebreaker') or '(pas de message personnalise)')[:160]}")


if __name__ == "__main__":
    main()
