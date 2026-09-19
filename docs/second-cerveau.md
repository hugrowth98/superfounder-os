# Le second cerveau

**Ce que vous aurez à la fin** : un dossier que Claude lit avant chaque tâche, qui sait qui vous êtes, ce que vous vendez, à qui, comment vous parlez, et où en est chaque département, projet et client. Sans ça, l'IA plafonne à 50 % de qualité : propre, correct, interchangeable. Avec, vous démarrez à 80 %.

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

1. **Vérification de la structure.** Douze dossiers numérotés, livrés avec l'OS, chacun avec un rôle écrit dans le `CLAUDE.md`. Claude propose d'ajouter ou de retirer un département si votre métier le demande.
2. **CLAUDE.md, la carte.** Fourni. Claude vous demande seulement vos règles non négociables.
3. **About-Me, qui vous êtes.** Trois fichiers. `about-me.md` par une interview de 20 questions (faites-la à la voix, en marchant). `my-company.md`, un snapshot daté de votre activité. `anti-ai-voice.md`, fourni, où vous ajoutez vos expressions à vous.
4. **Contexte, la vérité unique.** Sept fichiers, chacun en trois prompts : cadrage, interview, synthèse. Les deux plus importants pour la suite : `Offer-Positioning.md` et `Clients-Problems-and-Messages.md`. Apportez vos transcripts d'appels de vente, c'est la meilleure matière.
5. **Vos départements et vos projets.** Six fiches livrées (Strategie, Marketing, Go-to-Market, Vente, Produit, Finance-Compta) : vous validez la Mission, vous donnez le chiffre qui compte. Puis vos initiatives en cours, trois maximum, chacune avec sa note et ses Étapes.
6. **Vos clients actifs.** Un dossier par client dans `06_Clients/`, avec sa note : qui, quelle mission, comment il aime travailler. Trois clients maximum pour commencer.
7. **Les rituels.** `/done` en fin de session (c'est ce qui garde le cerveau vivant), `/weekly-review` le vendredi, `/lint` une fois par mois, `/inbox-processor` quand ça déborde, `/import` pour un gros lot, `/create-skill` quand une tâche se répète.
8. **Les MCP.** Vos 3 à 5 outils prioritaires, branchés avec `/connect-mcp`.

## La forme d'une fiche

Chaque département, projet et client a une note courte, six sections maximum : Mission, Périmètre et Objectif (pour un département), Cadre, Étapes (pour un projet ou un client), Où on en est, Key Notes. Vous écrivez les premières. `/done` réécrit Où on en est à chaque session, date les décisions dans Cadre et coche les Étapes. L'historique complet vit dans le journal et dans le `_log.md` du dossier.

## Comment vérifier que c'est bon

Ouvrez une nouvelle session et demandez : "Où en est-on sur mes projets ?" Si Claude répond avec les Étapes cochées et la prochaine action de chacun, le second cerveau est installé.

## Le principe à retenir

Une information vit à un seul endroit, et ce qui n'est pas écrit n'existe pas. Chaque session finit par `/done`.
