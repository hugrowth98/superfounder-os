---
name: lead-qualifier
description: >
  Skill de tri rapide d'un gros export LinkedIn brut par seniorite / role. Utilise ce skill
  quand l'utilisateur a un fichier CSV LinkedIn (Sales Navigator, Lemlist, Waalaxy, Apify...)
  et veut un premier tri structurel par niveau de decision, avant le tri fin par ICP. Se
  declenche sur : "qualifie mes leads", "trie ce gros export", "scorer par seniorite",
  "classe par role", "CEO / CMO / Head of", "Tier 1 / Tier 2", "quels leads sont
  prioritaires". Produit un fichier Excel colore, trie, avec un onglet par categorie. Pour un
  tri par correspondance a l'ICP defini dans contexte.md, utiliser plutot `qualifier-liste`.
---

# Lead Qualifier - Tri rapide par seniorite

## Ce que fait ce skill (et sa difference avec qualifier-liste)

Ce skill fait un tri **structurel** d'un gros export LinkedIn : il classe chaque contact par
**role et niveau de decision** (CEO, CMO / Head of Marketing, Head of Sales, Freelance,
Directeur, Manager, Executant), lui met un score et un tier, et sort un Excel colore trie.

C'est complementaire de `qualifier-liste` :
- **lead-qualifier** (ce skill) : tri rapide, deterministe, par seniorite. Ideal sur un export
  brut de plusieurs centaines de lignes pour degrossir "qui est decideur ici".
- **qualifier-liste** : jugement fin par correspondance a **votre** ICP (secteur, taille,
  signaux) defini dans `contexte.md`. Ideal pour ne garder que ceux qui matchent vraiment
  votre client ideal.

Ordre conseille sur une grosse liste : `lead-qualifier` d'abord (degrossir par seniorite),
puis `qualifier-liste` sur le Tier 1 / Tier 2 (affiner par ICP).

A partir d'un ou plusieurs CSV, le skill :

1. Lit tous les leads sans en manquer aucun
2. Detecte automatiquement les noms de colonnes (camelCase `jobTitle`, snake_case
   `job_title`, etc.)
3. Classifie chaque contact dans une categorie standardisee selon son titre de poste et la
   taille de son entreprise
4. Attribue un score (1-10) et un tier (Tier 1 / Tier 2 / Tier 3 / -)
5. Genere un fichier Excel formate, colore, avec filtres, onglets par categorie et onglet
   resume, en conservant toutes les colonnes originales du CSV

## Categories et logique de tiering

| Categorie | Tier | Score |
|---|---|---|
| CEO (>10 employes) | Tier 1 | 10 |
| CEO (<=10 ou taille inconnue) | Tier 1 | 9 |
| CMO / Head of Marketing | Tier 2 | 6-8 selon taille |
| Head of Sales | Tier 2 | 6-8 selon taille |
| Freelance / Independant | Tier 3 | 4 |
| Directeur / C-suite | - | 1 |
| Responsable / Manager | - | 1 |
| Executant | - | 1 |

Le score CMO/Sales suit la taille d'entreprise : >50 salaries -> 8 | 11-50 -> 7 | <=10 ou
inconnu -> 6.

> Cette grille est un tri de seniorite generique (le decideur passe avant l'executant). Elle
> ne remplace pas votre ICP : un "CEO" peut etre hors cible et un "Manager" peut etre le bon
> interlocuteur selon votre marche. C'est `qualifier-liste` qui tranche la pertinence par
> rapport a `contexte.md`.

## Colonnes attendues dans le CSV

Le script detecte automatiquement les colonnes par leurs alias (camelCase, snake_case,
majuscules) :

| Role | Noms acceptes |
|---|---|
| Poste actuel | `occupation`, `Occupation`, `poste` |
| Titre / headline | `jobTitle`, `job_title`, `JobTitle`, `headline`, `title` |
| Taille entreprise | `companySize`, `company_size`, `companyEmployeesOnLinkedin`, `company_employees` |

**Toutes les autres colonnes du CSV sont conservees intactes** dans le fichier de sortie. Le
script ajoute uniquement trois colonnes en tete : `Categorie`, `Score`, `Tier`.

## Comment utiliser ce skill

### Etape 1 - Recuperer les fichiers

Demander a l'utilisateur ses fichiers CSV (il peut en donner plusieurs). S'ils sont deja dans
le contexte, passer directement a l'etape 2.

### Etape 2 - S'assurer que les dependances sont la (une seule fois)

Le script utilise `pandas` et `openpyxl`. L'utilisateur n'a rien a installer lui-meme : si un
`import` echoue, c'est **toi** qui lances l'installation, puis tu relances le script :

```bash
python3 -c "import pandas, openpyxl" 2>/dev/null || pip install pandas openpyxl
```

### Etape 3 - Lancer le script de classification

```bash
python3 .claude/skills/lead-qualifier/scripts/classify_leads.py \
  --files "/chemin/vers/fichier1.csv" "/chemin/vers/fichier2.csv" \
  --output "<meme dossier que l'input>/<nom-original>_qualifie.xlsx"
```

Enregistrer le fichier de sortie **dans le meme dossier que le CSV d'entree** (convention de
l'OS), suffixe `_qualifie.xlsx`. Le script :
- accepte un ou plusieurs fichiers CSV
- detecte automatiquement les colonnes disponibles
- supprime les colonnes de qualification existantes si le CSV a deja ete traite (re-run
  propre)
- applique la pipeline de classification complete (voir logique ci-dessous)
- conserve toutes les colonnes originales et ajoute `Categorie`, `Score`, `Tier` en tete
- genere le fichier Excel avec tous les onglets

### Etape 4 - Presenter le resultat

Indiquer a l'utilisateur : nombre total de leads traites, distribution par categorie (combien
de CEO, CMO, Freelance...), chemin du fichier Excel. Puis proposer la suite logique : affiner
le Tier 1 / Tier 2 avec `qualifier-liste` selon son ICP.

## Logique de classification (pour debogage ou ajustement)

Pipeline de priorite P0 -> P10 :

**P0 - Stagiaire / alternant** -> toujours Executant (stagiaire, intern, alternant,
apprentissage)

**P1 - Freelance explicite** -> freelance, independant, auto-entrepreneur, solopreneur,
fractionnel, portage salarial, manager de transition

**P2 - Freelance fonctionnel dans `occupation`** -> consultant, coach, formateur, expert,
specialiste, architecte, copywriter, advisor, avocat, entrepreneur...
*(Quand ces mots apparaissent dans le poste reel, pas juste dans la bio, c'est le signal le
plus fort)*

**P3 - CMO / Head of Sales dans `occupation`** -> cmo, vp marketing, head of marketing,
directeur commercial, head of sales...

**P4 - CEO dans `occupation`** -> fondateur, founder, ceo, pdg, gerant, president, owner,
managing director...
- Si taille = 1 -> Freelance
- Si taille > 10 -> CEO
- Sinon : si bio contient des mots fonctionnels -> Freelance, sinon CEO

**P5 - CEO dans `job_title` seulement** (signal plus faible)
- Si `occupation` a du contenu mais pas de mot CEO -> Freelance
- Si negatifs presents (futur entrepreneur, leadership diversite...) -> Responsable

**P6 - CMO / Head of Sales dans `job_title`** (si `occupation` n'est pas niveau "responsable")

**P7 - Mots fonctionnels dans `job_title`** -> Freelance

**P8 - Mots executants explicites** -> Executant (developer, designer, analyst, assistant...)

**P9 - C-suite / Directeur dans `occupation`** -> Directeur / C-suite (coo, cfo, vp, head of,
directeur...)

**P10 - Manager dans le texte combine** -> Responsable / Manager

**Defaut** -> Executant

## Regles importantes a retenir

- **`occupation` > `job_title`** : le poste actuel est toujours plus fiable que la headline
  marketing.
- **"Responsable" dans `occupation`** bloque la promotion en CMO/Sales depuis job_title seul.
- **Entrepreneur solo = Freelance** : "entrepreneur" seul sans "fondateur" ou titre clair.
- **Part-time** : uniquement si suivi d'un titre (ex: "part-time CMO") -> Freelance.
- **Associe en profession liberale** -> peut etre Directeur/C-suite selon contexte.

## Output Excel

- **Onglet "Tous les leads"** : tous les contacts tries par score decroissant, `Categorie` /
  `Score` / `Tier` en premieres colonnes (colorees), suivies de toutes les colonnes originales
- **Onglet "Resume"** : recapitulatif par categorie avec comptage
- **Un onglet par categorie** : "CEO", "Freelance - Independant", "CMO - Head of Marketing"...

Codes couleur : vert fonce = Tier 1 | bleu = Tier 2 | orange = Tier 3 | gris = hors tier
