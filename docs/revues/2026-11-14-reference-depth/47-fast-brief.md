# Review — FAST and BRIEF — detecting corners and describing their neighborhoods — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 5 to revision 6. Highest severity per card before correction:
0 blocking, 2 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The note covers the two building blocks separately. ORB's orientation, pyramid and
learned test pairs are linked to [CV-ORB](../../../vault/40-features-matching/references/42-orb.md);
gradient corner scores to [CV-CORNERS](../../../vault/40-features-matching/references/46-harris-shi-tomasi.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FAST-BRIEF-001 | Contiguous arc brighter than $I_p+t$ or darker than $I_p-t$: confirmed (Rosten 2006 §2.1, eq. 5). Expected answer said "removing maxima selects neighboring responses", the opposite of non-maximum suppression (§2.3). Missing practice condition: OpenCV 4.13's `TYPE_7_12` and `TYPE_5_8` share a 16-pixel pretest that rejects valid arcs (`fast.cpp` L216–L231; probe with 4.11.0) | Algorithm: the segment test and its post-processing | 2 expected criteria; 388 → 473 lexical words | Aligned with reference examples A and B | Important | Meaning-restoring fix of the expected answer; language fixes; implementation caveat added; Source line given exact passages |
| CV-FAST-BRIEF-002 | Hamming distance 2 for 101101 and 100001: recomputed. Bits as smoothed intensity comparisons: confirmed (Calonder §3, eqs. 1–2). "The XOR is worth one", "return the bit", "Hamming's distance does not tell what disagreements arise from" | Reasoning: correct metric for binary codes | 2 expected criteria; 362 → 364 lexical words | Consistent with reference example C | Minor | Language fixes; Source line given exact passages |
| CV-FAST-BRIEF-003 | ORB adds pyramid, orientation and selected tests: confirmed; test selection offline by greedy search on ~300k PASCAL 2006 keypoints (Rublee et al. §4.3). "brick", "Chain to rebuild", "in a ORB assembly", "an online trained network on the observed part" | Comparison: separates components from the assembled pipeline | 3 expected criteria; 369 → 354 lexical words | Consistent with CV-ORB | Minor | Language fixes; Source line now cites Calonder §3–§4 and Rublee §3.2, §4.3 instead of an unreadable tutorial |
| CV-FAST-BRIEF-004 | Fixed BRIEF pattern does not follow rotation: confirmed; measured tolerance of 10–15° then "a precipitous drop", and O-BRIEF shows rotation behavior depends on the orientation estimator (Calonder §4). Expected answer ended with "check the orientation/normalization of patches with constant detector", unclear; "before and after delivery" for *rotation* | Diagnosis: isolates descriptor from detector | 2 expected criteria; 383 → 416 lexical words | Aligned with reference example D and the controlled variation | Important | Meaning-restoring fix of the expected answer; measured evidence added; language fixes; Source line given exact passages |
| CV-FAST-BRIEF-005 | Compare full pipelines, not detector speed: consistent with Rosten 2006 Table 1 and Calonder §4 protocols. RANSAC numbers 72 and 1,177: recomputed. "prints" for samples, "stop, degeneration and repetition variants", "promise of historic speed" | Evaluation: end-to-end replacement decision | 3 expected criteria; 371 → 370 lexical words | Consistent with the reference evaluation section | Minor | Language fixes; Source line given exact passages |

Expected-answer changes (meaning-restoring language fixes):

- CV-FAST-BRIEF-001: "removing maxima selects neighboring responses." →
  "non-maximum suppression keeps the locally strongest of adjacent responses."
- CV-FAST-BRIEF-004: "check the orientation/normalization of patches with constant
  detector." → "Check the orientation normalization of the patches with the detector
  held fixed."

## Reference findings

Claims of revision 5 checked against their passages:

- Segment test on a 16-pixel circle, $n$ contiguous pixels brighter or darker by $t$,
  FAST-9 versus the original 12-of-16 test, decision tree and non-maximum
  suppression: confirmed (Rosten 2006 §§2.1–2.3).
- BRIEF bit $\mathbf1[I_s(x)<I_s(y)]$ on a smoothed patch and Hamming matching:
  confirmed (Calonder §3, eqs. 1–2; §1).
- "A fixed BRIEF pattern is not invariant to any rotation or scale": imprecise;
  BRIEF is not rotation-invariant but tolerated about 10–15° in the authors' test
  (§4, Orientation Sensitivity). Rewritten.
- "OpenCV 4.13 API verified with Context7": not reproducible in this session;
  replaced by citations of the 4.13.0 sources.
- Machine-translation defects that obscured meaning: "The shaft avoids unnecessary
  testing" (the decision *tree*), "Fine Noise", "removing non-maxima avoids clusters of
  answers" (responses), "Question of work", "Reference Response", "Logical example"
  with "very clear neighbors" (bright), "deletion of maxima check then local
  redundancy", "material results".

New claims verified for revision 6 (main ones):

- Rosten and Drummond 2006: motivation (§1); patch detectors and blurred images
  (§1.1); $n=12$ compass pretest and four weaknesses (§2.1); eqs. 5–7, ID3 tree and
  its approximation of the segment test (§2.2); score $V$, eq. 8 (§2.3); Table 1 and
  2.26 questions per pixel (§2.4); repeatability on 3-D scenes (§3); FAST-9 best,
  above about 200 corners per frame, noise sensitivity (§4); one-pixel lines and
  threshold dependence (§5).
- Rosten, Porter and Drummond (arXiv 0810.2434v1): pretest weakness for $n<12$
  (§III-A), exact tree with all $3^{16}$ rings (§III-B), score as maximum $t$ and
  $3\times3$ suppression (§III-C), Table IV.
- Calonder et al. 2010: smoothing, value 2 in a $9\times9$ window, "essential" on hard
  pairs (§3.1, Fig. 1); five sampling geometries, G II with $\sigma^2=S^2/25$ (§3.2);
  non-matching distances centered near 128 (§3.3); recognition-rate protocol and its
  caveat, Graffiti and monochrome areas, upright versus oriented descriptors, 10–15°
  tolerance, O-BRIEF, saturation beyond ~200 tests, timing table (§4).
- Rublee et al. 2011: rBRIEF learned by greedy search on ~300k keypoints from PASCAL
  2006 over 205,590 tests in a $31\times31$ patch (§4.3) — used for card 003 and in
  [CV-ORB](../../../vault/40-features-matching/references/42-orb.md).

Disagreements between papers and OpenCV 4.13 implementations (FR-036):

| Aspect | Paper | OpenCV 4.13.0 |
| --- | --- | --- |
| Inequalities | $I_{p\to x}\ge I_p+t$ (brighter), $\le I_p-t$ (darker) (Rosten 2006 eq. 5) | Strict `>` and `<` (`fast.cpp` L80) |
| Detector | Learned ID3 decision tree (§2.2) | Direct segment test with a hand-written pretest (`fast.cpp` L212–L270) |
| Suppression score | Sum of absolute differences, eq. 8 (2006); maximum $t$ (2010 §III-C) | Maximum passing threshold (`fast_score.cpp` L83–L209) |
| Variants | Only the 16-pixel circle is defined (2006 §2.1) | `TYPE_7_12` and `TYPE_5_8` described as "as defined in the paper" (`features2d.hpp` L605–L624); they share the 16-pixel pretest, which rejects most valid 7-of-12 arcs and all valid 5-of-8 arcs (L216–L231) |
| BRIEF smoothing | Gaussian, value 2, $9\times9$ window (§3.1) | $9\times9$ box sums from an integral image (`brief.cpp` L99–L119, L285) |
| BRIEF border | Not specified | Keypoints within 28 px of the border are removed (`brief.cpp` L288) |

Executed evidence for the pretest defect: a probe with the installed OpenCV 4.11.0
Python package (whose `FAST_t` logic differs from 4.13.0 only by loop unrolling and
hardware-abstraction hooks, checked by `diff` of `fast.cpp` and `fast_score.cpp` at
both tags) placed one bright arc of the required length on synthetic rings,
threshold 10, suppression off. `TYPE_9_16` detected all 16 starting positions;
`TYPE_7_12` detected 4 of 12 (starts 0, 9, 10, 11); `TYPE_5_8` detected none, and
detected a fully bright ring. A ring exactly $t$ brighter was not detected and
$t+1$ was. The probe script lives outside the repository; checks/47-fast-brief.py
reproduces the pretest logic analytically (checks 3–5). A Stack Overflow question
reports the same symptom for `TYPE_5_8`; no upstream fix was found in this pass.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 487 → 4,359. The body
includes the Mermaid diagram, the pseudocode, three tables and four worked examples.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task from both papers; FAST and BRIEF input and output contracts in OpenCV (types, `KeyPoint` fields, border margins, descriptor matrix, distance range); pipeline roles and downstream RANSAC cost |
| Intuition | Shallow | Developed | Arc versus half-circle intuition; BRIEF as yes/no questions with chance agreement; constructed arrow illustration; Mermaid data flow |
| Prerequisites | Shallow (one link) | Developed | Links by mechanism to CV-CORNERS, CV-FILTRES, CV-FLANN, CV-MATCHING, CV-HOMOGRAPHIE, CV-ORB |
| Assumptions | Shallow | Developed | Contrast threshold and blur, noise, no scale or orientation (10–15° tolerance), shared patch frame, texture; observability; degenerate cases (one-pixel lines, adjacent detections, unstable bits, border) |
| Procedure | Shallow (two sentences) | Developed | Pseudocode for FAST, BRIEF and matching; purpose of seven steps |
| Mathematics | Shallow | Developed | Three-state segment test (eq. 5) and OpenCV's strict inequalities; ID3 tree and its approximation; scores $V$ and maximum $t$; BRIEF eqs. 1–2 and G II sampling; Hamming metric; photometric deduction; worked examples A (pretests), B (wrap-around), C (binomial model), D (rotation displacement) |
| Parameters | Shallow (one sentence) | Developed | Nine-row table with source values and interactions; five-step tuning approach |
| Properties | Absent (merged) | Developed | FAST repeatability result and its scope; invariances; orientation-quality result (O-BRIEF); detector exactness; meaning of the distance |
| Cost and implementation | Shallow | Developed | Cost terms with variables; reported speeds with hardware; OpenCV 4.13 contracts for `FastFeatureDetector`, `FAST_t`, OpenCL cap, mask order, contrib BRIEF; execution status |
| Evaluation | Shallow | Developed | Repeatability on 3-D scenes, recognition-rate protocol and caveat, end-to-end metrics; proposed rotation baseline and known-angle variation with resampling confound; measurement limits |
| Failure modes and diagnosis | Shallow (four fragments) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (FAST-9, BRIEF, ORB, SIFT, Shi–Tomasi with LK, learned matching); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/47-fast-brief.py`](checks/47-fast-brief.py) (21 assertions): compass and
diametric pretests (3 and 2 compass pixels for 12- and 9-arcs; every 9-arc meets each
diametric pair; 4 of 12 and 0 of 8 valid arcs pass the shared pretest), wrap-around
(runs 9 versus 5; 25 entries), Hamming toy example and permutation invariance,
binomial model (mean 128, sd 8, $P(d\le64)\approx2.4\times10^{-16}$; 25.6 and 4.8 for a
10% flip rate), rotation displacements (2.1, 3.1, 6.2 px at 12.0 px; 4.2 and 6.3 px at
24 px), RANSAC budgets (72 and 1,177), storage (32 MB versus 256 MB), OpenCL cap (3,072
and 20,736 keypoints) and the straight-edge bound (8 of 16 pixels).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/47-fast-brief.md),
  revision 5 → 6: body rewritten and deepened. Appendix language fixes, applied
  identically to the cards: "Question of work" → "Working question", "Reference
  Response" → "Reference answer", the CV-FAST-BRIEF-001 reference answer (as in the
  card), "very clear neighbors distributed throughout" → "very bright neighbors
  scattered around", "keep threshold ... deletion of maxima check then local
  redundancy" → "Record the threshold ... non-maximum suppression then controls local
  redundancy", "undistinguishable" → "indistinguishable", "bad assumptions to be
  addressed" → "wrong hypotheses to process", "a tolerance of registration ...
  refused" → "a registration tolerance ... rejected", "promise of historic speed" →
  "historical speed claim", "code each position as light, dark or similar" → "label
  each position as brighter, darker or similar", "double the sequence" → "concatenate
  the sequence with itself", "return the bit" → "flip the bit", "Hamming's distance
  does not tell what disagreements arise from" → "The Hamming distance does not say
  whether disagreements come from", "in a ORB assembly ... little redundant tests on
  learning data" → "in ORB, the binary comparisons were selected offline on training
  data to be informative and weakly redundant", "Compensation expected" → "Expected
  compensation", "the two readings of a test" → "the two sample positions of each
  test", "discriminating experience" → "discriminating experiment", "prints" →
  "samples", "stop, degeneration and repetition variants" → "early termination,
  degeneracy handling and re-sampling variants". Tutorial links marked as not re-read.
  Sources split into scientific and implementation sources; closing provenance line
  replaced. Front matter unchanged except `revision`; H1 and per-card headings
  unchanged.
- [Cards](../../../vault/40-features-matching/47-fast-brief.md): the two
  expected-answer changes quoted above; the appendix fixes; further-explanation
  fixes "Sense of measurement" → "Meaning of the measure", "Chain to rebuild" →
  "Pipeline to reconstruct", "brick" → "building block", "Verification built" →
  "Constructed verification", "before and after delivery" → "before and after
  rotation", "Separately remove undetected dots, patch edges" → "Separately rule out
  undetected points, patch borders", "The historical numbers of an article" → "A
  paper's historical numbers"; blocking errors rewritten as gerunds ("his points" →
  "its points"). CV-FAST-BRIEF-001 gains an "Implementation caveat" paragraph
  (shared pretest, strict inequalities); CV-FAST-BRIEF-004 gains one sentence with
  Calonder et al.'s measured 10–15° tolerance and the O-BRIEF result. All five Source
  lines now cite exact passages. Questions, IDs, objectives, families, tags and target
  deck unchanged.

`rg -n -i "FAST|BRIEF|Hamming" vault/` outside this subject found no claim
contradicted here; ORB and matching notes are reviewed later in this run.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FAST-BRIEF-01 | CV-FAST-BRIEF | Predict how a camera gain change affects FAST corner counts and BRIEF bits, and explain why one is invariant and the other is not | Photometric behavior untested; absent understanding family | Understanding; Mathematics (photometric deduction) | 1 card, 3 criteria | [Rosten and Drummond 2006, eq. 5](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [Calonder et al. 2010, eq. 1](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf) |
| P-CV-FAST-BRIEF-02 | CV-FAST-BRIEF | Choose between upright BRIEF, an oriented binary descriptor and SIFT given the rotation range, a known sensor attitude and a CPU budget | Absent design family; the cost of orientation invariance reported by Calonder et al. is untested | Design; Alternatives | 1 card, 3–4 criteria | [Calonder et al. 2010, §4](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf); [Rublee et al. 2011, §3.2](https://doi.org/10.1109/ICCV.2011.6126544) |

No existing proposal concerns this subject. No question was found defective. The
objective of CV-FAST-BRIEF-005, "measure the compromis calculation repeatability",
is a mistranslation (objective lines are invariants in this pass); proposed wording:
"Measure the tradeoff between computation and repeatability."

## Sources

Scientific sources, opened at the passages listed (text extracted with `pdftotext`):

- Rosten and Drummond 2006, [author PDF](https://www.edwardrosten.com/work/rosten_2006_machine.pdf): all sections and Table 1.
- Rosten, Porter and Drummond, [arXiv 0810.2434v1](https://arxiv.org/abs/0810.2434): §III-A to §III-C, §VI-B (Table IV), §VII. The published TPAMI 2010 version was not opened.
- Calonder et al. 2010, [PDF](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf): §§1–5.
- Rublee et al. 2011, ORB, read in a course-hosted copy of the ICCV paper (canonical [DOI](https://doi.org/10.1109/ICCV.2011.6126544)): §4.1, §4.3.

Implementation sources (official code at tag 4.13.0):

- [`features2d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp): L571–L624.
- [`fast.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/fast.cpp): L56–L299, L440–L481, L520–L541.
- [`fast_score.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/fast_score.cpp): L50–L209.
- [opencv_contrib `xfeatures2d.hpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/xfeatures2d/include/opencv2/xfeatures2d.hpp): L150–L172.
- [opencv_contrib `brief.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/xfeatures2d/src/brief.cpp): L61, L99–L119, L181–L231, L270–L289.
- `fast.cpp` and `fast_score.cpp` at tag 4.11.0, compared with `diff` to justify the probe.
- [Stack Overflow question 41809634](https://stackoverflow.com/questions/41809634/opencv-fast-type-5-8), seen only as a search-result summary; not used as evidence.

Failed accesses and limits:

- docs.opencv.org/4.13.0 tutorials (FAST, BRIEF, ORB) not re-read (HTTP 403); links
  retained as not re-read.
- Context7 was not available in this session.
- The probe ran OpenCV 4.11.0, not 4.13.0; equivalence rests on the source `diff`.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC only on `45-recalage-ecc.md` ("missing local link or outside vault: ECC"), a file of another subject being edited concurrently; no error in this subject's files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 268 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/47-fast-brief.py` | 21 checks passed |
| `git diff --check` on this subject's files | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/47-fast-brief.md` | 5 cards, 354–473 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 5` → `6`; H1 and per-card headings unchanged; `$$` balanced |

Apart from the FAST probe described above, no feature extraction or matching was
executed; the proposed baseline and variation are protocols, not results. Obsidian
and AnkiDroid rendering are unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export
status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-FAST-BRIEF revision 6, CV-FAST-BRIEF-001 to 005, corrections listed above, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-FAST-BRIEF-01, P-CV-FAST-BRIEF-02).
