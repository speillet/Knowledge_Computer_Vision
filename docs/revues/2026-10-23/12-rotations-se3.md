# Revue — SO(3), SE(3) et conventions de transformation — 2026-10-23

## Synthèse

Quatre cartes auditées, plus leur fiche. Aucune affirmation fausse. Il y a
trois constats importants de corrigibilité ou de pertinence et un constat
mineur de notation dans la fiche. Les corrections sont appliquées : fiche en
révision 3, IDs et objectifs inchangés. Trois nouvelles cartes et un
complément ont été proposés ; deux cartes ont été acceptées et rédigées en
révision 4. Le sujet passe de 4 à 6 cartes.

Les cartes étaient justes mais trop faciles pour le profil visé. L'une se
résolvait par substitution d'indices au recto. Une autre admettait des
réponses valides hors du noyau. La dernière était une question fermée.

Auto-revue : Agent Claude Code (`revue-cartes`). Statut éditorial `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | Confirmé (Solà, éq. 171) | Faible : composition livrée par les indices | Recto qui révèle la réponse | `p_a` hors math | Important | Scénario de pose relative SLAM ; formule de composition ; variante OpenCV |
| CV-SE3-002 | Confirmé (Solà, éq. 170) ; calcul refait | Forte : confusion fréquente avec `tvec` | Noyau net | Accord fiche | Aucun | Enrichissement proposé |
| CV-SE3-003 | Confirmé (Solà, §II-E) | Forte | La question admet d'autres causes, comme la paramétrisation | Famille comparaison sans choix | Important | Conditions au recto ; adjoint ; critère de choix |
| CV-SE3-004 | Confirmé (Solà, Quaternion kinematics, §3.1, éq. 140–143) | Forte | Question oui/non qui suggère « non » | Accord fiche | Important | Scénario, test discriminant, exemples Eigen et SciPy |

Fiche : notation $\operatorname{Exp}([\delta\theta]_\times)$ incorrecte, car
Solà réserve `Exp` aux vecteurs et `exp` à l'algèbre de Lie (mineur).

## Corrections appliquées

- `vault/10-mathematiques-estimation/references/12-rotations-se3.md`,
  révision 3 :
  - formule de composition et pose relative ;
  - notation Exp corrigée ;
  - adjoint et transformation des jacobiennes ;
  - quatre choix de convention des quaternions ;
  - ordres Eigen et SciPy datés ;
  - double couverture ;
  - sources précisées par équation.
- `vault/10-mathematiques-estimation/12-rotations-se3.md` : CV-SE3-001, 003
  et 004 réécrites sans changer d'objectif.
- Journal de correction : une ligne par erreur distincte.

Aucune autre carte du vault ne traite quaternions, perturbations ou
composition de poses : pas d'autre carte à aligner.

## Enrichissements : décision de l'apprenant

Les ajouts suivants ont été acceptés le 2026-10-23 et rédigés en révision 4 :

- **CV-SE3-005**, la métrique géodésique, proposée comme « CV-SE3-005 » ;
- **CV-SE3-006**, les conventions d'axes caméra, proposée comme
  « CV-SE3-007 ». Elle prend le prochain ID libre : il n'y a pas de trou
  de numérotation.

La fiche reçoit seulement ce que ces deux cartes exigent : métrique,
variation contrôlée « Euler ou géodésique » et conventions d'axes.

Non retenus : la projection sur SO(3) et l'enrichissement de CV-SE3-002.
Ils restent possibles plus tard, avec les sources déjà vérifiées ci-dessous.

Le total passe de 238 à 240 cartes. Contrôles après ajouts :

- `check_vault.py` OK, 240 cartes ;
- 34 tests réussis ;
- catalogue régénéré puis à jour ;
- l'inventaire ne montre que les IDs ajoutés.

Table des propositions telle que soumise :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| CV-SE3-002 : lien avec `rvec`/`tvec` de `solvePnP` et exemple chiffré : $R=R_z(90°)$, $t=(1,0,0)$ donne $C=(0,1,0)\neq-t$ | Carte juste mais abstraite ; c'est l'erreur la plus courante en projet | approfondissement seul | aucun nouveau rappel | OpenCV 4.13.0, `calib3d.hpp`, l. 1031–1032 ; calcul du projet |
| CV-SE3-005 : erreur angulaire géodésique $\theta=\arccos\frac{\operatorname{tr}(R_1^TR_2)-1}{2}$ ; pièges des angles d'Euler et de $q/-q$ | Aucune métrique de rotation dans le vault, alors que pose, SLAM et calibration en rapportent | evaluation | 1 carte ; noyau à 3 points | Solà et al., annexe B-A ; calcul du projet |
| CV-SE3-006 : rotation la plus proche d'une matrice bruitée par SVD, avec correction du déterminant | Sortie de Zhang, DLT ou Umeyama non orthonormée ; risque de réflexion | algorithme | 1 carte ; noyau à 3 points | Zhang 1998, annexe C ; Eigen `Umeyama.h` au commit 4529102e, l. 128–139, qui suit Umeyama 1991, éq. 39–40 |
| CV-SE3-007 : conventions d'axes caméra OpenCV, OpenGL et ROS ; passage OpenCV→OpenGL par $\mathrm{diag}(1,-1,-1)$ | Aucune carte sur la source de bug d'intégration la plus fréquente entre vision, rendu et robotique | diagnostic | 1 carte ; noyau à 3 points | REP 103 au commit 6fbda48 ; Khronos `gluLookAt` ; OpenCV 4.13.0 `calib3d.hpp`, modèle sténopé |
| Fiche : sections métrique de rotation, projection sur SO(3) et conventions d'axes ; variation contrôlée « Euler ou géodésique » (FR-033) | Rubriques Évaluation et Échecs minces | fiche | sans carte | mêmes sources |

Calculs déjà exécutés, hors dépôt (NumPy 2.2.6, SciPy 1.13.1), cas
construits :

- ZYX $(30°, 89{,}9°, 0°)$ contre $(0°, 89{,}9°, -30°)$ : 30° d'écart sur
  deux angles d'Euler, 0,052° d'écart géodésique.
- $q$ et $-q$ : distance euclidienne 2, angle 0.
- Matrice proche d'une réflexion : $\det(UV^T)=-1$ ; après correction,
  $\det=+1$.
- $\mathrm{diag}(1,-1,-1)$ a un déterminant $+1$ et envoie le point OpenCV
  $(0,0,5)$, devant la caméra, sur $(0,0,-5)$, devant la caméra OpenGL.

## Sources

- [Solà, Deray et Atchuthan, A micro Lie theory, v9](https://arxiv.org/html/1812.01537v9) :
  §II-E, éq. 25–28 ; §II-F, éq. 29–32 ; annexe B : double couverture, Log
  (éq. 135) et angle par la trace, $\mathrm{Ad}_R=R$ (éq. 139) ; annexe D-A,
  éq. 170–171.
- [Solà, Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508),
  lu en HTML sur ar5iv : §3.1, éq. 140–143, table 2, et Eigen classé Hamilton.
- [Eigen 5.0.1-dev, Quaternion](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html) :
  avertissement sur l'ordre du constructeur et du stockage.
- [SciPy 1.18.0, Rotation.from_quat](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html) :
  ordre scalaire en dernier par défaut, paramètre `scalar_first`.
- Pour les propositions :
  - [Zhang 1998, annexe C](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) :
    $R=UV^T$ sous la seule contrainte d'orthogonalité ;
  - [Eigen `Umeyama.h`, commit 4529102e](https://gitlab.com/libeigen/eigen/-/blob/4529102e6d5c62be44d61d3215504eb581e18157/Eigen/src/Geometry/Umeyama.h#L128-139) ;
  - [REP 103, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst) :
    axes du corps, repère `_optical` et angles d'Euler déconseillés ;
  - [Khronos, gluLookAt](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml) ;
  - [OpenCV 4.13.0, `calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L1031-L1032).
- Non vérifiables :
  - la page HTML de documentation OpenCV et la page ros.org de REP 103
    bloquent les accès automatisés ; les sources équivalentes au tag ou au
    commit ont été lues ;
  - l'article d'Umeyama 1991 est payant : seule sa reprise par Eigen a été
    lue.

## Contrôles et limites

`check_vault.py` OK (125 Markdown, 52 fiches, 238 cartes) après corrections.
Les contrôles complets du passage sont consignés à la fin du sujet, dans le
suivi. Context7 n'est pas disponible dans cette session. Non vérifiés :
export Anki, rendu Obsidian et AnkiDroid, maîtrise, validation indépendante.
