---
name: engagement
description: >
  Fait grandir la portée par les commentaires : commenter chez les autres (qui, quand, quoi),
  répondre chez soi (routine, réponses dans la voix de l'utilisateur, envoi de la ressource
  promise), lire les signaux qui comptent pour le fil, respecter les limites du compte. Se
  déclenche sur : "réponds aux commentaires", "qui je devrais commenter", "plus de portée",
  "mes posts ont des likes mais pas de commentaires", "mon compte est restreint", "envoie la
  ressource à ceux qui ont commenté". Les messages privés qui suivent un commentaire relèvent
  des masters GTM (`detecter-signaux`, sous-skill engagement-contenu, et `cold-email`).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Engagement

Les commentaires sont l'activité au meilleur rendement sur LinkedIn : ils comptent plusieurs fois une réaction pour le fil, ils créent la relation, et ils mettent votre nom sous les posts de comptes plus gros que le vôtre. Le détail des poids et de la distribution est dans `{SKILL_BASE}/ressources/algorithme.md`.

## Ce que le fil compte

| Action | Poids relatif | Pourquoi |
|---|---|---|
| Enregistrement | environ 5 | le lecteur veut y revenir |
| Commentaire de plus de 15 mots | environ 4 | de la lecture, de la réflexion |
| Partage avec un mot | 3 à 4 | une nouvelle audience |
| Commentaire court | environ 2 | présent, mais léger |
| Réaction | 1 | la base |
| Temps de lecture | positif dès 10 secondes | même sans clic ; un défilement rapide compte en négatif |

## Commenter chez les autres

- 10 à 20 commentaires par jour, de plus de 15 mots chacun, sur des posts de la niche : un point de vue, une expérience, une question.
- Viser des comptes plus gros que le sien et arriver dans les 30 premières minutes : le commentaire reste en haut.
- Forme : une première phrase forte, un saut de ligne, une question pour finir.
- Trois gabarits, à réécrire dans la voix de l'utilisateur :
  - ajouter : "Ça rejoint ce qu'on voit chez [contexte] : [détail précis]. Vous observez la même chose sur [angle voisin] ?"
  - témoigner : "Testé le trimestre dernier. Résultat : [chiffre ou fait]. La seule chose que j'ajouterais : [idée]."
  - contredire avec respect : "J'ai vu l'inverse dans [contexte] : [preuve]. Vous avez des exceptions en tête ?"
- Les 15 minutes après avoir publié servent aussi à ça (sous-skill `publier`).

## Répondre chez soi

- Répondre à chaque commentaire dans la première heure, puis par passages ; une réponse relance (question, précision), elle ne dit pas seulement merci.
- Une ressource promise contre un mot-clé (sous-skill `cta`) s'envoie à chacun, le jour même. Avec Unipile connecté, le skill `repondre-commentaires` lit les commentaires d'un post et prépare les réponses dans la voix de l'utilisateur ; elles partent une par une, après validation.
- Ceux qui commentent sont les meilleurs prospects : la liste se récupère avec `scraper-engagement` (Unipile ou Apify) et se traite dans le master `detecter-signaux` (sous-skill engagement-contenu), jamais depuis ce sous-skill.

## Les limites du compte

Les plafonds journaliers d'invitations, de messages et d'interactions, le protocole de remise en route d'un compte averti, et la règle des 48 heures d'arrêt après une restriction sont dans `05_Departements/Go-to-Market/GARDE-FOUS.md` : une seule source pour la prospection et le contenu. Les groupes d'engagement organisés sont détectés et pénalisés depuis 2023 : un cercle de 10 à 20 pairs qui réagissent naturellement remplace un pod.

## Méthode

1. Diagnostic en une ligne : réactions sans commentaires (le contenu ne donne rien à dire : finir par une question précise, prendre position), commentaires sans réactions (le sujet divise, c'est bien), rien du tout (portée : cadence, commentaires chez les autres, hook).
2. Une liste de 10 à 20 comptes à commenter (les créateurs admirés de `strategie-contenu.md`, les comptes de la cible), et un créneau quotidien de 15 à 20 minutes.
3. Le rituel après publication (sous-skill `publier`), et les réponses préparées avec `repondre-commentaires` quand Unipile est branché.
4. Chaque mois, regarder les commentaires reçus : ce sont les prochaines idées de posts (sous-skill `ideation`).

## Exemples

- "Mes posts ont 40 likes et 2 commentaires" : finir chaque post par une question précise, écrire des posts qui invitent le désaccord ou le témoignage, un sondage de temps en temps ; réponse attendue : trois fins de post réécrites et une liste de 10 comptes à commenter.
- "Réponds aux commentaires de ce post" : `repondre-commentaires` (Unipile), réponses dans la voix de l'utilisateur, envoyées après validation ; réponse attendue : la liste des commentaires et les réponses proposées.
- "Mon compte est restreint" : arrêt complet 48 à 72 heures, reprise selon `GARDE-FOUS.md`, commentaires manuels avant tout envoi ; réponse attendue : le protocole et le calendrier de reprise.
