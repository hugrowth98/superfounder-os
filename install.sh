#!/usr/bin/env bash
# Superfounder OS : ajouter la structure et les skills à un workspace Claude Code EXISTANT.
#
# Si vous partez de zéro, vous n'avez pas besoin de ce script : clonez le dépôt,
# ouvrez-le dans Claude Code, dites "Installe mon second cerveau". Le dépôt EST le workspace.
#
#   ./install.sh --into ~/MonWorkspace            copie les skills et la structure dans un workspace existant
#   ./install.sh --into ~/MonWorkspace --dry-run  montre ce qui serait copié, sans rien écrire
#
# Ce que le script ne touche JAMAIS dans la cible : CLAUDE.md, 01 About-Me/, 02 Contexte/, 03 Branding/,
# et tout fichier qui existe déjà (une fiche, contexte.md, strategie-contenu.md, .env, _log.md...).
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
  [[ -e "$src" ]] || return 0
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
echo; echo "Skills (bibliothèque unique 10 Skills/, liens pour Claude Code et Codex) :"
sync_skills "$HERE/10 Skills" "$TARGET/10 Skills"
for l in .claude/skills .agents/skills; do
  if [[ -e "$TARGET/$l" && ! -L "$TARGET/$l" ]]; then echo "  = $TARGET/$l (existe, conservé : faites-en un lien vers 10 Skills/ si vous voulez une seule bibliothèque)"
  else echo "  ~ $TARGET/$l -> ../10 Skills"; [[ $DRY -eq 1 ]] || { mkdir -p "$(dirname "$TARGET/$l")"; ln -sfn "../10 Skills" "$TARGET/$l"; }; fi
done

echo; echo "Structure (si absente) :"
for d in "00 Inbox" "04 Projets" "05 Departements" "06 Clients" "07 Meeting" "08 Ressources" "09 Journal" "11 Archives"; do
  for f in "$HERE/$d"/*.md; do [[ -f "$f" ]] && copy_new "$f" "$TARGET/$d/$(basename "$f")"; done
done
for dep in Strategie Contenu Go-to-Market Vente Produit Finance-Compta; do
  copy_new "$HERE/05 Departements/$dep/$dep.md" "$TARGET/05 Departements/$dep/$dep.md"
  copy_new "$HERE/05 Departements/$dep/_log.md" "$TARGET/05 Departements/$dep/_log.md"
  for sub in "$HERE/05 Departements/$dep"/*/; do
    [[ -d "$sub" ]] || continue; s="$(basename "$sub")"
    copy_new "$sub/$s.md" "$TARGET/05 Departements/$dep/$s/$s.md"
    copy_new "$sub/_log.md" "$TARGET/05 Departements/$dep/$s/_log.md"
  done
done
for f in GUIDE.md contexte.md; do copy_new "$HERE/05 Departements/Go-to-Market/$f" "$TARGET/05 Departements/Go-to-Market/$f"; done
for f in strategie-contenu.md posts-de-reference.md swipe-file.md; do copy_new "$HERE/05 Departements/Contenu/LinkedIn/$f" "$TARGET/05 Departements/Contenu/LinkedIn/$f"; done
for d in "00 Inbox/_import" "05 Departements/Go-to-Market/sources" "07 Meeting/Clients" "07 Meeting/Prospects" "07 Meeting/Interne" "07 Meeting/Autres" "08 Ressources/Veille/sources" "08 Ressources/Veille/wiki/concepts" "08 Ressources/Veille/wiki/patterns" "08 Ressources/Veille/wiki/people" "08 Ressources/Veille/wiki/companies"; do keep "$d"; done
for f in "$HERE/08 Ressources/templates"/*.md; do copy_new "$f" "$TARGET/08 Ressources/templates/$(basename "$f")"; done
for f in Veille.md INDEX.md LOG.md _log.md; do copy_new "$HERE/08 Ressources/Veille/$f" "$TARGET/08 Ressources/Veille/$f"; done
copy_new "$HERE/docs" "$TARGET/docs"
copy_new "$HERE/AGENTS.md" "$TARGET/AGENTS.md"
copy_new "$HERE/opencode.json" "$TARGET/opencode.json"
copy_new "$HERE/.env.example" "$TARGET/.env.example"

echo
if [[ $DRY -eq 1 ]]; then echo "Dry-run : rien n'a été écrit."; else
echo "Terminé. Si votre workspace n'a pas encore de 01 About-Me/ ni de 02 Contexte/, copiez-les depuis ce dépôt"
echo "et lancez \"Installe mon second cerveau\". Sinon, dites \"Installe ma prospection\" ou \"Installe mon contenu\"."; fi
