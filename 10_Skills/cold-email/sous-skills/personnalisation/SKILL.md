---
name: personnalisation
description: >
  Construit la personnalisation d'une campagne : quelle donnée utiliser (6 seaux), hook fort ou hook léger, ouverture de deux phrases par personne ou par segment, prompts qui produisent les variables. Se déclenche sur : "personnalise", "personnalisation", "première ligne", "icebreaker", "accroche", "ouverture personnalisée", "à l'échelle", "prompts de personnalisation", "hook", "comment je recherche mes prospects", "ligne d'ouverture". Ne pas utiliser pour écrire une séquence entière (voir premier-contact et relance), ni pour un objet seul (voir objets).
---

Une ouverture qui cite un fait vérifié sur la personne, cousu au problème que vous résolvez, fait passer une campagne de 2 à 5 % de réponses à 10 à 20 % (de 6 à 8 % à 18 à 22 % sur les sources anglophones). La personnalisation à volume marche quand l'ouverture est la seule partie variable de l'email, quand elle ne porte aucune affirmation sur l'offre, et quand une ligne sans bon ancrage reste vide plutôt que générique.

## Ressources

- `{SKILL_BASE}/ressources/seaux-personnalisation.md` : les 6 seaux, hook fort et léger, playbooks par catégorie, matrice de décision, playbooks avancés.
- `{SKILL_BASE}/ressources/ouvertures-personnalisees.md` : la méthode "la liste est le message" et l'ouverture de deux phrases par personne.
- `{SKILL_BASE}/ressources/prompts-personnalisation.md` : les prompts qui produisent les variables, et le prompt maître de l'expéditeur.
- `{SKILL_BASE}/ressources/relecteurs.md` : le relecteur recherche sur chaque ancrage.

## Méthode

1. **Évaluer la donnée disponible** : quels seaux le CSV remplit-il déjà ? Posts (seau 1), engagement (seau 2), headline (seau 3), parcours (seau 5), signaux d'entreprise (seau 6) ?
2. **Décider la profondeur** avec la matrice de `seaux-personnalisation.md` : par personne si panier élevé, tier A, moins de 50 envois par jour, et si l'utilisateur peut relire les lignes ; par segment sinon. Le dire dans le brief.
3. **Choisir le hook** : fort (citation littérale) pour les comptes clés et le remplacement d'un concurrent ; léger (thème) pour le volume.
4. **Fournir les faits du métier** par segment (la carte de `ouvertures-personnalisees.md`) : le générateur ne cite que le travail présent dans le segment.
5. **Générer l'ouverture** de deux phrases (35 mots au plus) par ligne, avec le jugement `utilisable` et sa raison. Une ligne non utilisable prend l'ouverture de segment et se marque comme repli.
6. **Contrôler chaque ligne** : le test de l'inconnu (la ligne reste-t-elle vraie pour quelqu'un d'autre ?), le scoring interne, la checklist §H. Régénérer avec la raison de l'échec, deux ou trois fois ; corriger le prompt si le taux d'échec dépasse 20 %.
7. **Montrer chaque type** avant l'envoi : l'ouverture, le fait dessous, la source, un repli, le corps fixe. Rapporter la part de lignes personnalisées et de replis.

## Exécution

Chaque verbe seulement si sa colonne est vide :

1. `enrichir_personne` (skill `enrichir-personne`) : headline, résumé, ancienneté, parcours, et les 5 derniers posts avec `--posts`. Colonnes : `titre`, `headline`, `resume`, `anciennete_poste`, `experiences`, `posts_recents` (avec `--posts`).
2. `scraper_engagement` (skill `scraper-engagement`) : la réaction ou le commentaire sur un post donné (`--post <url>`, ou `--mes-posts N` pour vos N derniers posts). Colonnes : `signal_type` (`commentaire` ou `like`), `signal_detail`.
3. `enrichir_entreprise` (skill `enrichir-entreprise`) : description, site, et les 5 derniers posts de la page avec `--posts`. Colonnes : `description`, `tagline`, `domaine`, `posts_recents` (avec `--posts`). Aucune colonne `actualite` : l'actualité se lit dans `posts_recents` et dans `signal_detail`.
4. `detecter_signal` (skill `detecter-signaux` (script `detecter_signal.py`)) : levée, recrutement, changement de poste. Colonnes : `signal_type`, `signal_date`, `signal_detail`.
5. `detecter_techno` (skill `enrichir-entreprise --techno`) et `scraper_offres_emploi` (skill `scraper-offres-emploi`) quand l'angle le demande. Colonnes réelles : `technos` (liste des outils détectés), `nb_offres_emploi` (`enrichir_entreprise`) et, par offre, `poste`, `url_offre`, `signal_detail` ; Claude en déduit l'outil ou l'offre à citer, aucun verbe n'écrit `techno` ni `offres_emploi`.
6. Génération (interne, prompts de `prompts-personnalisation.md`) : colonnes `ouverture`, `ouverture_utilisable` (oui ou non), `ouverture_raison`, `ouverture_source`, `ouverture_seau` (1 à 6 ou repli).
7. `envoyer_sequence` (skill `envoyer-sequence`) : `envoyer_lemlist.py --colonne-message ouverture` pousse la colonne `ouverture` comme variable `icebreaker`, insérée dans le corps fixe écrit dans Lemlist (ou par le MCP), après validation.

Entrée : CSV normalisé avec au moins `prenom`, `entreprise`, `titre`, `linkedin_url`. Sortie : le même CSV enrichi des colonnes d'ouverture, dans `05_Departements/Go-to-Market/Messages/messages_<sujet>_<YYYY-MM-DD>.csv`.

## Repères

| Repère | Valeur |
|---|---|
| Ouverture | 2 phrases, 35 mots au plus, aucune affirmation sur l'offre |
| Fraîcheur d'un ancrage | moins de 90 jours ; un post de la semaine bat une levée d'il y a 2 ans |
| Seaux par valeur | 1 publié, 2 engagé, 3 auto-description, 4 tiroir à bazar, 5 parcours, 6 entreprise |
| Personnaliser si | panier > 25 k€, tier A, < 50 envois par jour, signal faible |
| S'en passer si | panier < 25 k€, tiers B et C, > 100 envois par jour, signal fort |
| Taux de repli acceptable | 30 à 60 % des lignes ; au-delà, changer de segment ou de donnée |
| Réponse attendue | 2 à 5 % sans signal, 10 à 20 % avec ; les 6 à 8 %, 18 à 22 % et 35 à 40 % des sources anglophones sont des repères étrangers |
| Effort à volume | la segmentation bat la personnalisation individuelle |

## Template

```
Bonjour {{prenom}},

{{ouverture : phrase 1, le fait vérifié sur la personne ; phrase 2, le problème à côté ou une question de diagnostic}}

{{corps fixe validé : ce que vous faites, la preuve chiffrée}}

{{CTA unique}} ?
```

Exemple d'ouverture (fictif, seau 1) : "Vous écriviez la semaine dernière que vos commerciaux passent plus de temps dans le CRM que chez les clients. Combien d'heures par semaine part dans la saisie chez Novapress ?"

Jugement rendu avec la ligne : `{"utilisable": true, "raison": "post relié à la saisie CRM, le problème de la campagne", "ouverture": "..."}`

## Règles

1. Un fait vérifié, daté, sourcé. Jamais une supposition sur la personne présentée comme un fait.
2. L'ouverture ne porte aucune affirmation sur l'offre : le corps fixe s'en charge, validé une fois.
3. Le test de l'inconnu sur chaque ligne : si elle reste vraie pour quelqu'un d'autre, elle n'est pas personnalisée.
4. Aucun compliment générique ; un compliment se justifie par un fait précis ou disparaît.
5. Une ligne sans bon ancrage reste vide (repli de segment), jamais générique.
6. La segmentation se rapporte comme de la segmentation, pas comme de la personnalisation.
7. Le prompt se corrige, pas les lignes : un taux d'échec élevé est un problème de prompt ou de donnée.
8. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md` sur chaque ouverture.

## Exemples

- "Personnalise la première ligne pour ces 150 DRH" : évaluation des seaux disponibles, profondeur par segment avec ouverture par personne sur les lignes qui ont un post récent, génération avec jugement, aperçus par type, rapport personnalisées contre replis.
- "Écris un icebreaker pour ce prospect" (données collées) : choix du seau le plus fort et le plus récent, trois variantes en interne, scoring, une seule ligne rendue, entre guillemets.
- "Comment je personnalise à l'échelle sans que ça sonne robot ?" : matrice de décision, ouverture variable plus corps fixe, prompts 8 et 9 de `prompts-personnalisation.md`, contrôle ligne par ligne, taux de repli attendu.
