---
type: index
status: active
date: AAAA-MM-JJ
maj: AAAA-MM-JJ
---

# Inbox

> Zone de capture. Tout ce qui arrive sans place définie atterrit ici : une idée, un vocal transcrit, un lien, un fichier déposé, un transcript pas encore trié. Un sas, pas un stockage.

## Règle

Rien ne reste ici plus de quelques jours. `/inbox-processor` route chaque item vers un projet, un département, un client, `08 Ressources/` ou `11 Archives/`, et ne supprime jamais rien sans un oui.

Un gros lot à digérer (export de conversations, dossier entier) va dans `_import/` et se traite par passes avec `/import`.

## Ne va pas ici

- Un livrable fini : il va dans le dossier qui l'a produit.
- Une source de veille identifiée : `08 Ressources/Veille/sources/`.
- Un transcript de call reconnu : `07 Meeting/`.
