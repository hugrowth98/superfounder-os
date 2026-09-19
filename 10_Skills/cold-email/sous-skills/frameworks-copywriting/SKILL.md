---
name: frameworks-copywriting
description: >
  Donne le framework, les principes et la structure de séquence pour écrire ou réécrire un email de prospection : les 13 frameworks nommés, les 8 autorisés côté commercial, les règles par composant, les variantes, le ton par type d'offre, les exemplaires annotés. Se déclenche sur : "framework", "faites le calcul", "rupture de schéma", "structure d'email", "principes de copy", "règles d'écriture", "variantes d'email", "comment écrire un cold email", "test de copy", "email pour des e-commerçants", "réécris cet email". Ne pas utiliser pour la personnalisation à volume (voir personnalisation), pour un objet seul (voir objets), ni pour l'envoi d'une séquence (voir premier-contact).
---

Un framework est un mécanisme qui a fait répondre des milliers de fois : le calcul posé devant le lecteur, la question avant le pitch, la valeur donnée sans demande. Choisir le bon selon la preuve disponible et la cible fait la différence entre 1 % et 8 % de réponses ; l'écart entre variantes d'un même email atteint un facteur 13.

## Ressources

- `{SKILL_BASE}/ressources/frameworks-13.md` : les 13 frameworks avec template et exemple, les 8 autorisés, la base de séquence par déclencheur.
- `{SKILL_BASE}/ressources/principes-copywriting.md` : la philosophie, les règles par composant, ce qu'on ne fait jamais.
- `{SKILL_BASE}/ressources/regles-copy.md` : les limites, le ton par type d'offre, le cas e-commerce, les contrôles.
- `{SKILL_BASE}/ressources/variations-email-1.md` : les 7 variantes et les emails 2 et 3.
- `{SKILL_BASE}/ressources/sequences.md` : structures 2, 3 et 4 emails, séquences prêtes.
- `{SKILL_BASE}/ressources/exemplaires.md` : dix emails annotés.
- `{SKILL_BASE}/ressources/registre-audience.md` : le registre selon la cible.

## Méthode

1. **Qualifier la demande** : un framework nommé, une réécriture, une structure de séquence, des principes, un type d'offre particulier ?
2. **Pour un framework** : lire le tableau de choix de `frameworks-13.md`, proposer le framework qui colle à la preuve disponible (un chiffre du prospect : Faites le calcul ; une ressource tierce : L'insight neutre ; rien : Les responsabilités du rôle), donner le template et un exemple adapté à l'offre de `05_Departements/Go-to-Market/contexte.md`.
3. **Pour une réécriture** : nommer les tics du texte d'origine (relecteurs, checklist §H), garder l'angle et les faits, réécrire dans un framework, montrer le avant et l'après avec trois lignes sur ce qui a changé.
4. **Pour une structure** : `sequences.md`, choisir 2, 3 ou 4 emails selon la cible, donner le rôle et le timing de chaque email.
5. **Pour un type d'offre** : `regles-copy.md` section 6, le ton, ce qui marche, ce qui échoue ; pour l'e-commerce, 15 à 30 mots et une offre de travail gratuit.
6. **Rendre l'email** en texte brut, puis proposer de passer à `premier-contact` pour le remplir sur la liste.

## Exécution

Ce sous-skill n'appelle aucun verbe de collecte : il produit un email de référence ou une structure, sur les données déjà présentes. Le remplissage sur une liste et l'envoi passent ensuite par `premier-contact` (collecte, colonnes, `envoyer-sequence`).

Sortie : un bloc texte (objet, corps, variantes) et, si l'utilisateur le demande, `sequence_<sujet>_<YYYY-MM-DD>.md` dans `05_Departements/Go-to-Market/Messages/`.

## Repères

| Vous avez | Framework |
|---|---|
| Un chiffre du prospect à multiplier | Faites le calcul |
| Un signal fort et une preuve courte | Déclencheur court |
| Une douleur sectorielle connue | Le défi des entreprises semblables |
| Une ressource tierce utile | L'insight neutre |
| Une cible par fonction, sans signal | Les responsabilités du rôle, Problèmes typiques du rôle |
| Envie d'inverser le réflexe vendeur | La question avant le pitch |
| Des pairs qui ont le même problème | Le persona pas si différent |
| Un compte clé et du temps | La valeur d'abord |
| Un lead magnet | Le contenu comme porte d'entrée |
| Un prestataire ou un outil à remplacer | Pourquoi vous payez ça ?, Avant / Après |
| Un process manuel à remplacer | Le problème d'abord |
| Un service, une agence, un freelance | Trouvaille, valeur, question |
| Une petite structure, un fondateur | L'email écrit à la main |

| Règle | Valeur |
|---|---|
| Longueur | moins de 100 mots, cible 50 à 90 ; e-commerce 15 à 30 |
| Structure de séquence | J0, J+3 même fil, J+14 nouvel objet ; puis 3 mois de pause |
| Réponses sur l'email 1 | 80 % |
| Variantes à tester | 3 ou 4 |

## Template

Le squelette commun aux 13 frameworks :

```
Objet : {{2 à 5 mots sur son sujet}}

Bonjour {{prenom}},

{{Observation : le déclencheur, avec sa source}}

{{Proposition de valeur en résultat : gagner, économiser, ou du temps, avec le "et donc"}}

{{Preuve chiffrée, une phrase, entreprise nommée si reconnaissable}}

{{CTA unique, une question}} ?

PS : {{deuxième preuve, touche personnelle, ou ligne de routage}} (facultatif)
```

Chaque framework réorganise ces briques ou en supprime : Faites le calcul insère un calcul avant le CTA, La valeur d'abord supprime le CTA, La question avant le pitch met le CTA en première ligne.

## Règles

1. Un framework par email. Combiner deux frameworks donne un email de 140 mots.
2. Les 8 autorisés sans validation ; les 5 autres (analogie, humour, email écrit à la main, contenu porte d'entrée, persona pas si différent, trouvaille-valeur-question) avec l'accord de l'utilisateur, parce qu'ils engagent une voix.
3. Le mécanisme se garde, les mots changent : un template n'est jamais envoyé tel quel.
4. Les exemples des ressources sont fictifs : chaque chiffre vient de `05_Departements/Go-to-Market/contexte.md` ou n'apparaît pas.
5. Fait avant adjectif, résultat avant fonctionnalité, lecteur avant expéditeur.
6. Une réécriture garde l'angle et les faits de l'original, et dit ce qu'elle a changé.
7. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md`.

## Exemples

- "Donne-moi un framework pour écrire à un DAF sur les économies" : Faites le calcul, template, exemple avec un chiffre public de l'entreprise cible et une preuve de `05_Departements/Go-to-Market/contexte.md`, puis proposition de le remplir sur la liste via `premier-contact`.
- "Comment je structure ma séquence de 3 emails ?" : `sequences.md`, rôle et timing de chaque email, rotation des angles, question de routage en email 3, exemple de chaque email.
- "Je vends à des marques e-commerce, aide-moi" : `regles-copy.md` section e-commerce, 15 à 30 mots, offre de travail gratuit faite d'avance, deux templates, ton relâché, un lead magnet en email 2.
