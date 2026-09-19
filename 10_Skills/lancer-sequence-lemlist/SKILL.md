---
name: lancer-sequence-lemlist
description: >
  Skill pour demarrer, mettre en pause ou reprendre une campagne Lemlist, via le serveur MCP
  officiel Lemlist. Utilise ce skill des que l'utilisateur veut lancer, arreter ou reprendre
  une campagne email. Se declenche sur : "lance la campagne", "démarre la séquence", "mets en
  pause la campagne", "reprends la campagne Lemlist".
---

# Demarrer / pauser une campagne Lemlist (via MCP)

## Garde-fou non negociable

**Ne jamais demarrer une campagne sans confirmation explicite de l'utilisateur.** C'est
l'action qui declenche des envois reels a de vrais prospects : toujours recapituler (nombre
de leads, contenu du premier message, expediteur) et attendre un "oui, lance" avant d'appeler
l'outil de demarrage.

## Ce que fait ce skill

Utilise l'outil MCP Lemlist de changement d'etat de campagne (`draft -> running`,
`running -> paused`, `paused -> running`, `running/paused -> archived`).

## Workflow

### Etape 1 - Verifier que la campagne est prete

Avant de proposer le lancement : sequence complete, expediteur configure, leads importes
(via `envoyer-vers-lemlist`). Utiliser l'outil de verification de disponibilite de la
campagne si le serveur MCP en expose un.

### Etape 2 - Recapituler avant de lancer

Presenter a l'utilisateur : nom de la campagne, nombre de leads, apercu du premier message,
expediteur. Demander une confirmation explicite.

### Etape 3 - Changer l'etat

Sur confirmation, appeler l'outil MCP de changement d'etat avec la transition demandee
(demarrer, pauser, reprendre, archiver).

### Etape 4 - Resumer

Nouvel etat de la campagne, date/heure du changement. Si demarrage : rappeler a
l'utilisateur d'utiliser `verifier-reponses` (cote LinkedIn) et de surveiller les retours
Lemlist regulierement (taux d'ouverture, de reponse) pour ajuster si besoin.
