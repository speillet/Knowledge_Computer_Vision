# Review –  Otsu, distance transform and watershed –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | Deduction/Assumption Cases; Documentary Context Below | Computable criterion: specifies the existing question | Finished core preserved; 196 → 297 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-WATERSHED-002 | Deduction/Assumption Cases; Documentary Context Below | Choice of topography: specifies the existing question | Finished core preserved; 187 → 291 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-WATERSHED-003 | Deduction/Assumption Cases; Documentary Context Below | Example of a label table: specifies the existing question | Finished core preserved; 193 → 297 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-WATERSHED-004 | Deduction/Assumption Cases; Documentary Context Below | Global threshold and different sizes: specifies the existing question | Finished core preserved; 200 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-WATERSHED-005 | Deduction/Assumption Cases; Documentary Context Below | Merger and fragmentation: specifies the existing question | Finished core preserved; 182 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-WATERSHED](../../../vault/90-segmentation/references/91-otsu-distance-watershed.md); [flashcards](../../../vault/90-segmentation/91-otsu-distance-watershed.md). reference note modified before the flashcards.

- **CV-WATERSHED-001 –  Computable criterion**: at threshold $t$, form the weights $\omega_0,\omega_1$ of the two groups and their averages $\mu_0,\mu_1$; Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$. Two very separate groups but one of which contains very few pixels may be less favored than a break explaining more about the overall variation. The criterion ignores positions: Spatially swapping pixels retains the histogram and threshold, but can destroy all objects. This built case shows why neither form, connectivity, nor business class are guaranteed. A default and size evaluation therefore necessarily completes the reading of the histogram.

- **CV-WATERSHED-002 –  Choice of topography**: For a binary mask and a positive distance inside, the thick centers are maxima of $D$. A conceptual watershed on $-D$ transforms them into a minima; another variant can use a gradient image with fixed germs. These constructs are not automatically identical to the OpenCV API taking a color image. The distance to a discrete background also depends on the chosen metric. On anisotropic pixels, a distance in indices is not directly a physical distance: integrate the spacings if the shape or threshold should be interpreted in millimeters rather than pixels.

- **CV-WATERSHED-003 –  Example of a label array**: assign 1 to the certain background, 2 and 3 to the two object interiors, then 0 to the areas to be decided. After propagation, the positive labels designate the basins and $-1$ the borders according to the contract cited. The number 1 is therefore not universally the "object" class: it is here an identifier chosen for the background. Keep a dictionary between labels and physical meaning before producing a binary mask. If we replace all positive labels with a single one, we destroy precisely the distinction of instances that the initialization should bring, even if the global region remains unchanged.

- **CV-WATERSHED-004 –  Overall threshold and different sizes**: Select all pixels where $D>\alpha\max D$ can remove germs from small objects, because the global maximum belongs to the thickest. Two properly masked objects can receive a germ and none, respectively. Comparing an overall threshold to a maxima detection adapted to the expected sizes is a discriminating variation, without assuming that a local rule solves all cases. Smoothing and removing close maxima also alters the number of germs. Viewing their number per annotated instance before the watershed makes it possible to distinguish a loss of small object and a merger of neighboring markers.

- **CV-WATERSHED-005 –  Merger and fragmentation**: An actual instance predicted in three fragments and three actual instances predicted as a single region may have opposite counting errors but a very close foreground. Using a table of overlaps between real and predicted labels reveals one-to-many and many-to-one relationships. A one-on-one matching with a fixed threshold measures objects found according to an announced rule; it does not replace the analysis of mergers. Also report the image counting error with its sign, because a signed average can undo important overcounts and undercounts. The measure must keep these failure modes separate.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html) –  Theory and example of distance transform; size and metric analyses of the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
