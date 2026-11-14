# Flashcards — NMS — suppressing redundant detections

reference note: [[80-detection-pose/references/81-nms|NMS]]. Source: Agent.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-NMS-001

Objective: unroll hard NMS. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-001
Question: Three continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$ and $C=(20,0,30,10)$ have scores $0.9$, $0.8$ and $0.7$. Which boxes are retained by hard NMS that suppresses candidates with IoU greater than 0.5?
Reponse: **Expected answer**: select $A$, delete $B$ because their intersection is 80, union 120 and IoU $2/3>0.5$; then keep $C$, disjoint. The output is $A,C$.

**Further explanation**: the calculation uses continuous `xyxy` coordinates without `+1`. The selection is greedy and follows the scores, without merging the boxes. At threshold 0.7, this example would keep all three: the threshold controls redundancy, not semantic correctness. Result executed in the repository's arithmetic example.

**Reasoning on instances**: Overlap is used as an indication of redundancy between predictions, without knowing the real identity of the objects. If A and B represent two close people, deleting B can remove a real instance; if they represent the same part, the deletion can instead be useful.

**Proposed check**: keep the outputs before and after the operation and check which annotations remain covered. The threshold therefore settles a tradeoff that depends on the scene. A distant box remains a candidate even with a lower score, as long as it passes the other filters in the pipeline. This reading avoids turning greedy selection into a "one box per image" or "one box per class" rule.

**Selection is not transitive**: construct three boxes of the same size with $A=(0,0,10,10)$, $B=(3,0,13,10)$ and $C=(6,0,16,10)$. The IoUs $A/B$ and $B/C$ equal $7/13>0.5$, but $A/C=4/16=0.25$. With decreasing scores A, B, C, NMS keeps A, deletes B, then keeps C: a deleted B does not in turn delete its neighbors. This distinguishes the greedy algorithm from a grouping into connected components of the overlap graph. The result depends on the ranking and does not search for the subset of boxes with maximum score sum.

**A common geometric transform preserves IoU**: Translating all boxes together or scaling every x and y coordinate by common positive factors multiplies intersections and unions by the same area factor, preserving IoU. Hard NMS decisions should therefore agree under this constructed transform when scores, tie-breaking and numerical precision are held fixed. Clipping boxes to an image border is different: it can change relative areas and overlaps. This provides a geometry check independent of detector quality.

**Blocking errors**: delete $C$ for the sole reason of its lower score, or treat the output as an average of $A$ and $B$.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Soft-NMS, §4](https://arxiv.org/abs/1704.04503); [convention hard NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html); [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-NMS-001 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-002

Objective: Distinguish three thresholds. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-002
Question: In object detection, how do the score threshold, NMS IoU threshold and evaluation IoU threshold differ?
Reponse: **Expected answer**: the score threshold filters predictions according to their confidence; the NMS threshold compares two predictions to reduce duplicates; the evaluation IoU threshold compares a prediction with an annotation according to the protocol.

**Further explanation**: The same number does not give the same meaning. The NMS does not consult the GT at the time of inference. Changing a score threshold can change recall and cost before NMS; changing NMS affects duplicates and retained neighbors; changing the evaluation threshold changes the localization requirement. Record all three separately.

**Example of distinction**: A prediction can pass the score threshold, be removed for its overlap with another prediction, and never reach evaluation. Conversely, two preserved boxes can correspond to a single object and one can become a duplicate in the measurement protocol.

**Proposed investigation**: Log the steps and their parameters separately, then calculate the coverage of the same annotations at each stage. Changing the evaluation IoU requirement does not change the boxes that the system has produced; changing the NMS threshold may change them. Set the parameters on validation data, then freeze the protocol. An identical numerical value, for example 0.5, does not make these three decisions play the same role.

**Separate setting and measurement**: take a candidate with a score of 0.4, an IoU of 0.8 with another prediction, and an IoU of 0.6 with a ground-truth box. A score threshold at 0.5 discards it before any measurement; if its score is admissible, NMS at 0.7 can remove it; if it survives, it satisfies a localization requirement at 0.5 but not at 0.75, under the other matching rules. These three comparisons involve different objects. To attribute a recall drop, keep counters after each step with a constant evaluation protocol, rather than changing the three thresholds simultaneously.

**AP requires the score-ranking information retained**: A high operational score cutoff may discard low-score true detections before the evaluator can sweep the precision-recall curve. Record whether AP is computed from the full retained prediction list or from a deployment-filtered list. The NMS threshold still compares predictions with predictions; the evaluation IoU still compares predictions with annotations. Sharing one threshold name or configuration field obscures which stage changed the measured recall ceiling.

**Blocking errors**: Using the AP50 threshold to decide directly which predictions suppress each other, or saying that NMS requires the ground truth.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html); [COCO](https://cocodataset.org/#detection-eval); [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-NMS-002 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-003

Objective: Choose the scope of a deletion. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-003
Question: Two candidates from different classes have scores $0.9$ and $0.8$ and IoU $0.8$. With NMS threshold $0.5$, what tradeoff distinguishes global suppression from per-class suppression?
Reponse: **Expected answer**: Global NMS keeps only the candidate with score $0.9$; per-class NMS keeps both. This protects two objects of different classes, but also leaves two competing labels on the same instance. Choose whether the annotations allow these two detections or impose an exclusive class.

**Further explanation**: Person and bicycle can be two legitimate objects that overlap. Two exclusive categories of the same part require a class decision; taking the maximum score does not guarantee the right label. A NMS per class also retains several disjoint instances of this class: it does not impose one box per category. Scores, coordinate frames and output rules must be comparable.

**Constructed case**: A person and their bike can provide two valid categories that overlap. Two exclusive part types on the same instance pose another question: you have to decide the label, not just prevent boxes from being deleted.

**Proposed validation**: Clearly annotate instances and taxonomy, then examine interclass conflicts and neighbors of the same class. One NMS per class protects different categories but not two people very close to each other. The right choice is measured on errors useful to the product, with scores and thresholds recorded, without inferring a physical identity from the overlap alone.

**Constructed taxonomy conflict**: If the same instance receives the scores 0.8 for "vehicle" and 0.75 for "car", the two labels can be consistent in a hierarchical taxonomy but redundant in a single-category contract. Set this policy before choosing the suppression. With the same geometry, a person holding a bicycle and a part receiving two exclusive classes call for different decisions. Testing inter-class conflicts and same-class neighbors separately helps to measure what class separation actually protects. The highest score does not indicate, by construction, whether two hypotheses share a physical identity.

**Cross-class scores may not have a shared meaning**: Global NMS orders candidates from different classes by score. If those scores have different calibration or class priors, that ordering need not reflect which physical hypothesis is better. Class-separated NMS avoids cross-class suppression but leaves the taxonomy decision unresolved. A proposed validation includes overlapping legitimate classes and mutually exclusive labels on the same instance, with the annotation contract fixed before comparing the suppression policy.

**Blocking errors**: Believing that per-class NMS solves inter-class confusions, or that global NMS knows the real identity of objects.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Torchvision 0.29, batched_nms: description and threshold](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html), consulted on 2026-10-21; case constructed by the project; [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), consulted on 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-NMS-003 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-004

Objective: Explain the effect of Soft-NMS. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-004
Question: How does Gaussian Soft-NMS differ from hard NMS, and why must candidates be reordered after a score penalty?
Reponse: **Expected answer**: instead of an immediate deletion beyond an overlap threshold, it reduces the score of each candidate according to its overlap with the retained box $M$: $s_i\leftarrow s_i\exp(-\operatorname{IoU}(M,b_i)^2/\sigma)$, with $\sigma>0$. The modified scores change the next maximum, so the order must be recalculated.

**Further explanation**: The Gaussian penalty acts on overlaps without the discontinuous threshold of hard NMS. A final score threshold can eliminate boxes whose scores have become too low: Soft-NMS does not guarantee to keep everything or to resolve all occlusions. Specify variant and area convention before a comparison.

**Interpretation of the order**: After penalization, a candidate initially second may lose priority to another candidate with little overlap. Taking the current maximum again is part of the greedy logic. Traversing the old ranking once would be another procedure.

**Example of a check**: Record at each step the retained box and the remaining scores on a small known set. Then compare hard and soft to announced score thresholds, counting duplicates and real neighbors removed. Changing the scores does not add any observations to the scene and does not necessarily resolve very superimposed instances. An improvement must be measured on validation before being attributed to the method.

**Calculated change in rank**: after selection of A, a box B with a score of 0.8 and IoU 0.8 becomes $0.8e^{-0.8^2/0.5}\simeq0.222$ for $\sigma=0.5$. A disjoint box C of score 0.5 remains at 0.5 and thus comes before B. With a final threshold of 0.25, B is removed. This constructed case makes explicit the roles of the decay parameter and the score threshold. Reusing a threshold selected for the initial scores without further validation can change the recall, since the values have been transformed by post-processing.

**The Gaussian parameter controls attenuation strength**: For fixed nonzero overlap $u$, the multiplier is $\exp(-u^2/\sigma)$. Increasing positive sigma weakens the penalty; as sigma tends to infinity the multiplier tends to one. As sigma approaches zero from above, nonzero overlap is strongly penalized, while zero overlap retains multiplier one. These limiting cases are derived checks of parameter meaning. They do not turn Soft-NMS into a calibrated probability model or settle the best deployment threshold.

**Blocking errors**: Keeping the old order despite the new scores, or saying that Soft-NMS can never remove a box.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Bodla et al., §4 penalties, §5 final threshold](https://arxiv.org/abs/1704.04503); [code original](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx); [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-004 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-005

Objective: Find the cause of a disappearance. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-005
Question: An object disappears from final outputs in a dense region. How can NMS be identified as the cause and a verifiable intervention chosen?
Reponse: **Expected answer**: compare boxes, scores and classes before/after NMS with the annotation; check which GT ceases to be covered, if a correct proposal existed and by which box it was deleted. If it did not exist, changing NMS will not recreate it.

**Further explanation**: Two distinct people compete within per-class NMS: sharing the label does not mean sharing the identity. If a real neighbor is removed, test threshold or Soft-NMS on validation and measure recall, duplicates, AP and effects on the tracker. Check the coordinates and the top-k upstream; a duplicate deletion that leaves the GT covered does not decrease its recall. The expected result is a substantiated cause and a measured compromise.

**Why the upstream stage must be checked**: If a real box is missing from the decoded predictions, NMS has never had the opportunity to keep it. If it exists and then disappears, finding its competitor and the overlap calculation makes it possible to test a concrete selection cause.

**Proposed ablation**: only vary the postprocessing on the same network outputs, with the same annotations and detection limits. Measure missed objects and duplicates together, then observe the affected tracks. A local improvement in a crowd can introduce more duplicates elsewhere. The correction must therefore respond to the diagnosis and remain verified on a held-out set, not just make a box reappear in a chosen image.

**Deletion log**: For each removed candidate, keep its ID, the ID of the box that suppressed it, the classes, the scores and the IoU computed in the common coordinate frame. Replaying the selection on the same predictions then isolates the post-processing without retraining the network. Measure the coverage of the ground truth with a defined matching, because two candidates on one ground-truth box are not two recalled objects. If a top-k precedes NMS, also consider the candidates lost there: raising the NMS threshold does not recover a box eliminated by this upstream filter.

**Coverage loss needs a one-to-one object interpretation**: Before and after NMS, use the same annotation-matching policy and distinguish unique covered objects from prediction count. Ten surviving boxes on one person are not ten recalled people. Conversely, removal of a duplicate may change counts without losing any object. A proposed replay should record which correct candidate was removed, its suppressor and whether another valid candidate still covers that annotation under the fixed evaluation protocol.

**Blocking errors**: Changing the threshold directly on the test set, or confusing a missing proposal with a suppression.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Soft-NMS, §§1 and 4](https://arxiv.org/abs/1704.04503); [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-NMS-005 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-006

Objective: interpret the inclusion of boxes in a deletion by IoU. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-006
Question: Two continuous boxes of the same class, $A=(0,0,100,100)$ and $B=(40,40,60,60)$, have scores $0.9$ and $0.8$. Does B being contained in A imply suppression by hard NMS at IoU threshold $>0.5$? Justify the answer.
Reponse: **Expected answer**: No. The intersection has the area of B, 400, and the union that of A, 10000: IoU $=0.04$. A is selected, then B remains since the threshold is not exceeded.

**Further explanation**: For $B\subset A$, IoU $=|B|/|A|$, and not intersection divided by area of B. This last ratio would equal 1. Geometry alone does not decide between a nested object, a part of an object and two localizations of the same instance. An analytical example of the project.

**Geometric reading**: A small box entirely contained in a large one has an intersection equal to its own area, but a union equal to the large area. The coverage of the small box and the IoU therefore answer two different questions. Replacing one with the other would change the deletion rule.

**Consequences for diagnosis**: Two surviving boxes do not prove two instances: they can be two very different localizations of the same part. Conversely, both an object and a part of it can be legitimate if the taxonomy provides for it. Check annotations, scores and the output contract before changing the overlap measure. This analytical case shows a limit to the slogan “big boxes eliminate small ones”.

**Condition of inclusion**: for $B\subset A$ and a strict deletion at threshold $\tau$, B can only be deleted by A if $|B|>\tau|A|$, provided that A is actually selected before it. At $\tau=0.5$, a contained box covering 4% of the large area is therefore very far from the condition. Reversing the scores does not change the IoU, but changes the first box retained; with more candidates, it can change the whole greedy sequence. This reasoning distinguishes the symmetry of the overlap measure from the algorithm's dependence on ranking.

**Blocking errors**: Giving an IoU of 1 as soon as there is inclusion, or automatically removing any smaller box.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [GIoU, version 2, §3, equation 1](https://arxiv.org/html/1902.09630v2); [Soft-NMS, §4 : hard NMS](https://arxiv.org/html/1704.04503); calculation of the project; [Bodla et al., Soft-NMS, §4, selection and decay; geometric counterexamples constructed by the project](https://arxiv.org/html/1704.04503v2), consulted on 2026-10-30.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-006 provenance::agent pole::A pole::C pole::E
END
