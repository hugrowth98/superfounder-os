---
name: scraper-engagement
description: >
  Exécute le verbe scraper_engagement : récupère les personnes qui ont commenté ou réagi à un ou
  plusieurs posts LinkedIn (les vôtres, ceux d'un concurrent, d'un event, d'un sujet de votre
  marché), une ligne par personne et par post avec `signal_type` commentaire ou like et le texte du
  commentaire. Se déclenche sur : "qui a liké ce post", "qui a commenté", "récupère les engagers",
  "l'audience de ce post concurrent", "les gens qui ont réagi à mon live", "scrape les
  commentaires de". Ne pas utiliser pour : répondre aux commentaires, lister les posts d'une
  entreprise, ou les signaux hors LinkedIn (voir `detecter-signaux` (script `detecter_signal.py`)).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. Principal : Unipile, `GET /api/v1/posts/{id}/reactions` et `/comments` avec le
compte LinkedIn de l'utilisateur (abonnement, pas de crédit, jusqu'à 10 pages de 100 par type).
Secours (pas de compte Unipile, ou `canal_linkedin: lemlist`) : Apify
`harvestapi/linkedin-post-comments` (0,002 $ par commentaire) et
`harvestapi/linkedin-post-reactions` (0,002 $ par réaction), sans cookies. Rien de branché :
dites-le, renvoyez vers `connecter-outils`.

## Entrée

Une ou plusieurs URLs de posts, copiées via "Copier le lien" (formats
`linkedin.com/posts/<handle>_<slug>-activity-<id>-<suffixe>` ou
`linkedin.com/feed/update/urn:li:activity:<id>/`). Un fichier texte avec une URL par ligne pour
une série (les 5 derniers posts d'un concurrent, les posts d'un event).

## Sortie

`Listes-prospection/scraper-engagement_<sujet>_<date>.csv`, une ligne par personne et par post :
`prenom`, `nom`, `titre`, `seniorite`, `linkedin_url`, `source` (`unipile` ou nom de l'actor),
`date_extraction`, `signal_type` (`commentaire` ou `like`), `signal_date`, `signal_detail` (texte
du commentaire, ou "a réagi (LIKE) au post"), `fraicheur`, plus `post_url`, `reaction_type`
(LIKE, APPRECIATION, EMPATHY, PRAISE, INTEREST...), `commentaire_id`, `nb_likes_commentaire`,
`nb_posts_engages` (la même personne sur plusieurs posts), `provider_id` et `degre_relation`
(Unipile). Commentaires d'abord, puis réactions.

## Procédure

1. Vérifiez l'URL : le script refuse un lien sans id de post. Dry-run :
   `python3 scripts/scraper_engagement.py --post "<url>" --dry-run`
2. Lancez. Exemples :
   `python3 scripts/scraper_engagement.py --post "<url>"` (commentaires + réactions, Unipile)
   `python3 scripts/scraper_engagement.py --posts posts.txt --type commentaires`
   `python3 scripts/scraper_engagement.py --post "<url>" --source apify --max 500`
3. Lisez les compteurs : total, commentaires, réactions. Un total inférieur au compteur affiché
   sur LinkedIn vient d'un id de post ambigu (activity, ugcPost, share) ou d'un post de plus de
   1 000 réactions : dites-le, c'est partiel mais utilisable.
4. Priorisez pour la suite : commentaires, puis réactions fortes (APPRECIATION, PRAISE,
   INTEREST), puis LIKE ; `nb_posts_engages` supérieur à 1 vaut un signal empilé.
5. Lien cliquable, un seul next step : `qualifier-liste` (les engagers hors ICP sont nombreux),
   puis `enrichir-personne` sur les tiers A et B avant tout message.

Post d'un concurrent ou d'un sujet stratégique : le commentaire est un signal d'intérêt daté,
`signal_detail` sert d'accroche dans `cold-email` (citer ce que la personne a écrit, jamais
inventer).

## Garde-fous

- Unipile lit avec le compte de l'utilisateur : pas plus de 10 posts par jour, pas de boucle sur
  les posts d'un même auteur en rafale.
- Les auteurs de type entreprise (pages) sont gardés avec `type_auteur` renseigné : les écarter
  dans `qualifier-liste`, pas de message à une page.
- Aucune réponse ni réaction n'est envoyée par ce skill : lecture seule.
- Un commentaire cité dans un message reste fidèle au texte de `signal_detail`.
- Rien d'inventé : personne sans URL LinkedIn, colonne vide, à compléter par `enrichir-personne`.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `Impossible d'extraire l'id du post` | lien raccourci ou lien de profil | recopier via "Copier le lien" sur le post |
| Total très inférieur au compteur LinkedIn | mauvais format d'id pour ce post | passer l'URN (`urn:li:ugcPost:<id>`) ou utiliser `--source apify` |
| 401 Unipile | compte LinkedIn déconnecté | `connecter-outils` étape 2 |
| Apify : 0 résultat | post privé ou supprimé | vérifier dans un navigateur non connecté |
| Doublons entre deux runs | même post relancé | `dedoublonner` sur `linkedin_url` + `post_url` |
