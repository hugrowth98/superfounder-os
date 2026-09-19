---
name: envoyer-vers-lemlist
description: >
  Skill pour importer une liste de prospects qualifies (CSV) dans une campagne Lemlist
  existante, via le serveur MCP officiel Lemlist. Utilise ce skill des que l'utilisateur veut
  pousser une liste de leads dans une campagne Lemlist. Se declenche sur : "importe ces leads
  dans Lemlist", "ajoute cette liste à la campagne", "pousse ces prospects vers Lemlist".
---

# Importer des leads dans une campagne Lemlist (via MCP)

## Pre-requis

Serveur MCP Lemlist connecte (voir `creer-campagne-lemlist` pour la commande de connexion)
et une campagne deja creee (via `creer-campagne-lemlist` ou existante).

## Ce que fait ce skill

Utilise l'outil MCP Lemlist d'import de leads pour ajouter les prospects du CSV (issu de
`qualifier-liste` + `trouver-email` + `personnaliser-message`) a la campagne cible.

## Workflow

### Etape 1 - Verifier les donnees du CSV

Colonnes minimum requises par Lemlist : email, prenom, nom. Fortement recommande :
entreprise, poste, message/icebreaker personnalise (colonne `message` produite par
`personnaliser-message`) pour l'injecter comme variable dans le template email.

Si des lignes n'ont pas d'email valide (issu de `trouver-email`), les exclure et le signaler.

### Etape 2 - Identifier la campagne cible

Demander le nom ou l'id de la campagne si non precise. Lister les campagnes existantes via
l'outil MCP correspondant si besoin de retrouver l'id.

### Etape 3 - Importer

Appeler l'outil MCP Lemlist d'import de leads avec le CSV, en mappant les colonnes vers les
champs Lemlist attendus (email, firstName, lastName, companyName, icebreaker/custom
variable pour le message personnalise).

### Etape 4 - Resumer

Nombre de leads importes, nombre exclus (sans email valide), nombre de doublons ignores si
signale par Lemlist. Proposer l'etape suivante : "Pret a demarrer avec
`lancer-sequence-lemlist`."

## Garde-fou

Un import ne declenche jamais d'envoi automatique : les leads arrivent en attente dans la
campagne, l'envoi ne demarre qu'avec `lancer-sequence-lemlist` (action explicite).
