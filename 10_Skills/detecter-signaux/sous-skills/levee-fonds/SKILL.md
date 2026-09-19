---
name: levee-fonds
description: >
  Détecte les levées de fonds et les introductions en bourse sur votre marché ou dans vos comptes cibles, les score par tour, et déclenche l'approche entre la semaine 2 et la semaine 8, sur la douleur d'échelle que l'argent crée. Se déclenche sur : "levée de fonds", "qui a levé", "tour de table", "seed", "série A", "série B", "introduction en bourse", "startups financées", "post-levée", "budget frais", "portefeuille d'un fonds". Ne pas utiliser pour : les rachats et fusions, voir `evenements-entreprise` ; le recrutement qui suit la levée, voir `recrutement`.
---

Une levée met de l'argent et des objectifs dans la même entreprise : le conseil attend que les fonds soient déployés, la douleur d'échelle arrive, et les bricolages sont remplacés par des systèmes. Fenêtre : semaines 2 à 8 après l'annonce pour un tour Seed à Série B, jamais la semaine 1 ; semaines 5 à 12 pour une Série C et plus.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : points par tour, seuils d'action.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : levée Seed à Série B frais 90 jours ; Série C et plus 180 jours, fenêtre semaines 5 à 12 ; introduction en bourse j30 à j60, frais 180 jours.
- `{SKILL_BASE}/ressources/detection-par-signal.md` : filtres, coût.
- `{SKILL_BASE}/ressources/test-et-alors.md` : la levée seule ne dit pas quel problème vous réglez.

## Méthode

1. **Fixer le filtre une fois.** Pays (France), tours qui correspondent à votre offre (une PME qui lève 1 M€ en seed n'achète pas comme une scale-up en Série B), montant minimum, tranche d'effectif. Le filtre vit dans `05_Departements/Go-to-Market/contexte.md`, section signaux prioritaires.
2. **Détecter chaque semaine** avec `--periode last_7d` : vous payez les nouveaux signaux, pas l'historique.
3. **Qualifier l'entreprise.** Score ICP, exclusions. Une levée hors ICP ne vaut rien.
4. **Trouver les bonnes personnes.** Dirigeant fondateur, responsable commercial ou marketing selon vos personas. Pas la personne qui a annoncé la levée : celle qui va dépenser l'argent sur votre sujet.
5. **Dater.** `signal_date` = date d'annonce. Semaine 1 : on attend, tout le monde félicite. Semaines 2 à 4 : pic, ils planifient la dépense. Semaines 5 à 8 : encore bon, les recrutements ont commencé. Semaine 9 et plus : les fournisseurs sont choisis. Série C et plus : semaines 1 à 4 trop tôt, semaines 5 à 12 pic. Introduction en bourse : j30 à j60.
6. **Scorer par tour** (Repères), multiplié par la position dans la fenêtre. Empilez avec les offres d'emploi ouvertes depuis la levée : c'est le duo le plus fréquent.
7. **Choisir l'angle.** Pas la levée : ce que l'argent va casser. Passer de 3 à 8 commerciaux, ouvrir un deuxième marché, industrialiser une prospection tenue par le fondateur. Le test "et alors ?" doit nommer une douleur précise, sinon on attend un second signal.
8. **Envoyer** en semaine 2 à 4 (Série C et plus : semaines 5 à 12 ; introduction en bourse : j30 à j60). Tour de 10 M$ et plus : message 1:1 sous 24 h après l'ouverture de la fenêtre. En dessous : séquence par signal sous 72 h.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1 | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | actor `signalbase/signalbase-api`, `--type funding --pays FR --round "Seed,Series A,Series B"` (selon votre ICP), `--montant-min 1000000` (en dollars, le script convertit en cents pour l'API), `--effectif-min` et `--effectif-max`, `--periode last_7d`, `--verification verified`. Introduction en bourse : `--round IPO`. Portefeuille d'un fonds : `--investisseur <nom>`, ou `--type investors`. 0,04 $ par résultat. |
| 2 | qualifier_liste | `qualifier-liste` | score ICP, exclusions |
| 3 | trouver_personnes | `trouver-personnes` | dirigeants et responsables selon `05_Departements/Go-to-Market/contexte.md`, 1 à 3 personnes par entreprise |
| 4 | enrichir_personne | `enrichir-personne` | profil complet : `headline`, `anciennete_poste`, `experiences` |
| 5 | trouver_email | `trouver-email` | email pro vérifié |
| 6 | dedoublonner | `dedoublonner` | contre HubSpot et vos séquences en cours |
| 7 | envoyer_sequence | `envoyer-sequence` | programmée à l'ouverture de la semaine 2 ; email puis LinkedIn puis relance sur un autre angle à j7 |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : aucun en mode marché ; en mode comptes cibles, `entreprise, domaine, linkedin_entreprise_url` passé en `--liste-suivie`, ou `--entreprise <nom>` pour un seul compte.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`levee`, y compris pour une introduction en bourse : le tour est dans `signal_detail` et dans la colonne `round`), `signal_date` (annonce), `signal_detail` ("{{tour}}, {{montant}} {{devise}}, {{investisseur principal}}"), `score_signal`, `fraicheur`, `source` (`signalbase/signalbase-api`).

## Repères

| Tour | Points | Ce que ça change chez eux |
|---|---|---|
| Pre-seed, Seed | 20 | budget limité, tout à construire, le fondateur fait encore tout |
| Série A (5 à 15 M$) | 35 | première stack, premières recrues commerciales |
| Série B (15 à 50 M$) | 45 | douleur d'échelle, remplacement des outils de départ |
| Série C et plus (50 M$ et plus) | 45 | standardisation, besoins d'entreprise |
| Introduction en bourse | 50 | transformation, conformité |

| Fenêtre depuis l'annonce (Seed à Série B) | Multiplicateur | Action |
|---|---|---|
| semaine 1 | trop tôt | on attend, ils font de la presse |
| semaines 2 à 4 | ×1,5 | contacter : ils planifient la dépense |
| semaines 5 à 8 | ×1,0 | contacter : les recrutements ont commencé |
| semaine 9 et plus | ×0,7 | contexte : le budget est engagé ailleurs |

Série C et plus : semaines 1 à 4 trop tôt, semaines 5 à 12 ×1,5, semaines 13 à 24 ×1,0, frais 180 jours. Introduction en bourse : j0 à j29 trop tôt, j30 à j60 ×1,5, j61 à j180 ×1,0.

| Repère | Valeur |
|---|---|
| Délai, tour de 10 M$ et plus | moins de 24 h après l'ouverture de la fenêtre, message 1:1 |
| Délai, tour de moins de 10 M$ | moins de 72 h, séquence par signal |
| Frais jusqu'à | 90 jours (180 pour une Série C et plus, fenêtre semaines 5 à 12, et pour une introduction en bourse, fenêtre j30 à j60) |
| Empilement type | levée Série A (35×1,5) + offre commerciale ouverte depuis 18 jours (40×1,5) = 113, Chaud |

## Template

```
Bonjour {{prenom}},

Passer de {{effectif_actuel}} à {{effectif_cible}} commerciaux en {{duree}}, c'est le moment où {{ce_qui_casse}} : {{detail_concret}}. {{client_similaire}} a fait ce passage l'an dernier, {{resultat_chiffre}}.

Vous avez déjà quelqu'un sur {{probleme}}, ou c'est encore vous ?
```

## Règles

- Jamais de formule de félicitation sur la levée : dix concurrents l'écrivent la même semaine. On parle de ce que l'argent va casser.
- Jamais la semaine 1.
- Le montant se donne en dollars au script : `--montant-min 1000000` pour 1 M$, le script convertit en cents pour l'API. Ne convertissez pas vous-même : deux zéros de trop vident la liste ou la noient.
- On écrit à la personne qui va dépenser sur votre sujet, pas à celle qui a signé le communiqué.
- Une levée hors ICP ne se score pas, même grosse : votre offre ne s'y vend pas.
- Filtre de date obligatoire : sans `--periode`, vous payez l'historique.
- On empile avec `recrutement` : les offres publiées depuis la levée disent où va l'argent, et donc quel angle prendre.

## Exemples

- "Qui a levé en France la semaine dernière ?" : detecter_signal `--type funding --pays FR --periode last_7d`, tours et effectif de `05_Departements/Go-to-Market/contexte.md`, qualification ICP, séquence programmée en semaine 2.
- "Cette boîte a levé 8 M€ il y a 3 semaines" : Série A, 35×1,5 = 53, Tiède seul ; on cherche ses offres d'emploi (`recrutement`) et un nouveau dirigeant (`changement-poste`) avant d'écrire ; l'angle vient de ce que l'argent va casser.
- "Les boîtes du portefeuille de tel fonds" : `--type investors`, ou `--type funding --investisseur <nom>`, liste des entreprises financées, qualification ICP, ciblage permanent (déclencheur relation 1 et 2 de la taxonomie), pas de fenêtre.
