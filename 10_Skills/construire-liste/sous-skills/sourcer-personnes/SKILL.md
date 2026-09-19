---
name: sourcer-personnes
description: >
  Trouve les bonnes personnes chez les entreprises cibles : titres et booléens par
  persona, recherche Sales Navigator, employés d'une page entreprise, puis profil enrichi
  et email vérifié. Se déclenche sur : "trouve les DRH de", "les CEO de ces boîtes",
  "décisionnaires", "qui contacter chez", "booléen", "Sales Nav", "employés de ces
  entreprises", "à partir de cette liste d'entreprises". Ne pas utiliser pour trouver
  les entreprises (voir `sourcer-entreprises`), pour définir les personas (voir
  `cartographier-personas`), ni pour vérifier des emails existants (voir
  `nettoyer-verifier`).
---

On part d'une liste d'entreprises qualifiées et de personas écrits, jamais d'une recherche de personnes dans le vide : une liste d'entreprises se retrouve presque à coup sûr sur LinkedIn, une liste de personnes beaucoup moins, et les contacts se paient à la ligne.

## Ressources

- `{SKILL_BASE}/ressources/personas-comite-achat.md` : titres par fonction, ATL et BTL, exclusions de booléen.
- `{SKILL_BASE}/ressources/sources-par-besoin.md` : recherche par critères ou par page entreprise, la limite des 2 500.
- `{SKILL_BASE}/ressources/hygiene-liste.md` : la règle "ne relance que si vide", l'ordre d'entrée le moins cher.

## Méthode

1. Point de départ : un CSV d'entreprises passé par `qualifier-comptes` (tiers A et B, `exclu = non`), ou des critères d'entreprise si l'utilisateur n'a pas encore de liste. Dans ce second cas, faites d'abord `sourcer-entreprises`.
2. Lisez les personas dans `05_Departements/Go-to-Market/contexte.md`. Un persona, une recherche, un CSV. Les titres du persona deviennent un booléen : `("Directeur commercial" OR "Directrice commerciale" OR "Head of Sales" OR CRO) NOT (assistant OR stagiaire OR alternant OR "à la recherche")`. Le booléen marche dans le champ titre, entreprise et mots-clés, pas dans les filtres à choix ; pas de joker ; moins de 1 000 caractères ; parenthèses sur deux ou trois niveaux.
3. Choisissez le chemin. Liste d'entreprises précise (moins de 500 comptes, ABM, local) : les employés de chaque page entreprise, filtrés par titre. Critères larges (secteur, effectif, zone) : recherche par profil avec le booléen et les filtres d'entreprise. Sur Sales Navigator, si le total dépasse 2 500, découpez par région, par effectif, ou par première lettre du prénom.
4. Fixez le plafond par compte avant de lancer : 2 à 4 sur un tier A, 1 à 2 sur un B, 1 sur un C. Séniorité la plus haute d'abord, dans la limite du persona.
5. Annoncez volume et coût, lancez sur 10 comptes ou 25 lignes, mesurez le taux de match (comptes avec au moins une personne trouvée sur comptes cherchés). Sous 50 %, revoyez les titres avec `cartographier-personas` avant de continuer.
6. Lancez le reste. Fusionnez les runs, dédoublonnez par `linkedin_url`.
7. Enrichissez le profil seulement là où `titre`, `entreprise` ou `linkedin_url` manque : `enrichir_personne` sur ces lignes, pas sur les autres.
8. Cherchez l'email seulement là où `email` est vide : `trouver_email` avec prénom, nom et domaine d'abord, le `linkedin_url` en second. Lisez le taux de trouvés sur les 50 premières lignes. Le téléphone (`trouver_telephone`) seulement sur les tiers A et si le canal téléphone est dans `05_Departements/Go-to-Market/contexte.md`.
9. Rendez le CSV par persona, le taux de match, le taux d'emails trouvés, et le next step : `nettoyer-verifier` si des emails viennent d'une autre source, sinon `dedoublonner-liste` contre le CRM.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 3, par page entreprise | `trouver_personnes` | `trouver-personnes` (`harvestapi/linkedin-company-employees`) | `linkedin_entreprise_url`, titres du persona, plafond par compte | `prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `linkedin_url`, `linkedin_entreprise_url`, `ville`, `source`, `date_extraction` |
| 3, par critères | `trouver_personnes` | `trouver-personnes` (`harvestapi/linkedin-profile-search`, Unipile Sales Navigator, ou Crustdata) | booléen de titres, secteur, effectif, zone | mêmes colonnes, plus `domaine` quand l'outil le donne |
| 7 | `enrichir_personne` | `enrichir-personne` | `linkedin_url`, lignes où `titre` ou `entreprise` est vide | `titre`, `entreprise`, `domaine`, `ville`, `pays` complétés |
| 8 | `trouver_email` | `trouver-email` | `prenom`, `nom`, `domaine`, puis `linkedin_url` ; lignes où `email` est vide | `email`, `email_statut` |
| 8, tiers A | `trouver_telephone` | `trouver-telephone` | `linkedin_url` ou `prenom`, `nom`, `entreprise` | `telephone` |

Sortie : `trouver-personnes_<persona>-<sujet>_<date>.csv`, colonnes de `CONVENTIONS.md` section 8, avec `score_icp` et `tier` recopiés depuis la ligne entreprise.

**Où ça s'écrit** : chaque requête booléenne validée (persona, requête Sales Navigator ou LinkedIn, filtres, volume obtenu, date) dans `05_Departements/Go-to-Market/Ciblage/requetes-booleennes.md`, pour être rejouée sans la reconstruire.

## Repères

| Repère | Valeur |
|---|---|
| Résultats maximum par recherche Sales Navigator | 2 500 |
| Longueur maximum d'un booléen | environ 1 000 caractères |
| Taux de match acceptable | au moins la moitié des comptes renvoient une personne |
| Emails trouvés attendus | 70 % des lignes ; sous 50 % sur l'échantillon, on vérifie les noms et les domaines avant de relancer |
| Plafond par compte | 2 à 4 (A), 1 à 2 (B), 1 (C), 5 au maximum |
| Lignes de test | 10 comptes ou 25 lignes, puis 50 pour l'email |
| Ordre d'entrée pour l'email | prénom + nom + domaine, puis `linkedin_url` |

## Template

```
Persona : <nom> (<ATL | BTL>)
Booléen titre : (<titre 1> OR "<titre 2>" OR <variante EN>) NOT (assistant OR stagiaire OR alternant OR "à la recherche")
Chemin : <page entreprise | critères>
Filtres entreprise : <secteur> / <effectif> / <zone>   (ou : <n> comptes tier A et B)
Plafond par compte : <n>
Test : 10 comptes -> taux de match <x %>
Fichier : trouver-personnes_<persona>-<sujet>_<date>.csv
```

## Règles

- Jamais de personnes chez des comptes `exclu = oui` ou tier C sans demande explicite.
- Un persona par recherche et par fichier ; on ne mélange pas DG et responsable marketing dans un même CSV.
- Le booléen exclut toujours assistant, stagiaire, alternant, étudiant et les profils en recherche.
- Le poste actuel prime sur l'accroche du profil pour remplir `titre` ; l'accroche sert à départager un indépendant d'un dirigeant.
- Un enrichissement ne se lance que sur une cellule vide.
- Une entreprise locale sans page LinkedIn garde sa ligne entreprise avec le téléphone de la fiche : le canal sera l'appel.
- Aucun email deviné à partir d'un format de domaine : une adresse non renvoyée par l'outil reste vide.

## Exemples

- "Trouve les DRH de ces 80 entreprises" : chemin page entreprise, booléen DRH avec variantes, plafond 2 ; réponse attendue : un CSV de 80 à 160 lignes, taux de match, taux d'emails, next step `dedoublonner-liste`.
- "Les fondateurs de SaaS de 11 à 50 personnes en France" : `sourcer-entreprises` d'abord si aucune liste, puis recherche par critères en deux runs d'effectif ; réponse attendue : un CSV par persona, sous 2 500 par run, dédoublonné par `linkedin_url`.
- "Ajoute les emails à ma liste de contacts" : `trouver_email` sur les lignes où `email` est vide, test sur 50 lignes ; réponse attendue : `email` et `email_statut` remplis, taux de trouvés, lignes restées vides listées.
