---
name: trouver-email
description: >
  Exécute le verbe trouver_email : trouve et vérifie l'email professionnel des lignes d'un CSV
  qui n'en ont pas (ou dont l'email est invalide) avec FullEnrich, écrit `email` et
  `email_statut`, annonce le coût en crédits avant de lancer. Se déclenche sur : "trouve les
  emails", "il me manque les adresses", "enrichis les emails", "vérifie ces emails", "combien
  d'emails on peut trouver", "email de Jean Dupont chez Acme". Ne pas utiliser pour : un mobile
  (voir `trouver-telephone`), le profil LinkedIn (voir `enrichir-personne`), ou une liste sans
  prénom, nom et entreprise (passer d'abord par `trouver-personnes`).
---

## Outil

FullEnrich, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md` : c'est le seul outil d'enrichissement
contact de la stack. `POST /contact/enrich/bulk` par lots de 100, polling jusqu'à `FINISHED`.
1 crédit par email pro trouvé, 0 si rien n'est trouvé, 0 si le contact a déjà été enrichi il y a
moins de 3 mois. Les emails visibles sur un profil LinkedIn de 1er degré (Unipile) et ceux des
actors Apify ne sont pas vérifiés : ils passent aussi par ici avant un envoi. Pas de clé : dites-le
et renvoyez vers `connecter-outils`.

## Entrée

Un CSV normalisé de personnes. Pour chaque ligne, FullEnrich a besoin de `prenom` + `nom` +
(`entreprise` ou `domaine`), ou de `linkedin_url` (le meilleur match quand elle est là en plus du
nom). Les lignes qui n'ont ni l'un ni l'autre sont comptées `sans_cle_de_match` et laissées telles
quelles.

## Sortie

`Listes-prospection/trouver-email_<sujet>_<date>.csv`, mêmes lignes, `email` et `email_statut`
remplis : `DELIVERABLE` (bounce autour de 2 %, à privilégier), `HIGH_PROBABILITY` (autour de 9 %,
acceptable), `CATCH_ALL` (domaine qui accepte tout, à envoyer en dernier), `INVALID` ou
`INVALID_DOMAIN` (ne pas envoyer), `NOT_FOUND` (rien trouvé, pas facturé). `titre` est complété
si FullEnrich renvoie le poste actuel et que la colonne était vide.

## Procédure

1. Dry-run : `python3 scripts/trouver_email.py --in <csv> --dry-run`. Il compte les lignes à
   traiter (email vide ou statut invalide), celles déjà remplies, celles sans clé de match, et
   donne le coût maximal et le coût estimé (60 % de match en moyenne).
2. Annoncez : "N lignes à traiter, au plus N crédits, environ 0,6 N. Solde actuel X. On y va ?"
   Attendez le oui. Au-delà de 100 crédits estimés, le script exige `--confirmer` : c'est le
   rappel que la validation a bien été donnée.
3. Lancez : `python3 scripts/trouver_email.py --in <csv>` (ou `--max 200` pour découper, ou
   `--tier A` n'existe pas ici : filtrez la liste en amont avec `qualifier-liste`).
4. Lisez le résumé : emails trouvés, adresses fiables (`DELIVERABLE` + `HIGH_PROBABILITY`) sur le
   total. Sous 70 % de couverture fiable, la liste n'est pas prête pour une séquence email : dites-le.
5. Lien cliquable et un seul next step : `dedoublonner` contre le CRM si ce n'est pas fait, sinon
   `cold-email`.

Un seul contact ("l'email de Jean Dupont chez Acme") : écrivez un CSV d'une ligne avec `prenom`,
`nom`, `entreprise`, `domaine` et lancez de la même façon, ou utilisez le MCP FullEnrich
(`enrich_search_contact`) s'il est connecté.

## Garde-fous

- Ne lance que si la colonne `email` est vide ou le statut invalide. Jamais de relance sur un
  `DELIVERABLE`. `--force` sur demande explicite seulement.
- Coût annoncé avant tout appel, solde vérifié, arrêt si le solde ne couvre pas l'estimation.
- Pas plus de 100 contacts par requête (le script découpe), 1 s entre deux lots (limite 60
  requêtes par minute).
- On n'envoie jamais sur `CATCH_ALL` sans le dire, jamais sur `INVALID` : `envoyer-sequence` les
  filtre.
- Aucune adresse devinée par motif (`prenom.nom@domaine`) : si FullEnrich ne trouve pas, la
  colonne reste vide.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `FULLENRICH_API_KEY absent` | outil pas branché | `connecter-outils` étape 4 |
| HTTP 402 | plus de crédits | recharger sur app.fullenrich.com, relancer (les lignes déjà remplies sont sautées) |
| HTTP 429 | plus de 60 requêtes par minute | le script attend et réessaie ; sinon relancer plus tard |
| Beaucoup de `sans_cle_de_match` | colonnes `entreprise` et `domaine` vides | `enrichir-entreprise` ou `enrichir-personne` d'abord |
| Taux de match sous 40 % | noms tronqués, emojis, entreprises mal orthographiées | nettoyer les colonnes, ajouter `linkedin_url` |
| `status` bloqué sur `IN_PROGRESS` | gros lot | le script attend jusqu'à 10 minutes par lot, relancez ensuite |
