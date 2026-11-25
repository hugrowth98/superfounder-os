# Contribuer

Merci de vouloir améliorer Superfounder OS. Le dépôt est fait pour être forké, adapté et enrichi.

## Deux façons de contribuer

1. **Corriger ou améliorer un skill existant** : ouvrez une pull request avec le diff et, en description, le cas concret qui vous a poussé à modifier le skill.
2. **Proposer un nouveau skill** : ouvrez d'abord une issue qui décrit la tâche, les inputs, les étapes et l'output attendu. Règle d'or du dépôt : on ne crée jamais un skill sans avoir fait la tâche à la main au moins deux ou trois fois.

## Conventions

- Un skill = un dossier avec un `SKILL.md` et, si besoin, `references/` (fichiers lus à la demande) et `scripts/` (code exécuté par le skill). Tous les skills vont dans `10_Skills/`, un dossier par skill. `.claude/skills` et `.agents/skills` sont des liens vers `10_Skills/`, on n'y écrit jamais.
- Un skill ne contient jamais de donnée sur l'utilisateur : il lit `02_Contexte/`, `05_Departements/Go-to-Market/contexte.md` et `05_Departements/Marketing/Content-Brain/` à l'exécution. Pas de jetons de substitution.
- Le `CLAUDE.md` racine reste sous 200 lignes. C'est une carte, pas une bibliothèque. Un dossier de travail n'a pas de `CLAUDE.md` : il a une note du même nom que le dossier.
- Le frontmatter YAML de chaque `SKILL.md` contient au minimum `name` (identique au nom du dossier) et `description` (qui dit QUAND le skill se déclenche, avec les phrases typiques de l'utilisateur).
- Langue : français pour les skills métier, anglais accepté pour les skills techniques d'origine anglophone.
- Aucun tiret cadratin ni demi-cadratin dans les fichiers : utilisez `-`, `:` ou des parenthèses.
- Jamais de clé API, de token ni de donnée client dans le dépôt. Les clés vivent dans un `.env` local, ignoré par git.
- Un skill ne doit jamais envoyer un message, une invitation ou une campagne sans validation explicite de l'utilisateur.
- Le dépôt ne garde pas ses anciennes versions dans `11_Archives/` : l'historique, c'est git (`git show vX.Y.Z:chemin`). Un skill remplacé est supprimé du dépôt et noté dans le CHANGELOG ; `11_Archives/` est livré vide, c'est le dossier d'archives de l'utilisateur. `install.sh --into` y déplace les anciennes copies chez lui, jamais dans le dépôt.

## Vérifier avant d'envoyer

```bash
python3 scripts/validate_skills.py
```

```bash
python3 scripts/valider_gtm.py
```

Le premier vérifie que chaque `SKILL.md` a un frontmatter valide, qu'aucun tiret cadratin ne s'est glissé dans les fichiers markdown et qu'aucune chaîne ne ressemble à une clé API. Le second vérifie les masters (références vers les sous-skills et les ressources), les noms d'outils tiers interdits, la compilation des scripts et la cohérence avec `OUTILS.md`. Les deux tournent en CI.
