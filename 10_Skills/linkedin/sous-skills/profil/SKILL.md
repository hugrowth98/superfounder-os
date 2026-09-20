---
name: profil
description: >
  Fait du profil LinkedIn une page qui convertit : le titre (220 caractères), la section à
  propos (2 600 caractères), la sélection, la bannière, les preuves (recommandations,
  compétences, expériences chiffrées, URL personnalisée), écrits dans la voix de l'utilisateur
  et à partir de son offre. Se déclenche sur : "optimise mon profil", "mon titre LinkedIn",
  "réécris ma section à propos", "ma bannière", "les gens visitent mon profil mais ne
  m'écrivent pas". Ne pas utiliser pour un post (master `linkedin`) ni pour une page
  entreprise (hors périmètre).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Profil

Un post amène sur le profil ; le profil transforme la visite en abonnement, en connexion ou en message. Chaque élément se lit comme une page de vente courte : pour qui, quel résultat, quelle preuve, quelle prochaine étape. La matière vient de `02_Contexte/Offer-Positioning.md` (offre, différenciation, preuves) et de `Clients-Problems-and-Messages.md` (les mots des clients). Les formules détaillées sont dans `{SKILL_BASE}/ressources/profil.md`.

## Le titre (220 caractères)

Il dit ce que vous faites pour qui, pas votre poste. Trois formules :

| Formule | Exemple de forme |
|---|---|
| "J'aide [cible] à [résultat]" | "J'aide les dirigeants de PME B2B à remplir leur agenda de rendez-vous sans agence" |
| "[Rôle] · [niche] · [preuve]" | "Fondateur · prospection B2B · 120 dirigeants accompagnés" |
| "[Rôle] · [ce que vous faites] · [preuve ou appel]" | "Consultant GTM · j'installe votre machine à rendez-vous · ex-directeur commercial" |

À bannir : "visionnaire", "expert passionné", "ninja", "leader d'opinion", et un titre de poste seul. Les mots-clés que votre cible tape dans la recherche LinkedIn y sont.

## La section à propos (2 600 caractères)

```
[ACCROCHE, les 2 premières lignes visibles avant "voir plus"]
qui vous aidez et ce qui vous distingue, en une phrase précise

[LE PROBLÈME, 2 à 3 phrases] la douleur de votre cible, dans ses mots
[VOTRE APPROCHE, 3 à 5 phrases] comment vous la traitez, votre méthode
[LES PREUVES, 3 à 5 puces] résultats chiffrés, clients nommés si possible, certifications, médias
[AVEC QUI, 2 à 3 phrases] le client idéal, pour qu'il se reconnaisse
[LA SUITE, 1 à 2 phrases] la prochaine étape exacte : message, appel, email
```

## La sélection, la bannière, les preuves

- **Sélection** (3 à 5 éléments, le plus important à gauche, à jour chaque mois) : une ressource gratuite (elle nourrit la liste email), le meilleur post, un cas client ou un témoignage, la newsletter, une intervention.
- **Bannière** : 1 584 x 396 pixels, l'essentiel au centre (les bords sont coupés sur mobile), une promesse, une preuve ou un site ; les couleurs de `03_Branding/charte-visuelle.md` ; le master `infographie` peut la produire.
- **Preuves** : 5 à 10 recommandations demandées avec une question précise ("qu'est-ce qui a changé après nos trois mois ?"), les 3 compétences clés épinglées, des expériences avec des chiffres ("équipe de 5 à 25, chiffre d'affaires x3"), l'URL personnalisée, une activité régulière.

## Méthode

1. Lire l'offre et les mots des clients dans `02_Contexte/`, puis le profil actuel (collé par l'utilisateur).
2. Diagnostic en 5 lignes : titre, accroche de l'à propos, preuves, sélection, appel. Direct, sans faux compliments.
3. Trois titres, dans la voix de l'utilisateur, avec la formule utilisée.
4. La section à propos réécrite dans le gabarit, avec les chiffres et les noms qu'il a donnés, rien d'inventé ; un chiffre manquant devient une question.
5. La sélection recommandée (ordre), le brief de bannière, les recommandations à demander (à qui, avec quelle question).
6. Contrôle : vouvoiement ou tutoiement selon `Tone-and-Voice.md`, aucun mot de la liste noire, aucune donnée inventée.

## Exemples

- "Les gens visitent mon profil et ne m'écrivent pas" : le titre parle de lui et pas d'eux, aucune preuve chiffrée, pas de prochaine étape ; réponse attendue : trois titres, un à propos réécrit, un appel clair.
- "Réécris mon à propos" : gabarit en six blocs, chiffres de `Offer-Positioning.md`, question pour chaque chiffre manquant ; réponse attendue : le texte complet et deux variantes d'accroche.
- "Ma bannière" : promesse plus preuve, essentiel au centre, charte ; réponse attendue : le texte de la bannière et le brief pour le master `infographie`.
