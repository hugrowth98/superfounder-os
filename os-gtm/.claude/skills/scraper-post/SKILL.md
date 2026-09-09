---
name: scraper-post
description: >
  Skill pour recuperer les gens qui ont like et/ou commente un post LinkedIn (le vôtre ou
  celui d'un concurrent/sujet strategique) via Unipile, dedupe, et exporter en CSV. Couvre
  aussi bien votre propre audience que la detection d'un signal d'interet sur un post tiers
  (scraper-commentaires). Utilise ce skill des que l'utilisateur donne une URL de post
  LinkedIn et veut en recuperer l'audience. Se declenche sur : "scrape les engagers de ce
  post", "qui a like ce post LinkedIn", "qui a commente ce post", "regarde qui a commente ce
  post concurrent", "recupere l'audience de cette URL".
---

# Scraper les likers et commentateurs d'un post LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis le
`.env` racine.
**Endpoints** : `GET {UNIPILE_DSN}/api/v1/posts/{postId}/reactions` (likes) et
`GET {UNIPILE_DSN}/api/v1/posts/{postId}/comments` (commentaires).

Deux usages du meme skill :
- **Audience de votre propre post** : recuperer tout le monde qui a engage (mode `both`).
- **Detection de signal d'interet** (scraper-commentaires) : recuperer uniquement les
  commentateurs d'un post concurrent ou d'un sujet strategique pour votre marche (mode
  `comments`). Les gens qui commentent sur votre sujet sont plus receptifs qu'une liste
  froide, utile pour prioriser l'outreach.

## Workflow

### Etape 1 - Recuperer l'URL du post

Formats acceptes : `https://www.linkedin.com/posts/<handle>_<slug>-activity-<id>-<suffixe>`
ou `https://www.linkedin.com/feed/update/urn:li:activity:<id>/`. Si l'URL ne correspond a
aucun des deux formats, demander a l'utilisateur de recopier le lien via le menu "Copier le
lien" du post.

### Etape 2 - Lancer le scraping

Audience complete (like + commentaires) :
```bash
python3 .claude/skills/scraper-post/scripts/client.py "<account_id>" \
  "https://www.linkedin.com/posts/..." "output/engagers.csv"
```

Uniquement les commentateurs (usage signal d'interet / scraper-commentaires) :
```bash
python3 .claude/skills/scraper-post/scripts/client.py "<account_id>" \
  "https://www.linkedin.com/posts/..." "output/commentateurs.csv" --type comments
```

### Etape 3 - Resumer

Total d'engagers, repartition reactions/commentaires/les deux, chemin du CSV. Proposer
l'etape suivante : "Je peux qualifier cette liste avec `qualifier-liste`, ou lancer
l'outreach directement avec `envoyer-invitation`."

## Colonnes du CSV de sortie

`name, headline, linkedin_url, provider_id, engagement_type (reaction/comment/reaction+comment),
comment_text, comment_id`

## Notes

- Pour une analyse fine d'un post (reponses imbriquees aux commentaires, repartition
  par type de reaction), utiliser plutot les skills dedies `commentaires-publication` et
  `reactions-publication` : ce skill-ci est optimise pour l'export CSV d'audience
  (dedup + qualification), pas pour l'analyse detaillee affichee dans la conversation.
- Dedupe automatique par URL LinkedIn : quelqu'un qui a like ET commente n'apparait qu'une
  fois, avec `engagement_type = reaction+comment`.
- Pagination bornee a 10 pages (jusqu'a 1000 items par type d'engagement). Si le post a plus
  d'engagement que ca, le dire a l'utilisateur : partiel mais utilisable.
