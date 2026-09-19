# Conseils de construction de liste

Lu par le master avant une chaîne complète. Une liste sert à contacter les bonnes personnes avec la bonne donnée. Une liste brute convertit à 1 ou 2 % ; la même liste enrichie, scorée et segmentée convertit à 5 ou 15 %. Tout ce fichier découle de cet écart.

## Les principes

1. Mélangez les sources. Une seule source couvre 60 % du marché, deux en couvrent 85 %. Chaque source a ses trous, ils ne sont pas aux mêmes endroits.
2. Le scraping est l'étape 1, jamais la dernière. Une ligne extraite n'a ni email vérifié, ni effectif fiable, ni score. Elle passe par les portes, l'enrichissement et la vérification avant d'exister.
3. Partez d'un modèle et ajustez. Les trois chaînes du master (liste large, comptes choisis, fichier existant) couvrent presque tous les cas. On adapte une chaîne au besoin.
4. Testez petit. Dix lignes pour vérifier les colonnes, cinquante pour mesurer le taux de trouvés, puis le reste. Un run de 2 000 lignes lancé sur une mauvaise colonne coûte le prix de 2 000 lignes.
5. Ordre des opérations : entreprises avant personnes, portes avant enrichissement, dédoublonnage avant tout ce qui coûte, vérification avant tout envoi.
6. Une donnée manquante reste vide. Aucun email deviné, aucun effectif estimé, aucun titre supposé. Une colonne vide se remplit avec un outil ou reste vide.
7. Une liste vit. Les emails meurent à 2 % par mois, les titres à 3 % par mois. On relance `trouver_email --force` sur ce qui a plus de 30 jours, on ré-enrichit ce qui a plus de 90 jours, on relit l'ICP chaque trimestre avec ce qui a signé.

## Ce qui fait une bonne liste

Par ordre de valeur, ce qu'une ligne doit avoir :

1. Un email vérifié (`email_statut` en `DELIVERABLE` ou `HIGH_PROBABILITY`) ou un `linkedin_url` joignable.
2. Un téléphone direct quand le canal téléphone est prévu.
3. Un signal daté de moins de 30 jours.
4. Un `score_icp` et un `tier`.
5. Une entreprise complète : `domaine`, `secteur`, `effectif`, `ville`.

Une ligne avec 1 et 4 est prête pour une séquence. Une ligne avec 1, 3 et 4 est prête pour un message personnalisé. Une ligne sans 1 ni `linkedin_url` reste un nom, injoignable.

## Erreurs qui coûtent le plus

| Erreur | Ce que ça produit | Ce qu'on fait à la place |
|---|---|---|
| Une seule source | 40 % du marché absent | deux sources, fusion, dédoublonnage |
| Pas d'ICP écrit avant de chercher | une liste que personne n'ose contacter | `definir-icp` d'abord, une ligne dans `05_Departements/Go-to-Market/contexte.md` avant une ligne dans un CSV |
| Personnes avant entreprises | des contacts payés chez des comptes exclus | `qualifier-comptes` sur les entreprises, puis `sourcer-personnes` sur les tiers A et B |
| Pas de vérification | bounces, domaine grillé | un `email_statut` envoyable sur chaque adresse qui part ; une adresse importée sans statut repasse par `trouver_email --force` ou ne part pas |
| Pas de dédoublonnage | deux séquences à la même personne | `dedoublonner-liste` avant enrichissement et avant envoi |
| Toutes les lignes traitées pareil | l'effort de personnalisation dilué sur des tiers C | l'effort suit le tier, la séquence standard suit le reste |
| Filtrer trop | un marché de 80 entreprises | `definir-icp`, test de volume, élargir la couche adjacente |
| Filtrer trop peu | 12 000 lignes, aucune contactée | resserrer l'effectif et le secteur, ou découper en segments de moins de 1 000 |
| Ignorer l'anti-ICP | des clients qui churnent en deux mois | les disqualifiants dans `05_Departements/Go-to-Market/contexte.md` |
| ICP figé | une cible qui ne signe plus | relire les dix derniers signés chaque trimestre |

## Avant de remettre une liste à cold-email ou cold-call

- [ ] chaque adresse qui part a un `email_statut` envoyable (`DELIVERABLE`, `HIGH_PROBABILITY` ; `CATCH_ALL` et `UNKNOWN` à 20 % au plus), les adresses sans statut sont comptées et ne partent pas, bounce attendu sous 1 %
- [ ] au moins 70 % des lignes ont un email `DELIVERABLE` ou `HIGH_PROBABILITY`, ou un `linkedin_url`
- [ ] chaque ligne a `score_icp`, `tier`, et `exclu = non`
- [ ] les signaux présents ont `signal_date` de moins de 30 jours
- [ ] les doublons sont retirés, dans la liste et contre le CRM
- [ ] les concurrents et les clients sont marqués `exclu = oui`
- [ ] les fichiers de référence (`ne_plus_contacter`, dernières listes envoyées) ont été passés en `--contre` à `dedoublonner`
- [ ] le fichier est nommé `<verbe>_<sujet>_<date>.csv`, colonnes de `docs/conventions-gtm.md` section 8, dans `05_Departements/Go-to-Market/Listes-prospection/`
- [ ] le segment fait moins de 1 000 lignes, ou il est découpé par persona, secteur ou tier

## Segmenter pour personnaliser

Une liste se découpe avant d'écrire. Un segment par persona (le message change), par secteur (l'exemple change), par tier (l'effort change), par signal (l'accroche change). Un segment de moins de 1 000 lignes se personnalise ; au-delà, on écrit pour la moyenne et la moyenne ne répond pas.

## Combien de temps ça prend

Construire 100 prospects propres à la main prend 8 à 10 heures. Avec la chaîne, la même liste prend environ 30 minutes de supervision, dont la plus grande part est la relecture des échantillons. Le temps gagné va dans la personnalisation des tiers A.
