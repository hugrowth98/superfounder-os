---
name: veille-createurs
description: >
  La veille des posts qui ont performé chez des comptes LinkedIn choisis par l'utilisateur
  (concurrents, créateurs de sa niche, modèles) : demande les comptes, scrape leurs posts sur
  la fenêtre S-6 à S-2, classe en quatre catégories (20 éducationnels, 20 lead magnets, 10 hot
  takes, 10 storytelling), télécharge les visuels et rend un rapport HTML où chaque post a sa
  vignette, ses chiffres et son texte complet. Se déclenche sur : "veille créateurs", "qu'est-ce
  qui a marché chez", "les meilleurs posts de", "top posts lead magnet", "hot takes du mois",
  "analyse les posts de ces comptes", "surveille ces créateurs". Ne pas utiliser pour les
  newsletters et chaînes YouTube (`veille`), pour ses propres posts (`performance`), ni pour
  une page entreprise (`publications-entreprise`). Pour refaire un visuel du rapport à sa
  charte, enchaîner avec le sous-skill `reprise` du master `infographie`.
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : le script est dans `{SKILL_BASE}/scripts/veille_createurs.py`. Le master a déjà chargé le socle d'écriture.

# Veille créateurs : ce qui a marché chez les comptes que vous suivez

Le script scrape et classe, vous tranchez, le rapport montre. Aucune liste de comptes n'est livrée avec le skill : ce sont les comptes de l'utilisateur, demandés à chaque run ou mémorisés sur un oui.

## Étape 1 : les comptes

Demandez : "Sur quels comptes LinkedIn voulez-vous faire la veille ? Collez les URLs de profils (https://www.linkedin.com/in/...), une par ligne. Cinq à cinquante comptes, l'idéal est autour de trente."

- Si `05_Departements/Marketing/LinkedIn/comptes-veille.json` existe, proposez-le : "J'ai vos N comptes mémorisés le <date>. On repart dessus, on en ajoute, ou on change ?"
- Si l'utilisateur donne des noms sans URL, trouvez les URLs avec `trouver-url-linkedin`, montrez-les, attendez le oui.
- Un compte en double, une URL de page entreprise ou une URL sans `/in/` sont écartés et signalés.

À la fin du run, proposez une fois : "Je mémorise ces comptes dans `comptes-veille.json` pour la prochaine fois ?" Sur un oui, écrivez le fichier :

```json
{"maj": "AAAA-MM-JJ", "comptes": [{"url": "https://www.linkedin.com/in/exemple/", "note": "concurrent direct"}]}
```

## Étape 2 : le coût, puis le run

```bash
python3 {SKILL_BASE}/scripts/veille_createurs.py --comptes <url> <url> --dry-run
```

Le script affiche la fenêtre (du lundi de S-6 au dimanche de S-2, les deux dernières semaines sont exclues parce qu'un post a besoin d'une dizaine de jours pour que son engagement se stabilise), la liste des comptes et le coût maximal (0,002 $ par post, 40 posts par compte au plus : 30 comptes coûtent au plus 2,40 $). Annoncez-le, attendez le oui, relancez sans `--dry-run`. Apify (`APIFY_TOKEN` dans le `.env`, sinon `connecter-outils`), actor `harvestapi/linkedin-profile-posts`, sans cookies. Comptez deux minutes pour trente comptes.

Options : `--fichier comptes.txt` (une URL par ligne), `--memorises` (le JSON), `--fin AAAA-MM-JJ` (rejouer une autre fenêtre), `--sans-medias` (plus rapide, sans vignettes).

## Étape 3 : arbitrer

Le filet de motifs (commentez, DM, je vous offre, lien en clair pour un lead magnet ; voici comment, étapes, framework pour l'éducatif ; opinion impopulaire, arrêtez de, c'est mort pour le hot take ; il y a N ans, quand j'ai, ce que j'ai appris pour le storytelling) propose des candidats. Il se trompe dans les deux sens : il rate les lead magnets qui donnent un lien nu sans rien demander et il prend des lancements de produit pour des lead magnets. Il ne tranche donc jamais seul.

Lisez `candidats.txt` dans le dossier du run (tout ce qui entre dans un classement sur verdict automatique, plus les 40 plus gros posts non tranchés). Pour chacun, écrivez dans `verdicts.json` : `"<id>": "LM"`, `"EDU"`, `"HOT"`, `"STORY"` ou `"NON"`. Puis :

```bash
python3 {SKILL_BASE}/scripts/veille_createurs.py --reconstruire "<dossier du run>"
```

Répétez jusqu'à ce que chaque ligne des quatre classements affiche `verdict manuel` dans le rapport. Comptez dix minutes pour soixante candidats. Les verdicts d'un run précédent restent valables : copiez `verdicts.json` dans le nouveau dossier avant de commencer.

| Code | Catégorie | Quota | Ce qui y entre |
|---|---|---|---|
| EDU | Éducationnel | 20 | enseigne une méthode, un outil, un cadre, sans rien donner à télécharger |
| LM | Lead magnet | 20 | offre une ressource récupérable : commentaire-gate, DM, ou lien en clair |
| HOT | Hot take | 10 | une opinion tranchée, contrariante, sans ressource offerte |
| STORY | Storytelling | 10 | un récit à la première personne, avec un avant et un après |

Hors catégorie : actualités, lancements, recrutement, posts perso sans leçon. Un post n'a qu'une catégorie ; en cas de doute, la plus spécifique gagne (LM avant STORY avant HOT avant EDU). Plafond de trois posts par compte et par catégorie.

## Étape 4 : lire et rendre compte

Ouvrez `rapport.html` (le chemin s'affiche) : quatre tableaux avec la vignette, l'auteur, les interactions, le multiplicateur « x » (le rapport à la médiane du compte : à lire avec le nombre de posts du compte à côté, un compte à trois posts peut afficher x180), l'accroche, le post entier dépliable, le lien LinkedIn, et l'annexe de tous les posts de la fenêtre.

Lisez les vignettes des quatre classements et rendez à l'utilisateur cinq constats au plus, chacun avec le post qui le prouve : ce qui fait le CTA (dans l'image ou dans le texte), les ratios commentaires sur réactions, les formats visuels qui gagnent, les sujets qui reviennent. Puis un seul next step : un visuel à reprendre (`infographie`, sous-skill `reprise`), un post à écrire (`educatif`, `opinion`, `storytelling`, `lead-magnet`), ou un compte à ajouter au `swipe-file.md`.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `05_Departements/Marketing/LinkedIn/comptes-veille.json` | les comptes mémorisés, écrit sur un oui |
| `05_Departements/Marketing/LinkedIn/sources/veille-createurs_<debut>_<fin>/` | le run : `posts.raw.json` (le dump Apify), `posts.json` (classés), `verdicts.json`, `candidats.txt`, `top.json`, `images/` et `images/thumbs/`, `rapport.html` |

Le dossier `sources/` est ignoré par git : ce sont les données de l'utilisateur.

## Règles

- Les compteurs LinkedIn évoluent après le scrape ; ils sont figés à la date du run, écrite dans `run.json`.
- Une URL de profil avec un accent doit être passée décodée (`antoine-ladrière`, pas `antoine-ladri%C3%A8re`), sinon l'actor ne renvoie rien ; le script s'en charge.
- Les vidéos n'ont pas d'image fixe, seulement la vignette quand elle existe. Un post sans visuel est marqué "texte seul".
- Le skill ne publie rien, n'écrit ni dans le swipe file ni dans `posts-de-reference.md` sans un oui.

## Exemples

- "Fais la veille sur ces 12 comptes" avec les URLs : dry-run, coût annoncé (au plus 0,96 $), oui, run, arbitrage des candidats, reconstruction, rapport ; réponse attendue : le lien vers `rapport.html`, cinq constats, un next step, et la proposition de mémoriser les comptes.
- "Qu'est-ce qui a marché chez mes concurrents ce mois-ci ?" avec `comptes-veille.json` déjà rempli : `--memorises`, même chaîne ; réponse attendue : le rapport et la comparaison avec le run précédent si le dossier existe (nouveaux entrants, formats qui montent).
- "Reprends le numéro 3 des lead magnets à ma charte" : passez le fichier `images/LM03_img1.jpg` et le texte du post au sous-skill `reprise` du master `infographie`.
