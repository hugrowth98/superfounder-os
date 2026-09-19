---
name: envoyer-sequence
description: >
  Exécute le verbe envoyer_sequence : pousse une liste validée dans une séquence email (Lemlist)
  ou LinkedIn (Unipile, ou Lemlist multicanal selon OUTILS.md), avec échantillon de 3 messages
  validé avant tout envoi, compteurs journaliers bloquants et exclusion de ceux qui ont déjà
  répondu. Se déclenche sur : "lance la campagne", "envoie la séquence", "importe dans Lemlist",
  "envoie les invitations", "envoie le message 1", "lance la relance", "démarre l'outreach",
  "mets en pause la campagne". Ne pas utiliser pour : écrire les messages (master `cold-email`),
  vérifier qui a répondu (voir `verifier-reponses`), ni pour appeler (master `cold-call`).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md` : `canal_email: lemlist` (MCP Lemlist, OAuth ou clé), `canal_linkedin:
unipile` (scripts de ce skill, compte LinkedIn de l'utilisateur) ou `lemlist` (étapes LinkedIn
dans la séquence Lemlist). Lisez `05_Departements/Go-to-Market/GARDE-FOUS.md` avant tout envoi. Outil non branché : dites-le,
renvoyez vers `connecter-outils`, n'envoyez rien par un autre moyen.

Email, via les outils MCP Lemlist : `get_campaigns` (choisir une campagne existante) ou
`create_campaign_with_sequence` (créer, avec les étapes écrites par `cold-email`),
`add_sequence_step` (relances, 3 à 4 jours d'écart), `set_campaign_senders`,
`import_leads_to_campaign` ou `add_leads_to_campaign` (le CSV préparé ici),
`validate_campaign_readiness` et `preview_email` (contrôle), `launch_campaign` ou
`set_campaign_state` (démarrer, pauser, reprendre), `get_campaigns_stats` (suivi).
LinkedIn via Unipile : `scripts/envoyer_linkedin.py` (invitation puis message,
`POST /api/v1/users/invite` et `POST /api/v1/chats`).

## Entrée

Un CSV normalisé qualifié, dédoublonné contre le CRM, avec les messages écrits par `cold-email`
dans des colonnes nommées (`icebreaker`, `message_1`, `note_invitation`, `var_preuve`...),
`email` et `email_statut` pour l'email, `linkedin_url` ou `provider_id` pour LinkedIn, et
`exclu`, `ne_plus_contacter` à jour (`verifier-reponses`).

## Sortie

- Email : `Listes-prospection/envoyer-sequence_<sujet>_<date>_lemlist.csv` (colonnes Lemlist :
  `email`, `firstName`, `lastName`, `companyName`, `jobTitle`, `linkedinUrl`, `phone`,
  `icebreaker`, variables `var_*`), puis la campagne Lemlist avec ses leads, en pause tant que
  l'utilisateur n'a pas dit "lance".
- LinkedIn : `..._invitation.csv` ou `..._message.csv`, mêmes lignes avec
  `envoi_invitation_date`, `envoi_message_date`, `erreur_envoi`, `provider_id` résolu,
  `ne_plus_contacter` posé sur ceux qui ont répondu entre-temps. Compteurs dans
  `scripts/compteurs.json`.

## Procédure

1. Vérifiez l'amont : `qualifier-liste` fait, `dedoublonner --hubspot` (ou `--contre`) fait,
   emails vérifiés (couverture fiable au-dessus de 70 %), `verifier-reponses` passé sur les
   listes déjà contactées. Sinon, une étape manque : dites laquelle.
2. Email. Préparez le fichier :
   `python3 scripts/preparer_import_lemlist.py --in <csv> --colonne-message icebreaker`
   Le script écarte exclus, `ne_plus_contacter`, emails vides, invalides, non vérifiés,
   catch-all (sauf `--avec-catch-all`), et affiche 3 leads avec leur message. Montrez-les,
   attendez le oui. Puis MCP : choisissez ou créez la campagne (nom `module GTM <cible> <date>`),
   importez le CSV, `validate_campaign_readiness`, `preview_email` sur un lead, récapitulez
   (nombre de leads, expéditeur, première étape, cadence) et attendez un "oui, lance" explicite
   avant `launch_campaign`.
3. LinkedIn (Unipile). Quota : `python3 scripts/envoyer_linkedin.py quota`. Puis :
   `python3 scripts/envoyer_linkedin.py --in <csv> --etape invitation --colonne-message note_invitation --max 20`
   Le script affiche 3 messages et s'arrête. Montrez-les, attendez le oui, relancez avec
   `--confirmer`. Séquence par défaut : invitation, 2 jours, message 1, 3 jours, message 2, en
   re-passant `verifier-reponses` entre chaque étape (le script exclut aussi lui-même les
   conversations où le prospect a répondu).
   `python3 scripts/envoyer_linkedin.py --in <csv envoi invitation> --etape message --colonne-message message_1 --max 30 --confirmer`
4. LinkedIn via Lemlist (`canal_linkedin: lemlist`) : mêmes étapes que l'email, avec des étapes
   LinkedIn dans la séquence ; les quotas sont ceux de Lemlist, alignés sur `05_Departements/Go-to-Market/GARDE-FOUS.md`.
5. Rendez : envoyés, écartés par raison, quota restant, lien vers le fichier de sortie et vers
   la campagne, un seul next step : `verifier-reponses` dans 48 h.

## Garde-fous

- Jamais d'envoi sans validation explicite sur un échantillon de 3 messages affichés. Le script
  LinkedIn refuse sans `--confirmer` ; côté Lemlist, `launch_campaign` n'est appelé qu'après un
  "oui, lance" écrit.
- Invitations : 30 par jour, plafond dur dans le script (`LIMITE_INVITATIONS_JOUR` du `.env` ne
  peut que baisser). Messages : 50 par jour par défaut, 100 au plus. Compteur local, bloquant,
  remis à zéro chaque jour.
- Jamais de message à quelqu'un qui a répondu : exclusion automatique via les chats Unipile,
  et `ne_plus_contacter` respecté partout.
- Une ligne envoyée n'est jamais renvoyée (`envoi_<etape>_date`). Délai 45 s plus un aléa entre
  deux envois, arrêt sur 429.
- Note d'invitation : 300 caractères au plus (LinkedIn en refuse au-delà, et 200 sur un compte
  gratuit) ; pas d'envoi sur un email catch-all sans le dire ; pas de pièce jointe, pas de lien
  dans un premier message LinkedIn.
- Aucun message généré à la volée par ce skill : il envoie ce que `cold-email` a écrit et que
  l'utilisateur a validé.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `rien a envoyer (quota du jour epuise)` | 30 invitations déjà parties | reprendre demain, ou passer aux messages |
| 422 Unipile sur `provider_id` | valeur qui n'est pas un id Unipile (URL brute) | laisser le script résoudre depuis `linkedin_url` |
| `provider_id introuvable` | profil privé ou slug faux | corriger `linkedin_url`, ou `enrichir-personne` |
| Lemlist : leads importés mais campagne vide | mauvais mapping de colonnes | utiliser le CSV de `preparer_import_lemlist.py`, colonnes Lemlist natives |
| Lemlist : `validate_campaign_readiness` en échec | expéditeur absent ou variable `{{...}}` non définie | `set_campaign_senders`, vérifier les variables du template |
| 429 en cours de run | LinkedIn ou Unipile freine | le script s'arrête ; relancer plus tard, les lignes envoyées sont marquées |
