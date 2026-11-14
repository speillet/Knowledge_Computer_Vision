# Review — Multisensor calibration, hand–eye calibration and timing — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is now the pipeline and decision note for calibration *between*
sensors (camera rigs, camera–IMU, camera–LiDAR, robot–camera) and timing. The
$AX=XB$ solvers stay in
[CV-HANDEYE](../../../vault/50-calibration-geometrie/references/57-calibration-hand-eye.md),
clock offset and drift in
[CV-CAPTEURS](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md);
this note links to them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MULTICALIB-001 | Eye-in-hand chain ${}^bT_g\,{}^gT_c\,{}^cT_t$ equal across poses and $A_iX=XB_i$: confirmed by OpenCV 4.13.0 `calib3d.hpp` L2210–L2353. Expected answer "their meaning" mistranslated *leur sens* (their direction); "string" for chain, "catches" for captures, "assembly" for mounting, "top coordinate frame" for the upper-left index | Reasoning: turn $AX=XB$ into a defined frame chain before solving | 4 expected criteria; 348 → 355 lexical words | Notation identical to the reference and to CV-HANDEYE | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line moved to the versioned header with lines |
| CV-MULTICALIB-002 | Translation component along a single rotation axis unconstrained, $(R_A-I)n=0$: confirmed algebraically (recomputed by the check script) and consistent with OpenCV's requirement of two motions with non-parallel axes (L2352–L2353). "adds less average noise, but not necessarily new directions of stress" obscured the point (averaging versus new constrained directions); "lift it", "following $n$", "pose robot error" | Diagnosis: separate pose count from pose diversity | 2 expected criteria; 336 → 335 lexical words | Consistent with the reference Observability section | Minor | Language fixes; Source line given exact lines |
| CV-MULTICALIB-003 | Intrinsic reprojection does not test extrinsic, offset or scan distortion: confirmed as a separation of models; LiDAR motion distortion confirmed by LOAM Fig. 1 and §V-C; offset modelling by Qin and Shen §III. Expected answer "does not alone test … the deformation of the scan" made precise as motion distortion; "the wearer" (*porteur*: carrier platform), "A merger" (*fusion*), "Survey built", "time by point" | Comparison: three contracts with different validation data | 3 expected criteria; 367 → 379 lexical words | Consistent with worked example A and the failure table | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |

Expected-answer changes (meaning-restoring language fixes):

- CV-MULTICALIB-001: "We must define the coordinate frames, the relative A/B movements,
  their meaning and the unknown transformation X." → "The coordinate frames, the relative
  motions A and B, their direction and the unknown transformation X must be defined."
- CV-MULTICALIB-003: "It does not alone test the extrinsic between sensors, their temporal
  offset or the deformation of the scan." → "On its own, it tests neither the extrinsic
  between the sensors, nor their temporal offset, nor the motion distortion of the scan."

The objective line of CV-MULTICALIB-003 ("separating intrinsic extrinsic and time") is
protected; proposed wording for a learner-approved edit: "Separate intrinsic, extrinsic
and temporal calibration".

## Reference findings

Claims of revision 7 checked against their passages:

- Eye-in-hand convention $G_i={}^bT_{g_i}$, $C_i={}^{c_i}T_t$, $X={}^gT_c$,
  $A_{ij}=G_j^{-1}G_i$, $B_{ij}=C_jC_i^{-1}$: confirmed (OpenCV `calib3d.hpp`
  L2210–L2353).
- "Do not announce a universal minimum independent of the solver and trajectories":
  imprecise. OpenCV states a necessary minimum, two motions with non-parallel rotation
  axes and so at least three poses, while strongly recommending many more (L2352–L2353).
  Revision 8 states the necessary minimum and the recommendation.
- $\delta p\simeq(v+\omega\times p)\delta t$ and 20 cm at 10 m/s for 20 ms: confirmed
  arithmetic.
- No scientific error found. The body was shallow and the appendices contained
  mistranslations ("Question of work", "Reference Response", "derivation per chain",
  "Survey built", "Order of temporal magnitude", "built-in calculation", "the wearer",
  "A merger", "catches", "lift it", "following $n$").

New claims verified for revision 8 (main ones):

- Rehder, Siegwart and Furgale 2016 (thesis ch. 3): clock synchronization versus temporal
  calibration and the three synchronization schemes; offsets from integration,
  transmission and filter delays; mid-exposure measurement instant (§3.1); delayed error
  term and its linearization, eqs. 3.2–3.5 (§3.3.1); 1–2 min capture exciting all
  rotational degrees of freedom, sixth-order pose spline, cubic bias splines, IMU and
  projection models eqs. 3.6–3.11, plane model for LiDAR (§3.3.2); 0.5 px image noise,
  200 Hz IMU, 20 Hz camera (§3.4.2); simulation consistency and local convexity in $d$,
  "not … a formal proof" (§3.4.3); slope 0.498 versus 0.5 and ±0.2 ms residuals (§3.4.4).
- Qin and Shen: $t_{IMU}=t_{cam}+t_d$, constant unknown offset, drifting offsets
  "unqualified for sensor fusion", feature velocity and shifted observation (eqs. 1, 2, 4).
- LOAM: constant angular and linear velocity during a sweep and linear pose interpolation
  per point (§V-C, eq. 4); distortion from points received at different times (Fig. 1).
- OpenCV 4.13.0: `stereoCalibrate` convention $X_2=RX_1+T$, default
  `CALIB_FIX_INTRINSIC`, divergence warning and recommendation, criteria;
  `calibrateHandEye` inputs, methods, eye-in-hand and eye-to-hand chains, minimum
  motions; `calibrateRobotWorldHandEye` outputs.
- Kalibr wiki: IMU intrinsic and noise requirements, excitation advice, 20 Hz/200 Hz,
  Aprilgrid, temporal calibration on by default, outputs, IMU timestamp bursts, 4 Hz
  for multi-camera calibration.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 343 → 3,289. About a
fifth of the tokens are tables, the procedure block and the Mermaid diagram.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Spatial and temporal tasks; clock synchronization versus temporal calibration; table of four configurations with observations, estimates and constraints; data contract (directions, units, mid-exposure, per-point LiDAR time); pipeline roles |
| Intuition | Shallow (merged) | Developed | Static versus motion signatures; constructed time-offset illustration (20 px, 4 px); Mermaid pipeline diagram |
| Prerequisites | Developed (3 links) | Developed | Added CV-HANDEYE, CV-BA, CV-FUSION, CV-ICP with the reason for each |
| Assumptions | Shallow | Developed | Rigid mounting, constant offset, calibrated intrinsics, noise models; observability for hand-eye, camera–IMU, time offset, delay versus translation, plane normals; degenerate cases (planar motion, symmetric targets, IMU bursts) |
| Procedure | Shallow | Developed | Eight-step procedure with the purpose of each step, including the three synchronization schemes |
| Mathematics | Shallow (one chain) | Developed | Transform conventions; `stereoCalibrate` convention and camera-centre pitfall; hand-eye chain; continuous-time delayed error and its Jacobian; camera–IMU models; Qin–Shen approximation; LOAM interpolation; error propagation and worked example B |
| Parameters | Shallow | Developed | Nine-row table of noise models, rates, duration, exposure, spline order, temporal switch, hand-eye method and pose count, `stereoCalibrate` flags; five-step tuning approach |
| Properties | Shallow (merged) | Developed | Conditional consistency and its evidence; empirical precision with setup; separable versus simultaneous hand-eye; constant-offset model; validity domain |
| Cost and implementation | Shallow | Developed | Cost drivers with a constructed data count; OpenCV 4.13 and Kalibr contracts; execution status |
| Evaluation | Shallow | Developed | Metrics per configuration; baseline and exposure-change controlled variation adapted from Rehder et al. §3.4.4, with expected effect and confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Offline batch, online temporal calibration, hardware triggering, robot–world–hand–eye, targetless (not reviewed); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/55-calibration-multicapteurs.py`](checks/55-calibration-multicapteurs.py)
(11 assertions): time-offset pixel errors (20 px rotation; 20 px and 4 px translation),
delay–translation equivalence at two speeds, extrinsic error propagation (1.75 px and
8.7 cm for 0.1°; 5 px and 0.2 px for 1 cm; crossover at 5.7 m), the half-exposure rule
and 4% of the IMU period, data counts for a 2-minute capture, rank 2 of $(R_A-I)$ for a
single-axis rotation, and the `stereoCalibrate` inversion $X_1=R^\top(X_2-T)$.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md),
  revision 7 → 8: body rewritten and deepened as above; the imprecise "universal minimum"
  sentence replaced by OpenCV's necessary minimum and recommendation; appendix language
  fixed identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Documentary reference for this pass" → "Source consulted
  for this pass", "Component not constrained" → "Unconstrained component", "Order of
  temporal magnitude" → "Order of magnitude of a time offset", "Separate the Contracts" →
  "Separate the contracts", "Survey built" → "Constructed protocol"); sources split;
  closing provenance line replaced. Front matter unchanged except `revision`; H1 and
  per-card headings kept.
- [Cards](../../../vault/50-calibration-geometrie/55-calibration-multicapteurs.md): the
  two expected-answer fixes above; further-explanation fixes: "Check a string of
  transformations on a point and reserved movements" → "Check the chain of transformations
  on a point and on held-out motions"; "check the reverse of the string" → "check the
  inverse chain"; "precedes the solver setting" → "precedes solver tuning"; "Between two
  catches, multiply the equality left by … gives" → "Between two captures, multiplying the
  equality on the left by … gives"; "the assembly" → "the mounting"; "noncommutative" →
  "non-commuting"; "Copy the matrices of an API without checking their meaning" → "Passing
  an API's matrices without checking their direction and meaning"; "gross number of
  poses" → "raw number of poses"; "adds less average noise, but not necessarily new
  directions of stress" → "averages noise down, but does not necessarily add newly
  constrained directions"; "a reserved path" → "a held-out path"; "pose robot error" →
  "robot pose error"; "by developing homogeneous transformations, we obtain" → "Expanding
  the homogeneous transformations gives"; "following $n$" → "along $n$"; "lift it,
  subject to" → "remove it, provided"; "the wearer" → "the carrier platform"; "A merger" →
  "A fusion"; "for check" → "to check"; "inspecting time by point" → "inspecting the
  per-point LiDAR timestamps"; "Reserve a sequence with other moves" → "Hold out a sequence
  with other motions"; "built-in calculation" → "constructed calculation"; "Assimilate
  camera calibration quality and complete fusion quality" → "Equating camera calibration
  quality with the quality of the complete fusion". Source lines now cite the OpenCV
  4.13.0 header with lines, LOAM §V-C and Qin and Shen §III. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file repeats a corrected claim (`rg` over `vault/` for "universal minimum"
and the hand-eye minimum).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). The 2026-10-20 idea "Diagnose offset and clock drift separately" is
already covered by CV-CAPTEURS-002 and is not repeated.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-MULTICALIB-01 | CV-MULTICALIB | Predict how the estimated camera–IMU offset changes when only the exposure time changes, and use it to test the timestamp convention | Mid-exposure timestamping and induced-change validation are untested | Evaluation; Evaluation and controlled variation | 1 card, 3 criteria (half-exposure rule; what a slope of 0 or 1 would mean; confound of blur) | [Rehder et al. 2016, §3.1 and §3.4.4, in Rehder 2018 ch. 3](https://doi.org/10.3929/ethz-b-000334970) |
| P-CV-MULTICALIB-02 | CV-MULTICALIB | From projection errors measured at near and far range, decide whether an extrinsic error is rotational or translational | Range dependence as a discriminating check is untested | Diagnosis; Failure modes, worked example B | 1 card, 3 criteria ($f\delta\theta$, $f\delta t/Z$, crossover range) | Pinhole projection model, [OpenCV 4.13.0 `calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); derivation is a project deduction |

## Sources

Scientific sources, opened at the passages listed:

- Rehder, Siegwart and Furgale 2016 (IEEE T-RO), as chapter 3 of
  [Rehder 2018, ETH thesis](https://doi.org/10.3929/ethz-b-000334970) (PDF from the ETH
  Research Collection, text extracted with `pdftotext`): §1.2 (chapter-to-publication
  mapping), §3.1, §3.3, §3.3.1, §3.3.2 (to eq. 3.14), §3.4.2–§3.4.4 with Figs. 3.5–3.7.
- Qin and Shen 2018, [arXiv 1808.00692 PDF](https://arxiv.org/pdf/1808.00692): §I, §III-A
  to §III-C.
- Zhang and Singh 2014, [LOAM, RSS PDF](https://www.roboticsproceedings.org/rss10/p07.pdf):
  Fig. 1, §V-C.

Implementation sources:

- [OpenCV 4.13.0 `calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L636–L653, L1880–L2003, L2210–L2358, L2361–L2505.
- [Kalibr wiki, Camera-IMU calibration](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration),
  [Multiple camera calibration](https://github.com/ethz-asl/kalibr/wiki/multiple-camera-calibration)
  (raw wiki Markdown; unversioned, consulted 2026-11-14).

Failed accesses and limits:

- Furgale, Rehder and Siegwart 2013 (IROS): the author-hosted PDF returned
  "Page not found"; its findings were read through Rehder et al. 2016 as reproduced in the
  thesis, which states that it incorporates them. The 2013 paper itself is not verifiable
  in this pass.
- docs.opencv.org returned HTTP 403; the 4.13.0 header was read instead. Context7 was not
  available.
- Not reviewed: targetless camera–LiDAR methods, Kelly–Sukhatme and Mair et al. offset
  estimators (named in Rehder et al. §3.1 only).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/55-calibration-multicapteurs.py` | 11 checks passed |
| `git diff --check -- vault/50-calibration-geometrie/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/55-calibration-multicapteurs.md` | 3 cards, 355, 335 and 379 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 0 errors; 2 expected answers changed as recorded; front matter identical except `revision: 7` → `8` |
| Local link and anchor check over `vault/50-calibration-geometrie` | 129 local links, 0 errors |

No calibration, Kalibr run or OpenCV call was executed; the baseline and variation are
protocols. Mermaid and tables were not rendered in Obsidian; AnkiDroid rendering is
unverified. This is agent self-review without independent validation. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-MULTICALIB
revision 8, CV-MULTICALIB-001 to 003, corrections above, Agent Claude Code self-review,
to republish with `paquet-anki`) and the proposal register (P-CV-MULTICALIB-01,
P-CV-MULTICALIB-02).
