---
name: dedoublonner-liste
description: >
  Retire les doublons d'une liste, fusionne plusieurs sources en un fichier, et croise
  la liste avec le CRM pour écarter clients, affaires en cours et perdus récents. Clés
  dans l'ordre : linkedin_url, email, domaine + nom. Se déclenche sur : "dédoublonne",
  "doublons", "fusionne ces fichiers", "j'ai trois exports", "déjà dans HubSpot", "déjà
  contacté", "déjà client", "croise avec le CRM", "liste prospectable". Ne pas utiliser
  pour vérifier des emails (voir `nettoyer-verifier`), pour scorer (voir
  `qualifier-comptes`), ni pour importer dans le CRM (c'est une action séparée, sur
  validation).
---

Deux sources sur la même cible se recouvrent à 30 ou 60 % : sans dédoublonnage, la même personne reçoit deux séquences, chaque doublon coûte un enrichissement, et un client en cours reçoit un message froid. On dédoublonne avant d'enrichir, après avoir fusionné, et avant d'envoyer.

## Ressources

- `{SKILL_BASE}/ressources/regles-dedup.md` : clés et normalisation, priorité des sources par colonne, catégories CRM, liste de suppression, plafond par entreprise, journal des doublons.
- `{SKILL_BASE}/ressources/hygiene-liste.md` : la normalisation des colonnes qui rend les clés comparables.

## Méthode

1. Lisez chaque fichier, mappez ses colonnes vers `CONVENTIONS.md` section 8, comptez les lignes par fichier et par `source`.
2. Normalisez les clés : `linkedin_url` en minuscules sans paramètres ni barre finale, `email` en minuscules, `domaine` nu, `prenom` et `nom` sans accent ni majuscule, `entreprise` sans suffixe juridique.
3. Dédoublonnez les personnes : `linkedin_url` d'abord, puis `email`, puis `domaine` + `prenom` + `nom`. Les entreprises : `domaine`, puis `linkedin_entreprise_url`, puis `entreprise` normalisée. Un match sur `telephone` ou sur nom + titre + ville se montre à l'utilisateur avant de fusionner.
4. Fusionnez les colonnes des lignes en doublon : la valeur vérifiée la plus récente gagne, une cellule vide ne gagne jamais, LinkedIn gagne sur `titre` et `entreprise`, un `email_statut = valide` gagne sur tout autre email, `source` concatène. Si les lignes portent un `score_icp`, la plus haute reste et le fichier se rescore ensuite.
5. Croisez avec HubSpot si branché, par `email`, puis par URL LinkedIn si le CRM a la propriété, puis par `domaine` au niveau entreprise. Classez chaque match : client (affaire dans le pipeline clients, hors churn), affaire ouverte, churné, perdu depuis moins de 3 mois, perdu depuis plus de 3 mois, présent sans affaire, absent. Les quatre premières catégories sortent ; les autres restent, avec leur cycle de vie affiché. "Client" se définit par une affaire, jamais par le champ cycle de vie.
6. Croisez avec la liste de suppression : contactés dans les 90 jours, bounces durs, désabonnés, "pas intéressé".
7. Appliquez le plafond par entreprise : 5 contacts au plus par `domaine`, séniorité la plus haute puis fraîcheur, les autres marqués `exclu = oui`.
8. Écrivez le fichier fusionné et le journal des doublons, puis rendez le rapport : lignes par source, doublons par clé, catégories CRM, suppression, plafond, lignes gardées, points d'hygiène vus (emails de test, entreprises "Test", libellés en double par casse). Posez la question des "présents sans affaire, cycle de vie client" : on les exclut ou on les vérifie ? Next step : `qualifier-comptes` si le fichier n'a pas de `tier`, sinon `nettoyer-verifier`.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1 à 4 et 7 | `dedoublonner` (dans la liste) | `dedoublonner` | un ou plusieurs CSV avec `linkedin_url`, `email`, `domaine`, `prenom`, `nom`, `entreprise`, `source`, `date_extraction` | un CSV fusionné, `exclu`, `raison_exclusion = doublon` ou `= plafond par entreprise`, `source` concaténée |
| 5 | `dedoublonner` (contre le CRM, HubSpot) | `dedoublonner` | `email`, `linkedin_url`, `domaine` des lignes gardées | `exclu`, `raison_exclusion = deja client`, `= affaire en cours`, `= churne`, `= perdu recemment` ; catégorie CRM et cycle de vie dans le rapport |
| 6 | `dedoublonner` (liste de suppression) | `dedoublonner` | `email`, `linkedin_url` | `exclu`, `raison_exclusion = deja contacte`, `= bounce`, `= desabonne`, `= pas interesse` |

Sortie : `dedoublonner_<sujet>_<date>.csv` et `dedoublonner_<sujet>-doublons_<date>.csv` (journal). Si HubSpot n'est pas branché, l'étape 5 est sautée et le rapport le dit ; aucune catégorie CRM n'est devinée.

## Repères

| Repère | Valeur |
|---|---|
| Doublons attendus entre deux sources | 30 à 60 % |
| Clés personnes, dans l'ordre | `linkedin_url`, `email`, `domaine` + `prenom` + `nom` |
| Clés entreprises, dans l'ordre | `domaine`, `linkedin_entreprise_url`, `entreprise` normalisée |
| Perdu récent | moins de 3 mois depuis la date de fermeture, calculé à la date du jour |
| Fermé-perdu réapprochable | après 3 mois, signalé ; recommandé après 6 mois |
| Fenêtre "déjà contacté" | 90 jours |
| Plafond par entreprise | 5, dont 2 à 4 sur un tier A |
| Lots de recherche CRM | 200 emails par appel |

## Template

```
Dédoublonnage : <sujet>, <date>
Entrée : <n fichiers> (<source> <n>, <source> <n>) = <n> lignes
Doublons : linkedin_url <n>, email <n>, domaine + nom <n> = <n> retirés -> <n>
CRM (HubSpot, <n> affaires, <n> contacts lus) : client <n>, affaire ouverte <n>, churné <n>,
  perdu < 3 mois <n> (sortis) ; perdu > 3 mois <n>, présent sans affaire <n> (gardés, signalés)
Suppression : <n> retirés    Plafond par entreprise : <n> retirés
Gardées : <n> sur <n>    Journal : dedoublonner_<sujet>-doublons_<date>.csv
Hygiène : <emails de test>, <entreprises "Test">, <libellés en double>
Question : les <n> "présent sans affaire, cycle de vie client", on exclut ou on vérifie ?
```

## Règles

- Le dédoublonnage passe avant tout enrichissement et avant tout envoi.
- Aucune ligne supprimée : `exclu = oui`, une raison, une ligne dans le journal.
- Jamais de fusion sur le nom seul sans domaine, ni sur le titre.
- "Client" = une affaire dans le pipeline clients. Le cycle de vie s'affiche, il ne décide pas.
- Une cellule remplie n'est écrasée que par une valeur plus récente et vérifiée.
- Les identifiants de pipelines et d'étapes HubSpot se relisent à chaque run : ils changent.
- Le garde-fou "ne pas recontacter" de l'outil d'envoi est un filet, jamais la méthode.
- Aucune écriture dans HubSpot pendant un dédoublonnage : on lit, on ne modifie pas.

## Exemples

- "J'ai trois exports, fusionne-les" : mapping des colonnes, normalisation, dédoublonnage par les trois clés, fusion des colonnes par priorité ; réponse attendue : un CSV, le décompte par source et par clé, le journal.
- "Qui dans cette liste est déjà dans mon CRM ?" : croisement HubSpot par email, classement par catégorie ; réponse attendue : le tableau des catégories, la liste prospectable, la question sur les "présents sans affaire".
- "Enlève les gens que j'ai déjà contactés" : croisement avec la liste de suppression sur 90 jours ; réponse attendue : les lignes marquées `deja contacte` avec la date du dernier contact, le reste prêt pour `nettoyer-verifier`.
