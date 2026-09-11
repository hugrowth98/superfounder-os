---
name: done
description: Fin de session : extraction des decisions/faits, mise a jour du CLAUDE.md de chaque domaine touche (bloc ETAT, snapshot court), append du detail dans _journal.md, et si pertinent un artefact dans ressources/. A lancer a la fin de chaque session de travail.
user-invocable: true
context: main
---

# Fin de Session (/done)

Cloture la session et fait ruisseler ce qui compte. C'est la commande qui garde le contexte vivant.

Deux niveaux de memoire par domaine :
- **Snapshot (court, auto-charge)** : le `CLAUDE.md` du dossier du domaine. Claude Code le charge automatiquement quand on bosse dans ce dossier. Il doit rester court. /done ne touche QUE son bloc ETAT.
- **Detail (chronologique, a la demande)** : le `_journal.md` du dossier. L'historique complet. Lu seulement quand on en a besoin.

Plus, occasionnellement : un artefact reutilisable dans `ressources/`.

Structure du second cerveau :
- Identite : `ABOUT.ME/about-me.md` (+ `ABOUT.ME/my-company.md` si activite pro)
- Domaines : `Projects/<Domaine>/` (un dossier par domaine de votre activite : clients, contenu, acquisition, projets...)
- Snapshot domaine : `Projects/<Domaine>/CLAUDE.md` (bloc ETAT delimite)
- Detail domaine : `Projects/<Domaine>/_journal.md`
- Connaissance durable : `Intelligence/wiki/` (voir `Intelligence/CLAUDE.md` si present)
- Daily log perso (optionnel) : `Intelligence/Daily logs/YYYY-MM-DD.md`

## Le bloc ETAT (delimiteurs)

Dans le `CLAUDE.md` d'un domaine, la zone maintenue par /done est balisee :

```
<!-- ETAT:START (gere par /done, ne pas editer a la main) -->
## Etat actuel
maj : YYYY-MM-DD
- ...
## Priorites / en cours
- ...
## Decisions actees
- ...
## Prochaines etapes
- [ ] ...
<!-- ETAT:END -->
```

/done **remplace uniquement** ce qui est entre `ETAT:START` et `ETAT:END`. Tout ce qui est au-dessus (Role, conventions, regles ecrites a la main) est intouchable.

## Anti-doublon : quoi va ou
- `CLAUDE.md` (bloc ETAT) = l'etat actuel, court, reecrit (pas append).
- `_journal.md` = le detail chronologique, en append.
- `ressources/` = un artefact reutilisable durable (rare).
- Daily log = une ligne perso transverse (optionnel).

## Process

### Etape 1 : Extraction
Relis la session et extrais : **decisions** (choix actes), **faits** (infos nouvelles), **preferences** (feedback sur le comportement de l'IA), **contradictions** (avec ce qui est ecrit), **ressources** (liens/outils/concepts durables). Note aussi : fichiers crees/modifies, todos completes, prochaines etapes.

### Etape 2 : Detecter le(s) domaine(s)
Identifie le ou les domaines `Projects/<Domaine>/` touches par la session (fichiers modifies, mentions @, sujet), via l'arbre de routage du `CLAUDE.md` racine. Une session peut toucher plusieurs domaines : traite chacun.

Date du jour : `date +%Y-%m-%d`.

### Etape 3 : Snapshot dans le CLAUDE.md du domaine
Pour chaque domaine touche :

- **Si `Projects/<Domaine>/CLAUDE.md` n'existe pas** (NIVEAU CREATION, avec validation) :
  1. Scanne le dossier (`output/`, `ressources/`, et un eventuel `_contexte.md`) pour comprendre le role et l'etat.
  2. Propose un CLAUDE.md initial : un `## Role` (et `## Conventions` si applicable) en fixe, puis un bloc ETAT (delimite) avec Etat actuel / Priorites / Decisions / Prochaines etapes.
  3. Montre-le, demande validation, puis cree-le.

- **Si le CLAUDE.md existe** (direct) :
  1. Lis-le. Repere le bloc entre `ETAT:START` et `ETAT:END`.
  2. **Reecris** ce bloc (curation) : integre les decisions/faits/contradictions de la session, garde court (~1 ecran), mets a jour `maj:`, coche les prochaines etapes faites. Une contradiction : l'info de la session gagne.
  3. Ne touche jamais a ce qui est hors du bloc ETAT. Si le bloc n'existe pas encore dans un CLAUDE.md present, propose de l'ajouter (validation).

### Etape 4 : Detail dans _journal.md (append)
Pour chaque domaine touche, ajoute une entree datee dans `Projects/<Domaine>/_journal.md` (cree-le s'il manque, avec un titre `# Journal - <Domaine>`). Format, plus recent en haut :

```markdown
## YYYY-MM-DD HH:MM
- Accompli : ...
- Decisions : ...
- Faits : ...
- Fichiers : `...`
- Next : ...
```

C'est ici que va le detail. Append, jamais de reecriture.

### Etape 5 : Artefact ressources (si pertinent, validation)
Seulement si un **artefact reutilisable durable** a emerge (une methode, une checklist, une fiche de reference) qui ne tient ni dans le snapshot ni dans le journal : propose un fichier dans `Projects/<Domaine>/ressources/`. Montre, valide, cree. Sinon, ne rien creer. Par defaut on ne cree pas de fichier ressources.

### Etape 6 : Contexte personnel et connaissance (validation)
- Preference ou info perso importante : propose une mise a jour de `ABOUT.ME/about-me.md` (ou `my-company.md`, ou un fichier de `Contexte/`). Diff, validation.
- Ressource / concept durable : propose `/notes-permanentes` vers `Intelligence/wiki/`.

### Etape 7 : Daily log (optionnel)
Si l'utilisateur tient un Daily log perso, ajoute une ligne transverse dans `Intelligence/Daily logs/YYYY-MM-DD.md` : 1 a 2 lignes sur la journee, pas le detail metier (qui est dans les `_journal.md`).

### Etape 8 : Confirmation
```
Session loggee.
Domaines : [liste]
CLAUDE.md : [cree (X) / bloc ETAT mis a jour (Y)]
_journal.md : [entrees ajoutees]
Ressources : [fichier propose/cree / rien]
Perso / wiki : [propose / rien]

Extractions : X decisions, X faits, X preferences, X contradictions, X ressources
```

## Niveaux de validation
- Append `_journal.md` : direct.
- Reecrire le bloc ETAT d'un CLAUDE.md existant : direct.
- Creer un CLAUDE.md (1ere fois) : validation.
- Creer un fichier dans `ressources/` : validation.
- ABOUT.ME / wiki : validation.

## Regles
- Curation, pas accumulation : le bloc ETAT est reecrit court ; l'historique va dans `_journal.md`.
- Ne jamais editer hors du bloc ETAT dans un CLAUDE.md (regles ecrites a la main intouchables).
- Par defaut /done met a jour, il ne cree que sur validation (CLAUDE.md, ressources).
- Session tres courte (juste une question) : log minimal, aucun fichier cree.
- Francais, vouvoiement, pas d'em-dash ni en-dash.
