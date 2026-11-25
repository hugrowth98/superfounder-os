#!/usr/bin/env python3
"""migrer : installe le Content Brain dans un workspace Superfounder OS existant.

Le script compare le workspace au Superfounder OS standard et traite chaque fichier selon ce qu'il trouve :
  - absent                        il est ajoute
  - standard, jamais modifie      il est remplace (l'ancien part dans 11_Archives/)
  - standard, modifie par vous    il n'est PAS touche : il est liste, pour une fusion a la main
  - vos donnees de contenu        elles sont deplacees au nouvel endroit, sans changer leur contenu

Usage, depuis n'importe ou :
  python3 migrer.py                       le rapport, rien n'est ecrit
  python3 migrer.py --appliquer           applique ce que le rapport annonce
  python3 migrer.py --workspace <dossier> si le pack n'est pas dans le workspace
  python3 migrer.py --marketing <Nom>     si votre departement Marketing porte un autre nom

Rien n'est supprime. Chaque fichier remplace est copie dans 11_Archives/mise-a-jour-contenu_<date>/.
Stdlib uniquement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

PACK = Path(__file__).resolve().parent
NOUVEAU = PACK / "nouveau"
MKT_STD = "05_Departements/Marketing"
CB_REL = "Content-Brain"
SKILLS_GERES = ["10_Skills/linkedin", "10_Skills/installer-contenu", "10_Skills/planifier-post", "10_Skills/lint",
                "10_Skills/strategie-contenu", "10_Skills/clean-content"]
ANCIENNES_REFERENCES = ["LinkedIn/strategie-contenu.md", "LinkedIn/posts-de-reference.md", "LinkedIn/sources-veille.json",
                        "swipe-file.md", "comptes-veille.json", "banque-vecu.md", "Calendrier-publication.md",
                        "sous-skills/opinion", "exemples-opinion.md"]


def empreinte(octets: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(octets) + octets).hexdigest()


def est_standard(chemin: Path, connues: set[str]) -> bool:
    octets = chemin.read_bytes()
    return empreinte(octets) in connues or empreinte(octets.replace(b"\r\n", b"\n")) in connues


def trouver_workspace(depart: Path) -> Path | None:
    for d in [depart] + list(depart.parents):
        if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir() and (d / "05_Departements").is_dir() and d != PACK:
            return d
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", help="racine du workspace (defaut : le premier dossier parent qui contient CLAUDE.md et 10_Skills/)")
    ap.add_argument("--marketing", help="nom du dossier du departement Marketing s'il a ete renomme")
    ap.add_argument("--appliquer", action="store_true", help="ecrire (sans cette option : rapport seul)")
    a = ap.parse_args()

    ws = Path(a.workspace).resolve() if a.workspace else trouver_workspace(PACK.parent)
    if ws is None or not (ws / "10_Skills").is_dir():
        sys.exit("Workspace introuvable. Deposez le pack dans le workspace (par exemple dans 00_Inbox/) ou passez --workspace <dossier>.")
    if not NOUVEAU.is_dir():
        sys.exit(f"Pack incomplet : {NOUVEAU} manque.")
    connues = set(json.loads((PACK / "empreintes.json").read_text(encoding="utf-8"))["empreintes"])
    version = (PACK / "VERSION").read_text(encoding="utf-8").strip() if (PACK / "VERSION").exists() else "?"

    # ---------------------------------------------------------------- le departement Marketing
    if a.marketing:
        mkt = ws / "05_Departements" / a.marketing
    elif (ws / MKT_STD).is_dir():
        mkt = ws / MKT_STD
    else:
        candidats = {p.parent.parent for p in (ws / "05_Departements").glob("*/*/strategie-contenu.md")} | \
                    {p.parent for p in (ws / "05_Departements").glob("*/LinkedIn")}
        if len(candidats) != 1:
            sys.exit("Departement Marketing introuvable ou ambigu dans 05_Departements/. Relancez avec --marketing <Nom du dossier>.")
        mkt = candidats.pop()
    if not mkt.is_dir():
        sys.exit(f"Dossier introuvable : {mkt}")
    mkt_rel = mkt.relative_to(ws).as_posix()
    renomme = mkt_rel != MKT_STD
    cb = mkt / CB_REL
    anciens = [p.parent for p in mkt.rglob("strategie-contenu.md") if CB_REL not in p.parts]
    ancien = anciens[0] if anciens else mkt / "LinkedIn"

    def cible(rel: str) -> Path:
        return ws / (mkt_rel + rel[len(MKT_STD):] if rel.startswith(MKT_STD) else rel)

    def contenu_nouveau(src: Path) -> bytes:
        octets = src.read_bytes()
        if renomme and src.suffix in {".md", ".py", ".json", ".sh"}:
            nom = mkt.name
            octets = octets.replace(MKT_STD.encode(), mkt_rel.encode()).replace(b'"05_Departements" / "Marketing"', f'"05_Departements" / "{nom}"'.encode())
        return octets

    archive = ws / "11_Archives" / f"mise-a-jour-contenu_{date.today().isoformat()}"
    prevus = set()
    R = {k: [] for k in ("deplace", "ajoute", "remplace", "a_jour", "modifie", "obsolete", "garde", "references", "notes")}

    def archiver(p: Path) -> None:
        dst = archive / p.relative_to(ws)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if p.is_dir():
            shutil.copytree(p, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(p, dst)

    def deplacer(src: Path, dst: Path, note: str = "") -> None:
        if not src.exists():
            return
        if dst.exists():
            R["notes"].append(f"déjà en place, non déplacé : {src.relative_to(ws)} (la cible {dst.relative_to(ws)} existe)")
            return
        R["deplace"].append(f"{src.relative_to(ws)}  ->  {dst.relative_to(ws)}{note}")
        prevus.add(dst)
        if a.appliquer:
            archiver(src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

    def retirer_gabarit(src: Path) -> bool:
        """Un fichier de reglage reste a l'etat de gabarit : on l'archive, le nouveau gabarit prendra sa place."""
        if src.exists() and src.is_file() and est_standard(src, connues):
            R["obsolete"].append(f"{src.relative_to(ws)} (gabarit jamais rempli, remplacé par le nouveau)")
            if a.appliquer:
                archiver(src)
                src.unlink()
            return True
        return False

    # ---------------------------------------------------------------- 1. vos donnees de contenu
    for nom, dst in [("strategie-contenu.md", "01_Strategie/Strategie-contenu.md"), ("posts-de-reference.md", "01_Strategie/Posts-de-reference.md"),
                     ("sources-veille.json", "02_Veille/Sources-veille.json"), ("comptes-veille.json", "02_Veille/Comptes-veille.json")]:
        if not retirer_gabarit(ancien / nom):
            deplacer(ancien / nom, cb / dst)
    if not retirer_gabarit(ancien / "swipe-file.md"):
        deplacer(ancien / "swipe-file.md", cb / "02_Veille/Inspirations/_swipe-file-a-convertir.md", "  (à convertir en une fiche par post)")
    deplacer(ancien / "banque-vecu.md", cb / "03_Base-de-connaissances/Sources/_banque-vecu-a-convertir.md", "  (à convertir en une fiche par histoire)")
    if ancien.is_dir():
        for p in sorted(ancien.glob("Post-*.md")):
            deplacer(p, cb / "05_Calendrier-editorial/Brouillons" / p.name, "  (à classer : brouillon ou publié)")
        for p in sorted(ancien.glob("Brief-veille_*.md")):
            deplacer(p, cb / "02_Veille" / p.name)
        if (ancien / "sources").is_dir():
            for p in sorted((ancien / "sources").iterdir()):
                if p.name.startswith("veille"):
                    deplacer(p, cb / "02_Veille/sources" / p.name)
    vieux_cal = ancien / "Calendrier-publication.md"
    lignes_cal = []
    if vieux_cal.exists():
        lignes_cal = [l for l in vieux_cal.read_text(encoding="utf-8").splitlines() if l.startswith("|")][2:]
        prevus.add(vieux_cal)
        R["deplace"].append(f"{vieux_cal.relative_to(ws)}  ->  {(cb / '05_Calendrier-editorial/Calendrier.md').relative_to(ws)}  ({len(lignes_cal)} ligne(s) de programmation reprises)")
        if a.appliquer:
            archiver(vieux_cal)
            vieux_cal.unlink()

    # ---------------------------------------------------------------- 2. les fichiers du pack
    installes = set()
    for src in sorted(p for p in NOUVEAU.rglob("*") if p.is_file()):
        rel = src.relative_to(NOUVEAU).as_posix()
        dst = cible(rel)
        installes.add(dst)
        nouveau = contenu_nouveau(src)
        squelette = rel.startswith(MKT_STD + "/" + CB_REL + "/")
        if dst in prevus:
            R["a_jour"].append(dst.relative_to(ws).as_posix())
        elif not dst.exists():
            R["ajoute"].append(dst.relative_to(ws).as_posix())
            if a.appliquer:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(nouveau)
                if src.suffix == ".py":
                    dst.chmod(0o755)
        elif squelette or dst.read_bytes() == nouveau:
            R["a_jour"].append(dst.relative_to(ws).as_posix())
        elif est_standard(dst, connues):
            R["remplace"].append(dst.relative_to(ws).as_posix())
            if a.appliquer:
                archiver(dst)
                dst.write_bytes(nouveau)
        else:
            R["modifie"].append(dst.relative_to(ws).as_posix())
    if lignes_cal and a.appliquer:
        cal = cb / "05_Calendrier-editorial/Calendrier.md"
        cal.write_text(cal.read_text(encoding="utf-8").rstrip("\n") + "\n" + "\n".join(lignes_cal) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- 3. ce qui n'existe plus dans le standard
    for d in SKILLS_GERES:
        dossier = ws / d
        if not dossier.is_dir():
            continue
        for p in sorted(x for x in dossier.rglob("*") if x.is_file()):
            if p in installes or "__pycache__" in p.parts or p.name in {".DS_Store", "compteur.json", "compteurs.json", "baseline.json"}:
                continue
            if est_standard(p, connues):
                R["obsolete"].append(p.relative_to(ws).as_posix())
                if a.appliquer:
                    archiver(p)
                    p.unlink()
            else:
                R["garde"].append(p.relative_to(ws).as_posix())
    if a.appliquer:
        for d in SKILLS_GERES:
            for sous in sorted((ws / d).rglob("*"), reverse=True) if (ws / d).is_dir() else []:
                if sous.is_dir() and not any(sous.iterdir()):
                    sous.rmdir()

    # ---------------------------------------------------------------- 4. les references aux anciens chemins
    a_remplacer = {ws / x for x in R["remplace"]} | {ws / x.split(" (")[0] for x in R["obsolete"]}
    for p in sorted(ws.rglob("*")):
        if not p.is_file() or p.suffix not in {".md", ".py", ".json", ".sh"}:
            continue
        parts = p.relative_to(ws).parts
        if parts[0] in {".git", "11_Archives", ".claude", ".agents", "node_modules"} or PACK in p.parents or p.name == "CHANGELOG.md":
            continue
        if p in a_remplacer or (p in installes and p.relative_to(ws).as_posix() not in R["modifie"] and a.appliquer):
            continue
        try:
            texte = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        trouves = [r for r in ANCIENNES_REFERENCES if r in texte]
        if trouves:
            R["references"].append(f"{p.relative_to(ws).as_posix()} : {', '.join(trouves)}")

    # ---------------------------------------------------------------- le rapport
    titres = [("deplace", "VOS DONNÉES, DÉPLACÉES (contenu inchangé)"), ("ajoute", "AJOUTÉ"), ("remplace", "REMPLACÉ (standard, jamais modifié chez vous)"),
              ("modifie", "MODIFIÉ PAR VOUS : non touché, à fusionner à la main avec le dossier nouveau/ du pack"),
              ("obsolete", "RETIRÉ DU STANDARD (archivé)"), ("garde", "AJOUTÉ PAR VOUS dans un skill géré : conservé tel quel"),
              ("references", "ANCIENS CHEMINS ENCORE CITÉS : à corriger"), ("notes", "NOTES")]
    sortie = [f"Mise à jour contenu, version {version}, sur {ws}", f"Département Marketing : {mkt_rel}" + ("  (renommé : les chemins des skills installés sont adaptés)" if renomme else ""),
              "MODE : " + ("APPLIQUÉ" if a.appliquer else "RAPPORT SEUL, rien n'est écrit. Relancez avec --appliquer."), ""]
    for cle, titre in titres:
        if not R[cle]:
            continue
        sortie.append(f"{titre} : {len(R[cle])}")
        montre = R[cle] if cle in {"deplace", "modifie", "garde", "references", "notes"} else R[cle][:12]
        sortie += [f"  {x}" for x in montre]
        if len(montre) < len(R[cle]):
            sortie.append(f"  ... et {len(R[cle]) - len(montre)} autres")
        sortie.append("")
    sortie.append(f"Déjà à jour : {len(R['a_jour'])} fichier(s).")
    if a.appliquer:
        archive.mkdir(parents=True, exist_ok=True)
        (archive / "rapport.md").write_text("# Rapport de mise à jour du contenu\n\n```\n" + "\n".join(sortie) + "\n```\n", encoding="utf-8")
        sortie.append(f"Anciennes versions et rapport : {archive.relative_to(ws)}/")
    print("\n".join(sortie))


if __name__ == "__main__":
    main()
