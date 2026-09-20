---
name: sketchnote-tableau-blanc
description: >
  Le sketchnote sur tableau blanc : une photographie réaliste d'un tableau blanc (ou d'une
  grande feuille) écrit au marqueur, avec des doodles simples, quelques couleurs de feutre et
  des mots surlignés, comme un "graphic recording" d'atelier. Écrit la direction artistique et
  le prompt d'un brief produit par `brief-visuel`, puis lance l'image. Se déclenche sur :
  "sketchnote", "tableau blanc", "whiteboard", "au marqueur", "comme en atelier", "graphic
  recording", "dessine-moi". Ne pas utiliser pour un rendu aux couleurs de la charte (voir
  `infographie-editoriale`) ni pour une page de carnet en noir et blanc (voir `carnet-manuscrit`).
---

Le tableau blanc photographié raconte une session de travail : quelqu'un a expliqué quelque chose, en direct, au marqueur. Il tolère quelques couleurs (celles des feutres, pas celles de la charte), des doodles qui aident à comprendre, des mots surlignés qu'un lecteur pressé capte en deux secondes, et de l'espace : un tableau surchargé ne se lit pas en photo.

## Ressources

- `{SKILL_BASE}/ressources/lecture-charte.md` : ce qu'on garde de la charte (ton, interdits, logo dessiné).
- `{SKILL_BASE}/ressources/bibliotheque-structures.md` : structures 1, 2, 5, 6, 10, 12, 15.
- `{SKILL_BASE}/ressources/prompt-generation.md` : moteurs et checklist.

## Méthode

1. **Partir du brief** (blocs 1 à 6), avec 3 à 7 blocs au plus : un tableau se lit comme une mini-leçon, de haut en bas.
2. **Choisir un doodle par bloc**, spécifique et dessinable en quelques traits de marqueur, qui aide à comprendre (une balance pour un arbitrage, un entonnoir pour un tri, une horloge pour un délai). Aucun décor.
3. **Choisir 3 à 6 mots ou expressions à surligner** : ceux qu'un lecteur qui scrolle doit capter en deux secondes.
4. **Poser la hiérarchie** : le titre en haut (environ 10 pour cent), le contenu au centre (80 pour cent), le footer en bas (10 pour cent) ; la direction de lecture (haut vers bas, gauche vers droite, ou grille) ; les flèches entre blocs.
5. **Poser la palette des feutres**, fixe : noir pour le texte, les contours et les encadrés ; bleu pour les titres de blocs et la numérotation ; rouge pour les alertes et ce qu'il faut éviter ; vert pour les résultats et les validations ; surligneur fluo (jaune, vert ou orange) pour les mots-clés. Ce sont des couleurs de marqueur, pas la charte.
6. **Écrire le bloc 7** : format 4:5 ; support photographié (tableau blanc, ou grande feuille de bloc-notes) avec grain et éclairage naturel, pas un fichier plat ; tracés de marqueurs de tableau ; imperfections (lignes légèrement tremblantes, opacité d'encre variable) ; zéro police numérique ; mise en page aérée ; détails réalistes facultatifs (marqueurs posés sur le rebord, effaceur, traces d'un texte effacé).
7. **Écrire le bloc 8** avec le prompt ci-dessous.
8. **Générer** (outil natif, ou `generer_image.py --brief <brief.md>` ; `fal-ai/nano-banana-pro` rend bien ce style), montrer, corriger un point, relancer une variante.

## Le prompt de base (en anglais, à compléter)

```
A realistic photograph of a large whiteboard in a bright meeting room, shot straight on, portrait 4:5, natural light, slight grain. On the whiteboard, a hand-drawn sketchnote written with whiteboard markers by a founder explaining "<titre exact>" during a workshop.

STYLE:
- Everything handwritten with markers, no digital fonts at all; clean, legible block handwriting with natural imperfections (slightly shaky lines, uneven ink opacity)
- Marker colors only: black for text, outlines and boxes; blue for block titles and numbers; red for warnings and things to avoid; green for results and checks; a fluorescent highlighter (yellow) behind the key words listed below
- Simple doodles drawn in a few strokes next to each block, no decorative illustration
- Airy layout: title on top (about 10 percent of the height), content in the middle, a small footer at the bottom
- Optional realistic details: markers resting on the tray, an eraser, faint traces of erased text

CONTENT TO WRITE, EXACTLY AND NOTHING ELSE (French accents rendered correctly):
Title: "<titre exact>"
<blocs numérotés, titre, 1 à 2 phrases, le doodle décrit entre crochets>
Highlighted words: <liste>
Footer: "<footer exact>"

DO NOT: add words that are not listed, use printed fonts, add logos or icons other than described, add emojis, flatten the image into a digital design.
```

## Règles

- 3 à 7 blocs, jamais plus : l'espace blanc fait la lisibilité d'une photo.
- Les couleurs sont celles des feutres, fixes ; la charte ne s'applique pas ici.
- Chaque doodle sert la compréhension, sinon il saute.
- Le footer est court et constant (une signature, un appel au partage), vouvoyé.
- Le prompt part avec "exactly and nothing else".

## Exemples

- "Les 3 canaux qui marchent ensemble" : structure 5 ou 6, trois cercles reliés au marqueur, un doodle par canal (téléphone, enveloppe, logo dessiné), deux mots surlignés ; réponse attendue : le prompt et la photo.
- "Avant, pendant, après un rendez-vous" : structure 4, trois colonnes séparées par des traits, 2 points chacune, une flèche de gauche à droite ; réponse attendue : un tableau lisible, aéré.
- "Pourquoi le téléphone bat l'email en B2B" : structure 15 ou 9, deux colonnes, rouge pour l'email, vert pour l'appel, une conclusion encadrée ; réponse attendue : un contraste visible en deux secondes.
