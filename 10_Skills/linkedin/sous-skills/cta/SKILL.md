---
name: cta
description: >
  Écrit la fin d'un post LinkedIn : la question qui fait commenter, le mot-clé à commenter
  pour recevoir une ressource, le PS, l'invitation à enregistrer ou à suivre, selon l'objectif
  du post (portée, conversation, abonnés, leads, liste email). Se déclenche sur : "comment je
  termine", "CTA", "appel à l'action", "PS", "je veux des commentaires", "commentez pour
  recevoir", "fin de post". Ne pas utiliser pour le titre ou la section à propos du profil
  (sous-skill `profil`) ni pour un message privé de suite (masters GTM).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# CTA : la fin qui relance

La dernière ligne d'un post ne conclut pas, elle relance. Un seul appel par post : deux appels se neutralisent. L'appel se choisit selon l'objectif, il est précis (pas "dites-moi ce que vous en pensez"), il baisse la marche (un mot à commenter est plus facile qu'un paragraphe) et il colle au contenu : un cadre se fait enregistrer, une opinion se fait commenter, un récit se fait suivre.

## L'appel selon l'objectif

| Objectif | Type d'appel | Gabarit |
|---|---|---|
| Portée | enregistrer | "Enregistrez ce post pour votre prochain [situation]." |
| Conversation | question précise | "Quelle est la première chose que vous [action] quand [situation] ? Dites-le en commentaire." |
| Débat | prise de position | "D'accord ou pas ? Je réponds à chaque commentaire." |
| Abonnés | suivre | "Je publie un [type de contenu] par semaine sur [sujet]. Suivez-moi pour le prochain." |
| Leads | mot-clé à commenter | "Commentez [MOT] et je vous envoie le [modèle / guide / checklist] en message." |
| Liste email | lien en commentaire | "Le guide complet est en premier commentaire." |

## Les trois mécaniques qui font le plus de commentaires

**Le mot-clé à commenter.** Un post qui offre une ressource contre un mot en commentaire fait 3 à 5 fois plus de commentaires qu'un post ordinaire, et le fil le distribue davantage. Conditions : la ressource existe avant de publier, elle est envoyée à chacun (à la main ou par le sous-skill `engagement` avec le script `repondre-commentaires`), et le post dit ce qu'elle contient en 3 lignes. Voir `lead-magnet` pour le post entier.

**Le PS en question.** Après la dernière ligne, un "PS :" avec une question ouverte sur la situation du lecteur ("PS : vous en êtes où sur [sujet], vous ?"). Il fait commenter ceux qui n'auraient pas réagi au corps.

**La suite en commentaire.** "La suite en commentaire" pour un contenu trop long, avec le complément posté juste après : il crée un premier commentaire, et il fait lire jusqu'au bout.

## Règles

- Un seul appel, en une ou deux lignes, dans la voix de l'utilisateur (vouvoiement sur ce qui se publie, sauf si `Tone-and-Voice.md` dit le contraire).
- Précis : "Commentez votre pire erreur de recrutement" bat "Qu'en pensez-vous ?".
- Cohérent avec le contenu : un cadre se fait enregistrer, un avis se fait commenter, un récit se fait suivre, une ressource se fait demander.
- Un mot-clé à commenter engage à envoyer : ne jamais promettre une ressource qui n'existe pas encore.
- Pas de "likez et partagez si vous êtes d'accord" : ça mesure la mauvaise chose et ça sent la ferme à engagement.
- Aucun lien dans le corps du post : en premier commentaire, et le post le dit.

## Ce qui est rendu

Deux ou trois fins possibles, chacune avec l'objectif qu'elle sert et une ligne sur ce qu'elle déclenche, puis la recommandation. Si le post existe, la fin choisie est intégrée au texte complet.

## Exemples

- Post sur un cadre de qualification d'appel, objectif portée : "Enregistrez ce cadre pour votre prochain premier appel. Et repostez-le si votre équipe en a besoin." ; réponse attendue : trois fins (enregistrer, question, mot-clé) et le choix.
- Post d'opinion sur le recrutement, objectif conversation : "Le talent avant la culture. J'ai vu l'inverse coûter cher dix fois. Vous avez vu quoi, vous ?" ; réponse attendue : une question qui invite le désaccord.
- Post qui offre un modèle de séquence : "Commentez SEQUENCE et je vous l'envoie en message. Assurez-vous qu'on est connectés, sinon je ne peux pas vous écrire." ; réponse attendue : le mot-clé, la phrase sur la connexion, et le rappel d'envoyer à chacun.
