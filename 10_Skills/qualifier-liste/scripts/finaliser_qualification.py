"""finaliser_qualification : applique les portes d'exclusion et le bareme ICP (tires de contexte.md par Claude, ecrits
dans un fichier de regles JSON), puis les corrections ligne a ligne de Claude (fichier de scores), et ecrit un CSV avec toutes les lignes (gardees
triees par score, puis exclues avec leur raison, colonne exclu) et une copie des exclues seules. Aucun appel API.

Usage :
  python3 finaliser_qualification.py --in liste_pre.csv --regles regles.json [--scores scores.csv] [--sujet x]

regles.json (chaque bloc est optionnel) :
{
  "exclusions": [
    {"colonne": "secteur", "contient": ["interim", "ecole"], "raison": "secteur exclu"},
    {"colonne": "entreprise", "egal": ["Cabinet X"], "raison": "concurrent"},
    {"colonne": "effectif_num", "min": 5, "max": 2000, "raison": "taille hors cible"},
    {"colonne": "categorie_titre", "dans": ["stagiaire", "executant"], "raison": "pas decideur"},
    {"colonne": "domaine_generique", "egal": ["oui"], "raison": "email grand public, pas une entreprise"}
  ],
  "points": [
    {"nom": "secteur", "colonne": "secteur", "exact": ["saas", "logiciel"], "adjacent": ["it", "conseil"], "points_exact": 15, "points_adjacent": 7},
    {"nom": "effectif", "colonne": "effectif_num", "exact_min": 50, "exact_max": 500, "adjacent_min": 20, "adjacent_max": 1000, "points_exact": 10, "points_adjacent": 5},
    {"nom": "zone", "colonne": "pays", "exact": ["france", "fr"], "adjacent": ["belgique", "suisse"], "points_exact": 8, "points_adjacent": 4},
    {"nom": "techno", "colonne": "technos", "exact": ["hubspot"], "points_exact": 12, "points_absent": 6},
    {"nom": "signal 1", "colonne": "signal_type", "exact": ["offre_emploi", "vague_recrutement"], "fraicheur_max": 30, "points_exact": 15},
    {"nom": "engagement", "colonne": "signal_type", "exact": ["commentaire", "like"], "fraicheur_max": 7, "points_exact": 5}
  ],
  "bonus_empilement": 10,
  "tiers": {"A": 75, "B": 55, "C": 35}
}
Regles : "contient" et "exact"/"adjacent" comparent en minuscules sans accents, sous-chaine. "egal" compare la valeur entiere.
"min"/"max" excluent si la valeur numerique est hors bornes (ou vide si "vide_exclut": true). "fraicheur_max" : le point
n'est donne que si la colonne fraicheur est inferieure ou egale. "points_absent" : points quand aucune valeur (ni exact ni
adjacent) n'est trouvee (cas "aucun concurrent visible"). Le score est plafonne a 100 ; sous le seuil C, exclu = oui.

scores.csv (corrections de Claude, prioritaires) : colonnes cle, score_icp, tier, exclu, raison_exclusion, note.
`cle` = valeur de la colonne cle de pre_qualifier (linkedin_url normalisee, sinon email, sinon entreprise|nom).
Sorties : Listes-prospection/qualifier-liste_<sujet>_<date>.csv (toutes les lignes) et ..._exclus.csv (copie des exclues)
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
from gtm_common import afficher, arret, chemin_sortie, ecrire_csv, lire_csv, norm_linkedin_url, norm_texte, sujet_depuis_fichier  # noqa: E402

VERBE = "qualifier-liste"


def _num(v):
    try:
        return float(str(v).replace(" ", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def exclure(ligne: dict, regles: list[dict]) -> str:
    for r in regles:
        val = ligne.get(r.get("colonne", ""), "")
        n = norm_texte(val)
        raison = r.get("raison", f"regle sur {r.get('colonne')}")
        if r.get("contient") and any(norm_texte(x) in n for x in r["contient"] if x):
            return raison
        if r.get("egal") and any(norm_texte(x) == n for x in r["egal"]):
            return raison
        if r.get("dans") and n in {norm_texte(x) for x in r["dans"]}:
            return raison
        if "min" in r or "max" in r:
            x = _num(val)
            if x is None:
                if r.get("vide_exclut"):
                    return raison + " (valeur vide)"
                continue
            if ("min" in r and x < r["min"]) or ("max" in r and x > r["max"]):
                return raison
    return ""


def points(ligne: dict, regles: list[dict], bonus_empilement: int) -> tuple[int, str]:
    total, detail, signaux = 0, [], 0
    for r in regles:
        val = ligne.get(r.get("colonne", ""), "")
        n = norm_texte(val)
        x = _num(val)
        nom = r.get("nom", r.get("colonne"))
        fr = _num(ligne.get("fraicheur"))
        if "fraicheur_max" in r and (fr is None or fr > r["fraicheur_max"]):
            detail.append(f"{nom} 0 (trop ancien ou sans date)")
            continue
        gagne, lib = 0, ""
        if "exact_min" in r or "exact_max" in r:
            if x is not None and (x >= r.get("exact_min", -1e18)) and (x <= r.get("exact_max", 1e18)):
                gagne, lib = r.get("points_exact", 0), "exact"
            elif x is not None and (x >= r.get("adjacent_min", -1e18)) and (x <= r.get("adjacent_max", 1e18)):
                gagne, lib = r.get("points_adjacent", 0), "adjacent"
        else:
            if r.get("exact") and n and any(norm_texte(e) in n for e in r["exact"] if e):
                gagne, lib = r.get("points_exact", 0), "exact"
            elif r.get("adjacent") and n and any(norm_texte(e) in n for e in r["adjacent"] if e):
                gagne, lib = r.get("points_adjacent", 0), "adjacent"
            elif "points_absent" in r:
                gagne, lib = r["points_absent"], "absent"
        if gagne and ligne.get("signal_type") and r.get("colonne") == "signal_type":
            signaux += 1
        total += gagne
        detail.append(f"{nom} {gagne}" + (f" ({lib})" if lib else ""))
    if signaux >= 2 and bonus_empilement:
        total += bonus_empilement
        detail.append(f"empilement +{bonus_empilement}")
    return min(100, total), " ; ".join(detail)


def tier_de(score: int, seuils: dict) -> str:
    for t in ("A", "B", "C"):
        if score >= seuils.get(t, {"A": 75, "B": 55, "C": 35}[t]):
            return t
    return "D"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True, help="CSV sorti de pre_qualifier.py")
    ap.add_argument("--regles", help="JSON des portes et du bareme (tire de contexte.md)")
    ap.add_argument("--scores", help="CSV de corrections ligne a ligne (cle, score_icp, tier, exclu, raison_exclusion, note)")
    ap.add_argument("--sujet", default="")
    ap.add_argument("--out")
    a = ap.parse_args()

    if not a.regles and not a.scores:
        arret("donnez --regles regles.json et/ou --scores scores.csv")
    regles = json.loads(Path(a.regles).read_text(encoding="utf-8")) if a.regles else {}
    seuils = regles.get("tiers", {"A": 75, "B": 55, "C": 35})
    lignes = lire_csv(a.entree)
    corrections = {}
    if a.scores:
        for s in lire_csv(a.scores):
            k = norm_linkedin_url(s.get("cle")) or (s.get("cle") or "").strip().lower()
            if k:
                corrections[k] = s
    gardees, exclus = [], []
    for l in lignes:
        cle = norm_linkedin_url(l.get("cle") or l.get("linkedin_url")) or (l.get("cle") or l.get("email") or "").strip().lower()
        raison = exclure(l, regles.get("exclusions", [])) if regles else ""
        score, detail = points(l, regles.get("points", []), regles.get("bonus_empilement", 0)) if regles else (0, "")
        l["score_icp"], l["detail_score"] = score, detail
        l["tier"] = tier_de(score, seuils) if regles else ""
        if regles and not raison and l["tier"] == "D":
            raison = f"score {score} sous le seuil C ({seuils.get('C', 35)})"
        corr = corrections.get(cle)
        if corr:
            if corr.get("score_icp"):
                l["score_icp"] = int(_num(corr["score_icp"]) or 0)
                l["tier"] = corr.get("tier") or tier_de(l["score_icp"], seuils)
            if corr.get("tier"):
                l["tier"] = corr["tier"]
            if (corr.get("exclu") or "").strip().lower() in ("oui", "yes", "1", "true"):
                raison = corr.get("raison_exclusion") or "exclu par relecture"
            elif (corr.get("exclu") or "").strip().lower() in ("non", "no", "0", "false"):
                raison = ""
            if corr.get("note"):
                l["note_qualification"] = corr["note"]
        l["exclu"] = "oui" if raison else "non"
        l["raison_exclusion"] = raison
        (exclus if raison else gardees).append(l)
    gardees.sort(key=lambda r: -(int(r.get("score_icp") or 0)))
    sujet = sujet_depuis_fichier(a.entree.replace("_pre", ""), a.sujet)
    sortie = Path(a.out) if a.out else chemin_sortie(VERBE, sujet)
    ecrire_csv(gardees + exclus, sortie)  # toutes les lignes : gardees triees par score, puis exclues (colonne exclu)
    sortie2 = sortie.with_name(sortie.stem + "_exclus.csv")
    ecrire_csv(exclus, sortie2)  # copie des exclues seules, pour lecture
    par_tier: dict = {}
    for l in gardees:
        par_tier[l["tier"]] = par_tier.get(l["tier"], 0) + 1
    raisons: dict = {}
    for l in exclus:
        raisons[l["raison_exclusion"]] = raisons.get(l["raison_exclusion"], 0) + 1
    afficher(f"{len(gardees)} gardees ({', '.join(f'{t}: {n}' for t, n in sorted(par_tier.items()))}) -> {sortie}")
    afficher(f"{len(exclus)} exclues -> {sortie2}")
    for r, n in sorted(raisons.items(), key=lambda x: -x[1])[:5]:
        afficher(f"  {n:4d}  {r}")


if __name__ == "__main__":
    main()
