---
type: instructions
status: active
date: 2026-09-18
maj: 2026-09-18
---

# AGENTS.md

> Consignes de travail pour Codex et OpenCode dans ce workspace, reprises du fichier `CLAUDE.md`. Elles s'appliquent à ce dossier et à ses sous-dossiers. Le `CLAUDE.md` reste la référence pour Claude Code : les deux fichiers disent la même chose.

## Démarrage de chaque session

Avant de travailler, lire intégralement les trois fichiers suivants, dont les chemins sont relatifs à la racine du workspace :

1. `About-Me/about-me.md`
2. `About-Me/my-company.md`
3. `About-Me/anti-ai-voice.md`

Ces références sont des instructions de lecture explicites : ne pas supposer que leur contenu est chargé automatiquement. Puis ouvrir la note du dossier concerné et les références utiles selon la section 5. Si un fichier manque, le signaler sans inventer son contenu.

Les règles adressées à "tu" dans ce fichier s'appliquent au moteur qui le lit, quel qu'il soit. Les commandes en `/nom` désignent des skills : dans Codex on les appelle avec `$nom`, dans OpenCode via l'outil skill. Un nom d'outil propre à Claude Code ne désigne pas une capacité disponible ailleurs : signaler une capacité manquante plutôt que de prétendre l'avoir exécutée.

## Où sont les skills

Les 46 skills sont dans `Skills/`, un dossier par skill avec un `SKILL.md`. Codex les trouve via `.agents/skills`, lien symbolique vers `Skills/`. OpenCode les trouve via `opencode.json` (`skills.paths`), et charge `About-Me/` via le même fichier. Un skill se lit et se modifie dans `Skills/`, jamais à travers un lien. Un skill ajouté dans `Skills/` est visible des trois moteurs sans rien d'autre à faire.

## 1. Règles (toujours)

- Vouvoiement, ton direct et chaleureux, zéro jargon inutile. Français par défaut.
- Aucun tiret cadratin ni demi-cadratin, nulle part. Tiret simple, deux-points, virgule ou parenthèses.
- Une seule action à la fois. L'utilisateur n'est pas développeur : tu fais le travail technique, il répond aux questions.
- Rien ne part vers l'extérieur (message, invitation, campagne, email) sans un "oui" explicite.
- Jamais de contexte inventé. Si l'information manque, tu la demandes ou tu laisses vide.
- Ce qui n'est pas écrit dans ce dossier n'existe pas pour toi. Une décision prise en conversation finit dans un fichier avant la fin de la session.

## 2. Premier message : diagnostiquer, puis proposer

Avant de répondre au tout premier message d'une session, regarde discrètement l'état d'installation :

| Module | Test | Installé si |
|---|---|---|
| Le second cerveau | `About-Me/about-me.md` | ne contient plus de `[à remplir]` |
| La prospection | `Vente/contexte.md` et `.env` à la racine | sections remplies, au moins une clé présente |
| Le contenu | `Marketing/LinkedIn/ressources/strategie-contenu.md` | sections remplies |

Puis :
- **Rien n'est installé** : souhaite la bienvenue en 3 phrases (ce que l'OS permet : un second cerveau que l'IA lit avant chaque tâche, une machine de prospection, une machine de contenu), et lance `installer-second-cerveau`.
- **Second cerveau fait, un module manque** : propose "Installe ma prospection" ou "Installe mon contenu", au choix de l'utilisateur. Les deux lisent le second cerveau et n'interviewent que sur ce qui manque.
- **Tout est installé** : lis le journal d'hier et d'aujourd'hui s'ils existent, puis le bloc ETAT des notes de `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/`. Résume en 3 lignes où en est chaque dossier et propose la prochaine action la plus utile.

Les installeurs se lancent toujours par la même phrase : "Installe mon second cerveau", "Installe ma prospection", "Installe mon contenu". Les 46 skills vivent dans `Skills/` à la racine et sont visibles depuis n'importe quel dossier.

## 3. Le rôle de chaque dossier

| Dossier | Ce qu'il contient | Ce qu'il ne contient pas |
|---|---|---|
| `About-Me/` | Qui vous êtes, votre boîte, vos règles d'écriture. Trois fichiers, chargés à chaque session. Change en années. | Rien de daté, rien de projet |
| `Contexte/` | La vérité unique sur votre marché et vos méthodes : identité, réalité, objectifs, offre, clients, standards, voix. Sept fichiers, chargés selon la tâche. Change en trimestres. | L'état d'un projet, un livrable |
| `Branding/` | Charte, logos, polices, brand book. La référence visuelle. | Les visuels produits (ils vont dans `Marketing/`) |
| `Ressources/` | Ce qui aide à produire mais n'est pas du savoir : templates, exemples, hooks, docs d'API. Transverse à tous les dossiers. | Les assets propres à un dossier (ils vont dans son `ressources/`) |
| `Inbox/` | Zone tampon. Ce qui arrive sans place définie. Vidé par `/inbox-processor`. | Un livrable fini, une source du wiki |
| `Journal/` | Un fichier par jour, écrit par `/done` : ce qui a été fait, décidé, appris. Un fichier par semaine pour le bilan. La mémoire chronologique. | Le détail d'un projet (il vit dans sa note de dossier) |
| `Veille/` | Ce qui vient de l'extérieur : `sources/` (le brut, immuable), `wiki/` (la connaissance distillée), `INDEX.md`, `LOG.md`. | La production de l'utilisateur |
| `Meeting/` | Les transcripts de calls, dans cinq dossiers : `Clients/` (Actuels, Coaching, Anciens-clients, Ateliers), `Events/` (Live, Challenge), `Prospects/`, `Interne/`, `Autres/`. Ce qui s'y décide ruisselle vers la note du client. | Le compte rendu envoyé (il va chez le client) |
| `Produit-Client/` | Un dossier par client et par produit, chacun avec sa note, son contexte, ses livrables. | Un post qui parle d'un client (il va dans `Marketing/`) |
| `Marketing/` | Tout ce qui fait venir : `LinkedIn/`, `Newsletter/`, `Mailing/`, `Event/`, `Video/`, `Slides/`. | Une propale, un message de prospection |
| `Vente/` | Tout ce qui convertit : `Listes-prospection/`, `Messages/`, `Propositions/`, `Pipeline/`. | Un contenu publié |
| `Strategie/` | Les réflexions de dirigeant : offre, pricing, positionnement, études, décisions structurantes. | Un livrable client |
| `Archives/` | Terminé ou inactif, gardé accessible. | Ce qui est encore en cours |

Zones protégées, modifiées seulement sur demande explicite ou via un installeur : `About-Me/`, `Contexte/`, `Branding/`, `Skills/`.

## 4. La forme d'un dossier de travail

**Règle de lecture : avant de travailler dans un dossier, ouvre sa note.** Elle porte le nom exact du dossier. Si l'utilisateur parle d'un client, d'un module ou d'une initiative sans nommer de fichier, la note est le point d'entrée.

```
Vente/
  Vente.md          LA NOTE DU DOSSIER : même nom que le dossier, lue avant tout travail dedans
  _log.md           une ligne par session, écrite par /done
  contexte.md       le profil de prospection (propre à Vente)
  sources/          ce qu'on reçoit : exports, briefs, transcripts
  ressources/       assets propres à ce dossier
  Listes-prospection/  Messages/  Propositions/  Pipeline/   sous-dossiers nommés par nature
  Campagne-Q4/      une initiative datée : son dossier, sa note, archivée à la fin
```

La note a toujours ces sections, dans cet ordre :

| Section | Qui l'écrit |
|---|---|
| Rôle, Conventions, Organisation | l'utilisateur. `/done` n'y touche jamais |
| Roadmap | l'utilisateur l'écrit, `/done` coche |
| Bloc ETAT (État actuel, Décisions actées, Prochaines étapes) | `/done` le réécrit entièrement |
| Reprise | `/done` : où on s'est arrêté, ce qui bloque, la première action |
| Historique | `/done` : une ligne par session, la plus récente en haut, lien vers le journal |
| Liens | `/done` : les wikilinks vers les entités liées |

Règle de résolution : quand tu modifies un fichier, la note à mettre à jour est celle du dossier parent le plus proche qui en a une. Deux niveaux maximum sous un dossier de travail. Jamais de fichier à la racine du workspace.

## 5. Routage du contexte (quoi charger selon la tâche)

| Tâche | Charger en plus d'About-Me |
|---|---|
| Rédiger quoi que ce soit de publié (post, newsletter, page, message) | `Contexte/Tone-and-Voice.md` |
| Prospection, messages, qualification | `Contexte/Offer-Positioning.md` + `Contexte/Clients-Problems-and-Messages.md` + `Vente/contexte.md` |
| Contenu LinkedIn | `Contexte/Tone-and-Voice.md` + `Marketing/LinkedIn/ressources/strategie-contenu.md` |
| Stratégie, offre, pricing, objectifs | `Contexte/Goals-and-Direction.md` + `Contexte/Offer-Positioning.md` + `Contexte/Life-and-Work-Reality.md` |
| Standards de qualité, erreurs passées | `Contexte/Expertise-Standards-and-Landmines.md` |
| Valeurs, décisions difficiles | `Contexte/Constitution-Identity.md` |
| Travail sur un client | la note de son dossier dans `Produit-Client/` |
| Visuel, marque | `Branding/` |

Plus, toujours : la note du dossier où tu travailles. Tu l'ouvres toi-même, elle ne se charge pas seule.

## 6. Routage des livrables (premier match gagne)

1. Post LinkedIn, carrousel, calendrier éditorial, brief de veille : `Marketing/LinkedIn/livrables/`
2. Édition de newsletter : `Marketing/Newsletter/`
3. Email à l'audience déjà inscrite (promo d'event, nurturing, annonce) : `Marketing/Mailing/`
4. Livrable d'un event (funnel, landing, trames, slides) : `Marketing/Event/<Event>/`
5. Vidéo publiée, pub : `Marketing/Video/`
6. Support visuel transverse, planche d'atelier : `Marketing/Slides/`
7. Liste de prospects, run de scraping ou d'enrichissement : `Vente/Listes-prospection/`
8. Message outbound, séquence, icebreaker, playbook d'appel : `Vente/Messages/`
9. Propale, devis : `Vente/Propositions/`
10. Import, export ou dédoublonnage CRM, liste de call : `Vente/Pipeline/`
11. Livrable pour un client ou un produit : `Produit-Client/<Nom>/livrables/`, préfixé du nom
12. Réflexion de dirigeant, étude, décision structurante : `Strategie/livrables/`
13. Rien de tout ça : `Inbox/`

Tie-breaker : le support final l'emporte sur le sujet. Un post qui annonce un event va dans LinkedIn, pas dans Event. Un email d'invitation à ce même event va dans Mailing. Une propale qui détaille l'offre va dans Vente, pas dans Produit-Client.

## 7. Routage des entrées

| Ce qui arrive | Où ça va |
|---|---|
| Transcript de call | `Meeting/Clients/` (sous-dossier Actuels, Coaching, Anciens-clients ou Ateliers), `Meeting/Events/` (Live, Challenge), `Meeting/Prospects/`, `Meeting/Interne/` ou `Meeting/Autres/` par mois, règle dans `Meeting/Meeting.md`, puis les décisions ruissellent vers la note du client |
| Article, vidéo, newsletter, veille | `Veille/sources/` |
| Idée, vocal, lien, fichier déposé sans contexte | `Inbox/` |
| Décision qui change une zone protégée (prix, offre, marque) | proposée en diff, jamais écrite directement |

## 8. Conventions

- Livrable daté : `Nom-Sujet_YYYY-MM-DD.ext`. Note de dossier : le nom exact du dossier. Journal : `Journal/YYYY-MM-DD.md` et `Journal/YYYY-Www.md`.
- Une entité (client, produit, personne) porte son nom canonique et se cite en `[[wikilink]]`.
- Une seule version visible d'un livrable. Les versions précédentes vont dans `Archives/`.
- Frontmatter sur toute note et tout livrable créé : `type`, `status`, `date`, `maj`.
- Une information vit à un seul endroit. L'offre est dans `Contexte/Offer-Positioning.md`, nulle part ailleurs. `Vente/contexte.md` et `Marketing/LinkedIn/ressources/strategie-contenu.md` pointent dessus et ne gardent que ce qui leur est propre.

## 9. Rituels

| Quand | Commande | Ce qu'elle fait |
|---|---|---|
| Fin de chaque session | `/done` | extrait décisions et faits, écrit le journal du jour, réécrit ETAT, Reprise et Historique de la note du dossier touché, ajoute une ligne à son `_log.md` |
| Une fois par mois | `/lint` | santé du workspace : notes manquantes, ETAT périmés, contradictions, frontmatter, versions à archiver |
| Le soir | `/daily-review` | énergie, victoires, frictions, focus du lendemain, dans le journal du jour |
| Le vendredi | `/weekly-review` | bilan de la semaine, plan de la suivante, dans `Journal/` |
| Quand l'Inbox déborde | `/inbox-processor` | route chaque item vers le bon dossier |
| Un gros lot à digérer | `/import` | trie par passes de 100 items |
| Une source qui mérite de durer | `/notes-permanentes` | une page dans `Veille/wiki/` |
| Nouvel outil à brancher | `/connect-mcp` | installe le serveur MCP |
| "Y a-t-il un skill pour ça ?" | `find-skills` | cherche dans l'écosystème ouvert |
| Cartographier ses process | `/map-process` | par fréquence, pour décider où mettre l'IA |

Une tâche, une session, puis `/done`. Le bloc ETAT d'une note est maintenu par `/done` : ne pas l'éditer à la main.

## 10. Le bloc ETAT (format, dans chaque note de dossier)

```
<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : YYYY-MM-DD
## Décisions actées
## Prochaines étapes
- [ ] ...
<!-- ETAT:END -->
```

## 11. Une bibliothèque de skills, trois moteurs

Les 46 skills vivent dans `Skills/`, un dossier par skill. `.claude/skills` (Claude Code) et `.agents/skills` (Codex) sont des liens symboliques vers `Skills/` ; `opencode.json` pointe dessus pour OpenCode et lui fait charger `About-Me/`. `AGENTS.md` reprend cette carte pour Codex et OpenCode, qui ne suivent pas les imports `@`. Un skill se lit et se modifie dans `Skills/`, jamais à travers un lien. Le `.env` des outils de prospection est à la racine du workspace.
