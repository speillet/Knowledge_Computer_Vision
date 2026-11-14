# Review — SIFT — local features and multiscale descriptors — 2026-11-14

## Overview

7 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 1 important, 6 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The note now develops the full method (scale space, localization, edge test,
orientation, descriptor, ratio test) and the OpenCV 4.13 implementation contract.
Binary alternatives, nearest-neighbor indexes and pipeline comparison are linked to
[CV-FAST-BRIEF](../../../vault/40-features-matching/references/47-fast-brief.md),
[CV-ORB](../../../vault/40-features-matching/references/42-orb.md),
[CV-FLANN](../../../vault/40-features-matching/references/48-flann.md) and
[CV-MATCHING](../../../vault/40-features-matching/references/43-detecteurs-matchers.md).
The trailing section is now titled "Sources", so `#sources` resolves in the note.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SIFT-001 | SIFT gives keypoints and descriptors; matching, filtering and geometry are separate: confirmed (Lowe §1, §7). "misconstraint extrapolation", "A piece in relief", "Maintaining these associations of indices" | Understanding: separates representation from estimation | 3 expected criteria; 410 → 408 lexical words | Aligned with the reference data contract | Minor | Language fixes; Source line given exact sections |
| CV-SIFT-002 | DoG of neighboring smoothings, extremum across scale, 26 neighbors: confirmed (Lowe §3, eq. 1; §3.1). DoG ≈ $(k-1)\sigma^2\nabla^2G$: confirmed (§3). "eight in his level", "a scale development", "implies a suitable spacing" | Reasoning: characteristic scale | 2 expected criteria; 421 → 423 lexical words | Aligned with worked example A | Minor | Language fixes; Source line adds IPOL §2–§3 |
| CV-SIFT-003 | Orientation, 4×4×8 = 128, normalize–clip–renormalize: confirmed (Lowe §5, §6.1). "subtracting a constant ... does not already change", "crush", "distinguish then undetected keypoint" | Algorithm: descriptor construction | 3 expected criteria; 383 → 386 lexical words | Consistent with the reference mathematics | Minor | Language fixes; Source line given exact sections |
| CV-SIFT-004 | 20/21 rejected and 35/80 kept at 0.8: recomputed; ratio test and its operating point confirmed (Lowe §7.1, Fig. 11). Expected answer used French decimal commas ("0,952", "0,4375") and the explanation "0,8", "0,894"; "the query mischaracterizes the two", "when the search is approached" | Practice: compute and interpret the ratio | 2 expected criteria; 400 → 402 lexical words | Aligned with worked example D | Minor | Decimal fix in the expected answer; language fixes; Source line adds IPOL §5 |
| CV-SIFT-005 | Rotation normalized, oblique view not compensated by rotation and scale: confirmed (Lowe §6.1, §6.3). Missing measured limit for the comparison objective: matching above 50% only to about 50° tilt (§6.3, Fig. 9) | Comparison: limits of invariances | 2 expected criteria; 411 → 424 lexical words | Aligned with the reference properties | Minor | One sentence added with Lowe's measured limit; language fixes ("projection of the plan", "Example built") |
| CV-SIFT-006 | Repetition can produce a consistent but shifted consensus; independent evidence needed: consistent with Lowe §7 and IPOL §5 (ratio test omits repeated structures). "same motive", "Ambiguity to several solutions", "motion marker" | Diagnosis: misleading consensus | 2 expected criteria; 387 → 385 lexical words | Aligned with the failure table | Minor | Language fixes; Source line given exact sections |
| CV-SIFT-007 | Compare on the same pairs and full cost: consistent with Lowe §6.2–§6.4 and Rublee et al. §4.4, §6.1. Expected answer ended with "Set to validation and then freeze for the test", unintelligible; explanation said "A ratio of players" for an inlier ratio and "Laminate by rotation" for stratify | Evaluation: product comparison | 3 expected criteria; 386 → 395 lexical words | Aligned with the reference evaluation section | Important | Meaning-restoring fix of the expected answer; language fixes |

Expected-answer changes (meaning-restoring language fixes):

- CV-SIFT-004: "($20/21\approx0,952$) ... ($35/80=0,4375$)" → "($20/21\approx0.952$) ...
  ($35/80=0.4375$)".
- CV-SIFT-007: "Set to validation and then freeze for the test." → "Tune on
  validation, then freeze the settings for the test."

## Reference findings

Claims of revision 8 checked against their passages:

- DoG definition, $k=2^{1/s}$, 26 neighbors, localization, low-contrast and edge
  rejection, orientation, $4\times4\times8$ descriptor with normalization and clipping,
  ratio test: confirmed (Lowe §§3–7.1).
- "Lowe's historical threshold of 0,8 depends on his experiences": correct in substance
  (§7.1 gives its measured operating point); French decimal fixed.
- "API OpenCV 4.13 checked": not reproducible in this session (Context7 unavailable,
  docs.opencv.org HTTP 403); replaced by citations of the 4.13.0 sources.
- The "proposed controlled variation" rotated, scaled and blurred in turn, which is a
  sweep of conditions rather than one controlled variation (FR-033); replaced.
- Mistranslations: "Driver input" (pilot input), "Explained mathematics", "Cas
  industriel", "material speed gain" (hardware), "image experience" (experiment),
  "digital performance" (numerical), "Discriminant verification".
- No scientific error was found.

New claims verified for revision 9 (main ones):

- Lowe 2004: §3 (eq. 1, diffusion-equation derivation, $s+3$ images, octave
  resampling), §3.1 (arbitrarily close extrema), §3.2 (protocol, Fig. 3, $s=3$), §3.3
  (Fig. 4, $\sigma=1.6$, input blur 0.5, doubling ×4 keypoints), §4 (eqs. 2–3, 0.5 offset
  rule, $|D|<0.03$, Fig. 5 counts), §4.1 (eq. 4, $r=10$, negative determinant), §5 (36
  bins, 1.5σ, 80%, 15% multiple orientations, Fig. 6 noise result), §6.1 (Gaussian
  window half the width, 4-sample shift, trilinear interpolation, affine
  illumination invariance, 0.2), §6.2 (Fig. 8, larger descriptors can hurt), §6.3 (50°,
  Harris-affine 40% at 70°, Pritchard and Heidrich), §6.4 (Fig. 10), §7.1 (0.8: 90% of
  false matches removed, under 5% of correct ones lost, test conditions), §7.2 (BBF,
  200 candidates, two orders of magnitude, under 5% loss).
- IPOL 2014: $C_\text{DoG}=0.015$ relative to $n_\text{spo}=3$ and its $(2^{1/n}-1)$
  scaling, 80% prefilter, $C_\text{edge}=10$ (§3.3); relative-threshold drawback on
  repeated structures and $c\,N_AN_B$ cost (§5); parameter tables, negligible impact
  of $C_\text{edge}$, flat orientation histogram on isotropic structures, demo ratio
  0.6 (§6).
- Mikolajczyk and Schmid 2003: ROC criterion with 3 px and 30% overlap (§3.3); SIFT
  best except under light changes (Discussion and Conclusions).

Disagreements between the paper and OpenCV 4.13.0 (FR-036):

| Aspect | Lowe 2004 | OpenCV 4.13.0 |
| --- | --- | --- |
| Contrast threshold | $|D(\hat{\mathbf x})|<0.03$ on [0, 1] (§4) | `contrastThreshold / nOctaveLayers`, default $0.04/3=0.0133$; header advises 0.09 for Lowe's value (`sift.simd.hpp` L372–L376; `features2d.hpp` L276–L281) |
| Image doubling | Linear interpolation (§3.3) | Default `INTER_LINEAR` path; constructed derivation gives a +0.25 px bias, consistent with the library's own log message; optional precise path (`sift.dispatch.cpp` L191–L209, L480–L482; `resize.cpp` L4101) |
| Descriptor values | Unit vector after clipping (§6.1) | $512\times$ unit vector, rounded and saturated to [0, 255], even for `CV_32F` (`sift.simd.hpp` L947–L1001) |
| Feature budget | Not applicable | `retainBest(nfeatures)` runs before the mask filter (`sift.dispatch.cpp` L556, L570–L571) |
| Edge boundary | Keep if ratio $<(r+1)^2/r$ (§4.1) | Reject if $\operatorname{Tr}^2r\ge(r+1)^2\operatorname{Det}$ or $\operatorname{Det}\le0$ (L385): same rule, boundary rejected |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 847 → 3,957.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task; input depth and color handling; `KeyPoint` fields and units; descriptor type, scale and norm; frame contract; pipeline roles |
| Intuition | Shallow (merged with procedure) | Developed | Scale selection, edge rejection, local frame, shift-tolerant histograms; constructed label illustration; Mermaid pipeline |
| Prerequisites | Shallow (one link) | Developed | Links by mechanism to CV-FILTRES, CV-CORNERS, CV-SVD, CV-FLANN, CV-HOMOGRAPHIE |
| Assumptions | Shallow (bullets) | Developed | Similarity-like changes with Lowe's 50° result, linear photometry, texture, rigid verification; observability (close extrema, edges, isotropic orientation); degenerate cases |
| Procedure | Shallow (numbered list) | Developed | Pseudocode faithful to Lowe and OpenCV; purpose of eight steps |
| Mathematics | Shallow | Developed | Scale space and DoG derivation, localization equations, edge ratio, orientation, descriptor and normalization, ratio test with its measured operating point; worked examples A (sampling), B (edge test), C (contrast conventions), D (ratio and distance units), E (upsampling bias) |
| Parameters | Shallow (one bullet) | Developed | Ten-row table with paper, IPOL and OpenCV values; `nfeatures`/mask interaction; five-step tuning approach |
| Properties | Shallow | Developed | Covariance and noise results, illumination, viewpoint, distinctiveness and database size, descriptor ranking, ratio-test limits |
| Cost and implementation | Shallow | Developed | Cost terms with variables (pyramid samples, per-keypoint supports, matching, BBF); OpenCV 4.13 contracts; corrected illustrative snippet marked not executed |
| Evaluation | Shallow | Developed | Lowe's synthetic protocol, repeatability, descriptor ROC, end-to-end; baseline and one controlled variation (precise upscale) with confound; measurement limits |
| Failure modes and diagnosis | Shallow (three rows, no remedy column) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices; industrial uses labelled as project reasoning; "Sources" split into scientific and implementation sources |

Constructed examples are recomputed by [`checks/41-sift.py`](checks/41-sift.py)
(20 assertions): $k=1.2599$, blur ladders and incremental blurs, initial blurs 1.249
and 1.520, 9 octaves; edge bound 12.1 with ratios 12 and 8; contrast conventions
(0.0133, factor 2.25, 0.09; IPOL scaling 0.728 and 0.471 against 0.75 and 0.5); ratio
examples, $\sqrt{0.8}=0.894$, OpenCV distance scale (724, 204.8); +0.25 px upsampling
bias; tilt anisotropy (1.56, 2.00, 2.92); descriptor geometry (128, 12σ, 6σ, 21 px);
pyramid size (~32 $WH$) and exhaustive matching cost (512 million).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/41-sift.md), revision 8
  → 9: body rewritten and deepened. Appendix language fixes, applied identically to
  the cards: "Question of work" → "Working question", "Reference Response" →
  "Reference answer", CV-SIFT-007 reference answer as in the card, "calculate the
  candidates" → "compute the candidates", "misconstraint extrapolation to the other
  edge" → "leave the extrapolation to the opposite edge poorly constrained", "check a
  geometry on points not used for its adjustment" → "Check the geometry on points not
  used to fit it", "A piece in relief" → "A part with relief", "business-related, such
  as an inspection region offset from the fault" → "a business quantity, such as the
  offset of an inspection region relative to the defect", "Two methods at residuals
  mean neighbors" → "Two methods with similar mean residuals", "compromise" →
  "tradeoff", "tables" → "arrays", "Maintaining these associations of indices" →
  "Keeping these index associations", "Why DoG is Approaching a Laplacian" → "Why the
  DoG approximates a Laplacian", "a scale development" → "a first-order expansion in
  scale", "does not already change" → "does not change ... in the first place",
  "crush" → "swamp", "0,8"/"0,894" → "0.8"/"0.894", "which convention uses a particular
  API" → "which convention a particular API uses", "couple" → "pair", "the base" →
  "the database", "Example built" → "Constructed example", "Ambiguity to several
  solutions" → "Ambiguity with several solutions", "motion marker" → "motion prior",
  "A ratio of players" → "An inlier ratio", "quality-cost boundary" → "quality–cost
  frontier". The trailing section became "## Sources" with scientific and
  implementation subsections; the reference-style link definitions were replaced by
  inline links; a provenance line was added. Front matter unchanged except `revision`;
  H1 and per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/41-sift.md): the two expected-answer
  changes quoted above; the appendix fixes; further-explanation fixes "the
  description represents" → "the descriptor represents", "We can use distance L2" →
  "A typical chain uses the L2 distance", "eight in his level" → "eight in its
  level", "Why the scale intervenes" → "Why scale matters", "distinguish then
  undetected keypoint" → "distinguish an undetected keypoint", "Case built for
  adjustment" → "Constructed tuning case", "hardening the threshold ... dots" →
  "tightening the threshold ... points", "when the search is approached" → "when the
  search is approximate", "projection of the plan" → "projection of the plane", "same
  motive" → "same motif", "Laminate" → "Stratify", "another material" → "other
  hardware"; blocking errors rewritten as gerunds. CV-SIFT-005 gains one sentence with
  Lowe's measured 50° limit. All seven Source lines now cite exact sections (Lowe,
  IPOL, Rublee). Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault subject repeats a claim corrected here (`rg -n -i "sift|ratio test"
vault/`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SIFT-01 | CV-SIFT | Explain why SIFT discards a DoG extremum lying on an edge and apply the trace–determinant test to a given curvature ratio | Edge rejection untested; first proposed in the [2026-10-18 report](../2026-10-18/41-sift.md) but never registered | Reasoning; Mathematics, worked example B | 1 card, 3 criteria | [Lowe 2004, §4.1](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) |
| P-CV-SIFT-02 | CV-SIFT | A pipeline moved from Lowe's or IPOL's SIFT to OpenCV keeps "the same" contrast threshold and distance threshold and changes behavior: identify the two conventions that differ and how to transfer each | Implementation conventions (contrast scaling by layers, $512\times$ descriptors) untested | Diagnosis; Cost and implementation, worked examples C and D | 1 card, 3 criteria | [IPOL §3.3](https://doi.org/10.5201/ipol.2014.82); [OpenCV 4.13.0 `sift.simd.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/sift.simd.hpp#L292-L396) |

No question was found defective.

## Sources

Scientific sources, opened at the passages listed (text extracted with `pdftotext`):

- Lowe 2004, [author PDF](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf): §§3–7.2.
- Rey-Otero and Delbracio 2014, [IPOL article PDF](https://www.ipol.im/pub/art/2014/82/article.pdf)
  ([DOI](https://doi.org/10.5201/ipol.2014.82)): §2.2, §3.3, §5, §6.
- Mikolajczyk and Schmid 2003, [HAL inria-00548227](https://inria.hal.science/inria-00548227):
  abstract, §3.3, Discussion and Conclusions. The 2005 PAMI version was not opened.
- Rublee et al. 2011, course-hosted copy of the ICCV paper (canonical
  [DOI](https://doi.org/10.1109/ICCV.2011.6126544)): section list, §4.4 opening (card
  CV-SIFT-007 source retained).

Implementation sources (official code at tag 4.13.0):

- [`features2d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp): L266–L330, L1255–L1280.
- [`sift.dispatch.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/sift.dispatch.cpp): L144–L221, L224–L310, L368–L402, L474–L590.
- [`sift.simd.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/sift.simd.hpp): L84–L127, L292–L396, L538–L563, L709–L1032.
- [`resize.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp): L4096–L4108.
- [`core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp): L180–L205.

Failed accesses and limits:

- docs.opencv.org/4.13.0 matching tutorial not re-read (HTTP 403); link retained as not
  re-read.
- Context7 was not available in this session.
- The +0.25 px bias is derived from the code and the library's log message; it was not
  measured.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/41-sift.py` | 20 checks passed |
| `git diff --check` on this subject's files | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/41-sift.md` | 7 cards, 385–424 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 8` → `9`; H1 and per-card headings unchanged; `$$` balanced |

No SIFT extraction or matching was executed; the snippet is illustrative and the
proposed baseline and variation are protocols, not results. Obsidian and AnkiDroid
rendering are unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-SIFT revision 9, CV-SIFT-001 to 007, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-SIFT-01, P-CV-SIFT-02).
