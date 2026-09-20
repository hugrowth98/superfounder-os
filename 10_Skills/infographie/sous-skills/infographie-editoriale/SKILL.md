---
name: infographie-editoriale
description: >
  Le one-pager B2B premium : dense mais lisible, éditorial, pédagogique, structuré en cartes,
  aux couleurs et typographies de la charte de `03_Branding/`. Écrit la direction artistique
  et le prompt de génération d'un brief produit par `brief-visuel`, puis lance l'image.
  Se déclenche sur : "infographie premium", "one-pager", "cheat sheet", "playbook visuel",
  "version éditoriale", "avec ma charte", "style ressource à sauvegarder". Ne pas utiliser pour
  un rendu manuscrit (voir `carnet-manuscrit`) ni pour une photo de tableau blanc (voir
  `sketchnote-tableau-blanc`).
---

Le style des grandes infographies B2B qui se sauvegardent : un grand titre fort, des sections numérotées, des cartes encadrées, des blocs "utilisez ce prompt" et "conseil", des mini-tableaux, des checklists, des faux fichiers, des badges de catégorie, un footer discret, le logo visible mais secondaire. Dense, structuré, moderne sans être futuriste, jamais cartoon, jamais un modèle de générateur de visuels générique.

## Ressources

- `{SKILL_BASE}/ressources/lecture-charte.md` : la charte fait foi, l'ordre de priorité.
- `{SKILL_BASE}/ressources/bibliotheque-structures.md` : les structures et les patterns de composition.
- `{SKILL_BASE}/ressources/prompt-generation.md` : l'anatomie du prompt, les moteurs, la checklist.
- `{SKILL_BASE}/ressources/copywriting-visuel.md` : si un texte du brief dépasse encore une ligne.

## Méthode

1. **Partir du brief** (blocs 1 à 6 de `brief-visuel`). Sans brief, le produire d'abord.
2. **Poser les surfaces** : le fond global, le fond des cartes, le fond des blocs de section, dans les couleurs de la charte (deux niveaux de surface font la hiérarchie). Le fond sombre de la charte sert pour un bandeau ou un bloc prompt, jamais pour toute l'image sauf demande.
3. **Poser les couleurs par rôle** : texte principal, texte secondaire, accent principal sur le titre (1 à 2 mots), les numéros, les badges et les mots surlignés ; accent secondaire pour les contrastes froids ; couleur positive pour les validations et les bénéfices ; couleur d'alerte pour les erreurs à éviter. Jamais plus de trois couleurs actives sur une image.
4. **Poser la typographie** : la police de titres en gras pour le titre, les sous-titres et les titres de cartes ; la police de corps pour le texte ; un monospace pour les prompts, les commandes et les faux fichiers. Trois tailles : le titre, environ trois fois le corps ; les titres de cartes, une fois et demie ; le corps.
5. **Poser les composants** : badges et cartouches en pilule, cartes à bordure nette d'épaisseur moyenne, coins légèrement arrondis, ombres nulles ou très discrètes, connecteurs fins (traits, pointillés ou courbes sobres), icônes simples et éditoriales, peu nombreuses.
6. **Régler la densité** : 6 à 12 blocs sur une image 4:5, marges de 4 pour cent, gouttières régulières, aucune zone vide sans raison, aucune zone où deux textes se touchent. Un contenu qui ne tient pas se coupe (retour au bloc 6 du brief), il ne se tasse pas.
7. **Écrire le bloc 7** (direction artistique) en expliquant, pour chaque choix, quelle règle de la charte il respecte.
8. **Écrire le bloc 8** (prompt de génération) selon `prompt-generation.md` : cadre, structure, texte exact entre guillemets, direction artistique en hexadécimal, hiérarchie, contraintes, interdits de la charte, logo.
9. **Générer** : dans Codex ou un client avec un outil d'image, coller le prompt ; sinon `python3 {SKILL_BASE}/scripts/generer_image.py --brief <brief.md> --dry-run`, annoncer le moteur, le modèle, la taille et le coût, attendre le oui, relancer sans `--dry-run`.
10. **Montrer l'image, lire ce qui cloche** (texte mal rendu, carte trop pleine, couleur hors charte, mot inventé), corriger le prompt à cet endroit, relancer une variante. Sauvegarder l'image à côté du brief.

## Direction artistique par défaut (quand la charte ne dit rien)

Fond global crème, cartes plus claires, blocs de section plus soutenus ; texte presque noir ; un accent chaud unique sur le titre, les numéros et les badges ; titres en sans-serif géométrique gras, corps en serif lisible, prompts en monospace ; bordures nettes, coins à 8 px, aucune ombre, connecteurs fins pointillés ; icônes en trait simple, une par section au plus ; logo en haut à droite, 6 pour cent de la largeur.

## Règles

- La charte gagne sur tout, y compris sur cette direction par défaut.
- Une structure principale domine ; les blocs "prompt", "conseil", "exemple" sont des cartouches à l'intérieur, pas des structures.
- Aucun dégradé fort, aucune illustration décorative, aucun emoji, aucune police fantaisie, aucun rendu "présentation d'entreprise".
- Le texte du prompt reprend le bloc 6 mot pour mot : on ne paraphrase pas en anglais un texte qui doit s'afficher en français.
- Toute image part avec la contrainte "render exactly this text, nothing else".
- Format portrait 4:5 ; carré 1:1 seulement si le contenu est très compact et que l'utilisateur le demande.

## Exemples

- "Version premium de mon post sur les 7 signaux d'achat" : structure 3 (grille de conseils) en 7 cartes numérotées, accent sur "7 signaux", un cartouche "quand écrire" par carte ; réponse attendue : la direction artistique, le prompt, l'image en 4:5.
- "Compare Unipile et Lemlist pour LinkedIn" : structure 9 (tableau comparatif), colonnes "ce que c'est", "quand", "limite", encadré final "notre choix" ; réponse attendue : un tableau lisible sur téléphone, 5 lignes au plus.
- "Le système de prospection en 5 briques" : structure 5 (hub et rayons), concept central, 5 modules avec rôle et 3 points ; réponse attendue : un "operating system" visuel, connecteurs courbes, une couleur d'accent.
