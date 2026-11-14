# Review — Otsu, distance transforms and watershed — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 5 to revision 6. Highest severity per card before correction:
0 blocking, 1 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the pipeline note of the segmentation topic. Morphology stays in
[CV-MORPHO](../../../vault/30-traitement-image/references/33-morphologie-composantes.md);
instance metrics are introduced here only as far as counting needs them and link to
[CV-SEGMENTATION](../../../vault/90-segmentation/references/93-semantique-instances-panoptique.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$, equivalent to minimizing within-class variance: confirmed (Otsu eqs. 14, 16, 18). Small classes can lose against a split of the dominant mode: confirmed by recomputation (worked example A). "Business categories", "majority bottom" (background), "default and size evaluation" (defect) obscured the meaning | Reasoning: why a histogram optimum is not a segmentation optimum | 2 expected criteria; 355 → 360 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given Otsu §I–§III-A and the 4.13 implementation |
| CV-WATERSHED-002 | Markers from distance maxima, then propagation: confirmed (Beucher & Meyer §VI.B; tutorial). "Not automatically identical to the OpenCV API taking a color image" left out what OpenCV floods: the priority is the largest absolute channel difference between 4-neighbors (segmentation.cpp L151–L159), so in the tutorial the distance map only supplies markers. "Distance to the bottom" for distance to the background | Algorithm: rebuild the marker pipeline and the role of each map | 3 expected criteria; 346 → 380 lexical words | Further explanation now states the OpenCV relief, as the reference does | Important | Missing implementation condition added to "Choice of topography"; language fixes; Source line given exact passages |
| CV-WATERSHED-003 | 0 unknown, positive seeds, $-1$ boundaries, in-place `CV_32SC1`: confirmed (imgproc.hpp L3474–L3498; segmentation.cpp L161–L162). Missing limitation: the code also writes $-1$ on the one-pixel image frame and resets other negative inputs to 0 (L179–L193). "**check**", "worth −1", "modification on site", "entry", "exit" for check, set to, in place, input and output | Practice: an API contract whose misuse silently corrupts labels | 2 expected criteria; 374 → 408 lexical words | Wording aligned with the reference appendices | Minor | Limitation added to the signed-label paragraph; language fixes; Source line given header and code lines |
| CV-WATERSHED-004 | Global $D>\alpha\max D$ can drop seeds of small objects: confirmed by construction (worked example B: a 10 px disk next to a 15 px disk at $\alpha=0.7$). Expected answer said "germ" and "form hypotheses" for seed and shape assumptions | Diagnosis: separate a marker failure from a relief failure | 2 expected criteria; 362 → 360 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |
| CV-WATERSHED-005 | A merge keeps foreground IoU at 1 while the count fails: confirmed (worked example C). One-to-one matching above IoU 0.5 is unique for non-overlapping segments (Kirillov et al. §4.1, Theorem 1). "Fusions/separations", "fake objects", "Confound semantic overlap" obscured the meaning | Evaluation: choose instance-level measures for a counting product | 2 expected criteria; 266 → 268 lexical words | Wording aligned with the reference appendix | Minor | Language fixes; Source line given Kirillov et al. §4.1–§4.2 |

Expected-answer changes (meaning-restoring language fixes):

- CV-WATERSHED-001: "The objective separates intensities according to variance, not
  business categories; lighting, imbalance and noise can dominate." → "The objective
  separates intensity levels by variance, not by application categories such as defect
  versus sound surface; lighting, class imbalance and noise can dominate it."
- CV-WATERSHED-004: "Visualize markers: if there is only one common germ, review the
  separation of maxima and form hypotheses." → "Visualize the markers: if both objects
  share a single seed, revisit how the maxima are separated and the shape assumptions."

## Reference findings

Claims of revision 5 checked against their passages:

- Otsu's criterion and its equivalence with minimizing the weighted within-class
  variance: confirmed (Otsu §II, eqs. 13–18).
- $D(p)=\min_{q}\|p-q\|$ depends on metric and resolution: confirmed
  (imgproc.hpp L3586–L3612).
- OpenCV watershed contract (8-bit three-channel image, `int32` markers, 0 unknown,
  positive labels, $-1$ boundaries, array modified in place): confirmed (imgproc.hpp
  L3474–L3498; segmentation.cpp L161–L162). Incomplete: the image frame is also $-1$.
- "Watershed propagates basins according to a topography/implementation": imprecise.
  OpenCV's relief is a colour difference between neighbors, not the image values and not
  $-D$ (segmentation.cpp L151–L159, L190–L218, L295–L323).
- No scientific error was found in revision 5. Its body held one to three sentences per
  section, with mistranslations that obscured meaning: "transform distance" (distance
  transform), "fond" rendered as "bottom", "germs" (seeds), "business" (application),
  "default" (defect), "Question of work", "Reference Response", "**check**", "material
  results" (hardware results).

New claims verified for revision 6 (main ones):

- Otsu: cumulative moments eqs. 2–8, variance decomposition eqs. 13–16, criterion
  eqs. 17–19 and effective range; $\eta^*$ in $[0,1]$, zero only for constant images,
  one only for two-valued images, invariant under affine gray-level changes (§III-A);
  multithresholding less credible as classes increase (§III-B); unimodality observed,
  not proven (§III-D); valley difficulties (§I).
- Beucher and Meyer: distance function and its sections as erosions (§II.B.3), flooding
  definition (§III.A), oversegmentation (§IV.A), flooding from markers, markers with
  several components (§IV.B.1), ordered-queue algorithm (§V.B.1–3), coffee grains and
  thalweg lines of the distance function (§VI.B), closed contours (§VIII).
- Felzenszwalb and Huttenlocher: linear-time lower-envelope algorithm (§2.1) and
  separable 2-D transform (§2.2, eqs. 3–4).
- Kirillov et al.: unique matching above IoU 0.5 for non-overlapping segments
  (§4.1, Theorem 1); recognition quality is the F1 score (§4.2).
- OpenCV 4.13.0: Otsu types and dispatch, criterion code, first-maximum rule; distance
  types, chamfer weights, precise algorithm, linear cost, `CV_32F` output; watershed
  priority, 4-connectivity, dam rule, frame and negative inputs, no-marker exit;
  `connectedComponents` defaults; border initialization in the chamfer pass.
- scikit-image 0.25.2 `watershed`: arbitrary relief, `mask`, `compactness`,
  `watershed_line`, tie-breaking by entry time.

Disagreements and implementation details recorded in the note (FR-036):

| Aspect | Scientific description | OpenCV 4.13.0 |
| --- | --- | --- |
| Relief flooded | A function $f$ such as $-D$ or a gradient (Beucher & Meyer §III.A, §VI.B) | Max absolute BGR difference between 4-neighbors, computed on the fly (segmentation.cpp L151–L159) |
| Dams | One of two versions: basins touching without frontier, or with frontiers (§V.B.3) | $-1$ where a popped pixel sees two labels; also $-1$ on the image frame (L179–L193, L265–L293) |
| Otsu levels | $1,\dots,L$, class $C_0=[1,k]$ (§II) | $0,\dots,255$ or $65535$; $C_0$ is "$\le t^*$"; first maximum kept (thresh.cpp L1183–L1275) |
| Euclidean distance | Exact with the lower-envelope algorithm (F&H §2) | Exact only with `DIST_MASK_PRECISE`; chamfer approximation otherwise (imgproc.hpp L3586–L3612) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 333 → 4,657. About 3,650
of these are prose; the rest are tables, the pseudocode and the Mermaid diagram. The
length comes from covering three distinct methods (threshold selection, distance
transform, marker-controlled flooding) and their OpenCV contracts.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task and motivating case (Beucher & Meyer §VI.B); stage-by-stage data contract with types, ranges and units; upstream and downstream expectations; pipeline roles |
| Intuition | Shallow | Developed | One question per step; constructed two-coin illustration; Mermaid data-flow diagram of the 4.13 tutorial pipeline |
| Prerequisites | Shallow (one link) | Developed | Links to CV-ACQUISITION, CV-FILTRES, CV-IOU-AP, CV-METRIQUES-APPLIQUEES and CV-SEGMENTATION, by step |
| Assumptions | Absent | Developed | Global separability, polarity, blob-like objects, meaningful relief; observability of invisible boundaries; degenerate constant image, empty mask, border objects |
| Procedure | Shallow | Developed | Pseudocode of the tutorial pipeline with the purpose of each step; distance threshold as erosion |
| Mathematics | Shallow | Developed | Otsu eqs. 2–19 with units and $\eta^*$; derivation of why small classes lose; distance definitions, separable exact transform, chamfer error; flooding definition, ordered queue, OpenCV priority; worked examples A and B |
| Parameters | Shallow (list) | Developed | Nine-row parameter table with source values; four-step tuning approach |
| Properties | Absent | Developed | Optimality and invariances of Otsu; exactness of distance types; partition and closed contours, OpenCV note on touching markers, dam area bias; tie-breaking; no confidence |
| Cost and implementation | Shallow | Developed | Cost drivers with $N$ and $L$; OpenCV 4.13 contracts of `threshold`, `distanceTransform`, `connectedComponents`, `watershed`; scikit-image 0.25.2 alternative; execution status |
| Evaluation | Shallow | Developed | Instance-level protocol with unique matching (Theorem 1), F1, merges and splits; worked example C; baseline and $\alpha$ variation with a confound; measurement limits |
| Failure modes and diagnosis | Shallow (three sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (components, local thresholding, $-D$ or gradient relief, GrabCut, learned and promptable models); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/91-otsu-distance-watershed.py`](checks/91-otsu-distance-watershed.py)
(17 assertions): Otsu variance decomposition and eq. 18; small-defect case ($k^*=118$
with 50 defect pixels, $k^*=40$ with 100, switch at 96, $\eta^*$ 0.576 and 0.521);
band-split scores $W^2/16$ and $(2/\pi)\sigma^2$; disk separation bound
$2R\sqrt{1-\alpha^2}$ (1.43, 1.6 and 1.73 for $\alpha$ = 0.7, 0.6, 0.5), saddle values
13.23 and 15.20 px, lost 10 px seed; chamfer errors (−4.5% to +4.1% for 3×3,
−1.75% to +1.92% for 5×5); merge matching (F1 0 and 2/3).

## Applied corrections

- [Reference](../../../vault/90-segmentation/references/91-otsu-distance-watershed.md),
  revision 5 → 6: body rewritten and deepened as above; mistranslations fixed in the
  appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "majority bottom" → "majority background", "business class" →
  "application class", "default and size evaluation" → "evaluation by defect and size",
  "germs" → "seeds", "Overall threshold" → "Global threshold", "Merger and
  fragmentation" → "Merges and fragmentation", "real" → "ground-truth", "borders" →
  "boundaries"); the 2026-10-30 appendix of CV-WATERSHED-002 now states the OpenCV relief
  and the 2026-11-08 appendix of CV-WATERSHED-003 the image-frame behavior; trailing
  section renamed "Sources" (anchor `#sources`) and split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/90-segmentation/91-otsu-distance-watershed.md): expected
  answers of CV-WATERSHED-001 and CV-WATERSHED-004 corrected as quoted above. Further
  explanations and blocking errors of all five cards received the same language fixes
  as the reference appendices, plus: "fusions/separations" → "merges and splits",
  "the distance to the bottom" → "the distance to the background", "sub-segmented" →
  "under-segmented", "partially occulted" → "partially occluded", "Code a background
  known as unknown" → "Encoding a known background as unknown", "**check**" →
  "**Discriminating check**", "An exit of the right type" → "An output of the right
  type", "Ablation on germs" → "Ablation on seeds", "offer only a concentration" →
  "yield a single maximum", "fake objects" → "false objects", "Confound semantic overlap
  and correct counting" → "Confusing foreground overlap with correct counting". Added
  conditions: OpenCV relief (CV-WATERSHED-002), image frame and negative inputs
  (CV-WATERSHED-003). Source lines now cite exact passages. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for watershed,
Otsu and distance transform). `vault/01-Parcours/Cas-transfert.md` line 111 uses
"germs" and "maxima parasites" (seeds, spurious maxima); it is a shared file and was not
edited.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-WATERSHED-01 | CV-WATERSHED | State which relief `cv::watershed` floods and what follows for the distance-transform pipeline (markers from $D$, boundaries from colour differences; another implementation to flood $-D$) | A frequent implementation misconception; no card tests the relief | Understanding; Mathematics, marker-controlled watershed | 1 card, 3 criteria | [OpenCV 4.13.0 segmentation.cpp L151–L159, L265–L323](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/segmentation.cpp#L151-L159); [Beucher & Meyer §VI.B](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf) |
| P-CV-WATERSHED-02 | CV-WATERSHED | Decide whether $D>\alpha\max D$ gives two seeds for two touching disks of radius $R$ at centre distance $d$, and what lowering $\alpha$ costs | The merge/lost-object trade-off is only qualitative in CV-WATERSHED-004 | Reasoning; worked example B | 1 card, 3 criteria (saddle $\sqrt{R^2-d^2/4}$, bound $2R\sqrt{1-\alpha^2}$, small-object loss) | [Beucher & Meyer §II.B.3, §VI.B](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf); derivation is a project construction |

No question is defective. The card objectives are invariants and were not edited.

## Sources

Scientific sources, opened at the passages listed:

- Otsu 1979, [DOI 10.1109/TSMC.1979.4310076](https://doi.org/10.1109/TSMC.1979.4310076),
  read in a hosted PDF of the IEEE article (text extracted with `pdftotext`): abstract,
  §I, §II eqs. 1–19, §III-A, §III-B, §III-C (figure settings), §III-D, §IV.
- Beucher and Meyer 1993, [CMM PDF](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf)
  (text extracted with `pdftotext`): §I, §II.B.3, §III.A, §IV.A, §IV.B.1, §V.B.1–3,
  §VI.B, §VIII.
- Felzenszwalb and Huttenlocher, [Cornell technical report PDF](https://www.cs.cornell.edu/~dph/papers/dt.pdf):
  abstract, §1, §2.1, §2.2.
- Kirillov et al., [arXiv 1801.00868](https://arxiv.org/abs/1801.00868) (PDF text):
  §4.1 Theorem 1 and proof, §4.2 eqs. 1–2.

Implementation sources (official code and tutorial sources at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp):
  L303–L380, L3108–L3160, L3474–L3498, L3586–L3655, L4038–L4039.
- [`segmentation.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/segmentation.cpp): L88–L326.
- [`thresh.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/thresh.cpp): L1183–L1320, L1620–L1650.
- [`distransform.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/distransform.cpp): L45–L120.
- [Watershed tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown)
  and [thresholding tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.markdown): complete.
- [scikit-image v0.25.2 `_watershed.py`](https://github.com/scikit-image/scikit-image/blob/v0.25.2/skimage/segmentation/_watershed.py): L1–L200.

Failed accesses and limits:

- docs.opencv.org/4.13.0 pages returned HTTP 403 (known for this pass); the GitHub
  tutorial sources and headers from which they are generated were read instead. The
  rendered links are retained in the note as not re-read.
- Vincent and Soille 1991 (IEEE PAMI 13(6)): no accessible copy (Semantic Scholar mirror
  returned HTTP 202 with no content); not verifiable, not cited for any claim.
- Borgefors 1986: not opened; chamfer weights are cited from the OpenCV header, which
  states that they are the values suggested in the original paper.
- Meyer 1992 (OpenCV's citation for its variant): not opened; the OpenCV code and
  Beucher & Meyer §V.B were used instead.
- theoryofcomputing.org (journal version of Felzenszwalb & Huttenlocher) was refused by
  the proxy; the Cornell technical report was read.
- Context7 was not available in this session (see the scope record); official versioned
  code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/91-otsu-distance-watershed.py` | 17 checks passed |
| `git diff --check -- vault/90-segmentation/91-otsu-distance-watershed.md vault/90-segmentation/references/91-otsu-distance-watershed.md` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/90-segmentation/91-otsu-distance-watershed.md` | 5 cards, 268 to 408 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 5` → `6`; H1 and per-card headings unchanged; `$$` balanced; card paragraphs repeated in the appendices identical |

No OpenCV or scikit-image call and no image experiment was executed; the baseline and
variation are protocols, not results. The Mermaid diagram and tables were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-WATERSHED
revision 6, CV-WATERSHED-001 to 005, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-WATERSHED-01, P-CV-WATERSHED-02).
