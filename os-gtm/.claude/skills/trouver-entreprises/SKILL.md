---
name: trouver-entreprises
description: >
  Skill pour rechercher des entreprises par criteres (secteur, taille, localisation,
  mots-cles) via l'API Crustdata, et exporter le resultat en CSV. Utilise ce skill des que
  l'utilisateur veut trouver des entreprises cibles pour son ICP compte par compte. Se
  declenche sur : "trouve-moi des entreprises", "cherche des boites qui...", "liste-moi les
  entreprises dans tel secteur", "trouve des comptes cibles".
---

# Trouver des entreprises (Crustdata)

## Vue d'ensemble

**Base URL** : `https://api.crustdata.com`
**Auth** : header `Authorization: Token $CRUSTDATA_API_KEY`, cle chargee depuis le `.env`
racine.
**Endpoint** : `POST /v1/companies/search`

## Workflow

### Etape 1 - Construire les criteres a partir de contexte.md

Lire la section 2 (ICP) de `contexte.md` : secteur, taille d'entreprise, zone geographique.
Si l'utilisateur donne une cible dans sa phrase ("des PME SaaS en France"), l'utiliser en
priorite ; sinon se rabattre sur `contexte.md`.

### Etape 2 - Valider les noms de filtres (optionnel, gratuit)

Avant une recherche large, on peut valider les valeurs de filtres avec l'autocomplete gratuit :
```bash
curl -sS -H "Authorization: Token $CRUSTDATA_API_KEY" \
  "https://api.crustdata.com/screener/company/search/autocomplete/?field=industry&query=SaaS"
```

### Etape 3 - Lancer la recherche

```bash
python3 .claude/skills/trouver-entreprises/scripts/client.py search \
  --industry "Software Development" \
  --employee-range "11-50" \
  --location "France" \
  --limit 50 \
  --out "output/entreprises.csv"
```

Tous les parametres sont optionnels sauf au moins un critere. `--limit` par defaut 50.

### Etape 4 - Resumer

Nombre d'entreprises trouvees, chemin du CSV, 2-3 exemples de noms trouves pour validation
rapide par l'utilisateur. Proposer l'etape suivante : "Je peux chercher les decisionnaires
de ces entreprises avec `trouver-personnes`, ou verifier les signaux de recrutement avec
`scraper-offres-emploi`."

## Colonnes du CSV de sortie

`name, website, industry, employee_count, hq_country, company_type, description,
funding_stage, linkedin_url, year_founded`

## Cout

1 credit par recherche (DB), environ 2 credits en mode live. Verifier le solde avant un
batch important :
```bash
curl -sS -H "Authorization: Token $CRUSTDATA_API_KEY" https://api.crustdata.com/user/credits
```

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle invalide | verifier `CRUSTDATA_API_KEY` dans le `.env` racine |
| 402 | credits insuffisants | alerter l'utilisateur et arreter |
| 429 | rate limit | attendre et reessayer |
