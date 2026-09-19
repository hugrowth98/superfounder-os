---
name: lint
description: "Audit de santé du workspace ou d'un seul dossier : notes manquantes, sections Où on en est périmées, contradictions entre fichiers, frontmatter absent, versions non archivées, sous-dossiers par étape, fichiers à la racine, tirets cadratins, chemins morts, dossiers vides. Sur un dossier précis, ajoute l'audit de contexte : contradictions, répétitions, notes obsolètes, manques, infos mal rangées. Rapport puis plan. Lecture seule jusqu'à validation. Une fois par mois, ou avant de reprendre un dossier laissé longtemps."
user-invocable: true
context: main
---

# Lint : vérifier la santé du workspace

Un contexte écrit une fois et jamais vérifié devient faux, et une IA qui lit du faux produit du faux avec assurance. `/lint` passe le workspace au crible, produit un rapport, propose un plan. **Lecture seule : tu ne corriges rien avant validation.**

Argument optionnel : un dossier (`/lint "05_Departements/Vente"`). Sans argument, tout le workspace. Avec un dossier, les contrôles 1 à 9 se limitent à lui et le contrôle 10 s'ajoute.

## Les dix contrôles

### 1. Notes manquantes et sous-dossiers par étape

Tout projet, département et client a sa note (même nom que le dossier) et son `_log.md`. Aucun sous-dossier ne s'appelle `livrables`, `ressources`, `input` ou `output` : on range par nature, pas par étape. `sources/` est toléré pour le brut volumineux.

```bash
for d in "04_Projets"/*/ "05_Departements"/*/ "06_Clients"/*/; do
  d="${d%/}"; n=$(basename "$d")
  case "$n" in logos|photos) continue ;; esac
  [ -f "$d/$n.md" ]   || echo "NOTE MANQUANTE  $d/$n.md"
  [ -f "$d/_log.md" ] || echo "LOG MANQUANT    $d/_log.md"
done
find "04_Projets" "05_Departements" -type d \( -name livrables -o -name ressources -o -name input -o -name output \) | sed 's/^/SOUS-DOSSIER PAR ETAPE  /'
```

Note manquante : proposer la création depuis `08_Ressources/templates/projet.md`, `departement.md` ou `client.md`. Sous-dossier par étape : proposer l'aplatissement ou un nom par nature. Les `input/output/ressources` de `06_Clients/` sont tolérés tant que des scripts y pointent.

### 2. Sections Où on en est périmées

Un état qui n'a pas bougé depuis plus de trente jours alors que le dossier a des fichiers récents est un état mort, symptôme d'un `/done` qui n'a pas tourné.

```bash
grep -rl "^## Où on en est" --include="*.md" "04_Projets" "05_Departements" "06_Clients" | while IFS= read -r f; do
  maj=$(grep -m1 "^maj *:" "$f" | sed 's/[^0-9-]//g'); d=$(dirname "$f")
  recent=$(find "$d" -name "*.md" -mtime -30 -not -name "_log.md" | wc -l | tr -d ' ')
  echo "$maj | $recent fichiers récents | $f"
done | sort
```

### 3. Contradictions

Les valeurs qui doivent être uniques : un prix, une date d'event, un nom de marque, un objectif chiffré.

```bash
grep -rn --include="*.md" -E "[0-9 ]+ ?(euros|EUR|€)( ?/ ?| par )mois" "01_About-Me" "02_Contexte" "04_Projets" "05_Departements" | head -30
grep -rn --include="*.md" -iE "2[0-9] ?(au|-) ?2[0-9] sept" "01_About-Me" "04_Projets" | head -20
```

Pour chaque valeur trouvée à plusieurs endroits avec des contenus différents : nomme le fichier qui fait foi (`01_About-Me/my-company.md` pour l'offre et les prix, `02_Contexte/` pour l'ICP et le positionnement, `03_Branding/` pour la marque, la note du projet pour ses dates) et propose la correction des autres. En cas de doute, demande à l'utilisateur.

### 4. Frontmatter absent

```bash
find "04_Projets" "05_Departements" "06_Clients" "08_Ressources/templates" -name "*.md" -not -name "_log.md" -not -path "*/sources/*" -not -path "*/superfounder-os/*" | while IFS= read -r f; do
  head -1 "$f" | grep -q '^---$' || echo "SANS FRONTMATTER  $f"
done | head -40
```

Proposer `type`, `status`, `date`, `maj`. Cibler les notes et les livrables récents, pas les exports historiques.

### 5. Versions non archivées

Plusieurs versions d'un même livrable côte à côte, c'est n moins un fichiers faux.

```bash
find "04_Projets" "05_Departements" "06_Clients" -name "*.md" | sed -E 's/[-_]?v[0-9]+//; s/_2[0-9]{3}-[0-9]{2}-[0-9]{2}//' | sort | uniq -d | head -20
```

Identifier la version de référence (la plus récente, ou demander), lui mettre `status: final`, proposer le déplacement des autres vers `11_Archives/`.

### 6. Fichiers à la racine

```bash
ls -p | grep -v / | grep -vE "^(CLAUDE|AGENTS)\.md$|^opencode\.json$"
```

Tout autre fichier à la racine doit être routé vers un dossier ou `00_Inbox/`.

### 7. Tirets cadratins et demi-cadratins

```bash
grep -rln --include="*.md" -e $'\xe2\x80\x94' -e $'\xe2\x80\x93' "01_About-Me" "02_Contexte" "04_Projets" "05_Departements" "06_Clients" "10_Skills" | head -20
```

Tolérance zéro. Proposer tiret simple, deux-points, virgule ou parenthèses selon le contexte.

### 8. Chemins morts et anciens chemins

```bash
grep -rhoE '`[^`]+\.(md|csv|json|xlsx|py|sh)`' --include="*.md" "10_Skills" "04_Projets" "05_Departements" "06_Clients" CLAUDE.md | tr -d '`' | sort -u | while IFS= read -r p; do [ -e "$p" ] || echo "CHEMIN MORT  $p"; done | head -30
grep -rlnE "Projects/|Intelligence/|Produit-Client/|Marketing/|Strategie/|Veille/sources" --include="*.md" "10_Skills" "04_Projets" "05_Departements" "06_Clients" | grep -v "Veille/sources" | head
grep -rnE "(^|[^0-9] |[^0-9 ])(About-Me|Contexte|Branding|Journal|Meeting|Ressources|Skills|Archives|Inbox)/" --include="*.md" "10_Skills" CLAUDE.md AGENTS.md | grep -vE "[0-9]{2} (About-Me|Contexte|Branding|Journal|Meeting|Ressources|Skills|Archives|Inbox)/" | head
```

Un chemin sans son préfixe numérique (`Journal/` au lieu de `09_Journal/`) est un ancien chemin.

### 9. Dossiers vides et clients inactifs

```bash
find . -type d -empty -not -path "./.git/*" -not -path "*/superfounder-os/*" | head -20
find "06_Clients" -maxdepth 1 -mindepth 1 -type d -mtime +90 | head
```

Un dossier vide se supprime après validation. Un client sans activité depuis quatre-vingt-dix jours se propose à l'archivage. Un projet dont les Étapes sont toutes cochées aussi.

### 10. Audit de contexte d'un dossier (seulement avec un argument)

Le responsable d'un dossier, c'est l'utilisateur, et un contexte figé devient faux. Lis chaque note du dossier en entier, recompose ce que le dossier dit vraiment aujourd'hui, puis juge le reste sur cinq axes :

1. **Contradictions** : deux statuts, deux deadlines, deux prix, deux versions d'un process. Propose laquelle garder (la plus récente, la plus fiable). Si le doute reste, dis-le au lieu de trancher au hasard.
2. **Répétitions** : la même info dans deux notes. Propose la version unique et l'endroit où elle vit. Chaque info vit une seule fois.
3. **Notes obsolètes** : plus alignées avec la direction actuelle (ancienne version, projet fini, process remplacé). Propose `11_Archives/`. Le doute tranche vers l'archive.
4. **Manques** : un projet sans Étapes, un département sans Objectif, une note client sans interlocuteur dans Cadre, une section Où on en est encore en placeholder. Propose l'ajout concret.
5. **Mal rangées** : une info qui servirait mieux ailleurs. Propose la destination : un autre projet, un département, un client, `08_Ressources/`, ou `00_Inbox/` si un humain doit trancher.

## Le rapport

Du plus urgent au moins urgent :

```
=== Lint : <périmètre> : YYYY-MM-DD ===

BLOQUANT (l'IA lit du faux)
- Contradiction : l'offre est à 800 euros dans 01_About-Me/my-company.md et 990 dans
  04_Projets/Lancement-2026-10/Lancement-2026-10.md. Source de vérité : my-company. -> corriger l'autre
- Où on en est périmé : 05_Departements/Vente/Vente.md maj 2026-06-23, 42 fichiers modifiés depuis

À RANGER
- 12 versions de landing dans 04_Projets/Lancement-2026-10/, aucune taguée final
- 3 fichiers sans frontmatter dans 06_Clients/Alpha/

HYGIÈNE
- 2 tirets cadratins dans 02_Contexte/Tone-and-Voice.md
- 1 dossier vide : 05_Departements/Finance-Compta/

=== Plan proposé ===
1. ...
2. ...

Je corrige lesquels ?
```

## Exécution (après validation)

Chirurgicale : corriger une ligne, fusionner, déplacer. Pas de réécriture complète sans raison. Déplacer vers `11_Archives/` plutôt que supprimer. Si une destination n'existe pas, signaler au lieu d'inventer. Puis un log léger dans `09_Journal/YYYY-MM-DD.md`, au format de `/done` :

```markdown
## [HH:MM] Lint | <périmètre>

**Accompli**
- n contradictions résolues, n notes archivées, n infos déplacées, n sections ajoutées
```

## Règles

- Lecture seule tant qu'l'utilisateur n'a pas validé. Tu proposes, l'utilisateur décide.
- Corrige uniquement ce qu'il valide, un point à la fois, et récapitule à la fin.
- Ne supprime jamais un fichier : tu proposes un déplacement vers `11_Archives/`.
- Une contradiction citée est une contradiction avec une résolution proposée.
- Un lint qui ne trouve rien est un bon lint : dis-le en une ligne et arrête-toi.
- Français, vouvoiement avec l'utilisateur, aucun tiret cadratin ni demi-cadratin, pas d'emojis.
