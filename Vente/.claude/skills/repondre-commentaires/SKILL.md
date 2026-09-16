---
name: repondre-commentaires
description: >
  Skill pour repondre aux commentaires laisses sur un de vos posts LinkedIn, dans votre
  voix, via Unipile. Utilise ce skill des que l'utilisateur veut repondre aux commentaires
  d'un post. Se declenche sur : "réponds aux commentaires de ce post", "réponds aux gens qui
  ont commenté", "génère des réponses pour ce post".
---

# Repondre aux commentaires d'un post LinkedIn (Unipile)

## Vue d'ensemble

**Endpoint d'envoi** : `POST {UNIPILE_DSN}/api/v1/posts/{postId}/comments`
**Payload** : `{ account_id, text, comment_id }`

Chaine : recuperer les commentaires non repondus (reutilise `scraper-post` pour le fetch) ->
generer une reponse par commentaire (Claude, voix de `contexte.md`) -> envoyer avec une
pause de 2 secondes entre chaque (pas une vraie limite API, un throttle a respecter quand
meme pour rester naturel).

## Workflow

### Etape 1 - Recuperer les commentaires non repondus

```bash
python3 .claude/skills/repondre-commentaires/scripts/client.py "<account_id>" \
  "https://www.linkedin.com/posts/..." --own-author-id "<votre_provider_id>"
```

Exclut automatiquement vos propres commentaires. Les commentaires deja marques comme
repondus par Unipile (`has_replied`) sont aussi exclus.

### Etape 2 - Generer une reponse par commentaire

Lire `contexte.md` (section 5, voix) et rediger une reponse courte, naturelle, specifique au
commentaire (pas un template generique repete). Toujours montrer les reponses generees a
l'utilisateur pour validation avant envoi.

### Etape 3 - Envoyer apres validation

```python
import sys
sys.path.insert(0, '.claude/skills/repondre-commentaires/scripts')
from client import send_replies
replies = [{"comment_id": "...", "text": "..."}, ...]  # valides a l'etape 2
send_replies("<account_id>", "<url_du_post>", replies)
```

**Ne jamais envoyer sans validation explicite de l'utilisateur sur le contenu genere.**

### Etape 4 - Resumer

Nombre de reponses envoyees, nombre d'erreurs eventuelles.
