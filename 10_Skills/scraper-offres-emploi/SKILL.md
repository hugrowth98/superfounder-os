---
name: scraper-offres-emploi
description: >
  Exécute le verbe scraper_offres_emploi : les offres ouvertes d'un marché (mots-clés, lieu) ou
  d'entreprises précises, sur LinkedIn, Indeed ou Signalbase, avec un CSV par offre et un
  agrégat par entreprise (nombre d'offres, delta depuis le dernier run) où les cabinets,
  l'intérim, les ESN et les écoles sont écartés. Se déclenche sur : "qui recrute des SDR", "les
  boîtes qui cherchent un DAF à Lyon", "offres d'emploi ouvertes chez", "signal de recrutement",
  "combien de postes ouverts chez ces comptes", "qui embauche en ce moment". Ne pas utiliser
  pour : les autres signaux (voir `detecter-signaux` (script `detecter_signal.py`)), ni pour le nombre d'offres d'une seule
  entreprise déjà connue (voir `enrichir-entreprise`, colonne `nb_offres_emploi`).
---

## Outil

Apify uniquement, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md` :

| Besoin | `--source` | Actor | Coût vérifié |
|---|---|---|---|
| Mots-clés x lieux, offres récentes, ou ids d'entreprises LinkedIn | `linkedin` | `tagadanar/linkedin-jobs-scraper` | 0,0018 $ par offre (+0,0018 $ avec `--details`) |
| Requête + lieu + rayon + jours, comme dans la barre Indeed | `indeed` | `borderline/indeed-scraper` | 0,005 $ par offre |
| Marché entier avec filtres département et séniorité | `signalbase` | `signalbase/signalbase-api` (hiring) | 0,04 $ par résultat |

Pas de token Apify : dites-le et renvoyez vers `connecter-outils`.

## Entrée

Un ou plusieurs intitulés de poste (le poste dont l'ouverture est un signal pour l'offre de
l'utilisateur, section 4 de `05_Departements/Go-to-Market/contexte.md`), un lieu, une fenêtre (7 jours en routine
hebdomadaire), ou des ids numériques d'entreprises LinkedIn (`f_C=` dans l'URL de leur page
Jobs).

## Sortie

Deux fichiers dans `Listes-prospection/` :

- `scraper-offres-emploi_<sujet>_<date>.csv`, une ligne par offre : `entreprise`, `domaine`,
  `linkedin_entreprise_url`, `ville`, `pays`, `secteur`, `effectif`, `source` (nom de l'actor),
  `date_extraction`, `signal_type` (`recrutement`), `signal_date`, `signal_detail`, `fraicheur`,
  plus `poste`, `url_offre`, `type_contrat`, `teletravail`, `salaire`, `niveau`, `nb_candidats`,
  `plateforme`, `statut_entreprise` (`client_final`, `a_verifier`, `exclu`), `raison_statut`.
- `..._par-entreprise.csv`, une ligne par entreprise non exclue : `nb_offres`,
  `nb_offres_precedent`, `delta`, `premiere_vue`, `dernier_run`, postes dans `signal_detail`,
  trié par delta puis volume. L'historique vit dans `scripts/historique_offres.json`.

## Procédure

1. Choisissez la source : Indeed pour un métier précis dans une zone (PME, ETI), LinkedIn pour
   les postes tertiaires et les entreprises identifiées, Signalbase pour un marché large.
2. Dry-run, annoncez volume et coût, attendez le oui :
   `python3 scripts/scraper_offres_emploi.py --source indeed --mots-cles "responsable comptable" --lieu Lyon --jours 7 --max 200 --dry-run`
   `python3 scripts/scraper_offres_emploi.py --source linkedin --mots-cles "SDR,Business Developer" --lieu Paris --depuis week --max 200 --dry-run`
   `python3 scripts/scraper_offres_emploi.py --source linkedin --entreprises-ids 1441,10667 --max 100 --dry-run`
   `python3 scripts/scraper_offres_emploi.py --source signalbase --pays FR --search "SDR" --departements sales --periode last_7d --limite 100 --dry-run`
3. Relancez sans `--dry-run`. Le script garde les offres au titre exact (tous les fragments du
   mot-clé dans le titre), classe chaque entreprise contre `intermediaires-exclus.csv` et les
   mots suspects (recrutement, intérim, portage, école, alternance, ESN, conseil), puis agrège.
4. Point de contrôle : ouvrez les lignes `a_verifier`. Une petite structure qui publie quatre
   fois la même annonce est un cabinet ; un cabinet d'expertise comptable recrute pour lui-même
   (client final). Ajoutez les intermédiaires confirmés : `--exclure "Cabinet X,Interim Y"` lors
   du prochain run, la liste connue grandit.
5. Lisez l'agrégat : `delta` positif = l'entreprise a ouvert des postes depuis le dernier run,
   `premiere_vue = oui` = pas encore de référence (le delta ne vaut rien au premier passage,
   dites-le).
6. Lien cliquable vers les deux fichiers, un seul next step : `qualifier-liste` sur l'agrégat,
   puis `trouver-personnes` (le décideur du poste ouvert : DAF pour un comptable, DRH pour un
   recruteur, dirigeant en dessous de 200 salariés).

## Garde-fous

- Coût annoncé avant tout run ; `--max` à ce que la zone justifie (200 offres Indeed = 1 $).
- Les offres publiées par un intermédiaire ne sont jamais un signal sur le client final : elles
  restent dans le fichier avec `statut_entreprise = exclu`, jamais dans l'agrégat.
- `--sans-filtre-titre` seulement si l'utilisateur veut un panorama : sinon "Comptable unique"
  n'est pas "Responsable comptable".
- Le delta compare au dernier run enregistré, quel que soit le mot-clé : pour un suivi propre,
  gardez un `--sujet` par recherche et lancez à la même fréquence.
- Rien d'inventé : pas de domaine ni d'URL LinkedIn déduits du nom ; `enrichir-entreprise` les
  complète.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Indeed : 0 offre | lieu non compris ou métier trop précis | tester l'URL affichée par le dry-run dans un navigateur, élargir le mot-clé |
| Beaucoup d'offres brutes, 0 au titre exact | intitulé Indeed différent du métier | relancer avec un mot-clé plus court ("comptable") ou `--sans-filtre-titre` |
| LinkedIn : offres hors zone | lieu ambigu | nom complet ("Paris, Île-de-France, France") |
| Tout en `a_verifier` | mots suspects trop larges pour ce secteur (conseil, formation) | classer à la main puis `--exclure` les vrais intermédiaires |
| `delta` vide partout | premier run | normal, relancer la semaine suivante |
| Actor `TIMED-OUT` | trop de recherches dans un run | découper les mots-clés en plusieurs runs |
