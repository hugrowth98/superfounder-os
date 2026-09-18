---
name: import
description: Import intelligent par passes intentionnelles : alignement, scan, delegation a des sous-agents, plan puis execution. Route les notes/exports/PDF vers les dossiers de travail, Contexte ou le wiki Veille. 4 verdicts (KEEP/EXTRACT/SUMMARIZE/ARCHIVE).
user-invocable: true
context: main
---

# Import Intelligent

Importe un lot de contenu (notes, exports ChatGPT/Claude, PDF, docs) dans le second cerveau, par petites passes thematiques.

Structure du second cerveau :
- Zone d'import : `Inbox/_import/` (sous-dossier dedie de l'inbox pour cette commande)
- Destinations : les dossiers de travail (`Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/`), `Contexte/`, `Ressources/`, `Veille/sources/` (puis wiki), `Archives/`
- Identite : `About-Me/about-me.md` (+ `my-company.md` si present)
- Routage : arbre de decision du `CLAUDE.md` racine

## Principe : passes intentionnelles
```
On importe par petites passes thematiques, pas tout d'un coup.
Une passe = une source ou un theme, ~100 items max.
On vide Inbox/_import/, on met la source suivante, on relance /import.
```
Si un gros volume melange est deja dans `Inbox/_import/`, propose de decouper en plusieurs passes.

## Etape 1 : Alignement
Avant d'ouvrir un fichier, capte le contexte humain :
1. Qu'y a-t-il dans `Inbox/_import/` pour cette passe ? (etre precis)
2. Objectif : (a) ranger note par note dans les domaines, (b) extraire l'info utile vers le contexte (About-Me, le bloc ETAT de la note du dossier) et archiver le reste, (c) faire le tri (garder vs jeter), (d) un melange.
3. Quoi archiver direct (projets termines, sujets morts) ?
4. Quel domaine est central pour cette passe ?
5. Budget tokens limite ? (si oui, router les sous-agents vers un modele economique)

Reformule en 4 lignes max, fais valider. Ce resume briefe les sous-agents.

## Etape 2 : Preparation auto
- **Formats lourds** (PDF/docx/pptx/xlsx) : convertis en .md (markitdown si dispo, sinon le skill `pdf`/`docx`/`pptx`/`xlsx` selon le cas). Deplace les originaux dans `Inbox/_import/_originaux/`.
- **Exports ChatGPT/Claude** (JSON) : detecte le format, decoupe une conversation par fichier .md dans `Inbox/_import/_chats/` (titre reformule, frontmatter provider/date/nb_messages). Une conversation longue ne vaut presque jamais un KEEP integral : sa valeur est dans les idees, pas le verbatim.
Annonce le total a traiter. Au-dela de 150 items, propose de decouper.

## Etape 3 : Scan par l'agent principal
`ls -laR "Inbox/_import/" | head -200`. Echantillonne ~5 items representatifs pour saisir le style du corpus. Produis un mapping interne (types, volumes, sujets dominants, ecart avec l'intention annoncee). Decoupe en lots (notes courtes ~50/lot, conversations ~10/lot, PDF longs ~15/lot).

## Etape 4 : Table de routage du workspace
Construis ta carte des destinations :
- Identite : `About-Me/about-me.md` (+ `my-company.md`)
- Dossiers de travail : `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/` et leurs sous-dossiers ; lis la note de chacun (meme nom que le dossier) pour les mots-cles
- Contexte transverse : `Contexte/`
- Wiki : `Veille/INDEX.md` (ce qui existe deja)
Note les mots-cles par domaine : ils servent au matching.

## Etape 5 : Delegation a des sous-agents
Pour chaque lot, lance un sous-agent (en parallele). Brief : contexte du workspace (table de routage + mots-cles), intention de l'utilisateur (Etape 1), style du corpus (Etape 3). Chaque item -> objet JSON :
- `source`, `title` (reecris si peu parlant), `summary`, `created_hint`
- `verdict` :
  - `KEEP_NOTE` : garder tel quel dans un domaine / Contexte / ressources
  - `EXTRACT_CONTEXT` : extraire l'info utile vers le bloc ETAT de la note d'un dossier, `About-Me`, ou une page wiki ; archiver l'original
  - `SUMMARIZE` : regrouper avec d'autres items du meme groupe en une note de synthese
  - `ARCHIVE` : obsolete
- `verdict_reason`, `destination`, `context_patch` (si EXTRACT), `summarize_group` (si SUMMARIZE), `rename_suggestion`, `confidence`, `notes`

Regles de routage : suivre l'arbre du `CLAUDE.md` racine. Preferer rattacher a un dossier existant. Pour les sources de connaissance durable (concepts, frameworks), destination = `Veille/sources/` avec note "a passer en /notes-permanentes". Conversations ChatGPT/Claude : EXTRACT_CONTEXT ou SUMMARIZE presque toujours mieux que KEEP_NOTE.

## Etape 6 : Plan complet (aucune ecriture)
Presente le plan groupe par verdict puis destination (tableaux), avec vue d'ensemble des compteurs, alertes (doublons, candidats nouveau domaine, ecarts intention/corpus). Propose : (a) executer, (b) ajuster des verdicts, (c) voir le contenu d'items avant de decider.

## Etape 7 : Ajustements
Boucle jusqu'a validation.

## Etape 8 : Execution
Par lots de 15 :
- KEEP_NOTE : deplace (renomme si suggere) vers la destination, en respectant la convention de nommage du `CLAUDE.md` racine.
- EXTRACT_CONTEXT : applique le patch a la note cible (append sous `## Import du YYYY-MM-DD`), deplace l'original vers l'archive.
- SUMMARIZE : cree une note de synthese par groupe, archive les sources.
- ARCHIVE : deplace vers `Archives/import-YYYY-MM-DD/`.
Demander confirmation avant de creer un nouveau dossier de travail. Ne jamais ecrire dans les dossiers en lecture seule sans accord explicite.

## Etape 9 : Recap + feedback
Resume des compteurs et cout estime. Demande : ce qui a convenu, ce qui aurait pu etre mieux. Si feedback exploitable, propose un diff de ce SKILL.md (applique seulement si valide). Puis lance `/done` pour logger la session. Rappelle que `Inbox/_import/` est vide (sauf `_originaux/`) pour la prochaine passe.

## Principes
- Passes intentionnelles (~100 items max), pas tout en bloc.
- Alignement avant action.
- 4 verdicts, pas 1.
- Agent principal voit puis delegue avec brief.
- Plan puis execution, clairement separes.
- Respecter le CLAUDE.md racine (routage, nommage, dossiers en lecture seule).
- Francais, vouvoiement, pas d'em-dash ni en-dash.
