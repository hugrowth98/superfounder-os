---
name: trouver-personnes
description: >
  Exécute le verbe trouver_personnes : produit un CSV de décisionnaires par titre, séniorité,
  lieu, taille d'entreprise ou à partir d'un CSV d'entreprises, avec l'outil branché dans
  OUTILS.md. Se déclenche sur : "trouve les DRH de", "les CEO de ces boîtes", "décisionnaires",
  "qui contacter chez", "voici ma recherche Sales Navigator", "les Head of Sales de SaaS français",
  "2 contacts par entreprise", "les gens qui viennent de changer de poste". Ne pas utiliser pour :
  trouver des entreprises (voir `trouver-entreprises`), compléter un profil connu (voir
  `enrichir-personne`) ni trouver un email (voir `trouver-email`).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md` et les personas ATL et BTL de `05_Departements/Go-to-Market/contexte.md` (les titres à chercher). Priorité
`apify` : un actor selon l'entrée. Priorité `api` : Crustdata. Unipile en secours dans les deux
cas (compte LinkedIn de l'utilisateur, recherche classique ou Sales Navigator).

| Entrée | `--source` | Outil | Coût vérifié |
|---|---|---|---|
| Titres, lieu, taille, séniorité, sans cookies | `profils` | `harvestapi/linkedin-profile-search` | 0,10 $ par page de 25 profils (Short), +0,004 $ par profil en Full |
| CSV d'entreprises avec `linkedin_entreprise_url` | `employes` | `harvestapi/linkedin-company-employees` | 0,003 $ par profil (Short) + 0,02 $ par entreprise (mode one_by_one) |
| URL Sales Navigator de leads, cookies dans `.env` | `salesnav` | `curious_coder/linkedin-sales-navigator-search-scraper` | 0,005 $ par résultat |
| URL Sales Navigator ou mots-clés avec le compte de l'utilisateur | `unipile` | Unipile `POST /api/v1/linkedin/search` | abonnement, pas de crédit |
| Priorité api | `crustdata` | Crustdata `POST /screener/persondb/search/` | 3 crédits par tranche de 100 |

Aucun outil branché : dites lequel manque, renvoyez vers `connecter-outils`, ne simulez rien.

## Entrée

Soit des critères (titres du persona, lieu, taille, séniorité), soit un CSV d'entreprises déjà
qualifié (tiers A et B seulement) avec `linkedin_entreprise_url` remplie par
`trouver-entreprises` ou `enrichir-entreprise`, soit une URL de recherche Sales Navigator copiée
depuis le navigateur.

## Sortie

`05_Departements/Go-to-Market/Listes-prospection/trouver-personnes_<sujet>_<date>.csv`, une
ligne par personne : `prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `domaine`,
`linkedin_url`, `linkedin_entreprise_url`, `ville`, `pays`, `source`, `date_extraction`, plus
`headline`, et pour Unipile `provider_id` (nécessaire à `envoyer-sequence`) et `degre_relation`.
Les colonnes `score_icp` et `tier` de l'entreprise source sont recopiées en mode `employes`.
Dédoublonnage par `linkedin_url`.

## Procédure

1. Titres : prenez ceux du persona visé dans `05_Departements/Go-to-Market/contexte.md`, du plus au moins prioritaire, 20
   maximum, en français et en anglais ("Directeur commercial, Head of Sales, VP Sales").
2. Dry-run :
   `python3 scripts/trouver_personnes.py --source employes --in <csv entreprises> --titres "CEO,Fondateur,Directeur Général" --par-entreprise 2 --dry-run`
   `python3 scripts/trouver_personnes.py --source profils --titres "DRH,Head of People" --lieu France --taille 51-200,201-500 --max 100 --dry-run`
   `python3 scripts/trouver_personnes.py --source salesnav --url "https://www.linkedin.com/sales/search/people?..." --max 500 --dry-run`
   `python3 scripts/trouver_personnes.py --source crustdata --titres "Head of Sales,VP Sales" --seniorites "vp,head" --lieu France --max 100 --dry-run`
3. Annoncez volume et coût, attendez le oui, relancez sans `--dry-run`.
4. Sur-sourcez puis plafonnez : `--par-entreprise 2` (tier A : 2 à 4, tier B : 1 à 2, jamais plus
   de 5). Le script garde les meilleurs contacts dans l'ordre des titres demandés, puis par
   séniorité.
5. Vérifiez 3 lignes : le titre correspond au persona, l'entreprise est bien celle du CSV source
   (homonymes fréquents sur les noms courts).
6. Lien cliquable, nombre de lignes, et un seul next step : `enrichir-personne` puis
   `trouver-email` sur les tiers A et B, ou `qualifier-liste` si la liste vient d'une recherche large.

Option `--changement-poste` (sources `profils` et `salesnav`) : seulement les personnes arrivées
en poste depuis moins de 90 jours, un signal à part entière (`signal_type` à poser dans
`detecter-signaux` (script `detecter_signal.py`)).

## Garde-fous

- Pas de recherche de personnes sur des comptes non qualifiés : `qualifier-liste` d'abord.
- `jobTitles` plafonné à 20 par l'actor `employes` : le script coupe la liste, mettez les titres
  importants en premier.
- Source `salesnav` : cookies uniquement depuis `.env`, 500 profils par jour maximum, délais 5 à
  30 s entre pages. Source `unipile` : chaque résultat est une vue depuis le compte LinkedIn de
  l'utilisateur, restez sous 300 profils par jour.
- Plafond 5 contacts par entreprise, quel que soit l'outil.
- Une personne sans URL LinkedIn n'est pas inventée : la ligne reste avec la colonne vide.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `employes` : 0 résultat pour toutes les entreprises | URLs company fausses ou titres trop restrictifs | vérifier 2 URLs à la main, relancer sans `--titres` sur 3 entreprises pour tester |
| `employes` : faux positifs (assistante, stagiaire) | LinkedIn matche sur l'historique des titres | `--par-entreprise` filtre par titre courant ; passez ensuite `qualifier-liste` |
| `profils` : beaucoup de profils hors zone | libellé de lieu ambigu | nom complet du pays ou de la ville ("Paris, Île-de-France") |
| `jobTitles must NOT have more than 20 items` | plus de 20 titres | le script coupe, réduisez la liste |
| `salesnav` : "Cookies are expired" | cookies périmés | `connecter-outils` étape 8 |
| Crustdata : `total_count` énorme, peu de lignes | `--max` bas | relancer avec `--max` plus haut ou segmenter par région |
