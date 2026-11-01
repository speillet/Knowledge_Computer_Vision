# Review –  Morphology and related components –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MORPHO-001 | Deduction/Assumption Cases; Documentary Context Below | Properties to know: specifies the existing question | Finished core preserved; 208 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MORPHO-002 | Deduction/Assumption Cases; Documentary Context Below | Built labeling algorithm: specifies the existing question | Finished core preserved; 183 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MORPHO-003 | Deduction/Assumption Cases; Documentary Context Below | Why the area filter arrives too late: specifies the existing question | Finished core preserved; 204 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-MORPHO](../../../vault/30-traitement-image/references/33-morphologie-composantes.md); [flashcards](../../../vault/30-traitement-image/33-morphologie-composantes.md). reference note modified before the flashcards.

- **CV-MORPHO-001 –  Properties to know**: on ideal binary sets with the same structuring, the opening is anti-extensive: its result is included in the initial first plane. The closure is extensive: it can be added. They are idempotent: applying a second time the complete operation with the same structuring should no longer change the theoretical set obtained. Increasing the number of erosions and dilations on the other hand changes the effective support, and is not "repeat an identical opening". Finite images, edge values, and anchors must be consistent to find these properties in an implementation. Opening can break a thin bridge, closing can create a bridge; these topological changes can be decisive for counting objects.

- **CV-MORPHO-002 –  Labeling algorithm built**: browse the mask; at each foreground pixel not yet visited, create a label and explore by queue or stack its eligible neighbors. All affected pixels receive the same label, then the path resumes on the remaining pixels. This definition directly links the number of components to the number of routes launched. A practical implementation can use multiple passes or union-find, without changing the connectivity defined. Beware of the return of a library that includes the background in its number of labels: two components of foreground then give three labels in total. The properties of holes and contact also require a coherent neighborhood convention between background and foreground.

- **CV-MORPHO-003 –  Why the area filter arrives too late**: The area of a merged component essentially adds those of the two parts and the pixels of the bridge. It can therefore perfectly pass a minimum threshold, even when the count is false. Separately measuring the distance between borders before closing, the width of the bridge created and the maximum distance inside each part helps to choose a remedy. A marker watershed can use two reliable centers to provide separation, but bad markers can oversegment a single piece. In the evaluation, explicitly distinguish merge error, division error and boundary error: an average pixel score can remain good despite an object lost on counting.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html) –  §§1 – 4, erosion, dilation, opening and closing. View on 2026-10-30.
- [OpenCV 4.13, connectedComponents](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html) –  connectivity and labels. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
