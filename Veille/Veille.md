---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Veille

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

Tout ce qui vient de l'extérieur et qu'on garde. La mémoire longue du workspace, sur le pattern du LLM wiki : les sources brutes sont immuables, le wiki est écrit et maintenu par Claude, vous le lisez et vous guidez.

- `sources/` : le brut, jamais modifié. Articles clippés, transcripts de vidéos, newsletters, PDF convertis.
- `wiki/` : la connaissance distillée. Une page par entité : `concepts/` (une idée, une méthode), `patterns/` (une régularité observée), `people/` (une personne suivie), `companies/` (une entreprise, un outil, un concurrent).
- `INDEX.md` : le catalogue, une ligne par page. Lu en premier pour toute question de connaissance.
- `LOG.md` : le journal chronologique du wiki, en append.

Ne va pas ici : votre production (posts, livrables), une note sur un client (sa note de dossier), les transcripts de vos propres calls (`Meeting/`).

## Conventions

**Format d'une page du wiki**

```markdown
---
type: concept | pattern | person | company
maj: YYYY-MM-DD
sources: [liste des fichiers de sources/ utilisés]
---
# Titre

[Synthèse autonome, reformulée dans vos mots, 10 à 30 lignes]

## Liens
- [[Autre page]] : renforce / nuance / contredit / complète / applique

## Références
> citation ou passage clé, avec la source
```

**Opérations.** Ingérer (`/notes-permanentes`) : lire une source, extraire les concepts, créer ou mettre à jour les pages, relier aux pages existantes, mettre à jour `INDEX.md`, ajouter une ligne à `LOG.md`. Une source touche souvent 3 à 10 pages. Interroger : lire `INDEX.md` d'abord, ouvrir les pages pertinentes, répondre avec les sources. Une bonne réponse peut être filée dans le wiki comme nouvelle page. Nettoyer (`/lint`) : contradictions, affirmations dépassées, pages orphelines.

**Règles.** `sources/` ne se modifie jamais. Une page = une entité ou un concept, pas de pages fourre-tout. Toute page nouvelle entre dans `INDEX.md` le jour même. Format du LOG : `## [YYYY-MM-DD] ingest | Titre de la source`.

## Organisation

- `sources/` le brut, immuable
- `wiki/concepts/` `wiki/patterns/` `wiki/people/` `wiki/companies/` les pages
- `INDEX.md` le catalogue
- `LOG.md` le journal des ingestions

## Roadmap

- [ ]

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)

## Décisions actées
-

## Prochaines étapes
- [ ] Ingérer une première source
<!-- ETAT:END -->

## Reprise

[Où on s'est arrêté, ce qui bloque, la première action de la prochaine session. Réécrit par /done.]

## Historique

[Une ligne par session, la plus récente en haut, avec le lien vers le journal. Écrit par /done.]

## Liens

-
