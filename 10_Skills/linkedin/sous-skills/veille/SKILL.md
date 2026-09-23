---
name: veille
description: >
  La veille hebdomadaire : lit les newsletters et les chaînes YouTube que l'utilisateur suit
  (flux RSS, transcripts automatiques), calcule un score de vélocité par article (engagement
  pour 1 000 abonnés par jour), puis produit un brief éditorial en 6 sections (sujet le plus
  discuté, top 10 par engagement, lancement de la semaine, 10 idées de posts, 10 idées de
  newsletter, 10 idées de lead magnet), chaque idée ancrée sur une source précise. Se déclenche
  sur : "veille", "fais ma veille", "scanne mes sources", "qu'est-ce qui buzz", "tendances de
  la semaine", "brief de veille", "dernières newsletters", "dernières vidéos", "idées de
  contenu cette semaine". Pour rédiger un post à partir d'une idée du brief, enchaîner avec
  `educatif`, `storytelling`, `opinion` ou `lead-magnet`. Ne pas utiliser pour une idée qui
  vient du vécu de l'utilisateur (`interview`) ni sans source scrapée (`ideation`).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les scripts sont dans `{SKILL_BASE}/scripts/`. Le master a déjà chargé le socle d'écriture.

# Veille : le brief éditorial de la semaine

Le script lit les sources, Claude fait le travail éditorial. Rien dans le brief ne vient d'ailleurs que des sources lues cette semaine.

## Les fichiers de l'utilisateur

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| `05_Departements/Marketing/LinkedIn/sources-veille.json` | les newsletters (flux RSS, par thème et par tier), les chaînes YouTube (par tier), les autres flux | `installer-contenu` (phase 5), puis l'utilisateur au fil de l'eau |
| `05_Departements/Marketing/LinkedIn/sources/veille-abonnes.json` | le cache des abonnés par source, rafraîchi tous les 30 jours | `abonnes.py` |
| `05_Departements/Marketing/LinkedIn/sources/veille-chaines.json` | le cache des identifiants de chaînes YouTube | `veille.py` |
| `05_Departements/Marketing/LinkedIn/sources/veille_AAAA-MM-JJ.json` | le dump brut de la semaine (articles, vidéos, transcripts, scores) | `veille.py` |
| `05_Departements/Marketing/LinkedIn/Brief-veille_AAAA-MM-JJ.md` | le brief en 6 sections | Claude, après validation |

Les sources sans flux (Product Hunt, comptes X, communautés) sont listées dans `strategie-contenu.md`, section Sources de veille : le script ne les lit pas ; à l'étape 3, si l'utilisateur le demande, consultez-les avec WebSearch ou Firecrawl et marquez ces lignes du brief "vu à la main". Les comptes LinkedIn de personnes à surveiller relèvent du sous-skill `veille-createurs` (posts qui ont performé, quatre catégories, visuels) ; une page entreprise LinkedIn (la vôtre ou un concurrent) se lit avec `publications-entreprise` (Unipile).

Si `sources-veille.json` est vide ou absent : proposez d'ajouter des sources maintenant (une newsletter et une chaîne suffisent pour un premier run) ou de lancer "Installe mon contenu". Une source s'ajoute en éditant le JSON : un flux RSS (`https://<nom>.substack.com/feed`, ou le flux de n'importe quel blog) ou un identifiant de chaîne YouTube (`@handle`).

## Le pipeline

### 1. Les abonnés, une fois par mois

```bash
python3 {SKILL_BASE}/scripts/abonnes.py
```

Le script lit le nombre d'abonnés de chaque newsletter et de chaque chaîne, pour calculer la vélocité. Il ne refait rien si le cache a moins de 30 jours ; `--force` pour rafraîchir.

### 2. La veille de la semaine

```bash
python3 {SKILL_BASE}/scripts/veille.py --jours 7 --source toutes --tier 1 --contenu-complet
```

Sous le capot : lecture parallèle des flux RSS des newsletters, lecture de la page d'archive de chaque newsletter pour récupérer les likes, commentaires et partages par article ; lecture des flux Atom des chaînes YouTube ; transcripts des vidéos si la bibliothèque `youtube-transcript-api` est installée (sinon le script le dit et continue sans) ; vélocité par item : `(likes ou vues / abonnés x 1 000) / max(0,5, âge en jours)`, soit l'engagement par jour pour 1 000 abonnés ; détection des articles tronqués par un paywall. Le résultat est écrit dans `sources/veille_AAAA-MM-JJ.json`, le chemin s'affiche.

| Option | Effet |
|---|---|
| `--jours 7` | fenêtre de fraîcheur (défaut 7) |
| `--source newsletters` / `youtube` / `toutes` | ce qu'on lit |
| `--tier 1` / `2` / `3` / `tous` | priorité des chaînes YouTube (défaut 1) |
| `--sans-transcripts` | mode rapide, sans transcripts |
| `--contenu-complet` | le texte intégral (sinon un extrait de 1 500 caractères) |
| `--format md` | un digest markdown lisible au lieu du JSON, trié par vélocité |
| `--out chemin.json` | écrire ailleurs que dans `sources/` |
| `--stdout` | écrire sur la sortie standard au lieu d'un fichier |

Le script n'appelle aucune API payante : seulement les flux publics et les pages publiques des sources.

### 3. Le brief, par Claude

Lisez le JSON, croisez avec `strategie-contenu.md` (piliers, répartition, convictions) et `Tone-and-Voice.md`, puis rédigez le brief. Vous ne recopiez pas le JSON : vous sélectionnez, vous notez, vous mettez en forme dans la voix de l'utilisateur.

## Le format du brief (6 sections, figé)

**1. Le sujet le plus discuté.** Les 5 sujets de la semaine classés par nombre de sources distinctes qui en parlent. Colonnes : sujet (le thème en une phrase), description (pourquoi tout le monde en parle, 1 à 2 phrases), solution (ce que les sources proposent : frameworks, étapes, citations, dépôts, chiffres, pour se l'approprier), auteurs de référence (1 à 3), URL.

**2. Le top 10 des contenus qui font du bruit.** Classés par vélocité pondérée par la pertinence pour l'utilisateur (50 likes sur 5 000 abonnés valent plus que 500 sur 500 000). Colonnes : description (l'article en 1 à 2 phrases, plus likes, commentaires, vélocité), solution (le contenu appropriable : frameworks, listes, citations, données), auteur et URL.

**3. Le lancement de la semaine.** 3 à 5 lignes au plus sur une nouveauté (outil, modèle, fonctionnalité) ; section vide s'il n'y en a pas. Colonnes : source, description, ce que la source démontre (cas d'usage, étapes, prompts) ; une vidéo sans transcript est marquée.

**4. Dix idées de posts LinkedIn.** Strictement issues des sources. Colonnes : description (l'idée formulée comme un hook appropriable, pas "vous reprenez X sur Y"), format et pilier (angle 4A, pilier de `strategie-contenu.md`, format de publication : liste, carrousel, opinion, storytelling, live), solution (la matière de la source), source et URL. Le mix suit la répartition des piliers de `strategie-contenu.md` et varie les angles 4A.

**5. Dix idées de newsletter.** Même logique, format long (1 500 à 2 000 mots). Une source riche peut donner plusieurs angles (une vidéo avec 5 outils : un post liste et une newsletter de fond).

**6. Dix idées de lead magnet.** Même logique ; pour chacune, la nature de la ressource (PDF, checklist, quiz, dépôt, script, modèle) et la mécanique d'acquisition (mot-clé en commentaire, formulaire, newsletter).

## Les règles de production

1. **Zéro source hors de la veille.** Chaque idée cite une source présente dans le JSON de la semaine. Une idée qui vient du vécu ou de l'actualité de l'utilisateur relève d'`interview` ou d'`ideation`, pas de ce brief.
2. **La description est une idée appropriée, pas un commentaire.** Mauvais : "Vous reprenez X sur les 17 skills". Bon : "Comment 17 skills tournent à la place d'un assistant à 1 500 euros par mois".
3. **La solution est un dump substantiel de la source** : frameworks complets, listes, citations, étapes, chiffres. Pas de teaser, pas d'angle : de la matière à s'approprier.
4. **Une source riche donne plusieurs idées.** Une vidéo avec 5 outils peut nourrir 5 posts, une newsletter et un lead magnet.
5. **Légende d'honnêteté sur chaque ligne de solution** : vu en intégralité et repris fidèlement ; extrait seulement, l'essentiel est là ; vu par le titre ou le résumé, ou vidéo sans transcript : à lire avant de publier.
6. **La voix de l'utilisateur** : vouvoiement, phrases courtes, opinion tranchée, aucun tiret cadratin, aucune négation contrastive, aucun mot de la liste noire d'`anti-ai-voice.md`.

## Cadence

| Quand | Commande | Durée | Usage |
|---|---|---|---|
| Lundi matin | `--jours 7 --source toutes --tier 1 --contenu-complet` | 10 à 30 secondes | le brief de la semaine |
| Pressé | `--jours 7 --source toutes --tier 1 --sans-transcripts` | quelques secondes | moins riche, plus vite |
| Newsletters seulement | `--jours 7 --source newsletters` | quelques secondes | lecture papier-crayon |
| Une fois par mois | `--jours 30 --source toutes --tier tous --contenu-complet` | environ une minute | tendances longues, revue large |

## Où va le brief

Par défaut, en chat. S'il doit servir plus tard : `05_Departements/Marketing/LinkedIn/Brief-veille_AAAA-MM-JJ.md`, avec le frontmatter de `08_Ressources/templates/livrable.md`, sur un oui de l'utilisateur. Le dump JSON reste dans `sources/`. Quand l'utilisateur choisit une idée ("le post numéro 3"), passez l'idée et sa solution (la matière source) au sous-skill du type ; le sous-skill `ideation` peut aussi partir de ce brief pour bâtir le calendrier.

## Exemples

- "Fais ma veille" un lundi : `abonnes.py` (silencieux si le cache est frais), `veille.py --jours 7 --source toutes --tier 1 --contenu-complet`, puis le brief en 6 sections dans le chat ; réponse attendue : le brief, avec le nombre de sources lues et les erreurs éventuelles (flux injoignable, vidéo sans transcript).
- "Juste les newsletters, vite" : `--source newsletters`, brief réduit aux sections 1, 2 et 4 ; réponse attendue : dix idées de posts ancrées.
- "Ajoute la chaîne @exemple et la newsletter de Untel" : édition de `sources-veille.json` (tier proposé), puis `abonnes.py --force` pour la nouvelle source ; réponse attendue : le JSON mis à jour et la ligne ajoutée.
