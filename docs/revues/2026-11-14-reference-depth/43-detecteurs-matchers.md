# Review — Local detectors, descriptors and matchers — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the pipeline and comparison note of the topic: stage contracts,
matching strategies, stage-wise evaluation and failure attribution. Detector and
descriptor mechanisms are linked to the method notes reviewed earlier in this run
(CV-CORNERS, CV-FAST-BRIEF, CV-SIFT, CV-ORB); approximate search to CV-FLANN. AKAZE,
which has no method note, is summarized at comparison depth.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCHING-001 | Corner constrains two directions, edge one (aperture problem): confirmed (Harris p. 149; Shi–Tomasi ch. 4). Covariance $\sigma^2M^{-1}$: correct derivation (see CV-CORNERS example B). "linearized luminance constant", "no longer respect the single movement", "two independent stresses" | Reasoning on the structure matrix; overlaps CV-CORNERS-001 (same mechanism, different framing) | 2 expected criteria; 355 → 350 lexical words | Aligned with CV-CORNERS | Minor | Language fixes; Source line now cites the two primary papers |
| CV-MATCHING-002 | FAST locates, BRIEF describes: confirmed (Rosten §2.1; Calonder §3); descriptor border loss confirmed in OpenCV contrib BRIEF (`brief.cpp` L288). "FAST takes an image and coordinate frame candidate positions" (garbled), "fuzzy piece", "descriptors go wrong with the part" (French: *tournent mal avec la pièce*, degrade when the part rotates) | Comparison of stage roles; overlaps CV-FAST-BRIEF-003 | 1 expected criterion pair; 350 → 346 lexical words | Aligned with the reference stage table | Minor | Meaning-restoring explanation fixes; Source line given primary passages |
| CV-MATCHING-003 | Approximate search can miss neighbors and change the ratio: consistent with Lowe §7.2 (BBF, <5% loss at 200 candidates) and the FLANN contract (`features2d.hpp` L1290–L1306). "insider status" for *inlier* status, "He may miss", "lifting a symmetry" | Evaluation of an approximate search through the cascade | 4 expected criteria; 361 → 359 lexical words | Consistent with CV-FLANN | Minor | Language fixes; Source line given exact passages |
| CV-MATCHING-004 | Only geometry tests a physical model, and it does not resolve symmetries: confirmed (`findHomography` transfer error, calib3d.hpp L776–L844; IPOL §5). Expected answer said "cover" for coverage; explanation "a single brand" for a unique mark, "check also supports spatial points and reserved observations" (garbled) | Diagnosis: model consistency versus identity | 3 expected criteria; 349 → 353 lexical words | Aligned with worked example B | Minor | Language fix in the expected answer; meaning-restoring fixes; Source line given exact passages |

Expected-answer change (language fix): CV-MATCHING-004 "with residuals, thresholds
and cover" → "with residuals, thresholds and coverage".

## Reference findings

Claims of revision 7 checked against their passages:

- Stage separation (detector, descriptor, matcher, geometry): consistent with Lowe §7
  and the OpenCV API.
- Harris score, smallest eigenvalue, FAST circle comparisons, BRIEF binary tests:
  confirmed in the method notes' sources (Harris p. 150, Shi–Tomasi eq. 4.1, Rosten
  §2.1, Calonder §3).
- "AKAZE constructs a nonlinear multiscale representation; its descriptor variant must
  be named": confirmed (Alcantarilla et al. §1, §3.3; `features2d.hpp` L866–L897).
- "BF costs about n×m comparisons": confirmed by construction.
- "Context7 verification" in two appendix source lines: not reproducible in this
  session; those lines now say so.
- Mistranslations: "BRIEF described by binary tests", "Question of work", "Reference
  Response", "check" labels; no scientific error was found. The body was shallow (one
  or two sentences per section).

New claims verified for revision 8: Lowe §7.1 (global threshold versus ratio; second
neighbor as density estimate; 0.8 operating point); IPOL §5 (ratio drops repeated
structures); Mikolajczyk and Schmid 2003 §3.3 and conclusions; Schmid 2000 §3.1;
Calonder §4; Rosten §3; Rublee §6.3; Alcantarilla §1, §3.2, §3.3, §4; OpenCV
`DescriptorMatcher`, `BFMatcher`, `FlannBasedMatcher`, AKAZE, `DMatch`,
`findHomography` contracts.

Implementation points worth recording (FR-036):

| Aspect | Method expectation | OpenCV 4.13.0 |
| --- | --- | --- |
| Robust homography | RANSAC by default in most write-ups | `findHomography` defaults to `method=0`, plain least squares (calib3d.hpp L841–L844) |
| Iteration budget | $N$ from $w$ and $p$ | Capped at `maxIters=2000`: at $w=0.15$ only 0.637 confidence (example C) |
| Cross-check | Mutual nearest neighbors | `crossCheck=true` acts on `knnMatch` with $k=1$; presented as an alternative to the ratio test (features2d.hpp L1273–L1278) |
| FLANN matcher | Index suited to the descriptor | Default `KDTreeIndexParams`, no mask support (L1290–L1306) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 328 → 3,335. The note is
a comparison and protocol note; mechanism depth stays in the method notes.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (two sentences) | Developed | Stage contract table with OpenCV types, questions and owned failures; frames and units; index bookkeeping; pipeline role |
| Intuition | Shallow | Developed | Increasingly global questions; constructed shelf illustration; Mermaid flow with failure points |
| Prerequisites | Shallow (one link) | Developed | Links by stage to method and geometry notes |
| Assumptions | Shallow | Developed | Repeatability, distinctiveness within the population, one model, correct norm; observability (aperture, periodicity, texture); degenerate cases |
| Procedure | Shallow | Developed | Pipeline pseudocode; table of five matching strategies with what each tests and misses |
| Mathematics | Shallow | Developed | Detector summary (linked), distances and scales, ratio test with operating point, transfer residual, RANSAC budget; worked examples A (filters), B (periodic scene), C (RANSAC cap) |
| Parameters | Shallow | Developed | Stage-wise parameter table with OpenCV defaults; five-step tuning approach |
| Properties | Shallow | Developed | Equivariance versus invariance, search exactness, filters as heuristics, RANSAC and LMeDS guarantees, published comparisons with their scope |
| Cost and implementation | Shallow | Developed | Latency decomposition with variables and constructed costs; OpenCV 4.13 contracts for matchers, AKAZE and `findHomography` |
| Evaluation | Shallow | Developed | Stage-wise protocols; baseline and ratio-versus-mutual variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (SIFT, ORB, AKAZE, KLT, learned, direct); industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/43-detecteurs-matchers.py`](checks/43-detecteurs-matchers.py) (11 assertions):
filter outcomes on the distance table (precision 0.67, 0.75, 0.60; recall 0.8, 0.6, 0.6;
ratios 0.909, 0.903, 0.75), periodic inlier counts (5 vs 3; 21 vs 19), RANSAC budgets
(83, 1,354, 10,464) and capped confidence (0.637), brute-force costs (128 million vs 4
million) and storage, and the AKAZE descriptor size (486 bits = 162 × 3, 61 bytes).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/43-detecteurs-matchers.md),
  revision 7 → 8: body rewritten and deepened. Appendix language fixes, applied
  identically to the cards: "Question of work" → "Working question", "Reference
  Response" → "Reference answer", "in the vicinity" → "in the neighborhood", "directions
  of movement" → "directions of displacement", "can almost leave it the same" → "can
  leave it almost unchanged", "helps locate a move" → "helps localize a displacement",
  "So distinguish local location information and ambiguity of association" →
  "Distinguish local localization information from association ambiguity",
  "obscured" → "occluded", "What the Geometry Tests" → "What the geometry tests", "same
  medium" → "same support", "a single brand" → "a unique mark", "check also supports
  spatial points and reserved observations" → "Also check the spatial support of the
  points and held-out observations", "The linearized luminance constant" → "Linearized
  brightness constancy", "a window through two objects ... no longer respect the
  single movement" → "a window straddling two objects ... violate the single-motion
  assumption", "On the contrary" → "Conversely", "standardizations" →
  "normalizations", "in the field of variations useful" → "over the useful range of
  variations", "Measuring the Cascade Effect: on the same requests ... the insider
  status and the reserved geometric error" → "Measuring the cascade effect: on the
  same queries ... the inlier status and the geometric error on held-out points",
  "separation of the ex æquo" → "tie-breaking", "lifting a symmetry" → "breaking a
  symmetry", "for a $H$ homography sending" → "for a homography $H$ mapping", "points
  3D" → "3-D points", "conditional to" → "conditional on". Sources split into
  scientific and implementation sources; closing provenance line replaced. Front
  matter unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/43-detecteurs-matchers.md): the
  expected-answer change above; the appendix fixes; further-explanation fixes
  "Breakdown of Inputs and Outputs: FAST takes an image and coordinate frame candidate
  positions" → "FAST takes an image and returns candidate positions in its frame",
  "Example of a built diagnosis ... fuzzy piece ... descriptors go wrong with the part"
  → "Constructed diagnosis example ... blurred part ... descriptors degrade when the
  part rotates", "A complete string like ORB" → "A complete pipeline like ORB", "Why
  the approximation is taking place ... He may miss" → "Why the approximation matters
  ... It may miss"; blocking errors rewritten as gerunds ("two independent stresses" →
  "two independent constraints", "Deduct the physical validity of the reciprocity" →
  "Inferring physical validity from the reciprocity"). All four Source lines now cite
  primary papers or 4.13.0 code instead of unreadable tutorials. Questions, IDs,
  objectives, families, tags and target deck unchanged.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-MATCHING-01 | CV-MATCHING | On a small distance table with ground truth, compute precision and recall of nearest-neighbor, ratio and mutual filters and name the error each keeps | No card trains match-level evaluation with explicit denominators | Evaluation; worked example A | 1 card, 3 criteria | [Lowe 2004, §7.1](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [Mikolajczyk and Schmid 2003, §3.3](https://inria.hal.science/inria-00548227) |
| P-CV-MATCHING-02 | CV-MATCHING | Explain why `findHomography` can return a poor or unreliable model without error: default least-squares method, and an iteration cap that limits confidence at low inlier ratios | Verification-stage implementation traps untested | Diagnosis; worked example C | 1 card, 3 criteria | [OpenCV 4.13.0 `calib3d.hpp` L776–L844](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L776-L844) |

Overlap observations for the learner (no change made): CV-MATCHING-001 trains the
same corner-versus-edge mechanism as CV-CORNERS-001, and CV-MATCHING-002 the same role
separation as CV-FAST-BRIEF-003. Merging or retiring a card changes recall history and
is a learner decision. No question was found defective.

## Sources

Scientific sources, opened at the passages listed (text extracted with `pdftotext`):
Lowe 2004 §7–§7.2; IPOL 2014 §5–§6; Mikolajczyk and Schmid 2003 §3.3 and conclusions;
Schmid et al. 2000 §3.1; Calonder et al. 2010 §4; Rosten and Drummond 2006 §3; Rublee
et al. 2011 §6.3 (all opened earlier in this run, see the CV-SIFT, CV-FAST-BRIEF,
CV-ORB and CV-CORNERS reports); Alcantarilla, Nuevo and Bartoli 2013,
[BMVA archive PDF](https://www.bmva-archive.org.uk/bmvc/2013/Papers/paper0013/paper0013.pdf):
abstract, §1, §3.2, §3.3, §4 table passage.

Implementation sources (official headers at tag 4.13.0):
[`features2d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp)
L850–L897, L1060–L1100, L1255–L1306;
[`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp)
L776–L844; [`core/types.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/types.hpp)
L848–L860; [`core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp)
L180–L205.

Failed accesses and limits: docs.opencv.org/4.13.0 pages not re-read (HTTP 403),
links retained as not re-read; Context7 unavailable; the Mikolajczyk and Schmid 2005
PAMI evaluation was not opened (the 2003 CVPR version was).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/43-detecteurs-matchers.py` | 11 checks passed |
| `git diff --check` on this subject's files | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/43-detecteurs-matchers.md` | 4 cards, 346–359 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced |

No matching or estimation code was executed; the proposed baseline and variation are
protocols, not results. Obsidian and AnkiDroid rendering are unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-MATCHING revision 8, CV-MATCHING-001 to 004, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-MATCHING-01, P-CV-MATCHING-02).
