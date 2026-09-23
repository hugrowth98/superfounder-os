---
name: installer-contenu
description: >
  Installe la machine de contenu LinkedIn de Superfounder OS en huit phases : lit le second
  cerveau (02_Contexte/) pour ne rien redemander sur l'offre, la cible et la voix, puis
  construit avec l'utilisateur la voix et le style, les posts de référence et leurs chiffres,
  la stratégie de contenu (niche, piliers, répartition, convictions, objectif, cadence,
  formats), le swipe file, le système de veille (sources-veille.json et premier run), la
  charte visuelle, le profil LinkedIn, et finit par un premier brief. Se déclenche sur
  "Installe mon contenu", "personnalise mon système LinkedIn", "configure mon contenu",
  "setup LinkedIn", "remplir ma stratégie de contenu", "ajoute mes sources de veille", ou
  tout premier message dans ce dossier quand strategie-contenu.md contient encore [à remplir].
---

# Installer mon contenu

Tu installes la machine de contenu pour l'utilisateur. Il vient de dire "Installe mon contenu"
et veut que le master `linkedin` et le master `infographie` écrivent dans sa voix, avec sa
stratégie, ses sources et sa charte. Vouvoiement, une question à la fois, une valeur par défaut
à chaque fois que c'est raisonnable, jamais de tiret cadratin. Comptez 45 minutes à 1h30, en
plusieurs fois si l'utilisateur le veut : chaque phase se termine par une écriture validée, on
peut reprendre à la suivante.

Le principe : aucun skill de contenu ne contient de donnée sur l'utilisateur. Ils lisent le
contexte à chaque exécution. Ton travail est d'écrire les bons fichiers au bon endroit, une
seule fois chacun :

| Information | Où elle vit | Qui l'écrit |
|---|---|---|
| Offre, différenciation, preuves | `02_Contexte/Offer-Positioning.md` | le second cerveau |
| Clients, problèmes, mots exacts | `02_Contexte/Clients-Problems-and-Messages.md` | le second cerveau |
| Voix, marqueurs de style, ce qu'il ne dit jamais | `02_Contexte/Tone-and-Voice.md` | le second cerveau (ou ce skill si vide) |
| Niche, monopole, piliers, répartition, convictions, objectif, cadence, formats, fins de post | `05_Departements/Marketing/LinkedIn/strategie-contenu.md` | ce skill |
| Ses meilleurs posts, avec leurs chiffres et ce qui marche chez lui | `05_Departements/Marketing/LinkedIn/posts-de-reference.md` | ce skill, puis le sous-skill `performance` |
| Posts des autres qui l'inspirent | `05_Departements/Marketing/LinkedIn/swipe-file.md` | ce skill, puis au fil de l'eau |
| Newsletters et chaînes YouTube à lire chaque semaine | `05_Departements/Marketing/LinkedIn/sources-veille.json` | ce skill (phase 5), puis l'utilisateur |
| Couleurs, typographies, logo, interdits | `03_Branding/charte-visuelle.md` | ce skill (phase 6), sur un oui explicite |
| Clé Publora, si l'utilisateur programme depuis le chat | `.env` (`PUBLORA_API_KEY`) | `connecter-outils` |

**Règle d'or : n'invente jamais le positionnement, les convictions, le ton ni les sources.**
Déduis depuis ses posts, ou demande. Présente toujours ta proposition et fais valider avant
d'écrire.

---

## Phase 0 : lire ce qui existe déjà

Sans rien demander, lis : `02_Contexte/Offer-Positioning.md`, `02_Contexte/Clients-Problems-and-Messages.md`,
`02_Contexte/Tone-and-Voice.md`, puis les quatre fichiers de `05_Departements/Marketing/LinkedIn/`
et `03_Branding/charte-visuelle.md`. Note lesquels contiennent encore `[à remplir]` ou des listes vides.

- **Le second cerveau est rempli** : cas normal, aucune question sur l'offre, la cible ou la voix.
- **`Tone-and-Voice.md` est vide** : tu le construiras à la phase 1 depuis ses posts, la meilleure source possible, et tu l'écriras dans `02_Contexte/` après validation (la vérité unique).
- **Offre ou clients vides** : dis-le, propose "Installe mon second cerveau" d'abord, ou de continuer avec ce que ses posts révèlent (moins précis).
- **Une partie est déjà faite** (reprise de session) : annonce en une ligne où on en est et reprends à la première phase incomplète.

## Phase 1 : la voix et le style

Demande 5 à 10 de ses meilleurs posts LinkedIn, de types différents, avec leurs chiffres s'il les a (impressions, réactions, commentaires). S'il n'en a pas encore, passe en mode manuel : trois questions sur le ton (comment il parle à un client au téléphone, ce qu'il ne dirait jamais, tutoiement ou vouvoiement), et note que `posts-de-reference.md` est à alimenter.

Depuis les posts : le ton, les marqueurs de style (symboles, longueur des phrases, ouvertures, façon de finir), le vocabulaire, ce qu'il ne dit jamais, la langue, et ses expressions à lui pour la section 7 d'`01_About-Me/anti-ai-voice.md`. Si `Tone-and-Voice.md` était vide : présente, fais valider, écris. Sinon : signale seulement ce que les posts contredisent, et propose un diff.

Garde ses mots, ses tics, ses formulations. Ton travail est de capturer sa voix, pas de la réécrire.

## Phase 2 : les posts de référence et leurs chiffres

1. Range les posts par type dans `posts-de-reference.md` (éducatif, storytelling, opinion, lead magnet, autres), avec pour chacun une ligne "ce qui marche" et ses chiffres.
2. Déduis la synthèse de fin de fichier : marqueurs visuels, structure typique, longueurs, sujets à éviter.
3. S'il a donné des chiffres pour 10 posts ou plus : applique la méthode des tiers du sous-skill `performance` (`10_Skills/linkedin/ressources/analyse-performance.md`) et écris une section "Ce qui marche chez vous" (3 à 5 enseignements avec les posts qui les prouvent). Sinon, laisse la section avec un rappel : "à remplir après 20 posts, avec le sous-skill performance".

## Phase 3 : la stratégie de contenu

Une question à la fois, dans cet ordre, avec une valeur par défaut déduite de `02_Contexte/` et des posts :

1. **Niche** en une formule courte, et **posture** (expert, bâtisseur, pédagogue...).
2. **Monopole personnel** : curiosité, compétence, personnalité (3 à 5 territoires).
3. **IAP**, l'audience large qui le suit sans être cliente (l'ICP est déjà dans `02_Contexte/`).
4. **Piliers** : 3 thèmes avec leur part (proposer une répartition depuis les posts qui ont marché).
5. **Répartition** : fréquence, 4A (défaut 30/20/30/20), autorité / perso / offre (défaut 70/15/15), funnel (40/40/20, un lead magnet par semaine au plus).
6. **Convictions** : 5 à 8 phrases qu'il dirait même si 30 pour cent des gens ne sont pas d'accord, la première en conviction-phare ; puis les **sujets d'opinion** par thème.
7. **Objectif et cadence** : l'objectif principal (audience, leads, autorité, recrutement : un seul en premier), ce qu'un bon mois donne, les créneaux (défaut : mardi, mercredi, jeudi 8h, heure locale), le créneau d'écriture en lot, la programmation (native, ou Publora).
8. **Formats et fins de post** : les formats par défaut (texte, carrousel, infographie, vidéo), la fin de post par défaut, une signature ou un PS récurrent s'il en a.
9. **Créateurs admirés** : 3 à 5, et ce qu'il prend de chacun (technique, angle, format, jamais les mots).
10. **Ressources sauvegardées** et **autres sources** sans flux (X, Reddit, podcasts, communautés, comptes LinkedIn à surveiller). Peuvent rester "à compléter" : ne bloque pas.

## Phase 4 : le swipe file

Explique en deux phrases à quoi sert `swipe-file.md` (structures et hooks des autres, jamais leurs mots). S'il a sous la main des posts qu'il admire, colle-les avec une ligne d'analyse. Sinon, laisse le gabarit et dis-lui de l'alimenter chaque fois qu'un post l'arrête.

## Phase 5 : le système de veille

C'est le sous-skill `veille` du master `linkedin` qui lira ces sources chaque semaine. Trois questions :

1. **Les newsletters** qu'il lit vraiment (3 à 10) : pour chacune, le nom et l'URL du flux RSS (Substack : `https://<nom>.substack.com/feed`, même avec un domaine personnalisé ; un blog : son flux `/feed`, `/rss` ou `/feed.xml`). Range-les par thème avec un tier (1 = chaque semaine).
2. **Les chaînes YouTube** (3 à 10) : l'identifiant `@handle` de chacune, par tier.
3. **Les autres flux** RSS ou Atom, s'il en a.

Écris `05_Departements/Marketing/LinkedIn/sources-veille.json` (le gabarit livré contient un bloc `_exemple`, la structure exacte est dans le sous-skill `veille`). Puis le premier run, pour vérifier que tout se lit :

```bash
python3 10_Skills/linkedin/scripts/abonnes.py --force
python3 10_Skills/linkedin/scripts/veille.py --jours 14 --tier tous --sans-transcripts --format md --stdout
```

Corrige les flux en erreur (URL, handle). Propose ensuite les transcripts YouTube, qui rendent le brief bien plus riche : `pip3 install youtube-transcript-api` (une commande, gratuite) ; sans elle, le script tourne sans transcripts et le dit. Termine en donnant la phrase du lundi : "fais ma veille".

Une quatrième question, facultative : **les comptes LinkedIn** dont il veut voir les posts qui performent (concurrents, créateurs de sa niche, 5 à 50 URLs de profil). S'il en donne, écris `05_Departements/Marketing/LinkedIn/comptes-veille.json` (format dans le sous-skill `veille-createurs`) et donne la phrase du mois : "fais la veille créateurs". Sans réponse, rien à écrire : le sous-skill demandera les comptes au premier run.

## Phase 6 : la charte visuelle

`03_Branding/` est une zone protégée : tu n'y écris que sur un oui explicite. Demande ses couleurs (fond, texte, un accent) et sa police, ou l'URL de son site pour les lire, et s'il a un logo dans `03_Branding/`. Écris `03_Branding/charte-visuelle.md` (palette par rôle, typographies, interdits, logo) et coche la case dans `03_Branding/Branding.md`. S'il ne sait pas : laisse `[à remplir]`, le master `infographie` partira sur un style neutre et le dira. Cette phase se saute en une phrase.

## Phase 7 : le profil LinkedIn

Propose de passer le profil au sous-skill `profil` du master `linkedin` : il colle son titre et sa section à propos, tu rends un diagnostic en cinq lignes, trois titres et une section à propos réécrite depuis `Offer-Positioning.md`. Si Publora est branché ou s'il veut programmer depuis le chat, c'est le moment de lancer `connecter-outils` pour la clé (`PUBLORA_API_KEY`, test gratuit) et d'écrire "Publora" dans la ligne Programmation de `strategie-contenu.md`. Cette phase se saute aussi en une phrase.

## Phase 8 : validation et premier brief

Présente un récapitulatif lisible (pas de bloc de code) : positionnement, ton, piliers, convictions, cadence, sources. Demande :

> "Je valide et j'écris, ou vous voulez ajuster quelque chose ?"

Quand il valide, écris les fichiers. Vérifie qu'aucun `[à remplir]` ne subsiste dans les sections obligatoires de `strategie-contenu.md` (Positionnement, Monopole, Piliers, Répartition, Convictions, Objectif et cadence). Puis :

> "Tout est en place. On lance la première veille ("fais ma veille"), ou on écrit un premier post ? Dites-moi une idée, ou "interviewe-moi" si vous partez de votre vécu."

Rappelle-lui que plus il ajoute de posts dans `posts-de-reference.md`, plus la voix sera juste, qu'une source s'ajoute en une ligne dans `sources-veille.json`, et qu'il peut relancer cet installeur quand son positionnement bouge.

---

## Règles

- Une seule question à la fois, une valeur par défaut chaque fois que c'est raisonnable.
- Tu écris dans `02_Contexte/` et `03_Branding/` uniquement si le fichier est encore `[à remplir]`, après validation ; sinon tu proposes un diff.
- Jamais de donnée sur l'utilisateur dans un fichier de skill. Tout va dans `02_Contexte/`, `03_Branding/` ou `05_Departements/Marketing/LinkedIn/`.
- Une clé API se donne dans le chat et s'écrit dans `.env` par `connecter-outils`, jamais ailleurs.
- Aucun tiret cadratin ni demi-cadratin dans ce que tu écris.
