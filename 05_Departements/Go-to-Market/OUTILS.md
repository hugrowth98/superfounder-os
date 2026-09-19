# OUTILS.md : quel outil fait quoi

> Ce fichier est rempli une fois par `installer-gtm` (via `connecter-outils`) et lu par tous les skills d'exécution avant chaque action. Il ne pose jamais de question à l'utilisateur en cours de session. Pour changer d'outil : modifier la ligne, rien d'autre.

## Règle de priorité

`priorite: apify` si l'utilisateur a un compte Apify (par défaut). `priorite: api` sinon : chaque verbe utilise son outil API dédié.

```
priorite: [apify | api]
canal_linkedin: [unipile | lemlist]      choisi à l'onboarding
canal_email: lemlist
crm: [hubspot | aucun]
signaux_secours: [predictleads, theirstack | aucun]   outils optionnels branchés pour les événements et l'intent
```

## Carte verbe vers outil

| Verbe | Principal (priorité apify) | Principal (priorité api) | Secours | Actor Apify / point d'entrée |
|---|---|---|---|---|
| trouver_entreprises | Apify | Crustdata | Unipile (Sales Nav comptes) | `compass/crawler-google-places` (local), `harvestapi/linkedin-company-search` (filtres LinkedIn), `code_crafter/leads-finder` (bases larges, une ligne par entreprise), `curious_coder/linkedin-sales-navigator-search-scraper` (URL Sales Nav comptes, cookies du .env) ; Crustdata `POST /v1/companies/search` |
| trouver_lookalikes | Ocean.io | Ocean.io | aucun | API `POST /v3/search/companies` avec `lookalikeDomains` (10 domaines par lot, 0,2 crédit par résultat, `/preview` gratuit) ; MCP Ocean en option pour explorer à la main |
| trouver_personnes | Apify | Crustdata | Unipile (recherche classique ou Sales Nav) | `harvestapi/linkedin-profile-search` (filtres, sans cookies), `harvestapi/linkedin-company-employees` (depuis des URLs entreprise), `curious_coder/linkedin-sales-navigator-search-scraper` (URL Sales Nav leads, cookies du .env) ; Crustdata `POST /screener/persondb/search/` |
| enrichir_personne | Unipile (profil) + FullEnrich (contact) | idem | Apify `harvestapi/linkedin-profile-scraper` | Unipile `GET /api/v1/users/{id}` ; FullEnrich `POST /contact/enrich/bulk` |
| enrichir_entreprise | Unipile (page) + Crustdata | idem | Apify `harvestapi/linkedin-company` | Unipile `GET /api/v1/linkedin/company/{id}` ; Crustdata `GET /screener/company?company_domain=` |
| trouver_email | FullEnrich | FullEnrich | aucun | `POST /api/v2/contact/enrich/bulk`, champ `contact.emails` (1 crédit par email trouvé) |
| trouver_telephone | FullEnrich | FullEnrich | aucun | idem, champ `contact.phones` (10 crédits par mobile trouvé) |
| detecter_signal (master `detecter-signaux`) | Apify | Apify | PredictLeads (`--source predictleads` : levées, événements d'entreprise, offres ; quota mensuel), TheirStack (`--source theirstack` : offres, intent jobs + techno ; 1 crédit par résultat) | `signalbase/signalbase-api` (funding, acquisitions, hiring, job-changes, investors, companies ; 0,04 $ par résultat) ; PredictLeads `discover/financing_events`, `discover/news_events`, `discover/job_openings` ; TheirStack `jobs/search`, `companies/search` |
| scraper_offres_emploi | Apify | Apify | PredictLeads (`--source predictleads`), TheirStack (`--source theirstack`, filtre par techno citée) | `tagadanar/linkedin-jobs-scraper` (LinkedIn), `borderline/indeed-scraper` (Indeed), `signalbase/signalbase-api` signalType=hiring ; PredictLeads `discover/job_openings` ; TheirStack `jobs/search` |
| scraper_engagement | Unipile | Unipile | Apify | Unipile `posts/{id}/reactions` et `/comments` ; secours `harvestapi/linkedin-post-comments`, `harvestapi/linkedin-post-reactions` |
| detecter_techno (`enrichir-entreprise --techno`) | Apify | Apify | PredictLeads (`--source predictleads` : détections datées, `first_seen_at`, sans diff à faire) | `scrapemint/website-tech-stack-detector` ; PredictLeads `companies/{domaine}/technology_detections` |
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
| PredictLeads (optionnel) | [ ] | | |
| TheirStack (optionnel) | [ ] | | |
