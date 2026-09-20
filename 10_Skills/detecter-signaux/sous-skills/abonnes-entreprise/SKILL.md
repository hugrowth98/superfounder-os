---
name: abonnes-entreprise
description: >
  Détecte les personnes de votre cible qui suivent votre page entreprise LinkedIn (filtre Sales
  Navigator "Suit votre entreprise", croisé avec vos personas), garde les nouveaux abonnés depuis le
  dernier run et déclenche une approche qui donne avant de demander, sous 48 heures. Se déclenche
  sur : "qui suit ma page", "abonnés de ma page entreprise", "followers de la page", "nouveaux
  abonnés", "les DRH qui suivent ma boîte". Ne pas utiliser pour les abonnés d'une page qui n'est pas
  la vôtre (non listable : voir `signaux-concurrents`, engageurs), pour les réactions à vos posts
  (voir `engagement-contenu`), ni pour vos visiteurs de profil (voir `visite-profil`).
---

Un abonné de votre page a accepté de recevoir ce que vous publiez : il connaît votre nom, pas forcément votre offre. LinkedIn n'exporte pas la liste des abonnés d'une page, mais Sales Navigator la filtre pour la page reliée à votre compte. Un abonnement vaut 15 points, la fenêtre va de j0 à j2 pour un nouvel abonné, et le bon message donne quelque chose avant de demander quoi que ce soit.

## Ressources

- `{SKILL_BASE}/ressources/bareme-signaux.md` : abonnement à votre page 15.
- `{SKILL_BASE}/ressources/fenetres-fraicheur.md` : nouvel abonné j0 à j2, frais 30 jours.
- `{SKILL_BASE}/ressources/plays-signaux.md` : play 11 (nouveaux abonnés et engageurs), play 5 (ressource), play 4 (enquête).
- `{SKILL_BASE}/ressources/test-et-alors.md` : un abonnement ne se cite pas, un sujet se continue.

## Méthode

1. **Vérifier le prérequis.** Le compte Sales Navigator doit être relié à votre page entreprise (vous en êtes administrateur). Sinon le filtre ne rend rien, et la voie reste les engageurs de vos posts (`engagement-contenu`).
2. **Fixer la requête une fois** : les titres du persona (ou `--persona btl`), la zone, et `--suit-entreprise`. Enregistrez-la.
3. **Lancer chaque semaine** avec votre compte (Unipile) ou vos cookies. Le premier run donne le stock (tous les abonnés dans la cible) ; les suivants, les nouveaux.
4. **Garder les nouveaux** avec `dedoublonner --contre <run précédent>`, puis contre HubSpot et les séquences en cours. Le stock du premier run se travaille à part, en 1:many.
5. **Qualifier.** ICP, exclusion des salariés, des partenaires, des clients et des concurrents : sur une page, un abonné sur trois est un proche.
6. **Dater.** `signal_date` = date du run où la personne apparaît. j0 à j2 pour le message de bienvenue ; après, nurture.
7. **Choisir l'angle** : ce que vous publiez et ce que la personne y trouvera (une ressource, un cas, une prise de position), jamais "merci de suivre ma page". Le message est utile sans vente ; la vente vient au second signal.
8. **Envoyer sous 48 h**, LinkedIn d'abord, 1:many pour le stock, 1:1 pour un nouvel abonné tier A. Empilez avec `visite-profil` et `engagement-contenu` : abonné, visiteur et commentateur dans le même mois, c'est un Chaud.

## Exécution

| Étape | Verbe | Skill d'exécution | Paramètres et notes |
|---|---|---|---|
| 2 | construire_requete_salesnav | `construire-requete-salesnav` | `--persona btl --region France --suit-entreprise --nom "abonnés BTL" --enregistrer` |
| 3 | trouver_personnes | `trouver-personnes` | `--source unipile --url "<url>" --signal abonne_entreprise --max 500` (votre compte) ou `--source salesnav` (vos cookies, 0,005 $ par résultat). Ne marche qu'avec le compte relié à la page. |
| 4 | dedoublonner | `dedoublonner` | `--contre <run précédent>`, puis `--hubspot` |
| 5 | qualifier_liste | `qualifier-liste` | ICP, exclusions (salariés, partenaires, clients, concurrents) |
| 6 | enrichir_personne | `enrichir-personne` | `--posts` sur les tiers A : le sujet qu'ils portent |
| 7 | envoyer_sequence | `envoyer-sequence` | LinkedIn j0 (message utile, sans vente), email j7 avec une ressource si le canal existe |
| 8 | verifier_reponses | `verifier-reponses` | à j3 et j7 |

**CSV en entrée** : aucun ; le CSV du run précédent pour l'étape 4.

**CSV en sortie** : colonnes normalisées, plus `signal_type` (`abonne_entreprise`), `signal_date` (date du run), `signal_detail` ("suit votre page entreprise (Sales Navigator)"), `fraicheur`, `source`. Nom : `trouver-personnes_abonnes-<persona>_<date>.csv`.

## Repères

| Repère | Valeur |
|---|---|
| Points | 15 (barème : abonnement à votre page) |
| Fenêtre | j0 à j2 pour un nouvel abonné, frais 30 jours |
| Cadence | chaque semaine |
| Abonnés hors cible | un sur trois (proches, salariés, partenaires) |
| Message | utile, sans vente, 1:many pour le stock, 1:1 pour un tier A |

## Template

```
Requête : abonnés <persona>, <zone>, rejouée chaque <jour>
Stock (premier run) : <n> abonnés dans la cible, traités en 1:many le <date>
Run du <date> : <n> nouveaux, <n> dans l'ICP
À écrire sous 48 h : <n>, message sur <sujet publié>, ressource jointe : <laquelle>
```

## Règles

- L'abonnement ne se cite pas ; le sujet de vos publications, oui.
- Pas de message de vente au premier contact : une ressource, une question, un cas.
- Le stock se traite une fois, en 1:many ; ensuite seuls les nouveaux abonnés reçoivent un message.
- Sans page reliée au compte, ce sous-skill ne s'applique pas : `engagement-contenu` prend le relais.
- Les abonnés d'une page qui n'est pas la vôtre ne se listent pas : `signaux-concurrents` passe par leurs engageurs.

## Exemples

- "Qui suit ma page dans ma cible ?" : requête `--persona btl --suit-entreprise`, run Unipile, qualification ; réponse attendue : le stock trié par tier, et un message 1:many utile à valider.
- "Des nouveaux abonnés cette semaine ?" : run rejoué, diff contre la semaine dernière ; réponse attendue : les nouveaux dans l'ICP, avec l'angle par ligne, et les lignes qui empilent un autre signal.
- "Un DRH d'un compte cible vient de s'abonner" : `enrichir-personne --posts`, recherche d'un second signal, message 1:1 sous 48 h ; réponse attendue : un message de bienvenue avec une ressource, sans vente.
