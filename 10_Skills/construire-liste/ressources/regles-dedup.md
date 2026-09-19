# Règles de dédoublonnage

Lu par `dedoublonner-liste` et par la porte 0 de `gates-qualification.md`. Deux sources sur la même cible se recouvrent à 30 ou 60 %. Sans dédoublonnage, la même personne reçoit deux séquences, l'utilisateur paie deux enrichissements, et les statistiques de campagne sont fausses. On dédoublonne avant d'enrichir, après avoir fusionné des sources, et après avoir scoré (en gardant la ligne au meilleur score).

## Les clés, dans l'ordre

| Priorité | Clé | Normalisation avant comparaison | Fiabilité |
|---|---|---|---|
| 1 | `linkedin_url` | minuscules, sans paramètres, sans barre finale, sans "www." | la plus haute, une personne a une seule URL |
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
| `email`, `email_statut`, `telephone` | FullEnrich avec statut `valide` | CRM, puis base large |
| `effectif`, `secteur`, `ville`, `pays`, `domaine` | `enrichir_entreprise` (Crustdata, page LinkedIn) | base large, puis Google Maps |
| `signal_type`, `signal_date`, `signal_detail`, `score_signal` | le signal le plus récent | |
| `score_icp`, `tier` | le plus haut, puis on rescore après fusion | |
| `source` | les sources concaténées, séparées par un point-virgule : `sales-navigator;actor-apollo` | |
| `date_extraction` | la plus récente | |

Une cellule vide ne gagne jamais contre une cellule remplie. Une cellule remplie n'est écrasée que par une valeur plus récente et vérifiée.

## Contre le CRM

Le croisement se fait par `email` en minuscules, la seule clé native fiable dans HubSpot. Si le CRM porte une propriété URL LinkedIn, elle sert de seconde clé. Au niveau entreprise, `domaine` dit si l'entreprise est déjà cliente même quand le contact est nouveau.

Chaque ligne trouvée dans le CRM reçoit une catégorie, dans cet ordre de priorité :

| Catégorie | Définition | Action |
|---|---|---|
| Client | une affaire dans le pipeline clients, hors étape churn | exclu, `raison_exclusion = deja client` |
| Affaire ouverte | une affaire active dans un pipeline de vente | exclu, `raison_exclusion = affaire en cours` |
| Churné | une affaire au stade churn | exclu par défaut, à réactiver à la main après 6 mois |
| Perdu depuis moins de 3 mois | une affaire fermée perdue récente | exclu, `raison_exclusion = perdu recemment` |
| Perdu depuis plus de 3 mois | idem, plus ancienne | garde, signalé : il redevient approchable avec un angle neuf |
| Présent sans affaire | un contact connu, sans affaire rattachée | garde, avec son cycle de vie affiché (lead, abonné, utilisateur) |
| Absent | inconnu du CRM | garde, vrai nouveau |

"Client" se définit par une affaire dans le pipeline clients, pas par le champ cycle de vie. Un CRM où le produit crée des contacts marque des centaines de personnes "customer" sans affaire ; les compter comme clients gonfle le résultat et vide la liste. Le cycle de vie s'affiche, il ne décide pas. Le délai de 3 mois se calcule depuis la date du jour.

## Liste de suppression

Une liste de suppression par utilisateur, entretenue après chaque campagne : contactés dans les 90 derniers jours, bounces durs, désabonnés, "pas intéressé". Toute nouvelle liste s'y croise avant l'envoi. L'outil d'envoi a un garde-fou "ne pas recontacter un lead déjà présent" : il sert de filet, pas de méthode.

## Plafond par entreprise

Après fusion, on garde au plus 5 contacts par `domaine` (2 à 4 sur un tier A, 1 à 2 sur un B, 1 sur un C), classés par séniorité décroissante puis par fraîcheur. Les autres restent dans le fichier avec `exclu = oui`, `raison_exclusion = plafond par entreprise`.

## Journal des doublons

Chaque run écrit un second fichier à côté de la sortie, `dedoublonner_<sujet>-doublons_<date>.csv`, avec une ligne par ligne retirée : la clé qui a matché, la ligne gardée (son `linkedin_url` ou `email`), la ligne retirée, la source de chacune, la catégorie CRM si elle vient de là. L'utilisateur peut y vérifier un faux doublon et le réintégrer.

## Rapport

```
Fichiers en entrée : 3 (sales-navigator 412, actor-apollo 380, google-maps 96) = 888 lignes
Doublons dans les fichiers : linkedin_url 201, email 44, domaine + nom 17 = 262 retirés -> 626
Croisement CRM (HubSpot, 1 140 affaires, 2 300 contacts) :
  client 12, affaire ouverte 5, churné 3, perdu < 3 mois 4, perdu > 3 mois 9 (gardés), présent sans affaire 31 (gardés)
Liste de suppression : 18 retirés
Plafond par entreprise : 27 retirés
Sortie : dedoublonner_<sujet>_<date>.csv, 584 lignes gardées sur 888, journal : 304 lignes
Hygiène : 6 emails de test, 2 entreprises nommées "Test", 14 libellés d'entreprise en double par casse
```

## Ce qu'on ne fait pas

- Dédoublonner sur le nom seul sans domaine.
- Supprimer une ligne : on marque `exclu = oui` et on la journalise.
- Fusionner deux personnes parce qu'elles ont le même titre dans la même entreprise.
- Compter "customer" du cycle de vie comme client.
- Écraser un `email_statut = valide` récent par une valeur non vérifiée d'une autre source.
