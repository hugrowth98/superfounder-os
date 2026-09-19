---
name: installer-gtm
description: >
  Installe le module GTM de bout en bout pour un dirigeant ou un commercial qui ne code pas : lit le
  second cerveau (`01_About-Me/`, `02_Contexte/`) s'il est rempli, pose une question à la fois pour remplir
  contexte.md (offre et preuves, ICP en 3 couches avec scoring, personas ATL et BTL, 5 signaux
  prioritaires, canaux et volumes, voix, garde-fous), teste la taille du marché, connecte les
  outils via connecter-outils, fait valider le résumé, puis lance un premier run guidé.
  Se déclenche sur : "Installe ma prospection", "installe le GTM", "installe le module GTM",
  "on démarre", "je commence", "configure la prospection", ou tout premier message quand
  contexte.md contient encore des crochets [...].
  Ne pas utiliser pour : brancher ou rebrancher un seul outil (voir connecter-outils), modifier
  une ligne de contexte.md déjà remplie (le faire directement sur demande), construire une
  liste ou écrire un message (voir les masters).
---

# Installer le module GTM

L'utilisateur vient de dire "Installe ma prospection". C'est un dirigeant ou un commercial, pas un développeur : il ne touche ni terminal ni fichier. Tout le travail technique est fait ici, une étape à la fois, une seule question par message, avec une valeur par défaut proposée chaque fois que c'est raisonnable pour qu'il n'ait qu'à confirmer. Vouvoiement, ton direct, zéro jargon. Aucun tiret cadratin.

Ce que l'installation produit : `05_Departements/Go-to-Market/contexte.md` rempli et validé, `05_Departements/Go-to-Market/OUTILS.md` rempli par `connecter-outils`, un `.env` à la racine, et une première liste lancée. Rien n'est envoyé à personne pendant l'installation.

Durée : 45 minutes à 1h30 selon ce que le second cerveau contient déjà. Dire à l'utilisateur qu'il peut s'arrêter à la fin de n'importe quelle phase et reprendre plus tard avec "reprends l'installation".

## Règles pendant toute l'installation

- Une seule question par message. Reformuler la réponse en une ligne avant de passer à la suivante.
- Jamais de contexte inventé. Une information absente reste un crochet vide, jamais un exemple recopié.
- Lire avant de demander : ne poser que les questions auxquelles les fichiers existants ne répondent pas.
- Écrire dans `05_Departements/Go-to-Market/contexte.md` à la fin de chaque phase, pas tout à la fin, pour qu'une session interrompue ne perde rien.
- Ne rien écrire dans `01_About-Me/` ni `02_Contexte/` : ces fichiers appartiennent à `installer-second-cerveau`. Si une information devrait y vivre, la signaler et proposer de l'y ajouter après validation, dans un diff.
- Montrer les résumés en texte lisible, jamais en bloc de code ni en dump de fichier.

## Phase 0 : lire ce qui existe déjà

Sans rien demander, vérifier l'état du second cerveau : `01_About-Me/about-me.md` et les fichiers de `02_Contexte/` à la racine du workspace contiennent-ils encore des `[à remplir]` ?

Si le second cerveau est rempli, lire :
- `01_About-Me/about-me.md`, `01_About-Me/my-company.md`
- `02_Contexte/Offer-Positioning.md` ou `02_Contexte/Offre-positionnement.md` (offre, différenciation, preuves)
- `02_Contexte/Clients-Problems-and-Messages.md` (cible, problèmes dans leurs mots)
- `02_Contexte/Tone-and-Voice.md` (voix)
- `05_Departements/Go-to-Market/` s'il contient déjà des listes, des messages ou une note

Pour chaque fichier, noter s'il est rempli ou s'il contient encore `[à remplir]`. Un fichier rempli ferme les questions correspondantes : les sections 1 et 6 de `05_Departements/Go-to-Market/contexte.md` deviennent des pointeurs, et la moitié des questions de la section 2 et 3 sont déjà répondues (pré-remplir, faire confirmer).

Si les fichiers sont vides : le dire en une phrase et proposer deux options. Soit lancer `installer-second-cerveau` d'abord (recommandé, 1h pour les trois fichiers), soit répondre ici aux questions de la Phase 1 et remplir la section 1 de `05_Departements/Go-to-Market/contexte.md` directement. Dans ce second cas, demander l'adresse du site web de l'entreprise, lire la page d'accueil, la page offre et la page à-propos avec la lecture web intégrée, et proposer un premier jet de l'offre et de la cible à corriger plutôt qu'un questionnaire vide.

Annoncer ensuite ce qui est déjà connu et ce qui reste à faire, en cinq lignes maximum.

## Phase 1 : offre et preuves (section 1)

Objectif : une phrase d'offre qu'on peut dire au téléphone, et trois preuves citables.

Questions, dans l'ordre, seulement si la Phase 0 n'y a pas répondu :
1. "Si vous deviez dire ce que vous faites en une phrase à un dirigeant au téléphone, sans jargon, vous diriez quoi ? Le moule qui marche : on aide les [qui] à [résultat] sans [douleur]."
2. "Le problème que vous réglez, dans les mots de vos clients, pas les vôtres : la phrase qu'ils disent en rendez-vous."
3. "Quel format et quel prix ?"
4. "Trois clients que vous pouvez citer, avec un résultat chiffré chacun. Si vous n'en avez qu'un, on part avec un."
5. "Ce que vous ne faites pas, pour couper court si on vous le demande en appel."

Si une phrase d'offre proposée par l'utilisateur dépasse 25 mots ou contient un nom de méthode, proposer une version plus courte et faire choisir.

Écrire la section 1 (ou le pointeur vers `02_Contexte/`).

## Phase 2 : ICP en 3 couches et scoring (section 2)

Objectif : des critères qui se traduisent en filtres de recherche, et un barème sur 100.

Commencer par les meilleurs clients : "Citez vos 5 à 10 meilleurs clients, ceux que vous voudriez cloner. On va en déduire les critères plutôt que les deviner." Si le parent contient déjà l'ICP, le présenter et demander seulement ce qui manque.

Couche 1, firmographique, quatre questions : secteur (et secteur adjacent acceptable), effectif (fourchette), zone géographique (principale puis secondaire), stade ou chiffre d'affaires. Couche 2, technographique, deux questions : un outil ou une stack qui rend l'offre pertinente, un outil concurrent à repérer ; si l'offre ne dépend d'aucun outil, mettre la couche à 0 et le dire. Couche 3, comportementale : elle se remplit en Phase 4 avec les signaux.

Pondérations : proposer 40 / 20 / 40 et les seuils de tiers 75 / 55 / 35. Ne changer que si l'utilisateur le demande. Puis les exclusions : "B2C exclu par défaut, d'accord ? Vos concurrents à écarter ? Des secteurs ou des tailles à ne jamais toucher ?"

Test de volume, avant d'écrire : proposer d'estimer la taille du marché. "Je peux lancer une recherche à blanc pour compter combien d'entreprises correspondent à ces critères, sans rien exporter." Si Unipile est branché, lancer `trouver-entreprises --source unipile` sur une recherche Sales Navigator de comptes avec `--max 25` : la réponse donne le total de comptes correspondants, sans crédit. Sinon, lancer la source Apify choisie avec `--max 25` (quelques centimes) et lire le total dans le dry-run et le premier lot ; si aucun outil n'est encore branché, noter que le test se fera juste après la Phase 6 et y revenir. Lecture du résultat : moins de 300 comptes, l'ICP est trop étroit ou le marché est petit, il faudra ouvrir un critère ; plus de 5 000, c'est trop large pour du signal, il faut resserrer ; entre les deux, c'est bon. Faire choisir un ajustement si besoin, une seule fois.

Écrire la section 2.

## Phase 3 : personas et comité d'achat (section 3)

Objectif : les titres à chercher, l'angle par persona, et qui décide vraiment.

1. "Chez vos clients, qui signe ? Titres exacts tels qu'ils apparaissent sur LinkedIn." C'est l'ATL.
2. "Qui vit le problème tous les jours et vous fait entrer ?" C'est le BTL. Dans une TPE c'est souvent la même personne : le noter et ne pas forcer deux personas.
3. Pour chacun : ce qui l'empêche de dormir, ce qu'il mesure, le canal où il répond le mieux. Proposer une hypothèse tirée de la Phase 1 et faire corriger, plutôt que de poser trois questions ouvertes.
4. Comité d'achat : "Sur votre dernière vente, qui a joué quel rôle : champion, décideur, utilisateur, évaluateur, bloqueur ?" Remplir seulement les rôles qui existent vraiment.

Écrire la section 3.

## Phase 4 : les 5 signaux prioritaires (section 4)

Objectif : cinq signaux classés, avec la raison pour cette offre.

Présenter les sept signaux en une ligne chacun, dans les mots de l'utilisateur :
- Changement de poste : un décideur arrive, il cadre ses priorités dans les 90 jours.
- Levée de fonds : du budget neuf et un plan à tenir.
- Recrutement : ils cherchent un profil ou une compétence que vous fournissez.
- Événement : votre cible est réunie au même endroit, avant ou après.
- Techno : ils adoptent ou quittent un outil lié à votre offre.
- Engagement contenu : ils ont réagi à un post, visité un profil, répondu à quelque chose.
- Concurrents : ils sont clients d'un concurrent, ou un concurrent fait de la pub chez eux.

Recommander selon l'offre, en une phrase, avant de demander : service ou conseil, recrutement et changement de poste en tête ; logiciel, techno et levée ; formation ou coaching, engagement contenu et événement ; agence, concurrents et recrutement. Puis : "Lesquels gardez-vous, dans quel ordre ? Et pour chacun, pourquoi c'est un bon moment pour vous appeler ?" Fixer la fraîcheur maximale par signal (proposer les fenêtres de la table de `05_Departements/Go-to-Market/contexte.md`).

Écrire la section 4 et compléter la couche 3 de la section 2.

## Phase 5 : canaux, volumes et choix LinkedIn (section 5 et OUTILS.md)

Objectif : ce qu'on fait chaque semaine, et par quel outil pour LinkedIn.

1. "Quels canaux : LinkedIn, email, téléphone ? Les trois, c'est ce qui marche le mieux, et le téléphone est celui que vos concurrents n'osent pas."
2. "Combien de nouveaux prospects par semaine ? Je propose 20 pour commencer." Puis rendez-vous visés par semaine.
3. Volumes par canal, en rappelant les plafonds de `05_Departements/Go-to-Market/GARDE-FOUS.md` (30 invitations par jour, 30 emails par boîte par jour) et en proposant en dessous.
4. Jours et heures d'envoi. Proposer mardi à jeudi, 8h30 à 11h et 14h à 17h.
5. Séquence : proposer LinkedIn, email, email, LinkedIn, téléphone, et demander si une variante est voulue.

Choix LinkedIn, à expliquer en trois lignes puis à faire trancher :
- Unipile : votre propre compte LinkedIn piloté par vos skills, gratuit hors abonnement Unipile, garde-fous locaux (compteur d'invitations et de messages sur votre machine). Plus de contrôle, plus de réglages.
- Lemlist : vos séquences LinkedIn et email dans le même outil, avec leur interface et leurs relances. Plus simple si vous l'avez déjà.
- Email : Lemlist dans les deux cas.

Écrire la section 5. Noter `canal_linkedin` et `canal_email` pour `connecter-outils`, qui les écrira dans `05_Departements/Go-to-Market/OUTILS.md`.

Voix (section 6) : si `02_Contexte/Tone-and-Voice.md` existe, écrire le pointeur et demander seulement tutoiement ou vouvoiement en prospection (défaut : vouvoiement) et la longueur d'un premier message. Sinon, les cinq questions de la section 6, une par une.

Garde-fous propres (section 7) : "Qui ne faut-il jamais contacter : clients actuels et passés, partenaires, une liste que vous avez déjà ? Donnez-moi les domaines ou le fichier." Puis zones exclues, limite de volume plus basse, mots interdits. Une ligne vide vaut mieux qu'une ligne fausse.

Précisions libres (section 8) : "Quelque chose que je dois savoir avant de commencer : un événement qui arrive, une campagne en cours ailleurs, un compte LinkedIn fragile ?"

## Phase 6 : connecter les outils

Lire et suivre `connecter-outils`. Il branche les outils un par un, teste chaque clé par un vrai appel, écrit `.env` et remplit `05_Departements/Go-to-Market/OUTILS.md` (priorité, canal LinkedIn choisi en Phase 5, état des connexions). Rappeler à l'utilisateur qu'un seul outil suffit pour démarrer et que les autres se branchent plus tard avec "Connecte mes outils".

Si le test de volume de la Phase 2 n'a pas pu se faire, le lancer maintenant avec le premier outil branché.

## Phase 7 : valider contexte.md et OUTILS.md

Présenter un résumé lisible, section par section, de `05_Departements/Go-to-Market/contexte.md` : l'offre en une phrase, les critères ICP et les seuils, les deux personas, les cinq signaux, les canaux et volumes, les garde-fous propres. Puis l'état de `05_Departements/Go-to-Market/OUTILS.md` : priorité, canal LinkedIn, CRM, outils branchés et testés, outils restants.

Demander : "Voici ce que j'ai retenu. Dites-moi ce qui est juste et ce que vous voulez corriger avant que je le fige." Corriger, réafficher seulement les lignes changées, obtenir un oui explicite. Vérifier qu'il ne reste aucun crochet dans les sections 2 et 3 ; s'il en reste, poser la question manquante ou laisser vide en le disant. Écrire la date de remplissage en bas de `05_Departements/Go-to-Market/contexte.md`.

Proposer `/done` pour que l'installation remonte dans la note `Go-to-Market.md` et le journal du jour.

## Phase 8 : premier run guidé

Rappeler où vont les fichiers : listes et enrichissements dans `05_Departements/Go-to-Market/Listes-prospection/`, messages et scripts dans `Messages/`, runs de signaux dans `Signaux/`.

Proposer la première liste à partir du signal n°1 et du persona ATL : "Tout est en place. On lance une première liste ? Par exemple : trouve-moi 20 [persona ATL] de [secteur] en [zone] qui [signal n°1]." Si l'utilisateur dit oui, router vers `detecter-signaux` si la demande part d'un signal, sinon vers `construire-liste`, annoncer le coût avant tout appel payant, et livrer un CSV avec le lien cliquable. Puis un seul next step : qualifier la liste, ou préparer le premier appel avec `cold-call`.

## Reprise de session

Sur "reprends l'installation" ou tout message pendant que `05_Departements/Go-to-Market/contexte.md` contient encore des crochets dans les sections 2 ou 3 : relire `05_Departements/Go-to-Market/contexte.md` et `05_Departements/Go-to-Market/OUTILS.md`, dire en trois lignes ce qui est fait et ce qui reste, reprendre à la première phase incomplète. Sur "reprends à la phase N", aller à la phase demandée après ce même état des lieux.

## Exemples

- "Installe ma prospection" avec un second cerveau rempli : Phase 0 lit tout, annonce que l'offre, la cible et la voix sont connues, démarre à la Phase 2 avec l'ICP pré-rempli à confirmer.
- "On démarre" avec un second cerveau vide : Phase 0 propose le second cerveau ou le site web, l'utilisateur donne le site, Claude lit trois pages et propose l'offre et la cible à corriger.
- "Installe le GTM, j'ai déjà Lemlist" : Phase 5 note Lemlist pour LinkedIn et email sans réexpliquer Unipile en détail, Phase 6 branche Lemlist en premier.
