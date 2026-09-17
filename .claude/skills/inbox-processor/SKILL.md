---
name: inbox-processor
description: Trier les items de Inbox/ et les router vers le bon dossier de travail, Contexte, le wiki Veille ou Archives, en suivant les regles de routage du CLAUDE.md racine.
user-invocable: true
context: main
---

# Inbox Processor

Tu aides l'utilisateur a vider son `Inbox/` en routant chaque item au bon endroit.

## Contexte
`Inbox/` (a la racine du workspace) est un point de capture temporaire. Rien ne doit y rester plus de quelques jours. Le routage suit les regles du `CLAUDE.md` racine de l'utilisateur.

## Avant de commencer
1. Lis `About-Me/about-me.md` (et `my-company.md` si present).
2. Relis l'arbre de routage du `CLAUDE.md` racine : c'est la regle de verite (chaque type de livrable a son domaine).
3. Liste les dossiers de travail : `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/` et leurs sous-dossiers. Chacun a une note du meme nom que le dossier : c'est elle qui dit ce qui va dedans.
4. Scanne `Inbox/` (ignore `Inbox.md`).

## Processus

### Etape 1 : Scanner l'inbox
```
J'ai trouve [X] items dans votre inbox :
1. [Fichier] : [apercu]
...
On les traite un par un ?
```

### Etape 2 : Pour chaque item, proposer une action
```
Item : [nom]
Contenu : [resume 1-2 phrases]
Type detecte : [Idee / Tache / Reference / Transcript / Livrable / Source wiki / Autre]

Actions possibles :
1. Router vers un dossier de travail (`livrables/`, `sources/` ou `ressources/`)
2. Verser dans la note du dossier concerne (bloc ETAT)
3. Classer en contexte transverse (Contexte/) ou template (Ressources/templates/)
4. Ingerer dans le wiki (Veille/sources/ puis /notes-permanentes)
5. Archiver
6. Supprimer (pas utile)
7. Developper maintenant (on creuse ensemble)

Que voulez-vous faire ?
```

### Etape 3 : Executer
Applique l'arbre de routage du `CLAUDE.md` racine (premier match gagne) : chaque livrable part vers le sous-dossier `livrables/` du bon dossier de travail, en respectant la convention de nommage de l'utilisateur. En cas d'egalite, le support final (ou ca va etre publie/utilise) l'emporte sur le sujet.

Selon le type :
- Idee / fait lie a un dossier -> verser dans le bloc ETAT de sa note, supprimer l'item.
- Transcript de call -> deplacer vers `Meeting/Clients/<Nom>/` si la personne a un dossier, sinon `Meeting/Prospects/YYYY-MM/` (regle complete dans `Meeting/Meeting.md`). Autre source brute -> le `sources/` du dossier concerne.
- Source de connaissance (article, concept) -> deplacer vers `Veille/sources/` et proposer `/notes-permanentes`.
- Reference transverse -> `Contexte/` ou `Ressources/templates/`.
- Obsolete -> deplacer vers `Archives/`. Sans valeur -> supprimer (confirmer avant).
- Vague mais a potentiel -> proposer de developper (mode thinking-partner) puis classer.

Respecte le `CLAUDE.md` racine : ne jamais creer de fichier dans les dossiers en lecture seule (ex : `About-Me/`, `Contexte/`, `.claude/`) sauf demande explicite. Demander confirmation avant toute suppression.

### Etape 4 : Recapitulatif
```
Inbox traite.
- [X] vers des dossiers de travail
- [X] verses en contexte
- [X] vers le wiki Veille
- [X] archives / supprimes
Items restants : [X]
```

## Conseils
- Traite l'inbox regulierement.
- En cas de doute sur le routage, applique le CLAUDE.md racine ; si toujours ambigu, demande a l'utilisateur.
- Mieux vaut router vite que laisser trainer.
- Francais, vouvoiement, pas d'em-dash ni en-dash.
