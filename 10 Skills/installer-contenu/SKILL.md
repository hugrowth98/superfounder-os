---
name: installer-contenu
description: >
  Installe la machine de contenu LinkedIn de Superfounder OS : lit le second cerveau
  (02 Contexte/) pour ne rien redemander sur l'offre, la cible et la voix, puis construit avec
  l'utilisateur les trois fichiers de 05 Departements/Contenu/LinkedIn/ (strategie-contenu.md,
  posts-de-reference.md, swipe-file.md) que les 9 autres skills de contenu lisent à chaque
  exécution. Se déclenche sur "Installe mon contenu", "personnalise mon système LinkedIn",
  "configure mon contenu", "setup LinkedIn", "remplir ma stratégie de contenu", ou tout
  premier message dans ce dossier quand strategie-contenu.md contient encore [à remplir].
---

# Installer mon contenu

Tu installes la machine de contenu pour l'utilisateur. Il vient de dire "Installe mon contenu"
et veut que les skills écrivent dans sa voix. Vouvoiement, une question à la fois, jamais de
tiret cadratin.

Le principe : aucun skill de contenu ne contient de donnée sur l'utilisateur. Ils lisent le
contexte à chaque exécution. Ton travail est donc d'écrire les bons fichiers au bon endroit,
une seule fois chacun :

| Information | Où elle vit | Qui l'écrit |
|---|---|---|
| Offre, différenciation, preuves | `02 Contexte/Offer-Positioning.md` | le second cerveau |
| Clients, problèmes, mots exacts | `02 Contexte/Clients-Problems-and-Messages.md` | le second cerveau |
| Voix, marqueurs de style, ce qu'il ne dit jamais | `02 Contexte/Tone-and-Voice.md` | le second cerveau (ou ce skill si vide) |
| Piliers, répartition, convictions, sources, créateurs admirés | `05 Departements/Contenu/LinkedIn/strategie-contenu.md` | ce skill |
| Ses meilleurs posts | `05 Departements/Contenu/LinkedIn/posts-de-reference.md` | ce skill |
| Posts des autres qui l'inspirent | `05 Departements/Contenu/LinkedIn/swipe-file.md` | ce skill, puis au fil de l'eau |

**Règle d'or : n'invente jamais le positionnement, les convictions ou le ton.** Déduis depuis
ses posts, ou demande. Présente toujours ta proposition et fais valider avant d'écrire.

---

## Phase 0 - Lire le second cerveau

Sans rien demander, lis à la racine du workspace : `02 Contexte/Offer-Positioning.md`,
`02 Contexte/Clients-Problems-and-Messages.md`, `02 Contexte/Tone-and-Voice.md`. Note lesquels
contiennent encore `[à remplir]`.

- **Les trois sont remplis** : cas normal. Tu ne poses aucune question sur l'offre, la cible
  ou la voix. Il reste la Phase 1 (les posts) et la Phase 2 (la stratégie).
- **`Tone-and-Voice.md` est vide** : tu le construiras à la Phase 1 à partir de ses posts,
  c'est la meilleure source possible. Après validation, tu l'écris dans `02 Contexte/` (la
  vérité unique), jamais dans `ressources/`.
- **Offre ou clients vides** : dis-le simplement et propose de lancer "Installe mon second
  cerveau" d'abord, ou de continuer avec ce que ses posts révèlent (moins précis).

## Phase 1 - Les posts de référence (mode Express)

Demande à l'utilisateur de coller 5 à 10 de ses meilleurs posts LinkedIn, idéalement de types
différents, avec leurs résultats s'il les connaît. S'il n'en a pas encore, passe en mode
Manuel (Phase 2 avec quelques questions de plus sur le ton) et note dans
`posts-de-reference.md` qu'il est à alimenter.

À partir des posts :
1. Range-les par type dans `05 Departements/Contenu/LinkedIn/posts-de-reference.md` (Educational,
   Storytelling, Hot take, Lead magnet, Autres), avec pour chacun une ligne "Ce qui marche".
2. Déduis la synthèse de fin de fichier : marqueurs visuels, structure typique, longueurs,
   sujets à éviter.
3. Si `02 Contexte/Tone-and-Voice.md` était vide : déduis le ton, les marqueurs de style, le
   vocabulaire, ce qu'il ne dirait jamais, la langue. Présente, fais valider, écris.

Garde ses mots, ses tics, ses formulations. Ton job est de capturer sa voix, pas de la
réécrire.

## Phase 2 - La stratégie de contenu

Remplis `05 Departements/Contenu/LinkedIn/strategie-contenu.md` section par section. Déduis un
maximum des posts et de `02 Contexte/`, puis pose UNE question à la fois sur ce qui manque, en
proposant une valeur par défaut quand c'est raisonnable :

1. Niche en une formule, posture LinkedIn
2. Monopole personnel : curiosité, compétence, personnalité
3. IAP (l'audience large, au-delà des clients)
4. Les 3 piliers et leur part
5. Fréquence de publication, répartition 4A, mix autorité / perso / offre (proposer les défauts)
6. 5 à 8 convictions, la première étant la conviction-phare
7. Sujets d'opinion par thème
8. 3 à 5 créateurs admirés et ce qu'il prend de chacun
9. Sources de veille (YouTube, newsletters, autres) et ressources sauvegardées

Les sources de veille et ressources peuvent rester "à compléter" : ne bloque pas
l'installation pour ça.

## Phase 3 - Le swipe file

Explique en deux phrases à quoi sert `swipe-file.md` (structures et hooks des autres, jamais
leurs mots). S'il a sous la main des posts qu'il admire, colle-les avec une ligne d'analyse.
Sinon, laisse le gabarit et dis-lui de l'alimenter chaque fois qu'un post l'arrête.

## Phase 4 - Validation et écriture

Présente un récapitulatif lisible (pas de bloc de code) : positionnement, ton, piliers,
convictions. Demande :

> "Je valide et j'écris, ou vous voulez ajuster quelque chose ?"

Quand il valide, écris les fichiers. Vérifie qu'aucun `[à remplir]` ne subsiste dans les
sections obligatoires (Positionnement, Monopole, Piliers, Répartition, Convictions).

## Phase 5 - Premier post

Confirme que la machine est installée et propose de la tester tout de suite :

> "Tout est en place. On écrit un premier post ? Dites-moi une idée, ou tapez 'idées de
> posts' pour que je lance la veille."

Rappelle-lui que plus il ajoute de posts dans `posts-de-reference.md`, plus la voix sera
juste, et qu'il peut relancer cet installeur quand son positionnement bouge.

---

## Règles

- Une seule question à la fois.
- Tu écris dans `02 Contexte/` uniquement si le fichier est encore `[à remplir]`, après validation.
- Jamais de donnée sur l'utilisateur dans un fichier de skill. Tout va dans `02 Contexte/` ou `ressources/`.
- Aucun tiret cadratin ni demi-cadratin dans ce que tu écris.
