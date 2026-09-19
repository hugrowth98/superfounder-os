#!/usr/bin/env python3
"""trouver_lookalikes : entreprises semblables a vos meilleurs clients, par l'API Ocean.io (verbe trouver_lookalikes).

Entree : un CSV de clients de reference (colonne domaine, site_web ou email) ou --domaines a,b,c. Ocean prend jusqu'a
10 domaines de reference par recherche : au-dela, le script fait plusieurs lots et fusionne. L'apercu (gratuit) donne
le total avant de payer 0,2 credit par resultat.

Usage :
  python3 trouver_lookalikes.py --seeds clients.csv --pays fr --tailles 11-50,51-200 --max 100 --dry-run
  python3 trouver_lookalikes.py --domaines acme.fr,beta.com --pays fr,be --max 50
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import Ocean, afficher, arret, aujourd_hui, bandeau_dry_run, chemin_sortie, domaine, ecrire_csv, lire_csv, norm_linkedin_url  # noqa: E402

VERBE = "trouver-lookalikes"
TAILLES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]


def seeds_depuis(a) -> list[str]:
    doms = []
    if a.domaines:
        doms += [domaine(x) for x in a.domaines.split(",")]
    if a.seeds:
        for l in lire_csv(a.seeds):
            d = domaine(l.get("domaine") or l.get("site_web") or (l.get("email") or "").split("@")[-1])
            if d:
                doms.append(d)
    doms = sorted({d for d in doms if d})
    if not doms:
        arret("aucun domaine de reference : --domaines ou --seeds <csv avec domaine, site_web ou email>")
    return doms


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", help="CSV des clients de reference")
    ap.add_argument("--domaines", help="domaines de reference separes par des virgules")
    ap.add_argument("--pays", help="codes pays ISO en minuscules : fr,be,ch")
    ap.add_argument("--tailles", help="tranches : " + ",".join(TAILLES))
    ap.add_argument("--max", type=int, default=100, help="resultats max au total")
    ap.add_argument("--sujet", default="clients")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    seeds = seeds_depuis(a)
    pays = [p.strip() for p in a.pays.split(",")] if a.pays else None
    tailles = [t.strip() for t in a.tailles.split(",")] if a.tailles else None
    for t in tailles or []:
        if t not in TAILLES:
            arret(f"taille inconnue : {t}")
    lots = [seeds[i:i + 10] for i in range(0, len(seeds), 10)]
    par_lot = max(1, a.max // len(lots))
    resume = [f"{len(seeds)} domaine(s) de reference en {len(lots)} lot(s) de 10 max", f"filtres : pays={pays or 'tous'}, tailles={tailles or 'toutes'}",
              f"resultats : jusqu'a {par_lot} par lot, {a.max} au total ; cout : 0,2 credit par resultat, soit au plus {a.max * 0.2:.0f} credit(s)"]
    if a.dry_run:
        bandeau_dry_run("Ocean.io lookalikes", resume + ["l'apercu gratuit donnera le total disponible au vrai run"])
        return
    oc = Ocean()
    vus, lignes = set(seeds), []
    for n, lot in enumerate(lots, 1):
        total = oc.apercu_lookalikes(lot, pays, tailles, exclure=seeds)
        afficher(f"  [ocean] lot {n}/{len(lots)} : {total} entreprise(s) semblables disponibles, on en prend {min(par_lot, total)}")
        for c in oc.lookalikes(lot, taille_page=min(50, par_lot), max_resultats=par_lot, pays=pays, tailles=tailles, exclure=seeds):
            d = domaine(c.get("domain") or "")
            if not d or d in vus:
                continue
            vus.add(d)
            lignes.append({"entreprise": c.get("name", ""), "domaine": d, "linkedin_entreprise_url": norm_linkedin_url(c.get("linkedinUrl") or c.get("linkedin_url") or ""),
                           "pays": c.get("primaryCountry", ""), "ville": c.get("primaryCity", "") or c.get("city", ""),
                           "secteur": "|".join(c.get("industries") or []) if isinstance(c.get("industries"), list) else c.get("industries", ""),
                           "effectif": c.get("companySize", ""), "source": "ocean", "date_extraction": aujourd_hui(),
                           "technos": "|".join(c.get("technologies") or []) if isinstance(c.get("technologies"), list) else "",
                           "seeds": ",".join(lot), "signal_type": "lookalike", "signal_detail": f"ressemble a {', '.join(lot[:3])}"})
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, a.sujet)
    ecrire_csv(lignes, sortie, colonnes_extra=["technos", "seeds"])
    afficher(f"{len(lignes)} lookalike(s) -> {sortie}")


if __name__ == "__main__":
    main()
