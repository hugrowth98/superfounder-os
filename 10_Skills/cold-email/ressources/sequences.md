# Séquences : structures, timing, séquences prêtes

Une séquence est une suite de messages sur un ou plusieurs canaux, avec un angle unique et un support qui change à chaque étape. Ce fichier donne les structures (2, 3, 4 emails), la rotation des propositions de valeur, deux séquences multicanal prêtes à adapter, et les règles de timing.

## 1. La structure de référence : 3 emails

| Email | Jour | Fil | But | Ce qu'on sait |
|---|---|---|---|---|
| 1 | J0 | nouveau | obtenir la réponse | 80 % des réponses positives arrivent ici ; testez 3 à 4 variantes |
| 2 | J+3 à J+5 | même fil (RE:) | ajouter du contexte | ce que vous avez coupé de l'email 1 : preuve, ressource, autre angle ; plus court |
| 3 | J+14 à J+17 | nouveau fil, nouvel objet | baisser la friction | ils n'ont pas répondu deux fois : offrez une ressource, demandez la bonne personne |

Après l'email 3 sans réponse : pause de 3 mois, puis une nouvelle séquence avec un autre angle. Jamais plus de 3 emails sans pause longue : au-delà, vous agacez et vous finissez en spam.

Un jour entre deux emails est trop court. 3 à 5 jours est le bon écart.

### Email 1 : présenter l'offre
Ligne 1, pourquoi vous, pourquoi maintenant. Ligne 2, votre offre en clair, courte. Ligne 3, la preuve (vous n'en êtes pas à votre premier client). Ligne 4, le CTA. Les 7 variantes sont dans `variations-email-1.md`.

### Email 2 : ajouter du contexte
Tout ce que vous avez dû couper. Le fil est conservé, le lecteur peut remonter. Toujours court, un peu plus de détail. Nouvel angle de valeur (voir la rotation ci-dessous).

### Email 3 : baisser la friction
Ils ne sont pas convaincus. Un lead magnet, un audit court, une ressource. Un CTA moins exigeant. La question de routage : "si ce n'est pas vous, qui suit ce sujet chez {{entreprise}} ?"

## 2. La variante 4 emails

Quand la cible est un compte à plusieurs interlocuteurs ou que le cycle est long.

| Email | Rôle | Longueur |
|---|---|---|
| 1 | ouverture sur un déclencheur : observation + étude de cas en une ligne + CTA question | 3 à 4 phrases BTL, 2 à 3 phrases ATL |
| 2 | la douleur et l'indicateur principal : le problème relié au chiffre qu'il suit | plus court que le 1 |
| 3 | la responsabilité de quelqu'un d'autre : "qui gère X chez vous ?", ouvre le fil vers la bonne personne | 2 phrases |
| 4 | la rupture : "ce n'est pas la priorité en ce moment ?", sortie propre, porte ouverte | 2 à 3 phrases |

Timing : email 2 à J+3, email 3 à J+14 (nouvel objet), email 4 à J+21 si rien. Le squelette de chaque email : ouverture (déclencheur) + hypothèse + preuve chiffrée + question ouverte.

## 3. Les structures courtes de la couche récente

Deux ou trois emails suffisent dans la plupart des cas. Chaque étape apporte une raison distincte de s'y intéresser.

**Deux emails**
- Email 1, pertinence et résultat : un rôle, un événement ou un flux de travail vérifié ; un problème, un résultat ; une preuve seulement si elle est sourcée ; un CTA à faible effort.
- Email 2, le détail utile : une checklist, un exemple, un risque, un détail de mise en œuvre. On ne répète ni l'ouverture ni la proposition de valeur. Un CTA qui colle au nouvel angle.

**Trois emails**
- Email 1, pertinence et problème : un fait vérifié ou un flux de travail dont il est responsable, relié à un problème probable.
- Email 2, preuve ou méthode : une preuve approuvée, ou une méthode concrète. Sans preuve, une ressource pratique.
- Email 3, clôture ou routage : la pertinence en une ligne, puis "je ferme le fil, ou je contacte quelqu'un d'autre ?". Aucune fausse urgence.

**Contrôles de séquence** : un seul angle de campagne sur toutes les étapes ; on change le support (preuve, ressource, question), pas la promesse ; 50 à 90 mots par email ; un CTA par étape ; on s'arrête à la condition d'arrêt fixée ou dès qu'un prospect se désinscrit ou répond.

## 4. La rotation des propositions de valeur

Ne répétez jamais le même angle d'un email à l'autre :

| Email | Angle |
|---|---|
| 1 | économiser de l'argent |
| 2 | gagner de l'argent |
| 3 | gagner du temps |

L'ordre s'adapte à l'offre, la règle est de tourner. Et chaque angle porte son "et donc" : "gagner 3 heures par mois" est faible, "gagner 3 heures par mois pour que vos commerciaux appellent au lieu de saisir" est fort.

## 5. La rupture : ce qui marche, ce qui ne marche pas

Marche : "Est-ce que je m'adresse à la bonne personne ?", "Quelqu'un d'autre s'occupe de ce sujet chez vous ?", nommer les autres personnes du service (`trouver_personnes` sur la même entreprise permet d'écrire "Sinon, {{prenom_collegue}} serait la bonne personne ?").

Ne marche pas : culpabiliser, supplier, l'humour forcé ("vous avez dû être avalé par un crocodile"), "je clôture votre dossier" sur un ton vexé.

## 6. Séquence prête : "le plafond de la recommandation", 7 touches

Pour vendre un accompagnement commercial, du conseil ou un système de prospection à un dirigeant qui vit sur le bouche-à-oreille. Angle unique : la recommandation a un plafond, comment générer du pipeline au-delà ? Email et LinkedIn alternés. Envoi via `envoyer-sequence` (Lemlist pour l'email ; Unipile ou Lemlist pour LinkedIn selon `05_Departements/Go-to-Market/OUTILS.md`).

| Jour | Canal | Touche | Ce qu'elle fait |
|---|---|---|---|
| 1 | Email | Le miroir | décrit sa situation exacte, sans pitch |
| 2 | LinkedIn | Invitation | sans note, ou une note sans pitch |
| 4 | Email | Le repère | introduit un chiffre de référence sur son métier |
| 8 | LinkedIn | Engagement, message doux | un commentaire sur un de ses posts, puis un message court |
| 11 | Email | La preuve | une étude de cas |
| 17 | LinkedIn | La ressource | un message qui donne quelque chose d'utile |
| 22 | Email | La rupture | dernier message, faible pression |

**J1, le miroir**

```
Objet : vos 3 derniers clients

Bonjour {{prenom}},

D'après votre site, vos trois derniers clients viennent de recommandations d'anciens clients.

C'est le meilleur canal qui existe, et c'est aussi celui qu'on ne pilote pas : le mois où personne ne vous recommande, le pipeline attend.

Vous avez une deuxième source de rendez-vous en place, ou pas encore ?
```

**J2, LinkedIn** : invitation sans note. Ou : "Bonjour {{prenom}}, je suis vos contenus sur {{sujet}}, ravi de vous suivre ici."

**J4, le repère**

```
Objet : RE: vos 3 derniers clients

{{prenom}}, un repère utile : sur les cabinets de conseil de votre taille que j'accompagne, un dirigeant sur trois reçoit moins d'un rendez-vous entrant par mois hors recommandation.

Vous vous situez où par rapport à ça ?
```

**J8, LinkedIn** : un commentaire sur son post le plus récent (une phrase de fond, pas "super post"), puis un message : "J'ai vu votre post sur {{sujet}}. Vous avez creusé la question de la deuxième source de rendez-vous ? Je vous ai écrit deux mots par email à ce sujet."

**J11, la preuve**

```
Objet : {{client_similaire}}

Bonjour {{prenom}},

{{client_similaire}}, cabinet de {{n}} personnes, vivait à 100 % sur la recommandation jusqu'à {{mois}}.

En {{delai}}, ils ont ajouté {{n}} rendez-vous par mois avec une routine de prospection de deux heures par semaine tenue par l'associé.

Je vous envoie le détail de la routine ?
```

**J17, LinkedIn** : "{{prenom}}, sans rien attendre en retour : voici la liste des {{n}} questions qu'on pose à un dirigeant avant de lancer sa prospection. {{lien}} Si une seule vous fait réfléchir, elle a servi."

**J22, la rupture**

```
Objet : je ferme le dossier ?

Bonjour {{prenom}},

Je vous ai écrit trois fois sur le plafond de la recommandation.

Pas de réponse veut dire que ce n'est pas le moment, et c'est très bien.

Une dernière question avant de fermer : le sujet reviendra plutôt à la rentrée, ou jamais ?
```

## 7. Séquence prête : "lead magnet", 2 emails

Pour les personnes qui ont réagi à un lead magnet (commentaire sous un post, téléchargement). Liste construite avec `scraper_engagement`.

| Email | Rôle |
|---|---|
| 1 | positionner le système derrière le lead magnet |
| 2 | inviter à un atelier ou un live, en CTA secondaire |

**Email 1**

```
Objet : votre commentaire sous le post

Bonjour {{prenom}},

Vous avez demandé {{lead magnet}} sous mon post de {{jour}}, le voici : {{lien}}.

Ce document vient d'un système qu'on installe chez des {{profil}} : {{résultat chiffré chez un client}}.

Si vous voulez voir comment il s'applique à {{entreprise}}, je vous montre en 15 minutes. Sinon, bonne lecture.
```

**Email 2 (J+4)**

```
Objet : RE: votre commentaire sous le post

{{prenom}}, j'anime un atelier en ligne le {{date}} sur {{sujet du lead magnet}} : on construit le système en direct, avec les questions des participants.

Vous voulez le lien d'inscription ?
```

## 8. Timing et saisonnalité

**Heures et jours** : mardi à jeudi, 8h à 10h ou 14h à 16h, heure du destinataire. Évitez le lundi matin et le vendredi après-midi. Variez légèrement les heures d'un jour à l'autre et laissez Lemlist espacer les envois de 30 secondes à 3 minutes.

**Baisse attendue, à ne pas prendre pour une panne** :

| Période | Baisse normale | Retour |
|---|---|---|
| Vacances de Noël | 20 à 30 % | mi-janvier |
| Juillet et août | 10 à 20 % (plus fort en France les deux premières semaines d'août) | septembre |
| Fin de trimestre | 10 à 15 % | deux premières semaines du trimestre suivant |
| Salon du secteur | 15 à 25 % la semaine de l'événement | la semaine suivante |
| Ponts de mai | 10 à 20 % | la semaine suivante |

Enquêtez seulement si la baisse dépasse ces normes ou ne revient pas à la date prévue.

## 9. Réutiliser sa liste

**Tous les 3 mois.** Personne ne se souvient de votre email d'il y a 20 minutes, encore moins d'il y a 3 mois, et leurs priorités ont bougé. Calculez le nombre d'emails par jour qui vous permet de refaire le tour de votre marché adressable en 3 mois.

**Petit marché (moins de 20 000 personnes)** : tout le monde, sur tous les canaux, mais un canal à la fois et jusqu'au bout. Email à tout le monde, puis appel à tout le monde, puis LinkedIn à tout le monde. Un enchaînement complexe (email J1, appel J3, message J5) donne les mêmes résultats avec beaucoup plus de stress.

## 10. Les règles de conception

1. L'email 1 apporte 80 % des réponses : mettez-y 80 % de l'effort.
2. Testez 3 à 4 variantes d'email 1 en même temps.
3. Email 2 dans le même fil, en réponse à vous-même.
4. Email 3 avec un nouvel objet, un nouveau départ.
5. Le CTA de routage dans l'email 3 : "{{prenom_collegue}} serait mieux placé pour en parler ?"
6. Sans réponse après 3 emails : 3 mois de pause.
7. Jamais plus de 3 emails sans pause longue.
8. Chaque email apporte une valeur seule : jamais une relance qui ne fait que demander la permission de relancer.
9. Un prospect qui répond, sur n'importe quel canal, sort de la séquence le jour même (`verifier_reponses`).
