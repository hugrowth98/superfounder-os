# Contenu

> Chargé automatiquement par Claude Code quand on travaille dans ce dossier. Le bloc ETAT est maintenu par /done : ne pas l'éditer à la main.

## Rôle

Le module de contenu de Superfounder OS (jour 3). Une chaîne de production de posts LinkedIn dans la voix de l'utilisateur : trouver quoi dire, écrire dans le bon format, maximiser la portée. Dix skills scopés à ce dossier, un socle commun (`linkedin-writing-core`) que tous les autres chargent en premier.

## Contexte à charger avant d'écrire

Aucun skill de ce dossier ne contient de donnée sur l'utilisateur. Avant de rédiger quoi que ce soit :
- `Contexte/Tone-and-Voice.md` (la voix) et `ABOUT.ME/anti-ai-voice.md` (déjà chargé)
- `Contexte/Offer-Positioning.md` et `Contexte/Clients-Problems-and-Messages.md`
- `ressources/strategie-contenu.md` (piliers, convictions, sources, créateurs admirés)
- `ressources/posts-de-reference.md` (ses posts : l'échantillon l'emporte sur les principes)
- `ressources/swipe-file.md` (les posts des autres, pour les structures)

Si `strategie-contenu.md` ou un fichier de `Contexte/` contient encore `[à remplir]`, dis-le et propose "Installe mon contenu" (ou "Installe mon second cerveau" si c'est `Contexte/`).

## Premier message dans ce dossier

- `ressources/strategie-contenu.md` encore `[à remplir]` dans ses sections obligatoires : bienvenue en 2 phrases, puis lance `installer-contenu`.
- Installé : lis le bloc ETAT ci-dessous et propose la prochaine action (un post à écrire, la veille de la semaine, un post à optimiser).

## La chaîne en 5 stations

| Station | L'utilisateur écrit | Skill |
|---|---|---|
| 1. Trouver quoi dire | "idées de posts", "fais ma veille", "interviewe-moi" | `linkedin-ideation`, `linkedin-interview` |
| 2. Le socle | (chargé automatiquement par les skills de rédaction) | `linkedin-writing-core` |
| 3. Écrire dans le bon format | "écris un tuto sur", "raconte", "mon avis sur", "post lead magnet" | `linkedin-educational`, `linkedin-storytelling`, `linkedin-hot-take`, `linkedin-lead-magnet` |
| 4. Maximiser la portée | "propose des hooks", "améliore ce post" | `viral-hook-writer`, `linkedin-post-optimizer` |
| 5. Installer ou ré-installer | "Installe mon contenu" | `installer-contenu` |

Si le type de post n'est pas précisé, `linkedin-writing-core` choisit le format puis charge le skill spécialisé.

## Conventions

- Chaque post produit va dans `output/`, un fichier par post : `Post-Sujet_YYYY-MM-DD.md`. Le brief de veille hebdo : `Brief-veille_YYYY-MM-DD.md`.
- Les sources (transcripts, articles, idées brutes) vont dans `input/`.
- Les posts qui ont bien marché remontent dans `ressources/posts-de-reference.md`. Les posts des autres qui arrêtent le scroll vont dans `ressources/swipe-file.md`.
- Vouvoiement sur tout contenu publié, sauf si `Contexte/Tone-and-Voice.md` dit le contraire.
- Aucun tiret cadratin ni demi-cadratin dans un post.

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)
## Priorités / en cours
-
## Décisions actées
-
## Prochaines étapes
- [ ] Installe mon contenu
<!-- ETAT:END -->
