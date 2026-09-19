"""dedoublonner : fusionne une ou plusieurs listes en supprimant les doublons, journalise chaque fusion, et (option)
croise avec HubSpot ou avec un fichier de reference (deja contactes, ne plus contacter).

Cles, dans l'ordre : linkedin_url normalisee, puis email (minuscules), puis domaine + nom (personnes) ou domaine,
linkedin_entreprise_url, nom d'entreprise (listes d'entreprises). Deux lignes qui partagent une cle fusionnent, la
valeur la plus complete gagne colonne par colonne (statut d'email le plus fiable, score le plus haut, signal le plus
recent, sources concatenees, exclu = oui si l'une des deux l'est).

Usage :
  python3 dedoublonner.py --in a.csv [--in b.csv ...] [--sujet x]
  python3 dedoublonner.py --in liste.csv --hubspot                     annote ce qui existe dans HubSpot (dans_crm, hubspot_contact_id)
  python3 dedoublonner.py --in liste.csv --hubspot --exclure-crm        annote et met exclu = oui sur ces lignes
  python3 dedoublonner.py --in liste.csv --max-par-entreprise 3         garde au plus 3 personnes par domaine (defaut 5, 0 = illimite)
  python3 dedoublonner.py --in liste.csv --contre deja_contactes.csv    exclut ce qui est dans un fichier de reference
  python3 dedoublonner.py --in liste.csv --dry-run                      compte sans ecrire
Sorties : Listes-prospection/dedoublonner_<sujet>_<date>.csv et ..._doublons.csv (journal)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import HubSpot, afficher, arret, bandeau_dry_run, chemin_sortie, domaine, ecrire_csv, lire_csv, norm_linkedin_url, norm_texte, sujet_depuis_fichier  # noqa: E402

VERBE = "dedoublonner"
ORDRE_STATUT = {"DELIVERABLE": 5, "HIGH_PROBABILITY": 4, "CATCH_ALL": 3, "LINKEDIN_1ER_DEGRE": 2, "APIFY_NON_VERIFIE": 1, "": 0, "NOT_FOUND": -1, "INVALID": -2, "INVALID_DOMAIN": -2}


def est_liste_personnes(lignes: list[dict]) -> bool:
    avec_nom = sum(1 for l in lignes if (l.get("nom") or l.get("prenom") or l.get("linkedin_url")))
    return avec_nom >= max(1, len(lignes) // 2)


def cles(l: dict, personnes: bool) -> list[tuple[str, str]]:
    out = []
    if personnes:
        u = norm_linkedin_url(l.get("linkedin_url"))
        if u:
            out.append(("linkedin_url", u))
        e = (l.get("email") or "").strip().lower()
        if e and "@" in e:
            out.append(("email", e))
        d, n = domaine(l.get("domaine") or ""), norm_texte(l.get("nom"))
        p = norm_texte(l.get("prenom"))
        if d and n:
            out.append(("domaine+nom", f"{d}|{n}|{p[:1]}"))
        elif norm_texte(l.get("entreprise")) and n:
            out.append(("entreprise+nom", f"{norm_texte(l.get('entreprise'))}|{n}|{p[:1]}"))
    else:
        d = domaine(l.get("domaine") or l.get("site_web") or "")
        if d:
            out.append(("domaine", d))
        u = norm_linkedin_url(l.get("linkedin_entreprise_url"))
        if u:
            out.append(("linkedin_entreprise_url", u))
        n = norm_texte(l.get("entreprise"))
        if n:
            out.append(("entreprise", n))
    return out


def fusion(a: dict, b: dict) -> dict:
    r = dict(a)
    for k, vb in b.items():
        va = r.get(k, "")
        vb = "" if vb is None else str(vb)
        if k == "email_statut":
            if ORDRE_STATUT.get(vb.upper(), 0) > ORDRE_STATUT.get((va or "").upper(), 0):
                r[k] = vb
                if b.get("email"):
                    r["email"] = b["email"]
            continue
        if k == "email" and va and vb and va.lower() != vb.lower():
            continue  # tranche par email_statut
        if k in ("score_icp", "score_signal"):
            if not (va or "").strip() or not vb.strip():
                r[k] = (va or "").strip() or vb.strip()
            else:
                try:
                    r[k] = str(max(int(float(va)), int(float(vb))))
                except ValueError:
                    r[k] = va or vb
            continue
        if k == "source":
            parts = [p for p in (va or "").split("+") if p] + [p for p in vb.split("+") if p]
            r[k] = "+".join(dict.fromkeys(parts))
            continue
        if k == "exclu":
            r[k] = "oui" if "oui" in (va, vb) else (va or vb)
            continue
        if k in ("signal_type", "signal_date", "signal_detail", "fraicheur"):
            continue  # gere en bloc ci-dessous
        if len(vb.strip()) > len((va or "").strip()):
            r[k] = vb
    sa, sb = (a.get("signal_date") or ""), (b.get("signal_date") or "")
    plus_recent = b if sb > sa else a
    for k in ("signal_type", "signal_date", "signal_detail", "fraicheur"):
        if plus_recent.get(k):
            r[k] = plus_recent[k]
    sig = [s for s in (a.get("signaux") or "").split(" | ") if s]
    for src in (a, b):
        if src.get("signal_type"):
            tag = f"{src['signal_type']}:{src.get('signal_date', '')}"
            if tag not in sig:
                sig.append(tag)
    if sig:
        r["signaux"] = " | ".join(sig)
        r["nb_signaux"] = str(len(sig))
    return r


def dedoublonner(lignes: list[dict], personnes: bool) -> tuple[list[dict], list[dict]]:
    groupes: list[dict] = []
    index: dict = {}
    journal = []
    for i, l in enumerate(lignes):
        ks = cles(l, personnes)
        cible = next((index[k] for k in ks if k in index), None)
        if cible is None:
            gid = len(groupes)
            groupes.append({"ligne": dict(l), "membres": [i], "cles": set(ks)})
            for k in ks:
                index[k] = gid
            continue
        g = groupes[cible]
        cle_match = next(k for k in ks if k in index)
        journal.append({"groupe": cible + 1, "type_cle": cle_match[0], "cle": cle_match[1], "ligne_gardee": g["membres"][0] + 2,
                        "ligne_fusionnee": i + 2, "fichier": l.get("_fichier", ""),
                        "entreprise": l.get("entreprise", ""), "nom": f"{l.get('prenom', '')} {l.get('nom', '')}".strip()})
        g["ligne"] = fusion(g["ligne"], l)
        g["membres"].append(i)
        for k in ks:
            if k not in index:
                index[k] = cible
    resultat = []
    for g in groupes:
        l = g["ligne"]
        for col in ("linkedin_url", "linkedin_entreprise_url"):
            n = norm_linkedin_url(l.get(col))
            if n:
                l[col] = n
        if l.get("email"):
            l["email"] = l["email"].strip().lower()
        if l.get("domaine"):
            l["domaine"] = domaine(l["domaine"])
        resultat.append(l)
    return resultat, journal


def croiser_hubspot(lignes: list[dict], personnes: bool, exclure: bool, dry_run: bool) -> int:
    emails = [l.get("email") for l in lignes if l.get("email") and "@" in l["email"]]
    doms = [domaine(l.get("domaine") or "") for l in lignes if domaine(l.get("domaine") or "")]
    if dry_run:
        bandeau_dry_run("HubSpot search", [f"{len(set(emails))} emails a verifier (lots de 100), {len(set(doms))} domaines (lots de 90)", "cout : aucun (API HubSpot)"])
        return 0
    hs = HubSpot()
    contacts = hs.contacts_par_email(emails) if emails else {}
    entreprises = hs.entreprises_par_domaine(doms) if doms else {}
    n = 0
    for l in lignes:
        c = contacts.get((l.get("email") or "").strip().lower())
        e = entreprises.get(domaine(l.get("domaine") or ""))
        if c:
            l["hubspot_contact_id"] = c["id"]
            l["hubspot_lifecycle"] = (c.get("props") or {}).get("lifecyclestage", "")
        if e:
            l["hubspot_entreprise_id"] = e
        dans = bool(c) or (not personnes and bool(e))
        l["dans_crm"] = "oui" if dans else "non"
        if dans:
            n += 1
            if exclure:
                l["exclu"] = "oui"
                l["raison_exclusion"] = l.get("raison_exclusion") or ("deja dans HubSpot (contact)" if c else "deja dans HubSpot (entreprise)")
    return n


def croiser_fichier(lignes: list[dict], reference: str, personnes: bool) -> int:
    ref = lire_csv(reference)
    ref_cles = {k for r in ref for k in cles(r, personnes)}
    n = 0
    for l in lignes:
        if any(k in ref_cles for k in cles(l, personnes)):
            l["exclu"] = "oui"
            l["raison_exclusion"] = l.get("raison_exclusion") or f"deja dans {Path(reference).name}"
            n += 1
    return n



def plafonner(lignes: list[dict], n: int, journal: list[dict]) -> int:
    """Garde au plus n personnes par domaine (ou par entreprise si pas de domaine) : meilleur score_icp, puis ligne la plus remplie."""
    groupes: dict[str, list[dict]] = {}
    for l in lignes:
        cle = domaine(l.get("domaine") or "") or norm_texte(l.get("entreprise") or "")
        if cle:
            groupes.setdefault(cle, []).append(l)
    retires = 0
    for cle, grp in groupes.items():
        if len(grp) <= n:
            continue
        grp.sort(key=lambda l: (-float(l.get("score_icp") or 0), -sum(1 for v in l.values() if v)))
        for l in grp[n:]:
            if (l.get("exclu") or "").lower() != "oui":
                l["exclu"] = "oui"
                l["raison_exclusion"] = l.get("raison_exclusion") or f"plafond {n} par entreprise"
                journal.append({"cle": cle, "raison": f"plafond {n} par entreprise", "email": l.get("email", ""), "linkedin_url": l.get("linkedin_url", "")})
                retires += 1
    return retires


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entrees", action="append", required=True, help="un ou plusieurs CSV (repetable)")
    ap.add_argument("--hubspot", action="store_true", help="croiser avec HubSpot (HUBSPOT_ACCESS_TOKEN)")
    ap.add_argument("--exclure-crm", action="store_true", help="avec --hubspot : mettre exclu = oui sur les lignes deja dans HubSpot (par defaut : annoter seulement dans_crm)")
    ap.add_argument("--sans-exclure", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--max-par-entreprise", type=int, default=5, help="garder au plus N personnes par domaine (meilleur score_icp puis plus complet), 0 = illimite")
    ap.add_argument("--contre", action="append", help="CSV de reference (deja contactes, ne plus contacter), repetable")
    ap.add_argument("--type", choices=["personnes", "entreprises"], help="forcer le type de liste (detecte sinon)")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lignes = []
    for f in a.entrees:
        for l in lire_csv(f):
            l["_fichier"] = Path(f).name
            lignes.append(l)
    if not lignes:
        arret("aucune ligne lue")
    personnes = (a.type == "personnes") if a.type else est_liste_personnes(lignes)
    uniques, journal = dedoublonner(lignes, personnes)
    afficher(f"  [{'personnes' if personnes else 'entreprises'}] {len(lignes)} lignes lues dans {len(a.entrees)} fichier(s), {len(uniques)} uniques, {len(journal)} fusion(s)")
    n_crm = croiser_hubspot(uniques, personnes, bool(a.exclure_crm), a.dry_run) if a.hubspot else 0
    n_plafond = plafonner(uniques, a.max_par_entreprise, journal) if (personnes and a.max_par_entreprise) else 0
    if n_plafond:
        afficher(f"  [plafond] {n_plafond} personne(s) au-dela de {a.max_par_entreprise} par entreprise : exclu = oui")
    n_ref = sum(croiser_fichier(uniques, r, personnes) for r in (a.contre or []))
    if a.dry_run:
        afficher(f"[dry-run] {n_ref} ligne(s) presentes dans les fichiers de reference ; rien ecrit")
        return
    for l in uniques:
        l.pop("_fichier", None)
    sujet = a.sujet or sujet_depuis_fichier(a.entrees[0])
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(uniques, sortie)
    sortie2 = sortie.with_name(sortie.stem + "_doublons.csv")
    ecrire_csv(journal, sortie2)
    prospectables = sum(1 for l in uniques if (l.get("exclu") or "non") != "oui")
    afficher(f"{len(uniques)} lignes -> {sortie} ({prospectables} prospectables"
             + (f", {n_crm} deja dans HubSpot" if a.hubspot else "") + (f", {n_ref} dans les fichiers de reference" if a.contre else "") + ")")
    afficher(f"{len(journal)} fusion(s) journalisee(s) -> {sortie2}")


if __name__ == "__main__":
    main()
