---
id: CV-FIABILITE
type: probleme
domaine: d13
poles: [A, C, D, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Splits, annotations, calibration des scores et dérive

## Problème, données et hypothèses

Établir si un système se généralise aux scènes et usages réellement visés. Entrées : unités d'acquisition, labels, sites/temps et hypothèses ; sortie : protocole et analyse d'erreurs. La séparation de fichiers ne garantit pas l'indépendance des données.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Définir unité de split (objet, scène, séquence, patient, région), puis annoter selon un contrat contrôlé. Séparer entraînement, validation des choix et test. Examiner long-tail, ambiguïtés et sous-groupes avant de réduire tout à une moyenne.

## Mathématiques, conventions et unités

Une précision mesurée dépend du point d'exploitation et de la prévalence. Un score calibré vise une correspondance entre scores et fréquences selon protocole ; ce n'est pas la calibration géométrique d'une caméra. L'incertitude et la détection OOD doivent être évaluées sur les changements pertinents, pas déduites d'un softmax.

## Paramètres et propriétés

Taxonomie, ignore, qualité des labels, split, seuils et règles de sélection d'échantillons. Active learning choisit des annotations utiles selon une stratégie ; il peut aussi biaiser l'évaluation si le test devient adaptatif.

## Coût et implémentation

Collecte/revue d'annotations ont un coût ; calculer quelques scores ne le résume pas. Aucun résultat de généralisation ou d'incertitude réel n'est revendiqué.

## Évaluation et variation contrôlée

Baseline : split par séquence/site et modèle figé ; variation de saison/caméra, avec mêmes annotations comparables. Décomposer acquisition, distribution, labels et seuil. Rapporter erreurs et couverture, y compris les échecs rares.

## Échecs et diagnostic

Test très bon mais nouveau site faible : rechercher fuite et décalage. Une augmentation du score de confiance ne prouve pas une meilleure calibration ; fixer protocole et échantillon avant les résultats.

## Alternatives et usages

Conserver données brutes, contrats et traçabilité, puis réviser collecte/modèle sous validation. Une surveillance d'exploitation ne remplace pas le test initial.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent unité de split, sélection et calibration des probabilités. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-FIABILITE-001

**Question de travail** : Pourquoi des frames voisines d’une même vidéo ne constituent-elles pas forcément un bon train/test indépendant ?

**Réponse de référence** : Elles partagent scène, objets et conditions ; la séparation doit suivre le scénario de généralisation.

**Pourquoi les fichiers restent liés** : deux frames voisines contiennent souvent les mêmes objets, le même décor et presque la même acquisition. Un modèle peut retrouver ces indices dans le test sans avoir démontré sa généralisation vers une nouvelle scène. Des crops issus du même original peuvent renforcer encore cette proximité.

**Choix de protocole** : définir d'abord ce qui sera nouveau en exploitation, puis regrouper les données selon cette unité avant les dérivations et augmentations. Pour une nouvelle usine, séparer seulement les frames d'une séquence ne teste pas nécessairement le changement de site. Pour une autre tâche, une généralisation plus locale peut être pertinente. Contrôler doublons et recouvrements, conserver validation et test séparés, puis rapporter les groupes réellement évalués. Un split plus difficile n'est pas automatiquement meilleur ; il doit représenter le scénario annoncé sans lui transmettre indirectement des observations d'entraînement.

### Cas lié à CV-FIABILITE-005

**Question de travail** : Un détecteur garde des scores élevés sur un nouveau capteur mais se trompe davantage. Que conclure ?

**Réponse de référence** : La confiance affichée n’est pas une preuve de calibration ou de fiabilité hors distribution.

**Lecture de la confiance** : un score élevé peut être appris dans une distribution où certains indices étaient fiables, puis rester élevé lorsque ces indices changent de signification. La normalisation de la sortie ne détecte pas automatiquement ce décalage. Le nouveau capteur peut aussi rompre couleur, gamma, résolution ou plage d'intensité.

**Enquête proposée** : comparer une entrée identique à travers les deux chaînes et mesurer les erreurs sur un lot annoté représentatif du nouveau capteur. Examiner calibration et rejet au point d'exploitation, avec les mêmes règles de localisation. Une chute de qualité nécessite une action, mais le score seul ne dit pas s'il faut corriger le prétraitement, recollecter ou adapter le modèle. Conserver une validation indépendante pour vérifier la correction. Une surveillance des distributions peut donner une alarme utile ; elle ne démontre pas à elle seule une dérive de précision sans référence appropriée.

**Repère documentaire de cette passe** : [Cawley et Talbot 2010](https://www.jmlr.org/papers/v11/cawley10a.html), résumé et biais de sélection. Les autres développements figurent dans les [cartes associées](../133-donnees-generalisation.md).

## Sources et cartes

- [Ovadia et al., 2019, résumé/introduction](https://arxiv.org/abs/1906.02530) : limites de calibration sous changement de distribution.
- [Cawley–Talbot, 2010, résumé et introduction](https://www.jmlr.org/papers/v11/cawley10a.html) : surajustement de la sélection et biais d’évaluation.

- [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881).
- [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html).
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
- [Cartes associées](../133-donnees-generalisation.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
