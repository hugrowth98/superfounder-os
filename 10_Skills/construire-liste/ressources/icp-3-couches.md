# L'ICP en trois couches et son score sur 100

Lu par `definir-icp`, `qualifier-comptes` et `selectionner-comptes`. Ce fichier décrit le cadre et la façon de lire la section 2 de `05_Departements/Go-to-Market/contexte.md`, "Client idéal (ICP) en 3 couches, scoring sur 100". Les valeurs propres à l'utilisateur (secteurs, effectifs, pondérations, seuils, exclusions) vivent dans `05_Departements/Go-to-Market/contexte.md` et nulle part ailleurs : aucun skill ne les contient en dur, et `installer-gtm` est le seul à les écrire.

## Pourquoi trois couches

Un ICP réduit à "PME B2B en France" donne une liste de dizaines de milliers d'entreprises et un taux de réponse de 1 à 2 %. Les entreprises qui matchent les trois couches convertissent 3 à 5 fois mieux que le reste du marché, ont un cycle de vente plus court et churnent moins. Les trois couches répondent à trois questions : à quoi ressemble l'entreprise (firmographique), avec quoi elle travaille (technographique), qu'est-ce qui se passe chez elle en ce moment (comportementale).

## Couche 1 : firmographique (40 points par défaut)

| Critère de `05_Departements/Go-to-Market/contexte.md` | Ce qu'on y écrit | Exemple | Exact | Adjacent | Sinon |
|---|---|---|---|---|---|
| Secteur | les 2 à 4 secteurs des meilleurs clients ; l'adjacent est un cran à côté | SaaS B2B, ESN, cabinets de conseil ; adjacent : agences digitales | 15 | 7 | 0 |
| Effectif | la fourchette où l'offre se vend le mieux ; l'adjacent est la tranche voisine | 11 à 50 ; adjacent : 1 à 10 et 51 à 200 | 10 | 5 | 0 |
| Zone géographique | pays, régions, villes ; l'adjacent est la zone secondaire | France ; adjacent : Belgique, Suisse | 8 | 4 | 0 |
| Stade ou chiffre d'affaires | si connu et discriminant, sinon vide | 1 à 10 M€, ou levée de moins de 18 mois | 7 | 3 | 0 |

## Couche 2 : technographique (20 points par défaut)

| Critère de `05_Departements/Go-to-Market/contexte.md` | Ce qu'on y écrit | Présent | Neutre | Sinon |
|---|---|---|---|---|
| Outil ou stack qui rend l'offre pertinente | les outils sur lesquels l'offre se branche, ou qui prouvent une maturité (un CRM, un site avec formulaire) | 12 | 6 | 0 |
| Outil concurrent en place | déjà équipé chez un concurrent : 3 points (il faut le faire changer) ; aucun concurrent visible : 8 | 3 | 8 | 8 |

Le verbe `detecter_techno` renseigne cette couche sur un domaine. Sans détection, la couche vaut 14 points (6 pour l'outil pertinent en neutre, 8 pour aucun concurrent visible) et la ligne reste dans la liste. Si l'offre ne dépend d'aucun outil, `05_Departements/Go-to-Market/contexte.md` met la couche à 0 et redistribue ses 20 points sur les couches 1 et 3.

## Couche 3 : comportementale (40 points par défaut)

| Critère de `05_Departements/Go-to-Market/contexte.md` | Points | D'où vient la donnée |
|---|---|---|
| Signal prioritaire n°1 de la section 4, daté de moins de 30 jours | 15 | `signal_type`, `signal_date` |
| Signal prioritaire n°2 à n°5, daté de moins de 60 jours | 10 | idem |
| Deux signaux ou plus qui s'empilent | 10 | `signal_type` avec plusieurs types séparés par `+` |
| Engagement direct avec l'utilisateur (visite de profil, commentaire, réponse passée, événement) | 5 | `signal_type = commentaire` ou `like`, ou le CRM |

Les fenêtres (30 et 60 jours) sont modifiables dans `05_Departements/Go-to-Market/contexte.md`. Ces signaux sont détectés par `detecter-signaux`, qui écrit aussi `score_signal` et `fraicheur`. Dans le score ICP, ils comptent quand le CSV les porte déjà. Signal absent = 0 point, jamais de point négatif : une entreprise sans signal connu plafonne à 60, tier B, et reste éligible ; le tier A demande un signal.

## Tiers et exclusions

| Tier | Score par défaut | Ce qu'on en fait |
|---|---|---|
| A | 75 à 100 | contact cette semaine, message écrit à la main, téléphone en priorité |
| B | 55 à 74 | séquence multicanal standard |
| C | 35 à 54 | nurturing, pas de téléphone |
| D | sous 35 | `exclu = oui`, `raison_exclusion = score <n> sous le seuil C (35)` |

Les quatre lignes d'exclusion de la section 2 court-circuitent le score : B2C (oui ou non), concurrents nommés, secteurs exclus, tailles exclues et autres bornes dures. La section 7 ajoute les exclusions propres à l'utilisateur : clients actuels et passés à ne jamais contacter, partenaires et apporteurs d'affaires, listes ou fichiers à croiser, zones exclues. Une ligne qui tombe dans l'une de ces exclusions sort avant d'être notée, ce qui évite de payer un enrichissement pour rien.

## Ce que les skills lisent, et où

| Donnée | Section de `05_Departements/Go-to-Market/contexte.md` | Skill qui la lit |
|---|---|---|
| Valeurs cibles et points des trois couches | 2, tables des couches | `qualifier-comptes`, `definir-icp` |
| Seuils A, B, C, D | 2, table des tiers | `qualifier-comptes`, `selectionner-comptes` |
| B2C, concurrents nommés, secteurs exclus, tailles exclues | 2, Exclusions | `qualifier-comptes`, portes 2 à 5 |
| Titres ATL et BTL, comité d'achat | 3 | `cartographier-personas`, `sourcer-personnes` |
| Les 5 signaux prioritaires et leur fraîcheur | 4 | couche 3 du score |
| Nouveaux prospects par semaine, rendez-vous visés | 5 | test de volume de `definir-icp`, master pour "combien de lignes" |
| Clients, partenaires, listes à croiser, zones exclues | 7 | porte 0, `dedoublonner-liste` |
| Mots-clés B2C ou concurrents propres au marché de l'utilisateur | aucune : ils vivent dans `05_Departements/Go-to-Market/Ciblage/mots-cles-exclusion.md`, le seul endroit | portes 4 et 5, en complément des listes de départ de `gates-qualification.md` |

Une valeur entre crochets dans la section 2 veut dire que l'OS n'est pas installé : `definir-icp` s'arrête et renvoie vers `installer-gtm`, sauf si l'utilisateur veut travailler son ICP maintenant.

## Format de la section 2, tel que `installer-gtm` la remplit

```
### Couche 1 : firmographique (40 points par défaut)
| Critère | Valeur cible | Points si exact | Points si adjacent | Sinon |
| Secteur | SaaS B2B, ESN, cabinets de conseil ; adjacent : agences digitales | 15 | 7 | 0 |
| Effectif | 11 à 50 ; adjacent : 1 à 10, 51 à 200 | 10 | 5 | 0 |
| Zone géographique | France ; adjacent : Belgique, Suisse | 8 | 4 | 0 |
| Stade ou chiffre d'affaires | 1 à 10 M€ | 7 | 3 | 0 |

### Couche 2 : technographique (20 points par défaut)
| Outil ou stack qui rend votre offre pertinente | HubSpot, Lemlist, un CRM quel qu'il soit | 12 | 6 | 0 |
| Outil concurrent en place | outil d'automatisation LinkedIn : 3 ; aucun : 8 | 3 | 8 | 8 |

### Couche 3 : comportementale (40 points par défaut)
signal n°1 < 30 jours : 15 / signaux n°2 à 5 < 60 jours : 10 / empilement : 10 / engagement direct : 5

### Tiers
A : 75 à 100 / B : 55 à 74 / C : 35 à 54 / D : sous 35

### Exclusions
B2C : oui / Concurrents : agences de prospection, coachs commerciaux, agences IA de service /
Secteurs exclus : retail, restauration, associations, secteur public / Tailles exclues : moins de 3, plus de 500
```

Les pondérations ci-dessus sont les valeurs par défaut. `installer-gtm` les ajuste avec l'utilisateur : ce qui distingue ses meilleurs clients pèse plus lourd, la somme reste à 100.

## Exemple noté

Utilisateur : coach en prospection pour dirigeants de PME B2B en France, offre à 1 200 € par mois, signal n°1 "recrute un commercial".

Entreprise évaluée : agence web de 24 salariés à Nantes, utilise HubSpot, a publié une offre de business developer il y a 12 jours.

| Critère | Constat | Points |
|---|---|---|
| Secteur | agence digitale, adjacent | 7 / 15 |
| Effectif | 24, exact | 10 / 10 |
| Zone | France | 8 / 8 |
| Stade ou CA | inconnu | 0 / 7 |
| Outil pertinent | HubSpot, présent | 12 / 12 |
| Outil concurrent | aucun visible | 8 / 8 |
| Signal n°1 | offre de business developer, 12 jours | 15 / 15 |
| Signaux 2 à 5, empilement, engagement direct | rien | 0 / 25 |
| Total | | 60, tier B |

Sans l'offre d'emploi, la même agence tombe à 45, tier C. Si en plus son dirigeant a commenté un post de l'utilisateur cette semaine (l'engagement contenu est son signal n°3), elle passe à 85, tier A (10 pour le second signal, 10 pour l'empilement, 5 pour l'engagement direct) : le signal fait la différence entre "un jour" et "cette semaine".

## Anti-ICP

Aussi utile que l'ICP : les clients qui ont churné vite, demandé beaucoup de support, négocié chaque euro. Leurs points communs deviennent des exclusions ou des critères à zéro point. Un ICP se relit tous les trimestres à partir de ce qui a signé et de ce qui a churné.
