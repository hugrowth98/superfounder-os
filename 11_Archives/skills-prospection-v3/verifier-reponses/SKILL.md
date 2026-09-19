---
name: verifier-reponses
description: >
  Skill pour lister les conversations LinkedIn ou des prospects ont repondu, via Unipile.
  Sert aussi de garde-fou obligatoire avant tout envoi (jamais de relance a quelqu'un qui a
  deja repondu). Utilise ce skill des que l'utilisateur veut savoir qui a repondu, ou avant
  de lancer une relance. Se declenche sur : "qui a répondu", "vérifie les réponses", "y a-t-il
  des nouvelles réponses", "check les conversations LinkedIn".
---

# Verifier les reponses recues (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`.
**Endpoints** :
- `GET {UNIPILE_DSN}/api/v1/chats?account_id=<id>&limit=<n>` (liste des conversations)
- `GET {UNIPILE_DSN}/api/v1/chats/{chatId}/messages?limit=<n>` (messages d'une conversation)

Pas de webhook ni de notification push dans cette version : ce skill fonctionne par
verification manuelle (polling), a lancer quand l'utilisateur le demande.

## Usage 1 : lister qui a repondu

```bash
python3 .claude/skills/verifier-reponses/scripts/client.py "<account_id>" "<own_provider_id>"
```

`own_provider_id` = l'identifiant Unipile du compte LinkedIn connecte lui-meme (pour
distinguer "j'ai envoye le dernier message" de "le prospect a repondu en dernier"). Le
recuperer une fois via `GET /api/v1/accounts` et le garder pour la session.

Retourne la liste des conversations ou le dernier message ne vient pas de nous, avec le
texte du dernier message recu.

## Usage 2 : garde-fou avant un envoi (obligatoire)

**Avant tout envoi via `envoyer-invitation` ou `envoyer-dm` a une liste existante en
conversation**, ce skill doit etre appele pour exclure les prospects ayant deja repondu.
Cette regle n'est pas negociable : ne jamais relancer quelqu'un qui a repondu, meme pour une
relance "amicale".

## Workflow

### Etape 1 - Lister les reponses

Lancer le script, recuperer la liste des repliers.

### Etape 2 - Croiser avec la liste de prospects a relancer

Si l'utilisateur veut relancer une liste, retirer de cette liste tous les
`attendee_provider_id` presents dans les repliers.

### Etape 3 - Resumer

Nombre de nouvelles reponses, aperçu des 3 premiers messages recus. Si l'utilisateur
demande une relance, confirmer explicitement le nombre de prospects exclus pour avoir deja
repondu avant de lancer quoi que ce soit.
