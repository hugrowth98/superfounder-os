---
name: publier
description: >
  Décide quand et à quel rythme publier : la cadence hebdomadaire, les créneaux, la routine
  des 90 minutes après publication, la constance thématique, l'écriture en lot et la
  programmation (native LinkedIn, ou Publora par le skill `planifier-post`). Se déclenche sur :
  "quand publier", "à quelle heure", "combien de posts par semaine", "je publie tout le
  dimanche", "programme ma semaine", "je n'ai pas le temps d'être régulier". Ne pas utiliser
  pour écrire le post (sous-skills du type) ni pour commenter chez les autres (sous-skill
  `engagement`).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Publier : cadence, créneaux, routine

La régularité bat le volume, et la présence après publication bat les deux. La cadence et les créneaux de l'utilisateur sont dans `Strategie-contenu.md` (section Objectif et cadence) ; ce sous-skill les applique, et les ajuste avec ses chiffres (sous-skill `performance`) plutôt qu'avec des moyennes. Le détail de la distribution est dans `{SKILL_BASE}/ressources/algorithme.md`.

## La cadence

| Rythme | Effet | Pour qui |
|---|---|---|
| 1 par semaine | présence de base | débutant, dirigeant très pris |
| 3 à 4 par semaine | la zone de croissance | dirigeant ou consultant qui construit son audience |
| 5 par semaine | rendements décroissants | créateur à plein temps |
| tous les jours, ou deux par jour | la qualité baisse, le fil ne suit pas | à éviter |

Trois à quatre posts par semaine, sur les mêmes deux ou trois sujets : le fil apprend de quoi vous parlez et distribue mieux ; changer de sujet toutes les semaines remet le compteur à zéro.

## Les créneaux (heure locale du lecteur)

| Jour | Fenêtre | Note |
|---|---|---|
| mardi, mercredi, jeudi | 7h30 à 8h30, puis 12h à 13h | les meilleurs jours pour une audience B2B |
| lundi | 8h à 9h | bon, mais la boîte mail concurrence |
| vendredi | 7h30 à 8h30 | correct, chute après midi |
| samedi | 9h à 11h | moins de concurrence, moins de lecteurs |
| dimanche | 19h à 21h | la fenêtre "je prépare ma semaine" |

Audience dans deux fuseaux : deux créneaux, jamais le même post deux fois. Le créneau exact se vérifie sur les chiffres de l'utilisateur au bout d'un mois.

## Les 90 minutes qui décident

Le fil montre d'abord le post à une fraction des abonnés et mesure la vitesse des réactions : 20 commentaires en 30 minutes valent plus que 50 en 24 heures. Le rituel après publication :

```
T+0 à 5 min     répondre à chaque premier commentaire
T+5 à 15 min    commenter 5 à 10 posts de sa niche (des comptes plus gros que le sien)
T+15 à 30 min   revenir, répondre à tous les nouveaux commentaires
T+30 à 60 min   continuer chez les autres, répondre chez soi
T+1 à 2 h       dernier passage
```

On ne programme donc pas un post à une heure où l'on ne peut pas être là. Répondre vite fait commenter davantage (un commentaire de plus de 15 mots pèse plusieurs fois une réaction).

## Écrire en lot, programmer, être présent

1. Un créneau d'écriture par semaine (le vendredi ou le dimanche soir) : les 3 ou 4 posts de la semaine, validés, enregistrés dans `05_Departements/Marketing/Content-Brain/05_Calendrier-editorial/Brouillons/`.
2. Programmer : LinkedIn le fait nativement jusqu'à trois mois à l'avance ; avec Publora branché, le skill `planifier-post` programme depuis le chat, contrôle les bonnes pratiques (longueur, hook, lien en premier commentaire, créneau, collision) et tient `Calendrier.md`.
3. Les jours de publication ne servent qu'à la présence : 90 minutes d'engagement, pas d'écriture.
4. Une fois le post sorti : le fichier passe de `Brouillons/` à `Publies/`, avec `statut: publie`, `publie_le` et `url`. L'idée d'origine passe à `publiee`. Le skill `clean-content` relève ensuite les chiffres chaque semaine, les écrit dans le frontmatter et dans `Calendrier.md`, et note le post dans le champ `utilise_dans` des fiches qui ont servi.

## Méthode

1. Lire la cadence et les créneaux de `Strategie-contenu.md` ; s'ils sont vides, proposer 3 posts par semaine, mardi, mercredi, jeudi à 8h, et les écrire dans le fichier sur un oui.
2. Poser le calendrier de la semaine : jour, heure, type de post, pilier (le sous-skill `ideation` fournit les idées).
3. Vérifier la présence : l'utilisateur peut-il être là 90 minutes après chaque créneau ? Sinon déplacer.
4. Programmer avec `planifier-post` (Publora) ou donner les heures à saisir dans LinkedIn.
5. Après un mois, comparer les créneaux avec les chiffres (sous-skill `performance`) et ajuster.

## Exemples

- "Je poste deux fois par semaine, je veux grandir" : passer à 3 ou 4, mardi, mercredi, jeudi 7h30, un créneau du samedi 10h en plus ; 60 minutes bloquées après chaque post ; réponse attendue : le calendrier type et le rappel des 90 minutes.
- "Je n'arrive pas à être régulier" : écrire les 4 posts le dimanche soir, programmer mardi à vendredi 8h avec `planifier-post`, garder les matins pour répondre ; réponse attendue : le plan et la première commande de programmation en dry-run.
- "Mon audience est en France et au Québec" : 8h Paris pour la France, 8h Montréal (14h Paris) pour le Québec, avec deux posts différents ; réponse attendue : les deux créneaux et l'alternance des sujets.
