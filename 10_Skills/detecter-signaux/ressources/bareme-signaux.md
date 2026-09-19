# Barème des signaux

> Lu par `multi-signaux` et par chaque sous-skill pour remplir la colonne `score_signal`. Les points sont des repères issus de campagnes B2B outbound, pas une vérité : recalibrez-les tous les mois avec vos propres réponses et rendez-vous.

## Comment lire ce barème

- Un signal vaut ses points bruts multipliés par son multiplicateur de fraîcheur (section 4).
- Plusieurs signaux sur la même personne ou le même compte s'additionnent (section 6).
- Le total tombe dans un niveau de chaleur (section 5) qui fixe l'action et le délai.
- Dans le CSV : `score_signal` = total après multiplicateurs, arrondi à l'entier. `fraicheur` = jours écoulés depuis le signal le plus récent. `signal_type` = les types séparés par `+`. `signal_detail` = un fait par signal, séparés par ` | `.

## 1. Tier 1 : signaux chauds (50 à 100 points)

| Signal | Points | Ce que ça révèle | Sous-skill |
|---|---|---|---|
| Demande de démo, de devis ou de tarif reçue par vous | 100 | intention d'achat directe | votre formulaire, votre CRM |
| Changement de poste d'un champion vers un compte cible | 75 | relation déjà construite, mandat de nouveauté | `changement-poste` |
| Plusieurs interlocuteurs d'un même compte actifs en 30 jours | 70 | comité d'achat en formation | `multi-signaux` |
| Inscription à un essai ou à une version gratuite de votre produit | 65 | évaluation en main | votre produit, votre CRM |
| Introduction en bourse | 50 | transformation, conformité, budgets neufs | `evenements-entreprise` |
| Client d'un concurrent qui a laissé un avis négatif | 50 | douleur documentée et publique | `signaux-concurrents` |

## 2. Tier 2 : signaux tièdes (20 à 49 points)

| Signal | Points | Ce que ça révèle | Sous-skill |
|---|---|---|---|
| Levée Série B, Série C et au-delà | 45 | douleur d'échelle, remplacement des bricolages | `levee-fonds` |
| Retrait d'un concurrent de la stack | 45 | remplacement en cours | `changement-techno` |
| Évaluation en cours chez un concurrent (cycle d'achat ouvert) | 45 | fenêtre d'achat ouverte | `signaux-concurrents` |
| Offre d'emploi pertinente pour votre offre | 40 | besoin budgété | `recrutement` |
| Entreprise rachetée | 40 | revue des fournisseurs inévitable | `evenements-entreprise` |
| Fusion | 40 | consolidation des outils | `evenements-entreprise` |
| Nouveau dirigeant inconnu dans un compte cible | 40 (proposé) | mandat de 90 jours | `changement-poste` |
| Levée Série A | 35 | première stack à construire | `levee-fonds` |
| Commentaire sur un de vos posts | 35 | engagement actif | `engagement-contenu` |
| Téléchargement d'une de vos études de cas | 35 | phase de recherche | votre site, votre CRM |
| Ajout d'un outil adjacent au vôtre | 35 | extension de la stack | `changement-techno` |
| Entreprise qui rachète | 35 | intégration, doublons d'outils | `evenements-entreprise` |
| Lancement de produit | 30 | équipe commerciale et marketing en formation | `evenements-entreprise` |
| Offre d'emploi qui mentionne un nouvel outil | 30 | migration en cours | `changement-techno` |
| Participation active à votre communauté | 30 | intérêt actif | votre communauté |
| Like sur un de vos posts | 25 | engagement passif | `engagement-contenu` |
| Participation à votre webinar (présent, pas inscrit) | 25 | intérêt pour la catégorie | `engagement-contenu` |
| Nouveau bureau, nouvelle implantation | 25 | expansion régionale | `evenements-entreprise` |
| Croissance générale de la stack (5 outils ou plus ajoutés) | 25 | mode achat actif | `changement-techno` |
| Engagement avec le contenu d'un concurrent | 25 | intérêt pour la catégorie | `signaux-concurrents` |
| Levée Pre-seed ou Seed | 20 | budget limité, tout à construire | `levee-fonds` |
| Engagement avec la page d'un de vos collaborateurs | 20 | notoriété par votre réseau | `engagement-contenu` |
| Ajout d'un concurrent de votre catégorie | 20 | besoin couvert, à revoir au renouvellement | `changement-techno` |
| Déménagement du siège | 20 | possible changement de fournisseurs | `evenements-entreprise` |

## 3. Tier 3 : signaux frais (5 à 19 points)

| Signal | Points | Ce que ça révèle | Sous-skill |
|---|---|---|---|
| Actualité d'entreprise sans autre précision (expansion, prix, presse) | 15 | déclencheur possible | `evenements-entreprise` |
| Abonnement à votre page ou à votre profil | 15 | notoriété | `engagement-contenu` |
| Abonnement à votre newsletter | 15 | notoriété | votre outil d'emailing |
| Clic dans un de vos emails | 15 | intérêt actif | `verifier-reponses` |
| Abonné d'un concurrent | 15 | conscience de la catégorie | `signaux-concurrents` |
| Mouvement marquant d'un concurrent (pub, lancement) | 15 | pression concurrentielle | `signaux-concurrents` |
| Téléchargement d'un rapport sectoriel | 10 | intérêt général | votre site |
| Ouvertures répétées de vos emails, sans clic | 10 | surveillance | `verifier-reponses` |
| Ouverture d'un email, sans clic | 5 | engagement minimal | `verifier-reponses` |

### Signaux du barème d'origine que ce master ne détecte pas

Gardez ces points si vous avez la donnée par ailleurs et saisissez-la à la main dans le CSV. Aucun outil de la stack ne la produit.

| Signal | Points |
|---|---|
| 3 visites ou plus de votre page tarifs en 7 jours | 80 |
| Comparaison de votre offre à un concurrent sur un comparateur de logiciels | 60 |
| 5 visites ou plus de votre site en 2 semaines | 50 |
| Client d'un concurrent qui visite votre site | 50 |
| Pic de recherche sur votre thème (donnée d'intention achetée) | 40 |
| 3 articles ou plus lus sur votre site | 20 |
| Visite unique de votre site | 10 |

## 4. Multiplicateurs de fraîcheur

Deux courbes, parce qu'un like de 20 jours ne vaut plus rien alors qu'une levée de 20 jours entre juste dans sa fenêtre.

### Signaux rapides : engagement, champion qui bouge, actualité, avis

| Ancienneté du signal | Multiplicateur |
|---|---|
| moins de 24 h | ×1,5 |
| 1 à 7 jours | ×1,2 |
| 8 à 14 jours | ×1,0 |
| 15 à 30 jours | ×0,7 |
| plus de 30 jours | ×0,3 |

### Signaux lents : levée, recrutement, techno, événements d'entreprise, nouveau dirigeant

| Position dans la fenêtre (voir `fenetres-fraicheur.md`) | Multiplicateur | Action |
|---|---|---|
| avant la fenêtre (trop tôt) | ×1,0 | le score compte, l'envoi attend l'ouverture |
| fenêtre optimale | ×1,5 | contacter |
| fenêtre secondaire | ×1,0 | contacter |
| après la fenêtre, signal encore frais | ×0,7 | contexte dans le message, pas d'accroche dessus |
| signal expiré | ×0,3 | retirer du scoring, retour au ciblage ICP |

La forme de cette seconde courbe est celle de la fenêtre du changement de poste (×1,5 au pic, ×1,0 ensuite, ×0,7 en fin de course), étendue aux autres signaux lents.

## 5. Seuils d'action et délais

| Score | Chaleur | Action | Délai | Qui |
|---|---|---|---|---|
| 150 et plus | Brûlant | appel, puis message écrit le même jour | moins d'1 heure | vous, à la main |
| 100 à 149 | Chaud | message 1:1 écrit pour cette personne, séquence courte | moins de 24 heures | vous, ou séquence 1:1 |
| 50 à 99 | Tiède | séquence semi-personnalisée par signal, surveillance des nouveaux signaux | moins de 72 heures | séquence |
| 20 à 49 | Frais | nurture : newsletter, invitation, contenu | cette semaine | automatique |
| 0 à 19 | Froid | rien, on surveille | en continu | système |

Si vous utilisez déjà les couleurs Rouge, Orange, Jaune, Gris : Rouge = Brûlant et Chaud, Orange = Tiède, Jaune = Frais, Gris = Froid.

Délais de référence : une demande entrante traitée en 5 minutes a 21 fois plus de chances d'être qualifiée qu'en 30 minutes. Un signal perd la moitié de sa valeur en 7 jours. Le premier fournisseur à contacter un champion qui vient de bouger a 3 fois plus de chances de signer.

## 6. Empilement

Additionnez les signaux d'une même personne, ou d'un même compte quand vous multi-threadez. Chaque signal garde son propre multiplicateur.

| Cas | Calcul | Score | Chaleur |
|---|---|---|---|
| Champion arrivé il y a 5 jours, levée Série B il y a 3 semaines (fenêtre optimale), commentaire hier | 75×1,2 + 45×1,5 + 35×1,5 = 90 + 67,5 + 52,5 | 210 | Brûlant |
| Levée Série A il y a 3 semaines, offre d'emploi commerciale publiée il y a 18 jours | 35×1,5 + 40×1,5 = 52,5 + 60 | 113 | Chaud |
| Like il y a 3 jours, abonnement à votre page il y a 10 jours, clic email il y a 2 jours | 25×1,2 + 15×1,0 + 15×1,2 = 30 + 15 + 18 | 63 | Tiède |
| Nouveau bureau il y a 40 jours (dans la fenêtre), ouverture d'email il y a 6 semaines | 25×1,5 + 5×0,3 = 37,5 + 1,5 | 39 | Frais |
| Abonné d'un concurrent depuis 2 mois | 15×0,3 | 5 | Froid |

Un seul signal frais de Tier 1 bat trois signaux vieux de Tier 2 : un champion arrivé hier vaut 75×1,5 = 113 (Chaud) ; une levée, une offre et un like vieux de 2 mois valent (45+40+25)×0,3 = 33 (Frais).

Comité d'achat : quand 2 personnes ou plus du même `domaine` portent chacune un signal dans les 30 derniers jours, ajoutez 70 au compte et traitez-le comme une seule affaire à multi-threader (un message par rôle, coordonnés dans la même semaine).

## 7. Recalibrage

- Après 30 jours : ajustez les seuils (150 / 100 / 50 / 20) si trop ou trop peu de comptes tombent en Chaud.
- Après 3 mois : ajustez les points de chaque signal à partir des réponses et rendez-vous obtenus, signal par signal.
- Mesurez la conversion signal vers rendez-vous, pas le volume de signaux détectés.
- Un signal qui n'a jamais produit un rendez-vous en 3 mois passe en contexte (Tier 3), quel que soit son score d'origine.
