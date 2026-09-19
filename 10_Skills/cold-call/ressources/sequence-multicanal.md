# La séquence multicanal : LinkedIn, email, email, LinkedIn, téléphone

Les canaux ne travaillent pas en silos. Chaque touche prépare la suivante, et la dernière est l'appel : c'est lui qui prend le rendez-vous. Un prospect qui a reçu une invitation et deux emails n'est plus un inconnu quand on l'appelle. L'objection "envoyez-moi un mail" tombe d'elle-même : "je vous en ai déjà envoyé deux, autant se voir 20 minutes".

Le téléphone est la touche qui convertit. Les quatre premières servent à ce que l'appel arrive au bon moment, chez quelqu'un qui a déjà vu votre nom. Cette séquence est celle de `05_Departements/Go-to-Market/contexte.md` section 5 par défaut ; l'utilisateur peut la raccourcir, jamais l'inverser (l'appel n'ouvre pas, il ferme).

## Les cinq touches

| Jour | Touche | Rôle | Contenu | Longueur | Ce qui déclenche la suite |
|---|---|---|---|---|---|
| J0 | LinkedIn : invitation | se faire connaître, poser un visage, ouvrir la porte | sans note, ou une note de 200 caractères qui nomme le signal sans le citer brut | 0 à 200 caractères | acceptée ou non, on passe à J+2 quoi qu'il arrive |
| J+2 | Email 1 | dire le problème et prouver qu'on le règle | problème, cause, conséquence dans les mots du persona ; une preuve chiffrée ; un créneau proposé | 60 à 90 mots | pas de réponse à J+5 |
| J+5 | Email 2 | relancer sans répéter | un angle différent (un autre des trois problèmes) ou une autre preuve, jamais "je me permets de revenir vers vous" | 3 phrases | pas de réponse à J+7 |
| J+7 | LinkedIn : message ou geste | rappeler qu'on existe, juste avant l'appel | si l'invitation est acceptée : un DM de 2 phrases qui annonce l'appel ("je vous appelle jeudi matin, dites-moi si un autre moment vous arrange") ; sinon : une visite de profil et une réaction sur un post récent | 2 phrases | J+9 |
| J+9 à J+12 | Téléphone | prendre le rendez-vous | le script en 5 temps de `script-appel`, avec le signal en raison d'appel ; deux tentatives à deux moments différents (matin, fin d'après-midi) | 90 secondes avant de demander le rendez-vous | rendez-vous, refus net, ou passage en nurturing |

Après la touche 5 sans contact : un dernier email de deux lignes ("je n'ai pas réussi à vous joindre, si le sujet [X] revient chez vous, mon numéro est en signature"), puis nurturing 90 jours : rien, sauf si un nouveau signal apparaît. Pas de troisième relance email, pas de troisième appel dans la même séquence.

## Le rôle de chaque canal

- LinkedIn ouvre et rappelle. Il ne vend pas et ne demande pas de rendez-vous en premier message. Une invitation acceptée est un signal d'engagement (5 points, `05_Departements/Go-to-Market/contexte.md` couche 3) qui remonte le prospect dans la liste d'appel.
- L'email argumente. C'est le seul endroit où le problème, la cause et la conséquence sont écrits noir sur blanc, avec la preuve. Il donne au prospect de quoi vous situer avant l'appel.
- Le téléphone convertit. Il est réservé aux tiers A et B, aux personnes dont on a le mobile ou la ligne directe, et il arrive toujours après au moins une touche écrite quand c'est possible. En appel à froid pur (aucune touche avant), il faut un signal frais pour le rendre légitime.

## Timing et rythme

- Les touches écrites partent du mardi au jeudi, entre 8h30 et 11h ou entre 14h et 17h, heure du prospect. Jamais le lundi matin, jamais le vendredi après-midi, jamais le week-end.
- Les appels se font en sessions bloquées d'une heure, deux fois par semaine minimum, avec la liste prête et la fiche de `brief-avant-appel` sous les yeux. Le meilleur créneau pour joindre un dirigeant : 8h30 à 9h30 et 17h30 à 18h30.
- Un prospect qui a émis un signal chaud (visite de profil, commentaire, réponse à un post) sort de la séquence standard : on l'appelle dans les 48 heures, avec le signal en raison d'appel.
- Une prise de poste se travaille entre le jour 14 et le jour 45 ; une levée entre la semaine 2 et la semaine 8 ; une offre d'emploi tant qu'elle est ouverte.

## Ce qui arrête la séquence

- Une réponse, sur n'importe quel canal, même un "non merci" : tout s'arrête, l'utilisateur lit et répond lui-même. `verifier_reponses` tourne avant chaque touche.
- Un rendez-vous pris : le prospect passe dans le CRM, la séquence est close.
- Un opt-out ou un "ne m'appelez plus" : `ne_plus_contacter`, sous 48 heures.
- Un "rappelez-moi dans trois mois" : une tâche datée, rien d'autre d'ici là.

## Variantes

- Pas de LinkedIn (persona absent ou compte fragile) : email J0, email J+3, téléphone J+6 à J+8, dernier email J+12.
- Pas d'email (pas d'adresse vérifiée) : invitation J0, DM à l'acceptation, téléphone J+5.
- Liste warm (déjà rencontrés, anciens prospects, commentateurs d'un post) : téléphone direct, avec la relation comme raison d'appel ("on avait échangé en mars", "vous aviez commenté mon post sur X").
- Compte en warmup (`05_Departements/Go-to-Market/GARDE-FOUS.md` section 2) : la séquence garde son ordre, les volumes descendent aux plafonds de la semaine en cours.
