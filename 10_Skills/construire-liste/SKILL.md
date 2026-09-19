---
name: construire-liste
description: >
  Construit une liste de prospection B2B de bout en bout : définir l'ICP, cartographier
  les personas, sourcer des entreprises et des personnes, sélectionner des comptes,
  qualifier, nettoyer et vérifier, dédoublonner. Se déclenche sur : "fais-moi une liste
  de", "trouve des entreprises", "trouve des décisionnaires", "qui viser chez", "ICP",
  "client idéal", "personas", "comité d'achat", "lookalikes", "comptes cibles", "qualifie
  cette liste", "score ces prospects", "enlève les B2C", "enlève les concurrents",
  "nettoie ma liste", "vérifie les emails", "taux de bounce", "dédoublonne", "qui est déjà
  dans le CRM". Ne pas utiliser pour : détecter un signal d'achat (levée, recrutement,
  changement de poste, engagement), voir `detecter-signaux` ; écrire un message ou une
  séquence, voir `cold-email` ; préparer un appel, voir `cold-call` ; remplir contexte.md
  la première fois, voir `installer-gtm`.
---

## Repérage

Résolvez `SKILL_BASE` une fois par session : Glob sur `**/construire-liste/SKILL.md`, le dossier qui contient ce fichier est `SKILL_BASE`. Les sous-skills sont dans `{SKILL_BASE}/sous-skills/`, un dossier par sous-skill avec son `SKILL.md`. Les ressources sont dans `{SKILL_BASE}/ressources/`. Ne supposez jamais un chemin en dur.

## Rôle

Vous êtes le responsable des données de prospection : vous construisez la liste que `detecter-signaux`, `cold-email` et `cold-call` consomment ensuite. Vous routez la demande vers l'un des huit sous-skills, ou vous enchaînez la chaîne complète quand l'utilisateur dit "fais-moi une liste".

## Table de routage

| Demande | Sous-skill | Phrases déclencheuses | Fichier à lire |
|---|---|---|---|
| Définir qui viser, critères, scoring, volume du marché | `definir-icp` | "ICP", "client idéal", "qui viser", "critères", "combien d'entreprises", "ma cible est trop large" | `{SKILL_BASE}/sous-skills/definir-icp/SKILL.md` |
| Qui contacter dans l'entreprise, comité d'achat, angle par rôle | `cartographier-personas` | "personas", "quel poste", "qui décide", "comité d'achat", "ATL", "BTL", "décideur ou opérationnel" | `{SKILL_BASE}/sous-skills/cartographier-personas/SKILL.md` |
| Trouver des entreprises | `sourcer-entreprises` | "trouve des entreprises", "des boîtes qui", "des agences", "des cabinets", "commerces à Lyon", "où trouver" | `{SKILL_BASE}/sous-skills/sourcer-entreprises/SKILL.md` |
| Trouver des personnes, titres, booléens | `sourcer-personnes` | "trouve les DRH de", "les CEO de ces boîtes", "décisionnaires", "booléen", "Sales Nav", "employés de" | `{SKILL_BASE}/sous-skills/sourcer-personnes/SKILL.md` |
| Choisir des comptes à la main, lookalikes, ABM | `selectionner-comptes` | "comme mes clients", "lookalikes", "comptes cibles", "ABM", "combien de comptes", "mes meilleurs clients" | `{SKILL_BASE}/sous-skills/selectionner-comptes/SKILL.md` |
| Scorer, trier, exclure sur un fichier existant | `qualifier-comptes` | "qualifie", "score", "trie", "tier", "enlève les B2C", "enlève les concurrents", "qui est prioritaire" | `{SKILL_BASE}/sous-skills/qualifier-comptes/SKILL.md` |
| Vérifier les emails, normaliser, hygiène | `nettoyer-verifier` | "vérifie les emails", "bounce", "catch-all", "nettoie", "normalise", "emojis dans les prénoms", "SARL dans les noms" | `{SKILL_BASE}/sous-skills/nettoyer-verifier/SKILL.md` |
| Doublons, fusion de sources, croisement CRM | `dedoublonner-liste` | "dédoublonne", "doublons", "fusionne ces fichiers", "déjà dans HubSpot", "déjà contacté", "déjà client" | `{SKILL_BASE}/sous-skills/dedoublonner-liste/SKILL.md` |

## Logique de routage

1. Si la section 2 de `05_Departements/Go-to-Market/contexte.md` contient encore des crochets, rien ne se lance : proposez `installer-gtm`. Exception : l'utilisateur veut travailler son ICP maintenant, ouvrez `definir-icp`.
2. L'utilisateur donne un fichier (un chemin, "ma liste", "cet export") : la demande porte sur ce fichier. "Qualifie", "score", "trie", "enlève" : `qualifier-comptes`. "Vérifie", "bounce", "emails", "normalise" : `nettoyer-verifier`. "Doublons", "CRM", "déjà contacté", "fusionne" : `dedoublonner-liste`. "Nettoie" sans précision : une question, doublons, emails ou hors cible ?
3. Pas de fichier, il veut trouver : des entreprises (secteur, type de boîte, ville) vers `sourcer-entreprises` ; des personnes (titres, "décisionnaires", "DRH de") vers `sourcer-personnes` ; "comme mes clients", "lookalikes", "comptes cibles" vers `selectionner-comptes`.
4. Une question de stratégie sans fichier ni recherche : "qui viser", "critères", "trop large" vers `definir-icp` ; "qui chez", "quel poste", "comité d'achat" vers `cartographier-personas`.
5. "Fais-moi une liste de X" : c'est la chaîne complète, décrite ci-dessous.
6. La demande part d'un signal ("qui recrute", "qui a levé", "qui a liké") : `detecter-signaux` d'abord, puis `qualifier-comptes` sur le CSV produit.
7. Une demande qui croise deux sous-skills ("les DRH des boîtes qui ressemblent à mes clients") s'exécute dans l'ordre entreprises puis personnes : `selectionner-comptes`, puis `sourcer-personnes`. Le premier sous-skill écrit son CSV, le second le lit.
8. S'il manque une information pour router, une seule question, jamais deux.

## Ce que le master fait lui-même

La chaîne "fais-moi une liste de X". Lisez `{SKILL_BASE}/ressources/conseils-list-building.md` et `{SKILL_BASE}/ressources/gates-qualification.md`, puis :

1. Relisez l'ICP et les personas de `05_Departements/Go-to-Market/contexte.md`. Les contraintes ajoutées dans la demande (une ville, un secteur, un effectif) s'appliquent par-dessus, sans modifier `05_Departements/Go-to-Market/contexte.md`.
2. Annoncez le plan en cinq lignes : sources choisies (`{SKILL_BASE}/ressources/sources-par-besoin.md`), volume attendu, coût estimé par étape payante, nom du fichier final, canal visé. Attendez le oui.
3. Enchaînez : `sourcer-entreprises`, puis `qualifier-comptes` (les portes d'exclusion et le score ICP sur les entreprises), puis `sourcer-personnes` sur les tiers A et B seulement, puis `nettoyer-verifier`, puis `dedoublonner-liste` (dans la liste, puis contre le CRM).
4. Rendez le rapport en entonnoir (une ligne par porte avec le nombre de lignes retirées), le lien vers le CSV final, et un seul next step : `cold-email` si les emails sont vérifiés, `detecter-signaux` si l'utilisateur veut prioriser par timing.

Trois chaînes selon le point de départ :

```
Liste large (l'utilisateur part de zéro)
  definir-icp (vérification) -> sourcer-entreprises -> qualifier-comptes
  -> sourcer-personnes (tiers A et B) -> nettoyer-verifier -> dedoublonner-liste

Comptes choisis (ABM, 20 à 200 comptes)
  selectionner-comptes -> cartographier-personas -> sourcer-personnes (par page entreprise)
  -> nettoyer-verifier -> dedoublonner-liste

Fichier existant (export, achat, ancienne liste)
  dedoublonner-liste -> qualifier-comptes -> nettoyer-verifier
  -> sourcer-personnes seulement pour les comptes tier A sans contact
```

Chaque étape écrit son CSV dans `05_Departements/Go-to-Market/Listes-prospection/`, nommé `<verbe>_<sujet>_<AAAA-MM-JJ>.csv`, avec les colonnes de `CONVENTIONS.md` section 8 dans l'ordre. Une étape ne remplit jamais une colonne déjà remplie : elle ne relance un outil que si la cellule est vide. Le fichier final de la chaîne porte le sujet demandé par l'utilisateur, par exemple `dedoublonner_agences-immo-lyon_2026-09-19.csv`.

Trois règles d'ordre que vous appliquez à chaque chaîne : qualifier les entreprises avant de chercher les personnes (on ne paie pas des contacts chez des comptes exclus), dédoublonner avant d'enrichir (on ne paie pas deux fois la même ligne), vérifier avant de remettre à `cold-email` (on n'envoie pas sur une adresse non vérifiée).

Vous répondez aussi directement à "combien de lignes il me faut" : partez des nouveaux prospects entrés en séquence par semaine (section 5 de `05_Departements/Go-to-Market/contexte.md`), multipliez par 4 semaines, ajoutez 30 % pour les exclusions et les emails introuvables.

## Repères chiffrés

| Repère | Valeur |
|---|---|
| Résultats maximum d'une recherche Sales Navigator | 2 500, au-delà on segmente |
| Couverture du marché avec une seule source | environ 60 %, deux sources environ 85 % |
| Recouvrement entre deux sources sur la même cible | 30 à 60 % de doublons |
| Décroissance annuelle des emails | 22 à 30 %, soit environ 2 % par mois |
| Décroissance annuelle des intitulés de poste | 30 à 35 % |
| Taux de bounce visé | sous 1 % ; au-dessus de 3 %, on arrête d'envoyer |
| Âge maximum d'une liste avant re-vérification | 30 jours |
| Contacts par compte | 2 à 4 sur un compte tier A, 1 à 2 sur un tier B, plafond 5 |
| Couverture email minimum avant de lancer une séquence | 70 % des lignes |
| Taille d'un segment pour rester personnalisable | sous 1 000 lignes |

Les seuils de tiers (A, B, C, D) et les pondérations du score ICP ne sont pas ici : ils sont dans `05_Departements/Go-to-Market/contexte.md`.

## Avant de répondre

Lisez `05_Departements/Go-to-Market/contexte.md` : la section 2 (trois couches, points, seuils de tiers, exclusions), la section 3 (personas ATL et BTL, comité d'achat), la section 4 (cinq signaux prioritaires), la section 5 (canaux et volumes), la section 7 (garde-fous propres à l'utilisateur). Lisez `05_Departements/Go-to-Market/OUTILS.md` dès que la demande implique un appel (`priorite`, `crm`, outil de chaque verbe). Si un outil nécessaire n'est pas branché, dites lequel et renvoyez vers `connecter-outils`, sans rien simuler.

Avant tout appel payant : annoncez le nombre de lignes et le coût, lancez d'abord sur 10 à 50 lignes, montrez le résultat, puis seulement le reste. Avant tout import dans le CRM : montrez l'échantillon et attendez le oui.
