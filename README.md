# Superfounder OS

**Le système d'exploitation de croissance d'un dirigeant B2B, avec l'IA en bras droit.**

[![Licence MIT](https://img.shields.io/badge/licence-MIT-yellow.svg)](LICENSE)
[![45 skills](https://img.shields.io/badge/skills-45-blue.svg)](#ce-que-contient-le-dépôt)
[![Claude Code](https://img.shields.io/badge/pour-Claude%20Code-black.svg)](https://www.anthropic.com/claude-code)
[![validate-skills](https://github.com/hugrowth98/superfounder-os/actions/workflows/validate.yml/badge.svg)](https://github.com/hugrowth98/superfounder-os/actions/workflows/validate.yml)

Le rôle d'un dirigeant tient en deux verbes : vendre, et construire des systèmes. Ce dépôt contient les systèmes. Un workspace Claude Code complet, prêt à ouvrir, avec 45 skills utilisés chaque semaine sur un vrai business : un second cerveau que l'IA lit avant chaque tâche, une machine de prospection, une machine de contenu.

Tout est en français, pensé pour un dirigeant qui ne code pas. Vous écrivez des phrases dans le chat, Claude fait le travail technique.

## Pourquoi ce dépôt

La plupart des entreprises utilisent l'IA sur le produit : coder plus vite, faire de la recherche, livrer. Presque jamais sur la distribution. Le problème, c'est que créer un produit devient une commodité. Ce qui fait la différence, c'est votre capacité à le mettre devant les bonnes personnes et à le vendre.

Superfounder OS met l'IA là où elle a le plus d'impact pour un dirigeant, en trois jours :

| Jour | Ce que vous installez | La phrase à taper | Où |
|---|---|---|---|
| **1. Le second cerveau** | Qui vous êtes, votre offre, vos clients, votre voix, dans des fichiers que Claude lit avant chaque tâche. Sans ça, l'IA plafonne à 50 %. Avec, vous démarrez à 80 %. | `Installe mon second cerveau` | racine |
| **2. La prospection** | Trouver, détecter un signal, trier, enrichir, écrire, envoyer, suivre. En 7 phrases, avec 25 skills. | `Installe ma prospection` | `Projects/Prospection/` |
| **3. Le contenu** | Veille, idéation, rédaction par format, hook, optimisation. 10 skills qui écrivent dans votre voix. | `Installe mon contenu` | `Projects/Contenu/` |

Chaque jour lit ce que le précédent a produit et n'interviewe que sur ce qui manque. Le détail de chaque jour est dans [docs/](docs/).

## Démarrer

```bash
git clone https://github.com/hugrowth98/superfounder-os.git MonOS
cd MonOS
claude
```

Puis, dans le chat : `Installe mon second cerveau`. Le dépôt est votre workspace. Il n'y a rien d'autre à installer.

Prérequis : [Claude Code](https://www.anthropic.com/claude-code) et un abonnement Claude payant. Pour la prospection, selon vos canaux : Unipile (LinkedIn), Crustdata (recherche), FullEnrich (emails), Lemlist (campagnes), Apify (scraping). Python 3.10 ou plus pour les scripts de prospection.

Vous avez déjà un workspace Claude Code ? `./install.sh --into ~/MonWorkspace` y ajoute les modules sans toucher à vos fichiers existants.

## Ce que contient le dépôt

```
superfounder-os/                  ← le dossier que Claude Code ouvre
├── CLAUDE.md                     la carte : règles, diagnostic du premier message, routage, rituels
├── ABOUT.ME/                     TOUJOURS chargé. Qui vous êtes. Change en années.
│   ├── about-me.md  my-company.md  anti-ai-voice.md
├── Contexte/                     À LA DEMANDE. La vérité unique sur l'offre, les clients, la voix. 7 fichiers.
├── Inbox/                        capture en vrac, vidée par inbox-processor
├── Intelligence/                 daily logs, sources brutes, wiki de connaissance durable
├── ressources-templates/         modèles transverses
├── Projects/
│   ├── Prospection/              jour 2 : CLAUDE.md copilote, contexte.md, GUIDE.md, 25 skills scopés
│   ├── Contenu/                  jour 3 : CLAUDE.md copilote, ressources/ (stratégie, posts, swipe file), 10 skills scopés
│   ├── Clients/  Strategie/      même patron : CLAUDE.md + input/ output/ ressources/
├── .claude/skills/               les 10 skills transverses (jour 1)
│   ├── installer-second-cerveau  done  daily-review  weekly-review  inbox-processor
│   ├── import  map-process  notes-permanentes  connect-mcp  find-skills
├── docs/                         jour-1, jour-2, jour-3
├── install.sh                    pour un workspace existant seulement
└── scripts/validate_skills.py    contrôle qualité, lancé en CI
```

## Comment c'est construit (et pourquoi)

Le dépôt applique les pratiques documentées de Claude Code pour la gestion du contexte. Si vous voulez adapter l'OS, gardez ces cinq règles.

1. **Une information vit à un seul endroit.** L'offre est dans `Contexte/Offer-Positioning.md`, nulle part ailleurs. Le `contexte.md` de la prospection et la `strategie-contenu.md` du contenu pointent dessus et ne gardent que ce qui leur est propre. Quand l'offre change, un seul fichier change.
2. **Trois vitesses de changement, trois couches.** `ABOUT.ME/` change en années et est importé dans le contexte à chaque session (`@ABOUT.ME/...` dans le CLAUDE.md racine). `Contexte/` change en trimestres et se charge à la demande. Le bloc ETAT d'un domaine change en semaines et est réécrit par `/done`.
3. **Les skills sont des procédures sans état.** Aucun skill ne contient de donnée sur vous. Ils lisent `Contexte/` et `ressources/` à chaque exécution. Pas de placeholders à remplacer, pas de recompilation quand votre positionnement bouge.
4. **Le contexte vit près de son usage.** Les 25 skills de prospection sont dans `Projects/Prospection/.claude/skills/`, les 10 de contenu dans `Projects/Contenu/.claude/skills/`. Claude Code ne les charge que quand vous travaillez dans ce dossier : la liste reste courte partout, et chaque dossier a son `CLAUDE.md` copilote de moins de 200 lignes.
5. **Une boucle d'écriture, ou le graphe pourrit.** `/done` en fin de session fait ruisseler les décisions dans le bloc ETAT du domaine et dans son `_journal.md`. Un contexte construit une fois et jamais réécrit est mort en trois semaines.

## Une journée type, une fois les trois jours faits

Le matin, vous ouvrez le workspace et demandez "on fait quoi aujourd'hui" : Claude lit les blocs ETAT de chaque domaine et propose. Vous travaillez dans un dossier, ses skills et son copilote se chargent seuls. Vous capturez en vrac dans `Inbox/`. Le soir, `/done` puis `/daily-review`. Le vendredi, `/weekly-review`. Une fois par trimestre, vous relisez `Contexte/`.

Le contenu nourrit la prospection (ceux qui commentent vos posts sont vos meilleurs prospects). La prospection nourrit les rendez-vous. Les rendez-vous nourrissent le contenu.

## Sécurité et données

- Les clés API vivent dans `Projects/Prospection/.env`, ignoré par git. Le dépôt ne contient que `.env.example`, vide.
- Aucun skill n'envoie d'invitation, de message ou de campagne sans un "oui" explicite de votre part.
- Vos fichiers personnels (`ABOUT.ME/`, `Contexte/`, `ressources/`, `_journal.md`) sont à vous. Si vous versionnez votre workspace, faites-le dans un dépôt privé.
- `scripts/validate_skills.py` tourne en CI sur chaque push : frontmatter des skills, absence de tirets cadratins, de clés API, de placeholders, taille des CLAUDE.md.

## Contribuer

Les pull requests sont bienvenues, en particulier des skills pour d'autres canaux ou d'autres outils. Lisez [CONTRIBUTING.md](CONTRIBUTING.md) et lancez le validateur avant d'envoyer.

## Auteur

Construit par [Hugo Dollfus](https://www.linkedin.com/in/hugo-dollfus/), fondateur de [Superfounder](https://www.superfounder.fr/). Chaque skill est utilisé sur son propre business et chez ses clients avant d'atterrir ici. Pour suivre les évolutions et les tutos : [Les Tutos d'Hugo](https://hugodollfus.substack.com/).

## Licence

[MIT](LICENSE). Utilisez, modifiez, redistribuez. Une mention est appréciée, pas obligatoire.
