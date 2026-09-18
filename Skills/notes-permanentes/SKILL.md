---
name: notes-permanentes
description: Transformer des sources (highlights, transcripts, articles, livres) en pages de connaissance integrees au wiki Veille (concepts, patterns, people, companies), avec mise a jour de l'INDEX et du LOG.
user-invocable: true
context: main
---

# Notes Permanentes -> Wiki Veille

Tu transformes les sources de l'utilisateur en connaissance durable, integree a son wiki. Ce systeme n'utilise pas un Zettelkasten classique mais le pattern LLM Wiki (Karpathy / Charlie Hills) : tu ne crees pas un systeme parallele, tu nourris `Veille/`.

Lis d'abord la note du dossier : `Veille/Veille.md`. Elle porte le schema du wiki. C'est la regle de verite sur les conventions de pages, l'ingest, l'index et le log.

Structure du wiki :
- Sources brutes (immuables) : `Veille/sources/`
- Pages du wiki : `Veille/wiki/{concepts,patterns,people,companies}/`
- Catalogue : `Veille/INDEX.md`
- Journal chronologique : `Veille/LOG.md`

Une page de wiki = une entite ou un concept autonome, reformule dans les mots de l'utilisateur, relie aux pages existantes par des `[[wikilinks]]`.

## Avant de commencer
1. Lis `About-Me/about-me.md` pour le style et les centres d'interet.
2. Lis `Veille/Veille.md` (le schema) et `Veille/INDEX.md` (ce qui existe deja).
3. Repere les sources disponibles dans `Veille/sources/` (articles, transcripts, newsletters) et `Inbox/`.

## Etape 1 : Choisir la source
```
Session Notes Permanentes (wiki Veille)
a) Je scanne vos sources recentes (Veille/sources/, Inbox/) et je propose les meilleurs concepts a extraire
b) Vous me donnez une source precise a traiter
c) On complete / consolide des pages existantes du wiki
```

## Etape 2 : Identifier les concepts
- **Option a** : scanne les fichiers recents de `Veille/sources/`, repere les passages riches en concepts (pas les simples citations), propose 3 a 5 extractions avec pour chacune : le concept en une phrase, la source, le lien potentiel avec une page existante (via l'INDEX).
- **Option b** : lis la source, identifie tous les concepts/entites extractibles, groupe par theme.
- **Option c** : lis l'INDEX, repere les pages marquees a creer ou les pages a enrichir, cherche dans les sources de quoi les completer.

Attendre validation de l'utilisateur avant de creer ou modifier.

## Etape 3 : Ingest dans le wiki
Pour chaque element valide, suis le flux d'ingest decrit dans `Veille/Veille.md` :

1. **Cree ou mets a jour la page** dans le bon sous-dossier (`concepts/`, `patterns/`, `people/`, `companies/`). Reformule dans les mots de l'utilisateur. Frontmatter et format selon le schema du wiki ; a defaut :
```markdown
---
type: [concept|pattern|person|company]
maj: YYYY-MM-DD
sources: [liste]
---
# [Titre]

[Synthese reformulee, autonome]

## Liens
- [[Page liee]] - [renforce / nuance / contredit / complete / applique]

## References
> [citation ou passage cle]
- source : [...]
```
2. **Cross-reference** : mets a jour les pages liees (ajoute les `[[wikilinks]]` reciproques), note les contradictions avec des claims existants.
3. **Mets a jour `Veille/INDEX.md`** : ajoute la page avec sa ligne de description, dans la bonne categorie.
4. **Append au `Veille/LOG.md`** une entree datee, prefixe coherent : `## [YYYY-MM-DD] ingest | [Titre source]`.

## Etape 4 : Resume de session
```
Session terminee.
Pages creees : [X]
Pages enrichies : [X]
INDEX mis a jour : oui
LOG : entree ajoutee

Suite ?
a) Autres concepts de la meme source
b) Autre source
c) Lint du wiki (contradictions, orphelines, concepts manquants)
```

## Regles
- Ne pas dupliquer le systeme : tout va dans `Veille/wiki/`, jamais un nouveau dossier de notes.
- Respecter le schema de `Veille/Veille.md` ; en cas de doute, le relire.
- Une page = une entite ou un concept (atomicite). Reformuler, jamais copier-coller le highlight brut.
- Toujours mettre a jour INDEX et LOG (c'est ce qui rend le wiki navigable).
- Respecter le style de l'utilisateur (lire `About-Me/about-me.md` et `Contexte/Tone-and-Voice.md` s'il existe).
- Pas d'em-dash ni en-dash.
