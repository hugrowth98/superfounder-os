---
name: envoyer-invitation
description: >
  Skill pour envoyer des invitations LinkedIn a une liste de prospects via Unipile, avec
  garde-fou strict de 30 invitations par jour maximum. Utilise ce skill des que l'utilisateur
  veut envoyer des invitations LinkedIn a une liste. Se declenche sur : "envoie les
  invitations", "connecte-toi a ces prospects", "lance les demandes de connexion", "envoie
  les demandes LinkedIn".
---

# Envoyer des invitations LinkedIn (Unipile)

## Garde-fou non negociable

**30 invitations par jour maximum.** Au-dela, LinkedIn restreint ou bannit le compte. Ce
garde-fou est applique cote script via un compteur local (`scripts/compteur.json`, remis a
zero chaque jour), pas par l'API elle-meme : ne jamais le contourner meme si l'utilisateur
insiste, expliquer le risque (restriction du compte LinkedIn).

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`.
**Endpoint** : `POST {UNIPILE_DSN}/api/v1/users/invite`
**Payload** : `{ account_id, provider_id, message? }`. `provider_id` = identifiant Unipile du
profil cible (colonne `provider_id` produite par `export-salesnav`/`scraper-post`/
`trouver-personnes`), **pas** l'URL LinkedIn brute.

## Workflow

### Etape 1 - Verifier le quota restant

```bash
python3 .claude/skills/envoyer-invitation/scripts/client.py remaining
```

Si le quota du jour est deja consomme, le dire a l'utilisateur et proposer de reprendre le
lendemain.

### Etape 2 - Verifier qu'aucun prospect n'a deja repondu

Si la liste contient des prospects deja contactes precedemment, lancer `verifier-reponses`
et exclure ceux qui ont deja repondu avant d'envoyer quoi que ce soit.

### Etape 3 - Envoyer

Le script `client.py` expose `send_batch(account_id, contacts, delay_s=3.0)` ou `contacts`
est une liste de dicts `{provider_id, message}` (le message vient de `personnaliser-message`
si disponible). L'appeler depuis un petit script Python inline ou noter qu'il s'arrete
automatiquement a la limite quotidienne, meme en plein milieu du batch.

Exemple d'appel inline :
```bash
python3 -c "
import csv, sys
sys.path.insert(0, '.claude/skills/envoyer-invitation/scripts')
from client import send_batch
contacts = [{'provider_id': r['provider_id'], 'message': r.get('message')} for r in csv.DictReader(open('Listes-prospection/liste.csv'))]
print(send_batch('<account_id>', contacts))
"
```

### Etape 4 - Resumer

Nombre envoye, nombre non envoye par manque de quota (avec un decompte a reprendre demain),
erreurs eventuelles. Toujours mentionner le solde restant pour la journee.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `.env` racine |
| 422 | `provider_id` invalide | verifier que la colonne vient bien d'un export Unipile, pas d'une URL brute |
| 429 | rate limit Unipile ou LinkedIn | arreter le batch, reessayer plus tard |
