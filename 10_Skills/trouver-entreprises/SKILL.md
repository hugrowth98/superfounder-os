---
name: trouver-entreprises
description: >
  Exécute le verbe trouver_entreprises : produit un CSV d'entreprises à partir de critères (secteur,
  taille, lieu, mots-clés, URL Sales Navigator) avec l'outil branché dans OUTILS.md. Se déclenche
  sur : "trouve des entreprises", "des boîtes qui", "des agences à Lyon", "des cabinets comptables
  en Île-de-France", "les PME SaaS de 11 à 50", "voici ma recherche Sales Navigator de comptes",
  "une liste de restaurants", "sourcer des comptes". Ne pas utiliser pour : des personnes (voir
  `trouver-personnes`), des entreprises semblables à vos clients (voir `trouver-lookalikes`), ni
  pour scorer une liste existante (voir `qualifier-liste`).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. Priorité `apify` : un des actors ci-dessous selon le besoin. Priorité `api` :
Crustdata. Unipile est utilisable dans les deux cas si l'utilisateur a une recherche Sales
Navigator et un compte connecté. Aucun outil branché : dites lequel manque et renvoyez vers
`connecter-outils`, ne simulez rien.

| Besoin | `--source` | Outil | Coût vérifié |
|---|---|---|---|
| Commerces, services locaux, "à Lyon" | `google-maps` | `compass/crawler-google-places` | 0,003 $ par lieu, +0,001 $ par filtre |
| Filtres LinkedIn (mots-clés, lieu, taille, industrie) | `linkedin` | `harvestapi/linkedin-company-search` | 0,002 $ (short) ou 0,004 $ (full) par entreprise, 20 pages max |
| Base large par industrie, mots-clés, CA, financement | `base-large` | `code_crafter/leads-finder` | 0,002 $ par lead + 0,02 $ par run |
| URL Sales Navigator de comptes, cookies dans `.env` | `salesnav` | `curious_coder/linkedin-sales-navigator-search-scraper` | 0,005 $ par résultat |
| URL Sales Navigator avec le compte de l'utilisateur | `unipile` | Unipile `POST /api/v1/linkedin/search` (category companies) | abonnement, pas de crédit |
| Priorité api | `crustdata` | Crustdata `POST /v1/companies/search` | 1 crédit par recherche |
| Recherche précise : secteurs fins, mots-clés sur la description, technos du site, taille, pays, villes, CA, année, levée, croissance, lookalikes | `ocean` | Ocean.io `POST /api/public_api/v3/search/companies` | crédits Ocean par entreprise renvoyée (`creditsUsed` affiché après le run) ; référentiels et autocomplétion gratuits |
| Recherche précise par filtres exacts, et par modèle d'affaires : à qui ils vendent (`--vend-a`), clients clés, intégrations, lookalike par domaine ou par texte libre, actualités, postes ouverts, levée | `prospeo` | Prospeo `POST /search-company` (industries, lieux, technos résolus par `/search-suggestions`, gratuit) | 1 crédit par page de 25 avec résultats, gratuite si déjà payée sous 30 jours ; `--total-seulement` = 1 crédit ; `--filtres-json` colle le payload du tableau de bord |

## Entrée

Les critères de la demande, complétés par la couche 1 de l'ICP dans `05_Departements/Go-to-Market/contexte.md` (secteur,
effectif, zone). La demande prime, `05_Departements/Go-to-Market/contexte.md` comble les trous. Pas de CSV en entrée.

## Sortie

`05_Departements/Go-to-Market/Listes-prospection/trouver-entreprises_<sujet>_<date>.csv`, une
ligne par entreprise, colonnes normalisées : `entreprise`, `domaine`, `linkedin_entreprise_url`,
`ville`, `pays`, `secteur`, `effectif`, `source`, `date_extraction`. Colonnes en plus selon la
source : `site_web`, `telephone_entreprise`, `adresse`, `note_google`, `nb_avis`, `abonnes`,
`annee_creation`, `chiffre_affaires`, `financement_total`, `technos`, `description`, et pour
`base-large` le dirigeant trouvé au passage (`dirigeant_trouve`, `dirigeant_linkedin_url`,
`dirigeant_email`).

## Procédure

1. Reformulez la cible en une ligne (secteur, taille, zone, volume voulu) et choisissez la source
   avec le tableau. Une seule question si un critère bloquant manque (le lieu pour Google Maps).
2. Dry-run pour montrer l'input et le coût :
   `python3 scripts/trouver_entreprises.py --source linkedin --mots-cles "agence marketing" --lieu France --taille 11-50,51-200 --max 200 --dry-run`
3. Annoncez le coût et le volume, attendez le oui.
4. Relancez sans `--dry-run`. Autres exemples :
   `--source google-maps --recherche "cabinet d'expertise comptable" --lieu "Lyon, France" --max 100 --avec-site`
   `--source base-large --secteur "computer software" --pays france --taille 11-50 --max 300`
   `--source salesnav --url "https://www.linkedin.com/sales/search/company?..." --max 500`
   (l'URL de comptes se construit en texte : `construire-requete-salesnav --comptes --region France --effectif 11-50 --mots-cles SaaS`)
   `--source crustdata --secteur "Software Development" --taille 11-50 --lieu France --max 50`
   `--source ocean --secteur "Human Resources Software" --pays fr --taille 11-50,51-200 --mots-cles "SaaS,logiciel" --max 200 --enregistrer`
   `--source prospeo --secteur "Software Development" --lieu "France" --taille 11-50,51-200 --vend-a "Head of Sales" --total-seulement`
   `--source prospeo --icp-texte "cabinets de recrutement spécialisés tech, 10 à 50 personnes, France" --lookalike-niveau T2 --max 100 --enregistrer`
5. Ouvrez le CSV, vérifiez 3 lignes au hasard (nom, domaine, secteur cohérents), donnez le nombre
   de lignes et le lien cliquable.
6. Un seul next step : `qualifier-liste` (portes d'exclusion et score ICP) avant toute recherche
   de personnes, pour ne pas payer des contacts chez des comptes exclus.

Pour dépasser 1 000 entreprises sur LinkedIn (20 pages de 50), segmentez par lieu ou par taille et
lancez plusieurs runs, puis `dedoublonner`. Pour Sales Navigator, la limite est 2 500 résultats
par recherche : segmentez au-delà.

## Ocean.io : la recherche précise, l'IA comme traducteur

Ocean ne prend pas de texte libre : ses filtres attendent des libellés exacts (secteurs, technologies) et des
structures (mots-clés en "au moins un", "tous", "aucun"). C'est vous, Claude, qui traduisez la demande de
l'utilisateur en filtres, et qui vérifiez le volume avant de payer. La boucle, à chaque demande précise :

1. **Découper la demande** en critères : le métier (secteur), ce que la boîte fait (mots-clés sur sa
   description), sa taille, sa zone, son stade, ses outils. "Des SaaS RH à Paris qui viennent de lever"
   donne : secteur RH + mots-clés SaaS, villes Paris, tailles 11-50 et 51-200, levée depuis 6 mois.
2. **Chercher les libellés exacts**, gratuit :
   `python3 scripts/trouver_entreprises.py --source ocean --lister-secteurs "human resources"` (secteurs, catégories, industries LinkedIn qui contiennent les mots)
   `--lister-technos "hubspot"`, `--lister-mots-cles "recrutement"`, `--lister-lieux "Lyon"` (autocomplétion Ocean).
   Prenez deux ou trois secteurs voisins plutôt qu'un seul : Ocean découpe fin.
3. **Compter avant de payer** : `--total-seulement` avec les mêmes filtres (aperçu gratuit sur un compte
   Enterprise, sinon une seule entreprise facturée). Sous 300, ouvrez un critère (secteur adjacent, mots-clés
   en "au moins un") ; au-dessus de 5 000, resserrez (taille, ville, "tous" les mots-clés, `--technos`).
   Deux ou trois allers-retours suffisent.
4. **Lancer** avec `--max` calé sur le besoin, `--enregistrer --nom "<sujet>"` : la commande, les
   filtres et le volume vont dans `05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md`, pour être rejoués.
5. **Lire** `pertinence` (A, B, C avec `--lookalikes`), `mots_cles`, `technos` et `description` : ce sont eux qui
   disent si la traduction était bonne. Cinq lignes au hasard, sinon on corrige les filtres et on relance.

Les filtres disponibles : `--secteur`, `--categorie`, `--industrie-linkedin`, `--secteurs-exclus`, `--mots-cles` (au
moins un), `--mots-cles-tous`, `--mots-cles-exclus`, `--pays`, `--pays-exclus`, `--villes Ville:fr`, `--taille`,
`--ca`, `--technos`, `--technos-exclues`, `--fondee 2015-2024`, `--levee "Seed,Series A"`, `--levee-depuis`,
`--levee-min`, `--croissance 10` (pourcent d'effectif sur 6 mois), `--lookalikes` (à combiner avec les filtres),
`--relevance-min`, `--exclure-domaines` (vos clients et concurrents). Chaque entreprise sort avec sa page
LinkedIn (`linkedin_entreprise_url`), donc la chaîne continue sans enrichissement : `qualifier-liste`, puis
`trouver-personnes --source ocean --in <csv> --dirigeants` ou `--source employes`.

Le MCP Ocean, s'il est branché, sert à explorer à la main (`find_industries`, `search_companies` en langage
naturel) ; le script reste la voie qui écrit le CSV et le registre.

## Prospeo : la même boucle, avec le modèle d'affaires en plus

Prospeo suit la même boucle qu'Ocean (résoudre, compter, resserrer, lancer), avec trois différences : les valeurs se
résolvent par des suggestions gratuites (`--lister-secteurs`, `--lister-lieux`, `--lister-technos`, `--lister-titres`, et
les scripts le font seuls au vrai run), la page 1 coûte 1 crédit et donne le total (`--total-seulement`), et la cible se
décrit aussi par ce que fait l'entreprise : à qui elle vend (`--vend-a "VP Sales,Head of Sales" --vend-a-tailles smb,midmarket`),
quels clients elle cite (`--clients-cles`), quelles intégrations (`--integrations`), ou un texte libre de 5 000 caractères
(`--icp-texte`, lookalike sans graine, `--lookalike-niveau T1` pour resserrer). Les industries sont celles de LinkedIn :
"SaaS" ne rend rien, "software" rend "Software Development" ; pour "B2B SaaS", `--vend-a` bat toute industrie. Un lieu
Prospeo garde sa virgule (`--lieu "Paris, France"`), plusieurs lieux se séparent par un point-virgule. Le payload construit dans
le tableau de bord Prospeo (bouton "Search API") se colle tel quel avec `--filtres-json`. Le détail des filtres et des
formes à ne pas deviner : `10_Skills/construire-liste/ressources/prospeo-recherche.md`.

## Garde-fous

- Aucun run sans dry-run affiché et oui explicite. Le coût annoncé vient de `apify_run.PRIX`
  (prix vérifiés le 2026-09-19), la facture réelle est affichée en fin de run.
- Les cookies LinkedIn de la source `salesnav` viennent du `.env` (`LINKEDIN_LI_AT`,
  `LINKEDIN_LI_A`, `LINKEDIN_USER_AGENT` ou `LINKEDIN_COOKIES_FILE`), jamais d'un skill ni du chat.
  Pas plus de 500 résultats par jour avec cet actor, délai 5 à 30 s entre pages (compte LinkedIn
  en jeu).
- `--max` plafonné à ce que la demande justifie : on ne sur-source pas "au cas où".
- Une entreprise sans domaine ni URL LinkedIn reste dans le fichier, colonne vide : rien n'est
  inventé.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `APIFY_TOKEN absent du .env` | outil pas branché | `connecter-outils` |
| Google Maps : 0 résultat | lieu mal compris | écrire "Ville, Pays", ou le pays seul (l'actor découpe en sous-zones) |
| LinkedIn : résultats hors zone | libellé de lieu ambigu ("UK" donne Ukraine) | écrire le nom complet, "United Kingdom", "France" |
| `salesnav` : "Cookies are expired" ou 0 résultat | cookies périmés ou `li_a` manquant | refaire l'étape 8 de `connecter-outils` |
| `base-large` : peu de lignes | filtre industrie trop strict | passer par `--mots-cles`, ou élargir les tailles |
| Crustdata : 402 | plus de crédits | recharger, ou basculer `--source linkedin` |
