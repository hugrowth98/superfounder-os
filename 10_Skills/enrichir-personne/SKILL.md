---
name: enrichir-personne
description: >
  Exécute le verbe enrichir_personne : complète chaque ligne d'un CSV de personnes avec son profil
  LinkedIn (poste actuel, entreprise, ancienneté, expériences, localisation, headline) via Unipile,
  puis le contact vérifié (email pro, mobile) via FullEnrich. Se déclenche sur : "enrichis ces
  contacts", "complète les profils", "récupère le poste actuel de", "ancienneté dans le poste",
  "profil complet de ces personnes", "il me manque l'entreprise de ces gens". Ne pas utiliser
  pour : trouver de nouvelles personnes (voir `trouver-personnes`), un email seul (voir
  `trouver-email`), un téléphone seul (voir `trouver-telephone`), une entreprise (voir
  `enrichir-entreprise`).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. Profil : Unipile `GET /api/v1/users/{identifiant}` avec le compte LinkedIn de
l'utilisateur (priorités apify et api), secours Apify `harvestapi/linkedin-profile-scraper`
(0,004 $ par profil, sans compte LinkedIn). Contact : FullEnrich `POST /contact/enrich/bulk`,
seul outil d'enrichissement contact de la stack (1 crédit par email pro trouvé, 10 par mobile,
facturé au résultat, gratuit sous 3 mois pour un contact déjà enrichi). Rien de branché : dites
lequel manque, renvoyez vers `connecter-outils`, ne simulez rien.

## Entrée

Un CSV normalisé de personnes avec `linkedin_url` (ou `provider_id` Unipile). Pour la partie
contact il faut `prenom` + `nom` + (`entreprise` ou `domaine`), ou `linkedin_url`. Enrichissez
seulement les tiers A et B : le profil coûte des vues LinkedIn, le contact coûte des crédits.

## Sortie

`Listes-prospection/enrichir-personne_<sujet>_<date>.csv`, mêmes lignes que l'entrée (jamais
écrasée), colonnes normalisées complétées (`prenom`, `nom`, `titre`, `seniorite`, `entreprise`,
`domaine`, `linkedin_entreprise_url`, `email`, `email_statut`, `telephone`, `ville`, `pays`)
plus `headline`, `resume`, `anciennete_poste`, `experiences` (4 dernières), `formation`,
`competences`, `langues`, `nb_relations`, `abonnes`, `degre_relation`, `provider_id`,
`ouvert_au_poste`, `recrute`, `date_enrichissement`, `erreur_enrichissement` ; avec `--posts`, `posts_recents`
(les 5 derniers posts de la personne via Unipile, séparés par ` || `).

## Procédure

1. Comptez les lignes à traiter : le script ne relance que les lignes sans `date_enrichissement`
   (profil) et sans `email` ou avec un `email_statut` invalide (contact).
2. Dry-run, montrez le nombre et le coût :
   `python3 scripts/enrichir_personne.py --in <csv> --contact --dry-run`
3. Attendez le oui, puis :
   profil seul : `python3 scripts/enrichir_personne.py --in <csv>`
   profil + email : `... --contact`
   profil + email + mobile (10 crédits par mobile, à réserver aux tiers A pour le téléphone) :
   `... --contact --telephone`
   sans compte LinkedIn connecté : `... --source apify`
   contact seul sur un fichier déjà profilé : `... --sans-profil --contact`
4. Relisez 3 lignes : le `titre` vient du poste actuel (pas du headline marketing), l'entreprise
   correspond à la ligne d'origine. Un changement d'entreprise entre la source et le profil est
   une information (la personne a bougé), signalez-la.
5. Lien cliquable, compteurs (profils enrichis, emails trouvés, crédits facturés), un seul next
   step : `trouver-email` s'il reste des lignes sans email, sinon `cold-email`.

Lots de plus de 100 profils Unipile : `--max 100` par run et une pause d'une heure entre deux
runs. FullEnrich traite par lots de 100 avec polling automatique.

## Garde-fous

- Ne relance que si vide : une valeur déjà présente n'est jamais écrasée (sauf `titre`, mis à
  jour au poste actuel). `--force` seulement sur demande explicite.
- Unipile : chaque lecture est une vue de profil depuis le compte de l'utilisateur. Pause 1,5 s
  entre deux profils, 300 par jour maximum, jamais en boucle sur une liste non qualifiée.
- FullEnrich : coût maximal et coût estimé affichés avant le run, solde vérifié, arrêt si le
  solde ne couvre pas l'estimation. Au-delà de 100 crédits estimés, une validation explicite en
  plus.
- Les emails et téléphones visibles sur un profil de 1er degré arrivent avec le statut
  `LINKEDIN_1ER_DEGRE` : non vérifiés, à passer par `trouver-email` avant un envoi.
- Aucune donnée inventée : profil introuvable = `erreur_enrichissement` remplie, ligne conservée.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `UNIPILE_ACCOUNT_ID absent` | compte LinkedIn pas relié dans Unipile | `connecter-outils` étape 2 |
| 404 sur un profil | slug d'URL faux ou profil fermé | corriger `linkedin_url`, sinon la ligne reste avec `erreur_enrichissement` |
| 429 Unipile | trop de lectures d'affilée | attendre 15 minutes, relancer (les lignes déjà faites sont sautées) |
| FullEnrich `sans_cle_de_match` élevé | lignes sans prénom + nom + entreprise ni URL | passer d'abord par `trouver-personnes` ou corriger les colonnes |
| `email_statut = NOT_FOUND` | FullEnrich n'a rien trouvé, pas facturé | tenter `trouver-email --force` dans 3 mois, ou passer au téléphone |
| Apify : profil absent du résultat | URL non publique ou renommée | vérifier l'URL dans un navigateur |
