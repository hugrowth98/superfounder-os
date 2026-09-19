---
name: verifier-reponses
description: >
  Exécute le verbe verifier_reponses : liste qui a répondu, sur quel canal (LinkedIn via Unipile,
  email via la boîte Lemlist), quand, avec le dernier message reçu, et pose `ne_plus_contacter =
  oui` sur ces personnes dans la liste en cours. Garde-fou obligatoire avant toute relance. Se
  déclenche sur : "qui a répondu", "des nouvelles réponses ?", "vérifie les réponses", "check
  les conversations", "avant de relancer", "qui a dit oui", "mets à jour la liste avec les
  réponses". Ne pas utiliser pour : envoyer (voir `envoyer-sequence`), répondre à un prospect
  (l'utilisateur répond lui-même), ni analyser une campagne (stats Lemlist via le MCP).
---

## Outil

Lisez `05_Departements/Go-to-Market/OUTILS.md`. LinkedIn : Unipile `GET /api/v1/chats`, `/chats/{id}/messages` et
`/chats/{id}/attendees` avec le compte de l'utilisateur (abonnement), le script
`scripts/verifier_reponses.py` garde les conversations où le dernier message vient du prospect
(`is_sender` du message, ou comparaison avec `UNIPILE_OWN_PROVIDER_ID`). Email : MCP Lemlist
`get_inbox_conversations` (et `get_inbox_conversation` pour le fil complet), résultat sauvé en
JSON puis normalisé par le même script. Pas de webhook : c'est une vérification à la demande,
à lancer avant chaque étape de séquence et chaque matin de session d'appels. Outil non
branché : dites-le, renvoyez vers `connecter-outils`.

## Entrée

Rien d'obligatoire. En option, la liste en cours de séquence (`--in`), pour y marquer les
répondants, et le JSON des conversations Lemlist (`--lemlist-json`).

## Sortie

`Listes-prospection/verifier-reponses_<sujet>_<date>.csv`, une ligne par personne qui a
répondu, la plus récente en premier : `prenom`, `nom`, `entreprise`, `email`, `linkedin_url`,
`source` (`unipile` ou `lemlist`), `date_extraction`, plus `canal` (`linkedin` ou `email`),
`date_reponse`, `dernier_message`, `ne_plus_contacter` (`oui`), `provider_id`, `chat_id`,
`campagne`, `lemlist_lead_id`, `sentiment` (si Lemlist le donne). Avec `--in` : une copie
`<liste>_maj.csv` où les répondants portent `ne_plus_contacter = oui`, `canal_reponse`,
`date_reponse`, `dernier_message`.

## Procédure

1. LinkedIn : `python3 scripts/verifier_reponses.py` (ou `--depuis 7` pour la semaine).
2. Email : appelez le MCP Lemlist `get_inbox_conversations` (filtre sur la campagne en cours si
   possible), écrivez la réponse telle quelle dans un fichier JSON à côté de la liste, puis
   `python3 scripts/verifier_reponses.py --lemlist-json inbox.json --in <liste en cours>`.
3. Lisez les 3 derniers messages affichés et classez chaque réponse en deux mots pour
   l'utilisateur : intéressé (à rappeler), pas maintenant (à reprogrammer), non (à retirer),
   hors sujet (auto-reply, absence). Ne répondez à personne : c'est lui qui répond.
4. Rendez : nombre de réponses par canal, la liste des intéressés avec le dernier message, le
   lien vers le fichier et vers `<liste>_maj.csv`, et un seul next step : `cold-call` (brief
   avant appel) pour les intéressés, ou `envoyer-sequence` étape suivante sur la liste mise à
   jour.

Avant toute relance (`envoyer-sequence --etape message`, relance Lemlist), ce skill a été passé
dans la journée : le script d'envoi LinkedIn refait le contrôle lui-même, la campagne Lemlist
arrête d'elle-même les leads qui répondent, mais la liste locale doit refléter les deux.

## Garde-fous

- Lecture seule : aucun message, aucune réaction, aucune réponse envoyée par ce skill.
- Un prospect qui a répondu, même "non", ne reçoit plus rien de la séquence :
  `ne_plus_contacter = oui` est définitif dans la liste, sauf demande explicite de l'utilisateur.
- Un auto-reply (absence, "je ne suis plus dans l'entreprise") est une réponse au sens du script
  : gardez la ligne marquée, signalez-la comme telle, l'utilisateur décide.
- Le dernier message est cité tel quel, jamais résumé dans le CSV (le résumé se fait en chat).
- Sans `UNIPILE_OWN_PROVIDER_ID` et sans champ `is_sender`, le script ne peut pas savoir qui a
  parlé en dernier : il le dit, lancez `connecter-outils` étape 2.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| Toutes les conversations remontent comme réponses | `is_sender` absent et `UNIPILE_OWN_PROVIDER_ID` vide | `connecter-outils` étape 2 (le test l'écrit dans `.env`) |
| Répondant sans nom ni URL | participants illisibles | garder `provider_id`, la ligne se croise quand même avec la liste |
| `--in` ne marque personne | ni `provider_id`, ni `linkedin_url` normalisée, ni email commun | passer par le fichier de sortie de `envoyer-sequence` (il porte `provider_id`) |
| JSON Lemlist non reconnu | structure inattendue | vérifier que le fichier contient une liste sous `conversations`, `items` ou `data` |
| 429 Unipile | trop de lectures | attendre 15 minutes |
