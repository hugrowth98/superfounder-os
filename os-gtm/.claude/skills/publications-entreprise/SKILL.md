---
name: publications-entreprise
description: >
  Skill pour lister toutes les publications LinkedIn recentes d'une entreprise (les
  votres ou celles d'un concurrent) via l'API Unipile : texte, date, reactions,
  commentaires, reposts. Utilise ce skill des que l'utilisateur veut voir ce qu'une
  entreprise publie sur LinkedIn. Se declenche sur : "qu'est-ce que cette boite publie
  sur LinkedIn", "liste les posts de cette entreprise", "veille concurrentielle sur
  LinkedIn", "montre-moi les publications de [entreprise]".
---

# Publications d'une entreprise LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `GET {UNIPILE_DSN}/api/v1/users/{provider_id}/posts?account_id=<id>&is_company=true`

Point important : cet endpoint est le meme que pour lister les posts d'un profil
personnel - seul le flag `is_company=true` change le comportement. Il n'existe pas
d'endpoint pour lister les employes/utilisateurs d'une entreprise (LinkedIn ne l'expose
pas publiquement, Unipile ne le contourne pas) : si l'utilisateur demande ca, le
prevenir plutot que de chercher un endpoint qui n'existe pas.

`{provider_id}` doit etre l'id numerique interne LinkedIn (pas le public_identifier
textuel) : le script le resout automatiquement via une recherche entreprise si on lui
donne un nom.

## Workflow

### Etape 1 - Identifier l'entreprise

Nom ou identifiant de l'entreprise a surveiller.

### Etape 2 - Lancer la recuperation

```bash
python3 .claude/skills/publications-entreprise/scripts/client.py "<account_id>" "<nom_ou_id_entreprise>" --max 50
```

### Etape 3 - Pagination

Le script pagine automatiquement via `cursor` jusqu'a `--max` (defaut 50). Pour une
entreprise tres active, prevoir que les posts les plus recents remontent en premier.

## Format de sortie

Plusieurs publications attendues : restituer en **tableau markdown**, une ligne par
post, avec le maximum de colonnes disponibles :

| Date | Texte (extrait) | Reactions | Commentaires | Reposts | Lien |
|---|---|---|---|---|---|
| 06/07/2026 | The Government of Alberta worked with Claude to find and fix... | 1628 | 86 | 68 | linkedin.com/posts/anthropicresearch_... |

Tronquer le texte a ~120 caracteres dans le tableau (le texte complet reste disponible
dans le JSON brut si l'utilisateur en a besoin pour un post precis). Trier par date
decroissante (deja l'ordre naturel retourne par l'API).

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| Entreprise introuvable | recherche sans resultat | redemander le nom exact ou l'URL LinkedIn |
| 0 publication | page peu active ou recente | le signaler tel quel, ce n'est pas une erreur |
| 429 | rate limit Unipile | attendre et reessayer |
