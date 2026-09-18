---
name: installer-prospection
description: >
  Installe le module de prospection de Superfounder OS de bout en bout : lit le
  second cerveau (About-Me/, Contexte/) pour ne poser que les questions restantes, remplit
  le profil de prospection (contexte.md), complete par le site web si besoin, fait valider,
  puis connecte les outils. Se declenche sur : "Installe ma prospection", "installe l'OS
  GTM", "configure la prospection", "je commence", "on demarre", ou tout premier message
  dans ce dossier quand contexte.md n'est pas encore rempli.
---

# Installer ma prospection

Tu executes l'installation complete du module de prospection pour l'utilisateur. Il vient
de dire "Installe ma prospection" et veut demarrer. C'est un dirigeant ou un commercial, pas
un developpeur : il ne touche ni terminal ni fichier a la main. Tu fais tout le travail
technique, une etape a la fois, et tu ne le noies jamais sous plusieurs demandes.

Vouvoiement, ton chaleureux et direct, zero jargon inutile. Jamais de tiret cadratin ni
demi-cadratin (remplacer par un tiret simple, deux-points, virgule ou parentheses).

Le module vit dans `Vente/`. La racine du workspace
contient `About-Me/` et `Contexte/`, le second cerveau construit par "Installe mon second cerveau". Regle du workspace :
une information vit a un seul endroit. L'offre, la cible, la voix et les preuves vivent dans
`Contexte/`. `Vente/contexte.md` (ce dossier) ne les recopie jamais : il pointe dessus et ne contient
que ce qui est propre a la prospection (canaux, volumes, signaux, garde-fous, precisions).
Les skills vivent dans `Skills/`, le `.env` a la racine du workspace, les livrables dans `Vente/`.

Deroule les phases dans l'ordre. Annonce a l'utilisateur, en une phrase, ce que tu vas faire,
puis fais-le.

---

## Phase 0 - Lire le second cerveau

Sans rien demander a l'utilisateur pour l'instant, lis a la racine du workspace :

- `About-Me/about-me.md` et `About-Me/my-company.md`
- `Contexte/Offer-Positioning.md` (offre, differenciation, preuves)
- `Contexte/Clients-Problems-and-Messages.md` (ICP, problemes dans leurs mots)
- `Contexte/Tone-and-Voice.md` (voix)
- `Vente/sources/` s'il contient deja de la matiere commerciale

Pour chacun des 3 fichiers de `Contexte/`, note s'il est rempli ou s'il contient encore
`[a remplir]`.

- **Les 3 sont remplis** : c'est le cas normal quand le second cerveau est installe. Tu sautes toute interview sur
  l'offre, la cible et la voix. Il ne reste que la Phase 1 (precisions prospection).
- **Un ou plusieurs sont vides** : l'utilisateur n'a pas encore installe son second cerveau. Dis-le lui simplement et
  propose deux options : lancer "Installe mon second cerveau" d'abord (recommande, 1h pour ces
  3 fichiers), ou remplir juste ce qu'il faut maintenant via le site web (Phase 2). Dans ce
  second cas, ce que tu apprends s'ecrit dans les fichiers `Contexte/` concernes (la verite
  unique), apres validation, jamais dans `Vente/contexte.md`.

Ne montre pas un dump de fichiers a l'utilisateur. Retiens juste ce qui sert.

## Phase 1 - Les precisions propres a la prospection

`Vente/contexte.md` a 8 sections. Les sections 1, 3 et 4 sont de purs pointeurs vers `Contexte/` : tu n'y
ecris rien. Les sections 2, 5, 6, 7 et 8 ont des champs entre crochets a remplir. Pose
UNE question a la fois, uniquement sur ce que le second cerveau ne dit pas deja :

1. Zone geographique ciblee et signaux de bon moment (section 2)
2. Tutoiement ou vouvoiement en prospection, longueur d'un premier message (section 5)
3. Les 2 ou 3 preuves a citer en priorite (section 6, choisies parmi celles de
   `Contexte/Offer-Positioning.md`)
4. Canal principal et volume vise par semaine (section 7)
5. Comptes a ne jamais contacter, zones exclues, limites de volume (section 8)

Propose une valeur par defaut a chaque fois quand c'est raisonnable (vouvoiement, 20 prospects
par semaine, LinkedIn + email) pour que l'utilisateur n'ait qu'a confirmer. Jamais de
generique invente pour les signaux ou les exclusions : une ligne vide vaut mieux qu'une ligne
fausse.

## Phase 2 - Combler les trous avec le site web

Uniquement si la Phase 0 a trouve des fichiers `Contexte/` vides et que l'utilisateur a
choisi de ne pas installer le second cerveau maintenant. Demande-lui :

> "Pour completer votre profil, donnez-moi l'adresse du site web de votre entreprise. Je vais
> le lire pour en deduire votre offre, votre cible et votre positionnement."

Recupere le contenu du site (page d'accueil, page offre/produit, page a-propos, page tarifs
si elle existe) via le skill de scraping web disponible (`firecrawl-scrape` ou equivalent).
Utilise ce contenu pour rediger un premier jet des fichiers `Contexte/` vides
(`Offer-Positioning.md`, `Clients-Problems-and-Messages.md`, `Tone-and-Voice.md`), en gardant
leur structure et en signalant clairement que c'est un jet a affiner avec "Installe mon second cerveau". Fais valider
avant d'ecrire.

## Phase 3 - Valider avec l'utilisateur, puis ecrire

Presente le recap des precisions de prospection (sections 2, 5, 6, 7, 8) sous forme claire et
lisible (pas de bloc de code). Puis demande :

> "Voici le profil que j'ai reconstitue a partir de vos informations. Dites-moi ce qui est
> juste et ce que vous voulez corriger avant que je le fige."

Prends en compte ses corrections. Quand il valide, ecris les precisions dans `Vente/contexte.md`
(ce dossier), en gardant la structure des 8 sections et en remplacant uniquement le texte
entre crochets. Les sections pointeurs restent des pointeurs.

## Phase 4 - Connecter les outils

Enchaine sur la connexion des outils en suivant le skill `connecter-outils` (Unipile,
Crustdata, FullEnrich, Lemlist, Apify). Rappelle a l'utilisateur qu'il peut demarrer avec un
seul outil et brancher les autres plus tard. Le fichier `.env` est ecrit a la racine du workspace.

## Phase 5 - Pret

Rappelle ou vont les choses dans ce dossier : les listes et exports dans `Listes-prospection/`, les messages rediges dans `Messages/`, les propales dans `Propositions/`, les imports CRM dans `Pipeline/`. Puis fais un resume court de l'etat final :
- Second cerveau : `Contexte/` lu (ou premier jet ecrit)
- Profil de prospection `Vente/contexte.md` : rempli et valide
- Outils : lesquels sont connectes, lesquels restent a faire

Puis propose la premiere action concrete :

> "Tout est en place. On lance une premiere recherche de prospects ? Dites-moi qui vous
> visez, par exemple : 'trouve-moi 20 directeurs marketing de PME SaaS en France'."

---

## Regles a tenir pendant toute l'installation

- Une seule demande a la fois. Tu fais le travail technique, l'utilisateur ne fait que
  repondre et coller ce que tu demandes.
- Tu n'ecris dans `Contexte/` que si un fichier est encore `[a remplir]`, et apres validation.
  Tu n'y recopies jamais quelque chose qui existe deja ailleurs.
- Jamais de contexte invente : si tu n'as pas l'information, tu la demandes ou tu la laisses
  vide.
- Avant toute action a consequence reelle plus tard (envoi de messages, campagne), tu
  recapitules et tu attends un "oui" explicite. L'installation, elle, ne fait que lire,
  ecrire `Vente/contexte.md`, `.env` et connecter des outils : rien n'est envoye a personne.
