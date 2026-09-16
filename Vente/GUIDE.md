# GUIDE.md - Le module de prospection

Bonne nouvelle : vous n'avez presque rien a faire pour installer. Une seule commande met tout
en place. Ce document est la comme aide-memoire, ou si vous preferez voir le parcours a
l'avance.

A la fin, vous aurez : une liste de prospects cibles, tries, enrichis, avec des messages
ecrits dans votre voix, envoyes en campagne, avec un suivi des reponses.

---

## Installation en une commande

1. **Installez votre second cerveau d'abord** ("Installe mon second cerveau" a la racine du workspace).
   La prospection lit votre offre, votre cible et votre voix dans `Contexte/` : elle ne vous
   les redemande pas.
2. **Ouvrez le dossier `Vente/`** dans Claude Code. Verifiez que vous avez un
   abonnement Claude payant actif (Pro ou plus).
3. **Ecrivez simplement "Installe ma prospection"** dans le chat (ou meme juste "bonjour" :
   Claude vous proposera de demarrer l'installation).

C'est tout. Claude va, tout seul :

- Lire votre second cerveau (`Contexte/`) et ne vous poser que les questions propres a la
  prospection : canaux, volume, signaux, garde-fous.
- Vous demander l'adresse de votre site web seulement si le second cerveau n'est pas installe.
- Vous montrer le profil de prospection reconstitue et vous laisser le corriger avant de le figer.
- Vous connecter vos outils un par un (Unipile, Crustdata, FullEnrich, Lemlist, Apify).
- Vous proposer de lancer une premiere recherche de prospects.

Vous n'editez aucun fichier, vous ne touchez pas au terminal : vous repondez aux questions
dans le chat, Claude fait le reste.

> Une fois installe, vous n'etes meme pas oblige de relire ce guide. Ecrivez simplement ce
> que vous voulez faire (par exemple "trouve-moi 20 directeurs marketing de PME SaaS en
> France") et Claude vous guide.

---

## Le parcours de prospection (apres installation)

Chaque etape correspond a une phrase que vous ecrivez dans le chat. Pas besoin de comprendre
la technique : vous deroulez, Claude s'occupe du reste.

### Etape 1 - Trouver des prospects

> "Trouve-moi 20 [votre cible, ex: directeurs marketing de PME SaaS en France]"

Declenche `trouver-personnes` (ou `trouver-entreprises` si vous ciblez des comptes plutot que
des contacts).

### Etape 2 - Detecter un signal d'interet (optionnel mais recommande)

> "Regarde qui a commente ce post [URL d'un post concurrent ou d'un sujet cle de votre marche]"

Declenche `scraper-post` en mode commentaires. Les gens qui commentent un post sur votre
sujet sont plus receptifs qu'une liste froide.

### Etape 3 - Trier la liste

> "Qualifie cette liste selon mon ICP"

Declenche `qualifier-liste`. Garde ce qui matche votre cible (definie dans `Contexte/`),
ecarte le reste avec la raison.

### Etape 4 - Enrichir

> "Trouve les emails de ces prospects"

Declenche `trouver-email`. Recupere emails et telephones verifies.

### Etape 5 - Ecrire les messages

> "Redige un message pour chacun, dans ma voix"

Declenche `personnaliser-message`. Un message par prospect, base sur son profil et votre
positionnement.

### Etape 6 - Lancer

Selon le canal :
- LinkedIn : *"Envoie les invitations a cette liste"* -> `envoyer-invitation`
- Email : *"Cree une campagne Lemlist avec ces messages"* -> `creer-campagne-lemlist` puis
  `lancer-sequence-lemlist`

### Etape 7 - Suivre les reponses

> "Qui a repondu cette semaine ?"

Declenche `verifier-reponses`. Ne relance jamais quelqu'un qui a deja repondu (regle appliquee
automatiquement par tous les skills d'envoi).

---

## Rebrancher un outil plus tard

Si vous voulez ajouter ou reconnecter un outil apres l'installation :

> "Connecte mes outils"

Declenche `connecter-outils`, qui reprend la connexion la ou vous en etes.

---

## Garde-fous integres (non negociables)

- **Max 30 invitations LinkedIn par jour.** Au-dela, LinkedIn restreint le compte.
- **Jamais de relance a quelqu'un qui a repondu.** Verifie avant chaque envoi.
- **Sequence par defaut** : invitation -> 2 jours -> message 1 -> 3 jours -> message 2.
- **Rien ne part sans votre validation** du contenu au prealable.

## En cas de blocage

> "Quelque chose ne marche pas, aide-moi a deboguer"

Decrivez ce que vous avez essaye et ce qui s'est passe. Claude ira lire le `SKILL.md`
concerne et vous dira quoi verifier (cle API, format de fichier, quota...).
