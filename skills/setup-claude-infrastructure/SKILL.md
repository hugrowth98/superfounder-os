---
name: setup-claude-infrastructure
description: Aide n'importe qui à construire son infrastructure Claude complète (CLAUDE.md + ABOUT.ME/ + 7 fichiers Contexte/ + structure Projects/ + MCP + premiers skills). Process étape par étape avec interviews 3-prompts pour chaque fichier stratégique. Se déclenche sur "construire mon infrastructure Claude", "créer mon cerveau IA", "setup workspace Claude", "infrastructure Claude Code", "monter mon second brain IA", "configurer Claude pour mon business", "créer mon ABOUT.ME", "fichiers de contexte Claude".
argument-hint: [optionnel : numéro d'étape pour reprendre où vous en étiez, ex: "étape 3" ou "contexte"]
user-invocable: true
context: main
---

# Setup Claude Infrastructure : Le skill qui te construit ton cerveau IA

**Objectif :** transformer Claude en assistant ultra-personnalisé qui connaît la vie, le business, les clients et la voix de l'utilisateur, et qui sait où ranger ce qu'il produit.

**Durée totale :** 4-8h, à étaler sur quelques jours.

**Architecture cible produite :**
```
votre-workspace/
├── CLAUDE.md                              ← GPS racine
├── ABOUT.ME/                              ← chargé chaque session
│   ├── about-me.md
│   ├── my-company.md
│   └── anti-ai-voice.md
├── Contexte/                              ← chargé à la demande
│   ├── Constitution-Identity.md
│   ├── Life-and-Work-Reality.md
│   ├── Goals-and-Direction.md
│   ├── Offer-Positioning.md
│   ├── Clients-Problems-and-Messages.md
│   ├── Expertise-Standards-and-Landmines.md
│   └── Tone-and-Voice.md
├── ressources-templates/
├── Intelligence/
├── Projects/[adapté au métier]/{input,output,ressources}
└── .claude/skills/
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

1. **Vérifier le contexte.** Lire la racine du dossier courant. Y a-t-il déjà un CLAUDE.md ? Un dossier ABOUT.ME/ ? Contexte/ ?
2. **Si workspace vierge** → proposer de démarrer à l'Étape 1 (setup).
3. **Si workspace partiellement construit** → afficher un état des lieux (✅/❌/🚧) et proposer la prochaine étape logique.
4. **Demander à l'utilisateur** :
   - Son métier / activité (sert à adapter les sous-dossiers Projects/)
   - Le temps qu'il a pour cette session (1h, demi-journée, étalé sur la semaine)
   - S'il a une préférence pour démarrer par une étape précise

Format de l'état des lieux :
```
État de votre infrastructure :
├── CLAUDE.md                                        ✅ Existe (X lignes)
├── ABOUT.ME/
│   ├── about-me.md                                  🚧 Existe mais vide
│   ├── my-company.md                                ❌ Manquant
│   └── anti-ai-voice.md                             ❌ Manquant
├── Contexte/
│   ├── Constitution-Identity.md                     ❌
│   ├── Life-and-Work-Reality.md                     ❌
│   ...

Prochaine étape recommandée : Étape 2 (compléter ABOUT.ME/about-me.md)
```

---

## Étape 1 : Setup initial (structure de dossiers)

**Quand :** workspace vierge ou structure incomplète.

**Process :**
1. Demander à l'utilisateur le nom du dossier parent souhaité (s'il n'est pas déjà dans le bon dossier).
2. Avertir : "Je vais créer une arborescence vide. Tu confirmes ?"
3. Créer la structure exacte décrite dans la section 2.3 du guide (`references/guide-complet.md`).
4. Confirmer avec un `tree -L 3` et passer la main.

**Adaptations selon le métier (à proposer) :**
- Coach indépendant : `Sales/`, `LinkedIn/`, `Coaching-Clients/`, `Contenu/`, `Stratégie/`
- Agence : `Sales/`, `Production/`, `Comptes-Clients/`, `Marketing/`, `RH/`
- Solo dev : `Open-Source/`, `Side-Projects/`, `Freelance/`, `Apprentissage/`
- Créateur de contenu : `YouTube/`, `Newsletter/`, `Twitter/`, `Sponsors/`, `Produits/`

Demander avant de figer.

---

## Étape 2 : Construire CLAUDE.md (le GPS racine)

**Quand :** structure créée, mais CLAUDE.md vide ou inexistant.

**Process :**
1. Lire la section 3 du guide (`references/guide-complet.md`).
2. Présenter le **Prompt de Cadrage** à l'utilisateur (section 3.1) : « Voilà comment on va construire ton CLAUDE.md. Je vais t'interviewer en 4-5 questions sur ton style de collaboration, puis générer le fichier. »
3. **Faire l'interview directement avec l'utilisateur** (une question à la fois, push back si réponse vague).
4. Quand toutes les questions sont couvertes, demander confirmation : « OK pour générer le CLAUDE.md ? »
5. Produire le fichier (max 200 lignes, sections numérotées).
6. **Test à froid obligatoire** : proposer à l'utilisateur d'ouvrir une nouvelle session et de tester avec « Comment tu vas ranger les choses qu'on produit ensemble ? ».

---

## Étape 3 : Construire ABOUT.ME/

**Quand :** CLAUDE.md prêt, ABOUT.ME/ vide.

**3 fichiers à produire dans cet ordre :**

### 3a. about-me.md (qui vous êtes)
- Lire section 4.1 du guide.
- Présenter le PROMPT 1 (cadrage) → confirmer la compréhension.
- Présenter le PROMPT 2 (interview, 20 questions sur 6 axes : identité, façon de travailler, ce qui est bon, ce qu'on déteste, règles, convictions).
- **Recommander à l'utilisateur** : « Fais ça en mode vocal pendant une marche de 30 min, c'est plus naturel ».
- Mener l'interview une question à la fois, push-back si vague.
- Présenter le PROMPT 3 (synthèse) → produire `ABOUT.ME/about-me.md` (max 1500 mots, structure imposée).

### 3b. my-company.md (snapshot business)
- Lire section 4.2 du guide.
- Même process 3-prompts (8 questions sur 4 axes : offre active, objectifs 90j, focus actuel, anti-objectifs).
- Produire `ABOUT.ME/my-company.md` daté (snapshot).
- Rappeler à l'utilisateur : à mettre à jour tous les 1-3 mois.

### 3c. anti-ai-voice.md (optionnel mais recommandé)
- Lire section 4.3 du guide.
- Pas d'interview : génération directe à partir du template.
- Demander à l'utilisateur s'il veut ajouter ses propres règles bannies.

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
8. **Demander relecture** : « Lis le fichier généré et dis-moi ce qui sonne juste / faux. On itère si besoin. »
9. Mettre à jour mentalement l'état des lieux et proposer le fichier suivant.

**Note importante sur Offer-Positioning.md :** la version dans `references/guide-complet.md` a été reconstituée fidèlement à partir du pattern strict des 6 autres prompts (la version Notion d'origine était partiellement coupée à l'export). Si l'utilisateur a accès à la version originale complète, lui proposer de la fournir.

---

## Étape 5 : Initialiser ressources-templates/, Intelligence/, Projects/

**Quand :** au moins quelques fichiers Contexte/ produits (pas obligé d'attendre les 7).

**Process :**
1. Lire section 6 du guide.
2. **ressources-templates/** : demander à l'utilisateur s'il a déjà des hooks, exemples de newsletters, templates de mails à déposer. Sinon créer les fichiers vides à remplir au fil de l'eau.
3. **Intelligence/** : créer la sous-structure (`daily-logs/`, `transcripts/`, `veille/`, `concurrents/`) et le fichier `daily-logs/_TEMPLATE.md`.
4. **Projects/** : valider/ajuster les sous-dossiers selon le métier. Présenter la convention de nommage `Nom-Sujet_YYYY-MM-DD.ext` et le tag projet multi-support `[lancement-X]_...`.

---

## Étape 6 : Connecter les MCP

**Quand :** workspace fonctionnel, l'utilisateur veut étendre.

**Process :**
1. Lire section 7 du guide.
2. Présenter la hiérarchie : MCP natifs > fichiers locaux > navigateur > Computer Use.
3. Demander à l'utilisateur ses 3-5 outils prioritaires.
4. Lui faire connecter les MCP via Claude Code (`/mcp`).
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
3. Aider l'utilisateur à poser dans son agenda :
   - Rituel hebdo (vendredi, 10 min)
   - Rituel mensuel (30 min)
   - Rituel trimestriel (1h)

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
- [ ] Dossier parent créé (sandbox dédié)
- [ ] Arborescence créée

Niveau 1 : Fondations (chargées chaque session)
- [ ] CLAUDE.md (testé à froid)
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

## Reprise de session

Si l'utilisateur invoque le skill avec un argument (ex: "étape 3" ou "contexte"), aller directement à l'étape demandée après avoir vérifié l'état des lieux.

Si l'utilisateur dit « reprends là où on s'était arrêté » sans précision, faire le diagnostic initial et déduire la prochaine étape logique.

---

## Référence

Le guide complet (avec tous les prompts d'interview verbatim) est dans `references/guide-complet.md`. Le lire **par section**, jamais en entier : chaque étape de ce skill correspond à une section précise du guide.
