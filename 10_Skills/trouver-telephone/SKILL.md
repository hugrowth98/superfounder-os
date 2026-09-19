---
name: trouver-telephone
description: >
  Exécute le verbe trouver_telephone : trouve le mobile des lignes d'un CSV qui n'en ont pas avec
  FullEnrich (10 crédits par numéro trouvé), en annonçant le coût avant, réservé aux prospects à
  appeler. Se déclenche sur : "trouve les numéros", "il me faut les mobiles", "téléphone de ces
  décideurs", "prépare ma session d'appels", "numéros des tiers A". Ne pas utiliser pour : un
  email (voir `trouver-email`), une liste non qualifiée (passer par `qualifier-liste`), ni le
  standard d'une entreprise (voir `enrichir-entreprise`, colonne `telephone_entreprise`).
---

## Outil

FullEnrich, champ `contact.phones`, quelle que soit la priorité de `05_Departements/Go-to-Market/OUTILS.md`. Même endpoint que
l'email (`POST /contact/enrich/bulk`), même polling, mais 10 crédits par mobile trouvé, 0 si rien
n'est trouvé. Taux de match habituel autour de 30 %. Pas de clé : dites-le et renvoyez vers
`connecter-outils`.

## Entrée

Un CSV normalisé de personnes déjà qualifié, avec `tier` rempli par `qualifier-liste`. Pour
chaque ligne : `prenom` + `nom` + (`entreprise` ou `domaine`), ou `linkedin_url`. Le téléphone
est le canal de conversion (`cold-call`) : on ne cherche des mobiles que pour les personnes qu'on
va vraiment appeler, tiers A d'abord.

## Sortie

`Listes-prospection/trouver-telephone_<sujet>_<date>.csv`, mêmes lignes, `telephone` rempli
(format international renvoyé par FullEnrich). Les lignes hors du tier demandé sont conservées
telles quelles.

## Procédure

1. Dry-run sur le tier visé : `python3 scripts/trouver_telephone.py --in <csv> --tier A --dry-run`.
   Le script compte les lignes sans `telephone`, le coût maximal (10 par ligne) et le coût estimé
   (3 par ligne au taux de match habituel).
2. Annoncez le coût en crédits et en euros selon le plan de l'utilisateur, attendez le oui. Au-delà
   de 100 crédits estimés (donc environ 34 lignes), le script exige `--confirmer`.
3. Lancez : `python3 scripts/trouver_telephone.py --in <csv> --tier A --confirmer`, ou `--max 20`
   pour une première session d'appels.
4. Résumé : mobiles trouvés, crédits facturés, solde restant. Sous 25 % de match, proposez de
   compléter par le standard (`telephone_entreprise` via `enrichir-entreprise`) plutôt que de
   relancer.
5. Lien cliquable, un seul next step : `cold-call` (brief avant appel) avec la liste des lignes
   qui ont un `telephone`.

## Garde-fous

- Ne lance que si `telephone` est vide. `--force` sur demande explicite seulement.
- Jamais sans `--tier` ou `--max` sur une liste de plus de 50 lignes : à 10 crédits le numéro, une
  liste entière coûte vite plusieurs centaines de crédits.
- Coût annoncé avant, solde vérifié, `--confirmer` exigé au-delà de 100 crédits estimés.
- Numéro trouvé = donnée personnelle : usage professionnel, pas de SMS de masse, pas d'export vers
  un outil hors stack. Retrait immédiat de la ligne si la personne le demande (voir `05_Departements/Go-to-Market/GARDE-FOUS.md`).
- Rien d'inventé : pas de numéro deviné depuis le standard, la colonne reste vide si FullEnrich ne
  trouve pas.

## Erreurs fréquentes

| Symptôme | Cause | Fix |
|---|---|---|
| `[tier] 0 ligne(s) en tier A` | colonne `tier` vide ou notée autrement (A, "Tier A") | passer `qualifier-liste`, ou lancer sans `--tier` avec `--max` |
| HTTP 402 | solde insuffisant | recharger ; le script s'arrête avant si le solde ne couvre pas l'estimation |
| Beaucoup de `sans_cle_de_match` | pas d'entreprise ni de domaine | `enrichir-personne` d'abord |
| Numéros fixes au lieu de mobiles | FullEnrich renvoie le numéro le plus probable | garder, annoter, appeler quand même : c'est souvent une ligne directe |
| `--confirmer` refusé | coût estimé > 100 crédits | découper avec `--max`, ou valider explicitement puis relancer avec le drapeau |
