# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

## [5.2.0] - 2026-09-19

Audit de cohérence du module GTM (20 bloquants, 12 doublons, 30 contradictions de chiffres corrigés) et tout en CLI.

### Ajouté
- Lemlist et Ocean.io par l'API en CLI, le MCP devient optionnel : `envoyer-sequence/scripts/envoyer_lemlist.py` (filtre, crée ou choisit la campagne, pousse les leads avec leurs variables, `--lancer`, `--pauser`, `--lister`), `verifier_reponses.py` lit les réponses email par l'API, `trouver-lookalikes/scripts/trouver_lookalikes.py` (aperçu gratuit puis recherche par lots de 10, 0,2 crédit par résultat).
- `enrichir-entreprise --posts` et `enrichir-personne --posts` (5 derniers posts, Unipile), `enrichir-entreprise --techno --techno-source predictleads --recentes-jours N`, `scraper-engagement --mes-posts N`, `detecter_signal.py --verification` et `--par-cible` sur les personnes, `dedoublonner --exclure-crm` et `--max-par-entreprise N`.
- Vocabulaires fixés dans `docs/conventions-gtm.md` section 8 : `email_statut` (valeurs FullEnrich), `seniorite`, `categorie_titre`, `tier`, `chaleur`, `signal_type` (une valeur canonique par signal), colonnes de réponse, `source`.
- Le validateur `scripts/valider_gtm.py` bannit "Apollo", les références périmées et les formules de félicitation dans les templates, et confronte tout actor cité à `OUTILS.md`.

### Changé
- Les runs de signaux vont dans `05_Departements/Go-to-Market/Signaux/` (`detecter-signaux_<type>-<source>-<sujet>_<date>.csv`) ; `qualifier-liste` écrit un seul fichier (toutes les lignes, colonne `exclu`) plus une copie des exclues ; préfixes `enrichir-entreprise_techno_` et `enrichir-entreprise_pubs_`.
- Fenêtres de fraîcheur alignées sur `detecter-signaux/ressources/fenetres-fraicheur.md` dans tout le module ; limites d'envoi alignées sur `GARDE-FOUS.md` (30 invitations, 50 DM, 100 interactions, note 300 caractères, 3 relances max tous canaux, chauffe 3 semaines, rebond alerte 3 % arrêt 5 %, catch-all 20 %, opt-out 48 h) ; séquence multicanal de référence LinkedIn J0, email J+2, email J+5, LinkedIn J+7, téléphone J+9 à J+12 ; email seul 3 emails max.
- Propriétaires uniques : no-show dans `cold-call`, nomination dans `changement-poste`, IPO dans `levee-fonds`, client d'un concurrent dans `signaux-concurrents` ; ouvertures et clics d'email retirés du barème ; abonnés d'une page retirés (non listables) ; le signal brut ne s'écrit plus dans aucun template.
- Colonnes citées par les sous-skills alignées sur celles que les scripts écrivent ; scopes HubSpot complétés (deals, notes, tâches).

## [5.1.0] - 2026-09-19

Deux sources optionnelles pour les signaux.

### Ajouté
- PredictLeads et TheirStack comme secours du verbe detecter_signal, par le même script (`--source predictleads`, `--source theirstack`) : événements d'entreprise (expansion, partenariat, lancement, nomination, rachat), levées, offres actives, intent (recrute et utilise une techno), offres filtrées par techno citée. Nouveaux types `events` et `intent`. Aussi dans `scraper-offres-emploi` (`--source predictleads|theirstack`) et `enrichir-entreprise --techno --source predictleads` (détections datées, `--recentes-jours`).
- Clients `PredictLeads` et `TheirStack` dans `10_Skills/_commun/gtm_common.py`, tests dans `connecter-outils` (`--outil predictleads|theirstack`), ligne `signaux_secours:` dans `OUTILS.md`, clés dans `.env.example`.

## [5.0.0] - 2026-09-19

Le module GTM : la prospection reconstruite en méthode et exécution séparées.

### Ajouté
- Quatre masters de méthode dans `10_Skills/` : `construire-liste` (8 sous-skills), `detecter-signaux` (8 sous-skills, barème de signaux, 137 déclencheurs, 11 plays), `cold-email` (9 sous-skills, 13 frameworks, 34 templates, relecteurs, infra email), `cold-call` (5 sous-skills sur la méthode d'appel en 5 temps). Chaque master route vers ses sous-skills, chaque sous-skill décrit le travail en verbes.
- Quatorze skills d'exécution, un par verbe, avec scripts Python (`--help`, `--dry-run`, coût annoncé) et une bibliothèque commune `10_Skills/_commun/` : `trouver-entreprises`, `trouver-lookalikes`, `trouver-personnes`, `enrichir-personne`, `enrichir-entreprise` (`--techno`, `--pubs`), `trouver-email`, `trouver-telephone`, `scraper-offres-emploi`, `scraper-engagement`, `qualifier-liste`, `dedoublonner`, `crm`, `envoyer-sequence`, `verifier-reponses`.
- `installer-gtm` (onboarding en 8 phases : offre, ICP en 3 couches scoré sur 100, personas ATL et BTL, 5 signaux prioritaires, canaux, outils, validation, premier run) remplace `installer-prospection`. `connecter-outils` étendu à 7 outils.
- Dans `05_Departements/Go-to-Market/` : `OUTILS.md` (quel outil fait quel verbe, priorité Apify ou API, canal LinkedIn), `GARDE-FOUS.md`, `Ciblage/` (décisionnaires par taille, requêtes booléennes, mots-clés d'exclusion), `Signaux/`. `contexte.md` réécrit : il traduit `02_Contexte/` en critères de prospection, sans le recopier.
- `docs/prospection.md` (mode d'emploi du module) et `docs/conventions-gtm.md` (comment les skills GTM sont écrits), `scripts/valider_gtm.py`.

### Changé
- Stack fermée à 7 outils : Apify par défaut pour tout scraping et tout signal, Unipile pour le compte LinkedIn, Crustdata en secours API, FullEnrich seul pour l'enrichissement contact, Ocean.io pour les lookalikes, Lemlist pour l'envoi, HubSpot pour le CRM.
- `.env.example` couvre les 7 outils, les cookies Sales Navigator et les limites d'envoi.

### Archivé
- Les 22 skills de prospection v3 (Crustdata en dur, sans orchestrateur) dans `11_Archives/skills-prospection-v3/`, avec l'ancien `contexte.md` et l'ancien guide.

## [4.0.0] - 2026-09-18

Le second cerveau version 4 : douze dossiers numérotés, projets, départements, clients, fiches courtes.

### Changé
- Arbre à plat et numéroté : `00_Inbox` à `11_Archives`. `Marketing/` et `Vente/` deviennent six départements dans `05_Departements/` (Strategie, Marketing, Go-to-Market, Vente, Produit, Finance-Compta). `Produit-Client/` devient `06_Clients/`. `Veille/` rejoint `08_Ressources/`. Les skills vivent dans `10_Skills/`.
- Un projet (initiative avec une fin) vit dans `04_Projets/` et part en archive quand ses Étapes sont cochées. Un département n'a pas de fin. Un client est une mission signée.
- Fin des sous-dossiers par étape (`livrables/`, `ressources/`, `input/`, `output/`) : fichiers à plat, sous-dossier par nature seulement au-delà d'une dizaine d'items. `sources/` reste pour le brut volumineux.
- Fiches courtes, six sections maximum : Mission, Périmètre, Objectif (frontmatter `objectif:`), Cadre avec décisions datées, Étapes, Où on en est, Key Notes. Plus de bloc ETAT, de Reprise ni d'Historique : l'historique vit dans `_log.md` et le journal.
- Sept templates dans `08_Ressources/templates/` : projet, departement, client, journal-jour, journal-semaine, reflexion, livrable.
- `/done` réécrit Où on en est, date les décisions dans Cadre, coche les Étapes, propose l'archivage d'un projet fini. `/lint` gagne un dixième contrôle : l'audit de contexte d'un dossier (contradictions, répétitions, obsolète, manques, mal rangé). `/inbox-processor`, `/import` et `/weekly-review` suivent la nouvelle carte.
- `installer-second-cerveau` : une étape pour valider la fiche de chaque département et créer les premiers projets, avant les clients.
- `07_Meeting/` simplifié : Clients, Prospects, Interne, Autres.
- Imports `@` du `CLAUDE.md` avec l'espace échappé (`@01_About-Me/...`), seule forme qui charge.

### Ajouté
- `/create-skill` : transformer une tâche faite trois fois à la main en skill, avec cadrage, étapes, test et écriture du SKILL.md.

### Retiré
- `Marketing/Event/` : un event est un projet dans `04_Projets/`.

## [3.2.0] - 2026-09-18

Une bibliothèque de skills, trois moteurs : Claude Code, Codex, OpenCode.

### Changé (rupture avec 3.1)
- **Les 46 skills vivent dans `Skills/`**, un dossier par skill, à la racine. Plus de skills scopés dans `Vente/.claude/skills/` ni `Marketing/.claude/skills/` : ils sont visibles depuis n'importe quel dossier, et "Installe ma prospection" ou "Installe mon contenu" se tapent depuis la racine.
- `.claude/skills` (Claude Code) et `.agents/skills` (Codex) sont des liens symboliques vers `Skills/`, versionnés. Sur Windows sans mode développeur, l'installeur propose des copies.
- Le `.env` des outils de prospection passe de `Vente/.env` à la racine du workspace. Les scripts le trouvent d'eux-mêmes.

### Ajouté
- `AGENTS.md` : la carte du `CLAUDE.md` reprise pour Codex et OpenCode, avec la lecture explicite d'`About-Me/` (ils ne suivent pas les imports `@`).
- `opencode.json` : charge `About-Me/` et pointe `skills.paths` sur `./Skills`.
- Section 11 du `CLAUDE.md`, section du README, entrée dans le validateur et `install.sh`.

## [3.1.0] - 2026-09-17

`Meeting/` se range par relation, plus par mois.

### Changé
- **`Meeting/` a cinq dossiers** : `Clients/` (sous-dossiers `Actuels/<Nom>/`, `Coaching/<Nom>/`, `Anciens-clients/<Nom>/`, `Ateliers-cold-call/`, `Ateliers-collectifs/`), `Events/` (`Live/`, `Challenge/`, vos events marketing), `Prospects/YYYY-MM/`, `Interne/YYYY-MM/`, `Autres/YYYY-MM/`. La règle de routage en huit étapes, premier match gagne, est dans `Meeting/Meeting.md`. Un prospect passe dans `Clients/` au troisième call ou dès qu'un atelier ou un onboarding est planifié ; un dossier terminé glisse dans `Anciens-clients/` tel quel.
- `CLAUDE.md`, `README.md`, `/inbox-processor` et `installer-second-cerveau` pointent vers le nouveau routage.

## [3.0.0] - 2026-09-16

Une seule structure, pour votre workspace comme pour ceux de vos clients. Le parcours en trois jours devient trois modules installables dans l'ordre que vous voulez, une fois le second cerveau en place.

### Changé (rupture avec 2.x)
- **Rangement à plat par fonction**, plus de `Projects/` ni de `input/ output/ ressources` imbriqués : `About-Me/`, `Contexte/`, `Branding/`, `Ressources/`, `Inbox/`, `Journal/`, `Veille/`, `Meeting/`, `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/`, `Archives/`.
- **Une note par dossier de travail**, du même nom que le dossier (`Vente/Vente.md`) : rôle, conventions, organisation, bloc ETAT, reprise, historique. Elle remplace le `CLAUDE.md` de sous-dossier. Un `_log.md` par dossier, une ligne par session.
- **`Journal/`** remplace `Intelligence/Daily logs/` : un fichier par jour, écrit par `/done`, un par semaine par `/weekly-review`. Le template à emojis disparaît.
- **`Veille/`** remplace `Intelligence/` : `sources/` (le brut), `wiki/` (la connaissance), `INDEX.md`, `LOG.md`.
- `Projects/Prospection/` devient `Vente/` avec quatre sous-dossiers typés (`Listes-prospection/`, `Messages/`, `Propositions/`, `Pipeline/`). Les 25 skills restent scopés dans `Skills/`.
- `Projects/Contenu/` devient `Marketing/` avec sept briques (`LinkedIn/`, `Newsletter/`, `Mailing/`, `Event/`, `Video/`, `Slides/`, `Site-vitrine/` à créer au besoin). Les 10 skills restent scopés dans `Skills/`, les ressources de contenu vivent dans `Marketing/LinkedIn/ressources/`.
- `Projects/Clients/` devient `Produit-Client/`, `Projects/Strategie/` devient `Strategie/`.
- Plus de notion de jour 1, 2, 3. Les trois phrases restent : "Installe mon second cerveau", "Installe ma prospection", "Installe mon contenu". Les deux dernières lisent le second cerveau et n'interviewent que sur ce qui manque.
- `/done` réécrit sur trois niveaux : le journal du jour, la note du dossier touché (ETAT, Reprise, Historique), son `_log.md`. Il propose un diff pour `About-Me/`, `Contexte/` et `Branding/` au lieu d'y écrire.
- `docs/` : un fichier par module, sans numéro de jour.

### Ajouté
- `/lint` : neuf contrôles de santé du workspace (notes manquantes, ETAT périmés, contradictions, frontmatter, versions non archivées, fichiers à la racine, tirets cadratins, chemins morts, dossiers orphelins). Lecture seule jusqu'à validation.
- `Ressources/templates/` : `note-de-dossier.md`, `note-de-dossier-client.md`, `journal-jour.md`.
- `Branding/`, `Meeting/`, `Archives/` avec leur note.

## [2.0.0] - 2026-09-11

Refonte complète : le dépôt devient un workspace Claude Code prêt à ouvrir, structuré selon les pratiques documentées de gestion du contexte (skills scopés par dossier, CLAUDE.md imbriqués, imports, une vérité par information, lecture du contexte à l'exécution).

### Changé (rupture avec 1.x)
- Le dépôt EST le workspace : `git clone`, ouvrir, "Installe mon second cerveau". Plus de copie de skills dans `~/.claude`.
- Les trois installeurs partagent la même nomenclature et la même phrase : `installer-second-cerveau` (ex setup-claude-infrastructure), `installer-prospection` (ex installer-gtm), `installer-contenu` (ex linkedin-system-installer). Chacun lit ce que le précédent a produit.
- L'OS-GTM devient `Projects/Prospection/`, ses 25 skills sont scopés à ce dossier. `contexte.md` ne contient plus que ce qui est propre à la prospection et pointe vers `Contexte/` pour l'offre, la cible et la voix.
- Le pack LinkedIn devient `Projects/Contenu/`, ses 10 skills sont scopés à ce dossier. Le mécanisme de placeholders (`apply_profile.py` et jetons entre doubles accolades) est supprimé : les skills lisent `Contexte/` et `ressources/` à chaque exécution. Les 7 fichiers-gabarits de références sont consolidés en 3 fichiers de `ressources/` (stratégie, posts de référence, swipe file).
- `linkedin-interview-2` devient `linkedin-interview` et range ses pépites dans `Projects/Contenu/ressources/banque-vecu.md`.
- `install.sh` ne sert plus qu'à ajouter les modules à un workspace existant (`--into`).

### Ajouté
- Les 8 skills du second cerveau, à la racine : `done`, `daily-review`, `weekly-review`, `inbox-processor`, `import`, `map-process`, `notes-permanentes`, `connect-mcp`.
- Le CLAUDE.md racine orchestrateur : diagnostic de l'état d'installation au premier message, routage du contexte, routage des livrables, rituels, imports d'ABOUT.ME.
- Le squelette complet : `ABOUT.ME/` et `Contexte/` avec gabarits, `Inbox/`, `Intelligence/` (schéma du wiki, INDEX, LOG), `Projects/{Clients,Strategie}/` avec leur CLAUDE.md.
- `docs/` : un fichier par jour du parcours.
- `anti-ai-voice.md` en version générique.
- Le validateur vérifie aussi l'absence de placeholders résiduels et la taille des CLAUDE.md (200 lignes).

## [1.1.0] - 2026-09-09

### Ajouté
- Le pack contenu LinkedIn : 10 skills qui produisent des posts dans votre voix, de la veille au visuel.
  - `linkedin-system-installer` : interview + script `apply_profile.py` qui personnalise les 8 skills du pack à partir d'un profil JSON (re-runnable, garde une copie `.template`).
  - `linkedin-writing-core` : le socle éditorial (voix, formatage, système de hooks) avec 7 fichiers de références dont une bibliothèque de hooks et 11 templates de posts.
  - `linkedin-ideation` : veille sur vos sources et brief éditorial hebdomadaire, avec 4 fichiers de références.
  - `linkedin-educational`, `linkedin-storytelling`, `linkedin-hot-take`, `linkedin-lead-magnet` : un skill par intention de post.
  - `viral-hook-writer` et `linkedin-post-optimizer` : les 2 lignes avant le "voir plus", puis le contrôle qualité final.
  - `linkedin-interview-2` : fouille votre vécu pour produire la matière première du contenu.

## [1.0.0] - 2026-09-09

### Ajouté
- `skills/setup-claude-infrastructure` : le skill qui construit le second cerveau (CLAUDE.md, ABOUT.ME, 7 fichiers de contexte, structure Projects, MCP, premier skill), avec son guide complet de prompts d'interview.
- `os-gtm/` : l'OS de prospection complet, 25 skills, du ciblage au suivi des réponses (Unipile, Crustdata, FullEnrich, Lemlist, Apify).
- `skills/find-skills` : découverte et installation de skills depuis l'écosystème ouvert (skills.sh).
- `install.sh` : installation en une commande (skills globaux ou locaux, déploiement de l'OS-GTM dans un workspace).
- `scripts/validate_skills.py` + workflow GitHub Actions : vérification du frontmatter de chaque SKILL.md, absence de tirets cadratins et de clés API.
