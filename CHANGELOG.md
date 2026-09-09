# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

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
