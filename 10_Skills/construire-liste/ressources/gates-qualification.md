# Les portes de qualification

Lu par `qualifier-comptes` et par le master pour la chaîne complète. Une liste passe huit portes dans l'ordre. Chaque porte retire des lignes (`exclu = oui`, `raison_exclusion` renseignée) ou complète des colonnes. Les lignes exclues restent dans le fichier, marquées, pour que l'utilisateur puisse vérifier. L'ordre compte : les portes gratuites et brutales passent avant les portes qui demandent du jugement, et tout passe avant le moindre enrichissement payant.

| Porte | Ce qu'elle regarde | Colonnes lues | Sortie |
|---|---|---|---|
| 0. Dédoublonnage et exclusions fixes | doublons dans le fichier, entreprises et domaines interdits par `05_Departements/Go-to-Market/contexte.md`, clients et affaires en cours du CRM | `linkedin_url`, `email`, `domaine`, `entreprise` | `exclu`, `raison_exclusion = doublon` ou `= exclusion fixe` ou `= deja client` |
| 1. Titre | le poste correspond-il à un persona | `titre`, `effectif` | `seniorite` renseignée ; `raison_exclusion = titre hors persona` |
| 2. Taille | l'effectif est-il dans les bornes dures | `effectif` | `raison_exclusion = effectif hors bornes` |
| 3. Secteur | le secteur est-il exclu | `secteur` | `raison_exclusion = secteur exclu` |
| 4. B2C | l'entreprise vend-elle aux particuliers | `secteur`, `entreprise`, `titre`, description si présente | `raison_exclusion = B2C` |
| 5. Concurrent | l'entreprise vend-elle la même chose que l'utilisateur | mêmes colonnes | `raison_exclusion = concurrent (famille)` |
| 6. Score ICP | la note sur 100 (`icp-3-couches.md`) | toutes les colonnes de fit et de signal | `score_icp` ; `raison_exclusion = score ICP < seuil D` |
| 7. Tier | le rang final | `score_icp` | `tier` = A, B ou C |

Une ligne exclue à une porte ne passe pas les suivantes. Une donnée manquante ne fait jamais exclure : elle laisse passer et se signale dans le rapport, pour enrichir ensuite les lignes qui en valent la peine.

## Porte 0 : dédoublonnage et exclusions fixes

Règles dans `regles-dedup.md`. Les exclusions fixes viennent de la section 7 de `05_Departements/Go-to-Market/contexte.md` : clients actuels et passés à ne jamais contacter, partenaires et apporteurs d'affaires, listes ou fichiers à croiser, zones exclues. Le croisement CRM se fait ici si HubSpot est branché : un client actuel ou une affaire ouverte sort avant tout le reste.

## Porte 1 : titre

Le poste actuel dans l'entreprise actuelle prime sur l'accroche du profil. Les vrais dirigeants écrivent "CEO" dans leur poste ; ceux qui ne l'écrivent que dans l'accroche sont le plus souvent des indépendants. Quand la source donne les deux, `titre` reçoit le poste actuel, et l'accroche ne sert qu'à départager.

Ordre de lecture, le premier qui matche gagne :

1. Stagiaire, alternant, intern, apprenti, étudiant : `seniorite = stagiaire`, exclu.
2. Freelance, indépendant, auto-entrepreneur, portage, fractional, à mon compte, en transition, à la recherche, open to work : `seniorite = independant`, exclu sauf si un persona de `05_Departements/Go-to-Market/contexte.md` vise les indépendants.
3. Consultant, coach, formateur, expert, conférencier, auteur, avocat, expert-comptable, thérapeute dans le poste actuel : `seniorite = independant`, même règle. Ces mots dans le poste sont un signal plus fort que "CEO" dans l'accroche.
4. Titres d'un persona ATL de `05_Departements/Go-to-Market/contexte.md` (CEO, DG, fondateur, président, gérant, directeur de fonction, VP, head of) : `seniorite = c-level`, `vp` ou `directeur`. Si `effectif = 1`, reclasser en `independant`. "Chef de projet", "chef de produit", "chef de secteur", "chef de rayon" ne sont pas des dirigeants ; "chef d'entreprise" l'est. "Futur entrepreneur", "leadership", "en devenir" à côté d'un titre de dirigeant annulent le titre.
5. Titres d'un persona BTL (responsable, manager, chef de projet, chargé de, business developer) : `seniorite = manager` ou `operationnel`. Un "responsable" dans le poste actuel reste manager même si l'accroche dit "directeur".
6. Développeur, designer, analyste, assistant, coordinateur, ingénieur sans mention de direction : `seniorite = operationnel`, exclu sauf persona dédié.
7. Rien ne matche : `seniorite` vide, exclu avec `raison_exclusion = titre hors persona`, et la ligne apparaît dans l'échantillon du rapport pour que l'utilisateur tranche.

Titres en français et en anglais, féminins compris : "Directrice commerciale" vaut "Directeur commercial", "Fondatrice" vaut "Fondateur". Les listes par fonction sont dans `personas-comite-achat.md`.

## Porte 2 : taille

`effectif` dans les tailles exclues de la section 2 de `05_Departements/Go-to-Market/contexte.md` (ligne "Tailles exclues, autres") : exclu. Entre les bornes mais hors de la valeur cible : la ligne passe, le score s'en charge (adjacent ou zéro). `effectif` vide : la ligne passe, marquée "effectif à enrichir" dans le rapport. Un effectif LinkedIn est une fourchette déclarée, souvent gonflée pour les petites structures : sur un tier A, `enrichir_entreprise` le vérifie.

## Porte 3 : secteur

`secteur` dans les secteurs exclus de la section 2 de `05_Departements/Go-to-Market/contexte.md` : exclu. Les libellés de secteur varient d'une source à l'autre ("Logiciels informatiques", "Software Development", "SaaS") : comparez au sens, pas au mot exact. Secteur vide : la ligne passe.

## Porte 4 : B2C

Une entreprise est B2C quand elle vend principalement à des particuliers. La question à se poser : qui paie ? Pas qui est servi au bout de la chaîne.

Premier passage par mots-clés, dans `entreprise`, `secteur`, `titre` et toute colonne descriptive. Liste de départ, complétée par les mots propres au marché de l'utilisateur écrits en section 8 de `05_Departements/Go-to-Market/contexte.md` :

```
particuliers, grand public, boutique, e-shop, e-commerce, retail, magasin, franchise,
restaurant, bar, traiteur, hôtel, camping, voyage, tourisme,
coiffure, beauté, esthétique, cosmétique, mode, bijouterie, prêt-à-porter,
salle de sport, fitness, yoga, bien-être, nutrition,
coaching de vie, développement personnel, thérapie, sophrologie, coaching parental,
immobilier résidentiel, auto-école, garde d'enfants, animalerie, jeux vidéo, presse grand public
```

Second passage, au jugement, sur les lignes qui ont matché ou qui restent ambiguës :

| Cas | Verdict |
|---|---|
| Un logiciel qui vend aux restaurants, aux coiffeurs, aux salles de sport | B2B, il vend à des entreprises |
| Une plateforme de formation pour les entreprises | B2B ; pour les particuliers : B2C |
| Une marque qui vend via des entreprises (fintech distribuée par des banques) | B2B |
| Une agence marketing dont les clients sont des marques B2C | B2B, elle vend à des entreprises |
| Un coach de dirigeants, un coach d'équipes | B2B ; coach de vie, parental, sportif pour particuliers : B2C |
| Un restaurant, un commerce, un cabinet médical | B2C, sauf si l'utilisateur les vise (cible locale : la porte est désactivée quand la ligne B2C de la section 2 de `05_Departements/Go-to-Market/contexte.md` dit non) |

En cas de doute franc, la ligne passe. Une exclusion doit être nette.

## Porte 5 : concurrent

Les concurrents sont nommés dans la section 2 de `05_Departements/Go-to-Market/contexte.md` (ligne "Concurrents"), par nom ou par famille ; les mots-clés propres au marché sont en section 8. Exemple pour un coach en prospection : agence de prospection ou de lead gen, SDR externalisé, coach ou formateur commercial, agence qui vend du conseil ou du build IA aux PME.

Ne sont pas concurrents : un produit logiciel (même IA), une agence marketing, SEO, contenu ou branding hors prospection, un cabinet de conseil sur un autre sujet (RH, finance, juridique, IT), un freelance technique sans positionnement commercial, et toute entreprise cliente potentielle. Une agence IA vend du service sur mesure ; un éditeur d'outil IA vend un produit. Le premier est concurrent, le second est un prospect.

Sortie : `exclu = oui`, `raison_exclusion = concurrent (nom de la famille)`. Si l'utilisateur veut garder les concurrents pour une liste de partenaires, ils restent dans le fichier avec cette raison, faciles à filtrer.

## Porte 6 : score ICP

Méthode dans `scoring-tam.md`, pondérations et seuils dans `05_Departements/Go-to-Market/contexte.md`. `score_icp` sous le seuil D : `exclu = oui`, `raison_exclusion = score ICP < 35` (avec le seuil réel de `05_Departements/Go-to-Market/contexte.md`). Les lignes entre le seuil D et le seuil C sont les candidates à l'enrichissement : une donnée de plus les fait souvent changer de tier.

## Porte 7 : tier

`tier = A`, `B` ou `C` selon les seuils de `05_Departements/Go-to-Market/contexte.md`. Les contacts par compte : 2 à 4 sur un A, 1 à 2 sur un B, 1 sur un C (nurturing, pas de téléphone). Au-delà du plafond par entreprise, les contacts en trop sont marqués `exclu = oui`, `raison_exclusion = plafond par entreprise`, en gardant la séniorité la plus haute.

## Rapport en entonnoir

```
Entrée : trouver-personnes_saas-france_2026-09-19.csv (208 lignes)
Porte 0  doublons et exclusions fixes    -23   -> 185
Porte 1  titre hors persona              -41   -> 144
Porte 2  effectif hors bornes            -34   -> 110
Porte 3  secteur exclu                    -6   -> 104
Porte 4  B2C                              -8   ->  96
Porte 5  concurrent                       -3   ->  93
Porte 6  score ICP < 35                  -12   ->  81
Porte 7  tiers                           A 14, B 37, C 30
Manquant : effectif vide sur 19 lignes gardées, secteur vide sur 7
Sortie : qualifier-liste_saas-france_2026-09-19.csv (208 lignes, 127 exclues)
```

Sous l'entonnoir : cinq lignes du tier A avec le détail de leur score, cinq lignes exclues tirées au hasard avec leur raison, et une seule question si une porte a retiré plus de la moitié du fichier.
