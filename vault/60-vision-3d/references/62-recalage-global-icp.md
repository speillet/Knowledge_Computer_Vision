---
id: CV-ICP
type: pipeline
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent initialisation, correspondances et directions peu contraintes. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-ICP-001

**Question de travail** : Pourquoi combiner FPFH/RANSAC puis ICP plutôt que lancer ICP depuis n’importe quelle pose ?

**Réponse de référence** : L’initialisation globale cherche une zone compatible à partir de correspondances ; ICP affine localement et peut converger sur de mauvaises associations.

**Pourquoi l'initialisation compte** : ICP construit ou actualise des associations à partir de la pose courante. Si cette pose est éloignée, les plus proches voisins peuvent représenter d'autres surfaces ; optimiser sur ces paires peut renforcer un mauvais alignement local. La recherche globale utilise d'autres indices pour proposer une région de pose avant le raffinement.

**Exemple construit** : deux pieds identiques d'une pièce peuvent offrir deux alignements locaux plausibles. Un faible résidu après ICP ne désigne pas automatiquement le bon pied. Contrôler l'orientation et la translation finales, le recouvrement et des surfaces distinctives réservées. Consigner sens source→cible et unités avant toute comparaison. Les features géométriques et RANSAC apportent des hypothèses utiles ; elles restent limitées par texture géométrique, symétries et recouvrement. Une odométrie ou une contrainte métier peut fournir une autre initialisation si elle est justifiée et évaluée.

### Cas lié à CV-ICP-005

**Question de travail** : Point-to-plane remplace-t-il toujours avantageusement point-to-point ?

**Réponse de référence** : Il exploite des normales fiables et une géométrie qui contraint les mouvements utiles ; il peut être mal posé sur certaines surfaces ou normales bruitées.

**Comparaison des informations utilisées** : point-to-point pénalise une différence de positions selon trois composantes ; point-to-plane utilise une approximation locale de surface. Lorsque les normales et l'initialisation sont adaptées, cette approximation peut être efficace. Si les normales sont instables ou la géométrie pauvre, le critère peut perdre son intérêt ou laisser certaines directions peu contraintes.

**Ablation construite** : conserver nuages, correspondances initiales, seuil et référence, puis comparer les variantes en faisant varier séparément le bruit des normales et le recouvrement. Mesurer erreur de pose, convergence, échecs et coût. Une baisse du résidu propre à une variante n'est pas directement comparable au résidu d'une autre formulation. Le bon choix dépend de la surface observée et de la précision demandée. Ne pas utiliser un seul cas plan favorable pour annoncer une supériorité sur toutes les pièces et toutes les initialisations.

**Repère documentaire de cette passe** : [Open3D 0.19, ICP registration](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html), Point-to-plane ICP et évaluation. Les autres développements figurent dans les [cartes associées](../62-recalage-global-icp.md).

## Sources et cartes

- [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html).
- [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
- [Cartes associées](../62-recalage-global-icp.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
