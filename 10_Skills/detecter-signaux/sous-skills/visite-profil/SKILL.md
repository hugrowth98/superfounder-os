---
name: visite-profil
description: >
  Détecte les personnes de votre cible qui ont consulté votre profil LinkedIn récemment (filtre Sales
  Navigator "Vues de profil récentes", croisé avec vos personas), garde les nouvelles depuis le
  dernier run et déclenche l'approche sous 48 heures sur votre sujet, jamais sur la visite. Se
  déclenche sur : "qui a visité mon profil", "vues de profil", "ils sont passés sur mon profil", "qui
  regarde mon profil", "visiteurs de mon profil", "les CEO qui ont vu mon profil". Ne pas utiliser
  pour les réactions à vos posts (voir `engagement-contenu`), pour les abonnés de votre page (voir
  `abonnes-entreprise`), ni pour un compte qui n'est pas le vôtre (LinkedIn ne le donne pas).
---

Quelqu'un qui consulte votre profil vous a cherché, ou vous a croisé et a voulu en savoir plus : il vous connaît, il est sur LinkedIn cette semaine, et il n'a rien demandé. Sales Navigator liste ces personnes pour votre compte ; filtrées sur vos personas, c'est la liste la plus chaude que vous n'avez pas encore contactée. Une visite vaut 20 points (proposé), la fenêtre va de j0 à j7 après la détection.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : visite de profil 20, empilement avec une réaction ou un changement de poste.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : visite j0 à j7, frais 30 jours, courbe rapide.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 11 (nouveaux abonnés et engageurs), play 5 (ressource pour ouvrir).
- `{SKILL_BASE}/ressources/test-et-alors.md` : la visite ne se cite jamais ; le sujet, oui.

## Méthode

1. **Fixer la requête une fois.** Les titres du persona (ou `--persona atl`), la zone, et le filtre `--vues-profil`. LinkedIn ne donne pas la date exacte de la visite, seulement "récente" : c'est la répétition du run qui date le signal. Enregistrez la requête (`--enregistrer`), elle se rejoue telle quelle.
2. **Lancer chaque semaine, le même jour**, avec votre compte (Unipile, gratuit) ou vos cookies (actor, 0,005 $ par résultat). Le filtre ne marche qu'avec le compte dont c'est le profil.
3. **Garder les nouveaux.** `dedoublonner --contre <csv du run précédent>` : une visite déjà vue la semaine dernière n'est pas un nouveau signal. Puis contre HubSpot et les séquences en cours.
4. **Qualifier.** ICP, exclusion des concurrents, des clients, des recruteurs et des commerciaux qui vous prospectent : sur un profil visible, la moitié des visiteurs sont hors cible.
5. **Dater.** `signal_date` = date du run. j0 à j7 : pic. Après 30 jours, contexte.
6. **Empiler.** Une visite plus une réaction à un post, un changement de poste ou une offre ouverte, et la ligne passe Chaud (`multi-signaux`). Une visite seule reste Tiède : on écrit, mais court.
7. **Choisir l'angle** : le sujet qu'il est venu chercher (votre titre, votre dernier post, votre offre), et une question sur son cas. Jamais "vous avez visité mon profil" : ça met la personne en faute, et elle ne répond pas.
8. **Envoyer sous 48 h**, LinkedIn d'abord (il y est) : invitation avec une note courte s'il n'est pas en relation, message direct sinon. Email à j3 sans réponse, une relance à j7 sur un autre angle, puis stop.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 1 | construire_requete_salesnav | `construire-requete-salesnav` | `--persona atl --region France --vues-profil --nom "visites ATL" --enregistrer` (ajoutez `--effectif`, `--titres-exclus "assistant,stagiaire"`) |
| 2 | trouver_personnes | `trouver-personnes` | `--source unipile --url "<url>" --signal visite_profil --max 200` (votre compte, inclus dans l'abonnement) ou `--source salesnav --url "<url>" --signal visite_profil` (vos cookies, 0,005 $ par résultat). Le CSV reçoit `signal_type = visite_profil`, `signal_date` = date du run, `degre_relation` avec Unipile. |
| 3 | dedoublonner | `dedoublonner` | `--contre <run précédent>` (les nouveaux seulement), puis `--hubspot` et les séquences en cours |
| 4 | qualifier_liste | `qualifier-liste` | ICP, exclusions (concurrents, clients, recruteurs) |
| 5 | enrichir_personne | `enrichir-personne` | `--posts` : son dernier post donne l'angle ; `anciennete_poste` dit s'il vient d'arriver (second signal) |
| 6 | trouver_email | `trouver-email` | seulement si le canal email est prévu à j3 |
| 7 | envoyer_sequence | `envoyer-sequence` | LinkedIn j0 (invitation avec note, ou message), email j3, relance j7, puis stop |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 ; une réponse arrête tout |

**CSV en entrée** : aucun, la requête suffit ; le CSV du run précédent pour l'étape 3.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`visite_profil`), `signal_date` (date du run, pas de la visite), `signal_detail` ("a consulté votre profil (Sales Navigator, vues de profil récentes)"), `fraicheur`, `source` (`unipile` ou `curious_coder/linkedin-sales-navigator-search-scraper`). Nom : `trouver-personnes_visites-<persona>_<date>.csv`.

## Repères

| Repère | Valeur |
|---|---|
| Points | 20 (proposé, entre l'abonnement 15 et le like 25) |
| Fenêtre | j0 à j7 après la détection, frais 30 jours |
| Cadence | chaque semaine, le même jour |
| Part de visiteurs hors cible | environ la moitié (recruteurs, commerciaux, curieux) |
| Volume | limité à 2 500 par recherche, rarement atteint |
| Canal | LinkedIn d'abord, email à j3 |

## Template

```
Requête : visites <persona>, <zone>, rejouée chaque <jour>
Run du <date> : <n> visiteurs, <n> nouveaux depuis le <date précédente>, <n> dans l'ICP après qualification
À écrire sous 48 h : <n> (Chaud : <n> avec un second signal)
Message : invitation ou message sur <sujet>, jamais sur la visite
```

## Règles

- La visite ne se cite jamais dans le message.
- Le diff contre le run précédent est obligatoire : sans lui, la même personne reçoit un message chaque semaine.
- Une visite seule ne déclenche pas d'appel ; empilée avec un changement de poste ou une offre, oui.
- Le run tourne sur votre compte, dans les quotas de `05_Departements/Go-to-Market/GARDE-FOUS.md` ; pas de visite en retour en masse.
- Un visiteur déjà en séquence ou déjà client sort de la liste avant toute écriture.

## Exemples

- "Qui a visité mon profil cette semaine dans ma cible ?" : requête `--persona atl --vues-profil`, run Unipile, diff contre la semaine dernière, qualification ; réponse attendue : la liste des nouveaux visiteurs dans l'ICP, avec un angle par ligne et les lignes Chaud en tête.
- "Un CEO de ma cible est passé sur mon profil hier" : `enrichir-personne --posts` sur lui, recherche d'un second signal (poste, offre), message sous 48 h sur son sujet ; réponse attendue : une invitation avec note de 300 caractères au plus, ou un message s'il est en relation.
- "Mets-moi une veille sur les visites" : requête enregistrée, rappel hebdomadaire, diff automatique, sortie dans `Signaux/` ; réponse attendue : le plan de cadence et le premier run.
