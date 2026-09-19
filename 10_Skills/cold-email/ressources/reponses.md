# Répondre aux réponses

Une réponse est un autre genre que l'email à froid. Pas de limite de mots de séquence, jamais de variante en rotation, jamais de template envoyé tel quel. La première phrase répond à ce que la personne a écrit. Un paragraphe de fond. Une seule action suivante, alignée sur son intention.

`verifier_reponses` (skill `verifier-reponses`) remonte qui a répondu et sur quel canal ; la personne sort de la séquence le jour même ; la réponse part depuis la boîte de l'expéditeur, à la main ou via Lemlist, jamais en automatique.

## 1. Le déroulé d'une réponse positive

1. Accuser réception de l'intérêt ou de la demande exacte.
2. Répondre à la question immédiate en premier.
3. Fournir ce qui a été promis seulement si c'est prêt et présent ; sinon, dire quand.
4. Orienter vers une seule action suivante, celle qui colle à son intention.
5. Sourcer toute affirmation nouvelle.

Règle absolue : ne jamais écrire "ci-joint", "en lien", "envoyé" ou "prévu le" si la pièce, le lien ou le créneau n'existe pas dans le contexte de travail. Dans ce cas, rendez `contexte_insuffisant` et nommez ce qui manque hors du brouillon destiné au prospect.

## 2. Le routage selon la réponse

| Il écrit | Vous faites |
|---|---|
| "Envoyez-moi de la doc" | envoyer la ressource avant de demander un rendez-vous |
| une question factuelle | répondre d'abord, proposer ensuite |
| "On peut se parler" | un chemin précis pour caler l'échange |
| "Ce n'est pas moi" | remercier, demander le bon rôle ou le bon contact |
| "Pas maintenant" | confirmer une date de reprise raisonnable |
| "Pas intéressé" | respecter, confirmer qu'on n'insistera pas |
| une objection | reconnaître sans pression, un fait qui la lève si on l'a, sinon clore poliment |

## 3. Les réponses types

Des squelettes à réécrire dans la voix de `05_Departements/Go-to-Market/contexte.md`. Les chiffres et noms sont fictifs.

### Intéressé ("ça m'intéresse, dites-m'en plus")

```
Merci {{prenom}}.

En deux lignes : {{ce que vous faites pour son cas précis, en résultat et en délai}}. Pour {{client_similaire}}, ça a donné {{resultat}} en {{delai}}.

Le plus simple pour voir si ça s'applique chez {{entreprise}} : 20 minutes en visio, je regarde {{son cas}} avec vous. Jeudi 10h ou vendredi 14h ?
```

Deux créneaux précis, pas un lien d'agenda sec. Le lien vient en second si la personne préfère.

### "Envoyez-moi de la doc"

```
Bien sûr {{prenom}}. Voici {{nom exact de la ressource}} : {{lien ou pièce présente}}.

Il couvre {{contenu réel, deux ou trois points}}. La partie {{section}} est celle qui correspond le mieux à {{son cas}}.

Si vous voulez qu'on regarde comment ça s'applique chez {{entreprise}}, dites-le moi et je vous propose un créneau. Sinon, bonne lecture.
```

La doc part d'abord, le rendez-vous vient après. Si la ressource n'existe pas encore : "Je vous l'envoie {{jour précis}}" et une tâche créée.

### Pas maintenant ("revenez vers moi dans 3 mois")

```
Entendu {{prenom}}, je reviens vers vous {{mois précis}}.

D'ici là, une chose qui peut servir sans engagement : {{ressource ou conseil concret}}.

Bon {{trimestre, été, lancement}}.
```

Notez la date dans le CRM (`dedoublonner` / HubSpot) et retirez la personne des séquences jusqu'à cette date. Un "pas maintenant" relancé avant la date devient un "plus jamais".

### Pas le bon contact ("ce n'est pas moi qui gère ça")

```
Merci de me le dire {{prenom}}. Qui suit {{sujet}} chez {{entreprise}} ? Un prénom suffit, je m'occupe du reste.

Et si ça vous arrange, je peux lui écrire en mentionnant que vous m'avez orienté.
```

Ne jamais écrire au collègue "X m'a dit de vous contacter" sans son accord explicite dans la réponse.

### Objection ("on a déjà un prestataire / un outil")

```
Logique, {{prenom}}, et je ne cherche pas à le remplacer demain.

Ce que je vois chez ceux qui ont {{solution en place}} : {{une limite précise, sourcée}}. Si ce n'est pas votre cas, tant mieux, vous êtes bien équipé.

Si ça l'est un jour, {{client_similaire}} a fait la bascule en {{delai}} sans interruption. Je vous laisse mon contact pour ce moment-là.
```

Un seul fait, pas un argumentaire. Une objection sur le prix se traite avec le calcul (`frameworks-13.md`, Faites le calcul) et jamais avec une remise dans un email.

### Pas intéressé

```
Compris {{prenom}}, merci d'avoir pris le temps de répondre. Je ne reviendrai pas vers vous sur ce sujet.

Bonne continuation.
```

Aucun second pitch caché. La personne passe en `ne_plus_contacter`.

### "Comment vous avez eu mon email ?"

```
Bonne question {{prenom}}. Votre adresse vient de {{source réelle : annuaire professionnel, votre profil public, un outil de recherche B2B}}, et je vous ai écrit parce que {{le lien avec sa fonction}}.

Si vous préférez ne plus recevoir de message de ma part, dites-le moi et je vous retire de ma liste aujourd'hui.
```

Répondre en 24 heures, sans se justifier au-delà. Le détail des obligations est dans `delivrabilite.md` (section RGPD).

### Le no-show (rendez-vous manqué)

```
{{prenom}}, on avait un créneau à {{heure}}. Rien de grave j'imagine, ces choses-là arrivent.

{{jour}} à {{heure}} ou {{jour}} à {{heure}}, lequel vous arrange ?
```

Une relance, deux créneaux, pas de reproche. Sans réponse après deux jours, un dernier message avec la ressource promise et la porte ouverte.

## 4. Les réponses de rattrapage

**Preuve manquante.** Dites ce que vous ne pouvez pas confirmer et quelle source il faudrait. Ne devinez pas pour garder l'élan.

**Demande mal comprise.** Reformulez brièvement le besoin corrigé, répondez, sans défendre le message précédent.

**Erreur de votre part** (mauvais prénom, mauvaise entreprise, fait faux). Une phrase d'excuse, la correction, et rien d'autre. "Mauvaise variable de mon côté, désolé. Ce que je voulais vous dire tient en une ligne : {{le point}}." Pas de justification technique.

## 5. Les messages selon le statut d'un lead entrant

Pour les leads qui viennent à vous (formulaire, téléchargement, inscription), un canal court (email, LinkedIn, WhatsApp si la personne l'a donné). Deux à quatre lignes, vouvoiement, direct, sans emoji, et un seul but : caler le rendez-vous.

| Statut | Message |
|---|---|
| Formulaire commencé, pas terminé | accuser le formulaire, une ligne sur ce qu'on fait, proposer de finir en 2 minutes ensemble |
| Formulaire terminé, pas de rendez-vous | reprendre la priorité qu'il a indiquée, proposer deux ou trois créneaux, CTA direct |
| Rendez-vous pris | donner le déroulé, poser une question de préparation, créer le lien ; ne rien revendre |
| Appel tenté sans réponse | le mentionner en une ligne, passer à l'email pour caler |
| LinkedIn | n'en parler que si l'invitation a bien été envoyée |

Objets pour ces messages : courts, fonctionnels, contextuels. "Suite à votre demande", "Prochaine étape", "Votre créneau de jeudi".

## 6. Les contrôles d'une réponse

- La première phrase répond au message du prospect.
- La réponse contient une action suivante, une seule.
- Ce qui est promis est présent, ou l'envoi est bloqué jusqu'à ce qu'il le soit.
- Chaque "joint", "lien", "envoyé", "prévu" correspond à une pièce réelle.
- Aucune affirmation nouvelle sans source.
- Aucune limite de séquence ni variante en rotation appliquée.
- Réponse dans les 24 heures ouvrées ; dans l'heure pour un "intéressé".
