# Le Content Brain : structure et formats

Tous les skills de contenu lisent ce fichier avant d'écrire : `installer-contenu`, `strategie-contenu`, `clean-content`, le master `linkedin` et ses sous-skills, le master `infographie`, `planifier-post`. Il dit où vit chaque chose, comment une fiche est écrite, et les règles qui gardent le brain propre.

Le Content Brain est un dossier du workspace, pas un second cerveau à côté. Il ne recopie rien de ce que l'OS range déjà ailleurs : il y renvoie par des liens.

## Le dossier

```
05_Departements/Marketing/Content-Brain/
  Content-Brain.md              la carte : piliers, compteurs, trous. Reconstruite par script.
  _log.md                       une ligne par passage d'un skill qui modifie le brain
  01_Strategie/
    Strategie-contenu.md        écrite par strategie-contenu
    Posts-de-reference.md       vos meilleurs posts, avec leurs chiffres
    Pilier-N_<Nom>.md           une page par pilier. Reconstruite par script.
    Sujet_<Nom>.md              une page par sujet. Reconstruite par script.
  02_Veille/
    Sources-veille.json         newsletters et chaînes suivies (sous-skill veille)
    Comptes-veille.json         comptes LinkedIn suivis (sous-skill veille-createurs)
    Marche/                     une fiche par signal de marché
    Inspirations/               une fiche par post d'un autre
    sources/                    dumps bruts et caches des scripts, hors git
  03_Base-de-connaissances/
    Enseignements/              une idée par fiche
    Methodes/                   modèles, process, trames
    Preuves/                    chiffres, résultats, cas clients
    Histoires/                  vécu personnel et vécu client
    Sources/                    Posts/ Newsletters/ Calls/ Docs/ : une fiche par source traitée
  04_Idees/                     une fiche par idée de post
  05_Calendrier-editorial/
    Calendrier.md               les posts programmés et publiés, semaine par semaine
    Brouillons/                 un fichier par post en cours
    Publies/                    les posts sortis, avec date, lien et chiffres
    Recycles/                   les versions pour un autre canal
```

## Ce que le brain ne contient pas

| Besoin | Où ça vit | Comment le brain s'y relie |
|---|---|---|
| Offre, clients, voix | `02_Contexte/` | liens depuis `Strategie-contenu.md` |
| Règles d'écriture | `01_About-Me/anti-ai-voice.md` | lien depuis `Strategie-contenu.md` |
| Transcripts de calls | `07_Meeting/` | la fiche source pointe dessus |
| Propositions commerciales | `05_Departements/Vente/Propositions/` | la fiche source pointe dessus |
| Capture en vrac | `00_Inbox/` | traitée par `clean-content` |
| Sources brutes de veille, wiki | `08_Ressources/Veille/` | liens depuis les fiches de `Marche/` |
| Charte visuelle | `03_Branding/` | lue par le master `infographie` |
| Visuels et infographies | `05_Departements/Marketing/LinkedIn/` | liés depuis le post |
| Fichiers remplacés | `11_Archives/` | aucun skill ne supprime |

## Les formats de fiche

Chaque fiche commence par un frontmatter. Les noms de champs sont fixes : les skills et les scripts les cherchent tels quels.

### Fiche de connaissance (`03_Base-de-connaissances/`)

```markdown
---
type: enseignement        # enseignement | methode | preuve | histoire
pilier: [nom exact d'un pilier de Strategie-contenu.md]
sujets: [sujet 1, sujet 2]   # 1 à 3 sujets du pilier, le plus pertinent d'abord
douleur: [le problème client auquel la fiche répond, ou "aucune"]
source: "[[Sources/Calls/Call-Decouverte_2026-11-12]]"
diffusion: public         # public | anonyme | interne
date: 2026-11-12
utilise_dans: []          # liens vers les posts publiés qui s'en sont servis
---

# [L'idée, dite en une phrase complète]

[2 à 6 lignes courtes, dans les mots de l'utilisateur.]

**Preuve :** [chiffre, exemple ou résultat, ou "pas encore"]
**Sujets :** [[Sujet_Nom-du-sujet]]
**Voir aussi :** [[Autre fiche]]
```

Règles :
- Une idée par fiche. Une fiche qui en porte deux se coupe en deux.
- Le titre est l'idée elle-même, pas une étiquette. "Le premier call se gagne sur les questions" plutôt que "Découverte".
- Les chiffres restent tels que la source les donne.
- Pas de source, pas de fiche.
- Une fiche sans sujet renvoie à son pilier : `**Pilier :** [[Pilier-2_Nom]]`.
- Le dossier suit le type : `enseignement` dans `Enseignements/`, `methode` dans `Methodes/`, `preuve` dans `Preuves/`, `histoire` dans `Histoires/`.

### Fiche source (`03_Base-de-connaissances/Sources/`)

Ce dont les fiches sont tirées. Si la source n'a pas d'autre maison dans le workspace (un post, une newsletter), son texte entier vit ici. Si elle existe déjà ailleurs (un transcript, une proposition), la fiche pointe dessus et ne recopie rien.

```markdown
---
type: source
nature: call              # post | newsletter | call | doc | interview
date: 2026-11-12
traite_le: 2026-11-12
original: 07_Meeting/Prospects/2026-11/Transcript_Decouverte_2026-11-12.md
diffusion: anonyme
---

# [Titre court de la source]

[3 lignes : de quoi ça parle. Ou le texte entier pour un post ou une newsletter.]

**Fiches tirées de cette source :**
- [[Titre de la fiche]]
```

### Signal de marché (`02_Veille/Marche/`)

```markdown
---
type: marche
url: https://...
date: 2026-11-12
pilier: [pilier concerné]
---

# [Ce qui se passe, en une phrase]

[3 à 5 lignes : les faits, les chiffres tels qu'écrits.]

**Pourquoi ça compte pour mon client :** [une ligne]
**Mon avis :** [laissé vide pour l'utilisateur, ou "voir [[fiche]]"]
```

Un signal décrit ce que disent les autres. Il ne devient jamais l'opinion de l'utilisateur tout seul : un post part du signal et y répond avec une fiche de la base.

### Inspiration (`02_Veille/Inspirations/`)

```markdown
---
type: inspiration
auteur: [Prénom Nom]
url: https://...
format: hot-take          # educatif | storytelling | hot-take | lead-magnet
pilier: [pilier concerné, ou vide]
date: 2026-11-12
reactions:
commentaires:
---

# [Les deux premières lignes du post]

**Structure :** [comment le post est construit]
**Pourquoi ça marche :** [une ou deux lignes]
**Ce que j'en prends :** [la technique, l'angle ou le format, jamais les mots]
```

### Idée (`04_Idees/`)

```markdown
---
type: idee
statut: nouvelle          # nouvelle | retenue | redigee | publiee | ecartee
pilier: [pilier]
format: educatif          # educatif | storytelling | hot-take | lead-magnet
support: texte            # texte | carrousel | infographie | video
fiches: ["[[Fiche A]]", "[[Fiche B]]"]
signal: "[[Marche/...]]"  # facultatif
date: 2026-11-12
---

# [Titre de l'idée]

**Idée centrale :** [le point]
**Pourquoi maintenant :** [la raison de le publier cette semaine]
**Douleur :** [le problème client touché]
**Preuve :** [le chiffre, l'histoire ou l'exemple]
**Hook de départ :** [une ligne]
```

### Post (`05_Calendrier-editorial/`)

```markdown
---
type: post
statut: brouillon         # brouillon | programme | publie | recycle
format: educatif          # educatif | storytelling | hot-take | lead-magnet
support: texte            # texte | carrousel | infographie | video
canal: linkedin
pilier: [pilier]
idee: "[[04_Idees/...]]"
fiches: ["[[Fiche A]]"]
publie_le:
url:
impressions:
reactions:
commentaires:
partages:
releve_le:
chiffres_definitifs: non
---

[Le texte du post]
```

Nom du fichier : `Post-<Sujet>_<AAAA-MM-JJ>.md`. Les quatre valeurs de `format` sont les quatre sous-skills d'écriture du master `linkedin`.

## Le trajet d'un post

1. Une idée naît dans `04_Idees/` (`nouvelle`), puis est choisie (`retenue`).
2. Le post est écrit dans `Brouillons/` (`brouillon`), l'idée passe à `redigee`.
3. Il est programmé (`programme`), puis publié : le fichier passe dans `Publies/` (`publie`), l'idée à `publiee`.
4. À la publication, le lien du post est ajouté au champ `utilise_dans` de chaque fiche qu'il a utilisée.
5. `clean-content` relève les chiffres pendant 30 jours, puis marque `chiffres_definitifs: oui`.

L'idéation écarte les fiches utilisées dans les 90 derniers jours, sauf demande contraire.

## Le cloisonnement des clients

- Par défaut, les skills de contenu ne lisent ni `06_Clients/` ni `07_Meeting/Clients/`.
- L'ouverture se fait client par client, par un champ dans la note du client : `contenu: non`, `anonyme` ou `nomme`. Sans ce champ, c'est non.
- `anonyme` : le nom du client devient un rôle et un secteur ("le dirigeant d'un cabinet de conseil de 12 personnes"). `nomme` : le nom peut sortir.
- Chaque fiche porte `diffusion`. Les skills d'écriture n'utilisent jamais une fiche `interne`, et gardent l'anonymat d'une fiche `anonyme`.
- Une fiche tirée d'une proposition commerciale ou d'un email client est `interne` par défaut.
- Le flux va dans un seul sens : rien du Content Brain ne s'écrit dans un dossier client.
- Jamais de mot de passe, de clé, de coordonnées bancaires ni de donnée personnelle d'un tiers dans le brain.

## Les règles

- Un seul Content Brain. Si le dossier existe, on le complète.
- Les mots de l'utilisateur ne sont pas réécrits quand ils sont bons.
- Avant de créer une fiche, vérifier que l'idée n'existe pas déjà. Si oui, compléter la fiche et garder les deux sources.
- Les pages de piliers, les pages de sujets et la carte ne s'éditent pas à la main : on change le `pilier` ou les `sujets` d'une fiche, puis on relance `python3 10_Skills/clean-content/scripts/reconstruire.py`.
- Aucun skill ne supprime. Un fichier à retirer part dans `11_Archives/`, sur un oui.
- Aucun fait, chiffre ni citation inventé. Ce qui manque s'écrit "à confirmer" et se demande.
- Aucun tiret cadratin ni demi-cadratin.
- Chaque passage d'un skill qui modifie le brain ajoute une ligne à `_log.md`.
