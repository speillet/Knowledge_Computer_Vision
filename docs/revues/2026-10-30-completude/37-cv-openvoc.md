# Review –  Open-vocabulary detection and grounding –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OPENVOC-001 | Deduction/Assumption Cases; Documentary Context Below | Where the text intervenes: specifies the existing question | Finished core preserved; 198 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-OPENVOC-002 | Deduction/Assumption Cases; Documentary Context Below | Time division of the test: specifies the existing question | Finished core preserved; 215 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-OPENVOC-003 | Deduction/Assumption Cases; Documentary Context Below | Separate vocabulary and localization: specifies the existing question | Finished core preserved; 181 → 285 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-OPENVOC](../../../vault/80-detection-pose/references/83-detection-open-vocabulary.md); [flashcards](../../../vault/80-detection-pose/83-detection-open-vocabulary.md). reference note modified before the flashcards.

- **CV-OPENVOC-001 –  Where the text comes in**: In Grounding DINO described by the cited article, textual representations can guide the selection of queries and participate in decoding regions. The interface is therefore not limited to classifying a global vector after the fact. For a flashcard of outputs, check what each score represents: token, expression or aggregated category according to the implementation. Two occurrences of the same word in an image still require two distinct regions. A test built with an object, two objects and no object, with fixed prompt, allows to check cardinality and location without confusing the best linguistic compatibility with a certain presence.

- **CV-OPENVOC-002 –  Time cutting of the test**: simulate several updates to the catalog: set to an initial version, freeze the system, then introduce reserved products and close negatives. Measure the annotation and maintenance gain per cycle, as well as errors on old and new objects. The cost of a textual method includes the definition of categories and the validation of prompts; that of the closed includes collection, training and new validation. If one product is visually indistinguishable from another in the available image, no formulation is sufficient to guarantee the distinction. This protocol evaluates a capacity for evolution, rather than a single favorable photograph of the catalog.

- **CV-OPENVOC-003 –  Separate vocabulary and location**: For each false positive, compare first the proposed region to the visible object, then the category of this object to the business definition. A correct box on a semantically neighboring object is a different problem than a box placed between multiple objects. Adding precise formulations can move scores from an entire distribution: re-evaluate recall and rejection, without assuming an invariant threshold to prompt. Record the exact expressions, their tokenization if it affects the interpretation of scores and the rules of grouping into labels. These elements are part of the decision-making model and must be versioned with the checkpoint.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Liu et al., Grounding DINO](https://arxiv.org/html/2303.05499v4) –  §3.2 – 3.3, text-guided selection and decoding; project testing. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
