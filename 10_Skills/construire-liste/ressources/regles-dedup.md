# Règles de dédoublonnage

Lu par `dedoublonner-liste` et par la porte 0 de `gates-qualification.md`. Deux sources sur la même cible se recouvrent à 30 ou 60 %. Sans dédoublonnage, la même personne reçoit deux séquences, l'utilisateur paie deux enrichissements, et les statistiques de campagne sont fausses. On dédoublonne avant d'enrichir, après avoir fusionné des sources, et après avoir scoré (en gardant la ligne au meilleur score).

## Les clés, dans l'ordre

| Priorité | Clé | Normalisation avant comparaison | Fiabilité |
|---|---|---|---|
| 1 | `linkedin_url` | `https://www.linkedin.com/in/<slug>` : minuscules, avec `www.`, sans paramètres, sans barre finale | la plus haute, une personne a une seule URL |
| 2 | `email` | minuscules, sans espace | haute ; deux emails différents peuvent être la même personne (pro et perso) |
| 3 | `domaine` + `prenom` + `nom` | domaine nu, prénom et nom sans accent ni majuscule, sans tiret | moyenne ; deux homonymes dans la même entreprise sont rares mais existent |
| 4 | `telephone` | format international | contrôle secondaire |
| 5 | `prenom` + `nom` + `titre` + `ville` | idem | dernier recours, risque de faux doublon, à faire valider |

Pour les entreprises : `domaine` d'abord, puis `linkedin_entreprise_url`, puis `entreprise` normalisée (sans suffixe juridique, sans accent, minuscules). Deux lignes avec le même `domaine` et deux noms différents sont la même entreprise (une marque et sa raison sociale).

Un match sur la clé 1 ou 2 fusionne sans question. Un match sur la clé 3 fusionne aussi, en le comptant à part dans le rapport. Un match sur la clé 4 ou 5 se montre à l'utilisateur avant de fusionner.

## Ordre de priorité des sources

Quand deux lignes fusionnent, chaque colonne garde une seule valeur. Règle générale : la valeur vérifiée la plus récente gagne. À égalité, la source la plus fiable pour cette colonne gagne :

| Colonne | Source qui gagne | Puis |
|---|---|---|
| `titre`, `entreprise`, `linkedin_url` | LinkedIn (Sales Navigator, profil, page entreprise) | base large, puis CRM |
| `email`, `email_statut`, `telephone` | FullEnrich, statut le plus fiable d'abord (`DELIVERABLE`, puis `HIGH_PROBABILITY`, puis `CATCH_ALL`) | CRM, puis base large |
| `effectif`, `secteur`, `ville`, `pays`, `domaine` | `enrichir_entreprise` (Crustdata, page LinkedIn) | base large, puis Google Maps |
| `signal_type`, `signal_date`, `signal_detail`, `score_signal` | le signal le plus récent | |
| `score_icp`, `tier` | le plus haut, puis on rescore après fusion | |
| `source` | les sources concaténées, séparées par `+`, nom complet de l'actor ou de l'outil : `curious_coder/linkedin-sales-navigator-search-scraper+code_crafter/leads-finder`, `unipile+fullenrich` | |
| `date_extraction` | la plus récente | |

Une cellule vide ne gagne jamais contre une cellule remplie. Une cellule remplie n'est écrasée que par une valeur plus récente et vérifiée.

## Contre le CRM

`dedoublonner --hubspot` croise par `email` en minuscules (contacts, lots de 100), la seule clé native fiable dans HubSpot, puis par `domaine` au niveau entreprise (lots de 90) : `domaine` dit si l'entreprise est déjà connue même quand le contact est nouveau. Chaque ligne reçoit `dans_crm` (`oui` ou `non`), `hubspot_contact_id`, `hubspot_entreprise_id` et `hubspot_lifecycle`. Par défaut c'est une annotation ; `--exclure-crm` met `exclu = oui`, `raison_exclusion = deja dans HubSpot (contact)` ou `(entreprise)`.

Le script ne calcule aucune catégorie (client, affaire ouverte, churné, perdu). Les clients et les perdus viennent du seul export CRM qui existe, `crm lire --statut gagnes` et `crm lire --statut perdus` (`crm_clients-gagnes_<date>.csv`, `crm_clients-perdus_<date>.csv`, avec `affaire`, `montant`, `date_cloture`, `statut`), passés en `--contre` :

| Export | Règle | Action |
|---|---|---|
| `--statut gagnes` | un client se définit par une affaire gagnée, jamais par `hubspot_lifecycle` | en `--contre` : exclu, `raison_exclusion = deja dans crm_clients-gagnes_<date>.csv` |
| `--statut perdus`, `date_cloture` de moins de 3 mois | perdu récent, calculé à la date du jour | filtrer l'export sur `date_cloture`, passer ces lignes en `--contre` |
| `--statut perdus`, `date_cloture` de plus de 3 mois | il redevient approchable avec un angle neuf | garder, signaler dans le rapport |
| `dans_crm = oui` hors de ces exports | contact connu, sans affaire gagnée ni perdue | garder annoté (défaut) ou exclure avec `--exclure-crm`, question à l'utilisateur |

Pas d'export "churnés" ni "sans affaire". Un CRM où le produit crée des contacts marque des centaines de personnes `customer` sans affaire ; les compter comme clients gonfle le résultat et vide la liste. `hubspot_lifecycle` s'affiche, il ne décide pas.

## Fichiers de référence (`--contre`)

`--contre <csv>` (répétable) met `exclu = oui`, `raison_exclusion = deja dans <fichier>` sur toute ligne dont une clé (`linkedin_url`, `email`, `domaine` + `nom`) est dans le fichier. Deux fichiers à entretenir à la main après chaque campagne : `ne_plus_contacter` (bounces durs, désabonnés, "pas intéressé", lignes `ne_plus_contacter = oui` écrites par `verifier-reponses`) et les listes envoyées. Il n'y a pas de fenêtre de 90 jours automatique : la règle "pas recontacté avant 90 jours" se tient en passant en `--contre` les listes envoyées sur la période. L'outil d'envoi a un garde-fou "ne pas recontacter un lead déjà présent" : il sert de filet, pas de méthode.

## Plafond par entreprise

Après fusion, `--max-par-entreprise 5` (valeur par défaut, `0` pour lever le plafond) garde au plus 5 personnes par `domaine` (ou par `entreprise` sans domaine), meilleur `score_icp` puis ligne la plus remplie. Les autres restent dans le fichier avec `exclu = oui`, `raison_exclusion = plafond 5 par entreprise`, et une ligne dans le journal. La répartition 2 à 4 sur un tier A, 1 à 2 sur un B, 1 sur un C se fait au jugement, séniorité la plus haute d'abord.

## Journal des doublons

Chaque run écrit un second fichier à côté de la sortie, `dedoublonner_<sujet>_<date>_doublons.csv` : une ligne par fusion (`groupe`, `type_cle`, `cle`, `ligne_gardee`, `ligne_fusionnee`, `fichier`, `entreprise`, `nom`) et une ligne par personne retirée par le plafond (`cle`, `raison`, `email`, `linkedin_url`). L'utilisateur peut y vérifier un faux doublon et le réintégrer.

## Rapport

```
Fichiers en entrée : 3 (curious_coder/linkedin-sales-navigator-search-scraper 412, harvestapi/linkedin-profile-search 380, harvestapi/linkedin-company-employees 96) = 888 lignes
Doublons dans les fichiers : linkedin_url 201, email 44, domaine + nom 17 = 262 fusionnés -> 626
HubSpot (--hubspot) : dans_crm 55 annotés, hubspot_lifecycle affiché
Référence (--contre crm_clients-gagnes, crm_clients-perdus < 3 mois) : 24 exclus (gagnés 19, perdus < 3 mois 5) ; perdus > 3 mois 9 gardés, signalés
Référence (--contre ne_plus_contacter, dernière liste envoyée) : 18 exclus
Plafond 5 par entreprise (--max-par-entreprise 5) : 27 exclus
Sortie : dedoublonner_<sujet>_<date>.csv, 626 lignes dont 557 prospectables (888 - 262 - 24 - 18 - 27)
Journal : dedoublonner_<sujet>_<date>_doublons.csv, 289 lignes (262 fusions + 27 plafond)
Question : les 31 dans_crm = oui sans affaire, on exclut (--exclure-crm) ou on garde annotés ?
Hygiène : 6 emails de test, 2 entreprises nommées "Test", 14 libellés d'entreprise en double par casse
```

## Ce qu'on ne fait pas

- Dédoublonner sur le nom seul sans domaine.
- Perdre une ligne sans trace : un doublon fusionne et se journalise, une exclusion se marque `exclu = oui`.
- Fusionner deux personnes parce qu'elles ont le même titre dans la même entreprise.
- Compter `hubspot_lifecycle = customer` comme client : seul l'export `crm lire --statut gagnes` fait foi.
- Écraser un `email_statut = DELIVERABLE` récent par une valeur non vérifiée d'une autre source.
