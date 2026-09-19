---
name: trouver-lookalikes
description: >
  Exécute le verbe trouver_lookalikes : à partir d'une liste de domaines de clients, trouve des
  entreprises qui leur ressemblent avec l'API Ocean.io, en CLI, et les range en CSV normalisé.
  Se déclenche sur : "des boîtes comme mes clients", "lookalikes", "qui ressemble à", "des
  entreprises similaires à acme.fr", "mes meilleurs clients en modèle", "élargis ma liste de
  comptes", "est-ce que ce prospect ressemble à un client". Ne pas utiliser pour : une recherche
  par critères sans clients de référence (voir `trouver-entreprises`) ni pour des personnes
  (voir `trouver-personnes`).
---

## Outil

Ocean.io uniquement, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md`, par l'API
(`OCEAN_API_KEY`, branchée par `connecter-outils`) : `scripts/trouver_lookalikes.py`. Deux appels :
`POST /v3/search/companies/preview` (gratuit : le total disponible) puis `POST /v3/search/companies`
avec `lookalikeDomains` (10 domaines de référence par lot, 0,2 crédit par résultat, pagination
`searchAfter`). Filtres : pays (`--pays fr,be`), tailles (`--tailles 11-50,51-200`), les domaines de
référence sont exclus des résultats. Pas de clé : dites-le et renvoyez vers `connecter-outils`. Le MCP
Ocean reste utilisable en plus pour une exploration à la main.

## Entrée

Un CSV ou une liste de domaines de clients (colonne `domaine`, à défaut `site_web` ou `email`).
Prenez les clients gagnés récents et rentables, pas tous : 5 à 20 domaines suffisent, le script
fait lui-même des lots de 10 (limite d'Ocean par recherche).

## Sortie

`05_Departements/Go-to-Market/Listes-prospection/trouver-lookalikes_<sujet>_<date>.csv` :
`entreprise`, `domaine`, `linkedin_entreprise_url`, `ville`, `pays`, `secteur`, `effectif`,
`source` (`ocean`), `date_extraction`, `signal_type` (`lookalike`), `signal_detail` (à qui ça ressemble), plus
`technos` et `seeds` (les domaines de référence du lot). Les domaines de référence sont retirés.

## Procédure

1. Réunissez les clients de référence : 5 à 20 domaines, vos meilleurs clients ou les gagnés de `crm lire`.
2. Dry-run : `python3 scripts/trouver_lookalikes.py --seeds <csv clients> --pays fr --tailles 11-50,51-200 --max 100 --dry-run`
   (coût au plus `--max` × 0,2 crédit). Annoncez, attendez le oui.
3. Relancez sans `--dry-run` : le script affiche d'abord le total disponible par lot (gratuit), puis
   prend jusqu'à `--max` résultats, fusionne les lots, écarte les domaines de référence et les doublons.
4. Lisez le résultat : `technos` et `secteur` disent pourquoi ça ressemble ; `seeds` dit à quel lot.
5. Lien cliquable, un seul next step : `qualifier-liste` (score ICP), puis `trouver-personnes`.

## Garde-fous

- Pas plus de 10 domaines par appel, et un lot = des clients qui se ressemblent entre eux. Mélanger
  une banque et une boulangerie dans le même lot donne une graine sans sens.
- Ne jamais appliquer `minRelevance` sans demande explicite : ça retire 90 % des résultats sans
  prévenir.
- Toujours retirer les seeds et les clients actuels du résultat (`--seeds`), et croiser avec
  `dedoublonner` si un CRM existe.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `missingDomains` dans la réponse | domaine seed inconnu d'Ocean | corriger le domaine (pas de `www.`), ou le remplacer par un autre client |
| 0 résultat | filtres trop serrés combinés au mode precise | retirer un filtre, ou passer en `broad` |
| HTTP 401 ou 403 | token absent ou révoqué | `connecter-outils`, étape 5 |
| Résultats hors zone | pas de filtre pays | ajouter `primaryLocations.includeCountries: ["fr"]` |
| Le script ne trouve pas les colonnes | export Ocean avec des intitulés inattendus | ouvrir le fichier, renommer la colonne du domaine en `domaine`, relancer |
