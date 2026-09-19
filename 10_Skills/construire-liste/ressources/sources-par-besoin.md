# Sources par besoin

Lu par `sourcer-entreprises`, `sourcer-personnes` et le master pour planifier une chaîne. Une seule source couvre environ 60 % d'un marché, deux sources environ 85 %, trois environ 92 %. Deux sources bien choisies donnent 40 % d'entreprises de plus qu'une seule, et 30 à 60 % de doublons à retirer ensuite.

## Trois catégories de sources

| Catégorie | Ce que c'est | Intention du prospect | Volume |
|---|---|---|---|
| Chaudes | des gens ou des entreprises qui ont déjà un lien avec l'utilisateur : réactions à ses posts, inscrits à sa newsletter, participants à son événement, affaires perdues du CRM (`crm lire --statut perdus`) | la plus forte | faible, mais chaque ligne vaut dix lignes froides |
| Bases larges | recherche par critères dans une base : Sales Navigator, `code_crafter/leads-finder`, Crustdata | aucune, c'est le fit qui compte | fort |
| Spécialisées | cartes pour le local, annuaires professionnels, classements, lookalikes, signaux | moyenne à forte selon la source | moyen |

Une liste sérieuse mélange une source chaude quand elle existe, une base large pour le volume, une source spécialisée quand la cible n'est pas bien représentée sur LinkedIn.

## Matrice besoin vers source vers verbe vers outil

| Besoin | Source | Verbe | Outil et point d'entrée | Volume par run | Ce qu'on récupère |
|---|---|---|---|---|---|
| Beaucoup d'entreprises par secteur, effectif, zone | base large | `trouver_entreprises` | Apify, actor base large de `05_Departements/Go-to-Market/OUTILS.md` (`code_crafter/leads-finder` ou son remplaçant : il interroge une base de contacts et rend une ligne par entreprise, dédoublonnée par domaine, avec un dirigeant trouvé au passage) ; Crustdata en priorité api | milliers | entreprise, domaine, secteur, effectif, ville, pays, dirigeant_trouve |
| Entreprises avec les filtres LinkedIn (croissance, secteur LinkedIn, mots-clés) | Sales Navigator | `trouver_entreprises` | Unipile avec le compte de l'utilisateur (abonnement Sales Navigator requis pour les filtres avancés) | 2 500 par recherche | entreprise, linkedin_entreprise_url, effectif, secteur, ville |
| Personnes par titre, séniorité, zone | profils LinkedIn | `trouver_personnes` | Apify `harvestapi/linkedin-profile-search` ; Unipile Sales Navigator ; Crustdata en priorité api | 2 500 par recherche | prenom, nom, titre, entreprise, linkedin_url, ville |
| Les bonnes personnes chez une liste précise d'entreprises | pages entreprise | `trouver_personnes` | Apify `harvestapi/linkedin-company-employees` avec `linkedin_entreprise_url` | 1 à 5 par entreprise | prenom, nom, titre, linkedin_url |
| Des entreprises qui ressemblent à mes clients | lookalikes | `trouver_lookalikes` | Ocean.io, recherche par domaines de référence (10 domaines par appel, fusionnés en une graine) | centaines | entreprise, domaine, secteur, effectif, pays |
| Commerces, cabinets, artisans dans une ville | cartes | `trouver_entreprises` | Apify, actor Google Maps de `05_Departements/Go-to-Market/OUTILS.md` | centaines par ville et catégorie | entreprise, domaine, telephone_entreprise, ville, secteur, note_google, nb_avis |
| Une niche : annuaire d'une fédération, exposants d'un salon, classement sectoriel | annuaire | `trouver_entreprises` | Apify, scraping de la page de l'annuaire | dizaines à centaines | entreprise, domaine, ville, parfois telephone |
| Ceux qui ont le problème en ce moment | signaux | `detecter_signal`, `scraper_offres_emploi`, `scraper_engagement` | master `detecter-signaux` | variable | entreprise, signal_type, signal_date, signal_detail |
| Ceux que l'utilisateur connaît déjà | CRM | `lire_crm` | HubSpot, `crm lire --statut perdus` (affaires perdues, à filtrer sur `date_cloture` de plus de 6 mois) ; pas d'export "churnés" ni "sans affaire" | dizaines à centaines | contact et entreprise de l'affaire, `affaire`, `montant`, `date_cloture`, `source = hubspot` |
| Compléter ce qui manque sur une entreprise | enrichissement | `enrichir_entreprise` | Unipile page entreprise, Crustdata ; `detecter_techno` pour la stack | ligne par ligne | secteur, effectif, ville, pays, domaine, techno |

Chaque outil écrit les colonnes de `docs/conventions-gtm.md` section 8, avec `source` (le nom complet de l'actor Apify, par exemple `compass/crawler-google-places`, `code_crafter/leads-finder`, ou `unipile`, `crustdata`, `ocean`, `hubspot` ; plusieurs sources séparées par `+`) et `date_extraction`. Les actors nommés ici sont ceux de `05_Departements/Go-to-Market/OUTILS.md` au moment de l'écriture ; si `05_Departements/Go-to-Market/OUTILS.md` en nomme un autre pour le même verbe, c'est lui qui gagne, sans rien changer à la méthode.

## Choisir selon la cible

| Cible de l'utilisateur | Première source | Seconde source | Pourquoi |
|---|---|---|---|
| SaaS, tech, services numériques en France | Sales Navigator via Unipile | `code_crafter/leads-finder` | données LinkedIn à jour, l'actor apporte le volume et les domaines |
| PME traditionnelles (industrie, BTP, cabinets, distribution) | `code_crafter/leads-finder` ou Crustdata | annuaires professionnels | ces entreprises sont peu actives sur LinkedIn, l'annuaire les liste toutes |
| Startups financées | `detecter-signaux` (levées) | Sales Navigator | la levée donne le timing, Sales Navigator les personnes |
| Commerces et professions locales | Google Maps | pages entreprise LinkedIn pour le gérant | la carte donne le téléphone et le site, LinkedIn le décideur quand il y est |
| Niche étroite (moins de 500 entreprises en France) | annuaire ou classement | lookalikes Ocean.io | l'annuaire est exhaustif, les lookalikes trouvent ceux qui n'y sont pas |
| Comptes nommés (ABM) | fichier de l'utilisateur ou lookalikes | pages entreprise LinkedIn | on part des comptes, jamais d'une recherche large |

## Dépasser la limite de 2 500 résultats

Sales Navigator affiche au maximum 2 500 résultats par recherche. Au-delà, on découpe la même recherche en plusieurs : par région, par tranche d'effectif (11-50 puis 51-200), par secteur, par ancienneté dans le poste, et pour les personnes par première lettre du prénom. Chaque découpe devient un run, les runs se fusionnent puis se dédoublonnent par `linkedin_url` ou `domaine`.

## Ce qu'on ne fait pas

- Lancer une base large sans avoir fixé l'effectif et le secteur : on récupère 50 000 lignes inutilisables.
- Chercher des personnes avant d'avoir qualifié les entreprises : on paie des contacts chez des comptes qu'on va exclure.
- Faire confiance à l'effectif d'une seule source : croiser avec `enrichir_entreprise` sur les tiers A.
- Scraper un annuaire qui interdit l'extraction dans ses conditions d'utilisation, ou qui contient des données de particuliers.

## Trois exemples

Demande : "des cabinets d'expertise comptable de 10 à 50 personnes en Île-de-France". Plan : `code_crafter/leads-finder` (secteur comptabilité, effectif 11-50, région), puis annuaire de l'ordre régional pour les absents, fusion, dédoublonnage par domaine. Ordre de grandeur, à confirmer par un test de volume : 800 à 1 500 entreprises avant qualification.

Demande : "les boîtes qui ressemblent à mes trois meilleurs clients". Plan : domaines des trois clients, `trouver_lookalikes` sur Ocean.io, `enrichir_entreprise` sur les 200 premières, puis `qualifier-comptes`. Ordre de grandeur : 100 à 300 comptes tier A ou B.

Demande : "les restaurants gastronomiques de Bordeaux". Plan : Google Maps sur "restaurant gastronomique Bordeaux", filtre sur la note et le nombre d'avis, puis `sourcer-personnes` par page entreprise pour le gérant quand elle existe, sinon le téléphone de la fiche. Ordre de grandeur : 80 à 150 établissements, dont un tiers avec un gérant identifiable sur LinkedIn.
