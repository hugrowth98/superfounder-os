---
name: icebreaker-master
description: >
  Genere l'icebreaker parfait (la premiere ligne d'accroche) pour un message de prospection
  B2B outbound, email ou LinkedIn. Combine les meilleures pratiques de copywriting outbound
  (Voss, Braun, Moubeche). Gere 3 formats d'input : texte libre, fichier unique, CSV/XLSX
  batch (ex: export LinkedIn Sales Navigator, Apify). Se declenche sur "icebreaker", "premiere
  ligne", "opening line", "ice breaker", "hook prospection", "accroche". Pour rediger le
  message COMPLET (pas seulement la premiere ligne), utiliser `personnaliser-message`.
argument-hint: [colle les infos prospect OU chemin du fichier]
---

# Icebreaker Master - La premiere ligne qui fait repondre

**Objectif :** rediger UNE seule phrase (ou 2 tres courtes) a placer juste apres
`Hello {{firstName}},` et juste avant la proposition de valeur.

Le prospect doit se dire en la lisant : *"Cette personne a vraiment vu un point specifique qui
me rend different. Elle a l'air cool."*

Ce skill produit **uniquement l'accroche**. Pour le corps complet du message, enchainer avec
`personnaliser-message`, qui reprend l'icebreaker et deroule la proposition de valeur dans la
voix definie dans `05 Departements/Go-to-Market/contexte.md`.

Pour y arriver, se demander a chaque fois :
- **Qu'est-ce qui rend CE prospect fier ?** Quel fait concret, quelle decision, quel resultat,
  quelle approche qui le distingue ?
- **Comment a-t-il envie d'etre percu ?** Qu'est-ce qu'il valorise dans son travail, sa
  trajectoire, son entreprise ?
- Viser pile cet endroit-la, la ou le prospect se sent **reconnu pour la bonne raison**, pas
  flatte pour du creux.

**Langue & ton :** francais. **Tutoiement ou vouvoiement : lire la section 5 (Voix) de
`05 Departements/Go-to-Market/contexte.md`.** Si rien n'y est precise, vouvoiement par defaut. Respecter aussi les mots a
eviter listes dans cette section.

**Regle d'or du ton : ecrire comme a un ami sur WhatsApp.** Pas comme un mail commercial, pas
comme un post LinkedIn. Un message rapide, fluide, qu'on taperait au pouce entre deux trucs.
Si ca sonne "redige", c'est rate.

**Phrases courtes. Toujours.** Si une phrase depasse ~15 mots, la couper en deux. Deux phrases
courtes valent mieux qu'une phrase longue avec virgule au milieu.

**Un mot = un objectif.** Chaque mot doit servir. Si on peut l'enlever sans perdre le sens, on
l'enleve. Pas de "tout a fait", "bien sur", "en fait", "du coup", "par exemple".

**Output attendu :** UNE seule ligne finale, pas 3 versions, pas de scoring visible, pas
d'explication par defaut. Le travail de generation/scoring/selection se fait **en interne**,
silencieusement.

---

## Etape 1 - Detecter le format d'input

**Cas A - Texte libre** (un seul prospect, donnees collees dans le chat)
-> Generer 1 icebreaker.

**Cas B - Fichier unique** (path d'un JSON/MD/TXT avec les infos d'un prospect)
-> Lire le fichier, generer 1 icebreaker.

**Cas C - CSV/XLSX batch** (souvent un export LinkedIn Sales Navigator, Apify, PhantomBuster)
-> Lire le fichier, **inspecter les colonnes disponibles** (il y en a plus ou moins selon
l'export), generer un icebreaker par ligne, ecrire le resultat dans une nouvelle colonne
`icebreaker` et sauvegarder le fichier enrichi **dans le meme dossier que le fichier
d'entree** avec le suffixe `_icebreakers_YYYY-MM-DD.csv`.

Pour les CSV, utiliser Python (pandas) via Bash pour iterer proprement, pas des `sed`/`awk`.
Si `pandas` manque, l'installer d'abord (`pip install pandas`), sans demander a l'utilisateur.

---

## Etape 2 - Analyser la donnee disponible par prospect

Avant d'ecrire, identifier **UN element precis et "cool"** a exploiter. Ordre de priorite (du
plus fort au plus faible) :

1. **Contenu citable** (post LinkedIn recent, interview, podcast, article) -> meilleur materiau
2. **Signal d'entreprise specifique** (levee recente, lancement produit, milestone,
   recrutement d'un poste precis, expansion geo)
3. **Differenciateur de l'offre/approche** (modele de biz original, positionnement tranche,
   niche verticale)
4. **Parcours du prospect** (trajectoire atypique, passage d'une boite connue)
5. **Thematique metier partagee** (vision, conviction, pratique)

Si plusieurs elements -> choisir le **plus recent ET le plus specifique**. Un post de la
semaine > une levee d'il y a 2 ans > le secteur d'activite.

Si les donnees sont tres pauvres (juste prenom/nom/entreprise/titre) -> batir sur le **role +
fait concret sur l'entreprise**, jamais sur du flou type "j'ai vu votre profil".

---

## Etape 3 - Rediger (3 versions en interne, on ne sort que la meilleure)

Generer mentalement **3 variantes**, chacune avec un angle different :
- V1 : la plus directe, rebond frontal sur le materiau principal
- V2 : meme materiau, angle legerement different
- V3 : materiau alternatif (autre signal, autre aspect)

### Contraintes strictes (non-negociables)

- **Longueur max : 35 mots** (ideal 15-25)
- **Format : 1 phrase, ou 2 tres courtes maximum**
- **Ton : humain, naturel, credible, conversationnel** : se lit a voix haute sans accrocher
- **3 effets a produire simultanement :**
  1. Mettre en avant un fait **concret et specifique** lie au prospect ou son entreprise qui
     le rend fier
  2. Montrer qu'on **comprend ce qu'il fait** et pourquoi c'est interessant
  3. Creer de la **familiarite et de la sympathie**, sans tomber dans la flatterie
- **Hyper-specifique** : l'icebreaker ne doit PAS pouvoir etre envoye a quelqu'un d'autre sans
  modification
- **Nommage entreprise** : premiere lettre majuscule, reste minuscule (ex: `Skaizen`).
  Exception : 3-4 lettres tout en capitales d'origine (ex: `CGI`, `SNCF`, `BNP`). Supprimer
  suffixes juridiques (`SAS`, `SARL`, `SA`, `Group`, `Groupe`).
- **Toujours parler du prospect AVANT de parler de soi** : regle d'or

### Scoring interne (silencieux)

Noter chaque version /10, partir de 10 et retirer :
- **-3** si ca pourrait etre envoye a n'importe qui d'autre sans rien changer
- **-2** si ca ne montre pas une recherche reelle sur cette personne
- **-2** si ca tombe dans la flatterie creuse
- **-1** si ca ne cree pas d'ouverture naturelle vers la proposition de valeur qui suit
- **-1** si ca depasse 35 mots

Sortir uniquement la version avec le meilleur score. En cas d'egalite, preferer la plus
courte.

---

## Anti-patterns - INTERDICTION ABSOLUE

Ne jamais ecrire :

- "J'espere que ce message vous trouve en forme"
- "Je me permets de vous contacter"
- "En tant que [titre], vous savez probablement que..."
- "Felicitations pour votre [levee / nouveau poste]" sans aller plus loin
- "Je suis admiratif de votre carriere"
- Tout debut qui parle de soi avant le prospect ("Je suis [X] chez [Y]...")
- Adverbes creux : *vraiment, sincerement, honnetement, franchement* (sauf si c'est le style
  entier, ex: "Franchement chapeau pour...")
- Superlatifs vagues : *innovant, revolutionnaire, leader, incroyable, impressionnant*
- Mention du nombre de collaborateurs
- Flatterie generique non-justifiee par un fait
- Jargon commercial : *synergies, disruptif, scalable, accelerer, debloquer du potentiel*
- Phrases longues ou complexes (subordonnees imbriquees, relatives a rallonge)
- Tournures formelles "a l'ecrit" : *dont, lequel, laquelle, en effet, par ailleurs,
  toutefois, neanmoins, ainsi*

### Ponctuation et typographie - INTERDICTION STRICTE

Un icebreaker doit ressembler a un message WhatsApp, pas a un article :

- **Tiret cadratin** : JAMAIS. C'est le tell #1 d'un texte IA. Remplacer par virgule, point,
  ou "et".
- **Tiret demi-cadratin** : JAMAIS non plus. Meme raison.
- **Point-virgule** : personne n'ecrit avec des points-virgules sur WhatsApp.
- **Parentheses lourdes** qui coupent la phrase en deux.
- **Guillemets francais** autour du message lui-meme (seulement pour citer les mots du
  prospect).
- Autorises : virgules, points, points d'interrogation, points d'exclamation (avec
  parcimonie), deux-points simples. C'est tout.

Test : si tu dois utiliser un tiret pour faire tenir l'idee, c'est que la phrase est trop
chargee. Coupe en deux phrases courtes ou reformule avec une virgule.

---

## Style attendu - exemples calibres

**Quand on a un post citable (Strong Hook) :**
> "Dans votre post sur le burn-out des commerciaux, vous disiez qu'un SDR qui ne croit pas au
> produit c'est mort en 3 mois, exactement ce qu'on voit cote client."

**Quand on a un signal clair (Lite Hook) :**
> "Top votre levee de 4M chez Skaizen, surtout le choix de garder 100% de l'equipe tech en
> France, c'est rare dans votre vertical."

**Quand on a une thematique/approche :**
> "J'adore votre approche du growth applique au recrutement, ca me parle beaucoup."

**Quand les donnees sont pauvres (juste role + entreprise) :**
> "Top ce que vous faites avec Payfit sur la partie compliance automatisee, vrai
> differenciateur vs les concurrents US."

**Tonalites qui marchent :**
- "J'adore l'approche que vous avez sur..."
- "Franchement chapeau pour..."
- "Top ce que vous faites avec..."
- "Tres cool votre vision sur..."
- "Ce qui est fort dans votre demarche, c'est..."

Le compliment doit **toujours etre justifie par un element precis**, jamais suspendu dans le
vide.

---

## Principes cles

1. **Centre sur le prospect, jamais sur soi ni sur le produit** : l'icebreaker installe le
   terrain
2. **Champ de perception attribue a UNE personne** : si ca pourrait marcher pour 10 prospects
   identiques, c'est trop generique
3. **Eviter la flatterie** ("admiratif de votre carriere") : remplacer par du concret et
   sincere
4. **L'authenticite bat la sophistication** : ecrire comme on parle, pas comme on redige
5. **Pattern-interrupt** : ne pas demarrer comme tout le monde. Le cerveau du prospect filtre
   instantanement "Bonjour je me permets de..."
6. **Viser la fierte, pas l'ego** : reconnaitre pour la bonne raison, montrer qu'on a vu ce
   que le prospect veut qu'on voie

---

## Output final

**Mode texte libre (1 prospect) :**
Sortir uniquement la ligne finale, entre guillemets, sans commentaire. L'utilisateur peut
copier-coller directement.

**Mode CSV batch :**
1. Lire le CSV avec pandas, inspecter les colonnes pour comprendre la donnee disponible (le
   script s'adapte : parfois un post LinkedIn, parfois juste job title + company)
2. Pour chaque ligne, appliquer la logique etape 2 + 3
3. Ecrire la colonne `icebreaker` dans le CSV enrichi
4. Sauvegarder dans le meme dossier que l'input, suffixe `_icebreakers_YYYY-MM-DD.csv`
5. Signaler a l'utilisateur : nombre de lignes traitees, colonnes utilisees pour generer, path
   du fichier de sortie, 2-3 exemples d'icebreakers generes

**Si les donnees d'une ligne sont vraiment trop pauvres** pour un icebreaker specifique ->
laisser vide dans la colonne plutot que sortir un truc generique (mieux vaut un blanc qu'un
mauvais hook qui brule le prospect).
