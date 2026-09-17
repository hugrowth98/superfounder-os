---
name: installer-second-cerveau
description: Construit le second cerveau de l'utilisateur, le socle que tous les autres skills lisent avant d'agir : About-Me/ (3 fichiers), les 7 fichiers de Contexte/, les dossiers de ses clients actifs, les MCP et le premier skill. Process étape par étape, une étape à la fois, avec une interview en 3 prompts (cadrage, interview, synthèse) pour chaque fichier stratégique. Se déclenche sur "Installe mon second cerveau", "construire mon infrastructure Claude", "créer mon cerveau IA", "setup workspace", "on commence", "je démarre", ou tout premier message d'un utilisateur dont About-Me/about-me.md contient encore [à remplir].
argument-hint: [optionnel : numéro d'étape pour reprendre, ex "étape 3" ou "contexte"]
user-invocable: true
context: main
---

# Installer mon second cerveau

**Objectif :** transformer Claude en assistant qui connaît la vie, le business, les clients et la voix de l'utilisateur, et qui sait où ranger ce qu'il produit. C'est le socle : la prospection ("Installe ma prospection") et le contenu ("Installe mon contenu") lisent ce que ce skill produit et n'interviewent que sur ce qui manque.

**Le workspace existe déjà.** L'utilisateur a cloné Superfounder OS : l'arborescence, le CLAUDE.md racine, les fichiers About-Me/ et Contexte/ sont présents avec des `[à remplir]`, chaque dossier de travail a sa note. Ce skill ne crée pas la structure, il la remplit. Vouvoiement, une étape à la fois, jamais de tiret cadratin.

**Durée totale :** 4-8h, à étaler sur quelques jours.

**Architecture (déjà en place, à remplir) :**
```
CLAUDE.md          la carte, importe About-Me/ à chaque session
About-Me/          about-me.md, my-company.md, anti-ai-voice.md
Contexte/          7 fichiers : identité, réalité de travail, objectifs, offre, clients, standards, voix
Branding/  Ressources/  Inbox/  Journal/  Veille/  Meeting/
Produit-Client/    un dossier par client et par produit, chacun avec sa note
Marketing/  Vente/  Strategie/    les dossiers de travail, chacun avec sa note et ses sous-dossiers
.claude/skills/    les 11 skills transverses
```

**Référence canonique :** ce skill s'appuie sur `references/guide-complet.md` qui contient tous les prompts d'interview détaillés. Lis-le à la demande, section par section, jamais en entier d'un coup.

---

## Règles d'orchestration (à respecter strictement)

1. **Une étape à la fois.** Ne jamais enchaîner plusieurs étapes sans validation explicite de l'utilisateur.
2. **Toujours détecter où en est l'utilisateur** avant de proposer la suite. Lis l'arborescence, vérifie quels fichiers existent, lesquels sont vides.
3. **Proposer la prochaine étape logique**, ne pas imposer.
4. **Ne jamais créer un fichier sans confirmation** quand il s'agit de fichiers à contenu personnel (About-Me, Contexte, notes de client). La structure vide oui, le contenu non.
5. **Pour chaque fichier de Contexte/, suivre rigoureusement les 3 prompts** dans la même conversation : Cadrage, Interview, Synthèse. Ne jamais sauter de prompt.
6. **Écrire au fur et à mesure.** Chaque fichier est écrit à la fin de son étape, depuis la décharge fraîche, jamais tout à la fin.
7. **Pour les longs prompts d'interview**, lire la section correspondante de `references/guide-complet.md` et les présenter verbatim à l'utilisateur (ou les exécuter directement si l'utilisateur veut faire l'interview avec toi).

---

## Étape 0 : Diagnostic initial

Quand le skill est invoqué, commence TOUJOURS par :

1. **Vérifier le contexte.** Lire `About-Me/` et `Contexte/`. Un fichier est "à faire" s'il contient encore `[à remplir]`, "fait" sinon. Lister `Produit-Client/` : y a-t-il déjà des dossiers de clients ?
2. **Si tout est encore `[à remplir]`** : afficher l'état des lieux et proposer de démarrer à l'Étape 2 (CLAUDE.md est déjà fourni, on passe directement à About-Me).
3. **Si partiellement construit** : afficher un état des lieux et proposer la prochaine étape logique.
4. **Demander à l'utilisateur** :
   - Son métier / activité (sert à décider si un dossier de travail manque)
   - Le temps qu'il a pour cette session (1h, demi-journée, étalé sur la semaine)
   - S'il a des documents à déposer (CV, bio, offres écrites, transcripts d'appels) : à tout moment, un document déposé remplace une partie de l'interview

Format de l'état des lieux :
```
État de votre second cerveau :
├── CLAUDE.md                                        fourni
├── About-Me/
│   ├── about-me.md                                  à remplir
│   ├── my-company.md                                à remplir
│   └── anti-ai-voice.md                             fourni (section 7 à compléter)
├── Contexte/
│   ├── Constitution-Identity.md                     à remplir
│   ├── Life-and-Work-Reality.md                     à remplir
│   ...
├── Produit-Client/                                  aucun client pour l'instant

Prochaine étape recommandée : Étape 2 (compléter About-Me/about-me.md)
```

---

## Étape 1 : Vérifier la structure

**Quand :** toujours, en 30 secondes.

La structure est livrée avec Superfounder OS. Vérifie simplement qu'elle est intacte (`ls`) : `About-Me/`, `Contexte/` (7 fichiers), `Branding/`, `Ressources/templates/`, `Inbox/`, `Journal/`, `Veille/`, `Meeting/`, `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/`, `Archives/`. Chaque dossier de travail a une note du même nom (`Vente/Vente.md`).

Si l'utilisateur a un métier qui appelle un dossier de plus (par exemple `Formation/` pour un formateur, `Recrutement/` pour un cabinet), propose-le et crée-le sur le même patron : une note du même nom depuis `Ressources/templates/note-de-dossier.md`, un `_log.md`, et `sources/ livrables/ ressources/`. Ajoute-le à la table du CLAUDE.md racine (section 3). Demande avant de figer.

---

## Étape 2 : Adapter CLAUDE.md (la carte)

**Quand :** le CLAUDE.md racine est fourni et fonctionne tel quel. Cette étape sert seulement à l'ajuster.

**Process :**
1. Lire la section 3 du guide (`references/guide-complet.md`) pour comprendre le rôle du fichier.
2. Demander à l'utilisateur 2 choses, une à la fois : sa langue de travail si ce n'est pas le français, et ses règles de collaboration non négociables (ce que Claude ne doit jamais faire sans demander).
3. Modifier uniquement la section 1 (règles) du CLAUDE.md racine, et la section 3 si un dossier a été ajouté à l'Étape 1. Ne pas toucher au reste : le diagnostic du premier message, le rôle des dossiers, le routage et les rituels sont le coeur de l'OS.
4. Garder le fichier sous 200 lignes.

---

## Étape 3 : Construire About-Me/

**Quand :** les 3 fichiers d'About-Me/ existent avec des `[à remplir]`. C'est le coeur du second cerveau.

**3 fichiers à produire dans cet ordre :**

### 3a. about-me.md (qui vous êtes)
- Lire section 4.1 du guide.
- Présenter le PROMPT 1 (cadrage), confirmer la compréhension.
- Présenter le PROMPT 2 (interview, 20 questions sur 6 axes : identité, façon de travailler, ce qui est bon, ce qu'on déteste, règles, convictions).
- **Recommander à l'utilisateur** : « Faites ça en mode vocal pendant une marche de 30 min, c'est plus naturel ».
- Mener l'interview une question à la fois, push-back si vague.
- Présenter le PROMPT 3 (synthèse), produire `About-Me/about-me.md` (max 1500 mots, structure imposée). Demander une relecture rapide.

### 3b. my-company.md (snapshot business)
- Lire section 4.2 du guide.
- Même process 3-prompts (8 questions sur 4 axes : offre active, objectifs 90j, focus actuel, anti-objectifs).
- Produire `About-Me/my-company.md` daté (snapshot). C'est la source de vérité sur l'offre et les prix : partout ailleurs, on pointe dessus.
- Rappeler à l'utilisateur : à mettre à jour tous les 1-3 mois.

### 3c. anti-ai-voice.md (optionnel mais recommandé)
- Lire section 4.3 du guide.
- Le fichier est fourni en version générique. Ne pas le régénérer. Remplacer le `[à remplir]` de la section 7.
- Demander à l'utilisateur ses expressions orales à lui (celles qu'on entend quand il parle) et ses mots bannis, et compléter la section 7.

---

## Étape 4 : Construire les 7 fichiers Contexte/

**Quand :** About-Me/ complet.

**Règle critique :** chaque fichier suit le même pattern strict 3-prompts (Cadrage, Interview, Synthèse), tous dans la **même conversation**. La continuité du contexte est essentielle.

**Recommander à l'utilisateur :** ne pas tout enchaîner. Faire 1 ou 2 fichiers par session, pas plus. Chaque interview prend 30-45 min.

**Ordre suggéré (du plus stable au plus volatile) :**

1. **Constitution-Identity.md** (section 5.1 du guide) : boussole morale. Très stable, MAJ tous les 12 mois.
2. **Tone-and-Voice.md** (section 5.7) : voix d'auteur. Demander des documents : posts, mails, transcripts.
3. **Expertise-Standards-and-Landmines.md** (section 5.6) : niveau d'exigence et erreurs vécues.
4. **Offer-Positioning.md** (section 5.4) : offre actuelle, exclusions.
5. **Clients-Problems-and-Messages.md** (section 5.5), le plus stratégique. Demander en priorité : transcripts d'appels de vente, verbatim clients. S'il en a, les déposer dans `Meeting/Clients/<Nom>/` pour une mission, `Meeting/Coaching/<Nom>/` pour un coaching, `Meeting/Prospects/YYYY-MM/` pour un prospect.
6. **Life-and-Work-Reality.md** (section 5.2) : contraintes réelles, modèle éco.
7. **Goals-and-Direction.md** (section 5.3) : objectifs datés, mesurables.

**Pour chaque fichier :**

1. Annoncer le fichier qu'on va construire et son rôle (1 phrase).
2. **Lire la section correspondante de `references/guide-complet.md`** pour récupérer les 3 prompts exacts.
3. **Présenter le PROMPT 1 (Cadrage)** verbatim à l'utilisateur, ou en faire toi-même la confirmation et lui demander les documents.
4. Attendre les documents (ou validation qu'il n'y en a pas).
5. **Lancer l'interview (PROMPT 2)** : suivre les axes dans l'ordre, une question à la fois, push-back obligatoire selon les règles spécifiques au prompt.
6. Quand tous les axes sont couverts, demander : « OK pour produire le fichier final ? »
7. **Exécuter le PROMPT 3 (Synthèse)** : produire le fichier dans `Contexte/[NOM-FICHIER].md` en respectant la structure obligatoire et les contraintes (1-2 pages max, première personne, exemples MAUVAIS/BON).
8. **Demander relecture** : « Lisez le fichier généré et dites-moi ce qui sonne juste ou faux. On itère si besoin. »
9. Mettre à jour mentalement l'état des lieux et proposer le fichier suivant.

**Note sur Offer-Positioning.md :** la version dans `references/guide-complet.md` a été reconstituée à partir du pattern strict des 6 autres prompts. Si l'utilisateur a accès à une version plus complète de ce prompt, lui proposer de la fournir.

---

## Étape 5 : Vos clients actifs

**Quand :** au moins `Offer-Positioning.md` et `Clients-Problems-and-Messages.md` produits.

**Process :**
1. Demander : « Quels sont vos 3 clients les plus actifs en ce moment ? » Trois maximum pour commencer, les autres viendront au fil de l'eau.
2. Pour chaque client, une conversation courte : qui c'est (secteur, taille), la mission et son prix, l'interlocuteur principal, comment il aime travailler, où en est la mission. Un document déposé (propale, compte rendu, transcript) remplace les questions.
3. Créer `Produit-Client/<Nom>/` avec sa note `<Nom>.md` depuis `Ressources/templates/note-de-dossier-client.md`, remplie avec ce qui a été dit, plus `_log.md` et `livrables/`. Montrer, faire valider, écrire.

C'est la note que Claude lira avant tout travail pour ce client. Un transcript de call avec lui va dans `Meeting/Clients/<Nom>/`, et `/done` fait ruisseler ce qui s'y décide vers cette note.

---

## Étape 6 : Peupler Ressources/, Veille/, Branding/

**Quand :** au moins quelques fichiers Contexte/ produits.

**Process :**
1. `Ressources/` : demander à l'utilisateur s'il a déjà des exemples de bons contenus à lui (posts, newsletters, mails) à déposer. Ils serviront à calibrer la voix.
2. `Branding/` : s'il a une charte, des logos, des polices, les déposer ici. Sinon, une ligne dans `Branding/Branding.md` avec ses couleurs et sa police suffit pour commencer.
3. `Veille/` : expliquer le wiki en deux phrases (voir `Veille/Veille.md`) et proposer une première source à ingérer avec `/notes-permanentes`, par exemple un article qu'il cite souvent.
4. Présenter la convention de nommage des livrables : `Nom-Sujet_YYYY-MM-DD.ext` dans le `livrables/` du bon dossier, et la règle des notes : avant de travailler dans un dossier, on lit sa note.

---

## Étape 7 : Connecter les MCP

**Quand :** workspace fonctionnel, l'utilisateur veut étendre.

**Process :**
1. Lire section 7 du guide.
2. Présenter la hiérarchie : MCP natifs > fichiers locaux > navigateur > Computer Use.
3. Demander à l'utilisateur ses 3-5 outils prioritaires.
4. Les connecter un par un avec `/connect-mcp <nom>` (le skill cherche le bon serveur, demande les clés, écrit la config).
5. **Une fois connectés**, ajouter au CLAUDE.md une section "MCP connectés" qui liste pour chacun : nom, usage (lecture/écriture), actions requérant confirmation explicite.

**Garde-fou sécurité :** insister sur l'audit des permissions, surtout en écriture. Lecture seule par défaut, jamais d'envoi automatique, un MCP à la fois.

---

## Étape 8 : Créer le premier skill

**Quand :** l'utilisateur a fait une tâche 2-3 fois manuellement et veut l'automatiser.

**Règle d'or à rappeler :** ne JAMAIS créer un skill from scratch. Faire d'abord la tâche manuellement, plusieurs fois. Quand le pattern se stabilise, alors créer le skill.

**Process :**
1. Lire section 8 du guide.
2. Faire la synthèse : tâche en une phrase, inputs, étapes, outputs, variations, règles spécifiques.
3. Valider la synthèse avec l'utilisateur.
4. Créer `.claude/skills/[nom-skill]/SKILL.md` en suivant la convention frontmatter (name, description, argument-hint, user-invocable, context).
5. Créer un sous-dossier `examples/` ou `references/` si pertinent.

---

## Étape 9 : Poser les rituels de maintenance

**Quand :** infra complète.

**Process :**
1. Lire section 9 du guide.
2. Présenter la cadence de mise à jour par fichier.
3. Présenter les rituels fournis, un par un, avec la phrase à taper : `/done` en fin de chaque session (c'est celui qui garde le cerveau vivant), `/weekly-review` le vendredi, `/lint` une fois par mois, `/inbox-processor` quand l'Inbox déborde, `/daily-review` le soir pour ceux qui aiment.
4. Aider l'utilisateur à poser dans son agenda :
   - Rituel hebdo (vendredi, 10 min) : `/weekly-review`
   - Rituel mensuel (30 min) : `/lint`, puis relire `About-Me/my-company.md`
   - Rituel trimestriel (1h) : relire `Contexte/`
5. Lancer `/done` sur cette session d'installation : c'est la première entrée du journal.

---

## Erreurs à signaler activement

À chaque étape, surveiller et alerter si :
- L'utilisateur veut créer un skill sans avoir fait la tâche manuellement avant
- Le CLAUDE.md racine dépasse 200 lignes
- L'utilisateur veut donner accès à tout son disque dur (proposer un sandbox)
- Un fichier Contexte/ a été produit sans interview (résultats vagues garantis)
- Une même information (prix, offre) est écrite à deux endroits

---

## Checklist finale (à présenter quand l'utilisateur dit "j'ai fini")

```
Second cerveau : état final

Setup
- [ ] Claude Code installé
- [ ] Superfounder OS cloné dans un dossier dédié
- [ ] Arborescence vérifiée

Fondations (chargées chaque session)
- [ ] CLAUDE.md adapté (règles)
- [ ] About-Me/about-me.md
- [ ] About-Me/my-company.md
- [ ] About-Me/anti-ai-voice.md

Cerveau (chargé à la demande)
- [ ] Constitution-Identity.md
- [ ] Life-and-Work-Reality.md
- [ ] Goals-and-Direction.md
- [ ] Offer-Positioning.md
- [ ] Clients-Problems-and-Messages.md
- [ ] Expertise-Standards-and-Landmines.md
- [ ] Tone-and-Voice.md

Workspace
- [ ] Vos clients actifs dans Produit-Client/, chacun avec sa note
- [ ] Ressources/ et Branding/ initiés
- [ ] Une première page dans Veille/wiki/

Connectivité
- [ ] 3-5 MCP connectés et documentés dans CLAUDE.md
- [ ] Au moins 1 skill créé

Rituels
- [ ] /done lancé sur cette session
- [ ] Hebdo, mensuel, trimestriel posés dans l'agenda
```

---

## Et après

Quand la checklist est verte, propose la suite en une phrase : "Votre second cerveau est en place. Quand vous voulez, ouvrez `Vente/` et dites : Installe ma prospection. Ou `Marketing/` et dites : Installe mon contenu."

---

## Reprise de session

Si l'utilisateur invoque le skill avec un argument (ex: "étape 3" ou "contexte"), aller directement à l'étape demandée après avoir vérifié l'état des lieux.

Si l'utilisateur dit « reprends là où on s'était arrêté » sans précision, faire le diagnostic initial et déduire la prochaine étape logique.

---

## Référence

Le guide complet (avec tous les prompts d'interview verbatim) est dans `references/guide-complet.md`. Le lire **par section**, jamais en entier : chaque étape de ce skill correspond à une section précise du guide.
