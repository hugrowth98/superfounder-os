---
name: export-salesnav
description: >
  Skill pour exporter une recherche Sales Navigator ou LinkedIn classique en CSV exploitable
  (colonnes normalisees : nom, entreprise, headline, URL LinkedIn...). Utilise ce skill des
  que l'utilisateur veut exporter des resultats de recherche LinkedIn/Sales Nav en fichier.
  Se declenche sur : "exporte cette recherche Sales Nav", "exporte cette liste LinkedIn en
  CSV", "sors-moi un fichier de ces resultats LinkedIn".
---

# Exporter une recherche Sales Navigator ou LinkedIn en CSV

## Vue d'ensemble

Meme mecanisme technique que `recherche-salesnav` (meme endpoint Unipile), avec en plus la
normalisation des resultats et l'ecriture d'un CSV propre. Un seul skill couvre Sales
Navigator, recherche classique ET Recruiter : seul le parametre `--api` change.

## Workflow

### Etape 1 - Recuperer l'URL ou les criteres

Identique a `recherche-salesnav` : URL Sales Nav copiee, ou mots-cles.

### Etape 2 - Exporter

```bash
python3 .claude/skills/export-salesnav/scripts/client.py "<account_id>" \
  "https://www.linkedin.com/sales/search/people?..." \
  "output/salesnav-export.csv" \
  --category people --max 100
```

Pour une recherche LinkedIn classique plutot que Sales Nav : `--api classic`.
Pour cibler des entreprises plutot que des personnes : `--category companies`.

### Etape 3 - Resumer

Nombre de lignes exportees, chemin du CSV, chemin du JSON brut (garde en complement pour
verification/debug). Proposer l'etape suivante : "Je peux qualifier cette liste avec
`qualifier-liste`."

## Colonnes du CSV de sortie

**Personnes** : `first_name, last_name, headline, company, location, linkedin_url,
linkedin_slug, provider_id, network_distance`

**Entreprises** : `name, industry, location, employee_count, linkedin_url`

## Notes

- `provider_id` est l'identifiant interne Unipile du profil, necessaire pour
  `envoyer-invitation` et `envoyer-dm` (ce n'est pas l'URL LinkedIn).
- Le CSV separe automatiquement prenom/nom et retire les emojis du nom.
