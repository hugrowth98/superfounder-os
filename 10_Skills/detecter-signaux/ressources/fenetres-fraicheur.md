# Fenêtres de fraîcheur par signal

> Lu par chaque sous-skill pour dater un signal et par `multi-signaux` pour choisir le multiplicateur. Trois questions par signal : jusqu'à quand il est frais, quand il faut écrire, à quelle vitesse il perd sa valeur.

## La table

Les jours se comptent depuis la date du signal (`signal_date`), pas depuis le jour où vous l'avez détecté. "Trop tôt" veut dire : le score compte, l'envoi attend.

| Signal | Frais jusqu'à | Trop tôt | Fenêtre optimale | Fenêtre secondaire | Décroissance | Courbe |
|---|---|---|---|---|---|---|
| Champion qui change de poste (vous le connaissez) | 30 j | jamais | j0 à j14 | j15 à j30 | la plus rapide | rapide |
| Nouveau dirigeant inconnu dans un compte cible | 90 j | j0 à j13 | j14 à j45 | j46 à j90 | modérée | lente |
| Like, commentaire sur un post | 30 j | jamais | j0 à j7 | j8 à j14 | rapide | rapide |
| Nouvel abonné à votre page ou profil | 30 j | jamais | j0 à j2 | j3 à j7 | rapide | rapide |
| Participation à un webinar ou à un événement | 21 j | jamais | j0 à j2 (envoi du replay) | j3 à j7 | rapide | rapide |
| Salon, conférence où le prospect va | 21 j | plus de 14 j avant | j-7 à j+7 autour de l'événement | j-14 à j-8 | rapide | rapide |
| Levée de fonds (Seed à Série B) | 90 j | semaine 1 | semaines 2 à 4 | semaines 5 à 8 | modérée | lente |
| Levée Série C et au-delà (phase de déploiement) | 180 j | semaines 1 à 4 | semaines 5 à 12 | semaines 13 à 24 | lente | lente |
| Offre d'emploi pertinente | 60 j | jamais | j14 à j30 depuis la publication | j0 à j13 et j31 à j60 | modérée | lente |
| Vague de recrutement (5 postes ou plus) | 90 j | jamais | j14 à j30 | j31 à j90 | modérée | lente |
| Départ d'un collaborateur du service visé | 30 j | jamais | semaines 1 à 2 | semaines 3 à 4 | rapide | rapide |
| Nouveau membre dans le service visé | 60 j | semaine 1 | semaines 2 à 4 | semaines 5 à 8 | modérée | lente |
| Adoption ou retrait d'une techno | 60 j | jamais | j0 à j30 | j31 à j60 | modérée | lente |
| Offre d'emploi qui mentionne une migration d'outil | 60 j | jamais | j0 à j30 | j31 à j60 | modérée | lente |
| Rachat, fusion | 90 j | semaine 1 | semaines 2 à 6 après l'annonce | j60 à j90 après la clôture (l'intégration commence) | modérée | lente |
| Introduction en bourse | 180 j | j0 à j29 | j30 à j60 | j61 à j180 | lente | lente |
| Nouveau bureau, expansion géographique | 90 j | semaine 1 | semaines 2 à 4 | semaines 5 à 12 | modérée | lente |
| Lancement de produit | 60 j | jamais | semaines 1 à 2 | semaines 3 à 8 | modérée | lente |
| Partenariat annoncé | 60 j | jamais | j14 à j60 | j0 à j13 | modérée | lente |
| Avis négatif laissé sur un concurrent | 180 j | jamais | j0 à j60 | j61 à j180 | lente | lente |
| Engagement avec le contenu d'un concurrent | 30 j | jamais | j0 à j7 | j8 à j14 | rapide | rapide |
| Pub active d'un concurrent | tant qu'elle tourne | jamais | pendant la diffusion | 30 j après l'arrêt | nulle puis brutale | rapide |
| Actualité, mention presse | 30 j | jamais | j7 à j30 | j0 à j6 | modérée | rapide |
| Changement réglementaire qui touche le prospect | 60 j | jamais | j0 à j60 | j61 à j90 | modérée | lente |
| Demande de démo ou de devis reçue par vous | 7 j | jamais | 5 premières minutes | même journée | très rapide | rapide |

## Comment s'en servir

1. **Dans la fenêtre optimale** : le signal est l'angle du message. Vous écrivez dessus (sur le problème qu'il crée, jamais sur le signal lui-même, voir `test-et-alors.md`).
2. **Frais mais hors fenêtre optimale** : le signal est du contexte. Il colore le message, il n'en est pas l'accroche. Multiplicateur ×0,7 pour un signal lent, ×0,7 ou ×0,3 pour un rapide selon l'ancienneté.
3. **Expiré** : retirez-le du scoring et du message. Retour au ciblage par ICP, ou attente du prochain signal.
4. **Trop tôt** : le score compte, l'envoi est programmé à l'ouverture de la fenêtre. Une exception : un champion, on lui écrit le jour même.

## Trois règles de timing

- **La fenêtre l'emporte sur la détection.** Une offre d'emploi détectée le jour de sa publication n'oblige pas à écrire le jour même : programmez le contact à j14, sauf si le score cumulé du compte est déjà Chaud.
- **Le premier arrivé gagne, mais pas la semaine 1.** Sur une levée ou une nomination, la semaine de l'annonce est saturée de félicitations. Écrire en semaine 2 ou 3 vous sort du lot.
- **Relance dans la fenêtre, silence hors fenêtre.** Sans réponse et signal encore dans sa fenêtre : relancez avec un nouvel angle (autre douleur, autre preuve), pas une reformulation. Signal hors fenêtre : pas de relance à froid, attendez le prochain signal.

## Cadence de détection par signal

| Cadence | Signaux |
|---|---|
| chaque jour | champions (changements de poste sur votre liste), engagement sur vos posts, demandes entrantes |
| chaque semaine | levées, offres d'emploi, changements de poste sur le marché, engagement sur les posts des concurrents, pubs actives |
| chaque mois | techno (comparaison avec le mois précédent), rachats et fusions, nouveaux bureaux, avis sur les concurrents |
| chaque trimestre | rôles manquants dans les comptes cibles, clients des concurrents |
