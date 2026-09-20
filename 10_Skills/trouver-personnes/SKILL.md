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
| Décisionnaires d'entreprises précises (domaines) ou d'une cible Ocean, par titres, séniorités, départements ; plafond par entreprise ; arrivés depuis 90 jours | `ocean` | Ocean.io `POST /api/public_api/v3/search/people` (`includeDomains`, `peoplePerCompany`, `changedPositionAfter`) | crédits Ocean par personne renvoyée (`creditsUsed`) |

Aucun outil branché : dites lequel manque, renvoyez vers `connecter-outils`, ne simulez rien.

## Entrée

Soit des critères (titres du persona, lieu, taille, séniorité), soit un CSV d'entreprises déjà
qualifié (tiers A et B seulement) avec `linkedin_entreprise_url` remplie par
`trouver-entreprises` ou `enrichir-entreprise`, soit une URL de recherche Sales Navigator copiée
depuis le navigateur ou construite en texte par `construire-requete-salesnav` (titres, région,
effectif, relation, et les filtres à cocher : a consulté votre profil, suit votre page, a publié,
a changé de poste).

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
   `python3 scripts/trouver_personnes.py --source ocean --in <csv entreprises avec domaine> --dirigeants --par-entreprise 2 --format large --dry-run`
   `python3 scripts/trouver_personnes.py --source ocean --secteur "Human Resources Software" --lieu fr --seniorites fondateur,cxo --max 100 --dry-run`
3. Annoncez volume et coût, attendez le oui, relancez sans `--dry-run`.
4. Sur-sourcez puis plafonnez : `--par-entreprise 2` (tier A : 2 à 4, tier B : 1 à 2, jamais plus
   de 5). Le script garde les meilleurs contacts dans l'ordre des titres demandés, puis par
   séniorité.
5. Vérifiez 3 lignes : le titre correspond au persona, l'entreprise est bien celle du CSV source
   (homonymes fréquents sur les noms courts).
6. Lien cliquable, nombre de lignes, et un seul next step : `enrichir-personne` puis
   `trouver-email` sur les tiers A et B, ou `qualifier-liste` si la liste vient d'une recherche large.

Options communes à toutes les sources :
- `--dirigeants` : les 20 titres de dirigeants (CEO, PDG, DG, fondateur, gérant, président, general manager, en français et en anglais) à la place de `--titres`. C'est le plafond des actors harvestapi, et la liste qui marche pour "le décisionnaire d'une PME".
- `--strict-titre` : ne garde que les lignes dont le titre actuel contient un des titres demandés, avec `--titres-exclus` pour sortir les assistants et stagiaires. Les actors LinkedIn matchent aussi sur l'historique des titres : sans ce filtre, un "responsable production" ou une "chargée de communication" peuvent sortir sur une recherche de dirigeants.
- `--par-entreprise 2` : deux décisionnaires par entreprise, choisis par l'ordre des titres demandés puis par séniorité (le CEO avant le co-fondateur).
- `--format large` : en plus du CSV normalisé (une ligne par personne), un fichier `_decisionnaires.csv` avec une ligne par entreprise et les colonnes `d1_prenom`, `d1_nom`, `d1_titre`, `d1_linkedin_url`, `d2_*`. C'est le format qu'on lit avant d'appeler.
- `--enregistrer --nom "<sujet>"` : la requête et son volume vont dans `05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md` ; une URL déjà enregistrée par `construire-requete-salesnav` reçoit son volume automatiquement, sans option.

La chaîne courte "des entreprises précises vers leurs décisionnaires", en trois commandes :
`trouver-entreprises --source ocean ...` (ou toute autre source), puis `enrichir-entreprise --source ocean` si la
colonne `linkedin_entreprise_url` ou `domaine` manque, puis `trouver-personnes --source ocean --in <csv> --dirigeants
--par-entreprise 2 --format large` (par domaine, sans compte LinkedIn) ou `--source employes --in <csv> --dirigeants
--strict-titre --par-entreprise 2 --format large` (par page LinkedIn, actor harvestapi).

Option `--changement-poste` (sources `profils` et `salesnav`) : seulement les personnes arrivées
en poste depuis moins de 90 jours, un signal à part entière.

Option `--signal <type>` (toutes sources, pensée pour une URL Sales Navigator à filtre) : pose
`signal_type`, `signal_date` (la date du run, pas celle de l'action), `signal_detail` et
`fraicheur` sur chaque ligne. Types : `visite_profil`, `abonne_entreprise`, `a_publie`,
`changement_poste`. Exemple : `--source unipile --url "<url avec --vues-profil>" --signal
visite_profil`. Les sous-skills `visite-profil`, `abonnes-entreprise`, `a-publie` et
`changement-poste` de `detecter-signaux` s'en servent ; la fenêtre et le diff contre le run
précédent (`dedoublonner --contre`) sont décrits là-bas.

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
