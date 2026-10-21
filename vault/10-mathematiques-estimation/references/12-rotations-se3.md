---
id: CV-SE3
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# SO(3), SE(3) et conventions de transformation

## Problème, données et hypothèses

Composer des poses sans mélanger sens des transformations, axes ou unités. Entrées : rotations et translations avec repères nommés ; sortie : coordonnées transformées ou pose composée. Une matrice homogène n'indique pas son sens sans une convention explicite.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Une rotation conserve les normes et l’orientation de la base (déterminant +1), mais change généralement la direction d’un vecteur ; une pose rigide ajoute une translation. Composer dans l'ordre des repères, inverser algébriquement et tester un point connu. Une optimisation utilise une petite perturbation à trois paramètres pour la rotation.

## Mathématiques, conventions et unités

Définir $p_a=R_{ab}p_b+t_{ab}$ et $T_{ac}=T_{ab}T_{bc}$. $R^TR=I$, $\det R=1$ ; $T^{-1}$ utilise $R^T$ et $-R^Tt$. Les translations ont une unité de longueur ; les petites rotations sont en radians. $R'=R\operatorname{Exp}([\delta\theta]_\times)$ et $R'=\operatorname{Exp}([\delta\theta]_\times)R$ sont des perturbations locale et globale différentes.

## Paramètres et propriétés

Préciser ordre des composantes du quaternion, convention active/passive et normalisation. Un quaternion a quatre composantes et trois degrés de liberté ; q et −q représentent la même rotation. Les angles d'Euler ont des singularités de paramétrisation.

## Coût et implémentation

Les opérations élémentaires coûtent peu ; les erreurs de convention ont un effet sur tous les capteurs. Pseudocode illustratif : nommer les repères → composer → vérifier identité/inverse → tester un point ; aucune bibliothèque de groupes n'est exécutée.

## Évaluation et variation contrôlée

Variation analytique : inverser l'ordre de deux rotations non parallèles. Prédire une pose différente ; vérifier sur un axe connu. Tester ensuite qu'une transformation suivie de son inverse restitue le point, à tolérance numérique près.

## Échecs et diagnostic

Objets tournant dans le mauvais sens : vérifier axes, degrés/radians et inversion. Une pose visuellement plausible ne suffit pas ; contrôler points repères et composition des extrinsèques.

## Alternatives et usages

Matrices pour composition, quaternions pour stockage/interpolation, coordonnées tangentielles pour optimisation ; ne pas mélanger leurs Jacobiennes sans transformation.

## Sources et cartes

- [Solà et al., A micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Solà et al., A micro Lie theory, §§II-E–II-H](https://arxiv.org/html/1812.01537v9#S2.SS5).

- [Solà, Quaternion kinematics, §§2–4](https://arxiv.org/abs/1711.02508).
- [Cartes associées](../12-rotations-se3.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
