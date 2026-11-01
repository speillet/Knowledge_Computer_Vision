# Review –  Detection: Faster R-CNN, families YOLO and DETR –  2026-10-30

## Overview

13 enriched flashcards; reference note scope of revision 6 to 7, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | Project Deduction/Protocol; no new external confirmation claimed | Cost scales: specifies the existing question | Finished core preserved; 200 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-002 | Project Deduction/Protocol; no new external confirmation claimed | Versioned decoding: specifies the existing question | Finished core preserved; 182 → 289 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-003 | Deduction/Assumption Cases; Documentary Context Below | Cost of matching: specifies the existing question | Finished core preserved; 201 → 310 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-004 | Project Deduction/Protocol; no new external confirmation claimed | Controllable transformation: specifies the existing question | Finished core preserved; 180 → 286 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-005 | Project Deduction/Protocol; no new external confirmation claimed | Measurement under load: specifies the existing question | Finished core preserved; 195 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-006 | Deduction/Assumption Cases; Documentary Context Below | Site and level: specifies the existing question | Finished core preserved; 219 → 328 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-007 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Geometry of the site: specifies the existing question | Finished core preserved; 199 → 308 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-008 | Deduction/Assumption Cases; Documentary Context Below | Contribution and gradient: specifies the existing question | Finished core preserved; 229 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-009 | Deduction/Assumption Cases; Documentary Context Below | Information still limited: specifies the existing question | Finished core preserved; 241 → 346 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-010 | Deduction/Assumption Cases; Documentary Context Below | Merger recurrence: specifies the existing issue | Finished core preserved; 225 → 340 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-011 | Project Deduction/Protocol; no new external confirmation claimed | Counted error and cause: specifies the existing question | Finished core preserved; 215 → 323 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-012 | Project Deduction/Protocol; no new external confirmation claimed | check of annotations: specifies the existing question | Finished core preserved; 231 → 335 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DETECTEURS-013 | Project Deduction/Protocol; no new external confirmation claimed | Probability and label contract: specifies the existing question | Finished core preserved; 236 → 342 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-DETECTEURS](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md); [flashcards](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md). reference note modified before the flashcards.

In the new explanation FPN, distinction between flashcard fused descending $M_l$ and smooth output $P_l$: the $3\times3$ does not replace the recurrence of fused flashcards. Adjustment made during writing before delivery. Source: FPN §3, figure 3.

- **CV-DETECTEURS-001 –  Cost scales**: If the backbone produces a flashcard of $H'\times W'\times C$ features, this extraction is shared. A head then processes $K$ regions reduced to a fixed spatial representation; its work grows with the number of proposals selected, according to the architecture. Increasing K can improve coverage while weighing down head and post-processing, without changing the backbone’s main cost. Measuring the recall of proposals before classification is therefore useful: a region never proposed will not be found by a better head. A poor final score may come from RPN coverage or from the decision on already correct regions.

- **CV-DETECTEURS-002 –  Versioned Decoding**: An anchor offset representation, edge distances, and distance distribution do not describe the same regression tensor. Box conversion requires sites or anchors, strides, activations, and conventions of the exact variant. An export can move this decoding in the graph and remove a Python step without changing its mathematical necessity. For a given revision, make a known output and then check decoded box and back into the original image. This interface test separates a decoder error from a drive difference, without claiming that a choice is shared by the entire YOLO family.

- **CV-DETECTEURS-003 –  Cost of matching**: For $y_i$ targets and $\hat y_j$ predictions, we look for an injective assignment minimizing $\sum_i C(y_i,\hat y_{\sigma(i)})$, where the cost combines class compatibility and geometry according to the formulation. Swap the order in which annotations are presented should not change the overall problem. Once the assignment is selected, the losses supervise the pairs selected and the lack of subject matter of the other requests. Discreet pair selection and differentiable loss calculation are two operations. The number of requests also limits the number of possible exits; a scene denser than this ability requires an explicit examination of this constraint.

- **CV-DETECTEURS-004 –  Controllable transformation**: in this ideal letterbox, $x'=x/3$ and $y'=y/3+140$; the reverse is $x=3x'$ and $y=3(y'-140)$. A one-pixel error in the grid already corresponds to three pixels in the original, under this convention. For an object that has become $4\times3$, a displacement of one pixel represents a significant fraction of its width or height and can cause the IoU to drop sharply. Check the rounding actually applied by preprocessing rather than assuming this exact pattern for any image. Comparing candidates before filtering then makes it possible to distinguish between sensitive location and deletion of an initially correct prediction.

- **CV-DETECTEURS-005 –  Measurement under load**: note for each image arrival, beginning of service and decision available. Full latency includes queue wait and service; maximum throughput does not explain this wait when arrivals are irregular. Dense scenes can increase decoding and NMS while the backbone time remains close. Compare a distribution of number of candidates, then percentiles of delay and the rate of decisions too late. A high batch can dampen the engine but wait for several images before starting. The protocol must therefore reproduce the pace and processing policy of the product, in addition to the equipment announced.

- **CV-DETECTEURS-006 –  Site and level**: The four target distances verify $l=x-x_0$, $t=y-y_0$, $r=x_1-x$ and $b=y_1-y$. Eligibility by level is for $\max(l,t,r,b)$ in the cited formulation, not just on the box area. Two sites in the same box can therefore have different maximum distances. The "smaller area" rule sets out which boxes are still eligible; it does not allow an out of range box. To audit the assignment, count and view positives by object and level, keeping the exact edge conventions of the implementation. This can reveal a rare oversight without immediately blaming the loss.

- **CV-DETECTEURS-007 –  Geometry of the site**: The given distances have sums $l+r=70$ and $t+b=60$, equal to the width and height of the box. The center of it is $(55,40)$, distinct from the $(40,30)$ site. The center-ness target described by FCOS is $\sqrt{\min(l,r)/\max(l,r)\;\min(t,b)/\max(t,b)}$, here $\sqrt{(20/50)(20/40)}=\sqrt{0,2}\simeq0,447$. It expresses a geometric centrality, not a guaranteed IoU of the predicted box. This reading links distance asymmetry, auxiliary target and ranking, while keeping separate the calculated target values and the actually learned outputs.

- **CV-DETECTEURS-008 –  Contribution and gradient**: Comparing two examples of the same class with $p_t=0,99$ and $p_t=0,5$ gives, at $\gamma=2$, respective factors $10^{-4}$ and 0,25. The second is thus of much greater relative importance. The gradient does not correspond to that of a cross entropy multiplied by a fixed constant: the factor itself depends on $p_t$ and its derivative participates in the optimization. The numbers of positives, assignment rules and loss reduction in the lot still count. To interpret a workout, review these conventions before assigning an improvement or instability to the choice of $\gamma$ alone.

- **CV-DETECTEURS-009 –  Information still limited**: For two disjoint boxes whose union and enclosing rectangle keep the same area, GIoU can remain constant in certain local directions. The additional term provides a signal in many cases without becoming a complete and perfectly conditioned measure of all movements. Edges where intersection or enclosing rectangle change also introduce regime changes in the derivative. A small perturbation test of each coordinate makes it possible to compare the variations of loss to the expected geometry. This analysis concerns the regression of valid boxes; it does not correct a bad target matching or a wrong class.

- **CV-DETECTEURS-010 –  Merger recurrence**: note $M_l=L_l(C_l)+\operatorname{Upsample}(M_{l+1})$ the fused flashcard of the descending path, then $P_l=\operatorname{Conv}_{3\times3}(M_l)$ the smoothed output of the level, where $C_l$ is the feature of the backbone at the $l$ level and $L_l$ the lateral projection of the channels. Spatial sizes and alignment must be compatible for addition. A mismatch error can keep tensor shapes valid while harming the location. The flashcard therefore merges observed lateral information and a reassembled context; it does not create a high-resolution image. Linking the strides to the actual sizes of the objects helps to choose which outputs and which levels to analyze.

- **CV-DETECTEURS-011 –  Counted error and cause**: In the duplicate case, removing the first correct prediction could turn the second into TP without improving the object recall. This shows that the categories also depend on matching's ranking and rules. Conversely, correcting a class can retrieve a GT and simultaneously delete a FP according to the protocol. The oracle gains of several families do not necessarily add up as independent error numbers. For a real intervention, freeze the initial predictions, apply a precise correction and recalculate the complete metric. Diagnosis refers to a family of observed errors; the causal mechanism remains to be established.

- **CV-DETECTEURS-012 –  check of annotations**: A sample of disagreements from multiple models and regions drawn independently of their scores. An audit limited to very confident predictions of a system may favor its own biases. For each case, keep image, inclusion rule, old label, arbitration and new version of the dataset. A crowd or ignore zone does not necessarily follow the same count as an isolated object; apply the rules of the exact evaluator before qualifying a FP. After correction, recalculate all comparisons and keep previous results as historical, without mixing metrics produced on two different ground truths.

- **CV-DETECTEURS-013 –  Probabilities and label contracts**: A softmax per box requires that the probabilities of the chosen categories share a total mass, which corresponds to an exclusive choice in this set. Independent sigmoids can represent multiple labels simultaneously, but do not automatically make "vehicle", "car" and exclusive categories consistent. The dataset of annotations and the rule of decision must specify these relationships. At the image scale, aggregating the presence of a category can lose the number of instances; three cars become a single presence indicator. Maintaining instance identities and their boxes avoids confusing scene classification with object detection.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Carion et al., DETR](https://arxiv.org/html/2005.12872v3) –  §3.1, matching and supervision; project protocols and calculations. View on 2026-10-30.
- [Tian et al., FCOS](https://arxiv.org/html/1904.01355v5) –  §3.3, center-ness, equation 3; example calculated by the project. View on 2026-10-30.
- [Lin et al., Focal Loss](https://arxiv.org/html/1708.02002v2) –  §3, loss modulation; factors and gradient commentary deduced. View on 2026-10-30.
- [Rezatofighi et al., GIoU](https://arxiv.org/html/1902.09630v2) –  Algorithm 1 and §3.1; built sensitivity example. View on 2026-10-30.
- [Lin et al., FPN](https://arxiv.org/html/1612.03144v2) –  §3, flashcards merged then smoothing 3×3 outputs, figure 3. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
