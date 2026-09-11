#!/usr/bin/env bash
# Superfounder OS : ajouter les modules à un workspace Claude Code EXISTANT.
#
# Si vous partez de zéro, vous n'avez pas besoin de ce script : clonez le dépôt,
# ouvrez-le dans Claude Code, dites "Installe mon second cerveau". Le dépôt EST le workspace.
#
#   ./install.sh --into ~/MonWorkspace          copie les skills et les modules dans un workspace existant
#   ./install.sh --into ~/MonWorkspace --dry-run  montre ce qui serait copié, sans rien écrire
#
# Ce que le script ne touche JAMAIS dans la cible : CLAUDE.md, ABOUT.ME/, Contexte/, et tout
# fichier qui existe déjà (contexte.md, strategie-contenu.md, .env, _journal.md...).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET=""; DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --into) TARGET="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "Option inconnue : $1"; exit 1 ;;
  esac
done
if [[ -z "$TARGET" ]]; then echo "Usage : ./install.sh --into <workspace> [--dry-run]"; exit 1; fi
mkdir -p "$TARGET"; TARGET="$(cd "$TARGET" && pwd)"

copy_new() { # copie src vers dst seulement si dst n'existe pas
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then echo "  = $dst (existe, conservé)"; return; fi
  echo "  + $dst"
  [[ $DRY -eq 1 ]] || { mkdir -p "$(dirname "$dst")"; cp -R "$src" "$dst"; }
}
sync_skills() { # remplace les skills (ce sont des procédures versionnées, pas des données)
  local src="$1" dst="$2"
  for skill in "$src"/*/; do
    local name; name="$(basename "$skill")"
    echo "  ~ $dst/$name"
    [[ $DRY -eq 1 ]] || { rm -rf "${dst:?}/$name"; mkdir -p "$dst"; cp -R "$skill" "$dst/$name"; }
  done
}

echo "Cible : $TARGET"
echo; echo "Skills transverses (racine) :"
sync_skills "$HERE/.claude/skills" "$TARGET/.claude/skills"

echo; echo "Module Prospection :"
copy_new "$HERE/Projects/Prospection/CLAUDE.md"    "$TARGET/Projects/Prospection/CLAUDE.md"
copy_new "$HERE/Projects/Prospection/GUIDE.md"     "$TARGET/Projects/Prospection/GUIDE.md"
copy_new "$HERE/Projects/Prospection/contexte.md"  "$TARGET/Projects/Prospection/contexte.md"
copy_new "$HERE/Projects/Prospection/.env.example" "$TARGET/Projects/Prospection/.env.example"
copy_new "$HERE/Projects/Prospection/.gitignore"   "$TARGET/Projects/Prospection/.gitignore"
for d in input output ressources; do [[ $DRY -eq 1 ]] || mkdir -p "$TARGET/Projects/Prospection/$d"; done
sync_skills "$HERE/Projects/Prospection/.claude/skills" "$TARGET/Projects/Prospection/.claude/skills"

echo; echo "Module Contenu :"
copy_new "$HERE/Projects/Contenu/CLAUDE.md" "$TARGET/Projects/Contenu/CLAUDE.md"
for f in strategie-contenu.md posts-de-reference.md swipe-file.md; do
  copy_new "$HERE/Projects/Contenu/ressources/$f" "$TARGET/Projects/Contenu/ressources/$f"
done
for d in input output; do [[ $DRY -eq 1 ]] || mkdir -p "$TARGET/Projects/Contenu/$d"; done
sync_skills "$HERE/Projects/Contenu/.claude/skills" "$TARGET/Projects/Contenu/.claude/skills"

echo; echo "Squelette (si absent) :"
copy_new "$HERE/Inbox/CLAUDE.md" "$TARGET/Inbox/CLAUDE.md"
copy_new "$HERE/Intelligence/CLAUDE.md" "$TARGET/Intelligence/CLAUDE.md"
copy_new "$HERE/Intelligence/INDEX.md" "$TARGET/Intelligence/INDEX.md"
copy_new "$HERE/Intelligence/LOG.md" "$TARGET/Intelligence/LOG.md"
copy_new "$HERE/ressources-templates/daily-note.md" "$TARGET/ressources-templates/daily-note.md"
copy_new "$HERE/docs" "$TARGET/docs"

echo
if [[ $DRY -eq 1 ]]; then echo "Dry-run : rien n'a été écrit."; else
echo "Terminé. Si votre workspace n'a pas encore d'ABOUT.ME/ ni de Contexte/, copiez-les depuis ce dépôt"
echo "et lancez \"Installe mon second cerveau\". Sinon, ouvrez Projects/Prospection/ ou Projects/Contenu/"
echo "et dites \"Installe ma prospection\" / \"Installe mon contenu\"."; fi
