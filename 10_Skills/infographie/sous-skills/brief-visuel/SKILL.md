---
name: brief-visuel
description: >
  Transforme n'importe quel contenu (post LinkedIn, idée, framework, notes, transcript,
  description) en brief d'infographie complet : lecture de la charte, analyse du contenu,
  choix du type de visuel et de la structure, titre, textes exacts, direction artistique,
  prompt de génération et checklist qualité. Se déclenche sur : "fais-moi le brief",
  "brief d'infographie", "prépare le visuel de ce post", "transforme ça en infographie",
  "je veux un one-pager de", "quelle structure pour ce contenu". C'est le tronc commun des
  trois types de visuels ; la direction artistique et le prompt se terminent dans le sous-skill
  du type choisi (`infographie-editoriale`, `carnet-manuscrit`, `sketchnote-tableau-blanc`).
---

Une infographie ne résume pas un contenu : elle en extrait le système, la méthode, la grille de lecture ou le framework, puis le transforme en une image qu'on comprend en dix secondes et qu'on garde pour s'en servir. Le brief est ce qui sépare une image générique d'une ressource qu'on sauvegarde : tout ce que l'image montrera y est écrit avant de générer quoi que ce soit.

## Ressources

- `{SKILL_BASE}/ressources/lecture-charte.md` : lire `03_Branding/charte-visuelle.md` en premier, l'ordre de priorité, le style neutre si la charte est vide.
- `{SKILL_BASE}/ressources/bibliotheque-structures.md` : les quinze structures, la règle de sélection, les patterns de titre et de composition.
- `{SKILL_BASE}/ressources/copywriting-visuel.md` : les règles du texte d'image et la compression éditoriale.
- `{SKILL_BASE}/ressources/prompt-generation.md` : l'anatomie du prompt final, les moteurs, la checklist.
- `01_About-Me/anti-ai-voice.md` : la relecture du texte avant de rendre.

## Méthode

1. **Lire la charte** (`03_Branding/charte-visuelle.md`) et la traduire en 5 à 10 règles opérationnelles. Si elle est vide, une seule question, ou le style neutre de `lecture-charte.md`. Pour un carnet manuscrit ou un sketchnote, ne garder que le ton, les interdits et le logo.
2. **Analyser le contenu** : l'idée centrale ; le problème auquel il répond ; la promesse ; le lecteur cible et son niveau ; la transformation proposée ; les concepts clés ; les étapes, piliers ou catégories ; les tensions ; les exemples concrets ; les phrases qui peuvent devenir des titres ou des labels ; les éléments qui méritent d'être visualisés ; le framework caché. On n'invente rien : une donnée absente reste absente.
3. **Choisir le type de visuel** avec l'utilisateur, une seule question : éditorial premium (la charte, dense, cartes), carnet manuscrit (noir et blanc, page de cahier), sketchnote tableau blanc (photo d'un tableau, marqueurs). S'il ne sait pas : éditorial pour un contenu dense ou comparatif, carnet ou sketchnote pour une méthode courte ou un contenu de conviction.
4. **Choisir la structure** dans la bibliothèque : proposer les trois structures qui collent le mieux à la nature du contenu, plus "laissez-moi proposer", en une question. Une structure principale ; une hybridation légère au plus.
5. **Choisir le titre** : quatre options, une par pattern (A, B, C, D), avec le sous-titre ou son absence, la plus adaptée marquée "(recommandé)". Une question.
6. **Compresser** : garder les idées les plus fortes, écrire pour chaque bloc le titre court, la phrase d'explication, 2 à 4 points, un exemple si utile, une règle si possible. Règles de `copywriting-visuel.md`.
7. **Écrire le brief** au format ci-dessous, textes exacts compris, puis le passer au sous-skill du type choisi pour la direction artistique et le prompt final.
8. **Relire** : checklist §H d'`anti-ai-voice.md` sur tous les textes, checklist qualité de `prompt-generation.md`. Corriger, repasser.
9. **Sauvegarder** le brief dans `05_Departements/Marketing/LinkedIn/Infographie-<sujet>_<AAAA-MM-JJ>.md`, montrer le titre, la structure et cinq lignes du texte, attendre le oui avant de générer.

Une question à la fois. L'utilisateur peut répondre "autre" à chaque choix : on intègre sa réponse sans discuter.

## Le format du brief

```
# Infographie : <titre final>

## 1. Charte
Règles extraites (5 à 10 lignes) ; ou "style neutre" et pourquoi.

## 2. Analyse
Idée centrale / Problème / Promesse / Lecteur / Framework caché / Points à visualiser.

## 3. Type et structure
Type de visuel ; structure retenue et pourquoi ; ratio (4:5).

## 4. Titre et sous-titre
Les quatre options, la combinaison choisie, les 1 ou 2 mots en accent.

## 5. Structure détaillée
Section par section : nom, rôle, disposition, élément visuel.

## 6. Texte exact
Tout le texte visible, bloc par bloc, prêt à coller : titre, sous-titre, sections,
cartes, points, exemples, prompts, labels, footer. Rien d'autre n'apparaîtra.

## 7. Direction artistique
(écrite par le sous-skill du type)

## 8. Prompt de génération
(écrit par le sous-skill du type, en anglais, prêt à coller)

## 9. Checklist qualité
Les dix points de prompt-generation.md, cochés.
```

## Règles

- Le brief est en français ; le prompt de génération en anglais ; le texte de l'image dans la langue du contenu.
- Aucun chiffre, nom, citation ou source qui ne vienne pas du contenu ou de l'utilisateur.
- Une seule promesse par image, lisible dans le titre.
- Le texte exact est figé avant la direction artistique : on ne redesigne pas un texte flou.
- Le brief se sauvegarde avant la génération : c'est lui qu'on relance pour une variante.
- Vouvoiement sur tout ce qui sera lu par l'audience.

## Exemples

- "Transforme ce post sur mes 5 prompts de prospection en infographie" : type éditorial, structure 3 (grille de conseils) ou 1 (guide en étapes), titre pattern B ; réponse attendue : le brief en 9 blocs, sauvegardé, prêt à générer.
- "J'ai une idée : les 4 erreurs des dirigeants qui prospectent seuls" : type carnet manuscrit ou sketchnote, structure 15 (anti-guide), titre pattern C ; réponse attendue : le brief avec les quatre paires erreur puis correction, textes exacts.
- "Fais un visuel de ce transcript de 40 minutes" : analyse d'abord (le framework caché), puis une question sur le type, puis la structure ; réponse attendue : un brief qui tient sur une image, pas un carrousel.
