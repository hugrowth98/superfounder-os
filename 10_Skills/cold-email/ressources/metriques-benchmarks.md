# Métriques et repères

Ce qu'on mesure, ce qu'on peut doubler, ce qu'on vise, et le diagnostic quand un chiffre décroche. Les chiffres viennent de campagnes anglophones à grand volume ; en France, sur des listes plus petites et mieux ciblées, les taux de réponse sont souvent plus hauts et les volumes plus bas. Remplacez ces repères par les vôtres dès que vous avez 500 envois.

## 1. Les métriques à suivre

| Métrique | Définition | Où la lire |
|---|---|---|
| Taux de réponse | réponses / emails délivrés | Lemlist, `verifier_reponses` |
| Taux de réponse positive | réponses intéressées ou de routage / délivrés | à la main, colonne `reponse_type` |
| Taux de rendez-vous | rendez-vous pris / délivrés | CRM |
| Taux de rebond | emails non délivrés / envoyés | Lemlist |
| Taux de plainte | signalements spam / délivrés | Google Postmaster, Lemlist |
| Taux de désabonnement | opt-out / délivrés | Lemlist |

Le taux d'ouverture ne se mesure pas : le suivi d'ouverture (pixel) pèse sur la délivrabilité et les messageries l'ouvrent elles-mêmes. Jugez sur les réponses et les rendez-vous. Si vous devez estimer l'ouverture, faites-le sur un échantillon de 50 envois, une fois.

## 2. Les leviers 2X : ce qu'on peut doubler

| Métrique | Point de départ courant | Bon | Très bon |
|---|---|---|---|
| Réponse à froid | 0,5 à 1 % | 2 à 3 % | 5 % et plus |
| Ouverture (si mesurée une fois) | 20 à 40 % | 50 % | 60 % et plus |
| Clic (si un lien) | 2 à 5 % | 5 à 8 % | 10 % et plus |

## 3. Le taux de réponse selon le type de campagne

| Type | Réponse |
|---|---|
| À froid, sans signal | 6 à 8 % |
| Sur un signal | 18 à 22 % |
| Sur plusieurs signaux empilés | 35 à 40 % |
| Visiteur du site relancé | 25 à 30 % |
| Ancien client qui a changé d'entreprise | 20 à 25 % |
| Après engagement (commentaire, webinaire) | 15 à 25 % |

Objectifs d'une campagne saine à volume : réponse positive 5 à 8 %, rendez-vous 2 à 4 %.

## 4. La checklist de structure

Ouverture (déclencheur) + hypothèse + preuve chiffrée + question ouverte.

| Cible | Phrases | Mots |
|---|---|---|
| BTL (managers, opérationnels) | 3 à 4 | 90 maximum |
| ATL (dirigeants, directeurs) | 2 à 3 | 60 maximum |

## 5. Les repères de délivrabilité

| Métrique | Cible | Alerte | Critique |
|---|---|---|---|
| Rebond | moins de 2 % | 2 à 5 % | plus de 5 % : stop |
| Plainte spam | moins de 0,1 % | 0,1 à 0,3 % | plus de 0,3 % |
| Désabonnement | moins de 0,5 % | 0,5 à 1 % | plus de 1 % |
| Réponse (signal de réputation) | plus de 5 % | 3 à 5 % | moins de 3 % : la délivrabilité se dégrade |

Le taux de réponse est le signal positif le plus fort pour les messageries : une réponse crée une conversation, et quelqu'un qui répond ne signale pas en spam. Au-dessus de 15 %, réputation excellente ; au-dessus de 10 %, placement stable ; au-dessus de 5 %, minimum pour tenir dans la durée.

## 6. La performance par email de la séquence

| Email | Ce qu'on observe |
|---|---|
| 1 | 80 % des réponses positives ; le plus important à optimiser |
| 2 (J+3) | 40 à 60 % de l'attention de l'email 1 ; angle différent, plus court |
| 3 (J+14) | nouvel objet, nouvelle approche ; la question de routage marche bien |
| 4 (rupture) | souvent le meilleur taux de réponse de la séquence, parce qu'il crée une échéance et une sortie propre |

L'écart entre la pire et la meilleure variante d'email 1 atteint un facteur 13 : testez 3 ou 4 variantes en parallèle.

## 7. Les règles de test A/B

- Un seul changement à la fois : l'objet, ou la première ligne, ou le CTA. Jamais l'objet et le corps en même temps.
- Deux objets à la fois, pas plus ; 3 ou 4 variantes de corps au plus.
- 100 envois par variante avant de juger ; 200 pour trancher entre deux variantes proches.
- Mesurez le taux de réponse et le taux de rendez-vous, jamais l'ouverture seule : un objet accrocheur qui fait ouvrir sans faire répondre est un piège.
- Ne changez pas le volume et le texte la même semaine : vous ne saurez pas ce qui a joué.
- Le "et alors ?" sur chaque signal : est-il récent ? relié à mon offre ? est-ce que le lecteur s'en soucie ? Un signal qui rate une des trois questions ne porte pas d'email.
- Appariez la messagerie : envoyez depuis Google vers les destinataires Google, depuis Microsoft vers les destinataires Microsoft quand la campagne le permet (réglage Lemlist).

## 8. Les priorités d'optimisation

**Si le taux de réponse est bas (moins de 2 %)** : la pertinence et la personnalisation d'abord ; raccourcir ; un CTA plus doux ; une preuve chiffrée ; un autre framework (`frameworks-13.md`). Avant tout ça, vérifiez que les emails arrivent : rebond, plainte, `run_inbox_placement_test` dans Lemlist.

**Si le taux de rendez-vous est bas (moins de 20 % des réponses positives)** : mieux qualifier dans le message ; un CTA plus clair ; moins de friction pour caler (deux créneaux proposés) ; répondre plus vite (dans l'heure).

**Si la délivrabilité décroche (rebond, plainte)** : `delivrabilite.md` et `../sous-skills/infra-email/SKILL.md`. Sous 1 % de réponse, inutile de tester des outils de diagnostic : le résultat sera toujours le même, nouveaux domaines, nouveau texte, redémarrage.

## 9. Le diagnostic rapide

| Symptôme | Cause probable | Correction |
|---|---|---|
| Aucune réponse, rebond normal | délivrabilité (spam) ou objet | test de placement, puis objets |
| Délivré mais aucune réponse | pertinence du message | plus de personnalisation, plus court, autre angle |
| Des réponses mais pas de rendez-vous | CTA faible ou mauvaise qualification | demande plus claire, meilleur ciblage |
| Désabonnements élevés | trop agressif ou mauvaise cible | fréquence réduite, ICP resserré |
| Rebond en hausse | liste vieille ou domaine en cause | revérifier (`trouver_email`), pause, `infra-email` |
| Baisse générale une semaine | saisonnalité, salon, vacances | comparer aux normes de `sequences.md` avant d'agir |

## 10. Les repères d'infrastructure

- 15 à 25 emails par jour et par boîte Google, 10 à 15 par boîte Microsoft, 30 au maximum quelle que soit la boîte.
- 2 boîtes par domaine, 2 à 3 domaines par expéditeur, jamais le domaine principal.
- 3 semaines de chauffe avant le premier envoi à froid, chauffe jamais coupée.
- 100 % des emails vérifiés avant la campagne, listes de plus de 30 jours revérifiées.
- Texte brut, un lien au plus, aucune image dans l'email 1.

## 11. Les repères LinkedIn

| Métrique | Bon | Très bon | Excellent |
|---|---|---|---|
| Acceptation d'invitation | 25 % | 35 % | 45 % et plus |
| Réponse au message | 10 % | 15 % | 20 % et plus |
| Rendez-vous | 2 % | 5 % | 8 % et plus |

Le détail des limites et de la chauffe d'un compte est dans `linkedin-messages.md`.
