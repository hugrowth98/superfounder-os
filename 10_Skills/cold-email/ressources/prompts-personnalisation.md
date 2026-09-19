# Prompts de personnalisation

Des prompts courts qui produisent une variable à insérer dans un email fixe. Vous les exécutez vous-même (Claude) sur chaque ligne du CSV, ou vous les collez dans une variable IA de Lemlist (`create_ai_variable_prompt`). Chaque prompt produit une sortie qui doit s'emboîter grammaticalement dans une phrase donnée : c'est ce qui garantit que l'email reste lisible sur 500 lignes.

Règles communes à tous les prompts : sortie en minuscules sauf noms propres, pas de point final, pas de mot de vente ni de jargon, pas de guillemets, et la sortie doit tenir dans la phrase cible. Entrée : `domaine` (le site de l'entreprise), à défaut une description de l'entreprise (`enrichir_entreprise`).

## 1. Identifier l'ICP du prospect

Utile quand vous vendez à des gens qui prospectent (agences, éditeurs, cabinets) : leur cible devient votre accroche.

```
À partir de {{domaine}} (à défaut {{description}}), trouve les 3 profils que cette entreprise prospecte le plus probablement.

Règles :
- uniquement des intitulés de poste, 3 maximum
- version courte (DG plutôt que directeur général, DAF plutôt que directeur administratif et financier)
- "et" avant le dernier
- pas de point final

Exemples : "des DG" ; "des DG, des DRH et des DAF"
```

Sortie type pour un éditeur de CRM : "des directeurs commerciaux, des responsables RevOps et des commerciaux".

## 2. Décrire l'entreprise en une ligne

```
Décris ce que fait l'entreprise en une phrase courte à partir de {{domaine}} (à défaut {{description}}).

Règles :
- sans citer le nom de l'entreprise ni sa cible
- 8 mots maximum
- ton neutre, minuscules
- la proposition de valeur principale du site

La sortie doit tenir dans : "Intéresser des prospects à [sortie] n'a rien de simple."
Ajoute entre parenthèses une précision sur la seconde moitié si elle aide.
```

Sortie type : "l'automatisation de la prospection (pour équipes commerciales B2B)".

## 3. Catégoriser le produit ou le service

```
Catégorise le type de produit ou service à partir de {{domaine}} (à défaut {{description}}).

Règles :
- 6 mots maximum
- singulier, neutre, minuscules
- précis, pas vague
- abréviations acceptées ("tech" pour "technologie")

La sortie doit tenir dans : "On travaille avec un [sortie] comparable."
```

Sortie type pour un outil de prise de rendez-vous : "logiciel de planification de rendez-vous".

## 4. Les trois problèmes de leur cible

```
Identifie les 3 problèmes principaux de la cible de cette entreprise à partir de {{domaine}} (à défaut {{description}}).

Règles :
- des problèmes reliés à un indicateur de résultat (chiffre d'affaires, délai, coût, churn)
- classés du plus gros au plus petit
- 10 mots maximum par problème
- minuscules, pas de point final, "et" avant le troisième
- pas de mot répété, pas de jargon

Format : [problème 1], [problème 2] et [problème 3]

La sortie doit tenir dans : "Ils décrochent 25 rendez-vous par mois avec des prospects qui peinent à [sortie]"
```

Sortie type pour un logiciel RH : "recruter vite, retenir les nouvelles recrues et tenir la conformité".

## 5. L'objet en deux mots

```
Écris un objet d'email de deux mots exactement à partir de {{domaine}} (à défaut {{description}}).

Règles :
- 2 mots, pas un de plus
- minuscules
- des mots du métier du destinataire
- aucun mot de vente, de promotion ou de spam
- l'objet doit enchaîner naturellement avec la première ligne de l'email
- but : ouvrir, puis répondre avec intérêt
```

Sortie type pour une plateforme d'analytics : "vos indicateurs".

## 6. Template : la référence client

Assemble les sorties 1 à 4 dans un email fixe.

```
Notre client {{client_similaire}} prospectait {{sortie 1 : ICP}}.

Ils butaient sur {{sortie 4 : problème 1}}, {{problème 2}} et {{problème 3}}.

Vu que vous vendez {{sortie 2 : description}}, la même approche pourrait marcher en y ajoutant {{ressource gratuite qui règle ces problèmes}}.

Je vous envoie la campagne qu'ils utilisent pour décrocher 35 rendez-vous par mois ?
```

## 7. Template : l'approche par entreprise semblable

```
Bonjour {{prenom}}, j'ai vu que vous vendez {{sortie 2 : description}}.

Un de nos clients prospecte {{sortie 1 : ICP}} pour un {{sortie 3 : produit comparable}}.

Il aide des entreprises qui peinent à {{sortie 4 : les trois problèmes}}.

{{CTA en rotation}} les emails qu'il utilise pour décrocher 25 rendez-vous par mois ?

{{signature}}
```

Le CTA en rotation (variantes Lemlist, une par envoi, sans variable à l'intérieur) : "Je vous montre", "Je vous partage", "Ça vous dirait de voir", "Vous voulez que je vous envoie", "Si vous avez 15 minutes, je vous montre".

Correspondance des variables :

| Variable | Vient de | Utilisée dans |
|---|---|---|
| `domaine` | CSV (`enrichir_entreprise`) | prompts 1 à 5 |
| `description` | CSV (`enrichir_entreprise`), repli | prompts 1 à 5 |
| `prenom` | CSV | templates 6 et 7 |
| sortie 1 (ICP) | prompt 1 | templates 6 et 7 |
| sortie 2 (description) | prompt 2 | template 7 |
| sortie 3 (produit comparable) | prompt 3 | template 7 |
| sortie 4 (trois problèmes) | prompt 4 | templates 6 et 7 |

## 8. La première ligne à partir d'un post (seau 1)

Le texte du post vient de la colonne `posts_recents` (`enrichir_personne --posts`, les 5 derniers posts séparés par ` || `) : on prend le plus récent relié au problème.

```
Voici le dernier post LinkedIn de {{prenom}} {{nom}} ({{entreprise}}) : {{texte du post}}.

Résume en une phrase l'argument principal du post.

Règles :
- 20 mots maximum
- aucun compliment générique
- cite une affirmation précise du post, avec ses mots entre guillemets si possible
- ton parlé, vouvoiement

Format : "Votre post sur [sujet], surtout [affirmation précise], m'a arrêté."
Si le post ne contient aucune affirmation reliée à {{probleme que vous résolvez}}, réponds exactement : INUTILISABLE
```

Le mot INUTILISABLE laisse la colonne vide : `ouvertures-personnalisees.md` explique le repli.

## 9. Le signal et sa conséquence (seau 6)

```
Signal : {{signal_type}} chez {{entreprise}}, le {{signal_date}} : {{signal_detail}}.
Offre : {{offre en une ligne, depuis contexte.md}}.

Écris deux phrases. Phrase 1 : le signal, tel quel, avec sa source ("d'après votre page carrières", "d'après le communiqué du 12 mars"). Phrase 2 : la conséquence probable de ce signal sur le travail du destinataire, formulée comme une hypothèse ("j'imagine que", "en général ça veut dire").

Règles : 35 mots maximum en tout, pas d'adjectif, aucune mention de l'offre, aucun chiffre qui ne vient pas du signal.
```

## 10. Le prompt maître de l'expéditeur

À remplir une fois depuis `05_Departements/Go-to-Market/contexte.md` et à mettre en tête de tout prompt de rédaction, pour que chaque variable produite respecte la même ligne.

```
{{Entreprise de l'expéditeur}} {{ce qu'elle fait, en une phrase, depuis contexte.md}}.

Cible : {{icp}}. Personas : {{persona_atl}} et {{persona_btl}}.
Preuves autorisées : {{liste des preuves de contexte.md, avec chiffres}}. Aucune autre.
Ton : {{voix de contexte.md}}. Vouvoiement. Pas de jargon, pas de superlatif, pas de vente forcée.

Chaque message : le problème résolu, ce qu'on fait différemment, un CTA doux et unique.
Interdits : tiret cadratin, formule de politesse d'ouverture creuse, demande de permission d'écrire, salutation anglophone, puces, gras, plus d'un CTA, un fait absent des preuves autorisées.
```

## 11. Vérifier chaque sortie

Une variable générée passe les mêmes contrôles qu'un email : `relecteurs.md` (relecteur recherche pour les faits, relecteur qualité pour la forme) et la checklist §H d'`anti-ai-voice.md`. Une sortie qui échoue est régénérée avec la raison de l'échec, deux ou trois fois au plus. Un taux d'échec élevé signifie que le prompt ou la donnée d'entrée est mauvais : corrigez le prompt, ne rafistolez pas les lignes une par une.

Vérifiez aussi le prompt lui-même : un mot interdit ou un anglicisme dans le prompt se retrouve dans des centaines de lignes.
