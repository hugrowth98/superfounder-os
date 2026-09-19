---
name: qualifier-comptes
description: >
  Qualifie un CSV d'entreprises ou de personnes selon l'ICP de contexte.md : huit portes
  dans l'ordre (dédoublonnage, titre, taille, secteur, B2C, concurrent, score ICP, tier),
  un score sur 100, un tier A, B ou C, et une raison d'exclusion par ligne écartée. Se
  déclenche sur : "qualifie cette liste", "score ces prospects", "trie", "qui est
  prioritaire", "tier", "enlève les B2C", "enlève les concurrents", "garde ceux qui
  matchent mon ICP", "cet export est trop large". Ne pas utiliser pour définir l'ICP
  (voir `definir-icp`), pour vérifier des emails (voir `nettoyer-verifier`), ni pour
  croiser avec le CRM seul (voir `dedoublonner-liste`).
---

Qualifier, c'est faire passer chaque ligne par huit portes dans un ordre fixe, les gratuites d'abord, et ne payer un enrichissement que pour ce qui reste : sur un export brut, la moitié des lignes sort avant le score, et c'est autant de contacts qu'on n'a pas payés.

## Ressources

- `{SKILL_BASE}/ressources/gates-qualification.md` : les huit portes, les règles de titre, les listes B2C et concurrents, le rapport en entonnoir.
- `{SKILL_BASE}/ressources/icp-3-couches.md` : le score sur 100, les seuils de tiers, le format de `05_Departements/Go-to-Market/contexte.md`.
- `{SKILL_BASE}/ressources/scoring-tam.md` : nettoyage avant score, départageurs dans un tier, effort par tier.
- `{SKILL_BASE}/ressources/regles-dedup.md` : la porte 0.

## Méthode

1. Lisez la section 2 de `05_Departements/Go-to-Market/contexte.md` (couches et points, seuils, exclusions : B2C, concurrents nommés, secteurs exclus, tailles exclues), la section 3 (titres ATL et BTL), la section 4 (signaux prioritaires), la section 7 (clients, partenaires, listes à croiser) et la section 8 (mots-clés propres au marché). Si la section 2 contient des crochets ou si un point manque (pas de tailles exclues, pas de concurrents nommés), demandez avant de juger. Vous n'inventez aucun critère.
2. Lisez le CSV en entier, sans sauter de ligne. Repérez les colonnes de fit disponibles (`titre`, `effectif`, `secteur`, `pays`, `ville`, description) et celles qui manquent. Si seule `entreprise` est remplie, prévenez : la qualification sera dégradée, et demandez si on enrichit d'abord ou si on continue.
3. Deux niveaux de tri, dans cet ordre. Le tri structurel, déterministe, sur le titre et l'effectif (portes 1 et 2) : il dégrossit un gros export en quelques secondes. Puis le tri fin, au jugement, sur le fit ICP (portes 3 à 7) : il ne s'applique qu'à ce qui a passé le tri structurel.
4. Porte 0 : doublons dans le fichier, exclusions fixes de `05_Departements/Go-to-Market/contexte.md`, clients et affaires en cours si HubSpot est branché.
5. Porte 1 : `titre` contre les personas. Le poste actuel prime sur l'accroche. Stagiaires, indépendants (sauf persona dédié), opérationnels hors persona sortent. `seniorite` se remplit pour tous. Une personne sans ligne entreprise reçoit l'effectif et le secteur de son `domaine` si une autre ligne les porte.
6. Portes 2 et 3 : `effectif` hors bornes dures, `secteur` exclu. Une valeur vide laisse passer et se note dans le rapport.
7. Portes 4 et 5 : B2C et concurrent. Mots-clés d'abord, jugement ensuite sur les lignes qui ont matché ou qui restent ambiguës, avec toutes les colonnes descriptives. Qui paie décide du B2C. Un produit logiciel n'est pas un concurrent, une agence qui vend le même service l'est. Doute franc : la ligne passe.
8. Porte 6 : `score_icp` sur 100 avec les points de `05_Departements/Go-to-Market/contexte.md`, exact, adjacent ou zéro par critère de la couche 1, présent ou neutre pour la couche 2, signaux datés pour la couche 3 ; donnée manquante = 0 ou neutre, jamais négatif. Les colonnes `signal_type` et `signal_date`, si présentes, comptent dans la couche 3. Sous le seuil D : exclu.
9. Porte 7 : `tier`. Plafond de contacts par entreprise (2 à 4 en A, 1 à 2 en B, 1 en C), séniorité la plus haute gardée. Le tier C ne reçoit pas d'appel : nurturing seulement. Dans un tier, départagez par signal le plus récent, décideur identifié, activité LinkedIn récente.
10. Écrivez un seul CSV avec toutes les lignes, `score_icp`, `tier`, `exclu`, `raison_exclusion`. Rendez l'entonnoir, la répartition par tier, les trois raisons d'exclusion les plus fréquentes, cinq lignes tier A avec le détail de leur score, cinq lignes exclues au hasard. Une seule question si une porte a retiré plus de la moitié du fichier. Next step : `sourcer-personnes` sur les tiers A et B si le fichier est une liste d'entreprises, `nettoyer-verifier` si c'est une liste de personnes.

## Exécution

| Étape | Verbe | Skill d'exécution | Entrée | Sortie |
|---|---|---|---|---|
| 4 | `dedoublonner` (porte 0, dans le fichier et contre le CRM) | `dedoublonner` | le CSV, `linkedin_url`, `email`, `domaine` | `exclu`, `raison_exclusion = doublon` ou `= deja client` ou `= affaire en cours` |
| 5 à 9 | `qualifier_liste` | `qualifier-liste` | le CSV avec `titre`, `entreprise`, `domaine`, `secteur`, `effectif`, `ville`, `pays`, et si présents `signal_type`, `signal_date`, `score_signal` | mêmes colonnes, plus `seniorite`, `score_icp`, `tier`, `exclu`, `raison_exclusion` |
| après, si demandé | `enrichir_entreprise` | `enrichir-entreprise` | `domaine` des lignes gardées où `effectif` ou `secteur` est vide, et des lignes entre le seuil D et le seuil C | colonnes complétées, puis nouveau passage par `qualifier_liste` |

`qualifier_liste` est interne : il lit `05_Departements/Go-to-Market/contexte.md` et le CSV, sans appel payant. Sortie : `qualifier-liste_<sujet>_<date>.csv`.

**Où ça s'écrit** : les mots-clés B2C et concurrents découverts en qualifiant (au-delà de ceux de `contexte.md`) dans `05_Departements/Go-to-Market/Ciblage/mots-cles-exclusion.md`, relus au run suivant.

## Repères

| Repère | Valeur |
|---|---|
| Seuils de tiers | dans `05_Departements/Go-to-Market/contexte.md` ; défaut A 75, B 55, C 35 |
| Donnée manquante | 0 point, jamais une exclusion |
| Lignes sorties avant le score sur un export brut | souvent la moitié |
| Plafond de contacts par entreprise | 2 à 4 (A), 1 à 2 (B), 1 (C), 5 maximum |
| Candidates à l'enrichissement | les lignes entre le seuil D et le seuil C |
| Échantillon à montrer | 5 tier A avec détail du score, 5 exclues au hasard |
| Fichier trop gros pour un passage au jugement | au-delà de 500 lignes, par lots de 200, avec un point après chaque lot |

## Template

```
Entrée : <fichier> (<n> lignes, colonnes de fit : <liste>, manquantes : <liste>)
Porte 0  doublons et exclusions fixes    -<n>  -> <n>
Porte 1  titre hors persona              -<n>  -> <n>
Porte 2  effectif hors bornes            -<n>  -> <n>
Porte 3  secteur exclu                   -<n>  -> <n>
Porte 4  B2C                             -<n>  -> <n>
Porte 5  concurrent                      -<n>  -> <n>
Porte 6  score ICP < <seuil>             -<n>  -> <n>
Porte 7  tiers                           A <n>, B <n>, C <n>
Manquant : <colonne> vide sur <n> lignes gardées
Sortie : qualifier-liste_<sujet>_<date>.csv (<n> lignes, <n> exclues)
Tier A, 5 lignes : <entreprise> <score> (<détail par critère>)
Exclues, 5 lignes : <entreprise> : <raison>
```

## Règles

- Aucun critère hors `05_Departements/Go-to-Market/contexte.md`. Un critère qui manque se demande, il ne s'invente pas.
- Aucune ligne supprimée : une ligne écartée porte `exclu = oui` et sa raison.
- Une donnée manquante ne fait jamais exclure.
- Le tri structurel (titre, effectif) passe avant le tri au jugement (B2C, concurrent, score).
- En cas de doute franc sur un B2C ou un concurrent, la ligne reste.
- Le poste actuel prime sur l'accroche du profil.
- Le score se recalcule après chaque enrichissement ; un `score_icp` n'est jamais figé.
- Le rapport montre toujours un échantillon avant qu'une étape payante ne parte sur la liste qualifiée.

## Exemples

- "Qualifie cet export Sales Nav de 1 200 lignes" : tri structurel d'abord (titre, effectif), puis jugement par lots de 200 ; réponse attendue : l'entonnoir, la répartition A, B, C, cinq lignes de chaque, et la proposition d'enrichir les lignes proches du seuil.
- "Enlève les B2C et les concurrents de ma liste" : portes 4 et 5 seulement, mots-clés puis jugement ; réponse attendue : le CSV complet avec `exclu` et `raison_exclusion`, le décompte par raison, cinq lignes ambiguës à trancher.
- "Qui est prioritaire dans ce fichier ?" : toutes les portes, puis départage dans le tier A ; réponse attendue : les tiers, les 10 premières lignes avec la raison de leur rang, et le next step `sourcer-personnes` ou `nettoyer-verifier`.
