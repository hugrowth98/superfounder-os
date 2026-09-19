---
name: reengagement
description: >
  Écrit les emails qui réactivent des prospects anciens hors séquence active : rendez-vous sans suite, affaires perdues, prospects disparus, séquences terminées depuis 3 mois, renouvellements. Se déclenche sur : "réengager", "réactiver", "closed-lost", "affaire perdue", "il a disparu", "plus de nouvelles depuis", "relancer d'anciens leads", "reprendre contact". Ne pas utiliser pour les relances d'une séquence en cours (voir relance), pour un premier contact (voir premier-contact), ni pour un rendez-vous manqué (sous-skill no-show du master cold-call).
---

Un prospect qui a répondu une fois, ou qui a pris rendez-vous, vaut dix contacts à froid : la question orientée non ("ce serait une mauvaise idée de reprendre le fil ?") obtient 10 à 15 % de réponses sur ces listes. Le réengagement marche quand il reconnaît le silence, apporte du nouveau, et rend le non facile.

## Ressources

- `{SKILL_BASE}/ressources/templates-34.md` : les templates #31 à #34 et le tableau de timing du réengagement.
- `{SKILL_BASE}/ressources/sequences.md` : la pause de 3 mois et la réutilisation de la liste.
- `{SKILL_BASE}/ressources/reponses.md` : pour répondre quand le prospect reprend le fil.
- `{SKILL_BASE}/ressources/relecteurs.md` : relecture avant de rendre.

## Méthode

1. **Reconstituer l'historique** : dernier contact (date, canal), ce qui a été dit, l'objection donnée, pourquoi le fil s'est arrêté. Source : HubSpot (à lire dans le CRM, ou `crm lire --statut perdus` pour les affaires perdues avec leur `date_cloture`), le CSV de la liste d'appel (`resultat_appel`, `qualification_cold_call`, `objection_principale`, `next_step`), Lemlist, notes de l'utilisateur. Sans historique, c'est un premier contact, pas un réengagement.
2. **Classer la situation** : disparu en pleine conversation (2 à 3 semaines), démo sans suite (2 à 4 mois), affaire perdue (3 à 6 mois), séquence terminée (3 mois), renouvellement (30 à 60 jours avant).
3. **Vérifier que la personne est toujours en poste** (`enrichir_personne`). Si elle a changé d'entreprise, le message change : template #19 (reconnexion) plutôt que réengagement.
4. **Trouver ce qui a changé** depuis : une nouveauté de l'offre, un nouveau cas client, un signal chez le prospect (`detecter_signal`). Sans nouveauté, pas d'email.
5. **Choisir le template** selon la situation (#31 à #34) et écrire : reconnaître l'écart, citer ses mots s'il a donné une objection, dire le nouveau, CTA très doux.
6. **Revérifier l'email** si le dernier contact a plus de 30 jours (`trouver_email`).
7. **Passer les relecteurs**, montrer trois emails remplis, attendre le oui.

## Exécution

1. Historique : aucun verbe ne produit de colonnes `dernier_contact_*`, `statut_affaire`, `objection` ou `notes`. Le dernier contact, le statut de l'affaire et l'objection se lisent dans HubSpot (le skill `crm` n'exporte que les affaires gagnées ou perdues, `crm lire --statut perdus`, avec `date_cloture`, sans raison de perte) ou dans le CSV de la liste d'appel (`resultat_appel`, `qualification_cold_call`, `objection_principale`, `next_step`), et Claude les recopie dans le CSV de réengagement. `dedoublonner --hubspot` (skill `dedoublonner`) sert seulement à marquer `dans_crm` et les identifiants HubSpot.
2. `verifier_reponses` (skill `verifier-reponses`) : personne n'a repris le fil entre-temps. Colonnes : `reponse_canal`, `reponse_date`, `reponse_texte`, `ne_plus_contacter`.
3. `enrichir_personne` (skill `enrichir-personne`) : toujours en poste ? Colonnes : `titre`, `entreprise`, `anciennete_poste`, `experiences` (Claude compare avec l'entreprise connue ; aucune colonne `changement_poste`). Le signal `changement_poste` daté vient de `detecter_signal` (`signal_type`, `signal_date`).
4. `detecter_signal` (skill `detecter-signaux` (script `detecter_signal.py`)) : ce qui a changé chez lui. Colonnes : `signal_type`, `signal_date`, `signal_detail`.
5. `trouver_email` (skill `trouver-email`) si `email_statut` a plus de 30 jours.
6. Rédaction (interne) : colonnes `situation` (disparu, demo, perdu, sequence, renouvellement), `nouveaute`, `var_objet`, `var_email_1`, `var_email_2` (préfixe `var_` : poussées comme variables Lemlist).
7. `envoyer_sequence` (skill `envoyer-sequence`) : campagne Lemlist dédiée, 2 emails au plus ; `envoyer_lemlist.py` pousse les leads et leurs variables, les deux étapes s'écrivent dans Lemlist ou par le MCP. Après validation.

Entrée : CSV des anciens prospects, avec au minimum `prenom`, `entreprise`, `email`, `dernier_contact_date`. Sortie : `messages_reengagement_<sujet>_<YYYY-MM-DD>.csv` dans `05_Departements/Go-to-Market/Messages/`.

## Repères

| Situation | Attente avant d'écrire | Template |
|---|---|---|
| Disparu en pleine conversation | 2 à 3 semaines | #33 |
| Démo ou rendez-vous sans suite | 2 à 4 mois | #31 |
| Affaire perdue | 3 à 6 mois | #32 |
| Séquence terminée sans réponse | 3 mois | nouvelle séquence, autre angle |
| Renouvellement | 30 à 60 jours avant l'échéance | #34 |
| Réponse attendue | 10 à 15 % (#31), 20 à 25 % pour un ancien client qui a changé de poste |
| Emails par réengagement | 2 au plus, à 5 jours d'écart |

## Template

```
Objet : depuis notre échange

Bonjour {{prenom}},

Quand on s'est parlé en {{mois}}, vous m'aviez dit que {{objection, avec ses mots}}.

Depuis, {{ce qui a changé : nouveauté, cas client, résultat}}.

Ça mérite un second regard, ou le sujet est clos chez {{entreprise}} ?
```

Pour un prospect disparu en pleine conversation (#33) :

```
Objet : on en est où ?

Bonjour {{prenom}},

On parlait de {{sujet}} en {{mois}}, puis silence de votre côté. Ça arrive, les priorités bougent.

C'est toujours sur votre liste, ou je ferme le dossier ?
```

## Règles

1. Reconnaître l'écart : ne jamais faire comme si l'échange précédent n'avait pas eu lieu.
2. Ouvrir sur ce qui a changé, jamais sur "je prends de vos nouvelles".
3. Citer ses mots : l'objection nommée prouve qu'on a écouté.
4. Rendre le non facile : "toujours pertinent ?", "ça mérite un second regard ?", "je ferme le dossier ?". Jamais "réservons un créneau".
5. Deux emails au plus, puis 6 mois de silence.
6. Une personne en `ne_plus_contacter` ou qui a écrit "pas intéressé" ne se réengage pas.
7. Vérifier le poste et l'email avant d'écrire : un réengagement envoyé au mauvais poste brûle un contact chaud.
8. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md` sur chaque email.

## Exemples

- "Je veux relancer les prospects qui ont fait une démo il y a 3 mois" : l'historique lu dans HubSpot ou le CSV de la liste d'appel, `enrichir_personne` pour le poste, template #31 avec la nouveauté depuis la démo, deux emails à 5 jours, trois exemples montrés.
- "On a perdu cette affaire en mars, il avait dit que c'était trop cher" : template #32, l'objection prix citée, ce qui a changé (nouvelle formule, cas client comparable, calcul), CTA "second regard".
- "Il m'a posé un lapin jeudi" : sous-skill `no-show` du master `cold-call`, qui tient la procédure (appel dix minutes après l'heure, puis message de deux lignes avec deux créneaux).
