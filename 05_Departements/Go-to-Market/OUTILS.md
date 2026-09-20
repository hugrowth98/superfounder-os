# OUTILS.md : quel outil fait quoi

> Ce fichier est rempli une fois par `installer-gtm` (via `connecter-outils`) et lu par tous les skills d'exécution avant chaque action. Il ne pose jamais de question à l'utilisateur en cours de session. Pour changer d'outil : modifier la ligne, rien d'autre.

## Règle de priorité

`priorite: apify` si l'utilisateur a un compte Apify (par défaut). `priorite: api` sinon : chaque verbe utilise son outil API dédié.

```
priorite: [apify | api]
canal_linkedin: [unipile | lemlist]      choisi à l'onboarding
canal_email: lemlist
crm: [hubspot | aucun]
signaux_secours: [predictleads, theirstack | aucun]   outils optionnels branchés pour les événements, l'intent et les technos datées
```

## Carte verbe vers outil

| Verbe | Principal (priorité apify) | Principal (priorité api) | Secours | Actor Apify / point d'entrée |
|---|---|---|---|---|
| trouver_entreprises | Apify | Crustdata | Unipile (Sales Nav comptes) ; Ocean.io (`--source ocean`) et Prospeo (`--source prospeo`) pour une cible décrite précisément | `compass/crawler-google-places` (local), `harvestapi/linkedin-company-search` (filtres LinkedIn), `code_crafter/leads-finder` (bases larges, une ligne par entreprise), `curious_coder/linkedin-sales-navigator-search-scraper` (URL Sales Nav comptes, cookies du .env) ; Crustdata `POST /v1/companies/search` ; Ocean.io `POST /api/public_api/v3/search/companies` (secteurs exacts, mots-clés, technos, taille, villes, CA, levée, croissance ; référentiels et comptage `--total-seulement`) ; Prospeo `POST /search-company` (industries, lieux et technos résolus par `/search-suggestions` gratuit, mots-clés, taille, CA, levée, ICP inverse `--vend-a`, clients clés, intégrations, lookalike par domaine ou texte, actualités, postes ouverts ; 1 crédit par page de 25 ; `--filtres-json` = payload du tableau de bord) |
| trouver_lookalikes | Ocean.io | Ocean.io | aucun | API `POST /api/public_api/v3/search/companies` avec `lookalikeDomains` (10 domaines par lot ; `creditsUsed` affiché ; `/preview` gratuit sur un compte Enterprise, sinon comptage par une recherche de taille 1) ; MCP Ocean en option pour explorer à la main |
| construire_requete_salesnav | interne | interne | Unipile pour les ids de région, secteur, liste (gratuit) | `construire-requete-salesnav/scripts/construire_requete_salesnav.py` : critères en texte vers URL Sales Navigator (personnes ou comptes), décodage d'une URL, ids via Unipile `GET /api/v1/linkedin/search/parameters` |
| trouver_personnes | Apify | Crustdata | Unipile (recherche classique ou Sales Nav) | `harvestapi/linkedin-profile-search` (filtres, sans cookies), `harvestapi/linkedin-company-employees` (depuis des URLs entreprise), `curious_coder/linkedin-sales-navigator-search-scraper` (URL Sales Nav leads, cookies du .env) ; Crustdata `POST /screener/persondb/search/` ; Ocean.io `POST /api/public_api/v3/search/people` (`--source ocean` : décisionnaires par domaine ou par cible, `peoplePerCompany`, `changedPositionAfter`) ; Prospeo `POST /search-person` (`--source prospeo` : titres contient, similaires ou booléen, séniorités, départements, lieux canoniques, 500 domaines max, `max_person_per_company`, email ou mobile vérifié, contacts déjà révélés cachés ; 1 crédit par page de 25) puis `POST /bulk-enrich-person` (`--reveler` : 1 crédit par email vérifié, `--reveler-mobile` : 10 par mobile) ; `--dirigeants`, `--strict-titre`, `--format large` ; `--signal` pose `visite_profil`, `abonne_entreprise`, `a_publie`, `changement_poste` sur une URL Sales Nav à filtre |
| trouver_url_linkedin | Unipile | Unipile | Apify `apify/google-search-scraper` (sans compte LinkedIn) | Unipile `POST /api/v1/linkedin/search` (classique, "Prénom Nom Entreprise") ; Google `"Prénom Nom" Entreprise site:linkedin.com/in`, premier résultat, confiance par ligne |
| enrichir_personne | Unipile (profil) + FullEnrich (contact) | idem | Apify `harvestapi/linkedin-profile-scraper` | Unipile `GET /api/v1/users/{id}` ; FullEnrich `POST /contact/enrich/bulk` |
| enrichir_entreprise | Unipile (page) + Crustdata | idem | Apify `harvestapi/linkedin-company` ; Ocean.io par domaine (`--source ocean`, 1 000 par appel) ; Prospeo (`--source prospeo`, 50 par appel, 1 crédit par entreprise) | Unipile `GET /api/v1/linkedin/company/{id}` ; Crustdata `GET /screener/company?company_domain=` ; Ocean.io `POST /api/public_api/v2/lookup/companies` ; Prospeo `POST /bulk-enrich-company` |
| trouver_email | FullEnrich | FullEnrich | Prospeo (`--source prospeo`, second fournisseur : ce que FullEnrich n'a pas trouvé, ou une liste venue de Prospeo) | `POST /api/v2/contact/enrich/bulk`, champ `contact.emails` (1 crédit par email trouvé) ; Prospeo `POST /bulk-enrich-person` (1 crédit par email vérifié trouvé, 50 par appel, gratuit sous 90 jours) |
| trouver_telephone | FullEnrich | FullEnrich | aucun | idem, champ `contact.phones` (10 crédits par mobile trouvé) |
| detecter_signal (master `detecter-signaux`) | Apify | Apify | PredictLeads (`--source predictleads` : levées, événements d'entreprise, offres ; quota mensuel), TheirStack (`--source theirstack` : offres, intent jobs + techno ; 1 crédit par résultat) | `signalbase/signalbase-api` (funding, acquisitions, hiring, job-changes, investors, companies ; 0,04 $ par résultat) ; PredictLeads `discover/financing_events`, `discover/news_events`, `discover/job_openings` ; TheirStack `jobs/search`, `companies/search` |
| scraper_offres_emploi | Apify | Apify | PredictLeads (`--source predictleads`), TheirStack (`--source theirstack`, filtre par techno citée) | `tagadanar/linkedin-jobs-scraper` (LinkedIn), `borderline/indeed-scraper` (Indeed), `signalbase/signalbase-api` signalType=hiring ; PredictLeads `discover/job_openings` ; TheirStack `jobs/search` |
| scraper_engagement | Unipile | Unipile | Apify | Unipile `posts/{id}/reactions` et `/comments` ; secours `harvestapi/linkedin-post-comments`, `harvestapi/linkedin-post-reactions` |
| detecter_techno (`enrichir-entreprise --techno`) | Apify (le site) ; TheirStack si branché (les offres, daté) | idem | TheirStack (`--techno-source theirstack --recentes-jours N` : technographies tirées des offres, `first_date_found`, outils internes compris, 3 crédits par entreprise), PredictLeads (`--techno-source predictleads` : détections datées, `first_seen_at`) | `scrapemint/website-tech-stack-detector` ; TheirStack `POST /companies/technologies` ; PredictLeads `companies/{domaine}/technology_detections` |
| scraper_pubs (`enrichir-entreprise --pubs`) | Apify | Apify | aucun | `curious_coder/facebook-ads-library-scraper` (Meta), `s-r/linkedin-ads-library` (LinkedIn) |
| qualifier_liste | interne (Claude) | interne | aucun | lit `05_Departements/Go-to-Market/contexte.md` |
| dedoublonner | interne + HubSpot | interne + HubSpot | aucun | HubSpot search API |
| lire_crm, pousser_crm | HubSpot | HubSpot | aucun | HubSpot `deals/search`, `contacts/batch/upsert`, `notes`, `tasks` (skill `crm`) |
| envoyer_sequence (email) | Lemlist | Lemlist | aucun | API `POST /campaigns`, `POST /campaigns/{id}/leads/`, `/start`, `/pause` (script `envoyer_lemlist.py`) ; MCP Lemlist en option |
| envoyer_sequence (LinkedIn) | selon `canal_linkedin` | idem | aucun | Unipile `POST /api/v1/users/invite` puis `POST /api/v1/chats` (script `envoyer-sequence`), ou Lemlist multicanal |
| verifier_reponses | Unipile + Lemlist | idem | aucun | Unipile `GET /api/v1/chats`, `/messages`, `/attendees` ; Lemlist API `GET /activities?type=emailsReplied` et `linkedinReplied` |

## Actors Apify vérifiés (Store, palier BRONZE, le 2026-09-19)

Les prix servent aux estimations affichées par les scripts avant tout run (`apify_run.PRIX`). Un actor absent de cette table n'est pas utilisé par un skill.

| Actor | Usage | Prix |
|---|---|---|
| `compass/crawler-google-places` | commerces et services locaux | 0,003 $ par lieu, +0,001 $ par filtre |
| `harvestapi/linkedin-company-search` | entreprises par filtres LinkedIn | 0,002 $ (short) ou 0,004 $ (full) par entreprise |
| `code_crafter/leads-finder` | base large par industrie, taille, CA, financement | 0,002 $ par lead + 0,02 $ par run |
| `curious_coder/linkedin-sales-navigator-search-scraper` | URL Sales Navigator (leads ou comptes), cookies requis | 0,005 $ par résultat |
| `harvestapi/linkedin-profile-search` | personnes par filtres LinkedIn, sans cookies | 0,10 $ par page de 25 (short), +0,004 $ par profil (full) |
| `harvestapi/linkedin-company-employees` | personnes depuis des URLs d'entreprise | 0,003 $ par profil (short) + 0,02 $ par requête |
| `harvestapi/linkedin-profile-scraper` | profil complet depuis une URL | 0,004 $ par profil |
| `harvestapi/linkedin-company` | page entreprise depuis une URL ou un nom | 0,004 $ par entreprise |
| `apify/google-search-scraper` | URL LinkedIn d'une personne depuis son nom (recherche Google) | 0,0025 $ par page de résultats + 0,001 $ par run |
| `signalbase/signalbase-api` | levées, acquisitions, recrutement, changements de poste | 0,04 $ par résultat |
| `tagadanar/linkedin-jobs-scraper` | offres LinkedIn | 0,0018 $ par offre (+0,0018 $ avec details) |
| `borderline/indeed-scraper` | offres Indeed | 0,005 $ par offre |
| `harvestapi/linkedin-post-comments` | commentaires d'un post | 0,002 $ par commentaire |
| `harvestapi/linkedin-post-reactions` | réactions d'un post | 0,002 $ par reaction |
| `scrapemint/website-tech-stack-detector` | stack technique d'un domaine | 0,01 $ par domaine avec détection |
| `curious_coder/facebook-ads-library-scraper` | pubs Meta | 0,00075 $ par pub |
| `s-r/linkedin-ads-library` | pubs LinkedIn | 0,005 $ par pub |

## État des connexions

| Outil | Clé présente | Testée le | Compte / quota |
|---|---|---|---|
| Apify | [ ] | | |
| Unipile | [ ] | | |
| Crustdata | [ ] | | |
| FullEnrich | [ ] | | |
| Ocean.io | [ ] | | |
| Lemlist | [ ] | | |
| HubSpot | [ ] | | |
| Prospeo (optionnel) | [ ] | | |
| PredictLeads (optionnel) | [ ] | | |
| TheirStack (optionnel) | [ ] | | |
| Publora (optionnel, contenu) | [ ] | | |
