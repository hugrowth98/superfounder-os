---
name: inbox-processor
description: Trier les items de Inbox/ et les router vers le bon domaine Projects, Contexte, le wiki Intelligence ou l'archive, en suivant les regles de routage du CLAUDE.md racine.
user-invocable: true
context: main
---

# Inbox Processor

Tu aides l'utilisateur a vider son `Inbox/` en routant chaque item au bon endroit.

## Contexte
`Inbox/` (a la racine du workspace) est un point de capture temporaire. Rien ne doit y rester plus de quelques jours. Le routage suit les regles du `CLAUDE.md` racine de l'utilisateur.

## Avant de commencer
1. Lis `ABOUT.ME/about-me.md` (et `my-company.md` si present).
2. Relis l'arbre de routage du `CLAUDE.md` racine : c'est la regle de verite (chaque type de livrable a son domaine).
3. Liste les domaines actifs : `Projects/*/` (et les sous-dossiers s'il y en a).
4. Scanne `Inbox/` (ignore `CLAUDE.md`).

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
1. Router vers un domaine Projects/ (output ou ressources)
2. Verser dans le contexte du domaine (bloc ETAT du Projects/<Domaine>/CLAUDE.md)
3. Classer en contexte transverse (Contexte/) ou template (ressources-templates/)
4. Ingerer dans le wiki (Intelligence/raw/ puis /notes-permanentes)
5. Archiver
6. Supprimer (pas utile)
7. Developper maintenant (on creuse ensemble)

Que voulez-vous faire ?
```

### Etape 3 : Executer
Applique l'arbre de routage du `CLAUDE.md` racine (premier match gagne) : chaque livrable part vers le dossier `output/` du bon domaine, en respectant la convention de nommage de l'utilisateur. En cas d'egalite, le support final (ou ca va etre publie/utilise) l'emporte sur le sujet.

Selon le type :
- Idee / fait lie a un domaine -> verser dans le bloc ETAT du `Projects/<Domaine>/CLAUDE.md`, supprimer l'item.
- Transcript a exploiter -> deplacer vers l'`input/` du projet concerne (ou un dossier d'archive de transcripts).
- Source de connaissance (article, concept) -> deplacer vers `Intelligence/raw/` et proposer `/notes-permanentes`.
- Reference transverse -> `Contexte/` ou `ressources-templates/`.
- Obsolete -> archiver. Sans valeur -> supprimer (confirmer avant).
- Vague mais a potentiel -> proposer de developper (mode thinking-partner) puis classer.

Respecte le `CLAUDE.md` racine : ne jamais creer de fichier dans les dossiers en lecture seule (ex : `ABOUT.ME/`, `Contexte/`, `.claude/`) sauf demande explicite. Demander confirmation avant toute suppression.

### Etape 4 : Recapitulatif
```
Inbox traite.
- [X] vers domaines Projects
- [X] verses en contexte
- [X] vers le wiki Intelligence
- [X] archives / supprimes
Items restants : [X]
```

## Conseils
- Traite l'inbox regulierement.
- En cas de doute sur le routage, applique le CLAUDE.md racine ; si toujours ambigu, demande a l'utilisateur.
- Mieux vaut router vite que laisser trainer.
- Francais, vouvoiement, pas d'em-dash ni en-dash.
