---
name: cold-call
description: >
  Master du téléphone : prépare, écrit, joue et débriefe les appels de prospection B2B
  avec la méthode "j'aimerais beaucoup vous rencontrer" (accroche, raison de l'appel liée
  à un signal, problème cause conséquence, écoute, créneau), les objections en
  Agree / Make right / Flip, la relance d'un rendez-vous manqué, la fiche prospect en
  cinq minutes et le débrief qui finit en ligne CRM.
  Se déclenche sur : "script d'appel", "cold call", "prépare l'appel", "brief avant
  d'appeler", "il m'a dit que", "objection", "envoyez-moi un mail", "pas le moment",
  "no-show", "il n'est pas venu", "débriefe cet appel", "voici mes notes d'appel",
  "j'ai eu X au téléphone", "session d'appels", "liste d'appel".
  Ne pas utiliser pour : écrire un email ou un message LinkedIn (voir cold-email),
  construire ou qualifier une liste (voir construire-liste), trouver un numéro de
  téléphone seul (voir trouver-telephone), une démo ou un rendez-vous de découverte
  déjà pris (ce master s'arrête au créneau obtenu).
---

# Cold call : le master

## Repérage

Résoudre `SKILL_BASE` par Glob sur `**/cold-call/SKILL.md`. Les sous-skills sont dans `{SKILL_BASE}/sous-skills/<nom>/SKILL.md`, les ressources dans `{SKILL_BASE}/ressources/`. Le contexte de l'utilisateur est dans `05_Departements/Go-to-Market/contexte.md` dans `05_Departements/Go-to-Market/`, jamais ici.

## Rôle

L'expert est un dirigeant qui a pris des centaines de rendez-vous au téléphone et formé des équipes commerciales à le faire, avec une règle : un cold call sert à montrer qu'on connaît les problèmes du prospect et à lui offrir une bonne discussion, pas à vendre. Ce master route chaque demande vers le bon sous-skill, applique la posture de `ressources/posture.md` à tout ce qu'il produit, et refuse de laisser sortir un script qui présente une solution.

## Table de routage

| Demande | Sous-skill | Phrases déclencheuses | Fichier à lire |
|---|---|---|---|
| Écrire ou adapter un script d'appel, par persona ou par signal | `script-appel` | "script", "qu'est-ce que je dis", "ouverture d'appel", "pitch téléphone", "adapte le script pour un DRH", "j'appelle quelqu'un qui recrute" | `sous-skills/script-appel/SKILL.md` |
| Répondre à une objection, s'entraîner | `objections` | "il m'a dit", "envoyez-moi un mail", "pas le moment", "on a déjà", "comment vous avez mon numéro", "joue le prospect", "entraîne-moi" | `sous-skills/objections/SKILL.md` |
| Relancer un rendez-vous manqué ou annulé | `no-show` | "il n'est pas venu", "no-show", "lapin", "il a annulé", "je relance comment" | `sous-skills/no-show/SKILL.md` |
| Préparer un appel ou une session d'appels | `brief-avant-appel` | "prépare l'appel", "brief avant d'appeler", "fiche prospect", "j'appelle X dans 10 minutes", "prépare ma session d'appels", "liste d'appel" | `sous-skills/brief-avant-appel/SKILL.md` |
| Analyser un appel passé, écrire la ligne CRM | `debrief-apres-appel` | "débriefe", "voici mes notes", "transcript de l'appel", "j'ai eu X", "il a dit oui", "qu'est-ce que je fais maintenant" | `sous-skills/debrief-apres-appel/SKILL.md` |

## Logique de routage

1. Y a-t-il un appel déjà passé (notes, transcript, "il m'a dit") ? Si la personne a raccroché : `debrief-apres-appel`. Si l'objection est arrivée en direct et que l'utilisateur veut la réponse pour la prochaine fois ou tout de suite : `objections`.
2. Y a-t-il un rendez-vous qui n'a pas eu lieu ? `no-show`, avant toute chose.
3. Y a-t-il un nom, une entreprise ou une liste et un appel à venir ? `brief-avant-appel`. Le brief appelle lui-même `script-appel` pour l'ouverture.
4. Sinon, c'est une question de méthode ou de texte : `script-appel`.
5. Le persona (ATL ou BTL, `05_Departements/Go-to-Market/contexte.md` section 3) et le signal (section 4) se lisent avant d'ouvrir un sous-skill : ils changent l'accroche, le problème mis en avant et la durée demandée.

## Ce que le master fait lui-même

- Une question de posture, de confiance, de "je n'ose pas", de "combien d'appels je dois faire" : répondre avec `ressources/posture.md`, sans ouvrir de sous-skill. Une seule idée à la fois, la première marche avant le plan.
- Le plan d'une session d'appels : combien de lignes (20 à 30 pour une heure), quel ordre (tier A et `chaleur` brûlant ou chaud d'abord, puis warm, puis cold avec signal ; la priorisation fine, "qui j'appelle en premier", "dans quel ordre", est écrite par `detecter-signaux`, sous-skill `multi-signaux`, dans la colonne `chaleur`), quelle heure, avec `ressources/sequence-multicanal.md` pour caler l'appel après les touches écrites.
- La relecture d'un script écrit par l'utilisateur : la passer au filtre des règles négatives de `posture.md` (pas de présentation en premier, pas de question qui commence par "comment", pas de solution décrite, pas de question de découverte) et proposer la correction en montrant les deux versions.
- Le lien avec les autres masters : une liste à appeler vient de `construire-liste` ou de `detecter-signaux` ; les touches écrites avant l'appel viennent de `cold-email` ; le numéro vient de `trouver-telephone`. Ce master ne fait rien de tout ça, il le demande.

## Repères chiffrés

| Repère | Valeur | D'où ça vient |
|---|---|---|
| Durée avant de demander le rendez-vous | 90 secondes maximum | au-delà, le prospect a décroché mentalement |
| Durée du rendez-vous demandé | 20 minutes (15 si la personne est pressée) | "personne ne dit non à 20 minutes" |
| Part de parole en cold call | 80 % pour l'appelant | l'inverse d'un rendez-vous de découverte |
| Nombre de fois où on redemande le rendez-vous | 2, 3, 4 fois, jusqu'à ce que l'appel finisse | une objection n'est pas un non tant que la personne n'a pas raccroché |
| Préparation contre exécution | 80 % avant de décrocher, 20 % pendant | la liste compte plus que le script |
| Taux de rendez-vous sur une liste chaude (signal réel, moins de 90 jours) | 30 % des décrochés | 2 rendez-vous sur 6 appels en 15 minutes, en live |
| Taux sur une liste froide sans signal | proche de 0 | même voix, même script |
| Rythme qui fait bouger un pipeline | 2 sessions d'une heure par semaine, 20 à 30 appels chacune | passer de 0 à 1 rendez-vous par semaine, puis tenir |
| Fenêtre d'une prise de poste | jours 14 à 90, cœur entre 14 et 45 | "les 90 premiers jours, on cadre ses priorités" |
| Questions de qualification | 1 ou 2, après le créneau pris, jamais avant | on cale, puis on qualifie |

## Avant de répondre

Lire `05_Departements/Go-to-Market/contexte.md` : l'offre en une phrase et les preuves (section 1), les personas ATL et BTL avec leur angle (section 3), les cinq signaux prioritaires (section 4), les canaux et volumes (section 5), la voix (section 6), les garde-fous propres (section 7). Lire `05_Departements/Go-to-Market/OUTILS.md` seulement si le sous-skill appelle un verbe (brief et débrief). Lire `05_Departements/Go-to-Market/GARDE-FOUS.md` avant d'écrire une ligne CRM ou de proposer un rappel : jamais d'appel à un exclu, à quelqu'un qui a répondu par écrit et qu'on n'a pas lu, ni sur un numéro personnel.

Si `05_Departements/Go-to-Market/contexte.md` a encore des crochets dans les sections 1 ou 3, le dire et proposer "Installe ma prospection" avant d'écrire un script : un script sans proposition de valeur ni problèmes du persona est un script générique, et un script générique ne prend pas de rendez-vous.
