# Review –  Detection 3D, pose of object and pose articulated –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Deduction/Assumption Cases; Documentary Context Below | Defining the comparative quantity: specifies the existing question | Finished core preserved; 194 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-POSE3D-002 | Deduction/Assumption Cases; Documentary Context Below | Corner construction: specifies the existing question | Finished core preserved; 194 → 309 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-POSE3D-003 | Deduction/Assumption Cases; Documentary Context Below | Counter-example of geometry: specifies the existing question | Finished core preserved; 189 → 294 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-POSE3D-004 | Deduction/Assumption Cases; Documentary Context Below | Equivalence of poses: specifies the existing question | Finished core preserved; 194 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-POSE3D](../../../vault/80-detection-pose/references/84-detection-pose-3d.md); [flashcards](../../../vault/80-detection-pose/84-detection-pose-3d.md). reference note modified before the flashcards.

- **CV-POSE3D-001 –  Set Compared Quantity**: An average 3D seal error can write $J^{-1}\sum_j\|\hat p_j-p_j\|$ in a length unit, with visible seals or all seals according to protocol. Allowing rigid alignment or similarity removes some errors and changes the evaluated question. A AP of boxes, it, depends on a threshold of matching and the ranking of the scores. A rigid object pose estimates $R,t$ of a known model, while a skeleton estimates several related points. Specifying these unknowns and allowed transformations avoids comparing two digits, one of which has precisely neutralized the defect as the other measures.

- **CV-POSE3D-002 –  Corner construction**: for a geometric center $c$, dimensions $(l,w,h)$ and rotation $R$, the eight corners are $c+R(\pm l/2,\pm w/2,\pm h/2)^T$. If the center is anchored to the ground, the vertical component must be adjusted before using this formula. Transforming corners between sensors is more general than keeping a simple yaw: an extrinsic with roll or pitch can produce a box that is no longer described by a rotation around the single vertical axis of the target coordinate frame. A test with all distinct dimensions and non-zero rotation makes visible permutations, angle sign and loss of information when converting to a simplified box.

- **CV-POSE3D-003 –  Counter example of geometry**: A prediction may have the exact center but doubled dimensions and a wrong yaw. A matching per center distance can still accept it according to its threshold, while a volume overlap can be bad. The nuScenes protocol reports other errors to characterize size, orientation, and movement; these must be read with the AP. Conversely, a small metric offset represents a very different part of a pedestrian and a large vehicle. Thresholds and classes therefore define what the measure prefers. Check a few built boxes before interpreting an aggregate score change.

- **CV-POSE3D-004 –  Equivalence of poses**: If $S$ belongs to the symmetry group of the model, the poses $T$ and $TS$ can represent the same observable object. A suitable error can minimize a geometric distance on these symmetries, instead of arbitrarily comparing two single matrices. The symmetry of the complete mesh and the indistinguishability of the only visible surfaces are not exactly the same notion; the protocol must specify the one it deals with. An observed marking may reduce the relevant group of symmetries. The validation must then take into account this new information and not maintain an equivalence tolerance that would hide an angle that has become effectively observable.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [BOP](https://bop.felk.cvut.cz/tasks/) –  Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; box constructs and project examples. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
