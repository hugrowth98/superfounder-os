---
name: brief-avant-appel
description: >
  Produit en cinq minutes la fiche à avoir sous les yeux avant d'appeler une personne
  (qui, signal, entreprise, ouverture, les trois problèmes à citer, la preuve, les deux
  objections probables, la question d'après-créneau) ou prépare une session d'appels
  entière en triant la liste et en ajoutant l'ouverture à chaque ligne. Se déclenche sur :
  "prépare l'appel", "brief", "fiche prospect", "j'appelle X dans 10 minutes", "prépare ma
  session", "liste d'appel", "qui j'appelle en premier", "dans quel ordre". Ne pas utiliser
  pour : construire la liste elle-même (voir construire-liste), trouver le numéro seul
  (voir trouver-telephone), écrire le script générique d'un persona (voir script-appel),
  après l'appel (voir debrief-apres-appel).
---

# Le brief avant l'appel

"Le cold call, c'est 80 % de préparation et 20 % d'exécution", et la préparation, ce n'est pas un script : c'est savoir pourquoi on appelle cette personne, quels sont ses trois problèmes, quelle preuve citer et quel créneau proposer. Cinq minutes par fiche, ou une liste triée pour une session d'une heure, et "regardez votre liste avant de regarder votre script".

## Ressources

- `{SKILL_BASE}/ressources/scripts-par-signal.md` : l'ouverture selon le signal.
- `{SKILL_BASE}/ressources/objections-france.md` : les deux objections probables.
- `{SKILL_BASE}/ressources/sequence-multicanal.md` : où en est la personne dans la séquence.
- `05_Departements/Go-to-Market/contexte.md` sections 1 (preuves), 2 (barème), 3 (personas, problèmes), 4 (signaux), 7 (exclusions).
- `05_Departements/Go-to-Market/OUTILS.md` et `05_Departements/Go-to-Market/GARDE-FOUS.md` section 5 avant tout appel payant.

## Méthode

1. Identifier la personne : nom, entreprise, ou une ligne d'un CSV. Vérifier qu'elle n'est pas exclue (`05_Departements/Go-to-Market/contexte.md` section 7, `exclu`, `ne_plus_contacter`) et qu'elle n'a pas répondu par écrit sans être lue.
2. Compléter ce qui manque, dans cet ordre, en n'appelant un outil que si la colonne est vide : le profil (titre exact, ancienneté dans le poste, parcours, posts récents), l'entreprise (secteur, effectif, actualité, offres ouvertes), le signal (levée, prise de poste, recrutement, daté), l'engagement avec vous (réaction, commentaire, visite, invitation acceptée). Annoncer le coût avant, une seule fois pour la fiche.
3. Classer : persona ATL ou BTL, tier, signal prioritaire et sa fraîcheur. Si le score tombe sous le seuil du tier C, le dire et proposer de ne pas appeler.
4. Écrire l'ouverture (temps 1 et 2) à partir de `scripts-par-signal.md`, en disant ce que le signal implique, jamais le signal brut.
5. Écrire les trois problèmes à citer : ceux du persona dans `05_Departements/Go-to-Market/contexte.md`, reformulés avec ce qu'on a vu (un projet annoncé, une équipe qui grossit, une offre qui traîne depuis six semaines). Problème, cause, conséquence, en une ligne chacun.
6. Choisir la preuve la plus proche (même secteur, même taille, même problème) dans `05_Departements/Go-to-Market/contexte.md` section 1.
7. Anticiper les deux objections les plus probables pour ce profil, avec la réponse en une ligne.
8. Préparer l'après-créneau : la question de qualification en oui ou non, et la ligne CRM à remplir.
9. En mode session : trier la liste (rappels dus, puis tier A avec signal de moins de 30 jours, puis warm et engagés, puis le reste), garder 20 à 30 lignes pour une heure, ajouter à chaque ligne `ouverture`, `probleme_1`, `note_brief`, et proposer l'heure de la session (8h30 à 9h30 ou 17h30 à 18h30 pour des dirigeants).

## Exécution

| Étape | Verbe | Skill | Quand |
|---|---|---|---|
| Profil, parcours, posts récents | enrichir_personne | `enrichir-personne` | si `titre`, `seniorite` ou le parcours manquent |
| Secteur, effectif, actualité, offres | enrichir_entreprise | `enrichir-entreprise` | si `secteur`, `effectif` ou `domaine` manquent |
| Levée, prise de poste, recrutement sur cette entreprise | detecter_signal | `detecter-signaux` (script `detecter_signal.py`) | si `signal_type` est vide ou plus vieux que la fenêtre |
| A-t-il réagi à un de vos posts, accepté l'invitation | scraper_engagement | `scraper-engagement` | si un post ou une campagne LinkedIn récente existe |
| Numéro absent | trouver_telephone | `trouver-telephone` | seulement si `telephone` est vide, coût annoncé |

Entrée : un nom et une entreprise, ou un CSV aux colonnes normalisées. Sortie : `05_Departements/Go-to-Market/Messages/brief-appel_<Nom>_<YYYY-MM-DD>.md` pour une personne ; pour une session, le même CSV trié avec `ouverture`, `probleme_1`, `note_brief`, `ordre_appel`, enregistré sous `Listes-prospection/session-appels_<sujet>_<YYYY-MM-DD>.csv`. Une colonne déjà remplie n'est jamais recalculée.

## Repères

| Repère | Valeur |
|---|---|
| Temps de production d'une fiche | 5 minutes ; 2 en version express (ouverture, un problème, une objection) |
| Lignes pour une session d'une heure | 20 à 30 |
| Ordre d'appel | rappels dus, tier A et signal frais, warm et engagés, puis cold avec signal |
| Fraîcheur du signal pour appeler en premier | moins de 30 jours ; prise de poste entre J+14 et J+45 |
| Coût typique d'une fiche complète | 0 à 2 crédits selon ce qui manque ; le téléphone est le poste le plus cher |
| Ce qu'on ne prépare pas | des questions de découverte : il n'y en aura pas |

## Template

> **Qui.** [Prénom Nom], [titre] chez [entreprise] depuis [durée]. Persona [ATL ou BTL], tier [A], score [82].
> **Pourquoi maintenant.** [Signal, daté, et ce qu'il implique]. Engagement avec vous : [a accepté l'invitation le ..., a commenté ...].
> **L'entreprise en trois lignes.** [Secteur, effectif, actualité, ce qu'ils recrutent].
> **Ouverture.** "Bonjour [prénom], je vous appelle parce que [signal rendu légitime], et j'aimerais beaucoup qu'on se rencontre." Silence. "[Prénom Nom], je ne sais pas si vous me remettez."
> **Les trois problèmes à citer.** 1. [problème] à cause de [cause], ce qui fait que [conséquence]. 2. [...]. 3. [...].
> **La preuve.** "On accompagne déjà [client], [résultat chiffré]."
> **Objections probables.** "[Objection 1]" : [réponse en une ligne]. "[Objection 2]" : [réponse].
> **Créneau à proposer.** [Deux créneaux dans les 5 jours]. Après le oui : "est-ce qu'il y a une raison qui ferait que vous ne pourriez pas être là ?", puis "[question de qualification en oui ou non]".
> **Ligne CRM à préparer.** `Opportunité` si créneau, `Relance cold call` avec date si rappel, `Refus cold call` sinon.

## Règles

- Jamais inventer une donnée : une case vide reste vide, on l'annonce ("pas de signal daté trouvé, appel sur l'ICP seul").
- Le coût est annoncé avant tout appel payant, une fois pour la fiche, et rien n'est recalculé si la colonne existe.
- Un exclu ou une personne qui a répondu par écrit n'a pas de fiche : on le dit et on s'arrête.
- Le signal apparaît dans l'ouverture et nulle part ailleurs dans la fiche : la suite, ce sont des problèmes de dirigeant.
- Une fiche tient sur un écran ; on ne la lit pas pendant l'appel, on la regarde avant.
- Le numéro professionnel ou mobile pro seulement ; un numéro personnel trouvé n'est pas utilisé.

## Exemples

- "Prépare l'appel avec Marie Dupont de Transactis" : vérification des exclusions, profil et entreprise complétés si vides (coût annoncé), signal trouvé (prise de poste il y a 5 semaines), fiche en neuf lignes, lien vers le fichier.
- "J'appelle Paul dans 10 minutes, vite" : version express, trois lignes dans la conversation : l'ouverture, le problème le plus probable, l'objection la plus probable.
- "Prépare ma session de demain matin sur la liste des boîtes qui recrutent un SDR" : liste triée (rappels dus en tête), 25 lignes gardées, `ouverture` et `probleme_1` remplis pour chacune, créneau 8h30 à 9h30 proposé, CSV livré.
