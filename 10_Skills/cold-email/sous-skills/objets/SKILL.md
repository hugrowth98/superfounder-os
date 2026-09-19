---
name: objets
description: >
  Écrit et teste les objets d'email de prospection : règles, formules, tests A/B, ce qui marche en France. Se déclenche sur : "objet", "objet d'email", "ligne d'objet", "taux d'ouverture", "test A/B d'objet", "mes emails ne sont pas ouverts", "quel objet je mets". Ne pas utiliser pour écrire le corps de l'email (voir premier-contact ou relance), ni quand les emails partent en spam (voir infra-email).
---

Un objet de 2 à 5 mots, en minuscules, sur le sujet de l'email et pas sur l'offre, ressemble à un email de collègue et double le taux de réponse par rapport à un objet marketing. L'objet et la première ligne s'affichent côte à côte dans la boîte de réception : ils forment une seule pensée.

## Ressources

- `{SKILL_BASE}/ressources/principes-copywriting.md` : la section objet et la section première ligne.
- `{SKILL_BASE}/ressources/prompts-personnalisation.md` : le prompt "objet en deux mots".
- `{SKILL_BASE}/ressources/metriques-benchmarks.md` : les règles de test A/B.
- `{SKILL_BASE}/ressources/delivrabilite.md` : les mots qui déclenchent les filtres.

## Méthode

1. **Lire l'email** : quel framework, quel angle, quelle première ligne ? L'objet en découle, il ne se choisit pas avant le corps.
2. **Écrire 3 à 5 options** en mélangeant les familles : personnalisé (le signal, le chiffre du prospect), curiosité (un sujet, une question courte), valeur directe (un résultat, un nombre), deux mots du métier.
3. **Vérifier chaque option** : 2 à 5 mots ; minuscules sauf noms propres ; aucun mot de spam ; aucune promesse que le corps ne tient pas ; l'objet plus la première ligne se lisent d'une traite.
4. **Recommander un test** : deux objets de familles opposées (personnalisé contre curiosité, court contre un peu plus long), 100 envois chacun, jugés sur la réponse et le rendez-vous, jamais sur l'ouverture seule.
5. **Régler le fil** : l'email 2 garde l'objet en RE:, l'email 3 prend un nouvel objet.
6. **Passer le relecteur qualité** (`relecteurs.md`) sur les objets retenus.

## Exécution

Ce sous-skill n'appelle aucun verbe de collecte : il travaille sur un email déjà écrit et sur les colonnes du CSV (`signal_type`, `signal_detail`, `entreprise`, `secteur`) pour personnaliser l'objet.

1. Rédaction (interne) : colonnes `objet`, `objet_b` (variante de test), `objet_email_3`.
2. `envoyer_sequence` (skill `envoyer-sequence`) : les deux objets en variante A/B dans Lemlist (`set_ab_variant`), 50 % chacun, après validation.
3. `verifier_reponses` (skill `verifier-reponses`) après 100 envois par variante : taux de réponse par objet, choix du gagnant, généralisation.

Entrée : le CSV de campagne avec `email_1`. Sortie : le même CSV avec les colonnes d'objet, et le résultat du test noté dans `sequence_<sujet>_<date>.md`.

## Repères

| Repère | Valeur |
|---|---|
| Longueur | 2 à 5 mots ; 2 mots pour la formule automatique |
| Casse | minuscules, sauf noms propres et sigles |
| Ponctuation | aucune : pas de point d'exclamation, pas de majuscules décoratives |
| Test | 2 objets à la fois, 100 envois chacun, jugés sur la réponse |
| Fil | email 2 en RE:, email 3 nouvel objet |
| Mots à bannir | gratuit, garanti, urgent, offre, promotion, dernière chance, cliquez |
| Ouverture attendue (mesurée une fois, sur échantillon) | 50 % et plus ; sous 30 %, problème de délivrabilité, pas d'objet |

Ce qui marche en France : le nom de l'entreprise ou du projet du prospect ("les recrutements de Novapress"), un chiffre qui lui appartient ("12 postes ouverts"), un sujet de son métier en deux mots ("clôture mensuelle", "relances devis"), une question courte sans point d'interrogation racoleur ("question sur vos relances"). Ce qui échoue : "Proposition de partenariat", "Collaboration", "Opportunité", "Découvrez", un "RE:" mensonger sur un premier email, un objet qui vend.

## Template

Quatre familles, pour un email 1 sur le recrutement commercial :

```
Personnalisé     recrutement commercial chez Novapress
Chiffre          3 postes de commerciaux
Curiosité        question sur votre prospection
Deux mots        rendez-vous commerciaux

Test recommandé : "3 postes de commerciaux" contre "question sur votre prospection".
Email 3          vos rendez-vous de la rentrée
```

Pour un réengagement : "depuis notre échange" (reconnaît l'historique) contre "question rapide" (neutre).

Les formules par famille :

| Famille | Squelettes |
|---|---|
| Personnalisé | {{sujet du signal}} ; {{métrique}} chez {{entreprise}} ; {{n}} ans |
| Curiosité | question rapide ; une chose sur {{sujet}} ; {{entreprise}} et {{résultat}} |
| Valeur directe | 3 heures de saisie en moins ; {{n}} leads potentiels ; votre clôture en 5 jours |
| Deux mots | {{mot du métier}} {{mot du métier}} : "relances devis", "clôture mensuelle" |

## Règles

1. L'objet parle du lecteur ou de son sujet, jamais de vous ni de votre offre.
2. Il tient ce que le corps donne : un objet trompeur fait ouvrir une fois et classer en spam pour toujours.
3. Jamais de "RE:" ni de "TR:" sur un premier email.
4. Jamais de prénom dans l'objet : c'est le signe le plus sûr d'un envoi automatisé.
5. Un mot de spam dans l'objet et l'email ne part pas.
6. On juge un objet sur les réponses, pas sur les ouvertures.
7. Un seul objet par email ; les variantes en rotation ne servent qu'au test A/B.

## Exemples

- "Quel objet je mets pour cet email ?" : lecture du corps, 4 options (personnalisé, chiffre, curiosité, deux mots), test recommandé entre deux familles, objet de l'email 3.
- "Mes emails ne sont pas ouverts" : vérification que le problème vient bien de l'objet et pas de la délivrabilité (rebond, placement), puis test de deux objets de familles opposées sur 100 envois chacun.
- "Génère un objet pour chaque ligne de mon CSV" : prompt "objet en deux mots" de `prompts-personnalisation.md` sur `signal_detail` ou `secteur`, colonne `objet`, contrôle des mots de spam ligne par ligne, 10 exemples montrés avant de généraliser.
