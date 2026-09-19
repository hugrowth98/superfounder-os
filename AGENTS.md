---
type: instructions
status: active
date: 2026-09-18
maj: 2026-09-18
---

# AGENTS.md

> Consignes de travail pour Codex et OpenCode dans ce workspace, reprises du `CLAUDE.md`. Le `CLAUDE.md` reste la référence pour Claude Code : les deux fichiers disent la même chose.

## Démarrage de chaque session

Avant de travailler, lire intégralement, chemins relatifs à la racine du workspace :

1. `01_About-Me/about-me.md`
2. `01_About-Me/my-company.md`
3. `01_About-Me/anti-ai-voice.md`

Ces références sont des instructions de lecture explicites : ne pas supposer que leur contenu est chargé automatiquement. Puis ouvrir la note du dossier concerné et les références utiles selon la section 7. Si un fichier manque, le signaler sans inventer son contenu.

Les règles adressées à "tu" s'appliquent au moteur qui lit ce fichier. Les commandes en `/nom` désignent des skills : dans Codex on les appelle avec `$nom`, dans OpenCode via l'outil skill. Un nom d'outil propre à Claude Code ne désigne pas une capacité disponible ailleurs : signaler une capacité manquante plutôt que prétendre l'avoir exécutée.

## 1. Règles (toujours)

- Vouvoiement, ton direct et chaleureux, zéro jargon inutile. Français par défaut.
- Aucun tiret cadratin ni demi-cadratin, nulle part. Tiret simple, deux-points, virgule ou parenthèses.
- Une seule action à la fois. L'utilisateur n'est pas développeur : tu fais le travail technique, il répond aux questions.
- Rien ne part vers l'extérieur (message, invitation, campagne, email) sans un "oui" explicite.
- Jamais de contexte inventé. Si l'information manque, tu la demandes ou tu laisses vide.
- Jamais de suppression : ce qui n'a plus sa place va dans `11_Archives/`.
- Ce qui n'est pas écrit dans ce dossier n'existe pas pour toi. Une décision prise en conversation finit dans un fichier avant la fin de la session, via `/done`.

## 2. Premier message : diagnostiquer, puis proposer

Avant de répondre au tout premier message d'une session, regarde discrètement l'état d'installation :

| Module | Test | Installé si |
|---|---|---|
| Le second cerveau | `01_About-Me/about-me.md` | ne contient plus de `[à remplir]` |
| La prospection | `05_Departements/Go-to-Market/contexte.md` et `.env` à la racine | sections remplies, au moins une clé présente |
| Le contenu | `05_Departements/Marketing/LinkedIn/strategie-contenu.md` | sections remplies |

Puis :
- **Rien n'est installé** : souhaite la bienvenue en trois phrases (un second cerveau que l'IA lit avant chaque tâche, une machine de prospection, une machine de contenu) et lance `installer-second-cerveau`.
- **Second cerveau fait, un module manque** : propose "Installe ma prospection" ou "Installe mon contenu", au choix.
- **Tout est installé** : lis le journal d'hier et d'aujourd'hui s'ils existent, puis la section "Où on en est" des projets actifs et des départements. Résume en trois lignes et propose la prochaine action la plus utile.

Les trois installeurs se lancent par la même phrase : "Installe mon second cerveau", "Installe ma prospection", "Installe mon contenu".

## 3. L'arbre

| Dossier | Ce qu'il contient | Rythme |
|---|---|---|
| `00_Inbox/` | La capture : idée, lien, fichier déposé. Vidé par `/inbox-processor`. Gros lot dans `_import/` pour `/import`. | Jours |
| `01_About-Me/` | Qui vous êtes, votre boîte, vos règles d'écriture. Trois fichiers chargés à chaque session. | Années |
| `02_Contexte/` | La vérité unique sur votre marché et vos méthodes : identité, réalité, objectifs, offre, clients, standards, voix. Sept fichiers, chargés selon la tâche. | Trimestres |
| `03_Branding/` | Charte, logos, polices. | Années |
| `04_Projets/` | Une initiative avec un objectif et une fin : lancement, event, site, offre à structurer. Archivée quand ses Étapes sont cochées. | Semaines |
| `05_Departements/` | Les responsabilités continues de l'entreprise : Strategie, Marketing, Go-to-Market, Vente, Produit, Finance-Compta. | Jamais de fin |
| `06_Clients/` | Un dossier par client signé, avec sa note. | Mois |
| `07_Meeting/` | Les transcripts de calls : `Clients/`, `Prospects/`, `Interne/`, `Autres/`. | Jours |
| `08_Ressources/` | Ce qui aide à produire : `templates/`, exemples, docs d'outils, et `Veille/` (sources brutes, wiki). | Mois |
| `09_Journal/` | Un fichier par jour écrit par `/done`, un par semaine par `/weekly-review`. | Jours |
| `10_Skills/` | La bibliothèque de skills, lue par Claude Code, Codex et OpenCode. | Semaines |
| `11_Archives/` | Terminé ou remplacé, gardé accessible, à plat. | Rarement |

Zones protégées, modifiées seulement sur demande explicite ou via un installeur : `01_About-Me/`, `02_Contexte/`, `03_Branding/`, `10_Skills/`.

Projet, département ou client ? Un projet a une fin. Un département n'en a pas. Un client est une mission signée. Un prospect pas encore signé vit dans Vente. Un support réutilisable pour tous les clients vit dans Produit.

## 4. Les six départements

| Département | Ce qu'il fait | Ce qui n'y va pas |
|---|---|---|
| `Strategie/` | Offre, pricing, positionnement, études, décisions structurantes | Une propale, un livrable client |
| `Marketing/` | Ce que vous publiez : `LinkedIn/`, `Newsletter/`, `Video/`, `Slides/` | Un email à votre audience, une pub |
| `Go-to-Market/` | Ce qui amène un prospect à la conversation : `Listes-prospection/`, `Messages/`, `Mailing/`, `sources/`, et `contexte.md` (le profil de prospection) | Une propale, un post organique |
| `Vente/` | Ce qui transforme la conversation en contrat : `Propositions/`, `Pipeline/` | Une liste, un message outbound |
| `Produit/` | Vos offres et ce que vous livrez à tous vos clients : supports, templates, programmes | Le livrable d'un client précis |
| `Finance-Compta/` | Factures, prévisionnel, compta | Un devis non signé |

Frontière : le support final l'emporte sur le sujet. Un post qui annonce un event est du Marketing, l'email d'invitation du Go-to-Market, la propale de la Vente, et l'event lui-même est un projet. Vous pouvez renommer ou ajouter un département : même forme, une ligne de plus dans ce tableau.

## 5. La forme d'un dossier de travail

Tout projet, département et client a la même forme :

```
05_Departements/Vente/
  Vente.md          LA NOTE : même nom que le dossier, lue avant tout travail dedans
  _log.md           une ligne par session, écrite par /done
  Propositions/     un sous-dossier seulement quand une nature de fichier dépasse dix items
  Propale-Client_2026-05-22.md   sinon les fichiers sont à plat
```

**Règle de lecture : avant de travailler dans un dossier, ouvre sa note.** Si l'utilisateur parle d'un client, d'un département ou d'un projet sans nommer de fichier, la note est le point d'entrée.

Les sous-dossiers se nomment par ce qu'ils contiennent, jamais par une étape : pas de `livrables/`, `ressources/`, `input/`, `output/`. Seule exception : `sources/` pour le brut volumineux qu'on ne modifie pas.

La note est courte, six sections maximum :

| Section | Département | Projet | Client | Qui l'écrit |
|---|---|---|---|---|
| Mission | oui | oui | oui | l'utilisateur |
| Périmètre | trois à cinq responsabilités | | | l'utilisateur |
| Objectif | le chiffre, repris dans le frontmatter `objectif:` | | | l'utilisateur |
| Cadre | règles, outils, skills, sous-dossiers | contexte, contraintes | interlocuteurs, offre, conventions | l'utilisateur ; `/done` ajoute une décision datée en fin de section |
| Étapes | | cases | cases | l'utilisateur écrit, `/done` coche |
| Où on en est | oui | oui | oui | `/done` réécrit, cinq lignes max, avec le lien vers la dernière session |
| Key Notes | oui | oui | oui | `/done` complète les wikilinks |

`/done` ne réécrit jamais Mission, Périmètre, Objectif ni le texte de Cadre : il y corrige une ligne devenue fausse, et c'est tout. Un sous-dossier qui a sa propre note (comme `Contenu/LinkedIn/`) n'a que Mission, Cadre, Où on en est et Key Notes.

Règle de résolution : quand tu modifies un fichier, la note à mettre à jour est celle du dossier parent le plus proche qui en a une. Un fichier dans un projet remonte au projet, pas au département qui le porte.

## 6. Créer un document

1. **Une note** (projet, département, client) part toujours d'un template de `08_Ressources/templates/` : `projet.md`, `departement.md`, `client.md`. Jamais de zéro. Le dossier reçoit aussi un `_log.md`. Un nouveau projet s'ajoute à `04_Projets/Projets.md`.
2. **Un livrable** porte un frontmatter (`livrable.md`) : `type`, `status` (draft, final), `date`, `maj`, `client` si besoin, `tags`.
3. **Le journal** : `09_Journal/YYYY-MM-DD.md` depuis `journal-jour.md`, `09_Journal/YYYY-Www.md` depuis `journal-semaine.md`.
4. **Une réflexion** de dirigeant : `reflexion.md`, rangée dans `05_Departements/Strategie/`.
5. **Nommage** : `Nom-Sujet_YYYY-MM-DD.ext`. Un projet daté prend sa date dans son nom (`Lancement-2026-10`). Une entité porte son nom canonique et se cite en `[[wikilink]]`.
6. **Une seule version visible** d'un livrable. Les précédentes vont dans `11_Archives/`.
7. **Un projet multi-support** préfixe ses fichiers d'un tag commun, par exemple `[lancement]_`.
8. Jamais de livrable à la racine. Seuls `CLAUDE.md`, `AGENTS.md`, `opencode.json` et `.env` y vivent.

## 7. Routage du contexte (quoi charger selon la tâche)

| Tâche | Charger en plus d'About-Me et de la note du dossier |
|---|---|
| Rédiger quoi que ce soit de publié (post, newsletter, page, message) | `02_Contexte/Tone-and-Voice.md` |
| Prospection, messages, qualification | `02_Contexte/Offer-Positioning.md` + `02_Contexte/Clients-Problems-and-Messages.md` + `05_Departements/Go-to-Market/contexte.md` |
| Contenu LinkedIn | `02_Contexte/Tone-and-Voice.md` + `05_Departements/Marketing/LinkedIn/strategie-contenu.md` |
| Stratégie, offre, pricing, objectifs | `02_Contexte/Goals-and-Direction.md` + `02_Contexte/Offer-Positioning.md` + `02_Contexte/Life-and-Work-Reality.md` |
| Standards de qualité, erreurs passées | `02_Contexte/Expertise-Standards-and-Landmines.md` |
| Valeurs, décisions difficiles | `02_Contexte/Constitution-Identity.md` |
| Travail sur un client | sa note dans `06_Clients/<Client>/` |
| Visuel, marque | `03_Branding/` |

## 8. Routage des livrables (premier match gagne)

1. Post LinkedIn, carrousel, calendrier éditorial, brief de veille : `05_Departements/Marketing/LinkedIn/`
2. Édition de newsletter : `05_Departements/Marketing/Newsletter/`
3. Vidéo publiée, pub vidéo : `05_Departements/Marketing/Video/`
4. Support visuel d'atelier ou de live : `05_Departements/Marketing/Slides/`
5. Email à l'audience inscrite (promo, nurturing, annonce) : `05_Departements/Go-to-Market/Mailing/`
6. Liste de prospects, run de scraping ou d'enrichissement : `05_Departements/Go-to-Market/Listes-prospection/`
7. Message outbound, séquence, icebreaker, playbook d'appel : `05_Departements/Go-to-Market/Messages/`
8. Propale, devis, email d'envoi : `05_Departements/Vente/Propositions/`
9. Import, export ou dédoublonnage CRM, liste de call : `05_Departements/Vente/Pipeline/`
10. Support réutilisable pour tous les clients : `05_Departements/Produit/`
11. Réflexion de dirigeant, étude, décision structurante : `05_Departements/Strategie/`
12. Facture, prévisionnel : `05_Departements/Finance-Compta/`
13. Livrable d'un projet (landing, trame, séquence d'inscription) : `04_Projets/<Projet>/`, préfixé du tag du projet
14. Livrable pour un client signé : `06_Clients/<Client>/`, préfixé du nom du client
15. Rien de tout ça : `00_Inbox/`

## 9. Routage des entrées

| Ce qui arrive | Où ça va |
|---|---|
| Transcript de call | `07_Meeting/`, selon la règle de `07_Meeting/Meeting.md`, puis les décisions ruissellent vers la note du client ou du prospect |
| Article, vidéo, newsletter, veille | `08_Ressources/Veille/sources/`, puis `/notes-permanentes` si ça mérite une page de wiki |
| Idée, lien, fichier déposé sans contexte | `00_Inbox/` |
| Décision qui change une zone protégée (prix, offre, marque, façon de travailler) | proposée en diff, jamais écrite directement |

## 10. Rituels

Lire `10_Skills/<nom>/SKILL.md` avant d'appliquer un rituel.

| Quand | Commande | Ce qu'elle fait |
|---|---|---|
| Fin de session | `/done` | extrait décisions, faits, préférences, contradictions, ressources ; écrit le journal du jour ; réécrit Où on en est, date les décisions dans Cadre, coche les Étapes ; ajoute une ligne au `_log.md` ; propose l'archivage d'un projet fini |
| Le vendredi | `/weekly-review` | bilan, report des cases non cochées, plan de la semaine jour par jour |
| Le soir, pour ceux qui aiment | `/daily-review` | énergie, victoires, frictions, focus du lendemain |
| Inbox pleine | `/inbox-processor` | route chaque item vers un projet, un département, un client, les ressources ou l'archive |
| Gros lot à digérer | `/import` | trie par passes avec sous-agents, quatre verdicts |
| Une fois par mois, ou avant de reprendre un dossier | `/lint` | santé du workspace ; avec un dossier en argument, audit de son contexte |
| Source qui mérite de durer | `/notes-permanentes` | une page dans `08_Ressources/Veille/wiki/` |
| Tâche faite trois fois à la main | `/create-skill` | en fait un skill dans `10_Skills/` |
| Cartographier ses process | `/map-process` | par fréquence, pour décider où mettre l'IA |
| Nouvel outil | `/connect-mcp` | installe le serveur MCP |

Le ruissellement de `/done` : le journal (direct), la note du dossier (direct), son `_log.md` (direct), puis `01_About-Me/` et `02_Contexte/` en diff validé. En cas de contradiction entre un fichier et la conversation, l'info la plus récente gagne. Une tâche, une session, puis `/done`.

## 11. Une bibliothèque de skills, trois moteurs

Les skills vivent dans `10_Skills/`, un dossier par skill. `.claude/skills` (Claude Code) et `.agents/skills` (Codex) sont des liens symboliques vers `10_Skills/`. `opencode.json` pointe dessus pour OpenCode et lui fait charger `01_About-Me/`. `AGENTS.md` reprend cette carte pour Codex et OpenCode, qui ne suivent pas les imports `@`. Un skill se lit et se modifie dans `10_Skills/`, jamais à travers un lien. Le `.env` des outils de prospection est à la racine.
