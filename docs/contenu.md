# Le contenu : mode d'emploi

**Ce que vous aurez à la fin** : une machine qui lit vos sources chaque semaine, vous propose des idées ancrées, écrit vos posts dans votre voix, les transforme en visuels à vos couleurs, les programme au bon créneau et vous dit ce qui marche chez vous. Vous validez, vous ne rédigez plus.

**Durée** : 45 minutes à 1h30 d'installation (en plusieurs fois si vous voulez), puis 10 minutes par post et 15 minutes par semaine pour la veille.

## Avant de commencer

- Le second cerveau est installé. Le contenu lit `02_Contexte/Tone-and-Voice.md`, `Offer-Positioning.md` et `Clients-Problems-and-Messages.md`.
- Sous la main : 5 à 10 de vos meilleurs posts LinkedIn, avec leurs chiffres si vous les avez (impressions, réactions, commentaires). C'est la meilleure matière pour caler la voix et voir ce qui marche chez vous.
- Les newsletters que vous lisez vraiment et les chaînes YouTube que vous suivez (noms suffisent, les flux se trouvent).
- Facultatif : vos couleurs et votre police (une ligne), et un compte Publora si vous voulez programmer depuis le chat.

## La phrase à taper

```
Installe mon contenu
```

## Ce qui se passe, en huit phases

1. Claude lit votre second cerveau. Il ne vous redemande ni votre offre, ni votre cible, ni votre voix.
2. **Voix et style** : vous collez vos posts, il en tire vos marqueurs de style et vos expressions.
3. **Posts de référence** : rangés par type dans `posts-de-reference.md` avec leurs chiffres, et, dès 10 posts chiffrés, "ce qui marche chez vous".
4. **Stratégie** : niche, monopole personnel, piliers, répartition, convictions, objectif, cadence et créneaux, formats, fins de post, créateurs admirés, dans `strategie-contenu.md`. Une question à la fois, une valeur par défaut à chaque fois.
5. **Swipe file** : les posts des autres qui vous arrêtent, pour leurs structures.
6. **Système de veille** : vos newsletters et vos chaînes dans `sources-veille.json`, un premier run pour vérifier que tout se lit, les transcripts YouTube en option.
7. **Charte visuelle** : vos couleurs, votre police et votre logo dans `03_Branding/charte-visuelle.md`, pour les infographies.
8. **Profil** puis **premier brief** : le titre et l'à propos passés en revue, Publora branché si vous le voulez, et la première veille ou le premier post.

Aucun skill ne contient de donnée sur vous. Ils lisent ces fichiers à chaque exécution. Quand votre positionnement bouge, vous modifiez un fichier, pas seize skills.

## Le master `linkedin` et ses seize sous-skills

Vous n'avez pas à les nommer : les phrases suffisent.

| Vous voulez | Vous dites | Sous-skill |
|---|---|---|
| Savoir ce qui se dit cette semaine chez vos sources | "fais ma veille" | `veille` : brief en 6 sections (sujet le plus discuté, top 10, lancement, 10 idées de posts, 10 de newsletter, 10 de lead magnet), chaque idée ancrée sur une source |
| Voir ce qui a marché chez des comptes que vous suivez | "fais la veille créateurs", "qu'est-ce qui a marché chez" | `veille-createurs` : vous donnez les comptes, le skill scrape leurs posts sur la fenêtre S-6 à S-2 et rend un rapport HTML à quatre classements (20 éducatifs, 20 lead magnets, 10 hot takes, 10 storytelling) avec la vignette de chaque post |
| Trouver quoi dire, bâtir le calendrier | "idées de posts", "quoi poster" | `ideation` |
| Partir de votre vécu | "interviewe-moi", "page blanche" | `interview` |
| Écrire un post | "écris un tuto sur", "raconte", "mon avis sur", "post lead magnet" | `educatif`, `storytelling`, `opinion`, `lead-magnet` |
| Ouvrir et fermer | "propose des hooks", "comment je termine" | `hooks`, `cta` |
| Choisir le support | "carrousel ou texte", "je mets le lien où" | `formats` |
| Améliorer un draft | "améliore ce post", "challenge mon post" | `optimiser` |
| Publier au bon moment | "quand publier", "programme ma semaine" | `publier`, puis le skill `planifier-post` |
| Faire grandir la portée | "réponds aux commentaires", "qui commenter" | `engagement` |
| Tirer plusieurs contenus d'un seul | "recycle ce post", "découpe ce live" | `recycler` |
| Convertir les visites du profil | "optimise mon profil" | `profil` |
| Savoir ce qui marche chez vous | "analyse mes posts", "bilan du mois" | `performance` |
| Un visuel | "transforme ce post en infographie", "version manuscrite" | master `infographie` |
| Refaire à votre charte un visuel qui a marché ailleurs | "reprends cette infographie", "trois versions de ce visuel" | `infographie`, sous-skill `reprise` : trois PNG 1080x1350 dans trois structures, rendu HTML exact, sans IA d'image |

## La veille créateurs, chaque mois

Le sous-skill `veille-createurs` ne sait pas qui vous suivez : il vous demande les comptes LinkedIn (les URLs de profil, cinq à cinquante), annonce le coût Apify (0,002 $ par post, 40 posts par compte au plus), scrape leurs posts sur une fenêtre fermée (du lundi de S-6 au dimanche de S-2, pour que l'engagement soit stabilisé), puis classe en quatre catégories avec des quotas : 20 éducatifs, 20 lead magnets, 10 hot takes, 10 storytelling. Les motifs automatiques proposent, vous tranchez dans `verdicts.json`, le rapport HTML montre chaque post avec sa vignette, ses chiffres, son texte complet et son lien. Sur un oui, les comptes sont mémorisés dans `comptes-veille.json` pour le mois suivant. Un visuel du rapport se refait à votre charte avec le sous-skill `reprise` du master `infographie`.

## La veille, chaque lundi

Le sous-skill `veille` lit vos newsletters (flux RSS, avec les likes et les commentaires de chaque article) et vos chaînes YouTube (avec les transcripts si la bibliothèque est installée), calcule un score de vélocité (l'engagement pour 1 000 abonnés par jour) et vous rend un brief en six sections, dans votre voix, où chaque idée cite sa source. Le dump brut reste dans `05_Departements/Marketing/LinkedIn/sources/`, le brief dans `Brief-veille_AAAA-MM-JJ.md` si vous voulez le garder. Une source s'ajoute en une ligne dans `sources-veille.json`. Aucun appel payant : flux et pages publics.

## Programmer avec Publora

Le skill `planifier-post` programme un post validé sur Publora depuis le chat : vous donnez le fichier du post et l'heure locale, il vérifie les bonnes pratiques (longueur, hook, lien en premier commentaire, créneau, collision avec un autre post), joint une image ou le PDF d'un carrousel, tient `Calendrier-publication.md`, poste le premier commentaire après publication et lit les statistiques. Installation, comme les outils de prospection : compte sur publora.com (gratuit pour 15 posts par mois), profil LinkedIn relié dans le tableau de bord, clé API collée dans le chat, écrite dans `.env` et testée par `connecter-outils`. Sans Publora, Claude vous donne le post et l'heure, vous programmez dans LinkedIn.

## Où vont les choses

`05_Departements/Marketing/` a quatre briques, chacune avec sa note : `LinkedIn/` (les posts, les briefs, les infographies, le calendrier, à plat, avec `strategie-contenu.md`, `posts-de-reference.md`, `swipe-file.md`, `sources-veille.json`), `Newsletter/`, `Video/`, `Slides/`. Les emails à votre audience vont dans `05_Departements/Go-to-Market/Mailing/`, un event est un projet dans `04_Projets/`, votre charte dans `03_Branding/charte-visuelle.md`. Les skills vivent dans `10_Skills/` et sont visibles partout.

## Comment vérifier que c'est bon

Demandez un post sur un sujet que vous avez déjà traité. Comparez avec le vôtre. Si vous reconnaissez vos tics, vos mots, votre rythme, le contenu est installé. Sinon, ajoutez des posts dans `posts-de-reference.md` : c'est l'échantillon qui calibre. Puis "fais ma veille" : si le brief cite vos sources avec des chiffres, la veille tourne.

## La boucle hebdomadaire, une fois les trois modules installés

Le lundi, la veille sort les idées. Le vendredi ou le dimanche, les posts de la semaine s'écrivent en lot et se programment. Chaque post génère des commentaires ; les 90 minutes qui suivent la publication servent à répondre. Le mercredi, la prospection récupère ceux qui ont commenté et leur écrit. Le vendredi, `/weekly-review`. Et `/done` à la fin de chaque session, pour que le cerveau sache lundi ce qui s'est décidé jeudi.

Le contenu nourrit la prospection. La prospection nourrit les rendez-vous. Les rendez-vous nourrissent le contenu.
