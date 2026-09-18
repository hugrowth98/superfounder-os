---
name: done
description: "Fin de session : extraction des décisions, faits, préférences, contradictions et ressources, puis ruissellement vers le journal du jour, la note du projet, du département ou du client touché (Où on en est, Cadre, Étapes, Key Notes) et son _log.md. Propose l'archivage d'un projet dont la roadmap est cochée. À lancer à la fin de chaque session de travail."
user-invocable: true
context: main
---

# Fin de session (/done)

Tu clôtures la session et tu fais ruisseler ce qui compte vers les bons fichiers. Trente secondes. Curation, pas accumulation : l'état est réécrit court, l'historique va dans le journal. Rien de ce qui a été dit ne doit exister seulement dans la conversation.

## Les trois niveaux de mémoire

| Niveau | Fichier | Nature | Lu quand |
|---|---|---|---|
| 1. Chronologique | `09 Journal/YYYY-MM-DD.md` | ce qui s'est passé aujourd'hui, tous dossiers confondus | à la demande, et par `/weekly-review` |
| 2. État du dossier | la note du projet, du département ou du client (`05 Departements/Vente/Vente.md`) | où on en est maintenant, court | à chaque session dans ce dossier |
| 3. Détail du dossier | le `_log.md` du même dossier | une ligne par session, avec le lien vers le journal | à la demande |

Plus, sur validation seulement : `01 About-Me/`, `02 Contexte/`, `03 Branding/` pour ce qui est durable.

## Étape 1 : extraction

Relis toute la session et sors, en une ligne chacun :

1. **Décisions** : un choix acté. "La page d'inscription devient une page candidature."
2. **Faits** : une info nouvelle et vérifiable. "Le client Alpha a 4 consultants."
3. **Préférences** : un feedback sur ton comportement. "Plus court, pas de formule de politesse."
4. **Contradictions** : la session contredit un fichier. Le fichier dit 800 euros, la session dit 990.
5. **Ressources** : lien, outil, concept cité qui mérite de durer.

Note aussi : les fichiers créés ou modifiés, les todos complétés, les prochaines étapes identifiées mais pas faites.

Si la session a été très courte (une question, aucune décision, aucun fichier), fais un log minimal dans le journal et arrête-toi là.

## Étape 2 : détecter les dossiers touchés

Pour chaque fichier créé ou modifié, remonte au dossier parent le plus proche qui contient une note du même nom que lui. C'est cette note qu'on met à jour. Trois familles :

- un projet : `04 Projets/<Projet>/<Projet>.md`
- un département : `05 Departements/<Departement>/<Departement>.md` (un sous-dossier qui a sa propre note, comme `Contenu/LinkedIn/LinkedIn.md`, l'emporte)
- un client : `06 Clients/<Client>/<Client>.md`

Un fichier dans un projet remonte à la note du projet, jamais à celle du département qui le porte. Ajoute les dossiers cités dans la conversation même sans fichier modifié, si une décision les concerne. Une session peut toucher plusieurs dossiers : traite chacun.

Si le dossier touché n'a pas de note : propose de la créer depuis le template qui correspond (`08 Ressources/templates/projet.md`, `departement.md` ou `client.md`), montre-la, attends le "oui".

Date du jour : `date +%Y-%m-%d`. Heure : `date +%H:%M`.

## Étape 3 : le journal du jour (obligatoire, direct)

Ouvre `09 Journal/YYYY-MM-DD.md`. S'il n'existe pas, crée-le depuis `08 Ressources/templates/journal-jour.md` en remplaçant la date. Ajoute à la fin :

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

Omets les lignes vides. Le titre commence toujours par `## [HH:MM]` : c'est ce qui rend le journal lisible avec `grep "^## \[" "09 Journal/"*.md`.

## Étape 4 : la note du dossier (direct, sans validation)

Les notes ont toutes la même forme courte. Pour chaque dossier touché, lis la note en entier puis :

1. **Où on en est** : réécris la section en entier, cinq lignes maximum. Où on en est, la prochaine action, et la dernière session sous la forme `dernière session : YYYY-MM-DD, <titre> -> [[09 Journal/YYYY-MM-DD]]`. Curation : ce qui n'est plus vrai disparaît.
2. **Cadre** : pour chaque décision actée, ajoute une puce datée en fin de section, `- YYYY-MM-DD : <décision>`. Une contradiction se résout en faveur de la session : corrige la ligne fautive dans Cadre, Mission ou Objectif, et signale-le dans le journal.
3. **Étapes** (projet, client) : coche ce qui a été fait. N'ajoute une étape que si l'utilisateur l'a décidée.
4. **Key Notes** : ajoute les wikilinks vers les projets, départements, clients et personnes cités s'ils manquent.
5. **Frontmatter** : `maj:` à aujourd'hui. Si la Objectif d'un département a changé, mets à jour `objectif:`.

Tu ne réécris jamais Mission, Périmètre, Objectif, ni le texte de Cadre au-dessus des décisions datées : ils appartiennent à l'utilisateur. Tu y corriges seulement une ligne devenue fausse.

Si toutes les Étapes d'un projet sont cochées, propose : `status: completed` dans son frontmatter et déplacement du dossier vers `11 Archives/`. Attends le "oui".

## Étape 5 : le _log.md du dossier (direct)

Ajoute en haut de `_log.md` (crée-le avec un titre `# Log - <Nom>` s'il manque) :

```
- YYYY-MM-DD HH:MM : <titre de la session> -> [[09 Journal/YYYY-MM-DD]]
```

Une ligne, rien d'autre. Le contenu est dans le journal.

## Étape 6 : cocher les todos ailleurs

Si des tâches complétées pendant la session sont cochables dans la weekly note en cours (`09 Journal/YYYY-Www.md`), coche-les. Ne cherche pas ailleurs : les todos vivent dans les Étapes, les sections Où on en est et la weekly, nulle part d'autre.

## Étape 7 : contexte durable (validation obligatoire)

Si une extraction touche une zone protégée, ne l'écris pas. Propose :

| Ce qui a émergé | Fichier cible |
|---|---|
| Préférence sur ton comportement, info perso, façon de travailler | `01 About-Me/about-me.md` |
| Changement d'offre, de prix, d'objectif, de focus | `01 About-Me/my-company.md` |
| Nouveau verbatim client, évolution de l'ICP, du positionnement, de la voix | `02 Contexte/` |
| Règle de marque | `03 Branding/` |

Montre le diff et attends le "oui" :

```
Je propose de mettre à jour <fichier> :
- Ajouter : ...
- Modifier : <ancien> -> <nouveau>
OK ?
```

Si rien ne le mérite, ne propose rien.

## Étape 8 : ressource durable (validation)

Si une ressource extraite mérite une page de connaissance (un concept, une méthode, une personne, une boîte), propose `/notes-permanentes` vers `08 Ressources/Veille/wiki/`. Sinon, dépose le lien brut dans `00 Inbox/` avec une ligne de contexte.

## Étape 9 : confirmation

```
Session loggée.

Journal : 09 Journal/YYYY-MM-DD.md
Notes : <Nom>.md (Où on en est, Cadre, Étapes), <Nom>.md
_log : <dossiers>
Contexte durable : <proposé / rien>

Extractions : X décisions, X faits, X préférences, X contradictions, X ressources
```

## Niveaux de validation

| Action | Mode |
|---|---|
| Journal, Où on en est, décision datée dans Cadre, Étapes (cocher), Key Notes, `_log.md` | direct |
| Créer une note manquante, archiver un projet terminé | validation |
| `01 About-Me/`, `02 Contexte/`, `03 Branding/` | diff puis validation |
| Envoi vers l'extérieur (mail, CRM, Notion, campagne) | jamais |

## Règles

- Concis : une ligne par extraction, pas de paragraphe.
- Wikilinks dès qu'un fichier, un client, un projet ou une personne est cité.
- Français, vouvoiement avec l'utilisateur, aucun tiret cadratin ni demi-cadratin.
- Tu ne supprimes jamais un fichier. Tu ne réécris jamais une section écrite à la main.
- Si un fichier touché n'a pas de frontmatter, ajoute-le (`type`, `status`, `date`, `maj`) au lieu de le signaler.
- Chemins avec espaces : toujours entre guillemets dans une commande.
