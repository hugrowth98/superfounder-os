"""trouver_email : email pro verifie via FullEnrich, seulement sur les lignes qui en ont besoin.

Regle : une ligne est traitee si `email` est vide, ou si `email_statut` est invalide
(INVALID, INVALID_DOMAIN, BOUNCE...). Tout le reste est laisse tel quel. --force ignore la regle.
Il faut prenom + nom + (entreprise ou domaine), ou linkedin_url, pour qu'un contact soit envoye.

Usage :
  python3 trouver_email.py --in liste.csv --dry-run            compte les lignes a traiter et annonce le cout
  python3 trouver_email.py --in liste.csv                      lance (lots de 100, polling automatique)
  python3 trouver_email.py --in liste.csv --max 200 --confirmer   au-dela de 100 credits estimes, --confirmer est exige
Cout : 1 credit par email pro trouve, 0 si rien trouve, 0 si le contact a ete enrichi il y a moins de 3 mois.
Statuts ecrits dans email_statut : DELIVERABLE, HIGH_PROBABILITY, CATCH_ALL, INVALID, NOT_FOUND.
Sortie : Listes-prospection/trouver-email_<sujet>_<date>.csv (l'entree n'est jamais ecrasee).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import FullEnrich, afficher, arret, chemin_sortie, ecrire_csv, lire_csv, sujet_depuis_fichier  # noqa: E402

VERBE = "trouver-email"
SEUIL_CONFIRMATION = 100


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--max", type=int, help="nombre de lignes a traiter dans ce run")
    ap.add_argument("--force", action="store_true", help="re-chercher meme les emails deja presents")
    ap.add_argument("--confirmer", action="store_true", help="obligatoire si le cout estime depasse 100 credits")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    fe = FullEnrich(exiger_cle=not a.dry_run)
    champs = ["contact.emails"]
    apercu = fe.enrichir_lignes(lignes, champs, forcer=a.force, dry_run=True, maximum=a.max)
    if a.dry_run:
        return
    if apercu["credits_estimes"] > SEUIL_CONFIRMATION and not a.confirmer:
        arret(f"cout estime {apercu['credits_estimes']} credits (> {SEUIL_CONFIRMATION}) : validez avec l'utilisateur puis relancez avec --confirmer")
    stats = fe.enrichir_lignes(lignes, champs, forcer=a.force, dry_run=False, nom=f"trouver-email {sujet_depuis_fichier(a.entree, a.sujet)}", maximum=a.max)
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet))
    ecrire_csv(lignes, sortie)
    verifies = sum(1 for l in lignes if (l.get("email_statut") or "").upper() in ("DELIVERABLE", "HIGH_PROBABILITY"))
    afficher(f"{stats['trouves']} email(s) trouve(s) sur {stats['a_traiter']} traite(s), {verifies} adresses fiables sur {len(lignes)} lignes -> {sortie}")


if __name__ == "__main__":
    main()
