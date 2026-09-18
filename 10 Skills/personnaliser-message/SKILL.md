---
name: personnaliser-message
description: >
  Skill pour rediger un message de prospection personnalise par prospect (LinkedIn ou email),
  dans la voix definie dans contexte.md. Ne fait aucun appel API : c'est de la redaction pure
  a partir des donnees deja presentes sur chaque prospect. Utilise ce skill des que
  l'utilisateur veut rediger, personnaliser ou ecrire des messages pour une liste de prospects.
  Se declenche sur : "ecris un message pour chacun", "personnalise ces messages", "redige
  l'accroche pour cette liste", "prepare mes messages LinkedIn/email".
---

# Personnaliser un message par prospect

## Ce que fait ce skill

1. Lit `05 Departements/Go-to-Market/contexte.md` (sections 1 "Offre", 3 "Probleme resolu", 4 "Differenciation", 5 "Voix",
   6 "Preuves sociales") pour connaitre le fond et le ton a adopter.
2. Lit le CSV de prospects (issu de `qualifier-liste` ou `trouver-personnes` de preference,
   avec au minimum prenom, entreprise, poste, et idealement headline/activite recente).
3. Ecrit un message par prospect, adapte a ses donnees propres (pas de copier-coller
   generique avec juste le prenom change).
4. Ajoute une colonne `message` (et `sujet` si canal email) au CSV.

## Principes de redaction (non negociables)

- **Court.** Un message LinkedIn tient en 3-4 phrases max. Un email de prospection en 5-6
  lignes max.
- **Voix du client, pas la voix par defaut de Claude.** Respecter scrupuleusement le ton, le
  tutoiement/vouvoiement et les mots a eviter definis en section 5 de `05 Departements/Go-to-Market/contexte.md`.
- **Accroche specifique au prospect**, jamais un hook generique. S'appuyer sur ce qui est
  disponible dans les donnees : poste, entreprise, secteur, signal (recrutement, levee,
  activite LinkedIn recente) si present dans le CSV.
- **Un seul call-to-action**, simple et a faible friction (pas "achete", plutot "ca vous
  parle ?", "je vous montre en 2 minutes ?").
- **Jamais de superlatifs ni de jargon corporate** ("solution innovante", "révolutionnaire",
  "leader du marche") sauf si explicitement demande dans contexte.md.
- Ne jamais inventer un fait sur le prospect ou son entreprise qui n'est pas dans les
  donnees fournies.

## Workflow

### Etape 1 - Charger le contexte

Relire `05 Departements/Go-to-Market/contexte.md`. Si la section 5 (voix) n'est pas remplie, demander a l'utilisateur de
la preciser avant de rediger en masse (proposer 2-3 exemples de ton pour valider avant de
lancer tout le batch).

### Etape 2 - Rediger un echantillon

Sur les 3 premiers prospects de la liste, rediger le message et le montrer a l'utilisateur
pour validation avant de faire tourner sur toute la liste. Ajuster si retour negatif.

### Etape 3 - Generer pour toute la liste

Une fois l'echantillon valide, generer le message pour chaque ligne restante. Signaler les
lignes ou les donnees sont trop pauvres pour personnaliser correctement (proposer de les
enrichir d'abord via `trouver-email`/`trouver-entreprises`, ou de les exclure).

### Etape 4 - Sauvegarder

Ecrire le CSV enrichi de la colonne `message` (et `sujet` si email), meme emplacement que le
fichier d'entree, suffixe `_messages`.

### Etape 5 - Proposer l'etape suivante

"Pret a lancer : `envoyer-invitation` pour LinkedIn, ou `creer-campagne-lemlist` puis
`envoyer-vers-lemlist` pour email."
