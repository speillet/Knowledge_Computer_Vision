---
id: CV-SE3
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 4
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

Définir $p_a=R_{ab}p_b+t_{ab}$ et $T_{ac}=T_{ab}T_{bc}$, soit $(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc})$ : $t_{bc}$, exprimée dans $b$, est tournée dans $a$ avant l'addition (Solà et al., équation 171). $R^TR=I$, $\det R=1$ ; $T^{-1}=(R^T,-R^Tt)$ (équation 170). Pour une pose relative entre deux caméras données dans le monde, $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}$. Les translations ont une unité de longueur ; les petites rotations sont en radians.

$R'=R\operatorname{Exp}(\delta\theta)$ et $R'=\operatorname{Exp}(\delta\theta)R$ sont des perturbations locale (à droite) et globale (à gauche) différentes (§II-E, équations 25–28). L'adjoint les relie : $\operatorname{Exp}(\mathrm{Ad}_R\,\delta\theta_L)R=R\operatorname{Exp}(\delta\theta_L)$, avec $\mathrm{Ad}_R=R$ pour SO(3) (§II-F, équations 29–32 ; annexe B-C, équation 139). Une jacobienne par rapport à l'incrément local vaut donc $J_L=J_GR$. `Exp` prend un vecteur de $\mathbb R^3$ ; `exp` prend la matrice antisymétrique $[\delta\theta]_\times$.

## Paramètres et propriétés

Préciser ordre des composantes du quaternion, convention active/passive et normalisation. Solà (Quaternion kinematics, §3.1, équations 140–143) distingue quatre choix binaires : ordre des composantes, algèbre $ij=k$ ou $ij=-k$, fonction active ou passive, sens local→global ou l'inverse. Sa table 2 oppose Hamilton à JPL ; son §3.1.1 classe Eigen comme Hamilton malgré son stockage scalaire en dernier. Côté implémentation, le constructeur `Quaternion(w,x,y,z)` d'Eigen 5.0.1-dev prend le scalaire en premier mais stocke `[x,y,z,w]` ; `Rotation.from_quat` de SciPy 1.18.0 suppose le scalaire en dernier sauf `scalar_first=True`. Un quaternion a quatre composantes et trois degrés de liberté ; $q$ et $-q$ représentent la même rotation (micro Lie theory, annexe B). Les angles d'Euler ont des singularités de paramétrisation.

## Coût et implémentation

Les opérations élémentaires coûtent peu ; les erreurs de convention ont un effet sur tous les capteurs. Pseudocode illustratif : nommer les repères → composer → vérifier identité/inverse → tester un point ; aucune bibliothèque de groupes n'est exécutée.

## Évaluation et variation contrôlée

Variation analytique : inverser l'ordre de deux rotations non parallèles. Prédire une pose différente ; vérifier sur un axe connu. Tester ensuite qu'une transformation suivie de son inverse restitue le point, à tolérance numérique près.

Mesurer une erreur de rotation par l'angle de la rotation résiduelle : $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, l'angle de $\operatorname{Log}(R^T\hat R)$ (micro Lie theory, annexe B-A, équation 135). Depuis des quaternions unitaires, $\theta=2\arccos|\langle q_1,q_2\rangle|$ ; la valeur absolue absorbe la double couverture, formule dérivée par le projet. Borner l'argument de l'arccos dans $[-1,1]$ ; près de $\theta=0$, l'arccos de la trace perd de la précision, et le Log ou la formule par quaternion sont préférables.

Variation contrôlée, calculée le 2026-10-23 hors dépôt (NumPy 2.2.6, SciPy 1.13.1). Baseline : écart composante par composante d'angles d'Euler ZYX. Facteur varié : la mesure, à rotations identiques. Prédiction : divergence près du tangage de 90°. Résultat : $(30°;89{,}9°;0°)$ et $(0°;89{,}9°;-30°)$ diffèrent de 30° sur deux angles, contre 0,052° en angle géodésique ; $q$ et $-q$ sont à distance euclidienne 2 pour un angle nul. Cas construits, pas des mesures de système.

## Échecs et diagnostic

Objets tournant dans le mauvais sens : vérifier axes, degrés/radians et inversion. Une pose visuellement plausible ne suffit pas ; contrôler points repères et composition des extrinsèques.

Conventions d'axes caméra. OpenCV projette $x'=X_c/Z_c$, $y'=Y_c/Z_c$ (`calib3d.hpp` 4.13.0, l. 94–118) : les points visibles ont $Z_c>0$, et avec $v=f_yy'+c_y$ et des lignes qui croissent vers le bas, $Y_c$ pointe vers le bas, déduction du projet. ROS (REP 103) fixe le corps en $x$ avant, $y$ gauche, $z$ haut ; son repère `_optical` place $z$ avant, $x$ droite, $y$ bas, comme OpenCV. En OpenGL, `gluLookAt` envoie le point visé sur l'axe $-z$ et la direction « haut » sur $+y$. Passer d'OpenCV à OpenGL revient donc à appliquer $M=\mathrm{diag}(1,-1,-1)$, rotation de 180° autour de $x$ et de déterminant $+1$. Elle se compose à droite d'une pose caméra→monde, $T^{gl}_{wc}=T^{cv}_{wc}M$, et à gauche d'une matrice monde→caméra, $V^{gl}=M\,T^{cv}_{cw}$. Symptômes : scène derrière la caméra ou image retournée. Une seule inversion d'axe, de déterminant $-1$, est une réflexion. Test : un point connu devant la caméra doit le rester après conversion.

## Alternatives et usages

Matrices pour composition, quaternions pour stockage/interpolation, coordonnées tangentielles pour optimisation ; ne pas mélanger leurs Jacobiennes sans transformation.

## Sources et cartes

- [Solà et al., A micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Solà et al., A micro Lie theory, §II-E, équations 25–28, §II-F, équations 29–32, annexe B et équation 139](https://arxiv.org/html/1812.01537v9#S2.SS5).

- [Solà, Quaternion kinematics, §3.1, équations 140–143 et table 2](https://arxiv.org/abs/1711.02508).
- [Eigen 5.0.1-dev, Quaternion (consulté le 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html) : ordre du constructeur et du stockage.
- [SciPy 1.18.0, Rotation.from_quat (consulté le 2026-10-23)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html) : ordre scalaire en dernier par défaut.
- [OpenCV 4.13.0, `calib3d.hpp`, modèle sténopé, l. 94–118, et `solvePnP`, l. 1031–1032](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118) : la page HTML de documentation refuse les accès automatisés, l'en-tête source au tag a été lu.
- [REP 103, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst) : Axis Orientation, Suffix Frames, Rotation Representation.
- [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml).
- [Cartes associées](../12-rotations-se3.md) : CV-SE3-001 à 006.

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet. Révisions 3 et 4 : auto-revue `revue-cartes` par Agent Claude Code le 2026-10-23, corrections puis enrichissements acceptés par l'apprenant, sans validation indépendante.
