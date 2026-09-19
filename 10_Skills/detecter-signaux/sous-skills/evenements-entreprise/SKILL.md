---
name: evenements-entreprise
description: >
  Détecte les événements d'entreprise qui ouvrent une fenêtre d'achat (rachat, fusion, nouveau bureau, expansion géographique, partenariat, lancement de produit, réorganisation) et déclenche l'approche sur le problème que l'événement crée. Se déclenche sur : "rachat", "acquisition", "fusion", "M&A", "a été racheté", "nouveau bureau", "s'implante à", "expansion", "ouvre une antenne", "partenariat", "lancement de produit", "réorganisation". Ne pas utiliser pour : une levée de fonds ou une introduction en bourse, voir `levee-fonds` ; une offre d'emploi, voir `recrutement` ; une nomination ou un nouveau dirigeant, même dans une réorganisation, voir `changement-poste`.
---

Un rachat, une fusion, un nouveau bureau ou un lancement changent les priorités d'une entreprise et remettent ses fournisseurs sur la table : l'événement est public, daté, et la fenêtre dure de deux à six semaines après l'annonce.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : points par événement.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : rachat semaines 2 à 6 puis j60 à j90, nouveau bureau semaines 2 à 4, lancement semaines 1 à 2.
- `{SKILL_BASE}/ressources/taxonomie-declencheurs.md` : famille 6, firmographique (15 déclencheurs).
- `{SKILL_BASE}/ressources/test-et-alors.md` : un événement ne vaut que par le problème qu'il crée chez vous.

## Méthode

1. **Choisir les événements qui parlent à votre offre.** Pour un accompagnement commercial : rachat (deux équipes à fusionner), nouveau bureau (une équipe locale à monter), lancement (une offre à vendre). Pour du conseil en organisation : fusion, réorganisation. Les autres sont du contexte.
2. **Détecter.** Rachats et fusions : le signal `acquisitions`, chaque mois. Nouveaux bureaux : des postes ouverts dans une ville où l'entreprise n'était pas. Lancements, partenariats, réorganisations : les 5 derniers posts de la page entreprise (`enrichir-entreprise --posts`, colonne `posts_recents`), lus pour vos comptes cibles.
3. **Qualifier.** L'entreprise touchée est-elle dans l'ICP ? Dans un rachat, deux entreprises : l'acquéreur (intégration, 35) et l'acquise (revue des fournisseurs, 40). Les deux peuvent être des cibles.
4. **Dater.** `signal_date` = date de l'annonce. Rachat : semaine 1 trop tôt, semaines 2 à 6 pic, seconde fenêtre j60 à j90 après la clôture quand l'intégration commence. Nouveau bureau : semaines 2 à 4. Lancement : semaines 1 à 2.
5. **Scorer** (Repères), multiplié par la position dans la fenêtre.
6. **Chercher le second signal.** Un rachat s'accompagne presque toujours d'un changement de dirigeant (`changement-poste`) et d'offres d'emploi (`recrutement`). Un nouveau bureau, d'un recrutement local. C'est l'empilement qui fait passer Chaud.
7. **Choisir l'angle** : le problème opérationnel créé par l'événement. Deux CRM, deux façons de qualifier, un commercial seul loin du siège, une offre à lancer sans équipe dédiée.
8. **Envoyer** : rachat, fusion, lancement sous 72 h après l'ouverture de la fenêtre ; nouveau bureau, déménagement dans la semaine.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1a | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | actor `signalbase/signalbase-api`, `--type acquisitions --pays FR --periode last_30d`, `--effectif-min` et `--effectif-max`. 0,04 $ par résultat. Introduction en bourse : voir `levee-fonds`. |
| 1b | detecter_signal ou scraper_offres_emploi | `detecter-signaux` (script `detecter_signal.py`), `scraper-offres-emploi` | nouveau bureau : `--type hiring --ville <ville>`, ou offres LinkedIn filtrées par `--lieu <ville>` ; des postes dans une ville où l'entreprise n'avait personne. La ligne reste une `offre_emploi`, le nouveau bureau se note dans `signal_detail`. |
| 1c | enrichir_entreprise | `enrichir-entreprise --posts` | page LinkedIn de l'entreprise (Unipile) : effectif, adresse, `description`, `tagline`, et `posts_recents` (5 derniers posts). Lancement, partenariat, réorganisation, déménagement s'y lisent. Cadence mensuelle sur vos comptes cibles. |
| 1d | detecter_signal | `detecter-signaux` (script `detecter_signal.py`, `--source predictleads`) | si PredictLeads est branché (`signaux_secours:` dans `OUTILS.md`) : `--type events --pays FR --du <date>`, `--categories` expansion, nouveau bureau, partenariat, lancement, prix, nouveau client, rachat (les nominations `hires`, `promotes`, `leaves` reviennent à `changement-poste`). C'est la seule source qui couvre les événements sans lecture manuelle ; sans elle, 1c reste la méthode. |
| 2 | qualifier_liste | `qualifier-liste` | ICP des deux entreprises d'un rachat |
| 3 | trouver_personnes | `trouver-personnes` | le responsable qui porte le problème : direction commerciale pour une fusion d'équipes, dirigeant pour un nouveau bureau |
| 4 | enrichir_personne, trouver_email | `enrichir-personne`, `trouver-email` | profil complet, email vérifié |
| 5 | dedoublonner | `dedoublonner` | contre HubSpot |
| 6 | envoyer_sequence | `envoyer-sequence` | à l'ouverture de la fenêtre ; email puis LinkedIn puis relance sur un autre angle |
| 7 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : aucun en mode marché ; `entreprise, domaine, linkedin_entreprise_url` pour vos comptes cibles.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`acquisition` pour un rachat ou une fusion Signalbase, le côté, acquéreur ou acquise, dans `signal_detail` ; `offre_emploi` pour un nouveau bureau lu dans les offres ; `evenement:<categorie>` pour PredictLeads ou pour une lecture de la page, avec la catégorie PredictLeads : `evenement:opens_new_location`, `evenement:launches`, `evenement:partners_with`, `evenement:expands_offices_to`), `signal_date`, `signal_detail` ("a racheté {{entreprise}}, annoncé le {{date}}, {{source}}" ; "nouveau bureau à {{ville}}, {{n}} postes ouverts" ; "lancement de {{produit}}, post du {{date}}"), `score_signal`, `fraicheur`, `source` (`signalbase/signalbase-api`, `unipile`, `tagadanar/linkedin-jobs-scraper`).

## Repères

| Événement | Points | Fenêtre | Délai | Le problème créé |
|---|---|---|---|---|
| Entreprise rachetée | 40 | semaines 2 à 6, puis j60 à j90 | sous 72 h | revue des fournisseurs par l'acquéreur |
| Fusion | 40 | semaines 2 à 6 | sous 72 h | deux stacks, deux process, un seul à garder |
| Entreprise qui rachète | 35 | semaines 2 à 6 | sous 72 h | intégrer une équipe et ses outils |
| Lancement de produit | 30 | semaines 1 à 2, frais 60 j | sous 72 h | une offre à vendre sans équipe dédiée |
| Nouveau bureau, nouvelle ville | 25 | semaines 2 à 4, frais 90 j | dans la semaine | une équipe locale à monter, sans liste locale |
| Déménagement du siège | 20 | semaines 2 à 4 | dans la semaine | fournisseurs remis à plat |
| Partenariat, nouvelle intégration | 15 | j14 à j60 | dans la semaine | un écosystème qui s'étend |

Une nomination, même annoncée dans une réorganisation, relève de `changement-poste` (40 points, fenêtre j14 à j45). Une introduction en bourse relève de `levee-fonds` (50 points, fenêtre j30 à j60).

## Template

Rachat, à la direction commerciale de l'acquéreur, semaines 2 à 6 :

```
Bonjour {{prenom}},

Fusionner deux équipes commerciales, c'est deux CRM, deux façons de qualifier, et six mois où personne ne sait à qui appartient quel compte. {{client_similaire}} a tranché ça en {{delai}} avec {{solution}} : {{resultat_chiffre}}.

Le sujet est déjà sur votre table, ou pas encore ?
```

Nouveau bureau, au dirigeant, semaines 2 à 4 :

```
Bonjour {{prenom}},

Ouvrir une antenne à {{ville}}, c'est souvent un commercial seul, loin du siège, sans liste locale : le pipe met un trimestre à démarrer. {{client_similaire}} a raccourci ça à {{delai}} avec {{solution}}.

Qui porte le démarrage commercial sur place ?
```

## Règles

- Jamais une phrase qui dit que vous avez vu le rachat, jamais une formule de félicitation sur l'ouverture. On parle du problème d'intégration, d'antenne, de lancement.
- Semaine 1 d'un rachat : silence. Les équipes n'ont pas encore l'information elles-mêmes.
- Un rachat se lit des deux côtés : l'acquise vaut plus (40) que l'acquéreur (35), parce que ses fournisseurs vont être revus.
- Un événement seul reste Tiède au mieux : on cherche le second signal avant d'écrire.
- Les lancements et partenariats ne se détectent pas en masse dans la stack sans PredictLeads : réservez `enrichir-entreprise --posts` à vos comptes cibles, une fois par mois.
- Pas de supposition sur les conséquences d'un événement : si vous ne savez pas ce que le rachat change pour cette équipe, le test "et alors ?" échoue et vous attendez.

## Exemples

- "Quelles PME françaises ont été rachetées ce mois-ci ?" : detecter_signal `--type acquisitions --pays FR --periode last_30d`, tranche d'effectif de l'ICP ; acquises à 40, acquéreurs à 35 ; contact en semaine 2 sur la fusion des équipes.
- "Un compte cible ouvre un bureau à Lyon" : postes ouverts à Lyon vérifiés par scraper_offres_emploi, 25 points ×1,5 en semaine 2 à 4 ; message au dirigeant sur le démarrage commercial local ; on cherche le responsable local recruté (`changement-poste`).
- "Cette entreprise lance un nouveau produit" : lu dans `posts_recents` de sa page, 30 points, semaines 1 à 2 ; angle "une offre à vendre sans équipe dédiée" ; on empile avec les offres d'emploi ouvertes pour le lancement avant d'écrire.
