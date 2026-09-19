# Option techno : la stack technique d'un domaine (verbe detecter_techno)

> Lu par `enrichir-entreprise` quand l'option `--techno` est demandée. Script : `scripts/detecter_techno.py`.


## Outil

Apify `scrapemint/website-tech-stack-detector`, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md`. Prix
vérifié : 0,01 $ par domaine avec au moins une détection, gratuit pour un site injoignable ou sans
détection, la première ligne de chaque run est offerte. Une requête polie par site, pas de proxy.
Pas de token Apify : dites-le, renvoyez vers `connecter-outils`.

## Entrée

Un CSV avec `domaine` (à défaut `site_web` ou `email`, le script en tire le domaine), ou une
liste de domaines en ligne de commande. La couche 2 de l'ICP dans `05_Departements/Go-to-Market/contexte.md` dit quelles
technos comptent : l'outil qui rend l'offre pertinente, et l'outil concurrent déjà en place.

## Sortie

`Listes-prospection/enrichir-entreprise_techno_<sujet>_<date>.csv`, une ligne par domaine : `entreprise`,
`domaine`, `linkedin_entreprise_url`, `secteur`, `effectif` (recopiés de l'entrée), `source`
(nom de l'actor), `date_extraction`, `signal_type` (`techno`), `signal_date`, `signal_detail`,
`fraicheur`, plus `joignable`, `nb_technos`, `technos` (tout, séparé par `|`), et une colonne
par catégorie : `cms`, `ecommerce`, `analytics`, `marketing`, `chat`, `crm`, `paiement`,
`hebergement`, `framework`. Avec `--cherche` : `techno_cible` (oui/non) et
`techno_cible_detail`. Avec `--diff` : `ajouts`, `retraits`, `dernier_run`, et un second fichier
`..._diff.csv` avec une ligne par changement (`signal_type` `techno_ajout` ou `techno_retrait`,
colonne `techno`). L'historique vit dans `scripts/historique_technos.json`.

## Procédure

1. Dry-run : `python3 scripts/detecter_techno.py --in <csv> --dry-run` (coût = nombre de
   domaines x 0,01 $ au plus).
2. Annoncez, attendez le oui, lancez. Exemples :
   `python3 scripts/detecter_techno.py --in <csv> --cherche "hubspot,pipedrive,salesforce"`
   `python3 scripts/detecter_techno.py --domaines acme.fr,beta.com`
   `python3 scripts/detecter_techno.py --in Signaux/comptes-suivis.csv --diff`
3. Lisez le résultat par catégorie : `cms` et `ecommerce` disent la maturité, `marketing`,
   `chat` et `crm` disent l'équipement commercial, `paiement` dit s'il y a du transactionnel.
4. Mode diff en routine (mensuelle sur une liste suivie) : un `techno_ajout` sur un outil de la
   couche 2 est un signal daté du jour du run, à passer dans `qualifier-liste` avec la fenêtre de
   90 jours de `05_Departements/Go-to-Market/contexte.md`.
5. Lien cliquable, un seul next step : `qualifier-liste` (les points de la couche 2 se calculent
   sur `techno_cible` et sur les colonnes par catégorie).

## Garde-fous

- Coût annoncé avant tout run, même à 0,01 $ : 2 000 domaines font 20 $.
- Le détecteur voit ce qui est visible sur la page d'accueil : un outil absent des colonnes n'est
  pas forcément absent de l'entreprise. Ne jamais écrire "n'utilise pas X" dans un message, écrire
  "je n'ai pas vu X sur votre site".
- Le diff ne vaut qu'entre deux runs sur les mêmes domaines : `dernier_run` vide = première
  vue, pas de signal.
- Domaine injoignable : ligne conservée avec `joignable = non`, rien de deviné.
- Un domaine par entreprise : passez `dedoublonner` avant, le script ne facture pas deux fois
  mais l'historique s'écrase.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `aucun domaine` | colonnes `domaine`, `site_web`, `email` vides | l'enrichissement de base d'abord (`enrichir_entreprise.py --in <csv>`) |
| Beaucoup de `joignable = non` | sites qui bloquent les IP datacenter | relancer plus tard ; l'actor accepte un `proxyConfiguration` si l'utilisateur en a un |
| `techno_cible` vide | `--cherche` absent | passer les noms d'outils de la couche 2 |
| `_diff.csv` vide | premier run, ou aucune évolution | normal ; relancer à la prochaine échéance |
| Catégorie inattendue (un CRM classé marketing) | libellé de catégorie de l'actor | lire `technos` (complet), ajuster la règle dans `qualifier-liste` |
