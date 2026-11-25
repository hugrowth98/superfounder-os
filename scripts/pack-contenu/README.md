# Superfounder OS : mise à jour du contenu

Vous avez déjà un Superfounder OS installé et vous voulez la nouvelle façon de gérer votre contenu, sans repartir de zéro. Ce dossier l'ajoute à votre second cerveau actuel, en gardant ce que vous avez modifié.

**Claude : si l'utilisateur vous demande d'intégrer ce dossier, lisez `MISE-A-JOUR.md` et suivez-le.**

## Ce que vous gagnez

- **Un Content Brain** : un dossier qui réunit votre stratégie et ses piliers, votre veille, une base de connaissances tirée de vos posts, de vos calls et de votre vécu, vos idées, et votre calendrier éditorial avec les chiffres de chaque post.
- **Une stratégie qui se construit avec vous** : Claude lit votre second cerveau, rédige une première version, vous dit ce qu'il en pense, puis vous challenge une question à la fois.
- **Des posts qui partent de votre matière** : avant d'écrire, les skills LinkedIn vont chercher vos méthodes, vos preuves et vos histoires dans la base.
- **Un passage chaque lundi** : vos nouveaux calls deviennent des fiches, les chiffres de vos posts sont relevés, vos pages de piliers sont reconstruites, et vous recevez un rapport.

## Comment faire

1. Téléchargez ce dossier (bouton vert "Code", puis "Download ZIP") et décompressez-le.
2. Déposez-le dans le dossier `00_Inbox/` de votre workspace.
3. Ouvrez votre workspace dans Claude Code et écrivez :

```
Voici une nouvelle version pour gérer mon contenu, intègre-la à mon second cerveau.
```

Claude vous montre d'abord un rapport : ce qui change de place, ce qui est ajouté, ce que vous aviez modifié et qu'il ne touchera pas sans vous. Rien n'est écrit avant votre accord.

Comptez 20 à 40 minutes, selon ce que vous aviez adapté.

## Ce qui est garanti

- Rien n'est supprimé. Chaque fichier remplacé est copié dans `11_Archives/mise-a-jour-contenu_<date>/`.
- Un fichier que vous avez modifié n'est jamais écrasé : Claude vous propose une fusion et attend votre oui.
- Votre stratégie, vos posts de référence, vos sources de veille et votre banque de vécu changent de place, pas de contenu.
- Vos calls clients restent fermés au contenu tant que vous n'ouvrez pas un client vous-même.

## Ce que contient le dossier

| Élément | Rôle |
|---|---|
| `MISE-A-JOUR.md` | la procédure que Claude suit |
| `migrer.py` | le script qui compare votre workspace au standard, puis applique |
| `nouveau/` | les nouveaux fichiers, rangés comme dans un workspace |
| `base/` | la version d'origine des fichiers, pour voir ce que vous aviez changé |
| `empreintes.json` | les empreintes des versions publiées, pour reconnaître un fichier jamais modifié |
| `VERSION` | la version du Superfounder OS dont ce pack est tiré |

## Prérequis

Un workspace Superfounder OS en version 6 (dossiers numérotés de `00_Inbox/` à `11_Archives/`, skills dans `10_Skills/`), Claude Code, et Python 3.10 ou plus.

Ce dossier est fabriqué à partir du dépôt principal : https://github.com/hugrowth98/superfounder-os
