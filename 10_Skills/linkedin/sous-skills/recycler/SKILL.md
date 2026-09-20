---
name: recycler
description: >
  Tire plusieurs contenus d'un seul : un post texte en carrousel ou en vidéo courte, une
  newsletter en trois posts, un live en clips, un cas client en avant/après, et fait tourner
  les outils de création de LinkedIn (newsletter, live, articles collaboratifs, programmation).
  Se déclenche sur : "recycle ce post", "transforme en carrousel", "découpe ce live", "fais
  trois posts de ma newsletter", "newsletter LinkedIn", "que faire de ce post qui a marché".
  Ne pas utiliser pour écrire un post neuf (sous-skills du type) ni pour l'image d'une
  infographie (master `infographie`).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Recycler

Un contenu de fond par semaine peut devenir six à huit publications. Les 10 pour cent de posts qui ont le mieux marché méritent cinq fois plus de recyclage que les autres (sous-skill `performance` pour les trouver).

## La matrice

| Source | Cible | Comment |
|---|---|---|
| Post texte | Carrousel | 8 à 12 slides, une idée par slide, un nouveau titre (sous-skill `formats`) |
| Post texte | Vidéo | 30 à 90 secondes face caméra, sous-titres, le même point avec une anecdote |
| Carrousel | Newsletter | une slide devient un paragraphe, avec la profondeur et les liens |
| Newsletter | 3 à 5 posts | chaque idée devient un post autonome avec son propre hook |
| Vidéo, podcast | Post texte | transcrire, extraire la meilleure citation ou l'insight, réécrire |
| Article de blog | Post texte | l'idée numéro un, lien en premier commentaire |
| Épisode, interview | Carrousel | 8 à 10 citations ou idées en slides |
| Live | 3 à 5 clips | les meilleurs moments de 30 à 60 secondes, un par jour la semaine suivante |
| Cas client | Avant / après | situation de départ, résultats, ce qui a changé entre les deux (voir `{SKILL_BASE}/ressources/frameworks-narratifs.md`) |

## Règles

1. Jamais de copier-coller d'un format à l'autre : chaque support a ses règles.
2. Le hook change à chaque recyclage, même si l'idée est la même.
3. Deux à quatre semaines avant de rejouer un post texte en post texte ; entre deux formats, on peut enchaîner dans la même semaine.
4. La voix reste celle de l'utilisateur : `Tone-and-Voice.md` et `posts-de-reference.md`, relus avant d'adapter.

## Les outils de LinkedIn

- **Newsletter LinkedIn** : notification et email à chaque édition, taux d'ouverture élevés, indexée par les moteurs ; la première édition invite toutes les relations ; une seule newsletter par compte, abonnés non exportables ; hebdomadaire ou bimensuelle.
- **Live** : beaucoup plus de réactions et de commentaires qu'une vidéo native ; outil tiers nécessaire (StreamYard, Restream, OBS) ; annoncer 24 à 48 heures avant et une heure avant ; 30 à 60 minutes ; 3 à 5 clips ensuite.
- **Articles collaboratifs** : 2 à 4 paragraphes par contribution, badge après 5 à 10 contributions, bien référencés ; utile pour la crédibilité, pas pour la portée.
- **Programmation native** : jusqu'à trois mois à l'avance ; avec Publora, le skill `planifier-post`.

## La boucle hebdomadaire

```
une newsletter (ou un live) par semaine
  → 3 ou 4 posts texte tirés de ses sections
    → le meilleur post devient un carrousel
      → une vidéo de 60 secondes sur le même point
        → les questions des commentaires nourrissent la newsletter suivante
```

## Méthode

1. Identifier la source et ce qu'elle contient (idées, chiffres, citations, étapes).
2. Choisir les cibles avec la matrice, deux ou trois au plus par source.
3. Pour chaque cible : un nouveau hook, le gabarit du support (sous-skill `formats`), le texte dans la voix de l'utilisateur.
4. Étaler dans le calendrier (sous-skill `publier`), en respectant les délais entre formats.

## Exemples

- "Ce post a fait 5 000 impressions, j'en fais quoi ?" : un carrousel de 8 slides la semaine suivante, puis une vidéo de 60 secondes avec une anecdote ; réponse attendue : le découpage et les deux nouveaux hooks.
- "Ma newsletter a trois sections" : trois posts (lundi, mercredi, vendredi), la section la plus chiffrée en carrousel, les questions des lecteurs en hooks de la semaine d'après ; réponse attendue : les trois posts et le calendrier.
- "J'ai un live de 45 minutes" : 4 clips de 30 à 60 secondes (mardi à vendredi), un post texte des 5 points à retenir, la conversation entière en newsletter ; réponse attendue : les moments à couper avec leurs horodatages si le transcript existe.
