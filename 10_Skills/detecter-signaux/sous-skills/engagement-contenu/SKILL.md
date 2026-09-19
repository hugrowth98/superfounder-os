---
name: engagement-contenu
description: >
  Détecte les personnes qui réagissent à votre contenu (likes et commentaires sur vos posts, nouveaux abonnés, participants à vos webinars, abonnés et cliqueurs de votre newsletter) et déclenche l'approche dans les 24 à 48 heures, sur le sujet du contenu. Se déclenche sur : "qui a liké", "qui a commenté", "engagement sur mes posts", "mes abonnés", "nouveaux followers", "participants du webinar", "inscrits à ma newsletter", "qui a cliqué", "lead magnet", "commentaires sous mon post". Ne pas utiliser pour : l'engagement avec les posts d'un concurrent ou d'un influenceur, voir `signaux-concurrents` et la famille 5 de la taxonomie ; les visiteurs de votre site, non couverts.
---

Quelqu'un qui commente votre post, vient à votre webinar ou clique dans votre newsletter vous connaît déjà et parle de votre sujet cette semaine : taux de réponse de 25 à 30 %, un commentaire vaut 35 points, un like 25, et la fenêtre se ferme en 7 jours.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : commentaire 35, like 25, webinar 25, engagement avec un collaborateur 20, abonnement 15, clic 15, ouverture 5 à 10.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : like et commentaire j0 à j7, abonné j0 à j2, webinar j0 à j2.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 11 (nouveaux abonnés et engageurs), play 4 (enquête), play 5 (ressource).
- `{SKILL_BASE}/ressources/test-et-alors.md` : un like ne se cite jamais, un commentaire se continue.

## Méthode

1. **Choisir les contenus à surveiller.** Vos 5 derniers posts, vos posts qui ont dépassé la moyenne, les posts de vos collaborateurs qui publient, votre dernier webinar, votre dernière newsletter. Un post à 12 likes ne vaut pas un run ; un post à 200 réactions, si.
2. **Détecter** (Exécution). Posts : chaque jour ou chaque semaine selon votre rythme de publication. Webinar : la liste de présence le jour même. Newsletter : les clics de la dernière édition.
3. **Classer par force.** Commentaire, puis participant à un webinar, puis like, puis clic, puis abonné, puis ouverture. Un commentateur vaut deux likers ; un participant vaut deux inscrits.
4. **Qualifier.** ICP, exclusion des concurrents, des clients actuels, des personnes déjà en séquence. Sur un post qui marche, la moitié des engageurs sont hors cible.
5. **Dédoublonner et cumuler.** La même personne qui like trois posts en un mois vaut plus qu'un like isolé : additionnez, puis appliquez le multiplicateur du signal le plus récent.
6. **Dater.** `signal_date` = date de la réaction. j0 à j7 pour un like ou un commentaire, j0 à j2 pour un abonné ou un participant. Après 30 jours, contexte.
7. **Choisir l'angle** : le sujet du contenu et le problème qu'il touche, jamais la réaction. Un commentaire est une conversation publique : on la continue en citant l'idée de la personne. Un like ne se mentionne pas.
8. **Envoyer** sous 24 à 48 h, sur LinkedIn d'abord (la personne y est active), email ensuite.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1a | scraper_engagement | `scraper-engagement` | Unipile, `posts/{id}/reactions` et `posts/{id}/comments` sur vos posts et ceux de vos collaborateurs. Inclus dans l'abonnement, dans les quotas LinkedIn. Secours : `harvestapi/linkedin-post-comments`, 0,002 $ par commentaire, 0,004 $ avec le profil complet. |
| 1b | import | interne (Claude) | webinar, événement, newsletter : votre export CSV (inscrits, présents, abonnés, cliqueurs), colonnes ramenées aux noms normalisés |
| 1c | verifier_reponses | `verifier-reponses` | ouvertures et clics de vos séquences Lemlist |
| 1d | à la main | | nouveaux abonnés de votre profil ou de votre page : LinkedIn ne les liste pas par l'API, relevez-les depuis vos notifications, ou travaillez les engageurs |
| 2 | qualifier_liste | `qualifier-liste` | ICP, exclusions : concurrents, clients, salariés de clients, personnes déjà en séquence |
| 3 | dedoublonner | `dedoublonner` | contre HubSpot et vos séquences ; cumul des réactions d'une même personne sur 30 jours |
| 4 | enrichir_personne, trouver_email | `enrichir-personne`, `trouver-email` | profil complet, email vérifié |
| 5 | envoyer_sequence | `envoyer-sequence` | LinkedIn sous 24 à 48 h, email à j2, relance à j7 sur un autre angle |
| 6 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : la liste des URL de posts à surveiller ; ou votre export d'inscrits et de présents ; ou rien si le skill prend vos 5 derniers posts.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`commentaire`, `like`, `abonne`, `webinar_present`, `webinar_inscrit`, `newsletter_clic`, `newsletter_abonne`, `email_ouverture`), `signal_date`, `signal_detail` ("commentaire sous « {{titre du post}} » du {{date}} : {{extrait}}" ; "like sur 3 posts en 30 jours"), `score_signal`, `fraicheur`, `source` (`unipile`, `export_webinar`, `lemlist`).

## Repères

| Signal | Points | Fenêtre | Délai |
|---|---|---|---|
| Commentaire sur un de vos posts | 35 | j0 à j7, frais 30 j | sous 24 h |
| Participant à votre webinar | 25 | j0 à j2 (replay), frais 21 j | sous 48 h |
| Like sur un de vos posts | 25 | j0 à j7, frais 30 j | sous 48 h |
| Engagé avec le post d'un de vos collaborateurs | 20 | j0 à j7 | sous 72 h |
| Clic dans votre newsletter ou un email | 15 | j0 à j7 | sous 72 h |
| Abonné à votre page, votre profil, votre newsletter | 15 | j0 à j2 | sous 48 h, jamais seul |
| Inscrit à un webinar, absent | 15 (repère) | avant et après l'événement | nurture avec le replay |
| Ouvertures répétées sans clic | 10 | j0 à j7 | contexte |

| Repère | Valeur |
|---|---|
| Taux de réponse sur un engageur | 25 à 30 % : il vous connaît |
| Commentateur contre liker | 2 fois plus de valeur |
| Participant contre inscrit | le participant est venu ; l'inscrit absent reçoit le replay, pas un message de vente |
| Empilement type | commentaire (35) + like sur un autre post (25) + abonnement (15), dans la semaine ×1,2 = 90, Tiède ; plus une offre d'emploi ouverte (40×1,5) = 150, Brûlant |

## Template

Commentaire (on continue la conversation) :

```
Bonjour {{prenom}},

Votre remarque sur {{sujet_du_commentaire}} rejoint ce que je vois chez {{type_de_clients}} : {{probleme_precis}}. {{client_similaire}} l'a réglé avec {{solution}}, {{resultat_chiffre}}.

Vous le vivez de la même façon chez {{entreprise}} ?
```

Like ou abonné (on ne mentionne rien) :

```
Bonjour {{prenom}},

Sur {{sujet_du_post}}, la question qui revient chez les {{titre}} de {{secteur}}, c'est {{probleme}} : {{detail_concret}}. {{client_similaire}} l'a pris par {{solution}}.

C'est aussi votre sujet en ce moment, ou vous êtes passé à autre chose ?
```

## Règles

- Jamais "j'ai vu que vous aviez aimé mon post", jamais "merci pour l'abonnement". Le like ne se cite pas ; le commentaire se continue.
- Un abonné ou un liker seul reste Frais : on attend un second signal ou on l'ajoute au nurture.
- Un commentaire hostile ou hors sujet ne se travaille pas.
- Les inscrits absents à un webinar reçoivent le replay, pas un message de vente.
- Vos quotas LinkedIn passent avant le volume : on ne scrape pas 50 posts par jour.
- Une même personne qui réagit à trois posts reçoit un message, pas trois.
- Les concurrents et leurs salariés qui vous suivent sortent de la liste avant tout envoi.

## Exemples

- "Récupère tous ceux qui ont commenté mon post d'hier" : scraper_engagement sur l'URL du post, commentaires et réactions, qualification ICP, exclusions, commentateurs à 35 en tête, message LinkedIn sous 24 h qui continue leur remarque.
- "Qui est venu à mon webinar de mardi ?" : import de la liste de présence, colonnes normalisées, 25 points par présent, replay et proposition d'échange sous 48 h ; inscrits absents en nurture.
- "Cette personne a liké trois de mes posts ce mois-ci" : cumul 75 ×1,2 sur le plus récent = 90, Tiède ; on vérifie ses autres signaux (poste, offres, levée) ; message sur le sujet commun aux trois posts, sans mentionner les likes.
