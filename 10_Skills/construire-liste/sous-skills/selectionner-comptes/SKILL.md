---
name: selectionner-comptes
description: >
  Sélectionne une liste de comptes cibles par ressemblance aux meilleurs clients :
  analyse des clients signés, quatre couches de sélection (fit, techno, CRM, lookalikes),
  dimensionnement à partir d'un objectif de revenu, tiers A, B, C. Se déclenche sur :
  "comme mes clients", "lookalikes", "comptes cibles", "ABM", "combien de comptes il me
  faut", "mes meilleurs clients", "les boîtes qui ressemblent à", "liste de comptes
  nommés". Ne pas utiliser pour une recherche large par critères (voir
  `sourcer-entreprises`), pour écrire l'ICP lui-même (voir `definir-icp`), ni pour scorer
  un fichier existant (voir `qualifier-comptes`).
---

Choisir ses comptes avant de chercher des contacts concentre l'effort là où le fit est prouvé : une liste de comptes construite à partir des meilleurs clients signés convertit mieux qu'une recherche large, et coûte moins en contacts payés. La méthode part des clients, jamais d'un filtre.

## Ressources

- `{SKILL_BASE}/ressources/scoring-tam.md` : construire le modèle, prioriser dans un tier, croiser tier du compte et séniorité du contact.
- `{SKILL_BASE}/ressources/icp-3-couches.md` : les critères que les meilleurs clients doivent confirmer.
- `{SKILL_BASE}/ressources/sources-par-besoin.md` : lookalikes et pages entreprise.

## Méthode

1. Exportez les meilleurs clients : les 10 à 20 premiers par revenu, durée de vie ou vitesse de signature. Depuis HubSpot si branché, sinon l'utilisateur donne les noms et les domaines.
2. Trouvez ce qu'ils partagent : secteur, effectif, zone, stade, outils, ce qui se passait chez eux au moment de signer. Trois points communs suffisent ; s'ils contredisent `05_Departements/Go-to-Market/contexte.md`, signalez-le et proposez un passage par `definir-icp`.
3. Couche CRM : `crm lire --statut perdus`, puis gardez les affaires perdues de plus de 6 mois (`date_cloture`) : elles avaient le problème et le moment était mauvais, ou un concurrent a comblé le manque. Ces comptes sont chauds : ils connaissent déjà l'utilisateur. Il n'existe pas d'export "churnés" ni "contacts sans affaire" : si l'utilisateur veut ces comptes, il donne les noms.
4. Couche lookalikes : `trouver_lookalikes` à partir des domaines des meilleurs clients. Gardez ce qui confirme les trois points communs de l'étape 2.
5. Couche techno, si la couche 2 de l'ICP est remplie : `detecter_techno` sur les candidats pour repérer un outil concurrent (ils ont le besoin) ou complémentaire (l'offre se branche).
6. Dimensionnez. Objectif de revenu divisé par le panier moyen = affaires nécessaires ; divisé par le taux de signature = rendez-vous nécessaires ; divisé par le taux de rendez-vous par compte = comptes à cibler. Les taux viennent de l'historique de l'utilisateur, jamais d'une moyenne de marché. Exemple avec des hypothèses à remplacer : 100 000 € visés, panier 5 000 €, signature 25 %, rendez-vous sur 10 % des comptes : 20 affaires, 80 rendez-vous, 800 comptes.
7. Scorez et rangez avec `qualifier_liste` : tier A (10 à 50 comptes, sur mesure, 2 à 4 contacts, plusieurs canaux), tier B (50 à 200, personnalisation par segment, 1 à 2 contacts), tier C (200 à 1 000, séquence standard, 1 contact), 5 contacts au plus par entreprise. Un compte sans fit prouvé sort, même s'il est prestigieux.
8. Rendez la liste avec, pour chaque compte, le tier et la raison en une ligne (le point commun avec les clients qui l'a fait entrer). Proposez `cartographier-personas` puis `sourcer-personnes` par page entreprise. L'écriture dans HubSpot (`tier` sur la fiche entreprise) ne se fait que sur oui explicite.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1 et 3 | lire_crm (affaires gagnées, puis perdues) | `crm` (`lire --statut gagnes`, puis `perdus`) | rien | `entreprise`, `domaine`, `secteur`, `effectif`, `source = hubspot`, `affaire`, `montant`, `date_cloture`, `statut` |
| 4 | `trouver_lookalikes` | `trouver-lookalikes` | `domaine` des clients de référence, 10 par appel, plusieurs appels au-delà | `entreprise`, `domaine`, `linkedin_entreprise_url`, `secteur`, `effectif`, `pays`, `source = ocean`, `date_extraction` |
| 4 | `enrichir_entreprise` | `enrichir-entreprise` | `domaine`, lignes où `effectif` ou `secteur` est vide | `secteur`, `effectif`, `ville`, `pays` complétés |
| 5 | `detecter_techno` | `enrichir-entreprise --techno` | `domaine` | techno détectée, pour la couche 2 |
| 7 | `qualifier_liste` | `qualifier-liste` | le CSV fusionné | `score_icp`, `tier`, `exclu`, `raison_exclusion` |

Sortie : `trouver-lookalikes_<sujet>_<date>.csv` puis `qualifier-liste_<sujet>_<date>.csv`.

**Où ça s'écrit** : la liste ABM finale (compte, tier, raison, signal) dans `05_Departements/Go-to-Market/Ciblage/comptes-cibles.csv`, et sa copie de suivi dans `05_Departements/Go-to-Market/Signaux/comptes-suivis.csv` pour `detecter-signaux`.

## Repères

| Repère | Valeur |
|---|---|
| Clients à analyser | 10 à 20 meilleurs |
| Points communs à retenir | 3 |
| Fermés-perdus réutilisables | après 6 mois |
| Tier A | 10 à 50 comptes, 2 à 4 contacts, effort maximal |
| Tier B | 50 à 200 comptes, 1 à 2 contacts, personnalisation par segment |
| Tier C | 200 à 1 000 comptes, 1 contact, séquence standard |
| Formule de dimensionnement | revenu ÷ panier ÷ taux de signature ÷ taux de rendez-vous par compte |

## Template

```
Liste de comptes : <sujet>, <date>
Clients de référence : <n> (<domaines>)
Points communs : 1. <...>  2. <...>  3. <...>
Objectif : <revenu> -> <affaires> -> <rendez-vous> -> <comptes> (hypothèses : panier <x>, signature <y %>, rendez-vous <z %>)
Tier A (<n>) : <entreprise> : <raison en une ligne>
Tier B (<n>) : ...
Tier C (<n>) : ...
Écartés : <n>, raisons principales : <...>
Next step : cartographier-personas, puis sourcer-personnes par page entreprise
```

## Règles

- On part des clients signés. Sans client signé, ce sous-skill ne s'applique pas : renvoyez vers `definir-icp` et `sourcer-entreprises`.
- Les taux de conversion viennent de l'historique de l'utilisateur ; sans historique, on écrit des hypothèses marquées comme telles et on les relit après un mois.
- Un compte prestigieux sans fit prouvé n'entre pas en tier A.
- Les fermés-perdus de moins de 6 mois restent exclus.
- Ocean.io sert aux lookalikes et à rien d'autre.
- Aucune écriture dans HubSpot sans oui explicite sur l'échantillon.
- Une liste de comptes se relit chaque trimestre : les comptes contactés sans réponse descendent d'un tier, les nouveaux signés nourrissent l'étape 1.

## Exemples

- "Trouve-moi des boîtes comme mes trois meilleurs clients" : domaines des trois clients, `trouver_lookalikes`, enrichissement des colonnes vides, `qualifier_liste` ; réponse attendue : une liste tiérée avec la raison par compte, et le nombre de comptes par tier.
- "Combien de comptes il me faut pour 100 k€ cette année ?" : la formule avec les taux de l'utilisateur, ou des hypothèses marquées ; réponse attendue : le nombre de comptes, et si la liste actuelle ne suffit pas, les couches à activer (CRM, lookalikes).
- "Qui dans mon CRM je peux relancer ?" : `crm lire --statut perdus`, filtré sur les pertes de plus de 6 mois (pas d'export "churnés" ni "sans affaire") ; réponse attendue : une liste chaude avec l'affaire et la date de la perte, classée par tier.
