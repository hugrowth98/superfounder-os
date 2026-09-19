---
name: definir-icp
description: >
  Définit ou resserre le client idéal de l'utilisateur en trois couches (firmographique,
  technographique, comportementale), avec un score sur 100, des seuils de tiers, des
  disqualifiants, et un test de volume sur le marché réel. Se déclenche sur : "ICP",
  "client idéal", "qui viser", "mes critères", "ma cible est trop large", "combien
  d'entreprises correspondent", "à qui je vends", "affiner ma cible". Ne pas utiliser pour
  trouver des entreprises (voir `sourcer-entreprises`), pour choisir des comptes nommés
  (voir `selectionner-comptes`), ni pour cartographier qui contacter dans l'entreprise
  (voir `cartographier-personas`).
---

Un ICP écrit en trois couches et noté sur 100 transforme "les PME B2B" en une liste de quelques centaines d'entreprises qu'on peut contacter une par une ; les entreprises qui matchent les trois couches convertissent 3 à 5 fois mieux que le reste du marché.

## Ressources

- `{SKILL_BASE}/ressources/icp-3-couches.md` : le cadre, le score, le format attendu dans `05_Departements/Go-to-Market/contexte.md`, un exemple noté.
- `{SKILL_BASE}/ressources/scoring-tam.md` : comment tester le modèle sur les clients signés et perdus.
- `{SKILL_BASE}/ressources/conseils-list-building.md` : les erreurs de ciblage qui coûtent le plus.

## Méthode

1. Partez de ce qui a signé. Demandez les 10 à 20 meilleurs clients (les plus rentables, les plus rapides à signer, ceux qui restent). Si HubSpot est branché, tirez-les des affaires gagnées. Notez leurs points communs : secteur, effectif, zone, outils, ce qui se passait chez eux au moment de signer.
2. Faites l'anti-ICP avec les 5 pires : churn rapide, cycle long, support lourd, marge nulle. Leurs points communs deviennent des disqualifiants ou des critères à zéro point.
3. Remplissez la couche firmographique : secteurs cœur, adjacents, exclus ; effectif idéal, acceptable, bornes dures ; zones ; stade ; modèle. Une fourchette large sur un critère, jamais sur tous.
4. Remplissez la couche technographique : outils complémentaires (l'offre s'y branche), outils concurrents (le besoin existe), marqueur de maturité (un CRM, un site avec formulaire). Si l'utilisateur ne sait pas, laissez vide : `detecter_techno` renseignera plus tard.
5. Remplissez la couche comportementale : les 2 à 3 signaux qui précèdent un achat chez lui (recrutement d'un commercial, levée, nouveau dirigeant, réaction à un post). Ils deviennent les signaux prioritaires de `detecter-signaux`.
6. Posez les points. Partez des valeurs par défaut de la section 2 (couche 1 : 40, couche 2 : 20, couche 3 : 40), montez ce qui distingue les meilleurs clients, descendez le reste. La somme fait 100. Si l'offre ne dépend d'aucun outil, la couche 2 passe à 0 et ses points vont aux couches 1 et 3. Fixez les seuils A, B, C (défaut 75, 55, 35).
7. Testez le modèle : les 10 meilleurs clients doivent sortir A ou B, les 5 pires C ou D. Sinon, ajustez avant d'aller plus loin.
8. Testez le volume : lancez `trouver_entreprises` avec les critères de la couche 1, limité à 25 lignes. Lisez le total quand la source l'annonce (Sales Navigator via Unipile, Crustdata) ; avec un actor qui ne le donne pas, lancez 25 lignes par segment et extrapolez avec le nombre de pages. Comparez aux nouveaux prospects par semaine écrits en section 5 de `05_Departements/Go-to-Market/contexte.md` : le marché doit couvrir au moins six mois de prospection (26 fois ce volume), sinon élargissez un critère (zone secondaire, secteur adjacent). S'il couvre plus de dix ans, resserrez l'effectif ou le secteur : un marché qu'on ne contactera jamais dilue l'effort.
9. Écrivez la section 2 de `05_Departements/Go-to-Market/contexte.md` remplie, au format décrit dans `icp-3-couches.md`. Montrez-la, attendez le oui, puis proposez de l'écrire. Vous ne modifiez `05_Departements/Go-to-Market/contexte.md` que sur ce oui explicite.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1, si CRM branché | lire_crm (affaires gagnées) | `crm` (`lire --statut gagnes`) | rien | `entreprise`, `domaine`, `secteur`, `effectif` des clients signés |
| 8 | `trouver_entreprises` en comptage, limite 25 | `trouver-entreprises` | critères de la couche 1 | total annoncé par l'outil, 25 lignes témoins avec `entreprise`, `domaine`, `secteur`, `effectif`, `ville`, `pays`, `source`, `date_extraction` |
| 8, si demandé | `detecter_techno` sur 10 clients | `enrichir-entreprise --techno` | `domaine` | techno présente, pour remplir la couche 2 |

Le reste est du raisonnement avec l'utilisateur, sans appel payant. Le test de volume est le seul appel, annoncé avant d'être lancé.

## Repères

| Repère | Valeur |
|---|---|
| Clients à analyser pour un ICP | 10 à 20 meilleurs, 5 pires |
| Volume minimum d'un marché adressable | six mois de prospection, soit 26 fois les nouveaux prospects par semaine de la section 5 |
| Volume au-delà duquel on resserre | dix ans de prospection au rythme actuel |
| Conversion d'une cible bien définie contre une cible large | 3 à 5 fois plus |
| Seuils de tiers par défaut | A 75, B 55, C 35 |
| Relecture de l'ICP | chaque trimestre, à partir des signés et des churnés |
| Critères par couche | 3 à 5, pas plus |

## Template

```
### Couche 1 : firmographique (40 points par défaut)
| Critère | Valeur cible | Points si exact | Points si adjacent | Sinon |
| Secteur | <2 à 4 secteurs ; adjacent : ...> | 15 | 7 | 0 |
| Effectif | <fourchette ; adjacent : ...> | 10 | 5 | 0 |
| Zone géographique | <zones ; adjacent : ...> | 8 | 4 | 0 |
| Stade ou chiffre d'affaires | <ou vide> | 7 | 3 | 0 |
### Couche 2 : technographique (20 points par défaut)
| Outil ou stack qui rend votre offre pertinente | <outils> | 12 | 6 | 0 |
| Outil concurrent en place | <outils concurrents> | 3 | 8 | 8 |
### Couche 3 : comportementale (40 points par défaut)
signal n°1 < [30] jours : 15 / signaux n°2 à 5 < [60] jours : 10 / empilement : 10 / engagement direct : 5
### Tiers
A : [75] à 100 / B : [55] à [74] / C : [35] à [54] / D : sous [35]
### Exclusions
B2C : <oui | non> / Concurrents : <noms ou familles> / Secteurs exclus : <...> / Tailles exclues, autres : <...>
```

Le format complet, avec les exemples en commentaire, est la section 2 de `05_Departements/Go-to-Market/contexte.md` ; sa lecture est décrite dans `icp-3-couches.md`.

## Règles

- Un ICP se déduit des clients signés, jamais d'une intuition seule. Sans client signé, on écrit une hypothèse, on la marque comme telle, et on la relit après 5 rendez-vous.
- Une fourchette large sur un critère est acceptable ; sur tous les critères, ce n'est plus un ICP.
- Une donnée que l'utilisateur ne connaît pas reste vide dans `05_Departements/Go-to-Market/contexte.md`. Vous n'inventez ni pondération ni secteur.
- Les pondérations vivent dans `05_Departements/Go-to-Market/contexte.md`, jamais dans un skill.
- Le test de volume se fait avant de valider l'ICP.
- Vous ne modifiez `05_Departements/Go-to-Market/contexte.md` que sur un oui explicite, et vous montrez le bloc complet avant.
- Une seule question à la fois pendant la méthode.

## Exemples

- "Ma cible c'est les PME B2B" : vous demandez les 10 derniers clients signés, vous en tirez secteurs et effectifs communs, puis un test de volume ; réponse attendue : une section ICP à trois couches et un marché dimensionné sur six mois à dix ans de prospection.
- "Combien de boîtes correspondent à ma cible ?" : `trouver_entreprises` en comptage sur la couche 1 ; réponse attendue : le total, 25 lignes témoins, et un avis (élargir, resserrer, ou garder).
- "Mes clients qui restent sont tous des cabinets de 10 à 30 personnes avec HubSpot" : vous montez la pondération de l'effectif et de la techno, vous descendez le secteur ; réponse attendue : le barème ajusté, testé sur les 10 clients, prêt à écrire dans `05_Departements/Go-to-Market/contexte.md`.
