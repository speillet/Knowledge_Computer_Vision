---
id: CV-POSE3D
type: comparaison
domaine: d08
poles: [A, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SE3", "CV-BEV", "CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Détection 3D, pose d’objet et pose articulée

## Problème, données et hypothèses

Comparer des sorties souvent appelées « pose » : boîte 3D, transformation rigide d'objet, squelette articulé 2D/3D. Entrées/annotations et métriques diffèrent. Une boîte orientée n'est pas une reconstruction complète de la forme.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-BEV](../../60-vision-3d/references/64-nuages-bev-occupation.md) ; [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

PointPillars encode des piliers en pseudo-image pour une tête de détection ; CenterPoint prédit des centres et attributs 3D selon sa variante. La pose d'objet estime une transformation d'un modèle ; la pose articulée estime des keypoints et leur structure.

## Mathématiques, conventions et unités

Définir repère, unité des dimensions, ancrage de la boîte et axe/signe du yaw, généralement mètres/radians en données métriques. Pour une pose rigide, une symétrie de l'objet peut rendre plusieurs rotations visuellement équivalentes. Une erreur de joint doit préciser 2D pixels ou 3D longueur et éventuel alignement.

## Paramètres et propriétés

ROI, discrétisation, angles, visibilité, taxonomie et association de points. Ne pas mélanger conventions des datasets. Les données futures et la compensation ego sont des choix de protocole.

## Coût et implémentation

Nombre de points, voxels/piliers, résolution BEV et posttraitement coûtent différemment. Aucun réseau 3D, squelette ou solveur de pose exécuté.

## Évaluation et variation contrôlée

Variation proposée : raréfier les points avec distance, puis masquer des joints séparément. Évaluer sorties dans le repère d'origine et rapporter symétries/visibilité. L'AP nuScenes n'est pas simplement l'AP COCO avec une IoU 3D.

## Échecs et diagnostic

Yaw décalé de 90° : vérifier ordre longueur/largeur et convention d'axe avant le modèle. Pose d'objet ambiguë : tester symétrie et mesure réellement observable.

## Alternatives et usages

PnP si points 3D connus, modèle appris si observations adaptées, représentation d'occupation pour d'autres besoins ; conserver des tâches distinctes.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent contrat métrique et ambiguïtés de pose/symétrie. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-POSE3D-001

**Question de travail** : Pourquoi ne pas comparer directement score de détection 3D et erreur de pose articulée ?

**Réponse de référence** : Boîtes/classes et articulations sont des sorties différentes avec annotations, correspondances et métriques différentes.

**Différence des inconnues** : une détection 3D fournit généralement une localisation, des dimensions et une orientation de boîte avec une classe. Une pose articulée décrit des positions de joints et leurs relations ; une pose rigide d'objet relie un modèle à une observation. Ces sorties ne codent pas la même géométrie.

**Exemple construit** : une boîte entourant un piéton ne dit pas où se trouvent ses poignets. Un squelette bien ajusté ne fournit pas nécessairement une boîte 3D métrique dans le repère capteur. Définir d'abord l'information consommée par le module aval, ses unités et le traitement des points invisibles. Choisir ensuite correspondances et alignement autorisés dans l'évaluation. Une comparaison de scores hétérogènes peut être trompeuse même lorsque tous les articles emploient le mot pose. Une mesure doit être interprétée par son protocole, pas par son seul intitulé.

### Cas lié à CV-POSE3D-004

**Question de travail** : Un objet cylindrique est localisé correctement mais sa rotation autour de l’axe varie. Que vérifier ?

**Réponse de référence** : La symétrie visuelle et la définition de pose/évaluation : cette composante peut être ambiguë avec les observations disponibles.

**Intuition d'identifiabilité** : si plusieurs rotations de l'objet produisent la même apparence sous les observations disponibles, la vision ne peut pas toujours choisir une orientation unique. Le modèle d'évaluation doit alors préciser comment les symétries sont traitées et quelles parties de la pose restent observables.

**Exemple construit** : un cylindre sans marque distinctive peut être invariant à une rotation autour de son axe. Un marquage visible brise éventuellement cette ambiguïté ; une meilleure optimisation seule ne le fait pas apparaître. Si une étape d'assemblage exige cet angle, prévoir l'information supplémentaire et la mesurer. Une boîte orientée ou un score de pose faible ne suffit pas à trancher un degré de liberté symétrique. Rapporter la convention et l'incertitude évite de pénaliser arbitrairement des solutions visuellement équivalentes ou, inversement, de masquer une erreur observable sur un objet marqué.

**Repère documentaire de cette passe** : [BOP, Tasks](https://bop.felk.cvut.cz/tasks/), définition des tâches et métriques de pose. Les autres développements figurent dans les [cartes associées](../84-detection-pose-3d.md).

## Sources et cartes

- [BOP, tâches et métriques VSD/MSSD/MSPD](https://bop.felk.cvut.cz/tasks/), consulté le 2026-10-20 : symétries et visibilité.
- [OpenPose, résumé et fig. 2](https://arxiv.org/abs/1611.08050) : points et association pour la pose articulée 2D.

- [PointPillars, architecture](https://arxiv.org/abs/1812.05784).
- [CenterPoint, méthode](https://arxiv.org/abs/2006.11275).
- [nuScenes, detection evaluation](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
- [Cartes associées](../84-detection-pose-3d.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
