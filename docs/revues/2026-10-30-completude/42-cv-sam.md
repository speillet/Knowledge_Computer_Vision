# Review –  SAM, SAM 2 and video guided segmentation –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | Deduction/Assumption Cases; Documentary Context Below | Ambiguity of the prompt: clarifies the existing question | Finished core preserved; 205 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SAM-002 | Deduction/Assumption Cases; Documentary Context Below | Temporal state: specifies the existing question | Finished core preserved; 191 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SAM-003 | Deduction/Assumption Cases; Documentary Context Below | Two curves to report: specifies the existing question | Finished core preserved; 181 → 285 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SAM](../../../vault/90-segmentation/references/94-sam-sam2.md); [flashcards](../../../vault/90-segmentation/94-sam-sam2.md). reference note modified before the flashcards.

- **CV-SAM-001 –  Ambiguity of the prompt**: A point on a shirt may refer to the shirt, the person or a visible part of it. Multiple masks can be compatible with the same index; the choice depends on the contract of the task and additional information. The predicted quality score is used to rank proposals according to the model, without assigning a business category to the region. To compare two uses, freeze placement and number of prompts, policy of choice of mask and corrections allowed. Choosing a posteriori the best mask using the ground truth measures an oracle selection, different from the procedure actually available to the product.

- **CV-SAM-002 –  Temporal state**: A stored spread depends on the history, not just the current image. Two sequences arriving at the same frame with different initializations can therefore produce different outputs. To diagnose identity confusion, keep initialization frame, prompts, corrections, path order, and memory update instants. Comparing a recovery with reset memory and the original continuation is a proposed ablation, with announced information budget. A reset using the right target given by a human should not be counted as stand-alone recovery. The quality of an outline and the permanence of the identity remain two separate properties.

- **CV-SAM-003 –  Two curves to report**: for each frame, measure the quality of the first available output and that obtained after all the corrections allowed. Associate each release with a moment of availability and a number of interactions. The difference between the curves describes what the offline revision brought; it should not be erased in a final average presented as causal. A mask corrected to $t+2$ s may be excellent for annotating a video and too late for decision to $t$. A common protocol must therefore set the access to frames, the accepted deadlines and the rule of counting corrections.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Kirillov et al., SAM](https://arxiv.org/html/2304.02643v1) –  §2, ambiguity and conditioned task; §3, model; time protocols built without SAM 2 execution. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
