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

Lisez les personas ATL et BTL de `05_Departements/Go-to-Market/contexte.md` (les titres à chercher). Sans `--source`, le script
choisit tout seul, dans l'ordre du plus puissant au plus rustique parmi ce qui est branché dans `.env`, et dit pourquoi :

1. **Un outil API de recherche** s'il est branché : Prospeo, puis Crustdata, puis Ocean.io (par domaine ou par cible). Pour un CSV
   d'entreprises, ils demandent des domaines : sans colonne `domaine`, ils sont sautés (ajoutez-la avec `enrichir-entreprise`).
2. **Apify par Sales Navigator** (`salesnav`) : `APIFY_TOKEN` plus les cookies LinkedIn du `.env`, avec une URL Sales Navigator ou des filtres.
3. **Apify par LinkedIn** : `employes` pour un CSV d'entreprises (les URLs de page manquantes sont cherchées par Google, 0,0025 $ chacune),
   `profils` pour une cible par filtres ; avec un CSV de noms, `profils` cherche par lots de 10 noms (`currentCompanies`) et ne garde que
   les profils dont l'entreprise actuelle correspond.
4. **Apify par Google** (`google`) : sans compte LinkedIn ni outil API, une requête `("CEO" OR "Fondateur" ...) "Entreprise"
   site:linkedin.com/in` par entreprise. Le dernier recours, et le second passage automatique pour les entreprises que `employes` ou
   `profils` ont laissées sans personne (`--sans-google` pour l'éviter). Chaque ligne porte une `confiance` (haute : entreprise et titre
   confirmés dans le résultat, moyenne : l'un des deux).

`--source` force un chemin. Une URL Sales Navigator sans cookies Apify passe par Unipile (le compte de l'utilisateur).

| Entrée | `--source` | Outil | Coût vérifié |
|---|---|---|---|
| Entreprises par nom, sans compte ni outil API ; ou une cible par titres et lieu | `google` | `apify/google-search-scraper` | 0,0025 $ par requête (une par entreprise, ou par page de 10 profils) + 0,001 $ par run |
| Titres, lieu, taille, séniorité, sans cookies ; ou un CSV de noms d'entreprises par lots de 10 | `profils` | `harvestapi/linkedin-profile-search` | 0,10 $ par page de 25 profils (Short), +0,004 $ par profil en Full ; un lot de 10 entreprises = une page |
| CSV d'entreprises avec `linkedin_entreprise_url`, ou seulement le nom (URL cherchée par Google) | `employes` | `harvestapi/linkedin-company-employees` | 0,003 $ par profil (Short) + 0,02 $ par entreprise (mode one_by_one) ; + 0,0025 $ par URL cherchée |
| URL Sales Navigator de leads, cookies dans `.env` | `salesnav` | `curious_coder/linkedin-sales-navigator-search-scraper` | 0,005 $ par résultat |
| URL Sales Navigator ou mots-clés avec le compte de l'utilisateur | `unipile` | Unipile `POST /api/v1/linkedin/search` | abonnement, pas de crédit |
| Priorité api | `crustdata` | Crustdata `POST /screener/persondb/search/` | 3 crédits par tranche de 100 |
| Décisionnaires d'entreprises précises (domaines) ou d'une cible Ocean, par titres, séniorités, départements ; plafond par entreprise ; arrivés depuis 90 jours | `ocean` | Ocean.io `POST /api/public_api/v3/search/people` (`includeDomains`, `peoplePerCompany`, `changedPositionAfter`) | crédits Ocean par personne renvoyée (`creditsUsed`) |
| Personnes par titres (contient, similaires avec expansion, ou booléen), séniorités, départements, lieux canoniques, chez des entreprises précises (500 domaines) ou une cible ; email et mobile vérifiés révélés en lot | `prospeo` | Prospeo `POST /search-person` puis `POST /bulk-enrich-person` (`--reveler`) | 1 crédit par page de 25 ; révélation 1 crédit par email vérifié, 10 par mobile, 0 sans résultat ; `--cacher-deja-reveles` évite de payer deux fois |

Aucun outil branché : le script s'arrête en listant la cascade et ce qui manque ; renvoyez vers `connecter-outils` (Apify suffit
pour commencer), ne simulez rien.

## Entrée

Soit des critères (titres du persona, lieu, taille, séniorité), soit un CSV d'entreprises déjà
qualifié (tiers A et B seulement) avec `linkedin_entreprise_url` ou `domaine` remplie par
`trouver-entreprises` ou `enrichir-entreprise` (ou seulement une colonne `entreprise` : les noms suffisent, le script
cherche le reste), soit une URL de recherche Sales Navigator copiée
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
2. Dry-run (sans `--source`, la cascade choisit et l'annonce) :
   `python3 scripts/trouver_personnes.py --in <csv entreprises> --dirigeants --par-entreprise 2 --format large --dry-run`
   `python3 scripts/trouver_personnes.py --source google --in <csv de noms> --dirigeants --par-entreprise 2 --format large --dry-run`
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
   (homonymes fréquents sur les noms courts ; les lignes Google en confiance `moyenne` se vérifient toutes).
6. Lien cliquable, nombre de lignes, et un seul next step : `enrichir-personne` puis
   `trouver-email` sur les tiers A et B, ou `qualifier-liste` si la liste vient d'une recherche large.

Options communes à toutes les sources :
- `--dirigeants` : les 20 titres de dirigeants (CEO, PDG, DG, fondateur, gérant, président, general manager, en français et en anglais) à la place de `--titres`. C'est le plafond des actors harvestapi, et la liste qui marche pour "le décisionnaire d'une PME".
- `--strict-titre` : ne garde que les lignes dont le titre actuel contient un des titres demandés, avec `--titres-exclus` pour sortir les assistants et stagiaires. Les actors LinkedIn matchent aussi sur l'historique des titres : sans ce filtre, un "responsable production" ou une "chargée de communication" peuvent sortir sur une recherche de dirigeants.
- `--par-entreprise 2` : deux décisionnaires par entreprise, choisis par l'ordre des titres demandés puis par séniorité (le CEO avant le co-fondateur).
- `--format large` : en plus du CSV normalisé (une ligne par personne), un fichier `_decisionnaires.csv` avec une ligne par entreprise et les colonnes `d1_prenom`, `d1_nom`, `d1_titre`, `d1_linkedin_url`, `d2_*`. C'est le format qu'on lit avant d'appeler.
- `--enregistrer --nom "<sujet>"` : la requête et son volume vont dans `05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md` ; une URL déjà enregistrée par `construire-requete-salesnav` reçoit son volume automatiquement, sans option.

Avec Prospeo (`--source prospeo`) : la recherche ne révèle ni email ni mobile mais dit leur statut ; `--total-seulement` (1 crédit)
donne le total et la part d'emails vérifiés sur la page 1, avant de payer. `--titres-similaires --intensite NORMAL` élargit un
titre aux titres voisins ("Head of Sales" attrape VP et Director), `--booleen "(CEO OR CTO) AND !intern"` remplace la liste,
`--email-verifie --cacher-deja-reveles` ne garde que ce qu'on peut joindre et qu'on n'a pas déjà payé, `--reveler` obtient les
emails en lot (50 par appel, 1 crédit chacun), `--reveler-mobile` les mobiles (10 crédits). Le détail : `10_Skills/construire-liste/ressources/prospeo-recherche.md`.

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
| `google` : 0 ligne pour une entreprise | nom trop générique, ou personne ne l'affiche sur son profil | `--garder-faibles` pour voir les candidats, ou passer par `employes` avec l'URL de la page |
| `google` : homonyme d'entreprise | le nom court est porté par plusieurs boîtes | ajouter la ville ou le secteur dans `--mots-cles`, vérifier la ligne à la main |
