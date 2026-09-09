# Guide : Construire votre infrastructure Claude

Un processus étape par étape pour transformer Claude en assistant ultra-personnalisé qui connaît votre vie, votre business, vos clients, votre voix : et qui sait où ranger ce qu'il produit.

> **Ce guide est conçu pour devenir un skill.** Chaque étape est exécutable séquentiellement par Claude lui-même. Les sections marquées `[CLAUDE EXECUTE]` correspondent à des actions que l'IA peut faire. Les sections marquées `[HUMAIN]` requièrent une action de l'utilisateur. Les blocs `## PROMPT` sont à copier-coller tels quels dans une nouvelle conversation Claude.

---

## 0. Pourquoi vous avez besoin de ça

L'IA générique fonctionne par prédiction du mot suivant à partir de milliards de documents publics. Sans contexte personnel, elle produit mécaniquement la moyenne du web : propre, correct, générique. Inutilisable sans ré-écriture.

Avec une infrastructure de contexte structurée, Claude :
- Sait qui vous êtes (rôle, contraintes, énergie disponible, modèle économique)
- Sait ce que vous vendez et à qui
- Connaît le langage exact de vos clients
- Écrit dans votre voix, pas la sienne
- Sait où ranger ce qu'il produit
- Ne pose plus 10 questions de contexte à chaque session

**Courbe de qualité attendue :**
- Sans base : ~50% (générique)
- Avec socle : ~80% (cohérent, aligné)
- Après 2-3 itérations : ~95% (spécifique)
- Finition manuelle : derniers 5%

**Temps total pour mettre en place le système : 4-8h**, étalées sur quelques jours. Vous le faites une fois, vous le réutilisez à vie.

---

## 1. L'architecture cible (vue d'ensemble)

Voici l'arborescence que ce guide vous fait construire :

```
votre-workspace/
├── CLAUDE.md                              ← le GPS racine, lu à chaque session
├── ABOUT.ME/                              ← qui vous êtes (chargé chaque session)
│   ├── about-me.md
│   ├── my-company.md
│   └── anti-ai-voice.md (optionnel)
├── Contexte/                              ← votre cerveau (chargé à la demande)
│   ├── Constitution-Identity.md
│   ├── Life-and-Work-Reality.md
│   ├── Goals-and-Direction.md
│   ├── Offer-Positioning.md
│   ├── Clients-Problems-and-Messages.md
│   ├── Expertise-Standards-and-Landmines.md
│   └── Tone-and-Voice.md
├── ressources-templates/                  ← assets transversaux (hooks, exemples)
├── Intelligence/                          ← veille, transcriptions, daily logs
├── Projects/                              ← le travail en cours
│   ├── Sales/
│   │   ├── input/
│   │   ├── output/
│   │   └── ressources/
│   ├── LinkedIn/
│   │   ├── input/
│   │   ├── output/
│   │   └── ressources/
│   ├── Newsletter/
│   ├── Produit-Clients/
│   ├── Stratégie/
│   └── Marketing/
└── .claude/
    └── skills/                            ← vos skills custom
```

**Principes structurants :**

1. **Divulgation progressive** : `CLAUDE.md` et `ABOUT.ME/` sont chargés à chaque session. `Contexte/` n'est chargé que si la tâche le justifie. Vous évitez la saturation du contexte.
2. **Pas de duplication** : un fichier source = un seul endroit. On pointe via chemins relatifs.
3. **Sandbox dédié** : Claude n'a accès qu'à ce dossier parent, jamais à `~/Documents` ou `~/Desktop`.
4. **Convention de nommage** : `Nom-Sujet_YYYY-MM-DD.ext` pour les livrables datés.

> **Note sur le naming** : les fichiers de `Contexte/` portent des noms en anglais (`Constitution-Identity.md`, `Goals-and-Direction.md`, etc.). Ce sont les noms de référence des prompts d'interview. Vous pouvez les renommer en français si vous préférez : pensez juste à mettre à jour les prompts en conséquence.

---

## 2. Setup initial (pré-requis)

### 2.1 [HUMAIN] Installez Claude Code

Claude Code est un agent IA qui vit sur votre ordinateur, capable de lire/écrire des fichiers, exécuter des commandes, naviguer sur le web. C'est la brique qui rend cette infrastructure exploitable.

→ https://www.anthropic.com/claude-code

Installez-le, lancez-le une première fois, faites le tour des commandes (`/help`).

### 2.2 [HUMAIN] Créez votre dossier parent

Choisissez un nom et un emplacement (idéalement pas dans iCloud/Drive synchronisés agressivement) :

```bash
mkdir -p ~/MonCerveauIA
cd ~/MonCerveauIA
```

**Règle de sandbox :** Claude n'aura accès qu'à ce dossier. Ne le placez pas à la racine de votre Documents ou Bureau.

### 2.3 [CLAUDE EXECUTE] Créez la structure de dossiers vide

Lancez Claude Code dans ce dossier et collez ce prompt :

```
Crée la structure de dossiers suivante dans le répertoire courant,
en laissant les fichiers vides pour l'instant :

CLAUDE.md (vide)
ABOUT.ME/about-me.md (vide)
ABOUT.ME/my-company.md (vide)
ABOUT.ME/anti-ai-voice.md (vide)
Contexte/Constitution-Identity.md (vide)
Contexte/Life-and-Work-Reality.md (vide)
Contexte/Goals-and-Direction.md (vide)
Contexte/Offer-Positioning.md (vide)
Contexte/Clients-Problems-and-Messages.md (vide)
Contexte/Expertise-Standards-and-Landmines.md (vide)
Contexte/Tone-and-Voice.md (vide)
ressources-templates/.gitkeep
Intelligence/daily-logs/.gitkeep
Projects/Sales/input/.gitkeep
Projects/Sales/output/.gitkeep
Projects/Sales/ressources/.gitkeep
Projects/LinkedIn/input/.gitkeep
Projects/LinkedIn/output/.gitkeep
Projects/LinkedIn/ressources/.gitkeep
Projects/Newsletter/input/.gitkeep
Projects/Newsletter/output/.gitkeep
Projects/Newsletter/ressources/.gitkeep
Projects/Produit-Clients/input/.gitkeep
Projects/Produit-Clients/output/.gitkeep
Projects/Produit-Clients/ressources/.gitkeep
Projects/Stratégie/input/.gitkeep
Projects/Stratégie/output/.gitkeep
Projects/Stratégie/ressources/.gitkeep
Projects/Marketing/input/.gitkeep
Projects/Marketing/output/.gitkeep
Projects/Marketing/ressources/.gitkeep
.claude/skills/.gitkeep

Confirme la création avec un `tree -L 3`.
```

**Validation :** Vous devriez voir une arborescence propre. Tous les fichiers sont vides : on va les remplir un par un.

---

## 3. Étape 1 : Construire `CLAUDE.md` (le GPS racine)

`CLAUDE.md` est lu **automatiquement par Claude à chaque session**. C'est votre fichier le plus stratégique. Il doit rester court (sous 500 lignes) et contenir :

1. Les règles de collaboration globales
2. La cartographie de l'architecture
3. Les règles de routage (où ranger quoi)
4. Les fichiers à charger automatiquement

**Principe clé :** Ne l'écrivez pas vous-même. Faites-le générer par Claude après lui avoir expliqué votre fonctionnement.

### 3.1 [CLAUDE EXECUTE] Génération assistée

Dans une nouvelle conversation Claude Code, collez ce prompt :

```
## CONTEXTE

Tu vas m'aider à rédiger le fichier CLAUDE.md de mon workspace personnel.
Ce fichier sera lu automatiquement par toi à chaque session.

L'arborescence de mon workspace est la suivante :
[colle ici l'output du `tree -L 3` de l'étape 2.3]

## OBJECTIF DU FICHIER

CLAUDE.md doit contenir 5 sections :

1. **Règles de collaboration** (toujours valables)
   - Comportements à toujours adopter / éviter
   - Niveau de confirmation requis avant action
   - Langue par défaut
   - Style de communication attendu

2. **Fichiers à lire au démarrage de chaque session**
   - Liste des fichiers ABOUT.ME/* à charger systématiquement

3. **Architecture du workspace**
   - Description de chaque dossier racine
   - Convention input/output/ressources des Projects
   - Convention de nommage des fichiers

4. **Règles de routage des livrables**
   - Arbre de décision : où ranger quoi
   - Tie-breaker pour cas ambigus

5. **Routage automatique du contexte**
   - Quels fichiers Contexte/* charger selon la tâche

## TON RÔLE À CE STADE

Tu ne dois PAS écrire le fichier maintenant.

Tu dois d'abord m'INTERVIEWER pour comprendre :
- Mon style de collaboration préféré (direct, formel, en français/anglais ?)
- Les actions qui requièrent ma validation explicite
- Les types de livrables que je produis le plus souvent (posts LinkedIn ? propales ?
  briefs internes ? code ? autre ?)
- Comment je veux organiser mes Projects (par client ? par canal ? par type d'actif ?)

Pose-moi tes questions UNE PAR UNE.
N'écris le CLAUDE.md final qu'à la fin, quand tu auras tous les éléments.
```

### 3.2 [HUMAIN] Répondez à l'interview

Comptez 20-30 minutes. Soyez précis. Donnez des exemples concrets.

### 3.3 [CLAUDE EXECUTE] Production du fichier

Quand l'interview est finie, demandez :

```
Maintenant écris le CLAUDE.md final.

Contraintes :
- Maximum 200 lignes
- Sections clairement numérotées
- Arbre de décision de routage avec exemples concrets
- Aucun blabla : que des règles actionnables
- Format : markdown

Crée le fichier directement dans CLAUDE.md à la racine.
```

### 3.4 [HUMAIN] Test à froid

Ouvrez une nouvelle session Claude Code et tapez : « Comment tu vas ranger les choses qu'on produit ensemble ? »

Si la réponse est cohérente avec vos règles : ✅
Si elle est vague ou incorrecte : retournez à l'étape 3.3 et raffinez.

---

## 4. Étape 2 : Construire `ABOUT.ME/`

Ces fichiers sont chargés à **chaque session**. Ils définissent qui vous êtes en tant que personne et en tant qu'entreprise. Restez court : `<2000 tokens` pour `about-me.md`, `<1000 tokens` pour `my-company.md`.

### 4.1 Fichier `about-me.md` (qui vous êtes)

#### PROMPT 1 : Cadrage

```
Tu es une IA chargée de m'aider à créer le fichier about-me.md
de mon workspace.

Ce fichier sera lu par toi à chaque session.
Il doit te dire qui je suis EN TANT QUE PERSONNE :
- Mon rôle
- Ma façon de travailler
- Mes standards de qualité
- Mes préférences de collaboration

CE FICHIER N'EST PAS :
- Un CV
- Une bio LinkedIn
- Une description marketing

Il décrit la personne réelle, pour que tu travailles
avec moi comme un collègue le ferait.

À ce stade, tu ne dois PAS écrire le fichier.
Tu dois confirmer que tu as compris l'objectif,
et me demander quels documents existants peuvent t'aider
(bio existante, posts LinkedIn perso, transcripts d'interview,
profil personnel, etc.).
```

#### PROMPT 2 : Interview (20 questions)

```
Tu es une IA intervieweuse.
Tu vas m'interviewer pour produire la matière
du fichier about-me.md.

RÈGLES :
- Une question à la fois
- Toujours demander un exemple concret quand je reste vague
- Ne jamais reformuler "joliment" mes réponses
- Privilégier ce qui revient souvent

AXES D'INTERVIEW (DANS L'ORDRE) :

### AXE 1 : IDENTITÉ (3 questions)
- Quel est ton rôle / métier principal ?
- Comment tu te présenterais en 2 phrases à un nouveau collègue ?
- Quels sont les 3 mots qui te décrivent au travail ?

### AXE 2 : FAÇON DE TRAVAILLER (4 questions)
- À quel moment de la journée tu es le plus efficace ?
- Tu travailles plutôt seul ou en collaboration ?
- Comment tu prends tes décisions (instinct, data, consultation) ?
- Quel est ton rythme idéal (sprint intense / régularité) ?

### AXE 3 : CE QUI EST BON POUR TOI (4 questions)
- Quel type de livrable te rend fier ?
- Qu'est-ce qu'un "bon travail" pour toi ?
- Quels sont tes standards non négociables ?
- Quel ton tu préfères dans les échanges ?

### AXE 4 : CE QUE TU DÉTESTES (4 questions)
- Quel type de tâche tu refuses systématiquement ?
- Quel ton ou style te fait fuir ?
- Quels comportements d'IA te frustrent (verbosité ? sycophancy ?
  hedging ? autre) ?
- Qu'est-ce qui te fait perdre confiance en un collaborateur ?

### AXE 5 : TES RÈGLES (3 questions)
- Quelles sont tes 3 règles de vie professionnelles ?
- Y a-t-il des sujets ou actions qui requièrent ton accord explicite ?
- Comment tu veux qu'on te corrige quand tu te trompes ?

### AXE 6 : TES CONVICTIONS (2 questions)
- Quelle est une opinion forte que tu défends sur ton métier ?
- Qu'est-ce que tu refuses de croire malgré la pression ambiante ?

PUSH BACK :
Si je dis "ça dépend" → de quoi exactement ?
Si je dis "en général" → un exemple précis ?
Si je dis "j'aime bien" → qu'est-ce que ça produit concrètement ?

Commence par la question 1 de l'Axe 1. Attends ma réponse.
Continue axe par axe.
```

#### PROMPT 3 : Synthèse

```
Tu vas maintenant produire le fichier FINAL : about-me.md

À partir de :
- Toutes mes réponses à l'interview
- Les documents partagés
- Les patterns récurrents

CONTRAINTES :
- Première personne ("Je travaille mieux le matin...")
- 1 à 2 pages maximum (~1500 mots max)
- Ton factuel, sans embellissement marketing
- Pas de questions-réponses brutes : extrais les patterns

STRUCTURE OBLIGATOIRE :

# About Me

## Identité
[2-3 phrases : qui je suis, mon rôle]

## Comment je travaille
[Rythme, énergie, prises de décision, style de collaboration]

## Mes standards
[Ce qui définit un bon livrable pour moi]

## Ce que j'évite / Ce qui me frustre
[Comportements, tons, types de tâches à éviter]

## Mes règles non négociables
[3-5 règles claires, formulées comme des consignes]

## Mes convictions
[2-3 opinions fortes que j'assume]

---

Produis uniquement le contenu du fichier.
Écris-le directement dans ABOUT.ME/about-me.md.
```

### 4.2 Fichier `my-company.md` (votre business actuel)

#### PROMPT 1 : Cadrage

```
Tu vas m'aider à créer my-company.md.

Ce fichier sera lu à chaque session.
Il doit te donner le SNAPSHOT BUSINESS ACTUEL :
- Mes objectifs en cours
- Mon focus du moment
- Ce à quoi je dis non en ce moment
- Les décisions ouvertes

Ce n'est pas une description statique de l'entreprise.
C'est un état des lieux qui évolue tous les 1-3 mois.

Confirme que tu as compris, et demande-moi quels documents
peuvent t'aider (OKR, plan trimestriel, notes stratégie, etc.).
```

#### PROMPT 2 : Interview (8 questions)

```
Interview-moi sur mon business actuel.

AXE 1 : OFFRE ACTIVE
- Qu'est-ce que je vends activement en ce moment ?
- Qui sont mes clients actuels (1-2 phrases) ?

AXE 2 : OBJECTIFS
- Quel est mon objectif business prioritaire pour les 90 prochains jours ?
- Comment je le mesure (chiffre, signal qualitatif) ?

AXE 3 : FOCUS
- Sur quoi je passe 80% de mon temps cette semaine ?
- Quelle est la plus grosse décision ouverte que je dois trancher ?

AXE 4 : ANTI-OBJECTIFS
- À quoi je dis NON en ce moment (offres, projets, opportunités) ?
- Quel signal me ferait pivoter ce trimestre ?

Une question à la fois. Push back si je reste vague.
```

#### PROMPT 3 : Synthèse

```
Produis le fichier final : my-company.md

CONTRAINTES :
- Première personne
- ~800 mots max
- Date du jour mentionnée en haut (snapshot daté)

STRUCTURE :

# My Company : Snapshot YYYY-MM-DD

## Offre active
[Ce que je vends, à qui]

## Objectif 90 jours
[Le but, la mesure]

## Focus actuel
[Sur quoi je passe mon temps]

## Décisions ouvertes
[Ce que je dois trancher]

## Anti-objectifs
[Ce à quoi je dis non, et pourquoi]

---

À RAPPELER À L'UTILISATEUR : ce fichier est à mettre à jour
tous les 1-3 mois. Mets-le en favori dans ton éditeur.

Écris dans ABOUT.ME/my-company.md.
```

### 4.3 Fichier `anti-ai-voice.md` (optionnel mais recommandé)

Ce fichier contient les règles d'écriture pour ne jamais sonner IA. Indispensable si vous produisez du contenu publié (LinkedIn, newsletter, copy, mails).

#### PROMPT : Génération directe (pas besoin d'interview)

```
Crée le fichier ABOUT.ME/anti-ai-voice.md.

Il doit lister les règles d'écriture pour produire du contenu
qui ne sonne PAS IA, à appliquer sur tout livrable écrit publié
(LinkedIn, newsletter, copy, mails).

Inclure :

# Anti-AI Voice : Règles d'écriture

## Mots et tournures BANNIS
- "Plonger dans", "explorer", "naviguer dans"
- "Il est important de noter que..."
- "Dans le paysage actuel de..."
- "Libérez le potentiel de..."
- "Démêlez les complexités de..."
- "Élevez votre [n'importe quoi]"
- Tirets cadratin (-) en milieu de phrase pour faire dramatique
- Emojis décoratifs en début de paragraphe
- Bullet points qui commencent tous par un verbe à l'infinitif

## Structures BANNIES
- "Non seulement X, mais aussi Y"
- "X n'est pas juste Y, c'est Z"
- "Voici quelques [pluriel] à considérer..."
- Listes à 3 items parfaitement parallèles
- Conclusion qui résume ce qu'on vient de lire

## Ce qu'il FAUT faire
- Phrases courtes
- Casser le rythme volontairement
- Une idée par paragraphe
- Verbes concrets, pas abstraits
- Anecdotes personnelles plutôt que généralités
- Friction assumée : un avis, pas un consensus
- Finir net, pas avec "voilà" ou "j'espère que ça vous a plu"

## Test ultime
Si tu peux retirer une phrase sans rien perdre,
c'est qu'elle ne devait pas être là.

---

L'utilisateur peut compléter ce fichier au fil du temps
avec ses propres règles spécifiques.
```

---

## 5. Étape 3 : Construire `Contexte/` (les 7 fichiers stratégiques)

Ces fichiers ne sont pas chargés à chaque session : Claude les charge **à la demande**, selon la tâche. Le routage se fait via `CLAUDE.md`.

**Pattern universel pour CHAQUE fichier :**
1. **Prompt 1 : Cadrage** : Claude comprend l'objectif et demande les documents existants
2. **Prompt 2 : Interview** : Claude pose des questions précises, push-back obligatoire
3. **Prompt 3 : Synthèse** : Claude produit le fichier final

**Règle critique :** Faites les 3 prompts dans la **même conversation**. La continuité du contexte est essentielle.

**Conseil pratique :** Pour les interviews longues (axes multiples), faites-les en mode vocal pendant une marche de 30 minutes. Vous parlez plus naturellement que vous écrivez.

---

### 5.1 Fichier `Constitution-Identity.md`

**Rôle :** Boussole morale et décisionnelle. Vos valeurs vécues (par les arbitrages, pas les déclarations), vos lignes rouges, ce qui doit faire refuser une action à l'IA. Prioritaire sur tous les autres fichiers.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Constitution-Identity.md

Ce fichier fera partie d'une base de connaissance utilisée
pour transformer une IA en assistant personnel et business
hautement spécifique pour un dirigeant.

---

## OBJECTIF DU FICHIER

Le fichier Constitution-Identity.md a pour but de décrire
le socle identitaire réel du dirigeant.

Il doit permettre à une IA de comprendre :
- qui est cette personne dans ses décisions réelles
- quelles valeurs priment quand des principes entrent en conflit
- quelles sont ses lignes rouges non négociables
- dans quels cas l'IA doit refuser de proposer une action

Ce fichier sert de **boussole morale et décisionnelle**.
Il est prioritaire sur tous les autres fichiers.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une biographie
- un manifeste marketing
- un texte inspirationnel
- une présentation publique
- un résumé LinkedIn

Il ne cherche pas à être flatteur, cohérent ou inspirant.
Il cherche à être **vrai et exploitable**.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade précis du processus, ton rôle est uniquement de :

- comprendre la finalité exacte du fichier
- intégrer les contraintes de qualité attendues
- te préparer à extraire la réalité vécue plutôt que des intentions idéales

Tu ne dois PAS :
- poser de questions encore
- produire de contenu
- interpréter ou anticiper les réponses

Les questions et l'extraction du contenu viendront à l'étape suivante.

---

## CONTRAINTES GLOBALES À GARDER EN MÉMOIRE

Pour tout ce qui concerne ce fichier :

- la réalité prime sur la cohérence
- les arbitrages priment sur les déclarations
- les exemples concrets priment sur les principes abstraits
- ce qui a un coût est plus important que ce qui "sonne bien"

---

Confirme que tu as compris :
- l'objectif du fichier
- ton rôle à ce stade
- les limites à respecter

Attends ensuite l'instruction suivante.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée dans l'extraction
de valeurs réelles, de principes vécus et de règles implicites.

Tu dois aider à construire le contenu du fichier :
Constitution-Identity.md

Tu n'écris PAS le fichier.
Tu extrais la matière première nécessaire à sa rédaction.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- des valeurs démontrées par des choix réels
- des arbitrages quand deux principes entrent en conflit
- des lignes rouges non négociables
- des situations où ces valeurs ont eu un coût

Tu ne cherches PAS :
- des déclarations idéales
- des principes abstraits
- une cohérence artificielle

---

## RÈGLES DE CONDUITE

- Pose UNE question à la fois
- Exige toujours un exemple concret
- Reviens sur une réponse si elle est vague
- Accepte les contradictions si elles existent
- Privilégie ce qui a été difficile ou inconfortable

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : ARBITRAGES RÉELS
- Raconte-moi une situation où tu as dû choisir entre deux choses importantes.
- Qu'as-tu sacrifié ?
- Pourquoi ce choix-là, précisément ?

### AXE 2 : LIMITES & REFUS
- Parle-moi d'un moment où tu as dit non à quelque chose
  de rentable ou valorisant.
- Qu'est-ce qui t'a fait refuser ?
- Qu'est-ce que cela révèle sur tes limites ?

### AXE 3 : TRANSGRESSIONS
- Quand as-tu agi contre ce que tu pensais être une de tes valeurs ?
- Quelles conséquences concrètes cela a-t-il eues ?
- Qu'as-tu appris (ou pas) de cette situation ?

### AXE 4 : LIGNES ROUGES
- Dans quelles situations refuses-tu systématiquement d'avancer ?
- Qu'est-ce qui déclenche un arrêt immédiat
  (client, projet, comportement) ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds par :
- "C'est important pour moi" → Demande : *important comment ?
  pour quelles décisions ?*
- "Je crois que…" → Demande : *dans quelle situation concrète ?*
- "Je suis quelqu'un qui…" → Demande : *quand exactement ?*

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue étape par étape
- Ne saute aucun axe

Quand tous les axes sont couverts, attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir de :
- toutes mes réponses à l'interview précédente
- les exemples concrets fournis
- les arbitrages et contradictions exprimés

tu dois produire le fichier FINAL :
Constitution-Identity.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- comprendre comment je tranche réellement
- refuser de proposer des actions contraires à mes principes
- hiérarchiser les décisions selon mes valeurs réelles

Il servira de référence prioritaire
dans toutes les décisions futures.

---

## CONTRAINTES STRICTES

- Première personne ("je")
- 1 à 2 pages maximum
- Langage simple, direct, non héroïque
- Aucun jargon
- Aucune phrase générique
- Aucune optimisation marketing ou inspirationnelle

---

## STRUCTURE OBLIGATOIRE

### PRINCIPES FONDAMENTAUX
- Valeurs exprimées sous forme d'arbitrages
- Chaque principe doit impliquer un renoncement réel

### NON-NÉGOCIABLES
- Lignes rouges explicites
- Situations où l'IA doit refuser d'aider

### TENSIONS & PRIORITÉS
- Valeurs qui peuvent entrer en conflit
- Règle utilisée pour trancher dans ces cas-là

### NOTES POUR L'IA
- Ce que tu dois toujours prioriser
- Ce que tu ne dois jamais supposer
- Ce que tu dois challenger si cela apparaît

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Je valorise l'intégrité, l'excellence et l'humain."

BON :
> "Quand rapidité et qualité entrent en conflit, je choisis la qualité,
> même si cela me coûte du temps ou de l'argent. Je préfère perdre
> une opportunité que livrer quelque chose dont je ne suis pas fier."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.2 Fichier `Life-and-Work-Reality.md`

**Rôle :** Garde-fou opérationnel. Empêche l'IA de proposer des plans incompatibles avec votre vie réelle (temps disponible, énergie, modèle économique, contraintes).

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Life-and-Work-Reality.md

Ce fichier fait partie d'une base de connaissance
dont l'objectif est de transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Life-and-Work-Reality.md doit décrire
la réalité concrète de la vie et du travail du dirigeant,
telle qu'elle existe aujourd'hui.

Il doit permettre à une IA de comprendre :
- comment ses journées se déroulent réellement
- comment il gagne de l'argent aujourd'hui
- ce qui fonctionne vs ce qui dysfonctionne
- ce qui lui donne de l'énergie vs ce qui l'épuise
- quelles sont ses contraintes réelles (temps, charge, contexte)

Ce fichier sert de **garde-fou opérationnel** :
il empêche l'IA de proposer des actions ou des plans
qui seraient incompatibles avec la réalité humaine et business.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une organisation idéale
- une projection future
- une description "optimisée"
- une fiche de poste
- un texte motivationnel

Il ne cherche pas à montrer ce qui devrait être,
mais ce qui est réellement vécu.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- intégrer les contraintes de qualité attendues
- te préparer à extraire des faits concrets, pas des intentions

Tu ne dois PAS :
- poser de questions
- produire du contenu
- interpréter ou corriger la réalité

Les questions viendront à l'étape suivante.

---

## PRINCIPES À GARDER EN MÉMOIRE

Pour tout ce fichier :
- le réel prime sur l'idéal
- les faits priment sur les ressentis vagues
- les contraintes priment sur les possibilités
- ce qui est répété est plus important que ce qui est exceptionnel

---

Confirme que tu as compris :
- l'objectif du fichier
- ton rôle à ce stade
- les limites à respecter

Attends ensuite l'instruction suivante.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction de la réalité opérationnelle
de dirigeants solo ou de petites entreprises.

Tu dois aider à construire la matière première
du fichier Life-and-Work-Reality.md.

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire les faits.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est d'identifier :
- comment les journées se passent réellement
- comment le travail est organisé dans les faits
- où se crée la valeur aujourd'hui
- où se perd l'énergie, le temps ou la clarté
- quelles sont les contraintes structurelles actuelles

Tu ne cherches PAS :
- une version idéalisée
- une organisation cible
- des optimisations prématurées

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander des exemples concrets
- Challenger les réponses vagues ou idéalisées
- Revenir sur une réponse si elle manque de précision
- Accepter les incohérences (elles sont informatives)

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : JOURNÉES RÉELLES
- À quoi ressemble une journée typique, du début à la fin ?
- Quelles tâches occupent le plus de temps ?
- Qu'est-ce qui est souvent repoussé ?

### AXE 2 : TRAVAIL & BUSINESS
- Comment gagnes-tu de l'argent aujourd'hui, concrètement ?
- Quelles activités génèrent réellement du revenu ?
- Quelles activités prennent du temps sans en générer ?

### AXE 3 : ÉNERGIE & FATIGUE
- Quelles tâches te donnent de l'énergie ?
- Quelles tâches t'épuisent systématiquement ?
- À quels moments de la journée es-tu le plus / le moins efficace ?

### AXE 4 : CE QUI FONCTIONNE / CE QUI BLOQUE
- Qu'est-ce qui fonctionne plutôt bien aujourd'hui ?
- Qu'est-ce qui est clairement cassé ou frustrant ?
- Quels problèmes reviennent en boucle ?

### AXE 5 : CONTRAINTES ACTUELLES
- Quelles sont tes contraintes réelles en ce moment ?
  (temps, charge mentale, finances, contexte perso)
- Qu'est-ce qui limite le plus ta capacité d'action aujourd'hui ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "Ça dépend" → *Dépend de quoi exactement ?*
- "En général" → *Donne-moi un exemple précis.*
- "Je devrais" → *Que fais-tu réellement aujourd'hui ?*
- "Je manque de temps" → *Où passe ton temps concrètement ?*

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des exemples concrets fournis
- des contraintes et répétitions identifiées

tu dois produire le fichier FINAL :
Life-and-Work-Reality.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- proposer des actions compatibles avec ma réalité actuelle
- éviter les recommandations irréalistes ou inapplicables
- comprendre où se crée réellement la valeur aujourd'hui
- respecter mes limites humaines et opérationnelles

---

## CONTRAINTES STRICTES

- Première personne ("je")
- 1 à 2 pages maximum
- Langage simple, factuel, non idéalisé
- Aucune projection future
- Aucune recommandation ou optimisation
- Aucune phrase générique

---

## STRUCTURE RECOMMANDÉE

### RÉALITÉ QUOTIDIENNE
- Comment mes journées se déroulent réellement
- Où passe mon temps aujourd'hui

### TRAVAIL & BUSINESS ACTUEL
- Comment je gagne de l'argent
- Activités centrales vs périphériques

### ÉNERGIE & FATIGUE
- Ce qui me donne de l'énergie
- Ce qui m'épuise
- Moments de performance / baisse

### CE QUI FONCTIONNE / CE QUI BLOQUE
- Points solides
- Frictions récurrentes

### CONTRAINTES À RESPECTER
- Limites de temps, d'énergie, de contexte
- Ce que l'IA ne doit PAS ignorer

### NOTES POUR L'IA
- Ce que tu dois toujours garder en tête
- Ce que tu ne dois jamais proposer

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Je manque de temps et j'essaie de mieux m'organiser."

BON :
> "Mes matinées sont souvent fragmentées par des messages clients.
> J'ai 2 à 3 heures de vraie concentration maximum par jour,
> généralement en fin de matinée. Toute recommandation doit tenir
> compte de cette contrainte."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.3 Fichier `Goals-and-Direction.md`

**Rôle :** Boussole directionnelle. Oriente toutes les recommandations de l'IA vers vos vrais objectifs (résultats, pas activités), avec échéances et arbitrages explicites.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Goals-and-Direction.md

Ce fichier fait partie d'une base de connaissance
utilisée pour transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Goals-and-Direction.md doit décrire
la direction claire, concrète et priorisée
que le dirigeant souhaite suivre
sur une période donnée (année en cours + court terme).

Il doit permettre à une IA de comprendre :
- ce que le dirigeant cherche réellement à accomplir
- quels résultats concrets comptent vraiment
- quelles priorités priment sur les autres
- à quel horizon temporel chaque objectif s'inscrit

Ce fichier sert de **boussole directionnelle** :
il oriente toutes les recommandations,
suggestions et arbitrages proposés par l'IA.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une vision long terme abstraite
- une liste de rêves ou d'intentions
- un texte motivationnel
- un plan stratégique détaillé

Il ne cherche pas à inspirer.
Il cherche à **orienter l'action**.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- intégrer les contraintes de qualité attendues
- te préparer à extraire des objectifs concrets, mesurables et datés

Tu ne dois PAS :
- poser de questions
- produire de contenu
- reformuler ou anticiper des objectifs

Les questions viendront à l'étape suivante.

---

## PRINCIPES À GARDER EN MÉMOIRE

Pour tout ce fichier :
- le concret prime sur l'ambition
- les chiffres priment sur les formulations vagues
- les priorités priment sur l'exhaustivité
- ce qui est daté est plus important que ce qui est souhaité

---

Confirme que tu as compris :
- l'objectif du fichier
- ton rôle à ce stade
- les limites à respecter

Attends ensuite l'instruction suivante.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction d'objectifs concrets,
priorisés et mesurables
chez des dirigeants solo ou de petites entreprises.

Tu dois aider à constituer la matière première
du fichier Goals-and-Direction.md.

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire les objectifs réels.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- des objectifs précis (résultats, pas activités)
- des échéances claires
- des priorités assumées
- des arbitrages explicites entre objectifs concurrents

Tu ne cherches PAS :
- des intentions vagues
- des objectifs "inspirants"
- une liste exhaustive de tout ce qui serait bien à faire

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander un chiffre ou un critère mesurable
- Toujours demander une échéance
- Challenger toute réponse floue ou non priorisée
- Refuser les formulations abstraites

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : OBJECTIF PRINCIPAL
- Quel est l'objectif n°1 que tu veux absolument atteindre cette année ?
- Comment sauras-tu que cet objectif est atteint ?
  (chiffre, résultat observable)
- À quelle date précise ?

### AXE 2 : OBJECTIFS SECONDAIRES
- Quels sont les 1 à 2 autres objectifs importants, mais secondaires ?
- Comment se mesurent-ils ?
- À quel horizon s'inscrivent-ils ?

### AXE 3 : PRIORISATION & ARBITRAGES
- Si tu ne pouvais en atteindre qu'un seul, lequel choisirais-tu ?
- Quels objectifs passent volontairement au second plan ?
- Qu'es-tu prêt à sacrifier pour atteindre l'objectif principal ?

### AXE 4 : COURT TERME (3-6 MOIS)
- Qu'est-ce qui doit absolument avancer dans les 3 à 6 prochains mois ?
- Quels résultats concrets doivent être visibles à court terme ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "Développer le business" → *Développer comment ? Jusqu'à quel niveau ?*
- "Avoir plus de clients" → *Combien ? Quel impact financier ?*
- "Être plus visible" → *Sur quoi exactement ? Avec quel indicateur ?*
- "Améliorer X" → *Améliorer de combien ? D'ici quand ?*

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des chiffres, échéances et arbitrages exprimés

tu dois produire le fichier FINAL :
Goals-and-Direction.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- orienter ses recommandations vers mes vrais objectifs
- prioriser ses suggestions en fonction de mes échéances
- éviter toute proposition non alignée avec ma direction actuelle

Il sert de **référence directionnelle**
pour toutes les décisions futures.

---

## CONTRAINTES STRICTES

- Première personne ("je")
- 1 à 2 pages maximum
- Langage clair, factuel, sans emphase
- Aucun storytelling
- Aucune reformulation floue
- Aucun conseil ajouté

---

## STRUCTURE OBLIGATOIRE

### OBJECTIF PRINCIPAL
- Résultat attendu
- Indicateur(s) de succès
- Échéance précise

### OBJECTIFS SECONDAIRES
- Résultats attendus
- Indicateurs
- Échéances

### PRIORITÉS & ARBITRAGES
- Ce qui prime
- Ce qui est volontairement mis de côté

### FOCUS COURT TERME
- Résultats attendus à 3-6 mois
- Ce que l'IA doit prioriser maintenant

### NOTES POUR L'IA
- Ce que tu dois toujours garder en tête
- Ce que tu ne dois jamais prioriser

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Je veux développer mon activité cette année."

BON :
> "Mon objectif principal est d'atteindre 8 000 € de revenu mensuel
> récurrent d'ici le 30 septembre. Toute recommandation doit prioriser
> les actions qui contribuent directement à cet objectif."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.4 Fichier `Offer-Positioning.md`

**Rôle :** Référence de positionnement. Empêche l'IA de proposer des messages qui diluent l'offre, mélangent les ciblages ou contredisent le périmètre actuel.

> Note : la version originale de ces 3 prompts (page Notion "Votre Cerveau IA") avait des sections coupées à l'export. Les versions ci-dessous sont reconstituées à l'identique du pattern strict utilisé dans les autres fichiers de la même série.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Offer-Positioning.md

Ce fichier fait partie d'une base de connaissance
destinée à transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Offer-Positioning.md doit décrire
le positionnement réel de l'offre du dirigeant.

Il doit permettre à une IA de comprendre :
- ce qui est vendu aujourd'hui (format, prix, durée)
- à qui c'est vendu réellement
- quel problème principal cette offre résout
- ce qui différencie cette offre des alternatives
- ce qui est explicitement exclu (clients, demandes, situations)

Ce fichier sert de **référence de positionnement** :
il empêche l'IA de proposer des messages qui diluent l'offre,
mélangent les ciblages ou contredisent le périmètre actuel.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une vision d'offre future
- un repositionnement souhaité
- une page de vente
- un pitch commercial

Il décrit le positionnement **tel qu'il est vécu, formulé et vendu aujourd'hui**.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- intégrer les frontières du positionnement
- identifier les sources existantes
  qui permettent d'observer ce positionnement réel

Tu ne dois PAS :
- poser de questions métier
- produire du contenu
- reformuler ou améliorer l'offre

Les questions viendront à l'étape suivante.

---

## DOCUMENTATION EXISTANTE À PRENDRE EN COMPTE (IMPORTANT)

Avant toute interview, tu dois recommander
les **documents existants les plus utiles**
à analyser pour comprendre le positionnement réel.

Tu dois être sélectif (2 à 4 maximum) et expliquer pourquoi.

Selon le contexte, propose en priorité parmi :

- Pages de vente ou landing pages existantes
- Propositions commerciales envoyées
- Offres présentes sur le site ou Notion
- Devis ou contrats types
- Emails ou messages de closing
- Retranscriptions d'appels de vente
- Messages de refus envoyés à des prospects
- Feedbacks clients (positifs ou négatifs)

Pour chaque type de document recommandé,
explique brièvement ce que cela permet d'observer
(cible réelle, promesse implicite, exclusions, différenciation).

---

## INSTRUCTION AVANT LA SUITE

1. Confirme que tu as compris :
   - l'objectif du fichier
   - ton rôle à ce stade
   - les limites à respecter
2. Propose ensuite les documents existants
   à analyser avant l'interview

Attends que les documents soient fournis
ou validés avant de passer au Prompt 2.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction du positionnement réel d'une offre
chez des dirigeants solo ou de petites entreprises.

Tu dois constituer la matière première
du fichier Offer-Positioning.md
en t'appuyant sur :
- mes réponses
- les documents analysés (le cas échéant)

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire le réel.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- ce qui est vraiment vendu aujourd'hui
- qui achète réellement cette offre
- le problème dominant résolu
- les éléments de différenciation observés
- les exclusions et refus assumés

Tu ne cherches PAS :
- une offre idéale
- un positionnement amélioré
- une cible élargie

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander un exemple concret
- Challenger toute réponse vague
- Refuser les réponses "tout le monde"
- Pointer les incohérences entre discours et documents

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : OFFRE CONCRÈTE
- Qu'est-ce que tu vends aujourd'hui, concrètement ?
- Sous quel format (service, produit, accompagnement, abonnement) ?
- À quel prix ou dans quelle fourchette ?

### AXE 2 : CIBLE RÉELLE
- Qui achète réellement cette offre aujourd'hui ?
- Dans quelle situation se trouvent-ils au moment de l'achat ?
- Qui n'achète jamais, même s'il pourrait en théorie ?

### AXE 3 : PROBLÈME PRINCIPAL
- Quel est le problème n°1 que cette offre résout ?
- Comment ce problème se manifeste concrètement chez le client ?
- Que se passe-t-il si ce problème n'est pas résolu ?

### AXE 4 : DIFFÉRENCIATION
- Pourquoi les clients te choisissent toi plutôt qu'une alternative ?
- Qu'est-ce qui fait dire "c'est pour toi" ?
- Quelles alternatives envisagent-ils avant de te choisir ?

### AXE 5 : FRONTIÈRES & EXCLUSIONS
- Qu'est-ce que tu refuses de vendre ?
- À quels types de clients dis-tu non ?
- Dans quels cas cette offre n'est PAS adaptée ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "J'aide tout le monde" → Qui exactement a déjà payé ?
- "Ça dépend" → Donne-moi un cas précis.
- "Je m'adapte" → Jusqu'où, et où est la limite ?
- "C'est du sur-mesure" → Sur-mesure sur quoi exactement ?

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des exemples concrets fournis
- des documents analysés
- des patterns récurrents identifiés

tu dois produire le fichier FINAL :
Offer-Positioning.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- proposer des messages alignés avec mon offre actuelle
- éviter toute dilution ou élargissement non assumé
- respecter mes exclusions et refus
- adapter le ton à la cible réelle

Il sert de **référence de positionnement**
pour toute création de message ou contenu commercial.

---

## CONTRAINTES STRICTES

- Première personne ("je")
- 1 à 2 pages maximum
- Langage simple, factuel
- Aucune reformulation marketing "améliorée"
- Aucun conseil ajouté
- Aucun positionnement projeté

---

## STRUCTURE OBLIGATOIRE

### OFFRE
- Format et fourchette de prix

### CIBLE
- Profil des clients réels
- Situations typiques d'achat

### PROBLÈME RÉSOLU
- Problème principal
- Conséquences si non résolu

### DIFFÉRENCIATION
- Pourquoi on me choisit
- Alternatives courantes

### EXCLUSIONS & LIMITES
- Ce que je ne vends pas
- Clients ou cas refusés

### NOTES POUR L'IA
- Ce que tu peux proposer sans risque
- Ce que tu dois éviter
- Ce que tu dois clarifier avant d'agir

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "J'aide les entrepreneurs à mieux se positionner."

BON :
> "Je vends un accompagnement stratégique de 3 mois à des dirigeants
> solo en phase de stabilisation, facturé entre 3 000 et 5 000 €.
> Je refuse les projets de repositionnement pour des entreprises
> de plus de 20 personnes."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.5 Fichier `Clients-Problems-and-Messages.md` ⭐ (le plus stratégique)

**Rôle :** Référence marché et langage. Empêche l'IA de produire des messages génériques, théoriques ou déconnectés du terrain. C'est LE fichier qui transforme la qualité de tout votre contenu marketing.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Clients-Problems-and-Messages.md

Ce fichier fait partie d'une base de connaissance
destinée à transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Clients-Problems-and-Messages.md doit décrire
la réalité du marché telle qu'elle est vécue par les clients.

Il doit permettre à une IA de comprendre :
- qui sont les clients réels
- quels problèmes ils cherchent réellement à résoudre
- comment ces problèmes se manifestent concrètement
- quels mots ils utilisent pour en parler
- quels messages déclenchent l'intérêt ou l'achat
- quels messages échouent ou créent de la méfiance

Ce fichier sert de **référence marché et langage** :
il empêche l'IA de produire des messages génériques,
théoriques ou déconnectés du terrain.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une étude de marché académique
- une persona marketing idéalisée
- une reformulation marketing optimisée
- une stratégie de communication

Il décrit le marché **tel qu'il parle et agit aujourd'hui**.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- identifier les sources existantes
  qui révèlent les vrais problèmes et le vrai langage client

Tu ne dois PAS :
- poser de questions métier
- produire de contenu
- reformuler ou améliorer les messages

Les questions viendront à l'étape suivante.

---

## DOCUMENTATION EXISTANTE À PRENDRE EN COMPTE (CRITIQUE)

Avant toute interview, tu dois recommander
les **documents existants les plus révélateurs**
du marché réel.

Tu dois être sélectif (2 à 4 maximum) et justifier chaque choix.

Propose en priorité parmi :

- Retranscriptions d'appels de vente (discovery, closing)
- Emails ou messages entrants de prospects
- Messages de refus ou d'objections clients
- Feedbacks clients (positifs / négatifs)
- Commentaires LinkedIn, Slack, Discord, WhatsApp
- Notes prises juste après des rendez-vous
- Messages vocaux ou écrits envoyés par des clients

Pour chaque type de document recommandé :
- explique ce que cela permet d'observer
  (problème réel, mots utilisés, objections, déclencheurs, peurs)

---

## INSTRUCTION AVANT LA SUITE

1. Confirme que tu as compris :
   - l'objectif du fichier
   - ton rôle à ce stade
   - les limites à respecter
2. Propose ensuite les documents existants
   à analyser avant l'interview

Attends que les documents soient fournis
ou validés avant de passer au Prompt 2.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction de la réalité client
(problèmes, langage, déclencheurs, objections)
chez des dirigeants solo ou de petites entreprises.

Tu dois constituer la matière première
du fichier Clients-Problems-and-Messages.md
en t'appuyant sur :
- mes réponses
- les documents analysés (le cas échéant)

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire le réel.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- les problèmes réellement vécus par les clients
- leur manière spontanée d'en parler
- leurs peurs et blocages
- leurs objections récurrentes
- les messages qui déclenchent une réaction
- les messages qui échouent

Tu ne cherches PAS :
- des suppositions
- des personas idéaux
- des messages "qui devraient marcher"

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander des exemples concrets ou verbatim
- Challenger les réponses générales
- Pointer les écarts entre discours et documents
- Privilégier ce qui revient souvent

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : CLIENTS RÉELS
- Qui sont les clients qui achètent réellement aujourd'hui ?
- Dans quelle situation viennent-ils te voir ?
- Qui ne devient jamais client, et pourquoi ?

### AXE 2 : PROBLÈMES RÉELS
- Quel est le problème n°1 qu'ils cherchent à résoudre ?
- Comment ce problème se manifeste concrètement ?
- Qu'est-ce qui rend ce problème urgent ou douloureux ?

### AXE 3 : LANGAGE CLIENT
- Quelles phrases utilisent-ils spontanément ?
- Quels mots ou expressions reviennent souvent ?
- Quels termes évitent-ils ou rejettent-ils ?

### AXE 4 : OBJECTIONS & PEURS
- Quelles objections entends-tu le plus souvent ?
- Qu'est-ce qui les freine avant d'acheter ?
- Qu'ont-ils peur de perdre ou de regretter ?

### AXE 5 : DÉCLENCHEURS & MESSAGES
- Qu'est-ce qui déclenche vraiment l'intérêt ou l'achat ?
- Quels messages ont clairement fonctionné ?
- Quels messages ont échoué ou créé de la méfiance ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "Ils veulent X" → Qui exactement l'a dit ? Dans quel contexte ?
- "En général" → Donne-moi un exemple précis.
- "Ils cherchent…" → Avec quels mots exacts ?
- "Ça dépend" → Dépend de quoi concrètement ?

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des verbatim clients
- des documents analysés
- des patterns récurrents identifiés

tu dois produire le fichier FINAL :

Clients-Problems-and-Messages.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- comprendre la réalité du marché
- utiliser le langage exact des clients
- produire des messages crédibles et pertinents
- éviter tout discours générique ou déconnecté

Il sert de **référence marché**
pour toute création de contenu, message ou recommandation.

---

## CONTRAINTES STRICTES

- Première personne ("mes clients…")
- 1 à 2 pages maximum
- Langage simple, factuel
- Aucune reformulation marketing "améliorée"
- Aucun conseil ajouté
- Aucun persona fictif

---

## STRUCTURE OBLIGATOIRE

### CLIENTS RÉELS
- Profils qui achètent
- Situations typiques

### PROBLÈMES PRINCIPAUX
- Problèmes dominants
- Manifestations concrètes

### LANGAGE & VERBATIM
- Phrases réelles utilisées
- Mots récurrents
- Termes rejetés

### OBJECTIONS & PEURS
- Objections fréquentes
- Peurs implicites ou explicites

### MESSAGES QUI FONCTIONNENT
- Messages ou angles efficaces
- Pourquoi ils fonctionnent

### MESSAGES QUI ÉCHOUENT
- Messages rejetés
- Signaux de méfiance

### NOTES POUR L'IA
- Ce que tu peux utiliser sans risque
- Ce que tu dois éviter
- Ce que tu dois toujours vérifier

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Ils veulent gagner du temps."

BON :
> "Ils disent souvent : « Je passe mes journées à courir
> sans jamais avancer ». Les messages qui parlent
> d'optimisation pure sont rejetés.
> Ceux qui parlent de clarté et de priorités
> déclenchent l'intérêt."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.6 Fichier `Expertise-Standards-and-Landmines.md`

**Rôle :** Référence de qualité et de maturité. Empêche l'IA de proposer des solutions naïves, génériques ou déjà invalidées par votre expérience.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Expertise-Standards-and-Landmines.md

Ce fichier fait partie d'une base de connaissance
destinée à transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Expertise-Standards-and-Landmines.md doit décrire
le niveau réel d'expertise du dirigeant.

Il doit permettre à une IA de comprendre :
- comment il résout les problèmes dans son domaine
- ce qu'il considère comme du "travail bien fait"
- ce qu'il fait toujours ou jamais
- où et pourquoi les choses échouent habituellement
- quelles erreurs ont déjà été commises (et à ne plus répéter)

Ce fichier sert de **référence de qualité et de maturité** :
il empêche l'IA de proposer des solutions naïves,
génériques ou déjà invalidées par l'expérience.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- un CV
- une liste de compétences
- une méthode théorique
- une synthèse de livres ou frameworks
- une démonstration d'expertise

Il décrit **comment le travail est réellement fait**
et **où ça casse dans la vraie vie**.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- identifier les sources existantes
  qui révèlent l'expertise réelle et les erreurs passées

Tu ne dois PAS :
- poser de questions métier
- produire de contenu
- structurer ou améliorer la méthode

Les questions viendront à l'étape suivante.

---

## DOCUMENTATION EXISTANTE À PRENDRE EN COMPTE (ESSENTIEL)

Avant toute interview, tu dois recommander
les **documents existants les plus révélateurs**
de l'expertise réelle et des landmines.

Tu dois être sélectif (2 à 4 maximum) et justifier chaque choix.

Propose en priorité parmi :

- Livrables clients (bons et mauvais)
- Méthodes internes ou checklists existantes
- Retours clients après livraison
- Retranscriptions d'appels de débrief ou d'échec
- Notes personnelles post-mission
- Messages où le dirigeant corrige, refuse ou recadre
- Exemples de travaux jugés "excellents" ou "inacceptables"

Pour chaque type de document recommandé :
- explique ce que cela permet d'observer
  (standards implicites, erreurs récurrentes, critères de qualité, pièges)

---

## INSTRUCTION AVANT LA SUITE

1. Confirme que tu as compris :
   - l'objectif du fichier
   - ton rôle à ce stade
   - les limites à respecter
2. Propose ensuite les documents existants
   à analyser avant l'interview

Attends que les documents soient fournis
ou validés avant de passer au Prompt 2.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction de l'expertise réelle,
des standards implicites
et des erreurs vécues (landmines).

Tu dois constituer la matière première
du fichier Expertise-Standards-and-Landmines.md
en t'appuyant sur :
- mes réponses
- les documents analysés (le cas échéant)

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire le réel.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- la manière réelle de résoudre les problèmes
- les critères concrets de qualité
- ce qui est systématiquement fait ou évité
- les erreurs déjà vécues
- les pièges classiques observés chez les autres

Tu ne cherches PAS :
- une méthode idéale
- un framework académique
- une expertise "présentable"

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander un exemple réel
- Challenger les réponses trop théoriques
- Pointer les écarts entre discours et documents
- Privilégier ce qui a coûté cher (temps, argent, énergie)

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : MÉTHODE RÉELLE
- Comment abordes-tu un problème concret, étape par étape ?
- Quelles étapes sont indispensables ?
- Où les gens se trompent-ils le plus souvent ?

### AXE 2 : STANDARDS DE QUALITÉ
- À partir de quand considères-tu qu'un travail est "bon" ?
- Qu'est-ce qui rend un livrable inacceptable ?
- Quelles exigences refuses-tu de baisser ?

### AXE 3 : ALWAYS / NEVER
- Qu'est-ce que tu fais toujours, sans exception ?
- Qu'est-ce que tu refuses systématiquement de faire ?
- Pourquoi ?

### AXE 4 : ERREURS VÉCUES (LANDMINES)
- Quelles erreurs as-tu déjà commises ?
- Qu'est-ce que ça t'a coûté concrètement ?
- Quels signaux aurais-tu dû voir plus tôt ?

### AXE 5 : PIÈGES COURANTS
- Quelles erreurs vois-tu les autres faire en boucle ?
- Pourquoi ces erreurs sont-elles si fréquentes ?
- Comment les éviter ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "Ça dépend" → Dépend de quoi exactement ?
- "C'est évident" → Pour qui ? À quel moment ?
- "On fait comme ça" → Pourquoi précisément ?
- "C'est une bonne pratique" → Selon quelle expérience ?

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des exemples concrets fournis
- des documents analysés
- des erreurs et patterns identifiés

tu dois produire le fichier FINAL :

Expertise-Standards-and-Landmines.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- proposer des solutions à mon niveau d'exigence
- éviter les erreurs déjà identifiées
- respecter mes standards de qualité
- reconnaître les situations à risque

Il sert de **référence de qualité**
pour toute analyse, recommandation ou production.

---

## CONTRAINTES STRICTES

- Première personne ("je")
- 1 à 2 pages maximum
- Langage direct, opérationnel
- Aucun jargon
- Aucun framework théorique
- Aucun conseil ajouté

---

## STRUCTURE OBLIGATOIRE

### MÉTHODE
- Comment je traite un problème
- Étapes indispensables

### STANDARDS
- Ce que "bon travail" signifie pour moi
- Critères non négociables

### ALWAYS / NEVER
- Ce que je fais toujours
- Ce que je refuse de faire

### LANDMINES
- Erreurs déjà vécues
- Situations à haut risque
- Signaux faibles à ne pas ignorer

### NOTES POUR L'IA
- Ce que tu dois toujours respecter
- Ce que tu dois challenger
- Ce que tu dois refuser de proposer

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Il faut bien comprendre le client avant d'agir."

BON :
> "Si le problème n'est pas reformulé avec les mots du client,
> je considère que le travail n'a pas commencé. Toute solution
> proposée avant cette étape est prématurée."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

### 5.7 Fichier `Tone-and-Voice.md`

**Rôle :** Référence stylistique absolue. Garantit que tout contenu produit par l'IA soit immédiatement utilisable sans réécriture.

#### PROMPT 1 : Cadrage

```
Tu es une intelligence artificielle chargée de participer
à la création d'un fichier de référence appelé :

Tone-and-Voice.md

Ce fichier fait partie d'une base de connaissance
destinée à transformer une IA
en assistant personnel et business ultra spécifique
pour un dirigeant (solo / petite entreprise).

---

## OBJECTIF DU FICHIER

Le fichier Tone-and-Voice.md doit décrire
la manière dont le dirigeant s'exprime réellement.

Il doit permettre à une IA de comprendre :
- le ton naturel utilisé à l'écrit et à l'oral
- le niveau de directivité, de pédagogie ou de nuance
- le vocabulaire privilégié et le vocabulaire rejeté
- ce qui "sonne juste" ou "sonne faux"
- le niveau de formalisme acceptable selon les contextes

Ce fichier sert de **référence d'expression** :
il garantit que tout contenu produit par l'IA
soit immédiatement utilisable sans réécriture.

---

## CE QUE CE FICHIER N'EST PAS

Ce fichier n'est PAS :
- une charte éditoriale marketing
- une identité de marque institutionnelle
- un exercice de style
- une tentative d'amélioration du ton

Il décrit le ton **tel qu'il est réellement utilisé**,
pas tel qu'il devrait être.

---

## RÔLE ATTENDU DE L'IA À CE STADE

À ce stade, ton rôle est uniquement de :
- comprendre précisément la finalité du fichier
- identifier les documents existants
  qui révèlent le ton réel du dirigeant

Tu ne dois PAS :
- poser de questions sur le ton
- produire de contenu
- lisser, améliorer ou corriger le style

Les questions viendront à l'étape suivante.

---

## DOCUMENTATION EXISTANTE À PRENDRE EN COMPTE (ESSENTIEL)

Avant toute interview, tu dois recommander
les **documents existants les plus révélateurs**
du ton et de la voix réels.

Tu dois être sélectif (2 à 4 maximum) et justifier chaque choix.

Propose en priorité parmi :

- Posts LinkedIn, newsletters, articles
- Emails envoyés à des clients ou partenaires
- Messages Slack / WhatsApp / SMS
- Retranscriptions d'appels ou de réunions
- Notes internes ou documents bruts
- Textes écrits "à chaud" (sans relecture marketing)

Pour chaque type de document recommandé :
- explique ce que cela permet d'observer
  (rythme, vocabulaire, structure, posture, énergie)

---

## INSTRUCTION AVANT LA SUITE

1. Confirme que tu as compris :
   - l'objectif du fichier
   - ton rôle à ce stade
   - les limites à respecter
2. Propose ensuite les documents existants
   à analyser avant l'interview

Attends que les documents soient fournis
ou validés avant de passer au Prompt 2.
```

#### PROMPT 2 : Interview

```
Tu es une IA intervieweuse spécialisée
dans l'extraction du ton, de la voix
et des préférences d'expression réelles.

Tu dois constituer la matière première
du fichier Tone-and-Voice.md
en t'appuyant sur :
- mes réponses
- les documents analysés (le cas échéant)

Tu n'écris PAS le fichier final.
Tu poses des questions pour extraire le réel.

---

## OBJECTIF DE CETTE ÉTAPE

Ton objectif est de faire émerger :
- le ton naturel (pas contrôlé)
- les préférences de style
- les limites de tolérance
- les éléments qui déclenchent un rejet immédiat
- les variations acceptables selon le contexte

Tu ne cherches PAS :
- un ton "professionnel idéal"
- une voix de marque générique
- un style lissé ou amélioré

---

## RÈGLES DE CONDUITE

- Une question à la fois
- Toujours demander un exemple précis
- Challenger les réponses abstraites
- Pointer les écarts entre intention et écrits existants
- Privilégier les réactions viscérales ("j'aime / je déteste")

---

## AXES D'INTERVIEW (À SUIVRE DANS L'ORDRE)

### AXE 1 : TON NATUREL
- Comment parles-tu quand tu es à l'aise ?
- Quel ton adoptes-tu spontanément à l'écrit ?
- Qu'est-ce qui te ressemble le plus dans les documents fournis ?

### AXE 2 : CE QUI SONNE FAUX
- Qu'est-ce qui te met immédiatement mal à l'aise dans un texte ?
- Quels mots ou tournures rejettes-tu instinctivement ?
- Quels types de contenus te donnent envie de réécrire ou supprimer ?

### AXE 3 : NIVEAU DE DIRECTIVITÉ
- Préfères-tu être direct ou nuancé ?
- Jusqu'où peux-tu être affirmatif ?
- Quand est-ce que la prudence devient de la mollesse ?

### AXE 4 : FORMALISME & CONTEXTES
- Dans quels contextes acceptes-tu plus de formalisme ?
- Où refuses-tu toute langue de bois ?
- Comment ton ton varie-t-il selon l'audience ?

### AXE 5 : BONS VS MAUVAIS EXEMPLES
- Montre-moi un texte que tu trouves juste.
- Montre-moi un texte que tu trouves faux.
- Pourquoi exactement ?

---

## PUSH BACK OBLIGATOIRE

Si je réponds :
- "Ça dépend" → Dépend de quoi précisément ?
- "J'aime quand c'est clair" → Clair comment ? Avec quel style ?
- "Je veux rester simple" → Simple pour qui ? À quel niveau ?
- "C'est trop marketing" → Qu'est-ce qui l'est exactement ?

---

## DÉROULÉ

- Commence par la PREMIÈRE question de l'Axe 1
- Attends ma réponse
- Continue axe par axe
- Ne saute aucune étape

Quand tous les axes sont couverts,
attends l'instruction suivante.
```

#### PROMPT 3 : Synthèse

```
Tu es une IA architecte de base de connaissance.

À partir :
- de toutes mes réponses à l'interview précédente
- des documents analysés
- des préférences et rejets exprimés

tu dois produire le fichier FINAL :

Tone-and-Voice.md

---

## OBJECTIF DU FICHIER FINAL

Ce fichier doit permettre à une IA de :
- écrire exactement comme je parle
- respecter mes limites stylistiques
- produire des textes utilisables sans retouche
- éviter tout ton ou vocabulaire rejeté

Il sert de **référence stylistique absolue**
pour toute production écrite ou orale.

---

## CONTRAINTES STRICTES

- Langage simple et direct
- Aucune reformulation "améliorée"
- Aucun jargon marketing
- Aucune tentative de neutralisation du ton
- Aucune justification théorique

---

## STRUCTURE OBLIGATOIRE

### TON GLOBAL
- Description du ton dominant
- Énergie générale

### STYLE D'ÉCRITURE
- Rythme
- Longueur des phrases
- Structure préférée

### VOCABULAIRE
- Mots / expressions à privilégier
- Mots / expressions à éviter

### DIRECTIVITÉ & NUANCE
- Niveau d'affirmation acceptable
- Cas où la nuance est requise

### BONS VS MAUVAIS EXEMPLES
- Exemples qui sonnent juste
- Exemples qui sonnent faux

### NOTES POUR L'IA
- Ce que tu dois toujours respecter
- Ce que tu dois éviter absolument
- Ce que tu dois me demander en cas de doute

---

## EXEMPLE DE QUALITÉ ATTENDUE

MAUVAIS :
> "Adopte un ton professionnel et engageant."

BON :
> "Je préfère un ton direct, calme et pédagogique. Les phrases courtes
> me ressemblent. Les formules enthousiastes ou trop vendeuses
> me mettent mal à l'aise."

---

Produis uniquement le contenu du fichier Markdown final.
Aucune explication hors du fichier.
```

---

## 6. Étape 4 : Construire `ressources-templates/`, `Intelligence/`, `Projects/`

Ces dossiers ne se "remplissent" pas via interview : ils s'alimentent au fil de votre travail. Ce qu'il faut faire MAINTENANT, c'est poser les fondations.

### 6.1 `ressources-templates/` (assets transversaux)

**Objectif :** Stocker tout ce qui est réutilisable par n'importe quel projet (templates de posts, listes de hooks, exemples de bons mails, frameworks éditoriaux).

#### [HUMAIN] À déposer immédiatement si vous les avez

- 1 fichier `hooks-exemples.md` avec 30-50 accroches LinkedIn / Twitter qui ont marché chez vous ou chez vos références
- 1 fichier `exemples-newsletters.md` avec 5-10 newsletters dont vous voulez reprendre la structure
- 1 fichier `templates-mails.md` avec vos mails-types (suivi, propale, suivi-propale, etc.)

Si vous n'avez rien de tout ça, créez les fichiers vides. Vous les remplirez au fil de l'eau.

### 6.2 `Intelligence/` (veille, transcriptions, daily logs)

**Sous-dossiers recommandés :**
```
Intelligence/
├── daily-logs/         ← un fichier par jour pour continuité entre sessions
├── transcripts/        ← appels clients, réunions (TL;DV, Fireflies, etc.)
├── veille/             ← articles lus, idées captées
└── concurrents/        ← recherche concurrentielle, screenshots
```

#### [CLAUDE EXECUTE] Initialisation

```
Crée la sous-structure de Intelligence/ :

Intelligence/daily-logs/.gitkeep
Intelligence/transcripts/.gitkeep
Intelligence/veille/.gitkeep
Intelligence/concurrents/.gitkeep

Crée également un fichier modèle Intelligence/daily-logs/_TEMPLATE.md
avec la structure suivante :

# Daily Log : YYYY-MM-DD

## Énergie / état du jour
[mood, énergie /10]

## Ce que j'ai fait aujourd'hui
- ...

## Décisions prises
- ...

## Ce qui m'a frappé / ce que j'ai appris
- ...

## Pour demain
- ...

Confirme la création.
```

### 6.3 `Projects/` (le travail en cours)

La structure `input/output/ressources` est la convention universelle :
- `input/` = matière brute reçue (transcripts, briefs, exports clients)
- `output/` = livrables finaux produits par Claude
- `ressources/` = assets propres à ce projet (à distinguer de `ressources-templates/` qui est transversal)

#### [HUMAIN] Adaptez les sous-dossiers de `Projects/`

Le squelette créé à l'étape 2 utilise les catégories de référence (Sales, LinkedIn, Newsletter, Produit-Clients, Stratégie, Marketing). **Adaptez-les à votre activité.**

Quelques exemples selon le profil :

- **Coach indépendant** : `Sales/`, `LinkedIn/`, `Coaching-Clients/`, `Contenu/`, `Stratégie/`
- **Agence** : `Sales/`, `Production/`, `Comptes-Clients/`, `Marketing/`, `RH/`
- **Solo dev** : `Open-Source/`, `Side-Projects/`, `Freelance/`, `Apprentissage/`
- **Créateur de contenu** : `YouTube/`, `Newsletter/`, `Twitter/`, `Sponsors/`, `Produits/`

**Convention de nommage des fichiers `output/` :**

`Nom-Sujet_YYYY-MM-DD.ext`

Exemples :
- `Propale-Acme-Refonte_2026-05-04.docx`
- `Post-Defi-IA-20j_2026-05-04.md`
- `Edito-Newsletter-12_2026-05-04.md`

**Tag projet multi-support :** Si un même lancement éclate sur plusieurs dossiers, préfixez tous les fichiers avec un tag commun :
- `[lancement-cohorte-3]_post-annonce.md` dans LinkedIn
- `[lancement-cohorte-3]_email-warmup.md` dans Sales
- `[lancement-cohorte-3]_landing-copy.md` dans Marketing

---

## 7. Étape 5 : Connecter vos MCP (l'extension du sandbox)

Les MCP (Model Context Protocol servers) permettent à Claude d'accéder à vos outils externes : Gmail, Notion, Drive, Slack, Calendar, GitHub, et des centaines d'autres.

### 7.1 Hiérarchie de priorité (à respecter)

1. **MCP natifs** : Gmail, Google Calendar, Drive, Notion, Slack, Firecrawl, Apify
2. **Fichiers locaux exportés** (.csv, .md) : pour ce qui n'a pas de MCP
3. **Navigateur (Browser Use)** : pour les outils sans API
4. **Computer Use** : dernier recours, lent et coûteux

### 7.2 [HUMAIN] Connectez vos 3-5 MCP prioritaires

Identifiez vos 3 à 5 outils où vous passez le plus de temps. Connectez-les via Claude Code (`/mcp` ou via les paramètres).

**Conseil :** Ne connectez PAS tout. Chaque MCP rajoute du contexte au démarrage. Connectez seulement ce que vous utilisez vraiment.

**Conseil sécurité :** Pour chaque MCP, lisez les permissions. Ne donnez **jamais** d'accès en écriture si vous n'en avez pas besoin (ex : un MCP Gmail en lecture seule pour de la veille, pas en écriture).

### 7.3 [CLAUDE EXECUTE] Documenter les MCP dans CLAUDE.md

Une fois les MCP connectés, demandez à Claude :

```
Mets à jour CLAUDE.md pour ajouter une section "MCP connectés"
qui liste les outils auxquels j'ai donné accès, et pour chacun :
- Le nom
- L'usage typique (lecture / écriture / les deux)
- Les actions qui requièrent ma confirmation explicite avant d'être lancées

Exemple :
- Gmail : lecture seule, pour analyse / triage
- Notion : lecture + écriture, mais TOUJOURS demander confirmation
  avant de modifier une page
- Calendar : lecture seule
```

---

## 8. Étape 6 : Créer vos premiers skills

Un **skill** est un workflow réutilisable que Claude peut déclencher automatiquement. Il vit dans `.claude/skills/`.

### 8.1 Règle d'or

**Ne créez JAMAIS un skill from scratch.** Faites d'abord la tâche manuellement (avec Claude) 2-3 fois. Quand le pattern se stabilise, demandez à Claude de transformer ça en skill.

### 8.2 Top 7 skills à créer en priorité (quand vous en aurez besoin)

1. **Organisateur de fichiers** : range automatiquement les nouveaux fichiers selon vos règles
2. **Triage emails** : classifie / résume / archive
3. **Recyclage de contenu** : transforme un post en thread / une vidéo en 5 posts / etc.
4. **Rédacteur LinkedIn** : génère des posts dans votre voix
5. **Préparateur de réunions** : agrège contexte + agenda + objectifs
6. **Créateur de présentations** : structure + génère un .pptx
7. **Générateur d'infographies** : produit des visuels Excalidraw

### 8.3 [CLAUDE EXECUTE] Pattern de création d'un skill

Une fois que vous avez fait une tâche 2-3 fois manuellement, lancez :

```
On a fait cette tâche [X] plusieurs fois ensemble
(références : conversations du [date1], [date2], [date3]).

Je veux qu'on en fasse un skill réutilisable dans .claude/skills/[nom-skill]/.

ÉTAPE 1 : Avant de coder le skill, fais-moi une synthèse :
- Quelle est la tâche en une phrase ?
- Quels sont les inputs nécessaires ?
- Quelles sont les étapes (numérotées) ?
- Quels sont les outputs attendus ?
- Quelles sont les variations selon le contexte ?
- Quelles sont les règles spécifiques (ce qu'il faut éviter) ?

ÉTAPE 2 : Quand on est aligné sur la synthèse, rédige le skill :
- Crée .claude/skills/[nom-skill]/SKILL.md
- Inclus une description claire (c'est elle qui déclenche le skill auto)
- Si pertinent, crée un sous-dossier examples/ avec 1-2 exemples de référence

Commence par l'étape 1.
```

### 8.4 Structure type d'un skill

```
.claude/skills/redaction-linkedin/
├── SKILL.md              ← description + process + règles
└── examples/
    ├── post-storytelling.md
    ├── post-educational.md
    └── post-hot-take.md
```

---

## 9. Étape 7 : Maintenance & rituels

Une infra Claude n'est pas un projet "one-shot". Elle vit.

### 9.1 Cadence de mise à jour

| Fichier / dossier | Cadence |
|---|---|
| `ABOUT.ME/about-me.md` | Tous les 6-12 mois (rare changement) |
| `ABOUT.ME/my-company.md` | Tous les 1-3 mois (snapshot) |
| `Contexte/Goals-and-Direction.md` | Tous les 30 jours |
| `Contexte/Life-and-Work-Reality.md` | Tous les 3 mois |
| `Contexte/Offer-Positioning.md` | À chaque nouvelle offre / changement de prix |
| `Contexte/Clients-Problems-and-Messages.md` | Tous les 3 mois (alimenter avec nouveaux verbatim) |
| `Contexte/Expertise-Standards-and-Landmines.md` | Tous les 6 mois ou après une grosse erreur |
| `Contexte/Tone-and-Voice.md` | Tous les 6 mois ou après évolution de style |
| `Contexte/Constitution-Identity.md` | Tous les 12 mois (très stable) |
| `CLAUDE.md` | Quand une règle de routage ne marche plus |

### 9.2 Rituel hebdo (10 min)

Tous les vendredis :
1. Faire un dernier Daily Log de la semaine
2. Vérifier que les livrables produits cette semaine sont au bon endroit
3. Noter dans `Intelligence/veille/` tout ce qui a marqué la semaine
4. Vérifier qu'aucun fichier n'a atterri à la racine du workspace

### 9.3 Rituel mensuel (30 min)

Une fois par mois :
1. Mettre à jour `Goals-and-Direction.md` (snapshot du mois suivant)
2. Mettre à jour `my-company.md` si quelque chose a bougé
3. Lire les Daily Logs du mois et en faire un résumé dans `Intelligence/`
4. Identifier 1 nouvelle tâche récurrente → candidate à un skill

### 9.4 Rituel trimestriel (1h)

Tous les 3 mois :
1. Revue complète des fichiers `Contexte/`
2. Mise à jour de `Life-and-Work-Reality.md`
3. Audit du `Clients-Problems-and-Messages.md` avec les nouveaux verbatim
4. Décision sur les skills à créer / supprimer

---

## 10. Les 10 erreurs à éviter

1. **Créer un skill sans faire la tâche manuellement d'abord** → Vous coderez un skill qui ne sert à rien
2. **Surcharger CLAUDE.md** → Au-delà de 500 lignes, l'IA dilue son attention
3. **Télécharger des skills à l'aveugle** → Vous ne saurez plus ce qui est dans votre infra
4. **Automatiser des tâches rares** (< 1×/semaine) → Coût de maintenance > gain
5. **Tester 5 variables simultanément** → Vous ne saurez pas ce qui marche
6. **Demander des résultats one-shot** → Itérez, c'est là qu'on passe de 80 à 95%
7. **Dupliquer les fichiers de référence** → Centralisez, pointez via chemins relatifs
8. **Donner accès à tout le disque dur** → Sandbox dédié, toujours
9. **Cliquer "Toujours autoriser"** → Lisez chaque permission au moins la première fois
10. **Ne pas mettre à jour son système** → Les snapshots datés de plus de 6 mois polluent plus qu'ils n'aident

---

## 11. Checklist finale

Cochez quand c'est fait. Vous pouvez mettre 1 semaine, 1 mois ou 3 mois pour tout faire. L'important c'est l'ordre.

### Setup
- [ ] Claude Code installé et lancé une première fois
- [ ] Dossier parent créé (sandbox dédié, pas dans Documents/Bureau)
- [ ] Arborescence vide créée (étape 2.3)

### Niveau 1 : Fondations (chargées chaque session)
- [ ] `CLAUDE.md` rédigé et testé à froid
- [ ] `ABOUT.ME/about-me.md` rédigé via interview 3-prompts
- [ ] `ABOUT.ME/my-company.md` rédigé via interview 3-prompts
- [ ] `ABOUT.ME/anti-ai-voice.md` créé (optionnel mais recommandé si contenu)

### Niveau 2 : Cerveau (chargé à la demande)
- [ ] `Contexte/Constitution-Identity.md`
- [ ] `Contexte/Life-and-Work-Reality.md`
- [ ] `Contexte/Goals-and-Direction.md`
- [ ] `Contexte/Offer-Positioning.md`
- [ ] `Contexte/Clients-Problems-and-Messages.md` ⭐
- [ ] `Contexte/Expertise-Standards-and-Landmines.md`
- [ ] `Contexte/Tone-and-Voice.md`

### Niveau 3 : Workspace opérationnel
- [ ] Sous-dossiers `Projects/` adaptés à mon activité
- [ ] `ressources-templates/` initié (au moins fichiers vides)
- [ ] `Intelligence/` initié avec template Daily Log

### Niveau 4 : Connectivité et automatisation
- [ ] 3-5 MCP prioritaires connectés et documentés dans CLAUDE.md
- [ ] Au moins 1 skill créé (après avoir fait la tâche 2-3 fois manuellement)

### Rituels
- [ ] Rituel hebdo posé dans mon agenda (vendredi 10 min)
- [ ] Rituel mensuel posé dans mon agenda (30 min)
- [ ] Rituel trimestriel posé dans mon agenda (1h)

---

## 12. Pour aller plus loin

Quand toute la checklist est cochée, vous avez une infra solide. Les prochaines étapes naturelles :

1. **Skills avancés** : automatisations spécifiques à votre métier
2. **Sub-agents** : déléguer des tâches longues à des agents spécialisés en parallèle
3. **Intégration cloud** : exécuter votre infra depuis n'importe où via une API
4. **Partage d'équipe** : étendre le sandbox à votre équipe (avec ses propres `ABOUT.ME/` par membre)

---

## Notes pour la transformation en skill

> Cette section est destinée à l'IA qui transformera ce guide en skill `.claude/skills/setup-claude-infrastructure/`.

**Découpage suggéré du skill en sous-skills (pour rester sous la limite de contexte) :**

1. `setup-claude-infrastructure-init` : Étapes 0 à 2 (intro + arborescence)
2. `setup-claude-infrastructure-claude-md` : Étape 3 (CLAUDE.md)
3. `setup-claude-infrastructure-about-me` : Étape 4 (ABOUT.ME/)
4. `setup-claude-infrastructure-contexte` : Étape 5 (les 7 fichiers : un sous-skill par fichier si besoin)
5. `setup-claude-infrastructure-projects` : Étape 6 (workspace)
6. `setup-claude-infrastructure-mcp-skills` : Étapes 7-8 (MCP + skills)
7. `setup-claude-infrastructure-maintenance` : Étape 9 (rituels)

**Logique d'orchestration :**
- Le skill master vérifie où en est l'utilisateur (quel fichier existe, lequel est vide)
- Il propose la prochaine étape logique
- Il déclenche le sous-skill correspondant
- Il met à jour une "checklist d'avancement" stockée dans `.claude/skills/setup-claude-infrastructure/progress.md`

**Points de validation utilisateur (handoffs obligatoires) :**
- Avant de créer la structure de dossiers (validation du nom du dossier parent)
- Après chaque interview (l'humain doit avoir le temps de répondre, ne pas rusher)
- Avant écriture finale de chaque fichier (montrer un brouillon, demander OK)
- Avant connexion d'un MCP (validation des permissions)
- Avant création d'un skill (validation du périmètre)

**Données à demander à l'utilisateur en début de skill :**
- Nom et chemin du dossier parent
- Profession / métier (sert à adapter les sous-dossiers Projects/)
- Niveau de maturité existant (a-t-il déjà des fichiers ? un workspace embryonnaire ?)
- Temps disponible pour cette session (1h ? 1 journée ? 1 semaine étalée ?)

**Sources canoniques pour les prompts d'interview Contexte/ :**
- Page Notion "Votre Cerveau IA" + 7 sous-pages (une par fichier)
- Pour `Offer-Positioning.md` : la version Notion est partiellement coupée à l'export. La version intégrée dans ce guide est reconstituée fidèlement à partir du pattern strict utilisé dans les 6 autres prompts. À vérifier contre l'original quand accessible.

---

*Guide v2 : 2026-05-04*
*Sources : "Construisez votre infrastructure" + "Créez votre cerveau IA" (Hugo Dollfus, Substack) + page Notion "Votre Cerveau IA" (7 sous-pages avec les prompts originaux des fichiers Contexte/)*
