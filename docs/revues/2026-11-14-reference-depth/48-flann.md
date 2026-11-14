# Review — FLANN — approximate nearest-neighbor search and distance conventions — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 2 important, 2 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The note now develops FLANN's index families, time-bounded search, autotuning and the
OpenCV 4.13 `flann::Index` and `FlannBasedMatcher` contracts. The trailing section is
titled "Sources", so `#sources` resolves in the note.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLANN-001 | Build cost can exceed query gains: consistent with Muja and Lowe 2009 §3.3 (build-time weight); figures 2.1/0.3 s, 12/30 s and break-even 1,000 recomputed. Expected answer used $T_{requête}$ (French) and "the full cost" for *coût exhaustif*; explanation said "damping threshold" and "depreciation" for amortization, "material" for hardware, "2,1 s" | Comparison: amortization decision | 2 expected criteria; 384 → 413 lexical words | Aligned with worked example A | Minor | Meaning-restoring fix of the expected answer; one sentence on OpenCV's per-call index rebuild; language fixes |
| CV-FLANN-002 | Storage does not define the metric; Hamming for ORB: confirmed (Muja and Lowe 2014 §3.3; `miniflann.cpp` L330–L446). Expected answer said "changes the direction of the distances" for *le sens* (the meaning); explanation "how far its manufacturer is waiting" (which distance its extractor expects). Imprecise implementation claim: "check the need for Hamming2 and the actual matcher support": OpenCV's LSH forces plain Hamming and has no Hamming2 | Diagnosis: metric contract | 3 expected criteria; 396 → 416 lexical words | Aligned with CV-ORB-003 and the reference contract | Important | Meaning-restoring fix of the expected answer; explanation now states the verified LSH and k-d tree type contracts |
| CV-FLANN-003 | A missed second neighbor lowers the ratio artificially: correct; FLANN search is time-bound with no per-query bound (2014 §2.1). "call@1" for *rappel@1* (recall@1) obscured the metric; "0,91", "0,33"; "Ex-æquo", "several clues" | Reasoning: approximation and the ratio test | 2 expected criteria; 398 → 395 lexical words | Aligned with worked example B | Important | "call@1" → "recall@1" throughout; language fixes |
| CV-FLANN-004 | Recall against exact search, latency, memory, build and final inliers: consistent with 2009 §3–§4 and 2014 §4. Expected answer said "reserved data" for held-out data; explanation "The call describes", "reserved lot", "exhaustive research" | Evaluation: recall–time curve with downstream checks | 4 expected criteria; 381 → 371 lexical words | Aligned with the reference evaluation section | Minor | Language fix in the expected answer; language fixes |

Expected-answer changes (meaning-restoring language fixes, checked against the French
source with `git show b7142bb^`):

- CV-FLANN-001: "Compare $T_{construction}+N_qT_{requête}$ to the full cost" →
  "Compare $T_{\text{construction}}+N_qT_{\text{query}}$ to the exhaustive cost".
- CV-FLANN-002: "changes the direction of the distances" → "changes the meaning of the
  distances".
- CV-FLANN-004: "on reserved data" → "on held-out data".

## Reference findings

Claims of revision 6 checked against their passages:

- Randomized k-d forests and hierarchical k-means trees, budgeted exploration,
  memory–build–query–recall trade-off: confirmed (Muja and Lowe 2009 §3.1–§3.3;
  2014 §3.1–§3.2).
- "OpenCV 4.13 shows a kd-tree for SIFT and an LSH index for common binary ORB
  descriptors": the tutorial could not be re-read (HTTP 403); the substance is
  confirmed by the 4.13.0 code (default `KDTreeIndexParams`, LSH forcing Hamming).
- "call@1" (mistranslation of *rappel@1*), "research budget" (search budget),
  "comprehensive research" (exhaustive search), "entry/exit" (input/output),
  French decimal commas: language defects that obscured meaning.
- "API OpenCV 4.13 verified with Context7" (closing line): not reproducible in this
  session; replaced.
- No scientific error was found.

New claims verified for revision 7: Lowe 2004 §7.2 (k-d trees beyond ~10 dimensions,
BBF 200 candidates); Muja and Lowe 2009 §3 (precision definition), §3.1 ($D=5$, single
priority queue), §3.3 (eq. 1), §4 and §4.4 (60% precision and three orders of magnitude
on sift1M, smaller above 90%; k-means tree versus ANN and LSH), §4.5 (higher branching
for higher precision); Muja and Lowe 2014 §2.1 (error-bound versus time-bound), §3.1,
§3.2 (complexities), §3.3 (binary features, k-means tree unsuitable), §4 (precision);
Rublee et al. §5.2–§5.3.

Implementation findings (FR-036), from the 4.13.0 sources, not executed:

| Aspect | Expectation | OpenCV 4.13.0 |
| --- | --- | --- |
| Index reuse | Build once, query many times | `knnMatch(query, train, k)` clones an empty matcher and rebuilds the index on every call (`matchers.cpp` L589–L598, L1389–L1405) |
| Binary metric | Hamming or Hamming2 as the descriptor requires | LSH forces `FLANN_DIST_HAMMING`; no Hamming2 (`miniflann.cpp` L409–L412) |
| Type contract | — | Element type checked against the distance: L2 needs `CV_32F` (`miniflann.cpp` L330–L338) |
| Distances | Euclidean | `cvflann::L2` is squared (`dist.h` L237–L240); `FlannBasedMatcher` takes the square root (`matchers.cpp` L1424) |
| Search budget | Lowe used 200 candidates (§7.2) | `SearchParams` default `checks=32` (`miniflann.hpp` L147) |
| LSH defaults | — | cvflann `LshIndexParams(12, 20, 2)`; `cv::flann::LshIndexParams` has no defaults (`lsh_index.h` L64; `miniflann.hpp` L136) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 417 → 3,041.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task and why exact search fails in high dimension; OpenCV data, metric, output and guarantee contract; pipeline role |
| Intuition | Shallow | Developed | Index families in plain terms; constructed drone re-localization illustration; Mermaid flow with evaluation path |
| Prerequisites | Shallow (one link) | Developed | Links to CV-MATCHING, descriptor notes, CV-HOMOGRAPHIE, CV-SVD |
| Assumptions | Absent | Developed | Data structure, amortization, static database, metric at build time; observability of search errors; degenerate cases |
| Procedure | Shallow | Developed | Build, query and evaluation pseudocode; purpose of six steps |
| Mathematics | Shallow | Developed | Exact versus approximate neighbors, error-bound versus time-bound, precision/recall@k wording, complexities, autotuning cost (eq. 1), squared L2; worked examples A (amortization and OpenCV rebuild), B (ratio distortion and certification margin), C (multi-probe LSH model) |
| Parameters | Shallow | Developed | Six-row table with OpenCV and paper values; five-step tuning approach |
| Properties | Shallow | Developed | No per-query guarantee; published speed-ups with conditions; BBF result; binary-data limits; metric preservation |
| Cost and implementation | Shallow | Developed | Cost terms per index; OpenCV 4.13 contracts; illustrative snippet marked not executed |
| Evaluation | Shallow | Developed | Search, speed and downstream protocols; baseline and `checks` sweep with seed confound; measurement limits |
| Failure modes and diagnosis | Shallow | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices; industrial uses labelled as project reasoning; "Sources" with scientific and implementation subsections |

Constructed examples are recomputed by [`checks/48-flann.py`](checks/48-flann.py)
(13 assertions): amortization (2.1/0.3 s, 12/30 s, break-even 1,000, per-call rebuild),
ratio distortion (0.909 versus 0.333; margin 0.727), LSH probes (211 buckets; 0.58 and
>0.9999 at 30 bits; 0.11 and 0.75 at 60 bits; $1.2\times10^{-4}$ and 0.14% at 128 bits,
hypergeometric model), budgets (200 versus 32), unit-vector identity (0.8, 0.894) and
recall@1 (0.94).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/48-flann.md), revision 6
  → 7: body rewritten and deepened. Appendix language fixes, applied identically to the
  cards: "neighbor recall, index ratio and damping" → "neighbor recall, the ratio test
  under approximation and index amortization", "Question of work" → "Working
  question", "Reference Response" → "Reference answer" (with the expected-answer
  fixes above), "2,1 s"/"0,3 s"/"0,001"/"0,003"/"0,91"/"0,33" → decimal points, "on the
  same basis" → "on the same database", "without constituting a benchmark FLANN" →
  "they are not a FLANN benchmark", "depreciation" → "amortization", "A reconstructed
  base with each image" → "A database rebuilt for each image", "material" →
  "hardware", "Proposed Decision Curve: ... reserved lot ... exhaustive research" →
  "Proposed decision curve: ... held-out batch ... exhaustive search", "kd-trees" →
  "k-d trees", "k-mean tree partitions rather by group centers" → "k-means tree
  partitions by cluster centers instead", "labor economy" → "saved work", "damping
  threshold checks" → "break-even condition is", "reinstated" → "added back",
  "Standardization and metric" → "Normalization and metric", "Inverse case not to be
  forgotten" → "The inverse case", "call@1" → "recall@1", "Ex-æquo ... several clues"
  → "Ties ... several indices", "Read a quality – cost curve ... undominated ... will
  usually return someone" → "Read a quality–cost curve ... non-dominated ... usually
  returns something". Sources split into scientific and implementation subsections
  under "## Sources"; closing provenance line replaced. Front matter unchanged except
  `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/48-flann.md): the three expected-answer
  changes above; the appendix fixes; further-explanation fixes "on a small base or on a
  given material" → "on a small database or on given hardware", "how far its
  manufacturer is waiting" → "which distance its extractor expects", "The call
  describes" → "Recall describes"; blocking errors rewritten as gerunds. Additions:
  CV-FLANN-001 one sentence on the per-call index rebuild; CV-FLANN-002 the verified
  OpenCV contract (k-d tree needs `CV_32F`, LSH forces plain Hamming, no Hamming2),
  replacing the vaguer "check the need for Hamming2 and the actual matcher support".
  All four Source lines now cite exact passages. Questions, IDs, objectives, families,
  tags and target deck unchanged.

Other vault files repeating a corrected claim: none found (`rg -n "call@" vault/`
returns nothing after the fix; CV-MATCHING-003 already used "recall").

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FLANN-01 | CV-FLANN | Explain why a `FlannBasedMatcher` used through `knnMatch(query, train, k)` never amortizes its index, and how to restructure the calls | The amortization card stops at the cost model; the implementation trap is untested | Practice; worked example A | 1 card, 2–3 criteria | [OpenCV 4.13.0 `matchers.cpp` L589–L598, L1160–L1176](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L589-L598) |
| P-CV-FLANN-02 | CV-FLANN | Given LSH tables, key size and probe level, predict which true matches (by Hamming distance) are likely to be missed and how each parameter moves recall and cost | LSH mechanics untested; only k-d trees are described in cards | Reasoning; worked example C | 1 card, 3 criteria | [Muja and Lowe 2014, §3.3](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf); [OpenCV 4.13.0 `lsh_table.h`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/lsh_table.h#L270-L370) |

No existing proposal concerns this subject. No question was found defective. The
objective of CV-FLANN-004, "measure the recall time curve", reads better as "Measure
the recall–time curve" (objective lines are invariants in this pass).

## Sources

Scientific sources, opened at the passages listed (text extracted with `pdftotext`):

- Muja and Lowe 2009, [VISAPP PDF](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf): §2–§5.
- Muja and Lowe 2014, [TPAMI author PDF](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf): §2.1, §3.1–§3.3, §4 opening (`pdftotext` reported a damaged trailer but extracted the text).
- Lowe 2004 §7.2 and Rublee et al. 2011 §5.2–§5.3, opened earlier in this run.

Implementation sources (official code at tag 4.13.0):
[`features2d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp) L1290–L1306;
[`matchers.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp) L589–L598, L655–L661, L1101–L1176, L1389–L1441;
[`miniflann.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/miniflann.hpp) L100–L163;
[`miniflann.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/src/miniflann.cpp) L330–L446;
[`defines.h`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/defines.h) L73–L78, L130–L131;
[`dist.h`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/dist.h) L237–L240;
[`lsh_index.h`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/lsh_index.h) L64–L105;
[`lsh_table.h`](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/include/opencv2/flann/lsh_table.h) L270–L281, L352–L370.

Failed accesses and limits: the OpenCV matching tutorial (HTTP 403) was not re-read;
Context7 unavailable; the LSH probability model assumes uniformly spread bit
differences and was not measured.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/48-flann.py` | 13 checks passed |
| `git diff --check` on this subject's files | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/48-flann.md` | 4 cards, 371–416 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 6` → `7`; H1 and per-card headings unchanged; `$$` balanced |

No index was built and no search was executed; the snippet is illustrative and the
proposed baseline and variation are protocols, not results. Obsidian and AnkiDroid
rendering are unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-FLANN revision 7, CV-FLANN-001 to 004, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-FLANN-01, P-CV-FLANN-02).
