"""detecter_techno : la stack technique d'une liste de domaines (CMS, e-commerce, analytics, marketing, chat, CRM,
paiement, hebergement, frameworks) via Apify scrapemint/website-tech-stack-detector, une ligne par domaine.
Mode diff : compare au dernier run enregistre (historique_technos.json) et signale ajouts et retraits.

Usage :
  python3 detecter_techno.py --in liste.csv                      colonne domaine (ou site_web, ou email)
  python3 detecter_techno.py --domaines acme.fr,beta.com --diff  ajouts et retraits depuis le dernier run
  python3 detecter_techno.py --in liste.csv --cherche "hubspot,intercom"   marque les domaines qui utilisent ces technos
Cout : 0,01 $ par domaine avec au moins une detection (un site injoignable ou sans detection n'est pas facture).
Sorties : Listes-prospection/detecter-techno_<sujet>_<date>.csv (+ _diff.csv avec --diff)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import (PredictLeads, afficher, arret, aujourd_hui, bandeau_dry_run, chemin_sortie, domaine, ecrire_csv,  # noqa: E402
                        fraicheur, lire_csv, norm_texte, sujet_depuis_fichier)
from apify_run import lancer, prix  # noqa: E402

VERBE = "enrichir-entreprise_techno"
ACTOR = "scrapemint/website-tech-stack-detector"
HISTORIQUE = Path(__file__).resolve().parent / "historique_technos.json"
CATEGORIES = {"cms": ["cms"], "ecommerce": ["ecommerce", "e-commerce"], "analytics": ["analytics"], "marketing": ["marketing", "email", "automation"],
              "chat": ["chat", "widget", "support"], "crm": ["crm"], "paiement": ["payment", "paiement"], "hebergement": ["hosting", "cdn"],
              "framework": ["framework", "javascript", "language"]}


def _liste(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def domaines_depuis(a) -> tuple[list[str], list[dict]]:
    lignes = lire_csv(a.entree) if a.entree else []
    doms = []
    for l in lignes:
        d = domaine(l.get("domaine") or l.get("site_web") or l.get("email") or "")
        l["_dom"] = d
        if d and d not in doms:
            doms.append(d)
    for d in _liste(a.domaines):
        d = domaine(d)
        if d and d not in doms:
            doms.append(d)
    if not doms:
        arret("aucun domaine : --in <csv avec domaine ou site_web> ou --domaines a.com,b.com")
    return doms, lignes


def par_categorie(item: dict) -> dict:
    technos = item.get("technologies") or []
    noms = [t.get("name") for t in technos if isinstance(t, dict) and t.get("name")]
    cats: dict = {k: [] for k in CATEGORIES}
    for t in technos:
        if not isinstance(t, dict):
            continue
        cat = norm_texte(t.get("category"))
        for k, mots in CATEGORIES.items():
            if any(m in cat for m in mots):
                cats[k].append(t.get("name", ""))
                break
    bc = item.get("byCategory") or {}
    if isinstance(bc, dict):
        for k, v in bc.items():
            kk = norm_texte(k)
            for cat, mots in CATEGORIES.items():
                if any(m in kk for m in mots) and isinstance(v, list):
                    for x in v:
                        n = x.get("name") if isinstance(x, dict) else str(x)
                        if n and n not in cats[cat]:
                            cats[cat].append(n)
    return {"technos": noms, **{k: " | ".join(v) for k, v in cats.items()}}


def source_predictleads(a, doms: list[str], lignes: list[dict]) -> None:
    """Detections datees PredictLeads par domaine (first_seen_at, last_seen_at) : un vrai signal de changement, sans diff a faire."""
    if a.dry_run:
        bandeau_dry_run("PredictLeads technology_detections", [f"{len(doms)} domaine(s), une requete chacun", "cout : quota mensuel de l'abonnement"])
        return
    pl = PredictLeads()
    src_par_dom = {l["_dom"]: l for l in lignes if l.get("_dom")}
    cherche = [norm_texte(c) for c in _liste(a.cherche)]
    sortie = []
    for d in doms:
        src = src_par_dom.get(d, {})
        base = {"entreprise": src.get("entreprise", ""), "domaine": d, "linkedin_entreprise_url": src.get("linkedin_entreprise_url", ""),
                "secteur": src.get("secteur", ""), "effectif": src.get("effectif", ""), "source": "predictleads", "date_extraction": aujourd_hui()}
        try:
            dets = pl.par_entreprise(d, "technology_detections")
        except RuntimeError as e:
            sortie.append({**base, "signal_type": "techno", "signal_detail": f"erreur : {e}"[:200]})
            continue
        if not dets:
            sortie.append({**base, "signal_type": "techno", "signal_detail": "aucune detection", "nb_technos": 0})
            continue
        technos = []
        for it in dets:
            nom = it.get("technology_name") or it.get("technology_title") or it.get("technology_slug") or it.get("_id", "")
            premiere = str(it.get("first_seen_at") or "")[:10]
            derniere = str(it.get("last_seen_at") or "")[:10]
            technos.append((nom, premiere, derniere))
            if a.recentes_jours and premiere:
                fr = fraicheur(premiere)
                if fr and int(fr) <= int(a.recentes_jours):
                    sortie.append({**base, "signal_type": "techno_ajout", "signal_date": premiere, "fraicheur": fr, "techno": nom,
                                   "signal_detail": f"adopte {nom} (vu la premiere fois le {premiere})"})
        noms = [n for n, _, _ in technos]
        ligne = {**base, "signal_type": "techno", "signal_date": aujourd_hui(), "fraicheur": "0", "nb_technos": len(noms),
                 "technos": " | ".join(noms), "technos_datees": " | ".join(f"{n} ({p}..{q})" for n, p, q in technos[:60]),
                 "signal_detail": f"{len(noms)} techno(s) : " + ", ".join(noms[:8])}
        if cherche:
            trouvees = [n for n in noms if any(c in norm_texte(n) for c in cherche)]
            ligne["techno_cible"] = "oui" if trouvees else "non"
            ligne["techno_cible_detail"] = " | ".join(trouvees)
        sortie.append(ligne)
    out = Path(a.out) if a.out else chemin_sortie(VERBE, (a.sujet or (sujet_depuis_fichier(a.entree) if a.entree else "domaines")) + "-predictleads")
    ecrire_csv(sortie, out)
    afficher(f"{len(sortie)} ligne(s) (technos datees PredictLeads) -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", help="CSV avec domaine, site_web ou email")
    ap.add_argument("--domaines", help="domaines separes par des virgules")
    ap.add_argument("--diff", action="store_true", help="comparer au dernier run (ajouts, retraits) et ecrire un fichier _diff")
    ap.add_argument("--cherche", help="technos a reperer (marque la colonne techno_cible = oui), separees par des virgules")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source", choices=["apify", "predictleads"], default="apify",
                    help="apify (stack du jour, diff entre deux runs) ou predictleads (detections datees, first_seen_at)")
    ap.add_argument("--recentes-jours", type=int, help="predictleads : sortir une ligne techno_ajout par techno vue pour la premiere fois depuis N jours")
    a = ap.parse_args()

    doms, lignes = domaines_depuis(a)
    if a.source == "predictleads":
        source_predictleads(a, doms, lignes)
        return
    items, _ = lancer(ACTOR, {"websites": doms}, label=f"tech-stack ({len(doms)} domaines)", dry_run=a.dry_run, estimation=prix(ACTOR, len(doms)))
    if a.dry_run:
        return
    hist = json.loads(HISTORIQUE.read_text(encoding="utf-8")) if HISTORIQUE.exists() else {}
    cherche = [norm_texte(c) for c in _liste(a.cherche)]
    par_dom = {}
    for it in items:
        d = domaine(it.get("domain") or it.get("website") or it.get("finalUrl") or "")
        if d:
            par_dom[d] = it
    src_par_dom = {}
    for l in lignes:
        if l.get("_dom") and l["_dom"] not in src_par_dom:
            src_par_dom[l["_dom"]] = l
    sortie_lignes, diffs = [], []
    for d in doms:
        it = par_dom.get(d)
        src = src_par_dom.get(d, {})
        base = {"entreprise": src.get("entreprise", ""), "domaine": d, "linkedin_entreprise_url": src.get("linkedin_entreprise_url", ""),
                "secteur": src.get("secteur", ""), "effectif": src.get("effectif", ""), "source": ACTOR, "date_extraction": aujourd_hui(),
                "signal_type": "techno", "signal_date": aujourd_hui(), "fraicheur": "0"}
        if not it:
            sortie_lignes.append({**base, "joignable": "non", "signal_detail": "site injoignable ou aucune detection", "nb_technos": 0})
            continue
        cats = par_categorie(it)
        technos = cats.pop("technos")
        ligne = {**base, "joignable": "oui" if it.get("reachable", True) else "non", "nb_technos": it.get("techCount", len(technos)),
                 "technos": " | ".join(technos), **cats,
                 "signal_detail": f"{len(technos)} techno(s) : " + ", ".join(technos[:8])}
        if cherche:
            trouvees = [t for t in technos if any(c in norm_texte(t) for c in cherche)]
            ligne["techno_cible"] = "oui" if trouvees else "non"
            ligne["techno_cible_detail"] = " | ".join(trouvees)
        prev = hist.get(d, {})
        if a.diff:
            avant = set(prev.get("technos", []))
            apres = set(technos)
            ajouts, retraits = sorted(apres - avant), sorted(avant - apres)
            ligne["ajouts"] = " | ".join(ajouts)
            ligne["retraits"] = " | ".join(retraits)
            ligne["dernier_run"] = prev.get("date", "")
            if prev and (ajouts or retraits):
                for t in ajouts:
                    diffs.append({**base, "signal_type": "techno_ajout", "signal_detail": f"ajoute {t} (absent le {prev.get('date')})", "techno": t})
                for t in retraits:
                    diffs.append({**base, "signal_type": "techno_retrait", "signal_detail": f"retire {t} (present le {prev.get('date')})", "techno": t})
        hist[d] = {"technos": technos, "date": aujourd_hui()}
        sortie_lignes.append(ligne)
    HISTORIQUE.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    sujet = sujet_depuis_fichier(a.entree, a.sujet) if a.entree else (a.sujet or "domaines")
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(sortie_lignes, sortie)
    afficher(f"{len(sortie_lignes)} domaine(s), {sum(1 for l in sortie_lignes if l.get('joignable') == 'oui')} joignable(s) -> {sortie}")
    if a.diff:
        sortie2 = sortie.with_name(sortie.stem + "_diff.csv")
        ecrire_csv(diffs, sortie2)
        afficher(f"{len(diffs)} changement(s) depuis le dernier run -> {sortie2}")


if __name__ == "__main__":
    main()
