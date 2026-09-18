---
name: connecter-outils
description: >
  Skill pour connecter, un par un, tous les outils du module de prospection (Unipile, Crustdata, FullEnrich,
  Lemlist, Apify) directement depuis le chat, sans terminal ni edition de fichier a la main
  pour l'utilisateur. Utilise ce skill au tout debut, avant tout autre skill, ou des que
  l'utilisateur veut brancher/reconnecter un outil. Se declenche sur : "connecte mes
  outils", "Installe ma prospection", "configure mes clés API", "branche Unipile/Crustdata/
  FullEnrich/Lemlist/Apify".
---

# Connecter les outils du module de prospection (pour profils non-dev)

## Principe

L'utilisateur ne touche jamais un terminal ni un fichier `.env` a la main. Pour chaque
outil : lui donner le lien exact, il copie-colle la valeur demandee ici dans le chat, et
c'est **toi** (Claude Code) qui ecris le `.env` (via l'outil Edit/Write) ou qui lances la
commande de connexion (via l'outil Bash). Toujours verifier avec un vrai appel API avant de
passer a l'outil suivant, et corriger immediatement si ca ne marche pas.

Faire les 5 outils un par un, dans cet ordre. Ne pas passer au suivant tant que le precedent
n'est pas verifie comme fonctionnel (sauf si l'utilisateur veut sauter un outil, auquel cas
le laisser vide et continuer).

---

## Outil 1 : Unipile (LinkedIn + Sales Navigator)

### Etape 1 - Compte et cles

Dire a l'utilisateur :
> "Va sur [dashboard.unipile.com/signup](https://dashboard.unipile.com/signup) et cree ton
> compte (ou connecte-toi si tu en as deja un).
> Une fois connecte, deux choses a recuperer :
> 1. Le **DSN**, affiche directement sur ta page de profil (format
>    `https://apiXX.unipile.com:XXXXX`)
> 2. L'**Access Token** (c'est la cle API), a generer sur
>    [dashboard.unipile.com/access-tokens](https://dashboard.unipile.com/access-tokens)
> Colle-moi les deux ici."

### Etape 2 - Ecrire dans .env

Des reception, ecrire dans `.env` (creer le fichier a partir de `.env.example` s'il
n'existe pas encore) :
```
UNIPILE_API_KEY=<valeur collee>
UNIPILE_DSN=<valeur collee, avec le https:// devant>
```

### Etape 3 - Connecter le compte LinkedIn (etape a ne pas sauter)

Une cle API seule ne suffit pas : il faut aussi autoriser Unipile a agir sur le compte
LinkedIn de l'utilisateur. Dire :
> "Dernier point cote Unipile : retourne sur ton dashboard, section **Accounts**, clique sur
> **Connect an account**, choisis **LinkedIn**, puis la methode **Credential**. Rentre ton
> email et ton mot de passe LinkedIn. LinkedIn va t'envoyer un code de verification par mail
> : va le chercher et recopie-le pour valider. Dis-moi quand c'est fait."

### Etape 4 - Verifier et recuperer les identifiants techniques

Une fois l'utilisateur confirme, appeler :
```bash
curl -sS -H "X-API-KEY: $(grep UNIPILE_API_KEY .env | cut -d= -f2-)" \
  "$(grep UNIPILE_DSN .env | cut -d= -f2-)/api/v1/accounts"
```
Verifier que la reponse contient un compte `"type":"LINKEDIN"` avec `"status":"OK"`. En
extraire :
- `id` (racine de l'objet compte) -> a ecrire dans `.env` comme `UNIPILE_ACCOUNT_ID`
- `connection_params.im.id` -> c'est le `provider_id` propre a l'utilisateur, necessaire
  pour `verifier-reponses`/`repondre-commentaires`. Le noter et le proposer a l'utilisateur
  de l'ajouter aussi en variable `UNIPILE_OWN_PROVIDER_ID` dans `.env` pour ne pas avoir a
  le rechercher a chaque fois.

Si le statut n'est pas `OK` (ex: `CREDENTIALS`), dire a l'utilisateur de recommencer la
connexion du compte LinkedIn (etape 3).

---

## Outil 2 : Crustdata (donnees entreprises et personnes)

### Etape 1 - Compte et cle

Dire :
> "Va sur [app.crustdata.com](https://app.crustdata.com), cree un compte, puis recupere ta
> cle API sur [app.crustdata.com/api-keys](https://app.crustdata.com/api-keys). Colle-la
> ici."

### Etape 2 - Ecrire dans .env

```
CRUSTDATA_API_KEY=<valeur collee>
```

### Etape 3 - Verifier

```bash
curl -sS -H "Authorization: Token $(grep CRUSTDATA_API_KEY .env | cut -d= -f2-)" \
  https://api.crustdata.com/user/credits
```
Une reponse `{"credits": <nombre>}` confirme que la cle fonctionne. Annoncer le solde a
l'utilisateur.

---

## Outil 3 : FullEnrich (emails et telephones)

Pas de cle a copier : connexion via serveur MCP officiel.

### Etape 1 - Lancer la connexion (toi, pas l'utilisateur)

```bash
claude mcp add --transport http fullenrich https://mcp.fullenrich.com/mcp
```

### Etape 2 - Authentification

Le serveur passe en statut "Needs authentication" tant que l'OAuth n'est pas complete.
Dire a l'utilisateur : "Je viens de lancer la connexion a FullEnrich. Essaie de me demander
un truc lie a FullEnrich (ex: 'verifie mes credits FullEnrich') : ca devrait ouvrir une
fenetre dans ton navigateur pour te connecter a ton compte FullEnrich et autoriser l'acces."

**Non teste de bout en bout au moment de la redaction de ce skill** : si l'authentification
ne se declenche pas comme prevu, verifier `claude mcp get fullenrich` pour le statut, et a
defaut orienter l'utilisateur vers <https://help.fullenrich.com/en/articles/14190120-mcp-server>.

### Etape 3 - Verifier

Une fois le statut "Connected" (`claude mcp list`), chercher les outils disponibles (ils
apparaissent avec un nom lie a fullenrich) et faire un appel simple (verification de
credits ou recherche) pour confirmer que ca repond.

---

## Outil 4 : Lemlist (campagnes email/multicanal)

Pas de cle a copier non plus : connexion via serveur MCP officiel.

### Etape 1 - Lancer la connexion (toi, pas l'utilisateur)

```bash
claude mcp add --transport http lemlist https://app.lemlist.com/mcp
```

Si le message `MCP server lemlist already exists` apparait, c'est deja connecte : passer
directement a la verification.

### Etape 2 - Authentification

Meme principe que FullEnrich : au premier usage reel d'un outil Lemlist, une fenetre de
connexion OAuth s'ouvre dans le navigateur de l'utilisateur pour choisir son equipe et
autoriser l'acces.

### Etape 3 - Verifier

Chercher les outils Lemlist disponibles (prefixe `lemlist`) et appeler un outil de lecture
simple (ex: lister les campagnes existantes) pour confirmer la connexion.

---

## Outil 5 : Apify (scraping et automatisation web)

Pas de cle a copier : connexion via serveur MCP officiel, meme principe que FullEnrich et
Lemlist.

### Etape 1 - Lancer la connexion (toi, pas l'utilisateur)

```bash
claude mcp add --transport http apify https://mcp.apify.com
```

Si le message `MCP server apify already exists` apparait, c'est deja connecte : passer
directement a la verification.

### Etape 2 - Authentification

Meme principe que FullEnrich et Lemlist : au premier usage reel d'un outil Apify, une fenetre
de connexion OAuth s'ouvre dans le navigateur de l'utilisateur pour autoriser l'acces a son
compte Apify.

### Etape 3 - Verifier

Chercher les outils Apify disponibles (prefixe `apify`) et appeler un outil de lecture simple
pour confirmer la connexion.

---

## A la fin

Resumer a l'utilisateur l'etat des 5 outils (connecte / a refaire), et proposer de
commencer le parcours GUIDE.md a l'etape 3 (remplir `Vente/contexte.md` via `installer-prospection`).
