# Les 6 seaux de personnalisation, les hooks, les playbooks

La personnalisation part d'une donnée. Ce fichier classe les données disponibles en six seaux (du plus fort au plus faible), dit comment les transformer en accroche (hook fort ou hook léger), et donne les playbooks avec et sans personnalisation selon la catégorie de contact. Les prompts pour produire ces accroches sont dans `prompts-personnalisation.md`, la méthode d'ouverture par personne dans `ouvertures-personnalisees.md`.

## 1. Les six seaux, classés par valeur

### Seau 1 : ce que la personne a publié (le plus fort)
Interventions en conférence, webinaires, articles, posts LinkedIn, épisodes de podcast. La personne a choisi ses mots, vous les citez. Collecte : `enrichir_personne` (posts récents), recherche web sur "prénom nom + podcast / conférence".

### Seau 2 : ce avec quoi elle a interagi
Posts commentés, partagés, aimés. Les commentaires qu'elle a écrits. Dit quels sujets l'occupent cette semaine. Collecte : `scraper_engagement` sur les posts de votre marché, `enrichir_personne` (activité récente).

### Seau 3 : comment elle se décrit
La ligne de titre LinkedIn, la section "Infos", la description de son poste (rôle, spécialité, réussites). Ses propres mots pour cadrer la pertinence. Collecte : `enrichir_personne`.

### Seau 4 : le tiroir à bazar
Centres d'intérêt, bénévolat personnel, langues, écoles, pages suivies. Utile pour créer un lien humain, à petite dose. Une info hors sujet sur son école fait tomber l'email dans "le stagiaire a regardé mon profil". Collecte : `enrichir_personne`.

### Seau 5 : le parcours
Ancienneté dans l'entreprise, trajectoire (mouvements entre entreprises), recommandations données et reçues, mandats, mentorat, distinctions, certifications, relations communes, compétences validées. Collecte : `enrichir_personne`, `detecter_signal` (changement de poste).

### Seau 6 : l'entreprise
Le langage du site, les posts et articles de l'entreprise, les mentions presse, l'introduction en bourse, les levées, les résultats publiés, les fusions et acquisitions (a acquis, a été acquise, a fusionné), la croissance, les recrutements et embauches clés, les déménagements et nouvelles implantations, les lancements de produits, fonctionnalités et intégrations, les opérations marketing, les concurrents et leurs mouvements, les résultats bons ou mauvais visibles de l'extérieur. Collecte : `enrichir_entreprise`, `detecter_signal`, `scraper_offres_emploi`, `detecter_techno`, `scraper_pubs`.

C'est le seau de la personnalisation à volume : un signal d'entreprise vaut pour tous les décideurs de l'entreprise.

## 2. Sans personnalisation : les cinq pertinences de repli

Quand aucun seau n'est rempli, l'email reste pertinent par le segment :

1. Démographique : le persona (le titre, la fonction).
2. Firmographique : la taille ou le stade de l'entreprise.
3. Firmographique : le secteur.
4. Firmographique : la zone géographique.
5. Technographique : la stack technique.

"On travaille avec des cabinets d'expertise comptable de 20 à 80 personnes en région lyonnaise" est une pertinence de repli honnête. C'est de la segmentation, pas de la personnalisation : ne la comptez pas comme telle dans vos rapports.

## 3. Hook fort, hook léger

**Hook fort (citation littérale)** : une citation ou une référence directe à son contenu.

> Dans votre post sur l'épuisement des SDR, vous écriviez que "le vrai problème, c'est le manque de leads qualifiés"...

> Dans votre épisode sur le passage à l'échelle, vous disiez avoir "galéré sur la prévisibilité du pipeline jusqu'à"...

**Hook léger (lien de thème)** : le sujet sans la citation.

> Vous publiez beaucoup sur les difficultés du RevOps ces temps-ci...

> La prévisibilité du pipeline a l'air d'être votre sujet du moment...

| Situation | Hook | Effort |
|---|---|---|
| Compte clé, panier élevé | fort | élevé |
| Milieu de marché | l'un ou l'autre | moyen |
| PME, volume | léger | faible |
| Un champion existe déjà dans le compte | léger | faible |
| Remplacement d'un concurrent en place | fort | élevé |

Hook fort intégré :

> Dans votre post sur l'outbound "cassé", vous citiez des taux de réponse sous 1 %. On aide des équipes comme {{client_similaire}} à dépasser 15 % en ciblant sur signal plutôt qu'en volume. Ouvert à comparer nos notes ?

Hook léger intégré :

> Vous agrandissez l'équipe SDR de {{entreprise}}. La plupart des responsables SDR que je rencontre parlent de temps de montée en charge et de qualité du pipeline. {{client_similaire}} a réduit la montée en charge de 40 %. C'est un chantier chez vous ?

## 4. Les playbooks par catégorie de contact

Trois catégories : **entrant** (il vous a contacté, téléchargé, demandé une démo), **après engagement** (il a réagi à un post, assisté à un webinaire, visité une page : un pont entre lui et vous), **sortant** (à froid).

### Avec personnalisation (manuel, comptes clés)

| Catégorie | Première ligne | Deuxième ligne |
|---|---|---|
| Entrant | le déclencheur seul (ce qu'il a fait) | CTA pour caler un créneau, pertinence de repli en option |
| Après engagement | le déclencheur, puis "mais surtout" la personnalisation | le hook + la pertinence de repli |
| Sortant | le titre ou le résumé du contenu de la personne + un extrait | le hook + la pertinence de repli |

Entrant :
> Merci d'avoir téléchargé le guide de la prospection à froid. 15 minutes pour voir comment l'appliquer chez {{entreprise}} ?

Après engagement :
> Vous étiez à notre webinaire sur la prospection par signal, mais surtout, votre post sur "l'outbound est mort" m'a arrêté. Vous parliez de taux de réponse sous 1 %. On aide des éditeurs SaaS à dépasser 15 % en ciblant sur signal. Ça vaut un échange ?

Sortant :
> Votre post sur l'épuisement des SDR, et surtout la ligne "empiler des gens sur le problème ne passe pas à l'échelle", m'a parlé. On travaille avec des éditeurs entre 5 et 20 M€ qui ont touché ce mur. La plupart passent du volume au signal. C'est sur votre radar ?

### Sans personnalisation (automatisé, volume)

| Catégorie | Première ligne | Deuxième ligne |
|---|---|---|
| Entrant | le déclencheur seul | CTA pour caler un créneau |
| Après engagement | le déclencheur | la pertinence de repli |
| Sortant | la pertinence de repli avec une ouverture en rupture de schéma | la pertinence de repli ("on travaille avec...") |

Entrant :
> Merci pour votre demande de démo. On se cale 15 minutes pour voir comment {{produit}} marche chez des {{secteur}} ? {{lien agenda}}

Après engagement :
> Vu que vous avez regardé notre page tarifs. On travaille avec des éditeurs SaaS entre 5 et 20 M€ sur la prospection. Un échange rapide pour voir si ça colle ?

Sortant :
> Question rapide : comment votre équipe gère la prévisibilité du pipeline en ce moment ? On travaille avec des éditeurs entre 5 et 20 M€ qui vivent avec un flux de leads en dents de scie. Ça vaut le coup d'en parler ?

### La matrice de décision

| Facteur | Personnaliser | S'en passer |
|---|---|---|
| Panier | plus de 25 k€ par an | moins de 25 k€ |
| Volume | moins de 50 envois par jour | plus de 100 par jour |
| Fit ICP | comptes tier 1 | tiers 2 et 3 |
| Force du signal | signal faible (il faut compenser) | signal fort (il porte l'email) |
| Concurrence | marché saturé | marché calme |

À l'échelle, la segmentation bat la personnalisation individuelle sur le rapport effort / résultat. La personnalisation par personne se réserve aux comptes qui la méritent.

## 5. L'ICP doré et les meilleurs déclencheurs

**Empiler les signaux** au lieu de filtrer sur l'effectif :

| Niveau | Signal | Exemple |
|---|---|---|
| 1 | créée récemment | moins de 2 ans |
| 2 | financée | a levé |
| 3 | dirigeant qui débute | jamais été dirigeant avant |

Faites tourner le signal le plus important en premier ; n'enrichissez pas la suite si le premier échoue ; changez le message selon le nombre de signaux vrais.

**Les déclencheurs qui marchent** : le changement de poste reste fiable ("bravo pour le poste, maintenant que vous reprenez...") mais tout le monde l'utilise. Les signaux sociaux (posts sur un mot-clé, engagement sur un sujet) battent aujourd'hui les déclencheurs "logiques" (recrutement, levée, expansion) sur la plupart des comptes. Sur une entreprise de recrutement offshore, le déclencheur "a posté sur LinkedIn" a battu tous les autres.

**Taux de réponse selon le déclencheur** : à froid sans signal 6 à 8 %, sur signal 18 à 22 %, sur signaux empilés 35 à 40 %, visiteur du site 25 à 30 %, ancien client qui a changé de poste 20 à 25 %.

## 6. Utiliser l'IA sans se brûler

- **Montrez votre source.** "D'après votre page carrières, vous avez 12 postes ouverts" plutôt que "vous avez 12 postes ouverts". Si c'est faux, c'est la source qui l'est.
- **Une IA pour une partie de l'email, pas pour tout.** L'ouverture est variable, le corps est fixe et validé. Vous gardez la main sur le test A/B.
- **Les études de cas du prospect.** `enrichir_entreprise` peut lire ses cas clients : "J'ai vu votre cas avec {{client du prospect}} sur {{sujet}}". En PS : "Même si on ne se parle jamais, ce cas client est vraiment bien fait."
- **Jamais de compliment généré.** "J'adore votre travail" est reconnu en une seconde.

## 7. Playbooks avancés, avec la stack

| Playbook | Mécanisme | Verbes |
|---|---|---|
| Vidéo personnalisée | une vidéo courte qui dit "Bonjour {{prenom}}" avec son site en fond, le reste identique pour tous | enregistrement manuel, lien dans l'email 2 |
| Image personnalisée | l'image d'une de ses pubs ou de son site insérée dans un visuel (fonction native de Lemlist) | `scraper_pubs`, puis l'image en relance |
| Lookalikes | les entreprises semblables à vos meilleurs clients, message "les entreprises comme la vôtre" | `trouver_lookalikes` |
| Abonnés d'un concurrent | les personnes qui suivent ou commentent un concurrent, message comparatif | `scraper_engagement` sur les posts du concurrent |
| Offre d'emploi | un poste ouvert révèle un besoin, message "les entreprises qui recrutent ce poste ont en général {{probleme}}" | `scraper_offres_emploi` |
| Pubs actives | les pubs du prospect citées dans l'email ou reprises en image | `scraper_pubs` |
| Avis clients | un avis Google du prospect cité, nom du client et sujet | `trouver_entreprises` (fiche locale), lecture des avis |

Exemple abonnés d'un concurrent :

> Bonjour {{prenom}}, vous suivez {{concurrent}} sur LinkedIn. Deux raisons pour lesquelles des équipes passent de {{concurrent}} à nous : {{limite 1}}, et {{limite 2}}. Un comparatif de 15 minutes vous serait utile ?

Exemple avis client (contact après engagement) :

> Bonjour {{prenom}}, vous avez réagi à notre post sur {{sujet}}. J'ai vu sur Google que {{nom du client}} a laissé un avis sur la façon dont {{entreprise}} l'a aidé sur {{sujet de l'avis}}. On aide des {{secteur}} exactement sur ce point, par exemple {{cas client}}. Un échange rapide ?

Le nom du client de l'avis prouve que vous avez cherché ; le cas client du même secteur prouve que vous savez faire ; le post cité réchauffe le contact ; la fiche Google trouve les entreprises locales que LinkedIn ne montre pas.

## 8. Campagne multi-signaux : la structure de table

Pour une campagne sur des comptes à plusieurs signaux, deux tables.

**Table entreprises** : nom, URL LinkedIn, croissance d'effectif sur un an (signal 1), case "plus de 10 % ?", actualité récente (signal 2), case "acquisition ?", levée, page contact.

**Table personnes** : nom, titre, service (classé par Claude), profil, cas d'usage propres à ce service (générés à partir de la description de l'entreprise et de votre offre), email vérifié, première ligne (générée selon le signal vrai).

Première ligne selon le signal : si croissance de plus de 10 %, "{{entreprise}} a grandi de {{n}} personnes cette année..." ; si acquisition, "{{entreprise}} vient de racheter {{cible}}..." ; sinon, la pertinence de repli. Puis la proposition de valeur, les cas d'usage propres au service, la preuve, le CTA. Les morceaux s'assemblent par formule dans le CSV, colonne par colonne.
