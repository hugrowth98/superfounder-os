---
name: qualifier-liste
description: >
  Exécute le verbe qualifier_liste : applique les portes d'exclusion et le barème ICP de
  contexte.md à un CSV (entreprises ou personnes), écrit `score_icp`, `tier`, `exclu`,
  `raison_exclusion`, et rend la liste triée par score plus le fichier des exclus. Aucun outil
  externe : un pré-traitement déterministe (classification des titres, séniorité, effectif,
  domaine), puis le jugement de Claude traduit en règles et en corrections. Se déclenche sur :
  "qualifie cette liste", "score ces prospects", "qui est prioritaire", "enlève les B2C",
  "enlève les concurrents", "tier A", "trie par ICP", "combien sont dans ma cible". Ne pas
  utiliser pour : les doublons (voir `dedoublonner`), les emails invalides (voir
  `trouver-email`), ni pour définir l'ICP lui-même (master `construire-liste`, `definir-icp`).
---

## Outil

Interne, quelle que soit `05_Departements/Go-to-Market/OUTILS.md`. Deux scripts sans appel API :
`scripts/pre_qualifier.py` (pré-traitement) et `scripts/finaliser_qualification.py` (portes,
barème, tiers, corrections). Le barème et les exclusions viennent de la section 2 de
`05_Departements/Go-to-Market/contexte.md` : s'il reste des crochets dedans, arrêtez et proposez `installer-gtm`.

## Entrée

Un CSV normalisé (sortie de n'importe quel verbe). Le score utilise ce qui est là : `secteur`,
`effectif`, `pays` ou `ville`, `technos`, `signal_type` et `fraicheur`, `titre` ou `headline`.
Plus les colonnes sont remplies, plus le score est fiable : `enrichir-entreprise` avant, si
`secteur` et `effectif` manquent.

## Sortie

- `Listes-prospection/qualifier-liste_<sujet>_<date>.csv` : toutes les lignes, les gardées d'abord triées par
  `score_icp` décroissant, puis les exclues (`exclu = oui`, `raison_exclusion`), avec `tier` (A, B, C, D), `detail_score` (les points par
  critère, lisibles), et les colonnes du pré-traitement : `categorie_titre` (dirigeant,
  marketing, sales, direction, manager, independant, executant, stagiaire, inconnu),
  `seniorite`, `independant`, `effectif_num`, `taille_tranche`, `domaine_generique`, `cle`.
- `..._exclus.csv` : les lignes exclues avec `raison_exclusion` (porte ou score sous le seuil C).

## Procédure

1. Pré-traitement : `python3 scripts/pre_qualifier.py --in <csv>` écrit `<csv>_pre.csv` et
   affiche la répartition par catégorie de titre.
2. Traduisez `05_Departements/Go-to-Market/contexte.md` en `regles.json` (rangé à côté de la liste, nom
   `qualifier-liste_<sujet>_regles.json`) : un bloc `exclusions` par ligne de la section
   "Exclusions" (B2C, concurrents nommés, secteurs, tailles, autres), un bloc `points` par
   critère des trois couches avec les valeurs cibles et adjacentes et les points de la table, les
   `fraicheur_max` de la section 4 pour la couche 3, le `bonus_empilement`, les seuils de tiers.
   Le format exact est dans l'en-tête de `finaliser_qualification.py`. Montrez le JSON à
   l'utilisateur en 5 lignes ("j'exclus X, je donne 15 points à Y") avant de l'appliquer.
3. Ce que les règles ne voient pas, vous le jugez ligne à ligne et l'écrivez dans `scores.csv`
   (colonnes `cle`, `score_icp`, `tier`, `exclu`, `raison_exclusion`, `note`) : une entreprise
   B2C reconnaissable à sa description, un concurrent sous un autre nom, un "CEO" qui est un
   indépendant, une personne de la liste "ne jamais contacter" de la section 7. Lisez les lignes
   en `categorie_titre` `inconnu` et `direction`, les `domaine_generique = oui`, et un échantillon
   de 20 lignes gardées.
4. Finalisez : `python3 scripts/finaliser_qualification.py --in <csv>_pre.csv --regles regles.json --scores scores.csv`.
5. Rendez le rapport en entonnoir : lignes lues, exclues par raison (top 5), gardées par tier,
   puis le lien cliquable vers les deux fichiers, et un seul next step : `trouver-personnes` sur
   les tiers A et B (liste d'entreprises) ou `enrichir-personne` puis `trouver-email` (liste de
   personnes).

Sur plus de 300 lignes, ne relisez pas tout : les règles font le gros, vos corrections portent
sur les cas ambigus que le pré-traitement signale.

## Garde-fous

- Aucun critère inventé : tout vient de `05_Departements/Go-to-Market/contexte.md`. Un critère absent du fichier, c'est une
  question à l'utilisateur, pas une supposition.
- Les portes d'exclusion passent avant le score : un concurrent à 95 points reste exclu.
- Une donnée manquante ne vaut jamais un point (ni une exclusion, sauf `vide_exclut`
  explicite) : un effectif vide donne 0 sur ce critère, dites combien de lignes sont dans ce cas.
- Le pré-traitement classe sur le poste actuel (`titre`) avant le `headline` marketing : un
  "CEO" en headline avec un poste de consultant est un indépendant.
- Ne pas mélanger deux listes de nature différente (entreprises et personnes) dans un même run :
  le barème n'est pas le même.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Tout le monde en tier D | seuils ou points de `regles.json` trop hauts, colonnes vides | vérifier `detail_score` sur 3 lignes, remplir `secteur` et `effectif` (`enrichir-entreprise`) |
| `categorie_titre = inconnu` massif | `titre` et `headline` vides | `enrichir-personne` d'abord |
| Correction de `scores.csv` sans effet | `cle` différente (URL non normalisée, majuscules) | copier la colonne `cle` du fichier `_pre.csv` |
| Signal jamais compté | `fraicheur` vide ou supérieure à `fraicheur_max` | vérifier `signal_date` dans la source |
| Un B2C passe | aucune colonne ne le dit | le juger sur `description` ou le site, l'exclure dans `scores.csv` |
| Score plafonné à 100 avec des points en trop | barème mal réparti | réajuster les pondérations dans `05_Departements/Go-to-Market/contexte.md`, pas dans le JSON seul |
