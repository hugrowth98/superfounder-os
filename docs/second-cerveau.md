# Le second cerveau

**Ce que vous aurez à la fin** : un dossier que Claude lit avant chaque tâche, qui sait qui vous êtes, ce que vous vendez, à qui, et comment vous parlez. Sans ça, l'IA plafonne à 50 % de qualité : propre, correct, interchangeable. Avec, vous démarrez à 80 %.

**Durée** : 1 h pour le socle (About-Me), puis 30 à 45 min par fichier de Contexte, à étaler sur quelques jours. Vous le faites une fois, vous le réutilisez à vie.

## Avant de commencer

- Claude Code installé, abonnement Claude payant actif.
- Superfounder OS cloné dans un dossier dédié (pas dans Documents ni sur le Bureau) :

```bash
git clone https://github.com/hugrowth98/superfounder-os.git MonOS
cd MonOS
claude
```

## La phrase à taper

```
Installe mon second cerveau
```

Claude fait un état des lieux, puis vous emmène étape par étape. Vous ne touchez aucun fichier.

## Ce qui se passe

1. **Vérification de la structure.** Elle est livrée avec l'OS : treize dossiers, chacun avec un rôle écrit dans le `CLAUDE.md`. Claude propose d'ajouter un dossier de travail si votre métier en appelle un de plus.
2. **CLAUDE.md, la carte.** Fourni. Claude vous demande seulement vos règles non négociables et ajuste une section.
3. **About-Me, qui vous êtes.** Trois fichiers. `about-me.md` par une interview de 20 questions (faites-la à la voix, en marchant). `my-company.md`, un snapshot daté de votre activité. `anti-ai-voice.md`, fourni, où vous ajoutez vos expressions à vous.
4. **Contexte, la vérité unique.** Sept fichiers, chacun en trois prompts : cadrage, interview, synthèse. Les deux plus importants pour la suite : `Offer-Positioning.md` et `Clients-Problems-and-Messages.md`. Apportez vos transcripts d'appels de vente, c'est la meilleure matière.
5. **Vos clients actifs.** Un dossier par client dans `Produit-Client/`, avec sa note : qui, quelle mission, comment il aime travailler. Trois clients maximum pour commencer.
6. **Les rituels.** `/done` en fin de session (c'est ce qui garde le cerveau vivant), `/weekly-review` le vendredi, `/lint` une fois par mois, `/inbox-processor` quand ça déborde.
7. **Les MCP.** Vos 3 à 5 outils prioritaires, branchés avec `/connect-mcp`.

## Comment vérifier que c'est bon

Ouvrez une nouvelle session et demandez : "Qu'est-ce que tu sais de mes clients ?" Si Claude répond avec leurs mots à eux, le second cerveau est installé.

## Le principe à retenir

Une information vit à un seul endroit. L'offre est dans `Contexte/Offer-Positioning.md`, nulle part ailleurs. La prospection et le contenu viendront la lire, ils ne vous la redemanderont pas.

Suite : [la prospection](prospection.md) ou [le contenu](contenu.md), dans l'ordre que vous voulez.
