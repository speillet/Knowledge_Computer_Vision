# Review — 3D detection, object pose and articulated pose — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 7 to revision 8. Highest severity per card before correction: 0 blocking,
1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

Revision 7 had a body of 305 words with one to three sentences per contract section.
This is a comparison note: the deepened body contrasts 3D box detection
(CenterPoint, nuScenes protocol), model-based 6-DoF pose (PnP, BOP errors) and
articulated pose (OpenPose, HRNet, OKS, Human3.6M protocols). Point-cloud encoders
stay in [CV-BEV](../../../vault/60-vision-3d/references/64-nuages-bev-occupation.md)
and PnP solvers in
[CV-EPIPOLAIRE](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md),
linked rather than restated. Unclear translations were resolved against the
pre-migration French text (`git show b7142bb^:vault/80-detection-pose/84-detection-pose-3d.md`).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Boxes, rigid poses and skeletons have different unknowns and metrics: confirmed (CenterPoint §3; BOP 2020 §2.1; COCO keypoint evaluation; Martinez et al. §4 for root and rigid alignment). "A AP of boxes, it, depends", "comparing two digits", "the coordinate frame sensor" | Comparison: choose a metric from the consumer | 1 criterion; 365 → 369 words | Aligned with the reference appendix | Minor | Language fixes; Martinez et al. added to the source line |
| CV-POSE3D-002 | Convention checks (frame, anchor, size order, yaw axis and sign, unit): confirmed and sharpened by the nuScenes results format (size as width, length, height; global frame). Blocking error "Retract without check the box convention" meant *retraining* without checking it (French: "Réentraîner sans contrôler"); "make a box turn a quarter turn" meant *look* rotated | Practice: convention round trip | 1 list criterion; 381 → 383 words | Aligned with the appendix | Important (garbled grading criterion) | Blocking error restored; language fixes; pinned nuScenes source added |
| CV-POSE3D-003 | nuScenes matches by 2D center distance on the ground plane (0.5–4 m) and reports TP errors and NDS; COCO matches by IoU: confirmed (nuScenes README at b40adc4). Expected answer said "ground center distances" | Evaluation: benchmark-specific matching | 2 criteria; 351 → 360 words | Aligned with the appendix | Minor | Meaning-preserving clarification of the expected answer; language fixes |
| CV-POSE3D-004 | Rotation about a symmetry axis can be unobservable; texture can break the symmetry: confirmed (BOP 2020 §2.3 keeps only symmetries "that cannot be resolved by the model texture"; §2.2 MSSD/MSPD/VSD). "a more accurate solver does not create a visible absent coordinate frame" (an absent visible landmark), "slice a symmetrical degree of freedom" | Diagnosis: symmetric degree of freedom | 1 criterion; 289 → 284 words | Aligned with the appendix | Minor | Language fixes; BOP 2020 §2.3 added to the source line |

Expected-answer change (CV-POSE3D-003, meaning-preserving clarification): "The
nuScenes association uses ground center distances and a specific protocol; COCO bbox
uses overlaps and its own rules." → "nuScenes matching uses 2D center distances on the
ground plane and a specific protocol; COCO bbox matching uses overlaps (IoU) and its
own rules."

Blocking-error change (CV-POSE3D-002, meaning-restoring): "Retract without check the
box convention." → "Retraining without checking the box convention."

## Reference findings

Claims of revision 7 checked: PointPillars encodes pillars as a pseudo-image and
CenterPoint predicts centers and attributes (confirmed, CenterPoint §3–§4; pillar
details belong to CV-BEV); symmetric objects make several rotations equivalent
(confirmed, BOP 2020 §2.2–§2.3); "The AP nuScenes is not just the AP COCO with a IoU
3D" (confirmed: center-distance matching, nuScenes README). No scientific error was
found. The proposed variation "rarefy points with distance, then hide joints
separately" varied two factors; the new protocol keeps one controlled variation (point
density) and moves joint occlusion to a separate experiment.

New claims verified for revision 8 (main ones): CenterPoint box parameterization,
heatmap radius, regression heads with $(\sin\alpha,\cos\alpha)$ and log size, velocity
tracking with 3-frame track memory, IoU-guided score and geometric-mean fusion,
nuScenes ranges and grids, second-stage sampling, 58.0 mAP / 65.5 NDS and 16 frames/s;
nuScenes results format, 0.5 s past-data rule, class ranges, preprocessing, AP and TP
definitions, NDS; BOP pose direction, localization versus detection, VSD/MSSD/MSPD,
symmetry identification with $\max(15\text{ mm},0.1d)$, AR thresholds, App. A
remarks on ADD/ADI and on grasping versus augmented reality; PoseCNN ADD and ADD-S at
10% of the diameter; OpenPose confidence maps, PAF line integral, per-limb Hungarian
matching, runtime invariance to the number of people; HRNet Gaussian targets,
$256\times192$ / $384\times288$ crops, flip averaging, quarter offset, 73.4 AP;
COCO keypoint format, OKS and $\sigma_i$ values; Human3.6M protocols #1 and #2.

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 305 → 4,207, of which about 900 are table cells
and 150 pseudocode and Mermaid lines.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Comparison table of the three outputs; nuScenes, BOP, OpenCV and COCO data contracts with frames, units and size order; pipeline roles |
| Intuition | Shallow | Developed | Center-based 3D detection, PnP with symmetry sets, bottom-up versus top-down keypoints; constructed warehouse illustration; Mermaid diagram |
| Prerequisites | Developed (three links) | Developed | CV-DETECTEURS, CV-IOU-AP, CV-MULTICALIB and CV-ICP links; target competencies |
| Assumptions | Absent | Developed | Calibration and timing, gravity-aligned cuboids, range-dependent density, model and texture, PnP minimum points, skeleton and visibility; observability and degenerate cases |
| Procedure | Shallow | Developed | Pseudocode for the three pipelines with the purpose of each step |
| Mathematics | Shallow | Developed | Box corners; CenterPoint score target; nuScenes AP, TP errors and NDS; MSSD, MSPD, VSD, ADD, ADD-S; OpenPose maps and line integral; OKS; MPJPE protocols; worked examples A (size order), B (OKS), C (cylinder ADD versus MSSD), D (alignment) |
| Parameters | Shallow (list) | Developed | Seven-row table with source values; tuning approach |
| Properties | Absent | Developed | Orientation-agnostic assignment, what each metric guarantees, PnP limits, runtime scaling, published results with protocol |
| Cost and implementation | Shallow | Developed | Cost drivers; OpenCV 4.13 `solvePnP` and `solvePnPRansac` contracts with line numbers; execution status |
| Evaluation | Shallow | Developed | Five-protocol table; one controlled variation (point density) with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/84-detection-pose-3d.py`](checks/84-detection-pose-3d.py) (10 assertions):
aligned 3D IoU 1/3 and ASE 2/3 for a size-order swap, identical footprint after a 90°
yaw compensation with AOE $\pi/2$; OKS values 0.135, 0.722, 0.897 at $s=100$ px and
0.0003, 0.646 at $s=50$ px; cylinder ADD 15.31 mm against 10.77 mm, MSSD 0 with the
axial symmetry and 15.31 mm without, 8 of 10 BOP thresholds passed; root-aligned error
30 mm, rigid-aligned 29.5 mm.

## Applied corrections

- [Reference](../../../vault/80-detection-pose/references/84-detection-pose-3d.md),
  revision 7 → 8: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Documentary reference" → "Source consulted",
  "Difference of unknowns" → "Different unknowns", "Intuition of Identifiable" →
  "Identifiability intuition", "Define the comparative quantity" → "Define the compared
  quantity", "Counter-example of geometry" → "Geometric counter-example"); sources
  split; closing provenance line replaced. Front matter unchanged except `revision`; H1
  and per-card headings unchanged.
- [Cards](../../../vault/80-detection-pose/84-detection-pose-3d.md): the two changes
  quoted above and 20 further exact replacements in explanations, blocking errors and
  Source lines. Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-POSE3D-01 | CV-POSE3D | Compute the keypoint similarity of a fixed pixel error for different keypoint types and person scales, and explain why OKS replaces a pixel tolerance | No card covers the articulated-pose metric, one of the three outputs this note compares | Reasoning; worked example B | 1 card, 3 criteria | [COCO keypoint evaluation](https://cocodataset.org/#keypoints-eval); [HRNet §4.1](https://arxiv.org/html/1902.09212v1) |
| P-CV-POSE3D-02 | CV-POSE3D | Describe how a center-based 3D detector turns a BEV heatmap peak into a box (offset, height, log size, $(\sin,\cos)$ yaw, velocity) and why it avoids orientation-specific anchors | The algorithm family is absent; the 3D detection mechanism is untested | Algorithm; Procedure | 1 card, 3–4 criteria | [CenterPoint §3–§4](https://arxiv.org/html/2006.11275v2) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed (arXiv HTML converted to text):

- Yin et al., CenterPoint, [arXiv HTML v2](https://arxiv.org/html/2006.11275v2): §1,
  §3, §4, §4.1, §4.2, §5.
- Hodaň et al., BOP Challenge 2020, [arXiv HTML v2](https://arxiv.org/html/2009.07378v2):
  §2.1–§2.4, App. A.
- [BOP tasks page](https://bop.felk.cvut.cz/tasks/): 6D localization and 6D detection
  of seen objects (read on 2026-11-14).
- Xiang et al., PoseCNN, [arXiv HTML v3](https://arxiv.org/html/1711.00199v3): §I,
  §III-D (losses), §V-B.
- Cao et al., OpenPose, [arXiv HTML v2](https://arxiv.org/html/1812.08008v2): §I,
  §III-C, §III-D, §III-E, §V-C.
- Sun et al., HRNet, [arXiv HTML v1](https://arxiv.org/html/1902.09212v1): §3, §4.1.
- Martinez et al., [arXiv HTML v2](https://arxiv.org/html/1705.03098v2): §4 and
  Tables 2–3 captions.
- COCO keypoint evaluation, read from `https://cocodataset.org/dataset/keypoints-eval.htm`
  (the page behind `#keypoints-eval`).

Implementation sources (read as raw files):

- nuScenes devkit at commit `b40adc4` (master on 2026-11-14):
  `python-sdk/nuscenes/eval/detection/README.md` and
  `configs/detection_cvpr_2019.json`. The newest tag returned by the GitHub API was
  v1.1.2, older than the current README, so the commit is cited instead.
- OpenCV 4.13.0 `modules/calib3d/include/opencv2/calib3d.hpp`: L563–L586,
  L1010–L1077, L1118–L1128.

Failed accesses and limits:

- docs.opencv.org was not used (HTTP 403 in this pass, per the brief); Context7 was
  not available.
- Downloaded but not used for claims: the nuScenes paper (arXiv 1903.11027) and the
  BOP 2018 paper (arXiv 1808.08319); the devkit README is the normative source for the
  metric.
- PointPillars was not re-read: its mechanism is developed and sourced in CV-BEV.
- Human3.6M's original paper was not opened; the protocols are cited as described by
  Martinez et al.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | FAIL only on `130-evaluation-fiabilite/references/134-metriques-applications.md` ("missing local link or outside vault: $$"), a file of another subject edited in parallel; no error in this subject's files (the run before that edit returned OK) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/84-detection-pose-3d.py` | 10 checks passed |
| `git diff --check -- vault/80-detection-pose/ docs/revues/2026-11-14-reference-depth/checks/84-detection-pose-3d.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/80-detection-pose/84-detection-pose-3d.md` | 4 cards, 284 to 383 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$`, inline `$` and fences balanced; every appendix paragraph identical to its card paragraph; local links resolve |

No detector, PnP solver or keypoint model was run; the controlled variation is a
protocol, not a result. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering is unverified. This is agent self-review, without independent
scientific validation or measurement of learner proficiency. Export status: **to
republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-POSE3D revision 8, CV-POSE3D-002 blocking-error fix, CV-POSE3D-003 expected-answer
clarification and language fixes in all four cards, Agent Claude Code self-review, to
republish with `paquet-anki`) and the proposal register (P-CV-POSE3D-01,
P-CV-POSE3D-02).
