# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

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
