"""verifier_reponses : qui a repondu, sur quel canal, quand, et quel etait le dernier message. Marque ne_plus_contacter.

Canaux :
  linkedin  Unipile GET /api/v1/chats + /messages + /attendees : conversations ou le dernier message vient du prospect
  email     Lemlist : la boite de reception est lue par le MCP (get_inbox_conversations) ; sauvegardez la reponse en JSON
            et passez-la avec --lemlist-json pour la normaliser et la fusionner

Usage :
  python3 verifier_reponses.py                                   reponses LinkedIn (Unipile)
  python3 verifier_reponses.py --lemlist-json inbox.json         + reponses email
  python3 verifier_reponses.py --in liste.csv                    en plus, marque ne_plus_contacter = oui dans une copie de la liste
  python3 verifier_reponses.py --depuis 7                        seulement les reponses des 7 derniers jours (quand la date est connue)
Sorties : Listes-prospection/verifier-reponses_<sujet>_<date>.csv, et <liste>_maj.csv si --in.
Aucun envoi, lecture seule.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import Lemlist, Unipile, afficher, aujourd_hui, bandeau_dry_run, chemin_sortie, ecrire_csv, lire_csv, norm_linkedin_url, sujet_depuis_fichier  # noqa: E402

VERBE = "verifier-reponses"


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


def _split_nom(nom):
    nom = (nom or "").strip()
    parts = nom.split(" ", 1)
    return (parts[0], parts[1]) if len(parts) > 1 else (nom, "")


def linkedin(dry_run: bool) -> list[dict]:
    if dry_run:
        bandeau_dry_run("Unipile chats", ["lecture des conversations (100 max), des derniers messages et des participants", "cout : abonnement Unipile"])
        return []
    u = Unipile()
    lignes = []
    for r in u.repondants():
        prenom, nom, url, pid = "", "", "", r.get("provider_id") or ""
        try:
            for p in u.participants(r["chat_id"]):
                if p.get("is_self") or (u.own_provider_id and p.get("provider_id") == u.own_provider_id):
                    continue
                prenom, nom = _split_nom(_g(p, "name") or f"{_g(p, 'first_name')} {_g(p, 'last_name')}")
                url = norm_linkedin_url(_g(p, "profile_url", "public_profile_url"))
                pid = pid or _g(p, "provider_id", "id")
                break
        except Exception as e:  # les participants ne bloquent pas la detection
            afficher(f"  [unipile] participants du chat {r['chat_id']} illisibles : {str(e)[:80]}")
        if not prenom:
            prenom, nom = _split_nom(r.get("nom_chat") or "")
        lignes.append({"prenom": prenom, "nom": nom, "linkedin_url": url, "source": "unipile", "date_extraction": aujourd_hui(),
                       "reponse_canal": "linkedin", "reponse_date": r.get("date_reponse", ""), "reponse_texte": (r.get("dernier_message") or "").replace("\n", " ")[:500],
                       "ne_plus_contacter": "oui", "provider_id": pid, "chat_id": r["chat_id"]})
    return lignes


def lemlist(chemin: str) -> list[dict]:
    data = json.loads(Path(chemin).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for k in ("conversations", "items", "data", "results", "inbox"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    lignes = []
    for c in data if isinstance(data, list) else []:
        lead = c.get("lead") or c.get("contact") or c
        msgs = c.get("messages") or []
        dernier = msgs[-1] if msgs and isinstance(msgs[-1], dict) else {}
        texte = _g(c, "lastMessage", "snippet", "preview", "text") or _g(dernier, "text", "body", "snippet")
        prenom, nom = _g(lead, "firstName", "first_name"), _g(lead, "lastName", "last_name")
        if not prenom and _g(lead, "name"):
            prenom, nom = _split_nom(_g(lead, "name"))
        lignes.append({"prenom": prenom, "nom": nom, "entreprise": _g(lead, "companyName", "company"), "email": (_g(lead, "email") or "").lower(),
                       "linkedin_url": norm_linkedin_url(_g(lead, "linkedinUrl", "linkedin_url")), "source": "lemlist", "date_extraction": aujourd_hui(),
                       "reponse_canal": "email", "reponse_date": str(_g(c, "lastMessageAt", "updatedAt", "date", "createdAt") or _g(dernier, "date", "createdAt"))[:10],
                       "reponse_texte": (texte or "").replace("\n", " ")[:500], "ne_plus_contacter": "oui",
                       "campagne": _g(c, "campaignName", "campaign.name", "campaignId"), "lemlist_lead_id": _g(lead, "_id", "id", "leadId"),
                       "sentiment": _g(c, "sentiment", "interest", "label")})
    return lignes


def lemlist_api(depuis_jours: int | None, campagne_id: str | None) -> list[dict]:
    """Reponses email et LinkedIn lues par l'API Lemlist (activites emailsReplied, linkedinReplied)."""
    import datetime as _dt
    lm = Lemlist()
    depuis = (_dt.date.today() - _dt.timedelta(days=depuis_jours)).isoformat() if depuis_jours else None
    lignes = []
    for typ, canal in (("emailsReplied", "email"), ("linkedinReplied", "linkedin")):
        try:
            acts = lm.activites(typ, campagne_id, depuis)
        except RuntimeError as e:
            afficher(f"  [lemlist] {typ} : {e}")
            continue
        for ac in acts:
            lignes.append({"prenom": _g(ac, "firstName", "leadFirstName"), "nom": _g(ac, "lastName", "leadLastName"),
                           "entreprise": _g(ac, "companyName"), "email": (_g(ac, "leadEmail", "email") or "").lower(),
                           "linkedin_url": norm_linkedin_url(_g(ac, "linkedinUrl", "leadLinkedinUrl")), "source": "lemlist",
                           "date_extraction": aujourd_hui(), "reponse_canal": canal, "reponse_date": str(_g(ac, "createdAt", "date"))[:10],
                           "reponse_texte": (_g(ac, "body", "text", "snippet") or "")[:300],
                           "campagne": _g(ac, "campaignName", "campaignId"), "lemlist_lead_id": _g(ac, "leadId", "_id"),
                           "ne_plus_contacter": "oui"})
    afficher(f"  [lemlist] {len(lignes)} reponse(s) par API")
    return lignes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", help="liste a marquer (ne_plus_contacter = oui sur les repondants)")
    ap.add_argument("--lemlist-json", help="fichier JSON des conversations Lemlist (sortie du MCP get_inbox_conversations), optionnel")
    ap.add_argument("--sans-lemlist", action="store_true", help="ne pas interroger l'API Lemlist")
    ap.add_argument("--campagne-id", help="lemlist : limiter a une campagne")
    ap.add_argument("--sans-linkedin", action="store_true", help="ne pas interroger Unipile")
    ap.add_argument("--depuis", type=int, help="ne garder que les reponses des N derniers jours (date connue)")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = []
    if not a.sans_linkedin:
        lignes += linkedin(a.dry_run)
    if a.lemlist_json:
        lignes += lemlist(a.lemlist_json)
    elif not a.sans_lemlist and not a.dry_run:
        import os
        from gtm_common import load_env
        load_env()
        if os.environ.get("LEMLIST_API_KEY"):
            lignes += lemlist_api(a.depuis, a.campagne_id)
        else:
            afficher("  [lemlist] pas de LEMLIST_API_KEY : reponses email non lues (connecter-outils)")
    if a.dry_run:
        return
    if a.depuis:
        seuil = (date.today() - timedelta(days=a.depuis)).isoformat()
        lignes = [l for l in lignes if not l.get("reponse_date") or l["reponse_date"] >= seuil]
    lignes.sort(key=lambda l: l.get("reponse_date") or "", reverse=True)
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, a.sujet or "inbox")
    ecrire_csv(lignes, sortie)
    nl = sum(1 for l in lignes if l["reponse_canal"] == "linkedin")
    afficher(f"{len(lignes)} reponse(s) : {nl} LinkedIn, {len(lignes) - nl} email -> {sortie}")
    for l in lignes[:3]:
        afficher(f"  - {l.get('prenom')} {l.get('nom')} ({l['reponse_canal']}, {l.get('reponse_date') or 'date ?'}) : {(l.get('reponse_texte') or '')[:120]}")

    if a.entree:
        liste = lire_csv(a.entree)
        par_pid = {l["provider_id"]: l for l in lignes if l.get("provider_id")}
        par_url = {l["linkedin_url"]: l for l in lignes if l.get("linkedin_url")}
        par_email = {l["email"]: l for l in lignes if l.get("email")}
        n = 0
        for l in liste:
            rep = par_pid.get(l.get("provider_id") or "") or par_url.get(norm_linkedin_url(l.get("linkedin_url"))) or par_email.get((l.get("email") or "").lower())
            if rep:
                l["ne_plus_contacter"] = "oui"
                l["reponse_canal"] = rep["reponse_canal"]
                l["reponse_date"] = rep.get("reponse_date", "")
                l["reponse_texte"] = rep.get("reponse_texte", "")
                n += 1
        sortie2 = Path(a.out).with_name(Path(a.out).stem + "_maj.csv") if a.out else chemin_sortie(VERBE, sujet_depuis_fichier(a.entree, a.sujet), suffixe="maj")
        ecrire_csv(liste, sortie2)
        afficher(f"{n} ligne(s) de la liste marquees ne_plus_contacter = oui -> {sortie2}")


if __name__ == "__main__":
    main()
