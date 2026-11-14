# Review — SORT — multi-object tracking with motion and association — 2026-11-14

## Overview

8 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 2 important, 6 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

Tracking is a learner priority. The note now derives the behavior of the pinned
implementation (noise settings, gains, overlap budget, life-cycle trace) instead of
describing SORT generically. Appearance and low-score association stay in
[CV-ASSOCIATION](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md);
metric definitions stay in
[CV-METRIQUES-TEMPS](../../../vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | Predict, associate by IoU and assignment, correct, manage births and deaths; Kalman does not verify identity: confirmed (SORT §§3.2–3.4; `sort.py` L210–L253). "the assignment chooses the torques" (*couples*, pairs) | Understanding: separating responsibilities of filter, association and life cycle | 2 expected criteria; 384 → 393 lexical words | Expected answer "associate boxes with detections ... correct associates" ambiguous | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections and lines |
| CV-SORT-002 | State $[u,v,s,r,\dot u,\dot v,\dot s]$, measurement $[u,v,s,r]$, constant $r$, per-frame step: confirmed (§3.2; L94–L117). Blocking error "gear for speed" mistranslated *le rapport pour une vitesse* (the ratio for a velocity): the misconception being tested was unreadable | Reasoning: units and frame-rate dependence | 3 expected criteria; 414 → 418 lexical words | "**check**" label; "Two frames consecutive to ten frames per second" | Important | Blocking error restored; language fixes; Source line cites §3.2 and the tracker class |
| CV-SORT-003 | $K=25/34$, $u^+=107.35$ px, $P^+=6.62$ px², 102 px with $R=100$: confirmed by recomputation (checks/111-sort.py, check 12). Decimal commas "107,35" and "6,62" in the expected answer and explanation; "it also reduces its uncertainty" lost the comparative (*moins*) | Reasoning: weighting of prediction and measurement | 2 expected criteria; 365 → 370 lexical words | Source line cited only L94 | Minor | Decimal fix in the expected answer; language fixes; Source line cites the noise settings and filterpy defaults |
| CV-SORT-004 | Deletion when `time_since_update > max_age`; output only for tracks updated this frame meeting the hit condition: confirmed (L141–L145, L243–L250). Missing condition: `hit_streak` restarts after a miss, so a re-associated track is withheld for `min_hits` frames (trace, checks/111-sort.py, checks 8–9) | Algorithm: memory versus output | 3 expected criteria; 390 → 438 lexical words | "issues the tracks updates", "exception to global boot" | Important | Expected answer language fix; one sentence added to the explanation on the restart of `hit_streak`; Source line cites the lines |
| CV-SORT-005 | Diagonal 0.90 beats crossed 0.62, rejection leaves one pair: confirmed (check 10; L154–L196). Decimal commas "0,90", "0,62" in the expected answer; "the crosses" | Practice: objective solved by maximize-then-reject | 3 expected criteria; 392 → 390 lexical words | Consistent with the code's shortcut path | Minor | Decimal and language fix of the expected answer; Source line given exact lines |
| CV-SORT-006 | Discriminating missed detection, expiry and wrong association from a per-frame trace: consistent with §§3.3–3.4 and the code. "false holds of tracks", "tracks competitors", "Discriminant Chronology" | Diagnosis: first divergence in a replayed trace | 2 expected criteria; 383 → 389 lexical words | Expected answer "track, frame by frame" meant *trace* | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-SORT-007 | Flow, AP and ReID each insufficient: consistent with SORT Table 1 (detector swap) and HOTA §§4–6. Expected answer "The stream describes point/pixel displacements" (*flot*, optical flow); "I/O" | Comparison: output contracts of temporal tasks | 2 expected criteria; 373 → 375 lexical words | Aligned with CV-FLOT terminology | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-SORT-008 | Tracker speed is not system latency: confirmed (§4.3 reports 260 Hz for the tracking component on one i7 core). "Ancillary observations", "do not announce tracking performance with the only time of assignment" | Evaluation: end-to-end timing and identity metrics | 2 expected criteria; 378 → 380 lexical words | Appendix reference answer aligned | Minor | Language fixes; Source line cites §4.3 |

Expected-answer changes (sourced or meaning-restoring language fixes):

- CV-SORT-001: "predict tracks with Kalman, associate boxes with detections by IoU and
  assignment, correct associates, and then manage creations and disappearances. The
  association chooses the measure of a track; …" → "Predict the tracks with Kalman,
  associate the predicted boxes with detections by IoU and assignment, correct the
  associated tracks, then manage creations and deletions. The association chooses the
  measurement of a track; …".
- CV-SORT-003: "≈107,35 px" → "≈107.35 px".
- CV-SORT-004: "deletion occurs … A missed frame can leave the track memorized; the second
  one deletes it. The reference only issues the tracks updates in the frame and meets its
  hit conditions." → "Deletion occurs … One missed frame can leave the track in memory; the
  second consecutive one deletes it. The reference outputs only tracks updated in the
  current frame that meet its hit condition."
- CV-SORT-005: "the diagonal gives 0,90, against 0,62 for the crosses … After zero is
  rejected, there is a pair left. The two associations crossed each would have exceeded
  the threshold." → "The diagonal gives 0.90, against 0.62 for the crossed pairs … After the
  zero is rejected, one pair remains. Each of the two crossed associations would have
  exceeded the threshold."
- CV-SORT-006: "track, frame by frame, detections, … Check first if the box exists, if the
  track was still memorized, and if an eligible pair was chosen." → "Trace, frame by frame,
  the detections, … Check first whether the box exists, whether the track was still in
  memory, and whether an admissible pair was chosen."
- CV-SORT-007: "The stream describes point/pixel displacements; the AP … the ReID …" →
  "Optical flow describes point or pixel displacements; AP … ReID …".
- CV-SORT-008: initial "measure" capitalized only.

Explanation added (CV-SORT-004, condition revealed by the enriched reference): "Because
`hit_streak` restarts when a track resumes after a miss, a re-associated track is withheld
again until it has `min_hits` consecutive updates: with the defaults, one missed detection
removes the box from the output for three frames." Source: `sort.py` L141–L142, L245;
trace recomputed by checks/111-sort.py.

Protected fields not edited (`Objective:` lines in lower case or awkward English):
CV-SORT-002 "interpret a state and its units", CV-SORT-003 "interpret the weight of a
measure" (proposed "Interpret the weight of a measurement"), CV-SORT-004 "Distinguish
between memory and transmission" (proposed "Distinguish retention from output"),
CV-SORT-008 "define a complete performance measure". No question is defective.

## Reference findings

Claims of revision 8 checked against their passages:

- State, units, constant-velocity assumption: confirmed (§3.2). The note said speeds are
  "per frame in the reference": confirmed.
- Default `max_age=1`, `min_hits=3`, `iou_threshold=0.3`; deletion rule; output condition;
  maximize-then-reject with a shortcut: confirmed (L154–L253).
- "the reference does not make a separate association by class": confirmed (no class field
  in the input contract, L213).
- Analytical counterexample and scalar example: arithmetic confirmed; written with French
  decimal commas.
- No scientific error was found. The body was shallow on noise settings, life-cycle timing,
  evaluation protocol and failure remedies, and contained mistranslations ("trackss",
  "Connexions", "Proposed Variation Not Performed on Video", "report" for the aspect ratio).

New claims verified for revision 9: detector and 50% threshold, Table 1 MOTA 15.1 (ACF) and
34.0 (FrRCNN VGG16) (§3.1); occluder favored by IoU scale (§3.3); probation, zero initial
velocity with large covariance, $T_{Lost}=1$ and its two reasons, new identity on
reappearance (§3.4); tuning on the training split (§4); MOTChallenge 2015 test set with 11
sequences, 50% overlap for true positives, metric list (§4, §4.1, §4.2, reference [6]);
Table 2 MOTA 33.4, MOTP 72.1, 1,001 ID switches versus MDP 30.3 and 680; 260 Hz on one core of
an i7 2.5 GHz (§4.3); MOTA, IDF1 and HOTA definitions and the detection bias of MOTA (HOTA
§4.1, §4.2, §5, §6, §9.1).

Implementation observations recorded in the note (FR-036): noise settings
$R=\mathrm{diag}(1,1,10,10)$, $P_0=\mathrm{diag}(10,10,10,10,10^4,10^4,10^4)$,
$Q=\mathrm{diag}(1,1,1,1,0.01,0.01,10^{-4})$ built from filterpy's identity defaults; the
`>` (shortcut) versus `<` (filter) asymmetry at the IoU threshold; the class-level ID counter
shared across `Sort` instances; the area-velocity guard; `lap.lapjv` or SciPy as solver.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 918 → 3,037.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Developed (short) | Developed | Input and output arrays with units, positive IDs, score and class ignored, frame time base, detector contract (§3.1), pipeline role and confirmation delay |
| Intuition | Shallow | Developed | Mechanism in plain terms; occluder favored by IoU scale (§3.3); constructed crossing illustration; existing diagram kept |
| Prerequisites | Developed | Developed | CV-FUSION, NMS and CV-SOT links added |
| Assumptions | Shallow | Developed | Constant velocity independent of camera motion, overlap budget, detector quality (Table 1), no appearance, unobserved velocities and constant ratio; degenerate cases from the code |
| Procedure | Developed (list) | Developed | Pseudocode of `Sort.update` with the shortcut, rejection, probation and deletion; purpose of each step |
| Mathematics | Developed (state, KF) | Developed | Box recovery, actual $R$, $P_0$, $Q$ with units; association objective; worked examples A (gains), B (IoU budget, zero initial velocity, frame rate), C (life-cycle trace) |
| Parameters | Shallow | Developed | Parameter table with paper and code values, interactions; tuning approach |
| Properties | Shallow | Developed | Per-frame optimality, conditional filter optimality, identity memory, frame-rate dependence, speed scope |
| Cost and implementation | Shallow | Developed | Cost with variables and solver; reported speed with hardware; implementation contract (threshold asymmetry, ID counter, output rule, solver choice); execution status |
| Evaluation | Shallow | Developed | Paper protocol and Table 2; MOTA bias reading with HOTA §9.1; proposed baseline and frame-subsampling variation with confound control; measurement limits |
| Failure modes and diagnosis | Developed (3-row table, no remedy) | Developed | Eight-row table with discriminating checks and conditional remedies |
| Alternatives and sources | Shallow | Developed | Conditional choices (SORT, DeepSORT, ByteTrack, OC-SORT, SOT); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by [`checks/111-sort.py`](checks/111-sort.py)
(14 assertions): noise settings, first and steady-state gains (0.9999/0.9988; 0.653/0.059;
area 0.277/0.0027; ratio 0.270), IoU budget $0.538\,w$, zero-velocity failure (IoU 0.2),
frame-rate halving (0.43 → 0.11), life-cycle traces (first output at frame 13; gap 20–22;
deletion and ID 2 at 25), the counterexample, the threshold asymmetry, the scalar update,
MOTA error ratio 39.9 and lifetime durations.

## Applied corrections

- [Reference](../../../vault/110-tracking-association/references/111-sort.md), revision 8 →
  9: body rewritten and deepened; decimal commas removed; mistranslations fixed in the
  appendices ("Question of work", "Reference Response", "Example of liability" → "Example of
  failure", "torques" → "pairs", "Ancillary observations", "Causal Order", "report" → "aspect
  ratio", "Physical Duration and Issue" → "Physical duration and output", "An issue can
  introduce fictitious rows" → "A formulation can add dummy rows", "Discriminant Chronology"
  → "Discriminating timeline", "trackss", "false supports" → "false track continuations",
  "Spatial Invariance at IDs" → "Invariance of per-frame scores to IDs", "seniority" →
  "frame age", "the front's" → "the question's"). Sources split; closing provenance line
  replaced. Front matter unchanged except `revision`; H1, per-card headings, image and
  reference-style link definitions kept.
- [Cards](../../../vault/110-tracking-association/111-sort.md): expected answers corrected
  as quoted above; explanation of CV-SORT-004 extended; all shared paragraphs aligned word
  for word with the appendices; other language fixes include "gear for speed" → "the ratio
  $r$ for a velocity", "Why Units Matter" → "Why units matter", "**check**" →
  "**Discriminating check**", "Weighting Intuition", "Chronology to explain" → "Timeline to
  explain", "a detection feedback" → "a returning detection", "a correct appearance may miss
  detection" → "a good appearance model cannot recover a missed detection". Source lines
  cite exact sections and lines. IDs, questions, objectives, families, tags and target deck
  unchanged.

Other subjects: no other card repeats a corrected SORT claim (`rg` for `max_age`, "107,35",
"0,62" outside this topic).

## Proposals

To register as `pending` in the [proposal register](../propositions.md):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SORT-01 | CV-SORT | A small object moving fast is detected in every frame but never gets a stable ID in SORT: explain the zero initial velocity and the IoU budget, and give the discriminating check | No card trains the relation between per-frame displacement, box size and the IoU threshold, a frequent field failure | Diagnosis; worked example B | 1 card, 3 criteria ($d\le0.538w$ at 0.3; zero velocity at birth; check displacement/width) | [Bewley et al. 2016, §3.3–3.4](https://arxiv.org/abs/1602.00763); [sort.py L154–L196](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L154-L196) |
| P-CV-SORT-02 | CV-SORT | Design the life cycle of a SORT-based counting system (lifetime in seconds, probation, output of predicted boxes) for a given frame rate and occlusion distribution | The "design" family is absent; life-cycle parameters are tested only for the default code | Design; Parameters and tuning | 1 card, 3–4 criteria | [Bewley et al. 2016, §3.4](https://arxiv.org/abs/1602.00763); [sort.py L199–L253](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L199-L253) |

## Sources

Scientific sources, opened at the passages listed:

- Bewley et al., SORT, [arXiv 1602.00763v2 PDF](https://arxiv.org/abs/1602.00763): abstract,
  §3, §3.1 (Table 1), §3.2, §3.3, §3.4, §4, §4.1, §4.2 (Table 2), §4.3, reference [6].
- Luiten et al., HOTA, [arXiv 2009.07736v2](https://arxiv.org/abs/2009.07736): §4.1 eq. 2,
  §4.2 eq. 4, §5 eqs. 10–14 and α range, §6, §9.1.

Implementation sources:

- [abewley/sort at 2236dff, `sort.py`](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py): L1–L275.
- [rlabbe/filterpy at 5df4e09, `filterpy/kalman/kalman_filter.py`](https://github.com/rlabbe/filterpy/blob/5df4e095fac07684a05c495bd72d3424f7c68c9c/filterpy/kalman/kalman_filter.py): L388–L403.

Not opened: the CLEAR MOT paper itself (Bernardin and Stiefelhagen 2008); MOTA is quoted
from HOTA §4.1. No access failure. Context7 was not available.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/111-sort.py` | 14 checks passed |
| `git diff --check` on the two vault files | No whitespace error |
| `inventaire_cartes.py vault/110-tracking-association/111-sort.md` | 8 cards, 370–438 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 8` → `9`; H1 and per-card headings unchanged; `$$` and fences balanced |

SORT was not run: the life-cycle and gain examples re-implement the pinned code's rules in
plain Python and are not executions of `sort.py`. The proposed variation is a protocol.
Rendering in Obsidian and AnkiDroid is unverified. Agent self-review only. Export status:
**to republish with `paquet-anki`**.

Shared files not edited, entries needed: `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-SORT revision 9, CV-SORT-001 to 008, corrections above, to republish with
`paquet-anki`) and the proposal register (P-CV-SORT-01, P-CV-SORT-02).
