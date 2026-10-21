---
id: CV-EPIPOLAIRE
type: methode
domaine: d05
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SE3", "CV-ZHANG"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Épipolaire, PnP et triangulation

## Problème, données et hypothèses

Distinguer contraintes entre deux vues, pose depuis points 3D connus et reconstruction de points. Les coordonnées doivent être corrigées de distorsion ou traitées par un modèle cohérent ; préciser repère et échelle des points.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-ZHANG](52-calibration-zhang.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

La fondamentale relie points pixels ; l'essentielle exploite les intrinsèques. PnP estime la pose objet→caméra à partir de 3D–2D. La triangulation cherche un point 3D expliquant plusieurs rayons ; faible parallaxe et bruit peuvent rendre sa profondeur très incertaine.

## Mathématiques, conventions et unités

Pour $X_2=RX_1+t$, $E=[t]_\times R$ et $x_2^TEx_1=0$ en coordonnées normalisées. En pixels idéaux $F=K_2^{-T}EK_1^{-1}$. La direction t issue de deux vues monoculaires n'a pas d'échelle métrique. PnP renvoie t dans l'unité des points 3D ; la caméra a centre $-R^Tt$.

## Paramètres et propriétés

Minimum, ambiguïtés et raffinement dépendent de la variante. P3P peut donner plusieurs solutions ; dans OpenCV 4.13.0, `solvePnP(..., SOLVEPNP_P3P)` exige quatre points, tandis que `solveP3P` accepte trois correspondances et retourne les solutions candidates. Vérifier chiralité, parallaxe et résidus, pas le seul nombre de points.

## Coût et implémentation

RANSAC, solveur et optimisation aval ont des coûts différents. Aucun appel OpenCV exécuté ; les conventions `solvePnP` ont été vérifiées dans la documentation 4.13.

## Évaluation et variation contrôlée

Cas analytique : deux rayons presque parallèles donnent une profondeur sensible à une petite erreur angulaire. Variation proposée : modifier baseline ou distance en conservant bruit image ; rapporter incertitude et erreur 3D sur référence.

## Échecs et diagnostic

Profondeur immense avec petit résidu : examiner parallaxe, échelle, chiralité et mauvaise association. Pose inversée : contrôler monde→caméra et axes.

## Alternatives et usages

Homographie pour un plan ; PnP si carte 3D connue ; deux vues puis reconstruction si carte inconnue. Ne pas interpréter toute translation comme métrique.

## Sources et cartes

- [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
- [Cartes associées](../53-epipolaire-pnp-triangulation.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
