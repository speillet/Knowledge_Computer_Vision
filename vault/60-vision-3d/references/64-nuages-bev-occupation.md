---
id: CV-BEV
type: comparaison
domaine: d06
poles: [C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SE3", "CV-CAPTEURS", "CV-MULTICALIB"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Nuages, BEV et représentations d’occupation

## Problème, données et hypothèses

Représenter l'environnement pour la perception robotique. Distinguer nuages irréguliers, voxels, piliers, tenseur BEV et volume sémantique. Entrées : points/images et poses synchronisées ; sortie : représentation avec résolution, visibilité et repère explicités.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md) ; [CV-MULTICALIB](../../50-calibration-geometrie/references/55-calibration-multicapteurs.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

PointNet++ agrège des voisinages de points ; voxels/piliers organisent l'espace. Lift-Splat-Shoot projette des features image dans un repère spatial avec hypothèses de profondeur ; BEVFormer agrège vues et temps ; BEVFusion combine des modalités selon sa conception. Ces méthodes ne rendent pas la calibration facultative.

## Mathématiques, conventions et unités

Une grille utilise une taille de cellule en mètres et une origine/étendue. La cartographie probabiliste sépare libre, occupé et inconnu. Une Occupancy Network approxime une fonction intérieur/extérieur continue ; une SDF utilise une distance signée et une surface au niveau zéro. Aucune de ces représentations n'est automatiquement une probabilité calibrée de collision.

## Paramètres et propriétés

Résolution, limites spatiales, compensation ego, masques de visibilité et classes doivent être choisis. Augmenter la finesse augmente mémoire et sparsité ; un voxel non observé ne devient pas libre par défaut.

## Coût et implémentation

Coût des points, du volume dense/sparse et des fenêtres temporelles ; transferts et fusion comptent. Aucun modèle BEV ou robot exécuté.

## Évaluation et variation contrôlée

Variation proposée : masquer un capteur ou augmenter l'offset temporel en gardant scène et modèle fixes. Mesurer couverture, doublons et erreurs par distance, y compris l'espace inconnu.

## Échecs et diagnostic

Objets fantômes : vérifier synchronisation et ego-motion. Carte vide : contrôler axes, ROI, unités et FOV. La libre traversabilité exige davantage qu'une absence de boîte détectée.

## Alternatives et usages

Carte d'occupation géométrique, prédiction sémantique, surface reconstruite et liste d'objets remplissent des contrats distincts ; le choix dépend de l'interface aval.

## Sources et cartes

- [Qi et al., PointNet++, résumé](https://arxiv.org/abs/1706.02413)
- [Philion–Fidler, Lift-Splat-Shoot, résumé](https://arxiv.org/abs/2008.05711)
- [Liu et al., BEVFusion, résumé (version v3)](https://arxiv.org/abs/2205.13542)
- [Park et al., DeepSDF, §3](https://arxiv.org/abs/1901.05103)

- [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html).
- [BEVFormer, méthode](https://arxiv.org/abs/2203.17270).
- [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html).
- [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
- [Cartes associées](../64-nuages-bev-occupation.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
