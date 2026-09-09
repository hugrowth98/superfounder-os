---
name: profil-entreprise-linkedin
description: >
  Skill pour recuperer le profil complet d'une entreprise sur LinkedIn (description,
  secteur, taille, site web, followers, historique d'effectifs) via l'API Unipile.
  Utilise ce skill des que l'utilisateur veut des infos detaillees sur une entreprise
  precise identifiee sur LinkedIn. Se declenche sur : "regarde le profil LinkedIn de
  cette boite", "combien d'employes chez", "c'est quoi cette entreprise sur LinkedIn",
  "fiche entreprise LinkedIn".
---

# Profil d'entreprise LinkedIn (Unipile)

## Vue d'ensemble

**Auth** : header `X-API-KEY: $UNIPILE_API_KEY`, DSN dans `$UNIPILE_DSN`, charges depuis
le `.env` racine.
**Endpoint** : `GET {UNIPILE_DSN}/api/v1/linkedin/company/{identifiant}?account_id=<id>`

`{identifiant}` accepte le `public_identifier` (slug LinkedIn, ex: `anthropicresearch`)
ou l'id numerique interne. Un slug "intuitif" ne marche pas toujours (ex: `unipile` seul
-> 404) : dans ce cas le script retente automatiquement via une recherche entreprise.

## Workflow

### Etape 1 - Identifier l'entreprise

Nom, public_identifier ou URL LinkedIn de l'entreprise. Le script gere la resolution
automatique par recherche si le nom donne ne correspond a aucun identifiant direct.

### Etape 2 - Lancer la recuperation

```bash
python3 .claude/skills/profil-entreprise-linkedin/scripts/client.py "<account_id>" "<nom_ou_identifiant>"
```

## Format de sortie

Une entreprise est une seule entite : restituer sous forme de **tableau markdown a deux
colonnes** (Champ / Valeur), avec le maximum d'informations disponibles :

| Champ | Valeur |
|---|---|
| Nom | Anthropic |
| Description | We're an AI research company... |
| Secteur | Research Services |
| Site web | anthropic.com |
| Abonnes | 4 049 506 |
| Effectif (tranche) | 501-1000 (effectif exact si disponible : 5261) |
| Localisation | (si renseignee) |

Ne pas inclure le bloc `viewer_permissions` (tres verbeux, sans valeur pour
l'utilisateur). Si `insights.employeesCount.employeesCountGraph` est present (historique
de croissance des effectifs), le signaler en une ligne resumee ("effectif en hausse/baisse
sur les X derniers mois") plutot que de deverser le graphe brut.

## Erreurs a gerer

| Code | Sens | Action |
|---|---|---|
| 401 | cle/DSN invalide | verifier `UNIPILE_API_KEY`/`UNIPILE_DSN` dans le `.env` racine |
| 404 (meme apres fallback recherche) | entreprise introuvable | redemander le nom exact ou l'URL LinkedIn a l'utilisateur |
| 429 | rate limit Unipile | attendre et reessayer |
