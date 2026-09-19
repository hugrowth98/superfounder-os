# Conventions de construction du module GTM

Ce fichier est le contrat que suit tout ce qui est écrit dans ce dossier. Il est lu avant d'écrire un skill, une ressource ou un script. Il ne s'adresse pas au client final.

## 1. Langue et ton

- Tout en français accentué. Vouvoiement de l'utilisateur dans chaque skill, chaque ressource, chaque message généré.
- Aucun tiret cadratin (U+2014) ni demi-cadratin (U+2013), nulle part. Tiret simple, deux-points, virgule ou parenthèses.
- Ton direct, concret, sans jargon creux. Règles d'écriture complètes dans `01_About-Me/anti-ai-voice.md` du workspace parent (à lire pour tout template de message ou d'email).
- Les templates d'emails et de messages sont adaptés au B2B français : vouvoiement, phrases courtes, pas d'anglicisme d'ouverture, pas de formule de politesse creuse, chiffres et faits avant adjectifs. On adapte, on ne traduit pas mot à mot.

## 2. Ce qu'on ne mentionne jamais

- Aucune marque de fournisseur de skills tiers : ni le nom des dépôts d'origine, ni leur produit, ni leurs liens, ni leurs blocs. Aucune tournure du type "utilisez d'abord X".
- Aucun outil hors de la stack (section 4), sauf dans `cold-email/sous-skills/infra-email` et ses ressources pour les fournisseurs d'infrastructure (registrar, boîtes mail, outils de diagnostic DNS), qui ne sont pas des outils GTM. Un outil hors stack qui apparaissait dans une source est remplacé par l'outil de la stack qui fait la même chose, ou supprimé avec la méthode conservée.
- Pas d'historique ("cette version remplace..."). On décrit ce que le skill fait maintenant.

## 3. Les verbes (l'interface entre méthode et outil)

Chaque skill de méthode décrit ses actions avec ces verbes, jamais avec un nom d'outil. Chaque verbe a un skill d'exécution dans `10_Skills/` qui lit `05_Departements/Go-to-Market/OUTILS.md` pour savoir quel outil appeler. Exception assumée : un verbe qui n'est qu'un appel d'actor n'a pas son propre dossier, il est porté par le skill du même sujet (detecter_signal par le master `detecter-signaux`, detecter_techno et scraper_pubs par `enrichir-entreprise`).

| Verbe | Skill d'exécution | Ce qu'il fait |
|---|---|---|
| trouver_entreprises | `trouver-entreprises` | liste d'entreprises par critères |
| trouver_lookalikes | `trouver-lookalikes` | entreprises semblables à une liste de clients |
| trouver_personnes | `trouver-personnes` | décisionnaires par titre, séniorité, entreprise |
| enrichir_personne | `enrichir-personne` | profil LinkedIn complet + contact vérifié |
| enrichir_entreprise | `enrichir-entreprise` | firmographique, site, LinkedIn, techno |
| trouver_email | `trouver-email` | email pro vérifié (cascade incluse) |
| trouver_telephone | `trouver-telephone` | mobile |
| detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | levée, acquisition, recrutement, changement de poste, sur une liste ou un marché |
| scraper_offres_emploi | `scraper-offres-emploi` | offres ouvertes d'une entreprise ou d'un marché |
| scraper_engagement | `scraper-engagement` | likes, commentaires, réactions d'un post |
| detecter_techno | `enrichir-entreprise --techno` | stack technique d'un domaine |
| scraper_pubs | `enrichir-entreprise --pubs` | pubs actives d'un concurrent (Meta, LinkedIn) |
| qualifier_liste | `qualifier-liste` | score ICP, tiers, exclusions, sur un CSV |
| dedoublonner | `dedoublonner` | fusion multi-sources + dédup contre le CRM |
| lire_crm, pousser_crm | `crm` | lire les clients gagnés et perdus, pousser contact + note + tâche dans HubSpot |
| envoyer_sequence | `envoyer-sequence` | pousser une liste dans une séquence email ou LinkedIn |
| verifier_reponses | `verifier-reponses` | qui a répondu, sur quel canal |

## 4. La stack (liste fermée, 7 outils, plus 2 optionnels pour les signaux)

| Outil | Rôle | Clé dans .env |
|---|---|---|
| Apify | par défaut pour tout scraping et tout signal (actors dans `05_Departements/Go-to-Market/OUTILS.md`) | `APIFY_TOKEN`, cookies `LINKEDIN_*` pour Sales Nav |
| Unipile | tout ce qui touche à LinkedIn avec le compte de l'utilisateur : Sales Nav, profils, posts, invitations, DM | `UNIPILE_API_KEY`, `UNIPILE_DSN`, `UNIPILE_ACCOUNT_ID` |
| Crustdata | recherche d'entreprises et de personnes par API quand Apify n'est pas voulu | `CRUSTDATA_API_KEY` |
| FullEnrich | email, vérification, téléphone. Seul outil d'enrichissement contact | `FULLENRICH_API_KEY` |
| Ocean.io | lookalikes uniquement | `OCEAN_API_KEY` (MCP) |
| Lemlist | envoi email, et LinkedIn si l'utilisateur le choisit | `LEMLIST_API_KEY` (MCP) |
| HubSpot | CRM : lecture des clients, import, dédup, pipeline | `HUBSPOT_ACCESS_TOKEN` |
| PredictLeads (optionnel) | secours du verbe detecter_signal : événements d'entreprise (expansion, partenariat, lancement, nomination), levées, offres, détections techno datées | `PREDICTLEADS_API_KEY`, `PREDICTLEADS_API_TOKEN` |
| TheirStack (optionnel) | secours du verbe detecter_signal : offres d'emploi filtrées par techno citée, intent (entreprises qui recrutent et utilisent une techno) | `THEIRSTACK_API_KEY` |

Règle de priorité, fixée à l'onboarding et écrite dans `05_Departements/Go-to-Market/OUTILS.md` : Apify d'abord si l'utilisateur a un compte Apify ; sinon l'outil API du verbe (Crustdata, FullEnrich, Unipile). Jamais redemandé en cours de session.

## 5. Forme d'un master

```
10_Skills/<master>/
  SKILL.md                   l'orchestrateur
  sous-skills/<nom>/SKILL.md un sous-skill par cas
  ressources/                frameworks, barèmes, templates, lus par les sous-skills
```

`SKILL.md` du master, dans cet ordre :
1. Frontmatter : `name`, `description` en bloc `>` (une phrase sur ce qu'il fait, puis "Se déclenche sur :" et la liste des phrases déclencheuses, puis "Ne pas utiliser pour :").
2. `## Repérage` : résoudre `SKILL_BASE` par Glob sur `**/<master>/SKILL.md`, sous-skills dans `{SKILL_BASE}/sous-skills/`, ressources dans `{SKILL_BASE}/ressources/`.
3. `## Rôle` : deux phrases, qui est l'expert, ce qu'il route.
4. `## Table de routage` : colonnes Demande, Sous-skill, Phrases déclencheuses, Fichier à lire.
5. `## Logique de routage` : l'ordre des tests (persona d'abord, puis position, puis demande précise...).
6. `## Ce que le master fait lui-même` : les cas transverses avec les ressources à lire.
7. `## Repères chiffrés` : 5 à 10 benchmarks à citer.
8. `## Avant de répondre` : lire `05_Departements/Go-to-Market/contexte.md` (ICP, personas, signaux prioritaires, canaux) et `05_Departements/Go-to-Market/OUTILS.md`.

## 6. Forme d'un sous-skill

1. Frontmatter : `name`, `description` en bloc `>` avec déclencheurs et exclusions ("Ne pas utiliser pour X, voir <autre sous-skill>").
2. Une phrase d'ouverture : ce que c'est, pourquoi ça marche, le chiffre clé.
3. `## Ressources` : les fichiers de `{SKILL_BASE}/ressources/` à lire.
4. `## Méthode` : les étapes, numérotées.
5. `## Exécution` : la séquence de verbes (section 3) avec le skill d'exécution à appeler pour chacun, et les colonnes du CSV attendues en entrée et en sortie.
6. `## Repères` : barème, fenêtres de timing, seuils, en tableau.
7. `## Template` : le message ou le livrable type, quand il y en a un.
8. `## Règles` : 4 à 8 règles courtes, dont ce qu'on ne fait jamais.
9. `## Exemples` : 3 demandes d'utilisateur avec la réponse attendue en une ligne.

## 7. Forme d'un skill d'exécution

1. Frontmatter avec déclencheurs.
2. `## Outil` : lit `05_Departements/Go-to-Market/OUTILS.md` à la racine, prend l'outil principal du verbe, sinon le secours. Si aucun outil n'est branché : dire à l'utilisateur lequel brancher et comment (`connecter-outils`), ne rien simuler.
3. `## Entrée` et `## Sortie` : colonnes CSV normalisées (section 8).
4. `## Procédure` : la commande ou l'appel, un script par outil dans `scripts/`, les paramètres, les limites et coûts.
5. `## Garde-fous` : quotas, compteur journalier en fichier local, ce qui bloque.
6. `## Erreurs fréquentes` : symptôme, cause, fix.

Les scripts sont en Python 3.9+, `requests` seulement, lisent le `.env` de la racine (trouvée en remontant jusqu'à `05_Departements/Go-to-Market/OUTILS.md`), ne contiennent aucune clé, ont `--help` et `--dry-run` (affiche ce qui serait fait et le coût estimé, sans appel). La bibliothèque commune vit dans `10_Skills/_commun/` (`gtm_common.py` : racine, .env, OUTILS.md, CSV, clients HTTP ; `apify_run.py` : lancer un actor, attendre, lire le dataset, table des prix). Sorties en CSV UTF-8 : les listes et enrichissements dans `05_Departements/Go-to-Market/Listes-prospection/`, les runs de signaux dans `05_Departements/Go-to-Market/Signaux/`, les messages et séquences dans `05_Departements/Go-to-Market/Messages/`, nommés `<verbe>_<sujet>_<YYYY-MM-DD>.csv`.

## 8. Colonnes CSV normalisées

Toujours ces noms, dans cet ordre quand ils existent : `prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `domaine`, `linkedin_url`, `linkedin_entreprise_url`, `email`, `email_statut`, `telephone`, `ville`, `pays`, `secteur`, `effectif`, `source`, `date_extraction`, `score_icp`, `tier`, `signal_type`, `signal_date`, `signal_detail`, `score_signal`, `fraicheur`, `exclu`, `raison_exclusion`, `ne_plus_contacter`.

Conventions : `source` = nom complet de l'actor Apify (`signalbase/signalbase-api`) ou `unipile`, `crustdata`, `fullenrich`, `ocean`, `lemlist`, `hubspot` ; `fraicheur` = nombre entier de jours écoulés depuis `signal_date` ; un concurrent est encodé `exclu = oui` et `raison_exclusion = concurrent (famille)`.

## 9. Fichiers racine que tout le monde lit

- `05_Departements/Go-to-Market/contexte.md` : ICP en 3 couches et scoring sur 100 (tableaux avec les points en ligne), personas ATL et BTL avec comité d'achat, 5 signaux prioritaires, canaux, volumes, garde-fous propres. Rempli par `installer-gtm`. Une info vit ici et nulle part ailleurs : les skills n'ont aucune donnée sur l'utilisateur.
- `05_Departements/Go-to-Market/OUTILS.md` : verbe vers outil principal, secours, actor Apify, prix. Rempli par `installer-gtm` via `connecter-outils`.
- `05_Departements/Go-to-Market/GARDE-FOUS.md` : limites d'envoi, règles de personnalisation, ce qu'on n'envoie jamais.

## 10. Nommage

Skills et sous-skills en français, minuscules, tirets : `detecter-signaux`, `changement-poste`, `premier-contact`. Ressources : `nom-explicite.md`. Pas de doublon de nom entre deux dossiers. Un skill = un dossier = un `SKILL.md`. `scripts/valider.py` vérifie tout ça : frontmatter YAML, tirets, marques interdites, références croisées, compilation des scripts, actors contre `05_Departements/Go-to-Market/OUTILS.md`.
