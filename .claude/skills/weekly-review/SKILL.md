---
name: weekly-review
description: Bilan de la semaine ecoulee, carry-forward des taches non completees, planification de la semaine suivante jour par jour. Ecrit une weekly note dans Intelligence/Daily logs.
user-invocable: true
context: main
---

# Weekly Review

Bilan de la semaine, report des taches non completees, et planification de la semaine suivante repartie par jour. Vue jour par jour, simple a tenir.

Structure du second cerveau :
- Identite : `ABOUT.ME/about-me.md` (+ `ABOUT.ME/my-company.md` si activite pro)
- Daily logs et weekly notes : `Intelligence/Daily logs/`
- Domaines : `Projects/<Domaine>/`

## Process

### Etape 1 : Lire le contexte
Lis `ABOUT.ME/about-me.md` (et `my-company.md` si present). Lis les daily notes de la semaine (`Intelligence/Daily logs/`) pour le contexte des sessions recentes.

### Etape 2 : Determiner la semaine
```bash
CURRENT_WEEK=$(date +%Y-W%V)
PREV_WEEK=$(date -v-7d +%Y-W%V 2>/dev/null || date -d "7 days ago" +%Y-W%V)
echo "Semaine: $CURRENT_WEEK | Precedente: $PREV_WEEK"
```

### Etape 3 : Carry-forward
Lis la weekly note precedente (`Intelligence/Daily logs/$PREV_WEEK.md`). Extrais toutes les lignes `- [ ]` (taches non completees) pour les reinjecter. Si la note n'existe pas, passe cette etape.

### Etape 4 : Scanner l'activite de la semaine
```bash
find Projects Inbox Intelligence -type f -name "*.md" -mtime -7 2>/dev/null | grep -v ".git" | head -50
```
Presente un resume rapide de ce qui a bouge cette semaine, par domaine.

### Etape 5 : Brain dump
> Comment s'est passee votre semaine ? Qu'est-ce qui a avance, qu'est-ce qui a bloque, qu'est-ce qui a emerge ?

Attendre la reponse libre (dictee vocale possible). Extraire avancees, blocages, emergences.

### Etape 6 : Plan de la semaine suivante par jour
> Quelles sont vos intentions transverses pour la semaine ? Et qu'est-ce que vous voulez faire chaque jour (Lundi a Dimanche) ?

Recuperer les intentions generales et les actions par jour. Integrer les taches carry-forward dans les bonnes journees, en consultant l'utilisateur si besoin.

### Etape 7 : Generer la weekly note
Cree `Intelligence/Daily logs/YYYY-WXX.md` :

```markdown
---
type: weekly
week: YYYY-WXX
---
# YYYY-WXX (DD-DD mois)

## Transverse / Intentions
- [Intention]

## Lundi
- [ ] Tache

## Mardi
- [ ] Tache

## Mercredi
- [ ] Tache

## Jeudi
- [ ] Tache

## Vendredi
- [ ] Tache

## Samedi
- [ ] Tache

## Dimanche
- [ ] Tache
```

### Etape 8 : Confirmation
Resume : nombre de taches carry-forward, intentions transverses retenues, repartition par jour, priorites.

## Output Style
- Francais, vouvoiement
- Concis, interactif
- Pas d'emojis, pas d'em-dash ni en-dash
