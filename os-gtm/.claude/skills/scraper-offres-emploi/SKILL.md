---
name: scraper-offres-emploi
description: >
  Skill pour detecter si une entreprise a augmente son nombre d'offres d'emploi ouvertes
  depuis la derniere verification (signal d'investissement dans un poste ou une equipe, ex:
  elle recrute un SDR = elle investit dans l'outbound). Utilise ce skill pour prioriser des
  comptes selon un signal de recrutement. Se declenche sur : "cette entreprise recrute ?",
  "verifie les offres d'emploi de", "detecte un signal de recrutement", "qui recrute sur tel
  poste".
---

# Detecter un signal de recrutement (Crustdata)

## Vue d'ensemble

Pas d'endpoint dedie chez Crustdata pour ca : ce skill compare le nombre d'offres d'emploi
ouvertes d'une entreprise (`job_postings_count`) a la derniere valeur connue, stockee en
local dans `scripts/baseline.json` (pas de base de donnees, un simple fichier JSON qui
grandit au fil des verifications).

**Endpoint sous-jacent** : `GET https://api.crustdata.com/screener/company?company_domain=<domaine>`

## Workflow

### Etape 1 - Identifier le ou les domaines a verifier

A partir d'une liste d'entreprises (issue de `trouver-entreprises` par exemple) ou d'un
domaine donne directement par l'utilisateur.

### Etape 2 - Verifier le signal

```bash
python3 .claude/skills/scraper-offres-emploi/scripts/client.py acme.com --threshold 5
```

Le seuil par defaut (`--threshold 5`) declenche un signal positif si le nombre d'offres a
augmente d'au moins 5 depuis la derniere verification. Ajuster selon la taille de
l'entreprise (baisser le seuil pour une PME, l'augmenter pour un grand compte).

**Premiere verification d'un domaine** : pas de baseline connue, `previous_count = 0`, donc
le signal sera quasi toujours positif. C'est normal - le signal ne devient utile qu'a partir
de la deuxieme verification. Le dire a l'utilisateur.

### Etape 3 - Traiter un batch

Pour verifier plusieurs entreprises, boucler l'appel sur chaque domaine du CSV et agreger les
resultats. Ne garder que les signaux positifs pour la suite (priorisation dans
`qualifier-liste` ou ciblage direct dans `trouver-personnes`).

### Etape 4 - Resumer

Liste des entreprises avec signal positif, delta d'offres pour chacune. Proposer l'etape
suivante : "Je peux chercher les decisionnaires de ces entreprises avec `trouver-personnes`."

## Cout

1 credit (cache) ou 4 credits (temps reel) par entreprise verifiee, via l'endpoint
d'enrichissement Crustdata.
