---
name: premier-contact
description: >
  Écrit le premier email d'une séquence de prospection B2B (email 1) à partir d'un signal, d'une preuve et d'un persona. Se déclenche sur : "écris un email", "email 1", "premier contact", "premier email", "cold email pour", "template outbound", "comment je démarre un email", "email de prospection". Ne pas utiliser pour les relances (voir relance), le réengagement d'anciens prospects (voir reengagement), un objet seul (voir objets), une ouverture personnalisée seule (voir personnalisation), ni pour l'infrastructure (voir infra-email).
---

L'email 1 apporte 80 % des réponses positives d'une séquence : c'est là que va l'effort. Il marche quand il part d'un fait vérifié sur le lecteur, nomme un problème qu'il a, prouve avec un chiffre, et demande une seule chose. Cible : 50 à 90 mots, 3 à 6 lignes, une question à la fin.

## Ressources

- `{SKILL_BASE}/ressources/principes-copywriting.md` : les règles par composant, à lire en premier.
- `{SKILL_BASE}/ressources/variations-email-1.md` : les 7 variantes d'email 1 avec exemples.
- `{SKILL_BASE}/ressources/templates-34.md` : les 23 templates de premier contact, par cas d'usage.
- `{SKILL_BASE}/ressources/frameworks-13.md` : les frameworks nommés et les 8 autorisés côté commercial.
- `{SKILL_BASE}/ressources/brief-strategie.md` : le brief à remplir avant d'écrire.
- `{SKILL_BASE}/ressources/relecteurs.md` : les quatre relectures avant de rendre.

## Méthode

1. **Lire `05_Departements/Go-to-Market/contexte.md`** : offre, preuves autorisées, ICP, personas ATL et BTL, signaux prioritaires, voix. Sans preuve chiffrée validée, demander une preuve ou écrire une preuve de mécanisme.
2. **Remplir le brief** (`brief-strategie.md`) : cible, persona, registre, niveau de connaissance, angle en une phrase, signal, preuve, CTA. Le montrer à l'utilisateur et continuer.
3. **Identifier le persona** : ATL (dirigeant, directeur) ou BTL (manager, opérationnel), d'après la colonne `seniorite` du CSV et les personas de `05_Departements/Go-to-Market/contexte.md`. Lire `message-atl` ou `message-btl` pour la longueur et l'angle.
4. **Trouver le déclencheur** : quel signal justifie d'écrire maintenant ? (`signal_type`, `signal_detail`, ou un fait de `enrichir_personne` / `enrichir_entreprise`). Sans signal, choisir la pertinence de repli (segment) et le dire.
5. **Choisir la variante et le framework** : selon le tableau de fin de `variations-email-1.md` et le tableau de choix de `frameworks-13.md`. Un email 1 sans signal prend la variante 7 (douleur du rôle) ou le framework "Les responsabilités du rôle".
6. **Écrire trois variantes** de l'email 1 sur le même angle (objet + corps), pour le test A/B/C. Fait avant adjectif, un seul CTA, aucune puce.
7. **Passer les relecteurs** (`relecteurs.md`) et la checklist §H d'`anti-ai-voice.md`. Corriger, repasser.
8. **Montrer trois emails remplis** sur trois prospects réels de la liste, attendre le "oui", puis remplir le CSV.

## Exécution

Séquence de collecte, chaque verbe seulement si sa colonne est vide :

1. `enrichir_personne` (skill `enrichir-personne`) : titre, séniorité, ancienneté, posts récents, headline. Colonnes : `titre`, `seniorite`, `linkedin_url`, `activite_recente`.
2. `detecter_signal` (skill `detecter-signaux` (script `detecter_signal.py`)) : levée, recrutement, changement de poste. Colonnes : `signal_type`, `signal_date`, `signal_detail`, `score_signal`, `fraicheur`.
3. `scraper_engagement` (skill `scraper-engagement`) si la campagne vise les personnes qui ont réagi à un post. Colonne : `signal_detail` (le post, le commentaire).
4. `enrichir_entreprise` (skill `enrichir-entreprise`) : effectif, secteur, site, description. Colonnes : `secteur`, `effectif`, `domaine`, `description_entreprise`.
5. `trouver_email` (skill `trouver-email`) : email vérifié. Colonnes : `email`, `email_statut`. Seules les lignes `valide` partent ; `catch-all` sur 10 % d'abord.
6. Rédaction (interne) : colonnes ajoutées `persona` (ATL ou BTL), `framework`, `objet`, `email_1`, `email_2`, `email_3`, `ouverture` (si personnalisée), `ouverture_source`.
7. `envoyer_sequence` (skill `envoyer-sequence`) : Lemlist pour l'email, canal LinkedIn selon `05_Departements/Go-to-Market/OUTILS.md`. Après validation explicite sur trois exemples.

Entrée : CSV aux colonnes normalisées (`prenom`, `nom`, `titre`, `seniorite`, `entreprise`, `domaine`, `linkedin_url`, `email`, `email_statut`, `secteur`, `effectif`, `signal_type`, `signal_date`, `signal_detail`, `score_icp`, `tier`). Sortie : le même CSV enrichi des colonnes de rédaction, écrit dans `05_Departements/Go-to-Market/Messages/messages_<sujet>_<YYYY-MM-DD>.csv`, et la séquence de référence (objets, corps, variantes) dans `sequence_<sujet>_<YYYY-MM-DD>.md` au même endroit.

## Repères

| Repère | Valeur |
|---|---|
| Longueur | 50 à 90 mots, 3 à 6 lignes ; ATL 2 à 3 phrases, BTL 3 à 4 |
| Objet | 2 à 5 mots, sur le sujet, pas sur l'offre |
| CTA | un seul, une question d'intérêt ou de ressource |
| Part des réponses | 80 % sur l'email 1 |
| Réponse attendue | 6 à 8 % à froid, 18 à 22 % sur signal, 35 à 40 % sur signaux empilés |
| Fraîcheur du signal | moins de 30 jours ; prise de poste entre 14 et 45 jours |
| Variantes à tester | 3 ou 4, 100 envois chacune avant de juger |
| Écart entre variantes | jusqu'à un facteur 13 |

## Template

```
Objet : {{sujet du signal, 2 à 5 mots}}

Bonjour {{prenom}},

{{Le fait vérifié, avec sa source}} : {{question d'observation}} ?

{{Ce que vous faites, en résultat}}. {{client_similaire}} {{résultat chiffré}} en {{delai}}.

{{CTA doux}} ?

{{Prénom de l'expéditeur}}
```

Exemple rempli (fictif) : voir `templates-34.md`, #1, et les exemplaires B1 à B5 de `exemplaires.md`.

## Règles

1. Un fait vérifié en première ligne, avec sa source. Aucun fait inventé : une colonne vide vaut mieux qu'un signal faux.
2. Une preuve chiffrée de `05_Departements/Go-to-Market/contexte.md`, jamais un adjectif ("significatif", "excellent").
3. Un seul CTA, une question, jamais une demande de 30 minutes dès l'email 1.
4. Vouvoiement, "Bonjour {{prenom}}", signature d'une ligne. Aucune formule de politesse creuse, aucune demande de permission d'écrire, aucune salutation anglophone.
5. Texte brut : pas de puce, de gras, d'image, de pièce jointe, plus d'un lien.
6. Aucun tiret cadratin ni demi-cadratin. Checklist §H d'`anti-ai-voice.md` sur chaque email.
7. Jamais d'envoi sans avoir montré trois emails remplis et obtenu un oui explicite.
8. Un prospect qui a déjà répondu ou qui est en `ne_plus_contacter` ne reçoit rien.

## Exemples

- "Écris-moi un cold email pour les DAF d'ETI qui recrutent un comptable" : brief en 8 lignes, persona ATL, framework Faites le calcul (variante 4), trois variantes d'objet et de corps, trois emails remplis sur trois DAF de la liste, attente du oui.
- "Fais un email 1 pour cette liste de 200 dirigeants d'agences" : vérification des colonnes vides, `detecter_signal` puis `trouver_email` sur les lignes manquantes avec annonce du coût, variante 1 avec repli de segment pour les lignes sans signal, CSV enrichi dans Messages/.
- "Mon email 1 ne marche pas, regarde" : passage des quatre relecteurs sur son texte, constats du plus fort au plus faible (pertinence, preuve, forme, voix), réécriture proposée sur le même angle.
