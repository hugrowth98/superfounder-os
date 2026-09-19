# Scorer un marché adressable

Lu par `qualifier-comptes` et `selectionner-comptes`. Un marché adressable (TAM) est la liste de toutes les entreprises qui pourraient acheter. Le scorer, c'est donner à chacune un nombre entre 0 et 100 à partir de ce qu'on observe, puis ranger en tiers pour décider qui on contacte cette semaine, qui on contacte ce trimestre, et qui on laisse. Le calcul est local, sans appel payant : il tourne sur des colonnes déjà présentes dans le CSV.

## Construire le modèle

1. Partez des trois couches et de leurs points par défaut (40, 20, 40) décrits dans `icp-3-couches.md`, avec les valeurs cibles de l'utilisateur dans la section 2 de `05_Departements/Go-to-Market/contexte.md`. Au plus une dizaine de critères en tout.
2. Pour chaque groupe, écrivez la règle de notation en trois niveaux : plein, partiel, zéro. Pas de demi-points, pas de règle à sept cas.
3. Fixez les seuils de tiers. Les seuils par défaut sont A à 75, B à 55, C à 35. Un utilisateur dont le marché est étroit descend les seuils ; un utilisateur noyé sous les tiers A les monte.
4. Ajoutez les disqualifiants : ils valent une exclusion immédiate, pas un malus. Un secteur exclu sort de la liste sans être noté.
5. Testez le modèle sur les 10 derniers clients signés : ils doivent sortir en A ou B. Sur 5 affaires perdues pour mauvais fit : elles doivent sortir en C ou D. Sinon, ajustez les pondérations avant de scorer la liste.

Un modèle qui tient sur une page est un modèle qu'on applique. Les équipes qui empilent visites du site, scores d'intention tiers et pondérations croisées finissent par ne plus rien scorer du tout.

## Avant de scorer

| Nettoyage | Pourquoi |
|---|---|
| Retirer les noms d'entreprise bidons ("test", "mon entreprise", "auto-entrepreneur", "freelance" seul) | ils faussent les tiers et gaspillent l'enrichissement |
| Retirer les franchises listées par agence quand la cible est le siège | dix lignes pour une seule décision |
| Signaler les effectifs aberrants (10 000 pour un cabinet local) | une erreur de source, à vérifier avant de noter |
| Dédoublonner par `domaine` | une entreprise scorée deux fois apparaît deux fois en tier A |
| Appliquer les disqualifiants | on ne paie pas `enrichir_entreprise` pour une ligne qu'on va exclure |

L'ordre complet des portes est dans `gates-qualification.md`.

## Noter une ligne

Pour chaque groupe, prenez la valeur de la colonne (`secteur`, `effectif`, `pays`, `ville`, `signal_type`, `signal_date`), comparez-la à `05_Departements/Go-to-Market/contexte.md`, attribuez plein, partiel ou zéro. Une donnée manquante vaut zéro, jamais un point négatif : le score d'une ligne incomplète est un plancher, pas une note définitive. Additionnez, écrivez `score_icp`, déduisez `tier`.

Exemple sur une ligne : `secteur = agence digitale` (adjacent, 7 sur 15), `effectif = 24` (exact, 10 sur 10), `pays = France` (8 sur 8), CA inconnu (0 sur 7), techno non détectée (6 + 8 = 14 sur 20), `signal_type = recrutement` daté de 12 jours et signal n°1 (15 sur 15), rien d'autre (0 sur 25) : `score_icp = 54`, tier C à un point du B. Après `detecter_techno` (HubSpot présent : 12 au lieu de 6) et `enrichir_entreprise` (CA dans la cible : 7), la même ligne monte à 67, tier B : c'est pour ça qu'on enrichit les C proches du seuil avant de les écarter.

## Prioriser dans un tier

Deux comptes au même score ne se valent pas. Trois départageurs, dans cet ordre :

1. Le signal le plus récent (`signal_date`) passe devant.
2. Le décideur est identifié et joignable (une ligne personne avec `linkedin_url` ou `email` renseigné) passe devant un compte sans contact.
3. Le décideur est actif sur LinkedIn (a publié dans les 30 jours) passe devant un profil silencieux.

## Croiser le tier du compte et la séniorité du contact

| Tier du compte | Contact ATL (C-level, VP, directeur) | Contact BTL (manager, opérationnel) |
|---|---|---|
| A | recherche approfondie, angle sur mesure, plusieurs canaux, 2 à 4 contacts | message personnalisé, demande de mise en relation vers le décideur |
| B | personnalisation par segment, offre en avant | personnalisation par segment |
| C | nurturing, 1 contact, pas de téléphone | nurturing, ou rien |
| D | exclu | exclu |

Le tier du compte décide de l'effort, la séniorité du contact décide de l'angle.

## Livrer

- `qualifier-liste_<sujet>_<date>.csv` avec toutes les lignes, `score_icp`, `tier`, `exclu`, `raison_exclusion`, plus une copie `..._exclus.csv` pour lecture. Les lignes gardées sont celles où `exclu = non`.
- Le rapport donne la répartition par tier, les trois raisons d'exclusion les plus fréquentes, et cinq lignes tirées au hasard dans le tier A avec le détail de leur score.
- Avant de lancer un enrichissement ou une séquence sur la liste scorée, montrez ces cinq lignes et attendez le oui.
- Quand de nouvelles données arrivent (enrichissement, signal), rescorez tout le fichier : un score n'est jamais figé.

## Ce que le score ne fait pas

Le score dit à qui vous consacrez votre temps cette semaine. Le moment de contacter vient de `score_signal` et `fraicheur`, produits par `detecter-signaux`. Le contenu du message vient de `cold-email`.
