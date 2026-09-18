---
name: inbox-processor
description: "Vider 00 Inbox/ : chaque item est lu, typé, puis routé vers un projet, un département, un client, 08 Ressources/ (référence ou source de veille) ou 11 Archives/, en suivant le routage du CLAUDE.md. Jamais de suppression sans un oui. À lancer dès que l'inbox dépasse cinq items ou une fois par semaine."
user-invocable: true
context: main
---

# Inbox processor

Tu aides l'utilisateur à vider `00 Inbox/`. C'est un sas : rien n'y reste plus de quelques jours. Chaque item finit à un seul endroit, avec un nom propre et un frontmatter.

## Avant de commencer

1. Relis la section "Routage" du `CLAUDE.md` : c'est la règle de vérité.
2. Liste les destinations possibles : `ls "04 Projets" "05 Departements" "06 Clients"`.
3. Scanne `00 Inbox/` en ignorant `Inbox.md`, `_log.md` et `_import/` (ce dernier se traite avec `/import`).

## Étape 1 : scanner

```
J'ai trouvé X items dans l'inbox :
1. <fichier> : <aperçu en une ligne>
...
On les traite un par un ?
```

## Étape 2 : pour chaque item, typer et proposer

```
Item : <nom>
Contenu : <résumé en une ou deux phrases>
Type : Idée / Tâche / Transcript / Livrable / Source de veille / Référence / Réflexion / Autre

Destinations possibles :
1. Un projet (04 Projets/<Projet>/) : ça sert une initiative avec une fin
2. Un département (05 Departements/<Departement>/) : ça sert une responsabilité continue
3. Un client (06 Clients/<Client>/) : ça concerne une mission signée
4. Une source de veille (08 Ressources/Veille/sources/) puis /notes-permanentes si ça mérite de durer
5. Une référence (08 Ressources/) : template, exemple, doc d'API
6. Un transcript de call (07 Meeting/, routage de la note Meeting.md)
7. 11 Archives/ : obsolète ou déjà traité
8. Développer maintenant : on creuse ensemble, puis on range
9. Supprimer : doublon ou vide, seulement avec ton oui

Je propose : <numéro>, parce que <une raison>. OK ?
```

Une seule proposition argumentée par item. L'utilisateur dit oui, ou corrige.

## Étape 3 : exécuter

- **Idée ou fait lié à un dossier** : verser dans Où on en est, en décision datée dans Cadre, ou en case dans Étapes de la note du dossier (format de `/done`), puis retirer l'item de l'inbox.
- **Livrable ou fichier** : déplacer dans le dossier, renommer en `Nom-Sujet_YYYY-MM-DD.ext`, ajouter le frontmatter s'il manque (`type`, `status`, `date`, `maj`, `client` si besoin).
- **Nouveau projet** : créer le dossier, sa note depuis `08 Ressources/templates/projet.md`, son `_log.md`, et l'ajouter à `04 Projets/Projets.md`.
- **Transcript** : appliquer le routage de `07 Meeting/Meeting.md`, puis faire ruisseler les décisions vers la note du client ou du prospect.
- **Source de veille** : déplacer dans `08 Ressources/Veille/sources/`, proposer `/notes-permanentes`.
- **Vague mais à potentiel** : dérouler l'idée avec l'utilisateur en trois questions (c'est quoi, pour qui, quelle première action), puis ranger le résultat.
- **Archive** : déplacer vers `11 Archives/` à plat, nom d'origine conservé.
- **Suppression** : uniquement après un oui explicite sur cet item précis.

Ne jamais écrire dans `01 About-Me/`, `02 Contexte/`, `03 Branding/` : si un item les concerne, proposer un diff comme `/done` le fait.

## Étape 4 : récapitulatif

```
Inbox traitée.
- X vers des projets, X vers des départements, X vers des clients
- X en veille, X en références, X en Meeting
- X archivés, X supprimés (avec ton oui)
Items restants : X
```

Puis une ligne dans `09 Journal/YYYY-MM-DD.md` au format de `/done` si au moins un fichier a bougé.

## Règles de routage

- Projet si l'item a un objectif, une fin, et demande plusieurs actions.
- Département si l'item sert une responsabilité qui ne se termine pas.
- Client si l'item cite une mission signée. Un prospect pas signé va dans [[Vente]].
- Le support final l'emporte sur le sujet : un post qui parle d'un client va dans Contenu, pas chez le client.
- En cas de doute entre deux destinations, demande. Mieux vaut ranger vite qu'attendre, mais jamais au hasard.
- Français, vouvoiement avec l'utilisateur, wikilinks, aucun tiret cadratin ni demi-cadratin. Chemins avec espaces entre guillemets.
