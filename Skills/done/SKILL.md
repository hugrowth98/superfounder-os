---
name: done
description: "Fin de session : extraction des décisions, faits, préférences, contradictions et ressources, puis ruissellement vers le journal du jour, la note du dossier touché (bloc ETAT, Reprise, Historique) et son _log.md. À lancer à la fin de chaque session de travail."
user-invocable: true
context: main
---

# Fin de session (/done)

Tu clôtures la session et tu fais ruisseler ce qui compte vers les bons fichiers. Trente secondes. Curation, pas accumulation : l'état est réécrit court, l'historique va dans le journal.

## Les trois niveaux de mémoire

| Niveau | Fichier | Nature | Lu quand |
|---|---|---|---|
| 1. Chronologique | `Journal/YYYY-MM-DD.md` | ce qui s'est passé aujourd'hui, tous dossiers confondus | à la demande, et par `/weekly-review` |
| 2. État du dossier | la note du dossier (`Vente/Vente.md`) | où on en est maintenant, court | avant tout travail dans le dossier |
| 3. Détail du dossier | `_log.md` du dossier | une ligne par session, avec le lien vers le journal | à la demande |

Plus, sur validation : `About-Me/` et `Contexte/` pour ce qui est durable.

## Étape 1 : extraction

Relis la session et sors, en une ligne chacun :

1. **Décisions** : un choix acté. "L'offre coaching passe à 1500 euros."
2. **Faits** : une info nouvelle et vérifiable. "Le client a 4 commerciaux."
3. **Préférences** : un feedback sur ton comportement. "Plus court, pas de formule de politesse."
4. **Contradictions** : la session contredit un fichier. Le fichier dit 1200, la session dit 1500.
5. **Ressources** : lien, outil, concept cité qui mérite de durer.

Note aussi : les fichiers créés ou modifiés, les todos complétés, les prochaines étapes identifiées.

Si la session a été très courte (une question, aucune décision, aucun fichier), fais un log minimal dans le journal et arrête-toi là.

## Étape 2 : détecter les dossiers touchés

Pour chaque fichier créé ou modifié, remonte au dossier parent le plus proche qui contient une note de dossier (un `.md` du même nom que le dossier). C'est cette note qu'on met à jour.

Ajoute les dossiers cités dans la conversation même sans fichier modifié, si une décision les concerne. Une session peut toucher plusieurs dossiers : traite chacun.

Un fichier dans une initiative datée (`Marketing/Event/Lancement-2026-10/...`) remonte à la note de l'initiative, pas à celle du domaine. Un fichier dans `Produit-Client/<Client>/` remonte à la note du client.

Si le dossier touché n'a pas de note : propose de la créer depuis `Ressources/templates/note-de-dossier.md`, montre-la, attends le "oui".

Date du jour : `date +%Y-%m-%d`. Heure : `date +%H:%M`.

## Étape 3 : le journal du jour (obligatoire, direct)

Ouvre ou crée `Journal/YYYY-MM-DD.md` (depuis `Ressources/templates/journal-jour.md`). Ajoute à la fin :

```markdown
## [HH:MM] <Dossier(s) touché(s)> | <titre de la session en six mots>

**Accompli**
-

**Extractions**
- Décisions :
- Faits :
- Préférences :
- Contradictions : <fichier> disait X, la session dit Y, corrigé
- Ressources :

**Fichiers**
- `chemin/fichier.md`

**Prochaines étapes**
- [ ]
```

Omets les lignes vides. Le titre commence toujours par `## [HH:MM]` : c'est ce qui rend le journal lisible par `grep "^## \["`.

## Étape 4 : la note du dossier (direct, sans validation)

Pour chaque dossier touché, lis sa note puis :

1. **Bloc ETAT** (entre `ETAT:START` et `ETAT:END`) : réécris-le. Intègre les décisions, les faits, les contradictions résolues. Mets `maj :` à aujourd'hui. Coche les prochaines étapes faites, ajoute les nouvelles. Garde-le sous quinze lignes.
2. **Reprise** : réécris trois lignes maximum. Où on s'est arrêté, ce qui bloque, la première action de la prochaine session.
3. **Roadmap** : coche ce qui a été fait.
4. **Historique** : ajoute une ligne en haut, `- YYYY-MM-DD : <titre de la session> -> [[Journal/YYYY-MM-DD]]`. Garde dix lignes.
5. **Liens** : ajoute les wikilinks vers les entités citées si elles manquent.
6. **Frontmatter** : `maj:` à aujourd'hui.

Une contradiction se résout en faveur de la session : l'information la plus récente gagne. Signale-le dans le journal.

Tu ne touches jamais aux sections Rôle, Conventions et Organisation. Elles appartiennent à l'utilisateur.

Une note client (`Produit-Client/<Nom>/<Nom>.md`) suit les mêmes règles ; en plus, un fait sur l'interlocuteur, le prix ou la façon de travailler du client va dans sa section dédiée.

## Étape 5 : le _log.md du dossier (direct)

Ajoute en haut de `_log.md` (crée-le avec un titre `# Log - <Nom>` s'il manque) :

```
- YYYY-MM-DD HH:MM : <titre de la session> -> [[Journal/YYYY-MM-DD]]
```

Une ligne, rien d'autre. Le contenu est dans le journal.

## Étape 6 : cocher les todos ailleurs

Si des tâches complétées pendant la session sont cochables dans la weekly note en cours (`Journal/YYYY-Www.md`), coche-les. Ne cherche pas ailleurs : les todos vivent dans les notes de dossier et la weekly, nulle part d'autre.

## Étape 7 : contexte durable (validation obligatoire)

Si une extraction touche une zone protégée, ne l'écris pas. Propose :

| Ce qui a émergé | Fichier cible |
|---|---|
| Préférence sur ton comportement, info perso | `About-Me/about-me.md` |
| Changement d'offre, de prix, d'objectif | `About-Me/my-company.md` puis `Contexte/Offer-Positioning.md` |
| Nouveau verbatim client, évolution de l'ICP | `Contexte/Clients-Problems-and-Messages.md` |
| Évolution de la voix | `Contexte/Tone-and-Voice.md` |
| Règle de marque | `Branding/` |

Montre le diff et attends le "oui" :

```
Je propose de mettre à jour <fichier> :
- Ajouter : ...
- Modifier : <ancien> -> <nouveau>
OK ?
```

Si rien ne le mérite, ne propose rien.

## Étape 8 : ressource durable (validation)

Si une ressource extraite mérite une page de connaissance (un concept, une méthode, une personne), propose `/notes-permanentes` vers `Veille/wiki/`. Sinon, dépose le lien brut dans `Veille/sources/`.

## Étape 9 : confirmation

```
Session loggée.

Journal : Journal/YYYY-MM-DD.md
Notes de dossier : <Nom>.md (ETAT, Reprise, Historique), <Nom>.md
_log : <dossiers>
Contexte durable : <proposé / rien>

Extractions : X décisions, X faits, X préférences, X contradictions, X ressources
```

## Niveaux de validation

| Action | Mode |
|---|---|
| Journal, bloc ETAT, Reprise, Historique, Roadmap, `_log.md` | direct |
| Créer une note de dossier manquante | validation |
| `About-Me/`, `Contexte/`, `Branding/` | diff puis validation |
| Envoi vers l'extérieur (mail, CRM, campagne) | jamais |

## Règles

- Concis : une ligne par extraction, pas de paragraphe.
- Wikilinks dès qu'un fichier, un client ou une entité est cité.
- Français, vouvoiement, aucun tiret cadratin ni demi-cadratin.
- Tu ne supprimes jamais un fichier.
- Tu ne réécris jamais une section écrite à la main.
- Si un fichier touché n'a pas de frontmatter, ajoute-le (`type`, `status`, `date`, `maj`) au lieu de le signaler.
