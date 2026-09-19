---
name: creer-campagne-lemlist
description: >
  Skill pour creer une nouvelle campagne email (ou multicanal) dans Lemlist via son serveur
  MCP officiel, a partir des messages personnalises et du positionnement defini dans
  contexte.md. Utilise ce skill des que l'utilisateur veut creer une campagne Lemlist. Se
  declenche sur : "crée une campagne Lemlist", "monte une séquence email", "prépare la
  campagne pour cette liste".
---

# Creer une campagne Lemlist (via MCP)

## Pre-requis : connecter le serveur MCP Lemlist

Ce skill n'utilise **aucun script custom** : Lemlist expose un serveur MCP officiel, il
suffit de le connecter une fois a Claude Code :

```bash
claude mcp add --transport http lemlist https://app.lemlist.com/mcp
```

Authentification par OAuth (pas de cle API a copier) : au premier appel d'un outil Lemlist,
une page de consentement s'ouvre dans le navigateur pour choisir l'equipe et autoriser
l'acces. A faire une seule fois.

## Ce que fait ce skill

Une fois le serveur connecte, les outils Lemlist sont disponibles directement (prefixe
`lemlist` dans la liste des outils MCP). Ce skill guide leur utilisation pour :
1. Creer la campagne avec sa sequence initiale (objet `create_campaign_with_sequence` ou
   equivalent expose par le MCP)
2. Ajouter des etapes de sequence supplementaires si besoin (relance)
3. Verifier que la campagne est prete avant tout demarrage (verification de lecture, pas
   d'envoi a ce stade)

## Workflow

### Etape 1 - Rassembler le contenu

A partir de `personnaliser-message` (messages deja rediges par prospect) ou, a defaut, du
positionnement dans `05_Departements/Go-to-Market/contexte.md` (sections 1, 3, 4, 6) pour ecrire un email generique de
premier contact.

### Etape 2 - Creer la campagne

Utiliser l'outil MCP Lemlist de creation de campagne avec sequence (nom de campagne clair,
ex: `module de prospection - [cible] - [date]`), en fournissant le contenu du premier email (objet + corps).
Garder la campagne en `draft`, ne pas la demarrer a cette etape.

### Etape 3 - Ajouter les relances si besoin

Si l'utilisateur veut une sequence a plusieurs etapes, ajouter les etapes suivantes (delai
recommande : 3 a 4 jours entre chaque relance).

### Etape 4 - Verifier avant de rendre la main

Verifier que la campagne a bien un expediteur configure et un contenu complet (pas de
variable `{{...}}` non definie). Signaler tout probleme a l'utilisateur.

### Etape 5 - Resumer

Nom et id de la campagne creee, nombre d'etapes de sequence, statut (draft). Proposer
l'etape suivante : "Je peux y importer les leads avec `envoyer-vers-lemlist`."

## Garde-fou

**Ne jamais demarrer une campagne (passage en `running`) a cette etape.** La creation reste
en brouillon jusqu'a validation explicite via `lancer-sequence-lemlist`.
