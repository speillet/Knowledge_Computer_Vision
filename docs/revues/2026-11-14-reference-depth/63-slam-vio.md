# Review — SLAM, VIO, IMU preintegration and loop closure — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for visual-inertial odometry and SLAM. Filtering
and factor-graph machinery stay in
[CV-FUSION](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md)
and [CV-FACTEURS](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md),
reprojection and bundle adjustment in
[CV-EPIPOLAIRE](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md)
and [CV-BA](../../../vault/50-calibration-geometrie/references/54-bundle-adjustment.md);
the note links to them. The anchors `#cv-vio-004` and `#cv-vio-005` of the card file,
targeted by `vault/01-Parcours/Poles-metiers.md`, are unchanged.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Increments $\Delta v_{ij}$, $\Delta p_{ij}$: confirmed (Forster et al. §VI eq. 33); specific-force model confirmed (§V eqs. 27–28); first-order bias update and re-propagation for large changes confirmed (Forster §VI-C eq. 44; VINS-Mono §IV-B). "Avoids naïvely resuming the entire raw sequence at each calculation" was imprecise: preintegration avoids re-integration when the starting state's linearization point changes (Forster §VI) | Understanding: what preintegration summarizes and what a VIO still needs | 2 expected criteria; 350 → 360 lexical words | Wording aligned with the reference appendices | Minor | Expected-answer language fix; imprecise sentence corrected with source; language fixes; Source line given exact equations |
| CV-VIO-002 | Loop closure adds a constraint and redistributes drift: confirmed in VINS-Mono §VII–§VIII (4-DOF loop constraints, pose graph) and ORB-SLAM3 §VI-A (geometric verification after DBoW2). Source line cited VINS-Mono §IV-B and §V-B, which concern preintegration and initialization: unsupported citation | Comparison: odometry versus loop-corrected SLAM contracts | 2 expected criteria; 372 → 374 | "False stress", "reserved reference", "sending" mistranslated | Minor | Language fixes; Source line replaced by the loop-closure sections |
| CV-VIO-003 | Yaw and global position are gauge freedoms of VIO, scale is not: confirmed (Zhang and Scaramuzza §III-A eq. 11, Table I; VINS-Mono §VII); excitation needed for scale (VINS-Mono §I) | Reasoning: separate a gauge from an estimation error | 2 expected criteria; 299 → 290 | Expected answer "can remain a gauge" weakened a sourced statement | Minor | Expected-answer fix (language and sourced strength); language fixes ("strain", "freedoms withdrawn", "visual monocular"); Source line updated |
| CV-VIO-004 | 2° at 100°/s over 20 ms: recomputed (checks/63-slam-vio.py). Expected answer "measure precision" mistranslated *précision* (accuracy) | Design: AR headset pipeline with latency and evaluation | 3 expected criteria; 299 → 311 | "Seniority" (age), "helmet" (headset), "channel" (pipeline), "Criteria for correction" mistranslated | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given ORB-SLAM3 §V-D/§VII-B and Zhang |
| CV-VIO-005 | Accelerometer-bias laws confirmed by kinematics. "A constant gyroscope bias … can also incorrectly orient gravity" omitted the condition: only a tilt (roll/pitch) error leaks gravity, with a position error growing as $g\,b_\omega t^3/6$; a yaw error leaks none (recomputed by checks/63-slam-vio.py) | Diagnosis: separate texture, excitation, bias, timing and loop causes | 3 expected criteria; 369 → 395 | Condition added identically in the card and the reference appendix | Minor | Missing condition added; language fixes ("essays", "Reserve sequences", "final path") |

Expected-answer changes (no change of criteria):

- CV-VIO-001 (language): "No: it summarizes measurements between keyframes in
  constraints with noise and bias; the system must also associate the vision,
  initialize and estimate the states." → "No: it summarizes the measurements between
  keyframes into constraints with their noise and bias dependence; the system must
  also associate visual observations, initialize and estimate the states."
- CV-VIO-003 (language and sourced strength, Zhang and Scaramuzza §III-A): "Without
  external reference, the global yaw can remain a gauge, while the metric scale
  depends on sufficient excitation and calibration and can be mistakenly estimated."
  → "Without an external reference, global yaw remains a gauge freedom, while the
  metric scale depends on sufficient excitation and calibration and can be wrongly
  estimated."
- CV-VIO-004 (meaning-restoring): "Define coordinate frames/time, calibrate sensors
  and delays, choose causal estimation and loss management, then measure precision,
  drift and latency on representative movements." → "Define frames and time
  references, calibrate sensors and delays, choose causal estimation and
  tracking-loss handling, then measure accuracy, drift and latency on representative
  motions."

## Reference findings

Claims of revision 7 checked against their passages:

- Preintegration increments with $R_i$ body→world: confirmed (Forster et al. §VI
  eq. 33).
- "A VIO without global references keeps global translation and yaw unobservable":
  confirmed (Zhang and Scaramuzza §III-A eq. 11; VINS-Mono §VII).
- "The metric scale requires sufficient excitation and calibration": confirmed for
  excitation (VINS-Mono §I).
- "DBoW2/NetVLAD offer location candidates; geometric verification is still
  required": confirmed for DBoW2 (VINS-Mono §VII-A, §VII-B; ORB-SLAM3 §VI-A). NetVLAD
  was not opened and is no longer named in the body.
- "A Sim(3) alignment can hide a bad scale": confirmed by Table I of Zhang and
  Scaramuzza and recomputed in worked example D.

No scientific error was found in revision 7. Its body held one to three sentences
per section, and its English obscured meaning: "no encrypted drift" (*no quantified
drift*), "Single vision" (*monocular vision*), "The check trajectory remains out of
scope", "speed" (*velocity*), "material performance" (*hardware performance*).

New claims verified for revision 8 (main ones):

- Forster et al.: IMU model with specific force and random-walk biases (§V eqs. 27–28,
  §VI-E eqs. 46–47); discrete integration assuming constant orientation between
  samples, Earth rotation neglected, discrete noise $\mathrm{Cov}(\eta_d)=\mathrm{Cov}(\eta)/\Delta t$ (§V eqs. 29–31);
  re-integration problem and increments (§VI eqs. 32–33); covariance propagation
  (§VI-B); first-order bias update (§VI-C eq. 44); residuals (§VI-D); structureless
  vision factor and reprojection residual (§VII eq. 50).
- VINS-Mono: excitation needed for scale (§I); 4-DOF versus 7-DOF pose graphs (§II);
  keyframes by rotation-compensated parallax (§IV-A); re-propagation for large bias
  changes (§IV-B); initialization thresholds of 30 features and 20 pixels (§V-A);
  linear initialization of velocities, gravity and scale (§V-B eqs. 16–20);
  marginalization fixing linearization points and keeping spatially separated
  keyframes (§VI-D); drift directions, roll and pitch observable, DBoW2 with 500
  extra BRIEF corners, two-step verification (§VII, §VII-A, §VII-B, Fig. 10); online
  extrinsic calibration (§I).
- ORB-SLAM3: MAP IMU initialization in 2 s with 10 keyframes at 4 Hz, 5% then 1% scale
  error, possible failure under slow motion (§V-B); visual loss below 15 tracked
  points, new map after 5 s (§V-D); raw DBoW2 precision and recall of 50–80% and
  geometric verification (§VI-A); median of 10 runs, 3.5 cm on EuRoC, 9 mm on TUM-VI
  room, end-only ground truth on TUM-VI (abstract, §VII-A, §VII-B).
- MSCKF: left-nullspace projection giving $2M_j-3$ residuals (§III-D eqs. 23–24),
  $N_{\max}$ pose management and QR step (§III-E), complexity linear in features and
  at most cubic in states (§III-F), 3.2 km drive with about 10 m final error measured
  against the parking spot, 14 Hz on a 2 GHz T7200 (§IV).
- Zhang and Scaramuzza: yaw-only gauge (§III-A eq. 11), alignment per configuration
  (Table I), ATE and relative error (§IV-A, §IV-B).

Variants recorded in the note (FR-036): Forster et al. correct bias changes to first
order only (§VI-C), whereas VINS-Mono re-propagates when the change is large
(§IV-B). GTSAM 4.2 sets IMU noise covariances to identity matrices by default, which
are placeholders rather than sensor values.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 343 → 3,973.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Inputs with units and rates, specific-force model, calibration inputs; state definition and frames; odometry / relocalization / SLAM output contracts with consumers |
| Intuition | Shallow | Developed | Complementarity of IMU and camera; constructed corridor illustration (missing loop, false loop); Mermaid data flow |
| Prerequisites | Shallow (four links) | Developed | Links to CV-SE3, CV-FUSION, CV-FACTEURS, CV-EPIPOLAIRE, CV-BA, CV-CAPTEURS, CV-MULTICALIB, CV-ORB, CV-FLOT, CV-METRIQUES-TEMPS, CV-ICP |
| Assumptions | Shallow (one sentence) | Developed | Sensor model; rigid synchronized rig; four gauge directions with sources; scale excitation with a one-line derivation; visual degeneracies; initialization conditions |
| Procedure | Shallow | Developed | Event-driven pseudocode with purpose of each step; MSCKF / sliding-window / keyframe-SLAM comparison table |
| Mathematics | Shallow (two formulas) | Developed | Conventions and noise units; IMU integration; preintegration increments, covariance, bias update; visual factor and MSCKF nullspace; VINS-Mono linear initialization; worked examples A (noise versus bias), B (tilt and gravity leak), C (scale versus excitation) |
| Parameters | Shallow (list) | Developed | Eight-row parameter table with source values and interactions; tuning approach |
| Properties | Absent (merged with parameters) | Developed | Exactness of preintegration and its limits; MAP up to linearization; structural drift; what loops do; IMU bridging of visual loss |
| Cost and implementation | Shallow | Developed | Cost drivers for preintegration, MSCKF, sliding windows and loops; GTSAM 4.2 contract (gravity convention, noise units and defaults, sensor frame, bias consistency, bias Jacobians); execution status |
| Evaluation | Shallow | Developed | Alignment per configuration; ATE versus relative error; worked examples D (alignment hides scale) and E (latency); published results with protocol; proposed baseline and time-offset variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (stereo VO, VIO, filter versus optimization, SLAM versus odometry, LiDAR, GNSS and wheels); industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/63-slam-vio.py`](checks/63-slam-vio.py) (12 assertions): discrete noise
0.028 m/s² at 200 Hz; noise-only spread 6.3 mm/s and 3.7 cm after 10 s against 0.2 m/s
and 1.0 m from a 0.02 m/s² bias; 1° tilt from 0.1°/s over 10 s, 0.17 m/s² of leaked
gravity per degree and 2.85 m of cubic drift; growth ratios 8 versus 4 when time
doubles; no leak for yaw; 10% versus 1% scale error at 0.2 and 2 m/s²; ATE 1.46 m after
4-DOF alignment versus 0 after Sim(3) for a 5% scale error over 100 m; 2° and 35 mm at
1 m for 20 ms at 100°/s.

## Applied corrections

- [Reference](../../../vault/60-vision-3d/references/63-slam-vio.md), revision 7 → 8:
  body rewritten and deepened as above; mistranslations fixed in the appendices,
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Example of limit" → "Example of a limit",
  "Proposed Ablations" → "Proposed ablations", "Seniority budget of pose" → "Pose
  age budget", "helmet" → "headset", "essays" → "tests", "algebraic add-ins" →
  "algebraic additions", "Documentary reference" → "Documentation consulted");
  sources split into scientific and implementation sources; closing provenance line
  replaced. Front matter unchanged except `revision`; H1, per-card headings and
  appendix headings kept.
- [Cards](../../../vault/60-vision-3d/63-slam-vio.md): three expected answers fixed
  (quoted above); the imprecise preintegration sentence of CV-VIO-001 corrected; the
  gravity-leak condition added to CV-VIO-005 (also in the reference appendix);
  language fixes in further explanations, blocking errors and grading criteria
  ("Criteria for correction of the case" → "Grading criteria for the case"); Source
  lines cleaned of "consult the 2026-10-30" fragments and given sections relevant to
  each card. Questions, IDs, objectives, families, tags, `cas_pole` tags and target
  deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`preintegration`, `Sim(3)`, `yaw` and `gyroscope bias`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). No CV-VIO proposal is registered yet; the 2026-10-20 proposal
on first-order bias correction versus reintegration is now covered by the CV-VIO-001
explanation and is not repeated.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-VIO-01 | CV-VIO | Explain what ATE and the relative error over sub-trajectory lengths each reveal about a VIO run, and why ATE depends on when an error occurs | Evaluation family absent; no card trains the choice of trajectory metric | Evaluation; Evaluation and controlled variation | 1 card, 3 criteria | [Zhang and Scaramuzza 2018, §IV-A and §IV-B](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) |
| P-CV-VIO-02 | CV-VIO | Configure IMU preintegration in a factor-graph library: gravity sign convention, continuous-time noise densities and their units, and a bias random-walk factor | Practice family absent; sign and unit errors break VIO silently | Practice; Cost and implementation (GTSAM 4.2 contract) | 1 card, 3 criteria | [GTSAM 4.2 `PreintegrationParams.h` L27–L59](https://github.com/borglab/gtsam/blob/4.2/gtsam/navigation/PreintegrationParams.h); [Forster et al. §V](https://arxiv.org/abs/1512.02363) |

## Sources

Scientific sources, opened at the passages listed:

- Forster et al., [arXiv 1512.02363v3 PDF](https://arxiv.org/pdf/1512.02363v3) (text
  extracted with `pdftotext`): §V, §VI, §VI-A to §VI-E, §VII.
- Qin, Li and Shen, VINS-Mono, [arXiv HTML 1708.03852v1](https://arxiv.org/html/1708.03852v1):
  §I, §II, §III, §IV-A, §IV-B, §V-A, §V-B, §VI-D, §VII, §VII-A, §VII-B, §VIII.
- Campos et al., ORB-SLAM3, [arXiv HTML 2007.11898](https://arxiv.org/html/2007.11898):
  abstract, §I, §II, §V-B, §V-D, §VI-A, §VII-A, §VII-B.
- Mourikis and Roumeliotis, MSCKF, [ICRA 2007 PDF](https://www-users.cse.umn.edu/~stergios/papers/ICRA07-MSCKF.pdf):
  abstract, §III-D, §III-E, §III-F, §IV.
- Zhang and Scaramuzza, [IROS 2018 PDF](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf):
  §III-A (eqs. 8–11), Table I, §IV-A, §IV-B.

Implementation sources (official code at tag 4.2):

- GTSAM 4.2 headers under [`gtsam/navigation/`](https://github.com/borglab/gtsam/tree/4.2/gtsam/navigation):
  `PreintegrationParams.h` L27–L59, `PreintegratedRotation.h` L33–L38,
  `ImuFactor.h` L63–L134 and L160–L167, `CombinedImuFactor.h` L63–L65,
  `ManifoldPreintegration.h` L42–L46, `PreintegrationBase.h` L150–L156.

Failed accesses and limits:

- The GTSAM tutorial (§4.1) cited by CV-VIO-002 was not re-read; it is retained from
  the 2026-10-20 pass.
- Not opened: NetVLAD, the EuRoC and TUM-VI dataset papers (their figures are cited
  through ORB-SLAM3), observability and consistency analyses of EKF-based VIO
  (Hesch et al.), Kalibr and Allan-variance procedures. The tuning advice that uses
  Allan variance is labelled as project method.
- Context7 was not available in this session; GTSAM headers at a tag replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | One failure, outside this subject: `80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md` (another agent's file in progress); no error in CV-VIO files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/63-slam-vio.py` | 12 checks passed |
| `git diff --check -- vault/60-vision-3d/ docs/revues/2026-11-14-reference-depth/checks/63-slam-vio.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/60-vision-3d/63-slam-vio.md` | 5 cards, 290–395 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…` (including the anchors `cv-vio-004` and `cv-vio-005`), `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 7` → `8`; H1 and the 10 per-card headings unchanged; `$$` balanced |

No VIO system, GTSAM factor or dataset was run; the proposed baseline and variation
are protocols, not results. The Mermaid diagram and tables were not rendered in
Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-VIO revision 8, CV-VIO-001 to CV-VIO-005, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-VIO-01, P-CV-VIO-02).
