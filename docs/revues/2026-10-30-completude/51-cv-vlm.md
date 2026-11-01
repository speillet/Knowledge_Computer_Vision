# Review –  VLM, grounding and frontier vision – action –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VLM-001 | Project Deduction/Protocol; no new external confirmation claimed | Optimized quantity: specifies the existing question | Finished core preserved; 205 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VLM-002 | Deduction/Assumption Cases; Documentary Context Below | Representation Goulot: specifies the existing question | Finished core preserved; 204 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VLM-003 | Project Deduction/Protocol; no new external confirmation claimed | Cost of indexing: specifies the existing question | Finished core preserved; 218 → 329 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VLM-004 | Project Deduction/Protocol; no new external confirmation claimed | Anchor tests built: specifies the existing question | Finished core preserved; 215 → 323 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-VLM](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md); [flashcards](../../../vault/120-generatif-multimodal/121-vlm-grounding.md). reference note modified before the flashcards.

- **CV-VLM-001 –  Optimized quantity**: an autoregressive generation models $p(y\mid I,q)=\prod_kp(y_k\mid y_{<k},I,q)$ for a $I$ image, a $q$ question and $y_k$ tokens. A probable sequence under this model is not automatically a true visual proposition. A syntactically valid JSON format can also contain a false box or object. The evaluation must therefore separate respect for the schema, accuracy of the facts and spatial or temporal anchoring. For an action output, add more method-specific units, coordinate frames, and execution contract; the plausibility of tokens does not validate a physical action.

- **CV-VLM-002 –  Representation bottleneck**: learned queries query the features of the visual encoder by cross attention and produce an intermediate representation for the language model. They are not the free questions typed by the user. Limiting the number of vectors transmitted can reduce the cost of the interface while constraining the information available on small details. A frozen encoder and a frozen LLM can be linked by learned parameters without updating all their weights. The mechanism of the bridge and the learning protocol must therefore be described separately from the final behavior, which remains to be measured on the visual observations of the task.

- **CV-VLM-003 –  Indexing cost**: with a video of duration $T$ and a sampling step $\Delta$, the number of frames retained is of the order of $T/\Delta$. The cost includes decoding, visual encoding, building windows, and generating or indexing outputs. Reducing this number can make short events disappear; increasing the context can add cost and delay without restoring a frame never observed. A hybrid pipeline can first propose intervals and then describe them, but it is necessary to measure the recall of this preselection: an excluded event will never reach the VLM. Evaluate each step and the final index on the same reserved events.

- **CV-VLM-004 –  Anchor tests built**: use a positive image, a comparable negative image and, if feasible, a variation where only the target object changes. Check if the assertions actually follow this variation and if the correction increases the refusal rather than the accuracy. A decrease in the number of false assertions obtained by never responding is not the same result as better recognition; report coverage of responses and risk of error among responses issued. These tests must respect the distribution of the images, because an artificial masking can introduce an artifact. Outputs must remain connected to the exact version of the input and prompt used.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Li et al., BLIP-2](https://arxiv.org/html/2301.12597v2) –  §3.1, learned queries and cross attention; probabilistic models and built tests. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
