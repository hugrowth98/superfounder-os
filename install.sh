#!/usr/bin/env bash
# Superfounder OS : installation en une commande.
#
#   ./install.sh                  installe les skills autonomes dans ~/.claude/skills (global)
#   ./install.sh --local          installe les skills autonomes dans ./.claude/skills (projet courant)
#   ./install.sh --os-gtm DIR     copie l'OS-GTM dans DIR/OS-GTM (DIR = votre workspace Claude)
#
# Les options se combinent : ./install.sh --local --os-gtm ~/MonCerveauIA
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.claude/skills"
OSGTM_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --local) TARGET="$(pwd)/.claude/skills"; shift ;;
    --os-gtm)
      OSGTM_DIR="${2:-}"
      if [[ -z "$OSGTM_DIR" ]]; then echo "Usage : --os-gtm <dossier-workspace>"; exit 1; fi
      shift 2 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "Option inconnue : $1"; exit 1 ;;
  esac
done

echo "Skills autonomes -> $TARGET"
mkdir -p "$TARGET"
for skill in "$HERE"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "${TARGET:?}/$name"
  cp -R "$skill" "$TARGET/$name"
  echo "  + $name"
done

if [[ -n "$OSGTM_DIR" ]]; then
  mkdir -p "$OSGTM_DIR"
  DEST="$OSGTM_DIR/OS-GTM"
  if [[ -d "$DEST" ]]; then
    echo "OS-GTM existe déjà dans $DEST : mise à jour des skills uniquement (contexte.md et .env conservés)"
    rm -rf "${DEST:?}/.claude/skills"
    mkdir -p "$DEST/.claude"
    cp -R "$HERE/os-gtm/.claude/skills" "$DEST/.claude/skills"
    cp "$HERE/os-gtm/CLAUDE.md" "$HERE/os-gtm/GUIDE.md" "$DEST/"
  else
    cp -R "$HERE/os-gtm" "$DEST"
    cp "$DEST/.env.example" "$DEST/.env"
    echo "OS-GTM -> $DEST"
  fi
  echo
  echo "Étape suivante : ouvrez $DEST dans Claude Code et écrivez \"installe l'OS GTM\"."
fi

echo
echo "Terminé. Relancez Claude Code pour charger les nouveaux skills."
