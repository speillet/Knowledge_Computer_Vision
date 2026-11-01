# Review –  MeanShift and CamShift –  follow an appearance distribution –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MEANSHIFT-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Weighted iteration: specifies the existing question | Finished core preserved; 219 → 329 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MEANSHIFT-002 | Deduction/Assumption Cases; Documentary Context Below | Moments of scope: specifies the existing question | Finished core preserved; 222 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MEANSHIFT-003 | Deduction/Assumption Cases; Documentary Context Below | Identity missing from the histogram: specifies the existing question | Finished core preserved; 220 → 325 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MEANSHIFT-004 | Deduction/Assumption Cases; Documentary Context Below | Two factors, four tests: specifies the existing question | Finished core preserved; 221 → 322 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-MEANSHIFT](../../../vault/110-tracking-association/references/115-meanshift-camshift.md); [flashcards](../../../vault/110-tracking-association/115-meanshift-camshift.md). reference note modified before the flashcards.

- **CV-MEANSHIFT-001 –  Weighted Iteration**: For $p(x,y)\ge0$ scores in window $W$, the current center displacement $c$ is $m(c)=\sum_Wp(x,y)(x,y)^T/\sum_Wp(x,y)-c$, in this uniform window model. A common multiplication of all scores by a positive constant does not change the centroid; adding a uniform mass can instead move it towards the geometric center of the window. This distinction explains why normalizing the histogram and changing its contrast are not always equivalent operations. The stop criterion measures a move or budget of iterations, without establishing that the found mode represents the original object.

- **CV-MEANSHIFT-002 –  Moments of extent**: Around the centroid, the matrix of normalized central moments $\begin{bmatrix}\mu_{20}&\mu_{11}\\\mu_{11}&\mu_{02}\end{bmatrix}/M_{00}$ describes the dispersion 2D of the mass. Its own directions give main axes; their values inform the extent according to a window conversion convention. Close values make the orientation undetermined, as for an almost circular distribution. These quantities describe the backprojection in the image plane, not the physical axes 3D of the part. A distractor can change center, orientation and size simultaneously. The appearance mask should therefore be inspected before interpreting a suitable window as a reliable geometric measurement of the target.

- **CV-MEANSHIFT-003 –  Identity missing from histogram**: A histogram retains color frequency and loses much of their spatial arrangement. Two different objects can therefore produce very similar distributions, even with a high backprojection mass. An ROI containing more pixels of the desired color can attract the window without being the target. Testing a background of the same color and then a textured distractor makes it possible to verify this hypothesis. Adding a spatial descriptor or detection changes the information used and requires a new evaluation; increasing the number of iterations does not restore the spatial relationships that the histogram model has deleted.

- **CV-MEANSHIFT-004 –  Two factors, four tests**: To distinguish adaptation and appearance, compare histogram H1 with fixed/adaptive window, then histogram H2 with the same two policies. Measure overlap, center error and initialization losses and identical sequences. The interaction can be important: an adaptive window benefits from a clean backprojection but encompasses more background with a poorly separated histogram. A change of binning modifies the trade-off between color discrimination and noise robustness; a low-saturation mask further changes the retained pixels. These choices must be recorded separately to make the result reproducible and attributable to the mechanism actually modified.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, MeanShift/CamShift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) –  MeanShift, centroid and backprojection; moments and factorial plan deduced by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
