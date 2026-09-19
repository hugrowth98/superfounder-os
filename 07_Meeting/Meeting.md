---
type: departement
status: active
date: AAAA-MM-JJ
maj: AAAA-MM-JJ
---

# Meeting

## Mission

Les transcripts de vos calls, un fichier par call. C'est la matière première la plus sous-exploitée d'un business de service : les mots exacts de vos clients, leurs objections, leurs douleurs.

Ne va pas ici : le compte rendu envoyé au client après le call (il va dans `06_Clients/<Client>/`), les notes de réunion sans transcript.

## Cadre

Nommage `Transcript_Sujet_YYYY-MM-DD.md`. Routage d'un nouveau transcript, premier match gagne :

1. Call avec un client signé : `Clients/<Nom>/`, le même nom que dans `06_Clients/`.
2. Call avec une personne externe pas encore cliente : `Prospects/YYYY-MM/`.
3. Call sans personne externe (équipe, associé, partenaire) : `Interne/YYYY-MM/`.
4. Rien de tout ça : `Autres/YYYY-MM/`.

Un prospect devient client à la signature. On crée alors `Clients/<Nom>/` et on y remonte tous ses calls de `Prospects/` : l'historique reste ensemble. Quand une mission se termine, le dossier part dans `11_Archives/` tel quel.

Ce qui se décide dans un call ruisselle vers la note du client via `/done`. Les douleurs entendues alimentent `02_Contexte/Clients-Problems-and-Messages.md` (proposé en diff) et vos idées de contenu.

- `Clients/<Nom>/` : un dossier par client signé
- `Prospects/YYYY-MM/` : les premiers calls, rangés par mois
- `Interne/YYYY-MM/` : équipe, associés, partenaires
- `Autres/YYYY-MM/` : ce qui ne rentre nulle part

## Où on en est

- [ ] Déposer un premier transcript

## Key Notes

- [[Clients]]
