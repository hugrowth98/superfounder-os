---
name: weekly-review
description: "Bilan de la semaine écoulée, report des tâches non cochées, intentions transverses, plan de la semaine suivante jour par jour, écrit dans 09_Journal/YYYY-Www.md. Le vendredi, ou dès qu'l'utilisateur dit qu'il veut planifier sa semaine."
user-invocable: true
context: main
---

# Weekly review

Bilan de la semaine, report de ce qui n'est pas fini, plan de la suivante réparti par jour. Une vue jour par jour, simple à tenir, avec un seul next step visible à la fois.

## Étape 1 : lire le contexte

Lis `01_About-Me/about-me.md` et `01_About-Me/my-company.md` pour les objectifs et le focus du moment. Lis les notes du journal de la semaine (`09_Journal/YYYY-MM-DD.md`) pour ce qui s'est passé session par session.

## Étape 2 : déterminer la semaine

```bash
CURRENT_WEEK=$(date +%Y-W%V)
PREV_WEEK=$(date -v-7d +%Y-W%V 2>/dev/null || date -d "7 days ago" +%Y-W%V)
echo "Semaine : $CURRENT_WEEK | Précédente : $PREV_WEEK"
```

## Étape 3 : report des tâches

Lis `09_Journal/$PREV_WEEK.md`. Extrais toutes les lignes `- [ ]` non cochées. Ajoute les cases non cochées des sections Étapes et Où on en est des projets actifs (`04_Projets/*/*.md`). Si la weekly précédente n'existe pas, passe.

## Étape 4 : scanner l'activité

```bash
find "04_Projets" "05_Departements" "06_Clients" "00_Inbox" -name "*.md" -mtime -7 -not -name "_log.md" | grep -v superfounder-os | head -50
```

Résume en cinq lignes maximum ce qui a bougé, par projet, département et client. Repère au passage les tâches ouvertes citées dans ces fichiers.

## Étape 5 : brain dump

> Comment s'est passée votre semaine ? Qu'est-ce qui a avancé, qu'est-ce qui a bloqué, qu'est-ce qui a émergé ?

Attends la réponse libre. Extrais avancées, blocages, émergences, et les nouvelles tâches qui en découlent.

## Étape 6 : intentions transverses

> Quels sont vos deux ou trois fils rouges pour la semaine ? Ceux qui ne tiennent pas dans un jour.

Rappelle le focus en cours dans `01_About-Me/my-company.md` si le brain dump s'en éloigne. C'est le moment de fermer une boucle plutôt que d'en ouvrir une.

## Étape 7 : répartir par jour

Répartis toutes les tâches sur lundi à dimanche : le report, le brain dump, ce que le scan a révélé. Groupe sous `### [[Projet]]` ou `### [[Département]]` quand plusieurs tâches d'un même dossier se suivent. Une tâche qui s'étale apparaît sur plusieurs jours. Gardez une journée contenu fixe si vous en avez une. Présente la répartition et attends la validation.

## Étape 8 : écrire la weekly note

Crée `09_Journal/YYYY-Www.md` depuis `08_Ressources/templates/journal-semaine.md`, remplis Transverse et chaque jour. Le brain dump n'est pas recopié : il a servi à extraire.

## Étape 9 : confirmation

Résumé : nombre de tâches reportées, intentions retenues, nombre de tâches par jour, la première tâche de lundi.

## Style

Français, vouvoiement avec l'utilisateur, concis, interactif (attendre les réponses), pas d'emojis, aucun tiret cadratin ni demi-cadratin.
