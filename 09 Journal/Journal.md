---
type: departement
status: active
maj: AAAA-MM-JJ
---

# Journal

## Mission

La mémoire chronologique du workspace. Un fichier par jour, écrit par `/done` à la fin de chaque session : ce qui a été accompli, décidé, appris, et ce qui reste à faire. Un fichier par semaine, écrit par `/weekly-review` : le bilan et le plan.

C'est ici qu'on répond à la question "pourquoi on avait décidé ça déjà ?". L'état présent d'un dossier vit dans sa note, l'historique vit ici.

Ne va pas ici : le détail d'un projet, un livrable, une note de réflexion.

## Cadre

`YYYY-MM-DD.md` pour un jour, `YYYY-Www.md` pour une semaine. Créés depuis `08 Ressources/templates/journal-jour.md`.

Chaque entrée de session commence par `## [HH:MM] <Dossier> | <titre>`, ce qui rend le journal lisible en une commande : `grep "^## \[" 09 Journal/*.md | tail -10`.

Vous pouvez écrire dans la note du jour, mais ce n'est pas un journal intime à tenir : c'est `/done` qui le remplit.

## Où on en est

- [ ] Lancer /done sur cette session

## Key Notes

- [[Note liée]]
