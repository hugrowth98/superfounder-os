---
name: daily-review
description: Reflexion quotidienne guidee : energie, wins, frictions, apprentissage, focus du lendemain. Ecrit dans le Daily log.
user-invocable: true
context: main
---

# Daily Review

Tu guides l'utilisateur dans sa reflexion quotidienne, puis tu ecris le resultat dans son Daily log.

Structure du second cerveau :
- Identite : `ABOUT.ME/about-me.md`
- Daily log du jour : `Intelligence/Daily logs/YYYY-MM-DD.md`
- Template : `ressources-templates/obsidian/daily.md` (s'il existe)

## Avant de commencer

1. Lis `ABOUT.ME/about-me.md` pour le contexte sur l'utilisateur.
2. Recupere la date : `date +%Y-%m-%d`.
3. Lis la daily note du jour si elle existe deja (logs de session anterieurs, focus pose le matin).
4. Jette un oeil a `Inbox/` : y a-t-il des captures non traitees a mentionner ?

## Le processus

Ouvre par :
```
Daily Review : [date]
Quelques questions pour votre reflexion du jour.
```

Pose ces questions une par une, en laissant l'utilisateur repondre (il peut dicter a la voix) :

1. **Energie** : "Comment vous sentez-vous aujourd'hui ? (1-10)"
2. **Wins** : "Qu'est-ce qui s'est bien passe ?"
3. **Friction** : "Qu'est-ce qui a ete difficile ou frustrant ?"
4. **Apprentissage** : "Qu'est-ce que vous avez appris ou realise ?"
5. **Demain** : "Quelle est LA chose importante pour demain ?"

Cloture par un resume :
```
Energie : [X]/10
Win principal : [Win]
Friction principale : [Friction]
Insight : [Apprentissage]
Focus demain : [Priorite]

Je l'ecris dans votre Daily log ?
```

## Ecriture dans le Daily log

Cible : `Intelligence/Daily logs/YYYY-MM-DD.md`.
- Si elle existe : append la section Daily Review a la fin, sans toucher au reste (logs `/done`, Focus du jour, etc.).
- Si elle n'existe pas : cree-la depuis le template de daily note s'il existe, puis ajoute la section.

Reporte aussi les elements dans les bonnes sections du template quand c'est naturel (Wins -> Fait, insight -> Pense, etc.).

Section Daily Review a ajouter :
```markdown
---

## Daily Review : HH:MM

**Energie :** [X]/10

### Ce qui s'est bien passe
- [Win]

### Ce qui a ete difficile
- [Friction]

### Ce que j'ai appris
[Insight]

### Focus demain
[Priorite]
```

## Connexions
Si l'utilisateur mentionne un domaine ou un projet, propose de logger l'info dans le contexte concerne :
```
Vous avez mentionne [Domaine]. Je le note dans le contexte du domaine (bloc ETAT du Projects/[Domaine]/CLAUDE.md) ?
```

## Output Style
- Francais, vouvoiement
- Concis, interactif, pas de blabla
- Pas d'em-dash ni en-dash
