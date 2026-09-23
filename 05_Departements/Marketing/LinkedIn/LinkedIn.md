---
type: departement
status: active
maj: AAAA-MM-JJ
---

# LinkedIn

## Mission

Tout post LinkedIn, même lié à un client, plus les drafts, les briefs visuels, les carrousels, les infographies et le calendrier éditorial. Un fichier par post, à plat dans ce dossier.

Quatre fichiers que le master `linkedin` lit vivent ici aussi : `strategie-contenu.md` (piliers, convictions, cadence, formats), `posts-de-reference.md` (vos posts, pour caler la voix), `swipe-file.md` (les posts des autres, pour les structures), `sources-veille.json` (les newsletters et les chaînes que la veille lit chaque semaine).

Ne va pas ici : les messages de prospection envoyés en DM (`05_Departements/Go-to-Market/Messages/`), la source qui a inspiré le post (`08_Ressources/Veille/sources/`).

## Cadre

Un post par fichier : `Post-Sujet_YYYY-MM-DD.md`. Le brief de veille hebdo : `Brief-veille_YYYY-MM-DD.md` (sous-skill `veille`, dump brut dans `sources/`). Le calendrier des posts programmés : `Calendrier-publication.md` (skill `planifier-post`). Une infographie : `Infographie-Sujet_YYYY-MM-DD.md` (le brief) et `.png` (l'image), produits par le master `infographie` à partir de `03_Branding/charte-visuelle.md`. Les sources (transcripts, articles, idées brutes) dans `sources/`.

Les posts qui ont bien marché remontent dans `posts-de-reference.md`. Les posts des autres qui arrêtent le scroll vont dans `swipe-file.md`. Plus l'échantillon est riche, plus la voix est juste.

- à plat : les posts, les briefs, les infographies, le calendrier, plus `strategie-contenu.md`, `posts-de-reference.md`, `swipe-file.md`, `sources-veille.json`
- `sources/` transcripts, articles, idées brutes à repurposer, les dumps et caches de la veille (`veille_*.json`) et les runs de la veille créateurs (`veille-createurs_<debut>_<fin>/` avec `rapport.html` et les visuels), tous ignorés par git
- `comptes-veille.json` : les comptes LinkedIn à surveiller, si vous avez choisi de les mémoriser (sous-skill `veille-createurs`) ; une infographie reprise d'un visuel existant vit dans son dossier `Infographie-Sujet_YYYY-MM-DD/` (`data.json` et trois PNG, sous-skill `reprise`)

## Où on en est

- [ ] Premier post

## Key Notes

- [[Note liée]]
