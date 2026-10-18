# Contrat pédagogique des fiches et des cartes

**Statut** : proposition issue des choix confirmés, à éprouver sur le pilote.

## Profil et langue

Les explications ciblent un ingénieur ayant déjà les bases ML/DL. Elles portent
sur les spécificités de vision : modèles, hypothèses, géométrie, représentations,
paramètres, protocoles, compromis et échecs. Une notion générale est rappelée
lorsqu'elle débloque une explication concrète.

Les textes sont en français. Noms originaux, acronymes, termes techniques anglais
et identifiants de code sont conservés. Les termes importants sont introduits
avec leur équivalent français si cela aide, puis employés de manière cohérente.

## Contrat d'une fiche de référence

Chaque fiche validée couvre les rubriques suivantes. Une rubrique non applicable
est signalée et justifiée plutôt que remplie artificiellement.

| Rubrique | Contenu attendu |
| --- | --- |
| Problème | Besoin, tâche, entrées/sorties et place dans un pipeline |
| Intuition | Mécanisme, illustration ou exemple filé utile |
| Prérequis | Notions nécessaires et liens pour combler un manque |
| Hypothèses | Conditions d'application, observations et cas dégénérés |
| Déroulement | Étapes, rôle de chaque étape et pseudocode utile |
| Mathématiques | Équations expliquées, conventions, symboles, dimensions/unités pertinentes |
| Paramètres | Effets, interactions, sensibilité et démarche de réglage |
| Propriétés | Invariances, approximations et limites des garanties |
| Coût et implémentation | Complexité ou facteurs de coût ; code expliqué et statut d'exécution |
| Évaluation | Protocole, métriques, données pertinentes et limites de la mesure |
| Échecs et diagnostic | Symptômes, causes possibles, vérifications discriminantes et remèdes conditionnels |
| Alternatives et sources | Comparaisons sous conditions, usages industriels, sources primaires et cartes associées |

La fiche peut être longue. Sous-sections, schémas et liens doivent permettre
de retrouver les éléments sans imposer une lecture linéaire à chaque révision.

Le contrat s'adapte au type de fiche : problème, méthode, comparaison,
métrique/protocole ou pipeline. Toute notion n'a pas à être présentée comme
un algorithme. Les rubriques nécessaires sont déterminées par la profondeur
et les compétences affichées dans l'inventaire ; leur non-applicabilité est justifiée.

Les entrées/sorties précisent, lorsque pertinent, repères, formes et types des
données, plages de valeurs, couleur, unités et normalisation. Les changements
de résolution, crop, padding ou coordonnées restent traçables jusqu'à la sortie.
Les hypothèses de cadence et d'accès aux frames futures sont explicites.

## Contrat d'une carte

Une carte comporte :

- Un identifiant pédagogique stable et une fiche parente.
- Un objectif de rappel explicite et un type de question.
- Une question contextualisée, compréhensible hors de la fiche.
- Une réponse directe, suivie des explications utiles.
- Les conditions de validité, limites ou contre-exemples pertinents.
- Les critères permettant de décider si la réponse donnée est satisfaisante.
- Les références et un lien vers l'approfondissement dans la fiche.
- Son domaine, sa famille et les pôles servis par sa fiche, exportés comme
  étiquettes pour suivre la maîtrise par domaine et par pôle dans Anki.
- Sa provenance de rédaction : apprenant, agent ou mixte.

La réponse peut contenir paragraphes, équations, listes, schémas et code.
Sa longueur dépend de ce qu'il faut expliquer. Une comparaison peut constituer
un seul objectif cohérent ; plusieurs questions indépendantes dans une carte
doivent être retravaillées. Aucun nombre uniforme de cartes par méthode
ni limite arbitraire de mots ou de durée n'est imposé.

La réponse directe reste repérable au début du verso. Les détails sont organisés
par rôle : mécanisme, raisonnement, limites, exemple. Le recto ne doit pas
révéler la réponse par un titre ou un extrait de source.

### Noyau attendu et approfondissement

Le verso distingue trois éléments :

- **Noyau attendu** : points nécessaires pour satisfaire l'objectif annoncé.
- **Approfondissement** : détails, dérivations, exemples et connexions utiles,
  conservés dans la réponse développée sans devoir tous être récités à chaque révision.
- **Erreurs bloquantes** : contresens qui invalident la réponse, par exemple
  confusion de tâche, de repère ou d'hypothèse déterminante.

Une réponse est satisfaisante si tous les points du noyau sont couverts sans
erreur bloquante. L'absence d'un détail facultatif n'est pas un échec de rappel.
Si le noyau devient trop composite pour être corrigé sans ambiguïté, des cartes
complémentaires peuvent être ajoutées en conservant une carte de synthèse développée.
Le nombre de points attendus dépend de l'objectif, sans quota uniforme.

## Familles de cartes

Les consignes suivantes illustrent la conception ; leurs réponses pédagogiques
ne sont pas encore rédigées.

| Famille | Objectif | Exemple de consigne |
| --- | --- | --- |
| Compréhension | Expliquer une méthode avec ses hypothèses | Décrire le pipeline d'ORB et le rôle de ses composants |
| Raisonnement mathématique | Interpréter ou reconstruire une relation | Expliquer une erreur de reprojection et ses conventions |
| Déroulement algorithmique | Suivre les étapes et leur raison d'être | Décrire une itération d'estimation robuste et son acceptation |
| Comparaison et décision | Choisir selon des contraintes explicites | Comparer SIFT et ORB pour un matching sous budget de calcul |
| Diagnostic | Départager les causes possibles d'un échec | Vérifier une homographie instable malgré de nombreux matches |
| Mise en pratique | Comprendre un extrait de code ou un réglage | Relier un matcher à la représentation des descripteurs |
| Évaluation | Interpréter une mesure et ses angles morts | Expliquer les conclusions permises par un score de tracking |
| Conception de système | Proposer une chaîne complète sous contraintes | Concevoir le contrôle de pièces sur une ligne cadencée, des exigences à la validation |

Les familles pertinentes sont couvertes sans multiplier les questions redondantes.
Les cloze et cartes inversées ne sont pas imposées ; leur ajout doit servir
un objectif identifié et être vérifié avec le modèle de note retenu.

## Pratique et transfert

Pour une famille prioritaire, les contenus doivent relier :

1. Une référence simple ou une baseline, avec hypothèses et résultat attendu.
2. Une variation contrôlée : bruit, échelle, occultation, seuil, cadence,
   initialisation ou autre facteur pertinent.
3. Une prédiction argumentée de l'effet de cette variation.
4. Une observation ou mesure, puis l'explication d'un éventuel écart.

Une expérimentation peut être petite et ciblée ; elle n'impose pas de réentraîner
tous les réseaux ni de construire une plateforme d'exercices séparée.
Un cas analytique est acceptable s'il est explicitement identifié comme tel.

Les scénarios de validation du transfert ne doivent pas être des copies des
exemples déjà corrigés. Pour chacune des six familles du pilote — matching,
calibration/géométrie, tracking, détection, segmentation classique et recalage
3D — deux scénarios sont préparés avec une réponse de référence : un choix
de méthode et un diagnostic sur un contexte différent.

Leur correction examine : adéquation à la tâche, hypothèses/conventions,
justification du choix, vérification discriminante et limites de la conclusion.
Chaque critère applicable doit être satisfait ; une non-applicabilité est justifiée.

Les incidents rencontrés par l'apprenant en projet sont une source de cas
réalistes. Ils sont anonymisés, ne conservent aucune donnée confidentielle
et suivent les mêmes critères de correction.

## Vérifier l'utilité des cartes

Le pilote pédagogique consigne une première tentative et un rappel différé
lors d'une autre session, aux dates choisies par l'apprenant. Aucune durée
optimale ou performance de mémorisation n'est présupposée.

L'échantillon est choisi avant les résultats et couvre toutes les familles
du pilote ainsi que chaque type de carte produit. Sa composition et ses limites
sont conservées ; les échecs ne sont pas retirés du bilan a posteriori.

Pour chaque carte essayée : résultat selon son noyau, durée de révision,
ambiguïtés, surcharge ressentie, indices révélant la réponse et modifications
nécessaires sont notés.
Une question impossible à corriger clairement, une erreur scientifique ou une
information essentielle révélée au recto empêche sa validation éditoriale
tant que le défaut n'est pas corrigé.

Les résultats de rappel et de transfert restent distincts : réciter une
explication connue ne démontre pas, seul, le diagnostic d'une scène nouvelle.

Les durées mesurées servent à estimer la charge quotidienne du premier lot de
production. Aucun plafond n'est fixé a priori. Si l'apprenant juge cette charge
excessive, les options sont de scinder les cartes trop composites, d'espacer
davantage les cartes de comparaison et de diagnostic dans un deck dédié, ou de
réduire le nombre de cartes par fiche.

## Équations, code et illustrations

- Introduire les symboles au voisinage de leur première utilisation.
- Définir repères, sens des transformations, dimensions et unités utiles.
- Expliquer le rôle et les conditions d'utilisation des équations.
- Placer les dérivations nécessaires dans le raisonnement ; les calculs de
  détail peuvent figurer dans un approfondissement lié.
- Distinguer pseudocode, extrait illustratif et exemple exécuté. Signaler un
  exemple non exécuté au lieu d'en annoncer un résultat vérifié.
- Pour un exemple exécutable : dépendances/versions pertinentes, entrées,
  résultat attendu et conditions de reproductibilité utiles.
- Un appel de bibliothèque doit éclairer l'algorithme et ne suffit pas, seul,
  à en expliquer le fonctionnement.
- Chaque visuel a une légende, une fonction explicative et une provenance ;
  les conditions de réutilisation et fichiers nécessaires sont conservés.

## Sources, revue et corrections

Une propriété algorithmique est sourcée dans un article ou une référence
scientifique primaire pertinente. Une affirmation propre à une implémentation
est reliée à sa documentation ou à son code officiel et à sa version.
Les deux niveaux sont distingués ; la sortie d'une bibliothèque ne remplace
pas la justification d'une propriété générale.

Une divergence entre sources est consignée avec les variantes et conditions
comparées. Une affirmation centrale non résolue reste marquée incertaine et
empêche de valider la fiche correspondante.

Chaque revue conserve sa date, son auteur ou relecteur, les sources examinées,
les limites et la liste des corrections. Une auto-revue est nommée comme telle ;
elle n'est pas présentée comme une validation indépendante.
Une correction scientifique identifie les cartes affectées et les remet à
relire avant publication de leur nouvelle version.

### Rédaction et appropriation

Chaque fiche et carte indique si elle a été rédigée par l'apprenant, par un
agent ou par les deux. Une affirmation centrale rédigée par un agent est
confrontée au passage précis de la source citée ; la présence d'une référence
ne suffit pas.

Relire un contenu généré n'équivaut pas à le produire. L'effet de génération
([Slamecka et Graf, 1978](https://doi.org/10.1037/0278-7393.4.6.592)) montre
qu'une information produite par l'apprenant est mieux retenue qu'une information
seulement lue, dans des tâches verbales simples. Son ampleur pour des cartes
techniques reformulées n'est pas établie ici. La répartition du travail reste
une décision ouverte de la spec.

## Grille de revue éditoriale

1. Le problème et l'objectif de rappel sont-ils explicites ?
2. Les hypothèses, conventions et limites sont-elles vérifiables ?
3. Les explications sont-elles cohérentes, et chaque source citée soutient-elle
   réellement l'affirmation ?
4. Les comparaisons donnent-elles des raisons conditionnelles ?
5. Les critères fournis permettent-ils de corriger une réponse ?
6. Les cartes apportent-elles des angles complémentaires sans doublons inutiles ?
7. Le contenu reste-t-il lisible et complet après export ?

La réussite de cette revue est distincte de la maîtrise personnelle de
l'apprenant et de la réussite technique d'un export.

## Fondement pédagogique et limite de l'inférence

[Roediger et Karpicke](https://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PsychSci.pdf)
étudient le rappel actif et la rétention différée de passages en prose. Leur
travail soutient l'intérêt du rappel pour un contenu développé, sans déterminer
une longueur optimale de flashcard ni certifier une expertise professionnelle.

Le couple fiche complète / cartes à objectif explicite est un choix de conception
adapté à la demande. Le pilote servira à en évaluer profondeur, lisibilité
et facilité de correction.
