---
name: recherche-salesnav
description: >
  Skill pour lancer une recherche LinkedIn Sales Navigator (ou classique) via l'API Unipile,
  a partir d'une URL Sales Nav copiee-collee ou de mots-cles. Utilise ce skill des que
  l'utilisateur fournit une URL Sales Navigator ou veut lancer une recherche LinkedIn
  avancee. Se declenche sur : "lance cette recherche Sales Nav", "voici une URL Sales
  Navigator", "cherche sur LinkedIn ces criteres".
---

# Recherche Sales Navigator / LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN` (format
`https://api<N>.unipile.com:<port>`). Les deux charges depuis le `.env` racine.
**Endpoint** : `POST {UNIPILE_DSN}/api/v1/linkedin/search?account_id=<id>`

Le meme endpoint sert pour Sales Navigator (`api: sales_navigator`), une recherche LinkedIn
classique (`api: classic`) ou Recruiter (`api: recruiter`) - seul ce parametre change.

## Trouver son account_id

```bash
curl -sS -H "X-API-KEY: $UNIPILE_API_KEY" "$UNIPILE_DSN/api/v1/accounts"
```
Chercher le compte de type `LINKEDIN` et noter son `id`. Le demander une fois a
l'utilisateur puis le garder pour la session.

## Workflow

### Etape 1 - Recuperer l'URL Sales Nav ou les mots-cles

Si l'utilisateur a une recherche deja construite dans Sales Navigator, demander l'URL
complete (menu "Copier le lien" du navigateur). Sinon, construire une recherche par
mots-cles simples.

### Etape 2 - Lancer la recherche

```bash
python3 .claude/skills/recherche-salesnav/scripts/client.py "<account_id>" \
  "https://www.linkedin.com/sales/search/people?..." \
  --category people --max 100
```

Ou avec des mots-cles au lieu d'une URL :
```bash
python3 .claude/skills/recherche-salesnav/scripts/client.py "<account_id>" \
  "directeur marketing SaaS France" --api classic --category people --max 50
```

### Etape 3 - Pagination et limites reelles (verifie en test live)

Le parametre de limite par page fonctionne correctement (pas plafonne a ~10 comme
suppose au depart) : **50 max en `classic`, 100 max en `sales_navigator`/`recruiter`**,
10 par defaut si omis. Au-dela, l'API renvoie une erreur 400 explicite. Le script gere
la pagination automatiquement via `cursor` avec une borne de securite (`max_results +
50` iterations). Le `cursor` encode aussi les parametres de recherche (api/category/
keywords) : impossible de le reutiliser pour une recherche differente, il faut repartir
de zero (`cursor=null`).

### Etape 4 - Passer a l'export

Ce skill retourne les resultats bruts (JSON). Pour un CSV exploitable, enchainer avec
`export-salesnav` qui normalise et ecrit le fichier.

## Format de sortie

Quand le resultat n'est pas exporte en CSV et doit etre presente directement dans la
conversation, restituer en **tableau markdown**, une ligne par profil/entreprise, avec
le maximum de colonnes disponibles selon le type de recherche :

Pour `category: people` :
| Nom | Headline | Localisation | Degre | Entreprise actuelle | URL LinkedIn |
|---|---|---|---|---|---|

Pour `category: companies` :
| Nom | Secteur | Localisation | Abonnes | Description (extrait) | URL LinkedIn |
|---|---|---|---|---|---|

En `sales_navigator`, des champs supplementaires sont disponibles (`summary` complet,
`current_positions[]` avec anciennete) : les inclure si pertinents pour la demande de
l'utilisateur plutot que de s'en tenir aux colonnes minimales ci-dessus.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| 400 (limit trop eleve) | `limit` > 50 en classic ou > 100 en sales_navigator/recruiter | plafonner selon l'api utilisee, ne jamais forcer plus haut |
| 422 | URL Sales Nav mal formee | redemander l'URL complete a l'utilisateur |
| 429 | rate limit Unipile | attendre et reessayer |
