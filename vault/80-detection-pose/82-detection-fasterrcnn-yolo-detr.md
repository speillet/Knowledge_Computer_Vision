# Flashcards — Detection: Faster R-CNN, YOLO families and DETR

reference note: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-DETECTEURS-001

Objective: Situate feature sharing. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-001
Question: In Faster R-CNN, does processing regions require running the entire backbone again on each crop?
Reponse: **Expected answer**: No: the RPN and the per-region head share the convolutional feature maps computed once by the backbone; each region's representation is pooled from those shared maps.

**Further explanation**: Distinguish the cost of proposals and head; measure the number of regions and the implementation variant.

**How the computation is shared**: the backbone transforms the image into common feature maps. The proposal network and the detection head then use these representations, depending on the variant. Per-region processing adds a cost related to the number and size of the region representations, without repeating the whole feature extraction on the raw image for each region.

**Constructed comparison**: Two implementations can have the same backbone but different numbers of proposals, and therefore different latencies. Time feature extraction, proposals, per-region operations and postprocessing separately to locate the slowdown. The two-stage label describes how decisions are organized; it does not give a universal latency formula. Keep resolution, batch and thresholds in the protocol, and also compare quality on small objects and dense scenes. The product choice rests on this complete assessment rather than on the announced number of stages.

**Cost scaling**: If the backbone produces an $H'\times W'\times C$ feature map, this extraction is shared. A head then processes $R$ regions reduced to a fixed spatial representation; its work grows with the number of retained proposals, depending on the architecture. Increasing $R$ can improve coverage while adding work to the head and postprocessing, without changing the backbone's main cost. Measuring proposal recall before classification is therefore useful: a region that is never proposed cannot be recovered by a better head. A poor final score may come from RPN coverage or from the decision on regions that were already correct.

**Shared features do not make proposal count free**: After a shared backbone, increasing the retained proposal count still increases work in region pooling, per-region heads and downstream filtering. A project timing decomposition should therefore hold proposal limits fixed or report them explicitly when comparing two-stage detectors. Include crowded images where the retained population approaches its cap. A backbone-only benchmark misses the portion of cost that changes with the number of candidate regions.

**Blocking errors**: Describing the two stages as requiring a complete backbone pass for each region.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [Faster R-CNN, §III, §III-B and Table V: shared convolutional features and per-stage timing](https://arxiv.org/html/1506.01497v3). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-001 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-002

Objective: Do not generalize the whole YOLO family. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-002
Question: Why must a version be named when describing a YOLO model's anchors, losses or NMS?
Reponse: **Expected answer**: The family contains heterogeneous variants and recipes; these choices are not inferred from the name YOLO alone.

**Further explanation**: Compare full version/checkpoint/resolution and protocol.

**Why the name is not enough**: a family can change its box representation, its training assignment, its backbone and its final selection. An explanation that is correct for one paper can become false when applied to a checkpoint trained with another recipe under a similar name.

**Configuration to record (project proposal)**: Record repository and revision, architecture, data, preprocessing, resolution, target-assignment policy and the postprocessing actually executed. Pass a few known boxes through encoding and decoding. Then compare the systems on the same annotations, criteria and cost scope. An anchor-free variant does not remove the need to assign training targets. An NMS-free output must also be described by its contract. This level of precision links an error to a design decision instead of generalizing a detail to every generation.

**Versioned decoding**: Anchor offsets, edge distances and a distribution over distances do not describe the same regression tensor. Converting it to boxes requires the locations or anchors, strides, activations and conventions of the exact variant. An export can move this decoding into the graph and remove a Python step without making it unnecessary. For a given revision, encode a known box, decode it and map it back into the original image. This interface test separates a decoder error from a training difference, without claiming that a choice is shared by the entire YOLO family.

**A checkpoint name needs an export contract**: Record repository and revision, checkpoint, preprocessing, tensor layout, box decoding and postprocessing together. Two implementations carrying the same family name can expose decoded boxes or raw regression tensors and may include different filtering stages in exported graphs. A proposed parity check compares intermediate and final outputs on the same images before interpreting deployment differences as an architectural property of YOLO.

**Four versions, four contracts**: YOLO v1 has no anchors: each cell of a $7\times7$ grid predicts two boxes, one sum-squared error trains everything ($\lambda_{\text{coord}}=5$, $\lambda_{\text{noobj}}=0.5$, square roots of width and height), and NMS adds 2–3% mAP [YOLO, §2.2–§2.3]. YOLOv3 regresses from 9 k-means priors, 3 per scale, with sum-squared error on the offsets, logistic objectness and binary cross-entropy on independent class outputs [§2.1–§2.3]. YOLOX predicts one anchor-free box per location, trains with BCE and an IoU loss, assigns with SimOTA and keeps NMS: its NMS-free variant lost 0.8 AP (46.5 against 47.3) and was left out of the final models [§2.1, Table 2]. YOLOv10 trains an extra one-to-one head and uses only that head at inference, without NMS [§3.1].

**Same tensor, two boxes** (constructed, recomputed in the check script of this pass): take the raw output $(0,0,0,0)$ at cell $(10,7)$ of a stride-32 level. YOLOv3 decodes $b_x=\sigma(0)+10=10.5$ cells, a centre at $(336,240)$ px, and the size of the cell's prior [§2.1]. YOLOX 0.3.0 decodes $(t+\text{grid})\times\text{stride}$ and $e^{t}\times\text{stride}$ (`yolo_head.py` L249–L250): centre $(320,224)$, the cell's corner, and size $32\times32$ px. A decoder borrowed from the wrong version moves every centre by half a cell and replaces the prior's size by the stride.

**Blocking errors**: Attributing the original YOLO design to all generations. Decoding a checkpoint's raw tensor with the formulas of another YOLO version.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [YOLO, §2.2–§2.3: loss weights, NMS gain](https://arxiv.org/html/1506.02640v5); [YOLOv3, §2.1–§2.3: priors, decoding, losses](https://arxiv.org/html/1804.02767v1); [YOLOX, §2.1 and Table 2: anchor-free, losses, SimOTA, optional end-to-end variant](https://arxiv.org/html/2107.08430v2); [YOLOX 0.3.0 `yolo_head.py` L249–L250](https://github.com/Megvii-BaseDetection/YOLOX/blob/0.3.0/yolox/models/yolo_head.py#L249-L250); [YOLOv10, §1 and §3.1: NMS-free training with consistent dual assignments](https://arxiv.org/html/2405.14458v2). Added reasoning and the decoding contrast: project constructions; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-DETECTEURS-002 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-003

Objective: distinguish between the three assignments. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-003
Question: What is Hungarian matching used for during DETR training, and why is it different from NMS?
Reponse: **Expected answer**: It associates targets and queries to define supervision, with no-object for others; the NMS deletes predictions at inference.

**Further explanation**: The evaluator's matching is yet another, separate step. Set prediction can avoid NMS in this design.

**How supervision is assigned**: Query predictions are compared with the targets to choose a minimal-cost match. The loss uses this match to learn classes and boxes; the remaining queries learn the no-object class, depending on the formulation. This decision uses annotations during training.

**Contrast with inference**: NMS compares the available predictions, without annotations, to remove duplicates. The evaluator compares predictions with the ground truth to count errors and successes. All three operations match or compare boxes, but their inputs, objectives and moments of use differ. In a constructed diagnosis, first find the stage at which an object is wrongly supervised, removed or counted. Bipartite matching is therefore neither a universal postprocessing recipe nor an automatic proof that a deployed variant produces no duplicates.

**Matching cost**: For targets $y_i$ and predictions $\hat y_j$, the matcher seeks an injective assignment $\sigma$ minimizing $\sum_i C(y_i,\hat y_{\sigma(i)})$, where the cost combines class compatibility and geometry according to the formulation. Permuting the order of the annotations does not change the optimization problem. Once the assignment is fixed, the losses supervise the selected pairs and the no-object class of the other queries. Discrete pair selection and differentiable loss computation are two separate operations. The number of queries also bounds the number of possible outputs; a scene denser than this capacity requires an explicit check of the constraint.

**Matching cost and optimized loss have different roles**: The Hungarian cost chooses which prediction supervises each target; the subsequent loss updates the model using those assignments, including no-object supervision for unmatched queries. Changing cost weights can change assignment discontinuously even if prediction tensors are unchanged. This assignment operates with annotations during training. It is not an inference algorithm for identifying and suppressing duplicate boxes, and does not require ground truth at deployment.

**Blocking errors**: Describe the three mechanisms as a single interchangeable matching.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [DETR, §3.1, fig. 1 and equations 1 – 2](https://arxiv.org/abs/2005.12872); [Carion et al., DETR, §3.1, matching and supervision; project protocols and calculations](https://arxiv.org/html/2005.12872v3), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-003 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-004

Objective: analyze small objects after resize. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-004
Question: Track A — diagnosis: with checkpoint and images fixed, small-object AP falls when $1920\times1080$ images are resized to a $640\times640$ input with preserved aspect ratio and centered padding. Some objects originally measure $12\times9$ pixels. Which checks distinguish possible causes?
Reponse: **Expected answer**: First check that boxes are mapped back correctly through the resize and the padding. Then measure the objects' effective size and the recall of these same objects before filtering, after the score threshold, then after NMS if any. A GT covered before a filtering stage but uncovered afterward indicates a selection loss; if no correct candidate exists upstream, examine scale, features and training assignment.

**Further explanation**: The factor is $1/3$, the vertical padding 140 pixels per side, and the object becomes $4\times3$. The reference note computes a case where a perfectly located box with score $0.8$ is removed in favor of a less well located box with score $0.9$. Keep classes, IoU threshold and the original size strata when comparing recall. The small size alone does not prove that a loss of information caused the failure.

**Controllable transformation**: in this ideal letterbox, $x'=x/3$ and $y'=y/3+140$; the inverse is $x=3x'$ and $y=3(y'-140)$. A one-pixel error in the grid already corresponds to three pixels in the original, under this convention. For an object that has become $4\times3$, a displacement of one pixel represents a significant fraction of its width or height and can cause the IoU to drop sharply. Check the rounding actually applied by preprocessing rather than assuming this exact pattern for any image. Comparing candidates before filtering then makes it possible to distinguish between sensitive localization and the removal of an initially correct prediction.

**The effective object can be only a few pixels**: With scale $640/1920=1/3$, a $12\times9$ px object becomes approximately $4\times3$ px before padding, and the resized image height is 360 px with 140 px padding above and below. A box-coordinate inversion can be tested independently of feature resolution. Even a correct inversion cannot restore details lost by sampling. Compare upstream candidate coverage on the same small-object subset before attributing the entire AP drop to NMS.

**Blocking errors**: Forgetting to invert the padding, counting duplicates as recall, or tuning thresholds on the test set.

**Grading criteria for this case**: three discriminating checks (geometry, scale, filtering), explicit assumptions and a conditional conclusion. Constructed case; geometric calculation verified, no field observation.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; project diagnosis and calculations; [FPN, version 2, §3](https://arxiv.org/html/1612.03144v2); [Soft-NMS, §4](https://arxiv.org/html/1704.04503); [COCO detection evaluation: size strata](https://cocodataset.org/#detection-eval). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-004 provenance::agent pole::A pole::C pole::E cas_pole::A::diagnostic
END

## CV-DETECTEURS-005

Objective: compare detection pipelines. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-005
Question: Which information should accompany a speed comparison between two detectors?
Reponse: **Expected answer**: Hardware, backend/precision, resolution, batch, number of objects, pre/postprocessing, transfers and the latency/throughput protocol.

**Further explanation**: Also measure quality at fixed thresholds and for critical sizes. An engine time alone is not a camera-to-decision latency.

**Compare the same quantity**: Throughput measures the number of images processed per unit of time; latency is the delay experienced by one observation. An engine can improve the first while adding waiting time before an isolated image is processed.

**Proposed protocol**: State warm-up, measurement synchronization and whether copies and decoding are included, then report a latency distribution under representative load. Check quality at the same thresholds, especially for critical sizes and classes. Top-k or score settings can reduce postprocessing cost while changing recall: they are part of the configuration. A comparison useful to the product uses the same outputs, the same hardware target and the same decision requirement. An isolated FPS figure from a paper demonstrates neither this comparability nor compliance with a camera-to-decision budget.

**Measurement under load**: Record, for each image, its arrival, the start of service and the time the decision is available. Full latency includes queueing and service; maximum throughput does not account for this wait when arrivals are irregular. Dense scenes can increase decoding and NMS time while backbone time stays similar. Compare the distribution of candidate counts, then latency percentiles and the rate of late decisions. A large batch can amortize engine cost but must wait for several images before starting. The protocol must therefore reproduce the product's arrival rate and processing policy, in addition to the stated hardware.

**Throughput and single-image latency are different measurements**: A batch can increase completed images per second while making each arriving image wait for batch formation. GPU kernels can also complete asynchronously with respect to host timing. Use an explicit start/end contract and appropriate synchronization or device events for the quantity measured. Report warmup, queueing and latency quantiles under realistic arrival rates; dividing batch time by batch size is not a measurement of request-to-result latency.

**Blocking errors**: Comparing FPS figures measured over different scopes.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; Comparison protocol proposed by the project; per-stage timing in [Faster R-CNN, §IV-A, Table V](https://arxiv.org/html/1506.01497v3). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-DETECTEURS-005 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-006

Objective: Reconstruct location assignment in FCOS. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-006
Question: In FCOS as described in paper §§3.1–3.2, how is a prediction location assigned its training target, including when several annotated boxes contain it?
Reponse: **Expected answer**: Keep the boxes that contain the site and whose largest edge distance falls in the FPN level's range. If there are several, choose the box with the smallest area; if there are none, the site is negative. The selected box provides the class and regression targets.

**Further explanation**: The range applies to the largest of the four distances to the edges. This is the formulation described in these sections, before the variants with center sampling: anchor-free does not mean "without assignment".

**Role of this decision**: The site does not receive a box simply because it exists in the image; it must be admissible for the geometry and the level concerned. The selection resolves supervision conflicts before the loss is computed. NMS does not fulfil this role, since it acts on predictions during the final selection.

**Constructed example**: Two overlapping objects may contain the same site, but the size and area rule chooses the target described by this formulation. Changing the assignment then changes the positive examples and the regressions learned. To diagnose missed objects, visualize sites that are actually supervised rather than limited to the overall loss curve.

**Site and level**: The four target distances verify $l=x-x_0$, $t=y-y_0$, $r=x_1-x$ and $b=y_1-y$. Eligibility by level applies to $\max(l,t,r,b)$ in the cited formulation, not just to the box area. Two sites in the same box can therefore have different maximum distances. The "smallest area" rule chooses among the boxes that are still eligible; it does not make an out-of-range box eligible. To audit the assignment, count and view positives by object and level, keeping the exact edge conventions of the implementation. This can reveal an object that is rarely or never supervised, without immediately blaming the loss.

**The training location is not an object center requirement**: In the cited FCOS rule, an eligible location inside an assigned box predicts distances to its four edges; it need not coincide with the box center. Feature-pyramid range constraints and any center-sampling variant must be stated separately. A site inside two overlapping boxes can receive different targets after the tie-breaking rule. This makes annotation assignment a training policy, distinct from the decoder that reconstructs a box from distances.

**Blocking errors**: Assigning the target by NMS, or assuming that every site inside a box is positive on all levels.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [FCOS, version 5, §§3.1 – 3.2](https://arxiv.org/html/1904.01355v5). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-006 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-007

Objective: Calculate the distance regression targets. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-007
Question: In FCOS, image location $(x,y)=(40,30)$ is assigned to box $(x_0,y_0,x_1,y_1)=(20,10,90,70)$. Using continuous input-pixel coordinates with a top-left origin, what are its four targets $(l,t,r,b)$ to the left, top, right and bottom edges?
Reponse: **Expected answer**: $(l,t,r,b)=(x-x_0,y-y_0,x_1-x,y_1-y)=(20,20,50,40)$ pixels.

**Further explanation**: Decoding $(x-l,y-t,x+r,y+b)$ restores $(20,10,90,70)$. The site is already expressed in the image: do not multiply it again by the stride. Constructed analytical example, computed without running a network.

**Geometric interpretation**: Each value is a length from the site to a face in the same coordinate frame. The sum left + right gives the box width, and top + bottom its height. The site is not necessarily the center, so distances can be asymmetrical.

**Round-trip check**: Encode a known box, decode it, then apply the inverse of the resize and padding to recover the original annotation. Also test a site near an edge. If another implementation normalizes the targets by the stride, declare it and invert it exactly once. A network can learn numerically consistent values while producing wrong boxes if these conventions are mixed at the interface.

**Geometry of the site**: The given distances have sums $l+r=70$ and $t+b=60$, equal to the width and height of the box. The box centre is $(55,40)$, distinct from the site $(40,30)$. The center-ness target described by FCOS is $\sqrt{\min(l,r)/\max(l,r)\;\min(t,b)/\max(t,b)}$, here $\sqrt{(20/50)(20/40)}=\sqrt{0.2}\simeq0.447$. It expresses geometric centrality, not a guaranteed IoU of the predicted box. This reading links distance asymmetry, the auxiliary target and ranking, while keeping the computed target values separate from the outputs actually learned.

**A site on the boundary has a zero distance**: Constructed boundary case: moving the site to $(20,30)$ on the same box gives distances $(0,20,70,40)$ px. Algebraic decoding still recovers the box, while the geometric centerness target becomes zero. Whether this boundary site is eligible depends on strict versus non-strict containment in the training implementation and any center-sampling rule. Separate that assignment convention from the distance formula, and test sites just inside and outside rather than inferring eligibility from nonnegative decoded lengths.

**Blocking errors**: Confusing these distances with centre/width/height, expressing them in feature-map cells, or adding 1 to continuous coordinate differences.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [FCOS, version 5, §3.1, equation 1 and decoding](https://arxiv.org/html/1904.01355v5); project calculation. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-DETECTEURS-007 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-008

Objective: Explain the modulation of easy negatives by Focal Loss. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-008
Question: In dense detection, how does Focal Loss reduce the dominance of many easy negatives beyond simple class weighting?
Reponse: **Expected answer**: It multiplies the cross entropy by $(1-p_t)^\gamma$, where $p_t$ is the probability of the correct label and $\gamma>0$. An easy negative has $p_t$ close to 1: its contribution decreases sharply. A class weighting alone does not distinguish between easy and difficult examples of this class.

**Further explanation**: The complete form is $-\alpha_t(1-p_t)^\gamma\log p_t$. $\alpha_t$ weights the class; $\gamma=0$ returns the weighted cross entropy. At $\gamma=2$ and $p_t=0.9$, the factor is $0.01$. The relative focus on difficult cases does not protect against poor annotations.

**What the modulation targets**: For a negative correctly classified as background, the probability of the correct label can be close to one. Its reduced loss prevents many easy cases from overwhelming learning of more difficult examples. Class weighting acts on another dimension of imbalance.

**Limit of diagnosis**: A difficult example can be informative or misannotated. Giving it greater relative importance therefore does not guarantee better supervision. In a constructed ablation, keep assignment and data fixed, and compare contribution distributions and errors by size and class. The formula describes a modification of the training objective, not a promise of better recall for every detector configuration.

**Contribution and gradient**: Comparing two examples of the same class with $p_t=0.99$ and $p_t=0.5$ gives, at $\gamma=2$, factors of $10^{-4}$ and $0.25$ respectively. The second thus has a much greater relative weight. The gradient is not that of a cross-entropy multiplied by a fixed constant: the factor itself depends on $p_t$, and its derivative takes part in the optimization. The number of positives, the assignment rules and the loss reduction over the batch still matter. To interpret a training run, review these conventions before attributing an improvement or an instability to the choice of $\gamma$ alone.

**The logit gradient includes a second term**: For binary cross entropy with $p_t=\operatorname{sigmoid}(z_t)$ and no alpha factor, $FL=-(1-p_t)^\gamma\log p_t$ has derivative $\partial FL/\partial z_t=(1-p_t)^\gamma[\gamma p_t\log p_t-(1-p_t)]$. This project derivation follows the product and chain rules. At $\gamma=0$ it becomes $p_t-1$. Detaching the modulator drops the logarithmic term, so it is a different optimization rule even when the forward values are identical. The sign of $z_t$ must encode the correct binary target.

**Blocking errors**: Confusing $p_t$ with the object probability for a negative, or saying that the loss eliminates all negatives.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [Focal Loss, version 2, §§2 and 3.1 – 3.2, equation 5](https://arxiv.org/html/1708.02002v2). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-008 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-009

Objective: Explain the GIoU signal for disjoint boxes. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-009
Question: Two axis-aligned rectangular boxes $A$ and $B$ remain strictly disjoint during a small displacement. Why does loss $1-\operatorname{IoU}$ provide no guidance for this displacement, and which term does GIoU add?
Reponse: **Expected answer**: The intersection remains zero, so IoU remains zero and the loss stays constant at 1. GIoU subtracts from IoU the empty fraction of the smallest axis-aligned rectangle containing the two boxes: $|C\setminus(A\cup B)|/|C|$. This geometric term can vary even without overlap and provide a signal for regression.

**Further explanation**: For $A=(0,0,2,2)$ and $B=(3,0,5,2)$ in continuous coordinates, the union is 8 and $|C|=10$: GIoU $=-0.2$, loss $=1.2$. Moving $B$ closer, to $(2.5,0,4.5,2)$, gives a loss of $10/9$ while IoU is still zero. Constructed calculation; no general guarantee of convergence.

**Why the additional term helps**: Relative positions change the empty space of the enclosing rectangle even when the intersection does not change. The loss thus varies with the geometry where the overlap term alone is flat in this case. This does not mean that every direction of motion receives an informative signal.

**Proposed validation**: Check the calculation on simple boxes, then separate the localization signal from score ranking. A better loss on pairs of boxes does not imply a better AP if assignment, scores or annotations are the problem. Compare variants with the same data and recipe as far as possible, examining concrete localization errors on held-out data.

**Information still limited**: For two disjoint boxes whose union and enclosing rectangle keep the same area, GIoU can remain constant in certain local directions. The additional term provides a signal in many cases without becoming a complete and perfectly conditioned measure of all movements. Edges where intersection or enclosing rectangle change also introduce regime changes in the derivative. A small perturbation test of each coordinate makes it possible to compare the variations of loss to the expected geometry. This analysis concerns the regression of valid boxes; it does not correct a bad target matching or a wrong class.

**Enclosing geometry distinguishes some disjoint positions**: Constructed example: two unit boxes separated horizontally by a one-unit gap have enclosing area three and union area two, giving GIoU $=-1/3$. Increasing that gap to two units makes the enclosing area four and GIoU $=-1/2$. The IoU loss remains one in both cases while the generalized term changes. This does not promise a nonzero gradient in every possible local movement direction.

**Blocking errors**: Claiming that non-overlapping boxes force GIoU to zero, or replacing $C$ with the union of the two boxes.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [GIoU, version 2, §3.1 and algorithms 1 – 2](https://arxiv.org/html/1902.09630v2); project calculation. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-DETECTEURS-009 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-010

Objective: explain the contribution of the lateral connections of FPN. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-010
Question: For small-object detection, what do FPN's lateral connections provide beyond simply upsampling the backbone's final feature map?
Reponse: **Expected answer**: They combine the semantically strong deep features brought down by the top-down path with the finer, better-localized backbone features of the same level. Upsampling the deep map alone does not restore the spatial information of these finer levels.

**Further explanation**: In the original FPN: a $1\times1$ lateral projection, addition at a common resolution after nearest-neighbour upsampling by 2, then a $3\times3$ convolution. It is a feature pyramid computed from one image, not a set of resized images. It does not recover details already lost by the input resize.

**Difference between computation and observation**: Interpolating a deep map increases its number of positions but does not recreate the details it no longer represents. The lateral connections, by contrast, bring features computed at finer resolutions of the backbone. Their fusion combines localization and semantic information.

**Discriminating check**: Compare small and large objects at a fixed input resolution, changing only access to the finer levels. Review recall, localization and cost. If the small object already covers almost no pixels in the input, an FPN does not restore the physical information destroyed by acquisition or resizing. The feature pyramid is a building block of the system, not a substitute for a suitable image contract.

**Fusion recurrence**: Write $M_l=L_l(C_l)+\operatorname{Upsample}(M_{l+1})$ for the fused map of the top-down path, then $P_l=\operatorname{Conv}_{3\times3}(M_l)$ for the smoothed output of the level, where $C_l$ is the backbone feature at level $l$ and $L_l$ the lateral channel projection. Spatial sizes and alignment must be compatible for the addition. A misalignment can keep tensor shapes valid while harming localization. The map therefore merges observed lateral information with upsampled context; it does not create a high-resolution image. Relating the strides to the actual object sizes helps choose which outputs and levels to analyze.

**Upsampling adds locations, not recovered measurements**: A coarse feature map interpolated to a finer grid still derives from the same coarse samples. Lateral features supply separately computed finer spatial evidence, which is why the fusion differs from interpolation alone. Test thin or small objects at matched input resolution and training protocol when assessing that contribution. No feature-pyramid mechanism can recover a physical defect that acquisition and input resizing have already removed.

**Blocking errors**: Attributing newly observed detail to interpolation alone, or confusing FPN with an image pyramid.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [FPN, version 2, §3 and figure 3](https://arxiv.org/html/1612.03144v2). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-010 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-011

Objective: Distinguish class, localization and duplicate errors. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-011
Question: Three independent cases each have one “car” GT instance, without ignore/crowd annotations. With TIDE thresholds $t_b=0.1$ and $t_f=0.5$, which error describes each FP: (a) “truck,” IoU $0.8$; (b) “car,” IoU $0.3$; (c) “car,” IoU $0.8$, with the GT already matched to a higher-score box?
Reponse: **Expected answer**: (a) Classification: sufficient localization, wrong class. (b) Localization: correct class, intermediate overlap. (c) Duplicate: class and localization sufficient, but the GT is already matched to a higher-scoring detection.

**Further explanation**: TIDE also distinguishes the combined classification-and-localization error, background errors, and missed GT not already explained by a classification or localization error. Orient checks to labels/classes, geometry or postprocessing as appropriate, without automatically inferring a cause. The number of FP alone does not measure the loss of AP: their score ranking also counts.

**Usefulness of the categories**: they indicate where to look for an explanation, without automatically identifying the cause. A wrong class can come from an ambiguous taxonomy or from the model; poor localization can come from the network or from a coordinate transformation; a duplicate can reflect the postprocessing.

**Proposed protocol**: Select examples of each type, keep the image, the annotations and the outputs of each stage, then test one hypothesis at a time. The rank of errors by score matters for AP: correcting several low-score errors does not necessarily have the same effect as correcting one very confident error. An oracle correction is a tool for diagnosing the protocol, not predicting the gain of an actual retraining.

**Counted error and cause**: In the duplicate case, removing the first correct prediction could turn the second into a TP without improving object recall. This shows that the categories also depend on score ranking and matching rules. Conversely, correcting a class can recover a GT and simultaneously remove an FP, depending on the protocol. The oracle gains of several types do not necessarily add up like independent error counts. For a real intervention, freeze the initial predictions, apply one precise correction and recompute the complete metric. The diagnosis names a type of observed error; the causal mechanism remains to be established.

**An error category is not a causal diagnosis**: The same localization-type false positive can result from poor box regression, incorrect inverse resizing or an annotation convention mismatch. TIDE-style categories organize observed evaluation errors; identifying the cause requires intermediate outputs or controlled ablations. A duplicate category similarly depends on score ordering and prior matching. Keep the evaluator fixed when comparing interventions so changed category counts are not mistaken for proof of one internal failure mechanism.

**Blocking errors**: Counting (c) as a second TP, or attributing (a) to poor localization.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [TIDE, version 2, §2.2: types and weighting of errors](https://arxiv.org/html/2008.08115v2); built cases of the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-011 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-012

Objective: Diagnose a false positive that may come from a missing annotation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-012
Question: A detector produces a highly confident box with no matched GT, although the image appears to contain an object of the target class. What should be checked before concluding that it confused the background with an object?
Reponse: **Expected answer**: Compare the image with the annotation policy: real presence and class, box conventions, exclusions and crowd/ignore rules. If the object should have been annotated but was omitted, a non-ignored detection is counted as an FP despite its visual relevance. The model's confidence is not enough to prove the omission.

**Further explanation**: The project proposes to arbitrate ambiguous cases, version the corrections and re-evaluate all models on the same corrected GT, keeping the previous results. TIDE documents missing objects and wrong crowd flags; this makes neither every FP suspect nor every annotation set exhaustive.

**Proposed arbitration**: Have the case checked against an annotation rule common to all models, with access to the image and the relevant context. Keep intentionally excluded objects separate from accidental omissions. Document the version and the reasons for each correction.

**Limits of the conclusion**: a model can be very confident and wrong; apparent plausibility is not enough to create new ground truth. Re-evaluating all systems on the same corrected version avoids favoring the one whose outputs triggered the review. The review examines the quality of the benchmark as well as that of the detector, and its outcome must be traceable.

**Annotation audit**: Sample disagreements from several models and image regions, drawn independently of their scores. An audit limited to one system's most confident predictions may favor its own biases. For each case, keep the image, the inclusion rule, the old label, the arbitration and the new version of the dataset. A crowd or ignore region does not necessarily follow the same counting rule as an isolated object; apply the rules of the exact evaluator before calling a detection an FP. After correction, recompute all comparisons and keep the previous results as history, without mixing metrics produced on two different ground truths.

**How often the annotation is at fault**: among Mask R-CNN's 100 most confident background errors on COCO, TIDE's Table 5 bins 57 as misannotations: 34 bad annotations, 20 ambiguous cases such as a mannequin, a sculpture or a reflection, and 3 missing crowd flags; §3.4 rounds this to 50 of 100. The sample holds only the most confident errors of one model, so it justifies inspecting a confident unmatched box, not presuming that half of all FPs are annotation errors.

**Why every model is re-scored** (constructed, recomputed in the check script of this pass): four objects are annotated and a fifth real one is not. Model A ranks TP, the unannotated object, then three TPs; model B finds the four annotated objects and misses the fifth. On the old ground truth A scores $86/101\approx0.851$ and B 1. Once the fifth object is annotated, A scores 1 while B's recall stops at 0.8 and it scores $81/101\approx0.802$: the correction reverses the ranking.

**Evaluator check**: at pycocotools commit `8c9bcc3`, `_prepare` overwrites a dataset's `ignore` field with `iscrowd` (L107–L109), so marking a doubtful region `ignore=1` does not stop its detections from counting as FPs; only `iscrowd=1` does, under the crowd overlap rule.

**Blocking errors**: Removing inconvenient FPs for a single model only, or automatically turning any confident detection into an annotation. Re-scoring only the model whose detections revealed the omission.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [TIDE, version 2, §3.4, Appendix D with Table 5, Appendix E: misannotated top errors and ignored detections](https://arxiv.org/html/2008.08115v2); [cocoapi cocoeval.py at 8c9bcc3, `_prepare` L107–L109](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L107-L109); correction protocol and the two-model case constructed by the project.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-012 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-013

Objective: Distinguish instances, classes and per-instance labels. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-013
Question: A task requires localizing three cars and two bicycles, with one label per object. Is this necessarily multilabel classification per box? Distinguish the number of instances, classes present and labels per instance.
Reponse: **Expected answer**: No: there are five instances, two classes present, but one label per instance in this contract. Detection can produce multiple instances of the same class. Multi-label means that multiple labels are valid for the same instance, depending on the taxonomy.

**Further explanation**: Hierarchical labels such as "vehicle" and "car" can coexist if the annotations allow it; two exclusive classes proposed for the same object remain an ambiguity. YOLOv3 uses independent logistic classifiers, but the labels actually output also depend on thresholds and postprocessing. A per-class NMS guarantees neither a single label per instance nor a single box per class.

**Contract example**: Five distinct objects in two categories require five location and class decisions, without imposing multiple labels on each. A hierarchical taxonomy can add another rule, but it must then be defined in the annotations and expected outputs.

**Impact on the pipeline**: Close boxes can represent duplicates, competing categories, or separate objects. NMS does not know this semantics directly. Examine labels by instance and annotation coverage before turning a multiclass output into a deletion rule. This distinction links supervision, postprocessing and evaluation, instead of deducing the contract from the number of labels present in the image alone.

**Probability and label contract**: A softmax per box makes the probabilities of the categories share a total mass, which corresponds to an exclusive choice within that set. This exclusivity applies to the scores, not necessarily to the output: torchvision 0.29's Faster R-CNN turns every class whose softmax score exceeds 0.05 into a separate detection before per-class NMS, so one proposal can still be output with two labels. Independent sigmoids can represent several labels at once, but they do not automatically make "vehicle", "car" and exclusive categories consistent. The annotation set and the decision rule must specify these relationships. At the image level, aggregating the presence of a category can lose the number of instances: three cars become a single presence indicator. Keeping instance identities and their boxes avoids confusing scene classification with object detection.

**Multiple instances and multiple valid labels are separate axes**: A single box can have several valid attributes such as car, red and damaged, while an image can contain many boxes each with one exclusive object class. The output schema should specify which labels describe an instance and which refer to the whole image. This determines loss and decision policy; the mere presence of two object categories does not force independent multilabel classification for every detection.

**Blocking errors**: Confusing multiple objects in an image with multiple labels for one object, or limiting the output to one box per category.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [YOLOv3, version 1, §§2.2 – 2.3](https://arxiv.org/html/1804.02767v1); [Torchvision 0.29, batched_nms: separation of categories](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html); [torchvision 0.29.0, roi_heads.py L680–L735: one detection per class above the score threshold](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/roi_heads.py#L680-L735); examples of project contracts. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-013 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-014

Objective: Assign, encode and decode an anchor with the right box-coder weights. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-014
Question: In input pixels $(x_1,y_1,x_2,y_2)$, an image has one ground-truth box $(36,60,196,156)$ and an anchor $(36,36,164,164)$; another anchor overlaps that ground truth with IoU $0.78$. (a) Compute the anchor's IoU with the ground truth and the training label it receives under the Faster R-CNN RPN rule and under the RetinaNet rule. (b) Compute its Faster R-CNN regression targets $(t_x,t_y,t_w,t_h)$. (c) torchvision 0.29 builds R-CNN box-head targets with coder weights $(10,10,5,5)$ and RPN targets with $(1,1,1,1)$. An exported model is decoded in C++ with $(1,1,1,1)$ for every head. If the box head, given this $128\times128$ box as a proposal, outputs exactly its training targets, which box does the deployment draw, and why?
Reponse: **Expected answer**: (1) Intersection $128\times96=12288$ px², union $16384+15360-12288=19456$ px², IoU $\approx0.632$. RPN: ignored, because the IoU is neither above 0.7 nor the highest for this box (0.78 elsewhere), and not below 0.3. RetinaNet: positive, because the IoU reaches 0.5. (2) Centres $(100,100)$ and $(116,108)$, sizes $128\times128$ and $160\times96$: $t=(16/128,\ 8/128,\ \log1.25,\ \log0.75)=(0.125,\ 0.0625,\ 0.223,\ -0.288)$. (3) The head learned $(10t_x,10t_y,5t_w,5t_h)=(1.25,\ 0.625,\ 1.116,\ -1.438)$, and torchvision's decoder divides by the weights before inverting eq. 2. Decoding with $(1,1,1,1)$ moves the centre by $(160,80)$ px instead of $(16,8)$ and multiplies the sizes by $1.25^5$ and $0.75^5$: about $(64.7,164.8,455.3,195.2)$ instead of $(36,60,196,156)$. The weights belong to the trained model's output contract.

**Further explanation**: Eq. 2 measures centre offsets in anchor widths and heights and sizes as log ratios, so scaling a box and its anchor together leaves $t$ unchanged. Faster R-CNN marks as positive the highest-IoU anchor or anchors of each box and any anchor above 0.7, as negative a non-positive anchor below 0.3 for every box, and leaves the rest out of the loss; torchvision's matcher uses $\ge0.7$ and $<0.3$. RetinaNet assigns at IoU 0.5, sends $[0,0.4)$ to background and ignores $[0.4,0.5)$. Its §4 adapts the RPN rule with these thresholds without restating the highest-IoU clause; torchvision enables that clause for RetinaNet too. The same anchor is therefore unsupervised in one detector and a regression positive in the other.

**Why the weights exist and how the error hides**: Fast R-CNN normalizes its regression targets to zero mean and unit variance; the fixed weights $(10,10,5,5)$ divide the targets by 0.1, 0.1, 0.2 and 0.2, without mean subtraction. The reverse mistake, an RPN output decoded with $(10,10,5,5)$, divides offsets by 10 and log sizes by 5 and gives about $(34.7,40.4,168.5,161.2)$, close to the anchor: proposals that barely move. Both mistakes vanish when $t=0$, so a proposal that already fits its object decodes correctly whatever the weights. The clamp of $t_w$ and $t_h$ at $\log(1000/16)\approx4.14$, applied after the division, does not act here. Test by encoding a known box with the training coder and decoding it with the deployment code. Constructed example; recomputed in the check script of this pass.

**Blocking errors**: Computing $t_x$ from corner differences or normalizing $t_y$ by $w_a$. Writing $t_w=(w-w_a)/w_a$. Labelling the anchor RPN-positive because its IoU exceeds 0.5. Treating RetinaNet's $[0.4,0.5)$ band as background. Assuming that training absorbs any coder weights, so that decoding can ignore them.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [Faster R-CNN, §III-A2, labelling rule and eq. 2](https://arxiv.org/html/1506.01497v3); [RetinaNet, §4, Anchors and Box Regression Subnet](https://arxiv.org/html/1708.02002v2); [Fast R-CNN, §2.3, multi-task loss: target normalization](https://arxiv.org/abs/1504.08083); [torchvision 0.29.0, _utils.py L103–L116 and L183–L213: encoding and decoding with weights; L339–L345 and L384–L387: matcher thresholds](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/_utils.py#L183-L213); weights and matchers in [rpn.py L164–L173](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/rpn.py#L164-L173), [roi_heads.py L542–L544](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/roi_heads.py#L542-L544) and [retinanet.py L462–L470](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/retinanet.py#L462-L470). The boxes, labels and wrong decodings are project constructions.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-DETECTEURS-014 provenance::agent pole::A pole::C pole::E
END
