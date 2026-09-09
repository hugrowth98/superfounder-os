---
name: linkedin-hot-take
description: >
  Skill pour créer des posts LinkedIn d'opinion et de prise de position dans ta voix.
  Utilise ce skill quand l'utilisateur veut écrire un post LinkedIn de type : opinion tranchée,
  conviction forte, prise de position, réaction à une tendance, avis controversé, manifesto,
  "ce que tout le monde pense vs la réalité", post polarisant, ou tout post qui challenge une idée reçue.
  Se déclenche sur : "opinion", "conviction", "hot take", "avis", "je pense que", "prise de position",
  "impopulaire", "controversé", "mythe", "croyance", "la vérité sur", "ce que personne ne dit",
  "ce que tout le monde fait mal", "mon avis sur", "arrêtez de", "stop", "le problème avec".
  Charge TOUJOURS linkedin-writing-core en premier pour les règles de base.
---

# LinkedIn Hot Take - Posts d'opinion {{CREATOR_NAME}}

**Prérequis** : Lis d'abord `../linkedin-writing-core/SKILL.md` pour les règles fondamentales. Ce skill les complète avec les techniques de prise de position spécifiques.

## Quand utiliser ce skill

Ce skill couvre tous les posts qui prennent position, challengent ou provoquent la réflexion :
- **Opinion tranchée** : point de vue fort sur un sujet de l'industrie
- **Conviction / Manifesto** : croyance profonde qui guide les actions de {{CREATOR_FIRSTNAME}}
- **What we think vs The truth** : démontage d'une idée reçue
- **Réaction à une tendance** : avis sur une nouveauté, une mode, un buzz
- **Post polarisant** : position qui divise intentionnellement l'audience

## L'ADN des opinions de {{CREATOR_FIRSTNAME}}

{{CREATOR_FIRSTNAME}} n'est pas un provocateur gratuit. Ses opinions sont :
- **Fondées sur l'expérience** : il a vu, testé, ou observé ce dont il parle
- **Au service de l'audience** : l'opinion vise à faire réfléchir ou à débloquer
- **Assumées** : pas de "je pense peut-être que...", il affirme
- **Nuancées dans le développement** : le hook est tranché, le corps apporte la nuance

### Les convictions de {{CREATOR_FIRSTNAME}} (Manifesto)
Ces convictions irriguent tous ses posts d'opinion :

{{CONVICTIONS}}

> Consulte `references/manifesto-convictions.md` pour le détail des convictions et les angles de posts associés.

## Les 5 formats d'opinion

### 1. L'Opinion Tranchée
Prend position clairement sur un sujet.

**Structure** :
```
HOOK → L'opinion en une phrase percutante

CONSTAT → Ce que {{CREATOR_FIRSTNAME}} observe (factuel)
  "Voici ce que je vois :"
  → [Observation 1]
  → [Observation 2]

POURQUOI → L'explication derrière l'opinion
  "La raison est simple :"
  [Développement en 2-3 paragraphes courts]

CE QUE ÇA IMPLIQUE → Les conséquences concrètes
  → [Implication 1]
  → [Implication 2]

MA POSITION → Réaffirmation claire
  [1-2 phrases qui résument]

QUESTION → Ouvrir le débat
  "Et vous, quel est votre avis ?"
```

**Hooks typiques** :
- "J'ai une conviction qui dérange : [conviction]."
- "[Croyance populaire]. Je pense l'inverse."
- "Compétence sous-estimée en [domaine] : [compétence]."

### 2. Le What We Think vs The Truth
Démonte une croyance répandue en la confrontant à la réalité.

**Structure** :
```
HOOK → La croyance populaire + "C'est faux." ou "Voici pourquoi."

CE QU'ON CROIT → La version populaire/mainstream
  "La plupart des [persona] pensent que [croyance]."

POURQUOI C'EST FAUX → Les arguments
  "En réalité :"
  → [Argument 1 avec preuve]
  → [Argument 2 avec preuve]
  → [Argument 3 avec preuve]

CE QU'IL FAUT FAIRE À LA PLACE → L'alternative
  "Ce qui marche vraiment :"
  → [Action 1]
  → [Action 2]

CONCLUSION → Reformulation de la vérité
```

**Hooks typiques** :
- "[Croyance populaire] est un mythe. Voici pourquoi."
- "Tout le monde dit de [action]. Personne ne dit de [vraie action]."
- "Ce que [persona] croit : [X]. La réalité : [Y]."

### 3. Le Manifesto / Conviction Profonde
Exprime une croyance fondamentale de {{CREATOR_FIRSTNAME}} sur son domaine.

**Structure** :
```
HOOK → La conviction en une phrase

CONTEXTE → D'où vient cette conviction
  "J'en suis arrivé là après [expérience]."

DÉVELOPPEMENT → Les facettes de la conviction
  [3-4 paragraphes courts qui explorent l'idée sous différents angles]

EXEMPLES → Illustrations concrètes
  → [Exemple 1]
  → [Exemple 2]

CONCLUSION → La conviction reformulée, plus forte
  [Phrase de fermeture qui résonne]
```

**Ton** : Plus introspectif que les autres formats. {{CREATOR_FIRSTNAME}} réfléchit à voix haute, mais avec assurance.

### 4. La Réaction à une Tendance
Prend position sur une actualité, un buzz, une nouvelle technologie.

**Structure** :
```
HOOK → L'événement/tendance + angle de {{CREATOR_FIRSTNAME}}

CE QUI SE PASSE → Description factuelle (2-3 lignes)

CE QUE ÇA CHANGE → Impact concret pour l'audience
  → [Impact 1]
  → [Impact 2]
  → [Impact 3]

MON AVIS → La position de {{CREATOR_FIRSTNAME}}
  [2-3 paragraphes d'analyse]

CE QUE JE RECOMMANDE → Actions concrètes
  → [Recommandation 1]
  → [Recommandation 2]

QUESTION → Demander l'avis de l'audience
```

**Hooks typiques** :
- "[Entreprise/Outil] vient de lancer [chose]. Voici ce que ça change."
- "Tout le monde parle de [sujet]. Voici ce que personne ne dit."
- "[Tendance] : surcôté ou game-changer ? Mon avis."

### 5. Le Post Polarisant
Divise intentionnellement l'audience pour créer du débat.

**Structure** :
```
HOOK → Déclaration forte qui divise

DÉVELOPPEMENT → Argumentation solide
  [Arguments 1, 2, 3 avec exemples]

NUANCE → (Optionnel) Reconnaître la part de vérité de l'autre côté
  "Je comprends ceux qui pensent [autre avis]. Mais..."

RÉAFFIRMATION → Maintenir la position
  [Conclusion ferme]

QUESTION → Inviter au débat
  "Tu es d'accord ? Dis-le en commentaire."
```

**Règles du post polarisant** :
- Ne jamais être irrespectueux ou méprisant envers ceux qui pensent différemment
- La polarisation porte sur des IDÉES, pas sur des personnes
- Avoir des arguments solides (pas de provocation vide)
- La nuance peut venir dans le développement, même si le hook est tranché

## Techniques d'écriture d'opinion

### La montée en puissance
Commencer par le constat, monter en intensité, finir par la conviction.
```
Constat calme → Arguments → Exemples → Opinion tranchée → Punchline
```

### Le retournement
Présenter d'abord l'idée mainstream, puis la retourner.
```
"Tout le monde dit que [X]."
"J'ai cru ça aussi."
"Puis j'ai [expérience]."
"Et j'ai compris que [opinion inverse]."
```

### La preuve par l'absurde
Pousser une idée reçue jusqu'à ses conclusions logiques pour montrer ses limites.
```
"Si [croyance] était vraie, alors [conséquence absurde]."
"Or, [réalité]."
"Donc [conclusion]."
```

### L'empathie stratégique
Reconnaître la position adverse avant de la démonter. Ça renforce la crédibilité.
```
"Je comprends pourquoi [persona] fait [action]."
"C'est logique quand [contexte]."
"Mais voici le problème :"
```

## Sujets d'opinion typiques de {{CREATOR_FIRSTNAME}}

{{OPINION_TOPICS}}

## Erreurs spécifiques aux posts d'opinion

- **Provocation gratuite** : L'opinion doit apporter quelque chose, pas juste choquer.
- **Pas de preuves** : Une opinion sans argument est juste du bruit.
- **Trop de nuances dans le hook** : Le hook est tranché. La nuance vient après.
- **Moraliser** : {{CREATOR_FIRSTNAME}} partage son avis, il ne fait pas la leçon.
- **Opinions hors scope** : Rester sur le terrain d'expertise de {{CREATOR_FIRSTNAME}} ({{NICHE}}). Éviter politique, religion, société si ce n'est pas son sujet.
- **Attaquer des personnes** : Toujours critiquer des idées/pratiques, jamais des individus.

## Fichiers de référence

- `references/examples-hot-take.md` - Méta-analyse des facteurs de viralité opinion + emplacement de ton swipe file de posts d'opinion de référence (à remplir via l'installeur).
- `references/manifesto-convictions.md` - Tes convictions avec angles de posts associés + piliers thématiques (à remplir via l'installeur). C'est LA référence pour ancrer chaque post hot-take dans une conviction authentique.
- Consulte aussi `../linkedin-writing-core/references/examples-myposts.md` pour tes posts d'opinion réels.
- Consulte aussi `../linkedin-writing-core/references/post-templates.md` pour les templates Actualité/Réaction et Prise de conscience.
