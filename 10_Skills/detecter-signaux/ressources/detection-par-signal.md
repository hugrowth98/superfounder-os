# Détection par signal : les 30 déclencheurs principaux

> Lu par les sous-skills pour savoir quel verbe lancer, avec quel actor, à quel coût. Les coûts sont ceux affichés par les actors Apify au moment de l'écriture (tarif à l'unité, hors abonnement Apify) ; "inclus" veut dire couvert par votre abonnement Unipile, dans la limite des quotas LinkedIn. Les points renvoient à `bareme-signaux.md`, les fenêtres à `fenetres-fraicheur.md`.

## 1. Financement

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 1 | Levée Série A et plus | detecter_signal | `signalbase/signalbase-api`, `signalType: funding`, `round: Series A,Series B,Series C` | 0,04 $ par résultat | semaines 2 à 8 (Série C et plus : semaines 5 à 12) | 35 à 45 |
| 2 | Tour d'amorçage (Pre-seed, Seed) | detecter_signal | idem, `round: Pre-Seed,Seed` | 0,04 $ par résultat | semaines 2 à 4 | 20 |
| 3 | Introduction en bourse | detecter_signal | idem, `round: IPO` | 0,04 $ par résultat | j30 à j60 | 50 |
| 4 | Rachat, fusion | detecter_signal | `signalType: acquisitions` | 0,04 $ par résultat | semaines 2 à 6 | 35 à 40 |
| 5 | Palier de chiffre d'affaires annoncé | à la main | posts de la page entreprise (`enrichir-entreprise --posts`, colonne `posts_recents`) | inclus | j30 à j60 | 15 |

## 2. Équipe et postes

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 6 | Nouveau dirigeant dans un compte cible | detecter_signal | `signalType: job-changes`, `companyLinkedinUrl` ou `seniorities` + `countries: FR` | 0,04 $ par résultat | j14 à j45 | 40 (proposé) |
| 7 | Champion qui change de poste | detecter_signal | `--type job-changes --liste-suivie <csv des champions> --par-cible` (une requête exacte par `linkedin_url`) | 0,04 $ par résultat | j0 à j14 | 75 |
| 8 | Vague de recrutement (5 postes ou plus) | scraper_offres_emploi | `--source signalbase` (`--pays`, `--departements`, `--taille-equipe`, `--periode`), agrégat `_par-entreprise.csv` (`vague_recrutement`) | 0,04 $ par résultat | j14 à j30 | 40 |
| 9 | Recrutement de commerciaux (SDR, business developer, directeur commercial) | scraper_offres_emploi | `tagadanar/linkedin-jobs-scraper` (`keywords`, `location`, `postedSince`) ; `borderline/indeed-scraper` pour les PME et les postes non cadres | 0,0018 $ par offre LinkedIn (0,0036 $ avec `--details`), 0,005 $ par offre Indeed | j14 à j30 | 40 |
| 10 | Expansion d'un service (effectif qui grimpe) | enrichir_entreprise, puis trouver_personnes | colonne `effectif` à comparer entre deux runs d'`enrichir-entreprise`, Sales Nav pour compter les têtes par fonction | inclus | j30 à j90 | 40 |

## 3. Technologie et présence en ligne

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 11 | Adoption d'une techno visible sur le site | detecter_techno | `scrapemint/website-tech-stack-detector`, comparaison avec le mois précédent | 0,01 $ par site | j0 à j30 | 35 (adjacent), 20 (concurrent) |
| 12 | Retrait d'une techno | detecter_techno | idem, ligne disparue entre deux relevés | 0,01 $ par site | j0 à j30 | 45 si c'est un concurrent |
| 13 | Migration d'outil annoncée dans une offre d'emploi | scraper_offres_emploi | `tagadanar/linkedin-jobs-scraper` avec le nom de l'outil en `keywords`, `scrapeDetails: true` | 0,0036 $ par offre détaillée | j0 à j30 | 30 |
| 14 | Refonte du site | detecter_techno | changement de CMS ou de framework entre deux relevés, vérifié à l'œil | 0,01 $ par site | j30 à j60 | 15 |
| 15 | Pubs Meta ou LinkedIn actives | scraper_pubs | `curious_coder/facebook-ads-library-scraper` (Meta) ; LinkedIn via le skill `enrichir-entreprise --pubs` | 0,00075 $ par pub Meta | tant que la pub tourne | 15 |

## 4. Concurrence et fournisseurs

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 16 | Avis négatif sur un concurrent | à la main, puis trouver_personnes | lecture des comparateurs de logiciels de votre catégorie, une fois par mois ; auteur retrouvé par Sales Nav quand il est identifiable | inclus | j0 à j60 | 50 |
| 17 | Fin de contrat annuel chez un concurrent | à la main | date de signature connue (avis daté, annonce, échange), renouvellement 12 mois plus tard | 0 | j60 à j90 avant l'échéance | 45 |
| 18 | Client d'un concurrent | detecter_techno, scraper_offres_emploi | outil du concurrent détecté sur le site, ou demandé dans une offre d'emploi ; page clients du concurrent lue à la main chaque trimestre | 0,01 $ par site | permanent, à activer au renouvellement | 20 |
| 19 | Engagement avec les posts d'un concurrent ou de ses salariés | scraper_engagement | Unipile `posts/{id}/reactions` et `/comments` ; secours `harvestapi/linkedin-post-comments` | inclus ; secours 0,002 $ par commentaire | j0 à j7 | 25 |
| 20 | Abonné d'un concurrent | non listable | les abonnés d'une page ne s'exportent pas : passez par les engageurs (#19), même population, plus chaude | | | 15 |

## 5. Événements d'entreprise

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 21 | Nouveau bureau, nouvelle ville | detecter_signal, scraper_offres_emploi | `signalType: hiring` avec `city`, ou offres filtrées par `location` : des postes ouverts dans une ville où l'entreprise n'était pas | 0,04 $ ou 0,0018 $ | semaines 2 à 4 | 25 |
| 22 | Déménagement du siège | à la main | page entreprise (adresse), posts | inclus | semaines 2 à 4 | 20 |
| 23 | Lancement de produit ou de fonctionnalité | à la main | 5 derniers posts de la page (`enrichir-entreprise --posts`, colonne `posts_recents`) | inclus | semaines 1 à 2 | 30 |
| 24 | Partenariat annoncé | à la main | `enrichir-entreprise --posts` pour la page, `enrichir-personne --posts` pour les dirigeants | inclus | j14 à j60 | 15 |
| 25 | Changement réglementaire qui touche le secteur | à la main | votre veille sectorielle | 0 | j0 à j60 | 15 |

## 6. Marketing et réputation

| # | Signal | Verbe | Outil de la stack | Coût indicatif | Fenêtre | Points |
|---|---|---|---|---|---|---|
| 26 | Like ou commentaire sur un de vos posts | scraper_engagement | Unipile `posts/{id}/reactions` et `/comments` | inclus | j0 à j7 | 25 like, 35 commentaire |
| 27 | Participation à un salon ou à un événement | scraper_engagement, à la main | engageurs des posts de l'événement, liste des exposants et intervenants | inclus | j-7 à j+7 | 25 |
| 28 | Prix, récompense, classement | à la main | posts de la page entreprise | inclus | j14 à j30 | 15 |
| 29 | Mention presse | à la main | votre veille | 0 | j7 à j30 | 15 |
| 30 | Changement de sujet dans le contenu de l'entreprise | à la main | `posts_recents` (`enrichir-entreprise --posts`), comparés au trimestre précédent | inclus | j30 à j60 | 15 |

## Fiabilité d'un signal pris seul

| Tier | Signaux | Ce que ça veut dire | Délai |
|---|---|---|---|
| 1, intention la plus forte | levée Série A et plus, expansion dans une nouvelle région, changement de dirigeant dans le service qui achète | le budget est approuvé ou sur le point de l'être | le jour même (dans la fenêtre) |
| 2, intention forte | adoption ou retrait de la techno d'un concurrent, partenariat ou rachat, vague de 5 postes ou plus | l'investissement est en cours | 30 à 90 jours |
| 3, intention modérée | 1 à 3 offres d'emploi, prix, lancement de produit | de l'activité, sans urgence | séquence de nurture |
| 4, intention faible | activité sociale, mention presse, pic de trafic | du contexte, pas un déclencheur seul | à empiler avec un autre signal |

Un like seul est un contexte (tier 4) même s'il vaut 25 points : c'est l'empilement qui en fait un déclencheur.

## D'où vient la donnée

| Partie | Force | Sources dans la stack |
|---|---|---|
| Vos propres données | la plus forte | HubSpot (demandes, deals perdus, anciens clients), Lemlist (réponses), vos formulaires et listes d'inscrits |
| Données de vos relations | forte | engagement LinkedIn (Unipile), intros, comparateurs d'avis lus à la main |
| Données publiques | modérée à forte | Apify (levées, rachats, postes, offres, techno, pubs), Crustdata et Ocean.io (firmographique, lookalikes) |

## Règle de coût

Détectez d'abord avec ce qui est inclus (Unipile) ou quasi gratuit (offres d'emploi à 0,0018 $, techno à 0,01 $). Réservez detecter_signal à 0,04 $ par résultat à des filtres serrés : `countries: FR`, une tranche d'effectif, `date_preset: last_7d` en cadence hebdomadaire. Un run de 200 résultats coûte 8 $ : fixez toujours `limit` et une date pour ne pas payer des signaux que vous n'exploiterez pas. Mesurez le coût par rendez-vous obtenu, pas par signal détecté.
