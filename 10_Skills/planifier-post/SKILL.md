---
name: planifier-post
description: >
  Programme un post LinkedIn validé sur Publora (l'outil de programmation branché par
  `connecter-outils`), à la date et à l'heure choisies, avec les contrôles de bonnes pratiques
  du master `linkedin` (longueur, hook, lien en premier commentaire, créneau, collision avec un
  autre post), une pièce jointe (image ou PDF de carrousel), puis tient le calendrier local et
  poste le premier commentaire après publication. Se déclenche sur : "programme ce post",
  "planifie pour mardi 8h", "mets-le en brouillon", "qu'est-ce qui est programmé", "décale le
  post de jeudi", "annule le post", "poste le premier commentaire", "les stats de mon post".
  Ne pas utiliser pour écrire le post (master `linkedin`) ni pour choisir la cadence
  (sous-skill `publier`). Rien ne part sans le oui de l'utilisateur sur le texte, la date et
  le compte.
---

## Outil

Publora, par son API (`PUBLORA_API_KEY` dans `.env`, en-tête `x-publora-key`, base `https://api.publora.com/api/v1`), avec le client `Publora` de `10_Skills/_commun/gtm_common.py`. Le compte LinkedIn est connecté une fois dans le tableau de bord Publora (OAuth) ; l'API ne sait pas le connecter. Abonnement, aucun coût par appel : palier gratuit de 15 posts par mois, Pro pour l'illimité. Le MCP Publora est optionnel : ce skill passe par l'API pour rester lisible et rejouable.

## Installation, si Publora n'est pas branché

Le skill le voit à la première commande (`PUBLORA_API_KEY` absent, ou aucun compte LinkedIn dans la réponse). Dans ce cas, guidez l'utilisateur, une étape à la fois, comme `connecter-outils` le fait pour les outils de prospection :

1. **Le compte** : publora.com, créer un compte (gratuit pour commencer).
2. **Le profil LinkedIn** : dans le tableau de bord, menu Connections, bouton LinkedIn, autoriser. C'est la seule étape qui ne passe pas par le chat.
3. **La clé** : menu API (ou Settings, API Keys), Generate API Key, copier tout de suite : elle n'est affichée qu'une fois. L'utilisateur la colle dans le chat.
4. **L'écriture** : `python3 10_Skills/connecter-outils/scripts/verifier_connexions.py --set PUBLORA_API_KEY=<clé>` (jamais affichée, jamais dans un skill), puis `--outil publora` pour le test (appel gratuit : la clé est valide, les comptes connectés s'affichent avec l'état du jeton) et `--ecrire-outils` pour cocher la ligne Publora dans `05_Departements/Go-to-Market/OUTILS.md`.
5. **La vérification** : `python3 {ce dossier}/scripts/planifier_post.py --comptes` puis `--test`. Un jeton `expired` ou `expiring_soon` : reconnecter LinkedIn dans le tableau de bord.

Sans Publora, le skill ne programme rien : il livre le post prêt à coller et l'heure conseillée, et l'utilisateur programme dans LinkedIn (programmation native, jusqu'à trois mois à l'avance).

## Entrée

- Le post validé : un fichier `05_Departements/Marketing/LinkedIn/Post-<Sujet>_<date>.md` (le script lit le bloc "POST COMPLET", sinon le corps sans frontmatter) ou le texte lui-même (`--texte`).
- La date et l'heure locales (`--quand "AAAA-MM-JJ HH:MM"`, fuseau `Europe/Paris` par défaut, `--fuseau` sinon), ou `--brouillon`.
- Facultatif : `--media` (image ou PDF de carrousel, répétable), `--premier-commentaire` (le lien ou le complément à poster après publication), `--compte` si plusieurs profils LinkedIn sont connectés, `--sujet` pour le calendrier.

## Sortie

- Le post créé chez Publora (`postGroupId`), programmé ou en brouillon, avec l'heure effectivement enregistrée.
- Une ligne dans `05_Departements/Marketing/LinkedIn/Calendrier-publication.md` (programmé pour, compte, sujet, postGroupId, statut, premier commentaire), statuts rafraîchis par `--liste`.
- Après publication : le premier commentaire (`--commenter`), les statistiques (`--stats` : impressions, personnes atteintes, réactions, commentaires, partages ; mises en cache deux heures par Publora).

## Procédure

1. Le post est validé par l'utilisateur (texte final, sous-skill `optimiser` passé si besoin). Sinon, retour au master `linkedin`.
2. La date vient du sous-skill `publier` (cadence et créneaux) ou de l'utilisateur. Le script refuse une heure à moins de 15 minutes et signale un créneau hors des fenêtres conseillées.
3. `--dry-run` d'abord : le script affiche le compte, l'heure locale et UTC, la longueur, le hook, les pièces jointes, le premier commentaire, et ses contrôles :
   - bloquants (rien ne part) : texte vide, plus de 3 000 caractères, tiret cadratin ou demi-cadratin, média non pris en charge ;
   - avertissements (à corriger, ou `--force`) : premier paragraphe de plus de 210 caractères, lien dans le corps, hashtag en ouverture, plus de 3 emojis, texte très court, créneau hors fenêtre ou week-end.
4. Montrez le résultat, attendez le oui sur le texte, la date et le compte.
5. Relancez sans `--dry-run`. Avec un média : brouillon, téléversement (URL présignée, PUT, vérification), puis programmation. Le script signale un autre post déjà programmé à moins de 20 heures sur le même compte.
6. Le jour J, après la publication : `--commenter <postGroupId> --texte "..."` pour le premier commentaire (le lien), puis les 60 à 90 premières minutes en présence (sous-skill `engagement`). `--liste` met les statuts du calendrier à jour ; `--stats` lit les chiffres, à reporter dans `posts-de-reference.md` via le sous-skill `performance`.

## Commandes

```bash
python3 10_Skills/planifier-post/scripts/planifier_post.py --comptes
python3 10_Skills/planifier-post/scripts/planifier_post.py --test
python3 10_Skills/planifier-post/scripts/planifier_post.py --post "05_Departements/Marketing/LinkedIn/Post-Signaux_2026-09-22.md" --quand "2026-09-23 08:00" --dry-run
python3 10_Skills/planifier-post/scripts/planifier_post.py --post <fichier.md> --quand "2026-09-23 08:00" --premier-commentaire "Le guide complet : https://..."
python3 10_Skills/planifier-post/scripts/planifier_post.py --post <fichier.md> --media carrousel.pdf --quand "2026-09-24 08:00"
python3 10_Skills/planifier-post/scripts/planifier_post.py --texte "..." --brouillon
python3 10_Skills/planifier-post/scripts/planifier_post.py --liste --jours 14
python3 10_Skills/planifier-post/scripts/planifier_post.py --decaler <postGroupId> --quand "2026-09-25 08:00"
python3 10_Skills/planifier-post/scripts/planifier_post.py --annuler <postGroupId>
python3 10_Skills/planifier-post/scripts/planifier_post.py --commenter <postGroupId> --texte "..."
python3 10_Skills/planifier-post/scripts/planifier_post.py --stats <postGroupId>
```

## Garde-fous

- Rien ne part sans un oui explicite sur le texte, la date et le compte ; le script ne publie jamais "maintenant" (15 minutes au moins).
- Un tiret cadratin bloque, comme partout dans le workspace.
- Le lien va en premier commentaire, jamais dans le corps ; le script le rappelle et le calendrier garde le texte du commentaire.
- Un seul post par créneau et par compte : le script signale une collision à moins de 20 heures.
- La clé n'est jamais affichée ni copiée dans un fichier de skill.

## Erreurs fréquentes

| Message | Cause | Que faire |
|---|---|---|
| `Publora 401` | clé invalide ou révoquée | régénérer la clé dans le tableau de bord, `verifier_connexions.py --set PUBLORA_API_KEY=...` |
| `aucun compte LinkedIn connecte` | profil non relié | tableau de bord Publora, Connections, LinkedIn |
| jeton `expired` au `--test` | autorisation LinkedIn expirée | reconnecter LinkedIn dans le tableau de bord |
| `SCHEDULED_TIME_COERCED` dans la réponse | heure passée, ramenée à maintenant par Publora | le script refuse avant ; si ça arrive, `--decaler` tout de suite |
| `ce post n'est pas encore publie` au `--commenter` | pas de `postedId` tant que LinkedIn n'a pas publié | relancer après l'heure programmée |
| `MEDIA_URL_RATE_LIMITED` | trop d'URL de médias en une heure | passer par un fichier local (`--media`), ou attendre |
