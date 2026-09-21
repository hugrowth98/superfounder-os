# Changelog

Toutes les évolutions notables de ce dépôt sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions selon [SemVer](https://semver.org/lang/fr/).

## [6.2.0] - 2026-09-21

Le dépôt ne transporte plus ses propres vieilles versions, et l'export Sales Navigator a son skill.

### Ajouté
- `exporter-salesnav` : une URL Sales Navigator (copiée, ou construite par `construire-requete-salesnav`) en CSV normalisé, par Unipile (votre compte) ou par vos cookies (Apify), signal posé d'après le filtre à cocher de l'URL, `dedoublonner --contre` pour ne garder que les nouveaux ; procédure, garde-fous et erreurs. `construire-requete-salesnav`, `OUTILS.md`, `docs/conventions-gtm.md`, `CLAUDE.md` et `AGENTS.md` (dix-sept skills d'exécution) y renvoient.
- `trouver-personnes` : une URL Sales Navigator sans cookies ni Unipile s'arrête avec le message utile au lieu de tomber sur `profils`.
- Sous-skill `veille` : les sources sans flux (Product Hunt, comptes X, communautés) restent dans `strategie-contenu.md` et se lisent à la main ou par WebSearch à la demande ; une page entreprise LinkedIn par `publications-entreprise`.

### Supprimé
- `11_Archives/skills-prospection-v3/` (22 skills de la v3 et leurs docs) et `11_Archives/trouver-url-linkedin-v3/` : l'historique du produit est dans git (`git show v5.2.0:10_Skills/...`), pas dans le dossier d'archives livré à l'utilisateur, qui repart vide avec sa note. Règle écrite dans `CONTRIBUTING.md` et dans `11_Archives/Archives.md` ; `CONTRIBUTING.md` cite aussi le second validateur.

## [6.1.0] - 2026-09-21

`trouver-personnes` choisit sa source tout seul, du plus puissant au plus rustique parmi ce qui est branché, et sait travailler à partir de simples noms d'entreprises.

### Ajouté
- Cascade automatique sans `--source` : Prospeo, puis Crustdata, puis Ocean.io (outils API, par domaine ou par cible), sinon Apify par Sales Navigator (cookies du `.env`, URL ou filtres), sinon Apify par LinkedIn (`employes` pour un CSV d'entreprises, `profils` pour une cible), sinon Apify par Google ; le script annonce la source retenue et pourquoi, et s'arrête en listant ce qui manque si rien n'est branché. Une URL Sales Navigator sans cookies passe par Unipile.
- Source `google` (`apify/google-search-scraper`) : une requête `("CEO" OR "Fondateur" ...) "Entreprise" site:linkedin.com/in` par entreprise (0,0025 $), ou une cible par titres, lieu et mots-clés ; lecture des titres de résultat et de `personalInfo`, colonne `confiance` (haute : entreprise et titre confirmés, moyenne : l'un des deux), `--garder-faibles`, `--pays`.
- `employes` accepte un CSV sans URL de page : les URLs manquantes sont cherchées par Google (`site:linkedin.com/company "<nom>"`). `profils` accepte un CSV de noms : lots de 10 dans `currentCompanies`, 3 profils par entreprise, et ne garde que les profils dont l'entreprise actuelle correspond (mots significatifs de 4 lettres et plus).
- Second passage automatique par Google pour les entreprises que `employes` ou `profils` ont laissées sans personne (`--sans-google` pour l'éviter).
- `sourcer-personnes`, `OUTILS.md`, `docs/prospection.md` (question "je n'ai qu'Apify"), `CLAUDE.md` et `AGENTS.md` décrivent la cascade.

### Modifié
- `scripts/validate_skills.py` ne compte ni ne valide plus `11_Archives/`, et affiche un comptage lisible : skills de premier niveau, masters, sous-skills. `README.md` : un seul décompte (40 skills de premier niveau, 7 masters, 53 sous-skills), chemins et sections de note alignés sur la structure numérotée (`02_Contexte/`, "Où on en est", Mission à Key Notes), CI décrite avec ses deux validateurs.

## [6.0.0] - 2026-09-20

Le contenu passe au même patron que la prospection : un master `linkedin` avec seize sous-skills, un système de veille que chacun remplit avec ses sources, un onboarding en huit phases, et la programmation des posts sur Publora. Version majeure parce que neuf skills changent de nom et de place.

### Changé (rupture)
- Les skills `linkedin-ideation`, `linkedin-interview`, `linkedin-writing-core`, `linkedin-educational`, `linkedin-storytelling`, `linkedin-hot-take`, `linkedin-lead-magnet`, `viral-hook-writer` et `linkedin-post-optimizer` deviennent les sous-skills `ideation`, `interview`, `educatif`, `storytelling`, `opinion`, `lead-magnet`, `hooks` (réécrit en français) et `optimiser` du master `linkedin` ; le socle `linkedin-writing-core` devient le master lui-même. Leurs références (`voix.md`, `formules-de-hooks.md`, `structures-de-post.md`, `checklist-qualite.md`, `frameworks-strategie.md`, `veines-et-questions.md`, `exemples-<type>.md`) sont dans `10_Skills/linkedin/ressources/`. Les phrases déclencheuses ne changent pas ; les commandes directes `/linkedin-*` disparaissent. `install.sh --into` déplace les anciennes copies dans `11_Archives/skills-deplaces/` de la cible.

### Ajouté
- Master `linkedin` : rôle, socle d'écriture (voix, stratégie, structure universelle, hook en trois règles, format de rendu, checklist), table de routage de seize sous-skills et repères.
- Sous-skills nouveaux : `veille` (brief éditorial en 6 sections depuis les newsletters et les chaînes de l'utilisateur, scripts `veille.py` et `abonnes.py` : flux RSS et Atom, likes et commentaires lus sur les archives Substack y compris à domaine personnalisé, vues YouTube, abonnés en cache 30 jours, vélocité pour 1 000 abonnés par jour, transcripts par `youtube-transcript-api` si installée, dump dans `sources/`), `formats`, `cta`, `publier`, `engagement`, `recycler`, `profil`, `performance` (méthode des tiers sur ses propres posts).
- Ressources nouvelles : `algorithme.md`, `frameworks-narratifs.md`, `profil.md`, `analyse-performance.md` ; cinq structures longues ajoutées à `structures-de-post.md`, huit formules et cinq ouvertures ajoutées à `formules-de-hooks.md`. Tout est écrit en français, sans donnée d'un compte tiers.
- `05_Departements/Marketing/LinkedIn/sources-veille.json` : le gabarit des sources (newsletters par thème et tier, chaînes YouTube par tier, autres flux, bloc `_exemple`), rempli à l'installation ; caches et dumps de la veille ignorés par git.
- `planifier-post` : programme un post validé sur Publora (client `Publora` dans `_commun`, spec OpenAPI lue le 2026-09-20 : `x-publora-key`, `/platform-connections`, `/create-post`, `/update-post`, `/delete-post`, `/list-posts`, `/test-connection`, `/get-upload-url` et `/complete-media`, `/linkedin-comments`, `/linkedin-post-statistics`), avec les contrôles de bonnes pratiques (bloquants : vide, plus de 3 000 caractères, tiret cadratin ; avertissements : hook de plus de 210 caractères, lien dans le corps, hashtag en ouverture, emojis, texte court, créneau hors fenêtre), collision à moins de 20 heures, pièce jointe locale (image, PDF de carrousel), brouillon, décalage, annulation, premier commentaire après publication, statistiques, et le calendrier `Calendrier-publication.md`. Guide d'installation dans le skill et dans `connecter-outils` (outil optionnel numéro 4, test gratuit `GET /platform-connections`, `PUBLORA_API_KEY` dans `.env.example`, ligne dans l'état des connexions d'OUTILS.md).
- `installer-contenu` en huit phases : lire le second cerveau, voix et style, posts de référence et chiffres (tiers dès 10 posts), stratégie (niche, monopole, IAP, piliers, répartition, convictions, objectif et cadence, formats et fins de post, créateurs, ressources), swipe file, système de veille (sources, premier run, transcripts), charte visuelle, profil et Publora, validation et premier brief.
- `strategie-contenu.md` : sections "Objectif et cadence" et "Formats et fins de post" ; les sources à flux vivent dans `sources-veille.json`.
- `docs/contenu.md` réécrit (huit phases, tableau des sous-skills, la veille du lundi, Publora) ; `CLAUDE.md` et `AGENTS.md` section 13 "Les modules de contenu" ; `README.md` (40 skills de premier niveau, sept masters, cinquante-trois sous-skills) ; notes `Marketing.md` et `LinkedIn.md` ; validateur étendu aux skills de contenu et aux scripts.

## [5.6.0] - 2026-09-20

Le premier master de contenu visuel : un post, une idée ou un framework devient une infographie 4:5 aux couleurs de la charte, avec un brief sauvegardé et l'image générée.

### Ajouté
- Master `infographie` (`10_Skills/infographie/`) : rôle de designer B2B, table de routage vers quatre sous-skills, logique "la charte d'abord, le brief avant l'image, une image à la fois", choix du moteur (outil d'image natif de Codex ou du client, sinon OpenAI, sinon fal.ai), rangement `Infographie-<sujet>_<date>.md` et `.png` dans `05_Departements/Marketing/LinkedIn/`.
- Sous-skills : `brief-visuel` (brief en neuf blocs : contexte, idée centrale, structure parmi quinze, contenu extrait, texte exact de chaque bloc, hiérarchie, direction artistique, prompt, checklist), `infographie-editoriale` (le one-pager premium aux couleurs de la charte, composants, densité, direction artistique par défaut), `carnet-manuscrit` (la page de carnet en noir et blanc, prompt de base en anglais), `sketchnote-tableau-blanc` (la photo de tableau blanc au marqueur, palette des feutres fixe, doodles utiles).
- Ressources : `bibliotheque-structures.md` (quinze structures avec le contenu qui les appelle, sept patterns de composition, la méthode pour choisir), `copywriting-visuel.md` (titre, points, badges, blocs prompt et conseil, longueurs, interdits), `lecture-charte.md` (ce qu'on extrait de `03_Branding/charte-visuelle.md`, l'ordre de priorité en cas de conflit, le style neutre quand la charte est vide), `prompt-generation.md` (anatomie du prompt en anglais avec le texte exact entre guillemets, réglages par moteur, checklist avant de lancer, relance d'une variante).
- `scripts/generer_image.py` : `--brief <brief.md>` (extrait le bloc "Prompt de génération"), `--prompt`, `--prompt-fichier` ; moteur automatique d'après les clés (`OPENAI_API_KEY` puis `FAL_KEY`), OpenAI `gpt-image-2` par défaut (repli de taille automatique), fal.ai `openai/gpt-image-2`, `fal-ai/nano-banana-pro` (aspect_ratio, resolution) ou tout autre modèle ; formats 4:5, 1:1, 3:2, 2:3, 16:9, 9:16 ; `--qualite`, `--resolution`, `--variante N`, `--out`, `--dry-run` qui affiche le moteur, le modèle, la taille et le corps de la requête sans rien lancer ; le prompt utilisé est écrit à côté de l'image (`.prompt.txt`).
- `03_Branding/charte-visuelle.md` : le gabarit que le master lit (palette par rôle, typographies, composants, ton, interdits, logo, exemples, style neutre de repli), avec la note `Branding.md` qui y renvoie ; `installer-contenu` le propose en fin d'installation ; la note `Marketing/LinkedIn/LinkedIn.md` nomme les fichiers d'infographie.
- `.env.example` : `OPENAI_API_KEY` et `FAL_KEY` (section génération d'images). `CLAUDE.md`, `AGENTS.md` : section 13. `README.md` : 47 skills.

### Modifié
- `docs/contenu.md` : la station "Transformer en visuel", les quatre briques réelles de `Marketing/` (les emails à l'audience sont dans `Go-to-Market/Mailing/`, un event est un projet), la charte, 47 skills. `docs/prospection.md` : le registre `Ciblage/requetes-booleennes.md` dans "Où vont les fichiers".
- Chemins périmés de la v3 corrigés : la note `Marketing/LinkedIn/LinkedIn.md` décrit des fichiers à plat (plus de `livrables/` ni `ressources/`), l'exemple `Contenu/LinkedIn/` de `CLAUDE.md`, `AGENTS.md` et `done` devient `Marketing/LinkedIn/`, le guide d'interview du second cerveau décrit les six départements et la règle des fichiers à plat.
- CI : `scripts/valider_gtm.py` tourne après `validate_skills.py` sur chaque push.

## [5.5.0] - 2026-09-20

Prospeo entre dans la stack en option : recherche d'entreprises et de personnes par filtres exacts, emails et mobiles vérifiés révélés en lot, et la méthode qui va avec.

### Ajouté
- Client `Prospeo` dans `_commun/gtm_common.py` (doc REST lue le 2026-09-20 : `X-KEY`, `POST /search-company`, `/search-person`, `/search-suggestions` gratuit, `/bulk-enrich-person`, `/bulk-enrich-company`, `GET /account-information`), avec la résolution des libellés (industries, lieux, technos, titres), la pagination à 1 crédit par page de 25, la pause de débit, et la normalisation vers les colonnes du module (`email_statut` `DELIVERABLE` pour `VERIFIED`, `prospeo_person_id`, `prospeo_company_id`).
- `trouver-entreprises --source prospeo` : industries, lieux (libellés canoniques, plusieurs lieux séparés par `;`), taille (tranches traduites : 11-50 devient 11-20 et 21-50), mots-clés, technos, CA, année, levée (`--levee`, `--levee-depuis-jours`, `--investisseurs`), ICP inverse (`--vend-a`, `--vend-a-tailles`), clients clés, intégrations, lookalike par domaine ou par texte libre (`--icp-texte`, `--lookalike-niveau`), actualités, postes ouverts ; `--lister-secteurs`, `--lister-lieux`, `--lister-technos`, `--lister-titres` (gratuits), `--total-seulement`, `--filtres-json` (le payload du tableau de bord tel quel), `--enregistrer`.
- `trouver-personnes --source prospeo` : titres (contient, `--titres-similaires --intensite`, ou `--booleen`), séniorités, départements, lieux, entreprises par domaine (500 max), `--par-entreprise`, `--email-verifie`, `--mobile-verifie`, `--cacher-deja-reveles`, `--changement-poste` (90 jours), `--total-seulement` (total et part d'emails vérifiés), puis `--reveler` et `--reveler-mobile` (révélation en lot, 50 par appel).
- `trouver-email --source prospeo` (second fournisseur sur ce que FullEnrich n'a pas trouvé, ou une liste venue de Prospeo) et `enrichir-entreprise --source prospeo` (50 par appel).
- `construire-liste/ressources/prospeo-recherche.md` : la méthode, en français et sans marque tierce : le workflow en trois temps (résoudre gratuitement, chercher la page 1 pour le total et la couverture, révéler en lot), les filtres par modèle d'affaires, les formes de filtres qu'on ne devine pas, le piège de la taxonomie d'industries, le contrôle sur 20 adresses, et où Prospeo intervient dans chaque sous-skill. `sourcer-entreprises`, `sourcer-personnes`, `nettoyer-verifier` (le contrôle sur 20 adresses) et `sources-par-besoin.md` y renvoient.
- `connecter-outils` : Prospeo en outil optionnel (`PROSPEO_API_KEY`, test gratuit `GET /account-information`), `.env.example`, `OUTILS.md` (état des connexions, quatre verbes), `docs/conventions-gtm.md`, `docs/prospection.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`.

## [5.4.0] - 2026-09-20

Ocean.io devient une source de recherche précise, la chaîne "entreprises, page LinkedIn, décisionnaires" tient en trois commandes, et l'URL LinkedIn d'une personne se retrouve sans compte.

### Ajouté
- `trouver-entreprises --source ocean` : recherche par filtres exacts (secteurs du référentiel, catégories, industries LinkedIn, mots-clés au moins un / tous / aucun sur la description, technos du site, taille, pays, villes, CA, année de création, levée, croissance d'effectif, lookalikes combinés, pertinence), avec `--lister-secteurs`, `--lister-technos`, `--lister-mots-cles`, `--lister-lieux` (référentiels et autocomplétion, gratuits), `--total-seulement` (comptage avant de payer) et `--enregistrer` (commande, filtres et volume dans `Ciblage/requetes-booleennes.md`). Le skill décrit la boucle où l'IA traduit une demande en filtres, compte, ajuste, puis lance.
- `trouver-personnes --source ocean` : les décisionnaires d'entreprises précises (par domaine, `peoplePerCompany`) ou d'une cible Ocean, par titres, séniorités, départements, pays ; `--changement-poste` devient `changedPositionAfter`. Options communes `--dirigeants` (20 titres), `--strict-titre` (anti faux positifs sur le titre actuel), `--format large` (une ligne par entreprise, `d1_*`, `d2_*`), `--enregistrer` ; une URL Sales Navigator déjà au registre reçoit son volume automatiquement.
- `enrichir-entreprise --source ocean` : enrichissement par domaine (`lookup/companies`, 1 000 par appel) qui pose la page LinkedIn, le siège, les secteurs, la taille, le CA, l'année, la description, les technos.
- `trouver-url-linkedin` réécrit en skill d'exécution avec un script : Unipile avec votre compte, ou `apify/google-search-scraper` sans compte (`"Prénom Nom" Entreprise site:linkedin.com/in`, 0,0025 $ par personne), confiance haute / moyenne / faible et correspondance d'entreprise par ligne, sur un CSV ou un nom.
- Registre des requêtes `Ciblage/requetes-booleennes.md` : créé à la première requête, colonne Volume mise à jour par les runs (`enregistrer_requete`, `maj_volume_requete` dans `_commun`).

### Modifié
- Client Ocean réécrit sur la spec OpenAPI lue le 2026-09-20 : chemins `https://api.ocean.io/api/public_api/v2` et `/v3` (les anciens `/v3/...` étaient faux), `creditsUsed` et `total` lus dans chaque réponse, `/preview` réservé aux comptes Enterprise avec repli sur une recherche de taille 1, normalisation commune des entreprises (page LinkedIn dans `medias.linkedin`) et des personnes ; `trouver-lookalikes` et `connecter-outils` corrigés en conséquence.
- `installer-gtm` : les phases 2 et 3 appliquent les sous-skills `definir-icp` et `cartographier-personas` (une seule méthode), et le test de volume passe par Ocean `--total-seulement` quand il est branché.
- `construire-liste` : la chaîne courte "entreprises précises vers leurs décisionnaires" ; `sourcer-entreprises`, `sourcer-personnes`, `sources-par-besoin.md` : Ocean en première source pour une cible décrite précisément et pour les décisionnaires par domaine.
- `OUTILS.md` (verbe `trouver_url_linkedin`, actor `apify/google-search-scraper`, Ocean sur trois verbes), `docs/conventions-gtm.md`, `docs/prospection.md`, `Ciblage.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`.

## [5.3.0] - 2026-09-20

Les requêtes Sales Navigator se construisent en texte, et trois signaux de proximité arrivent avec elles.

### Ajouté
- `construire-requete-salesnav` : un skill d'exécution et son script qui transforment des critères en texte (titres ou booléen, région, effectif, séniorité, niveau de relation, entreprise, mots-clés, listes) en URL de recherche Sales Navigator, personnes ou comptes, avec les quatre filtres à cocher (`--vues-profil`, `--suit-entreprise`, `--a-publie`, `--nouveau-poste`). Décode aussi une URL existante (`--decoder`), retrouve un id de région ou de secteur par Unipile (`--resoudre`, gratuit), prend les titres d'un persona de `contexte.md` (`--persona atl`) et enregistre la requête dans `Ciblage/requetes-booleennes.md` (`--enregistrer`). L'encodage est vérifié contre sept URL produites par l'interface.
- Trois sous-skills dans `detecter-signaux` : `visite-profil` (qui a consulté votre profil, 20 points proposés, j0 à j7), `abonnes-entreprise` (qui suit votre page, 15 points, j0 à j2), `a-publie` (qui a publié ce mois-ci dans votre cible : joignable sur LinkedIn, accroche dans son post, 10 points proposés, départageur). Tous trois passent par la requête Sales Navigator puis `trouver-personnes --signal`, avec le diff contre le run précédent par `dedoublonner --contre`.
- `trouver-personnes --signal <type>` : pose `signal_type`, `signal_date` (date du run), `signal_detail` et `fraicheur` sur chaque ligne d'une URL Sales Navigator à filtre (`visite_profil`, `abonne_entreprise`, `a_publie`, `changement_poste`).
- `enrichir-entreprise --techno --techno-source theirstack --recentes-jours N` : les technos d'une entreprise avec leur date de première détection, leur confiance et le nombre d'offres qui les citent (TheirStack `POST /companies/technologies`, 3 crédits par entreprise). Tirée des offres d'emploi, cette source voit les outils internes que le site ne montre pas et donne le signal `techno_ajout` sans attendre deux relevés ; `changement-techno` la préfère quand elle est branchée.
- `Unipile.parametres()` (ids de recherche LinkedIn et Sales Navigator) et `TheirStack.technographies()` dans `_commun/gtm_common.py`.

### Modifié
- `detecter-signaux` : table de routage et vérification d'un compte nommé étendues aux trois signaux ; `execution-signaux.md` décrit la voie Sales Navigator ; barème, fenêtres, taxonomie (17 bis), détection par signal (31 à 33), plays (11) et signaux de cœur mis à jour. Les abonnés de votre page entreprise ne sont plus "non listables" : ils le sont par Sales Navigator pour la page reliée à votre compte ; ceux d'un concurrent ou d'un profil personnel restent non listables.
- `changement-poste` : voie Sales Navigator sans crédit (`--nouveau-poste`, date à confirmer par `enrichir-personne`) ; `changement-techno` : TheirStack en première source datée, le détecteur de site pour les retraits ; `engagement-contenu` et `brief-avant-appel` : la visite de profil et les abonnés de la page passent par un script ; `multi-signaux` : `a_publie` départage à score égal ; `sourcer-personnes` : la requête se construit et s'enregistre par le nouveau skill.
- `contexte.md` section 4 et `installer-gtm` phase 4 : dix signaux proposés au lieu de sept, les trois nouveaux au prix de l'abonnement Sales Navigator ; `OUTILS.md`, `docs/conventions-gtm.md` (verbe, vocabulaire `signal_type`, TheirStack), `docs/prospection.md` (TheirStack, Sales Navigator), `README.md`, `CLAUDE.md`, `AGENTS.md`.

## [5.2.0] - 2026-09-19

Audit de cohérence du module GTM (20 bloquants, 12 doublons, 30 contradictions de chiffres corrigés) et tout en CLI.

### Ajouté
- Lemlist et Ocean.io par l'API en CLI, le MCP devient optionnel : `envoyer-sequence/scripts/envoyer_lemlist.py` (filtre, crée ou choisit la campagne, pousse les leads avec leurs variables, `--lancer`, `--pauser`, `--lister`), `verifier_reponses.py` lit les réponses email par l'API, `trouver-lookalikes/scripts/trouver_lookalikes.py` (aperçu gratuit puis recherche par lots de 10, 0,2 crédit par résultat).
- `enrichir-entreprise --posts` et `enrichir-personne --posts` (5 derniers posts, Unipile), `enrichir-entreprise --techno --techno-source predictleads --recentes-jours N`, `scraper-engagement --mes-posts N`, `detecter_signal.py --verification` et `--par-cible` sur les personnes, `dedoublonner --exclure-crm` et `--max-par-entreprise N`.
- Vocabulaires fixés dans `docs/conventions-gtm.md` section 8 : `email_statut` (valeurs FullEnrich), `seniorite`, `categorie_titre`, `tier`, `chaleur`, `signal_type` (une valeur canonique par signal), colonnes de réponse, `source`.
- Le validateur `scripts/valider_gtm.py` bannit "Apollo", les références périmées et les formules de félicitation dans les templates, et confronte tout actor cité à `OUTILS.md`.

### Changé
- Les runs de signaux vont dans `05_Departements/Go-to-Market/Signaux/` (`detecter-signaux_<type>-<source>-<sujet>_<date>.csv`) ; `qualifier-liste` écrit un seul fichier (toutes les lignes, colonne `exclu`) plus une copie des exclues ; préfixes `enrichir-entreprise_techno_` et `enrichir-entreprise_pubs_`.
- Fenêtres de fraîcheur alignées sur `detecter-signaux/ressources/fenetres-fraicheur.md` dans tout le module ; limites d'envoi alignées sur `GARDE-FOUS.md` (30 invitations, 50 DM, 100 interactions, note 300 caractères, 3 relances max tous canaux, chauffe 3 semaines, rebond alerte 3 % arrêt 5 %, catch-all 20 %, opt-out 48 h) ; séquence multicanal de référence LinkedIn J0, email J+2, email J+5, LinkedIn J+7, téléphone J+9 à J+12 ; email seul 3 emails max.
- Propriétaires uniques : no-show dans `cold-call`, nomination dans `changement-poste`, IPO dans `levee-fonds`, client d'un concurrent dans `signaux-concurrents` ; ouvertures et clics d'email retirés du barème ; abonnés d'une page retirés (non listables) ; le signal brut ne s'écrit plus dans aucun template.
- Colonnes citées par les sous-skills alignées sur celles que les scripts écrivent ; scopes HubSpot complétés (deals, notes, tâches).

## [5.1.0] - 2026-09-19

Deux sources optionnelles pour les signaux.

### Ajouté
- PredictLeads et TheirStack comme secours du verbe detecter_signal, par le même script (`--source predictleads`, `--source theirstack`) : événements d'entreprise (expansion, partenariat, lancement, nomination, rachat), levées, offres actives, intent (recrute et utilise une techno), offres filtrées par techno citée. Nouveaux types `events` et `intent`. Aussi dans `scraper-offres-emploi` (`--source predictleads|theirstack`) et `enrichir-entreprise --techno --source predictleads` (détections datées, `--recentes-jours`).
- Clients `PredictLeads` et `TheirStack` dans `10_Skills/_commun/gtm_common.py`, tests dans `connecter-outils` (`--outil predictleads|theirstack`), ligne `signaux_secours:` dans `OUTILS.md`, clés dans `.env.example`.

## [5.0.0] - 2026-09-19

Le module GTM : la prospection reconstruite en méthode et exécution séparées.

### Ajouté
- Quatre masters de méthode dans `10_Skills/` : `construire-liste` (8 sous-skills), `detecter-signaux` (8 sous-skills, barème de signaux, 137 déclencheurs, 11 plays), `cold-email` (9 sous-skills, 13 frameworks, 34 templates, relecteurs, infra email), `cold-call` (5 sous-skills sur la méthode d'appel en 5 temps). Chaque master route vers ses sous-skills, chaque sous-skill décrit le travail en verbes.
- Quatorze skills d'exécution, un par verbe, avec scripts Python (`--help`, `--dry-run`, coût annoncé) et une bibliothèque commune `10_Skills/_commun/` : `trouver-entreprises`, `trouver-lookalikes`, `trouver-personnes`, `enrichir-personne`, `enrichir-entreprise` (`--techno`, `--pubs`), `trouver-email`, `trouver-telephone`, `scraper-offres-emploi`, `scraper-engagement`, `qualifier-liste`, `dedoublonner`, `crm`, `envoyer-sequence`, `verifier-reponses`.
- `installer-gtm` (onboarding en 8 phases : offre, ICP en 3 couches scoré sur 100, personas ATL et BTL, 5 signaux prioritaires, canaux, outils, validation, premier run) remplace `installer-prospection`. `connecter-outils` étendu à 7 outils.
- Dans `05_Departements/Go-to-Market/` : `OUTILS.md` (quel outil fait quel verbe, priorité Apify ou API, canal LinkedIn), `GARDE-FOUS.md`, `Ciblage/` (décisionnaires par taille, requêtes booléennes, mots-clés d'exclusion), `Signaux/`. `contexte.md` réécrit : il traduit `02_Contexte/` en critères de prospection, sans le recopier.
- `docs/prospection.md` (mode d'emploi du module) et `docs/conventions-gtm.md` (comment les skills GTM sont écrits), `scripts/valider_gtm.py`.

### Changé
- Stack fermée à 7 outils : Apify par défaut pour tout scraping et tout signal, Unipile pour le compte LinkedIn, Crustdata en secours API, FullEnrich seul pour l'enrichissement contact, Ocean.io pour les lookalikes, Lemlist pour l'envoi, HubSpot pour le CRM.
- `.env.example` couvre les 7 outils, les cookies Sales Navigator et les limites d'envoi.

### Archivé
- Les 22 skills de prospection v3 (Crustdata en dur, sans orchestrateur) dans `11_Archives/skills-prospection-v3/`, avec l'ancien `contexte.md` et l'ancien guide.

## [4.0.0] - 2026-09-18

Le second cerveau version 4 : douze dossiers numérotés, projets, départements, clients, fiches courtes.

### Changé
- Arbre à plat et numéroté : `00_Inbox` à `11_Archives`. `Marketing/` et `Vente/` deviennent six départements dans `05_Departements/` (Strategie, Marketing, Go-to-Market, Vente, Produit, Finance-Compta). `Produit-Client/` devient `06_Clients/`. `Veille/` rejoint `08_Ressources/`. Les skills vivent dans `10_Skills/`.
- Un projet (initiative avec une fin) vit dans `04_Projets/` et part en archive quand ses Étapes sont cochées. Un département n'a pas de fin. Un client est une mission signée.
- Fin des sous-dossiers par étape (`livrables/`, `ressources/`, `input/`, `output/`) : fichiers à plat, sous-dossier par nature seulement au-delà d'une dizaine d'items. `sources/` reste pour le brut volumineux.
- Fiches courtes, six sections maximum : Mission, Périmètre, Objectif (frontmatter `objectif:`), Cadre avec décisions datées, Étapes, Où on en est, Key Notes. Plus de bloc ETAT, de Reprise ni d'Historique : l'historique vit dans `_log.md` et le journal.
- Sept templates dans `08_Ressources/templates/` : projet, departement, client, journal-jour, journal-semaine, reflexion, livrable.
- `/done` réécrit Où on en est, date les décisions dans Cadre, coche les Étapes, propose l'archivage d'un projet fini. `/lint` gagne un dixième contrôle : l'audit de contexte d'un dossier (contradictions, répétitions, obsolète, manques, mal rangé). `/inbox-processor`, `/import` et `/weekly-review` suivent la nouvelle carte.
- `installer-second-cerveau` : une étape pour valider la fiche de chaque département et créer les premiers projets, avant les clients.
- `07_Meeting/` simplifié : Clients, Prospects, Interne, Autres.
- Imports `@` du `CLAUDE.md` avec l'espace échappé (`@01_About-Me/...`), seule forme qui charge.

### Ajouté
- `/create-skill` : transformer une tâche faite trois fois à la main en skill, avec cadrage, étapes, test et écriture du SKILL.md.

### Retiré
- `Marketing/Event/` : un event est un projet dans `04_Projets/`.

## [3.2.0] - 2026-09-18

Une bibliothèque de skills, trois moteurs : Claude Code, Codex, OpenCode.

### Changé (rupture avec 3.1)
- **Les 46 skills vivent dans `Skills/`**, un dossier par skill, à la racine. Plus de skills scopés dans `Vente/.claude/skills/` ni `Marketing/.claude/skills/` : ils sont visibles depuis n'importe quel dossier, et "Installe ma prospection" ou "Installe mon contenu" se tapent depuis la racine.
- `.claude/skills` (Claude Code) et `.agents/skills` (Codex) sont des liens symboliques vers `Skills/`, versionnés. Sur Windows sans mode développeur, l'installeur propose des copies.
- Le `.env` des outils de prospection passe de `Vente/.env` à la racine du workspace. Les scripts le trouvent d'eux-mêmes.

### Ajouté
- `AGENTS.md` : la carte du `CLAUDE.md` reprise pour Codex et OpenCode, avec la lecture explicite d'`About-Me/` (ils ne suivent pas les imports `@`).
- `opencode.json` : charge `About-Me/` et pointe `skills.paths` sur `./Skills`.
- Section 11 du `CLAUDE.md`, section du README, entrée dans le validateur et `install.sh`.

## [3.1.0] - 2026-09-17

`Meeting/` se range par relation, plus par mois.

### Changé
- **`Meeting/` a cinq dossiers** : `Clients/` (sous-dossiers `Actuels/<Nom>/`, `Coaching/<Nom>/`, `Anciens-clients/<Nom>/`, `Ateliers-cold-call/`, `Ateliers-collectifs/`), `Events/` (`Live/`, `Challenge/`, vos events marketing), `Prospects/YYYY-MM/`, `Interne/YYYY-MM/`, `Autres/YYYY-MM/`. La règle de routage en huit étapes, premier match gagne, est dans `Meeting/Meeting.md`. Un prospect passe dans `Clients/` au troisième call ou dès qu'un atelier ou un onboarding est planifié ; un dossier terminé glisse dans `Anciens-clients/` tel quel.
- `CLAUDE.md`, `README.md`, `/inbox-processor` et `installer-second-cerveau` pointent vers le nouveau routage.

## [3.0.0] - 2026-09-16

Une seule structure, pour votre workspace comme pour ceux de vos clients. Le parcours en trois jours devient trois modules installables dans l'ordre que vous voulez, une fois le second cerveau en place.

### Changé (rupture avec 2.x)
- **Rangement à plat par fonction**, plus de `Projects/` ni de `input/ output/ ressources` imbriqués : `About-Me/`, `Contexte/`, `Branding/`, `Ressources/`, `Inbox/`, `Journal/`, `Veille/`, `Meeting/`, `Produit-Client/`, `Marketing/`, `Vente/`, `Strategie/`, `Archives/`.
- **Une note par dossier de travail**, du même nom que le dossier (`Vente/Vente.md`) : rôle, conventions, organisation, bloc ETAT, reprise, historique. Elle remplace le `CLAUDE.md` de sous-dossier. Un `_log.md` par dossier, une ligne par session.
- **`Journal/`** remplace `Intelligence/Daily logs/` : un fichier par jour, écrit par `/done`, un par semaine par `/weekly-review`. Le template à emojis disparaît.
- **`Veille/`** remplace `Intelligence/` : `sources/` (le brut), `wiki/` (la connaissance), `INDEX.md`, `LOG.md`.
- `Projects/Prospection/` devient `Vente/` avec quatre sous-dossiers typés (`Listes-prospection/`, `Messages/`, `Propositions/`, `Pipeline/`). Les 25 skills restent scopés dans `Skills/`.
- `Projects/Contenu/` devient `Marketing/` avec sept briques (`LinkedIn/`, `Newsletter/`, `Mailing/`, `Event/`, `Video/`, `Slides/`, `Site-vitrine/` à créer au besoin). Les 10 skills restent scopés dans `Skills/`, les ressources de contenu vivent dans `Marketing/LinkedIn/ressources/`.
- `Projects/Clients/` devient `Produit-Client/`, `Projects/Strategie/` devient `Strategie/`.
- Plus de notion de jour 1, 2, 3. Les trois phrases restent : "Installe mon second cerveau", "Installe ma prospection", "Installe mon contenu". Les deux dernières lisent le second cerveau et n'interviewent que sur ce qui manque.
- `/done` réécrit sur trois niveaux : le journal du jour, la note du dossier touché (ETAT, Reprise, Historique), son `_log.md`. Il propose un diff pour `About-Me/`, `Contexte/` et `Branding/` au lieu d'y écrire.
- `docs/` : un fichier par module, sans numéro de jour.

### Ajouté
- `/lint` : neuf contrôles de santé du workspace (notes manquantes, ETAT périmés, contradictions, frontmatter, versions non archivées, fichiers à la racine, tirets cadratins, chemins morts, dossiers orphelins). Lecture seule jusqu'à validation.
- `Ressources/templates/` : `note-de-dossier.md`, `note-de-dossier-client.md`, `journal-jour.md`.
- `Branding/`, `Meeting/`, `Archives/` avec leur note.

## [2.0.0] - 2026-09-11

Refonte complète : le dépôt devient un workspace Claude Code prêt à ouvrir, structuré selon les pratiques documentées de gestion du contexte (skills scopés par dossier, CLAUDE.md imbriqués, imports, une vérité par information, lecture du contexte à l'exécution).

### Changé (rupture avec 1.x)
- Le dépôt EST le workspace : `git clone`, ouvrir, "Installe mon second cerveau". Plus de copie de skills dans `~/.claude`.
- Les trois installeurs partagent la même nomenclature et la même phrase : `installer-second-cerveau` (ex setup-claude-infrastructure), `installer-prospection` (ex installer-gtm), `installer-contenu` (ex linkedin-system-installer). Chacun lit ce que le précédent a produit.
- L'OS-GTM devient `Projects/Prospection/`, ses 25 skills sont scopés à ce dossier. `contexte.md` ne contient plus que ce qui est propre à la prospection et pointe vers `Contexte/` pour l'offre, la cible et la voix.
- Le pack LinkedIn devient `Projects/Contenu/`, ses 10 skills sont scopés à ce dossier. Le mécanisme de placeholders (`apply_profile.py` et jetons entre doubles accolades) est supprimé : les skills lisent `Contexte/` et `ressources/` à chaque exécution. Les 7 fichiers-gabarits de références sont consolidés en 3 fichiers de `ressources/` (stratégie, posts de référence, swipe file).
- `linkedin-interview-2` devient `linkedin-interview` et range ses pépites dans `Projects/Contenu/ressources/banque-vecu.md`.
- `install.sh` ne sert plus qu'à ajouter les modules à un workspace existant (`--into`).

### Ajouté
- Les 8 skills du second cerveau, à la racine : `done`, `daily-review`, `weekly-review`, `inbox-processor`, `import`, `map-process`, `notes-permanentes`, `connect-mcp`.
- Le CLAUDE.md racine orchestrateur : diagnostic de l'état d'installation au premier message, routage du contexte, routage des livrables, rituels, imports d'ABOUT.ME.
- Le squelette complet : `ABOUT.ME/` et `Contexte/` avec gabarits, `Inbox/`, `Intelligence/` (schéma du wiki, INDEX, LOG), `Projects/{Clients,Strategie}/` avec leur CLAUDE.md.
- `docs/` : un fichier par jour du parcours.
- `anti-ai-voice.md` en version générique.
- Le validateur vérifie aussi l'absence de placeholders résiduels et la taille des CLAUDE.md (200 lignes).

## [1.1.0] - 2026-09-09

### Ajouté
- Le pack contenu LinkedIn : 10 skills qui produisent des posts dans votre voix, de la veille au visuel.
  - `linkedin-system-installer` : interview + script `apply_profile.py` qui personnalise les 8 skills du pack à partir d'un profil JSON (re-runnable, garde une copie `.template`).
  - `linkedin-writing-core` : le socle éditorial (voix, formatage, système de hooks) avec 7 fichiers de références dont une bibliothèque de hooks et 11 templates de posts.
  - `linkedin-ideation` : veille sur vos sources et brief éditorial hebdomadaire, avec 4 fichiers de références.
  - `linkedin-educational`, `linkedin-storytelling`, `linkedin-hot-take`, `linkedin-lead-magnet` : un skill par intention de post.
  - `viral-hook-writer` et `linkedin-post-optimizer` : les 2 lignes avant le "voir plus", puis le contrôle qualité final.
  - `linkedin-interview-2` : fouille votre vécu pour produire la matière première du contenu.

## [1.0.0] - 2026-09-09

### Ajouté
- `skills/setup-claude-infrastructure` : le skill qui construit le second cerveau (CLAUDE.md, ABOUT.ME, 7 fichiers de contexte, structure Projects, MCP, premier skill), avec son guide complet de prompts d'interview.
- `os-gtm/` : l'OS de prospection complet, 25 skills, du ciblage au suivi des réponses (Unipile, Crustdata, FullEnrich, Lemlist, Apify).
- `skills/find-skills` : découverte et installation de skills depuis l'écosystème ouvert (skills.sh).
- `install.sh` : installation en une commande (skills globaux ou locaux, déploiement de l'OS-GTM dans un workspace).
- `scripts/validate_skills.py` + workflow GitHub Actions : vérification du frontmatter de chaque SKILL.md, absence de tirets cadratins et de clés API.
