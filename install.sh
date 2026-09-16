#!/usr/bin/env bash
# Superfounder OS : ajouter les modules à un workspace Claude Code EXISTANT.
#
# Si vous partez de zéro, vous n'avez pas besoin de ce script : clonez le dépôt,
# ouvrez-le dans Claude Code, dites "Installe mon second cerveau". Le dépôt EST le workspace.
#
#   ./install.sh --into ~/MonWorkspace            copie les skills et les modules dans un workspace existant
#   ./install.sh --into ~/MonWorkspace --dry-run  montre ce qui serait copié, sans rien écrire
#
# Ce que le script ne touche JAMAIS dans la cible : CLAUDE.md, About-Me/, Contexte/, Branding/, et tout
# fichier qui existe déjà (une note de dossier, contexte.md, strategie-contenu.md, .env, _log.md...).
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
keep() { [[ $DRY -eq 1 ]] || mkdir -p "$TARGET/$1"; }

echo "Cible : $TARGET"
echo; echo "Skills transverses (racine) :"
sync_skills "$HERE/.claude/skills" "$TARGET/.claude/skills"

echo; echo "Module Vente (prospection) :"
for f in Vente.md _log.md GUIDE.md contexte.md .env.example .gitignore; do
  copy_new "$HERE/Vente/$f" "$TARGET/Vente/$f"
done
for d in Listes-prospection Messages Propositions Pipeline; do
  copy_new "$HERE/Vente/$d/$d.md" "$TARGET/Vente/$d/$d.md"
  copy_new "$HERE/Vente/$d/_log.md" "$TARGET/Vente/$d/_log.md"
done
keep Vente/sources; keep Vente/ressources
sync_skills "$HERE/Vente/.claude/skills" "$TARGET/Vente/.claude/skills"

echo; echo "Module Marketing (contenu) :"
copy_new "$HERE/Marketing/Marketing.md" "$TARGET/Marketing/Marketing.md"
copy_new "$HERE/Marketing/_log.md"      "$TARGET/Marketing/_log.md"
for d in LinkedIn Newsletter Mailing Event Video Slides; do
  copy_new "$HERE/Marketing/$d/$d.md"  "$TARGET/Marketing/$d/$d.md"
  copy_new "$HERE/Marketing/$d/_log.md" "$TARGET/Marketing/$d/_log.md"
done
for f in strategie-contenu.md posts-de-reference.md swipe-file.md; do
  copy_new "$HERE/Marketing/LinkedIn/ressources/$f" "$TARGET/Marketing/LinkedIn/ressources/$f"
done
keep Marketing/LinkedIn/sources; keep Marketing/LinkedIn/livrables
sync_skills "$HERE/Marketing/.claude/skills" "$TARGET/Marketing/.claude/skills"

echo; echo "Squelette (si absent) :"
for d in Produit-Client Strategie Veille Meeting Journal Inbox Branding; do
  copy_new "$HERE/$d/$d.md" "$TARGET/$d/$d.md"
  [[ -f "$HERE/$d/_log.md" ]] && copy_new "$HERE/$d/_log.md" "$TARGET/$d/_log.md"
done
copy_new "$HERE/Veille/INDEX.md" "$TARGET/Veille/INDEX.md"
copy_new "$HERE/Veille/LOG.md"   "$TARGET/Veille/LOG.md"
keep Veille/sources; keep Veille/wiki/concepts; keep Veille/wiki/patterns; keep Veille/wiki/people; keep Veille/wiki/companies
keep Ressources; keep Archives
for f in note-de-dossier.md note-de-dossier-client.md journal-jour.md; do
  copy_new "$HERE/Ressources/templates/$f" "$TARGET/Ressources/templates/$f"
done
copy_new "$HERE/docs" "$TARGET/docs"

echo
if [[ $DRY -eq 1 ]]; then echo "Dry-run : rien n'a été écrit."; else
echo "Terminé. Si votre workspace n'a pas encore d'About-Me/ ni de Contexte/, copiez-les depuis ce dépôt"
echo "et lancez \"Installe mon second cerveau\". Sinon, ouvrez Vente/ ou Marketing/"
echo "et dites \"Installe ma prospection\" / \"Installe mon contenu\"."; fi
