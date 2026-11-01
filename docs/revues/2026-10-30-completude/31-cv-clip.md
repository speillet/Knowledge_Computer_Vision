# Review –  CLIP, SigLIP and text recognition –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | Deduction/Assumption Cases; Documentary Context Below | Decision and cost: specifies the existing issue | Finished core preserved; 198 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CLIP-002 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Algebraic counter-example: specifies the existing question | Finished core preserved; 190 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CLIP-003 | Deduction/Assumption Cases; Documentary Context Below | Loss formulas: specifies the existing question | Finished core preserved; 194 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CLIP-004 | Deduction/Assumption Cases; Documentary Context Below | Measurable sensitivity: specifies the existing question | Finished core preserved; 194 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-CLIP](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md); [flashcards](../../../vault/70-reconnaissance-representations/72-clip-siglip.md). reference note modified before the flashcards.

- **CV-CLIP-001 –  Decision and cost**: For standard embeddings $v$ and $t_j$, calculate $s_j=\tau v^Tt_j$ and then choose a candidate according to the fixed rule. A set of prompts of the same class can be encoded and then combined in text space, with explicit normalization; averaging embeddings and averaging probabilities are two different operations. Fixed texts can be pre-encoded, while each image still has to pass through the encoder. The number of candidates is then included in the comparisons. Keeping the version of this vocabulary with the model makes the results reproducible, because changing the formulations actually changes the classifier used.

- **CV-CLIP-002 –  Algebraic counter-example**: for two logs $a,b$, $p_1=1/(1+e^{b-a})$. A difference $a-b=\log19\simeq2,94$ is enough to give $p_1=0,95$, regardless of the absolute value of the two logs. Adding the same constant to the two does not change anything. If a third candidate receives a logit equal to $a$, the probability of the first becomes $19/(19+1+19)=19/39$, approximately 0,487, without any change in the image. This built case isolates the effect of the candidate set; it does not predict the values of a checkpoint. A robust rejection therefore requires a protocol including the absences and distributions actually encountered.

- **CV-CLIP-003 –  Loss formulas**: with positive pairs on the diagonal of a lot, a direction of CLIP uses $-\frac1n\sum_i\log[\exp(s_{ii})/\sum_j\exp(s_{ij})]$, supplemented by the direction text→image. A sigmoid form per pair writes $\log(1+\exp(-y_{ij}s_{ij}))$ with $y_{ij}\in\{-1,+1\}$, then an aggregation according to the method. Temperature and bias participate in the definition of logits; normalization conventions count for the comparison of gradients and loss values. The central difference is the coupling of candidates in the denominator, not a probabilistic certification of scores after transfer.

- **CV-CLIP-004 –  Measurable Sensitivity**: For each reserved image, keep the winning label, its margin with the second candidate and the decision changes between predefined formulations. Report the rate of disagreement by class and field, in addition to the final accuracy. An average of several prompts must be set before the test and its costs incorporated into the protocol. Separate also the images of the same object or sequence between games: several very similar views can make the validation too favorable. These measures transform an impression of robustness to words into observable property, without selecting only the formulation that succeeds on each example after the fact.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Radford et al., CLIP](https://arxiv.org/html/2103.00020v1) –  §2.3, symmetric loss; §3.1, text classification; algebraic project counterexamples. View on 2026-10-30.
- [Zhai et al., SigLIP](https://arxiv.org/pdf/2303.15343) –  summary, objective per pair; HTML v4 version inaccessible, use PDF. View on 2026-10-30.

The HTML URL SigLIP v4 returned 404; successful use of PDF, §3.2. Score normalization calculations are built-in counterexamples.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
