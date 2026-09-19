---
name: recrutement
description: >
  Détecte les signaux de recrutement utiles à la prospection (une offre d'emploi sur un rôle lié à votre offre, une vague de recrutement, un rôle absent de l'organigramme, un départ) et déclenche l'approche entre le jour 14 et le jour 30. Se déclenche sur : "offres d'emploi", "qui recrute", "recrute un commercial", "recrute un SDR", "vague de recrutement", "ils embauchent", "pas de responsable commercial", "rôle manquant", "quelqu'un est parti", "départ dans l'équipe". Ne pas utiliser pour : une personne qui prend un poste, voir `changement-poste` ; une offre qui révèle une migration d'outil, voir `changement-techno`.
---

Une offre d'emploi est un budget rendu public : elle dit ce que l'entreprise juge prioritaire, et le poste reste vide six à douze semaines pendant lesquelles quelqu'un porte le trou. Une offre pertinente vaut 40 points ; le taux de réponse d'un contact avec un signal est de 18 à 22 %, contre 6 à 8 % à froid.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : offre pertinente 40, actualité 15, seuils.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : offre j14 à j30, départ semaines 1 à 2, nouveau membre semaines 2 à 4.
- `{SKILL_BASE}/ressources/plays-signaux.md` : plays 1 (nouveau membre), 2 (compétences), 3 (titre rare), 6 (départ), 7 (rôle manquant).
- `{SKILL_BASE}/ressources/detection-par-signal.md` : actors, coûts.

## Méthode

1. **Nommer les rôles qui comptent pour vous.** Ceux que votre offre équipe, remplace ou fait monter : commerciaux, SDR, responsables marketing, ops. Ils vivent dans `05_Departements/Go-to-Market/contexte.md`. Une offre de comptable n'est pas un signal pour un coach en prospection.
2. **Choisir le type de signal.** Quatre : (a) offre pertinente, un poste ouvert dans votre périmètre ; (b) vague, 5 postes ou plus en 30 jours ; (c) rôle manquant, personne sur une fonction que votre offre couvre ; (d) départ, quelqu'un quitte le service visé.
3. **Détecter** (Exécution). Offres : LinkedIn pour les cadres, Indeed pour les PME et les postes non cadres. Vague : le signal `hiring`. Rôle manquant : compter les têtes. Départ : les changements de poste rattachés à l'entreprise.
4. **Qualifier** l'entreprise (ICP) et le rôle (strictement dans votre périmètre : "business developer" oui, "assistant commercial" non, sauf si votre offre le dit).
5. **Dater.** `signal_date` = date de publication. Pic j14 à j30 : le poste n'est pas pourvu, la douleur est maximale. Frais 60 jours. Une offre de plus de 60 jours est soit pourvue, soit abandonnée : contexte.
6. **Trouver la bonne personne** : le responsable qui recrute, pas le futur recruté. Le dirigeant dans une entreprise de moins de 30 personnes.
7. **Choisir l'angle** avec le test "et alors ?", et sa cinquième question : qu'est-ce que l'offre ne dit pas ? Deux SDR recrutés et personne en ops commerciales, c'est un angle. "Vous recrutez des SDR", non.
8. **Envoyer** dans les 24 h qui suivent la détection si l'offre a déjà 14 jours, sinon programmer à j14. Séquence par signal ; appel si le score cumulé est Chaud.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1a | scraper_offres_emploi | `scraper-offres-emploi` | `tagadanar/linkedin-jobs-scraper` : `keywords` (vos rôles), `location` (France ou villes), `postedSince: week` en cadence hebdo, `scrapeDetails: true` pour lire la description (l'outil demandé, la mission "structurer"), `companyIds` pour vos comptes cibles. 0,002 $ par offre, 0,004 $ avec le détail. `borderline/indeed-scraper` pour les PME et les postes non cadres, 0,005 $ par offre. |
| 1b | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | vague : `signalbase/signalbase-api`, `signalType: hiring`, `countries: FR`, `departments: sales,marketing`, `seniorities`, `team_size: 11-50,51-200`, `date_preset: last_30d`. 0,04 $ par résultat. |
| 1c | trouver_personnes | `trouver-personnes` | rôle manquant : chercher le titre dans l'entreprise ; zéro résultat sur une entreprise dans l'ICP = signal. À faire chaque trimestre sur vos comptes cibles. |
| 1d | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | départ : `signalType: job-changes`, `companyLinkedinUrl` de vos comptes cibles ; une personne du service visé apparaît avec une nouvelle entreprise. |
| 1e | scraper_offres_emploi | `scraper-offres-emploi` (`--source theirstack` ou `--source predictleads`) | si branchés : TheirStack filtre les offres par techno citée dans l'annonce (`--technos hubspot`), 1 crédit par offre ; PredictLeads donne les offres actives par intitulé sur son quota mensuel. |
| 2 | qualifier_liste | `qualifier-liste` | ICP de l'entreprise, rôle dans le périmètre, exclusion des cabinets de recrutement et de l'intérim qui publient pour d'autres |
| 3 | trouver_personnes | `trouver-personnes` | le responsable du service qui recrute, ou le dirigeant |
| 4 | enrichir_personne | `enrichir-personne` | profil complet |
| 5 | trouver_email, trouver_telephone | `trouver-email`, `trouver-telephone` | le téléphone si le compte est Chaud : un poste ouvert est un bon prétexte d'appel |
| 6 | dedoublonner | `dedoublonner` | contre HubSpot et les séquences en cours |
| 7 | envoyer_sequence | `envoyer-sequence` | à j14 après publication ; email puis LinkedIn puis relance sur un autre angle |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : aucun en mode marché ; `entreprise, linkedin_entreprise_url` pour vos comptes cibles (les `companyIds` LinkedIn se lisent dans l'URL des offres de la page).

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`offre_emploi`, `vague_recrutement`, `role_manquant`, `depart`), `signal_date`, `signal_detail` ("{{intitulé}}, publié le {{date}}, {{ville}}, {{url}}" ; pour une vague, "{{n}} postes en 30 jours, dont {{rôles}}"), `score_signal`, `fraicheur`, `source` (`tagadanar/linkedin-jobs-scraper`, `borderline/indeed-scraper`, `signalbase/signalbase-api`).

## Repères

| Signal | Points | Fenêtre | Délai |
|---|---|---|---|
| Offre pertinente | 40 | j14 à j30, frais 60 j | 24 h après détection, ou programmé à j14 |
| Vague de 5 postes ou plus | 40, fiabilité tier 2 | j14 à j30, frais 90 j | 30 à 90 jours pour dérouler |
| Rôle manquant | 15 (repère actualité) : c'est un angle plus qu'un déclencheur | permanent | liste revue chaque trimestre |
| Départ dans le service visé | 15 (repère actualité) | semaines 1 à 2, frais 30 j | sous 72 h |
| Nouveau membre dans le service visé | 15 (repère actualité) | semaines 2 à 4 | sous 72 h |

| Repère | Valeur |
|---|---|
| Empilement type | levée (45) + offre pertinente (40) = 85, Tiède ; les deux dans leur fenêtre (×1,5) = 128, Chaud |
| Un commentateur de vos posts qui recrute | 35 + 40 = 75, Tiède, et un angle tout trouvé |
| Ce que révèle un titre rare | "responsable ops commerciales" = le sujet a un budget ; "growth engineer" = une fonction technique de croissance existe |

## Template

Offre pertinente, au responsable qui recrute :

```
Bonjour {{prenom}},

Recruter un {{poste}} prend {{delai_recrutement}} en ce moment, et il lui faut encore {{delai_ramp}} avant son premier résultat. Entre les deux, {{ce_qui_attend}}. {{client_similaire}} a comblé ce trou avec {{solution}} : {{resultat_chiffre}}.

Vous gérez ce délai comment, de votre côté ?
```

Rôle manquant, au dirigeant :

```
Bonjour {{prenom}},

Dans une entreprise de {{effectif}} personnes, {{fonction}} tombe en général sur le dirigeant, entre deux autres sujets. Chez {{client_similaire}}, ça représentait {{n}} heures par semaine avant {{solution}}.

C'est vous qui portez le sujet aujourd'hui ?
```

## Règles

- Jamais "j'ai vu votre offre d'emploi". On parle du poste vide et de ce qu'il coûte.
- On écrit au recruteur du poste, jamais au candidat, jamais au partant.
- Un départ ne se nomme pas dans le message : on parle du trou de couverture, pas de la personne.
- Les cabinets de recrutement, l'intérim et les ESN publient pour leurs clients : on les exclut, sauf si ce sont eux, vos clients.
- Un rôle manquant se vérifie à deux sources (Sales Nav et le site) avant d'être affirmé : une PME de 30 personnes a souvent un commercial sans le titre.
- Une offre de plus de 60 jours ne sert plus d'accroche.
- On empile : offre + levée, offre + nouveau dirigeant, offre + commentaire sur vos posts sont les trois duos les plus rentables.

## Exemples

- "Trouve les PME françaises qui recrutent un SDR ce mois-ci" : scraper_offres_emploi LinkedIn, `keywords: SDR, business developer`, `location: France`, `postedSince: month`, `scrapeDetails: true`, exclusion des cabinets, contact du responsable commercial à j14 sur le délai de ramp.
- "Cette agence n'a pas de directeur commercial" : rôle manquant vérifié par trouver_personnes et le site, 15 points, angle "la prospection tombe sur le fondateur", message au dirigeant, pas de fenêtre.
- "Une entreprise cible a ouvert 6 postes en un mois" : vague, 40 points, fiabilité tier 2, on cherche la levée ou la nomination derrière (`levee-fonds`, `changement-poste`) et on écrit sur l'intégration de six recrues sans process.
