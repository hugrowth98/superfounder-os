# Option pubs : les pubs actives d'une entreprise (verbe scraper_pubs)

> Lu par `enrichir-entreprise` quand l'option `--pubs` est demandée. Script : `scripts/scraper_pubs.py`.


## Outil

Apify uniquement, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md` :

| Plateforme | Actor | Entrée | Coût vérifié |
|---|---|---|---|
| Meta (Facebook, Instagram) | `curious_coder/facebook-ads-library-scraper` | recherche par nom dans la bibliothèque (`q=`), ou URL de page Facebook | 0,00075 $ par pub |
| LinkedIn | `s-r/linkedin-ads-library` | nom de l'annonceur, pays, période | 0,005 $ par pub |

Meta renvoie le statut actif ou arrêté et les dates. LinkedIn n'expose pas de statut "en cours" :
la période (`last-30-days` par défaut) tient lieu de filtre "active". Pas de token Apify :
dites-le, renvoyez vers `connecter-outils`.

## Entrée

Un nom d'entreprise, plusieurs noms, une URL de page Facebook, ou un CSV avec `entreprise` (et
`facebook_url` si connue). Pour un signal "concurrent" (section 4 de `05_Departements/Go-to-Market/contexte.md`), la liste
des concurrents nommés dans la section 2 de `05_Departements/Go-to-Market/contexte.md`.

## Sortie

`Listes-prospection/enrichir-entreprise_pubs_<sujet>_<date>.csv`, une ligne par pub : `entreprise`
(annonceur), `source` (nom de l'actor), `date_extraction`, `signal_type` (`pub_active`, ou
`pub_arretee` avec `--toutes`), `signal_date` (début de diffusion), `signal_detail` (plateforme,
date, début du texte), `fraicheur`, plus `plateforme`, `active`, `date_debut`, `date_fin`,
`titre`, `texte`, `cta`, `lien` (page d'atterrissage), `url_pub`, `format`, `canaux` (Meta),
`pays`, `id_pub`, `nb_variantes` (Meta), `porte_parole` et `total_pubs_annonceur` (LinkedIn).
Le résumé en console donne le nombre de pubs par entreprise et par plateforme.

## Procédure

1. Dry-run : `python3 scripts/scraper_pubs.py --entreprises "Acme,Beta" --pays FR --max 50 --dry-run`.
   Coût = entreprises x plateformes x `--max` x prix unitaire.
2. Annoncez, attendez le oui, lancez. Exemples :
   `python3 scripts/scraper_pubs.py --entreprise "Acme" --plateforme meta --page-url https://www.facebook.com/acme`
   `python3 scripts/scraper_pubs.py --in <csv concurrents> --plateforme linkedin --periode last-30-days --max 30`
   `python3 scripts/scraper_pubs.py --entreprise "Acme" --toutes` (Meta : actives et arrêtées, pour l'historique)
3. Vérifiez l'annonceur : une recherche par nom dans la bibliothèque Meta ramène aussi des
   homonymes et des revendeurs, filtrez sur `entreprise` et `page_id`. Sur LinkedIn, `search`
   matche le nom d'annonceur, plus sûr.
4. Lisez ce que ça dit : nombre de pubs actives (investissement), date de début la plus ancienne
   (campagne longue = ça marche), `lien` (l'offre poussée), `cta`, `porte_parole`. C'est de la
   matière pour `cold-email` (parler de leur promesse, pas de leur pub).
5. Lien cliquable, un seul next step : `qualifier-liste` si les annonceurs sont des prospects
   (signal "investit en acquisition"), ou une note de veille concurrentielle si ce sont des
   concurrents.

## Garde-fous

- Coût annoncé avant tout run ; `--max 50` par défaut, monter seulement pour un gros annonceur.
- Une pub trouvée sous un nom n'est pas une preuve : vérifier `page_id` ou `advertiser_name`
  avant d'écrire "vous faites de la pub sur X" à quelqu'un.
- Textes et visuels appartiennent à l'annonceur : on s'en sert pour comprendre le marché, jamais
  pour les reproduire.
- Pas de statut "active" inventé côté LinkedIn : la colonne `active` reste vide, c'est la période
  qui parle.
- Rien n'est complété à la main (domaine, URL LinkedIn de l'annonceur) : `enrichir-entreprise`.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Meta : 0 pub | l'entreprise ne diffuse pas dans ce pays, ou nom mal orthographié | `--pays ALL`, ou passer `--page-url` |
| Meta : pubs d'homonymes | recherche par mot-clé | `--page-url` de la vraie page |
| LinkedIn : réponse vide | l'actor route par proxy résidentiel, parfois bloqué | relancer ; l'actor accepte un `proxy_url` personnel |
| LinkedIn : `total` seul | mode comptage | vérifier `max_ads` > 0 |
| Dates vides côté LinkedIn | `date_range` textuel | lire `date_debut` tel quel, `fraicheur` reste vide |
