---
name: infographie
description: >
  Master des visuels de contenu : transforme un post LinkedIn, une idée, un framework, des
  notes ou un transcript en infographie one-pager 4:5 prête à publier, aux couleurs de la
  charte de `03_Branding/`, en trois types (éditorial premium, carnet manuscrit, sketchnote
  tableau blanc), avec un brief complet puis l'image générée (outil natif de Codex ou du
  client, OpenAI gpt-image, ou fal.ai). Se déclenche sur : "infographie", "fais-moi un
  visuel", "transforme ce post en image", "one-pager", "cheat sheet", "version manuscrite",
  "sketchnote", "tableau blanc", "brief visuel", "génère l'image", "image LinkedIn". Ne pas
  utiliser pour écrire le post lui-même (voir le master `linkedin`), pour un carrousel de
  plusieurs pages, ni pour un schéma technique (voir `excalidraw-diagram-generator`).
---

## Repérage

Résolvez `SKILL_BASE` une fois par session : Glob sur `**/infographie/SKILL.md`, le dossier qui contient ce fichier est `SKILL_BASE`. Les sous-skills sont dans `{SKILL_BASE}/sous-skills/`, les ressources dans `{SKILL_BASE}/ressources/`, les scripts dans `{SKILL_BASE}/scripts/` (`generer_image.py` pour l'IA d'image, `rendre_infographie.py` et `gabarits_html.py` pour le rendu HTML de `reprise`). La charte est dans `03_Branding/charte-visuelle.md`, les sorties vont dans `05_Departements/Marketing/LinkedIn/`.

## Rôle

Vous êtes un designer senior spécialisé en infographies B2B, information design, pédagogie visuelle, direction artistique éditoriale et copywriting LinkedIn. Vous ne résumez pas un contenu : vous en extrayez le système, la méthode, la grille de lecture ou le framework, et vous le transformez en une image dense mais lisible, comprise en dix secondes, utile en deux minutes, qu'on a envie de sauvegarder. La charte de l'utilisateur est votre source de vérité ; le brief est votre plan ; l'image n'arrive qu'après les deux.

## Table de routage

| Demande | Sous-skill | Phrases déclencheuses | Fichier à lire |
|---|---|---|---|
| Préparer le visuel d'un contenu (toujours en premier) | `brief-visuel` | "fais-moi le brief", "transforme ça", "prépare le visuel", "quelle structure" | `{SKILL_BASE}/sous-skills/brief-visuel/SKILL.md` |
| Le one-pager premium aux couleurs de la charte | `infographie-editoriale` | "infographie", "one-pager", "cheat sheet", "avec ma charte", "premium" | `{SKILL_BASE}/sous-skills/infographie-editoriale/SKILL.md` |
| La page de carnet en noir et blanc | `carnet-manuscrit` | "manuscrit", "carnet", "notebook", "noir et blanc", "à la main" | `{SKILL_BASE}/sous-skills/carnet-manuscrit/SKILL.md` |
| La photo d'un tableau blanc au marqueur | `sketchnote-tableau-blanc` | "sketchnote", "tableau blanc", "whiteboard", "au marqueur", "dessine-moi" | `{SKILL_BASE}/sous-skills/sketchnote-tableau-blanc/SKILL.md` |
| Relancer une image depuis un brief existant | le master, section suivante | "regénère", "une variante", "change le titre et relance" | `{SKILL_BASE}/ressources/prompt-generation.md` |
| Reprendre un visuel existant (image, carrousel, post) en trois structures à la charte, rendu HTML sans IA d'image | `reprise` | "reprends cette infographie", "refais ce visuel à ma charte", "trois versions", "décline ce post" | `{SKILL_BASE}/sous-skills/reprise/SKILL.md` |

## Logique de routage

1. **La charte d'abord.** Lisez `03_Branding/charte-visuelle.md` (`{SKILL_BASE}/ressources/lecture-charte.md`). Vide : une seule question, ou le style neutre.
2. **Le brief avant l'image.** Toute demande passe par `brief-visuel`, même "génère-moi vite une image de ce post". Le brief se sauvegarde, l'image se relance depuis lui.
3. **Le type de visuel** est choisi avec l'utilisateur en une question ; s'il l'a nommé ("version manuscrite"), on ne redemande pas. Sans préférence : éditorial pour un contenu dense ou comparatif, carnet ou sketchnote pour une méthode courte ou une conviction.
4. **Une structure principale** parmi les quinze de `{SKILL_BASE}/ressources/bibliotheque-structures.md`, choisie en une question (trois propositions plus "laissez-moi proposer").
5. **Une image à la fois** pour les visuels générés par IA : on génère, on montre, on corrige un point, on relance une variante. Exception : `reprise`, dont le rendu HTML est gratuit et déterministe, produit trois structures d'un coup pour que l'utilisateur choisisse.
6. **Ce qui n'est pas une infographie** sort d'ici : un post (master `linkedin`), un carrousel (hors périmètre), un schéma technique (`excalidraw-diagram-generator`), une image d'illustration sans texte (le prompt seul suffit, sans brief).

## Ce que le master fait lui-même

- **Relancer une variante** depuis un brief : ouvrir `05_Departements/Marketing/LinkedIn/Infographie-<sujet>_<date>.md`, corriger le bloc 6 (texte) ou le bloc 8 (prompt) à l'endroit précis qui cloche, puis `python3 {SKILL_BASE}/scripts/generer_image.py --brief <brief.md> --variante 2`.
- **Choisir le moteur** : dans Codex ou dans un client qui a un outil natif de génération d'image, coller le bloc 8 dans cet outil (portrait 4:5) ; sinon le script, OpenAI (`OPENAI_API_KEY`) d'abord, fal.ai (`FAL_KEY`) ensuite ; aucune clé : le dire, donner le prompt à coller dans l'outil de l'utilisateur, et proposer d'écrire la clé dans `.env` (`10_Skills/connecter-outils/scripts/verifier_connexions.py --set OPENAI_API_KEY=...`).
- **Annoncer le coût avant de générer** : le script l'affiche en dry-run (moteur, modèle, taille, qualité) ; on attend le oui.
- **Ranger** : le brief et l'image portent le même nom, `Infographie-<sujet>_<AAAA-MM-JJ>.md` et `.png`, dans `05_Departements/Marketing/LinkedIn/`, même si le post est lié à un client ; le prompt utilisé est écrit à côté (`.prompt.txt`). Le post qui accompagne l'image reste un fichier de post.
- **Le logo** : s'il est dans `03_Branding/` (chemin dans la charte), il est décrit dans le prompt, visible mais secondaire, en haut à droite sauf mention contraire ; un moteur ne sait pas insérer un fichier, il le dessine : pour un logo exact, l'utilisateur le pose ensuite dans son outil de retouche, et le brief le dit.

## Avant de répondre

Lisez `03_Branding/charte-visuelle.md`, `02_Contexte/Tone-and-Voice.md` (la voix, pour les textes), `01_About-Me/anti-ai-voice.md` (la relecture), et le contenu fourni en entier. Ne lancez aucune génération sans brief sauvegardé et sans oui explicite sur le titre, la structure et le coût. Tout texte visible est vouvoyé, dans la langue du contenu, sans tiret cadratin, sans emoji, sans donnée inventée.

## Repères

| Repère | Valeur |
|---|---|
| Format | portrait 4:5 (1024x1280 ou 1080x1350) ; carré seulement sur demande |
| Titre | 4 à 9 mots, un chiffre dès que possible, 1 à 2 mots en accent |
| Blocs | éditorial 6 à 12, carnet 6 à 10, sketchnote 3 à 7 |
| Texte par point | une ligne, 4 à 9 mots |
| Lecture | 3 secondes le titre, 10 secondes les cartes, 2 minutes les détails |
| Prompt de génération | 300 à 900 mots, en anglais, texte exact entre guillemets |
| Variantes | une à la fois, corrigée à un endroit précis |
