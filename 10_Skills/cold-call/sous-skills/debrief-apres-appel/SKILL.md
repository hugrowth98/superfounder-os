---
name: debrief-apres-appel
description: >
  Analyse un appel terminé depuis des notes ou un transcript : résultat, probabilité que
  le rendez-vous ait lieu et débouche, objections entendues mot pour mot et meilleure
  réponse, ce qui a marché et un seul ajustement, prochain pas daté, ligne CRM, message de
  suivi ; ou le bilan chiffré d'une session d'appels. Se déclenche sur : "débriefe cet
  appel", "voici mes notes", "transcript de l'appel", "j'ai eu X au téléphone", "il a dit
  oui", "il m'a dit que", "bilan de ma session", "combien de rendez-vous ce matin",
  "qu'est-ce que je fais maintenant avec lui". Ne pas utiliser pour : préparer un appel
  (voir brief-avant-appel), s'entraîner sur une objection sans appel réel (voir
  objections), un rendez-vous manqué (voir no-show), un rendez-vous de découverte ou une
  démo (hors périmètre de ce master).
---

# Le débrief après l'appel

Un appel non débriefé est un appel perdu deux fois : la ligne CRM n'est pas écrite, et l'erreur se répète. Le débrief suit le rituel des ateliers, le positif d'abord, un seul ajustement, puis la ligne CRM "obligatoirement renseignée à la fin de chaque appel", avec une date de rappel pour toute relance, "sans tâche datée, le rappel se perd".

## Ressources

- `{SKILL_BASE}/ressources/posture.md` sections 4 à 6 et 10 : la grille des erreurs.
- `{SKILL_BASE}/ressources/objections-france.md` : la meilleure réponse à chaque objection entendue.
- `{SKILL_BASE}/ressources/sequence-multicanal.md` : ce qui arrête ou reprend la séquence.
- `05_Departements/Go-to-Market/contexte.md` sections 3 (le persona et ses problèmes) et 6 (voix, pour le message de suivi).
- `05_Departements/Go-to-Market/GARDE-FOUS.md` sections 1 et 4 avant d'envoyer le message de suivi.

## Méthode

1. Lire les notes ou le transcript. Extraire, dans les mots exacts du prospect : ce qu'il a dit de sa situation, chaque objection, chaque signe d'intérêt ("comment ça se passerait", "vous travaillez avec qui dans notre secteur", "envoyez-moi le créneau"), ce qui a été convenu à la fin.
2. Qualifier le résultat : rendez-vous pris (date, durée, invitation acceptée ou non), rappel demandé (date), refus, pas le bon interlocuteur (avec ou sans nom), entreprise hors cible, mauvais numéro, déjà client.
3. Estimer la probabilité que le rendez-vous ait lieu et débouche, de 0 à 100, avec les facteurs : invitation acceptée en ligne pendant l'appel (+), créneau à moins de 10 jours (+), question de qualification répondue (+), un problème reconnu ("oui, c'est ça") (+), créneau arraché après quatre objections (−), "envoyez-moi quand même un mail" après le oui (−), décideur absent (−).
4. Relever les objections et, pour chacune, comment elle a été prise et la réponse en trois temps qu'il fallait, tirée de la ressource et des problèmes du persona.
5. Dire ce qui a bien marché, en premier, avec une citation. Puis un seul ajustement, le plus important, dans la liste : présentation avant l'accroche, question de découverte, description de l'offre ou d'une fonctionnalité, argument ou chiffre en défense, "non mais", créneau demandé trop tard ou une seule fois, rendez-vous non verrouillé, signal cité brut, débit trop rapide.
6. Fixer le prochain pas, daté : confirmer le rendez-vous, rappeler tel jour à telle heure, envoyer l'intro par mail avec l'utilisateur en copie, ou clore.
7. Écrire la ligne CRM et le message de suivi (moins de 60 mots), le montrer, attendre le oui avant tout envoi.
8. Pour une session : compter appels, décrochés, rendez-vous, rappels, refus ; le taux de rendez-vous sur décrochés ; les deux objections les plus entendues ; l'ajustement unique pour la prochaine session.

## Exécution

Aucun verbe payant. `verifier_reponses` (skill `verifier-reponses`) si le prospect a dit qu'il écrirait, pour capter la réponse avant de relancer. Entrée : notes libres ou transcript collé, et la ligne du CSV de la liste d'appel si elle existe. Sortie : le débrief dans la conversation, la ligne CRM écrite dans le CSV de la liste (`resultat_appel`, `qualification_cold_call`, `rdv_date`, `date_rappel`, `next_step`, `objection_principale`), le message de suivi dans `05_Departements/Go-to-Market/Messages/suivi-appel_<Nom>_<YYYY-MM-DD>.md`. Si `05_Departements/Go-to-Market/OUTILS.md` dit `crm: hubspot`, proposer de pousser le contact, la note d'appel et la tâche datée dans HubSpot via le skill `crm` (`pousser --note "<débrief>" --tache "Rappeler" --echeance <date_rappel>`), après validation ; sinon la ligne reste dans le CSV.

## Repères

| Valeur de `qualification_cold_call` | Quand | Ce qui va avec |
|---|---|---|
| `Opportunité` | un créneau daté est pris | `rdv_date`, invitation envoyée, message de confirmation |
| `Relance cold call` | il demande à être rappelé, ou "pas le moment" avec une date | `date_rappel` obligatoire, sinon le rappel se perd |
| `Refus cold call` | refus net, ou trois vraies objections | rien avant 90 jours, sauf nouveau signal |
| `Contact non qualifié` | bonne entreprise, mauvais interlocuteur | le nom obtenu passe en nouvelle ligne, avec l'intro |
| `Entreprise non qualifiée` | hors cible | `exclu = oui`, raison |
| `Mauvais numéro` | injoignable, numéro faux | relance par un autre canal, pas de nouvel appel |
| `Client` | déjà client | retiré des listes d'appel |

Probabilité : au-dessus de 70, rendez-vous solide ; entre 40 et 70, envoyer la confirmation et un rappel J-1 ; sous 40, rappeler avant le rendez-vous pour le reconfirmer, ou considérer que c'est un oui de politesse.

## Template

> **Résultat.** [Rendez-vous mardi 14h, 20 minutes, invitation acceptée pendant l'appel.]
> **Probabilité qu'il ait lieu et débouche.** [75 %] : [invitation acceptée, créneau à 6 jours, a dit "oui, c'est exactement ça" sur le problème 2 ; a demandé un mail quand même].
> **Ce qu'il a dit.** "[citation 1]" "[citation 2]"
> **Objections.** "[objection, mot pour mot]" : pris en [trois temps / "oui mais"]. Réponse à garder : "[réponse en trois temps]".
> **Ce qui a bien marché.** [L'accroche a fait dire "c'est à quel sujet ?", le créneau a été redemandé trois fois.]
> **Un ajustement.** [La proposition de valeur a duré 40 secondes ; la couper à une phrase et laisser réagir.]
> **Prochain pas.** [Confirmation envoyée aujourd'hui, rappel J-1 lundi 17h.]
> **Ligne CRM.** `Opportunité`, rdv 2026-09-29 14:00, next_step "confirmer + rappel J-1".
> **Message de suivi (à valider).** "Bonjour [prénom], merci pour l'échange. Rendez-vous mardi 14h, l'invitation est dans votre boîte. On parlera de [problème reconnu] et de ce que [référence] a mis en place. À mardi. [Signature]"

## Règles

- Citations exactes du prospect, jamais paraphrasées, jamais complétées.
- Le positif d'abord, un seul ajustement. "On donne un seul ajustement, pas trois."
- Toute relance a une date. Un "rappelez-moi plus tard" sans date devient une date proposée dans le débrief.
- Le message de suivi est montré et validé avant d'être envoyé ; il tient en moins de 60 mots et ne décrit pas l'offre.
- Un "pas le bon interlocuteur" avec un nom crée une nouvelle ligne ; sans nom, c'est un ajustement à noter ("demander le nom et le numéro").
- Un refus n'est pas retravaillé : `Refus cold call`, prospect suivant. "Un refus est un refus."
- Pour une session, on compare au repère : 30 % de rendez-vous sur décrochés avec signal, et on regarde la liste avant le script si on est loin dessous.

## Exemples

- "Débriefe : elle a dit envoyez-moi un mail, j'ai insisté, elle a pris mercredi 11h mais elle n'a pas ouvert l'invitation" : résultat `Opportunité`, probabilité 45 %, l'objection et la réponse en trois temps, l'ajustement (verrouiller l'invitation pendant l'appel), prochain pas (mail de confirmation aujourd'hui, rappel J-1), message de suivi à valider.
- "Voici le transcript, il m'a renvoyé vers son associé" : `Contact non qualifié`, nouvelle ligne pour l'associé, mail d'intro à demander au prospect avec l'utilisateur en copie, ajustement s'il n'a pas demandé le numéro.
- "Bilan de ma session de ce matin, 22 appels" : décrochés, rendez-vous, rappels, refus, taux, les deux objections les plus entendues, un ajustement, et la liste des rappels datés à mettre en tête de la prochaine session.
