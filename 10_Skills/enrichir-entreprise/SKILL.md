---
name: enrichir-entreprise
description: >
  Exécute le verbe enrichir_entreprise : complète chaque ligne d'un CSV d'entreprises avec le
  firmographique (secteur, effectif, siège, année de création, type), le site, la page LinkedIn,
  et selon la source le nombre d'offres ouvertes et le chiffre d'affaires estimé. Se déclenche
  sur : "enrichis ces entreprises", "il me manque l'effectif", "récupère la page LinkedIn de ces
  boîtes", "fiche entreprise", "combien d'employés chez", "complète ma liste de comptes". Ne pas
  utiliser pour : trouver des entreprises (voir `trouver-entreprises`), la stack technique (voir
  `enrichir-entreprise --techno`), les personnes (voir `enrichir-personne`).
  Porte aussi les verbes detecter_techno (`--techno` : stack technique d'un domaine, mode diff) et scraper_pubs (`--pubs` : pubs actives Meta et LinkedIn). Se déclenche aussi sur : "quelle stack ils utilisent", "ils sont sur HubSpot ?", "ils font de la pub", "leurs pubs actives", "qui a changé d'outil".
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. Priorité apify comme api : Unipile `GET /api/v1/linkedin/company/{id}` d'abord
(page LinkedIn lue avec le compte de l'utilisateur, résolution par nom si l'URL manque), puis
Crustdata `GET /screener/company?company_domain=` pour ce que LinkedIn n'a pas (offres ouvertes,
CA estimé, stade de financement). Secours : Apify `harvestapi/linkedin-company` (0,004 $ par
entreprise, par URL LinkedIn ou par nom, sans compte LinkedIn). Rien de branché : dites lequel
manque, renvoyez vers `connecter-outils`, ne simulez rien.

| `--source` | Outil | Coût | Apporte |
|---|---|---|---|
| `unipile` (défaut) | Unipile page entreprise | abonnement | nom, site, secteur, effectif et tranche, siège, abonnés, année, type, spécialités, description |
| `crustdata` | Crustdata screener/company | 1 crédit (cache) ou 4 (temps réel) par entreprise | idem + `nb_offres_emploi`, `chiffre_affaires_estime`, `stade_financement` |
| `apify` | `harvestapi/linkedin-company` | 0,004 $ par entreprise | même contenu que la page LinkedIn, sans compte |

Les sources se cumulent (`--source unipile,crustdata`) : chacune ne remplit que ce qui est vide.

## Entrée

Un CSV normalisé d'entreprises avec `entreprise` et, si possible, `linkedin_entreprise_url` ou
`domaine`. Sans les deux, Unipile et Apify cherchent par nom (risque d'homonyme, à relire).

## Sortie

`Listes-prospection/enrichir-entreprise_<sujet>_<date>.csv`, mêmes lignes que l'entrée, colonnes
normalisées complétées (`entreprise`, `domaine`, `linkedin_entreprise_url`, `ville`, `pays`,
`secteur`, `effectif`) plus `effectif_tranche`, `site_web`, `abonnes`, `annee_creation`, `type`,
`specialites`, `telephone_entreprise`, `tagline`, `description`, `nb_offres_emploi`,
`chiffre_affaires_estime`, `stade_financement`, `unipile_id`,
`date_enrichissement_entreprise`, `erreur_enrichissement_entreprise`.

## Procédure

1. Dry-run : `python3 scripts/enrichir_entreprise.py --in <csv> --dry-run` (par défaut Unipile,
   ou Unipile puis Crustdata si `priorite: api`). Le script ne traite que les lignes sans
   `date_enrichissement_entreprise`.
2. Annoncez le nombre de lignes et le coût (Crustdata et Apify seulement), attendez le oui.
3. Lancez. Exemples :
   `python3 scripts/enrichir_entreprise.py --in <csv>`
   `python3 scripts/enrichir_entreprise.py --in <csv> --source unipile,crustdata --max 100`
   `python3 scripts/enrichir_entreprise.py --in <csv> --source apify`
4. Relisez les lignes enrichies par nom (sans URL ni domaine en entrée) : comparez `site_web` et
   `domaine` d'origine, un écart signale un homonyme.
5. Lien cliquable, compteur par source, un seul next step : `qualifier-liste` (le score ICP a
   besoin du secteur et de l'effectif) ou `trouver-personnes` si la liste est déjà qualifiée.

Pour un signal de recrutement chiffré (delta d'offres entre deux runs), passez plutôt par
`scraper-offres-emploi`, qui tient un historique par entreprise.

## Options techno et pubs

Deux enrichissements de plus, sur le même CSV, sans skill séparé :

| Option | Verbe | Ce que ça ajoute | Actor Apify | Coût |
|---|---|---|---|---|
| `--techno` | detecter_techno | une colonne par catégorie (`cms`, `ecommerce`, `analytics`, `marketing`, `chat`, `crm`, `paiement`, `hebergement`, `framework`), `technos`, `techno_cible` avec `--cherche`, et le mode `--diff` (ajouts, retraits depuis le dernier run) | `scrapemint/website-tech-stack-detector` | 0,01 $ par domaine détecté |
| `--pubs` | scraper_pubs | une ligne par pub active : plateforme, dates, texte, CTA, page d'atterrissage | `curious_coder/facebook-ads-library-scraper`, `s-r/linkedin-ads-library` | 0,00075 $ (Meta) et 0,005 $ (LinkedIn) par pub |

```
python3 scripts/enrichir_entreprise.py --in <csv> --techno --cherche "hubspot,pipedrive" --dry-run
python3 scripts/enrichir_entreprise.py --in <csv> --sans-base --pubs --plateforme meta --dry-run
python3 scripts/enrichir_entreprise.py --in Signaux/comptes-suivis.csv --sans-base --techno --diff
```

`--sans-base` saute l'enrichissement de base et ne fait que l'option. Chaque option écrit son propre CSV (`enrichir-entreprise_techno_...`, `enrichir-entreprise_pubs_...`). Procédure détaillée, lecture des colonnes, garde-fous et erreurs : `techno.md` et `pubs.md` dans ce dossier. Règle commune : on ne déduit jamais une absence ("ils n'utilisent pas X", "ils ne font pas de pub"), seulement ce qui a été vu.

## Garde-fous

- Ne relance que si vide : aucune valeur existante n'est écrasée, `--force` seulement sur demande.
- Unipile : une lecture par entreprise depuis le compte de l'utilisateur, pause 1 s, 300 par jour
  au plus, `--max` pour découper.
- Crustdata facture au résultat : dry-run obligatoire au-delà de 50 lignes, solde affiché.
- Une entreprise introuvable garde sa ligne avec `erreur_enrichissement_entreprise` : rien n'est
  deviné, ni effectif ni secteur.
- `effectif` reçoit le nombre exact quand il existe, sinon la tranche ("11-50") : les deux sont
  lisibles par `qualifier-liste`.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Unipile 404 même après recherche | nom trop générique ou page inexistante | fournir `linkedin_entreprise_url`, ou passer `--source apify` avec le nom exact |
| Effectif LinkedIn très différent du réel | profils rattachés à la page, pas l'effectif déclaré | lire `effectif_tranche` (déclarée) pour le scoring |
| Crustdata : ligne ignorée | pas de `domaine` | enrichir d'abord avec Unipile (donne `site_web`), relancer Crustdata |
| Apify : "non trouvee par l'actor" | URL renommée ou page fusionnée | vérifier dans un navigateur, corriger l'URL |
| Deux lignes pour la même entreprise après enrichissement | doublons en entrée (nom et URL différents) | `dedoublonner` avant d'enrichir |
