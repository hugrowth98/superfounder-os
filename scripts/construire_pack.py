#!/usr/bin/env python3
"""construire_pack : fabrique le dossier de mise a jour du contenu a partir de ce depot.

Le pack sert aux utilisateurs qui ont deja un Superfounder OS et veulent y ajouter le Content Brain.
Il est tire de l'arbre de travail : on modifie un skill ici, on relance ce script, le pack suit.

  nouveau/          les fichiers geres, copies depuis l'arbre de travail
  base/             les memes fichiers a la version de reference (--base, defaut v6.4.0)
  empreintes.json   l'empreinte git de chaque version publiee des fichiers geres (tout l'historique)
  VERSION           la version lue dans CHANGELOG.md
  + le contenu de scripts/pack-contenu/ (README.md, MISE-A-JOUR.md, migrer.py)

Usage :
  python3 scripts/construire_pack.py --sortie ../superfounder-os-mise-a-jour-contenu
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "scripts" / "pack-contenu"
# ce que le pack installe ou met a jour
GERES = ["10_Skills/_commun/content-brain.md", "10_Skills/installer-contenu/", "10_Skills/strategie-contenu/", "10_Skills/clean-content/",
         "10_Skills/linkedin/", "10_Skills/planifier-post/", "10_Skills/lint/", "05_Departements/Marketing/Content-Brain/",
         "05_Departements/Marketing/Marketing.md", "05_Departements/Marketing/LinkedIn/LinkedIn.md", "docs/contenu.md",
         "08_Ressources/templates/client.md", "CLAUDE.md", "AGENTS.md", "install.sh", "scripts/valider_gtm.py"]
# ce dont on garde les empreintes : les chemins geres et leurs anciens emplacements
HISTORIQUE = GERES + ["05_Departements/Marketing/", "05_Departements/Contenu/", "Departements/Contenu/", "Skills/linkedin", "Skills/installer-contenu",
                      "Skills/planifier-post", "Skills/lint"]
IGNORES = {".DS_Store", "compteur.json", "compteurs.json", "baseline.json"}


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(RACINE), *args], check=True, capture_output=True, text=True).stdout


def gere(chemin: str, liste: list[str]) -> bool:
    return any(chemin == g or (g.endswith("/") and chemin.startswith(g)) or (not g.endswith("/") and not g.endswith(".md") and chemin.startswith(g)) for g in liste)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sortie", required=True, help="dossier du pack (son contenu gere est remplace, son .git est conserve)")
    ap.add_argument("--base", default="v6.4.0", help="version de reference pour base/ (defaut v6.4.0)")
    a = ap.parse_args()
    sortie = Path(a.sortie).resolve()
    if RACINE in sortie.parents or sortie == RACINE:
        sys.exit("Le pack doit etre construit hors du depot.")
    sortie.mkdir(parents=True, exist_ok=True)
    for nom in ("nouveau", "base"):
        if (sortie / nom).exists():
            shutil.rmtree(sortie / nom)

    # nouveau/ : l'arbre de travail
    suivis = [l for l in git("ls-files", "--cached", "--others", "--exclude-standard").splitlines() if l]
    n = 0
    for rel in suivis:
        src = RACINE / rel
        if not gere(rel, GERES) or not src.is_file() or src.name in IGNORES or "__pycache__" in src.parts:
            continue
        dst = sortie / "nouveau" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        n += 1

    # base/ : la version de reference
    b = 0
    for ligne in git("ls-tree", "-r", "--name-only", a.base).splitlines():
        if not gere(ligne, GERES):
            continue
        dst = sortie / "base" / ligne
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(subprocess.run(["git", "-C", str(RACINE), "show", f"{a.base}:{ligne}"], check=True, capture_output=True).stdout)
        b += 1

    # empreintes : tout l'historique des fichiers geres
    empreintes = set()
    for rev in git("rev-list", "--all").split():
        for ligne in git("ls-tree", "-r", rev).splitlines():
            meta, _, chemin = ligne.partition("\t")
            if gere(chemin, HISTORIQUE):
                empreintes.add(meta.split()[2])

    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (RACINE / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    version = m.group(1) if m else "?"
    (sortie / "VERSION").write_text(version + "\n", encoding="utf-8")
    (sortie / "empreintes.json").write_text(json.dumps({"version": version, "base": a.base, "empreintes": sorted(empreintes)}, indent=0) + "\n", encoding="utf-8")
    for p in SOURCE.iterdir():
        if p.is_file():
            shutil.copy2(p, sortie / p.name)
    print(f"Pack {version} dans {sortie} : {n} fichiers dans nouveau/, {b} dans base/ ({a.base}), {len(empreintes)} empreintes.")


if __name__ == "__main__":
    main()
