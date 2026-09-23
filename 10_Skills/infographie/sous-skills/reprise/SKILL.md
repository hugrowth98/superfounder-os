---
name: reprise
description: >
  Reprend une infographie existante (une image, un carrousel, un visuel vu dans la veille) ou un
  post LinkedIn et le rend en trois infographies 1080x1350 à la charte de `03_Branding/`, chacune
  dans une structure différente, par un rendu HTML déterministe (Chrome headless), sans IA
  d'image : les couleurs, les polices et le texte sont exacts et se corrigent en dix secondes.
  Se déclenche sur : "reprends cette infographie", "refais ce visuel à ma charte", "trois
  versions de ce visuel", "décline ce post en infographies", "à partir de cette image", ou
  toute image d'infographie déposée avec une demande de reproduction. Ne pas utiliser pour un
  visuel sans modèle à partir d'une idée (`brief-visuel` puis `infographie-editoriale`), ni
  pour un rendu manuscrit ou tableau blanc.
---

> Sous-skill du master `infographie`. `SKILL_BASE` est le dossier du master (Glob sur `**/infographie/SKILL.md`) : les scripts sont dans `{SKILL_BASE}/scripts/`, le format des données dans `{SKILL_BASE}/ressources/format-donnees.md`.

# Reprise : un visuel qui a marché, refait à votre charte, en trois structures

Une image d'infographie en entrée, trois PNG en sortie. Le rendu est du HTML : la charte est respectée au pixel, et changer un mot ne relance pas une génération aléatoire. C'est l'exception à la règle "une image à la fois" du master : trois structures d'un coup, parce que le rendu est gratuit et déterministe.

## Ressources

- `{SKILL_BASE}/ressources/lecture-charte.md` : la charte fait foi ; vide, le style éditorial neutre.
- `{SKILL_BASE}/ressources/format-donnees.md` : le `data.json`, les huit gabarits, la règle des trois structures.
- `{SKILL_BASE}/ressources/bibliotheque-structures.md` : les quinze structures d'origine.
- `{SKILL_BASE}/ressources/copywriting-visuel.md` : si un texte dépasse une ligne.
- `01_About-Me/anti-ai-voice.md` : la relecture.

## Méthode

1. **Lire l'entrée en entier.** Une image : la lire avec l'outil de lecture d'image (réduire à 1 200 px avant si elle est lourde) et inventorier tout ce qu'elle contient : titre, sous-titre, chaque item avec son numéro, son nom, sa ligne technique, sa description, sa citation, les labels, le footer, le CTA. Rien n'est résumé à cette étape. Un post : le texte, la structure implicite, les items. Un carrousel : chaque page.
2. **Traduire en gardant les termes techniques.** Dans la langue de l'utilisateur (`Tone-and-Voice.md`), vouvoiement. Restent tels quels : noms de produits et de fonctions, commandes, termes du métier sans équivalent installé (prompt, hook, pipeline, outbound, funnel), noms propres, chiffres. Une citation reste une citation. Aucun tiret cadratin.
3. **Lire la charte** : `python3 {SKILL_BASE}/scripts/rendre_infographie.py --charte` affiche ce que le script en lit (palette par rôle, typographies, logo). Si tout est neutre, une question : "Vos couleurs et votre police, en une ligne ? Sinon je pars sur le style éditorial neutre." La palette de la charte se lit ainsi : fond principal, fond des cartes, fond des blocs (le bloc plein), texte principal, texte secondaire, accent principal (l'accent du titre, les commandes, les chiffres), accent secondaire (la pilule CTA ; sinon l'accent principal).
4. **Choisir les trois gabarits** avec la règle de `format-donnees.md` (la fidèle, la lisible, la réorganisée) et regarder ce qui existe déjà dans `05_Departements/Marketing/LinkedIn/` pour ne pas refaire trois fois la même chose. Dites les trois choix et pourquoi en deux lignes ; si l'utilisateur a demandé un lot, ne redemandez pas.
5. **Écrire `data.json`** dans `05_Departements/Marketing/LinkedIn/Infographie-<sujet>_<AAAA-MM-JJ>/`. L'accent du titre est une phrase complète. Le CTA est un placeholder à signaler tant que l'utilisateur n'a pas tranché entre commentaire-gate et lien en clair.
6. **Rendre** : `python3 {SKILL_BASE}/scripts/rendre_infographie.py <dossier>/data.json --gabarits <g1> <g2> <g3>`. Sans Chrome ni Chromium, le script écrit les HTML et le dit : l'utilisateur les ouvre et fait une capture 1080x1350.
7. **Vérifier en lisant les PNG**, dans cet ordre : le footer (logo, pilule) est visible et ne touche pas un bloc plein ; aucun texte coupé, aucune carte vide en bas ; un seul bloc plein au plus ; l'accent du titre est une phrase ; aucune icône, pastille, emoji, dégradé. Un débordement se corrige dans `data.json` (texte plus court) ou par `"densite": "serre"`. Relancer, relire. Ne pas livrer un PNG non relu.
8. **Livrer** : les trois PNG, le `data.json`, et une `fiche.md` (source, auteur, engagement, structures choisies, placeholders à valider). Finir par les liens et ce qui reste à trancher (titre, CTA).

## Règles

- Le skill n'invente ni chiffre, ni source, ni item absent de l'original.
- Il ne choisit pas à la place de l'utilisateur entre commentaire-gate et lien en clair.
- Il ne génère aucune image par IA ; pour un visuel photo ou une illustration, le master.
- `03_Branding/` est une zone protégée : proposer d'y écrire la charte si elle est vide, ne rien y écrire sans un oui.
- Logo : si `charte-visuelle.md` donne un fichier existant, il s'affiche en bas à gauche ; sinon le footer ne porte que la pilule.

## Exemples

- "Reprends cette infographie" avec une image de douze cartes : inventaire, traduction, `grille` (fidèle), `glossaire` (lisible), `systeme` en quatre familles (réorganisée) ; réponse attendue : trois PNG, le `data.json`, le CTA marqué placeholder.
- "Décline ce post en infographies" avec un post en cinq étapes : `etapes`, `grille`, `funnel` ; réponse attendue : trois PNG et la question sur le titre.
- "Le numéro 2 des hot takes de la veille, à ma charte" : l'image vient de `sources/veille-createurs_*/images/HOT02_img1.jpg`, le texte de `posts.json` ; même chaîne.
