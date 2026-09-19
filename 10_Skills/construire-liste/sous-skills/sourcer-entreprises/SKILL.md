---
name: sourcer-entreprises
description: >
  Trouve les entreprises qui correspondent à l'ICP en combinant plusieurs sources :
  chaudes (CRM, engagement, événements), bases larges (Sales Navigator,
  `code_crafter/leads-finder`, Crustdata), spécialisées (Google Maps pour le local, annuaires, lookalikes). Se
  déclenche sur : "trouve des entreprises", "des boîtes qui", "des agences", "des
  cabinets", "des commerces à", "où trouver des", "liste d'entreprises", "sourcer". Ne pas
  utiliser pour trouver des personnes (voir `sourcer-personnes`), pour partir des
  meilleurs clients (voir `selectionner-comptes`), ni pour partir d'un signal d'achat
  (voir `detecter-signaux`).
---

Une seule source couvre environ 60 % d'un marché, deux sources en couvrent 85 % : sourcer, c'est choisir deux sources qui n'ont pas les mêmes trous, les lancer avec les mêmes critères, fusionner, puis retirer les 30 à 60 % de doublons.

## Ressources

- `{SKILL_BASE}/ressources/sources-par-besoin.md` : les trois catégories, la matrice besoin vers source vers verbe vers outil, le choix selon la cible, la limite des 2 500.
- `{SKILL_BASE}/ressources/conseils-list-building.md` : ordre des opérations, test petit, erreurs qui coûtent.
- `{SKILL_BASE}/ressources/regles-dedup.md` : la fusion des sources par `domaine`.

## Méthode

1. Lisez la couche 1 de l'ICP dans `05_Departements/Go-to-Market/contexte.md` : secteurs, effectif, zones. Les contraintes de la demande ("à Lyon", "de plus de 20 personnes") s'ajoutent par-dessus. Sans ICP rempli, arrêtez et renvoyez vers `definir-icp`.
2. Cherchez d'abord la source chaude. Le CRM (les affaires perdues de plus de 6 mois : `crm lire --statut perdus`, filtré sur `date_cloture` ; il n'existe pas d'export "churnés" ni "sans affaire"), les réactions aux posts de l'utilisateur, ses inscrits. Une ligne chaude vaut dix lignes froides ; elle passe en tête de liste, repérable à sa `source` (`hubspot` pour l'export CRM, `unipile` ou l'actor de `scraper_engagement` pour les réactions).
3. Choisissez deux sources dans la matrice selon la cible : tech et services numériques, Sales Navigator puis `code_crafter/leads-finder` ; PME traditionnelles, `code_crafter/leads-finder` ou Crustdata puis annuaire ; local, Google Maps puis pages entreprise ; niche, annuaire puis lookalikes. Une seule source si l'utilisateur veut moins de 200 entreprises. `code_crafter/leads-finder` interroge une base de contacts : il rend une ligne par entreprise, dédoublonnée par domaine, avec le dirigeant trouvé au passage (`dirigeant_trouve`, `dirigeant_linkedin_url`, `dirigeant_email`, non vérifié).
4. Traduisez l'ICP en filtres de chaque outil : secteur, effectif, zone, mots-clés. Écrivez les filtres noir sur blanc avant de lancer. Sur Sales Navigator, si le total dépasse 2 500, découpez par région ou par tranche d'effectif.
5. Annoncez le plan : sources, filtres, volume attendu, coût par source, nom du fichier. Attendez le oui. Lancez sur 25 lignes, montrez-les, puis le reste.
6. Fusionnez les runs et dédoublonnez par `domaine`, puis par `linkedin_entreprise_url`, puis par `entreprise` normalisée. Notez dans `source` les sources concaténées.
7. Complétez ce qui manque sur les lignes gardées avec `enrichir_entreprise`, seulement là où `secteur`, `effectif`, `domaine` ou `linkedin_entreprise_url` est vide. Jamais sur les lignes déjà complètes.
8. Passez la liste à `qualifier-comptes` avant toute recherche de personnes. Rendez le fichier, le nombre de lignes par source, le nombre de doublons retirés, et le next step.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 2 | `lire_crm` (export des affaires perdues) | `crm` (`lire --statut perdus`) | rien | `entreprise`, `domaine`, `secteur`, `effectif`, `affaire`, `montant`, `date_cloture`, `statut`, `source = hubspot` |
| 3 à 5 | `trouver_entreprises` | `trouver-entreprises` | secteur, effectif, zone, mots-clés ; ou une catégorie et une ville pour Google Maps ; ou l'URL d'un annuaire | `entreprise`, `domaine`, `linkedin_entreprise_url`, `secteur`, `effectif`, `ville`, `pays`, `source`, `date_extraction`, et pour Google Maps `telephone_entreprise`, `note_google`, `nb_avis` |
| 3, si lookalikes | `trouver_lookalikes` | `trouver-lookalikes` | `domaine` des clients de référence, 10 par appel | mêmes colonnes, `source = ocean` |
| 6 | `dedoublonner` (dans la liste) | `dedoublonner` | les CSV de chaque run | un CSV fusionné, `exclu`, `raison_exclusion = doublon` |
| 7 | `enrichir_entreprise` | `enrichir-entreprise` | `domaine` ou `linkedin_entreprise_url`, lignes où une colonne de fit est vide | `secteur`, `effectif`, `ville`, `pays`, `domaine`, `linkedin_entreprise_url` complétés, plus `description`, `tagline`, `chiffre_affaires_estime`, `stade_financement`, `nb_offres_emploi` (et `posts_recents` avec `--posts`) |

Sortie : `trouver-entreprises_<sujet>_<date>.csv` dans `05_Departements/Go-to-Market/Listes-prospection/`.

## Repères

| Repère | Valeur |
|---|---|
| Couverture d'une source, de deux, de trois | 60 %, 85 %, 92 % |
| Doublons attendus entre deux sources | 30 à 60 % |
| Résultats maximum par recherche Sales Navigator | 2 500 |
| Volume par run Google Maps | quelques centaines par catégorie et par ville |
| Fermés-perdus réutilisables | après 6 mois, avec un angle neuf |
| Lignes de test avant le run complet | 25 |
| Contacts par compte prévus ensuite | 2 à 4 sur un tier A |

## Template

```
Plan de sourcing : <sujet>
Cible : <secteurs> / <effectif> / <zone> (+ contraintes de la demande)
Source chaude : <crm | engagement | aucune> -> <n> lignes
Source 1 : <outil> avec <filtres> -> <volume attendu>, <coût>
Source 2 : <outil> avec <filtres> -> <volume attendu>, <coût>
Fusion et dédoublonnage par domaine -> <volume net attendu>
Fichier : trouver-entreprises_<sujet>_<date>.csv
Next step : qualifier-comptes
```

## Règles

- Deux sources minimum au-delà de 200 entreprises visées.
- Jamais de recherche large sans effectif ni secteur fixés.
- Jamais de personnes avant que la liste d'entreprises soit passée par `qualifier-comptes`.
- L'effectif d'une base large est déclaratif : on le vérifie avec `enrichir_entreprise` sur les tiers A, pas sur tout le fichier.
- Une source qui produit plus de 30 % de lignes exclues à la qualification se remplace au prochain run.
- Aucun annuaire dont les conditions interdisent l'extraction, aucune donnée de particulier.
- Le coût est annoncé avant chaque run, et le run complet ne part qu'après validation des 25 lignes de test.

## Exemples

- "Trouve-moi des agences immobilières à Lyon" : Google Maps sur "agence immobilière Lyon", filtre sur le nombre d'avis, puis pages entreprise LinkedIn pour compléter ; réponse attendue : un CSV d'entreprises avec téléphone et site, doublons retirés, prêt pour `qualifier-comptes`.
- "Des SaaS RH de 20 à 200 personnes en France" : Sales Navigator via Unipile (secteur logiciels, mots-clés RH, effectif 11-50 et 51-200 en deux runs) puis `code_crafter/leads-finder` avec les mêmes filtres ; réponse attendue : fusion par domaine, nombre de lignes par source, taux de doublons.
- "Qui je peux recontacter dans mon CRM ?" : `crm lire --statut perdus`, filtré sur les pertes de plus de 6 mois (`date_cloture`) ; réponse attendue : une liste chaude avec la date de la perte et l'affaire, à traiter avant toute source froide.
