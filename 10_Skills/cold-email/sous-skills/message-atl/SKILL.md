---
name: message-atl
description: >
  Écrit pour un décideur de haut niveau (dirigeant, DG, fondateur, VP, directeur de fonction, membre du comité de direction) : angle, longueur, ce qu'il lit et ce qui le fait déléguer. Se déclenche sur : "email à un CEO", "écrire à un DG", "à un fondateur", "au DAF", "au directeur commercial", "au comité de direction", "décideur", "VP", "message ATL", "email dirigeant". Ne pas utiliser pour un manager, un responsable ou un opérationnel (voir message-btl), ni sans persona identifié (voir premier-contact).
---

Un dirigeant lit 2 à 3 phrases sur son téléphone et décide en 4 secondes : il répond si l'email touche un chiffre qu'il suit (chiffre d'affaires, marge, risque, position face à un concurrent), il délègue à un subordonné dès qu'il lit un détail opérationnel. Le persona ATL commande la longueur et l'angle ; ce sous-skill se lit avant `premier-contact` ou `relance` quand la cible est un décideur.

## Ressources

- `{SKILL_BASE}/ressources/registre-audience.md` : le registre d'un dirigeant très sollicité, la question de diagnostic, le CTA calme.
- `{SKILL_BASE}/ressources/brief-strategie.md` : le niveau de connaissance (un dirigeant est souvent expert du problème).
- `{SKILL_BASE}/ressources/frameworks-13.md` : Faites le calcul, Les responsabilités du rôle, La valeur d'abord.
- `{SKILL_BASE}/ressources/exemplaires.md` : les exemplaires B1 à B5, tous en ATL.
- `{SKILL_BASE}/ressources/templates-34.md` : #20 (nouveau dirigeant), #22 (calcul), #24 à #26 (série ROI).

## Méthode

1. **Confirmer le persona** : titre de la colonne `titre`, séniorité `seniorite`, et les personas ATL de `05_Departements/Go-to-Market/contexte.md`. En doute (un "directeur" d'une PME de 15 personnes est souvent opérationnel), demander à l'utilisateur.
2. **Choisir l'angle** parmi ce qu'un dirigeant suit : le chiffre d'affaires ou le pipeline, la marge ou un coût, un risque (juridique, technique, humain), la position face à un concurrent nommé, l'objectif de l'année, ce que voient ses actionnaires ou son conseil.
3. **Trouver le fait qui lui appartient** : un chiffre public de son entreprise (`enrichir_entreprise`), un signal (`detecter_signal`), une décision qu'il a annoncée. Le calcul (framework 1) part de ce chiffre.
4. **Écrire 2 à 3 phrases** : le fait, le résultat obtenu chez un pair de même taille, une question. Aucun détail de mise en œuvre, aucune fonctionnalité, aucun "gain de temps pour vos équipes".
5. **Poser la question en dirigeant** : une question de diagnostic ("combien de jours après la fin du chantier la marge est-elle connue ?") ou une question de résultat ("qu'est-ce que ça changerait sur l'objectif de l'année ?"). Pas de question qui demande du temps.
6. **Passer les relecteurs**, en insistant sur le relecteur prospect : un dirigeant de ce secteur répondrait-il ?

## Exécution

1. `enrichir_entreprise` (skill `enrichir-entreprise`) : chiffre d'affaires public, effectif, croissance, actualités, cas clients. Colonnes : `effectif`, `ca_public`, `croissance`, `actualite`.
2. `detecter_signal` (skill `detecter-signaux` (script `detecter_signal.py`)) : levée, acquisition, prise de poste, ouverture de site. Colonnes : `signal_type`, `signal_date`, `signal_detail`.
3. `enrichir_personne` (skill `enrichir-personne`) : ancienneté, parcours, prises de parole publiques. Colonnes : `anciennete`, `parcours`, `activite_recente`.
4. `trouver_email` (skill `trouver-email`) : l'email vérifié du dirigeant, pas celui de l'assistante ni une adresse générique. Colonnes : `email`, `email_statut`.
5. Rédaction (interne) : `persona` = ATL, `angle`, `objet`, `email_1`, puis `premier-contact` et `relance` pour la séquence.
6. `envoyer_sequence` (skill `envoyer-sequence`) après validation sur trois exemples.

Entrée et sortie : celles de `premier-contact`, avec `persona` = ATL et `seniorite` renseignée.

## Repères

| Repère | Valeur |
|---|---|
| Longueur | 2 à 3 phrases, 60 mots au plus |
| Cibler ATL quand | panier > 50 k€ par an, achat structurant, budget décidé au sommet, cycle long acceptable |
| Cibler les deux (multi-contact) quand | comité d'achat, budget et usage séparés, grand compte |
| Ce qu'il suit | chiffre d'affaires, marge, risque, concurrent, objectif annuel, regard du conseil |
| Ce qui le fait déléguer | un détail de flux de travail, une fonctionnalité, "vos équipes gagneront du temps" |
| Signal le plus fort | prise de poste entre 14 et 45 jours (8 à 12 % de réponse) |
| Angle le plus fort | le calcul sur un chiffre public de son entreprise (8 à 10 %) |

Les mots qui sonnent creux en français et qu'on remplace par un chiffre : "levier stratégique", "impact business", "avantage compétitif", "priorité du comité de direction". On dit "12 % de marge en plus sur les chantiers de moins de 50 k€", pas "un impact significatif sur la rentabilité".

## Template

```
Objet : {{chiffre ou sujet qui lui appartient}}

Bonjour {{prenom}},

{{Le fait public sur son entreprise, sourcé}} : {{la conséquence en chiffre d'affaires, marge ou risque}}.

{{Le dirigeant d'un pair de même taille}} {{résultat chiffré}} en {{delai}}.

{{Question de diagnostic ou de résultat}} ?
```

Exemple (fictif) :

```
Objet : 50 postes ouverts

Bonjour Marie,

50 postes ouverts sur votre page carrières, et un recrutement raté coûte environ 30 000 € : à 3 échecs sur 10, c'est 450 000 € sur l'année.

Le dirigeant de Novatech a ramené ce taux sous 10 % en un trimestre.

Qu'est-ce que ça changerait sur votre plan de recrutement 2027 ?
```

## Règles

1. 2 à 3 phrases. Un dirigeant qui doit faire défiler l'email ne le lit pas.
2. Le résultat, jamais le comment. Le "comment" est ce qu'il déléguera à quelqu'un d'autre.
3. Un chiffre qui lui appartient avant un chiffre qui vous appartient.
4. Une preuve de même taille et de même secteur, avec le titre du pair ("le dirigeant de", "la DAF de").
5. Pas de jargon de conseil, pas d'adjectif, pas de "stratégique".
6. Un CTA calme : une question de diagnostic ou de résultat, jamais "15 minutes cette semaine ?" en email 1.
7. Vouvoiement, registre tenu ; aucune chaleur non demandée, aucune remarque sur sa carrière.
8. Aucun tiret cadratin ; checklist §H d'`anti-ai-voice.md`.

## Exemples

- "Écris à des CEO de SaaS entre 5 et 20 M€" : persona ATL confirmé, angle chiffre d'affaires ou pipeline, framework Faites le calcul sur un chiffre public (effectif commercial, levée), 2 à 3 phrases, question de résultat, trois exemples montrés.
- "Le DAF n'a pas répondu, je passe par le DG ?" : lecture du comité d'achat dans `05_Departements/Go-to-Market/contexte.md`, email ATL au DG sur le risque ou la marge (pas sur le flux de travail du DAF), et question de routage vers le DAF en email 3.
- "Réécris cet email pour un directeur commercial plutôt qu'un manager" : suppression des détails opérationnels, passage de 4 à 3 phrases, angle objectif de l'année et pipeline, preuve avec le titre du pair, CTA de diagnostic.
