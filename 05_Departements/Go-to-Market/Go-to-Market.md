---
type: departement
status: active
objectif: [à remplir : par exemple rendez-vous qualifiés par semaine]
date: AAAA-MM-JJ
maj: AAAA-MM-JJ
---

# Go-to-Market

## Mission

Tout ce qui amène un prospect jusqu'à une conversation : listes de prospects, scraping et enrichissement, séquences email et LinkedIn, icebreakers, playbooks d'appel, emails à votre audience, publicités. Les canaux fonctionnent ensemble, pas en silos.

Ne va pas ici : la propale et le pipeline ([[Vente]]), un post organique ([[Marketing]]), un event daté (un projet dans `04_Projets/`).

## Périmètre

- Alimenter le pipeline en rendez-vous qualifiés chaque semaine
- Tenir les listes propres : dédoublonnées, enrichies, qualifiées
- Écrire des messages dans votre voix, personnalisés, jamais envoyés sans votre oui

## Objectif

[à remplir : par exemple rendez-vous qualifiés par semaine]. [Le chiffre, actuel vs cible, et le fichier qui fait foi.]

## Cadre

Les réglages du module GTM vivent ici : `contexte.md` (ICP scoré, personas, 5 signaux prioritaires, canaux, volumes, garde-fous propres ; rempli par "Installe ma prospection"), `OUTILS.md` (quel outil fait quel verbe, rempli par "Connecte mes outils"), `GARDE-FOUS.md` (limites d'envoi, personnalisation, RGPD), `Ciblage/` (le niveau opérationnel de l'ICP : décisionnaires par taille d'entreprise, requêtes booléennes, mots-clés d'exclusion). La vérité sur l'offre, la cible et la voix reste dans `02_Contexte/` : `contexte.md` la traduit en critères de prospection, il ne la recopie pas. Mode d'emploi complet : `docs/prospection.md`.

Quatre masters de méthode : `construire-liste` (ICP, personas, sourcing, qualification, dédoublonnage), `detecter-signaux` (changement de poste, levée, recrutement, événement, techno, concurrents, engagement, score), `cold-email` (premier contact, relances, objets, personnalisation, infra), `cold-call` (script, objections, no-show, brief, débrief). Chaque master route vers ses sous-skills, qui décrivent le travail en verbes ; les skills d'exécution (`trouver-*`, `enrichir-*`, `scraper-*`, `qualifier-liste`, `dedoublonner`, `crm`, `envoyer-sequence`, `verifier-reponses`) lisent `OUTILS.md` et appellent l'outil branché, avec `--dry-run` et coût annoncé avant tout run.

Règle absolue : rien ne part vers l'extérieur sans un oui explicite sur un échantillon de 3 messages. Un CSV par étape, colonnes normalisées, "ne relance que si vide".

- `Listes-prospection/` : les listes, enrichissements et qualifications, nommés `<verbe>_<sujet>_<date>.csv`
- `Signaux/` : les runs de détection et `comptes-suivis.csv`
- `Messages/` : séquences, messages personnalisés, scripts d'appel
- `Mailing/` : emails à l'audience déjà inscrite
- `Ciblage/` : décisionnaires par taille, requêtes booléennes, listes de mots-clés
- `sources/` : exports bruts reçus, immuables

## Où on en est

[Réécrit par /done, cinq lignes max : où on en est, la prochaine action, la dernière session.]

## Key Notes

- [[Vente]]
- [[Marketing]]
