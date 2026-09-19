---
name: changement-poste
description: >
  Détecte les changements de poste utiles à la prospection (un ancien client ou un champion qui arrive quelque part, un nouveau dirigeant dans un compte cible, tous les nouveaux titulaires d'un poste sur votre marché) et déclenche l'approche dans la fenêtre des jours 14 à 45. Se déclenche sur : "changement de poste", "vient d'être nommé", "nouveau directeur commercial", "nouveau dirigeant", "qui a pris un poste", "suivre mes anciens clients", "mes champions ont bougé", "période de grâce", "premiers 90 jours". Ne pas utiliser pour : les offres d'emploi et les vagues de recrutement, voir `recrutement` ; le rachat ou la réorganisation qui accompagne une nomination, voir `evenements-entreprise` (la nomination elle-même se traite ici).
---

Un dirigeant qui prend un poste a un mandat de résultats rapides, une période où changer de fournisseur ne se discute pas, et un budget qu'il n'a pas encore engagé : le taux de réponse est trois fois celui d'un contact à froid, avec un pic entre le jour 14 et le jour 45.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : champion 75, nouveau dirigeant 40, seuils d'action.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : champion j0 à j14, inconnu j14 à j45.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 10 (champion, séquence sur 10 jours), play 5 (ressource pour les nouveaux arrivants).
- `{SKILL_BASE}/ressources/test-et-alors.md` : avant d'écrire.

## Méthode

1. **Choisir le mode.** Trois cas, trois filtres : (a) vos champions, une liste de personnes que vous suivez ; (b) un compte cible, qui vient d'y arriver ; (c) votre marché, tous les nouveaux titulaires d'un poste en France ce mois-ci.
2. **Lancer la détection** (section Exécution). Cadence : chaque jour pour les champions, chaque semaine pour les deux autres modes.
3. **Qualifier l'entreprise d'arrivée.** Un champion qui arrive hors ICP reste un contact chaud, pas une séquence. Un inconnu hors ICP sort de la liste.
4. **Dater.** `signal_date` = date de prise de poste (le profil la donne au mois près ; le signal la donne au jour). `fraicheur` = jours écoulés. Avant j14 : on attend, sauf le champion à qui on écrit le jour même. j14 à j45 : pic. j46 à j90 : encore bon. Après j90 : expiré (×0,3), retour au ciblage ICP.
5. **Scorer.** Champion 75, inconnu 40, multiplié par la position dans la fenêtre. Ajoutez les autres signaux du compte (`multi-signaux`).
6. **Choisir l'angle** avec le test "et alors ?" : quelle douleur ce poste crée-t-il dans ses 90 premiers jours ? Un directeur commercial hérite d'un pipe et d'un CRM qu'il n'a pas choisis ; un directeur marketing hérite d'un site et d'une agence. Le message parle de ça, jamais de la nomination.
7. **Envoyer.** Champion : vous, à la main, LinkedIn puis email puis appel (play 10). Inconnu : séquence 1:1 courte, LinkedIn puis email, dans la fenêtre.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1 | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | actor `signalbase/signalbase-api`, `--type job-changes`. Mode champions : `--liste-suivie <csv des champions> --par-cible`, une requête exacte par `linkedin_url`. Mode compte cible : `--liste-suivie <csv des comptes> --par-cible` (une requête par `linkedin_entreprise_url`), ou `--entreprise-linkedin-url` pour un seul compte. Mode marché : `--pays FR --seniorites c_level,vp,director,head`, `--departements` et `--positions` selon vos personas, `--periode last_30d`. 0,04 $ par résultat. |
| 2 | qualifier_liste | `qualifier-liste` | score ICP de l'entreprise d'arrivée, exclusions (concurrents, clients actuels) |
| 3 | enrichir_personne | `enrichir-personne` | profil complet : `anciennete_poste` (prise de poste confirmée), `experiences` (ancien employeur, ancien titre), `headline` |
| 4 | trouver_email | `trouver-email` | email pro vérifié |
| 5 | trouver_telephone | `trouver-telephone` | champions seulement : l'appel du j7 |
| 6 | dedoublonner | `dedoublonner` | contre HubSpot : un champion est peut-être déjà un contact ouvert ou un deal en cours |
| 7 | envoyer_sequence | `envoyer-sequence` | dans la fenêtre. Champion : play 10. Inconnu : LinkedIn j0, email j2, relance j7 sur un autre angle |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 ; une réponse arrête la séquence |

**CSV en entrée** : mode champions, `prenom, nom, entreprise, linkedin_url` ; mode compte cible, `entreprise, linkedin_entreprise_url` ; mode marché, aucun fichier, les filtres suffisent.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`champion` ou `changement_poste`), `signal_date` (prise de poste), `signal_detail` ("ex-{{ancienne entreprise}}, {{ancien titre}} ; {{titre}} chez {{entreprise}} depuis {{date}}"), `score_signal`, `fraicheur`, `source` (`signalbase/signalbase-api`).

## Repères

| Fenêtre depuis la prise de poste | Multiplicateur | Action |
|---|---|---|
| j0 à j13 | trop tôt | surveiller ; le champion, lui, reçoit un message le jour même |
| j14 à j45 | ×1,5 | contacter : c'est le pic |
| j46 à j90 | ×1,0 | contacter : il construit encore sa stack |
| après j90 | ×0,3 | expiré : retour au ciblage ICP, ses fournisseurs sont choisis |

| Repère | Valeur |
|---|---|
| Points, champion vers un compte cible | 75 (Tier 1) |
| Points, nouveau dirigeant inconnu | 40 (proposé) |
| Taux de réponse | 3 fois celui d'un contact à froid |
| Délai, champion | moins de 24 h après détection : le premier fournisseur à écrire a 3 fois plus de chances de signer |
| Délai, inconnu | moins de 24 h après l'ouverture de la fenêtre (j14) |
| Champion : frais jusqu'à | 30 jours |
| Inconnu : frais jusqu'à | 90 jours |

## Template

Nouveau dirigeant inconnu, j14 à j45 (on ne félicite pas, on parle des 90 jours) :

```
Bonjour {{prenom}},

Reprendre {{perimetre}} chez {{entreprise}}, c'est hériter de {{ce_qu_il_herite}} sans l'avoir choisi, avec {{delai}} pour montrer un premier résultat. Chez {{client_similaire}}, la première brique a été {{action_concrete}} : {{resultat_chiffre}} en {{duree}}.

Vous prenez le sujet {{probleme}} en premier, ou il attend ?
```

Champion, j0 à j14 :

```
Bonjour {{prenom}},

Chez {{ancienne_entreprise}}, {{ce_qu_on_avait_fait}} avait donné {{resultat}}. Chez {{entreprise}}, {{probleme_probable}} doit se poser à peu près de la même façon, avec {{difference_du_nouveau_contexte}} en plus.

Un café dans les deux semaines pour voir si ça se rejoue ?
```

## Règles

- Jamais une phrase qui dit que vous avez vu le changement de poste, jamais une formule de félicitation sur la nomination. Le poste s'évoque par ce qu'il implique, pas par l'annonce.
- Un champion se traite à la main, par vous, sur trois canaux. Une séquence automatique gâche le signal le plus fort du barème.
- Avant j14, on n'écrit pas à un inconnu : il découvre son équipe, votre message tombe dans le vide.
- Un champion qui arrive hors ICP reçoit quand même un message : la relation vaut plus que le score.
- On empile : un nouveau dirigeant dans une entreprise qui vient de lever ou de publier une offre passe Chaud (`multi-signaux`).
- La liste de champions se tient à jour : anciens clients, anciens interlocuteurs, participants à vos ateliers, tous ceux qui ont vu votre travail de près.
- On ne paye pas 0,04 $ par résultat sur un marché entier sans filtre de pays, de séniorité et de date.

## Exemples

- "Préviens-moi quand un de mes anciens clients change de boîte" : mode champions, CSV de vos anciens clients avec `linkedin_url`, detecter_signal `--liste-suivie` sur ce CSV avec `--par-cible` chaque jour, message le jour même sur ce qu'on avait fait ensemble.
- "Qui vient d'être nommé directeur commercial dans une PME française ce mois-ci ?" : mode marché, `--type job-changes --positions "vp of sales" --seniorites head,director,vp --pays FR --periode last_30d`, qualification ICP, contact programmé à j14.
- "Un nouveau DG est arrivé chez un de mes comptes cibles il y a 3 semaines" : j21, pic de la fenêtre, 40 points ×1,5 ; test "et alors ?" sur ses 90 jours, message 1:1 sous 24 h, puis vérification des autres signaux du compte.
