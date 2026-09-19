# Exécution : le script Signalbase (verbe detecter_signal)

> Lu par le master et ses sous-skills au moment de lancer une détection. Le script est `{SKILL_BASE}/scripts/detecter_signal.py`.


## Outil

Apify `signalbase/signalbase-api`, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md` (aucun outil API
de la stack ne couvre ce verbe). Prix vérifié : 0,04 $ par résultat, 100 résultats par page au
plus. Six types : `funding`, `acquisitions`, `hiring`, `job-changes`, `investors`, `companies`.
Filtres utiles : `countries` (FR,BE,CH), `date_preset` (last_7d, last_30d, last_90d...), `round`,
`amount_min` (en cents, le script convertit depuis des dollars), `positions`, `seniorities`,
`departments`, `search`, `industry`, `personLinkedinUrl` et `companyLinkedinUrl` (job-changes,
URL exacte). Pas de token Apify : dites-le et renvoyez vers `connecter-outils`.

## Entrée

Soit un marché (pays, période, filtres du signal), soit une liste suivie : un CSV d'entreprises
(`linkedin_entreprise_url`, `domaine`, `entreprise`) ou de personnes (`linkedin_url`), rangé dans
`05_Departements/Go-to-Market/Signaux/`. Les signaux prioritaires et leur fraîcheur maximale sont
dans la section 4 de `05_Departements/Go-to-Market/contexte.md` : ne lancez que ceux-là, sur leur fenêtre.

## Sortie

`Listes-prospection/detecter-signaux_<type>-<sujet>_<date>.csv`, une ligne par signal :
`entreprise`, `domaine`, `linkedin_entreprise_url`, `ville`, `pays`, `secteur`, `effectif`,
`source` (`signalbase/signalbase-api`), `date_extraction`, `signal_type`, `signal_date`,
`signal_detail`, `fraicheur` (jours écoulés depuis `signal_date`, le multiplicateur de fraîcheur
est appliqué par le master `detecter-signaux`), et pour `job-changes` `prenom`, `nom`, `titre`,
`seniorite`, `linkedin_url`. Colonnes en plus selon le
type : `round`, `montant_usd`, `investisseurs`, `url_source` (funding), `acquereur` et son URL
(acquisitions), `poste`, `url_offre`, `seniorite_offre`, `nb_candidats` (hiring),
`post_annonce` (job-changes), `signal_id` pour dédoublonner entre deux runs.

## Procédure

1. Traduisez la demande en type + filtres, et vérifiez la fenêtre dans `05_Departements/Go-to-Market/contexte.md` (une levée
   se travaille de 2 à 12 semaines, un changement de poste de 14 à 90 jours).
2. Dry-run : `python3 scripts/detecter_signal.py --type funding --pays FR --periode last_30d --round "Seed,Series A" --limite 100 --dry-run`.
   Le coût est `limite x pages x 0,04 $` : 100 résultats = 4 $.
3. Annoncez volume et coût, attendez le oui, relancez sans `--dry-run`. Exemples :
   `--type job-changes --pays FR --positions "ceo,vp of sales,head of growth" --periode last_14d --limite 100`
   `--type hiring --pays FR --search "SDR" --departements sales --periode last_7d --limite 100`
   `--type acquisitions --pays FR,BE --periode last_90d --limite 50`
4. Liste suivie : `--liste-suivie Signaux/comptes-suivis.csv` garde seulement les signaux qui
   concernent ces comptes ou ces personnes (filtre après le run, coût du run complet). Pour des
   changements de poste sur peu de comptes, `--par-cible` lance une requête exacte par entreprise
   (`companyLinkedinUrl`), coût = comptes x limite x 0,04 $ : préférez-le sous 30 comptes.
5. Relisez 3 signaux : la date est dans la fenêtre, l'entreprise est bien celle nommée (les
   homonymes existent), `signal_detail` se lit seul.
6. Lien cliquable, nombre de signaux, un seul next step : `qualifier-liste` (score ICP et
   `score_signal` selon `05_Departements/Go-to-Market/contexte.md`), puis `trouver-personnes` sur les comptes retenus.

Deux runs sur la même fenêtre produisent des doublons : `dedoublonner` sur `signal_id` ou sur
`linkedin_entreprise_url` + `signal_date`.

## Garde-fous

- Aucun run sans coût annoncé : à 0,04 $ le résultat, 1 000 signaux valent 40 $. Commencez à
  `--limite 50`, élargissez si la qualité est là.
- `--pages` au-delà de 1 n'est utile que si l'actor honore la pagination : vérifiez qu'une page 2
  ne renvoie pas les mêmes `signal_id` avant d'en enchaîner dix.
- Les montants renvoyés par l'API sont en cents : le script écrit `montant_usd` en dollars,
  ne le reconvertissez pas.
- Un signal n'est pas une preuve : `verification` vaut `verified`, `unverified` ou `pending`,
  gardez la colonne et citez `url_source` dans un message plutôt que le montant.
- Rien n'est complété à la main : entreprise sans domaine ni URL LinkedIn, colonne vide, à passer
  par `enrichir-entreprise`.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| 0 résultat sur `job-changes` avec `--positions` | libellés hors liste (ceo, cto, cfo, coo, vp of sales, vp of marketing, head of product, head of growth, founder...) | reprendre les libellés exacts, ou `--seniorites c_level,vp` |
| Résultats hors pays | `--pays` absent | codes ISO en majuscules, séparés par des virgules |
| Page 2 identique à la page 1 | pagination ignorée par l'actor en mode run | rester sur une page, affiner les filtres |
| `amount_min` sans effet | montant donné en cents | donner des dollars, le script convertit |
| Liste suivie : 0 signal | URLs non normalisées ou domaines absents | remplir `linkedin_entreprise_url` et `domaine` via `enrichir-entreprise`, relancer |
| HTTP 402 Apify | crédit épuisé | recharger le compte Apify |
