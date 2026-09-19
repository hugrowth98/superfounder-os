---
type: departement
status: active
maj: AAAA-MM-JJ
---

# Veille

## Mission

Tout ce qui vient de l'extérieur et qu'on garde. La mémoire longue du workspace, sur le pattern du LLM wiki : les sources brutes sont immuables, le wiki est écrit et maintenu par Claude, vous le lisez et vous guidez.

- `sources/` : le brut, jamais modifié. Articles clippés, transcripts de vidéos, newsletters, PDF convertis.
- `wiki/` : la connaissance distillée. Une page par entité : `concepts/` (une idée, une méthode), `patterns/` (une régularité observée), `people/` (une personne suivie), `companies/` (une entreprise, un outil, un concurrent).
- `INDEX.md` : le catalogue, une ligne par page. Lu en premier pour toute question de connaissance.
- `LOG.md` : le journal chronologique du wiki, en append.

Ne va pas ici : votre production (posts, livrables), une note sur un client (sa note de dossier), les transcripts de vos propres calls (`07_Meeting/`).

## Cadre

**Format d'une page du wiki**

```markdown
---
type: concept | pattern | person | company
sources: [liste des fichiers de sources/ utilisés]
---
# Titre

- `sources/` le brut, immuable
- `wiki/concepts/` `wiki/patterns/` `wiki/people/` `wiki/companies/` les pages
- `INDEX.md` le catalogue
- `LOG.md` le journal des ingestions

## Où on en est

- [ ] Ingérer une première source

## Key Notes

- [[Autre page]] : renforce / nuance / contredit / complète / applique
