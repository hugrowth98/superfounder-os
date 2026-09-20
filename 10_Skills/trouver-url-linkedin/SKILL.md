---
name: trouver-url-linkedin
description: >
  Exécute le verbe trouver_url_linkedin : retrouve l'URL du profil LinkedIn d'une ou plusieurs
  personnes à partir du prénom, du nom et de l'entreprise, avec votre compte LinkedIn (Unipile) ou,
  sans compte, par une recherche Google scrapée (Apify), et pose un niveau de confiance par ligne.
  Se déclenche sur : "trouve l'URL LinkedIn de", "retrouve les profils LinkedIn de cette liste",
  "c'est qui sur LinkedIn", "il me manque les URL LinkedIn", "linkedin depuis le nom", "je n'ai
  que les noms et l'entreprise". Ne pas utiliser pour chercher des personnes par critères (voir
  `trouver-personnes`), ni pour retrouver un profil depuis un email (voir `enrichir-personne`, qui
  passe par FullEnrich).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. Deux voies, dans cet ordre :

| Voie | `--source` | Outil | Coût vérifié | Quand |
|---|---|---|---|---|
| 1 | `unipile` | recherche de personnes avec votre compte LinkedIn (`POST /api/v1/linkedin/search`, classique) | abonnement, pas de crédit | dès que Unipile est branché : c'est le défaut |
| 2 | `google` | Apify `apify/google-search-scraper`, une requête `"Prénom Nom" Entreprise site:linkedin.com/in` par personne, premier résultat `linkedin.com/in` | 0,0025 $ par page de résultats (une par personne) + 0,001 $ par run | sans compte LinkedIn, ou quand Unipile ne trouve pas |

Sans `--source`, le script prend Unipile si `UNIPILE_API_KEY` et `UNIPILE_ACCOUNT_ID` sont dans `.env`,
Google sinon. Rien de branché : dites-le, renvoyez vers `connecter-outils`, ne devinez aucune URL.

## Entrée

Un CSV avec `prenom`, `nom`, `entreprise` (les lignes qui ont déjà `linkedin_url` sont sautées, sauf
`--force`), ou une seule personne : `--nom "Prénom Nom" --entreprise "Société"`.

## Sortie

Le même CSV dans `05_Departements/Go-to-Market/Listes-prospection/trouver-url-linkedin_<sujet>_<date>.csv`, avec
`linkedin_url` (normalisée, `https://www.linkedin.com/in/<slug>`), `linkedin_confiance` (`haute` :
prénom et nom lus dans le résultat ; `moyenne` : un seul des deux ; `faible` : résultat sans le nom,
homonyme probable ; `aucune`), `linkedin_entreprise_match` (`oui`, `partiel`, `non`),
`linkedin_titre_trouve` et `linkedin_source`. Pour une personne seule, l'URL s'affiche directement.

## Procédure

1. Vérifiez les colonnes : `prenom` et `nom` sont obligatoires, `entreprise` divise les homonymes par
   dix. Un fichier sans entreprise passe par Unipile de préférence.
2. Dry-run : `python3 scripts/trouver_url_linkedin.py --in <csv> --dry-run` (le nombre de personnes, la voie, le coût).
3. Annoncez, attendez le oui, lancez. Exemples :
   `python3 scripts/trouver_url_linkedin.py --nom "Hugo Dollfus" --entreprise "Growth Hiring"`
   `python3 scripts/trouver_url_linkedin.py --in <csv>` (Unipile si branché)
   `python3 scripts/trouver_url_linkedin.py --in <csv> --source google --pays fr`
   `python3 scripts/trouver_url_linkedin.py --in <csv> --source google --force --max 50` (relance sur ce qu'Unipile n'a pas trouvé)
4. Lisez la répartition des confiances. `haute` s'utilise telle quelle ; `moyenne` se vérifie sur
   `linkedin_titre_trouve` et `linkedin_entreprise_match` ; `faible` se relit à la main ou se vide.
5. Un seul next step : `enrichir-personne` (le profil complet, puis l'email) ou `dedoublonner`.

Ordre de grandeur, mesuré sur vos listes : Google trouve environ 7 personnes sur 10, la plupart en
confiance haute. Unipile fait mieux sur les noms courants quand l'entreprise est donnée.

## Garde-fous

- Aucune URL n'est devinée à partir d'un format (`prenom-nom`) : une personne non trouvée reste vide.
- Une confiance `faible` ne part jamais en séquence sans relecture.
- Unipile compte dans les quotas de votre compte (`05_Departements/Go-to-Market/GARDE-FOUS.md`) ; Google n'y touche pas.
- Les requêtes Google ne contiennent que le nom et l'entreprise, jamais l'email ni le téléphone.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `[source] google (pas de compte Unipile dans .env)` alors que vous en avez un | `UNIPILE_ACCOUNT_ID` absent | `connecter-outils`, étape Unipile |
| Beaucoup de `faible` | noms courants sans entreprise | ajoutez la colonne `entreprise`, ou passez par Unipile |
| `aucune` sur des noms sûrs | profil peu indexé par Google | `--source unipile`, ou `trouver-personnes --source employes` sur la page entreprise |
| Google : 0 résultat partout | `countryCode` inadapté | `--pays` du marché de la personne |
