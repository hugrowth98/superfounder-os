---
name: relance
description: >
  Écrit les emails 2 et 3 d'une séquence de prospection active (relances à J+3 et J+14), avec rotation des propositions de valeur et question de routage. Se déclenche sur : "relance", "email 2", "email 3", "il n'a pas répondu", "pas de réponse", "que j'envoie après", "email de rupture", "séquence de relance", "bump". Ne pas utiliser pour le premier email (voir premier-contact), pour un prospect contacté il y a des semaines ou des mois hors séquence (voir reengagement), ni pour un objet seul (voir objets).
---

Une relance qui ajoute une information obtient 6 à 8 % de réponses ; une relance qui demande "avez-vous vu mon email" en obtient moins de 1 % et pèse sur la réputation du domaine. Les emails 2 et 3 tournent l'angle de valeur, raccourcissent, et finissent par demander la bonne personne.

## Ressources

- `{SKILL_BASE}/ressources/sequences.md` : la structure 3 emails, la variante 4 emails, la rotation des angles, la rupture.
- `{SKILL_BASE}/ressources/templates-34.md` : les relances #27 à #30 et le dernier essai #18.
- `{SKILL_BASE}/ressources/variations-email-1.md` : les templates d'email 2 et 3 en fin de fichier.
- `{SKILL_BASE}/ressources/principes-copywriting.md` : le "et donc" de chaque angle, les CTA.
- `{SKILL_BASE}/ressources/relecteurs.md` : relecture avant de rendre.

## Méthode

1. **Relire l'email 1** : quel framework, quel angle de valeur, quel CTA, quel objet ? La relance ne les répète pas.
2. **Vérifier qui a répondu** (`verifier_reponses`) : toute personne qui a répondu, sur n'importe quel canal, sort de la séquence avant d'écrire.
3. **Changer l'angle** : email 1 économiser de l'argent, email 2 gagner de l'argent, email 3 gagner du temps (ou l'ordre qui colle à l'offre). Chaque angle porte son "et donc".
4. **Chercher une information nouvelle** pour l'email 2 : une preuve coupée de l'email 1, une ressource, un signal frais (`detecter_signal` sur les lignes de la campagne).
5. **Écrire l'email 2** : même fil (RE: objet de l'email 1), plus court que l'email 1, un CTA d'un autre style. J+3 à J+5.
6. **Écrire l'email 3** : nouvel objet, nouveau fil, une autre variante d'email 1, une ressource ou un audit court, et la question de routage. J+14 à J+17.
7. **Écrire la rupture** si la séquence en compte 4 : "ce n'est pas la priorité en ce moment ?", sortie propre, porte ouverte. J+21.
8. **Passer les relecteurs**, montrer les trois emails remplis sur trois prospects, attendre le oui.

## Exécution

1. `verifier_reponses` (skill `verifier-reponses`) : qui a répondu et sur quel canal. Colonnes : `reponse`, `reponse_canal`, `reponse_date`, `ne_plus_contacter`. Les lignes avec réponse sont retirées.
2. `detecter_signal` (skill `detecter-signaux` (script `detecter_signal.py`)) sur les lignes restantes, seulement si `signal_date` a plus de 30 jours : une information nouvelle pour l'email 2. Colonnes : `signal_type`, `signal_date`, `signal_detail`.
3. `trouver_personnes` (skill `trouver-personnes`) sur la même entreprise, facultatif, pour nommer un collègue dans la question de routage de l'email 3. Colonne : `collegue_prenom`, `collegue_titre`.
4. Rédaction (interne) : colonnes `email_2`, `email_3`, `email_4` (si rupture), `objet_email_3`.
5. `envoyer_sequence` (skill `envoyer-sequence`) : ajout des étapes à la campagne Lemlist existante (`add_sequence_step`), délais J+3 et J+14, même fil pour l'email 2.

Entrée : le CSV de la campagne (`messages_<sujet>_<date>.csv`) avec `email_1` et `objet` remplis. Sortie : le même CSV enrichi des colonnes de relance, et `sequence_<sujet>_<date>.md` mis à jour dans `05_Departements/Go-to-Market/Messages/`.

## Repères

| Repère | Valeur |
|---|---|
| Email 2 | J+3 à J+5, même fil, plus court que l'email 1 |
| Email 3 | J+14 à J+17, nouvel objet, question de routage |
| Email 4 (rupture) | J+21, 2 à 3 phrases, sortie propre |
| Écart minimum | 3 jours ; 1 jour est trop court |
| Maximum sans pause | 3 emails (4 sur un compte multi-interlocuteurs) |
| Après la séquence | 3 mois de pause, puis un autre angle |
| Réponse attendue | email 2 : 40 à 60 % de l'attention de l'email 1 ; email 4 : souvent le meilleur taux de la séquence |
| Relance en 7 points | 6 à 8 % de réponse |

## Template

Email 2, même fil :

```
Objet : RE: {{objet de l'email 1}}

{{prenom}}, une chose que j'avais laissée de côté : {{preuve ou information nouvelle}}.

{{client_similaire}} {{résultat sous un autre angle que l'email 1}}.

{{CTA d'un autre style}} ?
```

Email 3, nouveau fil :

```
Objet : {{nouvel objet}}

Bonjour {{prenom}},

{{Une autre variante d'email 1 : douleur du rôle, chiffre, ou ressource}}.

{{Ressource ou audit court proposé}}.

Si ce n'est pas vous qui suivez {{sujet}} chez {{entreprise}}, qui devrais-je contacter ?
```

## Règles

1. Chaque relance apporte une information nouvelle. Jamais "je reviens vers vous", jamais "avez-vous vu mon email", jamais une relance qui ne fait que redemander.
2. L'angle de valeur change à chaque email ; le CTA change de style.
3. Chaque relance est plus courte que la précédente.
4. Pas de culpabilisation, pas de supplication, pas d'humour forcé sur le silence.
5. L'email 2 reste dans le fil ; l'email 3 ouvre un nouveau fil avec un nouvel objet.
6. Une personne qui a répondu, même "non", ne reçoit plus aucune relance.
7. L'humour (template #28) seulement si c'est la voix de l'expéditeur et si la cible n'est pas formelle.
8. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md` sur chaque email.

## Exemples

- "Il n'a pas répondu à mon premier email, j'envoie quoi ?" : demande de l'email 1, email 2 dans le même fil avec une preuve ou une ressource coupée de l'email 1, angle de valeur différent, CTA de ressource.
- "Écris les relances de ma campagne DAF" : `verifier_reponses` d'abord, puis email 2 (J+3, même fil, calcul détaillé promis dans l'email 1) et email 3 (J+14, nouvel objet, question de routage vers le contrôleur de gestion), colonnes ajoutées au CSV.
- "Fais-moi un email de rupture" : template #18 ou la rupture de la séquence 4 emails, 3 phrases, question de timing, sortie propre, sans reproche.
