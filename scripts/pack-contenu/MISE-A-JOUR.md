# Mise à jour du contenu : procédure pour Claude

> Ce fichier s'adresse à Claude. L'utilisateur a déposé ce dossier dans son workspace Superfounder OS et a dit quelque chose comme : "Voici une nouvelle version pour gérer mon contenu, intègre-la à mon second cerveau." Suis cette procédure dans l'ordre. Vouvoiement, une étape à la fois, aucun tiret cadratin.

Ce pack ajoute le Content Brain à un Superfounder OS déjà installé : un dossier `Content-Brain/` dans le département Marketing (stratégie et piliers, veille, base de connaissances, idées, calendrier éditorial), trois skills (`installer-contenu`, `strategie-contenu`, `clean-content`), et le master `linkedin` mis à jour pour écrire à partir des fiches de la base.

L'utilisateur a pu adapter son workspace : un `CLAUDE.md` retouché, un skill modifié, un département renommé. Ton travail est de garder ce qu'il a changé et de mettre à jour le reste.

## Règles

- Rien n'est supprimé. Tout fichier remplacé est copié dans `11_Archives/mise-a-jour-contenu_<date>/`.
- Rien n'est écrit avant que l'utilisateur ait vu le rapport et dit oui.
- Un fichier que l'utilisateur a modifié n'est jamais écrasé : tu proposes une fusion, il valide.
- Ses données (stratégie, posts, sources de veille, banque de vécu) changent de place, jamais de contenu, sauf aux étapes 5 et 6 où tu les convertis avec son accord.
- Si le script s'arrête sur une erreur, lis-la à l'utilisateur et arrête-toi. Ne contourne pas.

## Étape 1 : le rapport

Depuis la racine du workspace :

```bash
python3 <chemin du pack>/migrer.py
```

Si le script dit que le département Marketing est introuvable, demande à l'utilisateur le nom de son dossier de contenu dans `05_Departements/` et relance avec `--marketing "<Nom>"`.

Présente le rapport en clair, sans bloc de code, en quatre parties :

1. **Ce qui change de place** : ses fichiers de contenu et leur nouvelle adresse.
2. **Ce qui est ajouté ou remplacé** : en nombre, avec les skills concernés. Les fichiers remplacés sont ceux qu'il n'a jamais modifiés.
3. **Ce qu'il a modifié** : la liste "MODIFIÉ PAR VOUS". Pour chacun, dis en une ligne ce qu'il avait changé (compare son fichier à la version d'origine dans `base/` du pack) et ce que la nouvelle version apporte.
4. **Ce qui cite encore un ancien chemin** : ses propres skills ou notes.

Puis demande : "Je sauvegarde et j'applique ?"

## Étape 2 : sauvegarder et appliquer

1. Si le workspace est un dépôt git, propose un commit avant de commencer ("avant mise à jour contenu"). Sinon, la copie dans `11_Archives/` faite par le script suffit.
2. Lance `python3 <chemin du pack>/migrer.py --appliquer` (avec le même `--marketing` si besoin).
3. Lis le rapport final et confirme en trois lignes ce qui a été fait.

## Étape 3 : fusionner ce qu'il a modifié

Pour chaque fichier de la liste "MODIFIÉ PAR VOUS", un à la fois :

1. Lis trois versions : la sienne, celle d'origine (`base/<chemin>` dans le pack, quand elle existe) et la nouvelle (`nouveau/<chemin>`).
2. Repère ce qu'il a changé par rapport à l'origine. C'est ce qu'il faut garder.
3. Écris la fusion : la nouvelle version, avec ses changements reportés dedans. Montre le résultat en diff et attends son oui.
4. Archive son ancienne version dans le dossier d'archive du jour avant d'écrire.

Cas fréquents :
- **`CLAUDE.md` et `AGENTS.md`** : il a souvent ajouté des règles, un département ou une ligne de routage. Garde tout ce qu'il a ajouté. De la nouvelle version, reprends : la ligne "Le contenu" du tableau de diagnostic, la ligne `Marketing/` du tableau des départements, la ligne "Contenu LinkedIn" du routage du contexte, la règle 1 du routage des livrables, la ligne "Transcript de call" du routage des entrées, la ligne `clean-content` des rituels, et la section 13 en entier. Vérifie que le fichier reste sous 200 lignes.
- **La note `Marketing.md` ou `LinkedIn.md`** : garde ses sections Objectif, Où on en est et Key Notes telles quelles. Reprends Mission, Périmètre et Cadre de la nouvelle version, en y reportant ce qu'il avait ajouté.
- **Un sous-skill du master `linkedin` qu'il a adapté** : garde ses ajouts (exemples, règles de ton), et reprends de la nouvelle version la section "D'abord, le Content Brain" et les nouveaux chemins.

## Étape 4 : corriger les anciens chemins

Pour chaque fichier de la liste "ANCIENS CHEMINS ENCORE CITÉS" qui lui appartient (un skill qu'il a créé, une note), propose le remplacement ligne par ligne :

| Ancien | Nouveau |
|---|---|
| `LinkedIn/strategie-contenu.md` | `Content-Brain/01_Strategie/Strategie-contenu.md` |
| `LinkedIn/posts-de-reference.md` | `Content-Brain/01_Strategie/Posts-de-reference.md` |
| `LinkedIn/sources-veille.json` | `Content-Brain/02_Veille/Sources-veille.json` |
| `comptes-veille.json` | `Content-Brain/02_Veille/Comptes-veille.json` |
| `swipe-file.md` | `Content-Brain/02_Veille/Inspirations/` (une fiche par post) |
| `banque-vecu.md` | `Content-Brain/03_Base-de-connaissances/` (une fiche par histoire) |
| `Calendrier-publication.md` | `Content-Brain/05_Calendrier-editorial/Calendrier.md` |
| sous-skill `opinion` | sous-skill `hot-take` |

## Étape 5 : mettre la stratégie au nouveau format

Sa stratégie a été déplacée telle quelle. Le nouveau gabarit (`nouveau/05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`) a plus de sections, et la section Piliers a une forme que le script de reconstruction lit.

1. Garde tout ce qu'il a écrit. Reporte chaque réponse dans la section du même nom du nouveau gabarit.
2. Réécris la section Piliers à la forme attendue : un titre `### Pilier N : Nom (XX %)` par pilier, une ligne `Portée :`, une ligne `Test :`, puis `Sujets :` et une puce par sujet au format `- Sujet : douleur`. Les sujets viennent de ce qu'il avait écrit entre parenthèses ou après les deux-points. S'il n'en avait pas, laisse la liste vide : ne les invente pas.
3. Les sections nouvelles (Ce que dit le terrain, Message, Ton et voix, Parcours de conversion, Hors sujet et questions ouvertes) restent `[à remplir]`. Le skill `strategie-contenu` les remplira.
4. Montre le fichier, attends son oui, écris.

## Étape 6 : convertir les deux fichiers en fiches

Lis `10_Skills/_commun/content-brain.md` pour les formats, puis, s'ils existent :

- `02_Veille/Inspirations/_swipe-file-a-convertir.md` : une fiche `inspiration` par post qu'il avait collé, avec l'auteur, le format, la structure, pourquoi ça marche et ce qu'il en prend. Jamais le texte entier.
- `03_Base-de-connaissances/Sources/_banque-vecu-a-convertir.md` : ce fichier devient la fiche source (renomme-le `Banque-de-vecu_<date>.md`, `nature: interview`), et chaque pépite devient une fiche `histoire` dans `Histoires/`, avec son verbatim, son `pilier`, ses `sujets` et sa `diffusion`.

Montre les trois premières fiches, fais valider le format, puis continue. Les fichiers d'origine partent dans le dossier d'archive du jour, sur un oui.

Les posts déplacés dans `05_Calendrier-editorial/Brouillons/` : demande lesquels sont déjà publiés, passe-les dans `Publies/` avec `statut: publie` et leur date, et ajoute à chacun le frontmatter de post du fichier de structure.

## Étape 7 : vérifier

```bash
python3 10_Skills/clean-content/scripts/reconstruire.py --dry-run
python3 scripts/validate_skills.py
```

Le premier doit lister ses piliers et créer une page par pilier et par sujet. Relance-le sans `--dry-run` sur un oui. Le second n'existe que si le workspace vient du dépôt : s'il est absent, passe.

Vérifie aussi que les nouveaux skills sont visibles : `10_Skills/strategie-contenu/SKILL.md` et `10_Skills/clean-content/SKILL.md` existent, et `.claude/skills` pointe toujours vers `10_Skills/`.

## Étape 8 : la suite

Dis en cinq lignes ce qui a changé pour lui : où vit son contenu maintenant, les trois phrases à connaître ("Installe mon contenu", "Nourris mon brain", "clean content"), et ce qui reste à faire.

Puis propose une seule action : "Installe mon contenu". L'installeur reprend à la première phase incomplète, en général le cloisonnement des clients et la première récolte de fiches.

Le dossier du pack peut ensuite partir dans `11_Archives/`, sur un oui.
