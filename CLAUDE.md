# Superfounder OS

> Fichier lu par Claude Code au démarrage de chaque session, quel que soit le dossier.
> C'est la carte du workspace, pas une bibliothèque : il dit où sont les choses et quand les lire.

@ABOUT.ME/about-me.md
@ABOUT.ME/my-company.md
@ABOUT.ME/anti-ai-voice.md

## 1. Règles (toujours)

- Vouvoiement, ton direct et chaleureux, zéro jargon inutile. Français par défaut.
- Aucun tiret cadratin ni demi-cadratin, nulle part. Tiret simple, deux-points, virgule ou parenthèses.
- Une seule action à la fois. L'utilisateur n'est pas développeur : tu fais le travail technique, il répond aux questions.
- Rien ne part vers l'extérieur (message, invitation, campagne, email) sans un "oui" explicite.
- Jamais de contexte inventé. Si l'information manque, tu la demandes ou tu laisses vide.
- Tout livrable va dans le `output/` du bon domaine, nommé `Nom-Sujet_YYYY-MM-DD.ext`.

## 2. Premier message : diagnostiquer, puis proposer le bon jour

Avant de répondre au tout premier message d'une session, regarde discrètement l'état d'installation :

| Module | Test | Installé si |
|---|---|---|
| Jour 1, second cerveau | `ABOUT.ME/about-me.md` | ne contient plus de `[à remplir]` |
| Jour 2, prospection | `Projects/Prospection/contexte.md` et `.env` | sections remplies, au moins une clé présente |
| Jour 3, contenu | `Projects/Contenu/ressources/strategie-contenu.md` | sections remplies |

Puis :
- **Rien n'est installé** : souhaite la bienvenue en 3 phrases (ce que l'OS permet : un second cerveau que l'IA lit avant chaque tâche, une machine de prospection, une machine de contenu), et lance `installer-second-cerveau`.
- **Jour 1 fait, pas le jour 2** : propose "Installe ma prospection".
- **Jours 1 et 2 faits** : propose "Installe mon contenu".
- **Tout est installé** : lis les blocs ETAT des `Projects/*/CLAUDE.md`, résume en 3 lignes où en est chaque domaine, et propose la prochaine action la plus utile.

Les installeurs se lancent toujours par la même phrase : "Installe mon second cerveau", "Installe ma prospection", "Installe mon contenu". Chaque installeur lit ce que le précédent a produit et n'interviewe que sur ce qui manque.

## 3. Architecture

```
CLAUDE.md                   cette carte (chargée partout)
ABOUT.ME/                   qui vous êtes : chargé à chaque session via les imports ci-dessus
Contexte/                   la vérité unique sur l'offre, les clients, la voix : chargé à la demande (section 4)
Inbox/                      capture en vrac, vidée par inbox-processor
Intelligence/               daily logs, sources brutes (raw/), wiki de connaissance durable
ressources-templates/       modèles transverses (daily note, hooks, exemples)
Projects/<Domaine>/         un dossier par domaine, toujours : CLAUDE.md, _journal.md, input/ output/ ressources/
  Prospection/              jour 2, avec ses 25 skills scopés dans .claude/skills/
  Contenu/                  jour 3, avec ses 10 skills scopés dans .claude/skills/
  Clients/ Strategie/       livrables clients, réflexions de dirigeant
.claude/skills/             les 10 skills transverses (installeur jour 1, rituels, connect-mcp, find-skills)
docs/                       le parcours en 3 jours, un fichier par jour
```

Trois vitesses de changement, trois couches : `ABOUT.ME/` change en années, `Contexte/` en trimestres, le bloc ETAT d'un domaine en semaines. Une information vit à un seul endroit. Les dossiers de Projects ne redéfinissent jamais l'offre ou la voix : ils pointent vers `Contexte/`.

## 4. Routage du contexte (quoi charger selon la tâche)

| Tâche | Charger en plus d'ABOUT.ME |
|---|---|
| Rédiger quoi que ce soit de publié (post, newsletter, page, message) | `Contexte/Tone-and-Voice.md` |
| Prospection, messages, qualification | `Contexte/Offer-Positioning.md` + `Contexte/Clients-Problems-and-Messages.md` + `Projects/Prospection/contexte.md` |
| Contenu LinkedIn | `Contexte/Tone-and-Voice.md` + `Projects/Contenu/ressources/strategie-contenu.md` |
| Stratégie, offre, pricing, objectifs | `Contexte/Goals-and-Direction.md` + `Contexte/Offer-Positioning.md` + `Contexte/Life-and-Work-Reality.md` |
| Standards de qualité, erreurs passées | `Contexte/Expertise-Standards-and-Landmines.md` |
| Valeurs, décisions difficiles | `Contexte/Constitution-Identity.md` |

Les `CLAUDE.md` des dossiers de Projects se chargent seuls quand tu y travailles. Les skills de prospection et de contenu n'apparaissent que dans leur dossier : si l'utilisateur demande un post depuis la racine, va travailler dans `Projects/Contenu/`.

## 5. Routage des livrables (premier match gagne)

1. Post LinkedIn, calendrier, brief éditorial : `Projects/Contenu/output/`
2. Liste de prospects, messages, campagne, export : `Projects/Prospection/output/`
3. Livrable pour un client précis : `Projects/Clients/output/`, préfixé du nom du client
4. Réflexion de dirigeant (offre, pricing, vision, roadmap) : `Projects/Strategie/output/`
5. Source brute à exploiter (transcript, article, export) : `input/` du domaine concerné, ou `Intelligence/raw/`
6. Rien de tout ça : `Inbox/`, et on trie plus tard

Jamais de fichier à la racine. `ABOUT.ME/`, `Contexte/` et `.claude/` ne se modifient que sur demande explicite ou via un installeur.

## 6. Rituels

| Quand | Commande | Ce qu'elle fait |
|---|---|---|
| Fin de chaque session de travail | `/done` | extrait décisions et faits, réécrit le bloc ETAT du domaine, ajoute au `_journal.md` |
| Le soir | `/daily-review` | énergie, victoires, frictions, apprentissage, focus du lendemain |
| Le vendredi | `/weekly-review` | bilan, report des tâches, plan de la semaine suivante jour par jour |
| Quand l'Inbox déborde | `/inbox-processor` | route chaque item vers le bon dossier |
| Un gros lot à digérer (exports, PDF, notes) | `/import` | trie par passes, garde, extrait, résume ou archive |
| Une source qui mérite de durer | `/notes-permanentes` | l'intègre au wiki `Intelligence/` |
| Nouvel outil à brancher | `/connect-mcp` | installe le serveur MCP |
| "Y a-t-il un skill pour ça ?" | `find-skills` | cherche dans l'écosystème ouvert |
| Cartographier ses process | `/map-process` | par fréquence, pour décider où mettre l'IA |

Le bloc ETAT d'un `CLAUDE.md` de domaine est maintenu par `/done`. Ne pas l'éditer à la main.

## 7. Le bloc ETAT (format, dans chaque Projects/<Domaine>/CLAUDE.md)

```
<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : YYYY-MM-DD
## Priorités / en cours
## Décisions actées
## Prochaines étapes
- [ ] ...
<!-- ETAT:END -->
```
