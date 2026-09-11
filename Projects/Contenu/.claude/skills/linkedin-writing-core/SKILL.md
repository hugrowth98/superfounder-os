---
name: linkedin-writing-core
description: >
  Skill fondation pour la création de contenu LinkedIn dans la voix de l'utilisateur.
  Utilise ce skill dès que l'utilisateur mentionne LinkedIn, post LinkedIn, contenu LinkedIn,
  rédiger un post, écrire pour LinkedIn, créer du contenu, publication LinkedIn, accroche,
  hook, copywriting LinkedIn, ou toute demande liée à la rédaction de posts pour les réseaux sociaux professionnels.
  Ce skill est TOUJOURS chargé en premier - les autres skills LinkedIn (storytelling, educational, lead-magnet, hot-take)
  en dépendent et le complètent. Si l'utilisateur demande un post LinkedIn sans préciser le type, utilise ce skill
  pour déterminer le meilleur format puis charge le skill spécialisé correspondant.
---

# LinkedIn Writing Core

Ce skill est le socle de tout contenu LinkedIn produit pour le créateur. Il définit l'identité, la voix, les règles structurelles et les frameworks de décision. Tous les autres skills LinkedIn (storytelling, educational, lead-magnet, hot-take) héritent de ces règles.

> Ce skill ne contient aucune donnée sur le créateur : il lit le contexte à chaque exécution. Avant d'écrire, charge dans l'ordre `ABOUT.ME/` (déjà chargé), `Contexte/Tone-and-Voice.md`, `Contexte/Offer-Positioning.md`, `Contexte/Clients-Problems-and-Messages.md`, puis `Projects/Contenu/ressources/strategie-contenu.md` et `posts-de-reference.md`. Si l'un d'eux contient encore `[à remplir]`, propose de lancer "Installe mon contenu".

## Qui est le créateur

Voir `Contexte/Offer-Positioning.md` et `Projects/Contenu/ressources/strategie-contenu.md`, section Positionnement.

**Monopole personnel** : voir `Projects/Contenu/ressources/strategie-contenu.md`

**Posture LinkedIn** : voir `Projects/Contenu/ressources/strategie-contenu.md`

**ICP (clients)** : voir `Contexte/Clients-Problems-and-Messages.md`
**IAP (audience large)** : voir `Projects/Contenu/ressources/strategie-contenu.md`, section Audiences

## Voix & ADN éditorial

### Ton
Voir `Contexte/Tone-and-Voice.md`, section Ton.

### Ce que le créateur NE FAIT PAS
Voir `Contexte/Tone-and-Voice.md` (ce qu'il ne dirait jamais) et `ABOUT.ME/anti-ai-voice.md`.

### Marqueurs de style
Voir `Contexte/Tone-and-Voice.md`, section Marqueurs de style, et `Projects/Contenu/ressources/posts-de-reference.md`.

### Langue
Le créateur écrit dans la langue définie dans `Contexte/Tone-and-Voice.md`. Les termes techniques dans une autre langue sont acceptables quand ils sont naturels dans le métier, mais le post est toujours rédigé dans cette langue.

## Stratégie de contenu

### Répartition éditoriale (la fréquence de publication définie dans `Projects/Contenu/ressources/strategie-contenu.md`)
Voir `Projects/Contenu/ressources/strategie-contenu.md`, section Répartition éditoriale.

### Authority-First Framework (le mix autorité / perso / offre de `Projects/Contenu/ressources/strategie-contenu.md`)
- **Authority content** : expertise pure, insights basés sur l'expérience vécue
- **Personal brand** : backstory, behind the scenes, valeurs, lifestyle
- **Offer content** : cas clients, frameworks propriétaires, offres d'accompagnement

La répartition exacte est définie par `le mix autorité / perso / offre de `Projects/Contenu/ressources/strategie-contenu.md``.

### Piliers thématiques
Voir `Projects/Contenu/ressources/strategie-contenu.md`, section Piliers.

## Structure universelle d'un post

Chaque post LinkedIn suit cette architecture :

```
HOOK (2-3 lignes max)
- Doit passer le "thumb-stop test" : arrêter le scroll en < 2 secondes
- Apparaît avant le "voir plus" sur mobile

[saut de ligne]

CORPS DU POST
- Développement structuré
- Une idée principale, un angle clair
- Formaté pour le skim-reading (titres, listes, symboles)

[saut de ligne]

CONCLUSION / CTA
- Résumé ou punchline finale
- Question ouverte pour engager OU call-to-action clair
```

### Règles de formatage
- Max 3000 caractères (idéal : 1500-2500)
- Première ligne = hook visible avant "voir plus" (environ 140 caractères)
- Pas plus de 3 lignes avant le premier saut de ligne
- Utiliser des listes à puces avec → ou ↳ pour la lisibilité
- 2-3 bullet lists max dans un post
- Alterner paragraphes courts et listes
- Terminer par une question ou un CTA engageant

## Framework de décision : quel type de post ?

Quand l'utilisateur demande un post sans préciser le type, utilise cette grille :

| Objectif | Type de post | Skill à charger |
|----------|-------------|----------------|
| Partager une expérience, un parcours, un apprentissage | Storytelling | linkedin-storytelling |
| Enseigner, expliquer un framework, partager une méthode | Educational | linkedin-educational |
| Vendre, convertir, montrer un cas client, lancer une offre | Lead Magnet | linkedin-lead-magnet |
| Prendre position, challenger une idée reçue, opinion forte | Hot Take | linkedin-hot-take |

Si le type est clair, charge immédiatement le skill correspondant via `Read` sur son SKILL.md.

## Système de hooks

Le hook est l'élément le plus critique du post. Son seul objectif : briser le pattern de scroll du lecteur et le forcer à cliquer "... voir plus". Un bon hook crée un arrêt brutal - quelque chose d'inattendu, de contre-intuitif, ou de tellement spécifique que le lecteur pense "attends, quoi ?"

### Contraintes du hook

Le hook = les 2 lignes visibles avant "... voir plus" sur LinkedIn mobile. Environ 2 phrases courtes de ~55 caractères max chacune. Chaque caractère compte.

### Principes fondamentaux

Le hook doit parler du LECTEUR ou d'une tension universelle - jamais commencer par une réalisation personnelle du créateur. Il doit créer une boucle ouverte : une question sans réponse, une contradiction, ou une affirmation tellement audacieuse que le lecteur ne peut pas l'ignorer. Le hook doit sonner comme un message qu'un pote t'envoie et qui te fait répondre "attends, explique".

**Règles absolues :**
- Pas de réalisation personnelle en ouverture ("J'ai généré X€ de CA")
- Pas d'emoji en ouverture
- Pas de hashtag dans le hook
- Pas de phrases creuses type "Et si je vous disais que..."
- Le hook doit être vrai - ne jamais mentir, ne jamais inventer de chiffres
- Le hook annonce le contenu - pas de bait-and-switch

### Les 5 techniques de pattern interrupt

**1. Contradiction** - Dire quelque chose qui semble faux ou contre-intuitif. Le cerveau détecte l'incohérence et doit résoudre le conflit, il clique.
- "Plus tu [action courante], moins tu [résultat attendu]." / "Le problème n'est pas le volume."
- "Les pires posts LinkedIn génèrent le plus de followers." / "Et c'est logique quand on comprend l'algo."
- "L'outil le plus puissant du marché est gratuit." / "Et presque personne ne l'utilise correctement."

**2. Chiffre spécifique + contexte inattendu** - Un chiffre précis ancre l'attention. Le contexte inattendu crée la surprise. La spécificité signale "c'est du vécu, pas du générique".
- "J'ai supprimé [N] outils de ma stack." / "Mon [métrique] a augmenté de [X]%."
- "[N] lignes de prompt. [résultat spécifique]." / "Voici le système exact."
- "1 heure de setup. [bénéfice durable]." / "Sans y retoucher après."

**3. Accusation directe** - Interpeller le lecteur sur un comportement qu'il reconnaît immédiatement. Pas méchant, lucide. Le lecteur se sent "vu" et doit comprendre pourquoi.
- "Tu écris tes posts LinkedIn pour toi." / "Pas pour ton audience. Et ça se voit."
- "Tu utilises [outil/méthode] comme un stagiaire." / "Normal que les résultats soient moyens."
- "Ton système de [activité] n'en est pas un." / "C'est juste une liste de tâches que tu fais quand t'as le temps."

**4. Pensée volée** - Dire tout haut ce que le lecteur pense tout bas mais n'osera jamais publier. Crée une connexion immédiate de type "il lit dans mes pensées".
- "Tu sais que tes posts LinkedIn sont chiants." / "Ton audience aussi."
- "La plupart des outils que tu paies ne servent à rien." / "Tu le sais. Tu continues quand même."
- "Tu détestes [tâche pénible du métier]." / "Mais t'as pas encore trouvé comment faire autrement."

**5. Recadrage absurde** - Prendre quelque chose de banal et le rendre dramatique ou absurde. Le décalage entre le sujet et le traitement crée la surprise.
- "Ton hook LinkedIn a 1,2 seconde pour survivre." / "La plupart meurent instantanément."
- "Ta boîte mail est un cimetière d'opportunités." / "Voici comment les ressusciter."
- "L'IA ne va pas te remplacer." / "C'est le concurrent d'à côté qui l'utilise qui va le faire."

### Critères de qualité d'un hook

Avant de valider un hook, vérifie ces 6 critères :

1. **Boucle ouverte** : le lecteur DOIT cliquer pour résoudre la tension. Si le hook donne déjà la réponse, c'est raté.
2. **Spécificité** : les hooks vagues ("Comment réussir sur LinkedIn") ne marchent pas. Les hooks spécifiques marchent.
3. **Focus lecteur** : le hook parle du lecteur, de son problème, ou d'une vérité universelle. Pas des accomplissements du créateur.
4. **Longueur** : 2 lignes, ~55 caractères par ligne. Pas un caractère de trop.
5. **Ton le créateur** : direct, concret, sans jargon inutile. Ça doit sonner comme le créateur parle, pas comme un copywriter américain traduit.
6. **Véracité** : pas de chiffres inventés, pas de fausses promesses.

### Process de génération des hooks

Pour chaque post, génère le hook en suivant ce process :

1. **Identifier le sujet central et la tension** - Quelle est l'idée principale ? Quel conflit, quelle douleur, quel insight le post révèle ?
2. **Tester mentalement les 5 techniques** - Pour chaque technique (contradiction, chiffre, accusation, pensée volée, recadrage absurde), imaginer un hook possible.
3. **Choisir la technique la plus adaptée** au type de post et à l'émotion visée.
4. **Écrire le hook principal** - 2 lignes, ~55 caractères chacune, vérifié contre les 6 critères.
5. **Proposer 5 hooks alternatifs** - en utilisant des techniques différentes pour offrir du choix.

Consulte `references/hooks-library.md` pour la bibliothèque complète de templates de hooks classés par catégorie.

## Output attendu

Pour chaque post demandé, produis :

```
## 🎯 HOOK
[Le hook optimisé - 2-3 lignes max]

## 📝 POST COMPLET
[Le post entier, formaté pour LinkedIn, prêt à copier-coller]

## 💡 JUSTIFICATION
- Type de post : [storytelling/educational/lead-magnet/hot-take]
- Pilier : [pilier concerné parmi les piliers thématiques]
- Funnel : [Authority / Personal / Offer]
- Angle 4A : [Actionnable / Analytique / Aspirationnel / Anthropologique]

## 🔄 5 HOOKS ALTERNATIFS
1. [Hook alternatif 1]
2. [Hook alternatif 2]
3. [Hook alternatif 3]
4. [Hook alternatif 4]
5. [Hook alternatif 5]

## ✏️ VARIANTES
- Version courte (< 1000 car.) : [résumé]
- Angle alternatif : [autre façon d'aborder le sujet]
```

## Checklist qualité (avant de livrer)

Vérifie chaque post contre ces critères :

- [ ] Le hook passe le thumb-stop test (boucle ouverte + spécificité + focus lecteur)
- [ ] Le hook fait max 2 lignes de ~55 caractères, utilise une des 5 techniques de pattern interrupt
- [ ] Le hook ne commence pas par une réalisation personnelle, un emoji, ou un hashtag
- [ ] Le post sonne comme le créateur, pas comme un robot ou un coach LinkedIn générique
- [ ] Phrases courtes, paragraphes aérés, optimisé mobile
- [ ] Une seule idée principale développée en profondeur
- [ ] Contenu basé sur de l'expérience vécue ou un insight concret (pas du générique)
- [ ] 0-1 emoji max (sauf si le format l'exige)
- [ ] Symboles → ↳ ◉ utilisés pour la structure
- [ ] Le post apporte de la valeur réelle (le lecteur repart avec quelque chose)
- [ ] CTA ou question engageante en conclusion
- [ ] Longueur adaptée (1500-2500 caractères idéal)
- [ ] Pas de buzzwords vides, pas de "révolutionnaire", pas de fausse promesse
- [ ] Écrit en la langue définie dans `Contexte/Tone-and-Voice.md` avec termes techniques dans une autre langue seulement quand c'est naturel

## Fichiers de référence

- `references/hooks-library.md` - Bibliothèque complète de hooks classés par catégorie. Consulte ce fichier quand tu as besoin d'inspiration pour les hooks.
- `references/voice-guide.md` - Méthodo pour calibrer la voix + emplacement de tes exemples de posts. Consulte ce fichier pour calibrer le ton.
- `references/quality-checklist.md` - Checklist détaillée et anti-patterns. Consulte quand tu veux vérifier la qualité d'un post.
- `Projects/Contenu/ressources/swipe-file.md` : posts des créateurs admirés et posts likés. Pour s'inspirer des structures et styles qui performent.
- `Projects/Contenu/ressources/posts-de-reference.md` : les posts réels du créateur analysés. C'est LA référence pour calibrer la voix et le ton. À consulter en priorité.
- `references/formations-frameworks.md` - Synthèse des frameworks stratégiques (4A, Monopole Personnel, TOFU/MOFU/BOFU, Authority-First, ICP vs IAP). Consulte ce fichier pour les décisions stratégiques de contenu.
- `references/post-templates.md` - Templates de posts (Avant/Après, Célébration, Livre, Objectif, Retour d'expérience, Liste, Leçons, Portrait, Actualité, Annonce, Prise de conscience) + checklist. Consulte ce fichier pour la structure de départ d'un post.
