---
name: linkedin-ideation
description: >
  Skill d'idéation et de veille automatique pour générer des idées de posts LinkedIn.
  Utilise ce skill dès que l'utilisateur veut : trouver des idées de posts, faire de la veille sur ses sujets,
  analyser les tendances de son secteur, scraper des chaînes YouTube ou newsletters pour trouver de l'inspiration,
  créer un calendrier éditorial, ou planifier ses contenus LinkedIn.
  Se déclenche sur : "idées de posts", "inspiration", "de quoi je pourrais parler", "veille", "tendances",
  "qu'est-ce qui buzz", "calendrier éditorial", "planning contenu", "cette semaine", "sujets chauds",
  "idéation", "brainstorm", "actualités", "quoi poster", "brief éditorial", "content plan".
  Ce skill utilise WebSearch et des outils de scraping pour collecter les sources de veille de l'utilisateur
  puis croise les tendances avec ses frameworks LinkedIn pour générer des idées prêtes à développer.
---

# LinkedIn Ideation

Ce skill génère des idées de posts LinkedIn en croisant 3 sources :
1. **Veille temps réel** : actualités du secteur, lancements d'outils, tendances
2. **Sources de le créateur** : chaînes YouTube, newsletters, ressources sauvegardées
3. **Frameworks LinkedIn** : les 4A, TOFU/MOFU/BOFU, Authority-First, piliers thématiques

> Ce skill lit ses sources de veille et la stratégie de contenu dans `05 Departements/Contenu/LinkedIn/strategie-contenu.md` à chaque exécution. Si ce fichier contient encore `[à remplir]`, propose de lancer "Installe mon contenu".

## Workflow d'idéation

Quand l'utilisateur demande des idées de posts, exécute ces étapes **dans l'ordre** :

### Étape 1 - Collecte de la matière (veille)

Utilise les outils disponibles pour collecter des signaux frais :

**A. Actualités du secteur (WebSearch)**
Lance 3-5 recherches ciblées sur les piliers de le créateur (voir `les piliers de `05 Departements/Contenu/LinkedIn/strategie-contenu.md`` et `sa niche (voir `05 Departements/Contenu/LinkedIn/strategie-contenu.md`)`). Adapte les requêtes au domaine de l'utilisateur.

**B. Dernières vidéos YouTube (scraping ou WebSearch)**
Scrape les dernières vidéos des chaînes suivies (voir liste plus bas) :
- Pour chaque chaîne, cherche la dernière vidéo ou scrape la page `/videos`
- Extrais : titre, sujet, angle

**C. Dernières newsletters (scraping ou WebSearch)**
Scrape les derniers articles des newsletters suivies :
- Pour chaque newsletter, cherche les articles récents
- Extrais : titre, sujet, insights clés

**D. Autres sources (WebSearch)**
- Cherche les dernières nouveautés sur les autres sources de veille (voir liste)
- Note les signaux les plus prometteurs

### Étape 2 - Analyse & tri des signaux

Pour chaque signal collecté, évalue :
1. **Pertinence** : est-ce lié aux piliers de le créateur ?
2. **Fraîcheur** : est-ce une actualité récente (< 7 jours) ou un sujet evergreen ?
3. **Potentiel engagement** : est-ce que ça va générer du débat, des saves, du dwell time ?
4. **Authority-First** : le créateur a-t-il une expérience personnelle ou un avis unique sur ce sujet ?

Garde uniquement les 15-20 signaux les plus pertinents.

### Étape 3 - Transformation en idées de posts

Pour chaque signal, génère une idée de post structurée :

```
## Idée [N] - [Titre court]

**Signal source** : [YouTube / Newsletter / News / Autre] - [lien]
**Pilier** : [pilier concerné]
**Type 4A** : [Actionable / Analytical / Aspirational / Anthropological]
**Format recommandé** : [educational / storytelling / hot-take / lead-magnet]
**Funnel** : [TOFU / MOFU / BOFU]

**Angle** : [L'angle unique de le créateur sur ce sujet - en 1-2 phrases]

**Hook suggéré** : [Le hook, prêt à utiliser]

**Idée développée** : [3-5 lignes décrivant le contenu du post]
```

### Étape 4 - Calendrier éditorial

Organise les idées en un calendrier (la fréquence de publication définie dans `05 Departements/Contenu/LinkedIn/strategie-contenu.md`) respectant :
- **Répartition éditoriale** : voir `la répartition éditoriale de `05 Departements/Contenu/LinkedIn/strategie-contenu.md``
- **Répartition 4A** : varier Actionable, Analytical, Aspirational, Anthropological
- **Répartition formats** : varier educational, storytelling, hot-take, lead-magnet (max 1 lead-magnet/semaine)
- **Répartition funnel** : TOFU (40%), MOFU (40%), BOFU (20%)

```
| Jour | Idée | Type | Pilier | Hook |
|------|------|------|--------|------|
| ... | ... | Educational (Actionable) | ... | ... |
| ... | ... | Hot-take (Anthropological) | ... | ... |
| ... | ... | Storytelling (Aspirational) | ... | ... |
| ... | ... | Educational (Analytical) | ... | ... |
```

## Sources de veille de le créateur

### Chaînes YouTube suivies
Voir `05 Departements/Contenu/LinkedIn/strategie-contenu.md`, section Sources de veille.

### Newsletters suivies
Voir `05 Departements/Contenu/LinkedIn/strategie-contenu.md`, section Sources de veille.

### Autres sources de veille
Voir `05 Departements/Contenu/LinkedIn/strategie-contenu.md`, section Sources de veille.

### Ressources sauvegardées (playbooks & guides)

Consulte `05 Departements/Contenu/LinkedIn/strategie-contenu.md`, section Ressources sauvegardées, pour la liste des guides et ressources bookmarkés par le créateur. Ces ressources sont une mine d'or pour les posts educational et lead-magnet.

## Output attendu

Pour chaque session d'idéation, produis :

```
# 🧠 BRIEF ÉDITORIAL - Semaine du [date]

## 📡 SIGNAUX DE LA SEMAINE
[Top 5 signaux identifiés avec source]

## 💡 IDÉES DE POSTS (10-15)
[Chaque idée au format structuré ci-dessus]

## 📅 CALENDRIER RECOMMANDÉ
[Tableau la fréquence de publication définie dans `05 Departements/Contenu/LinkedIn/strategie-contenu.md`]

## 🔥 HOT TAKE DE LA SEMAINE
[L'actualité ou tendance qui mérite une réaction rapide]

## 💎 IDÉE LEAD MAGNET
[Si pertinent : une idée de ressource à offrir]
```

## Règles d'idéation

1. **Authority-First** : ne proposer QUE des sujets sur lesquels le créateur a une expérience ou un avis unique
2. **Pas de generic** : "5 outils à tester" n'est intéressant que si le créateur les a TESTÉS
3. **Mixer les formats** : ne pas proposer 10 posts educational d'affilée
4. **Actualité + Evergreen** : 50% d'idées liées à l'actu, 50% intemporelles
5. **Un seul sujet par post** : chaque idée = 1 post = 1 idée
6. **Penser engagement** : privilégier les sujets qui déclenchent des commentaires (opinions, questions, débats)
7. **Saisonnalité** : tenir compte des événements (rentrée, fin d'année, lancements majeurs)

## Fichiers de référence

Lis ces fichiers AVANT de générer des idées, ils contiennent tout le contexte stratégique de le créateur :

- `05 Departements/Contenu/LinkedIn/strategie-contenu.md` : **LIS EN PREMIER.** Positionnement, monopole personnel, piliers, répartition éditoriale, convictions, sources de veille. C'est le GPS de toute l'idéation.
- `05 Departements/Contenu/LinkedIn/swipe-file.md` : posts qui résonnent avec le créateur, classés par catégorie (4A), et posts des créateurs admirés. Analyse des patterns qui marchent.
- `05 Departements/Contenu/LinkedIn/posts-de-reference.md` : ses posts réels par thème, marqueurs de style, longueurs de référence, sujets à éviter. Pour calibrer les hooks et le ton des idées.
- Consulte aussi `../linkedin-writing-core/references/formations-frameworks.md` pour les frameworks stratégiques détaillés.
- Consulte aussi `../linkedin-writing-core/references/hooks-library.md` pour la bibliothèque de hooks.
