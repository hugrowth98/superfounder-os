---
name: trouver-url-linkedin
description: >
  Skill pour retrouver l'URL LinkedIn d'une personne a partir de son nom (et
  optionnellement son entreprise), via l'API Unipile. Utilise ce skill des que
  l'utilisateur cherche le profil LinkedIn de quelqu'un dont il n'a que le nom. Se
  declenche sur : "trouve l'URL LinkedIn de", "cherche le profil de", "c'est qui sur
  LinkedIn", "retrouve-moi ce contact sur LinkedIn".
---

# Trouver l'URL LinkedIn d'une personne (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `POST {UNIPILE_DSN}/api/v1/linkedin/search?account_id=<id>` avec
`category: "people"`.

## Workflow

### Etape 1 - Recuperer le nom (et l'entreprise si connue)

Demander a l'utilisateur le nom complet, et l'entreprise si elle est connue (ca affine
beaucoup la recherche quand le nom est courant).

### Etape 2 - Lancer la recherche

```bash
python3 .claude/skills/trouver-url-linkedin/scripts/client.py "<account_id>" "<nom complet>" \
  --entreprise "<entreprise>" --max 5
```

Sans entreprise connue :
```bash
python3 .claude/skills/trouver-url-linkedin/scripts/client.py "<account_id>" "<nom complet>"
```

### Etape 3 - Si 0 resultat avec nom + entreprise

Le script retente automatiquement avec le nom seul (une entreprise mal orthographiee ou
abregee peut faire echouer la recherche exacte - deja observe en test). Les resultats
issus de ce fallback sont marques `fallback_recherche_nom_seul: true`.

### Etape 4 - Restituer

## Format de sortie

Toujours restituer les resultats sous forme de **tableau markdown**, avec le maximum de
colonnes disponibles dans la reponse (pas seulement l'URL) :

| Nom | Headline | Localisation | Degre de relation | URL LinkedIn |
|---|---|---|---|---|
| Fabrice ALLARD | Fondateur Jobberry \| Conseil en Recrutement cadres | Paris | 1er degre | linkedin.com/in/fabrice-allard-recruteur |

Trier par degre de relation (1er degre et soi-meme en premier, puis 2e, 3e, hors reseau) -
le script renvoie deja les resultats dans cet ordre. Si plusieurs personnes portent le
meme nom sans element pour trancher, presenter tout le tableau et demander a
l'utilisateur laquelle il vise plutot que de deviner.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| 0 resultat (meme apres fallback) | orthographe ou personne non indexee | redemander le nom, proposer une recherche par entreprise seule a la place |
| 429 | rate limit Unipile | attendre et reessayer |
