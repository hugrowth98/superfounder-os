# Messages LinkedIn : les principes du cold email, adaptés

LinkedIn est un canal de conversation, pas un canal d'envoi. Les mêmes principes que l'email s'appliquent (un fait, un problème, une question, vouvoiement), avec trois différences : les messages sont deux fois plus courts, l'invitation ne contient jamais de pitch, et le compte a des limites qu'on ne dépasse pas. Exécution via `envoyer-sequence` (Unipile ou Lemlist selon `canal_linkedin` dans `05_Departements/Go-to-Market/OUTILS.md`).

## 1. Qui contacter en priorité

| Priorité | Cible | Comment la trouver |
|---|---|---|
| 1 | participants à un événement ou un webinaire LinkedIn | liste des participants, `scraper_engagement` sur le post de l'événement |
| 1 | personnes qui réagissent aux posts de votre marché ou de vos concurrents | `scraper_engagement`, puis `qualifier_liste` pour garder l'ICP |
| 1 | abonnés de votre page entreprise | Unipile |
| 1 | visiteurs de votre profil | Unipile, à la main |
| 2 | membres récents d'un groupe du secteur | à la main |
| 2 | abonnés à votre newsletter LinkedIn | Unipile |
| 2 | commentateurs de contenus | `scraper_engagement` |

Le filtre qui compte : "a publié dans les 30 derniers jours". Un compte actif répond ; un compte dormant gaspille une invitation sur les 400 du mois.

## 2. Les règles d'écriture

1. Un seul paragraphe, jamais plus.
2. 3 ou 4 phrases au maximum, 40 à 60 mots.
3. Créer une conversation, pas vendre. La question de la fin est celle qu'on poserait à un pair.
4. Un contenu qui s'affiche dans le message (un post, une vidéo courte, un lien vers un live) accroche l'œil.
5. Vouvoiement dans l'invitation et le premier message ; le "tu" seulement si l'autre le prend.
6. Aucune formule d'ouverture creuse, aucune demande de permission d'écrire. Le prénom, puis le fait.
7. Le pitch attend le deuxième ou le troisième message. L'invitation et le premier message ne vendent rien.

## 3. La séquence qui ressemble à un humain

```
Jour 1        voir le profil
Jour 1 ou 2   aimer un post récent (ou commenter une phrase de fond)
Jour 2 ou 3   envoyer l'invitation
              attendre l'acceptation
+4 à 24 h     premier message
Jour +5 à 7   relance si pas de réponse
Jour +10 à 14 dernière relance
```

Jamais les mêmes délais pour tout le monde : Unipile et Lemlist savent espacer aléatoirement. Jamais deux actions sur la même personne à la même minute.

## 4. Les templates

Tous fictifs, à réécrire dans la voix de `05_Departements/Go-to-Market/contexte.md`.

### La note d'invitation (300 caractères maximum, 200 sur un compte gratuit)

Avec note (meilleur taux d'acceptation, à réserver aux cibles prioritaires) :

> Bonjour {{prenom}}, j'ai lu votre post sur {{sujet}}. Ravi de vous suivre ici.

Sans note (plus de volume, acceptation un peu plus basse) : pour les cibles de priorité 2, avec un premier message fort pour compenser.

Ce qui fait refuser : un pitch dans la note, un lien, "j'aimerais vous présenter", plus de deux phrases.

### Après l'acceptation

> Merci d'avoir accepté, {{prenom}}. Question rapide : qu'est-ce qui vous prend le plus de temps sur {{sujet}} en ce moment ?

### Le visiteur de profil (28 à 35 % de réponse sur la source, contre 8 à 12 % à froid)

> Bonjour {{prenom}}, j'ai vu que vous étiez passé sur mon profil. Qu'est-ce qui a retenu votre attention ?

### La personne qui a réagi à un post

> Bonjour {{prenom}}, vous avez réagi à mon post sur {{sujet}}. {{Douleur du post}} est un sujet chez {{entreprise}} en ce moment ?

### Le commentateur

> Bonjour {{prenom}}, votre commentaire sous le post sur {{sujet}} m'a arrêté, surtout {{point précis}}. C'est un chantier chez {{entreprise}} ?

### Le participant à un événement

> Bonjour {{prenom}}, vous étiez à {{evenement}}. Qu'est-ce que vous en retenez ? De mon côté je repense à {{sujet}}, curieux de savoir si ça vous a parlé.

### La relation commune (seulement si elle est réelle)

> Bonjour {{prenom}}, on connaît tous les deux {{relation commune}}. Je travaille avec {{client_similaire}} sur {{sujet}}. Ouvert à un échange rapide ?

### L'abonné à la newsletter

> Bonjour {{prenom}}, vous vous êtes abonné à ma newsletter. Qu'est-ce qui vous a décidé ? La plupart des abonnés avec qui je parle ont {{probleme}} en tête.

### Le membre d'un groupe

> Bonjour {{prenom}}, on est tous les deux dans {{groupe}}. La discussion sur {{sujet}} était utile. C'est un sujet chez {{entreprise}} ?

### La relance (J+5 à 7)

> {{prenom}}, pas de souci si {{sujet}} n'est pas une priorité en ce moment. Si ça l'est, je vous partage ce qui marche chez {{client_similaire}}.

### La dernière relance (J+10 à 14)

> {{prenom}}, dernier message de ma part sur ce sujet. Si le timing est mauvais, dites-le moi et je reviens dans quelques mois.

### Le message qui donne (touche J17 des séquences multicanal)

> {{prenom}}, sans rien attendre en retour : {{ressource concrète, une ligne sur son contenu}}. {{lien}} Si une seule idée vous sert, elle a rempli son rôle.

## 5. Quel template pour quelle situation

| Situation | Template | Réponse attendue (source) |
|---|---|---|
| Visiteur de profil | visiteur | 28 à 35 % |
| Nouvelle connexion | après l'acceptation | 15 à 20 % |
| Réaction à un post | réaction | 18 à 25 % |
| Relation commune | relation commune | 20 à 28 % |
| Participant à un événement | événement | 15 à 22 % |
| Membre d'un groupe | groupe | 12 à 18 % |

## 6. Les limites du compte

| Limite | Valeur |
|---|---|
| Invitations par mois (compte standard) | 400 |
| Invitations par jour | 10 à 15 |
| Messages directs par jour | 15 à 20 |
| InMails ouverts par jour (compte premium) | 30 à 40, 800 par mois |
| Interactions par jour, toutes confondues | 120 au plus, rester bien en dessous |
| Invitations en attente | moins de 500 ; au-dessus de 700, danger |

Ce qui compte comme interaction : messages, invitations, InMails, visites de profil, réactions, commentaires, abonnements à des pages, recommandations, participations à des événements et des groupes.

`05_Departements/Go-to-Market/GARDE-FOUS.md` à la racine fixe les limites propres à l'utilisateur ; elles priment. Le skill `envoyer-sequence` tient un compteur journalier local et bloque au-delà.

## 7. Chauffer un compte

Nécessaire pour un compte inactif, un compte neuf, ou un compte qui sort d'une restriction.

| Période | Volume | Nature |
|---|---|---|
| Jours 1 à 10 | 60 interactions par jour au plus | manuel seulement : visites, réactions, commentaires de fond |
| Jours 11 à 20 | jusqu'à 80 par jour | premières invitations, 5 à 10 par jour, toujours manuel |
| Jour 21 et plus | montée progressive vers les limites | automatisation introduite doucement, surveillance des avertissements |

Les signaux qui font restreindre un compte : un pic d'activité soudain, le même message envoyé à tout le monde, des invitations hors heures de bureau, de l'activité le week-end, l'automatisation dès le premier jour.

### La santé du compte

| Indicateur | Sain | Alerte | Danger |
|---|---|---|---|
| Acceptation des invitations | plus de 30 % | 15 à 30 % | moins de 15 % |
| Réponse aux messages | plus de 10 % | 5 à 10 % | moins de 5 % |
| Visites de profil reçues | stables | en baisse | bloquées |
| Invitations en attente | moins de 500 | 500 à 700 | plus de 700 |

Sous 15 % d'acceptation : retirez les invitations en attente de plus de 3 semaines, resserrez la cible sur les comptes actifs, ajoutez une note, baissez le volume de moitié pendant deux semaines.

### Sortir d'une restriction

1. Arrêter toute automatisation le jour même.
2. Deux semaines d'activité manuelle seulement.
3. Répondre aux conversations en cours.
4. Publier du contenu utile.
5. Commenter les contenus des autres.
6. Réintroduire la prospection très progressivement.

## 8. Les sept facteurs de réussite

1. Ne jamais dépasser les limites : 400 invitations par mois, 120 interactions par jour, avec une marge.
2. Ne cibler que des comptes actifs (publication dans les 30 jours).
3. Des messages très courts : un paragraphe, 3 ou 4 phrases.
4. Un contenu qui accroche l'œil dans le message : vidéo courte, post, live, newsletter.
5. Des étapes qui ressemblent à un humain : délais aléatoires, séquence variée, vrais commentaires, pauses.
6. L'envoi aux heures de bureau du destinataire, du mardi au jeudi de préférence, jamais le week-end.
7. Écrire quand la personne est en ligne quand c'est possible : le message s'affiche en direct.

Les erreurs courantes : le pitch dans l'invitation, un premier message générique, plus de trois relances, une réponse tardive à quelqu'un qui a répondu, un compte non chauffé.

## 9. La checklist avant une campagne LinkedIn

- Cibles filtrées sur l'activité des 30 derniers jours.
- Messages sous 4 phrases, vouvoiement, aucun pitch dans l'invitation.
- Moins de 15 invitations par jour, compteur en place.
- Séquence avec délais aléatoires.
- Envois aux heures de bureau de la cible.
- Une ressource ou un contenu qui donne quelque chose.
- Relances planifiées, deux au plus.
- Compte chauffé si neuf ou inactif.
- Trois messages montrés à l'utilisateur et validés.

## 10. Coordonner LinkedIn et l'email

Les deux canaux se renforcent quand ils portent le même angle et se parlent. Dans une séquence multicanal (`sequences.md`, section 6), LinkedIn fait trois choses que l'email ne fait pas : montrer un visage (la visite de profil, la réaction), prouver qu'on lit (le commentaire de fond), et donner sans rien demander (la ressource en message). L'email porte le fond, les chiffres et la preuve.

Règles : jamais le même texte sur les deux canaux ; un canal ne relance pas ce que l'autre vient d'envoyer le même jour ; une réponse sur un canal arrête l'autre (`verifier_reponses`) ; sur un petit marché, un canal à la fois et jusqu'au bout.
