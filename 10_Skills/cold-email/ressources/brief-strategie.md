# Le brief de stratégie, avant tout email

Une campagne échoue plus souvent sur la stratégie que sur l'écriture. Un email bien écrit envoyé à la mauvaise personne, dans le mauvais registre, pour expliquer ce qu'elle sait déjà, fait moins bien qu'un email plat bien visé. Ce brief se remplit avant la première ligne, à partir de `05_Departements/Go-to-Market/contexte.md` et de la demande de l'utilisateur. Il se remplit même quand l'utilisateur a déjà tout spécifié : une partie de son travail est de contredire la spécification quand la donnée la contredit.

## 1. Le brief

```
BRIEF / {{utilisateur}} / {{campagne}}

OFFRE          Ce qu'on vend, en une phrase, en résultat. (contexte.md, section offre)
CIBLE          Qui reçoit. Fonction, niveau, taille et secteur d'entreprise, ce que
               contient sa semaine, combien de fois par jour on le sollicite.
PERSONA        ATL (dirigeant, directeur) ou BTL (manager, opérationnel). Décide la
               longueur et l'angle. (contexte.md, personas)
REGISTRE       Le ton, et une phrase qui explique le choix. (registre-audience.md)
CONNAISSANCE   Expert / Conscient mais pas chiffré / Non informé. Avec la preuve.
               Par sous-problème si le lecteur n'a pas le même niveau partout.
               Dire quel niveau commande la séquence.
ANGLE          Une phrase. La seule raison pour laquelle cette personne devrait
               s'y intéresser maintenant. Nomme une personne et un problème.
SIGNAL         Le déclencheur utilisé (signal_type, signal_date, source), ou
               "aucun" et la pertinence de repli choisie.
PREUVE         Les preuves de contexte.md utilisées, avec leurs chiffres exacts.
               Rien d'autre.
CTA            La demande unique de l'email 1, et celle des relances.
EXPÉDITEUR     Quelle boîte et quelle identité envoient, et pourquoi ce lecteur
               la croit.
HISTORIQUE     Ce qui a obtenu des réponses sur ce compte, avec la preuve.
               "Aucun historique" est une réponse valable et change l'écriture.
PROFONDEUR     Ouverture par personne, ou par segment, et le fait de segmentation.
               Selon la donnée disponible et ce que l'utilisateur peut relire.
À VALIDER      Affirmations, citations et preuves qui demandent un accord écrit
               de l'utilisateur avant envoi. Vide est acceptable. Deviner ne l'est pas.
DÉSACCORD      Où la recherche contredit l'utilisateur, la preuve, et ce qui
               changerait dans l'email. Ne pas fabriquer de désaccord.
```

Le brief reste court, c'est une note de travail. Il est montré à l'utilisateur avant le premier email. Il n'entre pas dans le livrable final sauf demande.

## 2. S'arrêter ou continuer

Vous écrivez le brief, vous le montrez, et vous continuez dans le même tour. Le brief est une information, pas une barrière de validation : attendre une réponse sur chaque petite réécriture ralentit tout.

Vous vous arrêtez et vous posez la question quand un point de DÉSACCORD changerait l'ANGLE. Test mécanique : réécrivez l'angle comme si le désaccord avait raison.

- Si l'angle nomme toujours la même personne et le même problème, continuez. Dites le conflit, écrivez sur la lecture de l'utilisateur, marquez l'alternative comme réversible.
- Si l'angle nomme une autre personne ou un autre problème, arrêtez-vous. Vous alliez écrire une autre campagne.

Quand vous continuez malgré un conflit, dites-le en une ligne au-dessus des emails. L'utilisateur ne doit pas découvrir le conflit en lisant une campagne en cours.

## 3. Cerner la cible

Le titre sur la liste est un début, pas une fin. Établissez :

- qui ils sont, avec les mots de fonction et de niveau que leur entreprise utilise ;
- ce que contient leur semaine : le travail récurrent que l'offre touche ;
- s'ils tiennent le budget : on n'écrit pas à un non-acheteur comme s'il pouvait acheter, on écrit sur ce qu'il possède et on facilite le routage ;
- combien de fois on les sollicite : un dirigeant très sollicité tolère mal la chaleur non demandée ;
- ce que leur métier trouve crédible : les spécialistes, la précision et la preuve ; les opérationnels, ce qui change dans leur travail.

La réponse va dans REGISTRE. On ne change plus de registre après le début de la rédaction, sauf preuve nouvelle.

## 4. L'axe de connaissance

Combien le lecteur sait-il déjà du problème ?

**Expert du problème.** Il vit dedans, il a des opinions, il a peut-être essayé de le régler. Ne lui expliquez pas le problème. N'ouvrez pas sur une statistique de marché qu'il connaît ou dont il se méfie. Montrez que vous comprenez les mécanismes de son travail. Nommez le trou et laissez-le en mesurer l'importance. Une question de diagnostic marche bien ici : elle porte sur une opération que lui seul peut mesurer. Lecteurs typiques : spécialistes seniors, directeurs métier, opérationnels expérimentés dans leur domaine.

**Conscient mais pas chiffré.** Il reconnaît le symptôme sans avoir mesuré son coût, ou sans savoir qu'un remède existe. Nommez le symptôme dans ses mots, puis chiffrez-le avec une preuve validée seulement. Un chiffre aide parce qu'il ajoute une information au lieu de lui enseigner son métier.

**Non informé.** Le problème est nouveau, normalisé ou hors de son quotidien. C'est le seul cas où l'éducation a sa place. Mettez l'essentiel de l'éducation dans l'email 2. L'email 1 doit quand même accrocher sur quelque chose qu'il reconnaît.

**Le test.** Le lecteur aurait-il pu écrire lui-même la première phrase ? Si oui, elle peut sonner comme venant de son monde. S'il l'aurait écrite mieux, vous enseignez à un expert : coupez, et descendez d'un niveau dans le travail.

## 5. Angle, cible et registre sont trois décisions

Elles échouent différemment. L'angle décide si le message dit quelque chose qui vaut la lecture. La cible décide si ce lecteur s'en soucie. Le registre décide s'il lit assez loin pour le découvrir.

Un angle peut être vrai et important pour l'entreprise, et sans intérêt pour la personne sur la liste. Classez les angles candidats selon le problème de qui ils nomment. Préférez l'angle qui nomme le travail du destinataire, pas un bénéfice d'entreprise qu'il ne possède pas.

Écrivez l'angle en une phrase qui nomme une personne et un problème. Si la phrase a besoin d'une proposition sur le produit pour avoir un sens, c'est une fonctionnalité, pas un angle.

## 6. Rechercher le marché

Recherchez à chaque campagne, même quand l'utilisateur a fourni un brief. Comprenez : le marché et ses changements récents qui touchent le travail du lecteur ; à qui l'utilisateur vend et qui contrôle le problème ; ses concurrents ; où il est fort et faible ; où il gagne et perd ; sa proposition de valeur soutenue par une preuve.

Sources dans cet ordre : les documents et transcripts d'appels fournis ; `05_Departements/Go-to-Market/contexte.md` et les briefs validés ; la recherche publique pour les tendances et l'actualité (`enrichir_entreprise`, `detecter_signal`, recherche web).

Notez d'où vient chaque chose. Chaque affirmation de l'email final a une source. Si un outil ou un document manque, dites-le et rendez `contexte_insuffisant` pour toute affirmation qui en dépend. Ne dites jamais qu'une recherche a été faite quand elle ne l'a pas été.

N'utilisez une tendance que si le destinataire la ressent dans son travail. Un commentaire de marché général ne mérite pas sa place. Test : le destinataire peut-il confirmer ou infirmer la conséquence à partir de sa propre semaine ?

## 7. Arbitrer entre consignes

Lisez `05_Departements/Go-to-Market/contexte.md`, `05_Departements/Go-to-Market/GARDE-FOUS.md` et la demande de l'utilisateur avant d'écrire. Priorité :

1. Les règles de `05_Departements/Go-to-Market/GARDE-FOUS.md` et les restrictions sur les affirmations (preuves fermées).
2. Le brief de campagne et les consignes de l'utilisateur pour cette campagne.
3. Les preuves et faits produits validés de `05_Departements/Go-to-Market/contexte.md`.
4. Les règles de métier de ce skill (`regles-copy.md`).

Une règle sur les faits, les affirmations, les noms et les validations bat une préférence de style. Une règle de métier peut battre un vieux document de planification quand celui-ci contredit une correction validée plus récente. Dans les deux cas, le conflit va dans DÉSACCORD.

Quand la recherche contredit l'utilisateur, dites : ce qu'il a dit ; ce que dit la preuve, avec la source ; ce qui changerait dans l'email si la preuve a raison. Puis continuez sur sa lecture, sauf si le conflit change l'angle. Soyez honnête sur la force de la preuve : l'historique de réponses du compte pèse plus qu'un article général ; une affirmation de fournisseur est une preuve faible.

## 8. Utiliser l'historique de réponses

Avant de fixer l'angle, regardez ce qui a obtenu des réponses sur ce compte (`verifier_reponses`, statistiques Lemlist). Jugez sur les réponses positives et les rendez-vous, pas sur les ouvertures ni les clics. La preuve du compte pèse plus qu'un pattern général parce qu'elle vient de la vraie audience. Quand elle est mince, dites-le. Traitez la première campagne comme un apprentissage, pas comme une vérité.

N'exposez jamais dans un livrable public les données brutes d'une campagne, l'identité d'un client, des totaux de réponses ou une copie privée. Convertissez la preuve privée en décision pour l'utilisateur.

## 9. Exemple de brief rempli (fictif)

```
BRIEF / Solvéo Conseil / plafond de la recommandation

OFFRE          Une routine de prospection de 2 h par semaine, tenue par le dirigeant, qui ajoute 4 à 8 rendez-vous par mois en 10 semaines.
CIBLE          Dirigeants de cabinets de conseil et d'agences B2B, 10 à 60 personnes, France. Semaine faite de production client et de réunions ; 5 à 10 sollicitations par jour.
PERSONA        ATL. 2 à 3 phrases, angle chiffre d'affaires et prévisibilité.
REGISTRE       Consultatif, posé, vouvoiement. Ils vendent eux-mêmes du conseil : pas de chaleur non demandée.
CONNAISSANCE   Conscient mais pas chiffré : ils savent que la reco plafonne, ils n'ont pas mesuré le coût d'un mois sans reco.
ANGLE          Un dirigeant qui vit à 100 % sur la recommandation n'a aucune prise sur le mois où elle s'arrête.
SIGNAL         Page références du site (3 derniers clients issus de reco), détecté par enrichir_entreprise. Repli : segment "cabinet de conseil 10 à 60".
PREUVE         Cabinet Arven : +6 rendez-vous par mois en 10 semaines, 2 h par semaine, associé. Validée le 12/09.
CTA            Email 1 : "une deuxième source de rendez-vous en place, ou pas encore ?". Email 2 : envoi de la routine. Email 3 : routage.
EXPÉDITEUR     Boîte thibault@solveo-conseil.fr, fondateur. Un pair, même métier.
HISTORIQUE     Campagne de juin : 4,2 % de réponses positives sur l'angle "cold call", 1,1 % sur l'angle "IA". Aucun test sur cet angle.
PROFONDEUR     Par segment (taille et type de cabinet). 40 % des lignes ont une page références exploitable : ouverture par personne sur ces lignes, repli sur les autres.
À VALIDER      Le chiffre "6 rendez-vous par mois" pour Arven (source : bilan de mission du 30/08).
DÉSACCORD      L'utilisateur veut ouvrir sur "l'IA dans la prospection". L'historique dit 1,1 % sur cet angle contre 4,2 %. L'angle reste le même problème (pipeline) et la même personne : on continue sur la reco, l'IA passe en email 2, réversible.
```
