---
name: multi-signaux
description: >
  Empile les signaux d'une même personne ou d'un même compte, calcule le score cumulé avec les multiplicateurs de fraîcheur, classe la liste par chaleur et fixe l'action et le délai de chaque ligne. Se déclenche sur : "empiler les signaux", "score cumulé", "quel prospect contacter en premier", "qui j'appelle en premier", "dans quel ordre", "priorise ma liste", "plusieurs signaux", "seuils d'action", "SLA", "système de scoring", "file de priorité", "chaleur d'un compte", "comité d'achat". Ne pas utiliser pour : détecter un seul type de signal, voir le sous-skill de ce signal ; un prospect sans aucun signal, retour au ciblage ICP.
---

Trois signaux ou plus sur le même compte donnent 35 à 40 % de réponses contre 6 à 8 % à froid : ce sous-skill additionne, pondère par la fraîcheur, classe, et dit qui contacter dans l'heure, dans la journée, dans la semaine.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : points, multiplicateurs, seuils, exemples d'empilement, recalibrage.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : la position de chaque signal dans sa fenêtre.
- `{SKILL_BASE}/ressources/plays-signaux.md` : le play qui correspond à chaque niveau de chaleur.
- `{SKILL_BASE}/ressources/detection-par-signal.md` : fiabilité d'un signal pris seul.

## Méthode

1. **Rassembler** les CSV produits par les sous-skills (un par signal) et les signaux saisis à la main (demandes entrantes, webinars, intros).
2. **Fusionner par personne** : clé `linkedin_url`, sinon `email`, sinon `prenom + nom + entreprise`. Une ligne par personne, `signal_type` joints par `+`, `signal_detail` joints par ` | `, `signal_date` = la plus récente, `fraicheur` = jours depuis cette date.
3. **Pondérer chaque signal** : points du barème × multiplicateur. Courbe rapide (engagement, champion, actualité, avis) selon l'ancienneté ; courbe lente (levée, recrutement, techno, événement, nouveau dirigeant) selon la position dans la fenêtre.
4. **Additionner** dans `score_signal`, arrondi à l'entier.
5. **Regrouper par compte** (`domaine`) : deux personnes ou plus avec un signal dans les 30 jours, on ajoute 70 au compte et on le traite comme une seule affaire (colonne de travail `comite = oui` ; `tier` reste le tier ICP).
6. **Classer** : score décroissant, puis signal le plus récent en premier à score égal. Brûlant toujours en tête.
7. **Fixer l'action et le délai** par niveau (Repères). Un signal trop tôt (semaine 1 d'une levée, j0 à j13 d'une nomination) garde son score mais son action est datée à l'ouverture de la fenêtre.
8. **Passer le test "et alors ?"** sur chaque ligne Chaud et Brûlant : l'empilement donne l'angle, le message n'en cite aucun.
9. **Livrer la file de priorité** (Template) et lancer les verbes d'action.
10. **Revoir chaque mois** : seuils après 30 jours, points après 3 mois, à partir des rendez-vous obtenus par signal.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 0 | detecter_signal | `detecter-signaux` (script `detecter_signal.py`, `--source theirstack`) | si TheirStack est branché : `--type intent --technos <techno de la couche 2> --nb-offres-min 3` donne d'un coup les entreprises qui recrutent et utilisent la techno, déjà empilées (offre 40 + techno) ; à fusionner avec les autres runs |
| 1 | dedoublonner | `dedoublonner` | fusion multi-sources par `linkedin_url`, `email`, puis nom + entreprise ; rapprochement HubSpot (client, deal ouvert, déjà en séquence : on sort ou on marque) |
| 2 | calcul | interne (Claude) | points × multiplicateur par signal, somme, arrondi ; bonus comité par `domaine` ; `chaleur` selon les seuils ; classement |
| 3 | qualifier_liste | `qualifier-liste` | `score_icp` et `tier` : un score signal élevé sur un compte hors ICP reste Froid |
| 4 | trouver_telephone | `trouver-telephone` | lignes Brûlant : l'appel vient en premier |
| 5 | trouver_email | `trouver-email` | lignes Chaud et Tiède sans email vérifié |
| 6 | envoyer_sequence | `envoyer-sequence` | Chaud : séquence 1:1 courte ; Tiède : séquence par signal dominant ; Frais : nurture |
| 7 | verifier_reponses | `verifier-reponses` | chaque jour sur Brûlant et Chaud ; une réponse arrête tout et remonte dans HubSpot |

**CSV en entrée** : les CSV des sous-skills, colonnes normalisées, avec `signal_type`, `signal_date`, `signal_detail`, `score_signal` par signal.

**CSV en sortie** : une ligne par personne, colonnes normalisées, `signal_type` cumulé, `signal_detail` cumulé, `signal_date` (la plus récente), `fraicheur`, `score_signal` (total), `chaleur` (`brulant`, `chaud`, `tiede`, `frais`, `froid`), `tier` inchangé (le tier ICP écrit par `qualifier-liste`, jamais écrasé), plus trois colonnes de travail : `comite` (`oui` quand deux personnes ou plus du même `domaine` portent un signal dans les 30 jours), `action` et `avant_le` (date limite de contact). Nom : `multi-signaux_<sujet>_<date>.csv`.

## Repères

| Score | Chaleur | Action | Délai | Qui |
|---|---|---|---|---|
| 150 et plus | Brûlant | appel, puis message écrit le même jour | moins d'1 h | vous, à la main |
| 100 à 149 | Chaud | message 1:1 écrit pour cette personne, séquence courte | moins de 24 h | vous, ou séquence 1:1 |
| 50 à 99 | Tiède | séquence semi-personnalisée sur le signal dominant, surveillance | moins de 72 h | séquence |
| 20 à 49 | Frais | nurture : newsletter, invitation, contenu | cette semaine | automatique |
| 0 à 19 | Froid | rien, on surveille | en continu | système |

| Combinaison | Ce que ça vaut | Traitement |
|---|---|---|
| Tier 1 + Tier 1 (champion + levée ; nouveau dirigeant + retrait d'un concurrent) | Brûlant ou Chaud | à la main, le jour même |
| Tier 2 + Tier 2 (offre + commentaire ; levée + offre ; avis négatif + engagement) | Chaud ou Tiède | séquence prioritaire |
| Tier 3 seul (actualité, abonné, pub active) | Frais | nurture |
| 3 signaux ou plus, quels qu'ils soient, dans leur fenêtre | Chaud au minimum | on écrit le jour même |

| Repère | Valeur |
|---|---|
| Réponses, 3 signaux ou plus | 35 à 40 % ; un signal, 18 à 22 % ; à froid, 6 à 8 % |
| Valeur des contrats signés sur signal | 3 à 4 fois la référence à froid |
| Perte de valeur d'un signal | la moitié en 7 jours |
| Fraîcheur contre nombre | un signal Tier 1 de ce matin (75×1,5 = 113, Chaud) bat trois signaux Tier 2 de deux mois ((45+40+25)×0,3 = 33, Frais) |
| Capacité | vous : 5 Brûlant par jour à la main ; séquence : 20 Chaud par jour |

## Template

La file de priorité, livrée en tableau au-dessus du CSV :

```
| Rang | Personne | Entreprise | Signaux (du plus récent au plus ancien) | Score | Chaleur | Action | Avant le |
|---|---|---|---|---|---|---|---|
| 1 | {{prenom nom}} | {{entreprise}} | commentaire (ce matin), offre business developer (j18), levée Série A (semaine 3) | 165 | Brûlant | appel + message | aujourd'hui 12h |
| 2 | {{prenom nom}} | {{entreprise}} | nouveau directeur commercial (j21), like (j4) | 90 | Tiède | séquence "nouveau dirigeant" | {{date}} |
| ... | | | | | | | |
```

Sous le tableau : les lignes "trop tôt" avec leur date d'ouverture, et les lignes retirées avec la raison (hors ICP, déjà client, en séquence, signal expiré).

Message empilé, quand deux signaux se répondent (on n'en cite aucun) :

```
Bonjour {{prenom}},

Recruter {{n}} commerciaux en un trimestre, c'est {{n}} intégrations à mener sans process écrit, pendant que {{ce_qui_attend}}. {{client_similaire}} a écrit le sien en {{delai}} et ramené le ramp de {{avant}} à {{apres}}.

Le process existe déjà chez vous, ou il reste à écrire ?
```

## Règles

- La fraîcheur compte plus que le nombre : un signal chaud d'hier passe devant trois signaux tièdes du mois dernier.
- Un score élevé sur un compte hors ICP reste Froid : le signal ne remplace pas la cible.
- Une réponse, un rendez-vous ou un deal ouvert dans HubSpot arrêtent la séquence, quel que soit le score.
- Le message n'énumère jamais les signaux : l'empilement sert à choisir l'angle et le délai, pas à prouver qu'on a surveillé.
- Un signal "trop tôt" ne déclenche rien avant l'ouverture de sa fenêtre, même s'il fait passer le score en Brûlant.
- On ne dépasse pas sa capacité : 5 Brûlant par jour à la main ; le reste attend demain, classé.
- Le barème se recalibre chaque mois sur les rendez-vous obtenus, jamais sur l'impression.
- Sans `05_Departements/Go-to-Market/contexte.md` rempli (ICP, personas, 5 signaux prioritaires), on ne score pas : on ne saurait pas quoi exclure.

## Exemples

- "Voilà ma liste de la semaine, qui j'appelle en premier ?" : fusion des CSV, score par signal × fraîcheur, bonus comité, classement, file de priorité en tableau avec action et date limite, puis trouver_telephone sur les Brûlant.
- "Cette boîte a levé il y a 3 semaines, recrute deux SDR depuis 15 jours et son CEO a commenté mon post ce matin" : 35×1,5 + 40×1,5 + 35×1,5 = 165, Brûlant ; test "et alors ?" (une première équipe commerciale à construire) ; appel dans l'heure, message le jour même, sans citer les trois signaux.
- "Construis-moi un système de scoring" : 5 à 10 signaux choisis dans `05_Departements/Go-to-Market/contexte.md`, points du barème, deux courbes de fraîcheur, seuils 150 / 100 / 50 / 20, une action, un délai et un responsable par seuil, un play par seuil, revue mensuelle.
