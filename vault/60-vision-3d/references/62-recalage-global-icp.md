---
id: CV-ICP
type: pipeline
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-SE3", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Recalage global et ICP local

## Problème, données et hypothèses

Estimer une transformation rigide source→cible entre nuages exprimés dans des unités compatibles. Sorties : pose et mesures de recouvrement/résidu sous seuil donné. Une pose correcte exige plus qu'un faible RMSE sur un petit sous-ensemble.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Réduire éventuellement par voxels, estimer normales et FPFH, rechercher des correspondances et une initialisation globale robuste ; raffiner localement par ICP. ICP alterne associations et optimisation avec une hypothèse d'initialisation suffisamment proche.

## Mathématiques, conventions et unités

Point-to-point : $\sum_i\|Rp_i+t-q_i\|^2$. Point-to-plane : $\sum_i[n_i^T(Rp_i+t-q_i)]^2$, normales cibles unitaires. Résidus en mètres si nuages métriques, coûts en m². Une surface plane laisse mal contraints certains déplacements tangents et rotations ; un changement d'objectif ne crée pas les contraintes absentes.

## Paramètres et propriétés

Voxel, rayons de voisinage, seuil de correspondance, rejet et critères d'arrêt sont relatifs à l'échelle et au bruit. Les ratios du tutoriel Open3D sont illustratifs. FPFH 33D est un descripteur, pas une pose.

## Coût et implémentation

Recherche des voisins, normales, features et itérations dominent. Aucun nuage réel traité ; les API legacy et tensor Open3D ne sont pas mélangées en code supposé exécutable.

## Évaluation et variation contrôlée

Variation analytique : mêmes points et correspondances connues, puis initialisation éloignée avec plus proches voisins. Prédire un risque d'associations erronées et de minimum local. Comparer pose de référence, recouvrement et erreur hors consensus.

## Échecs et diagnostic

Faible RMSE mais pose fausse : inspecter symétrie, zone de recouvrement, seuil et répartition des contraintes. Une plaque plane peut glisser sans grands résidus point-to-plane.

## Alternatives et usages

Initialisation par features, odométrie/IMU, contraintes métier ou recalage multivue. Toujours annoncer sens de pose et qualité de la référence.

## Sources et cartes

- [Open3D, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html).
- [Open3D, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
- [Cartes associées](../62-recalage-global-icp.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
