---
name: reactions-publication
description: >
  Skill pour lister toutes les reactions (likes, celebrate, support, love, insightful,
  funny) a une publication LinkedIn via l'API Unipile, avec repartition par type.
  Utilise ce skill des que l'utilisateur donne une URL de post et veut voir qui a
  reagi. Se declenche sur : "liste les reactions de ce post", "qui a like ce post",
  "combien de personnes ont reagi", "identifie les gens qui ont reagi fort a ce post".
---

# Reactions a une publication LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `GET {UNIPILE_DSN}/api/v1/posts/{social_id}/reactions?account_id=<id>`

Valeurs de reaction observees : `LIKE`, `APPRECIATION`, `EMPATHY`, `PRAISE` (et
probablement d'autres types LinkedIn standards non vus en test : `INTEREST`,
`ENTERTAINMENT`). `APPRECIATION`/`PRAISE` signalent un engagement plus fort qu'un simple
`LIKE` - utile pour prioriser un suivi commercial post-engagement.

Meme remarque que pour les commentaires : utiliser de preference un `social_id` obtenu
via une recherche/listing precedent plutot qu'extrait au regex d'une URL, LinkedIn ayant
plusieurs formats d'ID pour le meme post.

Le `cursor` de pagination est dans `paging.cursor` (pas au niveau racine de la reponse).
Limite stricte de `limit` a 100 par page (confirmee par une erreur 400 explicite
au-dela).

## Workflow

### Etape 1 - Recuperer l'identifiant du post

URL LinkedIn classique ou `social_id` direct (recommande).

### Etape 2 - Lancer la recuperation

```bash
python3 .claude/skills/reactions-publication/scripts/client.py "<account_id>" "<url_ou_social_id>"
```

Pagination automatique jusqu'a `--max-pages` (defaut 10, soit jusqu'a 1000 reactions).

### Etape 3 - Reactions a un commentaire precis

Le script gere aussi ce cas (parametre `comment_id` dans `list_reactions`) si
l'utilisateur veut les reactions a un commentaire specifique plutot qu'au post entier -
utile en complement du skill `commentaires-publication`.

## Format de sortie

Plusieurs reactions attendues : restituer en **tableau markdown**, une ligne par
personne, avec le maximum de colonnes disponibles :

| Nom | Type de reaction | Headline | Degre de relation |
|---|---|---|---|
| Fawzi Iliass | LIKE | Cybersecurity, Artificial Intelligence, Software Engineering | 3e degre |

Ajouter systematiquement, avant le tableau, un resume de repartition par type de
reaction (deja calcule par le script, fonction `summarize_by_type`) : "930 reactions au
total : 780 LIKE, 90 APPRECIATION, 60 PRAISE". Si la liste est longue, presenter en
priorite les reactions `APPRECIATION`/`PRAISE` (engagement fort) avant les simples
`LIKE`.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| 400 (limit > 100) | parametre hors bornes | le script plafonne deja a 100, ne pas forcer plus haut |
| 429 | rate limit Unipile | attendre et reessayer |
