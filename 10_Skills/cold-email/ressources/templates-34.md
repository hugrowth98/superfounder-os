# Bibliothèque des 34 templates de cold email

23 templates de premier contact (1 à 26, la série ROI occupe les numéros 24 à 26), 4 de relance (27 à 30), 4 de réengagement (31 à 34). Chaque template garde le mécanisme d'origine (ce qui le fait répondre) avec des mots de B2B français : vouvoiement, 3 à 6 lignes, un seul CTA, un fait avant un adjectif.

Les variables entre doubles accolades correspondent aux colonnes du CSV (`prenom`, `entreprise`, `titre`, `secteur`, `signal_detail`) ou aux preuves de `05_Departements/Go-to-Market/contexte.md` (`client_similaire`, `resultat`, `delai`, `probleme`). `envoyer-sequence` les convertit en variables Lemlist. Tous les exemples chiffrés sont fictifs.

Lisez `principes-copywriting.md` avant de choisir. Un template est un squelette : la chair vient du signal et de la preuve. Passez chaque email produit par `relecteurs.md`.

## Les plus performants sur la source

| Template | Cas | Taux de réponse observé (source anglophone) |
|---|---|---|
| #4 Événement du calendrier | timing léger | plus de 10 % |
| #20 Nouveau dirigeant | 90 premiers jours | 8 à 12 % |
| #22 Faites le calcul | ROI | 8 à 10 % |
| #27 Relance en 7 points | relance | 6 à 8 % |
| #31 Question orientée non | réengagement | 10 à 15 % |

Ces taux viennent de campagnes anglophones. En France, comptez un tiers de moins tant que vous n'avez pas vos propres chiffres.

---

## Premier contact (1 à 26)

### #1 La question d'observation (le cadre par défaut)

Cas d'usage : vous avez un signal et une preuve. Le squelette de 80 % des emails 1.

```
Objet : {{sujet du signal}}

Bonjour {{prenom}},

{{Question d'observation sur sa situation}} ?

{{Ce que vous faites}}, {{preuve chiffrée chez client_similaire}}.

{{CTA doux}} ?
```

Exemple :

```
Objet : recrutement commercial

Bonjour Claire,

Trois offres de commerciaux ouvertes chez Novapress en un mois : la prospection va devoir suivre le rythme ?

On installe la machine de prospection des équipes qui recrutent. Lumatek a signé 14 rendez-vous par mois dès le deuxième mois.

Ça vaut le coup d'en parler ?
```

### #2 L'analogie

Cas d'usage : une offre abstraite ou complexe à rendre concrète. À réserver aux expéditeurs qui assument un ton léger.

```
Objet : {{image de l'analogie}}

Bonjour {{prenom}},

{{Situation du quotidien}} : {{le choix absurde qu'on y fait}}.

C'est ce qui arrive à {{profil}} quand {{choix actuel du prospect}}.

{{Ce que vous faites à la place}}. {{cta}} ?
```

Exemple : "Recruter un commercial junior pour lancer la prospection, c'est acheter un vélo d'appartement en janvier. Le premier mois on y croit, le troisième il sert de portemanteau. On a mis 6 PME en rythme de prospection sans recruter, avec le dirigeant et deux heures par semaine. Vous voulez voir la routine ?"

### #3 Le recrutement d'utilisateurs finaux

Cas d'usage : l'entreprise recrute un poste que votre offre équipe. Signal : `scraper_offres_emploi`.

```
Objet : votre poste de {{poste}}

Bonjour {{prenom}},

Vous recrutez un {{poste}} d'après votre page carrières.

Les entreprises de votre taille perdent {{n}} semaines sur {{probleme}} pendant sa montée en charge.

{{client_similaire}} a réduit ce délai de {{pourcentage}}.

Je vous montre comment ?
```

### #4 L'événement du calendrier

Cas d'usage : un événement que tout le monde suit cette semaine (Roland-Garros, Tour de France, rentrée, Coupe du monde). Léger, humain, rupture de schéma. Plus de 10 % de réponse sur la source, à tester en France. À envoyer pendant l'événement, jamais après.

```
Objet : roland-garros

Bonjour {{prenom}},

Question rapide : vous suivez le tournoi cette semaine ?

Autre question, plus sérieuse : comment vous gérez {{probleme}} en ce moment ?

{{Prénom de l'expéditeur}}
```

### #5 L'anniversaire de poste

Cas d'usage : ancienneté visible sur le profil (`enrichir_personne`). Le lecteur compare hier et aujourd'hui.

```
Objet : {{n}} ans

Bonjour {{prenom}},

{{n}} ans chez {{entreprise}} ce mois-ci.

Question : {{probleme}} est devenu plus simple ou plus compliqué depuis vos débuts ?
```

### #6 L'email visuel

Cas d'usage : le problème se voit (site, annonce, pub, page carrières). Une capture d'écran annotée, une image personnalisée (fonction native de Lemlist) ou une vidéo de 60 secondes. Preuve que vous avez regardé.

```
Objet : {{page ou support}} de {{entreprise}}

Bonjour {{prenom}},

J'ai regardé {{page}} de {{entreprise}} ce matin, capture ci-jointe : {{ce qui coince, en une phrase}}.

{{La conséquence chiffrée}}.

Vous voulez la version corrigée ?
```

Règle : l'image s'ajoute en relance (email 2), jamais dans l'email 1 d'un domaine jeune. Une pièce jointe dès le premier envoi pèse sur la délivrabilité.

### #7 L'invité de podcast

Cas d'usage : le prospect a parlé quelque part (seau 1 de `seaux-personnalisation.md`). Citez un point précis.

```
Objet : {{nom du podcast}}

Bonjour {{prenom}},

Écouté votre épisode sur {{sujet}} chez {{podcast}}.

Votre point sur {{insight précis}} m'est resté.

On applique exactement ce raisonnement à {{domaine}} avec {{client_similaire}}.

Ça vaut un échange ?
```

### #8 La bascule concurrent

Cas d'usage : le prospect utilise un concurrent ou un outil que vous remplacez (`detecter_techno`). Citez la source.

```
Objet : {{concurrent}}

Bonjour {{prenom}},

Vous utilisez {{concurrent}} d'après {{source}}.

La plupart des équipes que je rencontre butent sur {{limite connue}} passé {{seuil}}.

{{client_similaire}} a réglé ça en {{solution}}.

Vous voulez comparer ?
```

### #9 L'engagement sur un contenu

Cas d'usage : le prospect a publié ou commenté (`enrichir_personne`, `scraper_engagement`). Le passage précis, pas le compliment.

```
Objet : votre post

Bonjour {{prenom}},

Lu votre post sur {{sujet}}, surtout le passage sur {{point précis}}.

On travaille exactement là-dessus avec {{client_similaire}}.

Ouvert à comparer nos notes ?
```

### #10 La relation commune

Cas d'usage : une vraie recommandation, avec l'accord de la personne. Jamais une fausse recommandation : c'est le moyen le plus rapide de brûler un compte.

```
Objet : {{prenom_contact_commun}}

Bonjour {{prenom}},

{{Contact commun}} m'a suggéré de vous écrire.

{{Il ou Elle}} m'a dit que {{priorité}} était votre sujet du moment.

On vient de l'aider sur {{resultat}}.

Une intro de 15 minutes ?
```

### #11 L'événement sectoriel

Cas d'usage : le prospect a participé à un salon, une conférence (liste des participants, posts).

```
Objet : {{evenement}}

Bonjour {{prenom}},

Vous étiez à {{evenement}}.

La conférence sur {{sujet}} disait en substance {{point}}.

On aide des {{secteur}} à le mettre en place.

Ça a résonné pour {{entreprise}} ?
```

### #12 Le déclencheur techno

Cas d'usage : la stack du prospect appelle un complément (`detecter_techno`).

```
Objet : {{techno}}

Bonjour {{prenom}},

Vous tournez sur {{techno}}.

La plupart des équipes y ajoutent {{complement}} pour {{probleme}}.

{{client_similaire}} vient de le faire.

Je vous montre ce que ça change ?
```

### #13 Le style métrique

Cas d'usage : un signal de croissance ou d'activité, relié à un problème typique de ce stade.

```
Objet : {{metrique}} chez {{entreprise}}

Bonjour {{prenom}},

{{entreprise}} est en train de {{signal}}.

Les entreprises qui font ça voient en général {{probleme}} arriver dans les {{delai}}.

{{client_similaire}} a obtenu {{resultat}} en {{delai}}.

Vous voulez voir comment ils ont fait ?
```

### #14 L'agitation du problème

Cas d'usage : cible par fonction, une tâche manuelle connue. Marche surtout en BTL.

```
Objet : {{tache_manuelle}}

Bonjour {{prenom}},

Combien de temps votre équipe passe sur {{tache_manuelle}} chaque semaine ?

La plupart des {{titre}} que je rencontre disent que c'est leur plus gros gouffre.

{{client_similaire}} l'a réduit de {{pourcentage}}.

Ça vaut un coup d'œil ?
```

### #15 L'empilement de preuves

Cas d'usage : deux clients reconnaissables du même secteur. En prose, jamais en puces.

```
Objet : {{client_1}}, {{client_2}}

Bonjour {{prenom}},

On a aidé {{client_1}} à {{resultat_1}} et {{client_2}} à {{resultat_2}}.

Les deux avaient le même point de départ : {{probleme}}.

C'est sur votre radar chez {{entreprise}} ?
```

### #16 Signal et timing

Cas d'usage : un signal frais (moins de 30 jours) dont l'implication est connue.

```
Objet : timing

Bonjour {{prenom}},

Vu {{signal}} la semaine dernière.

En général, ça veut dire {{implication}} dans les {{delai}}.

On accompagne les entreprises à ce stade sur {{solution}}.

On en parle tant que c'est frais ?
```

### #17 L'approche par compte

Cas d'usage : vous avez déjà échangé avec quelqu'un dans l'entreprise (multi-contact). Seulement si l'échange a eu lieu.

```
Objet : {{initiative}}

Bonjour {{prenom}},

{{entreprise}} est en train de {{signal}}.

J'ai échangé avec {{prenom_collegue}} de l'équipe {{departement}} sur {{sujet}}.

{{Il ou Elle}} m'a dit que vous étiez la bonne personne pour {{initiative}}.

On se cale 15 minutes ?
```

### #18 Le dernier essai

Cas d'usage : fin de séquence, après deux emails sans réponse. Une sortie propre, pas de culpabilisation.

```
Objet : dernier essai

Bonjour {{prenom}},

Je vous ai écrit deux fois sur {{sujet}}.

Pas de réponse veut dire pas d'intérêt, et ça me va.

Avant de fermer le dossier : {{probleme}} est un sujet chez vous, ou pas du tout ?

Si non, j'arrête là.
```

### #19 La reconnexion d'un ancien client

Cas d'usage : un ancien utilisateur a changé d'entreprise (`detecter_signal`, changement de poste). Le meilleur signal qui existe.

```
Objet : de {{ancienne_entreprise}} à {{nouvelle_entreprise}}

Bonjour {{prenom}},

Vu que vous êtes passé de {{ancienne_entreprise}} à {{nouvelle_entreprise}}.

Chez {{ancienne_entreprise}}, vous utilisiez {{offre}} pour {{usage}}.

{{nouvelle_entreprise}} a quelque chose d'équivalent en place ?
```

### #20 Le nouveau dirigeant (90 premiers jours)

Cas d'usage : prise de poste entre 14 et 45 jours (le pic du signal). 8 à 12 % de réponse sur la source.

```
Objet : 90 premiers jours

Bonjour {{prenom}},

Félicitations pour le poste de {{titre}} chez {{entreprise}}.

La plupart des nouveaux {{titre}} que je rencontre attaquent par {{priorité courante}}.

Je peux vous partager ce que {{client_similaire}} a fait dans son premier trimestre.

Intéressé ?
```

### #21 L'offre d'étude de cas

Cas d'usage : une étude de cas publiée chez un client comparable. Le CTA demande la permission d'envoyer.

```
Objet : cas {{client_similaire}}

Bonjour {{prenom}},

On vient de publier comment {{client_similaire}} a obtenu {{resultat}}.

Leur point de départ, {{probleme}}, vous parlera peut-être.

Je vous l'envoie ?
```

### #22 Faites le calcul

Cas d'usage : un chiffre public du prospect multiplié par un coût connu. 8 à 10 % de réponse sur la source.

```
Objet : {{nombre}} leads potentiels

Bonjour {{prenom}},

Calcul rapide : {{entreprise}} a {{cible}} {{personnes ou comptes}} qui {{signal}}.

Si {{pourcentage}} convertissent, ça fait {{resultat}} opportunités.

{{client_similaire}} en a capté {{resultat}} avec le même calcul.

Vous voulez le détail ?
```

### #23 Douleur et autorité

Cas d'usage : une source d'autorité nommée (étude, régulateur, dirigeant connu) a dit quelque chose que le lecteur ressent. Jamais d'autorité anonyme ("les experts disent").

```
Objet : {{douleur}}

Bonjour {{prenom}},

{{Source nommée}} vient de publier que {{citation ou chiffre}}.

La plupart des {{titre}} que je rencontre sentent cette pression.

On accompagne {{client_similaire}} sur {{solution}}.

Pertinent pour vous ?
```

### #24 à #26 La série ROI

Cas d'usage : le prospect a un coût que vous savez chiffrer. Trois déclinaisons du même mécanisme, la règle de trois posée devant le lecteur.

**#24 Le coût d'une tâche**

```
Objet : {{montant}} par an

Bonjour {{prenom}},

Votre {{poste}} passe {{n}} heures par semaine sur {{tache}}, d'après votre offre de poste.

À {{taux}} de l'heure chargé, c'est {{montant}} par an.

{{client_similaire}} a divisé ce temps par {{n}}.

Je vous envoie le calcul ?
```

**#25 Le coût d'un outil ou d'une infrastructure**

```
Objet : {{outil}} à {{montant}}

Bonjour {{prenom}},

Vous payez {{outil}} environ {{montant}} par an d'après ses tarifs publics.

{{pourcentage}} de ce que vous payez sert à {{usage réel}}.

On a ramené {{client_similaire}} à {{montant_2}} pour le même résultat.

Ça mérite une comparaison ?
```

**#26 Le coût du temps de montée en charge**

```
Objet : {{n}} semaines

Bonjour {{prenom}},

Un nouveau {{poste}} met {{n}} semaines à être productif chez vous, d'après vos annonces.

Chaque semaine coûte {{montant}} en salaire sans production.

{{client_similaire}} est passé de {{n}} à {{m}} semaines.

Je vous montre ?
```

---

## Relance (27 à 30)

Une relance ajoute une information. Jamais "je reviens vers vous", jamais "avez-vous vu mon email". Le détail des règles est dans `../sous-skills/relance/SKILL.md`.

### #27 La relance en 7 points

Cas d'usage : la relance standard, 3 à 5 jours après l'email 1, même fil. 6 à 8 % de réponse sur la source.

Les 7 points : rappeler le sujet en un mot ; ne pas culpabiliser ; ajouter une information ou un angle neuf ; plus court que l'email 1 ; un CTA d'un autre style ; même fil ; 3 à 5 jours après.

```
Objet : RE: {{objet de l'email 1}}

Bonjour {{prenom}},

Au sujet de {{sujet}} : j'ai vu {{nouvelle information}} cette semaine, ça m'a fait penser à {{entreprise}}.

Toujours d'actualité ?
```

### #28 Le robot

Cas d'usage : humour, quand c'est votre voix et que la cible n'est pas trop formelle. Même fil.

```
Objet : RE: {{objet de l'email 1}}

Bonjour {{prenom}},

Ceci est une relance automatique parce que vous n'avez pas répondu à mon dernier mail.

Je plaisante, je suis un vrai humain.

Plus sérieusement : est-ce que {{sujet}} vous a parlé, ou pas du tout ?
```

### #29 Le contenu tiers

Cas d'usage : une ressource utile qui n'est pas la vôtre. Aucune vente dans cet email.

```
Objet : RE: {{objet de l'email 1}}

Bonjour {{prenom}},

Une ressource rapide : {{cet article, cet épisode}} sur {{sujet}} vaut 20 minutes.

{{lien}}

J'ai pensé à vous vu {{contexte}}. Rien à vendre ici.
```

### #30 LinkedIn et vidéo

Cas d'usage : une vidéo de 60 secondes qui montre votre recherche, coordonnée avec une invitation LinkedIn le même jour.

```
Objet : RE: {{objet de l'email 1}}

Bonjour {{prenom}},

J'ai enregistré 60 secondes pour vous : {{lien}}

Je montre ce que j'ai vu sur {{entreprise}} et pourquoi {{solution}} pourrait aider.

Ça vaut le visionnage ?
```

---

## Réengagement (31 à 34)

Pour des prospects contactés il y a des semaines ou des mois, hors séquence active. Le détail est dans `../sous-skills/reengagement/SKILL.md`.

### #31 La question orientée non

Cas d'usage : un prospect qui avait réservé un rendez-vous sans le convertir, ou un échange resté sans suite. Une question à laquelle il est facile de répondre non, et c'est ce qui fait répondre. 10 à 15 % sur la source.

```
Objet : question rapide

Bonjour {{prenom}},

Ce serait une mauvaise idée de reprendre le fil ?

On avait échangé il y a {{delai}} sur {{sujet}}.

Depuis, {{ce qui a changé}}.

Toujours pertinent ?
```

### #32 La réactivation d'une affaire perdue

Cas d'usage : affaire perdue depuis 3 à 6 mois. Nommez l'objection d'origine et ce qui a changé.

```
Objet : depuis notre échange

Bonjour {{prenom}},

Quand on s'est parlé en {{mois}}, vous m'aviez dit que {{objection}} bloquait.

Depuis, on a {{amelioration}}. {{client_similaire}} a vu {{resultat}} après le changement.

Ça mérite un second regard ?
```

### #33 Le prospect disparu

Cas d'usage : conversation interrompue depuis 2 à 3 semaines. Une sortie facile, sans pression.

```
Objet : on en est où ?

Bonjour {{prenom}},

On parlait de {{sujet}} en {{mois}}.

Puis silence de votre côté. Ça arrive, les priorités bougent.

C'est toujours sur votre liste, ou je ferme le dossier ?
```

### #34 Le renouvellement ou l'extension

Cas d'usage : client existant, échéance dans 30 à 60 jours.

```
Objet : {{date d'échéance}}

Bonjour {{prenom}},

Votre {{contrat}} arrive à échéance dans {{delai}}.

Avant de renouveler, on regarde {{amelioration}} ? La plupart des clients de votre taille ajoutent {{option}} à ce stade.

15 minutes cette semaine ?
```

---

## Tableau de timing du réengagement

| Situation | Attente | Template |
|---|---|---|
| Disparu en pleine conversation | 2 à 3 semaines | #33 |
| Affaire perdue | 3 à 6 mois | #32 |
| Démo ancienne sans suite | 2 à 4 mois | #31 |
| Renouvellement qui approche | 30 à 60 jours avant | #34 |
| Séquence terminée sans réponse | 3 mois | nouvelle séquence, autre angle |

Principe : toujours une information nouvelle ou une raison de reprendre contact. Jamais "je prends de vos nouvelles" sans rien apporter.
