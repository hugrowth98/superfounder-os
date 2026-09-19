"""trouver_telephone : numero de mobile via FullEnrich, seulement sur les lignes sans `telephone`.

Regle : une ligne est traitee si `telephone` est vide. --force ignore la regle. Il faut prenom + nom +
(entreprise ou domaine), ou linkedin_url. Cout : 10 credits par mobile trouve, 0 si rien trouve.
Reservez ce verbe aux tiers A (le telephone est le canal de conversion, pas de prospection de masse).

Usage :
  python3 trouver_telephone.py --in liste.csv --dry-run              compte et annonce le cout
  python3 trouver_telephone.py --in liste.csv --tier A               ne traite que les lignes tier A
  python3 trouver_telephone.py --in liste.csv --max 30 --confirmer   --confirmer exige au-dela de 100 credits estimes
Sortie : Listes-prospection/trouver-telephone_<sujet>_<date>.csv (l'entree n'est jamais ecrasee).
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

VERBE = "trouver-telephone"
SEUIL_CONFIRMATION = 100


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--tier", help="ne traiter que ce tier (A, B...), colonne `tier`")
    ap.add_argument("--max", type=int)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--confirmer", action="store_true", help="obligatoire si le cout estime depasse 100 credits")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    if a.tier:
        hors_tier = [l for l in lignes if (l.get("tier") or "").strip().upper() != a.tier.upper()]
        for l in hors_tier:
            l["_saut"] = "1"
        afficher(f"  [tier] {len(lignes) - len(hors_tier)} ligne(s) en tier {a.tier}, {len(hors_tier)} ignoree(s)")
    cibles = [l for l in lignes if not l.get("_saut")]
    fe = FullEnrich(exiger_cle=not a.dry_run)
    champs = ["contact.phones"]
    apercu = fe.enrichir_lignes(cibles, champs, forcer=a.force, dry_run=True, maximum=a.max)
    if a.dry_run:
        return
    if apercu["credits_estimes"] > SEUIL_CONFIRMATION and not a.confirmer:
        arret(f"cout estime {apercu['credits_estimes']} credits (> {SEUIL_CONFIRMATION}) : validez avec l'utilisateur puis relancez avec --confirmer")
    stats = fe.enrichir_lignes(cibles, champs, forcer=a.force, dry_run=False, nom=f"trouver-telephone {sujet_depuis_fichier(a.entree, a.sujet)}", maximum=a.max)
    for l in lignes:
        l.pop("_saut", None)
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet))
    ecrire_csv(lignes, sortie)
    afficher(f"{stats['trouves']} mobile(s) trouve(s) sur {stats['a_traiter']} traite(s), {stats['credits_factures']} credits factures -> {sortie}")


if __name__ == "__main__":
    main()
