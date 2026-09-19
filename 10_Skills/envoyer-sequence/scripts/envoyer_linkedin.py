"""envoyer_linkedin : invitations puis messages LinkedIn via Unipile, avec compteurs journaliers bloquants et verification
des reponses avant tout message. Ne part jamais sans --confirmer, apres affichage de 3 messages.

Garde-fous codes ici (non contournables par un argument) :
  - invitations : LIMITE_INVITATIONS_JOUR du .env (defaut 30, plafond dur 30), compteur dans scripts/compteurs.json
  - messages    : LIMITE_DM_JOUR du .env (defaut 50, plafond dur 100)
  - avant chaque message : les prospects qui ont deja repondu (verifier-reponses, chats Unipile) sont exclus
  - une ligne deja envoyee (colonne envoi_<etape>_date remplie) n'est jamais renvoyee
  - delai entre deux envois : --delai secondes (defaut 45) plus un alea de 0 a 30 s

Usage :
  python3 envoyer_linkedin.py --in liste.csv --etape invitation --colonne-message note_invitation --dry-run
  python3 envoyer_linkedin.py --in liste.csv --etape invitation --colonne-message note_invitation --max 20 --confirmer
  python3 envoyer_linkedin.py --in liste.csv --etape message --colonne-message message_1 --max 30 --confirmer
  python3 envoyer_linkedin.py quota                       affiche ce qui reste aujourd'hui
Il faut provider_id (Unipile) ou linkedin_url (le script resout le provider_id via le profil, une lecture par ligne).
Sortie : Listes-prospection/envoyer-sequence_<sujet>_<date>_<etape>.csv (l'entree n'est jamais ecrasee).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from datetime import date
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import Unipile, afficher, arret, chemin_sortie, ecrire_csv, env, lire_csv, norm_linkedin_url, slug_linkedin, sujet_depuis_fichier  # noqa: E402

VERBE = "envoyer-sequence"
COMPTEURS = Path(__file__).resolve().parent / "compteurs.json"
PLAFONDS_DURS = {"invitation": 30, "message": 100}
DEFAUTS = {"invitation": 30, "message": 50}
LIMITE_NOTE_INVITATION = 300


def limite(etape: str) -> int:
    var = "LIMITE_INVITATIONS_JOUR" if etape == "invitation" else "LIMITE_DM_JOUR"
    try:
        v = int(env(var, obligatoire=False) or DEFAUTS[etape])
    except ValueError:
        v = DEFAUTS[etape]
    return max(1, min(v, PLAFONDS_DURS[etape]))


def _lire_compteurs() -> dict:
    return json.loads(COMPTEURS.read_text(encoding="utf-8")) if COMPTEURS.exists() else {}


def envoyes_aujourd_hui(etape: str) -> int:
    return int(_lire_compteurs().get(etape, {}).get(date.today().isoformat(), 0))


def incrementer(etape: str) -> None:
    d = _lire_compteurs()
    jour = date.today().isoformat()
    d.setdefault(etape, {})[jour] = int(d.get(etape, {}).get(jour, 0)) + 1
    COMPTEURS.write_text(json.dumps(d, indent=1), encoding="utf-8")


def restant(etape: str) -> int:
    return max(0, limite(etape) - envoyes_aujourd_hui(etape))


def resoudre_provider_id(u: Unipile, ligne: dict) -> str:
    if ligne.get("provider_id"):
        return ligne["provider_id"]
    ident = slug_linkedin(ligne.get("linkedin_url"))
    if not ident:
        return ""
    prof = u.profil(ident, complet=False)
    pid = prof.get("provider_id") or prof.get("id") or ""
    if pid:
        ligne["provider_id"] = pid
    return pid


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "quota":
        for e in ("invitation", "message"):
            afficher(f"{e:10s} : {envoyes_aujourd_hui(e)} envoye(s) aujourd'hui, {restant(e)} restant(s) sur {limite(e)}")
        return
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--etape", choices=["invitation", "message"], required=True)
    ap.add_argument("--colonne-message", help="colonne du texte a envoyer (facultative pour une invitation sans note)")
    ap.add_argument("--max", type=int, help="nombre d'envois max dans ce run (borne par le quota du jour)")
    ap.add_argument("--delai", type=int, default=45, help="secondes entre deux envois (+ alea 0 a 30 s)")
    ap.add_argument("--confirmer", action="store_true", help="obligatoire pour envoyer ; sans lui, le script montre 3 messages et s'arrete")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    etape = a.etape
    lignes = lire_csv(a.entree)
    col_date = f"envoi_{etape}_date"
    candidats = []
    raisons: dict = {}

    def ecarter(r):
        raisons[r] = raisons.get(r, 0) + 1

    for l in lignes:
        if (l.get("exclu") or "").lower() == "oui":
            ecarter("exclu"); continue
        if (l.get("ne_plus_contacter") or "").lower() == "oui":
            ecarter("ne plus contacter"); continue
        if l.get(col_date):
            ecarter(f"deja envoye ({col_date})"); continue
        if not (l.get("provider_id") or norm_linkedin_url(l.get("linkedin_url"))):
            ecarter("ni provider_id ni linkedin_url"); continue
        texte = (l.get(a.colonne_message) or "").strip() if a.colonne_message else ""
        if etape == "message" and not texte:
            ecarter(f"message vide ({a.colonne_message or 'colonne non indiquee'})"); continue
        if etape == "invitation" and len(texte) > LIMITE_NOTE_INVITATION:
            ecarter(f"note d'invitation > {LIMITE_NOTE_INVITATION} caracteres"); continue
        candidats.append(l)
    quota = restant(etape)
    n_prevu = min(len(candidats), quota, a.max or len(candidats))
    afficher(f"  [{etape}] {len(candidats)} candidat(s) sur {len(lignes)}, quota restant aujourd'hui {quota}/{limite(etape)}, ce run : {n_prevu}")
    for r, n in raisons.items():
        afficher(f"    ecartes : {n:4d}  {r}")
    if not candidats or n_prevu == 0:
        arret("rien a envoyer (quota du jour epuise ou aucun candidat)")
    afficher("Echantillon de 3 messages (a valider avec l'utilisateur) :")
    for l in candidats[:3]:
        texte = (l.get(a.colonne_message) or "").strip() if a.colonne_message else "(invitation sans note)"
        afficher(f"  - {l.get('prenom')} {l.get('nom')} ({l.get('entreprise')}) : {texte[:400]}")
    if a.dry_run or not a.confirmer:
        afficher("[stop] aucun envoi : relancez avec --confirmer une fois l'echantillon valide par l'utilisateur.")
        return

    u = Unipile()
    deja_repondu = set()
    if etape == "message":
        deja_repondu = {r["provider_id"] for r in u.repondants() if r.get("provider_id")}
        afficher(f"  [reponses] {len(deja_repondu)} conversation(s) avec reponse : ces personnes sont exclues")
    envoyes, erreurs = 0, 0
    for l in candidats:
        if envoyes >= n_prevu or restant(etape) <= 0:
            break
        try:
            pid = resoudre_provider_id(u, l)
            if not pid:
                l["erreur_envoi"] = "provider_id introuvable"; erreurs += 1; continue
            if pid in deja_repondu:
                l["ne_plus_contacter"] = "oui"; l["erreur_envoi"] = "a deja repondu, pas de relance"; continue
            texte = (l.get(a.colonne_message) or "").strip() if a.colonne_message else ""
            if etape == "invitation":
                u.inviter(pid, texte or None)
            else:
                u.envoyer_dm(pid, texte)
            incrementer(etape)
            l[col_date] = date.today().isoformat()
            envoyes += 1
            afficher(f"  envoye {envoyes}/{n_prevu} : {l.get('prenom')} {l.get('nom')} (reste {restant(etape)} aujourd'hui)")
            time.sleep(a.delai + random.randint(0, 30))
        except Exception as e:
            l["erreur_envoi"] = str(e)[:160]
            erreurs += 1
            if "429" in str(e):
                afficher("  [stop] limite de debit LinkedIn ou Unipile : arret du run, reprenez plus tard")
                break
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet), suffixe=etape)
    ecrire_csv(lignes, sortie)
    afficher(f"{envoyes} {etape}(s) envoye(s), {erreurs} erreur(s), {restant(etape)} restant(s) aujourd'hui -> {sortie}")


if __name__ == "__main__":
    main()
