---
name: envoyer-dm
description: >
  Skill pour envoyer des messages directs LinkedIn a une liste de prospects via Unipile,
  avec verification obligatoire des reponses deja recues avant tout envoi. Utilise ce skill
  des que l'utilisateur veut envoyer des DM/messages LinkedIn a une liste. Se declenche sur :
  "envoie les DM", "envoie les messages LinkedIn", "lance la relance", "envoie le message 1
  a cette liste".
---

# Envoyer des messages directs LinkedIn (Unipile)

## Garde-fou non negociable

**Jamais de message a quelqu'un qui a deja repondu.** Avant tout envoi, appeler
`verifier-reponses` et exclure ces prospects de la liste, meme si l'utilisateur ne le
demande pas explicitement. Une limite quotidienne de 100 DM/jour par defaut est aussi
appliquee via un compteur local (`scripts/compteur.json`).

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`.
**Endpoint** : `POST {UNIPILE_DSN}/api/v1/chats`
**Payload** : `{ account_id, attendees_ids: [provider_id], text }`

## Workflow

### Etape 1 - Verifier les reponses deja recues

Lancer `verifier-reponses` pour obtenir la liste des `provider_id` ayant deja repondu.

### Etape 2 - Verifier le quota restant

```bash
python3 .claude/skills/envoyer-dm/scripts/client.py remaining
```

### Etape 3 - Envoyer

```bash
python3 -c "
import csv, sys
sys.path.insert(0, '.claude/skills/envoyer-dm/scripts')
sys.path.insert(0, '.claude/skills/verifier-reponses/scripts')
from client import send_batch
import client as verif
already_replied = {r['attendee_provider_id'] for r in verif.list_repliers('<account_id>', '<own_provider_id>')}
contacts = [{'provider_id': r['provider_id'], 'message': r['message']} for r in csv.DictReader(open('Messages/liste_messages.csv'))]
print(send_batch('<account_id>', contacts, already_replied_ids=already_replied))
"
```

### Etape 4 - Respecter la sequence par defaut

Sequence recommandee (configurable si l'utilisateur en demande une autre) : invitation
acceptee -> attendre 2 jours -> message 1 -> attendre 3 jours -> message 2 (relance). Ne
jamais enchainer un message 2 sans re-verifier les reponses entre-temps.

### Etape 5 - Resumer

Nombre envoye, nombre exclu pour reponse deja recue, nombre non envoye par manque de quota,
erreurs. Toujours afficher separement le motif d'exclusion "a deja repondu" des autres
motifs.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `.env` racine |
| 422 | `attendees_ids` invalide | verifier que c'est bien un `provider_id` Unipile, pas une URL |
| 429 | rate limit | arreter le batch, reessayer plus tard |
