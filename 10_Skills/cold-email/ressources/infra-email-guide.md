# Guide complet de l'infrastructure email

De zéro à une campagne qui arrive en boîte de réception : dimensionner, acheter les domaines, créer les boîtes, configurer le DNS, connecter à Lemlist, chauffer, lancer, surveiller, dépanner. Ce fichier nomme les fournisseurs d'infrastructure (Google Workspace, Microsoft 365, les registrars, la chauffe de Lemlist) parce qu'ils ne sont pas des outils de prospection : c'est la seule exception à la stack fermée.

## 0. La ligne rouge, dans l'ordre

1. Calculer les besoins.
2. Acheter des domaines secondaires.
3. Créer les espaces de travail et les boîtes.
4. Configurer le DNS (MX, SPF, DKIM, DMARC).
5. Connecter les boîtes à Lemlist.
6. Chauffer 3 semaines.
7. Lancer avec des limites basses.
8. Surveiller, tous les jours.

### Les sept règles qu'on ne casse jamais

1. Jamais le domaine principal pour la prospection à froid. Toujours des domaines secondaires.
2. Deux boîtes par domaine au maximum. Si un domaine brûle, vous perdez deux boîtes, pas dix.
3. Un domaine = un espace de travail. On ne mélange pas plusieurs domaines dans un même compte Google Workspace ou Microsoft 365.
4. Plusieurs registrars. Aucun point de défaillance unique.
5. Chauffe de 3 semaines avant le premier envoi, 2 au strict minimum.
6. Chauffe jamais coupée une fois les campagnes lancées.
7. On démarre bas, on monte doucement. Ajouter de la capacité est facile ; réparer une réputation prend des mois.

## 1. Dimensionner

### La configuration d'un dirigeant seul

Deux ou trois domaines, deux boîtes par domaine, 30 emails par boîte et par jour en régime établi. Capacité : 120 à 180 emails par jour, 2 400 à 3 600 par mois, de quoi refaire le tour d'un marché de 3 000 comptes tous les 3 mois. Coût : 6 à 7 € par boîte et par mois, 10 à 15 € par domaine et par an.

| Domaines | Boîtes | Emails par jour (régime établi) | Emails par mois |
|---|---|---|---|
| 2 | 4 | 120 | 2 400 |
| 3 | 6 | 180 | 3 600 |

Commencez à 2 domaines. Le troisième s'ajoute quand les deux premiers ont 3 mois et une réputation propre.

### La configuration d'une équipe

On part de l'objectif mensuel et on remonte :

1. Objectif mensuel d'emails.
2. Divisé par 20 jours ouvrés = volume par jour.
3. Divisé par 20 (prudent) ou 25 (agressif) = boîtes nécessaires.
4. Multiplié par 1,5 (marge pour la rotation, la chauffe, les pannes) = boîtes avec marge.
5. Divisé par 2 = domaines nécessaires.
6. Répartition : 60 % Google Workspace, 40 % Microsoft 365.

| Objectif mensuel | Par jour | Boîtes (avec marge) | Domaines |
|---|---|---|---|
| 3 000 | 150 | 10 à 12 | 5 à 6 |
| 7 500 | 375 | 18 à 23 | 9 à 12 |
| 15 000 | 750 | 38 à 45 | 19 à 23 |
| 30 000 | 1 500 | 75 à 90 | 38 à 45 |

Minimum pratique pour une équipe : 15 boîtes, soit environ 375 emails par jour. La répartition 60/40 entre les deux fournisseurs diversifie le risque : ils n'ont pas la même infrastructure ni les mêmes filtres.

Lemlist propose un calcul intégré (`calculate_infrastructure`) qui donne le même résultat à partir de l'objectif.

## 2. Acheter les domaines

### Les noms

Pour un domaine principal `acme.fr`, des variantes lisibles et reliées à la marque :

- préfixe : `essayez-acme.fr`, `contact-acme.fr`, `equipe-acme.fr`, `hello-acme.com`
- suffixe : `acme-conseil.fr`, `acmegroupe.fr`, `acme-solutions.com`, `acmehq.com`

À éviter : chaînes aléatoires, fautes volontaires, mots de promotion (`promo`, `offre`, `deals`), chiffres, tirets multiples.

**Extensions** : `.com` et `.fr` sont les meilleures pour une cible française. `.eu` et `.org` acceptables en secours. Évitez `.io`, `.ai`, `.co`, `.xyz` pour la prospection : associés aux envois de masse.

Listez deux fois plus de noms que nécessaire : certains seront pris.

### L'achat

- Répartissez entre registrars : OVH, Gandi, Cloudflare, Namecheap. Pour 6 domaines, par exemple 2 chez OVH, 2 chez Gandi, 2 chez Cloudflare. Si un registrar bloque votre compte ou tombe, vous perdez un tiers de la capacité, pas tout.
- Renouvellement automatique activé sur chaque domaine, tout de suite.
- Protection Whois activée (en général gratuite).
- Chaque domaine entre dans le tableau de suivi (section 10).
- Lemlist vend aussi des domaines déjà configurés (`search_domains`, `purchase_domain`) : plus cher, mais le DNS et la chauffe sont faits. Le bon choix pour un dirigeant qui ne veut pas toucher au DNS.

### La redirection

Chaque domaine secondaire redirige vers votre site principal (redirection permanente 301, sur le domaine racine, SSL activé). Un prospect qui tape le domaine tombe sur votre site : le domaine a l'air légitime. Réglage dans le registrar : "redirection" ou "forwarding".

## 3. Créer les espaces de travail et les boîtes

### Google Workspace (Business Starter, environ 7 € par utilisateur et par mois)

Par domaine, à répéter :

1. workspace.google.com, "Commencer", avec de vraies informations d'entreprise.
2. Ajouter le domaine secondaire, vérifier la propriété par un enregistrement TXT dans le DNS.
3. Créer la première boîte (un vrai prénom), puis la seconde.
4. Le DNS (MX, SPF, DKIM) se configure pendant cette étape, section 4.

### Microsoft 365 (Business Basic, environ 6 € par utilisateur et par mois)

1. microsoft.com, offre Business Basic, créer le compte administrateur.
2. Ajouter le domaine secondaire, vérifier par TXT.
3. Créer les boîtes (deux au plus).
4. **Activer SMTP et IMAP** : centre d'administration, Utilisateurs, Utilisateurs actifs, la boîte, Courrier, Gérer les applications de messagerie, cocher IMAP et SMTP authentifié, enregistrer.
5. **Attendre une heure** avant de connecter la boîte à Lemlist. C'est l'erreur la plus fréquente : la connexion échoue parce que le réglage n'est pas propagé. Mettez un minuteur.

### Le nom des boîtes

Bon : de vrais prénoms, `claire@`, `thomas@`, `karim@`. Mauvais : `contact@`, `commercial@`, `info@`, `noreply@`, `prospection@`. Gardez le même prénom sur tous vos domaines (claire@ partout) : c'est la personne qui envoie, le domaine est un détail technique.

### La photo de profil

Une vraie photo sur chaque boîte, dans le compte Google ou Microsoft. Elle s'affiche dans la messagerie du destinataire, améliore le placement et les réponses. On ne saute pas cette étape.

## 4. Configurer le DNS

Chaque domaine a besoin des quatre enregistrements. Un seul qui manque et la délivrabilité tombe.

| Enregistrement | Rôle |
|---|---|
| MX | route le courrier entrant vers Google ou Microsoft |
| SPF | déclare quels serveurs peuvent envoyer pour le domaine |
| DKIM | signature numérique qui prouve l'authenticité |
| DMARC | politique en cas d'échec de SPF ou DKIM, et adresse des rapports |

### MX

Configuré pendant la création de l'espace de travail (Google et Microsoft donnent les valeurs à copier). Vérifiez qu'il pointe bien vers le bon fournisseur.

### SPF

Un enregistrement TXT sur la racine du domaine (`@`) :

| Fournisseur | Valeur |
|---|---|
| Google | `v=spf1 include:_spf.google.com ~all` |
| Microsoft | `v=spf1 include:spf.protection.outlook.com ~all` |

**Un seul enregistrement SPF par domaine.** Deux SPF, et les deux sont ignorés. Certains registrars en créent un par défaut : supprimez le doublon. Chaque `include:` compte pour une recherche DNS, la limite est de 10.

### DKIM

- Google : console d'administration, Applications, Google Workspace, Gmail, Authentifier les emails, générer une clé 2048 bits, copier l'enregistrement TXT (`google._domainkey`) dans le DNS, puis "Lancer l'authentification".
- Microsoft : deux enregistrements CNAME (`selector1._domainkey` et `selector2._domainkey`), valeurs données dans le centre d'administration Exchange, puis activer DKIM.

Copiez la valeur exacte, sans espace en trop. DKIM peut mettre 24 heures à se propager.

### DMARC

Jamais créé automatiquement. À ajouter à la main sur chaque domaine :

| Champ | Valeur |
|---|---|
| Type | TXT |
| Hôte | `_dmarc` |
| Valeur | `v=DMARC1; p=none; sp=none; pct=100; rua=mailto:vous@votre-domaine-principal.fr; ri=86400; aspf=r; adkim=r; fo=1` |

Montée progressive, une fois les rapports propres : `p=none` les 2 premières semaines (on observe), `p=quarantine; pct=50` les semaines 3 et 4, `p=reject` ensuite. Un domaine de prospection peut rester en `p=none` s'il n'envoie que depuis Google ou Microsoft avec SPF et DKIM valides ; `p=reject` protège surtout contre l'usurpation de votre domaine.

### Le domaine de suivi

Seulement si vous gardez le suivi de clic. Un CNAME sur un sous-domaine (`lnk.votre-domaine.fr`) vers la cible fournie par Lemlist, puis activation dans les réglages de la boîte. Chez Cloudflare, le proxy doit être désactivé (nuage gris) sur ce CNAME. Le suivi d'ouverture reste désactivé dans tous les cas.

### Vérifier

- Lemlist : `check_domain_health` et `get_domain_dns` sur chaque domaine ; `configure_domain_dns` pose les enregistrements manquants quand le registrar est compatible.
- Un vérificateur DNS public (MXToolbox) : MX, SPF, DMARC, listes noires.
- Un test de score (mail-tester.com) : visez 8/10 et plus.
- Google Postmaster Tools : la réputation de vos domaines vue par Gmail.

### Les délais de propagation

| Enregistrement | Habituel | Maximum |
|---|---|---|
| MX, SPF, DKIM | 15 minutes à 4 heures | 48 heures |
| DMARC | 15 minutes à 4 heures | 48 heures |
| CNAME de suivi | 15 à 30 minutes | 4 heures |

Astuce : mettez le TTL à 300 secondes avant de modifier, remontez à 3600 une fois que tout marche.

## 5. Connecter les boîtes à Lemlist

- Google : connexion OAuth depuis Lemlist (`connect_email_account`), avec le compte administrateur de l'espace de travail. Le mot de passe d'application (2FA activée, mot de passe généré pour "Courrier") est la méthode de secours.
- Microsoft : connexion une par une, après l'heure d'attente SMTP, en cochant "consentir au nom de l'organisation".
- Test après connexion : `test_email_account`.

Réglages par boîte après connexion :

- Limite d'envoi quotidienne : Google 15 à 25, Microsoft 10 à 15 (on montera à 30 après 8 semaines).
- Domaine de suivi si le suivi de clic est activé ; suivi d'ouverture désactivé.
- Étiquettes : domaine, fournisseur, campagne.
- Montée progressive activée : démarre à 2 par jour, +2 par jour jusqu'à la limite. Pour les boîtes neuves seulement : l'activer sur une boîte établie la remet à 2.

## 6. Chauffer

La chauffe de Lemlist échange des emails réels entre votre boîte et un réseau de boîtes qui les ouvrent, y répondent, les sortent du spam et les marquent importants. Les messageries apprennent que votre boîte est humaine.

| Période | Ce qui se passe | Campagnes ? |
|---|---|---|
| Semaine 1 | fondation, volume bas | non |
| Semaine 2 | montée, les scores de santé apparaissent | non |
| Semaine 3 | prêt, santé au-dessus de 70 %, idéalement 90 % | oui, avec prudence |

Réglages recommandés :

| Réglage | Boîte neuve | Boîte établie |
|---|---|---|
| Emails de chauffe par jour | 10 à 15 | 20 à 30 |
| Taux de réponse simulé | 30 à 40 % | 30 à 40 % |
| Augmentation quotidienne | activée | facultative |
| Lecture simulée | activée | activée |

Un filtre dans la boîte (étiquette "chauffe", archivage automatique) garde la boîte de réception lisible : Lemlist donne le mot-clé à filtrer.

Surveillez chaque jour pendant la chauffe : le score de santé (cible 90 %, minimum 70 %), l'état de la chauffe (active ou coupée), les compteurs envoyés et reçus (les deux doivent monter).

## 7. Lancer

### La checklist avant lancement

- Toutes les boîtes chauffées 3 semaines, santé au-dessus de 70 %.
- Aucune chauffe coupée, DNS vert sur chaque domaine.
- Liste vérifiée à 100 % (`trouver_email`).
- Emails écrits, relus (`relecteurs.md`), validés sur trois exemples par l'utilisateur.
- Mention d'opt-out présente (`delivrabilite.md`, section 4).
- `run_inbox_placement_test` passé sur le texte final.

### La montée en charge

| Fournisseur | Semaine 1 | Semaines 2 et 3 | Semaine 4 et plus | Après 8 semaines |
|---|---|---|---|---|
| Google | 10 à 15 par jour | 15 à 20 | 20 à 25 | 30 |
| Microsoft | 5 à 10 | 10 à 12 | 12 à 15 | 20 |

### Les réglages de délivrabilité

- Email 1 en texte brut, toujours.
- Suivi d'ouverture désactivé.
- Appariement des messageries : Google envoie vers Gmail, Microsoft vers Outlook, quand la campagne le permet.
- Limite par entreprise : 2 à 3 emails par jour et par entreprise, toutes campagnes confondues.
- Délai aléatoire de 3 à 8 minutes entre deux envois d'une même boîte.
- Envois mardi à jeudi, 8h à 11h heure du destinataire par défaut.

### La première campagne

50 à 100 contacts. Surveillance 2 ou 3 jours. Si rebond sous 2 %, aucune plainte et des réponses, on monte. On grandit en ajoutant des boîtes en rotation, jamais en poussant la limite d'une boîte.

### Les métriques de santé

| Métrique | Sain | Alerte | Stop |
|---|---|---|---|
| Réponse | 2 % et plus | 1 à 2 % | sous 1 % |
| Rebond | sous 3 % | 3 à 5 % | plus de 5 % |
| Plainte spam | 0 | une | plusieurs |
| Score de délivrabilité (audit Lemlist) | plus de 95 % | 90 à 95 % | sous 90 % |

## 8. Surveiller

**Chaque jour, 5 minutes** : rebond, réponses, plaintes ; un coup d'œil à deux ou trois emails de chauffe ; aucune alerte de liste noire.

**Chaque semaine, 15 minutes** : Google Postmaster Tools, Microsoft SNDS ; `run_deliverability_audit` ; comparaison des réponses d'une semaine sur l'autre ; tendance du rebond.

**Chaque mois, 30 minutes** : mise à jour de la liste d'exclusion ; audit des rebonds ; réputation des domaines ; nettoyage des contacts sans réponse depuis 6 mois ; rotation du contenu de chauffe ; revue des coûts.

**Chaque trimestre, 1 heure** : audit DNS complet de tous les domaines ; efficacité de la chauffe ; capacité pour le trimestre suivant ; leçons apprises dans le journal.

### La règle de montée

- 20 % de volume en plus par semaine, au maximum.
- Des domaines en plus plutôt que des boîtes poussées.
- Un nouveau domaine par semaine au plus, chacun avec sa chauffe complète.
- Jamais plus de volume et un nouveau texte la même semaine.

## 9. Dépanner et récupérer

### DNS

| Symptôme | Cause | Correction |
|---|---|---|
| "Enregistrement introuvable" | pas propagé, ou pas enregistré | attendre (15 minutes à 48 heures), vérifier que l'enregistrement est bien sauvegardé dans le registrar, TTL à 300, vérifier que vous éditez le bon domaine |
| "Plusieurs SPF détectés" | doublon | supprimer les doublons, garder une seule ligne `v=spf1` |
| "DKIM en échec" | pas ajouté, valeur tronquée, pas propagé | régénérer la clé, copier la valeur exacte, vérifier l'hôte (`google._domainkey` ou `selector1._domainkey`), attendre 24 heures, relancer l'authentification |
| "DMARC manquant" | jamais automatique | ajouter le TXT `_dmarc` (section 4) |
| Domaine de suivi en échec | CNAME faux, proxy Cloudflare actif, non activé dans Lemlist | vérifier le CNAME, nuage gris, activer dans Lemlist, attendre 30 minutes |

Les pièges : avez-vous enregistré ? le bon domaine ? l'hôte exact (`@`, vide, `_dmarc`) ? la valeur entière sans espace ? le proxy désactivé sur les CNAME ? un seul SPF ?

### Connexion

- "Compte déjà ajouté" : la boîte est connectée à un autre espace Lemlist ; la retirer de l'autre d'abord.
- OAuth Google échoue : vérifier que vous êtes administrateur, réessayer en navigation privée.
- Microsoft refuse : SMTP et IMAP activés ? l'heure d'attente passée ? le bon compte ?
- "Identifiants invalides" : régénérer le mot de passe d'application, vérifier que la 2FA est toujours active.
- La connexion saute : la 2FA a été désactivée, ou le DNS a changé.

### Chauffe

- Chauffe coupée par l'outil (rebond élevé sur les emails de chauffe) : presque toujours le DNS. Corriger, vérifier les listes noires, réactiver.
- Score sous 70 % : emails de chauffe en spam. Vérifier SPF, DKIM, DMARC, l'âge du domaine, baisser le volume de chauffe, vérifier les listes noires.
- Rien ne part : la boîte est déconnectée, reconnecter.
- Rien n'arrive : la chauffe n'est pas activée.

### Délivrabilité

**Les emails partent en spam.** Dans l'ordre : les quatre enregistrements DNS présents ? la redirection du domaine en place ? les boîtes chauffées 3 semaines ? le volume dans les limites ? le texte propre (mots de spam, liens, HTML) ? aucune liste noire ? le domaine de suivi en place si suivi de clic ? une photo sur chaque boîte ?

**Le rebond dépasse 5 %.** Pause immédiate. Identifier la source : liste, domaine, DNS. Nettoyer (retirer tous les rebonds). Reprendre à 50 % du volume pendant 3 jours, 75 % les jours 5 à 7, 100 % à partir du jour 8.

**Un domaine est listé.** Arrêter tout envoi depuis ce domaine. Identifier la liste (`run_deliverability_audit` ou MXToolbox). Suivre la procédure de retrait de la liste. Corriger la cause avant de reprendre. Listé sur plusieurs listes : le domaine est brûlé, on en monte un nouveau.

**Les réponses baissent.** Qu'est-ce qui a changé (liste, texte, volume, heure, CTA) ? Quand ? Quels domaines ? Facteur externe (vacances, salon) ? Revenir à la version qui marchait, changer une seule variable à la fois.

### Le protocole de récupération

```
Jour 1        pause des campagnes touchées
Jour 2        correction du problème identifié
Jours 3 à 5   reprise à 50 % du volume
Jours 6 à 8   surveillance, 75 %
Jours 9 à 11  surveillance, 100 %
Jour 12 et +  plein volume, surveillance maintenue
```

### Le cadre d'enquête

Cinq questions, dans l'ordre : qu'est-ce qui a changé ? quand ça a commencé ? quels domaines sont touchés ? que disent les métriques (rebond, plainte, réponse) ? un facteur externe ?

## 10. Le tableau de suivi

Un tableur, une ligne par domaine :

| Domaine | Registrar | Fournisseur | Boîte 1 | Boîte 2 | Admin | Date d'achat | Chauffe depuis | Santé | Statut |
|---|---|---|---|---|---|---|---|---|---|
| contact-acme.fr | OVH | Google | claire@ | thomas@ | admin@acme.fr | 2026-09-01 | 2026-09-08 | 92 % | actif |
| acme-conseil.fr | Gandi | Microsoft | claire@ | thomas@ | admin@acme.fr | 2026-09-15 | 2026-09-22 | 74 % | en chauffe |

## 11. La saisonnalité

| Période | Baisse attendue | Retour |
|---|---|---|
| Vacances de Noël | 20 à 30 % | mi-janvier |
| Juillet et août | 10 à 20 %, davantage début août | septembre |
| Fin de trimestre | 10 à 15 % | deux premières semaines du trimestre |
| Salon du secteur | 15 à 25 % la semaine de l'événement | la semaine suivante |

On n'enquête que si la baisse dépasse ces normes ou ne revient pas à la date prévue.
