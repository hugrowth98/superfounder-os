---
name: script-appel
description: >
  Écrit ou adapte le script d'appel en 5 temps (accroche, raison de l'appel liée au signal,
  problème cause conséquence avec sa question, écoute, créneau) pour un persona ATL ou BTL
  et un signal donnés, à partir de contexte.md. Se déclenche sur : "script d'appel",
  "qu'est-ce que je dis au téléphone", "accroche", "pitch téléphone", "adapte le script
  pour un DRH", "j'appelle quelqu'un qui recrute", "relis mon script", "prépare les
  ouvertures de ma liste". Ne pas utiliser pour : répondre à une objection précise (voir
  objections), relancer un rendez-vous manqué (voir no-show), préparer une personne
  nommée avec ses données (voir brief-avant-appel), un email (voir cold-email).
---

# Le script en 5 temps

Un script d'appel n'est pas un texte à lire, c'est un point d'atterrissage : 90 secondes pour montrer qu'on connaît les problèmes de la personne et lui offrir une bonne discussion. Sur une liste avec signal, 30 % des décrochés prennent le créneau ; sans signal, presque aucun, avec le même texte.

## Ressources

- `{SKILL_BASE}/ressources/posture.md` : lu en entier avant d'écrire une ligne.
- `{SKILL_BASE}/ressources/scripts-par-signal.md` : l'ouverture qui remplace le temps 2 selon le signal.
- `{SKILL_BASE}/ressources/objections-france.md` : pour le temps 4.
- `05_Departements/Go-to-Market/contexte.md` sections 1 (offre, preuves), 3 (personas et angle), 4 (signaux), 6 (voix).

## Méthode

1. Lire `05_Departements/Go-to-Market/contexte.md`. Si la section 1 ou 3 a encore des crochets, s'arrêter et proposer "Installe ma prospection".
2. Fixer le persona (ATL ou BTL) et le signal. Sans précision, écrire pour l'ATL avec le signal n°1.
3. Construire le tableau problème / cause / conséquence du persona : trois problèmes de dirigeant, "douloureux, urgents, reconnus", dans les mots de `05_Departements/Go-to-Market/contexte.md`. Pas des problèmes de RH ni d'outil : des projets en retard, des équipes surchargées, de la marge perdue, un risque daté.
4. Écrire la proposition de valeur en une phrase, moins de 20 mots, sur le moule "on aide les [X] à [Y] sans [douleur]". Sans nom de catégorie (cabinet, agence, formation).
5. Écrire les 5 temps avec le template ci-dessous. Chaque temps tient sur une ligne parlée.
6. Relire à voix haute : couper tout mot qui ne sert à rien, toute phrase de plus de 20 mots, toute description de l'offre.
7. Livrer le script, puis la variante "personne pressée" en trois phrases, puis la variante de l'autre persona en trois lignes.

## Exécution

Aucun verbe payant : ce sous-skill n'appelle aucun outil. Entrée : `05_Departements/Go-to-Market/contexte.md`, et si l'utilisateur donne une liste, un CSV aux colonnes normalisées avec au moins `prenom`, `titre`, `entreprise`, `tier`, `signal_type`, `signal_detail`. Sortie : `05_Departements/Go-to-Market/Messages/script-appel_<persona>_<YYYY-MM-DD>.md` ; pour une liste, le même CSV avec trois colonnes ajoutées, `ouverture` (la phrase du temps 2 adaptée au signal de la ligne), `probleme_1`, `probleme_2`. Une personne nommée avec des données à aller chercher passe par `brief-avant-appel`.

## Repères

| Temps | Durée | Ce qui doit s'être passé |
|---|---|---|
| 1. Accroche | 10 s | le prospect a demandé qui appelle |
| 2. Raison de l'appel | 10 s | il a entendu le signal ou la proposition de valeur, et vous vous êtes tu |
| 3. Problème, cause, conséquence | 30 s | il a dit "oui, c'est ça" ou "ah bon ?" |
| 4. Écoute | variable | une brèche ou une objection, prise sans contredire |
| 5. Créneau | 10 s, puis 2, 3, 4 fois | un créneau daté, l'invitation acceptée en ligne |
| Total avant la première demande de créneau | 90 s maximum | au-delà, il a décroché mentalement |
| Durée demandée | 20 minutes, 15 si pressé | "personne ne dit non à 20 minutes" |
| Part de parole | 80 % pour vous | c'est l'inverse d'un rendez-vous de découverte |

## Template

> **Temps 1, l'accroche.** "Bonjour [prénom], je vous appelle parce que j'aimerais beaucoup vous rencontrer." *(Silence. Il demande : c'est à quel sujet ? vous êtes qui ?)* "[Prénom Nom], je ne sais pas si vous me remettez." *(Ces dix secondes servent à préparer la suite.)*
>
> **Temps 2, la raison de l'appel.** Avec un signal : "Je vous appelle parce que [le signal, dit par ce qu'il implique, une phrase de `scripts-par-signal.md`]." Sans signal : "On aide les [X] à [Y] sans [douleur]." *(Puis on s'arrête. C'est lui qui relance : "ah oui ? c'est-à-dire ?")*
>
> **Temps 3, problème, cause, conséquence.** "Ce que je remarque en ce moment chez les [persona] comme vous, c'est [problème 1] à cause de [cause], ce qui fait que [conséquence]. Souvent il y a aussi [problème 2] et [problème 3]. Est-ce que c'est un sujet qui vous parle ?" *(La seule question de l'appel. Fermée.)*
>
> **Temps 4, l'écoute.** *(Il réagit. On ne creuse pas, on ne pose pas de question de découverte. "Oui, c'est ça" : temps 5 tout de suite. Une objection : "je comprends, vous avez raison, et moi ce que je remarque c'est [problème]", puis temps 5. Un blanc : on le laisse.)*
>
> **Temps 5, le créneau.** "C'est pour ça que j'aimerais qu'on se rencontre : vous offrir une bonne discussion sur ces sujets. On accompagne déjà [référence]. Pas pour vous vendre quoi que ce soit aujourd'hui, 20 minutes pour voir lequel est le plus chaud chez vous. Cette semaine ou la prochaine ?" *(Puis :)* "Vous avez votre agenda sous les yeux ? Je vous envoie l'invitation tout de suite [ou : envoyez-la moi directement sur le créneau qui vous arrange]. En attendant, est-ce qu'il y a une raison qui ferait que vous ne pourriez pas être là ? ... Vous pouvez l'accepter, comme ça c'est bloqué. Et juste pour préparer : vous êtes plutôt côté [enjeu A] ou côté [enjeu B] en ce moment ?"

Variante pressée : "Bonjour [prénom], je vous appelle parce que j'aimerais qu'on se rencontre. On aide les [X] à [Y]. *(pause)* Ce que je vois chez vos pairs, c'est [problème 1] et [problème 2]. J'aimerais vous offrir une bonne discussion là-dessus, 20 minutes cette semaine ?"

Variante BTL (celui qui vit le problème) : les problèmes sont ceux du quotidien (charge, délais, outils qui ne suivent pas), l'offre de discussion devient "je vous montre ce que font vos pairs là-dessus, et de quoi en parler en interne", 15 minutes, et s'il dit "je ne décide pas" : "très bien, on le cale à trois ?".

## Règles

- Jamais se présenter avant que le prospect l'ait demandé. "Bonjour, je suis X de la société Y" est catalogué prospection en deux secondes.
- Jamais de question de découverte, jamais de question qui commence par "comment". Une seule question : "est-ce que c'est un sujet qui vous parle ?"
- Jamais décrire l'offre, la méthode, une fonctionnalité, un prix. Montrer l'expertise en citant les problèmes, pas en décrivant la solution.
- Le signal ouvre l'appel et disparaît ensuite : on remonte aux problèmes de dirigeant, pas au détail de l'offre d'emploi ou de la levée.
- Une objection se prend en trois temps (je comprends, vous avez raison, et moi je remarque que) et finit par un créneau. Jamais "non mais", jamais "oui mais".
- Le créneau est daté avant de raccrocher, l'invitation acceptée en ligne, la question de qualification vient après, jamais avant.
- Le script est un point d'atterrissage : on le connaît, on ne le lit pas. "Quand on lit un script, on n'est pas dans la discussion."
- Vouvoiement, sauf `05_Departements/Go-to-Market/contexte.md` section 6.

## Exemples

- "Écris-moi le script pour appeler des DRH d'ETI industrielles qui recrutent un commercial" : script ATL avec le signal recrutement en temps 2, trois problèmes de DRH (poste vacant qui coûte, équipe qui absorbe, délai qui s'allonge), créneau 20 minutes.
- "Adapte-le pour le responsable recrutement, pas le DRH" : variante BTL, problèmes du quotidien, 15 minutes, "on le cale à trois ?" en réserve.
- "Voici mon script, relis-le" : les tics relevés un par un (présentation en premier, question de découverte, description de l'offre), la version corrigée en face, et le tableau problème / cause / conséquence reconstitué à partir de son texte.
