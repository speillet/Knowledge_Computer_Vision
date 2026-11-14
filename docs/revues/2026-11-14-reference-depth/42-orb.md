# Review — ORB — detection and oriented binary descriptors — 2026-11-14

## Overview

6 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 0 important, 6 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The note now develops ORB's own mechanisms (Harris-ranked FAST in a pyramid,
intensity-centroid orientation, steered and learned tests, `WTA_K` symbols) and the
OpenCV 4.13 contract. FAST, BRIEF and Harris are linked to
[CV-FAST-BRIEF](../../../vault/40-features-matching/references/47-fast-brief.md) and
[CV-CORNERS](../../../vault/40-features-matching/references/46-harris-shi-tomasi.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | FAST in a pyramid, Harris ranking, centroid orientation, steered tests: confirmed (Rublee §3.1, §3.2, §4.1–§4.3). "turned neighborhoods", "keypoint-centric patch", "actionable direction", "silently supplemented" | Algorithm: role of each component | 4 expected criteria; 382 → 370 lexical words | Aligned with the reference procedure | Minor | Language fixes; Source line given exact sections and code lines |
| CV-ORB-002 | Hamming counts differing tests; byte values are storage: recomputed (1 vs 128, 2 vs 3). "binary suites", "adds the disagreements", "separates metric storage and metric representation" | Reasoning: metric follows representation | 2 expected criteria; 388 → 387 lexical words | Aligned with worked example D | Minor | Language fixes; Source line given exact passages |
| CV-ORB-003 | `WTA_K` 3/4 needs `NORM_HAMMING2`, which counts differing 2-bit groups: confirmed (`orb.cpp` L772–L782; `core/base.hpp` L200–L204). Missing practice condition: the descriptor stays 32 bytes, so 3/4 give 128 symbols from seeded random tuples instead of 256 learned tests (`orb.cpp` L1206–L1226) | Practice: variant and norm | 2 expected criteria; 306 → 369 lexical words | Aligned with the reference parameters | Minor | Implementation paragraph added; language fixes; Source line given code lines |
| CV-ORB-004 | Cross-check is mutual nearest; ratio compares the two nearest; neither validates geometry: confirmed (`features2d.hpp` L1273–L1278; Lowe §7.1). Expected answer said "better enough", "No one guarantees ... a valid geometric pattern"; explanation said "0,8", "ex æquo", "reminders" for *recall* | Comparison: two filters, two questions | 2 expected criteria; 393 → 389 lexical words | Aligned with the reference failure table | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-ORB-005 | Pyramid range and resolution limit repeatability: confirmed; the authors state scale invariance was not adequately addressed (§7); default range $1.2^7=3.58$ recomputed. "remoteness", "well-solved marking", "announce that the pyramid solves" | Diagnosis: scale coverage before feature count | 3 expected criteria; 325 → 355 lexical words | Aligned with worked example C | Minor | One sentence with the default range and the authors' statement; language fixes |
| CV-ORB-006 | Baseline with recorded parameters, right norm, geometric validation and full cost: consistent with Rublee §6.1 and §6.3 (phone: matching 72.8 ms > extraction 66.6 ms). 64 kB for 2,000 descriptors recomputed. "Predicting behavior ... and not turning" (verbless), "cover", "reserved parts" | Design: baseline under constraint | 3 expected criteria; 380 → 403 lexical words | Aligned with the reference cost section | Minor | One sentence with the phone timings; language fixes |

Expected-answer change (meaning-restoring language fix):

- CV-ORB-004: "the ratio test requires the best neighbor to be better enough than the
  second. No one guarantees a correct physical match or a valid geometric pattern." →
  "the ratio test requires the best neighbor to be sufficiently better than the
  second. Neither guarantees a correct physical match or a valid geometric model."

## Reference findings

Claims of revision 8 checked against their passages:

- $\theta=\operatorname{atan2}(m_{01},m_{10})$ from patch moments: confirmed (§3.2,
  eqs. 1–3). Rotated test pattern and 256 tests: confirmed (§4.1). Offline
  learning of rBRIEF: confirmed (§4.3).
- `WTA_K=3`/`4` encoded on 2 bits with `NORM_HAMMING2`, "not Hamming squared":
  confirmed (`features2d.hpp` L443–L451; `core/base.hpp` L200–L204).
- Cross-check semantics in `BFMatcher`: confirmed (`features2d.hpp` L1273–L1278).
- "verified with Context7" (2026-10-30 and 2026-11-08 appendices): not reproducible in
  this session; the appendix source lines now say so and the claims were re-checked in
  the 4.13.0 sources.
- Mistranslations: "coordinates **Focus on the keypoint**" (centered on the keypoint,
  per the French source `git show b7142bb^`), "Ladder: discreet cover" (Scale: discrete
  coverage), "Choix industriel", "check useful", "Competences", "Connexions".
- No scientific error was found.

New claims verified for revision 9 (main ones): Rublee et al. §1 (goals), §2 (single
dominant orientation), §3.1 (FAST edge responses, low threshold then Harris top N,
pyramid), §3.2 (circular moments, instability as $|C|\to0$, IC better than BIN and MAX,
Fig. 2), §4.1 (eqs. 4–5, $S_\theta=R_\theta S$, 12° table, 5×5 sub-window smoothing),
§4.2 (variance and correlation), §4.3 (300k keypoints, 205,590 tests, greedy search),
§4.4 (Figs. 7–8, real-scene inlier table), §5.1–§5.3 (multi-probe LSH, Fig. 11), §6.1
(timings, five levels at $\sqrt2$, area interpolation), §6.3 (phone timings), §7
(scale invariance).

Disagreements between the paper and OpenCV 4.13.0 (FR-036):

| Aspect | Rublee et al. 2011 | OpenCV 4.13.0 |
| --- | --- | --- |
| Steering | Angle discretized in 12° steps, lookup table (§4.1) | Continuous rotation, nearest-pixel sampling (`orb.cpp` L240–L249) |
| Test smoothing | Integral image, each test point a 5×5 sub-window (§4.1) | Gaussian 7×7, $\sigma=2$, single-pixel reads (L1234) |
| Pyramid | Five levels at factor $\sqrt2$, area interpolation (§6.1) | 8 levels at factor 1.2 by successive `INTER_LINEAR_EXACT` resizes (L1132; header defaults) |
| Test set | 256 learned tests (§4.3) | Learned table only for `patchSize=31`; seeded random pattern otherwise; seeded random tuples for `WTA_K` 3/4 (L1206–L1226) |
| FAST wording | "FAST-9 (circular radius of 9)" (§3.1) | `TYPE_9_16`: 9 contiguous pixels on the 16-pixel circle of radius 3, as defined by Rosten and Drummond |
| Keypoint positions | Not specified | Level positions multiplied by $s^\ell$; with centre-aligned resizing this gives an offset of $0.5(s^\ell-1)$ px, a constructed derivation (L996–L1000; `resize.cpp` L798) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 739 → 3,445.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (merged with prerequisites) | Developed | Task from the paper; OpenCV input, mask, `KeyPoint` fields, 32-byte descriptors, norms; pipeline roles |
| Intuition | Shallow (step list) | Developed | Why orientation and decorrelation; constructed poster illustration; Mermaid data flow distinguishing blurred and unblurred levels |
| Prerequisites | Shallow | Developed | Links by mechanism to CV-FAST-BRIEF, CV-CORNERS, CV-FILTRES, CV-FLANN, CV-HOMOGRAPHIE |
| Assumptions | Absent (scattered) | Developed | Off-centre mass, in-plane changes, texture, one orientation; observability of identity and angle; degenerate cases |
| Procedure | Shallow | Developed | Pseudocode faithful to OpenCV 4.13; purpose of six steps with the paper's justification |
| Mathematics | Shallow | Developed | Moments and angle conventions, steered BRIEF, learning procedure, `WTA_K` symbols and Hamming2, Hamming; worked examples A (angle stability), B (angle error), C (level budgets and range), D (metrics), E (level offset) |
| Parameters | Shallow | Developed | Eight-row table with paper and OpenCV values and header warnings; five-step tuning approach |
| Properties | Shallow | Developed | Rotation, noise and real-scene results with their conditions; scale limits; distinctiveness |
| Cost and implementation | Shallow | Developed | Cost terms with variables; published timings including the phone; OpenCV 4.13 contracts; corrected snippet marked not executed |
| Evaluation | Shallow | Developed | Paper protocols and end-to-end metrics; baseline and `nlevels` variation with a budget confound |
| Failure modes and diagnosis | Shallow (three rows) | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by [`checks/42-orb.py`](checks/42-orb.py)
(17 assertions): centroid angles 45° and 135°, angle sensitivity (26.6° versus 0.57°),
angle-error displacements (1.31, 1.57, 0.71 px), per-level budgets (109, 90, 75, 63,
52, 44, 36, 31) and ranges (3.58, $179\times134$, 4), Hamming and Hamming2 examples and
ranges (256, 128), ratio examples (0.909, 0.333), 64,000 bytes, level offsets (0.1,
0.54, 1.29 px), published timing sums and ratios, and pyramid size (3.10 $WH$, bound
3.27 $WH$).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/42-orb.md), revision 8
  → 9: body rewritten and deepened. Appendix language fixes, applied identically to
  the cards: "Question of work" → "Working question", "Reference Response" →
  "Reference answer", "turned neighborhoods" → "rotated neighborhoods", "the test
  pattern is moved" → "is placed", "If the keypoints disappear themselves" → "If the
  keypoints themselves disappear", "predict three outcomes" → "plan for three
  outcomes", "cover and plausibility of the movement ... reserved parts" → "the
  coverage and the plausibility of the motion ... held-out parts", "steps that
  actually change in cost" → "every step whose cost actually changes", "keypoint-centric
  patch, set the moments" → "patch centered on the keypoint, define the moments",
  "actionable direction" → "usable direction", "binary suites ... adds" → "binary
  strings ... counts", "What the Winner Codes" → "What the winner encodes", "table
  length" → "array length", "built-up distance matrix, request A" → "constructed
  distance matrix, query A", "0,8" → "0.8", "calculations and reminders" →
  "computation and lower recall", "ex æquo and absent candidates" → "ties and missing
  candidates", "Scales and cost coverage" → "Scale coverage and cost", "Preparing
  behavior" → "Defining the behavior". The trailing section was split into scientific
  and implementation sources; reference-style link definitions were replaced by inline
  links; a provenance line was added. Front matter unchanged except `revision`; H1 and
  per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/42-orb.md): the expected-answer change
  quoted above; the appendix fixes; further-explanation fixes "Convert bytes to floats
  retains" → "Converting bytes to floats keeps", "Keep the compatible descriptors and
  matcher throughout the index" → "Keep descriptors, matcher and index consistent",
  "Two `00` and `11` win values" → "Winner values `00` and `11`", "a separate neighbor
  may be false" → "a well-separated neighbor may be wrong", "View levels" →
  "Visualize the levels", "well-solved marking ... after remoteness" → "well-resolved
  marking ... once the camera moves away"; blocking errors rewritten as gerunds.
  Additions: CV-ORB-003 implementation paragraph (32 bytes, 128 symbols, seeded random
  tuples, range 0–128); CV-ORB-005 default pyramid range and §7 statement; CV-ORB-006
  phone timings. All six Source lines now cite exact paper sections or 4.13.0 code
  lines. Questions, IDs, objectives, families, tags and target deck unchanged.

`rg -n -i "orb|WTA_K|HAMMING2" vault/` outside this subject found only the CV-FAST-BRIEF
card already aligned in this run and the CV-MATCHING note reviewed next.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ORB-01 | CV-ORB | Compute the intensity-centroid angle of a simple patch and explain why the angle becomes unstable when the centroid approaches the keypoint | Orientation is recited, never computed; its failure condition is untested | Reasoning; Mathematics, worked example A | 1 card, 3 criteria | [Rublee et al. 2011, §3.2](https://doi.org/10.1109/ICCV.2011.6126544) |
| P-CV-ORB-02 | CV-ORB | Size `nlevels` and `scaleFactor` for a required scale range and explain the effect on per-level budgets and cost | Pyramid configuration is untested beyond "check the range" | Practice; Parameters, worked example C | 1 card, 3 criteria | [OpenCV 4.13.0 `orb.cpp` L842–L855](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp#L842-L855); [Rublee et al. 2011, §6.1](https://doi.org/10.1109/ICCV.2011.6126544) |

No existing proposal concerns this subject. No question was found defective.

## Sources

Scientific source, opened at the passages listed: Rublee et al. 2011, read in a
course-hosted copy of the published ICCV paper (canonical
[DOI](https://doi.org/10.1109/ICCV.2011.6126544)), text extracted with `pdftotext`:
§§1–7 as listed above.

Implementation sources (official code at tag 4.13.0):

- [`features2d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp): L423–L461, L1255–L1280.
- [`orb.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp): L131–L1272.
- [`core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp): L195–L205.
- [`resize.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp): L789–L800 (`interpolationLinear` used by `INTER_LINEAR_EXACT`).

Failed accesses and limits:

- docs.opencv.org/4.13.0 pages (ORB class, ORB and matching tutorials) not re-read
  (HTTP 403); links retained as not re-read.
- The publisher's version of the ORB paper was not accessed; the read copy is the
  conference text hosted for a course.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/42-orb.py` | 17 checks passed |
| `git diff --check` on this subject's files | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/42-orb.md` | 6 cards, 355–403 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 8` → `9`; H1 and per-card headings unchanged; `$$` balanced |

No ORB extraction or matching was executed; the snippet is illustrative, the level
offset is derived from code, and the proposed baseline and variation are protocols,
not results. Obsidian and AnkiDroid rendering are unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-ORB revision 9, CV-ORB-001 to 006, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-ORB-01, P-CV-ORB-02).
