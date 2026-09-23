# Le format de `data.json` et les huit gabarits

Le sous-skill `reprise` écrit un `data.json` par infographie à reprendre, puis `scripts/rendre_infographie.py` le rend dans un ou plusieurs gabarits. Tous les gabarits lisent le même fichier ; chacun prend les champs dont il a besoin.

## Le fichier

```json
{
  "slug": "12-Skills-Claude",
  "date": "2026-09-22",
  "label": "Skills Claude · la bibliothèque",
  "titre": "12 skills Claude",
  "accent": "qui se déclenchent tout seuls",
  "accent_position": "fin",
  "sous_titre": "Vous les installez une fois. Claude les lance ensuite sans que vous ayez à demander.",
  "cta": "Commentez « SKILLS » pour recevoir les 12",
  "colonnes": ["Le skill", "Ce qu'il fait", "Ce que vous dites à Claude"],
  "items": [
    {"id": "01", "nom": "Grill me", "meta": "/grill-me",
     "desc": "Vous pose 10 à 15 questions avant de construire quoi que ce soit.",
     "cite": "Grille-moi avant de commencer.", "tier": "Must", "cote": "gauche"}
  ],
  "groupes": [{"nom": "Cadrer", "sous": "Avant de produire", "ids": ["01", "09", "08"]}],
  "coeur": {"label": "Le cœur", "titre": "Claude",
            "texte": "Chaque skill est une commande. Vous l'installez une fois, {accent}, sans y penser.",
            "accent": "il la déclenche au bon moment", "chiffres": [["4", "métiers"], ["12", "commandes"]]},
  "comparatif": {"gauche": "Avant", "droite": "Maintenant"},
  "niveaux": ["Fondations", "Orchestration", "Autonomie"],
  "densite": "normal",
  "source": {"auteur": "Nom", "url": "https://...", "date": "2026-09-07", "total": 2494}
}
```

| Champ | Rôle |
|---|---|
| `slug`, `date` | le nom des fichiers de sortie |
| `label` | le surtitre en monospace capitales, court |
| `titre` + `accent` | le titre en couleur de texte, l'accent dans la couleur d'accent de la charte. `accent_position` : `fin` (deuxième ligne) ou `debut`. L'accent est une phrase complète, pas un mot seul |
| `sous_titre` | une phrase, optionnelle |
| `cta` | le texte de la pilule (couleur d'accent secondaire de la charte, ou l'accent principal). Vide : pas de pilule |
| `colonnes` | les trois en-têtes du gabarit `glossaire` |
| `items` | la liste, dans l'ordre. `id` sur deux chiffres, `meta` en monospace couleur d'accent (commande, chiffre, outil), `desc` en gris, `cite` en italique (le gabarit ajoute les guillemets), `tier` pour `tierlist` et `pyramide`, `cote` pour `comparatif` |
| `groupes` | pour `systeme` : 2 à 4 familles, chaque item dans une seule |
| `coeur` | pour `systeme` : le bloc plein (couleur "fond des blocs" de la charte). `{accent}` dans `texte` est remplacé par la phrase `accent` |
| `comparatif` | les titres des deux colonnes ; la droite est le bloc plein |
| `niveaux` | `pyramide` : du bas vers le haut ; `tierlist` : du meilleur au moins bon |
| `densite` | `normal` ou `serre` (corps et marges réduits de 10 pour cent) |
| `source` | pour la fiche, jamais sur l'image |

## Les huit gabarits et les structures qu'ils servent

| Gabarit | Structures de la bibliothèque | Tient dans 1080x1350 avec |
|---|---|---|
| `grille` | 3 cheat sheet, 10 quadrants (4 items) | 6, 8, 9 ou 12 items ; description de 90 caractères à 12, 140 à 6 |
| `glossaire` | 7 glossaire, 13 anatomie | 8 à 12 lignes, description de 100 caractères |
| `systeme` | 5 hub et rayons, 6 cycle, 11 radial | 3 ou 4 groupes de 2 à 4 items |
| `etapes` | 1 guide en étapes, 2 timeline, 4 avant pendant après, 8 tutoriel | 4 à 7 items, description de 160 caractères |
| `comparatif` | 9 tableau comparatif, 15 anti-guide | 4 à 7 paires |
| `pyramide` | 12 pyramide, niveaux | 3 à 5 niveaux, 1 à 3 items par niveau |
| `funnel` | un entonnoir, des étages qui se rétrécissent | 4 ou 5 étages : `desc` ce qu'on fait, `cite` ce qu'on mesure |
| `tierlist` | 14 scorecard, un classement par rang | 3 ou 4 rangs, 2 à 5 items par rang |

## Choisir trois gabarits pour une reprise

1. **La fidèle** : le gabarit de la structure d'origine. Le témoin.
2. **La lisible** : celui qui rend le même contenu plus rapide à lire (souvent `glossaire`, `etapes` ou `comparatif`).
3. **La réorganisée** : celui qui regroupe ou hiérarchise autrement (`systeme`, `pyramide`, `funnel`, `tierlist`). Il demande un tri, c'est lui qui apporte le plus.

Jamais deux gabarits de la même famille sur la même reprise : `grille` et `glossaire` sont deux lectures d'une liste, pas deux structures.

| L'original est | Fidèle | Lisible | Réorganisée |
|---|---|---|---|
| une grille de cartes | `grille` | `glossaire` | `systeme` |
| une liste numérotée | `etapes` | `grille` | `pyramide` ou `funnel` |
| une opposition | `comparatif` | `glossaire` | `etapes` |
| un classement | `tierlist` | `grille` | `pyramide` |
| un schéma de flux | `funnel` ou `etapes` | `glossaire` | `systeme` |
