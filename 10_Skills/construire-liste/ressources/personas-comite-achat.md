# Personas et comité d'achat

Lu par `cartographier-personas` et `sourcer-personnes`. Ce sont des personnes qui achètent, jamais une entreprise en bloc. Ce fichier donne les rôles d'un comité d'achat, les personas types selon la taille de l'entreprise, la distinction ATL et BTL, les questions pour cartographier, et le format attendu dans `05_Departements/Go-to-Market/contexte.md`.

## ATL et BTL

| | ATL (au-dessus de la ligne) | BTL (sous la ligne) |
|---|---|---|
| Qui | C-level, VP, directeur, dirigeant de PME | manager, responsable, chargé de, opérationnel |
| Ce qu'il fait dans l'achat | décide, signe, débloque le budget | vit le problème, teste, pousse en interne |
| Ce qu'il lit | résultat business, chiffre, risque, comparaison avec ses pairs | gain de temps, quotidien, outil, exemple concret |
| Angle de message | "vos concurrents font X, voici ce que ça change sur votre pipe" | "voici comment gagner 4 heures par semaine sur cette tâche" |
| Longueur de message | court, une idée, une question | peut être plus long, démonstratif |
| Canal | LinkedIn et téléphone, email court | email, LinkedIn |

Dans une entreprise de moins de 20 personnes, le dirigeant est ATL et BTL à la fois : il décide et il fait. Le message lui parle des deux.

## Les rôles du comité d'achat

Un achat B2B au-dessus de quelques milliers d'euros implique en moyenne 6 à 10 personnes. Cinq rôles reviennent toujours :

| Rôle | Ce qu'il fait | Titres fréquents | Priorité de contact |
|---|---|---|---|
| Champion | porte le sujet en interne, organise l'évaluation | responsable de la fonction concernée, directeur opérationnel | premier, 40 à 50 % de l'effort |
| Décideur économique | signe, cherche le retour sur investissement | CEO, DG, DAF, VP | second, une fois le champion chaud |
| Utilisateur final | utilisera l'offre chaque jour | chargé de, chef de projet, commercial | contenu produit, témoignage |
| Évaluateur technique | vérifie l'intégration, la sécurité, la conformité | DSI, responsable IT, RSSI, DPO | au moment de la démonstration |
| Bloqueur | peut dire non, initie rarement | juridique, achats, finance | traiter ses objections avant qu'il les pose |

Un coach ou un consultant qui vend à un dirigeant de PME a souvent un comité de une à deux personnes : le dirigeant, parfois son associé ou son directeur commercial. Ne cherchez pas cinq rôles là où il n'y en a qu'un.

## Personas types par taille d'entreprise

| Effectif | Qui décide | Qui vit le problème | Combien de contacts par compte |
|---|---|---|---|
| 1 à 10 | le dirigeant | le dirigeant | 1 |
| 11 à 50 | le dirigeant, parfois un associé | un responsable de fonction (commercial, marketing, RH, ops) | 2 |
| 51 à 250 | le directeur de fonction, validation du DG | un ou deux managers | 2 à 3 |
| 251 à 1 000 | le VP ou directeur, budget arbitré par la DAF | des managers et des chefs de projet | 3 à 4 |
| Plus de 1 000 | un comité formel avec les achats | des équipes entières | 4 à 5, par entité ou pays |

## Attributs à documenter pour chaque persona

| Attribut | Question à se poser | Exemple |
|---|---|---|
| Titres | quels intitulés apparaissent sur LinkedIn, en français et en anglais | Directeur commercial, Directrice commerciale, Head of Sales, CRO |
| Séniorité | C-level, VP, directeur, manager, opérationnel | directeur |
| Fonction | quel département | commercial |
| Ce qu'il doit accomplir | son objectif de l'année | signer 20 clients de plus sans recruter |
| Douleur | ce qui le bloque aujourd'hui | pipe irrégulier, dépend de deux gros clients |
| Indicateur de succès | comment on le juge | nombre de rendez-vous qualifiés par mois |
| Rôle dans l'achat | champion, décideur, utilisateur, évaluateur, bloqueur | décideur |
| Angle de message | la promesse qui lui parle | "trois rendez-vous par semaine sans agence" |
| Ce qu'il ne veut pas entendre | ses allergies | "100 % automatisé", "sans effort" |

## Questions pour cartographier à partir des clients signés

1. Sur les dix derniers clients, qui a répondu au premier message ? Son titre exact.
2. Qui a signé ? Est-ce la même personne ?
3. Qui d'autre était dans la boucle (appel, email en copie, démonstration) ?
4. Qui a failli bloquer, et pour quelle raison ?
5. Sur les affaires perdues, à quel niveau l'échange s'est arrêté ?

Les réponses donnent le champion et le décideur réels, souvent différents de ceux qu'on imaginait. Si le CRM est branché, la liste des contacts associés aux affaires gagnées répond aux questions 1 à 3.

## Titres par fonction, pour les booléens

| Fonction | Titres ATL | Titres BTL |
|---|---|---|
| Direction | CEO, PDG, DG, Directeur général, Gérant, Président, Fondateur, Co-fondateur, Managing Director | Directeur de cabinet, Chief of Staff |
| Commercial | Directeur commercial, Directrice commerciale, Head of Sales, CRO, VP Sales | Responsable commercial, Business Developer, Account Executive, Sales Manager |
| Marketing | CMO, Directeur marketing, Head of Marketing, VP Marketing | Responsable marketing, Growth Manager, Chef de projet marketing |
| RH | DRH, Directeur des ressources humaines, CHRO, Head of People, VP People | Responsable RH, Talent Acquisition Manager, Chargé de recrutement |
| Finance | DAF, CFO, Directeur financier | Contrôleur de gestion, Responsable comptable |
| Technique | CTO, DSI, VP Engineering, Head of Engineering | Lead Developer, Responsable IT |
| Opérations | COO, Directeur des opérations | Responsable des opérations, Office Manager |

Exclusions à mettre dans tout booléen : assistant, stagiaire, alternant, étudiant, intern, "à la recherche", "en recherche", "open to work".

## Format de la section 3 de contexte.md, tel que `installer-gtm` la remplit

La section 3 tient en deux fiches et une table. La fiche ATL et la fiche BTL portent chacune une liste de titres (plusieurs fonctions possibles), ce qui préoccupe la personne, ce qu'elle mesure, l'angle d'approche et le canal. La table du comité d'achat dit qui joue chaque rôle chez les clients de l'utilisateur, ce qu'il attend, et son poids dans la décision.

```
### ATL : le décideur
- Titres à chercher : CEO, PDG, DG, Gérant, Fondateur, Co-fondateur, Président
- Ce qui l'empêche de dormir : un pipe irrégulier, deux ou trois gros clients qui pèsent trop
- Ce qu'il mesure : rendez-vous qualifiés par mois, chiffre signé
- Angle d'approche : des rendez-vous réguliers avec un système qu'il opère lui-même ; jamais "100 % automatisé"
- Canal qui marche le mieux : téléphone puis email

### BTL : celui qui vit le problème
- Titres à chercher : Directeur commercial, Directrice commerciale, Head of Sales, Responsable commercial
- Ce qu'il vit au quotidien : les commerciaux gèrent l'existant et ne prospectent plus
- Ce qu'il mesure : rendez-vous par commercial par semaine
- Angle d'approche : lui donner une méthode et de quoi convaincre le DG
- Canal qui marche le mieux : LinkedIn puis email

### Comité d'achat chez vos clients
| Rôle | Qui c'est (titre) | Ce qu'il attend de vous | Poids dans la décision |
| Champion | Directeur commercial | une méthode que son équipe applique | 40 % |
| Décideur économique | DG | des rendez-vous, un retour sur le prix en trois mois | 50 % |
| Utilisateur | Business developer | un quotidien plus simple | 10 % |
| Évaluateur | (aucun dans une PME) | | |
| Bloqueur possible | Associé | pas de dépense sans preuve | à surveiller |
```

Le reste des attributs de ce fichier (objectif de l'année, rôle dans l'achat par titre, ce qu'il ne veut pas entendre) sert à remplir ces lignes, sans champ dédié : il se fond dans "ce qui l'empêche de dormir" et "angle d'approche". Chaque fiche donne une recherche distincte dans `sourcer-personnes` et un CSV distinct ; quand la fiche ATL liste des titres de fonctions différentes (DG et DRH), une recherche par fonction.
