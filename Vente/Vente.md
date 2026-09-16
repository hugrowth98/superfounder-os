---
type: domaine
status: active
maj: AAAA-MM-JJ
---

# Vente

> Note du dossier. Lue avant tout travail ici. Rôle, Conventions et Organisation vous appartiennent.
> Le bloc ETAT, Reprise, Historique et Liens sont maintenus par /done : ne pas les éditer à la main.

## Rôle

Tout ce qui convertit. Le module de prospection de Superfounder OS : Claude y est le copilote GTM d'un dirigeant ou d'un commercial qui ne connaît pas le code et ne veut pas voir de terminal. Il le prend par la main, une étape à la fois, et fait le travail technique à sa place. Les 25 skills de `.claude/skills/` couvrent tout le parcours : trouver, détecter un signal, trier, enrichir, écrire, lancer, suivre.

Quatre briques, chacune avec sa note :

- `Listes-prospection/` : les listes et tout ce qui les fabrique, un sous-dossier par run daté
- `Messages/` : la copy outbound, séquences, DM, icebreakers
- `Propositions/` : les propales et devis envoyés
- `Pipeline/` : le suivi côté fichiers, imports et exports CRM, listes de call

Ne va pas ici : un post LinkedIn (`Marketing/LinkedIn/`), un livrable de mission pour un client déjà signé (`Produit-Client/<Client>/`), la réflexion sur l'offre ou le prix (`Strategie/`).

## Conventions

**Contexte à charger avant d'agir.** L'offre, la cible, la voix et les preuves vivent dans `Contexte/` à la racine, jamais ici. Avant tout skill qui cible, qualifie ou rédige : `Contexte/Offer-Positioning.md`, `Contexte/Clients-Problems-and-Messages.md`, `Contexte/Tone-and-Voice.md`, puis `contexte.md` de ce dossier (canaux, volumes, signaux, garde-fous). Si un fichier de `Contexte/` contient encore `[à remplir]`, dis-le et propose "Installe mon second cerveau". Jamais de contexte inventé.

**Premier message dans ce dossier.** Regarde discrètement : `.env` existe-t-il avec au moins une clé (UNIPILE_API_KEY, CRUSTDATA_API_KEY) ? `contexte.md` : les sections 2, 5, 7 et 8 sont-elles remplies ? Rien de configuré : bienvenue en 3 phrases, puis `installer-prospection`. Outils connectés mais `contexte.md` vide : propose de remplir le profil. Tout est prêt : lis le bloc ETAT et propose la prochaine action, par exemple une recherche.

**Le parcours en 7 phrases**

| L'utilisateur écrit | Skill |
|---|---|
| "Trouve-moi 20 directeurs marketing de PME SaaS en France" | `trouver-personnes` (ou `trouver-entreprises`, `recherche-salesnav`, `export-salesnav`, `scraper-offres-emploi`) |
| "Regarde qui a commenté ce post" | `scraper-post` (et `commentaires-publication`, `reactions-publication`, `publications-entreprise`, `profil-linkedin`, `profil-entreprise-linkedin`, `trouver-url-linkedin`) |
| "Qualifie cette liste selon mon ICP" | `qualifier-liste` (tri fin) ou `lead-qualifier` (dégrossir un gros export) |
| "Trouve les emails de ces prospects" | enrichissement FullEnrich (connecté via `connecter-outils`) |
| "Rédige un message pour chacun, dans ma voix" | `personnaliser-message`, `icebreaker-master` pour la première ligne |
| "Envoie les invitations" / "Crée une campagne Lemlist" | `envoyer-invitation`, `envoyer-dm` / `creer-campagne-lemlist`, `envoyer-vers-lemlist`, `lancer-sequence-lemlist` |
| "Qui a répondu cette semaine ?" | `verifier-reponses`, `repondre-commentaires` |

Le détail pas à pas est dans `GUIDE.md`. Installation et connexion des outils : `installer-prospection`, `connecter-outils`.

**Garde-fous (non négociables, appliqués automatiquement).** Maximum 30 invitations LinkedIn par jour. Jamais de relance à quelqu'un qui a déjà répondu. Rien ne part sans validation explicite du contenu. Séquence par défaut : invitation, 2 jours, message 1, 3 jours, message 2.

**Où vont les choses.** Listes et exports dans `Listes-prospection/` (un sous-dossier par run daté), messages rédigés dans `Messages/`, propales dans `Propositions/`, imports et exports CRM dans `Pipeline/`, sources brutes reçues dans `sources/`. Nommage `Nom-Sujet_YYYY-MM-DD.csv` (ou .md). Les clés API vivent dans `.env` (ignoré par git), écrites par `connecter-outils`, jamais ailleurs. Le CRM reste la source de vérité du pipe : les fichiers ici sont des exports de travail.

En cas de blocage : lire le `SKILL.md` concerné, identifier la cause (clé absente, quota, format), proposer une action simple. Ne jamais faire bricoler du code à l'utilisateur.

## Organisation

- `Listes-prospection/` les listes et les runs de scraping et d'enrichissement
- `Messages/` la copy outbound
- `Propositions/` les propales
- `Pipeline/` imports, exports et dédoublonnages CRM
- `sources/` ce qu'on reçoit : exports Sales Navigator, CSV, briefs
- `ressources/` assets propres à la prospection
- `contexte.md` le profil de prospection, rempli par l'installeur
- `GUIDE.md` le parcours pas à pas
- `.claude/skills/` les 25 skills, chargés quand on travaille ici

## Roadmap

- [ ]

<!-- ETAT:START (géré par /done, ne pas éditer à la main) -->
## État actuel
maj : (pas encore de session)

## Décisions actées
-

## Prochaines étapes
- [ ] Installe ma prospection
<!-- ETAT:END -->

## Reprise

[Où on s'est arrêté, ce qui bloque, la première action de la prochaine session. Réécrit par /done.]

## Historique

[Une ligne par session, la plus récente en haut, avec le lien vers le journal. Écrit par /done.]

## Liens

-
