---
name: trouver-lookalikes
description: >
  Exécute le verbe trouver_lookalikes : à partir d'une liste de domaines de clients, trouve des
  entreprises qui leur ressemblent avec Ocean.io (MCP), les exporte et les range en CSV normalisé.
  Se déclenche sur : "des boîtes comme mes clients", "lookalikes", "qui ressemble à", "des
  entreprises similaires à acme.fr", "mes meilleurs clients en modèle", "élargis ma liste de
  comptes", "est-ce que ce prospect ressemble à un client". Ne pas utiliser pour : une recherche
  par critères sans clients de référence (voir `trouver-entreprises`) ni pour des personnes
  (voir `trouver-personnes`).
---

## Outil

Ocean.io uniquement, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md`, via le serveur MCP `ocean`
(clé `OCEAN_API_KEY`, branché par `connecter-outils`). Deux outils MCP :

- `search_companies` avec `company_filters.lookalikeDomains` (10 domaines maximum par appel,
  fusionnés en une seule graine) : les entreprises semblables. C'est le cœur du verbe.
- `similar_customers` (domaine d'un prospect) : la question inverse, "lesquels de mes clients
  gagnés ressemblent à ce compte", utile pour une preuve de fit avant un appel.

Coût : 0,2 crédit par résultat au-delà des 10 premiers résultats gratuits de chaque recherche,
0,2 crédit par entreprise exportée. `lookup_company`, `list_company_fields`, `find_industries`
sont gratuits. Pas de MCP Ocean connecté : dites-le et renvoyez vers `connecter-outils`.

## Entrée

Un CSV ou une liste de domaines de clients (colonne `domaine`, à défaut `site_web` ou `email`).
Prenez les clients gagnés récents et rentables, pas tous : 5 à 10 domaines par lot suffisent. Le
script sort les lots : `python3 scripts/normaliser_lookalikes.py --seeds clients.csv --plan`.

## Sortie

`05_Departements/Go-to-Market/Listes-prospection/trouver-lookalikes_<sujet>_<date>.csv` :
`entreprise`, `domaine`, `linkedin_entreprise_url`, `ville`, `pays`, `secteur`, `effectif`,
`source` (`ocean`), `date_extraction`, plus `score_lookalike`, `seed_lot`,
`chiffre_affaires`, `annee_creation`, `technos`, `description`. Les domaines seeds sont retirés.

## Procédure

1. Vérifiez les domaines seeds avec `lookup_company` (gratuit) sur 2 ou 3 d'entre eux : un
   domaine inconnu d'Ocean n'ancre rien. Corrigez les domaines mal écrits.
2. Choisissez le mode : `companyMatchingMode: precise` (même produit ou service, par défaut) ou
   `broad` (même industrie, filet plus large). Ajoutez les filtres de la couche 1 de l'ICP
   (`primaryLocations.includeCountries`, `companySizes`) et `crmFilter.notInCrm: true` si un CRM est
   connecté à Ocean, pour ne pas ressortir des comptes déjà travaillés.
3. Annoncez le coût : `num_results` x 0,2 crédit (les 10 premiers gratuits), plus 0,2 par
   entreprise exportée. Attendez le oui.
4. Appelez `search_companies` par lot de 10 seeds avec
   `company_fields: ["company.name","company.domain","company.industries","company.companySize","company.primaryCountry","company.locations.locality","company.medias","company.revenue","company.yearFounded","company.description"]`
   et `num_results` égal au volume voulu. Sauvegardez la réponse dans un JSON (une liste, ajoutez
   `"seed_lot": 1` sur chaque objet si vous lancez plusieurs lots), ou passez par `export_companies`
   avec tous les domaines en un seul appel et téléchargez le CSV.
5. Normalisez : `python3 scripts/normaliser_lookalikes.py --in resultats.json --seeds clients.csv --sujet "clients-2026"`.
6. Donnez le nombre de lignes, 3 exemples de noms pour validation, le lien cliquable, puis un seul
   next step : `qualifier-liste`, puis `trouver-personnes` sur les tiers A et B.

Pour la question inverse ("ce prospect ressemble-t-il à un client ?"), `similar_customers` avec
`domain` et `num_results: 5`, réponse en chat, pas de CSV.

## Garde-fous

- Pas plus de 10 domaines par appel, et un lot = des clients qui se ressemblent entre eux. Mélanger
  une banque et une boulangerie dans le même lot donne une graine sans sens.
- Ne jamais appliquer `minRelevance` sans demande explicite : ça retire 90 % des résultats sans
  prévenir.
- Toujours retirer les seeds et les clients actuels du résultat (`--seeds`), et croiser avec
  `dedoublonner` si un CRM existe.
- Une réponse MCP tronquée (trop grande) : réduisez `num_results` ou passez par `export_companies`.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `missingDomains` dans la réponse | domaine seed inconnu d'Ocean | corriger le domaine (pas de `www.`), ou le remplacer par un autre client |
| 0 résultat | filtres trop serrés combinés au mode precise | retirer un filtre, ou passer en `broad` |
| Erreur d'authentification MCP | clé absente ou révoquée | `connecter-outils`, étape 5 |
| Résultats hors zone | pas de filtre pays | ajouter `primaryLocations.includeCountries: ["fr"]` |
| Le script ne trouve pas les colonnes | export Ocean avec des intitulés inattendus | ouvrir le fichier, renommer la colonne du domaine en `domaine`, relancer |
