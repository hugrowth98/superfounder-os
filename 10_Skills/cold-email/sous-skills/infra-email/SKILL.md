---
name: infra-email
description: >
  Monte, dimensionne et dépanne l'infrastructure d'envoi : domaines secondaires, DNS (SPF, DKIM, DMARC), boîtes, chauffe, volumes par boîte, listes noires, mise en production. Se déclenche sur : "domaine", "combien de domaines", "DNS", "SPF", "DKIM", "DMARC", "warmup", "chauffe", "boîte mail", "mes emails partent en spam", "blacklist", "liste noire", "délivrabilité", "rebond", "montée en charge", "infra email", "Google Workspace", "Microsoft 365". Ne pas utiliser pour écrire un email (voir premier-contact ou frameworks-copywriting), ni pour la conformité et les principes généraux de délivrabilité (le master les traite avec la ressource delivrabilite.md).
---

Une boîte qui envoie 30 emails par jour depuis un domaine secondaire chauffé 3 semaines, avec SPF, DKIM et DMARC en place, arrive en boîte de réception ; la même boîte sur le domaine principal, sans chauffe, finit en spam en dix jours et entraîne le domaine de l'entreprise avec elle. Ce sous-skill peut nommer les fournisseurs d'infrastructure (Google Workspace, Microsoft 365, registrars, chauffe de Lemlist) : seule exception à la stack fermée, parce que ce ne sont pas des outils de prospection.

## Ressources

- `{SKILL_BASE}/ressources/infra-email-guide.md` : le guide pas à pas complet, le dépannage et la récupération.
- `{SKILL_BASE}/ressources/delivrabilite.md` : l'authentification, la chauffe, le placement, la conformité, les rebonds, les listes noires.
- `{SKILL_BASE}/ressources/metriques-benchmarks.md` : les seuils de rebond, de plainte, de réponse.

## Méthode

1. **Qualifier la demande** : montage de zéro, dimensionnement, DNS, connexion, chauffe, lancement, ou dépannage (spam, rebond, liste noire, chauffe coupée).
2. **Dimensionner** : un dirigeant seul, 2 à 3 domaines, 2 boîtes par domaine, 30 emails par boîte et par jour en régime établi ; une équipe, la formule objectif mensuel / 20 jours / 20 par boîte × 1,5 / 2 par domaine, répartis 60 % Google et 40 % Microsoft.
3. **Dérouler la ligne rouge** dans l'ordre du guide : domaines (jamais le principal, plusieurs registrars, renouvellement automatique, redirection 301), espaces de travail (un par domaine, deux boîtes à vrais prénoms, photo), DNS (MX, SPF unique, DKIM 2048, DMARC à la main), connexion à Lemlist, 2 semaines de repos après les DNS puis 3 semaines de chauffe (domaine neuf), lancement à 10 à 15 par jour, montée de 20 % par semaine.
4. **Vérifier avant tout envoi** : `check_domain_health`, `get_domain_dns`, score de chauffe au-dessus de 70 %, `run_inbox_placement_test` sur le texte final, liste filtrée sur `email_statut` (seuls `DELIVERABLE` et `HIGH_PROBABILITY` partent, `CATCH_ALL` et `UNKNOWN` à 20 % au plus).
5. **Dépanner avec le cadre d'enquête** : qu'est-ce qui a changé, quand, quels domaines, que disent les métriques, facteur externe. Puis la table de dépannage du guide et le protocole de récupération (pause, correction, 50 %, 75 %, 100 %).
6. **Rendre un plan daté** : ce qu'on fait cette semaine, ce qu'on attend (propagation, chauffe), la date du premier envoi.

## Exécution

Aucun verbe de collecte : les actions passent par le MCP Lemlist, et le skill `connecter-outils` gère la clé.

- Lecture, sans validation : `list_domains`, `check_domain_health`, `get_domain_dns`, `list_mailboxes`, `calculate_infrastructure`, `run_deliverability_audit`, `run_inbox_placement_test`, `test_email_account`.
- Écriture, après validation explicite et annonce du coût : `search_domains` et `purchase_domain` (domaines vendus par Lemlist), `configure_domain_dns`, `connect_email_account`, `provision_mailboxes`, `update_mailbox` (limites d'envoi, chauffe).
- Hors outil : la création des espaces Google Workspace ou Microsoft 365 et les réglages du registrar se font à la main par l'utilisateur, avec les étapes du guide données une par une.

Sortie : le tableau de suivi des domaines (section 10 du guide) dans `05_Departements/Go-to-Market/Messages/infra-email_<YYYY-MM-DD>.md`, et un plan daté.

## Repères

| Repère | Valeur |
|---|---|
| Dirigeant seul | 2 à 3 domaines, 2 boîtes par domaine, 30 par boîte et par jour : 120 à 180 emails par jour |
| Équipe | objectif / 20 / 20 × 1,5 / 2 ; 15 boîtes minimum ; 60 % Google, 40 % Microsoft |
| Volume par boîte | Google 15 à 25 (30 après 8 semaines), Microsoft 10 à 15 (20 après 8 semaines) |
| Chauffe | 3 semaines avant le premier envoi à froid, jamais coupée, santé > 70 % (cible 90 %) |
| Âge du domaine avant envoi | 5 semaines minimum (2 de repos après les DNS, 3 de chauffe), 6 à 8 idéal |
| Montée | 20 % par semaine au plus, un nouveau domaine par semaine au plus |
| Rebond | alerte à 3 % (on vérifie la liste), arrêt de la campagne à 5 % |
| Plainte | < 0,1 % |
| Extensions | .com et .fr ; éviter .io, .ai, .co |
| Coût | 6 à 7 € par boîte et par mois, 10 à 15 € par domaine et par an |

## Template

Le plan d'un dirigeant seul, à dater :

```
Semaine 1   Acheter contact-{{marque}}.fr (OVH) et {{marque}}-conseil.fr (Gandi).
            Renouvellement automatique, Whois privé, redirection 301 vers le site.
            Créer un espace Google Workspace par domaine, 2 boîtes ({{prenom}}@, {{collegue}}@), photos.
            DNS : MX, SPF, DKIM (2048), DMARC p=none. Vérifier avec check_domain_health.
Semaines 2 et 3   Repos après les DNS : aucun envoi. Connecter les 4 boîtes à Lemlist en fin de semaine 3.
Semaines 4 à 6   Chauffe (10 à 15 par jour, réponse 30 à 40 %). Vérifier la santé chaque jour (cible 90 %).
            Aucun envoi à froid. Écrire et relire la séquence, filtrer la liste sur `email_statut`.
Semaine 7   Premier lot : 50 contacts, 10 à 15 emails par boîte et par jour. Surveiller 3 jours.
Semaines 8 à 11   +20 % par semaine jusqu'à 25 par boîte. Audit de délivrabilité chaque lundi.
Semaine 12  30 par boîte. Troisième domaine si le marché le demande.
```

## Règles

1. Jamais le domaine principal pour la prospection.
2. Deux boîtes par domaine au plus, un domaine par espace de travail, plusieurs registrars.
3. Chauffe de 3 semaines avant le premier envoi à froid (domaine neuf : 2 semaines de repos après les DNS d'abord), jamais coupée ensuite.
4. Un seul SPF par domaine ; DMARC ajouté à la main ; DKIM copié sans espace.
5. On grandit en ajoutant des boîtes, jamais en poussant une boîte au-delà de 30.
6. Suivi d'ouverture désactivé ; texte brut ; un lien au plus.
7. Aucun achat, aucune modification DNS, aucune connexion de boîte sans validation explicite et coût annoncé.
8. Sous 1 % de réponse, on ne diagnostique pas : nouveaux domaines, nouveau texte, redémarrage.

## Exemples

- "Combien de domaines il me faut pour 3 000 emails par mois ?" : 150 par jour, 10 à 12 boîtes avec marge, 5 à 6 domaines, 60/40 Google et Microsoft ; pour un dirigeant seul qui vise moins, 2 à 3 domaines suffisent.
- "Mes emails partent en spam depuis lundi" : cadre d'enquête (quoi, quand, quels domaines, métriques, externe), `check_domain_health` et `run_deliverability_audit`, table de dépannage, protocole de récupération à 50 % puis 75 % puis 100 %.
- "Monte-moi mon infra de zéro" : dimensionnement, plan daté sur 12 semaines, étapes données une par une (domaines, espaces de travail, DNS, connexion, chauffe), vérifications Lemlist à chaque étape, tableau de suivi créé.
