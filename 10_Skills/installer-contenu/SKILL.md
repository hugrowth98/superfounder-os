---
name: installer-contenu
description: >
  Installe la machine de contenu de Superfounder OS et son Content Brain en dix phases : lit le
  second cerveau (02_Contexte/) et fait l'inventaire de ce qui existe (posts, newsletters,
  transcripts), capte la voix, range les posts de référence et leurs chiffres, construit la
  stratégie de contenu (skill `strategie-contenu` : première version, avis, interview de
  challenge), crée le Content Brain et ses pages de piliers et de sujets, règle le cloisonnement
  des clients, fait une première récolte de fiches dans la base de connaissances, branche la
  veille et les comptes suivis, la charte visuelle et le profil, puis rend un bilan et programme
  le passage hebdomadaire `clean-content`. Deuxième entrée, relançable : "Nourris mon brain"
  traite une nouvelle source ou l'inbox. Se déclenche sur "Installe mon contenu", "installe mon
  content brain", "nourris mon brain", "ajoute cette source à mon brain", "traite mon inbox de
  contenu", "configure mon contenu", "setup LinkedIn", "ajoute mes sources de veille", ou tout
  premier message quand Strategie-contenu.md contient encore [à remplir].
---

# Installer mon contenu

Tu installes la machine de contenu pour l'utilisateur. Il vient de dire "Installe mon contenu" et veut que le master `linkedin` et le master `infographie` écrivent dans sa voix, avec sa stratégie et à partir de ce qu'il a déjà dit, écrit et vécu. Vouvoiement, une question à la fois, une valeur par défaut chaque fois que c'est raisonnable, jamais de tiret cadratin. Comptez 1 h 30 à 2 h, en plusieurs fois : chaque phase se termine par une écriture validée, on peut reprendre à la suivante.

Lis d'abord `10_Skills/_commun/content-brain.md` : la structure du Content Brain, les formats de fiche, le cloisonnement des clients. Suis-le à la lettre.

Le principe : aucun skill de contenu ne contient de donnée sur l'utilisateur, et une information vit à un seul endroit. Ton travail est d'écrire les bons fichiers au bon endroit, une seule fois chacun :

| Information | Où elle vit | Qui l'écrit |
|---|---|---|
| Offre, différenciation, preuves | `02_Contexte/Offer-Positioning.md` | le second cerveau |
| Clients, problèmes, mots exacts | `02_Contexte/Clients-Problems-and-Messages.md` | le second cerveau |
| Voix, marqueurs de style, ce qu'il ne dit jamais | `02_Contexte/Tone-and-Voice.md` | le second cerveau (ou ce skill si vide) |
| Stratégie de contenu : convictions, piliers, sujets, répartition, cadence | `Content-Brain/01_Strategie/Strategie-contenu.md` | `strategie-contenu` (phase 3) |
| Ses meilleurs posts, avec leurs chiffres | `Content-Brain/01_Strategie/Posts-de-reference.md` | ce skill, puis `clean-content` et `performance` |
| Newsletters et chaînes à lire chaque semaine | `Content-Brain/02_Veille/Sources-veille.json` | ce skill (phase 8) |
| Comptes LinkedIn à suivre | `Content-Brain/02_Veille/Comptes-veille.json` | ce skill (phase 8), sur un oui |
| Posts des autres qui l'inspirent | `Content-Brain/02_Veille/Inspirations/` | ce skill, puis au fil de l'eau |
| Ce qu'il sait, ce qu'il a vécu, ses preuves | `Content-Brain/03_Base-de-connaissances/` | ce skill (phase 6), puis `clean-content` et `interview` |
| Ce qu'un client accepte de voir dans le contenu | le champ `contenu:` de sa note dans `06_Clients/` | ce skill (phase 5) |
| Couleurs, typographies, logo, interdits | `03_Branding/charte-visuelle.md` | ce skill (phase 9), sur un oui explicite |
| Clé Publora, si l'utilisateur programme depuis le chat | `.env` (`PUBLORA_API_KEY`) | `connecter-outils` |

Tous les chemins `Content-Brain/` sont sous `05_Departements/Marketing/`.

**Règle d'or : n'invente jamais le positionnement, les convictions, le ton, les sources ni le contenu d'une fiche.** Déduis de ce qui est écrit, ou demande. Présente ta proposition et fais valider avant d'écrire.

Ne crée jamais un second Content Brain : si le dossier existe, complète-le.

---

## Phase 0 : lire et inventorier

Sans rien demander :

1. Lis `02_Contexte/Offer-Positioning.md`, `Clients-Problems-and-Messages.md`, `Tone-and-Voice.md`, puis `Content-Brain/Content-Brain.md`, `01_Strategie/Strategie-contenu.md`, `Posts-de-reference.md` et `03_Branding/charte-visuelle.md`. Note ce qui contient encore `[à remplir]`.
2. Compte la matière déjà présente dans le workspace : les posts et brouillons de `05_Departements/Marketing/` (LinkedIn, Newsletter), les transcripts de `07_Meeting/` par dossier, les propositions de `05_Departements/Vente/Propositions/`, les fichiers de `00_Inbox/`, les fiches déjà dans la base.
3. Annonce l'inventaire en trois lignes ("J'ai trouvé 34 posts, 6 newsletters et 21 transcripts, dont 9 calls clients qui restent fermés tant que vous ne les ouvrez pas") et le plan des phases.

Cas à traiter :
- **Le second cerveau est rempli** : cas normal, aucune question sur l'offre, la cible ou la voix.
- **`Tone-and-Voice.md` est vide** : tu le construiras à la phase 1 depuis ses posts, et tu l'écriras dans `02_Contexte/` après validation.
- **Offre ou clients vides** : dis-le, propose "Installe mon second cerveau" d'abord, ou de continuer avec ce que ses posts révèlent (moins précis).
- **Une partie est déjà faite** : annonce où on en est et reprends à la première phase incomplète. Chaque phase a un critère "fait" en dernière ligne.

## Phase 1 : la voix et le style

Demande 5 à 10 de ses meilleurs posts LinkedIn, de types différents, avec leurs chiffres s'il les a. S'il y en a déjà dans le workspace, propose de partir de ceux-là. S'il n'en a aucun, passe en mode manuel : trois questions sur le ton (comment il parle à un client au téléphone, ce qu'il ne dirait jamais, tutoiement ou vouvoiement).

Depuis les posts : le ton, les marqueurs de style (symboles, longueur des phrases, ouvertures, façon de finir), le vocabulaire, ce qu'il ne dit jamais, la langue, et ses expressions à lui pour la section 7 d'`01_About-Me/anti-ai-voice.md`. Si `Tone-and-Voice.md` était vide : présente, fais valider, écris. Sinon : signale seulement ce que les posts contredisent, et propose un diff.

Garde ses mots, ses tics, ses formulations. Ton travail est de capturer sa voix, pas de la réécrire.

Fait quand : `Tone-and-Voice.md` ne contient plus `[à remplir]`.

## Phase 2 : les posts de référence et leurs chiffres

1. Range les posts par format dans `Posts-de-reference.md` (éducatif, storytelling, hot take, lead magnet, autres), avec pour chacun une ligne "ce qui marche" et ses chiffres.
2. Déduis la synthèse de fin de fichier : marqueurs visuels, structure typique, longueurs, sujets à éviter.
3. Avec des chiffres pour 10 posts ou plus : applique la méthode des tiers du sous-skill `performance` (`10_Skills/linkedin/ressources/analyse-performance.md`) et écris une section "Ce qui marche chez vous". Sinon, laisse un rappel : "à remplir après 20 posts".

Fait quand : `Posts-de-reference.md` contient au moins 5 posts.

## Phase 3 : la stratégie de contenu

Passe la main au skill `strategie-contenu` (`10_Skills/strategie-contenu/SKILL.md`), en séance complète. Il lit tout le second cerveau, rédige une première version, donne son avis, challenge l'utilisateur en interview, et écrit `Strategie-contenu.md`. Les histoires et les chiffres donnés pendant l'interview deviennent déjà des fiches de la base.

Reviens ici quand la section Piliers a 3 ou 4 piliers, chacun avec 4 à 8 sujets. Les autres sections peuvent garder des questions ouvertes : ne bloque pas.

Fait quand : la section Piliers et la section Convictions ne contiennent plus `[à remplir]`.

## Phase 4 : créer le Content Brain

1. Vérifie que tous les dossiers du fichier de structure existent sous `Content-Brain/`. Crée ce qui manque, ne touche pas au reste.
2. Lance `python3 10_Skills/clean-content/scripts/reconstruire.py --dry-run`, montre les pages qui seraient créées (une par pilier, une par sujet), puis relance sans `--dry-run` sur un oui.
3. Dis à l'utilisateur d'ouvrir le workspace dans Obsidian s'il veut la vue en graphe : la carte au centre, les piliers, les sujets, puis les fiches à mesure qu'elles arrivent. Obsidian n'est qu'une visionneuse, rien ne casse sans lui.

Fait quand : `01_Strategie/` contient une page `Pilier-N_` par pilier de la stratégie.

## Phase 5 : le cloisonnement des clients

Les calls et les dossiers clients sont fermés au contenu par défaut. Pour chaque dossier de `06_Clients/` qui a une note, pose une question : "Ce que vous vivez avec [client] peut-il nourrir vos posts ?" Trois réponses :

- `non` : rien n'est lu. C'est la valeur par défaut, et celle à garder en cas de doute.
- `anonyme` : les calls sont lus, le client devient un rôle et un secteur dans les fiches.
- `nomme` : le nom peut sortir. À réserver aux clients qui ont donné leur accord.

Écris le champ `contenu:` dans le frontmatter de la note du client. Avec plus de dix clients, propose une réponse par lot ("tous en anonyme sauf ceux que vous me citez"), puis fais valider la liste.

Fait quand : chaque note de `06_Clients/` a un champ `contenu:`.

## Phase 6 : la première récolte

Tu transformes la matière de l'inventaire en fiches. Vingt sources pour commencer, les plus riches d'abord : les posts de référence, les newsletters, les lives et ateliers, les calls prospects, puis les calls des clients ouverts à la phase 5.

Pour chaque source, une à la fois :

1. **La fiche source** dans `03_Base-de-connaissances/Sources/<Posts|Newsletters|Calls|Docs>/`. Un post ou une newsletter sans autre maison dans le workspace : le texte entier. Un transcript ou une proposition : trois lignes et le chemin de l'original, rien n'est recopié. Une proposition ou un email client : `diffusion: interne`.
2. **Les idées qui valent une fiche.** Le tri : une scène vécue ou un fait précis, une douleur client reconnue, quelque chose que l'utilisateur est seul à pouvoir dire. Une généralité ne passe pas.
3. **Le doublon.** Avant de créer, cherche l'idée dans la base. Si elle y est, complète la fiche existante et ajoute la source.
4. **La fiche**, une idée chacune, dans `Enseignements/`, `Methodes/`, `Preuves/` ou `Histoires/` : le titre est l'idée dite en une phrase, le corps garde ses mots, les chiffres restent tels quels. Remplis `pilier` avec un pilier de la stratégie et `sujets` avec 1 à 3 de ses sujets. N'invente jamais un sujet : une fiche sans sujet qui convient garde `sujets: []`.
5. **La diffusion** : `public`, `anonyme` ou `interne`, selon la source et le champ `contenu:` du client.

Après les trois premières sources, arrête-toi : montre les trois meilleures fiches et fais valider le format (longueur, ton, niveau de détail). Corrige avant de continuer.

Donne un point d'avancement toutes les cinq sources ("12 sources faites, 31 fiches"). Au-delà de 40 sources, travaille par lots de 20 et demande avant chaque lot.

Fait quand : la base contient au moins une fiche par pilier.

## Phase 7 : organiser par pilier

1. Vérifie que chaque fiche a un `pilier` et, quand c'est possible, des `sujets`.
2. Lance `python3 10_Skills/clean-content/scripts/reconstruire.py` : il écrit la ligne de lien en bas de chaque fiche, refait les pages de piliers et de sujets, et la section "Où on en est" de la carte.
3. Lis ses alertes (fiche sans pilier reconnu, sujet hors stratégie) et corrige les fiches concernées.

Ces pages ne s'éditent jamais à la main : pour changer une page, on change le champ d'une fiche.

Fait quand : le script ne signale plus aucune fiche sans pilier.

## Phase 8 : la veille

C'est le sous-skill `veille` du master `linkedin` qui lira ces sources chaque semaine. Trois questions :

1. **Les newsletters** qu'il lit vraiment (3 à 10) : pour chacune, le nom et l'URL du flux RSS (Substack : `https://<nom>.substack.com/feed`, même avec un domaine personnalisé ; un blog : son flux `/feed`, `/rss` ou `/feed.xml`). Range-les par thème avec un tier (1 = chaque semaine).
2. **Les chaînes YouTube** (3 à 10) : l'identifiant `@handle` de chacune, par tier.
3. **Les autres flux** RSS ou Atom, s'il en a.

Écris `Content-Brain/02_Veille/Sources-veille.json` (le gabarit livré contient un bloc `_exemple`, la structure exacte est dans le sous-skill `veille`). Puis le premier run, pour vérifier que tout se lit :

```bash
python3 10_Skills/linkedin/scripts/abonnes.py --force
python3 10_Skills/linkedin/scripts/veille.py --jours 14 --tier tous --sans-transcripts --format md --stdout
```

Corrige les flux en erreur. Propose ensuite les transcripts YouTube : `pip3 install youtube-transcript-api` (une commande, gratuite) ; sans elle, le script tourne sans transcripts et le dit.

Du premier brief, écris une fiche de signal dans `02_Veille/Marche/` et montre-la : c'est le format que `clean-content` suivra.

Deux questions facultatives :
- **Les comptes LinkedIn** dont il veut voir les posts qui performent (5 à 50 URLs de profil). S'il en donne, écris `02_Veille/Comptes-veille.json` (format dans le sous-skill `veille-createurs`) et note dans la stratégie, section Créateurs admirés, ce qu'il prend de chacun.
- **Des posts qu'il admire**, sous la main : une fiche par post dans `02_Veille/Inspirations/`, avec la structure et ce qu'il en prend, jamais les mots.

Fait quand : `Sources-veille.json` a au moins une source, ou l'utilisateur a dit qu'il passait.

## Phase 9 : la charte visuelle et le profil

Deux étapes qui se sautent chacune en une phrase.

`03_Branding/` est une zone protégée : tu n'y écris que sur un oui explicite. Demande ses couleurs (fond, texte, un accent) et sa police, ou l'URL de son site pour les lire, et s'il a un logo. Écris `03_Branding/charte-visuelle.md` et coche la case dans `03_Branding/Branding.md`. S'il ne sait pas : laisse `[à remplir]`, le master `infographie` partira sur un style neutre et le dira.

Propose de passer le profil au sous-skill `profil` du master `linkedin`. Si Publora est branché ou s'il veut programmer depuis le chat, c'est le moment de lancer `connecter-outils` pour la clé et d'écrire "Publora" dans la ligne Programmation de la stratégie.

## Phase 10 : le bilan et la suite

1. Relance `reconstruire.py`, puis lis la carte et rends le bilan : le nombre de fiches par pilier et par type, les trois fiches les plus fortes (cite leur titre), les sujets sans fiche, sans preuve ou sans histoire.
2. Pour chaque manque, un remède en une ligne. Une catégorie vide parce que la matière n'existe pas encore s'écrit "rien de disponible" : ce n'est pas un échec, le remède est "interviewe-moi" (sous-skill `interview`) et l'enregistrement des prochains calls.
3. Dis en une phrase si le brain est prêt pour écrire : une stratégie remplie, et au moins cinq fiches par pilier.
4. Vérifie qu'aucun `[à remplir]` ne subsiste dans les sections Convictions, Piliers, Répartition éditoriale, Objectif et cadence de la stratégie.
5. Propose de programmer `clean-content` chaque lundi (voir sa section Planification), et lance le premier passage si l'utilisateur le veut.
6. Ajoute une ligne à `Content-Brain/_log.md`.

> "Votre Content Brain est en place. On écrit un premier post à partir d'une de vos fiches, ou vous voulez des idées pour la semaine ?"

---

## Nourris mon brain

La deuxième entrée, à utiliser dès que le Content Brain existe. L'utilisateur colle un post, un transcript, une newsletter, un document, ou dit "traite mon inbox".

1. Lis le fichier de structure, la stratégie (les piliers et leurs sujets) et le champ `contenu:` du client si la source en concerne un.
2. Applique la phase 6 à la source, ou à chaque fichier de contenu de `00_Inbox/`.
3. Applique la phase 7.
4. Rends en trois lignes : les fiches créées, les fiches complétées, les trous que cette source a comblés.

Les autres demandes relançables : "ajoute mes sources de veille" (phase 8), "ouvre ce client au contenu" (phase 5), "refais le bilan" (phase 10), "revois ma stratégie" (skill `strategie-contenu`).

---

## Règles

- Une seule question à la fois, une valeur par défaut chaque fois que c'est raisonnable.
- Un seul Content Brain. Rien n'est supprimé : ce qui doit sortir part dans `11_Archives/`, sur un oui.
- Pas de source, pas de fiche. Une idée par fiche. Les mots de l'utilisateur ne sont pas réécrits quand ils sont bons.
- Les clients sont fermés au contenu tant que leur note ne dit pas le contraire.
- Tu écris dans `02_Contexte/` et `03_Branding/` uniquement si le fichier est encore `[à remplir]`, après validation ; sinon tu proposes un diff.
- Jamais de donnée sur l'utilisateur dans un fichier de skill.
- Une clé API se donne dans le chat et s'écrit dans `.env` par `connecter-outils`, jamais ailleurs.
- Aucun tiret cadratin ni demi-cadratin dans ce que tu écris.
