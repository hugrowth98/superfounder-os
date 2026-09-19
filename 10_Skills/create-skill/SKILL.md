---
name: create-skill
description: "Transformer une tâche faite au moins trois fois à la main en skill réutilisable dans 10_Skills/ : cadrage du process, étapes détaillées avec les règles apprises, format de sortie, test sur un cas réel, puis écriture du SKILL.md. Se déclenche sur \"crée un skill\", \"fais-en un skill\", \"automatise cette tâche\", ou quand l'utilisateur décrit une routine qu'il répète."
user-invocable: true
context: main
---

# Créer un skill

Un skill est une procédure écrite pour Claude : quand la lancer, quoi lire, quoi faire étape par étape, quoi rendre. On n'écrit pas un skill à partir d'une idée. On l'écrit à partir d'une tâche déjà faite plusieurs fois, quand le pattern s'est stabilisé. Sinon on automatise une méthode qu'on n'a pas encore.

## Étape 0 : vérifier que c'est le moment

Demande : combien de fois cette tâche a été faite à la main, et où sont les derniers résultats. Moins de trois fois, ou aucun exemple à montrer : propose de la faire ensemble une fois de plus, à la main, et de créer le skill juste après. Un skill créé trop tôt produit du vague avec assurance.

## Étape 1 : cadrer

Cinq questions, une à la fois :

1. La tâche en une phrase : quel input, quel output.
2. Le déclencheur : la phrase que l'utilisateur tapera, et les situations où Claude doit proposer le skill de lui-même.
3. Ce que le skill doit lire avant d'agir : quels fichiers de `01_About-Me/`, `02_Contexte/`, quelle note de dossier.
4. Où va le résultat, avec quel nom (règle de routage du `CLAUDE.md`).
5. Ce qui ne doit jamais arriver : envoi, suppression, invention.

Reformule en cinq lignes. Attends le "oui".

## Étape 2 : écrire les étapes

Reprends le dernier exemple fait à la main et découpe-le en étapes numérotées. Pour chaque étape : ce que Claude lit, ce qu'il fait, ce qu'il montre à l'utilisateur, ce qu'il attend de lui. Note les règles apprises à l'usage ("toujours vérifier X avant Y", "ne jamais proposer Z"). Ces règles sont la valeur du skill : sans elles, c'est un prompt.

Un skill demande une validation à chaque point de non-retour, jamais sur les détails.

## Étape 3 : définir la sortie

Le format exact du résultat : nom de fichier, frontmatter, sections, longueur. Montre un exemple rempli. Si le skill produit plusieurs fichiers, dis lesquels et dans quel ordre.

## Étape 4 : tester

Rejoue le skill sur un cas réel, différent du dernier exemple. Compare la sortie à ce que l'utilisateur aurait fait. Corrige les étapes, pas la sortie. Deux tours maximum, puis on écrit.

## Étape 5 : écrire le SKILL.md

Crée `10_Skills/<nom-du-skill>/SKILL.md` :

```markdown
---
name: <nom-du-skill>
description: "<Ce que le skill fait, en une phrase, puis les mots qui le déclenchent entre guillemets.>"
user-invocable: true
context: main
---

# <Titre>

<Deux lignes : à quoi ça sert, quand on le lance.>

## Avant de commencer
<Ce que Claude lit.>

## Étape 1 : ...
## Étape 2 : ...

## Sortie
<Format exact, chemin, nom.>

## Règles
<Les règles apprises, les validations obligatoires, ce qu'on ne fait jamais.>
```

Le `name` est le nom du dossier, en minuscules avec des tirets. La `description` compte : c'est elle que Claude lit pour décider de proposer le skill. Scripts dans `scripts/`, exemples dans `examples/`, références longues dans `references/`, jamais dans le SKILL.md.

Vérifie qu'aucun tiret cadratin ni demi-cadratin ne s'est glissé dans le fichier. Le skill est visible de Claude Code, Codex et OpenCode sans rien d'autre à faire.

## Étape 6 : loguer

Une ligne dans `09_Journal/YYYY-MM-DD.md` au format de `/done`, et le skill cité dans la section Cadre de la note du département qui l'utilise.

## Règles

- Un skill fait une chose. Deux tâches, deux skills.
- Un skill lit le contexte, il ne le recopie pas : pas de prix, d'offre ou de cible en dur dans le SKILL.md.
- Français, vouvoiement avec l'utilisateur, aucun tiret cadratin ni demi-cadratin.
