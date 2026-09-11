# Jour 2 : la prospection

**Ce que vous aurez à la fin** : une liste de prospects ciblés, triés, enrichis, avec des messages écrits dans votre voix, envoyés en campagne, avec un suivi des réponses. Le tout piloté en phrases, sans terminal.

**Durée** : 45 min d'installation (dont la connexion des outils), puis 15 min par session de prospection.

## Avant de commencer

- Le jour 1 est fait : `Contexte/Offer-Positioning.md`, `Clients-Problems-and-Messages.md` et `Tone-and-Voice.md` sont remplis. La prospection les lit, elle ne vous les redemande pas.
- Selon vos canaux, un compte sur : Unipile (LinkedIn), Crustdata (recherche), FullEnrich (emails), Lemlist (campagnes email), Apify (scraping). Vous pouvez démarrer avec un seul et brancher les autres plus tard.

## La phrase à taper

Ouvrez `Projects/Prospection/` dans Claude Code, puis :

```
Installe ma prospection
```

## Ce qui se passe

1. Claude lit votre second cerveau et ne vous pose que les questions propres à la prospection : zone géographique, signaux de bon moment, tutoiement ou vouvoiement, volume visé, canal, comptes à ne jamais contacter.
2. Il écrit le profil de prospection (`contexte.md`) et vous le fait valider.
3. Il connecte vos outils un par un. Vous collez les clés dans le chat, il écrit le `.env`.
4. Il propose une première recherche.

## Le parcours en 7 phrases

| Vous écrivez | Ce qui se passe |
|---|---|
| "Trouve-moi 20 directeurs marketing de PME SaaS en France" | recherche par critères, export CSV |
| "Regarde qui a commenté ce post" | les gens qui commentent un post sur votre sujet sont plus réceptifs qu'une liste froide |
| "Qualifie cette liste selon mon ICP" | tri selon `Contexte/`, avec la raison de chaque exclusion |
| "Trouve les emails de ces prospects" | enrichissement, emails et téléphones vérifiés |
| "Rédige un message pour chacun, dans ma voix" | un message par prospect, à partir de son profil et de votre positionnement |
| "Envoie les invitations à cette liste" ou "Crée une campagne Lemlist" | LinkedIn ou email, après votre validation |
| "Qui a répondu cette semaine ?" | suivi, et jamais de relance à quelqu'un qui a répondu |

## Les garde-fous

Ils sont appliqués automatiquement, vous ne pouvez pas déraper : 30 invitations LinkedIn par jour maximum, jamais de relance à quelqu'un qui a répondu, rien ne part sans votre "oui" explicite.

## Le principe à retenir

Le module remplit le pipeline. Il ne remplace pas le téléphone. Il sert à ce que vous ayez toujours quelqu'un à appeler.

Suite : [Jour 3, le contenu](jour-3-contenu.md)
