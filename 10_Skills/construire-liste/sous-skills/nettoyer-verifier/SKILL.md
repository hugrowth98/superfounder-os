---
name: nettoyer-verifier
description: >
  Rend une liste envoyable : normalisation des colonnes (prénoms, noms, entreprises,
  titres, domaines, URL), lecture de `email_statut` sur chaque email et re-recherche des
  adresses importées sans statut, traitement des catch-all et des adresses génériques,
  calendrier d'hygiène. Se déclenche sur : "vérifie
  les emails", "taux de bounce", "catch-all", "nettoie ma liste", "normalise", "emojis
  dans les prénoms", "SARL dans les noms d'entreprise", "ma liste a plus d'un mois",
  "prête à envoyer ?". Ne pas utiliser pour retirer des doublons (voir
  `dedoublonner-liste`), pour trouver des emails manquants sur une liste sans email
  (voir `sourcer-personnes`), ni pour scorer (voir `qualifier-comptes`).
---

Une base B2B perd environ 2 % de ses emails par mois : une liste de six mois envoie 11 à 15 % de ses messages dans le vide, et au-delà de 3 % de bounce le domaine d'envoi se fait classer en spam. Un email cherché par FullEnrich arrive avec son statut, pour 1 crédit s'il est trouvé ; une réputation de domaine abîmée se répare en plusieurs semaines.

## Ressources

- `{SKILL_BASE}/ressources/hygiene-liste.md` : statuts et actions, seuils, calendrier, règle "ne relance que si vide", normalisation colonne par colonne.
- `{SKILL_BASE}/ressources/conseils-list-building.md` : la liste de contrôle avant remise à `cold-email`.

## Méthode

1. Lisez le fichier, comptez les lignes, repérez les colonnes. Renommez les colonnes de la source vers les noms de `docs/conventions-gtm.md` section 8 (`firstName` devient `prenom`, `companyName` devient `entreprise`, `jobTitle` devient `titre`). Conservez les colonnes de la source que vous ne savez pas mapper, après les colonnes normalisées.
2. Normalisez le texte, colonne par colonne, selon `hygiene-liste.md` : emojis et symboles hors des prénoms et noms, casse Prénom Nom, suffixes juridiques hors des entreprises, segment après une barre verticale hors des titres, domaines nus, URL LinkedIn sans paramètres, téléphones en international. Montrez 10 lignes avant et après, attendez le oui si plus de 20 % des lignes changent.
3. Séparez les lignes selon `email` : vide (rien à faire ici : canal LinkedIn ou téléphone, ou `trouver_email` via `sourcer-personnes`), rempli sans `email_statut` (adresse importée, non vérifiée), rempli avec un statut de moins de 30 jours (rien à faire), rempli avec un statut de plus de 30 jours ou `date_extraction` de plus de 30 jours (à re-chercher).
4. Il n'existe pas de vérification d'une adresse existante : FullEnrich ne vérifie que les emails qu'il trouve. Sur les lignes sans statut ou au statut de plus de 30 jours, relancez `trouver_email` avec `--force` (1 crédit par email trouvé, le statut FullEnrich remplace l'adresse importée). Une ligne où rien n'est trouvé reste non vérifiée : elle ne part qu'avec `--sans-verification`, déconseillé. Annoncez le coût, lancez sur 50 lignes, montrez la répartition, puis le reste.
5. Appliquez les actions : `INVALID` et `INVALID_DOMAIN` sont re-cherchés par `trouver_email` sans `--force` (une seule fois, avec `linkedin_url` si présent) et, si rien ne revient, `email` est vidé ; `NOT_FOUND` reste sans email ; une adresse générique (contact@, info@, rh@, ce n'est pas un statut, elle se repère à la main) exclut d'une séquence email, sauf entreprise locale sans autre adresse, où la ligne reste pour le téléphone ; `CATCH_ALL` et `UNKNOWN` restent, marqués, à envoyer par petits lots.
6. Calculez le bounce attendu : part des `CATCH_ALL` et `UNKNOWN` dans la liste. Au-dessus de 20 %, proposez de basculer ces lignes sur LinkedIn ou de les envoyer dans un lot séparé.
7. Rendez le rapport : lignes traitées, champs modifiés par colonne, répartition des statuts, couverture email (part des lignes en `DELIVERABLE` ou `HIGH_PROBABILITY`), lignes sans statut, lignes exclues et pourquoi, date de la prochaine vérification. Next step : `dedoublonner-liste` contre le CRM si ce n'est pas fait, sinon `cold-email`.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 1 et 2 | aucun, traitement local | interne | le CSV source | colonnes renommées et normalisées : `prenom`, `nom`, `titre`, `entreprise`, `domaine`, `linkedin_url`, `email`, `telephone` |
| 4 | `trouver_email` avec `--force` | `trouver-email` | `prenom`, `nom`, `domaine` ou `linkedin_url` des lignes sans statut ou au statut de plus de 30 jours | `email`, `email_statut` |
| 5 | `trouver_email` | `trouver-email` | `prenom`, `nom`, `domaine`, puis `linkedin_url`, lignes en `INVALID` ou `INVALID_DOMAIN` | `email`, `email_statut` |
| 5, tiers A sans email | `trouver_telephone` | `trouver-telephone` | `linkedin_url` | `telephone` |

Sortie : `trouver-email_<sujet>_<date>.csv`, toutes les lignes, `email_statut` renseigné sur chaque ligne passée par FullEnrich (vide = non vérifié), `exclu` et `raison_exclusion` sur les adresses génériques.

## Repères

| Repère | Valeur |
|---|---|
| Taux de bounce visé | sous 1 % |
| Seuil d'arrêt des envois | 3 % de bounce |
| Décroissance des emails | 22 à 30 % par an, environ 2 % par mois |
| Âge maximum d'un statut avant re-vérification | 30 jours |
| Part de `CATCH_ALL` et `UNKNOWN` tolérée dans un envoi | 20 % au plus, en lots séparés |
| Couverture email avant remise à `cold-email` | 70 % en `DELIVERABLE` ou `HIGH_PROBABILITY` |
| Bounce doux | 3 essais à 4 h, 24 h, 48 h, puis dur |
| Re-recherche (`--force`) des `CATCH_ALL` et `UNKNOWN` | chaque mois |
| Rafraîchissement des titres | chaque trimestre, ou au-delà de 90 jours |

## Template

```
Nettoyage et vérification : <fichier> (<n> lignes)
Colonnes renommées : <source -> normalisée>, ...
Champs modifiés : prenom <n>, nom <n>, entreprise <n>, titre <n>
Emails : vides <n>, sans statut ou statut > 30 j (re-cherchés avec --force) <n>, statut < 30 j <n>
Statuts : DELIVERABLE + HIGH_PROBABILITY <n> (<x %>), CATCH_ALL <n>, UNKNOWN <n>, INVALID + INVALID_DOMAIN <n> (vidés), NOT_FOUND <n>, sans statut <n> (non vérifiés), génériques <n> (exclus ou téléphone)
Couverture email envoyable : <x %>  Bounce attendu si envoi des CATCH_ALL et UNKNOWN : <x %>
Exclues : <n> (<raisons>)
Prochaine vérification : <date + 30 j>
Sortie : trouver-email_<sujet>_<date>.csv
```

## Règles

- Une adresse sans `email_statut` est non vérifiée : elle ne part pas, sauf `--sans-verification` (déconseillé). Le rapport dit combien de lignes sont dans ce cas ; on ne promet jamais une liste "100 % vérifiée".
- Une adresse `INVALID` ou `INVALID_DOMAIN` ne reste jamais dans `email`.
- Une adresse absente reste absente : aucun email construit à partir d'un format de domaine.
- On ne re-cherche pas un email dont le statut a moins de 30 jours, on n'enrichit pas une cellule remplie.
- La normalisation ne touche ni aux colonnes de données (dates, scores, statuts) ni aux URL au-delà du nettoyage indiqué.
- Une entreprise locale garde son adresse générique et sa ligne : le canal sera l'appel.
- Le rapport nomme la `source` qui a produit le plus d'`INVALID` : au-delà de 3 %, elle se remplace.

## Exemples

- "Ma liste est prête à envoyer ?" : comptage des lignes sans statut et des statuts de plus de 30 jours, re-recherche avec `--force` ; réponse attendue : couverture envoyable, bounce attendu, lignes restées sans statut, exclusions, et oui ou non avec ce qui manque.
- "Nettoie les prénoms, y'a des emojis partout" : normalisation des colonnes texte, 10 lignes avant et après ; réponse attendue : le CSV normalisé et le nombre de champs modifiés par colonne.
- "J'ai 4 % de bounce sur ma dernière campagne" : arrêt des envois, re-recherche avec `--force` des adresses sans statut ou anciennes, retrait des `INVALID`, lot séparé pour les `CATCH_ALL` et `UNKNOWN`, source fautive identifiée ; réponse attendue : la liste re-cherchée, le bounce attendu sous 1 %, et la source à remplacer.
