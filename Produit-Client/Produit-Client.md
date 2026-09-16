---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Produit-Client

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

Un dossier par client et par produit. Chaque client signé a son dossier avec sa note (qui c'est, la mission, comment il aime travailler, où on en est), ses sources et ses livrables. Chaque produit packagé aussi.

`livrables/` à la racine contient ce qui n'est pas encore rattaché à une entité précise : supports d'offre, briefs génériques.

Ne va pas ici : un post LinkedIn qui mentionne un client (`Marketing/LinkedIn/`), une propale envoyée à un prospect pas encore signé (`Vente/Propositions/`), une étude de marché (`Strategie/`).

## Conventions

Un client signé devient un dossier avec sa note, créée depuis `Ressources/templates/note-de-dossier-client.md`. Tant qu'il n'a pas signé, il vit dans `Vente/`.

Chaque livrable est préfixé du nom du client : `NomClient_Sujet_YYYY-MM-DD.ext`. Ce qui vient du client (brief, export) va dans son `sources/`, ce qu'on lui livre dans son `livrables/`. Ses transcripts de calls vont dans `Meeting/` et ce qui s'y décide ruisselle vers sa note via `/done`.

Le contexte propre à un client (ses enjeux, ses interlocuteurs, l'historique) vit dans sa note, jamais dans `Contexte/` (qui décrit votre activité, pas la sienne).

Avant toute session sur un client, lire sa note.

## Organisation

- `<NomClient>/` un dossier par client : `<NomClient>.md`, `_log.md`, `sources/`, `livrables/`
- `livrables/` ce qui n'est pas rattaché à un client précis
- `sources/` briefs et exports non rattachés
- `ressources/` assets transverses aux clients

## Roadmap

- [ ]

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)

## Décisions actées
-

## Prochaines étapes
- [ ] Créer le dossier du premier client
<!-- ETAT:END -->

## Reprise

[Où on s'est arrêté, ce qui bloque, la première action de la prochaine session. Réécrit par /done.]

## Historique

[Une ligne par session, la plus récente en haut, avec le lien vers le journal. Écrit par /done.]

## Liens

-
