---
name: crm
description: >
  Lit et écrit dans le CRM HubSpot depuis le module GTM : exporte les clients gagnés ou perdus (pour définir l'ICP, chercher des lookalikes, sélectionner des comptes) et pousse une liste qualifiée en contacts, avec l'entreprise rattachée, une note (le signal détecté) et une tâche d'appel datée. Se déclenche sur : "mes clients gagnés", "exporte mes clients", "les affaires perdues", "mets-les dans HubSpot", "pousse dans le CRM", "crée une tâche d'appel", "ajoute une note", "importe dans HubSpot". Ne pas utiliser pour : dédoublonner une liste contre le CRM, voir `dedoublonner` ; envoyer une séquence, voir `envoyer-sequence`.
---

Le CRM est la mémoire commerciale de l'utilisateur : on y lit ce qui a marché (les clients gagnés dessinent l'ICP) et on y écrit ce qu'on va faire (un contact, son signal, un appel à passer). Rien ne s'écrit sans un oui.

## Outil

`05_Departements/Go-to-Market/OUTILS.md`, ligne `crm:`. Seul HubSpot est pris en charge (clé `HUBSPOT_ACCESS_TOKEN`, token d'application privée avec les scopes contacts, companies, deals, notes et tasks en lecture et écriture). Si `crm: aucun`, dites-le à l'utilisateur et proposez `connecter-outils` ; ne simulez rien. Aucun crédit consommé : seul le token compte.

## Entrée

- `lire` : rien. Options `--statut gagnes|perdus`, `--depuis YYYY-MM-DD`, `--max`.
- `pousser` : un CSV aux colonnes normalisées, avec `email` rempli (HubSpot rattache par email ; une ligne sans email est ignorée et comptée). Utile : `domaine` (rattache l'entreprise), `tier` (filtre `--tier A,B`), `signal_type`, `signal_date`, `signal_detail` (deviennent la note), `exclu` (les `oui` ne sont jamais poussés).

## Sortie

- `lire` : `05_Departements/Go-to-Market/Listes-prospection/crm_clients-gagnes_<date>.csv` (ou `-perdus`), une ligne par contact d'affaire (jusqu'à 5 par affaire, ou une ligne entreprise seule), colonnes normalisées plus `affaire`, `montant`, `date_cloture`, `statut`, `source = hubspot`.
- `pousser` : rien sur disque ; dans HubSpot, les contacts créés ou mis à jour, l'association à l'entreprise (créée si absente), une note par contact, une tâche d'appel par contact si `--tache`.

## Procédure

```bash
# lire les clients gagnés depuis janvier
python3 scripts/crm.py lire --statut gagnes --depuis 2026-01-01

# pousser les tiers A et B d'une liste, avec le signal en note et un appel sous 2 jours
python3 scripts/crm.py pousser --in <fichier.csv> --tier A,B --tache "Appeler : nouveau DRH" --dry-run
python3 scripts/crm.py pousser --in <fichier.csv> --tier A,B --tache "Appeler : nouveau DRH" --confirmer
```

1. Pour `pousser`, lancez toujours `--dry-run` d'abord, montrez le résumé (combien de contacts, combien d'entreprises rattachées, note, tâche, 3 exemples) et attendez le oui de l'utilisateur.
2. Relancez avec `--confirmer`. Le script refuse d'écrire sans ce drapeau.
3. Dites ce qui a été écrit et proposez le next step (souvent : `envoyer-sequence` ou `cold-call` pour les tâches créées).

Ce que `lire` sert à faire ensuite : `construire-liste/sous-skills/definir-icp` (ce que les gagnés ont en commun), `trouver-lookalikes` (leurs domaines en graine), `selectionner-comptes`, et `dedoublonner --contre` (ne jamais prospecter un client).

## Garde-fous

- Aucune écriture sans `--dry-run` montré puis `--confirmer`.
- Une ligne `exclu = oui` ou `ne_plus_contacter = oui` n'est jamais poussée.
- Le script ne modifie jamais le stade d'une affaire ni le statut d'un contact existant : il ajoute, il n'écrase pas les propriétés remplies (HubSpot garde la valeur existante quand la nouvelle est vide).
- Une tâche est toujours datée (défaut : dans 2 jours) et de type appel : une tâche sans date se perd.
- `lire` plafonne à 500 affaires par défaut ; au-delà, dites-le et demandez si on filtre par date.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| HTTP 401 | token absent ou expiré | `connecter-outils` pour retester la clé |
| HTTP 403 sur notes ou tasks | scopes manquants sur l'application privée | ajouter `crm.objects.contacts.write`, `crm.objects.companies.write`, `crm.objects.deals.read`, notes et tasks, puis régénérer le token |
| 0 affaire trouvée en `lire` | le pipeline n'utilise pas les stades fermés standard | vérifier dans HubSpot que les affaires gagnées ont `hs_is_closed_won` à vrai, sinon filtrer sur `dealstage` à la main |
| contacts créés sans entreprise | colonne `domaine` vide | passer par `enrichir-entreprise` avant de pousser |
| doublons de contacts | emails en majuscules ou avec espaces dans le CSV | le script normalise en minuscules ; vérifier les alias (prenom.nom vs pnom) avec `dedoublonner --hubspot` |
