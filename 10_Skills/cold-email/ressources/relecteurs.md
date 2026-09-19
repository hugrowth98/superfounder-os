# Les quatre relecteurs, puis le contrôle final

Avant de rendre un email, une séquence ou une ouverture générée, vous (Claude) vous appliquez ces quatre relectures dans l'ordre, vous corrigez, puis vous passez le contrôle final. Vous ne rendez le texte qu'une fois tout au vert. Vous gardez un seul brouillon canonique du début à la fin : les relecteurs annotent, ils ne réécrivent pas chacun leur version.

Chaque relecteur rend au plus cinq constats. Un constat tient en une phrase : l'endroit, le problème, la correction proposée. On cite au plus douze mots du brouillon. On ne recopie pas le brouillon dans la sortie du relecteur. Le texte final apparaît une seule fois, à la fin.

Quand aucune correction n'est nécessaire, le relecteur rend `ok`.

## Relecteur 1 : le prospect (est-ce que ça me parle ?)

Vous lisez le brouillon dans la peau du destinataire, sur son téléphone, entre deux réunions.

1. Les deux premières lignes disent le sujet et pourquoi ça le concerne.
2. Le problème est reconnaissable sans information interne.
3. Le résultat est concret et compréhensible en une lecture.
4. Le CTA demande une seule action, à faible effort.
5. Le langage colle au registre et au niveau de lecture du brief.
6. Face à un expert, le texte montre qu'il connaît le travail sans le lui réexpliquer.
7. L'ouverture personnalisée repose sur un ancrage vérifié, ou sur le repli de segment validé.

Le test qui résume le relecteur : remplacez le destinataire et son entreprise par un inconnu. Si l'email reste vrai, il n'est pas personnalisé. Puis : "Vous répondriez à cet email ?" Si la réponse est non, dites pourquoi en une phrase.

## Relecteur 2 : la recherche (les faits sont-ils vrais et sourcés ?)

Vous relisez chaque affirmation factuelle ou causale du brouillon.

1. Chaque entreprise, personne, rôle, événement, produit et preuve renvoie à une donnée fournie (CSV, `05_Departements/Go-to-Market/contexte.md`, résultat d'un verbe).
2. Les dates et les rôles actuels sont assez récents pour la campagne (un poste vérifié il y a plus de 60 jours se revérifie).
3. Les déductions sont écrites comme des possibilités, pas comme des faits.
4. Une preuve client garde exactement le périmètre et le sens validés.
5. Aucune source n'est étirée vers une affirmation plus forte qu'elle ne le dit.
6. Aucune capacité ne devient un bénéfice, une réduction, une amélioration ou une cause non fournis.
7. Chaque ancrage personnalisé soutient directement la première ligne et date de moins de 90 jours.
8. Chaque tendance de marché est ressentie dans le travail du destinataire ; sinon c'est du commentaire.
9. Chaque mention "ci-joint", "en lien", "envoyé", "prévu le" correspond à une pièce présente ou à un fait de livraison validé.

Écrire "peut-être" devant un résultat non prouvé ne le rend pas sûr : supprimez le résultat ou demandez la preuve. Un ancrage qui correspond à un mot-clé mais pas au problème de la campagne est rejeté au profit du repli de segment. Quand seul le nom d'une ressource est validé, toute description inventée de son contenu est rejetée.

Quand un fait requis n'a pas de preuve, le relecteur rend `contexte_insuffisant` avec le fait manquant, et l'email ne part pas.

## Relecteur 3 : la qualité (la checklist)

Vous vérifiez la forme contre `regles-copy.md`.

1. La séquence compte deux ou trois emails (quatre au plus), de 50 à 90 mots chacun.
2. Les phrases restent sous 20 mots, l'objet entre 2 et 5 mots.
3. Chaque email a un CTA, et chaque email apporte un angle nouveau.
4. Le langage est simple et précis, sans fausse familiarité ni fausse urgence.
5. Aucun tiret cadratin ni demi-cadratin ; aucun suivi d'ouverture suggéré.
6. Aucun tic d'écriture machine : passez la checklist §H de `01_About-Me/anti-ai-voice.md` (workspace parent). Sans ce fichier, vérifiez au minimum : pas de "ce n'est pas X, c'est Y", pas de liste de trois pour le rythme, pas de question à laquelle le texte répond, pas de chute en aphorisme, pas de candeur mise en scène ("Honnêtement"), pas de demande de permission d'écrire, pas de formule de politesse d'ouverture creuse, pas de salutation anglophone.
7. Les variantes en rotation, si elles sont demandées, gardent les phrases de preuve identiques et ne contiennent aucune variable.
8. Vouvoiement partout ; "Bonjour {{prenom}}" ou le prénom seul en ouverture ; signature d'une ligne.
9. Texte brut : pas de puce, de gras, d'image ni de pièce jointe dans l'email 1.

Un email plus long passe seulement si l'utilisateur l'a demandé et si chaque preuve est sourcée.

## Relecteur 4 : la voix (est-ce que ça sonne comme l'expéditeur ?)

Vous relisez contre la section voix de `05_Departements/Go-to-Market/contexte.md` et, s'il existe, `02_Contexte/Tone-and-Voice.md` du workspace parent.

1. Le ton, le registre, le niveau de formalité, le vocabulaire et le point de vue correspondent au brief et à la voix définie.
2. L'offre, l'audience et le positionnement demandés sont présents.
3. Les mots, affirmations et procédés interdits par `05_Departements/Go-to-Market/contexte.md` sont absents.
4. Le CTA et l'étape suivante promise correspondent au processus de vente de l'utilisateur (un lien d'agenda seulement s'il en a un, une démo seulement s'il en fait).
5. Aucune consigne de l'utilisateur n'a été remplacée en silence par une préférence générale de copy.
6. Tout désaccord noté dans le brief (section "Désaccord") est visible et ne change pas la personne ni le problème visés en douce.
7. La profondeur de personnalisation correspond à ce que l'utilisateur peut relire et valider.

Lisez l'email à voix haute dans la voix de l'expéditeur. Si une phrase sonne "rédigée", elle se reformule comme il la dirait. Si le brief de voix manque ou se contredit, le relecteur rend `contexte_insuffisant` et demande deux ou trois exemples de messages de l'utilisateur avant de continuer.

## L'ordre des corrections

Corrigez dans cet ordre : prospect, recherche, qualité, voix. Un problème de pertinence (relecteur 1) se règle avant un problème de forme (relecteur 3). Une correction de voix (relecteur 4) ne change jamais un fait (relecteur 2).

## Le contrôle final

À lancer une fois les quatre relectures coordonnées et le brouillon corrigé.

- Le contexte requis est présent (`05_Departements/Go-to-Market/contexte.md` lu, preuves listées, persona identifié).
- Le brief (`brief-strategie.md`) donne la cible, le persona, le registre, le niveau de connaissance, l'angle, la profondeur de personnalisation et les désaccords.
- Les relectures ont eu lieu dans l'ordre prospect, recherche, qualité, voix.
- Objets entre 2 et 5 mots ; deux à trois emails ; 50 à 90 mots ; phrases sous 20 mots ; un CTA par email.
- Chaque affirmation a une source ; chaque bénéfice figure dans les preuves validées.
- Chaque ouverture personnalisée a un ancrage vérifié ou un repli validé.
- Aucune ressource offerte n'a de contenu inventé ; aucune pièce "jointe" n'est absente.
- Aucun tiret cadratin ; aucun tic machine non résolu ; aucun suivi d'ouverture.
- Les variantes en rotation gardent les phrases de preuve identiques.
- Le texte final apparaît une fois.
- Le rapport dit ce qui a été vérifié.

Si le contrôle échoue : une réparation, puis un dernier contrôle. Si le second échoue, rendez `relecture_humaine_requise` avec la liste des blocages. Pas de troisième tentative en silence.

## Ce que vous rendez à l'utilisateur

1. Le brief de stratégie (court).
2. Le statut : `complet`, `contexte_insuffisant` ou `relecture_humaine_requise`.
3. Le résumé des quatre relectures et du contrôle final, en quelques lignes.
4. Les objets et les emails finaux, une fois.
5. Le registre des faits (chaque affirmation et sa source) quand l'email contient des faits.
6. La couverture de personnalisation (part d'ouvertures personnelles, part de replis) quand les ouvertures varient.

Puis trois exemples complets sur trois prospects réels de la liste, et l'attente du "oui" avant `envoyer_sequence`.
