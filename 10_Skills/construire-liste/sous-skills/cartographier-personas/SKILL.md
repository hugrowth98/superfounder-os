---
name: cartographier-personas
description: >
  Cartographie qui contacter dans une entreprise cible : le comité d'achat, les personas
  ATL (C-level, VP, directeur) et BTL (manager, opérationnel), le rôle de chacun dans la
  décision, et l'angle de message par persona. Se déclenche sur : "personas", "qui
  contacter chez", "quel poste viser", "qui décide", "comité d'achat", "ATL", "BTL",
  "décideur ou opérationnel", "je vise le DG ou le directeur commercial ?". Ne pas
  utiliser pour définir l'entreprise cible (voir `definir-icp`), pour trouver les
  personnes elles-mêmes (voir `sourcer-personnes`), ni pour écrire le message (voir
  `cold-email`).
---

Ce sont des personnes qui achètent : un achat B2B implique en moyenne 6 à 10 personnes, et dans une PME de moins de 20 salariés une seule, le dirigeant. Cartographier les personas, c'est savoir à qui on écrit, avec quel angle, et dans quel ordre.

## Ressources

- `{SKILL_BASE}/ressources/personas-comite-achat.md` : rôles du comité, personas par taille, ATL et BTL, attributs, titres par fonction, format attendu dans `05_Departements/Go-to-Market/contexte.md`.
- `{SKILL_BASE}/ressources/icp-3-couches.md` : l'effectif cible, qui décide de la forme du comité.

## Méthode

1. Lisez la valeur cible d'effectif dans la section 2 de `05_Departements/Go-to-Market/contexte.md`. Elle décide du nombre de personnes à viser par compte : 1 sous 20 salariés (le dirigeant), 1 à 2 de 20 à 50, 2 à 4 au-delà de 50. La section 3 tient en deux fiches, ATL et BTL, plus la table du comité d'achat : dans une TPE, la fiche BTL peut rester vide.
2. Partez des affaires gagnées. Qui a répondu au premier message, qui a signé, qui était en copie, qui a failli bloquer. Si HubSpot est branché, les contacts associés aux affaires gagnées répondent aux trois premières questions. Sinon, cinq questions à l'utilisateur, une à la fois.
3. Nommez les rôles : champion (porte le sujet), décideur économique (signe), utilisateur (vit le problème), évaluateur technique, bloqueur. Dans une PME, le dirigeant cumule champion et décideur : un seul persona, deux angles.
4. Classez chaque persona ATL ou BTL. ATL décide et signe, lit court, veut un résultat chiffré et une comparaison avec ses pairs. BTL vit le problème, lit plus long, veut un gain concret sur sa semaine. Le persona BTL sert souvent de porte d'entrée vers l'ATL.
5. Pour chaque fiche, documentez : titres à chercher (français et anglais, masculin et féminin), ce qui l'empêche de dormir ou ce qu'il vit au quotidien, ce qu'il mesure, l'angle d'approche, le canal qui marche le mieux. Le rôle de chacun va dans la table du comité d'achat avec son poids. Une case que l'utilisateur ne sait pas remplir reste vide.
6. Vérifiez que les titres existent : lancez `trouver_personnes` sur 10 entreprises tier A avec les titres du persona, limité à 25 lignes. Si moins de la moitié des entreprises renvoient quelqu'un, les titres sont mal choisis pour cette taille d'entreprise (un "Head of Sales" n'existe pas dans un cabinet de 15 personnes ; c'est le gérant).
7. Fixez l'ordre de contact : champion d'abord, décideur quand le champion est chaud, évaluateur au moment de la démonstration, bloqueur traité par anticipation dans le message.
8. Écrivez la section 3 de `05_Departements/Go-to-Market/contexte.md` remplie (deux fiches et la table). Montrez, attendez le oui, puis proposez de l'écrire.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 2, si CRM branché | lire_crm (contacts des affaires gagnées) | `crm` (`lire --statut gagnes`) | rien | `prenom`, `nom`, `titre`, `entreprise`, `effectif` des contacts gagnés |
| 6 | `trouver_personnes`, limite 25 | `trouver-personnes` | `linkedin_entreprise_url` de 10 comptes tier A, titres du persona | `prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `linkedin_url`, `source`, `date_extraction` |

Le reste est du raisonnement. Le test de l'étape 6 est le seul appel, annoncé avant.

**Où ça s'écrit** : la carte des personas par tranche d'effectif (qui décide, qui vit le problème, qui signe, l'angle de chacun) dans `05_Departements/Go-to-Market/Ciblage/decisionnaires-par-taille.md`, relue par `sourcer-personnes`, `cold-email` et `cold-call`. La section 3 de `05_Departements/Go-to-Market/contexte.md` garde le résumé en dix lignes, ce fichier le détail.

## Repères

| Repère | Valeur |
|---|---|
| Personnes impliquées dans un achat B2B | 6 à 10 en moyenne, 1 à 2 dans une PME de moins de 50 |
| Personas par taille d'entreprise | 1 sous 20 salariés, 1 à 2 de 20 à 50, 2 à 4 au-delà de 50 |
| Effort par rôle | champion 40 à 50 %, décideur 20 à 30 %, utilisateur 15 à 20 %, évaluateur 5 à 10 % |
| Contacts par compte | 2 à 4 sur un tier A, 1 à 2 sur un tier B, 1 sur un tier C, 5 au plus par entreprise |
| Test de titres | 10 comptes, au moins la moitié doivent renvoyer une personne |
| Fiches dans `05_Departements/Go-to-Market/contexte.md` | 2 (ATL, BTL) plus la table du comité ; une recherche par fonction listée |

## Template

```
### ATL : le décideur
- Titres à chercher : <titres, variantes féminines et anglaises>
- Ce qui l'empêche de dormir : <douleur, dans ses mots>
- Ce qu'il mesure : <indicateur>
- Angle d'approche : <la promesse en une phrase ; ce qu'il ne veut pas lire>
- Canal qui marche le mieux : <téléphone | email | LinkedIn, dans l'ordre>

### BTL : celui qui vit le problème
- Titres à chercher : <...>
- Ce qu'il vit au quotidien : <...>
- Ce qu'il mesure : <...>
- Angle d'approche : <...>
- Canal qui marche le mieux : <...>

### Comité d'achat chez vos clients
| Rôle | Qui c'est (titre) | Ce qu'il attend de vous | Poids dans la décision |
| Champion | <titre> | <attente> | <x %> |
| Décideur économique | <titre> | <attente> | <x %> |
| Utilisateur | <titre ou "aucun"> | <attente> | <x %> |
| Évaluateur | <titre ou "aucun"> | <attente> | <x %> |
| Bloqueur possible | <titre ou "aucun"> | <objection> | à surveiller |
```

C'est la section 3 de `05_Departements/Go-to-Market/contexte.md` ; les attributs supplémentaires (objectif de l'année, ce qu'il ne veut pas entendre) se fondent dans "ce qui l'empêche de dormir" et "angle d'approche".

## Règles

- Une fiche (ATL ou BTL) par recherche et par CSV dans `sourcer-personnes`, et une recherche par fonction quand la fiche liste des titres de fonctions différentes : le fichier porte le persona en sujet.
- Les titres se vérifient sur le terrain (étape 6) avant d'entrer dans `05_Departements/Go-to-Market/contexte.md`.
- Pas de persona sans douleur écrite : un persona sans douleur donne un message sans angle.
- Le dirigeant d'une PME est toujours un persona, même quand la fonction visée est le marketing ou le commercial : c'est lui qui paie.
- Vous n'inventez ni objectif ni douleur ; ce que l'utilisateur ne sait pas reste vide, et `cold-call` le lui fera découvrir en appel.
- Vous ne modifiez `05_Departements/Go-to-Market/contexte.md` que sur un oui explicite.
- L'angle de message reste une phrase de brief pour `cold-email` ; l'écriture du message se fait là-bas.

## Exemples

- "Je vise le DG ou le directeur commercial ?" : vous lisez l'effectif cible ; réponse attendue : sous 50 salariés le DG seul, au-delà le directeur commercial en champion et le DG en décideur, avec l'ordre de contact.
- "Cartographie mes personas" : cinq questions sur les affaires gagnées, une à la fois, puis test de titres sur 10 comptes ; réponse attendue : la fiche ATL, la fiche BTL et la table du comité au format de la section 3, prêtes à écrire sur validation.
- "Mes messages aux DRH ne répondent pas" : vous vérifiez si le DRH est le champion ou le décideur pour cette offre et cette taille ; réponse attendue : un persona BTL (responsable recrutement) comme porte d'entrée, l'angle adapté, et le DRH repositionné en décideur.
