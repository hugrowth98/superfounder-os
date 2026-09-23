---
name: performance
description: >
  Lit les chiffres des posts de l'utilisateur pour trouver ce qui marche chez lui : classe ses
  posts en tiers par rapport à sa propre moyenne, sort les patterns gagnants (type de hook,
  longueur, format, appel, pilier, jour), le ratio commentaires sur réactions, et met à jour
  `posts-de-reference.md` avec les enseignements. Se déclenche sur : "qu'est-ce qui marche
  chez moi", "analyse mes posts", "mes meilleurs posts", "pourquoi ce post a marché", "quelle
  longueur me réussit", "bilan du mois". Ne pas utiliser pour classer les posts des autres
  (sous-skill `veille-createurs`, ou `publications-entreprise` pour une page entreprise).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture.

# Performance

Les repères du master (longueurs, créneaux, multiplicateurs) valent jusqu'à ce que l'utilisateur ait ses propres chiffres. Vingt posts suffisent pour voir un pattern ; quarante pour lui faire confiance. La méthode complète est dans `{SKILL_BASE}/ressources/analyse-performance.md`.

## Les données

Trois façons de les obtenir, de la plus simple à la plus complète :

1. **Collées par l'utilisateur** : pour chaque post, le texte (ou le hook), la date, les impressions, les réactions, les commentaires, les enregistrements si visibles, le format.
2. **Depuis `posts-de-reference.md`** : les posts qui y sont déjà avec leurs résultats.
3. **Par les outils** : avec Unipile branché, `scraper-engagement --mes-posts 40` liste ses derniers posts avec réactions et commentaires ; avec Publora branché, `planifier-post --stats <postGroupId>` donne impressions, personnes atteintes, réactions, commentaires et partages d'un post programmé par lui.

## Les tiers, relatifs à sa propre moyenne

| Tier | Seuil (engagement total : réactions + commentaires x 2) | Ce qu'on y cherche |
|---|---|---|
| S | 2,5 fois la moyenne et plus | le pattern à rejouer cinq fois |
| A | 1,5 à 2,5 fois | les variantes qui confirment |
| B | 0,8 à 1,5 fois | la base, ce qui est fiable |
| C | 0,4 à 0,8 fois | ce qui passe sans marquer |
| D | moins de 0,4 fois | ce qu'on arrête, ou ce qu'on refait autrement |

Le ratio commentaires sur réactions dit quel genre d'audience on a : au-dessus de 1, une audience qui parle (viser les questions, les débats, les ressources contre un mot) ; en dessous de 0,5, une audience qui lit (viser l'enregistrement, les cadres, les carrousels).

## Ce qu'on croise

Pour chaque tier : le type de hook (miroir de douleur, chiffre, contradiction, scène...), le type de post (éducatif, storytelling, opinion, lead magnet), la longueur, le format (texte, carrousel, image, vidéo), la fin (question, mot-clé, enregistrement), le pilier, le jour et l'heure. Un pattern existe quand trois posts au moins du tier S ou A partagent le même trait, et que le tier D ne l'a pas.

Les patterns les plus souvent observés sur des comptes B2B, à vérifier chez l'utilisateur : la vulnérabilité (un échec raconté) dépasse tout le reste ; un chiffre précis dans le hook ; une ressource contre un mot-clé ; un contrepied sur une croyance de la niche ; un visuel qui accompagne ; la longueur la plus courte pour une audience tactique, la plus longue pour une audience qui veut le détail.

## Méthode

1. Rassembler au moins 20 posts avec leurs chiffres (les trois sources ci-dessus).
2. Calculer la moyenne d'engagement, classer en tiers, noter le ratio commentaires sur réactions.
3. Étiqueter chaque post (hook, type, longueur, format, fin, pilier, jour) et repérer les traits communs des S et A absents des D.
4. Écrire cinq enseignements au plus, chacun avec les posts qui le prouvent, et trois hypothèses à tester le mois suivant.
5. Sur un oui, mettre à jour `posts-de-reference.md` (section "Ce qui marche chez vous", les posts S et A avec leurs chiffres) et, si la cadence ou les créneaux changent, `strategie-contenu.md`.
6. Rejouer : les S en carrousel et en vidéo (sous-skill `recycler`), les patterns dans les prochains hooks (sous-skill `hooks`).

## Exemples

- "Voilà mes 30 derniers posts avec leurs chiffres" : tiers, ratio, cinq enseignements, trois tests ; réponse attendue : un tableau court, les enseignements avec preuves, la mise à jour proposée de `posts-de-reference.md`.
- "Pourquoi ce post a marché ?" : le comparer aux S et A existants sur les sept traits ; réponse attendue : les deux ou trois traits qu'il partage avec les gagnants, et la façon de le rejouer.
- "Quelle longueur me réussit ?" : la longueur moyenne par tier ; réponse attendue : une fourchette propre à l'utilisateur, remplaçant le repère générique du master.
