---
name: import
description: "Importer un gros lot (notes, exports de conversations ChatGPT ou Claude, PDF, dossier déposé) dans le second cerveau par passes thématiques : alignement, préparation, scan, table de routage, sous-agents, plan, validation, exécution. Quatre verdicts par item : KEEP, EXTRACT, SUMMARIZE, ARCHIVE. Destinations : projets, départements, clients, 08_Ressources/, 11_Archives/."
user-invocable: true
context: main
---

# Import par passes

Zone d'import : `00_Inbox/_import/`. Une passe = une source ou un thème, cent items maximum. On vide `_import/`, on dépose la source suivante, on relance `/import`. Un gros volume mélangé se découpe avant de commencer.

## Étape 1 : alignement

Avant d'ouvrir un fichier, cinq questions à l'utilisateur :

1. Qu'y a-t-il dans `_import/` pour cette passe ?
2. Objectif : ranger note par note, extraire l'info utile vers les notes de contexte et archiver le reste, trier garder contre jeter, ou un mélange ?
3. Quoi archiver direct (projets terminés, sujets morts) ?
4. Quel dossier est central pour cette passe (un projet, un département, un client) ?
5. Budget tokens limité ? Si oui, sous-agents sur un modèle économique.

Reformule en quatre lignes maximum, fais valider. Ce résumé briefe les sous-agents.

## Étape 2 : préparation

- Convertis les formats lourds (PDF, docx, pptx) en Markdown si `markitdown` est disponible, sinon signale les fichiers non lisibles.
- Un export ChatGPT ou Claude (`conversations.json`) se découpe en un fichier par conversation, titre et date en frontmatter.
- Rapport : nombre d'items, formats, taille, ce qui n'a pas pu être converti.

## Étape 3 : scan

`find "00_Inbox/_import" -type f | sort`. Lis les titres et les vingt premières lignes de chaque item. Groupe par thème. Ne juge rien encore.

## Étape 4 : table de routage

Construis la table des destinations vivantes :

```bash
ls -d "04_Projets"/*/ "05_Departements"/*/ "06_Clients"/*/
```

Plus `08_Ressources/` (références), `08_Ressources/Veille/sources/` (brut à distiller), `11_Archives/`. Rappelle les frontières du `CLAUDE.md` : projet = objectif et fin, département = responsabilité continue, client = mission signée, le support final l'emporte sur le sujet.

## Étape 5 : sous-agents

Découpe les items en lots de vingt à trente. Chaque sous-agent reçoit : le résumé d'alignement, la table de routage, le lot. Il rend, par item, une ligne :

```
<fichier> | <verdict> | <destination> | <raison en dix mots> | <info à extraire si EXTRACT>
```

Les quatre verdicts :

- **KEEP** : la note vaut telle quelle, elle va dans un dossier avec un nom propre et un frontmatter.
- **EXTRACT** : la note contient une décision, un fait ou une préférence qui va dans Où on en est ou en décision datée dans Cadre d'une note (ou en proposition de diff pour `01_About-Me/` et `02_Contexte/`), puis la note part en archive.
- **SUMMARIZE** : plusieurs notes disent la même chose, on écrit une synthèse et on archive les originaux.
- **ARCHIVE** : rien à garder vivant, on garde le fichier dans `11_Archives/`.

Un sous-agent qui hésite écrit `? 00_Inbox/` : un humain tranchera.

## Étape 6 : plan complet, aucune écriture

```
Plan : X items (passe : <thème>)

KEEP -> 04_Projets/<Projet>/ (n)
KEEP -> 05_Departements/<Departement>/ (n)
KEEP -> 06_Clients/<Client>/ (n)
KEEP -> 08_Ressources/ (n)
EXTRACT (n) : <note cible> reçoit <info>
SUMMARIZE (n items en g groupes)
ARCHIVE (n)
-> 00_Inbox/ (n) : décisions humaines

Alertes : contradictions détectées avec le contexte existant, doublons, fichiers illisibles.
```

## Étape 7 : ajustements

L'utilisateur corrige ligne par ligne. Tu n'exécutes rien avant son "go".

## Étape 8 : exécution

Dans cet ordre : KEEP (déplacer, renommer `Nom-Sujet_YYYY-MM-DD.ext`, frontmatter), SUMMARIZE (écrire la synthèse, archiver les sources), EXTRACT (mettre à jour Où on en est et Cadre, proposer les diffs pour les zones protégées), ARCHIVE. Aucune suppression. Une ligne dans `09_Journal/YYYY-MM-DD.md` au format de `/done`, plus une ligne dans le `_log.md` de chaque dossier touché.

## Étape 9 : récap et boucle

Récap chiffré, ce qui reste dans `00_Inbox/`, et une question : qu'est-ce qui t'a fait corriger le plan ? La réponse améliore l'alignement de la passe suivante.

## Principes

- Une passe à la fois. Petit, validé, exécuté.
- Chaque info vit une seule fois, au bon endroit.
- Le doute tranche vers `00_Inbox/`, jamais vers la suppression.
- Ne jamais écrire dans `01_About-Me/`, `02_Contexte/`, `03_Branding/` sans diff validé.
- Français, vouvoiement avec l'utilisateur, aucun tiret cadratin ni demi-cadratin.
