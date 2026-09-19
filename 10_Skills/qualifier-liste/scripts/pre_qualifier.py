"""pre_qualifier : pre-traitement deterministe avant le scoring ICP (aucun appel API).

Ajoute a chaque ligne :
  categorie_titre   dirigeant | marketing | sales | direction | manager | independant | executant | stagiaire | inconnu
  seniorite         fondateur | c_level | vp | directeur | head | manager | senior | junior | autre (si vide)
  independant       oui si le titre ou le headline dit freelance, independant, consultant solo...
  effectif_num      entier tire de `effectif` ("11-50" -> 11, "1 200" -> 1200, "self" -> 1)
  taille_tranche    1-10 | 11-50 | 51-200 | 201-500 | 501-1000 | 1000+
  domaine           depuis l'email si vide (jamais un domaine grand public : gmail, hotmail...)
  domaine_generique oui si l'email est sur un domaine grand public
  cle               linkedin_url normalisee, sinon email, sinon entreprise|nom (pour le fichier de scores)

Usage : python3 pre_qualifier.py --in liste.csv [--out liste_pre.csv]
Le scoring lui-meme (gates, points, tiers) est fait par finaliser_qualification.py a partir des regles
que Claude tire de contexte.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import afficher, domaine, ecrire_csv, lire_csv, norm_linkedin_url, norm_texte, seniorite_depuis_titre  # noqa: E402

DOMAINES_GENERIQUES = {"gmail.com", "hotmail.com", "hotmail.fr", "yahoo.fr", "yahoo.com", "outlook.com", "outlook.fr", "icloud.com",
                       "live.fr", "live.com", "orange.fr", "wanadoo.fr", "free.fr", "sfr.fr", "laposte.net", "protonmail.com", "proton.me", "me.com"}

INDEPENDANT = [r"\bfreelance\b", r"\bindependant[e]?\b", r"\bauto ?entrepreneur", r"\bmicro ?entrepreneur", r"\bsolopreneur\b", r"\bself ?employed\b",
               r"\bportage\b", r"\bfractionn", r"\bfractional\b", r"\ba mon compte\b", r"\bmanager de transition\b", r"\btemps partage\b"]
FONCTIONNEL = [r"\bconsultant[e]?\b", r"\bcoach\b", r"\bformateur\b", r"\bformatrice\b", r"\bconferenci", r"\bexpert[e]?\b", r"\bspecialiste\b",
               r"\bghostwriter\b", r"\bspeaker\b", r"\bauteur[e]?\b", r"\bmentor\b", r"\bcopywriter\b", r"\badvisor\b", r"\bavocat[e]?\b",
               r"\bnotaire\b", r"\bexpert comptable\b", r"\bpsycholog", r"\btherapeute\b", r"\bosteopathe\b", r"\bkinesi", r"\bnutritionniste\b"]
DIRIGEANT = [r"\bceo\b", r"\bpdg\b", r"\bdg\b", r"\bdirecteur general\b", r"\bdirectrice generale\b", r"\bpresident[e]?\b", r"\bfondateur\b",
             r"\bfondatrice\b", r"\bfounder\b", r"\bco ?founder", r"\bcofondat", r"\bco ?fondat", r"\bchief executive\b", r"\bdirigeant[e]?\b",
             r"\bgerant[e]?\b", r"\bowner\b", r"\bproprietaire\b", r"\bmanaging director\b", r"\bmanaging partner\b", r"\bexecutive director\b",
             r"\bchairman\b", r"\bchairwoman\b", r"\bchef d entreprise\b"]
DIRIGEANT_NEGATIF = [r"\bfutur", r"\ben devenir\b", r"\bchef de (groupe|secteur|rayon|produit|service|zone|region|projet)\b", r"\bassistant", r"\boffice manager\b"]
MARKETING = [r"\bcmo\b", r"\bchief marketing", r"\bvp (of )?marketing\b", r"\bhead of marketing\b", r"\bdirect(eur|rice) (du )?marketing\b",
             r"\bmarketing director\b", r"\bdirector of marketing\b", r"\bresponsable marketing\b", r"\bhead of growth\b", r"\bdirect(eur|rice) (de la )?communication\b"]
SALES = [r"\bcro\b", r"\bcco\b", r"\bchief (revenue|commercial|sales)", r"\bvp (of )?sales\b", r"\bvp commercial\b", r"\bhead of sales\b",
         r"\bhead of revenue\b", r"\bdirect(eur|rice) (des |du )?commercial", r"\bdirect(eur|rice) des ventes\b", r"\bsales director\b",
         r"\bdirector of (sales|business development)\b", r"\bresponsable commercial", r"\bhead of business development\b"]
DIRECTION = [r"\bcoo\b", r"\bcfo\b", r"\bcto\b", r"\bcpo\b", r"\bchro\b", r"\bcio\b", r"\bdaf\b", r"\bdrh\b", r"\bdsi\b", r"\bchief [a-z]+ officer\b",
             r"\bvice president", r"\bvp\b", r"\bsvp\b", r"\bevp\b", r"\bhead of\b", r"\bdirect(eur|rice)\b", r"\bdirector\b", r"\bassocie[e]?\b",
             r"\bpartner\b", r"\bcountry manager\b", r"\bgeneral manager\b", r"\bchief of staff\b", r"\bsecretaire general"]
MANAGER = [r"\bmanager\b", r"\bresponsable\b", r"\bchef de\b", r"\bteam lead", r"\bsuperviseur\b", r"\bsupervisor\b", r"\bcharge[e]? de\b", r"\blead\b"]
EXECUTANT = [r"\bproduct owner\b", r"\bingenieur\b", r"\bengineer\b", r"\bdeveloppeur\b", r"\bdeveloper\b", r"\bdesigner\b", r"\banalyst[e]?\b",
             r"\bassistant[e]?\b", r"\bcoordinat", r"\bgrowth hacker\b", r"\bmedia buyer\b", r"\bcommercial[e]?\b", r"\bsdr\b", r"\bbdr\b",
             r"\baccount (manager|executive)\b", r"\bchargee? de clientele\b", r"\btechnicien"]
STAGIAIRE = [r"\bstagiaire\b", r"\bintern\b", r"\balternan", r"\bapprenti", r"\betudiant", r"\bstudent\b"]


def _match(texte: str, motifs: list[str]) -> bool:
    return any(re.search(m, texte) for m in motifs)


def effectif_num(v) -> str:
    s = norm_texte(v)
    if not s:
        return ""
    if any(x in s for x in ("self", "solo", "moi", "myself")):
        return "1"
    s = s.replace(" ", "")
    m = re.search(r"(\d+)", s)
    return m.group(1) if m else ""


def tranche(n: str) -> str:
    if not n:
        return ""
    v = int(n)
    for borne, lib in ((10, "1-10"), (50, "11-50"), (200, "51-200"), (500, "201-500"), (1000, "501-1000")):
        if v <= borne:
            return lib
    return "1000+"


def categorie(titre: str, headline: str, effectif: str) -> tuple[str, str]:
    """(categorie_titre, independant). Le poste actuel (titre) prime sur le headline."""
    t, h = norm_texte(titre), norm_texte(headline)
    combine = f"{t} {h}".strip()
    if not combine:
        return "inconnu", "non"
    if _match(combine, STAGIAIRE):
        return "stagiaire", "non"
    if _match(combine, INDEPENDANT):
        return "independant", "oui"
    if t and _match(t, FONCTIONNEL) and not _match(t, DIRIGEANT + MARKETING + SALES + DIRECTION):
        return "independant", "oui"
    if _match(t, MARKETING):
        return "marketing", "non"
    if _match(t, SALES):
        return "sales", "non"
    if _match(t, DIRIGEANT):
        if _match(t, DIRIGEANT_NEGATIF):
            return "manager", "non"
        if effectif == "1":
            return "independant", "oui"
        return "dirigeant", "non"
    if not t and _match(h, DIRIGEANT) and not _match(h, DIRIGEANT_NEGATIF):
        return ("independant", "oui") if (effectif == "1" or _match(h, FONCTIONNEL)) else ("dirigeant", "non")
    if _match(t or h, MARKETING):
        return "marketing", "non"
    if _match(t or h, SALES):
        return "sales", "non"
    if _match(t or h, EXECUTANT) and not _match(t or h, DIRECTION):
        return "executant", "non"
    if _match(t or h, DIRECTION):
        return "direction", "non"
    if _match(combine, MANAGER):
        return "manager", "non"
    if _match(combine, FONCTIONNEL):
        return "independant", "oui"
    return "executant", "non"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="entree", required=True)
    ap.add_argument("--out", help="defaut : <entree>_pre.csv a cote du fichier d'entree")
    a = ap.parse_args()

    lignes = lire_csv(a.entree)
    compte: dict = {}
    for l in lignes:
        eff = effectif_num(l.get("effectif") or l.get("effectif_tranche") or "")
        l["effectif_num"] = eff
        l["taille_tranche"] = tranche(eff)
        cat, indep = categorie(l.get("titre", ""), l.get("headline", ""), eff)
        l["categorie_titre"] = cat
        l["independant"] = indep
        if not (l.get("seniorite") or "").strip():
            l["seniorite"] = seniorite_depuis_titre(l.get("titre") or l.get("headline") or "")
        if cat == "stagiaire":
            l["seniorite"] = "junior"
        email = (l.get("email") or "").strip().lower()
        if email and "@" in email:
            d = domaine(email)
            l["domaine_generique"] = "oui" if d in DOMAINES_GENERIQUES else "non"
            if not (l.get("domaine") or "").strip() and d not in DOMAINES_GENERIQUES:
                l["domaine"] = d
        elif l.get("domaine"):
            l["domaine_generique"] = "non"
        l["cle"] = norm_linkedin_url(l.get("linkedin_url")) or email or f"{norm_texte(l.get('entreprise'))}|{norm_texte(l.get('nom'))}"
        compte[cat] = compte.get(cat, 0) + 1
    sortie = Path(a.out) if a.out else Path(a.entree).with_name(Path(a.entree).stem + "_pre.csv")
    ecrire_csv(lignes, sortie)
    afficher(f"{len(lignes)} lignes pre-qualifiees -> {sortie}")
    for cat, n in sorted(compte.items(), key=lambda x: -x[1]):
        afficher(f"  {cat:12s} {n}")


if __name__ == "__main__":
    main()
