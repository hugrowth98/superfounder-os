---
name: hooks
description: >
  Écrit les deux premières lignes d'un post LinkedIn, celles qu'on voit avant "voir plus",
  pour des dirigeants, consultants et experts qui vendent leur expertise. Se déclenche sur :
  "propose des hooks", "accroche", "mes posts ne prennent pas", "personne ne clique sur voir
  plus", "améliore l'ouverture", "variantes de hook pour ce sujet", ou quand un draft arrive
  avec un bon corps et une ouverture faible. Produit 3 à 5 hooks avec, pour chacun, la
  technique utilisée et le lecteur qu'il attire. Ne pas utiliser pour écrire le corps du post
  (sous-skill du type) ni pour un titre de profil (sous-skill `profil`).
---

> Sous-skill du master `linkedin`. `SKILL_BASE` est le dossier du master (Glob sur `**/linkedin/SKILL.md`) : les ressources sont dans `{SKILL_BASE}/ressources/`. Le master a déjà chargé le socle d'écriture : ce fichier le complète, il ne le répète pas.

# Hooks

Le hook a un seul travail : faire que la bonne personne s'arrête et appuie sur "voir plus". Il ne résume pas le post, il n'a pas besoin d'être malin, il ne parle pas à tout le monde. Un post moyen avec un grand hook bat un grand post avec un hook mou, à chaque fois. Le lecteur visé est l'ICP de `02_Contexte/Clients-Problems-and-Messages.md`, sauf si l'utilisateur vise son audience large (IAP de `Strategie-contenu.md`).

## Ce qu'il faut en entrée

1. Le sujet ou l'idée du post (ou le draft entier).
2. Qui doit s'arrêter : l'ICP par défaut.
3. Le format du post s'il est connu : `educatif`, `storytelling`, `hot-take`, `lead-magnet`.
4. La matière : les fiches du post (champ `fiches` du brouillon) et, pour la construction, les hooks des fiches de `05_Departements/Marketing/Content-Brain/02_Veille/Inspirations/` au même format et ceux de `Posts-de-reference.md`. Un hook cite un chiffre ou une scène seulement s'ils sont dans une fiche.

## La règle des 210 caractères

Sur mobile, seuls les 210 premiers caractères (2 à 3 lignes courtes) sont visibles. Écrivez le hook en 2 lignes d'environ 55 caractères, sans hashtag ni emoji, sans "Et si je vous disais que", sans réussite personnelle en ouverture ("J'ai généré X euros"), sans question à laquelle tout le monde répond oui ("Vous voulez plus de clients ?"), sans deux-points en fin de ligne 2 (ça coupe l'élan). Le hook est vrai et le corps tient ce qu'il promet.

## Les 7 techniques

Chaque hook qui marche en utilise au moins une, souvent deux.

| Technique | Ce qu'elle fait | Gabarit | Sert surtout à |
|---|---|---|---|
| Le miroir de douleur | décrit la situation exacte que vit le lecteur, il pense "c'est moi" | [sa situation précise, en 1 ou 2 lignes] | éducatif, cas client |
| La contradiction | dit une chose qui semble fausse, le cerveau doit résoudre le conflit | "Plus vous [action courante], moins vous [résultat attendu]." | opinion, changement de croyance |
| Le chiffre précis | un résultat concret, daté, chiffré ; la précision signale du vécu | [chiffre] + [contexte précis] + [délai] | cas client, résultats |
| La boucle ouverte | annonce un résultat ou un insight, retient le comment | "J'ai changé une ligne de mon profil. Trois messages en 48 heures." | storytelling, leçon, méthode révélée |
| L'adresse directe | nomme le lecteur et sa situation, le post a été écrit pour lui | "Si vous êtes [ICP] et que [situation], lisez ceci." | tous, surtout lead magnet et éducatif |
| L'accusation lucide | pointe une erreur que le lecteur reconnaît, sans mépris | "Vous écrivez vos posts pour vous. Pas pour votre audience. Et ça se voit." | éducatif, opinion |
| L'entrée en scène | plonge dans un moment précis, sans préambule | "Mardi, 9h14. Quatre messages non lus, de gens que je n'avais jamais croisés." | storytelling, victoire client |

Deux variantes utiles : la pensée volée (dire tout haut ce que le lecteur pense tout bas : "Vous savez que vos posts sont ennuyeux. Votre audience aussi.") et le recadrage absurde (rendre dramatique un détail banal : "Votre hook a 1,2 seconde pour survivre.").

## Le process

1. Identifier l'idée centrale et la tension du post (quel conflit, quelle douleur, quel insight).
2. Tester mentalement les 7 techniques sur cette tension.
3. Écrire le hook principal avec la technique la plus adaptée au type de post et à l'émotion visée.
4. Le passer au contrôle qualité ci-dessous.
5. Écrire 3 à 5 alternatives avec des techniques différentes, pour que l'utilisateur choisisse celle qui lui ressemble.
6. Si l'utilisateur a fourni un hook, le réécrire aussi, avec une ligne sur ce qui a changé et pourquoi.

## Contrôle qualité

- [ ] Précis, pas vague : "4 500 euros" et pas "de bons résultats", "30 jours" et pas "vite"
- [ ] Une tension : un écart, une contradiction, une question ou une reconnaissance qui demande une suite
- [ ] Moins de 210 caractères, idéalement moins de 150 ; la ligne 1 porte l'essentiel, la ligne 2 amplifie ou retourne, elle ne répète pas
- [ ] Aucun mot de trop : couper "je pense que", "d'expérience", "laissez-moi partager"
- [ ] Il attire le bon lecteur (l'ICP s'arrête, le passant continue)
- [ ] Ni appât, ni cliché LinkedIn ("Opinion impopulaire :", "Vous êtes d'accord ? 👇"), ni titres de gloire en ouverture
- [ ] Il sonne comme l'utilisateur (comparer à `Posts-de-reference.md`), pas comme un copywriter américain traduit
- [ ] Aucun tiret cadratin, aucune négation contrastive, aucun chiffre inventé

## Ce qui est rendu

```
**Hook 1** (miroir de douleur + adresse directe)
[1 à 2 lignes]
→ Pourquoi ça marche : [une phrase] · Lecteur attiré : [qui]

**Hook 2** (chiffre précis + boucle ouverte)
...

**Hook 3** (contradiction)
...
```

Au moins 3 variantes avec des techniques différentes. La bibliothèque classée par catégorie (story, chiffres, douleur, désir, urgence, polarisation, preuve, promesse, question, liste, actualité) est dans `{SKILL_BASE}/ressources/formules-de-hooks.md` : y piocher un gabarit, jamais une phrase telle quelle.

## Exemples

- "Sujet : j'ai divisé ma stack d'outils par deux" : chiffre précis ("J'ai supprimé 6 outils de ma stack. Mon pipeline a augmenté de 30 %.") ou contradiction ("Moins d'outils, plus de rendez-vous. Voici la liste que j'ai coupée.") ; réponse attendue : 4 hooks, techniques nommées.
- "Draft fourni, ouverture : Aujourd'hui je voulais partager une réflexion sur la prospection" : diagnostic (préambule, aucune tension), réécriture en entrée en scène ou miroir de douleur, 3 alternatives ; réponse attendue : l'original corrigé plus 3 hooks.
- "Post lead magnet sur un modèle de séquence" : adresse directe + boucle ouverte ("Si vous relancez encore à la main, ce modèle vous rend 2 heures par semaine.") ; réponse attendue : le hook et le mot-clé de commentaire cohérent avec `cta`.
