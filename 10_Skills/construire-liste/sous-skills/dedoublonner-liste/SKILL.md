---
name: dedoublonner-liste
description: >
  Retire les doublons d'une liste, fusionne plusieurs sources en un fichier, et croise
  la liste avec HubSpot (annotation ou exclusion) et avec les exports de clients gagnés
  et perdus, passés en fichiers de référence. Clés
  dans l'ordre : linkedin_url, email, domaine + nom. Se déclenche sur : "dédoublonne",
  "doublons", "fusionne ces fichiers", "j'ai trois exports", "déjà dans HubSpot", "déjà
  contacté", "déjà client", "croise avec le CRM", "liste prospectable". Ne pas utiliser
  pour vérifier des emails (voir `nettoyer-verifier`), pour scorer (voir
  `qualifier-comptes`), ni pour importer dans le CRM (c'est une action séparée, sur
  validation).
---

Deux sources sur la même cible se recouvrent à 30 ou 60 % : sans dédoublonnage, la même personne reçoit deux séquences, chaque doublon coûte un enrichissement, et un client en cours reçoit un message froid. On dédoublonne avant d'enrichir, après avoir fusionné, et avant d'envoyer.

## Ressources

- `{SKILL_BASE}/ressources/regles-dedup.md` : clés et normalisation, priorité des sources par colonne, croisement CRM, fichiers de référence (`--contre`), plafond par entreprise, journal des doublons.
- `{SKILL_BASE}/ressources/hygiene-liste.md` : la normalisation des colonnes qui rend les clés comparables.

## Méthode

1. Lisez chaque fichier, mappez ses colonnes vers `docs/conventions-gtm.md` section 8, comptez les lignes par fichier et par `source`.
2. Normalisez les clés : `linkedin_url` en `https://www.linkedin.com/in/<slug>` (minuscules, avec `www.`, sans paramètres ni barre finale), `email` en minuscules, `domaine` nu, `prenom` et `nom` sans accent ni majuscule, `entreprise` sans suffixe juridique.
3. Dédoublonnez les personnes : `linkedin_url` d'abord, puis `email`, puis `domaine` + `prenom` + `nom`. Les entreprises : `domaine`, puis `linkedin_entreprise_url`, puis `entreprise` normalisée. Un match sur `telephone` ou sur nom + titre + ville se montre à l'utilisateur avant de fusionner.
4. Fusionnez les colonnes des lignes en doublon : la valeur vérifiée la plus récente gagne, une cellule vide ne gagne jamais, LinkedIn gagne sur `titre` et `entreprise`, l'`email_statut` FullEnrich le plus fiable (`DELIVERABLE`, puis `HIGH_PROBABILITY`, puis `CATCH_ALL`) gagne sur tout autre email, `source` concatène avec `+`. Si les lignes portent un `score_icp`, la plus haute reste et le fichier se rescore ensuite.
5. Croisez avec HubSpot si branché (`--hubspot`, par `email`, puis par `domaine` au niveau entreprise) : chaque ligne reçoit `dans_crm`, `hubspot_contact_id`, `hubspot_entreprise_id` et `hubspot_lifecycle` ; `--exclure-crm` met `exclu = oui` sur ce qui est déjà dans HubSpot. Le script ne calcule aucune catégorie (client, affaire ouverte, churné, perdu) : les clients et les perdus s'exportent avec `crm lire --statut gagnes` et `crm lire --statut perdus` (les perdus de moins de 3 mois se filtrent sur `date_cloture`), et ces fichiers se passent en `--contre`. "Client" se définit par une affaire gagnée dans cet export, jamais par `hubspot_lifecycle`, qui s'affiche sans décider.
6. Croisez avec les fichiers de référence en `--contre` : le fichier `ne_plus_contacter` (bounces durs, désabonnés, "pas intéressé", `ne_plus_contacter = oui` écrit par `verifier-reponses`) et les dernières listes envoyées. Il n'y a pas de fenêtre de 90 jours automatique : la règle "pas recontacté avant 90 jours" se tient à la main, en passant les listes envoyées sur la période en `--contre`.
7. Appliquez le plafond par entreprise : `--max-par-entreprise 5` (valeur par défaut) garde 5 personnes au plus par `domaine`, meilleur `score_icp` puis ligne la plus remplie, et marque les autres `exclu = oui`, `raison_exclusion = plafond 5 par entreprise`, journalisées.
8. Écrivez le fichier fusionné et le journal des doublons, puis rendez le rapport : lignes par source, doublons par clé, lignes dans HubSpot, lignes dans les fichiers de référence, plafond, lignes gardées, points d'hygiène vus (emails de test, entreprises "Test", libellés en double par casse). Posez la question des lignes `dans_crm = oui` sans affaire : on les exclut (`--exclure-crm`) ou on les garde annotées ? Next step : `qualifier-comptes` si le fichier n'a pas de `tier`, sinon `trouver-email` sur les lignes sans adresse, puis `nettoyer-verifier`.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1 à 4 et 7 | `dedoublonner` (dans la liste, `--max-par-entreprise 5`) | `dedoublonner` | un ou plusieurs CSV avec `linkedin_url`, `email`, `domaine`, `prenom`, `nom`, `entreprise`, `source`, `date_extraction` | un CSV fusionné (les doublons fusionnent, une ligne par fusion dans le journal), `exclu`, `raison_exclusion = plafond 5 par entreprise`, `source` concaténée |
| 5 | `dedoublonner --hubspot` (`--exclure-crm` pour exclure) et `lire_crm` | `dedoublonner`, `crm` (`lire --statut gagnes`, puis `perdus`) | `email`, `domaine` des lignes gardées ; les exports CRM en `--contre` | `dans_crm`, `hubspot_contact_id`, `hubspot_entreprise_id`, `hubspot_lifecycle` ; `exclu`, `raison_exclusion = deja dans HubSpot (contact)` ou `(entreprise)`, `= deja dans crm_clients-gagnes_<date>.csv` |
| 6 | `dedoublonner --contre <fichier>` | `dedoublonner` | `linkedin_url`, `email`, `domaine` + `nom` | `exclu`, `raison_exclusion = deja dans <fichier>` |

Sortie : `dedoublonner_<sujet>_<date>.csv` et `dedoublonner_<sujet>_<date>_doublons.csv` (journal). Si HubSpot n'est pas branché, l'étape 5 se limite aux fichiers de référence et le rapport le dit ; rien n'est deviné.

## Repères

| Repère | Valeur |
|---|---|
| Doublons attendus entre deux sources | 30 à 60 % |
| Clés personnes, dans l'ordre | `linkedin_url`, `email`, `domaine` + `prenom` + `nom` |
| Clés entreprises, dans l'ordre | `domaine`, `linkedin_entreprise_url`, `entreprise` normalisée |
| Perdu récent | moins de 3 mois depuis `date_cloture` de l'export `crm lire --statut perdus`, à passer en `--contre` |
| Fermé-perdu réapprochable | après 3 mois, signalé ; recommandé après 6 mois |
| Fenêtre "déjà contacté" | 90 jours, tenue à la main : les listes envoyées sur la période passent en `--contre` |
| Plafond par entreprise | 5 (`--max-par-entreprise`), dont 2 à 4 sur un tier A, 1 à 2 sur un B, 1 sur un C |
| Lots de recherche HubSpot | 100 emails par appel, 90 domaines |

## Template

```
Dédoublonnage : <sujet>, <date>
Entrée : <n fichiers> (<source> <n>, <source> <n>) = <n> lignes
Doublons : linkedin_url <n>, email <n>, domaine + nom <n> = <n> fusionnés -> <n>
HubSpot (--hubspot) : dans_crm <n> (<annotés | exclus avec --exclure-crm>)
Référence (--contre) : clients gagnés <n>, perdus < 3 mois <n>, ne_plus_contacter <n>, listes envoyées <n> = <n> exclus
Plafond 5 par entreprise : <n> exclus
Gardées : <n> sur <n>    Journal : dedoublonner_<sujet>_<date>_doublons.csv
Hygiène : <emails de test>, <entreprises "Test">, <libellés en double>
Question : les <n> dans_crm = oui sans affaire, on exclut ou on garde annotés ?
```

## Règles

- Le dédoublonnage passe avant tout enrichissement et avant tout envoi.
- Aucune ligne perdue sans trace : un doublon fusionne et laisse une ligne dans le journal, une exclusion porte `exclu = oui` et sa raison.
- Jamais de fusion sur le nom seul sans domaine, ni sur le titre.
- "Client" = une affaire gagnée dans l'export `crm lire --statut gagnes`. `hubspot_lifecycle` s'affiche, il ne décide pas.
- Une cellule remplie n'est écrasée que par une valeur plus récente et vérifiée.
- Les identifiants de pipelines et d'étapes HubSpot se relisent à chaque run : ils changent.
- Le garde-fou "ne pas recontacter" de l'outil d'envoi est un filet, jamais la méthode.
- Aucune écriture dans HubSpot pendant un dédoublonnage : on lit, on ne modifie pas.

## Exemples

- "J'ai trois exports, fusionne-les" : mapping des colonnes, normalisation, dédoublonnage par les trois clés, fusion des colonnes par priorité ; réponse attendue : un CSV, le décompte par source et par clé, le journal.
- "Qui dans cette liste est déjà dans mon CRM ?" : `--hubspot` par email et domaine, `crm lire` pour les gagnés et les perdus en `--contre` ; réponse attendue : le nombre de `dans_crm`, les clients et perdus exclus, la liste prospectable, la question sur les `dans_crm` sans affaire.
- "Enlève les gens que j'ai déjà contactés" : `--contre` avec les listes envoyées des 90 derniers jours et le fichier `ne_plus_contacter` ; réponse attendue : les lignes marquées `deja dans <fichier>`, le reste prêt pour `trouver-email` puis `nettoyer-verifier`.
