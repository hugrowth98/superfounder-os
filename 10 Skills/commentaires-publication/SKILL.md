---
name: commentaires-publication
description: >
  Skill pour lister tous les commentaires (et leurs reponses) d'une publication
  LinkedIn via l'API Unipile, votre post ou celui d'un concurrent. Utilise ce skill des
  que l'utilisateur donne une URL de post et veut voir qui a commente. Se declenche
  sur : "liste les commentaires de ce post", "qui a commente ce post", "montre-moi les
  reponses a ce commentaire", "analyse les commentaires de ce post concurrent".
---

# Commentaires d'une publication LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `GET {UNIPILE_DSN}/api/v1/posts/{social_id}/comments?account_id=<id>`

Meme route pour deux usages selon les query params :
- sans `comment_id` : commentaires de premier niveau du post
- avec `comment_id=<id_du_commentaire>` : reponses a ce commentaire precis

**Point critique** : LinkedIn utilise plusieurs formats d'ID pour le meme post
(`urn:li:activity:`, `urn:li:ugcPost:`, `urn:li:share:`). Le `social_id` obtenu via une
recherche ou un listing precedent (skill `recherche-salesnav` ou
`publications-entreprise`) est plus fiable que l'ID extrait au regex depuis l'URL du
post. Si le nombre de commentaires recuperes ne correspond pas au compteur affiche sur
LinkedIn, verifier en premier le social_id utilise.

## Workflow

### Etape 1 - Recuperer l'identifiant du post

Formats acceptes par le script : URL LinkedIn classique
(`.../posts/<handle>_<slug>-activity-<id>-<suffixe>`) ou directement un `social_id`
(`urn:li:...`) si deja connu (recommande, plus fiable).

### Etape 2 - Lancer la recuperation

```bash
python3 .claude/skills/commentaires-publication/scripts/client.py "<account_id>" "<url_ou_social_id>"
```

Le script recupere automatiquement les reponses imbriquees a chaque commentaire qui en a
(`reply_counter > 0`). Pour ne recuperer que les commentaires de premier niveau (plus
rapide) : ajouter `--no-replies`.

### Etape 3 - Coherence du total

Le `total_items` retourne par l'API ne compte que le premier niveau. Le total reel
(commentaires + reponses) doit correspondre au compteur affiche sur LinkedIn - sinon
recreuser du cote du social_id utilise.

## Format de sortie

Plusieurs commentaires attendus : restituer en **tableau markdown**, une ligne par
commentaire, avec le maximum de colonnes disponibles :

| Auteur | Headline | Degre | Commentaire | Likes | Reponses | Date |
|---|---|---|---|---|---|---|
| Daniel Karimi | Ingeniero de Telecomunicaciones... | 3e degre | What makes the Claude Code story compelling... | 10 | 1 | 06/07/2026 |

Si un commentaire a des reponses, les afficher juste apres dans le meme tableau avec une
indentation visuelle ("> reponse a Daniel Karimi : ...") plutot que dans un tableau
separe, pour garder le fil de la conversation lisible.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| Total incoherent avec LinkedIn | mauvais social_id | redemander l'URL via "Copier le lien" du post, ou repartir d'un social_id issu d'une recherche |
| 429 | rate limit Unipile | attendre et reessayer |
