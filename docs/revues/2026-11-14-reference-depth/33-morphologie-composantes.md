# Review — Morphology and connected components — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for binary morphology and connected-component
labeling. Thresholding, distance transforms and watershed stay in
[CV-WATERSHED](../../../vault/90-segmentation/references/91-otsu-distance-watershed.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MORPHO-001 | Opening erodes then dilates and removes small structures; closing dilates then erodes and fills small holes and gaps: confirmed (Haralick et al. §III, Definitions 35–36 and the qualitative effects of disk openings and closings); anti-extensivity, extensivity and idempotence confirmed (Propositions 41–42, Theorems 38 and 40) and recomputed on toy sets. Expected answer said "erodes then expands", "the closure expands", "structurer" (French *dilate*, *fermeture*, *structurant*); "it can be added" for extensivity | Comparison: opposite effects of two compositions and the role of scale | 2 criteria; 312 → 308 lexical words | Consistent with reference worked example A | Minor | Meaning-restoring fix of the expected answer; language fixes; Source replaced (unreachable tutorial) by Haralick et al. and `imgproc.hpp` |
| CV-MORPHO-002 | 2 components under 4-connectivity, 1 under 8: recomputed; OpenCV returns N labels including background 0 (imgproc.hpp L4009–L4040). "Built labeling algorithm", "browse the mask", "number of routes launched", "countdown deducted from connectivity" | Reasoning: connectivity defines the object count | 1 criterion; 348 → 344 lexical words | Consistent with reference worked example B | Minor | Language fixes; Source cites the OpenCV header and Wu et al. |
| CV-MORPHO-003 | Closing can bridge a gap and labeling then counts one component: confirmed by construction (gaps up to $k-1$ px merge, worked example A) and consistent with closing "fuses narrow breaks" (Haralick §III). Expected answer "The structurer"; "The related labeling" and blocking error "Take a related component" (French *connexe* = connected) altered the meaning; "check" label, "still image structurer" (*image fixe*), "under check" | Diagnosis: separate a morphological merge from a labeling error | 1 criterion; 381 → 393 lexical words | Consistent with the reference failure table | Minor | Meaning-restoring fix of the expected answer; language fixes including the blocking error; Source cites Haralick §III |

Expected-answer changes (meaning-restoring language fixes, checked against the
pre-migration French text `git show b7142bb^:vault/30-traitement-image/33-morphologie-composantes.md`):

- CV-MORPHO-001: "The opening erodes then expands and can remove small foreground
  structures; the closure expands then erodes and can fill holes or gaps. Choose the
  structurer according to the sizes and shapes to keep." → "Opening erodes then
  dilates and can remove small foreground structures; closing dilates then erodes and
  can fill holes or gaps. Choose the structuring element according to the sizes and
  shapes to keep."
- CV-MORPHO-003: "The structurer may have created a bridge; …" → "The structuring
  element may have created a bridge; …"

No defective question or objective was found (the objective "Explaining a merger of
parts." is understandable).

## Reference findings

Claims of revision 7 checked:

- $A\ominus B=\{x:x+B\subseteq A\}$, $A\oplus B=\{a+b\}$, opening
  $(A\ominus B)\oplus B$: confirmed (Haralick et al., Definitions 1, 17, 35).
- "Two pixels that only touch diagonally are two components in 4-connectivity and one
  in 8-connectivity": confirmed (recomputed).
- "B expresses a scale in pixels; a variation in resolution changes its physical
  meaning": confirmed and quantified (worked example A).
- No scientific error found. The body was shallow (315 words) and contained
  mistranslations: "structuring" used as a noun, "expansion/closure", "Counting too
  low/high", "Question of work", "Reference Response", "**check**", "structurator",
  "ensemblist morphology", "finished image" (finite image), "closure" for closing.

New claims verified for revision 8 (main ones):

- Haralick, Sternberg and Zhuang 1987: dilation as Minkowski sum (Definition 1); chain
  rule (Proposition 3); dilation and erosion increasing (Propositions 12 and 22);
  erosion anti-extensive only if the origin is in $B$ (Proposition 20); erosion
  (Definition 17) versus Minkowski subtraction; reflection and duality (Definition 24,
  Theorem 25); chained erosions (Corollary 31); opening and closing definitions,
  idempotence, increasing property, translation invariance including translations of
  the element, anti-extensivity and extensivity regardless of the origin
  (Definitions 35–36, Theorems 38 and 40, Propositions 41–42); qualitative effects of
  disk openings and closings.
- Wu, Otoo and Suzuki 2009: two-pass scheme with scan masks, union-find, linear
  complexity, decision tree reducing neighbours inspected by about 2, union-find gain
  of 4 or more, up to 10× faster than the contour-tracing program in their tests
  (abstract, §1).
- OpenCV 4.13.0: morphology types and shapes (including `MORPH_DIAMOND` and
  hit-or-miss on `CV_8UC1`), magic border value, anchor semantics of
  `getStructuringElement`, min/max formulas of `erode` and `dilate`, opening and
  closing composition and iteration semantics, merging of iterations of full
  rectangles, `connectedComponents` outputs, label types, algorithm choices (Spaghetti
  default, BBDT, SAUF) and the label-ordering note.

Paper versus implementation (FR-036): the set opening uses the Minkowski sum with $B$
for the dilation step, whereas OpenCV's documented dilation is a maximum over the same
offsets as erosion, i.e. a dilation by the reflected element. For symmetric, centred
elements they coincide; for even-sized or off-centre elements the OpenCV composition
can shift the result and lose anti-extensivity (worked example C, derived from the
documented formulas and simulated in the checks script; no OpenCV call executed).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 315 → 3,126. About
600 tokens are tables, the pseudocode and the Mermaid diagram.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Mask contract (polarity, range, element, border, connectivity); OpenCV label and statistics outputs; units; label semantics; pipeline role |
| Intuition | Shallow | Developed | Erosion and dilation as fit and touch tests; opening and closing effects quoted from Haralick et al.; connectivity as a graph; constructed resolution illustration; Mermaid sequence |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES and CV-WATERSHED; set, graph and union-find background |
| Assumptions | Absent (merged) | Developed | Binary masks, scale separation, origin and symmetry of the element, border rule, complementary connectivity; observability and degenerate cases |
| Procedure | Shallow | Developed | Seven-step pseudocode from physical sizes to object-level checks |
| Mathematics | Shallow | Developed | Set definitions and duality; opening and closing properties; chain rule and size rules; OpenCV grey-level formulas; connectivity; two-pass labeling; worked examples A (gaps and resolution), B (connectivity and holes), C (asymmetric element) |
| Parameters | Shallow (list) | Developed | Eight-row table with units and a tuning approach |
| Properties | Shallow | Developed | Order properties and their implementation limits; idempotence versus iterations; topology changes; no semantics; arbitrary label order; discrete disks |
| Cost and implementation | Shallow | Developed | Cost drivers; reported labeling speed-ups labelled as empirical; four OpenCV 4.13 contracts with line ranges; execution status |
| Evaluation | Shallow | Developed | Object-level merge/split metrics; proposed 3×3 versus 5×5 closing variation with a confound; limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (opening, closing, area filter, watershed, instance segmentation, connectivity); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/33-morphologie-composantes.py`](checks/33-morphologie-composantes.py)
(12 checks): merge table for gaps 2–5 px and kernels 3 and 5; 0.2 mm at two
resolutions; opening of 2, 3 and 4 px strips; anti-extensivity, extensivity and
idempotence; chain rule; duality; corner pixels, diagonal line and diamond-ring hole
under 4/8 connectivity; set versus OpenCV-formula opening with a 2-pixel element and
agreement with a centred 3-pixel element; iteration sizes.

## Applied corrections

- [Reference](../../../vault/30-traitement-image/references/33-morphologie-composantes.md),
  revision 7 → 8: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Mechanism of Error" → "Mechanism of the error",
  "**check**" → "**Discriminating check**", "Built labeling algorithm" → "Constructed
  labeling algorithm", "§§1 – 4" → "§§1–4"); sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/30-traitement-image/33-morphologie-composantes.md): two
  expected answers fixed as quoted above. Other language fixes: "clear a defect" →
  "erase a defect"; "requires the structurer to hold in the foreground" → "requires
  the structuring element to fit inside the foreground"; "In a closure, sufficiently
  small intervals" → "In a closing, sufficiently small gaps"; "A useful structurator on
  a camera" → "A structuring element suited to one camera"; "a dust of similar size" →
  "a dust particle of similar size"; "The closure is extensive: it can be added" →
  "Closing is extensive: it can only add pixels"; "browse the mask … routes launched"
  → "scan the mask … explorations started"; "Announce a number without connectivity"
  → "Stating a count without its connectivity"; "under check" → "in a controlled
  test"; "the structurant scale" → "the scale of the structuring element"; "The related
  labeling" → "Connected-component labeling"; "the still image structurer" → "the
  structuring element on the same fixed image"; "A filtering by area after fusion does
  not find the two pieces" → "Area filtering after the merge does not recover the two
  parts"; "Take a related component for a guaranteed object" → "Taking a connected
  component for a guaranteed object". Source lines: unreachable tutorials replaced by
  Haralick et al., Wu et al. and versioned OpenCV headers. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`opening`, `closing`, `connectedComponents`, `structurer`); CV-WATERSHED treats
markers and distance transforms consistently with this note.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run).

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-MORPHO-01 | CV-MORPHO | Given the smallest defect to keep, the smallest legitimate gap and the footprint in mm/px, choose a structuring-element size for opening and closing, or conclude that morphology cannot satisfy both | No card trains the design decision linking physical sizes to the element; the subject has no design card | Design (absent family); Parameters and worked example A | 1 card, 3 criteria | [Haralick et al. 1987, §III](https://doi.org/10.1109/TPAMI.1987.4767941); [OpenCV 4.13.0 `getStructuringElement`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1517-L1530) |

## Sources

Scientific sources:

- Haralick, Sternberg and Zhuang 1987, read in the copy at
  [haralick.org](https://www.haralick.org/journals/04767941.pdf) (DOI
  10.1109/TPAMI.1987.4767941, confirmed through Crossref): §II (Definitions 1, 17, 24;
  Propositions 3, 12, 20, 22; Theorem 25; Corollary 31), §III (Definitions 35–36;
  Theorems 38, 40; Propositions 41–42; introductory paragraph on openings and
  closings).
- Wu, Otoo and Suzuki 2009, read in the authors' final manuscript at
  [sdm.lbl.gov](https://sdm.lbl.gov/~kewu/ps/paa-final.pdf) (DOI
  10.1007/s10044-008-0109-y, confirmed through Crossref): abstract and §1.

Implementation sources (OpenCV at tag 4.13.0):

- [`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L216–L241, L399–L420, L1514–L1530, L2325–L2412, L4009–L4085.
- [`modules/imgproc/src/morph.dispatch.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/morph.dispatch.cpp): L1004–L1017, L1236–L1247.
- [`modules/imgproc/src/filterengine.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/filterengine.hpp): `normalizeAnchor` (default anchor `ksize/2`).

Failed accesses and limits:

- Serra (1982) and Soille (2003), the reference books on morphology: not openly
  available; not consulted. Haralick et al. state that Matheron's and Serra's
  definitions of opening and closing are identical to theirs.
- Grana et al. 2010 (BBDT) and Bolelli et al. (Spaghetti): cited by OpenCV, not
  consulted; only their availability in OpenCV is stated.
- Rosenfeld's digital-topology results on complementary connectivity: not consulted;
  the hole example is a constructed case recomputed by the checks script.
- docs.opencv.org morphology tutorial and structural-analysis page: HTTP 403, retained
  as not re-read.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/33-morphologie-composantes.py` | 12 checks passed |
| `git diff --check -- vault/30-traitement-image/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/30-traitement-image/33-morphologie-composantes.md` | 3 cards, 308, 344 and 393 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged |
| Local links and anchors under `vault/30-traitement-image` | 0 errors |

No morphology or labeling code from a library was executed; the checks script
simulates set definitions and documented formulas, and the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not
rendered in Obsidian, and AnkiDroid rendering of the corrected cards is unverified.
This is agent self-review, without independent scientific validation or measurement
of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-MORPHO revision 8, CV-MORPHO-001 to -003, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-MORPHO-01).
