---
name: clean-content
description: >
  Le passage hebdomadaire qui garde le Content Brain à jour : traite l'inbox, transforme les
  nouveaux calls et les nouvelles propositions en fiches de la base de connaissances, relève les
  chiffres des posts publiés (Unipile) et les écrit dans le calendrier éditorial, relève les posts
  qui ont marché chez les comptes suivis, produit le brief de veille, reconstruit les pages de
  piliers et la carte, puis rend un rapport court avec les décisions à prendre. Se
  déclenche sur "clean content", "nettoie mon contenu", "mets à jour mon brain", "passage du
  lundi", "où en est mon contenu", "relève les chiffres de mes posts", "reconstruis mes piliers",
  et par la tâche planifiée du lundi. Ne pas utiliser pour installer le Content Brain
  (`installer-contenu`), pour revoir la stratégie (`strategie-contenu`), pour écrire un post
  (master `linkedin`), ni pour la santé du reste du workspace (`lint`).
---

# Clean content

Tu fais le passage hebdomadaire du Content Brain. L'utilisateur ne doit rien avoir à ranger : tu lis ce qui est arrivé dans la semaine, tu l'ajoutes au bon endroit, tu reconstruis les pages et tu lui rends un rapport qu'il lit en deux minutes. Vouvoiement, aucun tiret cadratin.

Lis d'abord `10_Skills/_commun/content-brain.md` (structure, formats de fiche, cloisonnement des clients), puis `Content-Brain/Content-Brain.md` et `01_Strategie/Strategie-contenu.md`. Si la stratégie contient encore `[à remplir]` dans la section Piliers, arrête-toi et propose "Installe mon contenu".

Tu peux lancer une seule étape quand l'utilisateur la demande ("relève les chiffres de mes posts" : étape 4 puis 7).

## Les huit étapes

### 1. Lire l'état

La carte, la stratégie, la dernière ligne de `_log.md` (la date du dernier passage, qui borne "depuis quand"), et le champ `contenu:` des notes de `06_Clients/`.

### 2. L'inbox

Les fichiers de `00_Inbox/` qui relèvent du contenu : un post collé, une idée, un lien, une note vocale transcrite. Chacun devient une fiche source, une idée ou une inspiration, au format du fichier de structure. Ce qui ne relève pas du contenu reste dans l'inbox pour `/inbox-processor`. L'original part dans `11_Archives/` une fois traité, sur un oui.

### 3. Les nouveaux calls et les nouvelles propositions

Depuis le dernier passage :

- `07_Meeting/Prospects/`, `Interne/`, `Autres/` : tous les nouveaux transcripts. `07_Meeting/Clients/<Nom>/` : seulement si la note du client dit `contenu: anonyme` ou `nomme`.
- `05_Departements/Vente/Propositions/` : les nouvelles propositions. Leur fiche source est `diffusion: interne`, les fiches qui en sortent sont anonymisées.

Pour chaque source :

1. Vérifie qu'elle n'a pas déjà sa fiche dans `03_Base-de-connaissances/Sources/` (champ `original`). Si oui, passe.
2. Écris la fiche source : trois lignes de résumé et le chemin de l'original. Le transcript et la proposition ne sont pas recopiés.
3. Relève les idées qui valent une fiche. Le tri : une scène vécue ou un fait précis, une douleur client reconnue, quelque chose que l'utilisateur est seul à pouvoir dire. Une généralité ne passe pas.
4. Pour chaque idée, vérifie qu'elle n'existe pas déjà dans la base. Si oui, complète la fiche existante et ajoute la source. Sinon, écris une fiche dans `Enseignements/`, `Methodes/`, `Preuves/` ou `Histoires/`, avec `pilier`, `sujets`, `douleur`, `source`, `diffusion`.
5. Garde les mots exacts de l'utilisateur et ceux du client quand ils sont bons. Les chiffres restent tels quels.
6. Dans la note de `Vente/` ou du client concerné, ajoute en Key Notes un lien vers les preuves tirées de cette source, si elles peuvent resservir en vente.

Au-delà de 15 nouvelles sources, traite les 15 plus récentes et dis combien il en reste.

### 4. Les chiffres des posts

```bash
python3 10_Skills/clean-content/scripts/releve_posts.py --dry-run
python3 10_Skills/clean-content/scripts/releve_posts.py --limite 40
```

Le script lit les derniers posts du compte LinkedIn via Unipile, met à jour impressions, réactions, commentaires et partages dans le frontmatter de chaque post de `05_Calendrier-editorial/Publies/`, marque les chiffres comme définitifs 30 jours après la publication, et ajoute le lien du post dans le champ `utilise_dans` des fiches qu'il a utilisées.

- Les posts LinkedIn absents du calendrier sont listés. Propose `--importer` : chacun devient un fichier dans `Publies/`, dont tu remplis ensuite `format` et `pilier` en lisant le texte.
- Unipile non branché : dis-le, propose `connecter-outils`, et prends les chiffres que l'utilisateur colle (`--depuis-json`) ou ceux de `planifier_post.py --stats` si Publora est branché.
- Un post qui dépasse nettement la moyenne des 20 derniers : propose de l'ajouter à `01_Strategie/Posts-de-reference.md` avec une ligne "ce qui marche". Le sous-skill `performance` fait l'analyse complète.

### 5. Ce qui a marché chez les autres

Si `02_Veille/Comptes-veille.json` existe et que le dernier run a plus de quatre semaines, lance le sous-skill `veille-createurs` du master `linkedin`. Propose au plus cinq posts à garder comme fiches dans `02_Veille/Inspirations/`, chacun avec sa structure et ce qu'on en prend. Rien n'y est écrit sans un oui.

### 6. La veille

Si `02_Veille/Sources-veille.json` est rempli, lance le sous-skill `veille`. De son brief :

- les signaux qui touchent un pilier deviennent des fiches dans `02_Veille/Marche/`, trois au plus par semaine ;
- les idées de posts retenues par l'utilisateur deviennent des fiches dans `04_Idees/`, chacune reliée à une fiche de la base quand il en existe une.

Un signal ne devient jamais l'opinion de l'utilisateur : le champ "Mon avis" reste vide, ou renvoie à une fiche existante.

### 7. Reconstruire

```bash
python3 10_Skills/clean-content/scripts/reconstruire.py --dry-run
python3 10_Skills/clean-content/scripts/reconstruire.py
```

Le script refait les pages de piliers dans `01_Strategie/Piliers/` (une page par pilier, ses sujets en sections avec le lien vers chaque fiche, puis ses idées, ses posts et sa veille), la ligne `**Pilier :**` en bas de chaque fiche, la section "Où on en est" de la carte et le tableau par semaine du calendrier. Il n'y a pas de page par sujet : si une version précédente en a laissé dans `01_Strategie/`, le script les range dans `11_Archives/`, avec les anciennes pages de piliers numérotées, et refait les pages de piliers au nom `Pilier_<Nom>.md`. Il ne supprime rien. Lis ses alertes : fiche sans pilier reconnu, sujet hors stratégie, page qui ne correspond plus à la stratégie. Corrige le champ de la fiche quand la bonne valeur est évidente, sinon mets la question dans le rapport.

Passe aussi le contrôle de cloisonnement : cherche les noms des dossiers de `06_Clients/` dans `03_Base-de-connaissances/` et `05_Calendrier-editorial/`. Chaque occurrence chez un client qui n'est pas `nomme` va dans le rapport.

### 8. Le rapport

Dans le chat, jamais dans un fichier du Content Brain, et en une ligne dans `Content-Brain/_log.md` (`- AAAA-MM-JJ : clean-content, N fiches, N sources, N posts relevés`). Format :

```
## Cette semaine
- Inbox : ...
- Calls et propositions : N sources, N fiches
- Posts : N relevés, le meilleur (titre, chiffres)
- Veille : N signaux, N idées

## Les 3 meilleures nouvelles fiches
[titre, pilier, une ligne sur pourquoi elle vaut un post]

## Ce qui se passe sur votre marché
[3 signaux au plus, chacun avec une question pour l'utilisateur]

## Où votre brain est mince
[par pilier : le sujet sans fiche, sans preuve ou sans histoire, et le remède]

## Décisions qui vous attendent
[doublons possibles, fiches sans pilier, sources en erreur, posts à classer, noms de clients trouvés]

## Vos 5 minutes cette semaine
[une seule question à creuser avec "interviewe-moi"]
```

Un rapport sans rien de neuf tient en trois lignes. Ne remplis pas les sections vides.

## La planification

À la fin du premier passage, propose de le programmer chaque lundi matin : une tâche planifiée dans l'application Claude si elle est disponible, sinon une ligne dans le plan de `/weekly-review`. Note le choix dans la section Cadre de `Content-Brain.md`. Un passage planifié s'arrête avant toute écriture qui demande un oui (archivage, inspirations, posts de référence, import de posts) et les met dans "Décisions qui vous attendent".

## Règles

- Rien n'est supprimé. Ce qui doit sortir part dans `11_Archives/`, sur un oui.
- Pas de source, pas de fiche. Aucun fait, chiffre ni citation inventé.
- Les clients sont fermés au contenu par défaut. Le nom d'un client `anonyme` devient un rôle et un secteur.
- Les pages de piliers et la carte ne s'éditent pas à la main : on corrige la fiche, on relance le script.
- Aucun envoi, aucune publication : ce skill lit, range et rapporte.
- `--dry-run` avant chaque script, et le résultat montré avant l'écriture.
- Aucun tiret cadratin ni demi-cadratin.

## Exemples

- "Clean content" un lundi : les huit étapes ; réponse attendue : le rapport, puis les questions de la section Décisions, une à la fois.
- "Relève les chiffres de mes posts" : étape 4 puis 7 ; réponse attendue : le tableau des posts mis à jour et le meilleur de la période.
- "J'ai changé un pilier, reconstruis" : étape 7 ; réponse attendue : les pages créées, les fiches dont le pilier n'existe plus, et la proposition de les rattacher.
