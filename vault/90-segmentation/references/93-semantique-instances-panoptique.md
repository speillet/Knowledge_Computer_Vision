---
id: CV-SEGMENTATION
type: comparaison
domaine: d09
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# Segmentation sémantique, instances et panoptique

## Problème, données et hypothèses

Définir la sortie avant de choisir architecture et loss : classe par pixel, masques d'objets comptables ou partition panoptique stuff/things sans recouvrement entre segments. Entrées : images et annotations cohérentes ; sorties : logits/masques/classes selon le contrat.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

U-Net exploite encodeur–décodeur et liens de résolution ; DeepLab exploite notamment convolutions dilatées et contexte selon variante ; Mask R-CNN associe détection et masque par instance. nnU-Net automatise des choix de pipeline en médical, au-delà d'un simple nom de réseau.

## Mathématiques, conventions et unités

IoU de classe utilise TP/(TP+FP+FN) ; Dice binaire vaut $2TP/(2TP+FP+FN)$ sous convention de classes/vides fixée. PQ combine recouvrement et reconnaissance d'instances dans un protocole d'appariement. Les moyennes et pixels ignorés doivent être annoncés ; les losses choisies ne sont pas ces métriques automatiquement.

## Paramètres et propriétés

Classes, background/void, résolution, stride, augmentations cohérentes image–masque, déséquilibre et seuils. Les petits objets et frontières demandent un protocole spécifique. Les IDs d'instances n'ont pas de valeur numérique sémantique.

## Coût et implémentation

Mémoire des features denses, crops, overlap et reconstruction complète comptent. Aucun entraînement exécuté ; ne pas confondre score sur patch et performance du volume ou de l'image entière.

## Évaluation et variation contrôlée

Baseline : modèle simple et protocole par scène/patient ; varier taille des crops ou résolution et inspecter petites structures. Évaluer recouvrement, instances et frontières selon usage, pas seulement la loss moyenne.

## Échecs et diagnostic

Pixels corrects mais objets fusionnés : la tâche/annotation peut être sémantique plutôt qu'instance. Coutures sur tuiles : contrôler overlap, padding et fusion avant de changer l'architecture.

## Alternatives et usages

Méthodes classiques sur acquisition stable ; segmentation dense ou prompts selon besoin et supervision. La performance algorithmique ne prouve pas l'utilité clinique.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent unité de sortie et agrégation des erreurs de segmentation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-SEGMENTATION-001

**Question de travail** : Quelle différence sépare segmentation sémantique, d’instances et panoptique ?

**Réponse de référence** : Sémantique : classe par pixel ; instances : séparer objets comptables ; panoptique : partition sans recouvrement, avec classe et instance pour things, classe pour stuff.

**Exemple de contrat** : deux personnes qui se touchent partagent le label sémantique personne mais doivent avoir des IDs d'instance différents si l'on veut les compter. Une région de ciel relève du stuff dans le contrat panoptique usuel et ne demande pas la même séparation en objets comptables.

**Conséquence pour les données** : un masque de classe ne contient pas forcément la frontière entre deux instances de même classe. Un modèle entraîné sur ces seuls labels ne reçoit donc pas explicitement cette information. Les identifiants d'instances peuvent être renumérotés sans changer la partition ; leur valeur numérique n'exprime pas une quantité à interpoler. Définir aussi pixels ignorés et politique de recouvrement avant l'évaluation. Un score de recouvrement par classe, un score d'instances et PQ testent des aspects différents : choisir celui qui correspond au livrable demandé, avec des mesures complémentaires si plusieurs propriétés comptent.

### Cas lié à CV-SEGMENTATION-004

**Question de travail** : Pourquoi une bonne Dice moyenne ne suffit-elle pas pour conclure à l’utilité d’une segmentation médicale ?

**Réponse de référence** : Elle mesure un recouvrement selon protocole ; validation externe, frontières, cas rares, unités physiques et usage visé apportent d’autres preuves.

**Pourquoi le recouvrement est partiel** : une région volumineuse peut conserver une forte Dice malgré une erreur localisée sur une frontière importante. Une petite structure manquée peut également peser peu dans certaines agrégations. Le score doit donc être interprété dans ses unités, son niveau d'agrégation et ses conventions de vides.

**Évaluation technique proposée** : séparer patients et sites, mesurer frontières dans la géométrie physique appropriée et conserver les cas rares ou absents. Définir la sortie effectivement utile et une référence indépendante, puis examiner les échecs individuellement. Une amélioration sur une validation interne peut dépendre de l'acquisition et ne pas se transférer à un autre site. Ces contrôles décrivent la validité technique du modèle ; ils ne constituent pas un avis médical ni une preuve d'utilité clinique. Le raisonnement senior garde distincts performance de segmentation, reproductibilité du protocole et conséquence dans l'usage envisagé.

**Repère documentaire de cette passe** : [Kirillov et al., Panoptic Segmentation](https://arxiv.org/html/1801.00868v3), définition de la tâche et Panoptic Quality. Les autres développements figurent dans les [cartes associées](../93-semantique-instances-panoptique.md).

## Sources et cartes

- [Reinke et al., 2024, pièges des métriques, P1–P3](https://www.nature.com/articles/s41592-023-02150-0) : tâche, frontières, petites structures et agrégation.

- [U-Net](https://arxiv.org/abs/1505.04597).
- [DeepLabv3+](https://arxiv.org/abs/1802.02611).
- [Mask R-CNN](https://arxiv.org/abs/1703.06870).
- [Panoptic Segmentation, tâche/PQ](https://arxiv.org/abs/1801.00868).
- [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
- [Cartes associées](../93-semantique-instances-panoptique.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
