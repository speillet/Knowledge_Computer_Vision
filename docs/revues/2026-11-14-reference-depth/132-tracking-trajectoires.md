# Review — Evaluating identities, trajectories and 3D localization — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 6 to revision 7. Highest severity per card before correction: 0 blocking,
3 important, 2 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a metric and protocol note covering two families: multi-object
tracking metrics (CLEAR MOT, IDF1, HOTA) and trajectory errors (ATE, RPE). Estimator
mechanisms and a longer scale-error example stay in
[CV-VIO](../../../vault/60-vision-3d/references/63-slam-vio.md), trackers in
[SORT](../../../vault/110-tracking-association/references/111-sort.md) and
[DeepSORT and ByteTrack](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md);
this note links to them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Identical boxes with swapped IDs leave per-frame detection unchanged: confirmed by the definitions (HOTA §3–§5; Ristani et al. §3.3). Source line cited Zhang and Scaramuzza §IV (ATE) and an "inferred inequality of aggregation", which do not support an identity claim: unsupported citation | Evaluation: separates detection from identity, the first decision when reading a tracking score | 1 criterion; 268 → 260 lexical words | "Decomposition of monitoring", "trackss", "classifying" (ranking), "the path" (learning path) | Important | Source line replaced by HOTA §4.1, §4.2, §5 and Ristani §3.3; language fixes |
| CV-METRIQUES-TEMPS-002 | HOTA is the per-threshold root averaged over 19 thresholds: confirmed (HOTA §5 eqs. 13–16; TrackEval `hota.py` L166–L173). The explanation stated that Cauchy–Schwarz equality "requires a compatible ratio between sequences": the condition is proportional profiles *across thresholds*. Expected answer said operations "do not switch" (commute) | Reasoning: aggregation order of a composite metric | 1 criterion; 364 → 399 | Source line cited Zhang and Scaramuzza (unrelated); "medium" for mean in the blocking errors; decimal commas | Important | Equality condition corrected; implementation note on TrackEval's single matching per frame added; meaning-restoring fix of the expected answer; Source line cites eqs. and code lines |
| CV-METRIQUES-TEMPS-003 | Sim(3) absorbs a metric scale error: confirmed (Zhang and Scaramuzza §III-A, Table I: 4-DoF alignment for visual-inertial systems). Explanation said the group must follow "the gauges and the lens" (objective) and that the score "no longer tests the mischievousness" (metric scale) | Evaluation: choosing an alignment from observability | 1 criterion; 285 → 297 | Source line cited HOTA §5 (unrelated) | Important | Meaning-restoring language fixes in the explanation; Source line cites Zhang and Scaramuzza §III and Sturm §VII-B |
| CV-METRIQUES-TEMPS-004 | ATE after alignment versus RPE over intervals: confirmed (Sturm et al. §VII-A/B, eqs. 1–5; Zhang and Scaramuzza §IV, Table II); $E_{ij}$ matches Sturm eq. 1 | Comparison: global consistency versus drift | 1 criterion; 327 → 349 | "bodies→world", "norm translation", "looping"; Source line cited HOTA | Minor | Language fixes; Source line cites equations |
| CV-METRIQUES-TEMPS-005 | Time association, interpolation, conventions, alignment, intervals and missing poses explain tool differences: confirmed (Sturm §VI–§VII; TUM tools page). Missing condition: the TUM `evaluate_rpe.py` prints a mean by default while the paper defines an RMSE. Expected answer read "matching time … loss processing" | Diagnosis: reconciling two trajectory evaluators | 1 criterion; 344 → 375 | "check then sense", "processing absences", "the same size" | Minor | Meaning-restoring fix of the expected answer; default-statistic condition added; language fixes; Source line cites Sturm §VI–§VII and the TUM tools page |

Expected-answer changes (meaning-restoring language fixes):

- CV-METRIQUES-TEMPS-002: "…then averages these scores; operations do not switch in
  general." → "…then averages these scores; the two operations do not commute in
  general."
- CV-METRIQUES-TEMPS-005: "matching time, interpolation, conventions of pose,
  alignment, intervals and loss processing." → "Time association, interpolation, pose
  conventions, alignment, intervals and the handling of lost or missing poses."

## Reference findings

Claims of revision 6 checked: HOTA per threshold then averaged (HOTA §5, eq. 16):
confirmed; $E_{ij}$ relative error (Sturm et al. §VII-A, eq. 1): confirmed; Sim(3) for
monocular, translation and yaw for VIO (Zhang and Scaramuzza §III-A, Table I):
confirmed; MOTA aggregates misses, FPs and switches (CLEAR MOT §2.2, eq. 2): confirmed.
No scientific error was found in the body; it was shallow (one to three sentences per
section) and mistranslated ("lacks" for misses, "the average score the thresholds",
"bodies→world", "Visual monocular", "Editor: agent"). The 2026-10-30 appendix attributed
the RPE formula to the project although it is Sturm et al.'s eq. 1; corrected.

New claims verified for revision 7 (main ones): CLEAR MOT mapping procedure,
sum-before-ratio example (16/20 = 80% versus 50%), threshold discussion and 50 cm
(§2.1.3, §2.2, Fig. 3, §4); IDF1 graph, miss definition, eqs. 6–11 and one-to-one ID
mapping versus CLEAR's many-to-many (Ristani et al. §3.3–§3.5); HOTA task definition,
TPA/FNA/FPA, DetA/AssA/LocA, 19 thresholds, MOTA and IDF1 problems, application
scenarios (§3–§6, §9); RPE and ATE definitions, drift per frame or per second,
$\Delta=n$ warning, quadratic cost, ATE/RPE correlation remark, 20 ms colour–depth delay
(Sturm et al. §VI–§VII); alignment groups and Umeyama alignment, relative error over
sub-trajectories, ATE sensitivity to the time of the error (Zhang and Scaramuzza
§III–§IV, Tables I–II); TrackEval matching, IDSW, MT/PT/ML, combination and
preprocessing; TUM script options; nuScenes center-distance mAP and NDS.

Source disagreements recorded in the note (FR-036):

| Aspect | Source A | Source B |
| --- | --- | --- |
| HOTA matching | Paper: separate matching per $\alpha$ with score $1/\epsilon+\mathcal A_{\max}+\epsilon\mathcal S$ (§5, eqs. 15–16) | TrackEval `12c8791`: one Hungarian per frame on global alignment × similarity, filtered per $\alpha$ (`hota.py` L66–L97) |
| MOTP | CLEAR MOT: mean distance of matches, lower is better (eq. 1) | TrackEval: mean IoU of TPs, higher is better (`clear.py` L115, L123, L179) |
| RPE statistic | Sturm et al.: RMSE (eq. 2) | TUM `evaluate_rpe.py`: mean translational error printed by default (tools page) |
| "ATE" | Trajectory: absolute trajectory error after alignment (Sturm §VII-B) | nuScenes: average translation error of 3D detections in meters (detection README) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 345 → 4,676. The note covers two metric families
and their reference implementations; estimator content and the long scale example are
linked to CV-VIO rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | MOT and trajectory data contracts (IDs, boxes, similarity, timestamps, pose files, units); outputs; time contract; pipeline roles |
| Intuition | Shallow | Developed | What each MOT metric counts (events, frames, per-TP overlap); ATE versus RPE; Mermaid data flow of both families |
| Prerequisites | Shallow (two links) | Developed | Links to CV-IOU-AP, DeepSORT/ByteTrack, CV-SE3, CV-ICP, CV-CAPTEURS, CV-POSE3D, CV-FIABILITE |
| Assumptions | Shallow | Developed | Exhaustive IDs and distractor handling; threshold choice; comparable sequences; gauge per sensor; clock synchronization; degenerate cases with code lines; observability |
| Procedure | Shallow | Developed | Pseudocode for CLEAR, IDF1, HOTA, ATE and RPE; purpose of each step with sources |
| Mathematics | Shallow (two formulas) | Developed | MOTA, MOTP, IDSW; IDP, IDR, IDF1; TPA/FNA/FPA, DetA, AssA, HOTA, LocA; RPE, ATE and alignment; frame invariance of RPE; worked examples A (four identity scenarios) and B (alignment groups) |
| Parameters | Shallow (list) | Developed | Ten-row table (thresholds, preprocessing, combination, MT/ML, time association, alignment, interval, statistic); four-step protocol-fixing approach |
| Properties | Shallow | Developed | MOTA detection weighting and frame-rate dependence (example C); IDF1 limits; HOTA decomposition and metric property claim; ATE time sensitivity; RPE invariance |
| Cost and implementation | Shallow | Developed | Cost drivers; TrackEval `12c8791` contracts and paper/code differences; NumPy alias issue; TUM script options; execution status |
| Evaluation | Shallow | Developed | Evaluator validation tests; sequence-level resampling; baseline and frame-deletion variation with expected effect and limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (HOTA, IDF1, MOTA, Track-mAP, RPE, ATE, nuScenes); HOTA authors' scenarios; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/132-tracking-trajectoires.py`](checks/132-tracking-trajectoires.py)
(14 checks): MOTA, IDF1, DetA, AssA and HOTA for the swap (0.90, 0.50, 1, 1/3, 0.577),
fragment (0.95, 0.75, 1, 0.75, 0.866), gap (0.75, 0.857, 0.75, 0.833, 0.791) and
corrected-swap (0.80, 0.80, 1, 0.556, 0.745) scenarios; MOTA at two frame rates (0.940,
0.945; switch share 16.7% and 9.1%); the HOTA aggregation counterexample and
Cauchy–Schwarz bound; ATE for a 2% scale error (0.0632 m rigid, 0 similarity), RPE over
1 m and 5 m (0.02, 0.10 m), a 1° tilt under 4-DoF alignment (0.0552 m) and a pure gauge
change (0).

## Applied corrections

- [Reference](../../../vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md),
  revision 6 → 7: body rewritten and deepened as above; appendices corrected identically
  to the cards ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "Choice of measures" → "Choice of metrics", "Decomposition of
  monitoring" → "Decomposition of tracking errors", "trackss" → "tracks", "Average and
  covariance of components" → "Mean of components and their covariation", equality
  condition corrected, "Permitted processing" → "Permitted transformation", "poses
  bodies→world" → "body-to-world poses", "Interpolation and Time" → "Interpolation and
  time", "allows to verify" → "verifies"); the 2026-10-30 source line now credits Sturm
  et al. for the RPE formula; two lines that Markdown would have parsed as link
  definitions were reflowed; sources split into scientific and implementation sources;
  closing provenance line replaced. Front matter unchanged except `revision`; H1 and the
  eight `### …CV-METRIQUES-TEMPS-…` headings kept.
- [Cards](../../../vault/130-evaluation-fiabilite/132-tracking-trajectoires.md): expected
  answers of 002 and 005 as quoted above. Further explanations: language fixes in all
  five; CV-METRIQUES-TEMPS-002 equality condition corrected and the TrackEval matching
  note added; CV-METRIQUES-TEMPS-003 "the gauges and the lens" → "the gauge freedoms and
  the evaluation objective", "mischievousness" → "metric scale"; CV-METRIQUES-TEMPS-005
  default-statistic note added. Blocking errors rephrased ("Freely swap medium and root"
  → "Freely swapping the mean and the square root"). Source lines now cite the passages
  that support each card and label project constructions. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file repeats a corrected claim (`rg` for HOTA, IDF1, MOTA, ATE, RPE,
Sim(3) and NDS). CV-VIO (another subject) states the alignment groups consistently with
Zhang and Scaramuzza Table I.

## Proposals

Existing pending proposal for this subject: P-CV-METRIQUES-TEMPS-01 (worked IDF1 after an
ID switch); worked example A of the reference supports it and is not duplicated below.
To register as `pending` (the register is a shared file, not edited here):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-METRIQUES-TEMPS-02 | CV-METRIQUES-TEMPS | Predict how MOTA, IDF1 and HOTA move when the same tracker output and ground truth are evaluated at half the frame rate, and explain why MOTA's identity term loses weight | No card trains the frame-rate dependence of MOT metrics, a common cause of incomparable benchmark numbers | Reasoning; Properties, example C | 1 card, 3 criteria (FN/FP per frame versus switches per event; MOTA moves toward detection quality; IDF1 and AssA count detections) | [HOTA §9.1, problem 7](https://arxiv.org/abs/2009.07736); [CLEAR MOT §2.2, eq. 2](https://doi.org/10.1155/2008/246309) |
| P-CV-METRIQUES-TEMPS-03 | CV-METRIQUES-TEMPS | Diagnose why an in-house HOTA differs from TrackEval on the same files: preprocessing of distractors, threshold set, per-frame versus per-threshold matching, sequence and class combination | Card 005 covers trajectory evaluators only; no card trains reconciling MOT evaluators | Diagnosis; Cost and implementation | 1 card, 3–4 criteria | [TrackEval `hota.py` L66–L173 and `mot_challenge_2d_box.py` L302–L329](https://github.com/JonathonLuiten/TrackEval/tree/12c8791b303e0a0b50f753af204249e622d0281a/trackeval); [HOTA §5](https://arxiv.org/abs/2009.07736) |

No defective question was found. The front of CV-METRIQUES-TEMPS-002 contains the formula
it asks about, which is intended: the card tests the order of operations.

## Sources

Scientific sources, opened at the passages listed:

- Bernardin and Stiefelhagen, CLEAR MOT, EURASIP JIVP 2008,
  [DOI](https://doi.org/10.1155/2008/246309); PDF from Springer, extracted with
  `pdftotext`: §2.1.3, §2.2 eqs. 1–5 and Fig. 3, §4.
- Ristani et al., [arXiv 1609.01775v2](https://arxiv.org/abs/1609.01775) (PDF text):
  §3.3 eqs. 3–5, §3.4 eqs. 6–11, §3.5.
- Luiten et al., HOTA, [arXiv HTML v2](https://arxiv.org/html/2009.07736v2): §3, §4.1–4.3,
  §5 eqs. 10–16, §6 eqs. 17–21, §9.1 and §9.2 problem headings. The PDF v5 URL returned
  HTTP 404; the HTML version was used.
- Sturm et al. 2012, [TUM RGB-D benchmark](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf)
  (PDF text): §VI, §VII-A eqs. 1–3, §VII-B eqs. 4–5.
- Zhang and Scaramuzza 2018, [IROS tutorial](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf)
  (PDF text): §III-A, §III-C eq. 13 and Table I, §IV-A, §IV-B eqs. 25–26 and Table II.

Implementation sources:

- [TrackEval at `12c8791`](https://github.com/JonathonLuiten/TrackEval/tree/12c8791b303e0a0b50f753af204249e622d0281a)
  (head of the official repository, 2022-11-29, GitHub API): `metrics/clear.py` (186
  lines), `metrics/identity.py` (135 lines), `metrics/hota.py` (203 lines), read in full;
  `datasets/mot_challenge_2d_box.py` L295–L440.
- [TUM RGB-D tools page](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools), usage
  text of `associate.py`, `evaluate_ate.py` and `evaluate_rpe.py` (unversioned; accessed
  2026-11-14). The scripts themselves were not downloaded: the old SVN URL returned 404.
- [nuScenes devkit detection README at `b40adc4`](https://github.com/nutonomy/nuscenes-devkit/blob/b40adc467b919192899405d9b77871afee8efa07/python-sdk/nuscenes/eval/detection/README.md):
  "Average Precision metric", "True Positive metrics", "nuScenes detection score".
- [NumPy 1.24.0 release notes](https://github.com/numpy/numpy/blob/v1.24.0/doc/source/release/1.24.0-notes.rst).

Not executed: TrackEval, the TUM scripts, any tracker or estimator. Context7 was not
available (scope record). Not re-verified: Umeyama's paper (cited through Zhang and
Scaramuzza Alg. 1) and Horn's method (cited through Sturm et al.).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (an intermediate run flagged two lines of this note that started with a bracketed citation followed by a colon; reflowed) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/132-tracking-trajectoires.py` | 14 checks passed |
| `git diff --check -- vault/130-evaluation-fiabilite/ …/checks/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/132-tracking-trajectoires.md` | 5 cards, 260–399 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 41 protected card lines identical; front matter identical except `revision: 6` → `7`; H1 and 8 per-card headings unchanged; `$$` and fences balanced |

No evaluator, tracker or estimator was run; the proposed baseline and variation are
protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering is unverified. Agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-METRIQUES-TEMPS revision 7, CV-METRIQUES-TEMPS-001 to 005, corrections listed above,
Agent Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-METRIQUES-TEMPS-02, P-CV-METRIQUES-TEMPS-03).
