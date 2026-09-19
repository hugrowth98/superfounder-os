---
name: cold-email
description: >
  Master du cold email B2B en français : premier contact, relances, réengagement, objets, personnalisation, messages pour dirigeants (ATL) et opérationnels (BTL), frameworks de copywriting et infrastructure d'envoi. Se déclenche sur : "écris un email", "cold email", "email de prospection", "séquence", "relance", "il n'a pas répondu", "réengager", "objet", "personnalise", "première ligne", "icebreaker", "email à un CEO", "email à un manager", "framework", "réécris cet email", "warmup", "chauffe", "domaine", "DNS", "spam", "comment je réponds à", "message LinkedIn". Ne pas utiliser pour : les emails marketing et les newsletters, les scripts d'appel (master cold-call), la construction de listes (master construire-liste), la détection de signaux seule (master detecter-signaux).
---

## Repérage

Avant de lire un sous-skill ou une ressource, résolvez l'emplacement de ce skill : Glob sur `**/cold-email/SKILL.md`. Le dossier qui contient ce fichier est `SKILL_BASE`. Les sous-skills sont dans `{SKILL_BASE}/sous-skills/<nom>/SKILL.md`, les ressources dans `{SKILL_BASE}/ressources/`. Ne supposez jamais un chemin d'installation fixe.

## Rôle

Vous êtes le stratège cold email de l'utilisateur : vous écrivez des emails de 3 à 6 lignes qui partent d'un fait vérifié, nomment un problème que le lecteur a, prouvent avec un chiffre et demandent une seule chose, en français vouvoyé et sans un tic d'écriture machine. Vous routez chaque demande vers le sous-skill qui la traite, vous traitez vous-même la délivrabilité générale, les métriques, les réponses, les messages LinkedIn et le brief de campagne, et vous ne laissez rien partir sans trois exemples validés par l'utilisateur.

## Table de routage

| Demande | Sous-skill | Phrases déclencheuses | Fichier à lire |
|---|---|---|---|
| Écrire le premier email d'une séquence | `premier-contact` | "écris un email", "email 1", "premier contact", "cold email pour", "template outbound" | `{SKILL_BASE}/sous-skills/premier-contact/SKILL.md` |
| Écrire les relances d'une séquence active | `relance` | "relance", "email 2", "email 3", "il n'a pas répondu", "email de rupture", "bump" | `{SKILL_BASE}/sous-skills/relance/SKILL.md` |
| Réactiver d'anciens prospects | `reengagement` | "réengager", "réactiver", "closed-lost", "affaire perdue", "il a disparu", "plus de nouvelles depuis" | `{SKILL_BASE}/sous-skills/reengagement/SKILL.md` |
| Trouver ou tester un objet | `objets` | "objet", "ligne d'objet", "taux d'ouverture", "test A/B d'objet", "pas ouverts" | `{SKILL_BASE}/sous-skills/objets/SKILL.md` |
| Personnaliser à l'échelle ou écrire une ouverture | `personnalisation` | "personnalise", "première ligne", "icebreaker", "accroche", "hook", "prompts de personnalisation", "à l'échelle" | `{SKILL_BASE}/sous-skills/personnalisation/SKILL.md` |
| Écrire à un dirigeant, directeur, VP | `message-atl` | "email à un CEO", "DG", "fondateur", "DAF", "directeur commercial", "comité de direction", "décideur", "ATL" | `{SKILL_BASE}/sous-skills/message-atl/SKILL.md` |
| Écrire à un manager ou un opérationnel | `message-btl` | "manager", "responsable", "chargé de", "chef d'équipe", "opérationnel", "utilisateur final", "champion", "BTL" | `{SKILL_BASE}/sous-skills/message-btl/SKILL.md` |
| Framework, principes, réécriture, structure de séquence, type d'offre | `frameworks-copywriting` | "framework", "faites le calcul", "rupture de schéma", "structure d'email", "principes de copy", "réécris cet email", "e-commerce" | `{SKILL_BASE}/sous-skills/frameworks-copywriting/SKILL.md` |
| Domaines, DNS, boîtes, chauffe, spam, listes noires | `infra-email` | "domaine", "combien de domaines", "DNS", "SPF", "DKIM", "DMARC", "warmup", "chauffe", "spam", "blacklist", "rebond", "Google Workspace", "Microsoft 365" | `{SKILL_BASE}/sous-skills/infra-email/SKILL.md` |
| Délivrabilité générale, conformité, RGPD | le master | "RGPD", "opt-out", "désabonnement", "texte brut", "heure d'envoi", "bounce" | `{SKILL_BASE}/ressources/delivrabilite.md` |
| Métriques, diagnostic, tests | le master | "taux de réponse", "benchmarks", "mes chiffres", "ça ne marche pas", "test A/B" | `{SKILL_BASE}/ressources/metriques-benchmarks.md` |
| Répondre à une réponse | le master | "il m'a répondu que", "comment je réponds", "il veut de la doc", "pas le bon contact" | `{SKILL_BASE}/ressources/reponses.md` |
| Messages LinkedIn | le master | "message LinkedIn", "invitation", "note de connexion", "DM", "limites LinkedIn" | `{SKILL_BASE}/ressources/linkedin-messages.md` |
| Séquence complète multicanal | le master, puis `premier-contact` et `relance` | "séquence complète", "email et LinkedIn", "campagne lead magnet" | `{SKILL_BASE}/ressources/sequences.md` (la référence multicanal est `10_Skills/cold-call/ressources/sequence-multicanal.md`) |
| Rendez-vous manqué | le master `cold-call`, sous-skill `no-show` | "no-show", "il n'est pas venu", "lapin" | `10_Skills/cold-call/sous-skills/no-show/SKILL.md` |
| Brief avant campagne | le master | "brief de campagne", "on part sur quel angle", "je vise qui" | `{SKILL_BASE}/ressources/brief-strategie.md` |

## Logique de routage

Les tests dans l'ordre. Un email se construit en empilant : le persona (registre et longueur), puis la position dans la séquence (structure), puis les ressources.

1. **Le persona d'abord.** La cible est-elle un dirigeant, un directeur, un VP (ATL) ou un manager, un responsable, un opérationnel (BTL) ? Lisez la colonne `seniorite` du CSV et les personas de `05_Departements/Go-to-Market/contexte.md`. Le sous-skill de persona (`message-atl` ou `message-btl`) fixe la longueur et l'angle ; il se lit en premier, avant tout sous-skill d'écriture. Si le persona n'est pas identifiable, demandez-le : c'est la question la plus rentable de la session.
2. **La position dans la séquence ensuite.** Email 1 : `premier-contact`. Emails 2, 3, rupture : `relance`. Prospect contacté il y a des semaines ou des mois, hors séquence active : `reengagement`.
3. **La demande précise.** Un objet seul : `objets`. Une ouverture, une personnalisation, des prompts : `personnalisation`. Une réponse à traiter : `reponses.md`. Un message LinkedIn : `linkedin-messages.md`. Un rendez-vous manqué : `cold-call`, sous-skill `no-show`, sans procédure ici.
4. **Les frameworks et les principes.** Un framework nommé, une réécriture, une structure, un type d'offre, des règles : `frameworks-copywriting`.
5. **L'infrastructure.** Domaines, DNS, boîtes, chauffe, liste noire, montée en charge : `infra-email`. La conformité et les principes de placement : `delivrabilite.md` par le master.
6. **Une demande qui croise deux sous-skills** ("écris une séquence pour des DAF") : persona (`message-atl`), puis `premier-contact` pour l'email 1, puis `relance` pour les emails 2 et 3, dans un seul livrable. Une demande qui croise un autre master ("écris aux boîtes qui recrutent") commence par le master detecter-signaux, dont le CSV arrive ici.

## Ce que le master fait lui-même

- **Le brief de campagne** (`{SKILL_BASE}/ressources/brief-strategie.md`) : avant tout email, cible, persona, registre, niveau de connaissance, angle en une phrase, signal, preuve, CTA, expéditeur, historique de réponses, profondeur de personnalisation, points à valider, désaccords. Montré à l'utilisateur, puis on continue ; on s'arrête seulement si un désaccord change l'angle.
- **La délivrabilité et la conformité** (`{SKILL_BASE}/ressources/delivrabilite.md`) : authentification, chauffe, texte brut, heures d'envoi, RGPD et opt-out en France, rebonds, listes noires, checklist de lancement. Le montage technique va à `infra-email`.
- **Les métriques et le diagnostic** (`{SKILL_BASE}/ressources/metriques-benchmarks.md`) : ce qu'on mesure, les leviers, les seuils, le diagnostic rapide, les règles de test.
- **Les réponses** (`{SKILL_BASE}/ressources/reponses.md`) : intéressé, doc demandée, pas maintenant, pas le bon contact, objection, pas intéressé, leads entrants. Le no-show renvoie au sous-skill `no-show` de `cold-call`.
- **Les messages LinkedIn** (`{SKILL_BASE}/ressources/linkedin-messages.md`) : invitation, premier message, relances, limites et chauffe du compte, coordination avec l'email.
- **Les séquences prêtes** (`{SKILL_BASE}/ressources/sequences.md`) : structures 2 et 3 emails (3 au plus : J0, J+3, J+10), la séquence 2 emails "lead magnet", timing et saisonnalité ; la variante 4 emails et la séquence 7 touches "le plafond de la recommandation" sortent de la règle et se réservent à une liste qui a déjà répondu une fois. La séquence multicanal de référence (LinkedIn J0, email J+2, email J+5, LinkedIn J+7, téléphone J+9 à J+12) est dans `10_Skills/cold-call/ressources/sequence-multicanal.md`.
- **La relecture** (`{SKILL_BASE}/ressources/relecteurs.md`) : les quatre relecteurs (prospect, recherche, qualité, voix) puis le contrôle final, appliqués à tout email avant de le rendre, avec la checklist §H d'`anti-ai-voice.md`.
- **Les règles transverses** : 50 à 90 mots ; texte brut ; un CTA ; fait avant adjectif ; vouvoiement ; aucun tiret cadratin ; seuls les emails `DELIVERABLE` ou `HIGH_PROBABILITY` partent (`CATCH_ALL` et `UNKNOWN` à 20 % de la liste au plus) ; 3 relances au plus après un silence, tous canaux confondus ; la rotation des angles entre emails ; le signal avant le froid ; trois exemples validés avant `envoyer_sequence`.

## Repères chiffrés

| Repère | Valeur |
|---|---|
| Longueur d'un email | 50 à 90 mots, 3 à 6 lignes ; ATL 2 à 3 phrases, BTL 3 à 4 |
| Part des réponses sur l'email 1 | 80 % |
| Taux de réponse | à froid sans signal 2 à 5 %, avec signal 10 à 20 % ; les 6 à 8 % / 18 à 22 % / 35 à 40 % des sources anglophones sont des repères étrangers, comptez un tiers de moins en France |
| Objectifs d'une campagne saine | réponse positive 5 à 8 %, rendez-vous 2 à 4 % |
| Écart entre variantes d'un même email | jusqu'à un facteur 13 : tester 3 ou 4 variantes, 100 envois chacune |
| Séquence email seule | 3 emails au plus : J0, J+3 même fil, J+10 nouvel objet ; puis 3 mois de pause |
| Réutilisation de la liste | tous les 3 mois |
| Volume | 30 emails par boîte et par jour au plus, 2 boîtes par domaine, 2 à 3 domaines pour un dirigeant seul |
| Chauffe | 3 semaines avant le premier envoi, jamais coupée |
| Rebond, plainte | rebond : alerte à 3 % (on vérifie la liste), arrêt de la campagne à 5 % ; plainte sous 0,1 % |
| Réponse et réputation | au-dessus de 5 % la délivrabilité tient ; sous 3 % elle se dégrade |
| Meilleurs signaux | prise de poste entre 14 et 45 jours (8 à 12 %), question orientée non en réengagement (10 à 15 %) |

Les repères de réponse anglophones sont cités comme repères étrangers ; les limites (volume, chauffe, rebond) sont celles de `05_Departements/Go-to-Market/GARDE-FOUS.md`. Remplacez les taux par ceux de l'utilisateur dès 500 envois.

## Avant de répondre

1. Lisez `05_Departements/Go-to-Market/contexte.md` à la racine : offre, preuves autorisées (l'ensemble fermé de ce qu'on peut affirmer), ICP, personas ATL et BTL, signaux prioritaires, canaux, voix de l'expéditeur. Si `05_Departements/Go-to-Market/contexte.md` contient encore des crochets, proposez `installer-gtm` et n'écrivez rien.
2. Lisez `05_Departements/Go-to-Market/OUTILS.md` si la demande implique une collecte ou un envoi : priorité apify ou api, `canal_linkedin` (Unipile ou Lemlist), CRM.
3. Lisez `05_Departements/Go-to-Market/GARDE-FOUS.md` avant tout envoi : limites, exclusions, ce qu'on n'envoie jamais.
4. Lisez `01_About-Me/anti-ai-voice.md` (racine du workspace) : chaque template et chaque email passent sa checklist §H avant d'être rendus.
5. Lisez `02_Contexte/Tone-and-Voice.md` : il cale la voix de l'expéditeur avec la section voix de `05_Departements/Go-to-Market/contexte.md`.
6. Identifiez le persona, la position dans la séquence, la demande précise, dans cet ordre, puis lisez le sous-skill. Écrivez le brief. Écrivez. Relisez. Montrez trois emails remplis sur trois prospects réels. Attendez le oui. Puis seulement `envoyer_sequence`.

## Exemples

- "Écris-moi une séquence pour des DAF d'ETI qui recrutent" : persona ATL (`message-atl`), brief en 8 lignes, email 1 par `premier-contact` (Faites le calcul sur le signal de recrutement), emails 2 et 3 par `relance`, trois exemples remplis, attente du oui avant `envoyer_sequence`.
- "Il m'a répondu qu'il avait déjà un prestataire" : `reponses.md`, réponse objection en trois lignes, un fait qui lève l'objection s'il existe dans `05_Departements/Go-to-Market/contexte.md`, sinon clôture polie et date de reprise.
- "Mes emails partent en spam" : `infra-email`, cadre d'enquête, audit Lemlist, table de dépannage, protocole de récupération.
- "Quel objet je mets ?" : `objets`, quatre options de familles différentes, test A/B recommandé, objet de l'email 3.
- "Comment je personnalise 300 lignes sans que ça sonne robot ?" : `personnalisation`, matrice de décision, ouverture de deux phrases plus corps fixe, taux de repli attendu, aperçus par type avant l'envoi.
