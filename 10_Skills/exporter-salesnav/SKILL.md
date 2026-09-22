---
name: exporter-salesnav
description: >
  Exporte une recherche Sales Navigator (une URL de leads ou de comptes, copiée du navigateur
  ou construite par `construire-requete-salesnav`) en CSV normalisé, avec votre compte LinkedIn
  (Unipile) ou vos cookies (Apify), et pose le signal quand l'URL porte un filtre à cocher
  (a consulté votre profil, suit votre page, a publié, a changé de poste). Se déclenche sur :
  "exporte cette recherche Sales Navigator", "sors-moi cette liste Sales Nav", "voici mon URL
  Sales Navigator", "les gens qui ont vu mon profil, en CSV", "exporte les 200 premiers". Ne pas
  utiliser pour construire l'URL (voir `construire-requete-salesnav`) ni pour une recherche
  sans URL (voir `trouver-personnes`, `trouver-entreprises`).
---

## Outil

Le script de `trouver-personnes` (`10_Skills/trouver-personnes/scripts/trouver_personnes.py`) avec `--url`, ou celui de `trouver-entreprises` pour une recherche de comptes. Deux chemins, dans cet ordre :

| Chemin | `--source` | Condition | Coût | Limite |
|---|---|---|---|---|
| Votre compte LinkedIn | `unipile` | `UNIPILE_API_KEY` et `UNIPILE_ACCOUNT_ID` dans `.env`, abonnement Sales Navigator sur le compte | inclus dans l'abonnement Unipile | chaque résultat est une vue depuis votre compte : 300 profils par jour au plus |
| Vos cookies, par Apify | `salesnav` | `APIFY_TOKEN` et `browser_cookie3` installé (cookies et user agent relus dans votre navigateur avant chaque run), sinon `LINKEDIN_COOKIES_FILE` + `LINKEDIN_USER_AGENT` | `curious_coder/linkedin-sales-navigator-search-scraper`, 0,005 $ par résultat | 500 profils par jour, délais de 5 à 30 s entre pages, `stopOnRateLimit` |

Sans `--source`, le script prend les cookies s'ils sont là, sinon Unipile. Les filtres "a consulté votre profil" et "suit votre page" ne se lisent qu'avec un compte qui est le vôtre : les deux chemins le sont.

## Entrée

Une URL `https://www.linkedin.com/sales/search/people?...` (ou `/sales/search/company?...` pour les comptes), et le nombre de résultats voulus. Si l'URL vient de `construire-requete-salesnav --enregistrer`, elle est déjà dans `05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md` et recevra son volume.

## Sortie

`05_Departements/Go-to-Market/Listes-prospection/trouver-personnes_<sujet>_<date>.csv` : `prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `linkedin_url`, `linkedin_entreprise_url`, `ville`, `headline`, `source`, `date_extraction`, plus `provider_id` et `degre_relation` avec Unipile ; avec `--signal`, `signal_type`, `signal_date` (la date du run), `signal_detail`, `fraicheur`. Pour les comptes : le CSV de `trouver-entreprises`.

## Procédure

1. Lisez l'URL : `python3 10_Skills/construire-requete-salesnav/scripts/construire_requete_salesnav.py --decoder "<url>"` dit quels filtres elle porte (titres, région, effectif, relation, et le filtre à cocher). C'est le signal à poser : `visite_profil` (VIEWED_YOUR_PROFILE), `abonne_entreprise` (FOLLOWS_YOUR_COMPANY), `a_publie` (POSTED_ON_LINKEDIN), `changement_poste` (RECENTLY_CHANGED_JOBS).
2. Dry-run :
   `python3 10_Skills/trouver-personnes/scripts/trouver_personnes.py --url "<url>" --signal visite_profil --max 100 --sujet "visites-ceo" --dry-run`
   (ajoutez `--source unipile` ou `--source salesnav` pour forcer un chemin ; pour des comptes : `trouver_entreprises.py --source salesnav --url "<url>"`).
3. Annoncez le chemin, le volume et le coût, attendez le oui, relancez sans `--dry-run`.
4. Gardez les nouveaux seulement : `python3 10_Skills/dedoublonner/scripts/dedoublonner.py --in <csv> --contre <csv du run précédent>` pour un signal qui se rejoue chaque semaine, puis contre le CRM.
5. Lien cliquable, nombre de lignes, et un seul next step : le sous-skill du signal dans `detecter-signaux` (`visite-profil`, `abonnes-entreprise`, `a-publie`, `changement-poste`) pour la fenêtre et le play, ou `enrichir-personne` puis `trouver-email` pour une liste sans signal.

## Garde-fous

- `--max` sous 300 avec Unipile, sous 500 avec les cookies : au-delà, le compte prend un risque ; le plafond du jour vaut pour tous les skills réunis (`GARDE-FOUS.md`).
- Les cookies ne se collent jamais dans le chat ni dans un skill : `rafraichir_cookies_linkedin.py` (`connecter-outils`, étape 9) les relit dans le navigateur avant chaque run. Le user agent vient du même navigateur : un user agent périmé fait renouveler la session par LinkedIn et le run s'arrête après la première page.
- Une URL avec `sessionId` expire : si le script rend 0 ligne, reconstruisez l'URL avec `construire-requete-salesnav` (sans `sessionId`).
- `signal_date` est la date de l'export, pas celle de la visite ou du changement : la fenêtre se calcule à partir du run précédent (`dedoublonner --contre`).

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| 0 résultat sur une URL qui en montre 200 dans le navigateur | URL périmée (`sessionId`) ou filtre à cocher lu avec un autre compte que le vôtre | reconstruire l'URL, vérifier que le compte Unipile ou les cookies sont ceux du profil qui a le filtre |
| "Cookies are expired" dès la page 1 | jeu de cookies incomplet (seulement `li_at` + `li_a`) ou session fermée | `rafraichir_cookies_linkedin.py --check` : le profil retenu doit avoir "Sales Navigator : oui" ; sinon se reconnecter à LinkedIn dans le navigateur |
| "Cookies are expired" après la page 1, le compte reste connecté | user agent différent du navigateur qui a émis les cookies : LinkedIn renouvelle le `li_at` | laisser le script construire le user agent (ne pas écrire `LINKEDIN_USER_AGENT` à la main), ou le recopier exactement depuis "my user agent" dans Google |
| Unipile : `sales_navigator` refusé | pas d'abonnement Sales Navigator sur le compte | passer par une recherche classique (`--mots-cles`) ou les cookies d'un compte abonné |
| Beaucoup de doublons d'une semaine sur l'autre | même URL rejouée sans `--contre` | `dedoublonner --contre <run précédent>` |
