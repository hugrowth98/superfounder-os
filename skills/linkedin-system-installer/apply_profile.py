#!/usr/bin/env python3
"""
apply_profile.py - Personnalise le LinkedIn Content System.

Lit un profil (linkedin-profile.json) contenant les valeurs des placeholders,
puis remplace tous les {{TOKEN}} dans les 8 skills frères.

Idempotent et re-runnable : pour chaque fichier .md, une copie pristine
"<fichier>.template" est créée au premier passage. Les remplacements partent
TOUJOURS du .template, ce qui permet de relancer l'installeur autant de fois
qu'on veut (re-personnalisation) sans accumuler les remplacements.

Usage :
    python3 apply_profile.py                # applique linkedin-profile.json
    python3 apply_profile.py --dry-run      # montre ce qui changerait, n'écrit rien
    python3 apply_profile.py --restore      # restaure les fichiers depuis les .template
    python3 apply_profile.py --profile /chemin/profil.json
"""
import argparse
import json
import os
import re
import sys

# Les 8 skills cibles (dossiers frères de l'installeur).
TARGET_SKILLS = [
    "linkedin-writing-core",
    "linkedin-ideation",
    "linkedin-educational",
    "linkedin-storytelling",
    "linkedin-hot-take",
    "linkedin-lead-magnet",
    "viral-hook-writer",
    "linkedin-post-optimizer",
]

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def skills_root():
    """Dossier parent de l'installeur = racine qui contient les 8 skills."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def iter_md_files(root):
    for skill in TARGET_SKILLS:
        skill_dir = os.path.join(root, skill)
        if not os.path.isdir(skill_dir):
            continue
        for dirpath, _dirs, files in os.walk(skill_dir):
            for f in files:
                if f.endswith(".md"):
                    yield os.path.join(dirpath, f)


def template_path(md_path):
    return md_path + ".template"


def read_pristine(md_path):
    """Renvoie le contenu pristine (depuis .template, créé si absent)."""
    tpl = template_path(md_path)
    if os.path.exists(tpl):
        with open(tpl, "r", encoding="utf-8") as fh:
            return fh.read()
    # Premier passage : le fichier live EST pristine -> on le sauvegarde.
    with open(md_path, "r", encoding="utf-8") as fh:
        content = fh.read()
    with open(tpl, "w", encoding="utf-8") as fh:
        fh.write(content)
    return content


def apply_profile(profile, dry_run=False):
    root = skills_root()
    changed, leftover = [], {}
    for md_path in iter_md_files(root):
        pristine = read_pristine(md_path)

        def repl(m):
            key = m.group(1)
            return str(profile.get(key, m.group(0)))

        new_content = TOKEN_RE.sub(repl, pristine)

        # Tokens restants non couverts par le profil
        for tok in TOKEN_RE.findall(new_content):
            leftover.setdefault(tok, []).append(os.path.relpath(md_path, root))

        if new_content != pristine:
            changed.append(os.path.relpath(md_path, root))
            if not dry_run:
                with open(md_path, "w", encoding="utf-8") as fh:
                    fh.write(new_content)
    return changed, leftover


def restore():
    root = skills_root()
    restored = 0
    for md_path in iter_md_files(root):
        tpl = template_path(md_path)
        if os.path.exists(tpl):
            with open(tpl, "r", encoding="utf-8") as fh:
                content = fh.read()
            with open(md_path, "w", encoding="utf-8") as fh:
                fh.write(content)
            restored += 1
    print(f"Restaure {restored} fichiers depuis les .template")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", action="store_true")
    args = ap.parse_args()

    if args.restore:
        restore()
        return

    here = os.path.dirname(os.path.abspath(__file__))
    profile_path = args.profile or os.path.join(here, "linkedin-profile.json")
    if not os.path.exists(profile_path):
        print(f"ERREUR : profil introuvable -> {profile_path}", file=sys.stderr)
        sys.exit(1)

    with open(profile_path, "r", encoding="utf-8") as fh:
        profile = json.load(fh)

    changed, leftover = apply_profile(profile, dry_run=args.dry_run)

    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"{mode}{len(changed)} fichiers personnalises :")
    for c in changed:
        print(f"  - {c}")

    if leftover:
        print("\nATTENTION : tokens encore presents (non fournis dans le profil) :")
        for tok, files in sorted(leftover.items()):
            print(f"  {{{{{tok}}}}} -> {len(files)} fichier(s) : {files[0]} ...")
    else:
        print("\nOK : aucun placeholder restant. Systeme entierement personnalise.")


if __name__ == "__main__":
    main()
