# Review — Epipolar geometry, PnP and triangulation — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for the three calibrated-camera problems: relative pose,
absolute pose and triangulation. It now opens with a comparison table, states the data
contract of each OpenCV 4.13 entry point, derives the constraints and ambiguities, and
quantifies them in five worked examples. Robust estimation and the planar case stay in
CV-HOMOGRAPHIE; joint refinement in CV-BA; dense stereo in CV-STEREO.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-001 | $E$ on normalized coordinates, $F=K_2^{-\top}EK_1^{-1}$ on pixels: confirmed (calib3d.hpp L2731–L2738 writes $[p_2;1]^\top K^{-\top}EK^{-1}[p_1;1]=0$) and recomputed (checks 1–3). "Removes the arbitrary scale from the right" mistranslated *de la droite* (the line); "dots", "re-inject them into a fundamental", "the corresponding places", "the only product" | Reasoning: coordinate contract of $E$ and $F$ | 1 expected criterion with two parts; 354 → 353 lexical words | Aligned with the reference appendix | Minor | Language fixes; Source line given header lines |
| CV-EPIPOLAIRE-002 | Monocular two-view pose gives the translation direction only: confirmed ("one can only get the direction of the translation", `t` "returned with unit length", L2761–L2769) and recomputed (check 4, scale 7). "This selects a meaning" mistranslated *sens* (the direction); "pose and cheirality", "allowable essential", "meter" | Understanding: scale of the translation | 1 expected criterion; 368 → 368 lexical words | Aligned with the appendix | Minor | Language fixes; Source line given header lines |
| CV-EPIPOLAIRE-003 | PnP estimates pose from 3-D–2-D, triangulation estimates points from known views: confirmed (solvePnP "brings points from the model coordinate system to the camera coordinate system", L1000–L1076; triangulatePoints, L2986–L3012); DLT rows recomputed (check 11). "Write Linear Triangulation", "Locate a camera", "digital solution", "SfM string", "Reverse entries and unknowns" | Comparison: which unknown each problem solves | 2 expected criteria; 363 → 364 lexical words | Aligned with the appendix | Minor | Language fixes; Source line given header lines and EPnP |
| CV-EPIPOLAIRE-004 | Low parallax gives small residuals but uncertain depth; $\sigma_Z\approx fB\sigma_d/d^2$: recomputed (checks 9–10: 0.025 m at 2 m, 0.625 m at 10 m). "Why reverse depth helps", "posing", "angle between radii", "Protocol built", "occlusionss", "reference 3D", "direction of parameters with little stress" | Diagnosis: conditioning of depth | 1 expected criterion; 357 → 361 lexical words | Aligned with the reference worked example C | Minor | Language fixes; Source line given header lines and the worked example |
| CV-EPIPOLAIRE-005 | `solvePnP` with P3P/AP3P needs exactly 4 points; `solveP3P` takes 3 and returns up to 4 solutions sorted by reprojection error: confirmed (L1057–L1059, L1140–L1172). Expected answer "degenerated", "request"; "return multiple assumptions" (*hypotheses*); "Proposed Protocol", "poses candidates", "reserved points" | Practice: minimal problem versus API contract | 3 expected criteria; 351 → 356 lexical words | Aligned with the appendix | Minor | Expected-answer wording fixed; language fixes; Source line given header lines |

Expected-answer change (meaning-restoring language fix):

- CV-EPIPOLAIRE-005: "configurations may be degenerated, and the selected API may request a
  fourth point" → "configurations may be degenerate, and the selected API may require a
  fourth point".

## Reference findings

Claims of revision 7 checked:

- $E=[t]_\times R$ for $X_2=RX_1+t$, $x_2^\top Ex_1=0$, $F=K_2^{-\top}EK_1^{-1}$: confirmed
  (derivation, check 1–2, header L2731–L2738).
- No metric scale from two monocular views; PnP returns $t$ in the unit of the 3-D points;
  camera centre $-R^\top t$: confirmed (L2761–L2769; check 4 and check 8).
- `solvePnP(..., SOLVEPNP_P3P)` needs four points, `solveP3P` three: confirmed (L1057–L1059,
  L1140–L1172).
- "`solvePnP` conventions have been verified in the 4.13 documentation": the documentation
  page is now blocked (403); re-verified in the 4.13.0 header.
- No scientific error in revision 7; sections held one to three sentences. Language defects:
  "dots", "the 2 image", "from the right" for *of the line*, "meaning" for *direction*,
  "pose reversed", "Question of work", "Reference Response", "Documentary reference".

New claims verified for revision 8 (main ones), in OpenCV 4.13.0 calib3d.hpp:

- `findEssentialMat`: five-point solver of Nistér, defaults RANSAC, 0.999, 1.0 px,
  1000 iterations, threshold as a point-to-epipolar-line distance in pixels "1-3"
  (L2608–L2750).
- `decomposeEssentialMat`: four candidates, unit translation (L2753–L2771); `recoverPose`:
  cheirality "triangulated 3D points should have positive depth", `distanceThresh` filters
  far points (L2773–L2960).
- `findFundamentalMat`: 7-point $N=7$, 8-point and robust methods $N\ge8$ (L2540–L2605),
  while the `FM_RANSAC` enum comment says "at least 15 points" (L637): an inconsistency
  inside the header, recorded in the note.
- `solvePnP` methods and point requirements, broken DLS/UPnP falling back to EPnP, SQPnP
  with at least 3 points, P3P after Ding et al. 2023; `solvePnPRansac` defaults (100
  iterations, 8.0 px, 0.99); "User code is responsible for solution quality assessment"
  (L563–L585, L1000–L1172).
- `triangulatePoints`: float input, homogeneous $4\times N$ output, rectified frame when the
  matrices come from `stereoRectify` (L2986–L3012).
- EPnP abstract and §1: four virtual control points, $12\times12$ eigen-problem, $O(n)$,
  $n\ge4$, planar and non-planar, Gauss–Newton refinement.

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 328 → 3,440.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Comparison table of the four problems; common model; data contract of each OpenCV entry point (inputs, outputs, frames, units); pipeline roles |
| Intuition | Shallow | Developed | One mechanism per problem; constructed robot illustration of scale; Mermaid diagram of a two-view initialization and localization |
| Prerequisites | Shallow (two links) | Developed | Links to CV-SVD, CV-HOMOGRAPHIE, CV-MATCHING, CV-MATCH-APPRIS, CV-BA, CV-STEREO, CV-VIO |
| Assumptions | Shallow | Developed | Calibration, static scene, scale (five degrees of freedom), pure rotation, planar scene, PnP configurations, parallax, cheirality |
| Procedure | Shallow | Developed | Pseudocode from essential matrix to PnP and scale setting, with the purpose of each step |
| Mathematics | Shallow (one formula) | Developed | Derivation of the constraint; rank and degrees of freedom; point-to-line distance; four decompositions; PnP objective, P3P and EPnP; DLT triangulation; depth uncertainty; worked examples A–E |
| Parameters | Shallow | Developed | Parameter table with 4.13 defaults and point requirements; four-step tuning approach |
| Properties | Shallow | Developed | Structural ambiguities; OpenCV's quality disclaimer; EPnP properties; algebraic triangulation; directions and units |
| Cost and implementation | One sentence | Developed | Cost drivers; OpenCV contracts with line numbers; illustrative pipeline snippet |
| Evaluation | Shallow | Developed | Metrics per problem; baseline and baseline-length variation with a matching confound; limits |
| Failure modes and diagnosis | Two sentences | Developed | Seven-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Two sentences | Developed | Homography, PnP, two-view, stereo, VIO, bundle adjustment; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/53-epipolaire-pnp-triangulation.py`](checks/53-epipolaire-pnp-triangulation.py)
(12 checks): epipolar constraint on normalized coordinates and on pixels with two
different cameras; scale-invariance of the point-to-line distance; projections unchanged
under a factor 7 on scene and baseline; the twisted pair and the single cheirality-valid
candidate; $E=0$ under pure rotation; $C=-R^\top t$; disparities, parallax angles and depth
uncertainties at 2 m and 10 m; DLT triangulation; rank 8 versus rank 6 of the eight-point
system for general versus coplanar points.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md),
  revision 7 → 8: body rewritten and deepened as above. Appendix language fixes, applied
  identically to the card text: "These constructed cases develop epipolarity, pose and
  depth distinguished by their contract" → "…epipolar geometry, pose and depth,
  distinguished by their contracts", "Question of work" → "Working question", "Reference
  Response" → "Reference answer", "homogeneous symbol … standardization convention" →
  "homogeneous notation … normalization convention", "Example of check" → "Example of a
  check", "dots" → "points", "Difference Between Problem and Function" → "Difference between
  problem and function", "multiple assumptions" → "several hypotheses", "Proposed Protocol"
  → "Proposed protocol", "poses candidates" → "candidate poses", "reserved points" →
  "held-out points", "Constraint at a distance" → "From constraint to distance", "in the 2
  image" → "in image 2", "from the right" → "of the line", "the only product" → "the bare
  product", "responds to other approximations" → "relies on other approximations", "the
  corresponding places" → "the loci of correspondences", "pose and cheirality" → "Pose and
  cheirality", "allowable essential" → "admissible essential matrix", "selects a meaning" →
  "selects a direction", "Write Linear Triangulation" → "Writing linear triangulation", "Why
  reverse depth helps … posing" → "Why inverse depth helps … setting", "unit sighting
  directions" → "unit viewing directions". Sources split into scientific and
  implementation; closing provenance line replaced. Front matter unchanged except
  `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md): the
  expected answer of -005 as quoted above; further explanations and blocking errors
  corrected as in the appendix, plus "use the correct matrices and direction of pose
  announced" → "use the matching matrices and the stated pose direction", "Locate a camera …
  Rebuilding the corner … digital solution" → "Locating a camera … Reconstructing the corner
  … numerical solution", "SfM string" → "SfM pipeline", "reference 3D" → "a 3-D reference",
  "direction of parameters with little stress" → "weakly constrained parameter direction",
  "Protocol built … angle between radii" → "Constructed protocol … angle between rays",
  "occlusionss" → "occlusions", blocking errors put in gerund form. All five Source lines
  now cite the 4.13.0 header at line level (and EPnP for -003) instead of the blocked
  documentation pages and the unverifiable "verified contract with Context7" label.
  Questions, IDs, objectives, families, tags and target deck unchanged.

`rg` over `vault/` finds the P3P and essential-matrix statements only in this subject, the
progress log and consistent statements in CV-HOMOGRAPHIE and CV-SVD.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (shared file, not
edited here). P-CV-EPIPOLAIRE-01 carries forward the 2026-10-20 proposal "Degeneration in
pure rotation", which was never registered.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-EPIPOLAIRE-01 | CV-EPIPOLAIRE | Diagnose a two-view initialization on a pure rotation or a planar scene: what happens to $E$ and to the eight-point system, and why a homography model should be tested first | Model selection before relative pose; degeneracies are only mentioned in explanations | Diagnosis; Assumptions, worked examples B and D | 1 card, 3 criteria | [OpenCV 4.13.0 calib3d.hpp L2753–L2810](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); derivation recomputed in the check script |
| P-CV-EPIPOLAIRE-02 | CV-EPIPOLAIRE | Choose a stereo baseline (or focal length) from a required depth tolerance at a given range, using $\sigma_Z\approx Z^2\sigma_d/(fB)$, and name the matching cost of a wider baseline | No card trains the design decision that the depth-uncertainty relation supports | Design; Mathematics, worked example C | 1 card, 3 criteria | Derivation of the note (worked example C); [CV-STEREO](../../../vault/60-vision-3d/references/61-stereo-profondeur.md) for rectified stereo |

No defective question was found.

## Sources

Scientific sources:

- Lepetit, Moreno-Noguer and Fua 2009, EPnP, [EPFL Infoscience PDF](https://infoscience.epfl.ch/record/160138/files/top.pdf)
  (text extracted with `pdftotext`): abstract and §1.
- **Not verifiable** in this pass: Nistér's five-point paper (TPAMI 2004; Semantic Scholar
  record without abstract or open PDF) and Hartley and Zisserman's textbook. The note cites
  Nistér only through OpenCV's documentation and states the epipolar, decomposition,
  degeneracy and triangulation results as derivations recomputed in the check script.

Implementation sources (official code at tag 4.13.0):

- [`modules/calib3d/include/opencv2/calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp):
  L563–L585, L632–L637, L1000–L1172, L2540–L2605, L2608–L2771, L2773–L2960, L2975–L3012.

Failed accesses and limits:

- docs.opencv.org returned HTTP 403; the documentation links kept in the 2026-10-30 and
  2026-11-08 appendices were not re-read.
- OpenCV source files (`five-point.cpp`, `solvepnp.cpp`, `triangulate.cpp`) were not read;
  implementation claims rest on the header documentation.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/53-epipolaire-pnp-triangulation.py` | 12 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md` | 5 cards, 353–368 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 41 protected card lines identical; front matter identical except `revision: 7` → `8`; H1 and 10 per-card headings unchanged; `$`, `$$` and fences balanced |

No OpenCV call or image experiment was executed; the snippet is illustrative and the
proposed baseline is a protocol, not a result. Mermaid and tables were not rendered in
Obsidian; AnkiDroid rendering is unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-EPIPOLAIRE
revision 8, CV-EPIPOLAIRE-001 to -005, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-EPIPOLAIRE-01, P-CV-EPIPOLAIRE-02).
