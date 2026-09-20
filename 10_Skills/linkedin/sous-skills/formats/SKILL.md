---
name: formats
description: >
  Choisit le support d'un post LinkedIn (texte seul, carrousel PDF, vidéo native, image,
  sondage, newsletter LinkedIn, lien externe) selon l'objectif, le contenu et la portée
  attendue, et donne les règles de chaque support (nombre de slides, longueur, sous-titres,
  lien en premier commentaire). Se déclenche sur : "quel format", "carrousel ou texte",
  "je fais une vidéo ?", "je mets le lien où", "sondage", "combien de slides", "newsletter
  LinkedIn". Pour produire l'image d'une infographie, passe la main au master `infographie` ;
  pour le calendrier de publication, au sous-skill `publier`.
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Formats

Le support se choisit après le contenu, jamais avant. Un cadre qui se lit en 8 slides, un récit qui se lit en texte, une démonstration qui se regarde en vidéo. Les multiplicateurs ci-dessous sont des repères observés sur des comptes B2B, pas des lois : les chiffres de l'utilisateur (sous-skill `performance`) l'emportent dès qu'il en a.

## Les supports

| Support | Portée (texte = 1) | Il sert à | Règles |
|---|---|---|---|
| Carrousel (PDF) | 2,5 à 3,5 | cadre, méthode pas à pas, liste, comparatif | 8 à 12 slides ; la slide 1 est un titre qui arrête, la dernière un appel (suivre, enregistrer, commenter) ; une idée par slide, texte gros et lisible sur téléphone, charte de `03_Branding/` ; texte d'accompagnement de 800 à 1 500 caractères avec son propre hook |
| Texte seul | 1 | récit, opinion, insight, coulisses | 1 500 à 2 500 caractères, hook dans les 210 premiers, une phrase par ligne, listes en → ou ↳, aucun lien dans le corps |
| Vidéo native | 1,2 à 2 | marque personnelle, démonstration, tuto | 30 à 90 secondes dans le fil (jusqu'à 10 minutes pour un tuto), sous-titres obligatoires (regardée sans son), vertical 9:16, visage plus texte à l'écran ; jamais un lien YouTube collé, toujours le fichier importé |
| Image avec texte | 1 à 1,5 | infographie, citation, capture commentée | une image par post ; l'infographie se fabrique avec le master `infographie` ; l'image doit se comprendre sans le texte |
| Sondage | 0,8 à 1,2 | connaître l'audience, préparer un post | un par semaine au plus, 2 ou 3 réponses plutôt que 4, une question qui divise vraiment |
| Newsletter LinkedIn | variable | contenu de fond, abonnés notifiés | hebdomadaire ou bimensuelle, notification et email à chaque édition, indexée par les moteurs ; une seule newsletter par compte, abonnés non exportables |
| Lien externe dans le corps | 0,3 à 0,6 | à éviter | le lien va en premier commentaire, le post le dit ("lien en commentaire") et donne déjà l'essentiel |

## L'arbre de décision

```
Portée maximale, contenu structuré        → carrousel
Récit, avis, une seule idée               → texte seul
Montrer un écran, une manipulation, soi   → vidéo native courte
Un chiffre ou un cadre à mémoriser        → image (master infographie) avec un texte court
Sonder avant d'écrire                     → sondage, puis un post sur les résultats
Fond, série, fidéliser                    → newsletter LinkedIn, avec 3 posts extraits (sous-skill recycler)
Faire cliquer hors LinkedIn               → texte natif + lien en premier commentaire
```

## Méthode

1. Lire le contenu ou l'idée (le post existe déjà, ou le brief du sous-skill du type).
2. Nommer l'objectif en un mot : portée, confiance, conversation, conversion, trafic.
3. Choisir le support avec l'arbre, dire pourquoi en une phrase, proposer un second choix.
4. Donner le gabarit du support : pour un carrousel, le découpage slide par slide (titre, une phrase, un élément visuel) ; pour une vidéo, le plan en 3 temps (accroche 3 secondes, démonstration, appel) et le texte d'accompagnement ; pour une image, le brief pour `infographie` ; pour un sondage, la question et les 2 ou 3 réponses.
5. Rappeler la règle du lien et la longueur du texte d'accompagnement.

## Le carrousel, slide par slide

```
Slide 1   le titre, comme un hook : chiffre ou promesse précise, 6 à 9 mots
Slide 2   le problème ou le contexte, une phrase
Slides 3 à N-1   une idée par slide : titre court, 1 à 2 phrases, un élément visuel simple
Slide N   l'appel : ce qu'on fait de l'idée, et suivre / enregistrer / commenter un mot-clé
```

Le fond, les couleurs et la typographie viennent de `03_Branding/charte-visuelle.md`. La fabrication des slides (PDF) se fait dans l'outil de l'utilisateur ; ce sous-skill livre le texte de chaque slide.

## Exemples

- "J'ai un cadre en 7 étapes pour préparer un appel" : carrousel de 9 slides (titre, 7 étapes, appel), texte d'accompagnement de 900 caractères avec hook ; réponse attendue : le découpage slide par slide et le texte.
- "Je veux raconter le client que j'ai perdu" : texte seul, cadre situation puis bascule puis leçon (sous-skill `storytelling`), moins de 1 300 caractères ; réponse attendue : le choix justifié, le second choix (vidéo face caméra de 60 secondes).
- "Je veux pousser mon article de blog" : texte natif qui donne l'idée principale, lien en premier commentaire ; réponse attendue : le post, et le commentaire à poster juste après.
