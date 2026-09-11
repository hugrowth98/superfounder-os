---
name: installer-second-cerveau
description: Jour 1 de Superfounder OS. Construit le second cerveau de l'utilisateur, le socle que tous les autres skills lisent avant d'agir : ABOUT.ME/ (3 fichiers), les 7 fichiers de Contexte/, les MCP et le premier skill. Process étape par étape, une étape à la fois, avec une interview en 3 prompts (cadrage, interview, synthèse) pour chaque fichier stratégique. Se déclenche sur "Installe mon second cerveau", "construire mon infrastructure Claude", "créer mon cerveau IA", "setup workspace", "on commence", "je démarre", ou tout premier message d'un utilisateur dont ABOUT.ME/about-me.md contient encore [à remplir].
argument-hint: [optionnel : numéro d'étape pour reprendre, ex "étape 3" ou "contexte"]
user-invocable: true
context: main
---

# Installer mon second cerveau (jour 1)

**Objectif :** transformer Claude en assistant ultra-personnalisé qui connaît la vie, le business, les clients et la voix de l'utilisateur, et qui sait où ranger ce qu'il produit. C'est le jour 1 : les jours 2 (prospection) et 3 (contenu) lisent ce que ce skill produit et n'interviewent que sur ce qui manque.

**Le workspace existe déjà.** L'utilisateur a cloné Superfounder OS : l'arborescence, le CLAUDE.md racine, les fichiers ABOUT.ME/ et Contexte/ sont présents avec des `[à remplir]`. Ce skill ne crée pas la structure, il la remplit. Vouvoiement, une étape à la fois, jamais de tiret cadratin.

**Durée totale :** 4-8h, à étaler sur quelques jours.

**Architecture (déjà en place, à remplir) :**
```
CLAUDE.md                     GPS racine, importe ABOUT.ME/ à chaque session
ABOUT.ME/                     about-me.md, my-company.md, anti-ai-voice.md
Contexte/                     7 fichiers : identité, réalité de travail, objectifs, offre, clients, standards, voix
Inbox/  Intelligence/  ressources-templates/
Projects/                     Prospection/ (jour 2), Contenu/ (jour 3), Clients/, Strategie/
.claude/skills/               les 10 skills transverses
```

**Référence canonique :** ce skill s'appuie sur `references/guide-complet.md` qui contient tous les prompts d'interview détaillés. Lis-le à la demande, section par section, jamais en entier d'un coup.

---

## Règles d'orchestration (à respecter strictement)

1. **Une étape à la fois.** Ne jamais enchaîner plusieurs étapes sans validation explicite de l'utilisateur.
2. **Toujours détecter où en est l'utilisateur** avant de proposer la suite. Lis l'arborescence du dossier de travail, vérifie quels fichiers existent, lesquels sont vides.
3. **Proposer la prochaine étape logique**, ne pas imposer.
4. **Ne jamais créer un fichier sans confirmation** quand il s'agit de fichiers à contenu personnel (ABOUT.ME, Contexte). La structure vide oui, le contenu non.
5. **Pour chaque fichier de Contexte/, suivre rigoureusement les 3 prompts** dans la même conversation : Cadrage → Interview → Synthèse. Ne jamais sauter de prompt.
6. **Pour les longs prompts d'interview**, lire la section correspondante de `references/guide-complet.md` et les présenter verbatim à l'utilisateur (ou les exécuter directement si l'utilisateur veut faire l'interview avec toi).

---

## Étape 0 : Diagnostic initial

Quand le skill est invoqué, commence TOUJOURS par :

1. **Vérifier le contexte.** Lire `ABOUT.ME/` et `Contexte/`. Un fichier est "à faire" s'il contient encore `[à remplir]`, "fait" sinon.
2. **Si tout est encore `[à remplir]`** → afficher l'état des lieux et proposer de démarrer à l'Étape 2 (CLAUDE.md est déjà fourni, on passe directement à ABOUT.ME).
3. **Si partiellement construit** → afficher un état des lieux (✅/❌/🚧) et proposer la prochaine étape logique.
4. **Demander à l'utilisateur** :
   - Son métier / activité (sert à adapter les sous-dossiers Projects/ si les 4 par défaut ne suffisent pas)
   - Le temps qu'il a pour cette session (1h, demi-journée, étalé sur la semaine)
   - S'il a une préférence pour démarrer par une étape précise

Format de l'état des lieux :
```
État de votre infrastructure :
├── CLAUDE.md                                        ✅ Existe (X lignes)
├── ABOUT.ME/
│   ├── about-me.md                                  🚧 À remplir
│   ├── my-company.md                                🚧 À remplir
│   └── anti-ai-voice.md                             ✅ Fourni (section 7 à compléter)
├── Contexte/
│   ├── Constitution-Identity.md                     🚧 À remplir
│   ├── Life-and-Work-Reality.md                     🚧 À remplir
│   ...

Prochaine étape recommandée : Étape 2 (compléter ABOUT.ME/about-me.md)
```

---

## Étape 1 : Vérifier la structure

**Quand :** toujours, en 30 secondes.

La structure est livrée avec Superfounder OS. Vérifie simplement qu'elle est intacte (`ls`) : `ABOUT.ME/`, `Contexte/` (7 fichiers), `Inbox/`, `Intelligence/`, `Projects/{Prospection,Contenu,Clients,Strategie}/` avec `input/ output/ ressources/`.

Si l'utilisateur a un métier qui appelle d'autres domaines (par exemple `Projects/Recrutement/` pour un cabinet, `Projects/Formation/` pour un formateur), propose-les et crée-les sur le même patron : `CLAUDE.md` + `input/ output/ ressources/`. Demande avant de figer.

---

## Étape 2 : Adapter CLAUDE.md (le GPS racine)

**Quand :** le CLAUDE.md racine est fourni et fonctionne tel quel. Cette étape sert seulement à l'ajuster.

**Process :**
1. Lire la section 3 du guide (`references/guide-complet.md`) pour comprendre le rôle du fichier.
2. Demander à l'utilisateur 3 choses, une à la fois : sa langue de travail si ce n'est pas le français, ses règles de collaboration non négociables (ce que Claude ne doit jamais faire sans demander), et les domaines Projects/ supplémentaires décidés à l'étape 1.
3. Modifier uniquement la section 1 (règles) et la section 3 (architecture) du CLAUDE.md racine. Ne pas toucher au reste : le diagnostic du premier message, le routage et les rituels sont le coeur de l'OS.
4. Garder le fichier sous 200 lignes.

---

## Étape 3 : Construire ABOUT.ME/

**Quand :** les 3 fichiers d'ABOUT.ME/ existent avec des `[à remplir]`. C'est le coeur du jour 1.

**3 fichiers à produire dans cet ordre :**

### 3a. about-me.md (qui vous êtes)
- Lire section 4.1 du guide.
- Présenter le PROMPT 1 (cadrage) → confirmer la compréhension.
- Présenter le PROMPT 2 (interview, 20 questions sur 6 axes : identité, façon de travailler, ce qui est bon, ce qu'on déteste, règles, convictions).
- **Recommander à l'utilisateur** : « Faites ça en mode vocal pendant une marche de 30 min, c'est plus naturel ».
- Mener l'interview une question à la fois, push-back si vague.
- Présenter le PROMPT 3 (synthèse) → produire `ABOUT.ME/about-me.md` (max 1500 mots, structure imposée).

### 3b. my-company.md (snapshot business)
- Lire section 4.2 du guide.
- Même process 3-prompts (8 questions sur 4 axes : offre active, objectifs 90j, focus actuel, anti-objectifs).
- Produire `ABOUT.ME/my-company.md` daté (snapshot).
- Rappeler à l'utilisateur : à mettre à jour tous les 1-3 mois.

### 3c. anti-ai-voice.md (optionnel mais recommandé)
- Lire section 4.3 du guide.
- Le fichier est fourni en version générique. Ne pas le régénérer. Remplacer le `[à remplir]` de la section 7.
- Demander à l'utilisateur ses expressions orales à lui (celles qu'on entend quand il parle) et ses mots bannis, et compléter la section 7.

---

## Étape 4 : Construire les 7 fichiers Contexte/

**Quand :** ABOUT.ME/ complet.

**Règle critique :** chaque fichier suit le même pattern strict 3-prompts (Cadrage → Interview → Synthèse), tous dans la **même conversation**. La continuité du contexte est essentielle.

**Recommander à l'utilisateur :** ne pas tout enchaîner. Faire 1 ou 2 fichiers par session, pas plus. Chaque interview prend 30-45 min.

**Ordre suggéré (du plus stable au plus volatile) :**

1. **Constitution-Identity.md** (section 5.1 du guide) : Boussole morale. Très stable, MAJ tous les 12 mois.
2. **Tone-and-Voice.md** (section 5.7) : Voix d'auteur. Demander des documents : posts, mails, transcripts.
3. **Expertise-Standards-and-Landmines.md** (section 5.6) : Niveau d'exigence + erreurs vécues.
4. **Offer-Positioning.md** (section 5.4) : Offre actuelle, exclusions.
5. **Clients-Problems-and-Messages.md** (section 5.5) ⭐ : LE plus stratégique. Demander en priorité : transcripts d'appels de vente, verbatim clients.
6. **Life-and-Work-Reality.md** (section 5.2) : Contraintes réelles, modèle éco.
7. **Goals-and-Direction.md** (section 5.3) : Objectifs datés, mesurables.

**Pour chaque fichier :**

1. Annoncer le fichier qu'on va construire et son rôle (1 phrase).
2. **Lire la section correspondante de `references/guide-complet.md`** pour récupérer les 3 prompts exacts.
3. **Présenter le PROMPT 1 (Cadrage)** verbatim à l'utilisateur, ou en faire toi-même la confirmation et lui demander les documents.
4. Attendre les documents (ou validation qu'il n'y en a pas).
5. **Lancer l'interview (PROMPT 2)** : suivre les axes dans l'ordre, une question à la fois, push-back obligatoire selon les règles spécifiques au prompt.
6. Quand tous les axes sont couverts, demander : « OK pour produire le fichier final ? »
7. **Exécuter le PROMPT 3 (Synthèse)** : produire le fichier dans `Contexte/[NOM-FICHIER].md` en respectant la structure obligatoire et les contraintes (1-2 pages max, première personne, exemples MAUVAIS/BON, etc.).
8. **Demander relecture** : « Lisez le fichier généré et dites-moi ce qui sonne juste ou faux. On itère si besoin. »
9. Mettre à jour mentalement l'état des lieux et proposer le fichier suivant.

**Note importante sur Offer-Positioning.md :** la version dans `references/guide-complet.md` a été reconstituée fidèlement à partir du pattern strict des 6 autres prompts (la version Notion d'origine était partiellement coupée à l'export). Si l'utilisateur a accès à la version originale complète, lui proposer de la fournir.

---

## Étape 5 : Peupler ressources-templates/ et Intelligence/

**Quand :** au moins quelques fichiers Contexte/ produits.

**Process :**
1. `ressources-templates/` : demander à l'utilisateur s'il a déjà des exemples de bons contenus à lui (posts, newsletters, mails) à déposer. Ils serviront à calibrer la voix. Sinon, on les ajoutera au fil de l'eau.
2. `Intelligence/` : expliquer le wiki en deux phrases (voir `Intelligence/CLAUDE.md`) et proposer une première source à ingérer avec `/notes-permanentes`, par exemple un article qu'il cite souvent.
3. Présenter la convention de nommage des livrables : `Nom-Sujet_YYYY-MM-DD.ext` dans le `output/` du domaine.

---

## Étape 6 : Connecter les MCP

**Quand :** workspace fonctionnel, l'utilisateur veut étendre.

**Process :**
1. Lire section 7 du guide.
2. Présenter la hiérarchie : MCP natifs > fichiers locaux > navigateur > Computer Use.
3. Demander à l'utilisateur ses 3-5 outils prioritaires.
4. Les connecter un par un avec `/connect-mcp <nom>` (le skill cherche le bon serveur, demande les clés, écrit la config).
5. **Une fois connectés**, mettre à jour CLAUDE.md avec une section "MCP connectés" qui liste pour chacun : nom, usage (lecture/écriture), actions requérant confirmation explicite.

**Garde-fou sécurité :** insister sur l'audit des permissions, surtout en écriture.

---

## Étape 7 : Créer le premier skill

**Quand :** l'utilisateur a fait une tâche 2-3 fois manuellement et veut l'automatiser.

**Règle d'or à rappeler :** ne JAMAIS créer un skill from scratch. Faire d'abord la tâche manuellement, plusieurs fois. Quand le pattern se stabilise, alors créer le skill.

**Process :**
1. Lire section 8 du guide.
2. Faire la synthèse (étape 1) : tâche en une phrase, inputs, étapes, outputs, variations, règles spécifiques.
3. Valider la synthèse avec l'utilisateur.
4. Créer `.claude/skills/[nom-skill]/SKILL.md` en suivant la convention frontmatter (name, description, argument-hint, user-invocable, context).
5. Créer un sous-dossier `examples/` ou `references/` si pertinent.

---

## Étape 8 : Poser les rituels de maintenance

**Quand :** infra complète.

**Process :**
1. Lire section 9 du guide.
2. Présenter la cadence de mise à jour par fichier.
3. Présenter les rituels fournis, un par un, avec la phrase à taper : `/done` en fin de chaque session (c'est celui qui garde le cerveau vivant), `/daily-review` le soir, `/weekly-review` le vendredi, `/inbox-processor` quand l'Inbox déborde.
4. Aider l'utilisateur à poser dans son agenda :
   - Rituel hebdo (vendredi, 10 min)
   - Rituel mensuel (30 min) : relire `ABOUT.ME/my-company.md`
   - Rituel trimestriel (1h) : relire `Contexte/`

---

## Erreurs à signaler activement

À chaque étape, surveiller et alerter si :
- L'utilisateur veut créer un skill sans avoir fait la tâche manuellement avant
- CLAUDE.md dépasse 500 lignes
- L'utilisateur veut donner accès à tout son disque dur (proposer un sandbox)
- Plusieurs variables testées simultanément
- Un fichier Contexte/ a été produit sans interview (résultats vagues garantis)

---

## Checklist finale (à présenter quand l'utilisateur dit "j'ai fini")

```
Infrastructure Claude : État final

Setup
- [ ] Claude Code installé
- [ ] Superfounder OS cloné dans un dossier dédié
- [ ] Arborescence vérifiée

Niveau 1 : Fondations (chargées chaque session)
- [ ] CLAUDE.md adapté (règles, domaines)
- [ ] ABOUT.ME/about-me.md
- [ ] ABOUT.ME/my-company.md
- [ ] ABOUT.ME/anti-ai-voice.md

Niveau 2 : Cerveau (chargé à la demande)
- [ ] Constitution-Identity.md
- [ ] Life-and-Work-Reality.md
- [ ] Goals-and-Direction.md
- [ ] Offer-Positioning.md
- [ ] Clients-Problems-and-Messages.md ⭐
- [ ] Expertise-Standards-and-Landmines.md
- [ ] Tone-and-Voice.md

Niveau 3 : Workspace
- [ ] Projects/ adapté au métier
- [ ] ressources-templates/ initié
- [ ] Intelligence/ initié

Niveau 4 : Connectivité
- [ ] 3-5 MCP connectés et documentés dans CLAUDE.md
- [ ] Au moins 1 skill créé

Rituels
- [ ] Hebdo posé dans l'agenda
- [ ] Mensuel posé dans l'agenda
- [ ] Trimestriel posé dans l'agenda
```

---

## Et après

Quand la checklist est verte, propose la suite en une phrase : "Votre second cerveau est en place. Quand vous voulez, ouvrez `Projects/Prospection/` et dites : Installe ma prospection."

---

## Reprise de session

Si l'utilisateur invoque le skill avec un argument (ex: "étape 3" ou "contexte"), aller directement à l'étape demandée après avoir vérifié l'état des lieux.

Si l'utilisateur dit « reprends là où on s'était arrêté » sans précision, faire le diagnostic initial et déduire la prochaine étape logique.

---

## Référence

Le guide complet (avec tous les prompts d'interview verbatim) est dans `references/guide-complet.md`. Le lire **par section**, jamais en entier : chaque étape de ce skill correspond à une section précise du guide.
