#!/usr/bin/env python3
"""envoyer_lemlist : pousser un CSV normalise dans une campagne Lemlist par l'API, puis (si demande) la demarrer.

Etapes : filtrer les lignes qui ne doivent pas partir (memes regles que preparer_import_lemlist.py), choisir ou creer
la campagne, montrer 3 leads, puis avec --confirmer : ajouter les leads (dedoublonnes par Lemlist) et, avec --lancer,
demarrer la campagne. Sans --confirmer, rien n'est ecrit chez Lemlist.

Usage :
  python3 envoyer_lemlist.py --in liste.csv --campagne "Signal levee sept" --colonne-message icebreaker --dry-run
  python3 envoyer_lemlist.py --in liste.csv --campagne-id cam_xxx --confirmer
  python3 envoyer_lemlist.py --in liste.csv --campagne "Signal levee sept" --confirmer --lancer
  python3 envoyer_lemlist.py --lister                      liste les campagnes existantes (id, nom, statut)
  python3 envoyer_lemlist.py --pauser cam_xxx              met une campagne en pause
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import Lemlist, afficher, arret, bandeau_dry_run, chemin_sortie, ecrire_csv, lire_csv, norm_linkedin_url, sujet_depuis_fichier  # noqa: E402

VERBE = "envoyer-sequence"
FIABLES = {"DELIVERABLE", "HIGH_PROBABILITY"}
INVALIDES = {"INVALID", "INVALID_DOMAIN", "NOT_FOUND", "BOUNCE", "BOUNCED"}


def preparer(lignes: list[dict], colonne_message: str, avec_catch_all: bool, sans_verification: bool) -> tuple[list[dict], dict]:
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
        elif statut == "CATCH_ALL" and not avec_catch_all:
            raison = "catch-all"
        elif statut not in FIABLES and statut != "CATCH_ALL" and not sans_verification:
            raison = "email non verifie"
        if raison:
            raisons[raison] = raisons.get(raison, 0) + 1
            continue
        lead = {"email": email, "firstName": l.get("prenom", ""), "lastName": l.get("nom", ""), "companyName": l.get("entreprise", ""),
                "jobTitle": l.get("titre", ""), "linkedinUrl": norm_linkedin_url(l.get("linkedin_url")), "phone": l.get("telephone", ""),
                "companyDomain": l.get("domaine", ""), "tier": l.get("tier", ""), "signal": l.get("signal_detail", "")}
        if colonne_message in l:
            lead["icebreaker"] = l.get(colonne_message, "")
        for k, v in l.items():
            if k.startswith("var_") and v:
                lead[k[4:]] = v
        gardees.append({k: v for k, v in lead.items() if v})
    return gardees, raisons


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", help="CSV normalise a pousser")
    ap.add_argument("--campagne", help="nom de la campagne (creee si absente)")
    ap.add_argument("--campagne-id", help="id d'une campagne existante (prime sur --campagne)")
    ap.add_argument("--colonne-message", default="icebreaker")
    ap.add_argument("--avec-catch-all", action="store_true")
    ap.add_argument("--sans-verification", action="store_true")
    ap.add_argument("--lancer", action="store_true", help="demarrer la campagne apres l'import")
    ap.add_argument("--lister", action="store_true", help="lister les campagnes et sortir")
    ap.add_argument("--pauser", help="id d'une campagne a mettre en pause, puis sortir")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--confirmer", action="store_true")
    a = ap.parse_args()

    if a.lister:
        for c in Lemlist().campagnes():
            afficher(f"  {c.get('_id') or c.get('id')}  {c.get('name')}  [{c.get('status') or c.get('state', '')}]")
        return
    if a.pauser:
        Lemlist().pauser(a.pauser)
        afficher(f"campagne {a.pauser} en pause")
        return
    if not a.entree or not (a.campagne or a.campagne_id):
        arret("il faut --in <csv> et --campagne <nom> (ou --campagne-id)")
    lignes = lire_csv(a.entree)
    leads, raisons = preparer(lignes, a.colonne_message, a.avec_catch_all, a.sans_verification)
    if not leads:
        arret("aucune ligne importable : " + ", ".join(f"{k} {v}" for k, v in raisons.items()))
    sans_msg = sum(1 for g in leads if a.colonne_message and not g.get("icebreaker"))
    resume = [f"{len(leads)} lead(s) a pousser sur {len(lignes)} ; ecartes : " + (", ".join(f"{v} {k}" for k, v in raisons.items()) or "aucun"),
              f"campagne : {a.campagne_id or a.campagne + ' (creee si absente)'}",
              f"message personnalise : colonne {a.colonne_message}" + (f", {sans_msg} lead(s) sans message" if sans_msg else ""),
              "demarrage : " + ("oui, juste apres l'import" if a.lancer else "non (la campagne reste en brouillon)"),
              "cout : aucun credit (import par API) ; l'envoi consomme le quota de vos boites"]
    bandeau_dry_run("envoyer-sequence via Lemlist", resume)
    afficher("Apercu (a valider par l'utilisateur) :")
    for g in leads[:3]:
        afficher(f"  - {g.get('firstName','')} {g.get('lastName','')} <{g['email']}> ({g.get('companyName','')}) : {(g.get('icebreaker') or '(pas de message personnalise)')[:160]}")
    if a.dry_run:
        afficher("[dry-run] Rien n'a ete envoye a Lemlist. Relancez avec --confirmer apres le oui de l'utilisateur.")
        return
    if not a.confirmer:
        arret("Import refuse sans --confirmer : montrez l'apercu, attendez le oui.")
    lm = Lemlist()
    cid = a.campagne_id
    if not cid:
        for c in lm.campagnes():
            if (c.get("name") or "").strip().lower() == a.campagne.strip().lower():
                cid = c.get("_id") or c.get("id")
                break
        if not cid:
            crea = lm.creer_campagne(a.campagne)
            cid = crea.get("_id") or crea.get("id")
            afficher(f"campagne creee : {a.campagne} ({cid}). Ajoutez la sequence (etapes, textes) dans Lemlist avant de lancer.")
    ok, doublons, erreurs = 0, 0, 0
    for g in leads:
        try:
            rep = lm.ajouter_lead(cid, g, dedoublonner=True)
            if isinstance(rep, dict) and rep.get("duplicate") or (isinstance(rep, dict) and "already" in str(rep).lower()):
                doublons += 1
            else:
                ok += 1
        except RuntimeError as e:
            if "409" in str(e) or "already" in str(e).lower():
                doublons += 1
            else:
                erreurs += 1
                afficher(f"  [erreur] {g['email']} : {e}")
    afficher(f"{ok} lead(s) ajoutes, {doublons} deja presents, {erreurs} erreur(s) dans la campagne {cid}")
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet), suffixe="lemlist")
    for l in lignes:
        l["campagne_lemlist"] = cid
    ecrire_csv(lignes, sortie, colonnes_extra=["campagne_lemlist"])
    afficher(f"trace -> {sortie}")
    if a.lancer:
        lm.demarrer(cid)
        afficher(f"campagne {cid} demarree.")


if __name__ == "__main__":
    main()
