---
name: signaux-concurrents
description: >
  Détecte les personnes qui gravitent autour de vos concurrents (engageurs de leurs posts, auteurs d'avis négatifs, clients identifiés, entreprises dont les pubs tournent ; les abonnés d'une page ne se listent pas) et déclenche l'approche sur le problème que le concurrent laisse ouvert. Se déclenche sur : "mes concurrents", "ceux qui suivent mon concurrent", "commentent chez mon concurrent", "avis négatifs", "clients de mon concurrent", "insatisfaits de", "les pubs de mon concurrent", "alternative à", "renouvellement chez un concurrent". Ne pas utiliser pour : un outil concurrent qui apparaît ou disparaît d'une stack, voir `changement-techno` ; l'engagement avec vos propres posts, voir `engagement-contenu`.
---

Les gens qui commentent chez un concurrent, qui le notent mal ou qui l'utilisent sont déjà dans votre catégorie, cette semaine : un avis négatif documenté vaut 50 points, un engagement avec le contenu d'un concurrent en vaut 25, et les deux se travaillent sans jamais dénigrer le concurrent.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : avis négatif 50, cycle d'évaluation 45, fin de contrat 45, engagement 25, client identifié 20, pub active 15.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : engagement j0 à j7, avis j0 à j60 (frais 180 jours), pub tant qu'elle tourne.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 8 (avis négatifs).
- `{SKILL_BASE}/ressources/taxonomie-declencheurs.md` : famille 4, concurrents (déclencheurs 8 à 16).

## Méthode

1. **Lister les concurrents dans `05_Departements/Go-to-Market/contexte.md`** : leur page LinkedIn, leurs dirigeants et salariés qui publient, la catégorie où on les compare, leur outil quand il laisse une trace sur un site.
2. **Choisir la source.** Quatre, du plus chaud au plus froid : (a) les auteurs d'avis négatifs ; (b) les engageurs de leurs posts et de ceux de leurs salariés ; (c) leurs clients identifiés ; (d) les entreprises dont les pubs tournent dans votre catégorie.
3. **Les abonnés d'une page ne s'exportent pas.** LinkedIn ne donne pas cette liste. Passez par les engageurs des 10 derniers posts : même population, en plus chaud.
4. **Détecter** (Exécution). Engageurs chaque semaine, avis chaque mois, clients chaque trimestre, pubs chaque mois.
5. **Qualifier.** ICP, et exclusion des salariés du concurrent, de ses partenaires et de vos clients actuels : un engageur sur trois est un collègue ou un ami du concurrent.
6. **Dater et scorer.** Engagement : j0 à j7, courbe rapide. Avis : j0 à j60, courbe lente. Client identifié : permanent, à réveiller 60 à 90 jours avant le renouvellement quand vous connaissez la date.
7. **Choisir l'angle** : le problème que le concurrent laisse ouvert, décrit dans l'avis ou dans les commentaires, et votre différence concrète. Pas de comparaison agressive : une alternative, pas un règlement de comptes.
8. **Envoyer** : avis négatif sous 24 h après identification ; engageur sous 72 h ; client identifié à l'approche du renouvellement.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1a | scraper_engagement | `scraper-engagement` | Unipile : `--post <url>` pour les derniers posts de la page du concurrent (URL relevées sur la page), `--mes-posts 10 --posts-de <slug>` pour chacun de ses salariés qui publient. Inclus dans l'abonnement, dans les quotas LinkedIn. Secours : `harvestapi/linkedin-post-comments`, 0,002 $ par commentaire. |
| 1b | lecture à la main, puis trouver_personnes | `trouver-personnes` | avis négatifs : lecture mensuelle des comparateurs de logiciels ou de prestataires de votre catégorie ; auteur retrouvé par Sales Nav quand nom et entreprise sont visibles. Aucun actor d'avis dans la stack. |
| 1c | detecter_techno, scraper_offres_emploi | `enrichir-entreprise --techno`, `scraper-offres-emploi` | clients d'un concurrent : son outil détecté sur le site par `enrichir-entreprise --techno --cherche <outil>` (`scrapemint/website-tech-stack-detector`, colonne `techno_cible = oui`), ou demandé dans une offre (`--mots-cles` = nom du concurrent). Page clients du concurrent lue à la main chaque trimestre. |
| 1d | scraper_pubs | `enrichir-entreprise --pubs` | pubs actives : `curious_coder/facebook-ads-library-scraper` pour Meta (0,00075 $ par pub) ; LinkedIn selon le skill. Sur le concurrent (`pub_active`, 15 : un budget marketing actif chez lui) et sur votre catégorie (les entreprises qui dépensent = budget actif, 15). |
| 2 | qualifier_liste | `qualifier-liste` | ICP, exclusion des salariés et partenaires du concurrent, de vos clients |
| 3 | dedoublonner | `dedoublonner` | contre HubSpot et vos séquences ; un engageur revient chaque semaine |
| 4 | enrichir_personne, trouver_email | `enrichir-personne`, `trouver-email` | profil complet, email vérifié |
| 5 | envoyer_sequence | `envoyer-sequence` | LinkedIn d'abord pour un engageur (il est actif là), email pour un auteur d'avis |
| 6 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : `entreprise, linkedin_entreprise_url, domaine` pour les concurrents, et la liste de leurs salariés qui publient (`linkedin_url`).

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`commentaire` ou `like` pour un engageur ; `techno` pour un client identifié par son site ; `pub_active` pour une pub qui tourne ; un avis négatif, saisi à la main, est une ligne `profil_entreprise` dont `signal_detail` porte l'avis), `signal_date`, `signal_detail` ("commentaire sous le post de {{concurrent}} du {{date}} : {{extrait}}" ; "avis {{note}}/5 du {{date}} sur {{concurrent}} : {{problème cité}}" ; "utilise {{concurrent}}, détecté sur {{domaine}}"), `score_signal`, `fraicheur`, `source` (`unipile`, `scrapemint/website-tech-stack-detector`, `curious_coder/facebook-ads-library-scraper` ; vide pour un avis saisi à la main).

## Repères

| Signal | Points | Fenêtre | Délai |
|---|---|---|---|
| Client parti d'un concurrent, avis négatif | 50 | j0 à j60, frais 180 j | sous 24 h |
| Client d'un concurrent en cycle d'évaluation (vous l'apprenez par le réseau) | 45 | j0 à j30 | sous 24 h |
| Fin de contrat annuel chez un concurrent | 45 | j60 à j90 avant l'échéance | à la date |
| Engagé avec les posts d'un concurrent ou de ses salariés | 25 | j0 à j7, frais 30 j | sous 72 h |
| Client d'un concurrent identifié | 20 | permanent | au renouvellement |
| Abonné d'un concurrent (non listable, saisi à la main) | 15 | permanent | à empiler, jamais seul |
| Pub active du concurrent ou d'une entreprise de votre catégorie | 15 | tant qu'elle tourne | dans la semaine, à empiler |

| Repère | Valeur |
|---|---|
| Engageur d'un concurrent qui commente aussi chez vous | 25 + 35 = 60, Tiède ; les deux dans la semaine ×1,2 = 72 |
| Part des engageurs à exclure (salariés, partenaires, amis du concurrent) | à vérifier à chaque run : souvent un sur trois |
| Renouvellement | contrat annuel : fenêtre de changement 60 à 90 jours avant la date anniversaire |

## Template

Engageur des posts d'un concurrent, sur LinkedIn :

```
Bonjour {{prenom}},

Les {{titre}} qui regardent {{categorie}} en ce moment butent souvent sur {{probleme}} : {{detail_concret}}. C'est le point qu'on a pris à l'envers : {{votre_difference}}.

Une comparaison en deux minutes vous serait utile ?
```

Auteur d'un avis négatif, par email :

```
Bonjour {{prenom}},

{{Le_probleme_decrit_dans_l_avis}} revient chez presque tous les utilisateurs de {{categorie}} que je croise : {{consequence_concrete}}. On a construit {{votre_difference}} pour ça, chez {{client_similaire}} ça a donné {{resultat_chiffre}}.

Je vous envoie une comparaison en une page ?
```

## Règles

- Jamais "j'ai lu votre avis", jamais "je vois que vous suivez {{concurrent}}". On parle du problème, pas de la trace.
- On ne dénigre jamais le concurrent, même quand l'avis le fait. Vous êtes l'alternative, pas l'avocat de l'accusation.
- Un abonné seul ne reçoit rien : 15 points, c'est du contexte. Il faut un second signal.
- Les salariés, partenaires et amis du concurrent sortent de la liste avant tout envoi.
- Un avis n'est exploitable que si son auteur est identifiable par son nom et son entreprise ; on ne devine pas une identité.
- Les abonnés d'une page ne se listent pas : on ne promet pas cette liste, on travaille les engageurs.
- Les pubs actives disent qu'un budget existe, pas qu'un besoin existe : signal de contexte, à empiler.

## Exemples

- "Récupère les gens qui commentent chez mon concurrent" : scraper_engagement sur les URL de ses derniers posts de page et `--mes-posts 10 --posts-de <slug>` pour ses deux dirigeants, exclusion des salariés et partenaires, qualification ICP, 25 points, message LinkedIn sous 72 h sur le problème de la catégorie.
- "Trouve les insatisfaits de tel prestataire" : lecture des comparateurs de la catégorie, auteurs identifiables retrouvés par trouver_personnes, 50 points, email sous 24 h sur le problème décrit, comparaison en une page proposée.
- "Qui utilise l'outil de mon concurrent parmi mes comptes cibles ?" : `enrichir-entreprise --techno --cherche <outil du concurrent>` sur la colonne `domaine` (colonne `techno_cible = oui`), `signal_type` = `techno`, 20 points, ciblage permanent, réveil 60 à 90 jours avant le renouvellement quand la date de signature est connue.
