---
id: CV-POSE3D
type: comparaison
domaine: d08
poles: [A, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [PointPillars, architecture](https://arxiv.org/abs/1812.05784).
- [CenterPoint, méthode](https://arxiv.org/abs/2006.11275).
- [nuScenes, detection evaluation](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
- [Cartes associées](../84-detection-pose-3d.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
