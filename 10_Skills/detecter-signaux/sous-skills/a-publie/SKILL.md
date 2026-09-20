---
name: a-publie
description: >
  Repère, dans une cible ICP, les personnes qui ont publié sur LinkedIn dans les 30 derniers jours
  (filtre Sales Navigator "A publié sur LinkedIn") : elles sont joignables sur LinkedIn et leur
  dernier post donne l'accroche. Se déclenche sur : "qui a publié récemment", "les CMO actifs sur
  LinkedIn", "ceux qui postent", "actifs sur LinkedIn", "qui publie dans ma cible", "nouveau post".
  Ne pas utiliser pour les réactions à vos posts (voir `engagement-contenu`), pour le contenu d'un
  concurrent (voir `signaux-concurrents`), ni pour un changement de poste (voir `changement-poste`).
---

Une personne qui a publié ce mois-ci lit ses notifications, répond aux commentaires et ouvre ses messages : LinkedIn est le canal qui marche pour elle, et son post dit de quoi elle parle en ce moment. Ce n'est pas un signal d'achat, c'est un signal d'accessibilité et une source d'accroche : 10 points (proposé), toujours empilé, jamais seul.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : a publié récemment 10, à empiler.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : a publié j0 à j7 après le post, frais 30 jours.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 11 (engageurs), et la voie inverse, s'engager d'abord.
- `10_Skills/cold-email/ressources/seaux-personnalisation.md` : seau 1, le contenu auto-produit, le hook fort.

## Méthode

1. **Partir d'une cible ICP**, pas d'un signal : titres du persona, zone, effectif. Le filtre `--a-publie` ne fait que trier les joignables. Sur une cible de 1 000 personnes, 100 à 200 ont publié dans le mois.
2. **Lancer par campagne** (ou chaque mois) avec votre compte ou vos cookies. Le filtre est public : il marche avec n'importe quel compte Sales Navigator.
3. **Qualifier.** ICP, exclusions. Et sortez les créateurs de contenu professionnels (coachs, agences de contenu) si votre offre ne les vise pas : ils publient tous les jours.
4. **Lire le dernier post** : `enrichir-personne --posts` rend les 5 derniers dans `posts_recents`. C'est la matière de l'accroche (seau 1). Un post sans lien avec votre sujet ne donne pas d'angle : la ligne retombe dans la cible froide.
5. **Dater.** `signal_date` = date du run ; la date du post se lit dans `posts_recents`. Fenêtre j0 à j7 après le post, frais 30 jours.
6. **S'engager d'abord**, à la main : un vrai commentaire sous le post, 24 h avant le message. C'est la seule étape sans script, et c'est celle qui fait répondre.
7. **Choisir l'angle** : l'idée du post, continuée ("vous écriviez que..., je vois la même chose chez..."), puis la question sur son cas. Le post se cite, la publication ne se commente pas ("j'ai vu que vous étiez actif").
8. **Envoyer sur LinkedIn**, invitation avec note ou message, puis email à j5 si le canal existe. Dans `multi-signaux`, les 10 points servent de départageur : à score égal, on écrit d'abord à celui qui publie.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1 | construire_requete_salesnav | `construire-requete-salesnav` | `--persona atl --region France --effectif 11-50,51-200 --a-publie --nom "ATL actifs" --enregistrer` |
| 2 | trouver_personnes | `trouver-personnes` | `--source unipile --url "<url>" --signal a_publie --max 300` (ou `--source salesnav`, 0,005 $ par résultat) |
| 3 | qualifier_liste | `qualifier-liste` | ICP, exclusions, créateurs de contenu hors cible |
| 4 | enrichir_personne | `enrichir-personne` | `--posts` : `posts_recents` (les 5 derniers), `anciennete_poste` (second signal possible) |
| 5 | dedoublonner | `dedoublonner` | contre HubSpot et les séquences en cours |
| 6 | à la main | | un commentaire sous le dernier post, 24 h avant le message |
| 7 | envoyer_sequence | `envoyer-sequence` | LinkedIn j0 (`--colonne-message ouverture` avec l'accroche tirée du post), email j5 |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : aucun, la requête suffit.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`a_publie`), `signal_date` (date du run), `signal_detail` ("a publié sur LinkedIn dans les 30 derniers jours (Sales Navigator)"), `fraicheur`, `source`, puis `posts_recents` après l'étape 4. Nom : `trouver-personnes_actifs-<persona>_<date>.csv`.

## Repères

| Repère | Valeur |
|---|---|
| Points | 10 (proposé), départageur, jamais seul |
| Fenêtre | j0 à j7 après le post, frais 30 jours |
| Part d'une cible qui publie dans le mois | 10 à 20 % |
| Étape manuelle | un commentaire par personne, 24 h avant le message |
| Canal | LinkedIn d'abord, email à j5 |

## Template

```
Cible : <persona>, <zone>, <effectif> ; filtre : a publié dans les 30 jours
Run du <date> : <n> personnes, <n> dans l'ICP, <n> avec un post lié à votre sujet
Par ligne : post du <date> sur <idée>, commentaire posté le <date>, message le <date>
Accroche : "<l'idée du post en une phrase>, ..." puis la question
```

## Règles

- Ce filtre trie, il ne qualifie pas : l'ICP passe avant.
- Un post sans lien avec votre sujet n'est pas une accroche : pas de personnalisation forcée.
- Le commentaire précède le message, et c'est un vrai commentaire, pas "super post".
- "J'ai vu que vous étiez actif sur LinkedIn" ne s'écrit jamais.
- Les 10 points ne font pas passer une ligne Chaud : ils départagent.

## Exemples

- "Les CMO actifs sur LinkedIn en France" : requête `--titres CMO --region France --a-publie`, run, qualification, `--posts` ; réponse attendue : une liste avec le dernier post et l'accroche par ligne, et les lignes sans angle marquées.
- "Priorise ma liste de 300 dirigeants" : la même liste passée par le filtre, puis `multi-signaux` ; réponse attendue : les 40 qui publient en tête à score égal, avec leur post.
- "Écris à ce fondateur qui poste beaucoup" : `enrichir-personne --posts`, commentaire d'abord, message le lendemain ; réponse attendue : le commentaire, puis l'invitation avec note qui continue son idée.
