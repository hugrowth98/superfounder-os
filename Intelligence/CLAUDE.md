# Intelligence

> Chargé automatiquement par Claude Code quand on travaille dans ce dossier. C'est le schéma du wiki : il dit comment la connaissance durable est structurée et comment on l'alimente.

## Rôle
La mémoire longue du workspace. Ce qui a été lu, appris, compris, et qui doit rester disponible dans six mois. Le pattern est celui du "LLM wiki" : les sources brutes sont immuables, le wiki est écrit et maintenu par Claude, vous le lisez et vous guidez.

## Structure

```
Intelligence/
├── Daily logs/        une note par jour (YYYY-MM-DD.md) et une par semaine (YYYY-WXX.md), écrites par daily-review, weekly-review et /done
├── raw/               sources brutes, jamais modifiées : articles, transcripts, PDF convertis, newsletters
├── wiki/
│   ├── concepts/      une idée, une méthode, un framework
│   ├── patterns/      une régularité observée (ce qui marche, ce qui échoue)
│   ├── people/        une personne (créateur suivi, expert, client clé)
│   └── companies/     une entreprise (concurrent, outil, client)
├── INDEX.md           le catalogue : chaque page, un lien, une ligne de résumé. Lu en premier pour toute question.
└── LOG.md             le journal chronologique, en append : ingestions, requêtes, nettoyages
```

## Format d'une page du wiki

```markdown
---
type: concept | pattern | person | company
maj: YYYY-MM-DD
sources: [liste des fichiers raw/ utilisés]
---
# Titre

[Synthèse autonome, reformulée dans vos mots, 10 à 30 lignes]

## Liens
- [[Autre page]] : renforce / nuance / contredit / complète / applique

## Références
> citation ou passage clé, avec la source
```

## Opérations

- **Ingérer** (`/notes-permanentes`) : lire une source de `raw/`, extraire les concepts, créer ou mettre à jour les pages, relier aux pages existantes, mettre à jour `INDEX.md`, ajouter une ligne à `LOG.md`. Une source touche souvent 3 à 10 pages.
- **Interroger** : lire `INDEX.md` d'abord, ouvrir les pages pertinentes, répondre avec les sources. Une bonne réponse peut être filée dans le wiki comme nouvelle page.
- **Nettoyer** (à la demande) : contradictions entre pages, affirmations dépassées par une source plus récente, pages orphelines sans lien entrant, concepts cités sans page.

## Règles
- `raw/` ne se modifie jamais. Le wiki se réécrit.
- Une page = une entité ou un concept. Pas de pages fourre-tout.
- Toute page nouvelle entre dans `INDEX.md` le jour même.
- Format du LOG : `## [YYYY-MM-DD] ingest | Titre de la source`, une entrée par opération.
