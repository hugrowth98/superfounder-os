# Prospeo : la base de contacts comme couche de données

Référence pour chaque étape qui touche de la donnée réelle quand Prospeo est branché : sourcer des entreprises, trouver des personnes, obtenir des emails et des mobiles vérifiés. À lire avant de recommander un fournisseur pour ces trois étapes.

Prospeo est une base B2B de contacts et d'entreprises (300 M de contacts, 90 M d'emails vérifiés, rafraîchie tous les 7 jours, une quarantaine de filtres) avec une API REST et un serveur MCP. Ce n'est pas un tableur : pas de colonnes de formule, pas de fusion, pas de dédoublonnage à l'import. On s'en sert pour chercher, enrichir et vérifier ; la fusion, le dédoublonnage et le scoring restent dans le module (`dedoublonner`, `qualifier-liste`).

## 1. Se connecter

Clé `PROSPEO_API_KEY` dans `.env`, branchée par `connecter-outils` (test gratuit : `GET /account-information`, qui rend les crédits restants, le plan et la date de renouvellement). Les scripts passent par l'API (`https://api.prospeo.io`, en-tête `X-KEY`). Le MCP (`https://mcp.prospeo.io`, même clé) reste optionnel, pour explorer à la main.

Les coûts, en crédits : 1 par page de 25 résultats de recherche qui contient au moins un résultat (une page déjà payée dans les 30 jours est gratuite, `free: true`), 1 par email vérifié révélé, 10 par mobile révélé (l'email est compris), 0 sans résultat, 0 pour un contact déjà enrichi depuis moins de 90 jours. Les suggestions de valeurs sont gratuites. Limite de débit sur les recherches : 1 par seconde sur le plan Starter.

## 2. Le workflow en trois temps, et le temps que personne ne fait

Toujours dans cet ordre.

### Temps 1 : résoudre les valeurs des filtres. Gratuit.

Les lieux, les industries, les technologies, les titres, les codes NAICS et SIC ne se devinent pas : une valeur approximative ne renvoie pas d'erreur, elle renvoie zéro résultat. C'est la façon la plus courante de perdre une après-midi. `search-suggestions` transforme ce que dit l'utilisateur en libellé canonique, et ça ne coûte rien : résolvez chaque lieu, techno, industrie et titre avant de construire quoi que ce soit.

```
trouver-entreprises --source prospeo --lister-secteurs software       (industries)
trouver-entreprises --source prospeo --lister-lieux "Paris"           (Paris, France ; Île-de-France, France...)
trouver-entreprises --source prospeo --lister-technos hubspot
trouver-personnes  --source prospeo --lister-titres "head of sales"
```

Les scripts le font aussi tout seuls au vrai run : une valeur qui n'existe pas telle quelle est remplacée par la première suggestion, et annoncée ; sans suggestion, ils s'arrêtent.

Piège de taxonomie : les industries sont celles de LinkedIn, pas les mots de l'utilisateur. "SaaS" ne renvoie rien, "Computer Software" non plus ; "software" renvoie "Software Development". Pour "B2B SaaS", soit on prend ce que rend la suggestion, soit on laisse tomber l'industrie et on décrit le modèle avec l'ICP inverse (`--vend-a`), qui donne presque toujours une meilleure liste.

### Temps 2 : chercher avec des filtres typés.

Au moins un filtre positif est obligatoire. Les résultats arrivent par pages de 25, chaque page avec résultats coûte 1 crédit : la discipline est de resserrer les filtres avant de paginer, pas de tirer dix pages pour trier après.

**La page 1 dit la taille de toute la liste.** La réponse porte `pagination.total_count` : c'est la réponse à "combien de résultats", pour 1 crédit. `--total-seulement` s'arrête là. Lisez-la avant de décider de paginer ou de redécrire la cible.

Sur les personnes, l'email et le mobile reviennent masqués (`j********@entreprise.com`) mais avec leur statut (`VERIFIED`, `UNVERIFIED`) et `revealed` : la page 1 dit donc exactement quelle couverture on achète avant de dépenser un crédit d'enrichissement. Les contacts déjà révélés par votre compte reviennent en clair, sans coût. Mieux : filtrez dessus en amont, avec `--email-verifie` et `--cacher-deja-reveles`, pour ne jamais payer deux fois la même personne.

### Temps 3 : révéler, en lot.

`--reveler` prend les `person_id` des résultats et les passe à l'enrichissement en lot, 50 par appel (1 crédit par email vérifié trouvé, `--reveler-mobile` ajoute les mobiles à 10 crédits). Jamais un appel par personne. Même mécanique côté entreprise : `enrichir-entreprise --source prospeo` rend ce que la recherche ne donne pas (technos, financement, offres ouvertes).

## 3. Les filtres qui font ce que les autres bases ne font pas

Ce sont ceux à sortir quand une recherche "industrie plus effectif" rend une liste trop large.

| Filtre | Ce qu'il fait | Option du module | Quand |
|---|---|---|---|
| ICP inverse (`company_icp`) | trouve les entreprises par ceux à qui **elles** vendent : titres, tailles de clients (micro, smb, midmarket, enterprise, large_enterprise), industries, marchés | `--vend-a "VP Sales,Head of Sales" --vend-a-tailles smb,midmarket` (plan Growth) | le meilleur filtre pour qui vend à des agences, des outils ou des services : il capte le modèle d'affaires, pas la verticale |
| Clients clés (`company_key_customers`) | les entreprises qui citent une marque comme client, 100 marques max | `--clients-cles "Salesforce,HubSpot"` (Growth) | vous vendez à l'écosystème d'une plateforme |
| Lookalike (`company_lookalike`) | par domaine de référence, ou par description libre de 5 000 caractères, avec un niveau T1 (le plus proche) à T3 | `--lookalike-domaine acme.fr`, `--icp-texte "..."`, `--lookalike-niveau T1` | partir des meilleurs clients, ou décrire une entreprise qui n'existe pas encore |
| Mots-clés (`company_keywords`) | n'importe quel mot dans les textes de l'entreprise | `--mots-cles`, `--mots-cles-tous`, `--mots-cles-exclus` | la catégorie n'a pas de code d'industrie propre ; et c'est aussi comment on trouve qui cite un concurrent |
| Intégrations (`company_integrations`) | les entreprises qui mentionnent une intégration | `--integrations` (Growth) | votre produit se branche sur quelque chose de précis |
| Technologies (`company_technology`) | la stack, valeurs canoniques | `--technos` (résolu par les suggestions) | ciblage technographique |
| Actualités (`company_news`) | levée, rachat, lancement, partenariat, expansion, licenciements, IPO, changement de direction, sur 60, 90, 180 ou 365 jours | `--actualites "Funding & Investment,Expansion" --actualites-jours 180` | prospection sur déclencheur |
| Levée (`company_funding`) | stades, ancienneté du dernier tour (30 à 365 jours), montants, investisseurs, accélérateur | `--levee "Seed,Series A" --levee-depuis-jours 365 --investisseurs` | budget frais |
| Postes ouverts (`company_job_posting_hiring_for`) | ce qu'ils recrutent | `--recrute "SDR,Business Developer"` | besoin actif, budget |
| Effectif par pays, croissance, par département | un effectif global cache la réalité locale | `--filtres-json` | qualification fine |

Côté personnes :

| Filtre | Ce qu'il fait | Option |
|---|---|---|
| Titre (`person_job_title`) | contient, exact, ou similaire avec expansion par l'IA (LOOSE, NORMAL, STRICT) ; ou un booléen jusqu'à 500 termes : `(CEO OR CTO) AND !intern`, `"Manager"` exact, `'vice president'` avec espaces | `--titres` (contient), `--titres-similaires --intensite NORMAL`, `--booleen "..."`, `--titres-exclus` |
| Plafond par entreprise (`max_person_per_company`) | 1 à 100 : c'est comment on obtient "2 décideurs par entreprise" | `--par-entreprise 2` (défaut avec une liste de domaines) |
| Coordonnées (`person_contact_details`) | seulement les emails ou mobiles vérifiés, et cacher les contacts déjà révélés | `--email-verifie`, `--mobile-verifie`, `--cacher-deja-reveles` |
| Séniorité, département, lieu | valeurs fixes ; le lieu se résout | `--seniorites fondateur,cxo,vp`, `--departements Sales,Marketing`, `--lieu "Paris, France"` |
| Changement de poste (`person_job_change`) | nouvelle entreprise depuis 30 à 365 jours | `--changement-poste` (90 jours, plan Growth) |
| Entreprises précises (`company.websites`) | 500 domaines max par recherche | `--in <csv avec domaine>` ou `--domaines` |

### Les formes qu'on ne devine pas

Se tromper ici est un rejet de schéma, pas une erreur utile. Le module traduit ses options ; si vous collez un payload du tableau de bord (`--filtres-json`), vérifiez ces points.

| Filtre | Forme | Piège |
|---|---|---|
| `company_headcount_range` | un tableau nu de tranches | tranches fixes : 1-10, 11-20, 21-50, 51-100, 101-200, 201-500, 501-1000, 1001-2000, 2001-5000, 5001-10000, 10000+. **Il n'y a pas de 11-50** : "11 à 50" se dit `["11-20","21-50"]`, ce que fait `--taille 11-50` |
| `company_revenue` | `{min, max, include_unknown_revenue}` | min et max sont des libellés, pas des nombres : `<100K`, `100K`, `500K`, `1M`, `5M`, `10M`, `25M`, `50M`, `100M`, `250M`, `500M`, `1B`, `5B`, `10B+` |
| `person_seniority` | `{include, exclude}` | valeurs fixes : `Founder/Owner`, `C-Suite`, `Partner`, `Vice President`, `Head`, `Director`, `Manager`, `Senior`, `Entry`, `Intern` |
| `company_funding.funding_date` | un nombre de jours parmi `30, 60, 90, 180, 270, 365` | "levé dans les 12 mois" = `365`, pas une plage de dates |
| `company_news.timeframe_days` | `60, 90, 180, 365` | et `categories` prend des libellés fixes ("Funding & Investment", "Mergers & Acquisitions", "Product Launch", "Partnership", "Expansion", "Layoffs & Restructuring", "IPO", "Leadership Change"...) |
| `company_location_search`, `person_location_search` | des chaînes canoniques | "Paris, France", "Île-de-France, France", "France" : telles que rendues par les suggestions, jamais composées |
| `max_person_per_company` | un entier nu | pas un objet |

Une phrase plus serrée bat un filtre de plus : "vend à des équipes outbound" via l'ICP inverse coupe plus fort qu'une pile de codes d'industrie, parce qu'elle vise ce que fait l'entreprise et pas l'étiquette qu'une taxonomie lui a collée.

## 4. La qualité des données, et le seul chiffre qui compte

Ce que le fournisseur annonce : emails vérifiés en trois passes (SMTP, résultats d'envoi réels, filtrage des catch-all et des pièges à spam), environ 98 % de délivrabilité et moins de 1 % de rebond sur les emails vérifiés ; mobiles vérifiés par l'opérateur et par les résultats d'appels réels, 25 à 30 % de décrochés en B2B ; base rafraîchie tous les 7 jours, ce qui compte parce qu'un email se périme de 22 à 30 % par an et un titre de 30 à 35 %.

Une annonce reste du marketing tant que l'utilisateur ne l'a pas testée sur sa propre liste. D'où le protocole, à ne jamais sauter :

### Le contrôle sur 20 adresses

1. Prenez 20 adresses de la vraie liste, pas un échantillon choisi par le fournisseur.
2. Passez-les dans un vérificateur que vous contrôlez, pas le statut du fournisseur lui-même.
3. Comparez le taux de rebond obtenu à ce que le fournisseur annonce.
4. Si ça tient, faites confiance au lot. Sinon, la liste est fausse avant que le texte ne soit accusé.

Ça ne coûte presque rien, et c'est la seule étape qui transforme un chiffre publié en un fait sur votre marché. `nettoyer-verifier` le porte.

## 5. Où Prospeo intervient dans chaque sous-skill

| Étape | Ce que Prospeo fait | Ce qu'il ne fait pas |
|---|---|---|
| `definir-icp` | `trouver-personnes --source prospeo ... --total-seulement` pour mesurer chaque variante d'ICP avant d'en choisir une | le barème, les pondérations |
| `sourcer-entreprises` | `trouver-entreprises --source prospeo` avec l'ICP inverse, le lookalike, les clients clés, les intégrations | la fusion des sources, le registre |
| `sourcer-personnes` | `trouver-personnes --source prospeo` avec les titres similaires et le plafond par entreprise, puis `--reveler` | le croisement CRM, l'envoi |
| `qualifier-comptes` | `enrichir-entreprise --source prospeo` pour technos, attributs, offres, financement, actualités | le score, les tiers |
| `nettoyer-verifier` | des emails et des mobiles vérifiés à la source, catch-all et pièges retirés en amont | les rebonds après envoi, les listes de suppression, la fusion multi-sources |
| `selectionner-comptes` | effectif par pays et CA pour dimensionner les tiers | la mise en étapes ABM |
| `cartographier-personas` | titres, séniorités, départements par compte | la logique du comité d'achat |

La règle : Prospeo répond à "qui existe et comment je le joins". Tout ce qui décide qui compte, dans quel ordre, et quoi dire, reste dans le module.

## 6. Un run complet, de bout en bout

```
1. RÉSOUDRE    --lister-secteurs, --lister-lieux, --lister-technos, --lister-titres sur tout ce que
               l'utilisateur a nommé. Gratuit. Sauté, la recherche rend zéro en silence.

2. CHERCHER    trouver-entreprises --source prospeo ... --total-seulement   (1 crédit : le total)
               trouver-personnes  --source prospeo ... --email-verifie --cacher-deja-reveles --total-seulement
               Au moins un filtre positif. 25 par page, 1 crédit par page avec résultats.
               La page 1 donne aussi la part d'emails vérifiés : la couverture qu'on achète.

3. RESSERRER   Couverture mince ou mauvaise forme ? On change les filtres, on ne pagine pas plus loin.
               --par-entreprise 2 empêche une grosse entreprise de manger la liste.

4. RÉVÉLER     trouver-personnes ... --reveler (--reveler-mobile) : 50 par appel, jamais un par un.
               enrichir-entreprise --source prospeo pour technos, attributs, offres.

5. CONTRÔLER   20 adresses dans votre propre vérificateur. Le taux de rebond confirme, ou pas.

6. EXPORTER    dedoublonner (HubSpot, séquences en cours), qualifier-liste, puis envoyer-sequence.
               Re-vérifier tout ce qui a plus de 30 jours avant d'envoyer.
```

Les temps 1 à 4 tiennent en une conversation. Le temps 5 est celui que personne ne fait, et c'est lui qui décide si la campagne marche.
