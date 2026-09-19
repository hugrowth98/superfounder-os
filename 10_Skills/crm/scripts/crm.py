#!/usr/bin/env python3
"""crm : lire et écrire dans HubSpot depuis le module GTM.

Deux commandes :
  lire     exporte les entreprises et contacts des affaires gagnées ou perdues (pour l'ICP,
           les lookalikes, la sélection de comptes). Aucun crédit, un token HubSpot suffit.
  pousser  crée ou met à jour les contacts d'un CSV (clé : email), rattache l'entreprise par
           domaine, ajoute une note et, si demandé, une tâche d'appel datée. Refuse sans
           --confirmer après avoir affiché ce qui serait écrit.

Exemples :
  python3 crm.py lire --statut gagnes
  python3 crm.py lire --statut perdus --depuis 2025-01-01
  python3 crm.py pousser --in liste.csv --note "Signal : levée série A le 2026-09-01" --dry-run
  python3 crm.py pousser --in liste.csv --tache "Appeler (nouveau DRH)" --echeance 2026-09-25 --confirmer
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

_ici = Path(__file__).resolve()
_racine = next(p for p in _ici.parents if (p / "CLAUDE.md").exists() and (p / "10_Skills").is_dir())
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (HubSpot, afficher, arret, bandeau_dry_run, chemin_sortie, domaine,  # noqa: E402
                        ecrire_csv, lire_csv, lire_outils, sujet_depuis_fichier)

ASSOC_NOTE_CONTACT = 202   # note -> contact
ASSOC_TACHE_CONTACT = 204  # tâche -> contact


def _verifier_crm():
    outils = lire_outils()
    if str(outils.get("crm", "")).lower() not in ("hubspot", ""):
        arret("OUTILS.md indique un CRM autre que HubSpot : ce skill ne sait parler qu'à HubSpot.")


# ------------------------------------------------------------------ lire

def lire(a):
    _verifier_crm()
    hs = HubSpot()
    prop = "hs_is_closed_won" if a.statut == "gagnes" else "hs_is_closed_lost"
    filtres = [{"propertyName": prop, "operator": "EQ", "value": "true"}]
    if a.depuis:
        ts = int(dt.datetime.fromisoformat(a.depuis).timestamp() * 1000)
        filtres.append({"propertyName": "closedate", "operator": "GTE", "value": str(ts)})
    affaires, after = [], None
    while True:
        body = {"filterGroups": [{"filters": filtres}], "limit": 100,
                "properties": ["dealname", "amount", "closedate", "dealstage"]}
        if after:
            body["after"] = after
        res = hs._req("POST", "/crm/v3/objects/deals/search", body)
        affaires += res.get("results", [])
        after = (res.get("paging") or {}).get("next", {}).get("after")
        if not after or len(affaires) >= a.max:
            break
    afficher(f"{len(affaires)} affaire(s) {a.statut}")
    lignes = []
    for d in affaires:
        did = d["id"]
        comp = hs._req("GET", f"/crm/v4/objects/deals/{did}/associations/companies").get("results", [])
        cont = hs._req("GET", f"/crm/v4/objects/deals/{did}/associations/contacts").get("results", [])
        entreprise = {}
        if comp:
            cid = comp[0]["toObjectId"]
            entreprise = hs._req("GET", f"/crm/v3/objects/companies/{cid}",
                                 params={"properties": "name,domain,industry,numberofemployees,city,country"}).get("properties", {})
        base = {
            "entreprise": entreprise.get("name", ""), "domaine": entreprise.get("domain", ""),
            "secteur": entreprise.get("industry", ""), "effectif": entreprise.get("numberofemployees", ""),
            "ville": entreprise.get("city", ""), "pays": entreprise.get("country", ""),
            "source": "hubspot", "date_extraction": dt.date.today().isoformat(),
            "affaire": d["properties"].get("dealname", ""), "montant": d["properties"].get("amount", ""),
            "date_cloture": (d["properties"].get("closedate") or "")[:10], "statut": a.statut,
        }
        if not cont:
            lignes.append(base)
        for c in cont[:5]:
            props = hs._req("GET", f"/crm/v3/objects/contacts/{c['toObjectId']}",
                            params={"properties": "firstname,lastname,jobtitle,email,hs_linkedin_url"}).get("properties", {})
            lignes.append({**base, "prenom": props.get("firstname", ""), "nom": props.get("lastname", ""),
                           "titre": props.get("jobtitle", ""), "email": props.get("email", ""),
                           "linkedin_url": props.get("hs_linkedin_url", "")})
    out = ecrire_csv(lignes, chemin_sortie("crm", f"clients-{a.statut}"),
                     colonnes_extra=["affaire", "montant", "date_cloture", "statut"])
    afficher(f"{len(lignes)} ligne(s) écrite(s) : {out}")


# ------------------------------------------------------------------ pousser

def _lot(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def pousser(a):
    _verifier_crm()
    lignes = [l for l in lire_csv(a.entree) if (l.get("email") or "").strip()]
    if not lignes:
        arret("Aucune ligne avec un email : HubSpot rattache les contacts par email.")
    if a.tier:
        lignes = [l for l in lignes if (l.get("tier") or "").upper() in a.tier.upper().split(",")]
    exclues = [l for l in lignes if (l.get("exclu") or "").lower() == "oui"]
    lignes = [l for l in lignes if (l.get("exclu") or "").lower() != "oui"]
    resume = [f"{len(lignes)} contact(s) à créer ou mettre à jour (clé email), {len(exclues)} exclu(s) ignoré(s)",
              f"entreprises rattachées par domaine : {sum(1 for l in lignes if l.get('domaine'))}",
              f"note par contact : {'oui' if a.note else 'non'}",
              f"tâche par contact : {'oui, échéance ' + a.echeance if a.tache else 'non'}"]
    bandeau_dry_run("crm pousser", resume)
    for l in lignes[:3]:
        afficher(f"  ex : {l.get('prenom','')} {l.get('nom','')} <{l['email']}> @ {l.get('entreprise','')} ({l.get('domaine','')})")
    if a.dry_run:
        afficher("[dry-run] Aucune écriture. Relancez avec --confirmer pour écrire dans HubSpot.")
        return
    if not a.confirmer:
        arret("Écriture refusée sans --confirmer (montrez ce résumé à l'utilisateur et attendez son oui).")
    hs = HubSpot()
    # 1. contacts (upsert par email)
    ids = {}
    for lot in _lot(lignes, 100):
        inputs = []
        for l in lot:
            props = {"email": l["email"].strip().lower(), "firstname": l.get("prenom", ""),
                     "lastname": l.get("nom", ""), "jobtitle": l.get("titre", ""),
                     "company": l.get("entreprise", ""), "hs_linkedin_url": l.get("linkedin_url", "")}
            if l.get("telephone"):
                props["phone"] = l["telephone"]
            inputs.append({"idProperty": "email", "id": props["email"], "properties": {k: v for k, v in props.items() if v}})
        res = hs._req("POST", "/crm/v3/objects/contacts/batch/upsert", {"inputs": inputs})
        for it in res.get("results", []):
            ids[(it.get("properties", {}).get("email") or "").lower()] = it["id"]
    afficher(f"{len(ids)} contact(s) écrits")
    # 2. entreprises par domaine, création si absente, association
    domaines = sorted({domaine(l.get("domaine") or "") for l in lignes if l.get("domaine")})
    connues = hs.entreprises_par_domaine(domaines) if domaines else {}
    for l in lignes:
        d = domaine(l.get("domaine") or "")
        cid = connues.get(d)
        if d and not cid:
            crea = hs._req("POST", "/crm/v3/objects/companies", {"properties": {"domain": d, "name": l.get("entreprise") or d}})
            cid = crea["id"]; connues[d] = cid
        cont_id = ids.get(l["email"].strip().lower())
        if cid and cont_id:
            hs._req("PUT", f"/crm/v4/objects/contacts/{cont_id}/associations/default/companies/{cid}")
    # 3. note et tâche
    now_ms = int(dt.datetime.now().timestamp() * 1000)
    n_notes = n_taches = 0
    for l in lignes:
        cont_id = ids.get(l["email"].strip().lower())
        if not cont_id:
            continue
        signal = l.get("signal_detail") or ""
        if a.note or signal:
            corps = a.note or ""
            if signal:
                corps += ("\n" if corps else "") + f"Signal : {l.get('signal_type','')} ({l.get('signal_date','')}) : {signal}"
            hs._req("POST", "/crm/v3/objects/notes",
                    {"properties": {"hs_timestamp": now_ms, "hs_note_body": corps},
                     "associations": [{"to": {"id": cont_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": ASSOC_NOTE_CONTACT}]}]})
            n_notes += 1
        if a.tache:
            ech = dt.datetime.fromisoformat(a.echeance) if a.echeance else dt.datetime.now() + dt.timedelta(days=2)
            hs._req("POST", "/crm/v3/objects/tasks",
                    {"properties": {"hs_timestamp": int(ech.timestamp() * 1000), "hs_task_subject": a.tache,
                                    "hs_task_body": signal or a.note or "", "hs_task_status": "NOT_STARTED", "hs_task_type": "CALL"},
                     "associations": [{"to": {"id": cont_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": ASSOC_TACHE_CONTACT}]}]})
            n_taches += 1
    afficher(f"{n_notes} note(s), {n_taches} tâche(s). Terminé.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("lire", help="exporter les clients gagnés ou perdus")
    r.add_argument("--statut", choices=["gagnes", "perdus"], default="gagnes")
    r.add_argument("--depuis", help="date de clôture minimale, YYYY-MM-DD")
    r.add_argument("--max", type=int, default=500)
    r.set_defaults(fn=lire)
    p = sub.add_parser("pousser", help="écrire un CSV dans HubSpot")
    p.add_argument("--in", dest="entree", required=True)
    p.add_argument("--tier", help="ne pousser que ces tiers, ex : A,B")
    p.add_argument("--note", help="texte de la note ajoutée à chaque contact")
    p.add_argument("--tache", help="sujet de la tâche d'appel à créer pour chaque contact")
    p.add_argument("--echeance", help="date de la tâche, YYYY-MM-DD (défaut : dans 2 jours)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--confirmer", action="store_true")
    p.set_defaults(fn=pousser)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
