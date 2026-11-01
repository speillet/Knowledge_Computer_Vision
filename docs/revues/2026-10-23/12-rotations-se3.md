# Review –  SO(3), SE(3) and transformation conventions –  2026-10-23

## Overview

Four flashcards audited, plus their reference note. No false claims. There are three important findings of correctability or relevance and one minor rating finding in the reference note. Corrections are applied: reference note in revision 3, IDs and objectives unchanged. Three new flashcards and a supplement were proposed; two flashcards were accepted and drafted for revision 4. The subject goes from 4 to 6 flashcards.

The flashcards were fair but too easy for the intended profile. One was solved by substituting clues on the front. Another admitted valid answers out of the kernel. The last one was a closed question.

Self-review: Agent Claude Code (`revue-cartes`). Editorial status `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | Confirmed (Solà, eq. 171) | Low: composition delivered by indices | Front that reveals the answer | `p_a` hors math | Important | Scenario of pose relative SLAM; composition formula; variant OpenCV |
| CV-SE3-002 | Confirmed (Solà, eq. 170); calculation redone | Strong: frequent confusion with `tvec` | Net Core | Agreement reference note | None | Proposed Enrichment |
| CV-SE3-003 | Confirmed (Solà, §II-E) | Forte | The question admits of other causes, such as parameterization | Family comparison without choice | Important | Conditions on the front; adjoint; criterion of choice |
| CV-SE3-004 | Confirmed (Solà, Quaternion kinematics, §3.1, eq. 140 – 143) | Forte | Yes/no question that suggests “no” | Agreement reference note | Important | Scenario, discriminating test, examples Eigen and SciPy |

reference note: notation $\operatorname{Exp}([\delta\theta]_\times)$ incorrect, because Sol to reserve `Exp` to vectors and `exp` to Lie algebra (minor).

## Corrections applied

- `vault/10-mathematiques-estimation/references/12-rotations-se3.md`, revision 3:
  - composition formula and relative pose;
  - Corrected Exp notation;
  - adjoint and transformation of the Jacobians;
  - Four choice of quaternions convention;
  - Eigen and SciPy orders dated;
  - double coverage;
  - Sources specified by equation.
- `vault/10-mathematiques-estimation/12-rotations-se3.md`: CV-SE3-001, 003 and 004 rewritten without changing the objectivees.
- Correction log: one line per separate error.

No other flashcard of the vault deals with quaternions, perturbations or composition of poses: no other flashcard to align.

## Enrichments: decision of the learner

The following additions were accepted on 2026-10-23 and drafted in revision 4:

- **CV-SE3-005**, the geodetic metric, proposed as "CV-SE3-005";
- **CV-SE3-006**, the camera axis conventions, proposed as "CV-SE3-007". It takes the next free ID: there is no numbering hole.

The reference note receives only what these two flashcards require: metric, Euler or geodesic controlled variation and axis conventions.

Not retained: projection on SO(3) and enrichment of CV-SE3-002. They remain possible later, with the sources already verified below.

The total goes from 238 to 240 flashcards. Checks after additions:

- `check_vault.py` OK, 240 flashcards;
- 34 successful tests;
- catalogue regenerated and updated;
- The inventory shows only the added IDs.

Table of proposals as submitted:

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| CV-SE3-002: link to `rvec`/`tvec` from `solvePnP` and numerical example: $R=R_z(90°)$, $t=(1,0,0)$ gives $C=(0,1,0)\neq-t$ | flashcard just but abstract; this is the most common error in project | further explanation alone | No new reminders | OpenCV 4.13.0, `calib3d.hpp`, l. 1031 – 1032; calculation of the project |
| CV-SE3-005: geodetic angular error $\theta=\arccos\frac{\operatorname{tr}(R_1^TR_2)-1}{2}$; Euler and $q/-q$ angle traps | No rotation metric in the vault, while pose, SLAM and calibration report it | evaluation | 1 flashcard; core at 3 points | Solà et al., Annex B-A; calculation of the project |
| CV-SE3-006: rotation closest to a matrix noisy by SVD, with correction of the determinant | Exit of Zhang, DLT or Umeyama not orthonormal; risk of reflection | algorithm | 1 flashcard; core at 3 points | Zhang 1998, Appendix C; Eigen `Umeyama.h` to commit 4529102e, l. 128 – 139, which follows Umeyama 1991, eq. 39 – 40 |
| CV-SE3-007: camera axis conventions OpenCV, OpenGL and ROS; passage OpenCV→OpenGL by $\mathrm{diag}(1,-1,-1)$ | No flashcard on the most common integration bug source between vision, rendering and robotics | diagnosis | 1 flashcard; core at 3 points | REP 103 to commit 6fbda48; Khronos `gluLookAt`; OpenCV 4.13.0 `calib3d.hpp`, pinhole model |
| reference note: metric rotation sections, projection on SO(3) and axis conventions; controlled variation "Euler or geodesic" (FR-033) | Sections Evaluation and Thin Failures | reference note | without flashcard | The same sources |

Calculations already executed, excluding deposit (NumPy 2.2.6, SciPy 1.13.1), built cases:

- ZYX $(30°, 89{,}9°, 0°)$ vs. $(0°, 89{,}9°, -30°)$: 30° deviation on two Euler angles, 0,052° geodesic deviation.
- $q$ and $-q$: Euclidean distance 2, angle 0.
- Matrix close to a reflection: $\det(UV^T)=-1$; after correction, $\det=+1$.
- $\mathrm{diag}(1,-1,-1)$ has a determinant $+1$ and sends the point OpenCV $(0,0,5)$, in front of the camera, to $(0,0,-5)$, in front of the OpenGL camera.

## Sources

- [Solà, Deray and Atchuthan, A micro Lie theory, v9](https://arxiv.org/html/1812.01537v9): §II-E, eq. 25 – 28; §II-F, eq. 29 – 32; Appendix B: Double Coverage, Log (eq. 135) and angle by trace, $\mathrm{Ad}_R=R$ (eq. 139); Annex D-A, Eq. 170 – 171.
- [Solà, Quaternion kinetics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508), read in HTML on ar5iv: §3.1, eq. 140 – 143, table 2, and Eigen classified Hamilton.
- [Eigen 5.0.1-dev, Quaternion](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html): warning on manufacturer and storage order.
- [SciPy 1.18.0, Rotation.from_quat](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html): Last scalar order by default, parameter `scalar_first`.
- For proposals:
  - [Zhang 1998, annexe C](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf): $R=UV^T$ under the sole constraint of orthogonality;
  - [Eigen `Umeyama.h`, commit 4529102e](https://gitlab.com/libeigen/eigen/-/blob/4529102e6d5c62be44d61d3215504eb581e18157/Eigen/src/Geometry/Umeyama.h#L128-139) ;
  - [REP 103, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst): body axes, coordinate frame `_optical` and Euler angles not recommended;
  - [Khronos, gluLookAt](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml) ;
  - [OpenCV 4.13.0, `calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L1031-L1032).
- Non-Verifiable:
  - The HTML documentation page OpenCV and the ros.org page of REP 103 block automated access; sources equivalent to the tag or commit have been read;
  - Umeyama 1991's article is paid: only its reprise by Eigen has been read.

## Checks and limitations

`check_vault.py` OK (125 Markdown, 52 reference notes, 238 flashcards) after corrections. The complete controls of the passage are recorded at the end of the subject, in the follow-up. Context7 is not available in this session. Not verified: export Anki, rendering Obsidian and AnkiDroid, mastering, independent validation.
