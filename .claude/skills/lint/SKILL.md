---
name: lint
description: "Audit de santé du workspace : notes de dossier manquantes, blocs ETAT périmés, contradictions entre fichiers, frontmatter absent, versions non archivées, fichiers à la racine, tirets cadratins, chemins morts, dossiers orphelins. Produit un rapport et un plan de correction. Lecture seule jusqu'à validation. À lancer une fois par mois."
user-invocable: true
context: main
argument-hint: [optionnel : un dossier à auditer, ex "Vente"]
---

# Lint : vérifier la santé du workspace

Un contexte écrit une fois et jamais vérifié devient faux, et une IA qui lit du faux produit du faux avec assurance. `/lint` passe le workspace au crible, produit un rapport, et propose un plan. **Lecture seule : tu ne corriges rien avant validation.**

Sans argument, tout le workspace. Avec un argument, ce dossier seulement.

## Les neuf contrôles

Lance-les dans cet ordre. Chacun est une commande, pas une impression.

### 1. Notes de dossier manquantes

Tout dossier de travail doit avoir sa note (même nom que le dossier) et son `_log.md`. Aucun dossier de travail n'a de `CLAUDE.md` : seule la racine en a un.

```bash
for d in Produit-Client/*/ Marketing/*/ Vente/*/ Vente Marketing Strategie Produit-Client Veille Meeting Journal; do
  d="${d%/}"; n=$(basename "$d")
  [ -d "$d" ] || continue
  case "$n" in livrables|sources|ressources) continue ;; esac
  [ -f "$d/$n.md" ]   || echo "NOTE MANQUANTE  $d/$n.md"
  [ -f "$d/_log.md" ] || echo "LOG MANQUANT    $d/_log.md"
  [ -f "$d/CLAUDE.md" ] && echo "CLAUDE.md PARASITE  $d/CLAUDE.md (un dossier de travail n'en a pas)"
done
```

Pour chaque manque : proposer la création depuis `Ressources/templates/note-de-dossier.md` (ou `note-de-dossier-client.md` sous `Produit-Client/`).

### 2. Blocs ETAT périmés

Un état qui n'a pas bougé depuis plus de trente jours alors que le dossier a des fichiers récents est un état mort.

```bash
for f in $(grep -rl "ETAT:START" --include="*.md" . 2>/dev/null); do
  maj=$(grep -m1 "^maj *:" "$f" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
  d=$(dirname "$f")
  recent=$(find "$d" -type f -mtime -30 -not -name "_log.md" -not -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  echo "$maj | $recent fichiers récents | $f"
done | sort
```

Signale les notes dont `maj` est vieux mais dont le dossier a bougé. C'est le symptôme d'un `/done` qui n'a pas tourné.

### 3. Contradictions

Cherche les valeurs qui doivent être uniques et se comparent mal : un prix, une date d'event, un nom d'offre, un objectif chiffré.

```bash
grep -rn --include="*.md" -E "[0-9]+ ?(euros|EUR|€)" About-Me Contexte Vente/Propositions Marketing Strategie | head -30
```

Pour chaque valeur trouvée à plusieurs endroits avec des contenus différents : nomme le fichier qui fait foi (`About-Me/my-company.md` pour l'offre et les prix, `Contexte/` pour l'ICP et le positionnement, `Branding/` pour la marque) et propose la correction des autres. En cas de doute sur la bonne valeur, demande à l'utilisateur plutôt que de trancher.

### 4. Frontmatter absent

```bash
for f in $(find Produit-Client Marketing Vente Strategie Veille -name "*.md" -not -name "_log.md" -newermt "-90 days" 2>/dev/null); do
  head -1 "$f" | grep -q '^---$' || echo "SANS FRONTMATTER  $f"
done | head -40
```

Proposer l'ajout de `type`, `status`, `date`, `maj`. Cibler les notes de dossier et les livrables récents, pas les archives.

### 5. Versions non archivées

Plusieurs versions d'un même livrable côte à côte, c'est n moins un fichiers faux.

```bash
find . -name "*.md" -not -path "./.git/*" -not -path "./.claude/*" | sed -E 's/[-_]?v[0-9]+//; s/_2[0-9]{3}-[0-9]{2}-[0-9]{2}//' \
  | sort | uniq -d | head -20
```

Pour chaque famille : identifier la version de référence (la plus récente, ou demander), lui mettre `status: final`, proposer le déplacement des autres vers `Archives/` avec leur suffixe de version.

### 6. Fichiers à la racine

```bash
ls -p | grep -v / | grep -vE "^(CLAUDE.md|README.md|CHANGELOG.md|CONTRIBUTING.md|LICENSE|install.sh)$"
```

Tout autre fichier à la racine doit être routé vers un dossier ou l'Inbox.

### 7. Tirets cadratins et demi-cadratins

```bash
grep -rln --include="*.md" -e $'\xe2\x80\x94' -e $'\xe2\x80\x93' About-Me Contexte Produit-Client Marketing Vente Strategie Journal | head -20
```

Règle à tolérance zéro. Proposer le remplacement par un tiret simple, deux-points, virgule ou parenthèses selon le contexte.

### 8. Chemins morts

Les notes et les fichiers de contexte qui pointent vers des fichiers qui n'existent plus.

```bash
grep -rhoE '`[A-Za-z0-9_./-]+\.(md|csv|json|xlsx)`' --include="*.md" About-Me Contexte Vente/contexte.md Marketing/LinkedIn/ressources \
  | tr -d '`' | sort -u | while read -r p; do [ -e "$p" ] || echo "CHEMIN MORT  $p"; done | head -30
```

### 9. Dossiers orphelins et clients inactifs

```bash
find . -type d -empty -not -path "./.git/*" | head -20
find Produit-Client -maxdepth 1 -mindepth 1 -type d -mtime +90 | head
```

Un dossier vide se signale, un client sans activité depuis quatre-vingt-dix jours se propose à l'archivage.

## Le rapport

Présente un rapport structuré, du plus urgent au moins urgent :

```
=== Lint du workspace : YYYY-MM-DD ===

BLOQUANT (l'IA lit du faux)
- Contradiction : l'offre est à 1200 euros dans About-Me/my-company.md et 1500 dans
  Vente/Propositions/Propale-Acme_2026-09-10.md. Source de vérité : my-company. -> corriger l'autre
- ETAT périmé : Vente/Vente.md maj 2026-06-23, 42 fichiers modifiés depuis

À RANGER
- 4 versions de la landing dans Marketing/Event/Lancement/, aucune taguée final
- 3 fichiers sans frontmatter dans Produit-Client/Acme/

HYGIÈNE
- 2 tirets cadratins dans Contexte/Tone-and-Voice.md
- 1 dossier vide : Archives/

=== Plan proposé ===
1. ...
2. ...

Je corrige lesquels ?
```

## Règles

- Lecture seule tant que l'utilisateur n'a pas validé. Tu proposes, il décide.
- Corrige uniquement ce qu'il valide, un point à la fois, et récapitule à la fin.
- Ne supprime jamais un fichier : tu proposes un déplacement vers `Archives/`.
- En cas de doute sur la valeur juste d'une contradiction, demande. Ne tranche pas au hasard.
- Un lint qui ne trouve rien est un bon lint : dis-le en une ligne et arrête-toi.
- Français, vouvoiement, aucun tiret cadratin ni demi-cadratin.
