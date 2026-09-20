---
name: changement-techno
description: >
  Détecte les changements de stack technique d'un compte (adoption d'un outil, retrait d'un outil, migration annoncée dans une offre d'emploi) et déclenche l'approche pendant la transition, quand les trous apparaissent. Se déclenche sur : "stack technique", "quel outil ils utilisent", "ils ont changé de CRM", "migration", "ils ont quitté", "ils viennent d'adopter", "outil adjacent", "technographique", "qui utilise tel outil", "retrait d'un concurrent". Ne pas utiliser pour : l'engagement avec le contenu d'un concurrent et ses clients identifiés par sa page, voir `signaux-concurrents` ; un événement d'entreprise sans changement d'outil, voir `evenements-entreprise`.
---

Une entreprise qui change un outil a déjà décidé de changer : elle est ouverte aux nouveaux fournisseurs, la transition crée des trous dans ses process, et la douleur est fraîche. Le retrait d'un concurrent de sa stack vaut 45 points, la fenêtre va du jour 0 au jour 30.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : retrait 45, ajout adjacent 35, migration 30, stack qui grossit 25 (un concurrent qui apparaît dans la stack : `signaux-concurrents`, 20).
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : j0 à j30, frais 60 jours.
- `{SKILL_BASE}/ressources/detection-par-signal.md` : lignes 11 à 14.
- `{SKILL_BASE}/ressources/taxonomie-declencheurs.md` : famille 4, fournisseurs adjacents (déclencheurs 1 à 7).

## Méthode

1. **Écrire votre carte des outils.** Trois listes dans `05_Departements/Go-to-Market/contexte.md` : vos concurrents (les outils ou prestataires que vous remplacez), vos adjacents (ceux que vous complétez), et les outils dont la présence prouve un besoin (un CRM sans outil de prospection, un site sans suivi de conversion). Sans cette carte, un relevé de stack ne dit rien.
2. **Savoir ce que chaque détecteur voit.** TheirStack lit les offres d'emploi : il voit le CRM, l'ERP, les outils RH, la téléphonie, avec la date de première mention, mais seulement chez les entreprises qui recrutent et citent leurs outils. Le détecteur de site lit le site : CMS, analytics, chat, marketing automation, paiement, hébergement, framework, chez tout le monde, sans date. Les deux se complètent ; avec TheirStack branché, commencez par lui.
3. **Relever la stack** de vos comptes cibles une fois par mois. Avec TheirStack, `--recentes-jours 60` rend directement les adoptions datées ; avec le détecteur de site, gardez chaque relevé.
4. **Comparer** (voie site) le relevé du mois avec le précédent : une ligne qui apparaît = adoption ; une ligne qui disparaît = retrait. C'est la différence qui est le signal, pas la photo. Le retrait ne se voit que par cette voie.
5. **Lire les offres d'emploi** avec le nom des outils en mots-clés : "expérience {{outil}}" dans une entreprise qui ne l'utilisait pas = migration en cours.
6. **Qualifier et dater.** ICP, puis `signal_date` = date du relevé où la différence apparaît (ou date de publication de l'offre). j0 à j30 : pic. Frais 60 jours.
7. **Scorer** (Repères) et empiler : un retrait d'outil et une offre d'emploi pour un nouvel outil dans le même mois, c'est une migration confirmée.
8. **Choisir l'angle** : le trou que la transition crée, jamais l'outil. Migrer des données, reformer une équipe, réécrire les process, perdre six semaines de relance.
9. **Envoyer** sous 72 h : les fenêtres se ferment vite pendant une migration.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1 | detecter_techno | `enrichir-entreprise --techno --techno-source theirstack --recentes-jours 60` | si TheirStack est branché (`signaux_secours:` dans `OUTILS.md`) : pour chaque `domaine`, les technos avec leur date de première détection (`first_date_found`), leur confiance et le nombre d'offres qui les citent ; une ligne `techno_ajout` par techno vue pour la première fois depuis N jours. Tirée des offres d'emploi, donc elle voit le CRM, l'ERP, les outils RH que le site ne montre pas, sans attendre deux relevés. 3 crédits par entreprise, 0 si rien. C'est la voie à préférer. |
| 1 bis | detecter_techno | `enrichir-entreprise --techno --diff` | sans TheirStack : actor `scrapemint/website-tech-stack-detector`, sur la colonne `domaine` de vos comptes cibles. 0,01 $ par site avec au moins une détection, gratuit sinon. Il lit le site (CMS, analytics, chat, paiement, marketing) : cadence mensuelle, relevé daté et conservé ; `--diff` compare au dernier relevé enregistré et écrit un fichier `_diff.csv` avec une ligne `techno_ajout` ou `techno_retrait` par changement. Le retrait ne se voit que par cette voie. |
| 2 | classement | interne (Claude) | lecture du `_diff.csv` : chaque ligne `techno_ajout` ou `techno_retrait` classée selon votre carte (concurrent, adjacent, preuve de besoin) |
| 3 | scraper_offres_emploi | `scraper-offres-emploi` | avec TheirStack : `--source theirstack --technos <slugs de vos concurrents et adjacents> --jours 30` (la techno est taguée par offre, 1 crédit par offre) ; sinon `--source linkedin` (`tagadanar/linkedin-jobs-scraper`), `--mots-cles` = noms des outils, `--details` (la description dit l'outil), `--depuis month`, 0,0036 $ par offre détaillée. |
| 4 | qualifier_liste | `qualifier-liste` | ICP, exclusions |
| 5 | trouver_personnes | `trouver-personnes` | le responsable de la fonction touchée par l'outil (marketing pour un outil marketing, commercial pour un CRM) |
| 6 | enrichir_personne, trouver_email | `enrichir-personne`, `trouver-email` | profil complet, email vérifié |
| 7 | dedoublonner | `dedoublonner` | contre HubSpot |
| 8 | envoyer_sequence | `envoyer-sequence` | sous 72 h ; email puis LinkedIn puis relance à j7 sur un autre angle |
| 9 | verifier_reponses | `verifier-reponses` | à j3 et j7 |
| 1 ter | detecter_techno | `enrichir-entreprise --techno --techno-source predictleads --recentes-jours 60` | si PredictLeads est branché et pas TheirStack : détections datées (`first_seen_at`), une ligne `techno_ajout` par techno vue pour la première fois depuis N jours, sur le quota mensuel. |

**CSV en entrée** : `entreprise, domaine` (comptes cibles), plus le relevé du mois précédent.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`techno_retrait`, `techno_ajout` ; une migration lue dans une offre est un `techno_ajout` dont `signal_detail` cite l'offre ; une croissance de stack, ce sont 5 lignes `techno_ajout` ou plus sur le même `domaine`), `signal_date` (`first_date_found` avec TheirStack, date du relevé sinon), `signal_detail` ("cite {{outil}} ({{catégorie}}) dans ses offres depuis le {{date}}, confiance {{niveau}}", "retiré : {{outil}} ({{catégorie}}), relevé du {{date}}" ou "offre {{intitulé}} demande {{outil}}, publiée le {{date}}"), `score_signal`, `fraicheur`, `source` (`theirstack`, `scrapemint/website-tech-stack-detector`, `tagadanar/linkedin-jobs-scraper`), et avec TheirStack `categorie_techno`, `confiance`, `offres_30j`.

## Repères

| Changement | Points | Ce que ça révèle |
|---|---|---|
| Retrait d'un concurrent de la stack | 45 | remplacement en cours, ils cherchent maintenant |
| Ajout d'un outil adjacent | 35 | extension de la stack, votre pièce manque à côté |
| Offre d'emploi qui mentionne un nouvel outil | 30 | migration en cours, projet de 6 à 12 mois |
| Croissance générale de la stack (5 outils ou plus ajoutés) | 25 | mode achat actif |

Un concurrent qui apparaît dans la stack est un client d'un concurrent : voir `signaux-concurrents` (`techno`, 20 points, permanent, à réveiller 60 à 90 jours avant le renouvellement).

| Repère | Valeur |
|---|---|
| Fenêtre | j0 à j30 (×1,5), j31 à j60 (×1,0), au-delà contexte |
| Délai | sous 72 h |
| Empilement type | retrait d'un concurrent (45) + offre pour un nouvel outil (30), les deux frais : 113, Chaud |
| Coût d'un relevé mensuel sur 300 comptes | 3 $ au plus |
| Ce que le relevé ne voit pas | CRM interne, ERP, RH, téléphonie : passer par les offres d'emploi |

## Template

Retrait d'un concurrent, au responsable de la fonction :

```
Bonjour {{prenom}},

Changer d'outil de {{categorie}} laisse en général un trou de {{duree}} sur {{fonction}} : les données à migrer, et les relances qui s'arrêtent pendant ce temps. {{client_similaire}} est passé par là en {{delai}} sans perdre {{metrique}}.

Vous en êtes à quelle étape ?
```

Ajout d'un outil adjacent :

```
Bonjour {{prenom}},

Les équipes qui mettent en place {{outil_adjacent}} découvrent en général le mois suivant qu'il leur manque {{ce_qui_manque}} pour en tirer quelque chose : {{detail_concret}}. C'est ce qu'on a branché chez {{client_similaire}} : {{resultat_chiffre}}.

Vous avez déjà buté dessus ?
```

## Règles

- Jamais "j'ai vu que vous utilisiez" ni "j'ai vu que vous aviez quitté". On parle de la transition et de ses trous.
- Une photo de stack n'est pas un signal. La différence entre deux photos en est un.
- On garde chaque relevé mensuel : sans historique, pas de différence.
- Le détecteur voit le site, pas l'entreprise : un CRM ou un ERP se détecte par les offres d'emploi.
- On empile avec `recrutement` : un nouvel outil et un poste ouvert pour l'administrer, c'est une migration confirmée.
- On ne dénigre jamais l'outil quitté ni celui adopté.
- Sans carte des outils dans `05_Departements/Go-to-Market/contexte.md`, on ne lance pas de relevé : on n'aurait rien à comparer.

## Exemples

- "Surveille la stack de mes 200 comptes cibles" : `enrichir-entreprise --techno --diff` sur la colonne `domaine` chaque mois (2 $), relevé conservé, différence dans le `_diff.csv`, lignes classées selon votre carte, alertes sur les retraits de concurrents et les ajouts d'adjacents.
- "Un compte a retiré notre concurrent de son site" : 45 points ×1,5 sous 30 jours, sous 72 h ; on cherche une offre d'emploi et un nouveau responsable dans la fonction pour multi-threader ; message sur le trou de la transition.
- "Une offre d'emploi demande une expérience sur un CRM qu'ils n'ont pas" : migration, 30 points, projet de 6 à 12 mois ; angle "ce qui casse pendant la migration" ; contact tôt dans le projet, quand le fournisseur d'à côté se choisit.
