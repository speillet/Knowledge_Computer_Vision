# Review — SO(3), SE(3) and transformation conventions — 2026-11-14

## Overview

6 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 10 to revision 11. Highest severity per card before correction:
0 blocking, 1 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

No scientific error was found in revision 10. Its body held about 760 words; most
contract sections were one to three sentences long, and the camera-axis and
quaternion passages carried mistranslations ("the manufacturer `Quaternion(w,x,y,z)`",
"local sense →global", "lines growing downwards", "the coordinate frame `_optical`
place $z$ front"). The cards repeated several of them, one expected answer (CV-SE3-006)
being hard to read as a grading criterion.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}$ and composition rule: confirmed (Solà et al., App. D-A, eq. 170–171). Round-trip example ($(0,-1,0)$ m): recomputed. "Check: … originally applied to $c_2$" meant "applied to the origin of $c_2$" | Reasoning: named-frame composition | 2 criteria; 395 → 392 words | Aligned with the reference appendix | Minor | Language fixes in the explanation and blocking errors |
| CV-SE3-002 | $C_w=-R^Tt$ and inverse $(R^T,-R^Tt)$: confirmed (eq. 170). Expected answer said "reverse pose"; explanation said "worldwide", "the radius" (ray) and "Digitally verify that the center found originally projects camera" | Practice: pose inversion, the most frequent pose bug | 2 criteria; 390 → 395 words | Aligned | Minor | Language fix of the expected answer ("inverse pose"); explanation rewritten where garbled |
| CV-SE3-003 | Right/left plus, adjoint, $\mathrm{Ad}_R=R$, $J_L=J_GR$: confirmed (§II-E eq. 25–28, §II-F eq. 29–32, eq. 139). Missing condition revealed by the enriched reference: a library tangent can also differ by scale (Ceres 2.2.0 quaternion tangent is half the rotation vector, applied on the left) | Comparison: Jacobian and covariance conventions | 3 criteria; 402 → 445 words | "**check**" label replaced | Minor | Language fixes; one sentence on the Ceres half-angle left tangent added to the explanation, with its code source |
| CV-SE3-004 | Four binary choices and Hamilton/JPL table: confirmed (Quaternion kinematics §3.1, eq. 140–143, Table 2); Eigen constructor and storage order: confirmed on Eigen 3.4; SciPy scalar-last default: confirmed on 1.18.0. Expected answer said "known by the two strings" (toolchains) | Diagnosis: quaternion interface errors | 2 criteria; 391 → 387 words | Aligned | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-SE3-005 | Geodesic angle from the trace: confirmed (App. B-A, eq. 135); $(30°,89.9°,0°)$ versus $(0°,89.9°,-30°)$: 0.0524° recomputed; REP 103 "24 'valid' conventions": confirmed. Expected answer said "their components may differ from 2 … since unit quaternions"; explanation used decimal commas and "geodetic" | Evaluation: parameterization-independent error | 3 criteria; 381 → 390 words | Aligned | Minor | Meaning-restoring fix of the expected answer; language and decimal fixes |
| CV-SE3-006 | OpenCV pinhole model (calib3d.hpp L94–L118), REP 103 body and `_optical` axes: confirmed; `gluLookAt` not re-read. Expected answer garbled ("ROS places the body in $x$ before, $y$ left, $z$ high, and its coordinate frame `_optical` the Convention ofOpenCV", "Homogenised", "Camera→monde", "remains in each convention" without "in front") | Diagnosis: camera-axis conversion | 3 criteria; 412 → 411 words | Aligned | Important | Meaning-restoring rewrite of the expected answer; language fixes |

Expected-answer changes (meaning-restoring language fixes, old → new):

- CV-SE3-002: "the reverse pose is $(R^T,-R^Tt)$" → "the inverse pose is $(R^T,-R^Tt)$".
- CV-SE3-003: "coordinate frame sensor or coordinate frame world, and announce it" → "sensor frame or world frame, and state it".
- CV-SE3-004: "Transform a point or axis known by the two strings" → "transform a known point or axis with both toolchains".
- CV-SE3-005: "large yaw and roll gaps compensate … their components may differ from 2 for a zero error; since unit quaternions" → "large yaw and roll differences compensate each other … their components can be at Euclidean distance 2 for a zero error; for unit quaternions".
- CV-SE3-006: the whole expected answer rewritten without changing its criteria: "OpenCV places $x$ to the right, $y$ down and $z$ forward, visible points having $Z_c>0$; in OpenGL, the camera looks along $-z$ with $y$ up; ROS places the body frame with $x$ forward, $y$ left, $z$ up, and its `_optical` frame follows the OpenCV convention. Moving from OpenCV to OpenGL is a 180° rotation about $x$ … on the right of a camera→world pose … on the left of a world→camera matrix … Check that a known point in front of the camera remains in front in each convention."

## Reference findings

Claims of revision 10 checked against their passages:

- Composition and inverse (eq. 170–171), right/left perturbations (eq. 25–28),
  adjoint (eq. 29–32), $\mathrm{Ad}_R=R$ (eq. 139), trace angle (eq. 135): confirmed on
  arXiv 1812.01537v9.
- Quaternion conventions (§3.1, eq. 140–143, Table 2) and Eigen classed as Hamilton
  (§3.1.1): confirmed on arXiv 1711.02508v1.
- Eigen constructor and storage order: confirmed on the Eigen 3.4 class page (the
  5.0.1-dev page previously cited carries the same warning).
- SciPy `from_quat`: confirmed on the versioned 1.18.0 page.
- OpenCV pinhole model and `solvePnP` direction: confirmed in calib3d.hpp at 4.13.0.
- REP 103 axes, `_optical` suffix and Euler-angle warning: confirmed at commit 6fbda48.

New claims verified for revision 11: Exp and Log of $SO(3)$ and $S^3$ (eq. 132–135),
rotation action and its Jacobian (eq. 136–138, 150), $J_l=J_r^T$ (eq. 147), $SE(3)$
exponential and $V(\theta)$ (eq. 172–174), $SE(3)$ adjoint (eq. 175), covariance on the
tangent space and its adjoint transport (eq. 51–55, including the global
"horizontal-plane" covariance example), $SE(n)$ versus $T(n)\times SO(n)$ versus composite
charts (§IV); quaternion double cover and half angle in $\mathbb R^4$ (eq. 110–112) and
SLERP (eq. 124–128); Zhou et al.'s discontinuity result (abstract); and the library
contracts below.

Implementation facts added, with their differences from the paper's default
conventions (FR-036):

| Aspect | Solà et al. default | Implementation |
| --- | --- | --- |
| Perturbation side | Right (local), §II-E | Ceres 2.2.0 `QuaternionManifold`: left product $\exp(\Delta)\otimes x$ (manifold.cc L27–L60) |
| Tangent scale | Full rotation vector $\theta u$ | Ceres quaternion $\Delta$: half the rotation vector ($\exp(\Delta)=[\cos\|\Delta\|,\dots]$) |
| $SE(3)$ tangent order | $(\rho,\theta)$ | Sophus 1.22.10: $(\upsilon,\omega)$, same order; GTSAM 4.2 `Pose3`: $[\omega,v]$, rotation first, adjoint $[R\ 0;\ [t]_\times R\ R]$ |
| $SE(3)$ retraction | $\operatorname{Exp}$ with $V(\theta)$ | GTSAM 4.2: `Exp` when `GTSAM_POSE3_EXPMAP` (default `ON`), otherwise rotation retraction plus added translation |
| Quaternion storage | $(w,x,y,z)$ | Eigen $[x,y,z,w]$ in memory; SciPy scalar last by default; Ceres `QuaternionManifold` $[w,x,y,z]$ |
| Rodrigues Jacobian | Lie Jacobians $J_r$, $J_l$ | OpenCV `Rodrigues`: $3\times9$ derivative of matrix entries |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 757 → 3,975. About
700 tokens are the two tables and the pseudocode.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (two sentences) | Developed | Task; contracts of $R$, $t$, $T_{ab}$, quaternions, rotation vectors, Euler angles, tangent increments and covariances with units; outputs; pipeline role and interface requirements |
| Intuition | Shallow | Developed | Index cancellation, curved space and two perturbation sides, lever arm; worked example A (IMU–camera lever arm through the adjoint, recomputed) |
| Prerequisites | Shallow (one link) | Developed | Mathematical prerequisites; links to CV-SVD, CV-ZHANG, CV-EPIPOLAIRE, CV-FUSION, CV-FACTEURS, CV-CAPTEURS |
| Assumptions | Shallow | Developed | Right-handedness (REP 103), numerical orthonormality, first-order validity (eq. 43), Log at 0 and $\pi$, double cover, Euler singularities, same time instant, observability |
| Procedure | Shallow (one sentence) | Developed | Eight-step pseudocode with the purpose of each step and the discriminating role of each boundary test |
| Mathematics | Partly developed (composition, perturbations, adjoint) | Developed | Exp/Log (eq. 134–135), rotation-action Jacobian, $SE(3)$ adjoint and covariance transport (eq. 54–55, 175), $SE(3)$ exponential versus composite charts with worked example B, quaternions and SLERP, projection onto $SO(3)$, worked example C (angle precision) |
| Parameters | Shallow (conventions in prose) | Developed | Convention table (direction, order, algebra, side, block order, tangent scale, camera axes) with library values and tests; numerical thresholds; tuning declared not applicable with justification |
| Properties | Shallow | Developed | Group structure, bi-invariance of the geodesic angle, Jacobian identities, representation trade-offs and continuity (Zhou et al.), chart differences |
| Cost and implementation | Shallow (one sentence) | Developed | Operation counts; contracts of OpenCV 4.13.0, Eigen 3.4, SciPy 1.18.0, Ceres 2.2.0, GTSAM 4.2, Sophus 1.22.10, REP 103 and `gluLookAt`; execution status |
| Evaluation | Partly developed (executed Euler variation) | Developed | Metrics and reporting; existing variation kept and recomputed; proposed boundary-test protocol with one injected error at a time; measurement limits |
| Failure modes and diagnosis | Shallow (prose) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow (one sentence) | Developed | Six conditional choices; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/12-rotations-se3.py`](checks/12-rotations-se3.py) (14 checks): the two-camera
round trip; the 5 mm lever-arm translation and its 25 µm second-order remainder; the
$SE(3)$ exponential translation $(2/\pi,2/\pi,0)$ m and its 0.900 m chord; the 0.0524°
geodesic angle of the Euler example; the double cover and $2\arccos|\langle q_1,q_2\rangle|$;
the quarter-turn quaternion; the trace formula returning 0 at $10^{-8}$ rad and drifting by
more than $10^{-5}$ relative at $10^{-6}$ rad; the Ceres half-angle left tangent; the
OpenCV-to-OpenGL matrix.

## Applied corrections

- [Reference](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md),
  revision 10 → 11: body rewritten and deepened as above; mistranslations fixed in the
  body and in all three appendices ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Documentary reference" → "Source consulted",
  "disturbances" → "perturbations", "deputy" → "adjoint", "Annex" → "Appendix", "Its
  reverse" → "Its inverse", "the two poses on the front" → "of the question",
  "Worldwide, the radius" → "In world coordinates, the ray", "**check of
  representation**" → "**Representation check**", "unitary … in convention announced …
  main angle" → "unit … in a stated convention … principal angle", "processes double
  coverage" → "handles the double cover", "kernel example" → "core example"); sources
  split into scientific and implementation sources; closing provenance line replaced.
  Front matter unchanged except `revision`; H1 and the six `### CV-SE3-00N` headings kept.
- [Cards](../../../vault/10-mathematiques-estimation/12-rotations-se3.md): the
  expected-answer fixes above; CV-SE3-003 explanation completed with the Ceres
  half-angle left tangent and its Source line with `manifold.cc`; language fixes in the
  explanations and blocking errors of all six cards ("**check**" → "**Discriminating
  check**", "derivation step by step" → "Step-by-step derivation", "Example
  interpreted" → "Worked example", "disruption" → "perturbation", decimal commas,
  "geodetic" → "geodesic", "Block the arccos argument" → "Clamp"); Source lines "see
  the" / "consult the" → "consulted", "Annex B-C" → "Appendix B-C". Questions, IDs,
  objectives, families, tags and target deck unchanged.

No other vault card repeats a claim corrected here (`rg` over `vault/` for quaternion
order, Euler angles and `gluLookAt`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). P-CV-SE3-01 (adjoint covariance transport) remains pending and is
not duplicated; the reference now develops its material in Mathematics and worked
example A.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SE3-02 | CV-SE3 | Explain why the same 6-vector increment yields different poses under the $SE(3)$ exponential, $T(3)\times SO(3)$ and a composite $\langle\mathbb R^3,SO(3)\rangle$ chart, and which of them change Jacobians at first order | No card trains the $SE(3)$ exponential ($V(\theta)\rho\neq$ translation) or chart differences between libraries (GTSAM `GTSAM_POSE3_EXPMAP`, Ceres product manifolds) | Reasoning; Mathematics, worked example B | 1 card, 3 criteria (screw versus chained motion; same Jacobian at $\tau=0$ for the first two; global translation increment for the composite) | [Solà et al., §IV and App. D-B, eq. 172–174](https://arxiv.org/html/1812.01537v9); [GTSAM 4.2 Pose3.cpp L211–L223](https://github.com/borglab/gtsam/blob/4.2/gtsam/geometry/Pose3.cpp) |

## Sources

Scientific sources, opened at the passages listed:

- Solà, Deray and Atchuthan, [arXiv HTML v9](https://arxiv.org/html/1812.01537v9):
  §II-E, §II-F (with the $SE(3)$ adjoint example), §II-G (eq. 41–43 and the rotation
  example), §II-H, §II-I, §IV (first example), App. B (eq. 131–151), App. D
  (eq. 168–183).
- Solà, Quaternion kinematics, [arXiv HTML v1](https://arxiv.org/html/1711.02508v1):
  §2.4.6, §2.7, §3.1 with Table 2, §3.1.1.
- Zhou et al. 2019, [arXiv abstract page](https://arxiv.org/abs/1812.07035): abstract.

Implementation sources:

- OpenCV 4.13.0 `modules/calib3d/include/opencv2/calib3d.hpp`: L94–L120, L681–L707,
  L1029–L1034.
- Eigen 3.4 `Quaternion` class documentation; Eigen 3.4.0 `Eigen/src/Geometry/Umeyama.h`
  L125–L150.
- SciPy 1.18.0 `Rotation.from_quat` and `Rotation.as_quat` pages.
- Ceres Solver 2.2.0 `docs/source/nnls_modeling.rst` L1567–L1645 and
  `internal/ceres/manifold.cc` L27–L60, L268–L280.
- GTSAM 4.2 `gtsam/geometry/Pose3.h` L136–L236, `Pose3.cpp` L57–L76 and L211–L235,
  `cmake/HandleGeneralOptions.cmake` L19–L42.
- Sophus 1.22.10 `sophus/se3.hpp` L237–L254, `sophus/so3.hpp` L282,
  `sophus/common.hpp` L157.
- REP 103 at commit 6fbda48: Axis Orientation, Suffix Frames, Rotation Representation.

Failed accesses and limits:

- The Khronos `gluLookAt` page was not re-read; its claim is retained from the
  2026-10-23 pass, which quoted it.
- Barfoot's "State Estimation for Robotics" was not consulted; the $SE(3)$ Jacobians are
  taken from Solà et al., who cite Barfoot for eq. 179–180.
- Context7 was not available in this session (see the scope record); versioned official
  documentation and code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/12-rotations-se3.py` | 14 checks passed |
| `git diff --check -- vault/10-mathematiques-estimation/ <check scripts>` | No whitespace error |
| `inventaire_cartes.py vault/10-mathematiques-estimation/12-rotations-se3.md` | 6 cards, 387 to 445 words, no anomaly; absent families: understanding, algorithm, design |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 10` → `11`; six `### CV-SE3-00N` headings unchanged; `$$` and code fences balanced |

No library call or pose computation outside the check script was executed. Tables,
multi-line display equations and the pseudocode were not rendered in Obsidian, and
AnkiDroid rendering of the corrected cards is unverified. This is agent self-review,
without independent scientific validation or measurement of learner proficiency.
Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-SE3 revision 11; meaning-restoring expected-answer fixes of CV-SE3-002 to 006;
CV-SE3-003 explanation completed with the Ceres half-angle left tangent; Agent Claude
Code self-review; to republish with `paquet-anki`) and the proposal register
(P-CV-SE3-02).
