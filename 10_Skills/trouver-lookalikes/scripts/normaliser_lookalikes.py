"""normaliser_lookalikes : transforme un resultat Ocean.io (export CSV telecharge, ou JSON colle depuis
le MCP) en CSV normalise du module GTM. Aucun appel API : les credits Ocean sont depenses par le MCP,
ce script ne fait que ranger.

Usage :
  python3 normaliser_lookalikes.py --in export_ocean.csv --sujet "clients-2026" [--seeds clients.csv]
  python3 normaliser_lookalikes.py --in resultats_mcp.json --sujet "clients-2026"
  python3 normaliser_lookalikes.py --seeds clients.csv --plan          affiche les lots de 10 domaines a passer au MCP

--seeds : CSV de clients (colonne domaine, ou email, ou site_web) : les domaines seeds sont retires
du resultat (on ne prospecte pas ses propres clients) et la colonne `seed_lot` indique quel lot a
produit la ligne quand le JSON contient une cle `seed_lot`.
Sortie : Listes-prospection/trouver-lookalikes_<sujet>_<date>.csv
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
from gtm_common import afficher, aujourd_hui, arret, chemin_sortie, domaine, ecrire_csv, lire_csv, norm_linkedin_url  # noqa: E402

VERBE = "trouver-lookalikes"
ALIAS = {
    "entreprise": ["name", "company.name", "Name", "Company", "Company name", "nom"],
    "domaine": ["domain", "company.domain", "Domain", "Website", "rootUrl", "company.rootUrl", "site_web"],
    "secteur": ["industries", "company.industries", "Industries", "Industry", "linkedinIndustry"],
    "effectif": ["companySize", "company.companySize", "Company size", "Size", "employeesCount",
                 "company.medias.linkedin.employeesCount", "Employees"],
    "pays": ["primaryCountry", "company.primaryCountry", "Country", "Primary country"],
    "ville": ["locality", "company.locations.locality", "City", "Locality"],
    "chiffre_affaires": ["revenue", "company.revenue", "Revenue"],
    "description": ["description", "company.description", "Description"],
    "technos": ["technologies", "company.technologies", "Technologies"],
    "annee_creation": ["yearFounded", "company.yearFounded", "Year founded"],
    "linkedin_entreprise_url": ["linkedin", "LinkedIn", "linkedinUrl", "LinkedIn URL", "medias.linkedin.url"],
    "score_lookalike": ["relevance", "Relevance", "similarity", "score", "relevanceTier"],
}


def _val(d: dict, cles: list[str]):
    for c in cles:
        cur = d
        for part in c.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur not in (None, "", [], {}):
            return cur
    return ""


def _linkedin(d: dict) -> str:
    medias = d.get("medias") or d.get("company.medias") or {}
    if isinstance(medias, dict):
        li = medias.get("linkedin")
        if isinstance(li, dict):
            return norm_linkedin_url(li.get("url") or li.get("link") or "")
        if isinstance(li, str):
            return norm_linkedin_url(li)
    if isinstance(medias, list):
        for m in medias:
            if isinstance(m, dict) and "linkedin" in (m.get("type") or m.get("name") or "").lower():
                return norm_linkedin_url(m.get("url") or "")
    return norm_linkedin_url(_val(d, ALIAS["linkedin_entreprise_url"]))


def _plat(v) -> str:
    if isinstance(v, list):
        return " | ".join(_plat(x) for x in v if x not in (None, ""))
    if isinstance(v, dict):
        return v.get("name") or v.get("value") or json.dumps(v, ensure_ascii=False)
    return "" if v is None else str(v)


def charger(chemin: Path) -> list[dict]:
    if chemin.suffix.lower() == ".json":
        data = json.loads(chemin.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for cle in ("companies", "results", "data", "items"):
                if isinstance(data.get(cle), list):
                    return data[cle]
            return [data]
        return data
    return lire_csv(chemin)


def domaines_seeds(chemin: str | None) -> list[str]:
    if not chemin:
        return []
    out = []
    for l in lire_csv(chemin):
        d = domaine(l.get("domaine") or l.get("site_web") or l.get("email") or l.get("domain") or "")
        if d and d not in out:
            out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", help="export Ocean (CSV) ou JSON des resultats MCP")
    ap.add_argument("--seeds", help="CSV des clients de reference (domaine, site_web ou email)")
    ap.add_argument("--sujet", default="clients")
    ap.add_argument("--plan", action="store_true", help="afficher les lots de 10 domaines seeds pour le MCP, sans rien ecrire")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true", help="lire et compter sans ecrire")
    a = ap.parse_args()

    seeds = domaines_seeds(a.seeds)
    if a.plan:
        if not seeds:
            arret("--plan demande --seeds avec au moins un domaine")
        for i in range(0, len(seeds), 10):
            afficher(f"lot {i // 10 + 1} : {', '.join(seeds[i:i + 10])}")
        afficher("Passez chaque lot dans search_companies (company_filters.lookalikeDomains, max 10 par appel).")
        return
    if not a.entree:
        arret("--in est requis (ou --plan avec --seeds)")

    brut = charger(Path(a.entree))
    lignes, exclus_seed, vus = [], 0, set()
    for d in brut:
        dom = domaine(_plat(_val(d, ALIAS["domaine"])))
        if dom in seeds:
            exclus_seed += 1
            continue
        if dom and dom in vus:
            continue
        vus.add(dom)
        locs = d.get("locations") or d.get("company.locations") or []
        ville = _plat(_val(d, ALIAS["ville"])) or (_plat(_val(locs[0], ["locality", "city"])) if isinstance(locs, list) and locs and isinstance(locs[0], dict) else "")
        ligne = {"entreprise": _plat(_val(d, ALIAS["entreprise"])), "domaine": dom,
                 "linkedin_entreprise_url": _linkedin(d), "ville": ville,
                 "pays": _plat(_val(d, ALIAS["pays"])), "secteur": _plat(_val(d, ALIAS["secteur"])),
                 "effectif": _plat(_val(d, ALIAS["effectif"])), "source": "ocean",
                 "date_extraction": aujourd_hui(), "score_lookalike": _plat(_val(d, ALIAS["score_lookalike"])),
                 "seed_lot": _plat(d.get("seed_lot", "")), "chiffre_affaires": _plat(_val(d, ALIAS["chiffre_affaires"])),
                 "annee_creation": _plat(_val(d, ALIAS["annee_creation"])), "technos": _plat(_val(d, ALIAS["technos"]))[:300],
                 "description": _plat(_val(d, ALIAS["description"]))[:300]}
        lignes.append(ligne)
    if a.dry_run:
        afficher(f"[dry-run] {len(brut)} lignes lues, {len(lignes)} gardees, {exclus_seed} retirees (clients seeds)")
        return
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, a.sujet)
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} lookalikes ({exclus_seed} clients seeds retires, {len(brut) - len(lignes) - exclus_seed} doublons) -> {sortie}")


if __name__ == "__main__":
    main()
