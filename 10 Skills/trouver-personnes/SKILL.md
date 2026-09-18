---
name: trouver-personnes
description: >
  Skill pour rechercher des personnes (decisionnaires, contacts) par poste, seniorite,
  entreprise ou localisation via l'API Crustdata, et exporter le resultat en CSV. Utilise ce
  skill des que l'utilisateur veut trouver des contacts nommes correspondant a son ICP. Se
  declenche sur : "trouve-moi des [poste]", "trouve les decisionnaires de ces entreprises",
  "cherche des contacts", "trouve-moi 20 directeurs marketing".
---

# Trouver des personnes (Crustdata)

## Vue d'ensemble

**Base URL** : `https://api.crustdata.com`
**Auth** : header `Authorization: Token $CRUSTDATA_API_KEY`, cle chargee depuis le `.env`
racine.
**Endpoint** : `POST /screener/persondb/search/`

C'est la methode de sourcing a privilegier pour trouver des personnes nommees (donnee
"employeur actuel" garantie a jour). Coute des credits des le premier appel, contrairement a
la recherche d'entreprises qui a une etape de validation gratuite.

## Workflow

### Etape 1 - Construire les criteres

Depuis la demande de l'utilisateur et/ou la section 2 de `05 Departements/Go-to-Market/contexte.md` : poste(s) visé(s),
niveau de seniorite, entreprise(s) cible(s) le cas echeant, zone geographique.

### Etape 2 - Lancer la recherche

```bash
python3 .claude/skills/trouver-personnes/scripts/client.py search \
  --titles "Head of Sales,VP Sales,Directeur Commercial" \
  --seniority-levels "director,vp" \
  --location "France" \
  --limit 100 \
  --out "Listes-prospection/personnes.csv"
```

- `--titles` : plusieurs valeurs separees par virgules, combinees en OU
- `--seniority-levels` : `Owner, Founder, C-level, Partner, VP, Head, Director, Manager, Senior`
- `--company-name` : pour cibler les contacts d'une entreprise precise (utile apres
  `trouver-entreprises`)

### Etape 3 - Cap par entreprise si sourcing multi-comptes

Si la recherche vise plusieurs entreprises en meme temps (ex: liste issue de
`trouver-entreprises`), sur-sourcer 3 a 5x le besoin puis garder les 5 meilleurs contacts par
entreprise (via `qualifier-liste` ensuite), plutot que de tout garder.

### Etape 4 - Resumer

Nombre de personnes trouvees / total disponible (`total_count` de la reponse), chemin du
CSV. Proposer l'etape suivante : "Je peux qualifier cette liste avec `qualifier-liste`, ou
trouver leurs emails avec `trouver-email`."

## Colonnes du CSV de sortie

`name, headline, title, company, company_domain, seniority_level, region, linkedin_url`

## Cout

3 credits pour 100 resultats (minimum 3 par appel). Verifier le solde avant un batch
important :
```bash
curl -sS -H "Authorization: Token $CRUSTDATA_API_KEY" https://api.crustdata.com/user/credits
```

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle invalide | verifier `CRUSTDATA_API_KEY` dans le `.env` racine |
| 402 | credits insuffisants | alerter l'utilisateur et arreter |
| 429 | rate limit | attendre et reessayer |
