# Les 6 signaux de cœur, classés par corrélation d'achat

> Lu par le master pour choisir quels signaux suivre en premier, et par chaque sous-skill pour sa phrase d'ouverture. Le classement va du signal qui prédit le mieux une signature à celui qui la prédit le moins. Le rang 1 vient avant tout le reste : commencez par vos anciens clients.

## 1. Anciens clients et anciens utilisateurs

- **Pourquoi ça marche** : la confiance est déjà là, la personne connaît votre méthode, la preuve de valeur arrive vite.
- **Où on le voit** : un ancien client, un ancien interlocuteur, un ancien utilisateur de votre offre arrive dans une nouvelle entreprise.
- **Détection** : detecter_signal (`signalbase/signalbase-api`, `--type job-changes --liste-suivie <csv des champions> --par-cible`), chaque jour.
- **Quand écrire** : le jour même, fenêtre j0 à j14, frais 30 jours.
- **Points** : 75 (Tier 1). Le premier fournisseur à écrire a 3 fois plus de chances de signer.
- **Sous-skill** : `changement-poste`, mode champions.

## 2. Nouveau dirigeant depuis moins de 90 jours

- **Pourquoi ça marche** : mandat de résultats rapides, période où changer de fournisseur ne se justifie pas, budget pas encore engagé. Il construit sa stack dans ses 90 premiers jours.
- **Où on le voit** : un directeur commercial, un directeur marketing, un CEO, un responsable d'équipe prend un poste dans un compte cible.
- **Détection** : detecter_signal (`signalType: job-changes`, filtres `countries`, `seniorities`, `departments`, `positions`, `date_preset`), chaque semaine.
- **Quand écrire** : jours 14 à 45 (pic), jusqu'à j90. Avant j14 il s'installe : trop tôt.
- **Points** : 40 (proposé). Taux de réponse 3 fois celui d'un contact à froid.
- **Sous-skill** : `changement-poste`.

## 3. Intention forte sur votre contenu

- **Pourquoi ça marche** : la personne vous connaît déjà. Un commentaire, une participation à un webinar, un abonnement à votre newsletter montrent une recherche en cours. Taux de réponse 25 à 30 %.
- **Où on le voit** : vos posts LinkedIn, vos webinars, vos emails, votre newsletter.
- **Détection** : scraper_engagement (`--mes-posts 5`, réactions et commentaires de vos posts), vos listes d'inscrits et l'export de votre outil d'emailing.
- **Quand écrire** : dans les 24 à 48 heures. Un commentaire vaut deux likes.
- **Points** : commentaire 35, like 25, webinar 25, abonnement à la newsletter 15.
- **Ce que ce master ne couvre pas** : les visiteurs anonymes de votre site (page tarifs, page démo), qui font partie de ce signal dans le classement d'origine et valent 50 à 80 points quand vous avez la donnée.
- **Sous-skill** : `engagement-contenu`.

## 4. Changement de stack technique

- **Pourquoi ça marche** : un projet de changement en cours prouve une ouverture aux nouveaux fournisseurs. La transition crée des trous dans les process, et des douleurs fraîches.
- **Où on le voit** : un outil disparaît ou apparaît sur le site du prospect ; une offre d'emploi demande une compétence sur un outil qu'il n'utilisait pas.
- **Détection** : detecter_techno (`scrapemint/website-tech-stack-detector`, comparaison mensuelle), scraper_offres_emploi (mots-clés outils).
- **Quand écrire** : j0 à j30 après le changement, frais 60 jours.
- **Points** : retrait d'un concurrent 45, ajout d'un outil adjacent 35, migration vue dans une offre 30.
- **Sous-skill** : `changement-techno`.

## 5. Expansion : levée, nouvelle région, nouveau produit

- **Pourquoi ça marche** : les objectifs fixés avec les investisseurs créent l'urgence, la douleur d'échelle apparaît, c'est le moment où l'entreprise remplace ses bricolages par des systèmes.
- **Où on le voit** : tour de financement, nouveau bureau, lancement de produit, rachat.
- **Détection** : detecter_signal (`signalType: funding`, `acquisitions`), detecter_signal `hiring` filtré par ville pour les nouveaux bureaux, `enrichir-entreprise --posts` pour les lancements.
- **Quand écrire** : semaines 2 à 4 après l'annonce (jusqu'à la semaine 8 pour une levée). Jamais la semaine 1.
- **Points** : Série B et plus 45, Série A 35, Seed 20, rachat 35 à 40, nouveau bureau 25, lancement 30.
- **Sous-skills** : `levee-fonds`, `evenements-entreprise`.

## 6. Recrutement ou réduction d'effectif

- **Pourquoi ça marche** : recruter, c'est une pression de montée en charge et un besoin d'efficacité ; réduire, c'est un mandat "faire plus avec moins". Les postes ouverts disent où va le budget et ce que l'entreprise juge prioritaire.
- **Où on le voit** : offres d'emploi, vagues de recrutement, départs, rôles absents de l'organigramme.
- **Détection** : scraper_offres_emploi (`tagadanar/linkedin-jobs-scraper`, `borderline/indeed-scraper`, `--source signalbase` pour les vagues), trouver_personnes pour les rôles manquants.
- **Quand écrire** : jours 14 à 30 après la publication, frais 60 jours ; départ : semaines 1 à 2.
- **Points** : offre pertinente 40, vague de 5 postes ou plus 40.
- **Sous-skill** : `recrutement`.

## Repères de performance

| Approche | Taux de réponse | Valeur des contrats |
|---|---|---|
| Contact à froid, sans signal | 6 à 8 % | référence |
| Un signal | 18 à 22 % | 2 à 3 fois la référence |
| Trois signaux ou plus empilés | 35 à 40 % | 3 à 4 fois la référence |
| Signal + approche multi-canal coordonnée sur le compte | 36 % de rendez-vous | la plus haute |

## Quatre règles de travail

1. Ne citez jamais le signal dans le message : le prospect reçoit dix formules de félicitation sur sa levée par semaine. Citez le problème que le signal crée (`test-et-alors.md`).
2. Agissez vite : un signal chaud expire en 3 à 7 jours, la moitié de sa valeur part en une semaine.
3. Empilez : trois signaux sur le même compte, on écrit le jour même.
4. Choisissez 5 signaux, pas 30. Ceux qui collent à votre offre et que la stack détecte sans effort. Les autres sont du contexte.
