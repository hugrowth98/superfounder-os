---
name: no-show
description: >
  Relance un rendez-vous manqué ou annulé sans culpabiliser ni forcer, reprogramme en une
  touche, et verrouille le prochain créneau avec la mécanique qui évite le no-show
  suivant ; tient la liste hebdomadaire des rendez-vous non honorés à reprogrammer.
  Se déclenche sur : "il n'est pas venu", "no-show", "il m'a posé un lapin", "il a annulé",
  "personne au rendez-vous", "je relance comment", "liste des no-shows de la semaine",
  "il ne répond plus depuis qu'il a accepté". Ne pas utiliser pour : un prospect qui n'a
  jamais pris de rendez-vous (voir script-appel ou la séquence multicanal), une objection
  en direct (voir objections), l'analyse de l'appel qui a mené au rendez-vous (voir
  debrief-apres-appel).
---

# Relancer un rendez-vous manqué

Un rendez-vous pris au téléphone est un rendez-vous fragile : sur une liste froide, 60 à 70 % ne viennent pas ("21 rendez-vous pris, 7 honorés") quand le créneau a été arraché plutôt qu'offert. "Plus on force le rendez-vous, plus on a de no-show." Le remède est double : verrouiller au moment de la prise, et reprogrammer vite, sans reproche, quand la personne ne vient pas.

## Ressources

- `{SKILL_BASE}/ressources/posture.md` sections 2, 7 et 9.
- `{SKILL_BASE}/ressources/sequence-multicanal.md` pour l'ordre des canaux de relance.
- `05_Departements/Go-to-Market/contexte.md` sections 3 (le problème qui justifiait la discussion) et 6 (voix).
- `05_Departements/Go-to-Market/GARDE-FOUS.md` section 4 : jamais de relance à quelqu'un qui a écrit pour annuler tant que l'utilisateur n'a pas lu.

## Méthode

1. Vérifier d'abord qu'il n'a pas prévenu : un email, un message LinkedIn, un SMS. S'il a annulé, on répond dans l'heure, on le remercie d'avoir prévenu, on propose deux créneaux. Aucun reproche.
2. Sans nouvelle, dix minutes après l'heure : un appel. Pas un message. "Bonjour [prénom], [Prénom Nom]. On avait rendez-vous à 14h, je voulais m'assurer que tout allait bien de votre côté." Puis silence.
3. Il répond : "Pas de problème, ça arrive." On ne demande pas pourquoi. On rappelle le sujet en une phrase (le problème du persona qui justifiait la discussion, pas l'offre) et on propose deux créneaux dans les cinq jours. Un rendez-vous "dans un mois, c'est trop tard".
4. On verrouille comme à la première prise : il envoie l'invitation lui-même ou l'accepte en ligne pendant l'appel, on demande "est-ce qu'il y a une raison qui ferait que vous ne pourriez pas être là cette fois ?", et une question pour l'engager sur le sujet ("c'est toujours d'actualité chez vous, [enjeu] ?").
5. Pas de réponse à l'appel : un message écrit de deux lignes sur le canal où il a déjà répondu (email si le rendez-vous venait d'un email, LinkedIn sinon), avec deux créneaux.
6. Toujours rien à J+3 : un second appel à un autre moment de la journée. Puis on arrête. Ligne CRM `Relance cold call` avec une date à 90 jours, ou `Refus cold call` si c'est le deuxième no-show.
7. Le rituel : chaque jeudi, sortir les rendez-vous de la semaine non honorés et les traiter en début de session d'appels, avant tout nouveau numéro. "Toujours commencer une session par les rappels dus."

## Exécution

`verifier_reponses` (skill `verifier-reponses`) avant tout appel ou message, pour lire ce qu'il a éventuellement écrit sur un autre canal. Aucun verbe payant. Entrée : le nom du prospect, l'heure du rendez-vous manqué, le canal d'origine ; ou pour le rituel, le CSV de la liste d'appel avec les colonnes `resultat_appel`, `rdv_date`, `rdv_honore`. Sortie : le script d'appel, le message de deux lignes, et la ligne CRM (`qualification_cold_call`, `date_rappel`, `next_step`) dans le CSV ; pour le rituel, la liste des no-shows de la semaine triés par date, dans `05_Departements/Go-to-Market/Messages/no-shows_<YYYY-MM-DD>.md`.

## Repères

| Repère | Valeur |
|---|---|
| Délai avant le premier appel de relance | 10 minutes après l'heure du rendez-vous |
| Créneaux proposés | 2, dans les 5 jours |
| Touches maximum pour un no-show | 3 : appel, message écrit, second appel à J+3 |
| Après deux no-shows | on arrête, `Refus cold call`, nurturing |
| No-show sur liste froide forcée | 60 à 70 % |
| Ce qui le fait baisser | invitation envoyée par le prospect ou acceptée pendant l'appel, "une raison qui ferait que vous ne pourriez pas être là ?", une question de qualification après le créneau, un rendez-vous à moins de 10 jours |

## Template

Appel, 10 minutes après : "Bonjour [prénom], [Prénom Nom]. On avait rendez-vous à 14h, je voulais m'assurer que tout allait bien de votre côté. *(silence)* Pas de problème, ça arrive. Je tiens toujours à cette discussion sur [problème du persona] : je peux mardi 11h ou jeudi 17h. Vous avez votre agenda ? Envoyez-moi directement l'invitation sur celui qui vous arrange. *(puis)* Et cette fois, est-ce qu'il y a une raison qui ferait que vous ne pourriez pas être là ?"

Message écrit, deux lignes : "Bonjour [prénom], on avait rendez-vous à 14h, je pense qu'un imprévu s'est glissé. Je vous propose mardi 11h ou jeudi 17h pour parler de [sujet] : dites-moi ce qui vous arrange et je vous renvoie l'invitation."

Réponse à une annulation : "Merci d'avoir prévenu, [prénom]. Je vous propose mardi 11h ou jeudi 17h, vous choisissez et je vous envoie l'invitation."

## Règles

- Jamais de reproche, jamais de "vous m'aviez confirmé", jamais "j'ai bloqué mon créneau pour rien". On suppose la bonne foi.
- Jamais demander pourquoi. On propose la suite.
- L'appel avant le message : un écrit se dodge, une voix moins.
- Deux créneaux précis, jamais "quand vous voulez".
- Le rendez-vous reprogrammé se verrouille comme le premier, sinon il sautera pareil.
- Deux no-shows, on arrête : il a dit oui pour faire plaisir. Le prospect suivant vaut plus.
- Rien ne part à quelqu'un qui a écrit entre-temps tant que l'utilisateur n'a pas lu sa réponse.

## Exemples

- "Mon rendez-vous de 14h n'est pas venu" : vérification des réponses, le script d'appel à passer maintenant, le message de repli, la ligne CRM à écrire selon l'issue.
- "Il a annulé ce matin par mail" : la réponse en deux lignes avec deux créneaux, envoyée après validation, et le rappel qu'une annulation prévenue n'est pas un no-show.
- "Sors-moi les no-shows de la semaine" : la liste triée par date depuis le CSV, avec pour chacun le canal d'origine et le prochain créneau à proposer, à traiter en ouverture de la session de jeudi.
