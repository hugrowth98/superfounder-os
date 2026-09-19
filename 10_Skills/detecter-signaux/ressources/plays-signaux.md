# Les 11 plays : du signal à la campagne

> Un play = un signal, une séquence de verbes, un message type, un timing. Lu par les sous-skills quand l'utilisateur veut passer de la détection à la campagne. Les messages sont des points de départ : chaque variable entre doubles accolades se remplit avec un fait vérifié, jamais avec une supposition. Signature : votre prénom, une ligne.

| # | Play | Signal | Timing |
|---|---|---|---|
| 1 | Nouveau membre dans le service visé | une recrue arrive dans le service qui achète | semaines 2 à 4 après l'arrivée |
| 2 | Ciblage par compétences | le profil affiche une compétence liée à votre offre | en continu |
| 3 | Ciblage par titre rare | un titre inhabituel prouve qu'un budget existe | en continu |
| 4 | Enquête sectorielle | vous créez votre propre signal | valeur d'abord |
| 5 | Ressource pour les nouveaux arrivants | des personnes prennent un poste cible chaque semaine | permanent |
| 6 | Départ d'un collaborateur | quelqu'un quitte le service visé | semaines 1 à 2 après le départ |
| 7 | Rôle manquant | l'entreprise n'a personne sur une fonction | en continu, revu chaque trimestre |
| 8 | Avis négatifs sur un concurrent | un utilisateur identifiable a laissé un avis négatif | j0 à j60 |
| 9 | Trois idées, dont la vôtre | vous créez la valeur par la recherche | en continu |
| 10 | Champion qui change de poste | un ancien client ou interlocuteur arrive dans un compte cible | j0 à j14, séquence sur 10 jours |
| 11 | Nouveaux abonnés et engageurs | une personne dans l'ICP réagit à vos posts ou vous suit | 24 à 48 heures |

## Play 1 : nouveau membre dans le service visé

- **Signal** : un compte cible vient d'ajouter quelqu'un au service qui achète votre offre (commercial, marketing, ops selon `05_Departements/Go-to-Market/contexte.md`).
- **Verbes** : detecter_signal (`job-changes`, `companyLinkedinUrl` par compte, ou `departments` + `countries` sur le marché), puis qualifier_liste, puis trouver_personnes (le responsable du service, pas la recrue), puis enrichir_personne, puis trouver_email, puis envoyer_sequence.
- **À qui** : au responsable du service, pas au nouvel arrivant.
- **Message** :

```
Bonjour {{prenom}},

Une équipe {{service}} qui passe de {{n}} à {{n+1}}, c'est le moment où ce qui tenait dans la tête d'une personne doit être écrit : {{exemple_de_process}}. {{client_similaire}} a fait ce passage en {{delai}} et {{resultat_chiffre}}.

Qui s'en charge chez vous pendant que l'équipe grandit ?
```

- **Timing** : semaines 2 à 4 après l'arrivée. Avant, le responsable est en onboarding.

## Play 2 : ciblage par compétences

- **Signal** : le profil LinkedIn affiche une compétence qui prouve l'usage d'un outil ou d'une méthode liés à votre offre (un outil que vous complétez, une méthode que vous industrialisez).
- **Verbes** : trouver_personnes (titre, secteur, pays), puis enrichir_personne (le profil complet contient la rubrique compétences), puis qualifier_liste (ne garder que les profils avec la compétence), puis trouver_email, puis envoyer_sequence.
- **Pourquoi** : plus précis qu'un titre. Un "responsable marketing" avec la compétence "automatisation" n'a pas le même quotidien qu'un autre sans.
- **Message** : celui de votre séquence ICP, avec la compétence comme angle ("les équipes qui ont mis en place {{methode}} butent en général sur l'étape d'après : {{probleme}}").
- **Timing** : en continu, par lots hebdomadaires.

## Play 3 : ciblage par titre rare

- **Signal** : un titre inhabituel existe dans l'entreprise. "Responsable ops commerciales" veut dire que le sujet a un budget. "Growth engineer" veut dire qu'une fonction technique de croissance existe. Le titre est la preuve d'une priorité.
- **Verbes** : trouver_personnes (le titre rare, en booléen, sur votre marché), puis enrichir_entreprise (l'entreprise est-elle dans l'ICP), puis trouver_email, puis envoyer_sequence.
- **Message** : celui de votre séquence ICP, adressé à la personne qui porte le titre, sur le problème que ce titre est censé régler.
- **Timing** : en continu.

## Play 4 : enquête sectorielle

- **Signal** : aucun. Vous le créez : une enquête auprès de dirigeants de votre ICP sur un sujet qui les concerne. Ceux qui répondent deviennent un signal d'engagement actif (35 points) et la matière d'un contenu à publier.
- **Verbes** : trouver_personnes, puis trouver_email, puis envoyer_sequence (l'invitation), puis verifier_reponses (les répondants), puis envoyer_sequence (le résultat, avec une proposition d'échange).
- **Message** :

```
Bonjour {{prenom}},

Je réunis les pratiques de {{n}} {{titre}} de {{secteur}} sur {{sujet}} : ce qui marche, ce qui a été abandonné. Cinq questions, quatre minutes : {{lien}}.

Vous recevez la synthèse complète avant publication, avec votre nom cité si vous le souhaitez.
```

- **Timing** : valeur d'abord. La proposition commerciale vient avec la synthèse, pas avec l'invitation.

## Play 5 : ressource pour les nouveaux arrivants

- **Signal** : chaque semaine, des personnes prennent un poste cible (commercial, responsable marketing, dirigeant de PME). Campagne permanente, sans vente : vous offrez une ressource utile pour leurs premières semaines.
- **Verbes** : detecter_signal (`job-changes`, `positions` ou `seniorities` + `countries: FR`, `date_preset: last_7d`, chaque lundi), puis qualifier_liste, puis trouver_email, puis envoyer_sequence (un seul message, pas de relance).
- **Message** (le poste peut être mentionné : c'est un cadeau, pas une vente) :

```
Bonjour {{prenom}},

Pour les premières semaines à un poste de {{titre}}, j'ai rassemblé {{ressource}} : {{ce_qu_elle_contient}}, utilisée par {{n}} {{titre}} avant vous. C'est ici : {{lien}}.

Rien à me renvoyer. Si une partie vous sert, dites-le-moi, j'améliore la suivante.
```

- **Timing** : permanent, un envoi par semaine. Les répondants entrent dans `engagement-contenu` avec un signal actif.

## Play 6 : départ d'un collaborateur

- **Signal** : quelqu'un quitte le service visé d'un compte cible. Le trou de couverture commence le jour de son départ.
- **Verbes** : detecter_signal (`job-changes`, `companyLinkedinUrl` : la personne apparaît avec une nouvelle entreprise), puis trouver_personnes (le responsable du service qu'elle a quitté), puis enrichir_personne, puis trouver_email, puis envoyer_sequence.
- **À qui** : au responsable qui perd la personne. Jamais au partant.
- **Message** (on ne nomme pas la personne partie) :

```
Bonjour {{prenom}},

Quand un {{poste}} part, le pipe qu'il tenait se refroidit en trois semaines et le suivant met {{delai_ramp}} à reprendre le même niveau. {{client_similaire}} a tenu le rythme pendant la transition avec {{solution}} : {{resultat_chiffre}}.

Le remplacement est déjà lancé de votre côté ?
```

- **Timing** : semaines 1 à 2 après le départ.

## Play 7 : rôle manquant

- **Signal** : l'entreprise n'a personne sur une fonction que votre offre couvre ou remplace. Pas de responsable commercial dans une PME de 30 personnes, pas de responsable contenu dans une entreprise qui publie, pas d'ops commerciales alors que des SDR existent.
- **Verbes** : trouver_entreprises (votre ICP), puis trouver_personnes (le titre recherché, par entreprise : zéro résultat = rôle manquant), puis trouver_personnes (le dirigeant ou le responsable au-dessus du trou), puis trouver_email, puis envoyer_sequence.
- **Message** :

```
Bonjour {{prenom}},

Dans une entreprise de {{effectif}} personnes, {{fonction}} tombe en général sur le dirigeant, entre deux autres sujets. Chez {{client_similaire}}, ça représentait {{n}} heures par semaine avant qu'on {{solution}}.

C'est vous qui portez le sujet aujourd'hui ?
```

- **Timing** : en continu, liste revue chaque trimestre. Marche surtout pour une offre qui automatise ou externalise une fonction.

## Play 8 : avis négatifs sur un concurrent

- **Signal** : un utilisateur identifiable a laissé un avis négatif sur un concurrent, sur un comparateur de logiciels ou de prestataires. La douleur est documentée, publique, et datée.
- **Verbes** : lecture des comparateurs à la main (une fois par mois), puis trouver_personnes (l'auteur, par nom et entreprise), puis enrichir_personne, puis trouver_email, puis envoyer_sequence.
- **Message** (on cite le problème, pas l'avis) :

```
Bonjour {{prenom}},

{{Le_probleme_decrit_dans_l_avis}} revient chez presque tous les utilisateurs de {{categorie}} que je croise. On a pris le sujet à l'envers : {{votre_difference_concrete}}.

Je vous envoie une comparaison en une page, sans engagement ?
```

- **Timing** : j0 à j60 après l'avis, frais 180 jours. Jamais de critique du concurrent dans le message : vous êtes une alternative, pas un règlement de comptes.

## Play 9 : trois idées, dont la vôtre

- **Signal** : aucun. Vous créez la valeur : deux idées utiles pour son activité, produites à partir de son site et de sa page, et votre offre en troisième, annoncée comme telle.
- **Verbes** : enrichir_entreprise (site, page LinkedIn, derniers posts), puis Claude produit deux idées à partir de ce que vous avez lu, puis trouver_email, puis envoyer_sequence.
- **Message** :

```
Bonjour {{prenom}},

En lisant {{ce_que_vous_avez_lu}}, trois pistes pour {{objectif_du_prospect}} :
1. {{idee_1}}
2. {{idee_2}}
3. {{votre_offre_en_une_ligne}} (celle-là, c'est nous, autant le dire).

J'en aurais de meilleures avec quinze minutes de contexte. Preneur ?
```

- **Timing** : en continu. Les deux premières idées doivent tenir seules : si elles sont creuses, le message ne part pas.

## Play 10 : champion qui change de poste

- **Signal** : un ancien client, un ancien interlocuteur ou un ancien utilisateur de votre offre arrive dans un compte qui correspond à l'ICP. Le signal le plus fort du barème (75).
- **Verbes** : detecter_signal (`job-changes`, `personLinkedinUrl` sur votre liste de champions, chaque jour), puis qualifier_liste (la nouvelle entreprise est-elle dans l'ICP), puis enrichir_personne, puis trouver_email, puis trouver_telephone, puis dedoublonner (HubSpot), puis envoyer_sequence (LinkedIn + email), puis verifier_reponses.
- **Séquence** :

| Jour | Canal | Contenu |
|---|---|---|
| j0 | LinkedIn | invitation ou message court : un souvenir précis de ce qu'on avait fait ensemble |
| j1 | email | ce qui avait marché chez lui, et ce que ça donnerait dans son nouveau contexte |
| j3 | email | une étude de cas de son nouveau secteur |
| j7 | téléphone | appel |
| j10 | email | dernier message, proposition de café, pas de démo |
| j14 | | sans réponse : nurture, et on garde le contact chaud |

- **Message (j1)** :

```
Bonjour {{prenom}},

Chez {{ancienne_entreprise}}, {{ce_qu_on_avait_fait}} avait donné {{resultat}}. Chez {{entreprise}}, {{probleme_probable}} doit se poser à peu près de la même façon, avec {{difference_du_nouveau_contexte}} en plus.

Un café dans les deux semaines pour voir si ça se rejoue ?
```

- **Timing** : j0 à j14, avant la fin des 30 jours. Vous, à la main : c'est une relation, pas une séquence.

## Play 11 : nouveaux abonnés et engageurs

- **Signal** : une personne dans l'ICP réagit à un de vos posts, commente, ou s'abonne à votre profil.
- **Verbes** : scraper_engagement (vos 5 derniers posts, chaque jour ou chaque semaine), puis qualifier_liste (ICP, exclusion des concurrents), puis dedoublonner (déjà en séquence ? déjà client ?), puis enrichir_personne, puis trouver_email, puis envoyer_sequence.
- **Message** (un like ne se mentionne pas ; un commentaire se continue) :

```
Bonjour {{prenom}},

Chez les {{titre}} de {{secteur}} que je rencontre, le sujet du moment c'est {{probleme_du_post}} : {{detail_concret}}. {{client_similaire}} l'a pris par {{solution}} et {{resultat_chiffre}}.

C'est aussi votre sujet, ou vous êtes déjà passé à autre chose ?
```

- **Timing** : 24 à 48 heures après la réaction. Un commentateur passe avant un liker ; un liker sur trois posts passe avant un liker sur un.

## Ce qui vaut pour tous les plays

- Le message parle du problème que le signal crée, jamais du signal (`test-et-alors.md`).
- Le signal donne l'angle du premier message ; les relances changent d'angle, pas de formulation.
- Vous ne pouvez pas griller votre marché : un prospect qui n'a pas répondu à un play reçoit le suivant quand un nouveau signal apparaît, pas avant.
- Segmentez par signal et par persona, ne personnalisez pas chaque ligne à la main : 10 séquences modulaires battent 200 messages uniques.
- Un signal, un play, un responsable, un délai. Si personne n'est responsable, le play n'existe pas.
