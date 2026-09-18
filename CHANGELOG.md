# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

## [3.2.0] - 2026-09-18

Le même dépôt pour Claude Code, Codex et OpenCode.

### Ajouté
- `AGENTS.md` à la racine : la carte du `CLAUDE.md` reprise pour Codex et OpenCode, avec une consigne de lecture explicite d'`About-Me/` (ils ne suivent pas les imports `@`) et la correspondance des commandes (`/nom` devient `$nom` dans Codex, l'outil skill dans OpenCode).
- `.agents/skills/` : trois liens symboliques (`os`, `vente`, `marketing`) vers les dossiers de skills, pour que Codex trouve les 46 skills.
- `opencode.json` : charge les trois fichiers d'`About-Me/` au démarrage d'OpenCode.
- Section 11 du `CLAUDE.md` et section du README qui décrivent le montage. Le validateur ignore `.agents/`. `install.sh` copie les trois nouveaux éléments.

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
- `Projects/Prospection/` devient `Vente/` avec quatre sous-dossiers typés (`Listes-prospection/`, `Messages/`, `Propositions/`, `Pipeline/`). Les 25 skills restent scopés dans `Vente/.claude/skills/`.
- `Projects/Contenu/` devient `Marketing/` avec sept briques (`LinkedIn/`, `Newsletter/`, `Mailing/`, `Event/`, `Video/`, `Slides/`, `Site-vitrine/` à créer au besoin). Les 10 skills restent scopés dans `Marketing/.claude/skills/`, les ressources de contenu vivent dans `Marketing/LinkedIn/ressources/`.
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
