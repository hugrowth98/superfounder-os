---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Meeting

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

Les transcripts de calls, un fichier par call, dans cinq dossiers : Clients, Events, Prospects, Interne, Autres. C'est la matière première la plus sous-exploitée d'un business de service : les mots exacts des clients, leurs objections, leurs douleurs.

Ne va pas ici : le compte rendu envoyé au client après le call (il va dans `Produit-Client/<Client>/livrables/`), les notes de réunion interne sans transcript.

## Conventions

Nommage `YYYY-MM-DD_<client-ou-prospect>_<sujet>.md`.

Routage d'un nouveau transcript, premier match gagne :

1. Coaching 1:1 d'un dirigeant (séance, atelier individuel, kick off coaching) : `Clients/Coaching/<Nom>/`.
2. Mission en cours avec un client (audit, done-with-you, ateliers d'équipe) : `Clients/Actuels/<Nom>/`, le même nom que dans `Produit-Client/`.
3. Atelier cold call en groupe : `Clients/Ateliers-cold-call/YYYY-MM/`.
4. Atelier collectif (IA, outils, méthode) : `Clients/Ateliers-collectifs/YYYY-MM/`.
5. Event marketing que vous organisez : `Events/Live/` ou `Events/Challenge/`.
6. Premier ou deuxième call avec une personne externe : `Prospects/YYYY-MM/`.
7. Call sans personne externe (équipe, board, partenaire) : `Interne/YYYY-MM/`.
8. Rien de tout ça : `Autres/YYYY-MM/`.

Un prospect devient client ou coaché au troisième call, ou dès qu'un atelier, un coaching, un kick off ou un onboarding est planifié. On crée alors son dossier et on y remonte tous ses calls de `Prospects/` : l'historique reste ensemble.

Quand une mission ou un coaching se termine, le dossier passe dans `Clients/Anciens-clients/<Nom>/` tel quel.

Nom d'un dossier : le nom canonique de la boîte quand il y en a une, sinon `Prenom-Nom`.

Ce dossier fait exception à la règle des deux niveaux : `Clients/Coaching/<Nom>/` en a trois.

Ce qui se décide dans un call ruisselle vers la note du client concerné via `/done`. Les douleurs entendues alimentent `Contexte/Clients-Problems-and-Messages.md` (proposé en diff) et les idées de contenu.

## Organisation

- `Clients/Actuels/<Nom>/` : un dossier par mission en cours, tous ses calls dedans.
- `Clients/Coaching/<Nom>/` : un dossier par dirigeant coaché en 1:1.
- `Clients/Anciens-clients/<Nom>/` : les missions et coachings terminés, dossier déplacé tel quel.
- `Clients/Ateliers-cold-call/YYYY-MM/` : les sessions de cold call en groupe.
- `Clients/Ateliers-collectifs/YYYY-MM/` : les ateliers collectifs.
- `Events/Live/`, `Events/Challenge/` : les events marketing que vous organisez.
- `Prospects/YYYY-MM/` : les premiers calls sans suite, rangés par mois.
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
