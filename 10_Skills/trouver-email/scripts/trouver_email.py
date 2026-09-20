"""trouver_email : email pro verifie via FullEnrich, seulement sur les lignes qui en ont besoin.

Regle : une ligne est traitee si `email` est vide, ou si `email_statut` est invalide
(INVALID, INVALID_DOMAIN, BOUNCE...). Tout le reste est laisse tel quel. --force ignore la regle.
Il faut prenom + nom + (entreprise ou domaine), ou linkedin_url, pour qu'un contact soit envoye.

Usage :
  python3 trouver_email.py --in liste.csv --dry-run            compte les lignes a traiter et annonce le cout
  python3 trouver_email.py --in liste.csv                      lance (lots de 100, polling automatique)
  python3 trouver_email.py --in liste.csv --max 200 --confirmer   au-dela de 100 credits estimes, --confirmer est exige
  python3 trouver_email.py --in liste.csv --source prospeo      Prospeo en second fournisseur (ce que FullEnrich n'a pas trouve, ou une liste venue de Prospeo)
Cout : FullEnrich 1 credit par email pro trouve, 0 si rien trouve, 0 si le contact a ete enrichi il y a moins de 3 mois.
Prospeo (--source prospeo) : 1 credit par email verifie trouve, 0 sinon, 0 si deja enrichi depuis moins de 90 jours ; lots de 50 ;
identifie la personne par prospeo_person_id, linkedin_url, ou prenom + nom + domaine (ou entreprise). Statut ecrit : DELIVERABLE.
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
from gtm_common import FullEnrich, Prospeo, afficher, arret, bandeau_dry_run, chemin_sortie, domaine, ecrire_csv, lire_csv, sujet_depuis_fichier  # noqa: E402

VERBE = "trouver-email"
SEUIL_CONFIRMATION = 100


def via_prospeo(lignes: list[dict], a) -> None:
    invalides = ("INVALID", "INVALID_DOMAIN", "NOT_FOUND", "BOUNCE")
    idx = [i for i, l in enumerate(lignes) if a.force or not (l.get("email") or "").strip() or (l.get("email_statut") or "").upper() in invalides]
    data, par_id = [], {}
    for i in idx:
        l = lignes[i]
        d = {"identifier": str(i)}
        if l.get("prospeo_person_id"):
            d["person_id"] = l["prospeo_person_id"]
        elif (l.get("linkedin_url") or "").strip():
            d["linkedin_url"] = l["linkedin_url"].strip()
        elif (l.get("prenom") or "").strip() and (l.get("nom") or "").strip() and (l.get("domaine") or l.get("entreprise")):
            d.update({"first_name": l["prenom"].strip(), "last_name": l["nom"].strip()})
            if l.get("domaine"):
                d["company_website"] = domaine(l["domaine"])
            if l.get("entreprise"):
                d["company_name"] = l["entreprise"]
            if l.get("linkedin_entreprise_url"):
                d["company_linkedin_url"] = l["linkedin_entreprise_url"]
        else:
            continue
        data.append(d)
        par_id[str(i)] = i
    if a.max:
        data = data[:a.max]
    if a.dry_run:
        bandeau_dry_run("Prospeo POST /bulk-enrich-person", [f"{len(data)} ligne(s) a traiter sur {len(lignes)} (lots de 50)",
                                                            f"cout : au plus {len(data)} credit(s) (1 par email {'trouve' if a.emails_non_verifies else 'verifie trouve'}, 0 sinon, 0 si deja enrichi sous 90 jours)"])
        return
    if not data:
        arret("aucune ligne a traiter (email deja present, ou ni prospeo_person_id, ni linkedin_url, ni prenom + nom + domaine)")
    if len(data) > SEUIL_CONFIRMATION and not a.confirmer:
        arret(f"cout possible {len(data)} credits (> {SEUIL_CONFIRMATION}) : validez avec l'utilisateur puis relancez avec --confirmer")
    pr = Prospeo()
    afficher(f"  [prospeo] {pr.solde()}")
    trouves, non, cout = pr.enrichir_personnes(data, email_verifie_seulement=not a.emails_non_verifies, mobile=False)
    ok = 0
    for ident, m in trouves.items():
        i = par_id.get(ident)
        if i is None:
            continue
        n = Prospeo.normaliser_personne(m)
        if n.get("email"):
            lignes[i]["email"] = n["email"]
            lignes[i]["email_statut"] = n.get("email_statut") or "DELIVERABLE"
            lignes[i]["email_source"] = "prospeo"
            ok += 1
        for k in ("linkedin_url", "titre", "prospeo_person_id"):
            if n.get(k) and not lignes[i].get(k):
                lignes[i][k] = n[k]
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet))
    ecrire_csv(lignes, sortie)
    afficher(f"{ok} email(s) trouve(s) sur {len(data)} traite(s) ({len(non)} sans resultat), {cout} credit(s) factures -> {sortie}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--max", type=int, help="nombre de lignes a traiter dans ce run")
    ap.add_argument("--force", action="store_true", help="re-chercher meme les emails deja presents")
    ap.add_argument("--confirmer", action="store_true", help="obligatoire si le cout estime depasse 100 credits")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source", choices=["fullenrich", "prospeo"], default="fullenrich", help="fullenrich (defaut) ou prospeo (second fournisseur, emails verifies)")
    ap.add_argument("--emails-non-verifies", action="store_true", help="prospeo : accepter aussi les emails non verifies (statut UNKNOWN)")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    if a.source == "prospeo":
        via_prospeo(lignes, a)
        return
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
