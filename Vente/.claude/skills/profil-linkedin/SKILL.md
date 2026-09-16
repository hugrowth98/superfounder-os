---
name: profil-linkedin
description: >
  Skill pour recuperer le profil LinkedIn complet d'une personne (le compte connecte
  lui-meme ou un tiers) via l'API Unipile : experiences, formations, competences,
  localisation, coordonnees si disponibles. Utilise ce skill des que l'utilisateur veut
  voir/analyser un profil LinkedIn precis. Se declenche sur : "regarde le profil LinkedIn
  de", "montre-moi le profil de", "quelles sont ses experiences", "recupere mon propre
  profil LinkedIn".
---

# Profil utilisateur LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `GET {UNIPILE_DSN}/api/v1/users/{identifiant}?account_id=<id>&linkedin_sections=*`

`{identifiant}` accepte :
- `me` : le compte LinkedIn connecte lui-meme (retourne un objet plus limite,
  `AccountOwnerProfile` : identite, headline, localisation, sales navigator - pas
  d'historique complet d'experiences)
- un `public_identifier` (slug de l'URL, ex: `jean-dupont`) : retourne un objet complet
  `UserProfile` (experiences, formations, competences avec nombre d'endorsements,
  langues, certifications, recommandations)
- un `provider_id` interne (si on l'a deja via une recherche precedente)

## Workflow

### Etape 1 - Identifier la personne

Si on n'a que le nom, passer par `trouver-url-linkedin` d'abord pour obtenir le
`public_identifier`. Si l'utilisateur demande son propre profil, utiliser `me`.

### Etape 2 - Lancer la recuperation

```bash
python3 .claude/skills/profil-linkedin/scripts/client.py "<account_id>" "<identifiant|me>"
```

### Etape 3 - Point d'attention : coordonnees de contact

Le champ `contact_info` (email, telephone) n'apparait que si la personne est deja une
relation de 1er degre du compte connecte (`network_distance: FIRST_DEGREE` ou `SELF`).
Pour un profil a distance 2/3 ou hors reseau, ces champs sont simplement absents - ne pas
le presenter comme une erreur, c'est le comportement normal de LinkedIn.

## Format de sortie

Un profil est une seule entite : restituer sous forme de **tableau markdown a deux
colonnes** (Champ / Valeur), avec le maximum d'informations disponibles dans la reponse,
en regroupant par section :

| Champ | Valeur |
|---|---|
| Nom | Fabrice ALLARD |
| Headline | Fondateur Jobberry \| Conseil en Recrutement cadres \| 25 ans d'expertise |
| Localisation | Paris, Ile-de-France, France |
| Degre de relation | 1er degre (connecte le 29/01/2026) |
| Email | fabriceallard@jobberry.com |
| Site web | jobberry.com |
| Abonnes / Relations | 1646 / 1486 |
| Poste actuel | Fondateur chez Jobberry (depuis 09/2007) |
| Poste precedent | Directeur Executif chez Page Personnel (1998-2007) |
| Formation | DESS Marketing, Universite Paris-Est Creteil |

Si plusieurs experiences/formations existent, les lister toutes en lignes distinctes
plutot que de n'en garder qu'une (ex: "Poste actuel", "Poste precedent 1", "Poste
precedent 2"...).

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| 404 | identifiant introuvable | verifier l'orthographe du public_identifier, ou repasser par `trouver-url-linkedin` |
| 429 | rate limit Unipile | attendre et reessayer |
