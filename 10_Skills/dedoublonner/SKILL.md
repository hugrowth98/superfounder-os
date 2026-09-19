---
name: dedoublonner
description: >
  Exécute le verbe dedoublonner : fusionne une ou plusieurs listes en supprimant les doublons
  (clé LinkedIn, puis email, puis domaine et nom), garde la valeur la plus complète de chaque
  colonne, journalise chaque fusion, et croise avec HubSpot ou avec un fichier de référence
  (déjà contactés, ne plus contacter). Se déclenche sur : "dédoublonne", "fusionne ces
  fichiers", "il y a des doublons", "qui est déjà dans HubSpot", "enlève ceux qu'on a déjà
  contactés", "croise avec le CRM", "liste prospectable". Ne pas utiliser pour : scorer (voir
  `qualifier-liste`), vérifier des emails (voir `trouver-email`), importer dans le CRM (hors
  périmètre de ce verbe, validation explicite requise).
---

## Outil

Interne (script Python, aucun crédit) pour la fusion. Pour le croisement CRM : HubSpot si
`05_Departements/Go-to-Market/OUTILS.md` dit `crm: hubspot` (clé `HUBSPOT_ACCESS_TOKEN`, contacts par email en lots de 100
via `batch/read`, entreprises par domaine via l'API search en lots de 90 ; `domain` n'est pas une
propriété unique, d'où la recherche). Si `crm: aucun`, le croisement se fait contre les fichiers
locaux de référence (`--contre`), par exemple `Listes-prospection/ne_plus_contacter.csv` ou les
listes déjà envoyées. Pas de token : dites-le, renvoyez vers `connecter-outils`, et croisez
contre les fichiers locaux en attendant.

## Entrée

Un ou plusieurs CSV normalisés de même nature (personnes, ou entreprises ; le script détecte,
`--type` force). Personnes : `linkedin_url` normalisée, puis `email`, puis `domaine` + `nom`
(+ initiale du prénom), puis `entreprise` + `nom`. Entreprises : `domaine`, puis
`linkedin_entreprise_url`, puis nom normalisé.

## Sortie

- `Listes-prospection/dedoublonner_<sujet>_<date>.csv` : lignes uniques, URLs LinkedIn
  normalisées, emails en minuscules, `source` concaténée (`unipile+fullenrich`),
  `email_statut` le plus fiable, `score_icp` le plus haut, signal le plus récent dans
  `signal_type` et `signal_date` et tous les signaux dans `signaux` (`type:date | ...`) avec
  `nb_signaux`. Avec `--hubspot` : `dans_crm`, `hubspot_contact_id`, `hubspot_entreprise_id`,
  `hubspot_lifecycle` (annotation seule) ; avec `--hubspot --exclure-crm` : en plus `exclu = oui`,
  `raison_exclusion = deja dans HubSpot (contact)` ou `(entreprise)`. Avec `--contre` : `exclu = oui`,
  `raison_exclusion = deja dans <fichier>`. Avec `--max-par-entreprise N` (défaut 5, `0` = illimité,
  listes de personnes) : au-delà de N personnes par domaine, `exclu = oui`, `raison_exclusion =
  plafond N par entreprise` (meilleur `score_icp` puis ligne la plus remplie gardés).
- `..._doublons.csv` : le journal, une ligne par fusion (`groupe`, `type_cle`, `cle`,
  `ligne_gardee`, `ligne_fusionnee`, `fichier`, `entreprise`, `nom`) et une ligne par personne
  retirée par le plafond (`cle`, `raison`, `email`, `linkedin_url`).

## Procédure

1. Dry-run pour compter : `python3 scripts/dedoublonner.py --in a.csv --in b.csv --dry-run`.
2. Lancez :
   `python3 scripts/dedoublonner.py --in a.csv --in b.csv --sujet "campagne-x"`
   `python3 scripts/dedoublonner.py --in liste.csv --hubspot` (annote `dans_crm`) ou `--hubspot --exclure-crm` (exclut)
   `python3 scripts/dedoublonner.py --in liste.csv --contre Listes-prospection/ne_plus_contacter.csv --contre <derniere liste envoyee>`
   `python3 scripts/dedoublonner.py --in liste.csv --contre Listes-prospection/crm_clients-gagnes_<date>.csv` (export de `crm lire --statut gagnes`, idem pour `perdus`)
3. Lisez les compteurs : lignes lues, uniques, fusions, déjà dans HubSpot, déjà dans les
   références, prospectables. Ouvrez 3 lignes du journal pour vérifier qu'une fusion sur
   `domaine+nom` n'a pas confondu deux homonymes de la même entreprise (le journal le montre).
4. Si `crm: hubspot`, demandez ce qu'on fait des lignes `dans_crm = oui` sans affaire : gardées
   annotées (par défaut) ou exclues (`--exclure-crm`). Les clients gagnés et les affaires perdues
   s'excluent avec l'export de `crm lire --statut gagnes` ou `perdus` passé en `--contre` : le
   script ne calcule aucune catégorie (client, affaire ouverte, churné). Le lifecycle est un indice,
   pas une preuve de relation.
5. Lien cliquable vers les deux fichiers, un seul next step : `trouver-email` s'il manque des
   adresses, sinon `cold-email`.

Règle d'ordre du master `construire-liste` : dédoublonner (entre sources et contre le CRM) avant
d'enrichir et de chercher les emails (on ne paie pas deux fois la même ligne), et contre le CRM
avant tout envoi.

## Garde-fous

- Rien n'est supprimé sans trace : chaque fusion est dans le journal, l'entrée n'est jamais
  écrasée.
- Une clé faible (`entreprise+nom`) ne fusionne que si prénom (initiale) et nom concordent :
  deux "Martin" chez Acme restent deux lignes.
- Le croisement HubSpot lit seulement (contacts, entreprises) : aucune écriture dans le CRM par
  ce verbe.
- Un `exclu = oui` venu d'une source survit à la fusion : on ne réhabilite pas un exclu par
  hasard.
- Pas d'invention pour départager deux valeurs : la plus complète gagne, et pour l'email c'est le
  statut FullEnrich qui tranche.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Deux lignes pour la même personne | URL LinkedIn absente d'un côté, email de l'autre, nom écrit différemment | `enrichir-personne` sur la liste puis relancer |
| Fusion de deux homonymes | même entreprise, même nom, même initiale | reprendre la ligne dans le journal, séparer à la main |
| `dans_crm` partout | domaine générique (gmail) ou domaine du client lui-même | vérifier `domaine`, retirer les domaines génériques avec `qualifier-liste` |
| HubSpot 401 ou 403 | token révoqué ou scopes manquants | `connecter-outils` étape 7 |
| Liste détectée "entreprises" par erreur | colonnes `nom` vides | `--type personnes` |
