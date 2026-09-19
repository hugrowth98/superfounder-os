# Délivrabilité, rebonds, conformité

Ce fichier couvre ce qui fait qu'un email arrive en boîte de réception, ce qu'on fait des rebonds, et ce que la loi française et le RGPD imposent à la prospection B2B par email. Le montage pas à pas de l'infrastructure (domaines, DNS, boîtes, chauffe) est dans `infra-email-guide.md`.

## 1. L'authentification en trois enregistrements

Trois enregistrements DNS prouvent aux messageries que vous êtes bien l'expéditeur. Les trois sont obligatoires sur chaque domaine d'envoi. Sans l'un d'eux, Gmail et Outlook classent en spam ou refusent.

| Enregistrement | Ce qu'il fait | À retenir |
|---|---|---|
| SPF | déclare quels serveurs ont le droit d'envoyer pour votre domaine | un seul enregistrement SPF par domaine, jamais deux |
| DKIM | signe chaque email pour prouver qu'il n'a pas été modifié | clé 2048 bits, générée chez Google Workspace ou Microsoft 365 |
| DMARC | dit quoi faire quand SPF ou DKIM échoue, et où envoyer les rapports | jamais ajouté automatiquement : à créer à la main sur chaque domaine |

Les valeurs exactes, la vérification et le dépannage sont dans `infra-email-guide.md`. Vérification rapide : `check_domain_health` et `get_domain_dns` dans Lemlist.

## 2. La chauffe et l'âge du domaine

| Âge du domaine | État | Ce qu'on fait |
|---|---|---|
| 0 à 2 semaines | tout neuf | aucun email ; DNS, boîtes, repos après les DNS |
| 2 à 5 semaines | frais | chauffe seule (3 semaines), aucun email à froid |
| 5 à 8 semaines | en chauffe | premiers envois à froid, montée progressive |
| 8 à 12 semaines | en construction | volume modéré, 20 à 30 par boîte et par jour |
| plus de 12 semaines | établi | plein volume, surveillance continue |

Minimum avant le premier email à froid : 5 semaines (2 de repos après les DNS, 3 de chauffe). Idéal : 6 à 8 semaines. La chauffe ne s'arrête jamais : 10 à 20 emails de chauffe par jour et par boîte pendant toute la vie de la campagne. Une boîte dont on coupe la chauffe perd sa réputation en quelques semaines.

Le calendrier de montée en charge d'un domaine neuf, à compter de l'activation de la chauffe (après les 2 semaines de repos DNS) :

| Semaine | Emails à froid par jour et par boîte | Emails de chauffe |
|---|---|---|
| 1 | 0 | 5 à 10 |
| 2 | 0 | 10 à 20 |
| 3 | 0 | 15 à 25 |
| 4 | 10 | 20 à 30 |
| 5 | 20 | 20 à 30 |
| 6 et plus | 30 | 10 à 20 |

## 3. Le placement en boîte de réception

**Texte brut, toujours.** Le HTML et les images sont des signaux de marketing pour les filtres et pour le lecteur. Le texte brut se lit partout, ne casse pas, et ressemble à un email de collègue.

| | Texte brut | HTML |
|---|---|---|
| Délivrabilité | meilleure | moins bonne (plus de signaux de spam) |
| Confiance | personnel | marketing |
| Suivi | pas de pixel d'ouverture | pixel possible, et nuisible |
| Affichage | identique partout | variable, peut casser |

**Pas de suivi d'ouverture.** Le pixel pèse sur le placement et les messageries ouvrent elles-mêmes les emails : la mesure est fausse. Désactivez-le dans Lemlist. Le suivi de clic se discute par campagne ; par défaut, non. Si vous le gardez, un domaine de suivi personnalisé (sous-domaine de votre domaine d'envoi) est obligatoire.

**Un lien au plus** dans un email à froid, et aucun dans l'email 1 si le domaine a moins de 3 mois.

**Heures d'envoi** : entre 8h et 18h à l'heure du destinataire, pics 8h à 10h et 14h à 16h, mardi à jeudi. Délai aléatoire de 30 secondes à 3 minutes entre deux envois. Variez légèrement les heures d'un jour à l'autre.

**Volume** : 30 emails à froid par boîte et par jour au maximum (15 à 25 sur Google, 10 à 15 sur Microsoft en régime normal). On grandit en ajoutant des boîtes, jamais en poussant une boîte au-delà.

**Le taux de réponse protège la réputation** : au-dessus de 5 %, la délivrabilité tient ; au-dessus de 10 %, elle est stable ; sous 3 %, elle se dégrade. Un email pertinent est aussi un email qui arrive.

## 4. La conformité en France

### Le cadre

En France, la prospection B2B par email est possible sans consentement préalable, à trois conditions posées par la CNIL et l'article L34-5 du Code des postes et des communications électroniques :

1. le message concerne la fonction professionnelle de la personne (un DAF reçoit une offre de logiciel financier, pas une offre de vacances) ;
2. la personne a été informée que son adresse serait utilisée pour de la prospection, et de sa provenance ;
3. elle peut s'y opposer simplement et gratuitement, à chaque message.

Le RGPD s'ajoute : la base légale est l'intérêt légitime (article 6.1.f), qui suppose une évaluation écrite (l'intérêt poursuivi, la nécessité du traitement, l'équilibre avec les droits de la personne), la minimisation des données, la transparence, le droit d'accès, de rectification et d'effacement, et un registre des traitements. Les adresses génériques (contact@, info@) ne sont pas des données personnelles ; les adresses nominatives le sont.

Ce qui vaut en France ne vaut pas partout : l'Allemagne exige en pratique le consentement, la Suisse et le Royaume-Uni acceptent l'intérêt légitime avec des nuances. Une campagne hors de France se vérifie pays par pays.

### La mention d'information et l'opt-out

Chaque email à froid porte une possibilité de refus simple. Deux formes acceptables :

- une phrase en fin d'email, dans la voix de l'expéditeur : "Si ce sujet ne vous concerne pas, répondez-moi un mot et je ne reviendrai pas vers vous." ;
- ou le lien de désabonnement de Lemlist, qui gère la liste d'exclusion.

La première forme convient à un dirigeant qui envoie 30 emails par jour ; la seconde devient obligatoire à volume, et Gmail comme Yahoo exigent depuis 2024 un désabonnement en un clic (en-têtes `List-Unsubscribe` et `List-Unsubscribe-Post`) pour tout expéditeur au-delà de 5 000 emails par jour. Lemlist ajoute ces en-têtes.

Une mention d'information plus complète peut vivre dans la signature ou en une ligne : "Vous recevez ce message en tant que {{fonction}} chez {{entreprise}}, adresse trouvée sur {{source}}. Pour ne plus en recevoir, répondez STOP."

### Les obligations concrètes

- Une demande de retrait est exécutée sous 48 heures, sur tous les outils (Lemlist `add_unsubscribe`, colonne `ne_plus_contacter` du CSV, CRM).
- Une demande d'accès ("d'où vient mon adresse ?") reçoit une réponse honnête sous un mois, en pratique sous 24 heures (`reponses.md`).
- La source des adresses est notée dans la colonne `source` du CSV : c'est ce qui permet de répondre.
- Aucune adresse personnelle (gmail.com, orange.fr) dans une campagne B2B.
- Un registre des traitements existe, même simple : quelle donnée, d'où, pour quoi, combien de temps. Les contacts sans réponse s'effacent ou se ré-évaluent après 3 ans au plus.
- Une évaluation d'intérêt légitime écrite d'une page suffit pour un dirigeant seul. Elle se garde avec le registre.

`05_Departements/Go-to-Market/GARDE-FOUS.md` à la racine reprend les règles propres à l'utilisateur ; il prime sur ce fichier.

## 5. Les listes noires

| Liste | Gravité | Effet |
|---|---|---|
| Spamhaus (ZEN, DBL) | critique | utilisée par la majorité des fournisseurs, dont les grands hébergeurs français |
| Barracuda | élevée | passerelles d'entreprise |
| SpamCop | moyenne à élevée | expire seule en 24 à 48 heures |
| SORBS | moyenne | plusieurs listes |
| URIBL, SURBL | élevée | vérifient les domaines cités dans le corps de l'email |

Vérification : `run_deliverability_audit` dans Lemlist, ou un vérificateur public de listes noires (MXToolbox). Fréquence : tous les jours pendant la chauffe, toutes les semaines en campagne. Retrait : formulaire de chaque liste (Spamhaus 24 à 48 heures, Barracuda 12 à 24 heures, SpamCop automatique). Un domaine listé sur plusieurs listes est considéré comme brûlé : on en monte un nouveau.

## 6. Les rebonds

| Type | Ce que c'est | Action |
|---|---|---|
| Rebond dur (5xx) | adresse invalide, définitif | retirer immédiatement, ne jamais réessayer |
| Rebond doux (4xx) | boîte pleine, serveur indisponible, temporaire | réessayer 2 ou 3 fois sur 24 à 72 heures |

| Taux de rebond | État | Action |
|---|---|---|
| moins de 1 % | excellent | continuer |
| 1 à 3 % | acceptable | surveiller |
| 3 à 5 % | alerte | revérifier la liste |
| 5 % et plus | critique | arrêt de la campagne, nettoyage, reprise à 50 % |

### Vérifier avant d'envoyer

- Chaque adresse passe par `trouver_email` (FullEnrich) avant toute campagne. Une adresse importée sans statut est non vérifiée : `trouver_email --force` la re-cherche (1 crédit si trouvée), sinon elle ne part pas (`--sans-verification` déconseillé). On ne promet jamais "100 % vérifiés".
- Une liste de plus de 30 jours se revérifie.
- `email_statut` `DELIVERABLE` et `HIGH_PROBABILITY` partent ; `CATCH_ALL` (le serveur accepte tout) et `UNKNOWN` partent avec prudence, 20 % de la liste au plus (`--avec-catch-all`) ; `INVALID`, `INVALID_DOMAIN`, `NOT_FOUND` et les adresses sans statut ne partent pas.
- Les adresses de rôle (info@, contact@, rh@) sont retirées.
- Les adresses de fournisseurs grand public sont retirées.
- Le coût de vérification (quelques centimes par adresse) est négligeable face à un domaine brûlé.

## 7. La checklist avant lancement

- Domaines d'envoi séparés du domaine principal, de plus de 5 semaines (2 de repos après les DNS, 3 de chauffe).
- Google Workspace ou Microsoft 365 sur chaque domaine, 2 boîtes au plus par domaine.
- SPF, DKIM, DMARC vérifiés sur chaque domaine (`check_domain_health`).
- Domaine de suivi personnalisé si le suivi de clic est activé ; suivi d'ouverture désactivé.
- Chauffe active sur chaque boîte depuis 3 semaines, score de santé au-dessus de 70 %, idéalement 90 %.
- Adresses filtrées sur `email_statut` : `DELIVERABLE` et `HIGH_PROBABILITY`, catch-all et `UNKNOWN` à 20 % au plus.
- Surveillance des listes noires en place.
- Mention d'opt-out dans chaque email, évaluation d'intérêt légitime écrite.
- Trois emails montrés à l'utilisateur et validés.
- Premier lot de 50 à 100 contacts, surveillé 2 ou 3 jours avant de monter.

## 8. La surveillance en campagne

- Volume : 15 à 30 par boîte et par jour, chauffe maintenue à 10 à 20.
- Rebond sous 3 % (alerte à 3 %, arrêt à 5 %), plainte sous 0,1 %, réponse au-dessus de 3 % (en dessous, la délivrabilité se dégrade).
- Listes noires et Google Postmaster Tools chaque semaine.
- Texte brut, envois aux heures ouvrées du destinataire.
- Désabonnements traités sous 48 heures.
- Rotation des boîtes entre campagnes.
- Listes de plus de 30 jours revérifiées.
