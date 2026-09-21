---
name: construire-requete-salesnav
description: >
  Exécute le verbe construire_requete_salesnav : transforme des critères en texte (titres ou booléen,
  région, effectif, séniorité, niveau de relation, entreprise actuelle, et les filtres à cocher : a
  consulté votre profil, suit votre page, a publié récemment, a changé de poste) en URL de recherche
  Sales Navigator prête à coller dans le navigateur ou à passer à `trouver-personnes --url` et
  `trouver-entreprises --url` ; sait aussi lire une URL existante et retrouver l'id d'une région ou
  d'un secteur. Se déclenche sur : "construis une requête Sales Nav", "URL Sales Navigator", "les CTO
  en France sur Sales Nav", "qui a visité mon profil", "qui suit ma page", "qui a publié", "en
  relation de 1er niveau", "décode cette URL", "l'id de la région". Ne pas utiliser pour lancer la
  recherche (voir `trouver-personnes`), ni pour choisir les titres d'un persona (voir
  `sourcer-personnes` et `cartographier-personas`).
---

## Outil

Interne : `scripts/construire_requete_salesnav.py`, aucun crédit. L'URL produite se lance ensuite avec le
compte LinkedIn de l'utilisateur (Unipile, `trouver-personnes --source unipile --url`, inclus dans
l'abonnement) ou avec ses cookies (`--source salesnav`, actor
`curious_coder/linkedin-sales-navigator-search-scraper`, 0,005 $ par résultat), ou dans le navigateur.
Unipile est facultatif ici : il ne sert qu'à retrouver l'id d'une région, d'un secteur, d'une
entreprise ou d'une liste que le script ne connaît pas (`GET /api/v1/linkedin/search/parameters`,
gratuit). Sans Unipile, l'id se lit dans une URL faite une fois dans l'interface, avec `--decoder`.

## Entrée

Des critères en texte. Les titres viennent de la demande ou de la fiche ATL ou BTL de
`05_Departements/Go-to-Market/contexte.md` (`--persona atl`). Pas de CSV.

## Sortie

Une URL `https://www.linkedin.com/sales/search/people?query=...` (ou `/company` avec `--comptes`),
un résumé lisible des filtres, et sur demande une ligne dans
`05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md` (`--enregistrer` : date, nom, persona,
filtres, URL, volume à remplir après le run).

## Procédure

1. Traduisez la demande en filtres : le persona (titres), la zone, la taille, puis les filtres à cocher
   qui font le signal (`--vues-profil`, `--suit-entreprise`, `--a-publie`, `--nouveau-poste`).
2. Construisez et lisez le résumé :
   `python3 scripts/construire_requete_salesnav.py --titres "CEO,Fondateur,Directeur Général" --titres-exclus "assistant,stagiaire" --region France --effectif 11-50,51-200`
   `python3 scripts/construire_requete_salesnav.py --persona atl --region France --vues-profil --nom "visites ATL" --enregistrer`
   `python3 scripts/construire_requete_salesnav.py --titres CMO --relation 1`
   `python3 scripts/construire_requete_salesnav.py --titres CMO --entreprises "Growth Hiring,Scalezia"`
   `python3 scripts/construire_requete_salesnav.py --comptes --region France --effectif 11-50 --mots-cles "SaaS RH"`
3. Une région ou un secteur inconnus : `--resoudre region:Lyon` (Unipile) ou décodez une URL faite dans
   l'interface : `--decoder "<url>"`. Sans les deux, donnez l'id numérique.
4. Collez l'URL dans le navigateur pour lire le total, ou passez directement au run :
   `trouver-personnes --source unipile --url "<url>" --max 100 --dry-run`, avec `--signal <type>` quand
   l'URL porte un filtre à cocher (le CSV reçoit `signal_type`, `signal_date`, `signal_detail`).
5. Au-delà de 2 500 résultats, découpez par région, par tranche d'effectif ou par première lettre du
   prénom : une URL par tranche, `dedoublonner` ensuite.
6. Un seul next step : `exporter-salesnav` (l'URL en CSV, avec le signal posé), qui s'appuie sur `trouver-personnes` (ou `trouver-entreprises` pour une recherche de comptes).

## Filtres pris en charge

| Option | Filtre Sales Navigator | Valeur | Vérifié |
|---|---|---|---|
| `--titres`, `--titres-exclus`, `--booleen-titre` | `CURRENT_TITLE` | booléen `("A" OR "B") NOT (C)` | oui, URL de l'interface |
| `--mots-cles` | `keywords` | texte libre | même encodage |
| `--entreprises`, `--entreprises-exclues` | `CURRENT_COMPANY` | `"Nom 1" OR "Nom 2"` | oui |
| `--anciennes-entreprises` | `PAST_COMPANY` | idem | même mécanique |
| `--region`, `--regions-exclues` | `REGION` | id (France 105015875, États-Unis 103644278) ou libellé résolu | oui pour France |
| `--effectif` | `COMPANY_HEADCOUNT` | ids A (indépendant), B 1-10, C 11-50, D 51-200, E 201-500, F 501-1000, G 1001-5000, H 5001-10000, I 10001+ | repris de l'actor, à confirmer au premier run |
| `--seniorites` | `SENIORITY_LEVEL` | owner 320, cxo 310, vp 300, director 220, manager 210, senior 120, entry 110 | repris de l'actor, à confirmer |
| `--relation` | `RELATIONSHIP` | 1 = F, 2 = S, 3 = O | F vérifié |
| `--vues-profil` | `VIEWED_YOUR_PROFILE` | id VYP | oui |
| `--a-publie` | `POSTED_ON_LINKEDIN` | id RPOL (30 derniers jours) | oui |
| `--suit-entreprise` | `FOLLOWS_YOUR_COMPANY` | id CF | oui |
| `--nouveau-poste` | `RECENTLY_CHANGED_JOBS` | id RPC (90 derniers jours) | oui |
| `--secteur` | `INDUSTRY` | id résolu par `--resoudre secteur:<mot>` | à confirmer |
| `--liste-comptes`, `--liste-leads` | `ACCOUNT_LIST`, `LEAD_LIST` | id de la liste (`--resoudre liste-comptes:<nom>`) | recette vérifiée pour ACCOUNT_LIST |
| `--filtre TYPE:id[:texte[:EXCLUDED]]` | n'importe quel type | libre | pour les filtres non listés (`COMPANY_TYPE`, `FUNCTION`, `YEARS_AT_CURRENT_COMPANY`...) |

Les quatre filtres à cocher ne marchent qu'avec le compte concerné : c'est votre profil qu'on a consulté,
votre page qu'on suit. Unipile (votre compte) et vos cookies conviennent ; Crustdata et les actors sans
cookies ne les connaissent pas.

## Encodage

Les parenthèses de structure restent brutes, `:` et `,` de structure sont encodés une fois, chaque
valeur de filtre est encodée deux fois (espace `%2520`, guillemet `%2522`, parenthèse d'un booléen
`%2528`, accent `%25C3%25A9`). `recentSearchParam` et `sessionId` sont propres à une session : le
script ne les met pas, une recherche s'ouvre sans eux. `--decoder` relit tout ça et rend une URL
propre. La recette a été vérifiée contre sept URL produites par l'interface (titres avec accents et
booléen de 27 termes, relation, région, entreprise, et les quatre filtres à cocher).

## Garde-fous

- Le script n'appelle rien de payant. Les ids inconnus passent par Unipile (gratuit) seulement si les
  clés sont dans `.env` ; sinon il s'arrête et dit comment trouver l'id.
- Une URL enregistrée dans `Ciblage/requetes-booleennes.md` porte un nom et une date : c'est ce qu'on
  rejoue chaque semaine pour les signaux `visite-profil`, `abonnes-entreprise` et `a-publie`.
- Pas plus de 2 500 résultats par recherche côté LinkedIn ; le run reste soumis aux quotas de
  `05_Departements/Go-to-Market/GARDE-FOUS.md`.
- Le booléen exclut par défaut ce que `sourcer-personnes` exclut : ajoutez `--titres-exclus
  "assistant,stagiaire,alternant"` sur toute recherche large.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Sales Navigator ouvre la recherche vide | un id de région ou de secteur faux | `--resoudre region:<nom>` ou `--decoder` sur une URL faite dans l'interface |
| `[stop] Unipile n'est pas branché` | libellé de région inconnu du script et pas de clé Unipile | donner l'id numérique, ou `connecter-outils` |
| `fiche ATL : les titres ne sont pas remplis` | `contexte.md` section 3 vide | `installer-gtm` phase 3, ou `--titres` |
| 0 résultat avec `--vues-profil` ou `--suit-entreprise` | run avec un compte qui n'est pas le vôtre | `--source unipile` (votre compte) ou vos cookies |
| Le booléen est tronqué | plus de 1 000 caractères | moins de titres, ou deux requêtes |
