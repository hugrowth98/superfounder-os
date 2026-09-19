# Superfounder OS

**Le système d'exploitation de croissance d'un dirigeant B2B, avec l'IA en bras droit.**

[![Licence MIT](https://img.shields.io/badge/licence-MIT-yellow.svg)](LICENSE)
[![45 skills](https://img.shields.io/badge/skills-45-blue.svg)](#ce-que-contient-le-dépôt)
[![Claude Code](https://img.shields.io/badge/pour-Claude%20Code-black.svg)](https://www.anthropic.com/claude-code)
[![validate-skills](https://github.com/hugrowth98/superfounder-os/actions/workflows/validate.yml/badge.svg)](https://github.com/hugrowth98/superfounder-os/actions/workflows/validate.yml)

Le rôle d'un dirigeant tient en deux verbes : vendre, et construire des systèmes. Ce dépôt contient les systèmes. Un workspace Claude Code complet, prêt à ouvrir, avec 47 skills utilisés chaque semaine sur un vrai business : un second cerveau que l'IA lit avant chaque tâche, une machine de prospection, une machine de contenu.

Tout est en français, pensé pour un dirigeant qui ne code pas. Vous écrivez des phrases dans le chat, Claude fait le travail technique.

## Pourquoi ce dépôt

La plupart des entreprises utilisent l'IA sur le produit : coder plus vite, faire de la recherche, livrer. Presque jamais sur la distribution. Le problème, c'est que créer un produit devient une commodité. Ce qui fait la différence, c'est votre capacité à le mettre devant les bonnes personnes et à le vendre.

Superfounder OS met l'IA là où elle a le plus d'impact pour un dirigeant, en trois modules :

| Module | Ce que vous installez | La phrase à taper | Où |
|---|---|---|---|
| **Le second cerveau** | Qui vous êtes, votre offre, vos départements, vos projets, vos clients, votre voix, dans des fichiers que Claude lit avant chaque tâche. Sans ça, l'IA plafonne à 50 %. Avec, vous démarrez à 80 %. | `Installe mon second cerveau` | racine |
| **La prospection (module GTM)** | Quatre masters de méthode (construire une liste, détecter des signaux, cold email, cold call) avec leurs sous-skills et leurs ressources (13 frameworks, 34 templates, 137 déclencheurs), et quatorze skills d'exécution qui appellent vos outils. Vous parlez en phrases simples, sans nommer d'outil. | `Installe ma prospection` | racine |
| **Le contenu** | Veille, idéation, rédaction par format, hook, optimisation. 10 skills qui écrivent dans votre voix. | `Installe mon contenu` | racine |

Le second cerveau se fait en premier. Les deux autres le lisent et n'interviewent que sur ce qui manque, dans l'ordre que vous voulez. Le détail de chaque module est dans [docs/](docs/).

## Démarrer

```bash
git clone https://github.com/hugrowth98/superfounder-os.git MonOS
cd MonOS
claude
```

Puis, dans le chat : `Installe mon second cerveau`. Le dépôt est votre workspace. Il n'y a rien d'autre à installer.

Prérequis : [Claude Code](https://www.anthropic.com/claude-code) et un abonnement Claude payant. Pour la prospection, selon vos canaux : Apify (scraping et signaux, par défaut), Unipile (LinkedIn), Crustdata (recherche par API), FullEnrich (emails et téléphones), Ocean.io (lookalikes), Lemlist (envoi), HubSpot (CRM). Un seul suffit pour démarrer. Python 3.10 ou plus pour les scripts de prospection.

Vous avez déjà un workspace Claude Code ? `./install.sh --into ~/MonWorkspace` y ajoute la structure et les skills sans toucher à vos fichiers existants.

## Claude Code, Codex ou OpenCode

Le dépôt fonctionne avec les trois, sans rien configurer. Claude Code lit `CLAUDE.md` et `.claude/skills`. Codex lit `AGENTS.md` et `.agents/skills`. OpenCode lit `AGENTS.md` et `opencode.json`. Les deux dossiers de skills sont des liens symboliques vers `10_Skills/` : sur Windows, activez le mode développeur avant de cloner, ou remplacez les liens par des copies (l'installeur le propose). Les trois phrases d'installation sont les mêmes partout.

## Ce que contient le dépôt

```
superfounder-os/            le dossier que Claude Code ouvre
├── CLAUDE.md               la carte : règles, diagnostic du premier message, arbre, départements, forme d'une fiche, routage, rituels
├── 00_Inbox/               capture en vrac, vidée par /inbox-processor ; _import/ pour /import
├── 01_About-Me/            TOUJOURS chargé. Qui vous êtes. Change en années.
│   ├── about-me.md  my-company.md  anti-ai-voice.md
├── 02_Contexte/            À LA DEMANDE. La vérité unique sur l'offre, les clients, la voix. 7 fichiers.
├── 03_Branding/            charte, logos, polices
├── 04_Projets/             une initiative avec une fin : un dossier, une note, des Étapes, archivé à la fin
├── 05_Departements/        les responsabilités continues, chacune avec sa fiche
│   ├── Strategie/  Marketing/ (LinkedIn, Newsletter, Video, Slides)  Go-to-Market/ (contexte.md, OUTILS.md, GARDE-FOUS.md, Ciblage, Listes-prospection, Signaux, Messages, Mailing)
│   ├── Vente/ (Propositions, Pipeline)  Produit/  Finance-Compta/
├── 06_Clients/             un dossier par client signé, avec sa note
├── 07_Meeting/             transcripts de calls : Clients/ Prospects/ Interne/ Autres/
├── 08_Ressources/          templates (projet, département, client, journal, réflexion, livrable), Veille/ (sources, wiki)
├── 09_Journal/             un fichier par jour écrit par /done, un par semaine par /weekly-review
├── 10_Skills/              la bibliothèque : 45 skills, une procédure par dossier (les masters GTM ont leurs sous-skills et ressources imbriqués)
├── 11_Archives/            terminé ou remplacé, gardé accessible
├── .claude/skills          lien vers 10_Skills/ (Claude Code)      .agents/skills  lien vers 10_Skills/ (Codex)
├── AGENTS.md  opencode.json  .env.example  install.sh  docs/  scripts/validate_skills.py
```

Une fiche (département, projet, client) tient en six sections : Mission, Périmètre et Objectif pour un département, Cadre, Étapes pour un projet ou un client, Où on en est, Key Notes. Vous écrivez les premières, `/done` fait vivre les dernières.

## Comment c'est construit (et pourquoi)

Le dépôt applique les pratiques documentées de Claude Code pour la gestion du contexte. Si vous voulez adapter l'OS, gardez ces six règles.

1. **Une information vit à un seul endroit.** L'offre est dans `Contexte/Offer-Positioning.md`, nulle part ailleurs. Le `contexte.md` de la prospection et la `strategie-contenu.md` du contenu pointent dessus et ne gardent que ce qui leur est propre. Quand l'offre change, un seul fichier change.
2. **Trois vitesses de changement, trois couches.** `About-Me/` change en années et est importé dans le contexte à chaque session. `Contexte/` change en trimestres et se charge à la demande. Le bloc ETAT d'une note de dossier change en semaines et est réécrit par `/done`.
3. **Les skills sont des procédures sans état.** Aucun skill ne contient de donnée sur vous. Ils lisent `Contexte/` et les ressources du dossier à chaque exécution. Pas de placeholders, pas de recompilation quand votre positionnement bouge.
4. **Une bibliothèque de skills, trois moteurs.** Les 45 skills sont dans `10_Skills/`, un dossier par skill. Claude Code les lit par le lien `.claude/skills`, Codex par `.agents/skills`, OpenCode par `opencode.json`. Vous ajoutez un skill dans `Skills/`, les trois le voient.
5. **Une note par dossier, pas un CLAUDE.md par dossier.** Le `CLAUDE.md` racine est la seule carte, sous 200 lignes. Chaque dossier de travail a une note du même nom, avec les mêmes sections partout : Rôle, Conventions, Organisation, Roadmap, ETAT, Reprise, Historique, Liens. Vous écrivez les trois premières, `/done` écrit les autres.
6. **Une boucle d'écriture, ou le graphe pourrit.** `/done` en fin de session fait ruisseler les décisions dans le journal du jour, la note du dossier et son `_log.md`. `/lint` une fois par mois vérifie que rien n'a dérivé. Un contexte construit une fois et jamais réécrit est mort en trois semaines.

## Une journée type, une fois les trois modules installés

Le matin, vous ouvrez le workspace et demandez "on fait quoi aujourd'hui" : Claude lit le journal de la veille et les blocs ETAT, et propose. Vous travaillez dans un dossier, vous ouvrez sa note, les 46 skills sont là. Vous capturez en vrac dans `Inbox/`. Le soir, `/done`. Le vendredi, `/weekly-review`. Une fois par mois, `/lint`. Une fois par trimestre, vous relisez `Contexte/`.

Le contenu nourrit la prospection (ceux qui commentent vos posts sont vos meilleurs prospects). La prospection nourrit les rendez-vous. Les rendez-vous nourrissent le contenu.

## Sécurité et données

- Les clés API vivent dans `.env` à la racine, ignoré par git. Le dépôt ne contient que `.env.example`, vide.
- Aucun skill n'envoie d'invitation, de message ou de campagne sans un "oui" explicite de votre part.
- Vos fichiers personnels (`About-Me/`, `Contexte/`, `Branding/`, `Journal/`, `Meeting/`, les `ressources/`, les `_log.md`) sont à vous. Si vous versionnez votre workspace, faites-le dans un dépôt privé.
- `scripts/validate_skills.py` tourne en CI sur chaque push : frontmatter des skills, absence de tirets cadratins, de clés API, de placeholders, taille du CLAUDE.md.

## Contribuer

Les pull requests sont bienvenues, en particulier des skills pour d'autres canaux ou d'autres outils. Lisez [CONTRIBUTING.md](CONTRIBUTING.md) et lancez le validateur avant d'envoyer.

## Auteur

Construit par [Hugo Dollfus](https://www.linkedin.com/in/hugo-dollfus/), fondateur de [Superfounder](https://www.superfounder.fr/). Chaque skill est utilisé sur son propre business et chez ses clients avant d'atterrir ici. Pour suivre les évolutions et les tutos : [Les Tutos d'Hugo](https://hugodollfus.substack.com/).

## Licence

[MIT](LICENSE). Utilisez, modifiez, redistribuez. Une mention est appréciée, pas obligatoire.
