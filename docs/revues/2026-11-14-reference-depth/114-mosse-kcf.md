# Review — MOSSE and KCF — tracking with correlation filters — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 5 to revision 6. Highest severity per card before correction:
0 blocking, 2 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

This is the method note under the comparison note
[CV-SOT](../../../vault/110-tracking-association/references/113-tracking-monoobjet.md),
which holds the task contract, the family comparison and the benchmark protocols; this
note links to it instead of restating them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORRELATION-001 | Loop extract → correlate → peak → check → update: confirmed (MOSSE §3 introduction, §§3.4–3.5; KCF §VIII-A). Source cited KCF §IV (regression) for the loop: imprecise. "From the pic to the image" (peak), "research" (search), "return to the coordinate frame image before setting the trust" obscured meaning | Algorithm: the per-frame loop and where it can fail | 3 criteria; 372 → 379 words | Aligned with reference appendix | Minor | Language fixes; Source given KCF §VIII-A and MOSSE §§3.4–3.5 |
| CV-CORRELATION-002 | KCF uses cyclic shifts, circulant structure and compatible kernels: confirmed (KCF §§IV–V, Theorem 1). Expected answer said "cyclic offsets" and "circulating matrix" (circulant). Omission: MOSSE also solves ridge regression over cyclic shifts, of several base samples in the primal with one channel; DCF equals MOSSE for one channel (KCF §VII-B, §VIII-A, App. A-F). "assimilating a core to a deep network" mistranslated "kernel" as "core" | Comparison: what the circulant and kernel structure buys | 3 criteria; 378 → 452 words | Aligned | Important (misleading omission and meaning-altering terms) | Expected-answer terms restored; one sentence on the MOSSE/DCF relation added to the further explanation; Source given exact sections |
| CV-CORRELATION-003 | PSR $=(g_{\max}-\mu_{sl})/\sigma_{sl}$ with an $11\times11$ exclusion: confirmed (MOSSE §3.5). Expected answer used French decimal commas and "bottom average"; missing condition: OpenCV 4.13 legacy MOSSE uses whole-map statistics and threshold 5.7 (`mosseTracker.cpp` L31–L33, L104–L109) | Reasoning: compute and interpret a confidence statistic | 2 criteria; 400 → 447 words | Aligned | Minor | Expected answer fixed (decimals, "off-peak (sidelobe) region", "not a calibrated probability"); implementation difference added to the further explanation |
| CV-CORRELATION-004 | Model contamination during occlusion and freezing/search separation: confirmed as a consequence of MOSSE eqs. 10–12 and KCF §VIII-A interpolation; protocols labelled as project constructions. "Separate research and learning", "region being crawled", "box on the bottom", "the gel" mistranslated | Diagnosis: contamination versus loss of coverage | 3 criteria; 351 → 354 words | Aligned | Minor | Language fixes; Source given exact sections |
| CV-CORRELATION-005 | Reset protocol, losses, overlap and centre error: correct, but the Source cited MOSSE §§3.2–3.5 and KCF §IV, which do not address evaluation protocols | Evaluation: fair comparison under different reset rules | 3 criteria; 285 → 286 words | Aligned | Important (unsupported citation) | Source replaced by OTB §4 and VOT §3.1; language fixes |

Expected-answer changes (sourced correction or meaning-restoring language fix):

- CV-CORRELATION-002: "KCF structures the examples as cyclic offsets of the patch; the
  circulating matrix allows efficient Fourier calculations, …" → "KCF structures the
  examples as cyclic shifts of the patch; the circulant matrix allows efficient Fourier
  computations, …" (KCF §IV-B, §IV-C).
- CV-CORRELATION-003: "PSR=$(0,8-0,2)/0,1=6$. The peak exceeds the bottom average by
  six standard deviations depending on the region outside the selected peak. It
  measures a response contrast, with no calibrated probability of a good target." →
  "PSR $=(0.8-0.2)/0.1=6$. The peak exceeds the mean of the off-peak (sidelobe) region
  by six standard deviations of that region. It measures response contrast, not a
  calibrated probability that the target is correct." (MOSSE §3.5).

## Reference findings

Claims of revision 5 checked: the simplified objective, the PSR definition and the
$O(n\log n)$ cost are confirmed (MOSSE §3.5, §4.3; KCF §IV-D). Defects: French
subscripts `horspic` in the PSR formula, decimal commas (`0,8`, `0,2`, `0,1`),
"circulating" for circulant, "core" for kernel, "research" for search, "on the
bottom" for on the background, "the gel" for freezing, and appendix labels "Question
of work" and "Reference Response". The revision-5 body did not record the
implementation differences below.

New verified content: MOSSE eqs. 3, 5, 10–12, preprocessing, eight initial
perturbations, $\sigma=2$, regularization study, PSR values (20–60, about 7, naive
filter 3–10) and timing; KCF eqs. 1–2, 6–7, 12, 17–18, 22, 30–31, Theorem 1 and
Example 2, §VI-C limits, §VII-B primal/dual tradeoff, App. A-A (label placement,
non-unitary FFT, 2.5× window, cosine window), App. A-F, Table I and Table II.

Paper versus OpenCV 4.13.0 (FR-036), now recorded in the note:

| Aspect | Paper | OpenCV 4.13.0 |
| --- | --- | --- |
| KCF window | 2.5 × target | 2 × box (`trackerKCF.cpp` L214–L218) |
| KCF features | Raw pixels or HOG | Gray plus compressed color names by default (L909–L917) |
| KCF failure handling | None (§VIII-A) | `update` returns `false` and skips the update below `detect_thresh` 0.5 (L353–L357) |
| MOSSE learning rate | 0.125 (§3.4) | 0.2 (`mosseTracker.cpp` L32) |
| MOSSE PSR | Sidelobe excludes $11\times11$ around the peak; about 7 at failure | Whole-map mean and deviation; threshold 5.7 (L33, L104–L109) |

Convention finding (constructed check, recomputed): with the $e^{-2\pi ikt/n}$ DFT
used by NumPy and OpenCV and the shift direction of KCF eq. 6, the direct ridge
solution is reproduced by $\hat x\odot\hat y/(\hat x^*\odot\hat x+\lambda)$; eq. 12
transcribed literally yields the time-reversed filter. The note states that the
conjugate's position depends on the DFT sign convention and shift direction and gives
a unit test. This is a convention dependence, not a claimed error in the paper.

## Reference depth

Body word counts (whitespace tokens, front matter excluded, H1 included, before the
first per-card appendix): 492 → 3,472.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Input windows and features per method, response map units, mapping to frame pixels, outputs, pipeline role (contract linked to CV-SOT) |
| Intuition | Shallow | Developed | Shifts as graded negatives; constructed 8-sample illustration with the conjugate pitfall |
| Prerequisites | Developed (two links) | Developed | Link to CV-SVD for ridge regression |
| Assumptions | Absent | Developed | Window-relative motion with constructed limits, cyclic approximation, appearance, scale, kernel compatibility; degenerate denominators, flat response |
| Procedure | Shallow | Developed | MOSSE and KCF pseudocode from §3 and Algorithm 1, purpose of each step |
| Mathematics | Shallow | Developed | MOSSE eqs. 3–5, 10–12; KCF eqs. 1–2, 12, 17, 22, 31; primal/dual tradeoff; label placement; FFT scaling; PSR; worked examples A and B |
| Parameters | Shallow | Developed | Table of paper values and OpenCV defaults with effects; tuning approach |
| Properties | Shallow | Developed | Exactness for the virtual set, translation only, kernel gain by feature type (Table I), illumination, adaptation, PSR invariance |
| Cost and implementation | Shallow | Developed | Complexities, reported speeds with conditions, OpenCV `TrackerKCF` and legacy `TrackerMOSSE` contracts, CSRT pointer, execution status |
| Evaluation | Shallow | Developed | KCF's metric choice and its bias, baseline with PSR-gated update as the controlled variation, measurement limits |
| Failure modes and diagnosis | Shallow | Developed | Eight-row symptom table including conjugate, label and FFT-scaling bugs |
| Alternatives and sources | Shallow | Developed | Conditional choices, industrial uses labelled as project reasoning, scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/114-mosse-kcf.py`](checks/114-mosse-kcf.py) (8 checks): direct versus DFT
ridge solution on 8 samples; time-reversed filter with the misplaced conjugate (peak at
index 6, 0.788, instead of index 0, 0.954); peak at $-s \bmod n$ for a shift $s$; PSR 6
for the card example; PSR 8.0 with exclusion versus 6.2 over the whole map; affine
invariance; representable and inside-the-window displacements for paddings 1, 2 and 2.5.

## Applied corrections

- [Reference](../../../vault/110-tracking-association/references/114-mosse-kcf.md),
  revision 5 → 6: body rewritten as above; appendix language fixes identical to the
  card fixes ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "From the pic to the image" → "From the peak to the image",
  "Separate research and learning" → "Separate search and learning", "core" →
  "kernel", "medium" → "support", "allows to compare the compromises" → "makes it
  possible to compare tradeoffs"); KCF links moved to the v3 HTML that was read;
  Appendix "F" named A-F; sources split; closing line replaced.
- [Cards](../../../vault/110-tracking-association/114-mosse-kcf.md): expected answers of
  002 and 003 as quoted above; further explanations of 002 and 003 extended with one
  sourced condition each; language fixes in all five cards, including blocking errors
  ("Update without check on any predicted box" → "Updating the model on every predicted
  box without a check", "Interpret PSR=6 as 60 % confidence" → "Interpreting PSR $=6$
  as 60% confidence"); all Source lines given exact sections. IDs, questions,
  objectives, families, tags and target deck unchanged.

No card of another subject repeats a corrected claim (`rg` for PSR, `horspic` and
decimal commas in `vault/`).

## Proposals

To register as `pending` (register not edited in this pass):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-CORRELATION-01 | CV-CORRELATION | Name the unit tests that validate a correlation-filter implementation before any video run: filter on its own training patch peaks at zero shift; a known shift $s$ moves the peak to $-s \bmod n$; Fourier and direct solves agree on a small case; label at the top-left element | Convention bugs (conjugate, label placement, wrap-around, FFT scaling) are untested by any card and produce plausible but wrong tracking | Practice; Mathematics and Failure modes | 1 card, 3–4 criteria | [KCF eqs. 6–12 and App. A-A](https://arxiv.org/html/1404.7584v3); checks/114-mosse-kcf.py |

No defective question was found.

## Sources

Scientific sources, read at the passages listed (texts extracted locally):

- Bolme et al. 2010, [MOSSE PDF](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf): abstract, §3 introduction, §§3.1–3.5, Figs. 3–4, §4.2, §4.3.
- Henriques et al. 2015, [KCF arXiv HTML v3](https://arxiv.org/html/1404.7584v3): §IV-A to §IV-E, §V-A to §V-C, §VI-A to §VI-C, §VII-A, §VII-B, §VIII-A to §VIII-C, Appendix A-A, A-F, Tables I–II.
- Wu, Lim and Yang 2013, [OTB](https://openaccess.thecvf.com/content_cvpr_2013/papers/Wu_Online_Object_Tracking_2013_CVPR_paper.pdf): §4 (card 005 source).
- Kristan et al. 2016, [VOT methodology](https://arxiv.org/abs/1503.01313): §3.1 (card 005 source).

Implementation sources (opencv_contrib at tag 4.13.0):
[`tracking.hpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/include/opencv2/tracking.hpp) L31–L149;
[`trackerKCF.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/trackerKCF.cpp) L195–L225, L330–L400, L430–L460, L900–L918;
[`mosseTracker.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/mosseTracker.cpp) L31–L230.

Not verifiable or not used: docs.opencv.org (HTTP 403); Context7 unavailable. The
CSRT paper was not read; the note only points to the OpenCV class.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/114-mosse-kcf.py` | 8 checks passed |
| `git diff --check -- vault/110-tracking-association/` | No whitespace error |
| Inventory of the card file | 5 cards, 379 / 452 / 447 / 354 / 286 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical (41); front matter identical except `revision`; H1 and `### CV-…` headings unchanged; `$` balanced |

No tracker was executed; the baseline and variation are proposed. Obsidian and
AnkiDroid rendering are unverified. Agent self-review, without independent validation
or measured learner proficiency. Export status: **to republish with `paquet-anki`**.

For the coordinator (shared files not edited): correction-log entry for
`Suivi-pilote.md` — 2026-11-14, CV-CORRELATION revision 6, cards 001–005, corrections
above, Agent Claude Code self-review, to republish with `paquet-anki`; proposal
P-CV-CORRELATION-01.
