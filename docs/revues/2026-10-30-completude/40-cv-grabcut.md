# Review –  GrabCut, regions and appearance models –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-GRABCUT-001 | Deduction/Assumption Cases; Documentary Context Below | Energy and cuts: specifies the existing question | Finished core preserved; 198 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-GRABCUT-002 | Deduction/Assumption Cases; Documentary Context Below | Hard Constraint and Preference: Specifying the Existing Question | Finished core preserved; 190 → 294 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-GRABCUT-003 | Deduction/Assumption Cases; Documentary Context Below | Quality – interaction curve: specifies the existing question | Finished core preserved; 200 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-GRABCUT](../../../vault/90-segmentation/references/92-grabcut-regions.md); [flashcards](../../../vault/90-segmentation/92-grabcut-regions.md). reference note modified before the flashcards.

- **CV-GRABCUT-001 –  Energy and cut-off**: for a binary label $L_p$, a unary term can be linked to $-\log p(I_p\mid L_p)$ under the corresponding color mixture. A schematic neighbor term $w_{pq}\mathbf1[L_p\ne L_q]$ penalizes a boundary between similar pixels; high contrast can reduce $w_{pq}$. With fixed appearance parameters and for a compatible binary energy, the cutoff of the graph optimizes this sub-problem. Alternating with the estimation of the mixtures does not imply an overall joint optimum of all the unknowns. Defining the solved sub-problem prevents confusing the solver's warranty with the correctness of the object model used.

- **CV-GRABCUT-002 –  Hard stress and preference**: A certain label conceptually prohibits the other attribution, while a probable label lets the energy choose. If an actual part of the object is attached to the bottom, changing the appearance settings does not make this solution admissible. In a built test, only correct this constraint, and then compare iterations on the same initial saved state. An improvement locates a contract defect; a persistent exclusion may still come from close colors or regularization. Distinguishing the four states of the mask until the final decision avoids losing interaction information by prematurely binarizing the labels.

- **CV-GRABCUT-003 –  Quality curve – interaction**: Set a common rule to place the initial rectangle, and then a budget for corrections or user time. Measure quality after zero, one, and then multiple interactions and keep the rate of images that do not reach the target to the maximum budget. Clicks are only comparable if their policy and accessible information are announced; a correction chosen with the reference mask constitutes a different oracle from a real operator. Compare also borders and small useful regions. This protocol gives an exploitable compromise curve, instead of an isolated optimization time obtained after a particularly favorable initialization.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html) –  Theory, models and cut-off; sub-problem/alternation distinction and project protocols. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
