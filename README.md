# Superfounder OS

**Le système d'exploitation de croissance d'un dirigeant B2B, avec l'IA en bras droit.**

[![Licence MIT](https://img.shields.io/badge/licence-MIT-yellow.svg)](LICENSE)
[![27 skills](https://img.shields.io/badge/skills-27-blue.svg)](#ce-que-contient-le-dépôt)
[![Claude Code](https://img.shields.io/badge/pour-Claude%20Code-black.svg)](https://www.anthropic.com/claude-code)
[![validate-skills](https://github.com/hugodollfus/superfounder-os/actions/workflows/validate.yml/badge.svg)](https://github.com/hugodollfus/superfounder-os/actions/workflows/validate.yml)

Le rôle d'un dirigeant tient en deux verbes : vendre, et construire des systèmes. Ce dépôt contient les systèmes. 27 skills pour Claude Code, utilisés chaque semaine sur un vrai business, pour installer un second cerveau, faire tourner une machine de prospection de bout en bout, et aller chercher les skills des autres quand ils existent déjà.

Tout est en français, pensé pour un dirigeant ou un commercial qui ne code pas. Vous écrivez des phrases dans le chat, Claude fait le travail technique.

## Pourquoi ce dépôt

La plupart des entreprises utilisent l'IA sur le produit : coder plus vite, faire de la recherche, livrer. Presque jamais sur la distribution. Le problème, c'est que créer un produit devient une commodité. Ce qui fait la différence, c'est votre capacité à le mettre devant les bonnes personnes et à le vendre.

Superfounder OS met l'IA là où elle a le plus d'impact pour un dirigeant :

| Levier | Ce que ça fait | Brique du dépôt |
|---|---|---|
| **L'IA installée en système** | Un second cerveau que Claude lit avant chaque tâche : qui vous êtes, votre offre, vos clients, votre voix. Sans ça, l'IA plafonne à 50 % de qualité. Avec, vous démarrez à 80 %. | `skills/setup-claude-infrastructure` |
| **La vente** | Trouver des prospects, détecter des signaux, trier, enrichir, écrire dans votre voix, envoyer, suivre les réponses. En 7 phrases. | `os-gtm/` |
| **L'extension** | Ne jamais repartir de zéro : chercher et installer les skills open source qui résolvent déjà votre problème. | `skills/find-skills` |

## Ce que contient le dépôt

```
superfounder-os/
├── skills/
│   ├── setup-claude-infrastructure/   le skill qui construit votre second cerveau (+ guide complet des prompts)
│   └── find-skills/                   découverte et installation de skills depuis skills.sh
├── os-gtm/                            l'OS de prospection : à ouvrir tel quel dans Claude Code
│   ├── CLAUDE.md                      le copilote GTM (lu automatiquement par Claude Code)
│   ├── GUIDE.md                       le parcours en 7 étapes
│   ├── contexte.md                    votre profil : offre, ICP, voix, garde-fous (rempli par l'installeur)
│   ├── .env.example                   les clés API attendues (copié en .env à l'installation)
│   └── .claude/skills/                25 skills de prospection
├── install.sh                         installation en une commande
├── scripts/validate_skills.py         contrôle qualité des skills (lancé en CI)
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE                            MIT
```

## Prérequis

- [Claude Code](https://www.anthropic.com/claude-code) installé, avec un abonnement Claude payant (Pro ou plus).
- Python 3.10 ou plus pour les scripts de l'OS-GTM (`openpyxl` et `pandas` uniquement pour le tri Excel de `lead-qualifier`).
- Pour l'OS-GTM, selon vos canaux : un compte [Unipile](https://www.unipile.com/) (LinkedIn), [Crustdata](https://crustdata.com/) (recherche d'entreprises et de personnes), [FullEnrich](https://fullenrich.com/) (emails et téléphones), [Lemlist](https://www.lemlist.com/) (campagnes email), [Apify](https://apify.com/) (scraping). Le skill `connecter-outils` vous guide pour brancher chacun depuis le chat.

## Installation

### Option A : en une commande (recommandé)

```bash
git clone https://github.com/hugodollfus/superfounder-os.git
cd superfounder-os
./install.sh --os-gtm ~/MonCerveauIA
```

`install.sh` copie les deux skills autonomes dans `~/.claude/skills` (disponibles dans tous vos projets) et dépose l'OS-GTM dans le workspace indiqué. Ajoutez `--local` pour installer les skills dans le projet courant plutôt que globalement.

### Option B : avec le Skills CLI

```bash
npx skills add hugodollfus/superfounder-os
```

### Option C : à la main

Copiez les dossiers de `skills/` dans `~/.claude/skills/` (ou `.claude/skills/` de votre projet). Copiez `os-gtm/` où vous voulez, renommez `.env.example` en `.env`, ouvrez le dossier dans Claude Code.

## Parcours recommandé

Les trois briques se branchent dans cet ordre. Chacune s'appuie sur la précédente.

### 1. Construire le second cerveau (4 à 8 h, étalées sur quelques jours)

Ouvrez Claude Code dans un dossier vide et tapez :

```
Construis mon infrastructure Claude.
```

Le skill fait un état des lieux, puis vous emmène étape par étape : l'arborescence, le `CLAUDE.md` (le GPS lu à chaque session), les trois fichiers `ABOUT.ME/` (qui vous êtes, votre entreprise, vos règles d'écriture anti-IA), puis les sept fichiers de `Contexte/` (identité, réalité de travail, objectifs, offre, clients et leurs mots exacts, standards, voix).

Chaque fichier suit le même rituel en trois prompts : cadrage, interview, synthèse. Claude vous pose une question à la fois et vous pousse quand la réponse est vague. Conseil : faites les interviews à la voix, en marchant.

Vous le faites une fois. Vous le réutilisez à vie. Tous les skills, y compris ceux de l'OS-GTM, viennent lire ce dossier avant d'agir.

### 2. Installer et faire tourner l'OS-GTM

Ouvrez le dossier `OS-GTM` dans Claude Code et écrivez :

```
Installe l'OS GTM.
```

Le skill `installer-gtm` lit votre second cerveau, pré-remplit votre profil (`contexte.md`), complète avec votre site web si besoin, vous fait valider, puis `connecter-outils` branche vos outils un par un. Vous ne touchez aucun fichier.

Ensuite, le parcours tient en 7 phrases :

| Étape | Vous écrivez | Skills déclenchés |
|---|---|---|
| 1. Trouver | "Trouve-moi 20 directeurs marketing de PME SaaS en France" | `trouver-personnes`, `trouver-entreprises`, `recherche-salesnav`, `export-salesnav`, `scraper-offres-emploi` |
| 2. Détecter un signal | "Regarde qui a commenté ce post" | `scraper-post`, `commentaires-publication`, `reactions-publication`, `publications-entreprise`, `profil-linkedin`, `profil-entreprise-linkedin`, `trouver-url-linkedin` |
| 3. Trier | "Qualifie cette liste selon mon ICP" | `qualifier-liste`, `lead-qualifier` |
| 4. Enrichir | "Trouve les emails de ces prospects" | enrichissement FullEnrich via `connecter-outils` |
| 5. Écrire | "Rédige un message pour chacun, dans ma voix" | `personnaliser-message`, `icebreaker-master` |
| 6. Lancer | "Envoie les invitations à cette liste" ou "Crée une campagne Lemlist avec ces messages" | `envoyer-invitation`, `envoyer-dm`, `creer-campagne-lemlist`, `envoyer-vers-lemlist`, `lancer-sequence-lemlist` |
| 7. Suivre | "Qui a répondu cette semaine ?" | `verifier-reponses`, `repondre-commentaires` |

**Garde-fous intégrés, non négociables** : maximum 30 invitations LinkedIn par jour, jamais de relance à quelqu'un qui a déjà répondu, rien ne part sans votre validation explicite, séquence par défaut invitation puis 2 jours, message 1, puis 3 jours, message 2.

Le détail de chaque skill est dans [os-gtm/GUIDE.md](os-gtm/GUIDE.md) et dans le tableau "Quel skill pour quel besoin" de [os-gtm/CLAUDE.md](os-gtm/CLAUDE.md).

### 3. Étendre avec find-skills

Demandez "y a-t-il un skill pour X ?" et le skill cherche sur [skills.sh](https://skills.sh/), vérifie la réputation de la source et le nombre d'installations, puis vous propose la commande d'installation. Vous ne réinventez que ce qui n'existe pas.

## Sécurité et données

- Les clés API vivent dans `os-gtm/.env`, ignoré par git. Le dépôt ne contient que `.env.example`, vide.
- Aucun skill n'envoie d'invitation, de message ou de campagne sans un "oui" explicite de votre part.
- Les fichiers d'état générés par les skills (compteurs, baselines, exports bruts) sont ignorés par git.
- Le script `scripts/validate_skills.py` refuse tout commit contenant une chaîne qui ressemble à une clé API. Il tourne en CI sur chaque push.

## Adapter les skills à votre voix

En l'état, les skills produisent du travail propre mais générique : ils ne vous connaissent pas encore. C'est exactement pour ça que le second cerveau vient en premier. Une fois vos fichiers de contexte en place, chaque skill devient le vôtre.

Pour aller plus loin, donnez vos fichiers de contexte à Claude et demandez-lui de relire chaque skill pour l'adapter à votre marché, votre offre et vos mots. Ne changez pas la méthode des skills. Modifiez uniquement ce qui les rend génériques.

## Contribuer

Les pull requests sont bienvenues, en particulier des skills de prospection pour d'autres outils ou d'autres canaux. Lisez [CONTRIBUTING.md](CONTRIBUTING.md) avant de proposer un changement, et lancez `python3 scripts/validate_skills.py` avant d'envoyer.

## Auteur

Construit par [Hugo Dollfus](https://www.linkedin.com/in/hugo-dollfus/), fondateur de [Superfounder](https://www.superfounder.fr/). Chaque skill est utilisé sur son propre business et chez ses clients avant d'atterrir ici.

Pour suivre les évolutions et les tutos qui vont avec : [Les Tutos d'Hugo](https://hugodollfus.substack.com/), la newsletter.

## Licence

[MIT](LICENSE). Utilisez, modifiez, redistribuez. Une mention est appréciée, pas obligatoire.
