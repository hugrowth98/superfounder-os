---
name: qualifier-liste
description: >
  Skill pour trier et scorer un CSV de prospects ou d'entreprises selon l'ICP defini dans
  contexte.md. Ne fait aucun appel API : c'est du raisonnement pur (lecture du CSV +
  lecture de contexte.md + jugement). Utilise ce skill des que l'utilisateur veut qualifier,
  trier, scorer ou filtrer une liste selon son client ideal. Se declenche sur : "qualifie
  cette liste", "trie ces prospects", "garde ceux qui matchent mon ICP", "score ces leads",
  "qui est pertinent dans cette liste".
---

# Qualifier une liste selon l'ICP

## Ce que fait ce skill

1. Lit `contexte.md` a la racine du projet (section 2 "Votre client ideal (ICP)" et section 8
   "Garde-fous") pour connaitre les criteres de ciblage.
2. Lit le CSV fourni par l'utilisateur, ligne par ligne, sans en sauter aucune.
3. Pour chaque ligne, juge si le prospect/l'entreprise matche l'ICP : secteur, taille, poste,
   zone geographique, signaux positifs mentionnes dans contexte.md.
4. Exclut automatiquement tout ce qui correspond aux garde-fous (comptes/entreprises a ne
   jamais contacter, zones exclues).
5. Ecrit deux fichiers CSV en sortie : un fichier "garde" (avec une colonne `score` de 1 a 10
   et une colonne `raison`) et un fichier "exclus" (avec la raison de l'exclusion).

## Ne pas faire

- Ne jamais inventer des criteres qui ne sont pas dans `contexte.md`. Si `contexte.md` n'est
  pas rempli ou trop vague sur un point, demander a l'utilisateur avant de juger.
- Ne pas appeler d'API externe : ce skill est purement du jugement sur des donnees deja
  presentes dans le CSV. Si des donnees manquent pour juger (ex: taille d'entreprise absente
  du CSV), le signaler plutot que de deviner.

## Colonnes de sortie

Le CSV d'entree est conserve tel quel (toutes ses colonnes originales), avec deux colonnes
ajoutees en tete :
- `score` : entier de 1 (hors cible) a 10 (correspond parfaitement a l'ICP)
- `raison` : une phrase courte expliquant le score ou l'exclusion

## Workflow

### Etape 1 - Charger le contexte

Relire `contexte.md`. Si les sections 2 et 8 sont encore au format template (crochets non
remplis), le signaler a l'utilisateur et demander de preciser l'ICP avant de continuer.

### Etape 2 - Lire le CSV

Demander le chemin du fichier si non fourni. Lire l'integralite des lignes.

### Etape 3 - Juger chaque ligne

Pour chaque prospect/entreprise, verifier dans l'ordre :
1. Garde-fou d'exclusion (section 8) : si ca matche, exclusion immediate, raison = le
   garde-fou concerne.
2. Correspondance ICP (section 2) : secteur, taille, poste/fonction, zone geographique.
3. Signaux positifs mentionnes dans contexte.md (ex: recrute un poste precis, vient de lever
   des fonds) : bonus sur le score si presents dans les donnees du CSV.

### Etape 4 - Ecrire les deux CSV de sortie

Nommage : `<nom-original>_qualifie.csv` (gardes, tries par score decroissant) et
`<nom-original>_exclus.csv` (exclus, avec raison). Les deux dans le meme dossier que le
fichier d'entree, sauf si l'utilisateur precise un autre emplacement.

### Etape 5 - Resumer

Donner un resume court : nombre de lignes lues, nombre gardees par tranche de score
(8-10 / 5-7 / 1-4), nombre exclues avec le top 2-3 raisons d'exclusion les plus frequentes.
Proposer l'etape suivante : "Je peux enrichir les emails de la liste gardee avec
trouver-email, ou rediger les messages avec personnaliser-message."
