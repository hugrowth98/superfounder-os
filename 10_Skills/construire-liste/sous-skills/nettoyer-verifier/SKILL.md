---
name: nettoyer-verifier
description: >
  Rend une liste envoyable : normalisation des colonnes (prénoms, noms, entreprises,
  titres, domaines, URL), vérification de chaque email avec un statut, traitement des
  catch-all et des adresses génériques, calendrier d'hygiène. Se déclenche sur : "vérifie
  les emails", "taux de bounce", "catch-all", "nettoie ma liste", "normalise", "emojis
  dans les prénoms", "SARL dans les noms d'entreprise", "ma liste a plus d'un mois",
  "prête à envoyer ?". Ne pas utiliser pour retirer des doublons (voir
  `dedoublonner-liste`), pour trouver des emails manquants sur une liste sans email
  (voir `sourcer-personnes`), ni pour scorer (voir `qualifier-comptes`).
---

Une base B2B perd environ 2 % de ses emails par mois : une liste de six mois envoie 11 à 15 % de ses messages dans le vide, et au-delà de 3 % de bounce le domaine d'envoi se fait classer en spam. Vérifier 100 % des adresses avant chaque envoi coûte quelques centimes par ligne ; une réputation de domaine abîmée se répare en plusieurs semaines.

## Ressources

- `{SKILL_BASE}/ressources/hygiene-liste.md` : statuts et actions, seuils, calendrier, règle "ne relance que si vide", normalisation colonne par colonne.
- `{SKILL_BASE}/ressources/conseils-list-building.md` : la liste de contrôle avant remise à `cold-email`.

## Méthode

1. Lisez le fichier, comptez les lignes, repérez les colonnes. Renommez les colonnes de la source vers les noms de `CONVENTIONS.md` section 8 (`firstName` devient `prenom`, `companyName` devient `entreprise`, `jobTitle` devient `titre`). Conservez les colonnes de la source que vous ne savez pas mapper, après les colonnes normalisées.
2. Normalisez le texte, colonne par colonne, selon `hygiene-liste.md` : emojis et symboles hors des prénoms et noms, casse Prénom Nom, suffixes juridiques hors des entreprises, segment après une barre verticale hors des titres, domaines nus, URL LinkedIn sans paramètres, téléphones en international. Montrez 10 lignes avant et après, attendez le oui si plus de 20 % des lignes changent.
3. Séparez les lignes selon `email` : vide (rien à vérifier, canal LinkedIn ou téléphone), rempli sans `email_statut`, rempli avec un statut de moins de 30 jours (rien à faire), rempli avec un statut de plus de 30 jours ou `date_extraction` de plus de 30 jours (à re-vérifier).
4. Vérifiez les lignes à vérifier avec `trouver_email` en mode statut : l'adresse existante est soumise, l'outil renvoie `valide`, `catch-all`, `invalide`, `inconnu`, `jetable`. Annoncez le coût, lancez sur 50 lignes, montrez la répartition, puis le reste.
5. Appliquez les actions : `invalide` vide `email` et tente une seule recherche avec `linkedin_url` si présent ; `jetable` exclut ; `generique` (contact@, info@) exclut d'une séquence email, sauf entreprise locale sans autre adresse, où la ligne reste pour le téléphone ; `catch-all` et `inconnu` restent, marqués, à envoyer par petits lots.
6. Calculez le bounce attendu : part des `catch-all` et `inconnu` dans la liste. Au-dessus de 20 %, proposez de basculer ces lignes sur LinkedIn ou de les envoyer dans un lot séparé.
7. Rendez le rapport : lignes traitées, champs modifiés par colonne, répartition des statuts, couverture email (part des lignes avec un `valide`), lignes exclues et pourquoi, date de la prochaine vérification. Next step : `dedoublonner-liste` contre le CRM si ce n'est pas fait, sinon `cold-email`.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1 et 2 | aucun, traitement local | interne | le CSV source | colonnes renommées et normalisées : `prenom`, `nom`, `titre`, `entreprise`, `domaine`, `linkedin_url`, `email`, `telephone` |
| 4 | `trouver_email` en mode statut | `trouver-email` | `email` des lignes à vérifier | `email_statut` |
| 5 | `trouver_email` | `trouver-email` | `prenom`, `nom`, `domaine`, puis `linkedin_url`, lignes passées `invalide` | `email`, `email_statut` |
| 5, tiers A sans email | `trouver_telephone` | `trouver-telephone` | `linkedin_url` | `telephone` |

Sortie : `trouver-email_<sujet>_<date>.csv`, toutes les lignes, `email_statut` renseigné sur chaque ligne qui a un `email`, `exclu` et `raison_exclusion` sur les jetables et les génériques.

## Repères

| Repère | Valeur |
|---|---|
| Taux de bounce visé | sous 1 % |
| Seuil d'arrêt des envois | 3 % de bounce |
| Décroissance des emails | 22 à 30 % par an, environ 2 % par mois |
| Âge maximum d'un statut avant re-vérification | 30 jours |
| Part de `catch-all` tolérée dans un envoi | 20 % au plus, en lots séparés |
| Couverture email avant remise à `cold-email` | 70 % de `valide` |
| Bounce doux | 3 essais à 4 h, 24 h, 48 h, puis dur |
| Re-vérification des catch-all | chaque mois |
| Rafraîchissement des titres | chaque trimestre, ou au-delà de 90 jours |

## Template

```
Nettoyage et vérification : <fichier> (<n> lignes)
Colonnes renommées : <source -> normalisée>, ...
Champs modifiés : prenom <n>, nom <n>, entreprise <n>, titre <n>
Emails : vides <n>, à vérifier <n>, déjà vérifiés < 30 j <n>
Statuts : valide <n> (<x %>), catch-all <n>, inconnu <n>, invalide <n> (vidés), jetable <n> (exclus), générique <n> (exclus ou téléphone)
Couverture email valide : <x %>  Bounce attendu si envoi des catch-all : <x %>
Exclues : <n> (<raisons>)
Prochaine vérification : <date + 30 j>
Sortie : trouver-email_<sujet>_<date>.csv
```

## Règles

- 100 % des adresses ont un `email_statut` avant toute remise à `cold-email`. Aucune exception, même sur une adresse "sûre".
- Une adresse `invalide` ne reste jamais dans `email`.
- Une adresse absente reste absente : aucun email construit à partir d'un format de domaine.
- On ne re-vérifie pas un statut de moins de 30 jours, on n'enrichit pas une cellule remplie.
- La normalisation ne touche ni aux colonnes de données (dates, scores, statuts) ni aux URL au-delà du nettoyage indiqué.
- Une entreprise locale garde son adresse générique et sa ligne : le canal sera l'appel.
- Le rapport nomme la `source` qui a produit le plus d'`invalide` : au-delà de 3 %, elle se remplace.

## Exemples

- "Ma liste est prête à envoyer ?" : comptage des lignes sans statut et des statuts de plus de 30 jours, vérification ; réponse attendue : couverture valide, bounce attendu, exclusions, et oui ou non avec ce qui manque.
- "Nettoie les prénoms, y'a des emojis partout" : normalisation des colonnes texte, 10 lignes avant et après ; réponse attendue : le CSV normalisé et le nombre de champs modifiés par colonne.
- "J'ai 4 % de bounce sur ma dernière campagne" : arrêt des envois, re-vérification complète, retrait des invalides et inconnus, source fautive identifiée ; réponse attendue : la liste re-vérifiée, le bounce attendu sous 1 %, et la source à remplacer.
