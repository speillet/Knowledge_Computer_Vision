# Review — Filters, gradients and pyramids — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for neighbourhood operators. Its title promised
gradients, but revision 7 had no derivative kernel; revision 8 adds Sobel, Scharr,
the Laplacian and derivative-of-Gaussian reasoning. Canny and Hough stay in
[CV-CANNY-HOUGH](../../../vault/30-traitement-image/references/32-canny-hough.md) and
sampling theory in
[CV-ACQUISITION](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FILTRES-001 | Median rejects impulses by rank; Gaussian averages: confirmed (Tomasi and Manduchi, Introduction; OpenCV 4.13 `medianBlur`); mean 36.7 and median 10 recomputed. Expected answer "while the Gaussian average" was ungrammatical (French *tandis que le Gaussien moyenne*); "compare multiple media" (*médianes*), "does not describe itself as a linear convolution" | Comparison: choose an operator from the noise model and the structure to keep | 1 criterion; 384 → 398 lexical words | Consistent with the reference noise-variance derivation | Minor | Meaning-restoring fix of the expected answer; language fixes; Source replaced (unreachable tutorial) by `imgproc.hpp` and the authors' bilateral summary |
| CV-FILTRES-002 | $\sigma_r'=\sigma_r/255$ and the affine case $\sigma_r'=\lvert\alpha\rvert\sigma_r$: confirmed by derivation and consistent with "insensitive to overall additive changes" (Tomasi and Manduchi, The Gaussian Case); 0.0784 and 0.0392 recomputed. "Record beach and color space" (*plage* = range), French decimal commas | Reasoning: keep parameters in the units of the data | 2 criteria; 385 → 385 lexical words | Consistent with reference worked example B | Minor | Language fixes; Source adds the authors' summary and `bilateralFilter` |
| CV-FILTRES-003 | PSNR definition and the $p\,a^2$ contribution: confirmed by derivation. Expected answer "with reserved images" (*réservées* = held-out); "rebuild gain", "bottom area", "decisive for the trade" (*métier*), "Proposed experience". Source line "built scarcity example", "consult the 2026-10-30" garbled | Diagnosis: evaluate a filter by the task it serves | 2 criteria; 363 → 369 lexical words | Consistent with the reference evaluation section | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line rewritten |
| CV-FILTRES-004 | Blur before decimation prevents aliasing: confirmed (Burt and Adelson, Gaussian Pyramid Generation; OpenCV `pyrDown`); 8 → 1 px and radius 5 → 40 px recomputed. "A five-ray window", "Consequences for Matching", "reduced calibration target" | Understanding: link prefiltering, scale and coordinates in a pyramid | 1 criterion; 369 → 368 lexical words | Consistent with CV-ACQUISITION worked example C | Minor | Language fixes; Source replaced by Burt and Adelson and `pyrDown` at 4.13.0 |

Expected-answer changes (meaning-restoring language fixes, verified against the
pre-migration French text `git show b7142bb^:vault/30-traitement-image/31-filtrage-gradients.md`):

- CV-FILTRES-001: "It rejects local extreme values via order, while the Gaussian
  average; the effect depends on noise and structures." → "It rejects local extreme
  values through ranking, whereas the Gaussian averages them into the output; the
  effect depends on the noise and the structures."
- CV-FILTRES-003: "Measure defect recall and location error at relevant scale, with
  reserved images and annotations." → "Measure defect recall and localization error at
  the relevant scale, with held-out images and annotations."

Defective protected fields (not edited; objective lines are invariants):

- CV-FILTRES-002 objective "settle a bilateral in the right units" (*régler* = tune).
  Proposed: "Tune a bilateral filter in the right units."
- CV-FILTRES-003 objective "Protect a business detail." (*détail métier*). Proposed:
  "Protect a task-critical detail."

No defective question was found.

## Reference findings

Claims of revision 7 checked:

- Convolution formula, bilateral weight with $\sigma_s$ in pixels and $\sigma_r$ in
  intensity units, $\sigma_r'=\sigma_r/255$: confirmed (derivation; Tomasi and
  Manduchi, The Idea and The Gaussian Case).
- "The separable Gaussian allows two 1-D passes; a naive bilateral visits each
  neighbour of the support for each pixel": confirmed.
- "A pyramid requires proper filtering before decimation": confirmed (Burt and
  Adelson; OpenCV `pyrDown`).
- No scientific error found. The body was shallow (333 words), had no derivative
  operator despite the title, and contained mistranslations: "Median: Nonlinear order
  statistics useful for pulses", "A shade changes at the edge", "Question of work",
  "Reference Response", "Consequences for Matching", "Building the Levels", "built
  rarity example".

New claims verified for revision 8 (main ones):

- Tomasi and Manduchi (authors' summary): linear smoothing blurs edges; combined domain
  and range filtering with normalization; bilateral acts as a domain filter in smooth
  regions; Gaussian range filter insensitive to additive intensity changes; per-band
  RGB smoothing produces a "more pronounced pink and purple band"; CIE-Lab distance;
  iterated filtering gives a cartoon-like look.
- Burt and Adelson 1983: REDUCE (eq. 1), separable normalized symmetric 5-tap kernel,
  equal contribution $a+2c=2b$ with $b=1/4$, $c=1/4-a/2$, $a=0.4$ Gaussian-like
  (Fig. 2–3), $L_l=g_l-\mathrm{EXPAND}(g_{l+1})$.
- OpenCV 4.13.0: `filter2D` computes correlation and switches to DFT for kernels of
  about 11×11; Gaussian 1-D kernel and the $\sigma$-from-`ksize` rule; `ksize` from
  $\sigma$ with 3σ (8-bit) or 4σ half-widths; `medianBlur` border, depth limits and
  algorithm selection (sorting networks; `medianBlur_8u_Om`; `medianBlur_8u_O1`
  contributed by Simon Perreault); `bilateralFilter` parameter semantics, speed note
  and no in-place operation; Sobel, Scharr and Laplacian kernels, truncated derivatives
  for 8-bit `ddepth`; `BORDER_DEFAULT = BORDER_REFLECT_101`; `pyrDown`.

Implementation notes (FR-036): the derivative kernels of OpenCV are unnormalized
(gains 2, 8, 32 on a unit ramp), so gradient thresholds are implementation-specific;
`filter2D` correlation differs from mathematical convolution for antisymmetric
kernels; OpenCV's `pyrDown` kernel $[1,4,6,4,1]/16$ is the $a=0.375$ member of Burt and
Adelson's family, not their $a=0.4$ example (project observation).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 333 → 3,348. About
600 tokens are tables, the pseudocode and the Mermaid diagram. The length comes from
four operator families (linear, rank, bilateral, derivative) plus pyramids, each with
its units and library contract.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task, input types and ranges, noise assumptions, output types and sizes, coordinate and anchor conventions, downstream dependence on scale and kernel gain |
| Intuition | Shallow | Developed | One mechanism per operator family and for pyramids; constructed steel-strip illustration; Mermaid choice diagram |
| Prerequisites | Shallow (one link) | Developed | Links to CV-ACQUISITION and the notes that build on this one (CV-CANNY-HOUGH, CV-MORPHO, CV-CORNERS, CV-SIFT) |
| Assumptions | Absent (merged) | Developed | Per-operator assumptions; observability (defect versus impulse); degenerate cases ($\sigma_r$ limits, even kernels, constant images) |
| Procedure | Shallow | Developed | Eight-step pseudocode with the purpose of each step |
| Mathematics | Shallow | Developed | Convolution versus correlation; noise-variance formula; Gaussian, separability and semigroup; median; bilateral with sources; Sobel, Scharr, Laplacian and derivative of Gaussian; pyramid kernel constraints and Laplacian levels; worked examples A (derivative gains), B (bilateral units), C (kernel sizes) |
| Parameters | Shallow (list) | Developed | Eight-row table with units and a tuning approach |
| Properties | Shallow | Developed | Linearity, separability, semigroup, conditional edge preservation, median geometry, rotational accuracy, scale consistency of pyramids |
| Cost and implementation | Shallow | Developed | Per-pixel costs and pyramid total; seven OpenCV 4.13 contracts with line ranges; execution status |
| Evaluation | Shallow | Developed | Task-based metrics per operator; proposed median-before-detector baseline and variation with an operating-point confound; limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/31-filtrage-gradients.py`](checks/31-filtrage-gradients.py) (19 checks):
ramp gains 2, 8, 32; noise gains 1.41, 3.46, 15.36; SNR ratios and the 1.6 factor;
the 100 → 400 threshold; separable factorization of Sobel and Scharr; bilateral weights
$3.7\times10^{-6}$, 0.78, 0.9998, 0.135 and the affine rule; OpenCV $\sigma$ and
`ksize` rules; 26 versus 169 multiplications; 3×3 noise and scratch attenuation;
median/mean; Gaussian semigroup; Burt–Adelson constraints and the $a=0.375$ kernel;
4/3 pyramid cost; pyramid coordinates; PSNR contribution.

## Applied corrections

- [Reference](../../../vault/30-traitement-image/references/31-filtrage-gradients.md),
  revision 7 → 8: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Consequences for Matching" → "Consequences for
  matching", "Building the Levels" → "Building the levels", "Complete form and role of
  standardization" → "… normalization", "built rarity example" → "constructed rarity
  example"); sources split into scientific and implementation sources; closing
  provenance line replaced. Front matter unchanged except `revision`; H1 and per-card
  headings unchanged.
- [Cards](../../../vault/30-traitement-image/31-filtrage-gradients.md): two expected
  answers fixed as quoted above. Other language fixes: "propagates the influence of
  this pulse at its output" → "carries … into its output"; "does not know how to
  distinguish … on their size alone" → "cannot distinguish … by their size alone";
  "compare multiple media" → "compare several window sizes"; "does not describe itself
  as a linear convolution" → "cannot be written as a linear convolution"; "two
  convolutions 1D replace a convolution 2D for the same kernel produced" → "two 1-D
  convolutions replace one 2-D convolution with the same product kernel"; "Advertise a
  better filter for all noises" → "Claiming that one filter is best for all noise
  types"; "Record beach and color space" → "Record the intensity range and the color
  space"; "overwhelms this distinction" → "erases this distinction"; "Treat all sigma as
  quantities without unity" → "Treating every sigma as a unitless quantity"; "rebuild
  gain" → "reconstruction gain"; "bottom area" → "background area"; "decisive for the
  trade" → "decisive for the inspection task"; "Proposed experience" → "Proposed
  experiment"; "reserved test" → "held-out test set"; "rules of association and
  constant thresholds" → "fixed association rules and thresholds"; "A five-ray window"
  → "A window of radius five"; "Confusing undersampling and controlled loss" →
  "Confusing plain subsampling with a controlled loss"; French decimal commas. Source
  lines: unreachable OpenCV tutorials replaced by versioned headers, Burt and Adelson
  and the authors' bilateral summary; the PSNR tutorial kept with its access status.
  Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`bilateral`, `Sobel`, `Scharr`, `pyrDown`); CV-CANNY-HOUGH, CV-CORNERS and CV-SIFT use
gradients consistently with this note.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). The 2026-10-18 proposal "Choose a derivative scale" (reasoning,
Canny 1986) remains in its report without a register entry; it is not repeated.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FILTRES-01 | CV-FILTRES | Given Sobel, Scharr and a central difference, compute their response to a unit ramp and their noise gain, and explain why a gradient threshold cannot be transferred between kernels or `ksize` values | No card tests derivative kernels although the note's title names gradients; threshold transfer is a frequent silent error | Reasoning; Mathematics, worked example A | 1 card, 3 criteria | [OpenCV 4.13.0 imgproc.hpp, Sobel and Scharr](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1765-L1859) |

## Sources

Scientific sources:

- Tomasi and Manduchi, authors' summary
  [Bilateral Filtering for Gray and Color Images (CVonline local copy)](https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/MANDUCHI1/Bilateral_Filtering.html),
  the page OpenCV's header links to: Introduction, The Idea, The Gaussian Case,
  Experiments with Color Images. The equations of the page are images and were not
  read; the formulas in the note follow the ICCV paper consulted in earlier passes and
  the OpenCV description.
- Burt and Adelson 1983, read in the copy at
  [courses.cs.tau.ac.il](https://courses.cs.tau.ac.il/~hezy/Vision%20Seminar/pyramid83.pdf)
  (DOI 10.1109/TCOM.1983.1095851, confirmed through Crossref): Gaussian Pyramid
  Generation, The Generating Kernel, Equivalent Weighting Functions, Laplacian pyramid
  definition.

Implementation sources (OpenCV at tag 4.13.0):

- [`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L1455–L1474, L1538–L1610, L1703–L1735, L1765–L1890, L3194–L3214.
- [`modules/imgproc/src/smooth.dispatch.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/smooth.dispatch.cpp): L280–L291, L389–L404 (OpenVX path, 6σ rule, not used in the note).
- [`modules/imgproc/src/median_blur.simd.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/median_blur.simd.hpp): L53–L61, L85, L349, L880–L905.
- [`modules/core/include/opencv2/core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp): L333–L342.

Failed accesses and limits:

- Tomasi and Manduchi ICCV 1998 PDF at users.soe.ucsc.edu: TLS certificate
  verification failed (curl and WebFetch); not bypassed.
- Burt and Adelson at persci.mit.edu and web.mit.edu: expired certificate; at
  courses.cs.washington.edu: proxy error 503; the TAU course copy was used.
- Perreault and Hébert 2007 (constant-time median): course copy returned HTTP 404; no
  complexity claim about it is made beyond the function names in OpenCV.
- docs.opencv.org tutorials (smoothing, pyramids, PSNR/SSIM): HTTP 403, retained as
  not re-read.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/31-filtrage-gradients.py` | 19 checks passed |
| `git diff --check -- vault/30-traitement-image/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/30-traitement-image/31-filtrage-gradients.md` | 4 cards, 398, 385, 369 and 368 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged |
| Local links and anchors under `vault/30-traitement-image` | 0 errors |

No filter, OpenCV call or image experiment was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-FILTRES revision 8, CV-FILTRES-001 to -004, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-FILTRES-01).
