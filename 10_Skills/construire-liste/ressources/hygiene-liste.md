# Hygiène d'une liste

Lu par `nettoyer-verifier`, et par `sourcer-personnes` avant de relancer un enrichissement. Une base B2B perd environ 2 % de ses emails par mois, 22 à 30 % par an ; les intitulés de poste bougent encore plus vite, 30 à 35 % par an. Une liste de six mois contient donc 11 à 15 % d'adresses mortes. Envoyer dessus coûte la réputation du domaine, et une réputation se répare en semaines.

## Statuts d'email et actions

Le verbe `trouver_email` écrit dans `email_statut` le statut FullEnrich de chaque adresse qu'il trouve. Il n'y a pas de vérification d'une adresse existante : FullEnrich ne vérifie que les emails qu'il trouve. Une adresse importée sans statut est non vérifiée ; on la re-cherche avec `trouver_email --force` (1 crédit si trouvé, le statut FullEnrich remplace), ou elle ne part qu'avec `--sans-verification` (déconseillé). Valeurs et conduite à tenir :

| `email_statut` | Ce que ça veut dire | Action |
|---|---|---|
| `DELIVERABLE` | la boîte existe, bounce autour de 2 % | envoyer |
| `HIGH_PROBABILITY` | très probablement valide, bounce autour de 9 % | envoyer |
| `CATCH_ALL` | le domaine accepte tout, la boîte n'est pas confirmée | envoyer par petits lots (`CATCH_ALL` et `UNKNOWN` ensemble au plus 20 % d'un envoi), surveiller le bounce, préférer LinkedIn ou le téléphone si possible |
| `UNKNOWN` | le serveur n'a pas répondu | traiter comme `CATCH_ALL` |
| `INVALID`, `INVALID_DOMAIN` | la boîte ou le domaine n'existe pas | ne jamais envoyer, vider `email` ; `trouver_email` les re-cherche une fois sans `--force`, avec le `linkedin_url` s'il est là |
| `NOT_FOUND` | FullEnrich n'a rien trouvé, pas facturé | la ligne reste, sans email ; canal LinkedIn ou téléphone |
| vide | non vérifié : adresse importée d'une autre source, jamais passée par FullEnrich | ne pas envoyer ; re-chercher avec `--force`, ou `--sans-verification` en le disant |

Une adresse générique (contact@, info@, bonjour@, rh@) n'est pas un statut : elle se repère à la main, s'exclut d'une séquence email B2B, et se garde pour une entreprise locale sans autre adresse, où on passe par le téléphone.

## Seuils à surveiller

| Mesure | Cible | Alerte | Ce qu'on fait |
|---|---|---|---|
| Taux de bounce | sous 1 % | au-dessus de 3 % | on arrête l'envoi, on re-cherche avec `trouver_email --force` les adresses sans statut ou anciennes, on retire les `INVALID` et on isole les `CATCH_ALL` et `UNKNOWN`, on cherche la source qui a produit les bounces |
| Plaintes spam | sous 0,1 % | au-dessus de 0,3 % | on relit le ciblage et le message |
| Désabonnements | 0,3 à 0,5 % | au-dessus de 1 % | ciblage trop large |
| Couverture email | 70 % des lignes | sous 50 % | on vérifie la qualité des noms et des domaines avant de relancer un enrichissement |

## Calendrier

| Quand | Quoi |
|---|---|
| Avant chaque envoi | chaque adresse qui part a un `email_statut` envoyable ; les adresses sans statut ne partent pas (sauf `--sans-verification`, déconseillé) |
| Chaque semaine | retirer les bounces durs de toutes les listes, les marquer `ne_plus_contacter = oui` |
| Chaque mois | re-chercher (`trouver_email --force`) les `CATCH_ALL` et `UNKNOWN` |
| Chaque trimestre | re-chercher tout ce qui a un statut de plus de 90 jours, rafraîchir `titre` et `entreprise` sur les lignes de plus de 90 jours, marquer `ne_plus_contacter = oui` les contacts sans réaction depuis 90 jours (règle manuelle, aucun script ne le fait) |
| Chaque semestre | ré-enrichir depuis LinkedIn, relire l'ICP avec ce qui a signé |

Règle simple : une liste dont `date_extraction` a plus de 30 jours repasse par `trouver_email --force` avant tout envoi.

## Quand ré-enrichir, et la règle "ne relance que si vide"

Un enrichissement coûte. On ne relance un verbe sur une ligne que si la cellule visée est vide :

| Cellule | On relance si | On ne relance pas si |
|---|---|---|
| `email` | vide, ou `email_statut` en `INVALID` ou `INVALID_DOMAIN` (le script les reprend sans `--force`) | `DELIVERABLE`, `HIGH_PROBABILITY` ou `CATCH_ALL` de moins de 30 jours |
| `email_statut` | vide avec un `email` rempli (adresse importée), ou `date_extraction` de plus de 30 jours : `trouver_email --force` | statut daté de moins de 30 jours |
| `telephone` | vide, et la ligne est en tier A, et le canal téléphone est dans `05_Departements/Go-to-Market/contexte.md` | déjà renseigné |
| `titre`, `entreprise` | vides, ou `date_extraction` de plus de 90 jours | renseignés et récents |
| `effectif`, `secteur` | vides et la ligne a passé les portes 0 à 5 | renseignés, ou ligne exclue |

Ordre d'entrée le moins cher d'abord : prénom + nom + domaine avant le `linkedin_url`. On s'arrête au premier résultat. On teste sur 50 lignes, on lit le taux de trouvés, et on lance le reste seulement s'il dépasse 50 %.

## Bounces

Un bounce doux (boîte pleine, serveur indisponible) se retente trois fois, à 4 heures, 24 heures et 48 heures ; s'il persiste, il devient dur. Un bounce dur sort de la campagne le jour même, est marqué `ne_plus_contacter = oui`, et fait remonter sa `source` dans le rapport : une source qui produit plus de 3 % de bounces se remplace.

## Normaliser les colonnes texte

À faire avant toute qualification et tout enrichissement : une ligne propre matche mieux, et un `prenom` avec un emoji finit dans le message.

| Colonne | Règle |
|---|---|
| `prenom`, `nom` | retirer emojis, symboles, idéogrammes accolés, certifications ("Adm.A.", "MBA"), titres ("Dr", "Me", "Maître", "Mme") ; tout en majuscules ou tout en minuscules devient Prénom Nom ; garder accents, tirets et apostrophes ("Jean-Pierre", "O'Brien") ; garder "de", "du", "van", "von" en minuscule |
| `entreprise` | retirer les suffixes juridiques (SARL, SAS, SASU, SA, EURL, SCI, SCOP, Ltd, LLC, Inc, GmbH, BV, Srl) ; couper tout ce qui suit un séparateur décoratif (barre verticale, point médian, puce, emoji) ; garder tel quel un acronyme de trois lettres ou moins (IBM, HEC, BNP) et un nom à casse volontaire (iZiCard) |
| `titre` | retirer les emojis ; ne garder que le premier segment avant une barre verticale ou un point médian ; garder les acronymes (CEO, DRH, DAF) |
| `domaine` | minuscules, sans protocole, sans "www.", sans chemin : `exemple.fr` |
| `linkedin_url` | `https://www.linkedin.com/in/<slug>` : minuscules, avec `www.`, sans paramètres après `?`, sans barre finale |
| `email` | minuscules, sans espace |
| `telephone` | format international sans espace, `+33612345678` |
| `effectif` | un entier ; une fourchette "11-50" garde la borne basse dans `effectif` |

Un nom d'entreprise qui contient un chiffre utile ("365 Media") le garde. "Tandem" et "Tandem SAS" ne se dédoublonnent pas ici ; la normalisation rend le match trivial pour `dedoublonner-liste`.

## Ce qu'on ne fait pas

- Envoyer sur une adresse sans `email_statut` envoyable, ou promettre une liste "100 % vérifiée".
- Garder un `INVALID` "au cas où".
- Croire qu'une adresse importée est vérifiée : FullEnrich ne vérifie que les emails qu'il trouve. Une adresse sans statut se re-cherche avec `trouver_email --force`, ou reste non vérifiée.
- Re-vérifier chaque semaine une liste qu'on n'utilise pas : la vérification se fait avant l'envoi, pas avant le stockage.
