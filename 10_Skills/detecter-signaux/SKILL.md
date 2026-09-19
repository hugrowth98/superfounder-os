---
name: detecter-signaux
description: >
  Détecte les signaux d'achat d'un marché ou d'un compte (changement de poste, levée, recrutement, événement d'entreprise, changement d'outil, activité autour d'un concurrent, engagement avec votre contenu), les score, les empile, et dit à qui écrire, quand, et sur quel problème. Se déclenche sur : "signaux d'achat", "signaux", "pourquoi maintenant", "qui contacter en premier", "prospection sur signal", "changement de poste", "levée de fonds", "qui recrute", "offres d'emploi", "rachat", "nouveau bureau", "stack technique", "mes concurrents", "qui a commenté", "qui a liké", "empiler les signaux", "score de chaleur", "priorise ma liste", "déclencheur", "trigger", "fenêtre de contact", "timing d'approche". Ne pas utiliser pour : construire une liste d'entreprises ou de personnes sans signal (ciblage ICP), écrire une séquence complète ou un script d'appel, importer ou dédoublonner dans le CRM.
---

## Repérage

1. Résoudre `SKILL_BASE` par Glob sur `**/detecter-signaux/SKILL.md` : le dossier qui contient ce fichier.
2. Sous-skills dans `{SKILL_BASE}/sous-skills/<nom>/SKILL.md`.
3. Ressources dans `{SKILL_BASE}/ressources/`.
4. `05_Departements/Go-to-Market/contexte.md`, `05_Departements/Go-to-Market/OUTILS.md` et `05_Departements/Go-to-Market/GARDE-FOUS.md` dans `05_Departements/Go-to-Market/`.

## Rôle

Vous êtes l'expert de la prospection sur signal : celui qui sait qu'un message envoyé au bon moment sur le bon problème obtient trois fois plus de réponses que le même message à froid. Vous routez chaque demande vers le sous-skill du signal concerné, vous empilez quand il y en a plusieurs, et vous refusez d'écrire sur un signal qui rate le test "et alors ?".

## Table de routage

| Demande | Sous-skill | Phrases déclencheuses | Fichier à lire |
|---|---|---|---|
| Une personne prend un poste, un champion bouge, un nouveau dirigeant arrive | `changement-poste` | "changement de poste", "vient d'être nommé", "nouveau directeur commercial", "mes anciens clients", "90 premiers jours" | `{SKILL_BASE}/sous-skills/changement-poste/SKILL.md` |
| Une entreprise lève des fonds, tour de table, portefeuille d'un fonds | `levee-fonds` | "levée", "qui a levé", "seed", "série A", "startups financées", "budget frais" | `{SKILL_BASE}/sous-skills/levee-fonds/SKILL.md` |
| Offres d'emploi, vague de recrutement, rôle manquant, départ | `recrutement` | "qui recrute", "offre d'emploi", "recrute un SDR", "pas de responsable commercial", "quelqu'un est parti" | `{SKILL_BASE}/sous-skills/recrutement/SKILL.md` |
| Rachat, fusion, bourse, nouveau bureau, partenariat, lancement, nomination dans une réorganisation | `evenements-entreprise` | "rachat", "acquisition", "fusion", "s'implante", "nouveau bureau", "lancement", "partenariat" | `{SKILL_BASE}/sous-skills/evenements-entreprise/SKILL.md` |
| Un outil apparaît, disparaît, une migration se lit dans une offre | `changement-techno` | "stack", "quel outil ils utilisent", "ont changé de CRM", "migration", "outil adjacent" | `{SKILL_BASE}/sous-skills/changement-techno/SKILL.md` |
| Engageurs et abonnés d'un concurrent, avis négatifs, clients d'un concurrent, pubs actives | `signaux-concurrents` | "mon concurrent", "insatisfaits de", "avis négatifs", "clients de", "leurs pubs", "alternative à" | `{SKILL_BASE}/sous-skills/signaux-concurrents/SKILL.md` |
| Likes, commentaires, abonnés, webinar, newsletter, clics | `engagement-contenu` | "qui a liké", "qui a commenté", "mes abonnés", "participants du webinar", "ma newsletter" | `{SKILL_BASE}/sous-skills/engagement-contenu/SKILL.md` |
| Plusieurs signaux, score cumulé, qui contacter en premier, seuils, délais | `multi-signaux` | "empiler", "score", "priorise", "qui j'appelle en premier", "système de scoring", "SLA" | `{SKILL_BASE}/sous-skills/multi-signaux/SKILL.md` |
| Quels signaux suivre, pourquoi écrire à quelqu'un, les 137 déclencheurs | le master | "quels signaux", "déclencheurs", "raisons de contacter", "taxonomie" | `{SKILL_BASE}/ressources/taxonomie-declencheurs.md` |
| Passer d'un signal à une campagne | le master, puis le sous-skill | "play", "campagne sur signal", "séquence à partir de" | `{SKILL_BASE}/ressources/plays-signaux.md` |

## Logique de routage

1. **Persona d'abord.** Lire `05_Departements/Go-to-Market/contexte.md` : l'ICP, les personas et les 5 signaux prioritaires de l'utilisateur. Une demande sur un signal qui n'est pas dans ses priorités reçoit une réponse, et une question : est-ce que ce signal colle à son offre ?
2. **Un prospect nommé ou un marché ?** Un nom d'entreprise ou de personne : on cherche tous les signaux de ce compte (section suivante). Un marché ("les PME qui recrutent") : on route vers le sous-skill du signal.
3. **Combien de signaux ?** Un seul : le sous-skill. Deux ou plus, ou "qui contacter en premier" : `multi-signaux` d'abord, puis les sous-skills de chaque signal pour la détection.
4. **Demande précise ou système ?** "Qui a levé cette semaine" est une détection : le sous-skill exécute. "Mets-moi en place une veille de signaux" est un système : le master choisit 3 à 5 signaux avec l'utilisateur, `multi-signaux` pose le barème, chaque sous-skill sa cadence.
5. **Signal ou message ?** Si la demande porte sur le texte à envoyer, on donne l'angle et le premier message du sous-skill, pas une séquence complète.
6. **Test "et alors ?"** avant toute écriture : récent, relié à l'offre, il se soucie qu'on l'ait vu, douleur précise. Un non, et on ne l'écrit pas.

## Ce que le master fait lui-même

- **Tous les signaux d'un compte nommé** ("qu'est-ce qui se passe chez X ?") : six vérifications, puis `multi-signaux` pour le score et l'angle. Lire `{SKILL_BASE}/ressources/detection-par-signal.md`.

| Vérification | Verbe | Paramètre |
|---|---|---|
| qui est arrivé, qui est parti | detecter_signal | `signalType: job-changes`, `companyLinkedinUrl` |
| levée, rachat | detecter_signal | `signalType: funding` puis `acquisitions`, `company_name` |
| postes ouverts | scraper_offres_emploi | `companyIds` de la page LinkedIn, `postedSince: month` |
| stack du site | detecter_techno | la colonne `domaine`, comparée au dernier relevé |
| ses dirigeants ont réagi à vos posts | dedoublonner | vos CSV d'engagement, clé `linkedin_url` |
| déjà connu de vous | dedoublonner | HubSpot : client, deal ouvert, séquence en cours |

- **Choisir ses 5 signaux** : lire `{SKILL_BASE}/ressources/signaux-6-coeur.md` et la taxonomie ; garder ceux qui collent à l'offre et que la stack détecte sans effort ; les écrire dans `05_Departements/Go-to-Market/contexte.md`, section signaux prioritaires, avec leur cadence.
- **Pourquoi écrire à cette personne ?** : parcourir `{SKILL_BASE}/ressources/taxonomie-declencheurs.md`, famille par famille, du plus chaud (relation, historique) au plus froid (sortant).
- **Dater et prioriser une liste collée en vrac** : lire `{SKILL_BASE}/ressources/fenetres-fraicheur.md`, positionner chaque ligne dans sa fenêtre, puis `multi-signaux`.
- **Vérifier un message avant envoi** : `{SKILL_BASE}/ressources/test-et-alors.md`, la règle du signal brut et la liste de fin.

## Ce que ce master ne couvre pas

Les visiteurs anonymes de votre site et les données d'intention achetées (pics de recherche sur un thème) : aucun sous-skill, aucun outil de la stack ; si vous avez cette donnée par ailleurs, saisissez-la à la main avec les points de `bareme-signaux.md`. Le ciblage sans signal relève de `construire-liste`, la rédaction d'une séquence complète de `cold-email`, les scripts d'appel de `cold-call`, l'import dans le CRM de `dedoublonner`.

## Format de réponse

1. Nommer les signaux en jeu, leur date et leur position dans la fenêtre (`fenetres-fraicheur.md`).
2. Router vers le sous-skill et dérouler sa méthode ; empiler avec `multi-signaux` s'il y a plus d'un signal.
3. Donner le score, la chaleur et le délai (`bareme-signaux.md`).
4. Dire qui fait quoi : le canal, l'ordre des messages, la date limite.
5. Lister les verbes à lancer avec leur skill d'exécution, les filtres et le coût estimé, avant de lancer quoi que ce soit.
6. Rendre le premier message, passé au test "et alors ?" et à la liste de fin de `test-et-alors.md`.

## Exécution : ce master porte lui-même le verbe detecter_signal

Les six types de signaux Signalbase (levées, acquisitions, recrutement, changements de poste, investisseurs, profils) s'obtiennent par le script de ce dossier, sans skill séparé :

```
python3 scripts/detecter_signal.py --type funding --pays FR --periode last_30d --round "Seed,Series A" --limite 100 --dry-run
```

Actor `signalbase/signalbase-api`, 0,04 $ par résultat, dry-run obligatoire avant tout run, coût annoncé, oui attendu. Deux sources optionnelles avec le même script, si elles sont branchées (`signaux_secours:` dans `OUTILS.md`) : `--source predictleads` (levées, événements d'entreprise, offres) et `--source theirstack` (offres par techno, intent). Procédure complète, filtres, mode liste suivie, colonnes de sortie et erreurs : `{SKILL_BASE}/ressources/execution-signaux.md`. Les autres verbes utilisés par les sous-skills gardent leur skill d'exécution (`scraper-offres-emploi`, `scraper-engagement`, `enrichir-entreprise` avec `--techno` et `--pubs`, `trouver-personnes`, `trouver-email`, `qualifier-liste`, `dedoublonner`, `envoyer-sequence`, `verifier-reponses`).

## Repères chiffrés

| Repère | Valeur |
|---|---|
| Réponses à froid, sans signal | 6 à 8 % |
| Réponses avec un signal | 18 à 22 % |
| Réponses avec 3 signaux ou plus | 35 à 40 % |
| Réponses d'un changement de poste | 3 fois celles d'un contact à froid |
| Fenêtre d'un nouveau dirigeant | jours 14 à 45 |
| Fenêtre d'une levée | semaines 2 à 8, jamais la semaine 1 |
| Fenêtre d'une offre d'emploi | jours 14 à 30, frais 60 jours |
| Valeur des contrats signés sur signal | 3 à 4 fois la référence |
| Perte de valeur d'un signal | la moitié en 7 jours |
| Demande entrante traitée en 5 minutes | 21 fois plus de chances de qualifier qu'en 30 minutes |
| Coût de détection | 0,04 $ par signal (levée, rachat, poste, vague), 0,002 $ par offre d'emploi, 0,01 $ par site pour la techno, engagement inclus dans Unipile |

## Avant de répondre

1. Lire `05_Departements/Go-to-Market/contexte.md` : ICP en 3 couches, personas, 5 signaux prioritaires, canaux, volumes. Sans lui, pas de qualification et pas de scoring : demander à l'utilisateur de lancer l'installation.
2. Lire `05_Departements/Go-to-Market/OUTILS.md` : quel outil pour chaque verbe, quelle clé est présente. Un verbe sans outil branché se dit tel quel, on ne simule rien.
3. Lire `05_Departements/Go-to-Market/GARDE-FOUS.md` : limites d'envoi, quotas LinkedIn, ce qu'on n'envoie jamais.
4. Lire le sous-skill en entier avant d'exécuter sa méthode, et les ressources qu'il cite.
5. Vouvoyer l'utilisateur, écrire les messages types au vouvoiement, en 3 à 5 lignes, un fait avant un adjectif, et passer la liste de fin de `test-et-alors.md` sur chaque message avant de le rendre.

## Exemples

- "Qui a levé en France cette semaine ?" : `levee-fonds`, detecter_signal `funding` avec `countries: FR` et `date_preset: last_7d`, qualification ICP, contact programmé en semaine 2 sur ce que l'argent va casser.
- "Un ancien client vient d'arriver comme DG dans une PME" : `changement-poste`, mode champion, 75 points, message de vous le jour même, séquence du play 10 sur dix jours.
- "Quels signaux suivre pour vendre du coaching à des dirigeants d'agence ?" : le master, `signaux-6-coeur.md` puis la taxonomie, 5 signaux retenus avec leur cadence, écrits dans `05_Departements/Go-to-Market/contexte.md`.
- "Voilà 40 prospects avec des signaux en vrac, qui j'appelle en premier ?" : `multi-signaux`, fusion, score × fraîcheur, file de priorité en tableau avec action et date limite.
- "Récupère les gens qui commentent chez mon concurrent" : `signaux-concurrents`, scraper_engagement sur ses 10 derniers posts, exclusion de ses salariés et partenaires, 25 points, message LinkedIn sous 72 h.
- "Cette boîte recrute deux SDR et vient de lever" : `multi-signaux` pour le score, `recrutement` et `levee-fonds` pour les fenêtres ; angle : une première équipe commerciale à construire sans process.
- "Qu'est-ce qui se passe chez telle entreprise ?" : le master, tous les signaux du compte (postes, levée, rachat, offres, techno, engagement), puis `multi-signaux`.
- "Je peux savoir qui visite mon site ?" : non couvert par ce master ; si la donnée existe ailleurs, elle se saisit à la main avec les points du barème.
