---
name: linkedin-educational
description: >
  Skill pour créer des posts LinkedIn éducatifs et d'expertise dans ta voix.
  Utilise ce skill quand l'utilisateur veut écrire un post LinkedIn de type : tutoriel, how-to,
  liste d'outils, framework, méthode, workflow, checklist, comparatif, bad vs good,
  infographie textuelle, guide pratique, ou tout post qui enseigne quelque chose.
  Se déclenche sur : "tutoriel", "comment faire", "how-to", "outils", "framework", "méthode",
  "workflow", "checklist", "étapes", "process", "comparatif", "bad vs good", "liste de",
  "guide", "les X meilleurs", "voici comment", "système", "stack", "playbook".
  Charge TOUJOURS linkedin-writing-core en premier pour les règles de base.
---

# LinkedIn Educational - Posts d'expertise {{CREATOR_NAME}}

**Prérequis** : Lis d'abord `../linkedin-writing-core/SKILL.md` pour les règles fondamentales. Ce skill les complète avec les structures éducatives spécifiques.

## Quand utiliser ce skill

Ce skill couvre tous les posts qui enseignent, expliquent ou partagent une expertise :
- **How-to / Tutoriel** : étapes pour accomplir quelque chose
- **Liste d'outils** : curation d'outils testés par {{CREATOR_FIRSTNAME}}
- **Framework / Méthode** : système conceptuel actionnable
- **Workflow** : process étape par étape
- **Checklist** : liste de vérification
- **Comparatif / Bad vs Good** : mise en opposition de deux approches
- **Infographie textuelle** : post structuré visuellement comme une infographie

## Principe fondamental : Authority-First

Le contenu éducatif générique ne performe plus. N'importe qui peut demander à une IA de produire "5 tips pour [sujet]". Ce qui fait la différence, c'est que le contenu vient de l'expérience vécue de {{CREATOR_FIRSTNAME}}.

Chaque post éducatif doit répondre à cette question : **"Qu'est-ce que je sais que les autres ne savent pas, parce que je l'ai vécu/testé/observé ?"**

Cela se traduit par :
- Des exemples issus de cas réels de {{CREATOR_FIRSTNAME}} ou de ses clients
- Des chiffres concrets (pas de "amélioration significative" mais "passé de [X] à [Y]")
- Des noms d'outils spécifiques avec contexte d'utilisation
- Un point de vue, pas juste de l'information, mais un avis

## Les 7 formats éducatifs

### 1. Le How-To / Tutoriel
Explique comment accomplir quelque chose, étape par étape.

**Structure** :
```
HOOK → Résultat obtenu + méthode annoncée
CONTEXTE → Pourquoi c'est utile (1-2 lignes)
ÉTAPES → Numérotées (3-7 étapes)
  Pour chaque étape :
  ↳ Action concrète
  ↳ Outil utilisé (si applicable)
  ↳ Résultat de l'étape
RÉSULTAT GLOBAL → Ce qu'on obtient à la fin
CTA → Question ou invitation à tester
```

**Exemple de hook** :
"J'ai rendu [tâche du métier] 10x plus rapide avec l'IA. (Et je vous dévoile tout ↓)"

**Règles** :
- Chaque étape doit être exécutable immédiatement
- Nommer les outils spécifiques (pas "un outil de transcription" mais le nom exact)
- Inclure les résultats chiffrés quand possible

### 2. La Liste d'Outils / Ressources
Curation d'outils testés, classés et commentés.

**Structure** :
```
HOOK → Nombre d'outils + problème résolu + (teaser d'un bonus)
INTRO → Pourquoi c'est utile (2-3 lignes)
LISTE → Pour chaque outil :
  → [Nom de l'outil]
  ↳ Ce qu'il fait (1 ligne)
  ↳ Points forts (1 ligne)
  ↳ Prix (si pertinent)
RECOMMANDATION → L'avis de {{CREATOR_FIRSTNAME}} (lequel il préfère et pourquoi)
CTA → Question ("Et vous, quel outil utilisez-vous ?")
```

**Exemple de hook** :
"J'ai testé 10 outils gratuits pour [résoudre un problème du métier] :"

**Règles** :
- {{CREATOR_FIRSTNAME}} doit avoir testé ou connaître les outils cités
- Toujours donner un avis/recommandation, pas juste une liste plate
- Inclure les prix quand c'est pertinent

### 3. Le Framework / Méthode
Présente un système conceptuel actionnable.

**Structure** :
```
HOOK → Nom du framework ou problème résolu
LE PROBLÈME → Ce que les gens font mal (2-3 lignes)
LE FRAMEWORK → Explication structurée
  → Composante 1 : explication
  → Composante 2 : explication
  → Composante 3 : explication
EXEMPLE → Application concrète du framework
CONCLUSION → Synthèse en 1 phrase + question
```

**Exemple** :
Le framework "Authority-First" est un bon exemple de ce format : un nom mémorable, une répartition claire, une logique défendable.

**Règles** :
- Le framework doit être original ou adapté par {{CREATOR_FIRSTNAME}}
- Pas de frameworks génériques déjà vus partout
- Illustrer avec un cas concret

### 4. Le Workflow / Process
Montre un process étape par étape, souvent lié à l'IA ou l'automatisation.

**Structure** :
```
HOOK → Résultat du workflow + temps gagné
LE PROCESS CLASSIQUE → Comment ça se faisait avant (le "avant")
LE NOUVEAU WORKFLOW → Les étapes automatisées
  1️⃣ Étape 1
  ↳ Détail + outil
  2️⃣ Étape 2
  ↳ Détail + outil
  3️⃣ Étape 3
  ↳ Détail + outil
RÉSULTAT → Chiffres concrets (temps gagné, résultats obtenus)
CTA → Offre du process ou question
```

**Spécificité** : Ce format est parfait pour les posts sur l'automatisation, montrer le avant/après d'un workflow.

### 5. La Checklist
Liste de vérification que le lecteur peut appliquer directement.

**Structure** :
```
HOOK → Nombre d'éléments + promesse
CONTEXTE → Pourquoi cette checklist est utile (2 lignes)
CHECKLIST → Éléments structurés
  → Point 1 : explication courte
  → Point 2 : explication courte
  [...etc]
DERNIER POINT → Laisser ouvert ("Et vous, quel est le point le plus important ?")
```

**Règles** :
- Chaque item doit être concret et vérifiable
- 5 à 10 éléments max
- Le dernier item peut être "?" pour engager en commentaire

### 6. Le Comparatif / Bad vs Good
Oppose deux approches pour montrer la meilleure voie.

**Structure** :
```
HOOK → Ce que les gens font vs ce qu'ils devraient faire
COLONNE "BAD" → Les pratiques obsolètes/inefficaces
COLONNE "GOOD" → Les bonnes pratiques
  Pour chaque paire :
  ❌ [Ce qu'ils font] → ✅ [Ce qu'ils devraient faire]
SYNTHÈSE → Le message principal
CONCLUSION → Question ou prise de position
```

**Variante "What we think vs The truth"** :
Même structure mais formulée comme une correction de croyance commune.

**Règles** :
- Les éléments "bad" doivent être des choses que l'audience fait réellement (pas des strawmen)
- Les éléments "good" doivent être actionnables
- Maximum 5-7 paires pour garder le post digestible

### 7. L'Infographie Textuelle
Post structuré visuellement comme une infographie, sans image.

**Structure** :
```
HOOK → Titre de l'infographie
SECTIONS → Structurées visuellement avec symboles

◉ Section 1
→ Point A
→ Point B

◉ Section 2
→ Point C
→ Point D

[...etc]

CONCLUSION → Synthèse
```

**Quand l'utiliser** : Quand le contenu se prête à une organisation visuelle (catégories, niveaux, comparaisons).

## Techniques d'écriture éducative

### Le "skimmable content"
Les posts éducatifs doivent être lisibles en diagonale. Si quelqu'un ne lit que les titres/sous-titres, il doit comprendre l'essentiel.

- Les titres des sections portent le message clé
- Les détails sont en dessous, pour ceux qui veulent creuser
- Alterner phrases courtes (le message) et développements (le contexte)

### La preuve par l'exemple
Chaque concept abstrait est immédiatement illustré :
```
❌ "L'IA permet d'optimiser [tâche]."
✅ "L'IA analyse 100 [éléments] en 5 minutes et les score selon ton critère. Voici comment je fais :"
```

### Le "so what" test
Après chaque point, se demander : "Et alors, qu'est-ce que le lecteur en fait ?"
Si la réponse n'est pas claire, ajouter un élément actionnable.

### Dwell time
Les posts éducatifs bien structurés génèrent du dwell time élevé car le lecteur prend le temps de lire chaque point. Favoriser :
- Les listes numérotées (l'œil suit naturellement)
- Les comparaisons (le cerveau veut voir les deux côtés)
- Les "open loops" entre sections (créer de la curiosité pour la suite)

## Erreurs spécifiques au contenu éducatif

- **Trop générique** : "5 tips pour [sujet]" peut être écrit par tout le monde. Ajouter l'angle {{CREATOR_FIRSTNAME}}.
- **Pas d'expérience derrière** : Si {{CREATOR_FIRSTNAME}} n'a pas testé/vécu ce dont il parle, ne pas prétendre.
- **Liste plate sans avis** : Une liste d'outils sans recommandation n'apporte rien. Donner un point de vue.
- **Trop technique** : Adapter au niveau de l'audience ({{ICP}}). Vulgariser sans simplifier à l'excès.
- **Pas de résultat** : Toujours montrer le "et donc ?", le résultat concret de la méthode.

## Fichiers de référence

- `references/examples-educational.md` - Méta-analyse des facteurs de viralité éducative + emplacement de ton swipe file de posts éducatifs de référence (à remplir via l'installeur).
- Consulte aussi `../linkedin-writing-core/references/examples-myposts.md` pour tes posts éducatifs réels.
- Consulte aussi `../linkedin-writing-core/references/post-templates.md` pour les templates Livre/Ressource, Liste, Leçons d'événement, Actualité.
