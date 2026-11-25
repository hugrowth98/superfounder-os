---
name: ideation
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

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`, les autres sous-skills dans `{SKILL_BASE}/sous-skills/`. Le master a déjà chargé le socle d'écriture (voix, stratégie, règles de hook, checklist) : ce fichier le complète, il ne le répète pas.

# LinkedIn Ideation

Ce skill génère des idées de posts LinkedIn en croisant 4 sources :
0. **Le Content Brain, en premier** : les fiches de la base de connaissances, les trous signalés par les pages de piliers, les signaux de `02_Veille/Marche/`
1. **Veille temps réel** : actualités du secteur, lancements d'outils, tendances
2. **Sources du créateur** : chaînes YouTube, newsletters, ressources sauvegardées
3. **Frameworks LinkedIn** : les 4A, TOFU/MOFU/BOFU, Authority-First, piliers thématiques

> Ce skill lit ses sources de veille et la stratégie de contenu dans `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md` à chaque exécution. Si ce fichier contient encore `[à remplir]`, propose de lancer "Installe mon contenu".

## Workflow d'idéation

Quand l'utilisateur demande des idées de posts, exécute ces étapes **dans l'ordre** :

### Étape 0 - Partir du Content Brain

Lis `10_Skills/_commun/content-brain.md`, puis dans `05_Departements/Marketing/Content-Brain/` :

1. `Content-Brain.md` et les pages `01_Strategie/Piliers/Pilier_<Nom>.md` : le nombre de fiches par pilier, les sujets "pas encore couverts".
2. Les fiches de `03_Base-de-connaissances/` dont `utilise_dans` est vide ou date de plus de 90 jours, hors `diffusion: interne`. Ce sont les idées les plus sûres : la matière existe déjà, dans ses mots.
3. `02_Veille/Marche/` : les signaux récents. Une idée née d'un signal doit y répondre avec une fiche de la base, sinon elle reste un commentaire d'actualité.
4. `04_Idees/` : les idées déjà notées (`nouvelle`, `retenue`) pour ne pas les reproposer, et `05_Calendrier-editorial/` pour ce qui est déjà programmé ou publié.

Au moins la moitié des idées proposées s'appuient sur une fiche existante, citée par son titre. Une idée sans fiche est signalée "matière à creuser" et renvoie au sous-skill `interview`.

Chaque idée retenue par l'utilisateur est écrite dans `04_Idees/` au format du fichier de structure (`statut: retenue`, `pilier`, `format`, `support`, `fiches`, `signal` s'il y en a un). Le calendrier recommandé suit la répartition de la stratégie et n'aligne jamais deux posts du même pilier à la suite.

### Étape 1 - Collecte de la matière (veille)

**D'abord le brief de la semaine, s'il existe** : si `05_Departements/Marketing/Content-Brain/02_Veille/Sources-veille.json` est rempli, le sous-skill `veille` a déjà lu les sources (`sources/veille_AAAA-MM-JJ.json`, ou `Brief-veille_AAAA-MM-JJ.md`). Pars de cette matière, elle est plus riche et déjà scorée. Les recherches ci-dessous complètent pour l'actualité du jour, ou remplacent la veille quand le fichier de sources est vide.

Utilise les outils disponibles pour collecter des signaux frais :

**A. Actualités du secteur (WebSearch)**
Lance 3-5 recherches ciblées sur les piliers du créateur (voir `les piliers de `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`` et `sa niche (voir `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`)`). Adapte les requêtes au domaine de l'utilisateur.

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
1. **Pertinence** : est-ce lié aux piliers du créateur ?
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

**Angle** : [L'angle unique du créateur sur ce sujet - en 1-2 phrases]

**Hook suggéré** : [Le hook, prêt à utiliser]

**Idée développée** : [3-5 lignes décrivant le contenu du post]
```

### Étape 4 - Calendrier éditorial

Organise les idées en un calendrier (la fréquence de publication définie dans `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`) respectant :
- **Répartition éditoriale** : voir `la répartition éditoriale de `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md``
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

## Sources de veille du créateur

### Chaînes YouTube suivies
Voir `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`, section Sources de veille.

### Newsletters suivies
Voir `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`, section Sources de veille.

### Autres sources de veille
Voir `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`, section Sources de veille.

### Ressources sauvegardées (playbooks & guides)

Consulte `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`, section Ressources sauvegardées, pour la liste des guides et ressources bookmarkés par le créateur. Ces ressources sont une mine d'or pour les posts educational et lead-magnet.

## Output attendu

Pour chaque session d'idéation, produis :

```
# 🧠 BRIEF ÉDITORIAL - Semaine du [date]

## 📡 SIGNAUX DE LA SEMAINE
[Top 5 signaux identifiés avec source]

## 💡 IDÉES DE POSTS (10-15)
[Chaque idée au format structuré ci-dessus]

## 📅 CALENDRIER RECOMMANDÉ
[Tableau la fréquence de publication définie dans `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`]

## 🔥 HOT TAKE DE LA SEMAINE
[L'actualité ou tendance qui mérite une réaction rapide]

## 💎 IDÉE LEAD MAGNET
[Si pertinent : une idée de ressource à offrir]
```

## Règles d'idéation

1. **Authority-First** : ne proposer QUE des sujets sur lesquels le créateur a une expérience ou un avis unique
2. **Pas de generic** : "5 outils à tester" n'est intéressant que si le créateur les a TESTÉS
3. **Mixer les formats** : ne pas proposer 10 posts éducatifs d'affilée (les quatre valeurs du champ `format` : `educatif`, `storytelling`, `hot-take`, `lead-magnet`)
4. **Actualité + Evergreen** : 50% d'idées liées à l'actu, 50% intemporelles
5. **Un seul sujet par post** : chaque idée = 1 post = 1 idée
6. **Penser engagement** : privilégier les sujets qui déclenchent des commentaires (opinions, questions, débats)
7. **Saisonnalité** : tenir compte des événements (rentrée, fin d'année, lancements majeurs)

## Fichiers de référence

Lis ces fichiers AVANT de générer des idées, ils contiennent tout le contexte stratégique du créateur :

- `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md` : **LIS EN PREMIER.** Positionnement, monopole personnel, piliers, répartition éditoriale, convictions, sources de veille. C'est le GPS de toute l'idéation.
- `05_Departements/Marketing/Content-Brain/02_Veille/Inspirations/` : posts qui résonnent avec le créateur, classés par catégorie (4A), et posts des créateurs admirés. Analyse des patterns qui marchent.
- `05_Departements/Marketing/Content-Brain/01_Strategie/Posts-de-reference.md` : ses posts réels par thème, marqueurs de style, longueurs de référence, sujets à éviter. Pour calibrer les hooks et le ton des idées.
- Consulte aussi `{SKILL_BASE}/ressources/frameworks-strategie.md` pour les frameworks stratégiques détaillés.
- Consulte aussi `{SKILL_BASE}/ressources/formules-de-hooks.md` pour la bibliothèque de hooks.
