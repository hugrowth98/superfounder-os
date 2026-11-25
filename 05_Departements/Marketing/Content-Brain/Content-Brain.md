---
type: departement
status: active
maj: AAAA-MM-JJ
---

# Content Brain

## Mission

Tout ce qui sert à produire votre contenu, au même endroit : la stratégie et ses piliers, la veille, la base de connaissances tirée de vos posts, de vos calls et de votre vécu, les idées, et le calendrier éditorial avec les chiffres de chaque post.

Ne va pas ici : votre offre, vos clients et votre voix (`02_Contexte/`, la stratégie y renvoie), les transcripts (`07_Meeting/`), les propositions ([[Vente]]), les visuels et infographies (`05_Departements/Marketing/LinkedIn/`).

## Cadre

La structure, les formats de fiche et les règles sont dans `10_Skills/_commun/content-brain.md`. Tous les skills de contenu le lisent avant d'écrire.

Trois skills font vivre ce dossier : `installer-contenu` ("Installe mon contenu", puis "Nourris mon brain" à chaque nouvelle source), `strategie-contenu` ("Challenge ma stratégie", à revoir chaque trimestre) et `clean-content` (le passage du lundi). Le master `linkedin` lit la base avant d'écrire un post et range ses brouillons dans le calendrier.

Les pages de piliers (dossier `01_Strategie/Piliers/`) et la section "Où on en est" ci-dessous sont reconstruites par `python3 10_Skills/clean-content/scripts/reconstruire.py`. On ne les édite pas à la main : on change le `pilier` ou les `sujets` d'une fiche.

Les calls et les dossiers clients sont fermés au contenu par défaut. Un client s'ouvre par le champ `contenu:` de sa note (`non`, `anonyme`, `nomme`).

- `01_Strategie/` : la stratégie, les posts de référence, le dossier `Piliers/` (une page par pilier, avec les fiches de chaque sujet)
- `02_Veille/` : sources suivies, comptes suivis, signaux de marché, inspirations
- `03_Base-de-connaissances/` : Enseignements, Methodes, Preuves, Histoires, Sources
- `04_Idees/` : une fiche par idée de post
- `05_Calendrier-editorial/` : Brouillons, Publies, Recycles, et `Calendrier.md`

## Où on en est

<!-- carte:debut -->
- [ ] Lancer "Installe mon contenu"
<!-- carte:fin -->

## Key Notes

- [[Strategie-contenu]]
- [[Posts-de-reference]]
- [[Calendrier]]
- [[Marketing]]
