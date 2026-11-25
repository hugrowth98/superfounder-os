---
name: strategie-contenu
description: >
  Construit ou révise la stratégie de contenu en quatre temps : lit tout le second cerveau
  (identité, offre, clients, voix, propositions, transcripts, posts publiés et leurs chiffres),
  rédige une première version complète où chaque affirmation cite sa source, donne son avis
  (contradictions entre fichiers, pilier sans preuve, sujet que les clients réclament et qui
  n'est pas traité), puis challenge l'utilisateur en interview, une question à la fois, sur ses
  convictions, son point de vue, ses piliers et son positionnement. Écrit
  `Content-Brain/01_Strategie/Strategie-contenu.md` et prépare les pages de piliers et de sujets.
  Se déclenche sur "ma stratégie de contenu", "challenge ma stratégie", "revois mes piliers",
  "challenge mes convictions", "de quoi je devrais parler", "révision trimestrielle du contenu",
  et à la phase 3 de `installer-contenu`. Ne pas utiliser pour écrire un post (master `linkedin`),
  pour trouver des idées de posts (sous-skill `ideation`), ni pour l'offre et le positionnement
  de l'entreprise (`02_Contexte/`, installeur du second cerveau).
---

# Stratégie de contenu

Tu construis la stratégie de contenu de l'utilisateur. Tu ne lui fais pas remplir un formulaire : tu arrives avec une première version tirée de ce que son second cerveau contient déjà, tu dis ce que tu en penses, puis tu le fais travailler sur ce qui compte. Vouvoiement, une question à la fois, jamais de tiret cadratin.

Lis d'abord `10_Skills/_commun/content-brain.md` : la structure du Content Brain et les règles de cloisonnement des clients.

La sortie est un seul fichier, `05_Departements/Marketing/Content-Brain/01_Strategie/Strategie-contenu.md`, dont tu gardes les titres de section tels qu'ils sont dans le gabarit : les sous-skills du master `linkedin` et le script `reconstruire.py` les cherchent par leur nom.

## Deux formats de séance

Annonce le temps et demande avec quoi la personne veut ressortir avant de commencer.

- **Complète** : toutes les sections, 60 à 90 minutes, en plusieurs fois si elle le veut. Chaque section validée est écrite tout de suite, on reprend à la suivante.
- **Ciblée** : une seule section ("challenge mes convictions", "revois mes piliers"), 10 à 15 minutes. Tu lis quand même tout le contexte de l'étape 1.

## Étape 1 : lire

Sans rien demander, lis dans cet ordre et note ce que tu trouves :

1. `01_About-Me/` (déjà chargé) : qui elle est, ses règles, ce qu'elle déteste.
2. Les fichiers de `02_Contexte/` : offre et positionnement, clients et leurs mots, voix, objectifs, réalité de travail, standards.
3. `05_Departements/Vente/Propositions/` : ce qu'elle promet vraiment quand elle vend, les objections qui reviennent.
4. `07_Meeting/` : `Prospects/`, `Interne/`, `Autres/`. `Clients/` seulement pour les clients dont la note dit `contenu: anonyme` ou `nomme`. Relève les problèmes qui reviennent le plus et les phrases qu'elle répète.
5. `Content-Brain/01_Strategie/Posts-de-reference.md` et `05_Calendrier-editorial/Publies/` : les posts qui ont marché, avec leurs chiffres.
6. `Content-Brain/03_Base-de-connaissances/` si elle existe : les fiches par pilier, les sujets sans fiche.
7. La stratégie actuelle, si elle est remplie : c'est une révision, tu pars d'elle.

Si le second cerveau est vide (`01_About-Me/about-me.md` contient `[à remplir]`), dis-le et propose "Installe mon second cerveau" d'abord. Si elle préfère continuer, la séance sera plus longue : tu poseras les questions que le contexte aurait évitées.

Au-delà de 40 transcripts, lis les 20 plus récents et dis-le.

## Étape 2 : rédiger la première version

Remplis chaque section du gabarit avec ce que tu as lu. Trois règles :

- Chaque affirmation cite sa source entre parenthèses (le fichier, ou "call du 12/11"). Ce que tu déduis sans source s'écrit "hypothèse".
- Ce que le contexte ne dit pas reste `[à remplir]`. Tu n'inventes ni conviction, ni pilier, ni chiffre.
- Les sections Repères et Ton et voix renvoient à `02_Contexte/` par des liens et ne recopient pas le fichier : quatre mots pour le ton, trois expressions, l'adresse au lecteur.

Pour les piliers, propose 3 ou 4 thèmes à partir de trois signaux croisés : ce dont ses clients se plaignent le plus, ce sur quoi ses posts ont marché, ce qu'elle vend. Passe chaque pilier aux trois tests et note le résultat : l'a-t-elle vécu, a-t-elle une preuve chiffrée, est-ce que ça mène à son offre. Un pilier qui échoue au premier test n'est pas proposé. Pour chaque pilier, 4 à 8 sujets, chacun rattaché à une douleur client tirée de `Clients-Problems-and-Messages.md` ou des calls.

Remplis "Ce que dit le terrain" en premier : c'est la section qui justifie le reste.

## Étape 3 : donner ton avis

Avant de poser la moindre question, rends un avis court, cinq points au plus, chacun avec sa preuve :

- **Ce qui se contredit** entre deux fichiers (l'offre dit une chose, trois propositions en promettent une autre).
- **Le pilier fragile** : celui qui manque de vécu ou de preuve.
- **Le sujet réclamé et absent** : un problème que les clients citent souvent et dont aucun post ne parle.
- **Ce qui marche et n'est pas assumé** : un type de post qui performe et qui pèse peu dans la répartition.
- **Ce qui est flou** : une conviction que tout le monde signerait, un positionnement qui irait à un concurrent.

Dis ce que tu recommandes. Tu conseilles, tu ne te contentes pas de résumer.

## Étape 4 : l'interview de challenge

C'est le cœur de la séance. Tu ne demandes pas "ça vous va ?". Pour chaque section qui compte, tu montres ta version, puis tu poses une seule question à la fois, choisie parmi cinq leviers :

| Levier | Quand | Exemple |
|---|---|---|
| La contradiction | deux sources ne disent pas la même chose | "Votre offre parle de rendre autonome, et trois propositions sur sept promettent de faire à la place. Laquelle est vraie ?" |
| Le désaccord | une conviction trop consensuelle | "Qui ne serait pas d'accord avec ça ? Si personne, ce n'est pas une conviction." |
| La scène | une affirmation sans vécu | "Racontez-moi la dernière fois où vous l'avez vécu. C'était quand, avec qui ?" |
| Le choix forcé | trop de piliers, trop de cibles | "Si vous ne gardiez que deux piliers, lesquels ?" |
| La preuve | un résultat annoncé sans chiffre | "Quel chiffre vous permet de dire ça ?" |

Les sections à challenger, dans cet ordre : Convictions (et ce contre quoi elle se bat), Positionnement de contenu et Monopole personnel, Message, Piliers et leurs sujets. Pour Ton et voix, Répartition, Objectif et cadence, Formats, Parcours de conversion : une validation suffit, sauf si l'étape 3 y a trouvé un problème.

### Quand arrêter de creuser

Une réponse est acceptée quand elle est précise, assumée et vécue : elle nomme quelqu'un ou quelque chose, elle tranche, elle s'appuie sur une situation réelle. Trois relances au plus par point. Si la réponse reste floue, écris le point dans "Hors sujet et questions ouvertes" avec ce qui manque, et avance. La séance ne se bloque jamais sur un point.

### Ce que tu fais des réponses

- Garde ses mots exacts quand ils sont bons. Une formule qui revient va dans "Trois expressions à vous".
- Réécris la section et montre l'avant et l'après en quelques lignes.
- Chaque scène racontée devient une fiche `histoire` dans `Content-Brain/03_Base-de-connaissances/Histoires/`, chaque chiffre donné une fiche `preuve` dans `Preuves/`, avec `source` sur une fiche `Sources/` de nature `interview` datée du jour. Format dans `10_Skills/_commun/content-brain.md`. Demande la diffusion (`public`, `anonyme`, `interne`) dès qu'un client apparaît.

## Étape 5 : écrire

1. Écris ou mets à jour `Strategie-contenu.md`, section par section, au fil des validations. Remplis "Dernière revue" avec la date du jour.
2. Dans la section Piliers, respecte la forme exacte : `### Pilier N : Nom (XX %)`, une ligne `Portée :`, une ligne `Test :`, puis `Sujets :` et une puce par sujet au format `- Sujet : douleur`.
3. Lance `python3 10_Skills/clean-content/scripts/reconstruire.py --dry-run`, montre ce qui serait créé (une page par pilier, une par sujet), puis relance sans `--dry-run` sur un oui.
4. Si une réponse contredit un fichier de `02_Contexte/` (la voix, l'offre, les clients), propose le diff de ce fichier. Tu n'y écris pas sans un oui explicite.
5. Ajoute une ligne à `Content-Brain/_log.md`.

Termine par un récapitulatif lisible : le positionnement en une phrase, la conviction-phare, les piliers avec leur part, les deux ou trois questions restées ouvertes, et la prochaine action ("Nourris mon brain" si la base est mince, sinon "donne-moi des idées de posts").

## Révision

Sur une stratégie déjà remplie, ne refais pas tout. Lis ce qui a changé depuis "Dernière revue" (nouveaux posts et leurs chiffres, nouveaux calls, nouvelles fiches), rends l'avis de l'étape 3 sur ces écarts, et ne challenge que les sections concernées. Un pilier renommé ou supprimé : préviens que les fiches de ce pilier devront changer de champ `pilier`, et propose de le faire.

## Règles

- Une seule question à la fois. Jamais de liste de questions.
- Tu n'inventes pas le positionnement, les convictions, le ton ni les chiffres. Tu déduis de ce qui est écrit, ou tu demandes.
- Les mots de l'utilisateur ne sont pas réécrits quand ils sont bons.
- Les noms de clients restent hors de la stratégie et des fiches, sauf `contenu: nomme` dans la note du client.
- Tu écris dans `02_Contexte/` uniquement par un diff validé.
- Aucun tiret cadratin ni demi-cadratin dans ce que tu écris.
