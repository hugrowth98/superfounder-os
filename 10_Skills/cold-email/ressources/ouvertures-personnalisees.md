# L'ouverture personnalisée : la liste est le message

Deux méthodes complémentaires. La première décrit la situation du prospect à partir de données publiques, si précisément qu'il se sent vu : la liste et le message se construisent ensemble. La seconde produit une ouverture de deux phrases par personne, cousue à un corps fixe validé une fois. Les deux reposent sur la même idée : un fait vérifié en première ligne, une preuve ou un signal cousu juste après, aucun adjectif.

## 1. La liste est le message

Si vous avez une bonne liste, vous avez un bon message. Le ciblage et le message ne sont pas deux étapes : vous construisez la liste sur des critères qui décrivent la situation réelle de l'acheteur, puis vous lui décrivez cette situation.

### Deux types de message

**Le segment qualifié par la douleur.** Deux à cinq critères publics identifient des prospects dans la même situation pénible qu'un client existant. Vous racontez comment vos clients ont traversé cette situation. Formule : le choix évident (ce que tout le monde fait), pourquoi vos clients ont fait le choix non évident, ce que ça leur a rapporté.

**La valeur sans permission (toujours supérieure).** Vous croisez 3 à 5 sources publiques pour produire un constat non évident, utile en soi. Test décisif : le destinataire paierait-il pour recevoir ce constat même s'il n'achète jamais ? Si oui, c'est de la valeur sans permission. Utilisez-la chaque fois que vous le pouvez.

### Le triangle de tension

La tension est une situation précise, prouvable par la donnée, bornée dans le temps, qui fait qu'il a besoin de vous maintenant. Un seul signal ne suffit pas : plusieurs données qui tirent dans des sens contraires.

- **Critère 1** : une caractéristique unique, prouvable par la donnée.
- **Critère 2** : une seconde caractéristique qui tire contre la première.
- **Amplificateur** : levée, croissance d'effectif ou de chiffre d'affaires, qui augmente la traction.
- **Donnée existentielle** : la mesure qui sépare les bons comptes des mauvais (une fourchette idéale).

Exemple : recrute trois commerciaux (critère 1) et n'a aucun outil de prospection détecté (critère 2, tire contre le premier), vient de lever (amplificateur), entre 20 et 80 salariés (donnée existentielle). Collecte : `scraper_offres_emploi`, `detecter_techno`, `detecter_signal`, `enrichir_entreprise`.

### L'architecture en 7 composants

1. **Une ouverture qu'il a ressentie** : un moment vécu physiquement, pas un fait. "Le vendredi soir où le devis part avec une faute dans le prix."
2. **Le lien avec ce qu'il fait déjà** : l'offre comme prolongement d'un comportement existant, pas comme rupture.
3. **Le constat à contre-courant** : "la plupart pensent X, en réalité Y". Il doit passer deux tests : le lecteur le reconnaît, et il ne l'avait jamais formulé.
4. **Une preuve légère** : une ligne, l'expérience du fondateur plutôt que les chiffres de l'entreprise.
5. **Le manque d'information** : assez pour la curiosité, jamais assez pour tout répondre.
6. **La qualification par disqualification** : un seuil qui exclut ceux qui ne conviennent pas. "Si vous faites moins de 50 devis par mois, ce n'est pas pour vous."
7. **Le CTA qui demande la vérité, pas du temps** : "Je suis proche, ou c'est différent chez {{entreprise}} ?" Jamais "vous avez 15 minutes ?".

### Les 11 règles

Ne jamais nommer votre produit dans la première étape. Écrire sur sa situation, pas sur votre solution. Cibler sur des événements, pas sur des titres. Utiliser les leviers de persuasion (réciprocité, preuve sociale, autorité, rareté) de façon systématique. Créer des manques d'information. Utiliser ses mots. Vendre contre l'habitude en place, pas contre les concurrents. Reconnaître qu'il existe plusieurs solutions. Un email parfait vaut mieux que dix moyens. La donnée bat la personnalisation de surface. Chiffrer le rendez-vous en euros.

### L'exemple de référence (valeur sans permission)

```
Bonjour Éric,

Votre pelle 20 tonnes n'a pas bougé depuis trois semaines d'après vos annonces de location.

Un permis de construire pour 40 logements vient d'être déposé rue des Acacias, à 2 km de votre dépôt.

Un chantier de cette taille demande environ six semaines de terrassement.

Au tarif de location public, c'est un chantier d'environ 45 000 €.

Voici le nom du conducteur de travaux, son email et son numéro. En espérant que ça serve.
```

Utile en soi, aucun produit mentionné, trois sources publiques croisées (annonces, permis de construire, tarifs), chiffré : le message est la démo.

### Le processus, de zéro à l'email

1. Comprendre vos meilleurs clients : dans quelle situation étaient-ils quand ils ont acheté ? (transcripts de vos appels de vente)
2. Extraire la tension : critère 1, critère 2, amplificateur, donnée existentielle.
3. Trouver les sources : ces critères sont-ils accessibles par la donnée ? (offres d'emploi, techno, pubs, levées, registres publics, avis)
4. Construire la liste sur la tension, pas sur la firmographie.
5. Écrire à l'envers : définir le message parfait, puis trouver la donnée qui le rend vrai.
6. Choisir segment qualifié ou valeur sans permission.
7. Appliquer les 7 composants.
8. Passer `relecteurs.md`.

### Anti-patterns

Les ouvertures "j'ai remarqué que". "Les entreprises comme la vôtre". "Vous avez 15 minutes ?". L'inventaire de fonctionnalités. La personnalisation de surface (ville, relations communes, un post cité sans lien avec le problème). Le ciblage horizontal (tous les DAF de France). La sur-séquence (2 à 3 messages maximum, chacun apportant une information nouvelle).

## 2. L'ouverture de deux phrases par personne

Une ouverture générée par destinataire, suivie d'un corps fixe validé une fois. Le corps porte les affirmations sur l'offre ; l'ouverture n'en porte aucune. C'est ce qui rend la personnalisation à volume compatible avec un contrôle sérieux.

```
Bonjour {{prenom}},

{{ouverture}}          <- deux phrases écrites pour cette personne

[corps fixe et validé, identique pour le segment]

[une demande]
```

### Définir l'ouverture

- Phrase 1 : la chose précise et vérifiée que cette personne fait.
- Phrase 2 : le problème juste à côté, ou une question de diagnostic sur son fonctionnement.
- 35 mots maximum pour les deux.
- Pas de salutation, pas de signature, pas de CTA dans l'ouverture.
- Jamais demander du temps dans l'ouverture.
- Jamais une question à laquelle l'email répond lui-même.

Pour une audience experte, la question de diagnostic bat l'affirmation : elle s'arrête avant d'expliquer à la personne son propre métier. Une forme par segment, tenue sur tout l'échantillon.

### Classer les ancrages

1. Quelque chose que la personne a publié sur son travail, relié au problème.
2. Quelque chose qu'elle a fait et qu'on peut vérifier : une intervention, un recrutement, un programme qu'elle pilote.
3. Un fait de segment, vrai du groupe : la spécialité, la ligne de produit, la fonction.

Le niveau 3 est de la segmentation, pas de la recherche personnelle. Étiquetez-le comme tel.

### Juger l'ancrage

Tout fait ne mérite pas une ligne personnelle. Forcer un lien est pire que ne pas en avoir. Le générateur rend un jugement avec la ligne :

```json
{"utilisable": true, "raison": "relie directement le rôle au problème", "ouverture": "<deux phrases>"}
```

Quand `utilisable` est faux, on écrit l'ouverture de segment validée et on marque la ligne comme repli. On rapporte à l'utilisateur la part d'ouvertures personnelles et la part de replis, sans exposer les données personnelles.

Rejetez un ancrage quand :
- il correspond à un mot-clé mais pas au problème de la campagne ;
- il oblige à deviner les priorités de la personne ;
- le lien demande un compliment ou une longue explication ;
- la ligne resterait vraie en remplaçant la personne et l'entreprise par un inconnu ;
- la source est vieille ou invérifiable.

Le réflexe qui aide à choisir : qu'est-ce qui rend cette personne fière ? Une décision, un résultat, une approche qui la distingue. Visez l'endroit où elle se sent reconnue pour la bonne raison, jamais flattée pour du creux.

### Fournir les faits du métier

Un modèle à qui l'on demande d'être précis sans lui donner les faits sera précis et faux. Donnez-lui une petite carte validée par segment :

```
Service client : onboarding, revues d'adoption, préparation des renouvellements
Opérations commerciales : routage des leads, passations, qualité des données
Contrôle de gestion : rapprochements, validations, préparation de clôture
```

Le générateur ne cite que le travail présent dans le segment sélectionné. Jamais de stéréotype pour combler un trou.

### Le contexte de marché

La phrase 1 parle de la personne. La phrase 2 peut utiliser un changement de marché s'il est actuel, vérifié et ressenti dans son travail. Test : peut-elle confirmer ou infirmer la conséquence à partir de sa propre semaine ? Sinon, c'est du commentaire de marché, hors de l'ouverture. L'événement s'énonce comme un fait ; la conséquence s'étiquette comme une hypothèse.

### Vérifier chaque ligne générée

Les ouvertures échouent surtout sur : une liste de trois pour le rythme ; "ce qui veut dire" en tête de phrase 2 ; un nom abstrait qui cache qui fait le travail ; une supposition sur le lecteur ; un compliment qui irait à n'importe qui ; une question qui demande du temps. Contrôlez la sortie fusionnée, pas seulement le template : une colonne de recherche qui échoue sur une ligne devient la ligne la plus visible de l'email.

Une ligne qui échoue est régénérée avec la raison et la ligne rejetée, deux ou trois fois. On ne corrige pas à la main des échecs répétés : le taux d'échec dit que le prompt ou l'entrée est mauvais.

### Adapter la profondeur à la capacité de relecture

Avant de construire un générateur, demandez comment l'utilisateur validera ce qui part. Quelqu'un qui doit signer chaque envoi ne peut pas relire 300 emails uniques. Dans ce cas, l'ouverture par segment est la bonne réponse : choisissez le fait de segment qui porte le plus de sens (rôle, spécialité, ligne de produit, cas d'usage), écrivez une ouverture validable par segment. L'ouverture par personne se réserve aux cas où la donnée est forte et où l'utilisateur accepte ce mode de validation. Tranchez avant de générer.

### Montrer chaque type avant l'envoi

On ne valide pas un placeholder. Montrez des aperçus groupés par type d'ancrage et par segment : l'ouverture, le fait vérifié dessous, la source, un exemple de repli où l'ancrage a été rejeté, le corps fixe qui suit. Montrer les ancrages rejetés aide l'utilisateur à faire confiance aux lignes qui passent.

## 3. Exemples d'ouvertures (fictifs)

Ancrage de niveau 1 (publié) :
> Vous écriviez la semaine dernière que vos commerciaux passent "plus de temps dans le CRM que chez les clients". Combien d'heures par semaine part dans la saisie chez Novapress ?

Ancrage de niveau 2 (fait vérifiable) :
> Vous pilotez le déploiement de l'agence de Nantes depuis mars, d'après votre profil. Une deuxième agence double en général le nombre de devis à relancer.

Ancrage de niveau 3 (segment, étiqueté repli) :
> Vous dirigez un cabinet d'expertise comptable de 30 personnes. La saison des bilans est en général le moment où les prospects entrants restent sans réponse.

Question de diagnostic (audience experte) :
> Vous suivez la marge par chantier chez Bâti-Ouest. Combien de jours après la fin du chantier la marge réelle est-elle connue ?

Repli quand la donnée est trop pauvre : laissez la colonne `ouverture` vide et utilisez l'ouverture de segment. Un blanc vaut mieux qu'une accroche qui brûle le prospect.

## 4. Scoring interne avant de retenir une ouverture

Partez de 10 et retirez : 3 si elle pourrait être envoyée à quelqu'un d'autre sans rien changer ; 2 si elle ne montre pas une recherche réelle sur cette personne ; 2 si elle tombe dans la flatterie ; 1 si elle n'ouvre pas naturellement sur le corps qui suit ; 1 si elle dépasse 35 mots. Gardez la meilleure ; à égalité, la plus courte.
