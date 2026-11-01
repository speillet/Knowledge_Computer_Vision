# Flashcards — NMS — suppressing redundant detections

reference note: [[80-detection-pose/references/81-nms|NMS]]. Source: Agent.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-NMS-001

Objective: unroll hard NMS. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-001
Question: Three continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$ and $C=(20,0,30,10)$ have scores $0,9;0,8;0,7$. Which boxes are retained by hard NMS that suppresses candidates with IoU greater than 0.5?
Reponse: **Expected answer**: select $A$, delete $B$ because their intersection is 80, union 120 and IoU $2/3>0,5$; then keep $C$, disjoint. The output is $A,C$.

**Further explanation**: calculation uses `xyxy` continuous without `+1`. The selection is greedy and follows the scores, without merging the boxes. At threshold 0,7, this example would keep all three: threshold check redundancy, not directly semantic accuracy. Result executed in the arithmetic example of the repository.

**Reasoning on instances**: Overlay is used as an index of redundancy between predictions, without knowing the real identity of the objects. If A and B represent two close people, deleting B can remove a real instance; if they represent the same part, the deletion can instead be useful.

**check**: keep the outputs before and after the operation and check which annotations remain covered. The threshold therefore settles a compromise depending on the scene. A remote box remains candidate even with a lower score, as long as it passes the other filters in the pipeline. This reading avoids turning the gluton selection into a "one box per image" or "one box per class" rule.

**Selection is not transitive**: build three boxes of the same size with $A=(0,0,10,10)$, $B=(3,0,13,10)$ and $C=(6,0,16,10)$. The IoU $A/B$ and $B/C$ are worth $7/13>0,5$, but $A/C=4/16=0,25$. With decreasing scores A, B, C, NMS keeps A, deletes B then keeps C: B deleted does not in turn delete its neighbors. This distinguishes the greediness algorithm from a grouping into related components of the overlap graph. The result depends on the ranking and does not automatically look for the set of maximum score sum boxes.

**Blocking errors**: delete $C$ for the sole reason of its lower score, or treat the output as an average of $A$ and $B$.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Soft-NMS, §4](https://arxiv.org/abs/1704.04503); [convention hard NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html); [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-NMS-001 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-002

Objective: There are three thresholds. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-002
Question: In object detection, how do the score threshold, NMS IoU threshold and evaluation IoU threshold differ?
Reponse: **Expected answer**: the score threshold filters predictions according to their confidence; the NMS threshold compares two predictions to reduce duplicates; the evaluation threshold IoU compares a prediction to an annotation according to the protocol.

**Further explanation**: The same number does not give the same meaning. The NMS does not consult the GT at the time of inference. Changing a score threshold can change recall and cost before NMS; changing NMS affects duplicates and retained neighbors; changing the rating threshold changes the location requirement. Record all three separately.

**Example of distinction**: A prediction can pass the score threshold, be removed for its overlap with another prediction, and never reach evaluation. Conversely, two preserved boxes can correspond to a single object and one can become a duplicate in the measurement protocol.

**Proposed investigation**: Log the steps and their parameters separately, then calculate the coverage of the same annotations at each stage. Changing the evaluation requirement IoU does not change the boxes that the system has produced; changing the threshold NMS may change them. Set the parameters to validation, then freeze the protocol. An identical numerical value, for example 0,5, does not bring the responsibilities of these three decisions closer together.

**Separate setting and measurement**: take a candidate with a score of 0,4, from IoU 0,8 with another prediction, but from IoU 0,6 with a score of GT. A score threshold at 0,5 discards it before any measurement; at an allowable score, a NMS at 0,7 can remove it; if it survives, it satisfies a localization requirement at 0,5 but not at 0,75, under the other rules of matching. These three comparisons relate to different objects. To assign a recall drop, keep counters after each step with constant evaluation protocol, rather than simultaneously changing the three thresholds.

**Blocking errors**: Use the AP50 threshold to decide directly which predictions are suppressed between them, or say that NMS requires the GT.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html); [COCO](https://cocodataset.org/#detection-eval); [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-NMS-002 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-003

Objective: Choose the scope of a deletion. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-003
Question: Two candidates from different classes have scores $0{,}9$ and $0{,}8$ and IoU $0{,}8$. With NMS threshold $0{,}5$, what tradeoff distinguishes global suppression from per-class suppression?
Reponse: **Expected answer**: The global NMS retains only the score candidate $0{,}9$; the class NMS retains both. This protects two objects of different classes, but also leaves two competing labels on the same instance. Choose whether the annotations allow these two detections or impose an exclusive class.

**Further explanation**: Person and bicycle can be two legitimate objects that overlap. Two exclusive categories of the same piece require a class decision; taking the maximum score does not guarantee the right label. A NMS per class also retains several disjoint instances of this class: it does not impose one box per category. Scores, coordinate frames and exit rules must be comparable.

**Constructed case**: A person and their bike can provide two valid categories that overlap. Two types of exclusive pieces on the same instance pose another question: you have to decide the label, not just prevent boxes from being deleted.

**Proposed Validation**: Clearly annotate instances and taxonomy, then examine interclass conflicts and neighbors of the same class. One NMS per class protects different categories but not two people very close to each other. The right choice is measured on errors useful to the product, with scores and thresholds recorded, without inferring a physical identity from the overlap alone.

**Conflict of taxonomy built**: If the same instance receives the scores 0,8 for "vehicle" and 0,75 for "car", the two labels can be consistent in a hierarchical taxonomy but redundant in a single category contract. Set this policy before choosing deletion. With the same geometry, a person holding a bike and a part receiving two exclusive classes ask for different decisions. Separately testing interclass conflicts and neighbors of the same class helps to measure what class separation actually protects. The highest score does not indicate, by construction, whether two hypotheses share a physical identity.

**Blocking errors**: Believe that NMS per class solves interclass confusions, or that NMS global knows the real identity of objects.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Torchvision 0.29, batched_nms: description and threshold](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html), Consult the 2026-10-21; built case of the project; [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), Consult the 2026-10-30.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-NMS-003 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-004

Objective: Explain the effect of Soft-NMS. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-004
Question: How does Gaussian Soft-NMS differ from hard NMS, and why must candidates be reordered after a score penalty?
Reponse: **Expected answer**: instead of an immediate deletion beyond a overlap, it reduces the score of each candidate according to its overlap with the retained box $M$: $s_i\leftarrow s_i\exp(-\operatorname{IoU}(M,b_i)^2/\sigma)$, with $\sigma>0$. The modified scores change the next maximum, so the order must be recalculated.

**Further explanation**: The Gaussian penalty acts on recoveries without the same discontinuous threshold as hard NMS. A final score threshold can eliminate boxes that have become too low: Soft-NMS does not guarantee to keep everything or resolve all occlusionss. Specify variant and area convention before a comparison.

**Interpretation of the order**: After penalization, a candidate initially second may become less priority than another candidate with little coverage. Resuming the current maximum is part of the greedy logic. Navigating once the old ranking would correspond to another procedure.

**Example of check**: Record at each step box retained and remaining scores on a small known set. Then compare hard and soft to announced score thresholds, counting duplicates and real neighbors removed. Changing the scores does not add any observations to the scene and does not necessarily resolve very superimposed instances. An improvement must be measured on validation before being attributed to the method.

**Calculated change in rank**: after selection of A, a box B with a score of 0,8 and IoU 0,8 becomes $0,8e^{-0,8^2/0,5}\simeq0,222$ for $\sigma=0,5$. A disjointed box C of score 0,5 remains at 0,5 and thus passes before B. With a final threshold of 0,25, B can be removed. This constructed case makes explicit the roles of the decay parameter and the score threshold. Reusing a selected threshold for initial scores without further validation can change the recall, since the values have been transformed by postprocessing.

**Blocking errors**: Keep the old order despite the new scores or say that Soft-NMS can never remove from the box.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Bodla et al., §4 penalties, §5 final threshold](https://arxiv.org/abs/1704.04503); [code original](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx); [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-004 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-005

Objective: Find the cause of a disappearance. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-005
Question: An object disappears from final outputs in a dense region. How can NMS be identified as the cause and a verifiable intervention chosen?
Reponse: **Expected answer**: compare boxes, scores and classes before/after NMS with the annotation; check which GT ceases to be covered, if a correct proposal existed and by which box it was deleted. If it didn't exist, changing NMS won't recreate it.

**Further explanation**: Two distinct people compete in one NMS per class: sharing the label does not mean sharing the identity. If a real neighbor is removed, test threshold or Soft-NMS on validation and measure recall, duplicates, AP and effects on the tracker. Check the coordinates and the top-k upstream; a duplicate deletion that leaves the GT covered does not decrease its recall. The expected result is a substantiated cause and a measured compromise.

**Why the upstream should be preserved**: If a real box is missing from the decoded predictions, NMS has never had the opportunity to keep it. If it exists and then disappears, finding its competitor and the overlap calculation makes it possible to test a concrete selection cause.

**Proposed ablation**: only vary the postprocessing on the same network outputs, with the same annotations and detection limits. Measure missed objects and duplicates together, then observe the affected time trackss. A local improvement in a crowd can introduce more duplicates elsewhere. The correction must therefore respond to the diagnosis and remain verified on a reserved set, not just make a box reappear in a chosen image.

**Deletion log**: For each candidate removed, keep their ID, the one in the box that deleted it, the classes, scores and the IoU calculated in the common coordinate frame. Then replaying the selection on the same predictions makes it possible to isolate the postprocessing without retraining the network. Measure the coverage of the GT with a defined matching, because two candidates on a GT are not two objects recalled. If a top-k precedes NMS, consider also the candidates lost there: increasing the threshold NMS does not recover a box eliminated by this upstream filter.

**Blocking errors**: Change the threshold directly on the test set or confuse proposal error and deletion.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [Soft-NMS, §§1 and 4](https://arxiv.org/abs/1704.04503); [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-NMS-005 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-006

Objective: interpret the inclusion of boxes in a deletion by IoU. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-NMS-006
Question: Two continuous boxes of the same class, $A=(0,0,100,100)$ and $B=(40,40,60,60)$, have scores $0{,}9$ and $0{,}8$. Does B being contained in A imply suppression by hard NMS at IoU threshold $>0{,}5$? Justify the answer.
Reponse: **Expected answer**: No. The intersection has the area of B, 400, and the union that of A, 10000: IoU $=0{,}04$. A is selected, then B remains since the threshold is not exceeded.

**Further explanation**: For $B\subset A$, IoU $=|B|/|A|$, and not intersection divided by area of B. This last report would be worth 1. Geometry alone does not slice between nested object, part of object and two locations of the same instance. An analytical example of the project.

**Geometric reading**: A small box entirely contained in a large one has an intersection equal to its own area, but a union equal to the large area. The cover for the small box and the IoU therefore answer two different questions. Replacing one with the other would change the deletion rule.

**Consequences of diagnosis**: Two surviving boxes do not prove two instances: they can be two very different locations of the same part. Conversely, both object and part of object can be legitimate if the taxonomy so provides. Check annotations, scores, and the exit contract before changing the overlap measure. This analytical case shows a limit to the slogan “big boxes eliminate small ones”.

**Condition of inclusion**: for $B\subset A$ and a strict deletion at threshold $\tau$, B can only be deleted by A if $|B|>\tau|A|$, provided that A is actually selected before it. At $\tau=0,5$, a contained box covering 4% of the large area therefore remains very far from the condition. Reversing the scores does not change the IoU, but changes the first box retained; with more candidates, it can change the whole greedy suite. This reasoning distinguishes the symmetry of the overlap measure and the algorithm's dependence on ranking.

**Blocking errors**: Give a IoU of 1 as soon as there is inclusion, or automatically remove any smaller box.
Source: [[80-detection-pose/references/81-nms|NMS reference]]; [GIoU, version 2, §3, equation 1](https://arxiv.org/html/1902.09630v2); [Soft-NMS, §4 : hard NMS](https://arxiv.org/html/1704.04503); calculation of the project; [Bodla et al., Soft-NMS, §4, selection and decay; built geometric counterexamples](https://arxiv.org/html/1704.04503v2), consult the 2026-10-30.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-006 provenance::agent pole::A pole::C pole::E
END
