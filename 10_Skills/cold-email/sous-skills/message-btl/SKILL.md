---
name: message-btl
description: >
  Écrit pour un manager, un responsable ou un opérationnel (chef d'équipe, responsable marketing, chargé de recrutement, contrôleur de gestion, chef de projet, utilisateur final) : douleur quotidienne, temps gagné chiffré, comment il devient votre champion en interne. Se déclenche sur : "email à un manager", "au responsable", "à un opérationnel", "utilisateur final", "champion", "message BTL", "chargé de", "chef d'équipe", "approche par le bas". Ne pas utiliser pour un dirigeant, un directeur ou un VP (voir message-atl), ni sans persona identifié (voir premier-contact).
---

Un manager ou un opérationnel vit dans le présent : il veut que le problème de sa semaine disparaisse, il lit 3 à 4 phrases, et il répond quand l'email nomme la tâche exacte qui lui prend 3 heures le vendredi. Le persona BTL commande la longueur et l'angle ; ce sous-skill se lit avant `premier-contact` ou `relance` quand la cible est un manager ou un opérationnel.

## Ressources

- `{SKILL_BASE}/ressources/registre-audience.md` : le registre d'un opérationnel, la question de diagnostic.
- `{SKILL_BASE}/ressources/frameworks-13.md` : Le problème d'abord, Problèmes typiques du rôle, Avant / Après, Trouvaille-valeur-question.
- `{SKILL_BASE}/ressources/variations-email-1.md` : la variante 7 (douleur du rôle) et la variante 3.
- `{SKILL_BASE}/ressources/templates-34.md` : #3 (recrutement d'utilisateurs), #12 (techno), #14 (agitation du problème).
- `{SKILL_BASE}/ressources/seaux-personnalisation.md` : les playbooks sans personnalisation, qui marchent bien en BTL.

## Méthode

1. **Confirmer le persona** : titre, séniorité, personas BTL de `05_Departements/Go-to-Market/contexte.md`. Manager, responsable, chargé de, chef de projet, analyste, coordinateur : BTL. Directeur de fonction dans une entreprise de plus de 200 personnes : ATL.
2. **Trouver la douleur de sa semaine** : la tâche manuelle, l'outil qu'il subit, le rapport du vendredi, la relance qu'il fait à la main. Sources : la fiche de poste de son propre recrutement ou de ses collègues (`scraper_offres_emploi`), sa stack (`detecter_techno`), ses posts (`enrichir_personne`).
3. **Chiffrer le temps ou l'effort** : "3 heures par semaine", "40 relances par mois", "12 minutes par note de frais". Un pourcentage seul ("70 % de temps en moins") passe après un chiffre absolu.
4. **Écrire 3 à 4 phrases** : la tâche nommée, ce qui change concrètement, la preuve chez une équipe comparable, une question. Le langage de l'action : "arrêter de", "ne plus refaire", "en 2 minutes au lieu de 20".
5. **Le faire bien voir de son chef** : un résultat qu'il pourra montrer (un rapport plus tôt, une erreur en moins, un délai tenu). C'est ce qui transforme un utilisateur en champion.
6. **Prévoir la suite** : un BTL convaincu a besoin d'un email qu'il peut transférer à son directeur. Préparer la version ATL (`message-atl`) en email 2 ou en pièce transférable.
7. **Passer les relecteurs**.

## Exécution

1. `scraper_offres_emploi` (skill `scraper-offres-emploi`) : les fiches de poste de son service décrivent les tâches quotidiennes. Colonnes réelles : `poste`, `url_offre`, `signal_detail` par offre, `nb_offres_emploi` par entreprise (`enrichir_entreprise`). Les tâches se déduisent par Claude en lisant la fiche à `url_offre` ; aucun verbe n'écrit `offres_emploi` ni `taches_detectees`.
2. `detecter_techno` (skill `enrichir-entreprise --techno`) : les outils qu'il utilise ou subit. Colonne réelle : `technos` (liste des outils détectés) ; Claude en tire l'outil à citer, aucune colonne `techno`.
3. `enrichir_personne` (skill `enrichir-personne`) : headline, ancienneté, et les posts avec `--posts`. Colonnes : `headline`, `anciennete_poste`, `posts_recents` (avec `--posts`).
4. `trouver_email` (skill `trouver-email`) : email vérifié. Colonnes : `email`, `email_statut`.
5. Rédaction (interne) : `persona` = BTL, `douleur`, `var_objet`, `var_email_1`, puis `premier-contact` et `relance` pour la séquence.
6. `envoyer_sequence` (skill `envoyer-sequence`) après validation sur trois exemples.

Entrée et sortie : celles de `premier-contact`, avec `persona` = BTL.

## Repères

| Repère | Valeur |
|---|---|
| Longueur | 3 à 4 phrases, 90 mots au plus |
| Cibler BTL quand | adoption par l'usage, produit qui s'essaie, vente par le bas, besoin d'un champion avant le budget |
| Ce qu'il suit | sa charge, le temps perdu, les erreurs qu'on lui reproche, ce que son chef voit |
| Ce qui ne lui parle pas | le retour sur investissement, "l'impact stratégique", le conseil d'administration |
| Angle le plus fort | la tâche manuelle nommée, chiffrée en heures |
| Signal le plus fort | le recrutement d'un poste de son équipe, sa stack |
| Réponse attendue | 2 à 5 % à froid, 10 à 20 % avec un signal de poste ou de techno (6 à 8 % et 18 à 22 % sur les sources anglophones) |

## Template

```
Objet : {{la tâche manuelle}}

Bonjour {{prenom}},

Combien de temps votre équipe passe sur {{tâche}} chaque semaine ? La plupart des {{titre}} que je rencontre disent {{n}} heures.

{{Ce qui change concrètement}} : {{résultat chez une équipe comparable, en heures ou en erreurs}}.

{{CTA de ressource ou d'intérêt}} ?
```

Exemple (fictif) :

```
Objet : vos rapports de campagne

Bonjour Julie,

Combien de temps vous passez chaque semaine à monter les rapports de campagne dans Excel ? Les responsables marketing que je rencontre disent 3 heures, le vendredi.

L'équipe marketing de Wexo sort le même rapport en 20 minutes le lundi matin, avec les mêmes sources, et la directrice l'a avant sa réunion.

Je vous montre le modèle ?
```

## Règles

1. 3 à 4 phrases, la tâche nommée dès la première.
2. Des heures, des minutes, des erreurs, des relances : un chiffre absolu avant un pourcentage.
3. Le langage de l'action ("arrêter de", "en 2 minutes"), pas le langage du résultat financier.
4. Un résultat qu'il peut montrer à son chef.
5. Une preuve chez une équipe de même fonction, pas chez un dirigeant.
6. Un CTA de ressource ou d'essai : "je vous montre le modèle ?", "vous voulez tester sur un rapport ?".
7. Vouvoiement, même avec un profil junior ; ton direct, jamais condescendant.
8. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md`.

## Exemples

- "Écris aux responsables marketing de PME" : persona BTL, douleur de la semaine trouvée dans les fiches de poste (`scraper_offres_emploi`), template #14, 3 à 4 phrases, CTA de ressource, trois exemples montrés.
- "J'ai un champion chez eux, il veut transférer à sa directrice" : un email ATL de 3 phrases (`message-atl`) rédigé pour être transféré, avec le résultat que le champion a obtenu en ligne 1.
- "Mon email parle de ROI et personne ne répond, la cible c'est des chefs de projet" : réécriture en BTL, la tâche nommée, le temps chiffré, la preuve chez une équipe comparable, suppression du ROI.
