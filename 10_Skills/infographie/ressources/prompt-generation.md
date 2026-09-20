# Le prompt de génération, et les moteurs

Le prompt final est le dernier bloc du brief. Il s'écrit en anglais (les modèles d'image le lisent mieux), il contient tout ce que l'image doit montrer, mot pour mot, et il part tel quel dans le moteur. Le brief le garde pour qu'on puisse relancer une variante sans tout refaire.

## Anatomie du prompt

Dans cet ordre, en blocs séparés par une ligne vide :

1. **Le cadre** : le type d'image ("a premium B2B editorial one-pager infographic", "a hand-drawn founder notebook page", "a photograph of a whiteboard sketchnote"), le format ("portrait 4:5, 1024x1280"), l'usage ("for a LinkedIn post, readable on a phone").
2. **La structure** : le nom de la structure et sa composition (le nombre de sections, leur ordre, la disposition, les colonnes, le chemin de lecture).
3. **Le texte exact**, bloc par bloc, entre guillemets, dans l'ordre de lecture : titre, sous-titre, chaque section avec son numéro, son titre, ses points, ses exemples, le footer. Rien d'autre ne doit apparaître : le prompt le dit ("render exactly this text, nothing else, no lorem ipsum").
4. **La direction artistique** : les couleurs en hexadécimal avec leur rôle, les typographies (ou leur famille : "geometric sans-serif bold for titles, serif for body"), les composants (cartes, badges pilule, bordures, rayons, ombres, connecteurs), la densité, le logo et sa position.
5. **La hiérarchie** : ce qui domine, les tailles relatives ("title 3x body size"), les mots en accent.
6. **Les contraintes** : "all text must be legible at phone size, minimum 14 px equivalent", "no spelling mistakes, French accents rendered correctly", "no extra icons, no emojis, no gradients, no stock illustrations, no watermark", "keep 4 percent safe margins".
7. **Les interdits de la charte**, repris tels quels.

Un prompt fait 300 à 900 mots. En dessous, le modèle invente ; au-dessus, il oublie le milieu.

## Ce que les moteurs savent faire

| Moteur | Modèle | Ce qu'il fait bien | Format | Clé |
|---|---|---|---|---|
| OpenAI (API) | `gpt-image-2` (défaut), `gpt-image-1` | le texte dans l'image, les compositions denses, les consignes longues | `1024x1280` demandé (4:5), sinon `1024x1536` ; `2048x2048` et `4096x4096` en carré | `OPENAI_API_KEY` |
| fal.ai | `openai/gpt-image-2` (défaut), `fal-ai/nano-banana-pro` (4:5 natif, 1K à 4K, bon sur le texte et les schémas), `fal-ai/ideogram/v3` (typographie) | les mêmes modèles sans compte OpenAI, plus des alternatives | `image_size` en largeur et hauteur, ou `aspect_ratio: 4:5` | `FAL_KEY` |
| Codex, ou un client avec un outil natif de génération d'image | celui de l'outil | le même prompt, collé tel quel | portrait 4:5 si l'outil le permet | aucune : le client |

Règle de choix : dans Codex ou dans un client qui a un outil d'image, l'outil natif avec le prompt final. Sinon `scripts/generer_image.py` : OpenAI si la clé est dans `.env`, fal.ai sinon. Le script écrit le prompt utilisé à côté de l'image (`.prompt.txt`) pour la variante suivante.

## Coût et itération

Une image en qualité haute coûte de l'ordre de quelques dizaines de centimes (le prix exact dépend du modèle, de la taille et de la qualité : lisez la page de prix du moteur, le script affiche le modèle et la taille avant de lancer). On génère une image, on la montre, on lit ce qui cloche (un texte mal rendu, une carte trop pleine, une couleur hors charte), on corrige le prompt à cet endroit précis, et on relance une variante `_v2`. Jamais trois variantes d'un coup : on ne saurait pas laquelle a corrigé quoi.

Deux fautes reviennent souvent : le modèle ajoute des mots ("Tips", "Step") qu'on n'a pas écrits, ou coupe un point trop long. Le remède est dans le texte exact (plus court) et dans la contrainte "render exactly this text".

## La checklist qualité avant de générer

- Le titre est clair et tient en 4 à 9 mots ; la promesse est visible en 3 secondes.
- Chaque bloc apporte une idée ; aucun bloc décoratif.
- Aucun paragraphe ; aucun point de plus d'une ligne.
- Le texte est lisible sur un téléphone (densité utile, pas de surcharge).
- Les couleurs, les typographies et les composants sont ceux de la charte ; les interdits sont dans le prompt.
- Le logo est placé s'il existe.
- Le texte a passé la checklist §H d'`anti-ai-voice.md` (aucun tiret cadratin, aucune négation contrastive, aucun mot de la liste noire).
- Le prompt contient le texte exact et la contrainte "nothing else".
- Le format est portrait 4:5.
- L'image donne envie d'être sauvegardée : on le vérifie en se demandant si on la garderait soi-même.
