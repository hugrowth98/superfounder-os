# Le module GTM : mode d'emploi

Vous n'avez presque rien à faire pour installer. Une phrase dans le chat, Claude fait le reste. Ce guide sert d'aide-mémoire : ce que c'est, ce qu'il faut avoir, les phrases à taper, où vont les fichiers.

## Ce que c'est

Le module GTM est un dossier que Claude Code lit pour faire tourner votre prospection B2B : définir votre cible, construire des listes de comptes et de décideurs, repérer le bon moment pour les contacter (recrutement, levée, prise de poste, engagement sur un post), écrire vos messages dans votre voix, les envoyer, suivre les réponses, préparer et débriefer vos appels. Vous parlez en phrases simples. Claude choisit la méthode, appelle les outils que vous avez branchés, et vous montre tout avant d'envoyer quoi que ce soit.

Le principe : vous validez, Claude exécute. Rien ne part sans votre oui.

## Ce qu'il faut avoir

| Outil | À quoi il sert ici | Obligatoire | Coût indicatif (septembre 2026, à vérifier) |
|---|---|---|---|
| Claude Code avec un abonnement Claude | le moteur de tout | oui | Pro dès 20 € par mois, Max conseillé pour un usage quotidien |
| Apify | scraper des sites, des offres d'emploi, des posts, détecter des signaux | oui, ou Crustdata | essai gratuit, puis dès 40 $ par mois |
| Unipile | piloter votre compte LinkedIn (recherche, profils, invitations, messages) | si LinkedIn par vos skills | environ 55 € par mois par compte |
| Lemlist | envoyer vos séquences email, et LinkedIn si vous préférez tout dans un outil | si vous envoyez des emails | dès 40 € par mois, multicanal dès 80 € |
| FullEnrich | trouver l'email pro vérifié et le mobile d'un décideur | si vous voulez appeler ou emailer | dès 30 $ par mois, 1 crédit par email, 10 par téléphone |
| Crustdata | rechercher des entreprises et des personnes par API, sans passer par Apify | non | sur devis, crédits à l'usage |
| Ocean.io | trouver des entreprises qui ressemblent à vos meilleurs clients | non | sur devis, essai gratuit |
| HubSpot | votre CRM : import, dédoublonnage, pipeline | non | gratuit pour démarrer |
| PredictLeads (optionnel) | les événements d'entreprise (expansion, partenariat, lancement, nomination), les levées, les technos datées | non | abonnement mensuel avec quota de requêtes |
| TheirStack (optionnel) | les offres d'emploi filtrées par techno citée, et l'intent (recrute et utilise telle techno) | non | 1 crédit par résultat, palier gratuit à l'inscription |

Un seul outil suffit pour commencer. Le minimum pour une première liste : Claude Code et Apify. Le minimum pour appeler : ajouter FullEnrich. Le minimum pour envoyer : ajouter Lemlist.

## Les 3 phrases pour démarrer

1. **"Installe ma prospection"** : Claude lit ce qu'il sait déjà de vous, vous pose une question à la fois (offre, cible, personas, signaux, canaux), teste la taille de votre marché, branche vos outils et vous propose une première liste. Comptez 45 minutes à 1h30, en plusieurs fois si vous voulez.
2. **"Connecte mes outils"** : pour brancher ou rebrancher un outil, un par un. Claude vous donne le lien, vous collez la clé dans le chat, il teste.
3. **"Fais-moi une liste de..."** : par exemple "fais-moi une liste de 20 DRH de PME industrielles en Auvergne-Rhône-Alpes qui recrutent un commercial". Claude construit, qualifie, enrichit, et vous livre un fichier.

## Les 4 masters et ce qu'on leur demande

Un master est un skill qui connaît une méthode entière et route votre demande vers le bon sous-skill. Vous n'avez pas à les nommer : les phrases suffisent.

| Master | Il sait faire | Exemples de phrases |
|---|---|---|
| Construire une liste | définir l'ICP, trouver des entreprises et des décideurs, qualifier, nettoyer, dédoublonner | "Trouve-moi 30 dirigeants de cabinets de recrutement à Lyon" ; "Qualifie cette liste selon mon ICP" ; "Trouve des entreprises qui ressemblent à mes trois meilleurs clients" |
| Détecter des signaux | qui recrute, qui a levé, qui vient de changer de poste, qui a réagi à un post, qui utilise tel outil | "Qui a levé des fonds ce mois-ci dans la fintech en France ?" ; "Regarde qui a commenté ce post" ; "Quels comptes de ma liste recrutent un SDR ?" |
| Cold email | premier contact, relances, objets, personnalisation par persona, délivrabilité | "Écris une séquence de 3 emails pour cette liste" ; "Relance ceux qui n'ont pas répondu, dans ma voix" ; "Cet email sent l'IA, corrige-le" |
| Cold call | script d'appel, objections, no-show, brief avant appel, débrief après | "Prépare l'appel avec Marie Dupont de Transactis" ; "Il m'a dit envoyez-moi un mail, je réponds quoi ?" ; "Débriefe cet appel : voici mes notes" ; "Mon rendez-vous de 14h n'est pas venu" |

## Où vont les fichiers

- Vos listes, enrichissements, offres d'emploi, engagements, technos et pubs : `05_Departements/Go-to-Market/Listes-prospection/`, un CSV par étape, nommé par ce qu'il contient et daté.
- Vos messages, séquences et scripts d'appel : `05_Departements/Go-to-Market/Messages/`.
- Vos runs de signaux (levées, changements de poste, recrutements, événements) et `comptes-suivis.csv`, la liste des comptes que vous surveillez : `05_Departements/Go-to-Market/Signaux/`.
- Ce que Claude sait de vous : `05_Departements/Go-to-Market/contexte.md`. Ce que font vos outils : `05_Departements/Go-to-Market/OUTILS.md`. Vos clés : `.env`, jamais lu à voix haute.
- Rien n'est supprimé par Claude : un fichier remplacé est renommé avec sa date.

Chaque réponse de Claude qui produit un fichier finit par un lien cliquable vers ce fichier.

## Les garde-fous, en cinq lignes

1. Rien ne part sans que vous ayez vu trois messages réels et dit oui.
2. 30 invitations LinkedIn par jour, 50 messages, 30 emails par boîte : au-delà, votre compte est en danger, Claude s'arrête.
3. Jamais de message à quelqu'un qui a répondu, à un client, à un partenaire, à un exclu.
4. Avant tout appel payant, Claude annonce le nombre de lignes et le coût, et attend votre oui.
5. Un email contient toujours un moyen de dire stop ; un opt-out est appliqué sous 48 heures. Le détail est dans `05_Departements/Go-to-Market/GARDE-FOUS.md`.

## Questions fréquentes

**Je n'ai aucun outil, je peux quand même démarrer ?**
Oui. "Installe ma prospection" remplit votre contexte sans outil. Pour la première liste, il faut au moins Apify (essai gratuit) ou Crustdata.

**Je ne sais pas coder, je dois toucher au terminal ?**
Non. Vous répondez aux questions dans le chat et vous collez des clés quand Claude vous les demande. Il écrit les fichiers.

**Combien ça coûte de faire une liste de 100 personnes avec emails ?**
Ordre de grandeur : quelques centimes à quelques euros de scraping, puis 1 crédit par email trouvé, soit environ 100 crédits FullEnrich. Claude vous donne le chiffre exact avant de lancer.

**Claude a envoyé quelque chose sans me demander ?**
Non, il ne peut pas : chaque envoi passe par une validation sur échantillon. Si vous avez un doute, demandez "qu'est-ce qui est parti cette semaine ?" et il lit les compteurs.

**Je veux changer ma cible ou mon offre.**
Dites-le : "mon ICP change, on vise maintenant les ETI" et Claude modifie la ligne dans `05_Departements/Go-to-Market/contexte.md`, vous montre le diff, et c'est tout. Une information vit à un seul endroit.

**J'ai déjà Lemlist pour LinkedIn, je dois prendre Unipile ?**
Non. À l'installation vous choisissez : Lemlist pour tout (plus simple), ou Unipile pour piloter LinkedIn avec votre propre compte et vos garde-fous locaux (plus de contrôle). Vous pouvez changer plus tard.

**Mon compte LinkedIn a reçu un avertissement.**
Dites-le tout de suite. Claude coupe les envois LinkedIn, vous propose deux semaines d'activité manuelle et une reprise progressive. Le protocole est dans `05_Departements/Go-to-Market/GARDE-FOUS.md`.

**Ça marche sans le reste du Superfounder OS ?**
Non : le module lit votre offre, votre cible et votre voix dans `01_About-Me/` et `02_Contexte/`. Installez le second cerveau d'abord ("Installe mon second cerveau"), même en version courte ; `installer-gtm` ne vous redemande que ce qui manque.

**Quelque chose ne marche pas.**
"Quelque chose ne marche pas, aide-moi" : décrivez ce que vous avez tapé et ce qui s'est passé. Claude lit le skill concerné et vous dit quoi vérifier (clé, quota, format de fichier).

**Comment je fais mon premier appel ?**
"Prépare l'appel avec [prénom nom, entreprise]" : Claude vous fait une fiche en cinq minutes, avec le signal, l'accroche et les objections probables. Puis vous décrochez. Puis "débriefe cet appel" avec vos notes.
