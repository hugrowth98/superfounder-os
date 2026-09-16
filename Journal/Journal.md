---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Journal

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

La mémoire chronologique du workspace. Un fichier par jour, écrit par `/done` à la fin de chaque session : ce qui a été accompli, décidé, appris, et ce qui reste à faire. Un fichier par semaine, écrit par `/weekly-review` : le bilan et le plan.

C'est ici qu'on répond à la question "pourquoi on avait décidé ça déjà ?". L'état présent d'un dossier vit dans sa note, l'historique vit ici.

Ne va pas ici : le détail d'un projet, un livrable, une note de réflexion.

## Conventions

`YYYY-MM-DD.md` pour un jour, `YYYY-Www.md` pour une semaine. Créés depuis `Ressources/templates/journal-jour.md`.

Chaque entrée de session commence par `## [HH:MM] <Dossier> | <titre>`, ce qui rend le journal lisible en une commande : `grep "^## \[" Journal/*.md | tail -10`.

Vous pouvez écrire dans la note du jour, mais ce n'est pas un journal intime à tenir : c'est `/done` qui le remplit.

## Organisation

[Un fichier par jour, un par semaine.]

## Roadmap

- [ ]

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)

## Décisions actées
-

## Prochaines étapes
- [ ] Lancer /done sur cette session
<!-- ETAT:END -->

## Reprise

[Où on s'est arrêté, ce qui bloque, la première action de la prochaine session. Réécrit par /done.]

## Historique

[Une ligne par session, la plus récente en haut, avec le lien vers le journal. Écrit par /done.]

## Liens

-
