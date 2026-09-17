---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Meeting

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

Les transcripts de calls, un fichier par call, rangés par nature de la relation : clients, prospects, events, interne, autres. C'est la matière première la plus sous-exploitée d'un business de service : les mots exacts des clients, leurs objections, leurs douleurs.

Ne va pas ici : le compte rendu envoyé au client après le call (il va dans `Produit-Client/<Client>/livrables/`), les notes de réunion interne sans transcript.

## Conventions

Nommage `YYYY-MM-DD_<client-ou-prospect>_<sujet>.md`.

Routage d'un nouveau transcript, premier match gagne :

1. La personne ou la boîte a un dossier dans `Clients/` : il y va.
2. Atelier collectif, challenge, masterclass, live, formation ouverte : `Events/<Nom-event>/`.
3. Call sans personne externe (équipe, board, partenaire opérationnel) : `Interne/YYYY-MM/`.
4. Premier ou deuxième call avec une personne externe : `Prospects/YYYY-MM/`.
5. Rien de tout ça : `Autres/YYYY-MM/`.

Un prospect devient client au troisième call, ou dès qu'un atelier, un coaching, un kick off ou un onboarding est planifié. On crée alors `Clients/<Nom>/` et on y remonte tous ses calls de `Prospects/` : l'historique reste ensemble.

Nom d'un dossier client : le nom canonique de la boîte quand il y en a une (le même que dans `Produit-Client/`), sinon `Prenom-Nom`.

Ce qui se décide dans un call ruisselle vers la note du client concerné via `/done`. Les douleurs entendues alimentent `Contexte/Clients-Problems-and-Messages.md` (proposé en diff) et les idées de contenu.

## Organisation

- `Clients/<Nom>/` : un dossier par client, tous ses calls dedans, du premier rdv au dernier atelier.
- `Prospects/YYYY-MM/` : les premiers calls sans suite, rangés par mois.
- `Events/<Nom-event>/` : ateliers collectifs, challenges, masterclasses, un dossier par event.
- `Interne/YYYY-MM/` : équipe, board, partenaires, rangés par mois.
- `Autres/YYYY-MM/` : ce qui ne rentre nulle part.

## Roadmap

- [ ]

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)

## Décisions actées
-

## Prochaines étapes
- [ ] Déposer un premier transcript
<!-- ETAT:END -->

## Reprise

[Où on s'est arrêté, ce qui bloque, la première action de la prochaine session. Réécrit par /done.]

## Historique

[Une ligne par session, la plus récente en haut, avec le lien vers le journal. Écrit par /done.]

## Liens

-
