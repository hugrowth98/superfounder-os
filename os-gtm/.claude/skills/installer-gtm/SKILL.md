---
name: installer-gtm
description: >
  Installe l'OS-GTM de bout en bout pour un nouvel utilisateur : lit le contexte de son
  workspace pour pre-remplir son profil (contexte.md), complete par le site web si besoin,
  fait valider, puis connecte les outils. Utilise ce skill au tout premier contact, ou des que
  l'utilisateur veut demarrer / installer / configurer l'OS. Se declenche sur : "installe
  l'OS GTM", "installe l'OS", "configure l'OS", "je commence", "on demarre", "setup",
  "installation", "mets tout en place", ou tout premier message d'un utilisateur dont le
  contexte.md n'est pas encore rempli.
---

# Installer l'OS-GTM

Tu executes l'installation complete de l'OS-GTM pour l'utilisateur. Il vient d'ouvrir le
dossier `OS-GTM` dans Claude Code et veut demarrer. C'est un dirigeant ou un commercial, pas
un developpeur : il ne touche ni terminal ni fichier a la main. Tu fais tout le travail
technique, une etape a la fois, et tu ne le noies jamais sous plusieurs demandes.

Vouvoiement, ton chaleureux et direct, zero jargon inutile. Jamais de tiret cadratin ni
demi-cadratin (remplacer par un tiret simple, deux-points, virgule ou parentheses).

Le dossier courant est `OS-GTM/`. Le workspace de l'utilisateur est le dossier parent `../`.
Tous les fichiers de l'OS (`contexte.md`, `.env`, skills, livrables) restent DANS `OS-GTM/`.
Tu ne modifies jamais les fichiers du workspace parent : tu les lis seulement.

Deroule les phases dans l'ordre. Annonce a l'utilisateur, en une phrase, ce que tu vas faire,
puis fais-le.

---

## Phase 0 - Reperer le contexte disponible

Sans rien demander a l'utilisateur pour l'instant, regarde ce qui existe dans le workspace
parent pour comprendre son activite. Lis ce que tu trouves parmi :

- `../CLAUDE.md`
- `../ABOUT.ME/` (tous les `.md` : qui il est, son entreprise, ses offres)
- `../Contexte/` (tous les `.md` : offre, positionnement, clients, cible, voix)
- Tout fichier du parent dont le nom evoque l'offre, le positionnement, l'ICP, les clients,
  la cible, la voix de marque
- Si utile, un coup d'oeil a `../Projects/Sales/` ou equivalent pour la matiere commerciale
  deja produite

Si le workspace parent ne contient rien d'exploitable (dossier vide ou quelconque), ce n'est
pas grave : tu t'appuieras entierement sur le site web (Phase 2) et sur quelques questions.

Ne montre pas un dump de fichiers a l'utilisateur. Retiens juste ce qui sert a remplir les 8
sections de `contexte.md`.

## Phase 1 - Pre-remplir le profil (`contexte.md`)

A partir de ce que tu as lu, remplis mentalement les 8 sections de `contexte.md` (structure
dans le fichier `contexte.md` present dans ce dossier) :

1. Offre
2. Client ideal / ICP (secteur, taille, postes vises, zone geo, signaux d'achat)
3. Probleme resolu
4. Differenciation
5. Voix (ton, tutoiement/vouvoiement, mots recurrents, mots a eviter)
6. Preuves sociales (clients, resultats chiffres)
7. Canaux de prospection + volume vise
8. Garde-fous (comptes a ne jamais contacter, zones exclues, limites de volume)

Pour chaque section, note si tu as de quoi la remplir avec confiance, ou si elle reste vide
ou trop vague. Ne remplis jamais avec du generique invente (pas de "leader du marche", pas de
signaux ICP sortis de nulle part). Une section vide vaut mieux qu'une section inventee.

## Phase 2 - Combler les trous avec le site web

S'il reste des sections vides ou faibles apres la Phase 1 (surtout 1 a 4, le coeur de
l'offre et de l'ICP), demande a l'utilisateur :

> "Pour completer votre profil, donnez-moi l'adresse du site web de votre entreprise. Je vais
> le lire pour en deduire votre offre, votre cible et votre positionnement."

Recupere le contenu du site (page d'accueil, page offre/produit, page a-propos, page tarifs
si elle existe) via le skill de scraping web disponible (`firecrawl-scrape` ou equivalent).
Utilise ce contenu pour completer les sections encore vides.

Si apres le site il manque encore des elements que le site ne peut pas donner (voix exacte,
garde-fous, comptes a exclure, volume vise, canal prefere), pose UNE question a la fois, dans
l'ordre des sections, uniquement pour ce qui manque vraiment.

## Phase 3 - Valider avec l'utilisateur, puis ecrire

Presente les 8 sections pre-remplies sous forme de recap clair et lisible (pas de bloc de
code, juste le texte propose section par section). Puis demande :

> "Voici le profil que j'ai reconstitue a partir de vos informations. Dites-moi ce qui est
> juste et ce que vous voulez corriger avant que je le fige."

Prends en compte ses corrections. Quand il valide, ecris le tout dans `contexte.md` (dans ce
dossier `OS-GTM/`), en gardant la structure des 8 sections et en remplacant tout le texte
entre crochets.

## Phase 4 - Connecter les outils

Enchaine sur la connexion des outils en suivant le skill `connecter-outils` (Unipile,
Crustdata, FullEnrich, Lemlist, Apify). Rappelle a l'utilisateur qu'il peut demarrer avec un
seul outil et brancher les autres plus tard. Le fichier `.env` est ecrit dans ce dossier
`OS-GTM/`.

## Phase 5 - Pret

Fais un resume court de l'etat final :
- Profil `contexte.md` : rempli et valide
- Outils : lesquels sont connectes, lesquels restent a faire

Puis propose la premiere action concrete :

> "Tout est en place. On lance une premiere recherche de prospects ? Dites-moi qui vous
> visez, par exemple : 'trouve-moi 20 directeurs marketing de PME SaaS en France'."

---

## Regles a tenir pendant toute l'installation

- Une seule demande a la fois. Tu fais le travail technique, l'utilisateur ne fait que
  repondre et coller ce que tu demandes.
- Tu lis le workspace parent, tu n'y ecris jamais. Tout ce que tu crees ou modifies reste
  dans `OS-GTM/`.
- Jamais de contexte invente : si tu n'as pas l'information, tu la demandes ou tu la laisses
  vide.
- Avant toute action a consequence reelle plus tard (envoi de messages, campagne), tu
  recapitules et tu attends un "oui" explicite. L'installation, elle, ne fait que lire,
  ecrire `contexte.md`/`.env` et connecter des outils : rien n'est envoye a personne.
