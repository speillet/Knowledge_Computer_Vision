# Review –  NMS –  remove redundant detections –  2026-10-30

## Overview

6 enriched flashcards; reference note scope of revision 5 to 6, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Selection is not transitive: specifies the existing question | Finished core preserved; 214 → 320 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-NMS-002 | Deduction/Assumption Cases; Documentary Context Below | Separate setting and measurement: specifies the existing question | Finished core preserved; 235 → 340 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-NMS-003 | Deduction/Assumption Cases; Documentary Context Below | Constructed taxonomy conflict: specifies the existing question | Finished core preserved; 238 → 340 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-NMS-004 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Calculated Rank Change: Specifies the existing question | Finished core preserved; 234 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-NMS-005 | Deduction/Assumption Cases; Documentary Context Below | Deletion log: specifies the existing question | Finished core preserved; 254 → 349 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-NMS-006 | Deduction/Assumption Cases; Documentary Context Below | Condition of inclusion: specifies the existing question | Finished core preserved; 222 → 320 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-NMS](../../../vault/80-detection-pose/references/81-nms.md); [flashcards](../../../vault/80-detection-pose/81-nms.md). reference note modified before the flashcards.

- **CV-NMS-001 –  Selection is not transitive**: build three boxes of the same size with $A=(0,0,10,10)$, $B=(3,0,13,10)$ and $C=(6,0,16,10)$. The IoU $A/B$ and $B/C$ are worth $7/13>0,5$, but $A/C=4/16=0,25$. With decreasing scores A, B, C, NMS keeps A, deletes B then keeps C: B deleted does not in turn delete its neighbors. This distinguishes the greediness algorithm from a grouping into related components of the overlap graph. The result depends on the ranking and does not automatically look for the set of maximum score sum boxes.

- **CV-NMS-002 –  Separate adjustment and measurement**: take a candidate with a score of 0,4, from IoU 0,8 with another prediction, but from IoU 0,6 with a score of GT. A score threshold at 0,5 discards it before any measurement; at an allowable score, a NMS at 0,7 can remove it; if it survives, it satisfies a localization requirement at 0,5 but not at 0,75, under the other rules of matching. These three comparisons relate to different objects. To assign a recall drop, keep counters after each step with constant evaluation protocol, rather than simultaneously changing the three thresholds.

- **CV-NMS-003 –  Built Taxonomy Conflict**: If the same instance receives the scores 0,8 for "vehicle" and 0,75 for "car", the two labels can be consistent in a hierarchical taxonomy but redundant in a single category contract. Set this policy before choosing deletion. With the same geometry, a person holding a bike and a part receiving two exclusive classes ask for different decisions. Separately testing interclass conflicts and neighbors of the same class helps to measure what class separation actually protects. The highest score does not indicate, by construction, whether two hypotheses share a physical identity.

- **CV-NMS-004 –  Calculated change in rank**: after selection of A, a box B with a score of 0,8 and IoU 0,8 becomes $0,8e^{-0,8^2/0,5}\simeq0,222$ for $\sigma=0,5$. A disjointed box C of score 0,5 remains at 0,5 and thus passes before B. With a final threshold of 0,25, B can be removed. This constructed case makes explicit the roles of the decay parameter and the score threshold. Reusing a selected threshold for initial scores without further validation can change the recall, since the values have been transformed by postprocessing.

- **CV-NMS-005 –  Deletion Log**: For each candidate removed, keep their ID, the one in the box that deleted it, the classes, scores and the IoU calculated in the common coordinate frame. Then replaying the selection on the same predictions makes it possible to isolate the postprocessing without retraining the network. Measure the coverage of the GT with a defined matching, because two candidates on a GT are not two objects recalled. If a top-k precedes NMS, consider also the candidates lost there: increasing the threshold NMS does not recover a box eliminated by this upstream filter.

- **CV-NMS-006 –  Condition of inclusion**: for $B\subset A$ and a strict deletion at threshold $\tau$, B can only be deleted by A if $|B|>\tau|A|$, provided that A is actually selected before it. At $\tau=0,5$, a contained box covering 4% of the large area therefore remains very far from the condition. Reversing the scores does not change the IoU, but changes the first box retained; with more candidates, it can change the whole greedy suite. This reasoning distinguishes the symmetry of the overlap measure and the algorithm's dependence on ranking.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Bodla et al., Soft-NMS](https://arxiv.org/html/1704.04503v2) –  §4, selection and decay; geometric counterexamples constructed. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
