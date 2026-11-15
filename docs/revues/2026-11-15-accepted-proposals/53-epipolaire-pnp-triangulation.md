# Review — Epipolar geometry, PnP and triangulation — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-EPIPOLAIRE-01. One card added,
CV-EPIPOLAIRE-006; the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/53-epipolaire-pnp-triangulation.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-006 | $E=[t]_\times R$, constraint $[p_2;1]^\top K^{-\top}EK^{-1}[p_1;1]=0$, unit-length $t$ and cheirality: calib3d.hpp L2632–L2641, L2753–L2771, L2808–L2810. Homography decomposition with up to four solutions, two removable by positive depth: calib3d.hpp L3444–L3488. Model selection (parallel $H$ and $F$ on the same samples, $T_H=5.99$, $T_F=3.84$, $R_H>0.45$, triangulation of every hypothesis, no initialization without a clear winner) and the planar twofold ambiguity: Mur-Artal et al. 2015, §II-B and §IV steps 2–4, eqs. 1–3. $E=0$ under pure rotation, the family $[e]_\times H$, rank 6 instead of 8, the second exact essential matrix and the degrees of freedom of the thresholds: project derivations recomputed by the check script | Diagnosis: a silent initialization failure. RANSAC keeps most matches and `recoverPose` returns a unit $t$ whether or not the data constrain it | 3 expected criteria (pair A: $E=0$ and arbitrary $t$; both pairs: one point-to-point map and rank 6; homography-first model selection and the action per pair); 568 lexical words | Notation $X_2=RX_1+t$, plane $n^\top X_1=d$ and $H\sim K(R+tn^\top/d)K^{-1}$ as in the reference and CV-HOMOGRAPHIE | Diagnosis |

The card tests a different objective from CV-EPIPOLAIRE-004 (depth conditioning of a
triangulated point at low parallax): here, the degeneracy of $E$ and of the eight-point
system, and the model test that must precede relative pose. The question describes the two
captures without naming the homography or the degeneracy.

## Reference findings

- Worked example D ended with "A homography, or the essential matrix with known
  intrinsics, is the appropriate model for such data". This is imprecise: the five-point
  solver can return $E$ for a planar scene, but the linear eight-point estimate of $E$ on
  normalized coordinates has the same rank 6 as the one for $F$ (recomputed), and the plane
  admits a second exact essential matrix (ORB-SLAM §II-B; recomputed). The sentence now
  says so and points to worked example F.
- The pure-rotation and planar-scene assumptions said what vanishes but not why a solver
  still returns a confident answer. They now state that every $[e]_\times R$ fits pure
  rotation data, that the rotation stays observable through $K^{-1}HK=R$, and that planar
  data admit a twofold ambiguity.
- The reference had no source for model selection. Worked example F adds the ORB-SLAM
  procedure, with its thresholds and selection ratio, and the argument that inlier counts
  cannot reveal the degeneracy.

## Applied corrections

- `vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md`: CV-EPIPOLAIRE-006
  appended.
- `vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md`, revision
  8 → 9: pure-rotation and planar-scene assumptions extended; worked example D corrected;
  worked example F added; ORB-SLAM added to the scientific sources and the inaccessible
  sources updated (Torr's model-selection papers); `decomposeHomographyMat` lines added to
  the implementation sources; the card listed under related flashcards; closing provenance
  line extended.

## Proposals

P-CV-EPIPOLAIRE-01: accepted by the learner on 2026-11-15, completed as CV-EPIPOLAIRE-006.

## Sources

Scientific source:

- Mur-Artal, Montiel and Tardós 2015, "ORB-SLAM: a Versatile and Accurate Monocular SLAM
  System", [arXiv 1502.00956v2](https://arxiv.org/abs/1502.00956) (PDF, text extracted with
  `pdftotext`): §II-B (map initialization, planar twofold ambiguity, model selection) and
  §IV steps 1–5, eqs. 1–4.

Implementation source, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns HTTP 403
from this environment; Context7 is unavailable in this session):

- `modules/calib3d/include/opencv2/calib3d.hpp` L2600–L2830 (`findEssentialMat`,
  `decomposeEssentialMat`, `recoverPose`) and L3444–L3495 (`decomposeHomographyMat`,
  `filterHomographyDecompByVisibleRefpoints`).

Failed accesses:

- Torr, Fitzgibbon and Zisserman 1999 (degeneracy) and Torr 2002 (GRIC): web searches found
  bibliographic records only; a core.ac.uk candidate returned HTTP 403. GRIC is mentioned
  only as cited by ORB-SLAM.
- Hartley and Zisserman and Nistér's five-point paper: not retried; still not verifiable.

## Checks and limitations

`python3 -I checks/53-epipolaire-pnp-triangulation.py` passes its 10 checks: $E=0$ and
$p_2\sim KRK^{-1}p_1$ for pair A, with the $10^\circ$ rotation recovered; every $[e]_\times R$
fitting pair A; rank 6 for pair A; singular values $0.2,0.2,0$ of $E$ for pair B;
$[t]_\times H_n=[t]_\times R$; every $[e]_\times H$ fitting the floor, rank 6 on the floor
(pixels and normalized coordinates) against rank 8 for a non-planar scene; a second valid
essential matrix fitting every floor match, rejected here by cheirality; the $\chi^2$
quantiles 5.99 and 3.84. Points are noise-free and constructed; no OpenCV call or image was
processed, so the premise that RANSAC keeps most matches is a scenario, not a measurement.
AnkiDroid rendering of the card is not verified.
