---
name: carnet-manuscrit
description: >
  La page de carnet manuscrite en noir et blanc : une feuille arrachée d'un carnet à spirale,
  écrite au stylo noir par un dirigeant qui explique un framework, dense, imparfaite, lisible.
  Écrit la direction artistique et le prompt d'un brief produit par `brief-visuel`, puis lance
  l'image. Se déclenche sur : "version manuscrite", "style carnet", "notebook", "écrit à la
  main", "noir et blanc", "comme une page de cahier", "handwritten". Ne pas utiliser pour un
  rendu aux couleurs de la charte (voir `infographie-editoriale`) ni pour un tableau blanc
  photographié (voir `sketchnote-tableau-blanc`).
---

Ce style casse le motif du feed : au milieu des carrousels et des visuels de modèle, une page écrite à la main arrête le pouce. Il marche pour une méthode courte, une conviction, un framework en 6 à 10 points. Il ignore la palette de la charte par nature (encre noire, papier blanc cassé) et n'en garde que le ton, les interdits et, si on le veut, le logo dessiné au trait.

## Ressources

- `{SKILL_BASE}/ressources/lecture-charte.md` : ce qu'on garde de la charte quand il n'y a pas de couleur.
- `{SKILL_BASE}/ressources/bibliotheque-structures.md` : structures 1, 2, 5, 10, 12, 15 conviennent le mieux à ce rendu.
- `{SKILL_BASE}/ressources/prompt-generation.md` : moteurs et checklist.

## Méthode

1. **Partir du brief** (blocs 1 à 6). Le texte doit être plus court que pour l'éditorial : 6 à 10 sections, chacune avec un titre de 2 à 4 mots et 2 à 4 points de 3 à 7 mots. L'écriture manuscrite prend de la place.
2. **Choisir les éléments dessinés** : un par section au plus, dessinable en quelques traits (mini-schéma, pyramide, flèche, bloc de comparaison, encadré, symbole d'alerte, esquisse de framework). Pas d'illustration.
3. **Poser la composition** : grand titre manuscrit en haut, souligné ; sections numérotées ; séparateurs, encadrés, soulignements et flèches dessinés à la main ; composition symétrique, espacement intentionnel, dense mais équilibrée.
4. **Écrire le bloc 7** : papier blanc cassé légèrement texturé, spirale ou marge visible, encre noire uniquement, écriture propre mais imparfaite (espacement inégal, léger tremblement), hiérarchie forte malgré le fait main, aucune couleur, aucun rendu numérique poli.
5. **Écrire le bloc 8** avec le prompt ci-dessous, complété du texte exact et du logo si demandé.
6. **Générer** (outil natif, ou `generer_image.py --brief <brief.md>`), montrer, corriger un point, relancer une variante.

## Le prompt de base (en anglais, à compléter)

```
Create a highly detailed hand-drawn notebook infographic in a clean black-and-white "founder notebook" style. The infographic should feel like a page torn from a real spiral notebook, drawn with a black pen by an intelligent founder explaining a framework visually.

STYLE AND VISUAL DNA:
- Handwritten text only (clean but imperfect marker or pen handwriting)
- Pure black ink on slightly textured off-white notebook paper
- Slight natural imperfections, uneven spacing, subtle hand-drawn wobble
- Looks authentic, not polished or corporate
- Minimalist, highly readable, "save-worthy"
- Feels like a genius founder explaining something on paper
- No colors (black and white only)
- Strong visual hierarchy despite the handmade style

LAYOUT RULES:
- Large handwritten title at the top: "<titre exact>"
- Clear numbered sections (<N> steps)
- Each section includes a short bold handwritten heading and 2 to 4 concise bullet points
- Use hand-drawn separators, boxes, underlines and arrows
- Include simple visual elements: mini diagrams, pyramids, arrows, comparison blocks, callout sections, warning symbols, small framework sketches
- Dense but visually balanced; the entire page must feel information-rich but easy to scan
- Symmetrical composition with intentional spacing
- Portrait 4:5, readable on a phone

TEXT TO RENDER, EXACTLY AND NOTHING ELSE (French accents rendered correctly):
<le bloc 6 du brief, section par section, entre guillemets>

FOOTER: "<footer exact, ou rien>"
DO NOT: add colors, printed fonts, extra words, emojis, logos other than the one described, decorative illustrations.
```

## Règles

- Noir et blanc, sans exception : une couleur transforme le carnet en autre chose.
- Aucune police numérique : tout est manuscrit, y compris les numéros.
- Le texte est plus court que dans l'éditorial ; un point qui ne tient pas sur une ligne manuscrite se coupe.
- Le logo, s'il est demandé, se dessine au trait dans un coin, jamais en couleur.
- Le prompt part avec "exactly and nothing else" : ce rendu invente facilement des mots.

## Exemples

- "Ma méthode en 6 étapes pour un premier appel, version cahier" : structure 1, six sections numérotées, une flèche entre chaque, un encadré "à ne pas faire" en bas ; réponse attendue : le prompt complet et l'image, noir et blanc.
- "Les 4 erreurs des dirigeants qui prospectent seuls" : structure 15, quatre paires "erreur" barrée puis "à la place" encadrée ; réponse attendue : une page symétrique en deux colonnes.
- "Le triangle contenu, prospection, appel" : structure 5 ou 12, un triangle dessiné au centre, trois annotations ; réponse attendue : peu de texte, un schéma qui porte l'idée.
