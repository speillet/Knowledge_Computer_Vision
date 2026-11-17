# Review — Evaluating identities, trajectories and 3D localization — 2026-11-17

## Overview

6 cards audited and clarified in `clarifier` mode (pilot of the pass). Highest severity per
card before correction, accuracy and clarity together: 0 blocking, 0 important, 6 minor
(every card used undefined acronyms or skipped steps; CV-METRIQUES-TEMPS-001 also carried
an unsupported attribution), 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 9 → 10.

Clarity metrics (`checks/clarity_metrics.py`), before → after: rubrics 9, 7, 9, 7, 7, 5
→ 6 for every card; undefined acronyms in all 6 cards → 0 real ones (the remaining flags,
TUM and GT, are expanded by apposition, which the heuristic does not detect). Lexical
words: 580 → 652, 399 → 443, 554 → 571, 349 → 421, 375 → 394, 608 → 738. Answers grew
because steps and definitions were added, while 36 old paragraphs were moved to the
reference or rewritten as steps (table below).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Numbers recomputed; HOTA §9.1 problem 6 and Ristani §3.3 confirmed. "Between 1 and $n-1$ errors" attributed to Ristani §3.1, §3.3: a project deduction from their Fig. 1 | Evaluation: separates detection from identity | 1 criterion, unchanged; 652 words | AP, MOTA, IDF1, IDSW, MODA, GT undefined; IDF1 $26/32$ given without its formula; 9 rubrics with three overlapping paragraphs | Minor | Key terms; 7 numbered steps from per-frame counts to the relabelled replay; attribution removed from the card and labelled in the reference |
| CV-METRIQUES-TEMPS-002 | Counterexample recomputed; Cauchy–Schwarz direction checked on 2000 random 19-threshold profiles | Reasoning: order of aggregation | 1 criterion, reworded; 443 words | DetA, AssA, HOTA, $\alpha$ undefined on the card; the angle reading and the inequality interrupted the reasoning | Minor | Question expands HOTA, DetA, AssA; counterexample in 5 steps; inequality kept as one step, its proof left in the reference |
| CV-METRIQUES-TEMPS-003 | Zhang and Scaramuzza §III-A, eqs. 11–12 and the monocular and stereo groups confirmed; worked example B recomputed | Evaluation: alignment group from observability | 1 criterion, reworded; 571 words | VIO, ATE, RPE, DoF, IMU, RMS, SE(3) undefined; ATE 0.063 m given without the RMS of the offsets | Minor | Key terms; 7 steps (4-DoF argument, offsets, RMS $\sqrt{110/11}$, residuals, Sim(3) scale, tilt, RPE) |
| CV-METRIQUES-TEMPS-004 | Sturm et al. §VII-A, VII-B (unchanged claims, 2026-11-14 report); frame cancellation recomputed numerically | Comparison: global consistency versus drift | 1 criterion, reworded; 421 words | ATE, RPE, SE(3) undefined; why RPE needs no alignment was asserted, not shown | Minor | Key terms; 6 steps with the cancellation of $S$ written out |
| CV-METRIQUES-TEMPS-005 | Unchanged claims (2026-11-14 report) | Diagnosis: reconciling evaluators | 6 criteria, unchanged; 394 words | TUM, RMSE, ATE, RPE undefined; checks scattered over four paragraphs | Minor | Key terms; one 7-step decision procedure in pipeline order |
| CV-METRIQUES-TEMPS-006 | Unchanged claims (2026-11-09 report); values recomputed | Reasoning: frame-based identity cost | 4 criteria, unchanged in substance, derivations moved to steps; 738 words | IoU, IDTP, IDFN, IDFP, IDP, IDR, CLEAR MOT undefined; the Y mapping choice shown only in an explanation paragraph | Minor | Question expands acronyms; Key terms; 8 steps |

## Questions and expected answers changed

Questions changed only to expand acronyms: CV-METRIQUES-TEMPS-001 (AP), -002 (HOTA, DetA,
AssA), -003 (VIO), -004 (ATE, RPE) and -006 (IoU, IDTP, IDFN, IDFP, IDF1, MOTA).
CV-METRIQUES-TEMPS-005 is unchanged. Expected answers, old → new:

- **001**: "Boxes/classes can be identical while IDs are exchanged or fragmented; AP does
  not measure this continuity." → "Boxes and classes can be identical in every frame
  while the identities (IDs) are exchanged or fragmented over time; AP (average
  precision) scores each frame independently and does not measure this continuity."
- **002**: "The reference calculates the root of the product at each threshold and then
  averages these scores; the two operations do not commute in general." → "HOTA takes
  the square root of DetA × AssA at each localization threshold, then averages these
  per-threshold scores; averaging DetA and AssA first and taking the root afterwards
  changes the result in general, because the two operations do not commute."
- **003**: "Adjusts the scale and can therefore hide a metric error that the system had
  to avoid." → "A Sim(3) alignment fits a scale factor as well as a rotation and a
  translation, so it can cancel a metric scale error that the VIO had to avoid; the
  score then no longer tests the metric scale."
- **004**: "ATE evaluates a trajectory after alignment; RPE evaluates relative
  displacements at defined intervals." → "No. ATE evaluates the whole trajectory after
  one global alignment; RPE evaluates the relative displacements over a defined
  interval."
- **006**: the same four criteria (global one-to-one mapping and Y's choice of ID 3; the
  counts and IDF1 of X and Y; the cost set by the shorter piece,
  $1-\min(a,b)/20$; one switch and MOTA 0.95 for both). The intermediate formulas
  moved to the step list, and the clause "equivalently, the minimum IDFN + IDFP" to
  step 5.

## Reference findings and changes

- Worked example A held two constructed examples of the same point: "Duration of a
  fragment" (10 frames, from the 2026-11-09 pass) and "Events versus frames" (8 frames,
  from the 2026-11-16 pass, written on the same day without seeing the other). They are
  merged into one progressive example, **One fragment: events versus frames**, built on
  the general formula $\mathrm{IDF1}=1-\min(a,b)/(2n)$ and $\mathrm{MOTA}=1-1/(2n)$ for
  $n$ frames; both earlier cases are its instances. The 8-frame figure is kept.
- The event count "between 1 and $n-1$ errors" is now labelled a project deduction;
  Ristani et al. are cited for their Fig. 1 (one against seven fragmentations, 33% each)
  and §3.3.
- New `## Going further` section with the card paragraphs not yet in the reference
  (001 replay, 002 practical consequence, 003 protocol, 004 time scales and evaluation,
  006 minimum-cost mapping). Revision 9 → 10.

## Paragraphs that left the cards

`checks/nothing_lost.py` lists 36 removed paragraphs: 18 found in the reference with a
ratio of 0.99 or 1.00, and 18 below 0.9, each checked by hand:

| Card | Removed paragraph | Where its content is now |
| --- | --- | --- |
| 001 | Reading the diagram | Step by step, steps 1–5, with the same figure |
| 001 | Further explanation ("identical sequence protocol") | Limits, first sentence |
| 001 | Events versus frames | Step 6; the citations in the reference's merged example |
| 002 | Old expected answer | Reworded expected answer (above) |
| 002 | Further explanation (conventions, ignore rules) | Limits |
| 002 | Analytical counterexample | Step by step, steps 1–4 |
| 003 | Old expected answer | Reworded expected answer (above) |
| 003 | Further explanation (gauge freedoms, tilt) | New Further explanation and step 6 |
| 003 | Example of hidden error | New Further explanation; "correct for another, scale-free task" in Limits (monocular case) |
| 003 | Why 4 DoF | Step 1; reference, after worked example B |
| 003 | Constructed example | Steps 2–7; reference, worked example B |
| 003 | Diagnosis | Limits; reference failure table and Going further |
| 004 | Old expected answer | Reworded expected answer (above) |
| 004 | Further explanation (interval, aggregation, failures) | Step 3 and Limits; the aggregation (RMSE) in the reference's Mathematics section |
| 005 | Further explanation (replay, TUM mean versus RMSE) | Decision procedure, steps 5 and 7 |
| 006 | Old expected answer | Condensed expected answer and steps 3–8 |
| 006 | Duration, not timing or event count | Limits; reference merged example |
| 006 | Opposite design choices | Further explanation and Limits; reference merged example |

## Proposals

- **P-CV-METRIQUES-TEMPS-04** (new, bridge card): compute DetA, AssA and HOTA at one
  threshold for a single identity switch. Card 002 reasons about aggregating AssA, but no
  card teaches how AssA is computed from $\mathcal A(c)=n_{gp}/(n_g+n_p-n_{gp})$.
- P-CV-METRIQUES-TEMPS-02 and -03 remain pending.

The prerequisites section already links every notion the cards rely on: box IoU and AP
(CV-IOU-AP), SE(3) poses (CV-SE3), point-set alignment (CV-ICP) and gauge freedoms
(CV-VIO, card CV-VIO-003). No change to `prerequis` was needed.

## Sources

Read on 2026-11-17: Ristani et al. 2016 (arXiv 1609.01775 PDF, `pdftotext`), §3.1 and
Fig. 1, §3.3; Luiten et al. (arXiv HTML v2), §9.1, problems 5 and 6; Zhang and Scaramuzza
2018 (IROS PDF, `pdftotext`), §III-A eqs. 11–12 and the monocular, stereo and inertial
groups; TrackEval `clear.py` at `12c8791`, L60–L100. Claims of cards 004, 005 and 006
not revalidated beyond their 2026-11-14 and 2026-11-09 reports. Context7 is unavailable
in this session.

## Checks and limitations

- `python3 -I docs/revues/2026-11-17-clarity/checks/132-tracking-trajectoires.py`:
  6 checks pass (general formula for $n=8$ and $n=10$, every value of the six cards,
  inequality direction, frame cancellation of RPE). The scripts of 2026-11-14 (14),
  2026-11-09 (8) and 2026-11-16 (7) still pass.
- `checks/protected_fields.py`: 0 protected field changed; question and expected-answer
  changes as listed above.
- `check_vault.py`, `sync_catalog.py --check`, `learning_path.py`, unit tests (71) and
  the inventory comparison pass, with no ID or Anki identity change.
- The Anki conversion of CV-METRIQUES-TEMPS-001 was inspected: key terms and steps become
  HTML lists. Rendering on AnkiDroid and in Obsidian is not verified, and whether the
  learner finds the cards clearer is for the learner to judge. Export status: **to
  republish with `paquet-anki`**.
