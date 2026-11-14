# Review — Intensity-based registration and ECC — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for direct, intensity-based parametric alignment.
The primary paper (Evangelidis and Psarakis, TPAMI 2008) was not readable in this
pass: every open copy found was blocked. The note therefore quotes only its abstract,
takes the update equations from the OpenCV 4.13 implementation that cites it, checks
them numerically, and uses Baker and Matthews' Lucas–Kanade framework (CMU-RI-TR-02-16)
for the Gauss–Newton structure, cost and evaluation protocol.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ECC-001 | Area-based alignment that updates an initial warp, versus features then robust geometry: confirmed (tracking.hpp L352–L360). Normalized criterion invariant to a positive gain and an offset: confirmed algebraically (check 1) and by the abstract ("invariant with respect to photometric distortions"). "Convergence pool" for *basin*, "cover" for overlap, "medium" for support, "Standardized Criteria"; expected answer "SIFT offers pairs and then a robust geometry" was unclear | Comparison: direct versus feature-based registration contract | 2 expected criteria; 354 → 358 lexical words | ID, question, tags unchanged; wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line moved from the blocked docs page to the 4.13.0 header and the paper abstract |
| CV-ECC-002 | Several optima on a periodic pattern; convergence is not identifiability: confirmed as a property of a local optimizer (Baker and Matthews §2.1 local increments; OpenCV stops on the change of $\rho$, ecc.cpp L519–L520). "Validation construite" left in French; "reserved points", "sense of warp", "media size", "test separate initializations of a period" obscured the meaning | Diagnosis: separate optimization from identifiability | 2 expected criteria; 362 → 373 lexical words | Aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer ("reserved" → "held-out", "movement" → "motion"); language fixes; Source line given code lines and the canonical-point protocol |
| CV-ECC-003 | Parameter counts 2/3/6/8: confirmed (tracking.hpp L321–L329). Richer models can be less stable: supported by conditioning (worked example E) and cost $O(n^2N)$ (Baker and Matthews §2.4). Expected answer "over-adjust … while translation or affine is sufficient as needed" obscured the meaning (*overfit*, *when*) | Practice: choose a motion model | 2 expected criteria; 358 → 367 lexical words | Aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |

Expected-answer changes (meaning-restoring language fixes):

- CV-ECC-001: "ECC optimizes an intensity criterion on an initialized warp; SIFT offers
  pairs and then a robust geometry." → "ECC optimizes an intensity criterion on an
  initialized warp; SIFT proposes point pairs, from which a robust estimator computes
  the geometry."
- CV-ECC-002: "Compare to reserved points/structures and movement constraints; the
  correlation can have several maxima." → "Compare with held-out points or structures and
  with motion constraints; the correlation can have several maxima."
- CV-ECC-003: "More parameters can over-adjust or reduce stability while translation or
  affine is sufficient as needed." → "More parameters can overfit or reduce stability
  when a translation or an affine model is sufficient for the need."

## Reference findings

Claims of revision 6 checked:

- ECC aligns by optimizing a photometric criterion under a motion model from an
  initialization: confirmed (tracking.hpp L337–L360).
- Correlation unchanged under a positive gain and an offset on a fixed, non-constant
  support: confirmed algebraically (check 1).
- "Specify the meaning of the warp and the use of its reciprocal": confirmed and made
  precise: the matrix maps template to input coordinates, and the header recommends
  `WARP_INVERSE_MAP` to bring the input into the template frame (L340–L358).
- A pyramid can enlarge the basin: plausible and shown on a constructed 1-D signal
  (worked example C); OpenCV builds no pyramid (ecc.cpp, no pyramid call), and Baker and
  Matthews' convergence results are explicitly without a pyramid (§3.4.3).
- No scientific error in revision 6; sections held one to three sentences; translation
  defects ("Question of work", "Reference Response", "Comparison built", "Validation
  construite", "medium", "cover", "Convergence pool", "Standardized Criteria", "reverse
  warping").

New claims verified for revision 7 (main ones), in OpenCV 4.13.0:

- Inputs: depth `CV_8U`, `CV_16U`, `CV_32F` or `CV_64F`, 1 or 3 channels, same type for both
  images; `warpMatrix` must be `CV_32FC1` (StsUnsupportedFormat otherwise); identity if
  empty; homography requires 3 rows; third row ignored for other models.
- `computeECC` definition with per-channel means over the mask; `findTransformECCWithMask`
  (template and input masks, intersection, default $\varepsilon=10^{-6}$) alongside
  `findTransformECC` (default 50 iterations, $\varepsilon=0.001$, `gaussFiltSize=5`).
- Internals: float conversion and Gaussian blur of both images, central-difference
  gradients $(-0.5,0,0.5)$, mask threshold–blur–erosion, `INTER_LINEAR + WARP_INVERSE_MAP`
  warping, statistics on valid pixels, Jacobians per model (affine row
  $(xI_x,xI_y,yI_x,yI_y,I_x,I_y)$ on raw pixel indices), float32 Hessian, $\lambda$,
  additive update, stopping on $|\rho_k-\rho_{k-1}|$, exceptions for NaN and for a
  non-positive $\lambda$ denominator, and a returned $\rho$ computed before the last update.
- Gaussian standard deviation from kernel size: $0.3((k-1)/2-1)+0.8$, so 1.1 px for $k=5$
  (imgproc.hpp L1468–L1470).

From Baker and Matthews (CMU-RI-TR-02-16): forward additive Lucas–Kanade (eqs. 3–5),
Gauss–Newton derivation and Hessian (§2.2), requirement of differentiable warps (§2.3),
cost $O(n^2N+n^3)$ per iteration (§2.4), inverse compositional cost $O(nN+n^3)$ with a
precomputed Hessian (§3.2.4), and the canonical-point convergence protocol with its
results (§3.4.1–§3.4.4).

Paper–implementation relation (FR-036):

| Aspect | Paper (abstract only) | OpenCV 4.13.0 |
| --- | --- | --- |
| Schemes | Forward additive and inverse compositional versions | Forward additive only |
| Per-iteration step | "Closed form solution (per iteration)"; exact form not read | $\Delta\mathbf p=H^{-1}G^\top(\lambda\mathbf t-\mathbf i)$ with $\lambda$ as in the note (ecc.cpp L571–L607), verified to maximize the linearized correlation (check 3) |
| Non-positive $\lambda$ denominator | Not verifiable | Exception `StsNoConv` (L593–L598) |
| Smoothing, masks, colour | Not verifiable | Gaussian blur of size `gaussFiltSize`; eroded masks; 3-channel support |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 324 → 4,001. The length comes from deriving the update, documenting the
OpenCV contract that replaces the unreadable paper, and five worked examples.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task with photometric model; OpenCV data contract (types, channels, matrix shape and direction, masks, return, units); display convention; pipeline roles |
| Intuition | Shallow | Developed | ECC versus SSD as a criterion, $\lambda$ as an estimated gain; constructed label illustration; Mermaid diagram of the OpenCV iteration with its exceptions |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-SVD, CV-FLOT, CV-SIFT, CV-MATCHING, CV-MATCH-APPRIS, CV-ICP by mechanism |
| Assumptions | Shallow | Developed | Photometric and geometric models, local initialization, observability (aperture, periodicity), overlap; degenerate cases tied to OpenCV exceptions |
| Procedure | Shallow | Developed | Pseudocode with caller-side pyramid and purpose of each step |
| Mathematics | Shallow | Developed | Criterion and normalized-SSD identity; linearization and Jacobians; OpenCV step with $\lambda$ and its Lucas–Kanade comparison; stopping rule and returned value; worked examples A–E |
| Parameters | Shallow | Developed | Parameter table with 4.13 defaults and interactions; four-step tuning approach |
| Properties | Shallow | Developed | Scope of photometric invariance and multimodal limit; local convergence; cost; score versus accuracy; paper results stated as the abstract gives them |
| Cost and implementation | Shallow | Developed | Cost drivers; OpenCV 4.13 contracts with line numbers; errors; illustrative, unexecuted Python call |
| Evaluation | Shallow | Developed | Baker–Matthews canonical-point protocol and results; baseline and pyramid variation with a blur confound control; measurement limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Eight-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (features with RANSAC, inverse compositional, phase correlation, optical flow, ICP); industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/45-recalage-ecc.py`](checks/45-recalage-ecc.py) (9 checks): photometric
invariance and $\rho=-1$ for a negative gain; the normalized-SSD identity $2-2\rho$; the
closed-form step as a local maximum of the linearized correlation on a random instance;
$\lambda=1.5$ and a zero ECC step against a $-0.157$ px SSD step at the true alignment;
1-D capture ranges of 7.75 px ($\sigma=3$) and 12.75 px ($\sigma=6$) with failure through a
non-positive $\lambda$ denominator; Gaussian $\sigma$ of 1.1 px and 2.6 px for kernels of 5 and
15; warp transfer $S H_c S^{-1}$ between pyramid levels; and the lever-arm ratio 369 for a
640-px template. The 1-D simulations were executed by that script (Python standard
library); they are constructed signals, not image experiments.

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/45-recalage-ecc.md),
  revision 6 → 7: body rewritten and deepened as above. Appendix language fixes, applied
  identically to the matching card text: "Question of work" → "Working question",
  "Reference Response" → "Reference answer", "offer transformation" → "provide a
  transformation", "the cover" → "the overlap", "two views close to a label" → "two nearby
  views of a label", "a large move" → "a large motion", "motion pattern" → "motion model",
  "non-constant medium" → "non-constant support", "a occlusion" → "an occlusion",
  "Comparison built" → "Constructed comparison", "installation … planned movement" →
  "setup … expected motion", "adjust" → "fit", "reserved points" → "held-out points",
  "admitted error" → "tolerated error", "Understanding the Standardized Criteria" →
  "Understanding the normalized criterion", "Valid media and hidden pixels" → "Valid
  supports and masked pixels", "Report media size" → "Report the support size", "plane
  Euclidean movement" → "planar Euclidean motion", "imposes on the contrary" → "instead
  imposes", "reverse warping" → "inverse warping". Sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/45-recalage-ecc.md): the three expected
  answers as quoted above; further explanations and blocking errors corrected as in the
  appendix, plus "Origin of Ambiguity" → "Origin of the ambiguity", "A translation of a
  period" → "A translation by one period", "Validation construite" → "Constructed
  validation", "eventually enhance" → "may improve", "Take digital convergence as
  physical truth" → "Taking numerical convergence as physical truth", "Assimilate maximum
  flexibility and maximum precision" → "Equating maximum flexibility with maximum
  precision". Source lines now cite the OpenCV 4.13.0 header or source at line level,
  the ECC abstract and Baker and Matthews instead of the blocked documentation page.
  Questions, IDs, objectives, families, tags and target deck unchanged.

`rg -n "findTransformECC|ECC" vault` finds ECC only in this subject, the matching index
and the progress tables; no other card repeats a corrected claim.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (shared file, not
edited here). P-CV-ECC-01 carries forward the 2026-10-20 proposal "Write the warp
convention returned", which was never registered.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ECC-01 | CV-ECC | Given a `findTransformECC` result, state which frame the matrix maps from and to, and which flag brings the input into the template frame; predict the visible error if the flag is omitted | The warp direction, a frequent practical error, is tested by no card | Practice; Problem and data contract | 1 card, 2 criteria | [OpenCV 4.13.0 tracking.hpp L337–L360](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp) |
| P-CV-ECC-02 | CV-ECC | Explain what the ECC update does with a global gain (the template scaled by $\lambda$) and why SSD-based Lucas–Kanade can be biased by the same change | The core mechanism that distinguishes ECC from Lucas–Kanade is not trained | Algorithm; Mathematics, worked example B | 1 card, 3 criteria | [OpenCV 4.13.0 ecc.cpp L571–L607](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/ecc.cpp); [Baker and Matthews §2.2](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf) |

No defective question was found.

## Sources

Scientific sources:

- Evangelidis and Psarakis 2008, TPAMI 30(10):1858–1865, [DOI 10.1109/TPAMI.2008.113](https://doi.org/10.1109/TPAMI.2008.113):
  abstract read through the Semantic Scholar API record. **Full text not verifiable**:
  the HAL deposit (inria.hal.science/hal-00864385) answered with a bot-protection page,
  scispace/typeset.io and core.ac.uk returned 403, and the author page did not load. The
  VISAPP 2008 companion paper ("Projective image alignment by using ECC maximization",
  SciTePress) was readable only on its first page (abstract and introduction).
- Baker and Matthews, "Lucas-Kanade 20 Years On: A Unifying Framework: Part 1",
  [CMU-RI-TR-02-16](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf)
  (PDF text extracted with `pdftotext`): §1, §2.1–§2.4, §3.2.4, §3.4.1–§3.4.4.

Implementation sources (official code at tag 4.13.0):

- [`modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): L263–L420.
- [`modules/video/src/ecc.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/ecc.cpp): L50–L630.
- [`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L1458–L1470, L1555–L1575, L3016–L3068.

Failed accesses and limits:

- docs.opencv.org/4.13.0 returned HTTP 403; the retained module-page links in the
  2026-10-30 and 2026-11-08 appendices were not re-read.
- Context7 was not available in this session.
- Not verified: the OpenCV sample `image_alignment.cpp`, and any claim about the
  ECC paper's experiments, its second $\lambda$ case or its convergence results. Mutual
  information is named as an alternative without verification.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (after rewording one line that the validator read as a link definition) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/45-recalage-ecc.py` | 9 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/40-features-matching/45-recalage-ecc.md` | 3 cards, 358–373 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 25 protected card lines identical; front matter identical except `revision: 6` → `7`; H1 and 6 per-card headings unchanged; `$`, `$$` and fences balanced |

No OpenCV call or image experiment was executed; the Python snippet is illustrative and
the proposed baseline is a protocol, not a result. Mermaid and tables were not rendered
in Obsidian; AnkiDroid rendering is unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-ECC revision 7,
CV-ECC-001 to -003, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-ECC-01, P-CV-ECC-02).
