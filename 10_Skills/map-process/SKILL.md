---
name: map-process
description: Cartographier tous les process recurrents (perso et pro) par frequence, et reflechir a leur optimisation avec l'IA. Produit une cartographie dans 05_Departements/Strategie/.
user-invocable: true
context: main
---

# Map Process

Tu guides l'utilisateur pour cartographier ses process et reflechir a leur amplification par l'IA.

Structure du second cerveau :
- Identite : `01_About-Me/about-me.md` (+ `01_About-Me/my-company.md` si activite pro)
- Dossiers de travail : `06_Clients/`, `05_Departements/Marketing/`, `05_Departements/Vente/`, `05_Departements/Strategie/`
- Sortie : `05_Departements/Strategie/Cartographie-process.md`

## Avant de commencer
1. Lis `01_About-Me/about-me.md` (et `my-company.md`) pour comprendre l'activite de l'utilisateur.
2. Verifie si une cartographie existe deja (pour l'enrichir, pas l'ecraser).

## Process

### Etape 1 : Exploration par pole
Le mapping suit l'activite reelle de l'utilisateur. Pour chaque pole, fais emerger les process (taches recurrentes ou declenchees). Exemples de poles a adapter :

- **Acquisition / vente** : prospection, sequences, relances, qualification, propositions
- **Contenu** : ideation, redaction, mise en forme, veille
- **Delivery / clients** : onboarding, preparation, livrables, suivi, reporting
- **Operations / admin** : mails, tri inbox, facturation, compta
- **Perso** : routines, sante, apprentissage, planification

Pose des questions ouvertes. Demande a l'utilisateur de se projeter heure par heure dans une journee type. Cherche les taches repetitives, les taches declenchees par un evenement, les taches ponctuelles mais frequentes.

### Etape 2 : Classification par temporalite
```markdown
## Daily
- [Process]
## Weekly
- [Process]
## Monthly
- [Process]
## On Trigger (evenement declencheur)
- [Process] -> Trigger : [evenement]
## Manuel (ponctuel)
- [Process]
```
La frequence revele le ROI : on priorise ce qui est fait souvent, penible, et qui pese sur le revenu (ou le temps).

### Etape 3 : Creation du fichier (apres validation)
Cree ou mets a jour `05_Departements/Strategie/Cartographie-process.md` :

```markdown
---
type: cartographie-process
maj: YYYY-MM-DD
---
# Cartographie des process

## Daily
- [[Process - Tri inbox]]
## Weekly
- [[Process - ...]]
## Monthly
- [[Process - Facturation]]
## On Trigger
- [[Process - Onboarding nouveau client]]
## Manuel
- [[Process - ...]]

## Priorisation (chronophage x penible x impactant)
1. [Process] - pourquoi prioritaire
```

### Etape 4 : Recapitulatif
```
Process cartographies : [X]
Candidats skills (a documenter via /create-skill) : [liste]
Candidats automatisation : [liste]
Prochaine etape : transformer les 3-5 process prioritaires en skills.
Par lequel voulez-vous commencer ?
```

## Regles
- Questions ouvertes, ne suppose pas.
- Garde une vue d'ensemble avant le detail.
- Valide avant de creer des fichiers.
- Francais, vouvoiement, pas d'em-dash ni en-dash.
