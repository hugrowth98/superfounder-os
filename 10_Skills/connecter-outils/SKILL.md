---
name: connecter-outils
description: >
  Branche un par un les 7 outils de la stack (Apify, Unipile, Crustdata, FullEnrich, Ocean.io,
  Lemlist, HubSpot) depuis le chat : demande la clé, la teste avec un appel gratuit, l'écrit dans
  le .env, coche "Etat des connexions" dans OUTILS.md et fixe priorite, canal_linkedin,
  canal_email et crm. Gère aussi les cookies LinkedIn pour les actors Sales Navigator d'Apify.
  Se déclenche sur : "connecte mes outils", "branche Unipile", "configure mes clés API",
  "installe ma prospection" (phase outils), "ma clé Apify a changé", "reconnecte LinkedIn",
  "ajoute mes cookies Sales Navigator". Ne pas utiliser pour : remplir contexte.md (voir
  `installer-gtm`) ni pour lancer une recherche (voir les skills de verbe).
---

## Outil

Aucun outil n'est requis avant ce skill : c'est lui qui écrit `05_Departements/Go-to-Market/OUTILS.md`. Son script
`scripts/verifier_connexions.py` s'appuie sur la bibliothèque commune de `10_Skills/_commun/`
(`gtm_common.py` : racine, .env, CSV, clients Unipile, FullEnrich, Crustdata, HubSpot ;
`apify_run.py` : lancer un actor, attendre, lire le dataset, prix vérifiés).

## Entrée

L'utilisateur, en conversation. Pour chaque outil, vous lui donnez le lien exact de la page où
copier la clé, il la colle dans le chat, vous l'écrivez dans `.env` avec
`python3 scripts/verifier_connexions.py --set CLE=VALEUR` (jamais affichée, jamais dans un skill).
S'il n'a pas l'outil : dites-le, laissez la ligne vide, passez au suivant.

## Sortie

- `.env` à la racine (créé depuis `.env.example` au premier `--set`)
- `05_Departements/Go-to-Market/OUTILS.md` : table "Etat des connexions" cochée, avec la date et le compte ou quota, et le bloc
  `priorite:` (apify si `APIFY_TOKEN` répond, sinon api), `canal_linkedin:` (unipile ou lemlist,
  choisi par l'utilisateur), `canal_email: lemlist`, `crm:` (hubspot si le token répond, sinon aucun)
- un résumé de 7 lignes à l'utilisateur : connecté, absent, à refaire

## Procédure

Une question à la fois, dans cet ordre. Après chaque clé, testez avec un appel gratuit :
`python3 scripts/verifier_connexions.py --outil <nom>`.

1. **Apify** (`APIFY_TOKEN`) : token personnel sur https://console.apify.com/settings/integrations.
   Test : `GET /v2/users/me`. Si présent, `priorite: apify`.
2. **Unipile** (`UNIPILE_API_KEY`, `UNIPILE_DSN`) : compte sur https://dashboard.unipile.com, le DSN
   est affiché sur la page d'accueil du dashboard (format `https://apiXX.unipile.com:XXXXX`), le
   token sur https://dashboard.unipile.com/access-tokens. Puis connecter le compte LinkedIn :
   dashboard, Accounts, Connect an account, LinkedIn, méthode Credential, code reçu par email.
   Le test lit `/api/v1/accounts`, vérifie un compte `LINKEDIN` en statut `OK` et écrit lui-même
   `UNIPILE_ACCOUNT_ID` et `UNIPILE_OWN_PROVIDER_ID` dans `.env`.
3. **Crustdata** (`CRUSTDATA_API_KEY`) : https://app.crustdata.com/api-keys. Test : `/user/credits`,
   annoncez le solde.
4. **FullEnrich** (`FULLENRICH_API_KEY`) : https://app.fullenrich.com/app/settings/api. Test :
   `/account/credits`, annoncez le solde (1 crédit par email, 10 par mobile).
5. **Ocean.io** (`OCEAN_API_KEY`) : app.ocean.io, Settings, page "API tokens" (réservée aux admins),
   bouton New token. Test : `/v2/credits/balance` (gratuit). Puis branchez le MCP :
   `claude mcp add --transport http ocean_data_api "https://api.ocean.io/mcp/?api-token=<cle>"`.
6. **Lemlist** : deux voies. MCP OAuth (recommandée, aucune clé à copier) :
   `claude mcp add --transport http lemlist https://app.lemlist.com/mcp`, la fenêtre de consentement
   s'ouvre au premier appel. Ou clé API (`LEMLIST_API_KEY`) sur https://app.lemlist.com/settings/integrations,
   testée sur `/api/team`.
7. **HubSpot** (`HUBSPOT_ACCESS_TOKEN`) : Paramètres, Intégrations, Applications privées, créer une
   app avec les scopes `crm.objects.contacts` et `crm.objects.companies` en lecture et écriture.
   Test : lecture d'un contact. Si présent, `crm: hubspot`.
8. **Cookies Sales Navigator pour Apify** (facultatif, seulement si l'utilisateur veut l'actor
   `curious_coder/linkedin-sales-navigator-search-scraper`) : sur linkedin.com connecté, ouvrir
   l'extension Cookie-Editor, copier la valeur du cookie `li_at` et celle de `li_a` (Sales Navigator),
   puis le user agent du navigateur (taper "my user agent" dans Google). Écrire `LINKEDIN_LI_AT`,
   `LINKEDIN_LI_A`, `LINKEDIN_USER_AGENT` dans `.env`. Variante : exporter tous les cookies en JSON
   dans un fichier hors du module GTM et écrire son chemin dans `LINKEDIN_COOKIES_FILE`. Ces cookies
   expirent en quelques semaines : à l'erreur "Cookies are expired", refaire l'étape.
9. Demandez le canal LinkedIn voulu (Unipile avec le compte de l'utilisateur, ou Lemlist multicanal),
   puis écrivez tout : `python3 scripts/verifier_connexions.py --ecrire-outils --canal-linkedin unipile`.
10. Résumez l'état des 7 outils et proposez un seul next step : `installer-gtm` si `05_Departements/Go-to-Market/contexte.md` a
    encore des crochets, sinon "on construit votre première liste".

## Garde-fous

- Ne jamais afficher, répéter ni logger une clé. `--set` écrit sans écho ; les scripts lisent `.env`.
- Un test échoue : corriger tout de suite avec l'utilisateur (clé recopiée sans espace, DSN avec
  `https://`), ne pas passer à l'outil suivant tant que ce n'est pas réglé, sauf s'il veut sauter.
- Aucun run Apify pendant la connexion : le test du token est gratuit, les cookies Sales Navigator
  ne sont pas testés (un test serait un run payant), ils sont seulement vérifiés présents.
- `05_Departements/Go-to-Market/OUTILS.md` et `.env` ne sont modifiés que par ce skill et `installer-gtm`.
- Compte LinkedIn récent ou déjà restreint : proposez d'écrire `LIMITE_INVITATIONS_JOUR=15` dans
  `.env`, `envoyer-sequence` la lit (plafond dur 30).

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Unipile : compte en statut `CREDENTIALS` | LinkedIn a demandé une revalidation | refaire la connexion du compte dans le dashboard, relancer le test |
| Unipile : 401 | DSN sans `https://` ou token d'un autre workspace | corriger `UNIPILE_DSN`, régénérer le token |
| Apify : HTTP 401 | token incomplet | recopier depuis la page Integrations |
| FullEnrich ou Crustdata : 402 | solde à zéro | recharger, l'outil reste coché mais le solde est noté dans OUTILS.md |
| Lemlist MCP "Needs authentication" | OAuth pas terminé | lancer un outil Lemlist de lecture (`get_team_info`), valider dans le navigateur |
| HubSpot : 403 | scopes manquants sur l'app privée | ajouter les scopes contacts et companies, régénérer le token |
| `OUTILS.md introuvable` | script lancé hors du module GTM | lancer depuis `10_Skills/connecter-outils/scripts/` du module GTM |
