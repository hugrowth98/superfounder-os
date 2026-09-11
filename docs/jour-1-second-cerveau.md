# Jour 1 : le second cerveau

**Ce que vous aurez à la fin** : un dossier que Claude lit avant chaque tâche, qui sait qui vous êtes, ce que vous vendez, à qui, et comment vous parlez. Sans ça, l'IA plafonne à 50 % de qualité : propre, correct, interchangeable. Avec, vous démarrez à 80 %.

**Durée** : 1 h pour le socle (ABOUT.ME), puis 30 à 45 min par fichier de Contexte, à étaler sur quelques jours. Vous le faites une fois, vous le réutilisez à vie.

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

1. **Vérification de la structure.** Elle est livrée avec l'OS. Claude propose d'ajouter des domaines si votre métier en appelle d'autres que Prospection, Contenu, Clients, Stratégie.
2. **CLAUDE.md, le GPS.** Fourni. Claude vous demande seulement vos règles non négociables et ajuste deux sections.
3. **ABOUT.ME, qui vous êtes.** Trois fichiers. `about-me.md` par une interview de 20 questions (faites-la à la voix, en marchant). `my-company.md`, un snapshot daté de votre activité. `anti-ai-voice.md`, fourni, où vous ajoutez vos expressions à vous.
4. **Contexte, la vérité unique.** Sept fichiers, chacun en trois prompts : cadrage, interview, synthèse. Les deux plus importants pour la suite : `Offer-Positioning.md` et `Clients-Problems-and-Messages.md`. Apportez vos transcripts d'appels de vente, c'est la meilleure matière.
5. **Les rituels.** `/done` en fin de session (c'est ce qui garde le cerveau vivant), `/daily-review` le soir, `/weekly-review` le vendredi, `/inbox-processor` quand ça déborde.
6. **Les MCP.** Vos 3 à 5 outils prioritaires, branchés avec `/connect-mcp`.

## Comment vérifier que c'est bon

Ouvrez une nouvelle session et demandez : "Qu'est-ce que tu sais de mes clients ?" Si Claude répond avec leurs mots à eux, le jour 1 est réussi.

## Le principe à retenir

Une information vit à un seul endroit. L'offre est dans `Contexte/Offer-Positioning.md`, nulle part ailleurs. Les jours 2 et 3 viendront la lire, ils ne vous la redemanderont pas.

Suite : [Jour 2, la prospection](jour-2-prospection.md)
