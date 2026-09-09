# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

## [1.0.0] - 2026-09-09

### Ajouté
- `skills/setup-claude-infrastructure` : le skill qui construit le second cerveau (CLAUDE.md, ABOUT.ME, 7 fichiers de contexte, structure Projects, MCP, premier skill), avec son guide complet de prompts d'interview.
- `os-gtm/` : l'OS de prospection complet, 25 skills, du ciblage au suivi des réponses (Unipile, Crustdata, FullEnrich, Lemlist, Apify).
- `skills/find-skills` : découverte et installation de skills depuis l'écosystème ouvert (skills.sh).
- `install.sh` : installation en une commande (skills globaux ou locaux, déploiement de l'OS-GTM dans un workspace).
- `scripts/validate_skills.py` + workflow GitHub Actions : vérification du frontmatter de chaque SKILL.md, absence de tirets cadratins et de clés API.
