---
name: linkedin-system-installer
description: >
  Installeur et personnalisateur du LinkedIn Content System. Utilise ce skill dès que l'utilisateur
  vient d'installer le pack de skills LinkedIn et veut le configurer à sa voix, ou demande à
  "personnaliser les skills LinkedIn", "configurer mon système LinkedIn", "adapter les skills à mon style",
  "setup LinkedIn", "installer le système de contenu", "remplir mon profil créateur", ou voit des
  {{PLACEHOLDERS}} dans ses skills LinkedIn. Ce skill interviewe l'utilisateur (positionnement, ICP, ton,
  piliers, convictions, sources de veille, exemples de posts) puis remplace automatiquement TOUS les
  placeholders dans les 8 skills du système pour qu'ils sonnent exactement comme lui.
---

# LinkedIn System Installer

Ton rôle : transformer un pack de skills LinkedIn générique en un système qui écrit exactement dans la voix de l'utilisateur. Tu mènes un entretien, tu construis un profil, puis tu lances un script qui remplace tous les `{{PLACEHOLDERS}}` dans les 8 skills frères.

## Les 8 skills personnalisés par cet installeur

`linkedin-writing-core` (socle), `linkedin-ideation`, `linkedin-educational`, `linkedin-storytelling`, `linkedin-hot-take`, `linkedin-lead-magnet`, `viral-hook-writer`, `linkedin-post-optimizer`.

Ils sont dans des dossiers FRÈRES de cet installeur (même dossier parent).

---

## Déroulé en 5 phases

### Phase 0 - Accueil et choix du mode

Explique en 2 phrases ce que tu vas faire (personnaliser les skills à sa voix), puis propose 2 modes via AskUserQuestion :

- **Mode Express (recommandé)** : l'utilisateur te donne son URL LinkedIn et/ou colle 3 à 10 de ses meilleurs posts. Tu INFÈRES la majorité du profil (positionnement, niche, ton, marqueurs de style, piliers, convictions) à partir de ces posts, puis tu fais valider.
- **Mode Manuel** : entretien guidé question par question.

Dans les deux cas, tu confirmes toujours avec l'utilisateur avant d'écrire quoi que ce soit.

### Phase 1 - Collecte des informations

Tu dois remplir TOUS les tokens du tableau ci-dessous. Pose les questions par petits groupes logiques (pas 25 questions séparées). En mode Express, déduis un maximum depuis les posts fournis, puis présente ta déduction et demande corrections.

**Règle d'or : n'invente jamais le positionnement, les convictions ou le ton de l'utilisateur.** Déduis depuis ses posts OU demande. Présente toujours ta proposition et fais valider avant d'appliquer.

#### Tokens d'identité et stratégie (obligatoires)

| Token | Ce qu'il faut récupérer |
|---|---|
| `CREATOR_NAME` | Nom complet |
| `CREATOR_FIRSTNAME` | Prénom |
| `NICHE` | Domaine / sujet principal en une formule courte (ex: "l'IA appliquée à la prospection B2B") |
| `POSITIONING` | 1-2 phrases : qui il aide + comment + résultat |
| `MONOPOLE` | Son intersection unique / monopole personnel (3-5 territoires qui le rendent unique). Multi-ligne. |
| `POSTURE` | Posture LinkedIn (ex: Expert + Builder, Experte + Pédagogue) |
| `ICP` | Clients cibles payants |
| `IAP` | Audience large (au-delà des clients) |
| `LANGUAGE` | Langue d'écriture des posts |
| `TONE_MARKERS` | Le ton, en liste de 3-5 puces |
| `DONT_LIST` | Ce qu'il ne fait JAMAIS dans ses posts, en liste |
| `STYLE_MARKERS` | Marqueurs de style (longueur de phrases, symboles, tics d'écriture), en liste |
| `CONTENT_MIX` | Répartition éditoriale par thème (ex: 40/20/20/20), en liste |
| `AUTHORITY_MIX` | Split autorité/perso/offre (ex: 70/15/15) |
| `POSTING_FREQUENCY` | Fréquence (ex: 4 posts/semaine) |
| `CONTENT_PILLARS` | Piliers thématiques, liste numérotée |
| `OFFERS` | Offres / produits / services |
| `CONVICTIONS` | 5-8 convictions fortes (manifesto), en liste |
| `OPINION_TOPICS` | Sujets d'opinion typiques, groupés par thème |
| `ADMIRED_CREATORS` | 3-5 créateurs qu'il admire + ce qu'il prend de chacun |

#### Tokens de veille (obligatoires, peuvent rester en liste à compléter)

| Token | Ce qu'il faut récupérer |
|---|---|
| `YOUTUBE_SOURCES` | Chaînes YouTube qu'il suit pour la veille |
| `NEWSLETTER_SOURCES` | Newsletters qu'il suit |
| `OTHER_SOURCES` | Autres sources (podcasts, X, communautés, ProductHunt...) |
| `SAVED_RESOURCES` | Playbooks / guides / ressources bookmarkés |

Si l'utilisateur n'a pas ces sources sous la main, mets une valeur du type "(À compléter : liste ici tes chaînes YouTube de veille)" pour qu'il les ajoute plus tard. Ne bloque pas l'installation pour ça.

#### Tokens d'exemples / swipe files (optionnels)

Ces tokens remplissent les fichiers de référence avec les VRAIS posts de l'utilisateur. Ils sont précieux pour calibrer la voix mais pas bloquants.

| Token | Contenu |
|---|---|
| `MY_POSTS_EXAMPLES` | 5-10 de ses meilleurs posts (idéalement avec leurs résultats) |
| `LIKED_POSTS` | Posts d'autres qui résonnent avec lui, classés par catégorie |
| `ADMIRED_CREATORS_SWIPE` | Posts complets des créateurs qu'il admire |
| `SWIPE_EDUCATIONAL` | Posts éducatifs de référence à imiter |
| `SWIPE_STORYTELLING` | Posts storytelling de référence |
| `SWIPE_HOT_TAKE` | Posts d'opinion de référence |
| `SWIPE_LEAD_MAGNET` | Posts lead magnet de référence |

Pour chaque token d'exemple non fourni, mets une note claire du type : "(Aucun exemple fourni pour l'instant. Ajoute ici tes posts de référence pour améliorer le calibrage de ta voix.)"

En mode Express, si l'utilisateur a collé ses posts, réutilise-les directement pour `MY_POSTS_EXAMPLES`.

### Phase 2 - Validation

Présente à l'utilisateur une synthèse lisible de tout ce que tu as collecté/déduit (surtout : positionnement, niche, ton, piliers, convictions). Demande explicitement : "Je valide et j'applique, ou tu veux ajuster quelque chose ?" N'avance pas sans accord.

### Phase 3 - Écriture du profil

Écris le fichier `linkedin-profile.json` DANS LE DOSSIER DE CET INSTALLEUR (à côté de `apply_profile.py`), au format JSON, avec une clé par token (sans les `{{ }}`). Les valeurs multi-lignes utilisent `\n`. Inspire-toi de `linkedin-profile.example.json` pour la structure.

Tous les tokens du tableau doivent avoir une valeur (jamais de `{{...}}` résiduel).

### Phase 4 - Application

Lance le script depuis le dossier de l'installeur :

```bash
python3 apply_profile.py --dry-run   # verifie d'abord ce qui va changer
python3 apply_profile.py             # applique pour de vrai
```

Le script :
- crée une copie pristine `.template` de chaque fichier au premier passage (permet de relancer l'installeur autant de fois que voulu pour re-personnaliser),
- remplace tous les `{{TOKEN}}` par les valeurs du profil dans les 8 skills,
- signale à la fin tout token resté non remplacé.

**Si le script signale des tokens restants**, c'est que le profil JSON en a oublié. Complète le profil et relance. Objectif : "aucun placeholder restant".

### Phase 5 - Confirmation

Confirme à l'utilisateur que le système est personnalisé. Rappelle-lui :
- qu'il peut relancer cet installeur quand il veut pour ajuster (le script repart des `.template`),
- que plus il ajoute de posts de référence (tokens swipe), meilleure sera la calibration de sa voix,
- qu'il peut maintenant utiliser n'importe quel skill LinkedIn du pack normalement.

---

## Notes importantes

- **Re-personnalisation** : pour repartir de zéro, lance `python3 apply_profile.py --restore` (remet les placeholders), puis relance l'install. Ou modifie `linkedin-profile.json` et relance `apply_profile.py`.
- **Aucun tiret cadratin** : quand tu rédiges les valeurs du profil, n'utilise jamais de tiret cadratin ni demi-cadratin. Utilise "-", ":", "," ou des parenthèses.
- **Reste fidèle** : ton job est de capturer la voix de l'utilisateur, pas de la réécrire. Si tu déduis depuis ses posts, garde ses mots, ses tics, ses formulations.
- **Si bash/python n'est pas disponible** dans l'environnement : tu peux à la place faire les remplacements toi-même avec l'outil Edit (remplace chaque `{{TOKEN}}` par sa valeur dans chaque fichier .md des 8 skills), mais le script est la voie recommandée.
