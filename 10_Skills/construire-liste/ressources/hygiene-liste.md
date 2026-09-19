# Hygiène d'une liste

Lu par `nettoyer-verifier`, et par `sourcer-personnes` avant de relancer un enrichissement. Une base B2B perd environ 2 % de ses emails par mois, 22 à 30 % par an ; les intitulés de poste bougent encore plus vite, 30 à 35 % par an. Une liste de six mois contient donc 11 à 15 % d'adresses mortes. Envoyer dessus coûte la réputation du domaine, et une réputation se répare en semaines.

## Statuts d'email et actions

Le verbe `trouver_email` renvoie un statut par adresse dans `email_statut`. Valeurs et conduite à tenir :

| `email_statut` | Ce que ça veut dire | Action |
|---|---|---|
| `valide` | le serveur confirme que la boîte existe | envoyer |
| `catch-all` | le domaine accepte tout, la boîte n'est pas confirmée | envoyer par petits lots (au plus 20 % d'un envoi), surveiller le bounce, préférer LinkedIn ou le téléphone si possible |
| `invalide` | la boîte n'existe pas | ne jamais envoyer, vider `email`, tenter `trouver_email` une fois avec le `linkedin_url` |
| `inconnu` | le serveur n'a pas répondu | traiter comme catch-all, re-vérifier dans 7 jours |
| `jetable` | adresse temporaire | exclure |
| `generique` | contact@, info@, bonjour@, rh@ | exclure d'une séquence email B2B ; garder pour une entreprise locale sans autre adresse, et passer par le téléphone |
| vide | rien trouvé | la ligne reste, sans email ; canal LinkedIn ou téléphone |

## Seuils à surveiller

| Mesure | Cible | Alerte | Ce qu'on fait |
|---|---|---|---|
| Taux de bounce | sous 1 % | au-dessus de 3 % | on arrête l'envoi, on re-vérifie toute la liste, on retire invalides et inconnus, on cherche la source qui a produit les bounces |
| Plaintes spam | sous 0,1 % | au-dessus de 0,3 % | on relit le ciblage et le message |
| Désabonnements | 0,3 à 0,5 % | au-dessus de 1 % | ciblage trop large |
| Couverture email | 70 % des lignes | sous 50 % | on vérifie la qualité des noms et des domaines avant de relancer un enrichissement |

## Calendrier

| Quand | Quoi |
|---|---|
| Avant chaque envoi | vérifier 100 % des adresses de la liste, sans exception |
| Chaque semaine | retirer les bounces durs de toutes les listes, les ajouter à la liste de suppression |
| Chaque mois | re-vérifier les `catch-all` et `inconnu` |
| Chaque trimestre | re-vérifier tout, rafraîchir `titre` et `entreprise` sur les lignes de plus de 90 jours, retirer les contacts sans réaction depuis 90 jours |
| Chaque semestre | ré-enrichir depuis LinkedIn, relire l'ICP avec ce qui a signé |

Règle simple : une liste dont `date_extraction` a plus de 30 jours repasse par `trouver_email` avant tout envoi.

## Quand ré-enrichir, et la règle "ne relance que si vide"

Un enrichissement coûte. On ne relance un verbe sur une ligne que si la cellule visée est vide :

| Cellule | On relance si | On ne relance pas si |
|---|---|---|
| `email` | vide, ou `email_statut = invalide` | `valide` ou `catch-all` de moins de 30 jours |
| `email_statut` | vide, ou `date_extraction` de plus de 30 jours | statut daté de moins de 30 jours |
| `telephone` | vide, et la ligne est en tier A, et le canal téléphone est dans `05_Departements/Go-to-Market/contexte.md` | déjà renseigné |
| `titre`, `entreprise` | vides, ou `date_extraction` de plus de 90 jours | renseignés et récents |
| `effectif`, `secteur` | vides et la ligne a passé les portes 0 à 5 | renseignés, ou ligne exclue |

Ordre d'entrée le moins cher d'abord : prénom + nom + domaine avant le `linkedin_url`. On s'arrête au premier résultat. On teste sur 50 lignes, on lit le taux de trouvés, et on lance le reste seulement s'il dépasse 50 %.

## Bounces

Un bounce doux (boîte pleine, serveur indisponible) se retente trois fois, à 4 heures, 24 heures et 48 heures ; s'il persiste, il devient dur. Un bounce dur sort de la campagne le jour même, entre dans la liste de suppression, et fait remonter sa `source` dans le rapport : une source qui produit plus de 3 % de bounces se remplace.

## Normaliser les colonnes texte

À faire avant toute qualification et tout enrichissement : une ligne propre matche mieux, et un `prenom` avec un emoji finit dans le message.

| Colonne | Règle |
|---|---|
| `prenom`, `nom` | retirer emojis, symboles, idéogrammes accolés, certifications ("Adm.A.", "MBA"), titres ("Dr", "Me", "Maître", "Mme") ; tout en majuscules ou tout en minuscules devient Prénom Nom ; garder accents, tirets et apostrophes ("Jean-Pierre", "O'Brien") ; garder "de", "du", "van", "von" en minuscule |
| `entreprise` | retirer les suffixes juridiques (SARL, SAS, SASU, SA, EURL, SCI, SCOP, Ltd, LLC, Inc, GmbH, BV, Srl) ; couper tout ce qui suit un séparateur décoratif (barre verticale, point médian, puce, emoji) ; garder tel quel un acronyme de trois lettres ou moins (IBM, HEC, BNP) et un nom à casse volontaire (iZiCard) |
| `titre` | retirer les emojis ; ne garder que le premier segment avant une barre verticale ou un point médian ; garder les acronymes (CEO, DRH, DAF) |
| `domaine` | minuscules, sans protocole, sans "www.", sans chemin : `exemple.fr` |
| `linkedin_url` | minuscules, sans paramètres après `?`, sans barre finale, préfixe `https://linkedin.com/in/` |
| `email` | minuscules, sans espace |
| `telephone` | format international sans espace, `+33612345678` |
| `effectif` | un entier ; une fourchette "11-50" garde la borne basse dans `effectif` |

Un nom d'entreprise qui contient un chiffre utile ("365 Media") le garde. "Tandem" et "Tandem SAS" ne se dédoublonnent pas ici ; la normalisation rend le match trivial pour `dedoublonner-liste`.

## Ce qu'on ne fait pas

- Envoyer sur une liste dont une seule adresse n'a pas de statut.
- Garder un `invalide` "au cas où".
- Confondre vérification et enrichissement : vérifier confirme une adresse qu'on a, enrichir en cherche une qu'on n'a pas. Les deux passent par `trouver_email`, avec des lignes différentes.
- Re-vérifier chaque semaine une liste qu'on n'utilise pas : la vérification se fait avant l'envoi, pas avant le stockage.
