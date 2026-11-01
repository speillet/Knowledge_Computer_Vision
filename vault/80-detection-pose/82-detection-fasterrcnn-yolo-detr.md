# Flashcards — Detection: Faster R-CNN, YOLO families and DETR

reference note: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-DETECTEURS-001

Objective: Find the sharing of features. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-001
Question: In Faster R-CNN, does processing regions require running the entire backbone again on each crop?
Reponse: **Expected answer**: No: the design shares features between RPN and head by region, with extraction of regional representations.

**Further explanation**: Distinguish the cost of proposals and head; measure the number of regions and the implementation variant.

**Reading the calculation share**: the backbone transforms the image into common feature maps. The network of proposals and the head then exploit these representations according to the variant. Regional processing adds a cost related to the number and size of regional representations, without requiring that all extraction be repeated on the raw image for each.

**Example of comparison built**: Two implementations can have the same backbone but different number of proposals, and therefore different lead times. Measure extraction, proposals, regional operations and postprocessing separately to identify the drop. A two-stage category describes the organization of decisions; it does not give a universal latency formula. Keep resolution, batch and thresholds in the protocol, and also compare quality on small objects and dense scenes. The product choice is based on this complete balance sheet, rather than just the number of steps announced.

**Cost scales**: If the backbone produces a map of $H'\times W'\times C$ features, this extraction is shared. A head then processes $K$ regions reduced to a fixed spatial representation; its work grows with the number of proposals selected, according to the architecture. Increasing K can improve coverage while weighing down head and post-processing, without changing the backbone’s main cost. Measuring the recall of proposals before classification is therefore useful: a region never proposed will not be found by a better head. A poor final score may come from RPN coverage or from the decision on already correct regions.

**Blocking errors**: Describe two steps as two mandatory complete backbones per region.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [Faster R-CNN, §3: sharing convolutions](https://arxiv.org/abs/1506.01497).
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

**Why the name is not enough**: a family can evolve in the representation of the boxes, the training assignment, the bones and the final selection. A correct explanation for an article can become false if applied to a checkpoint from another recipe with a neighboring name.

**reference note proposed configuration**: Record repository and revision, architecture, data, preprocessing, resolution, monitoring policy and postprocessing actually executed. Check some known boxes through encoding and decoding. Then compare the systems on the same annotations, criteria and costs included. An anchor-free variation does not eliminate the need to assign learning targets. An exit without NMS must also be described by his contract. This level of precision makes it possible to link an error to a design decision instead of generalizing a detail to all generations.

**Versioned Decoding**: An anchor offset representation, edge distances, and distance distribution do not describe the same regression tensor. Box conversion requires sites or anchors, strides, activations, and conventions of the exact variant. An export can move this decoding in the graph and remove a Python step without changing its mathematical necessity. For a given revision, make a known output and then check decoded box and back into the original image. This interface test separates a decoder error from a drive difference, without claiming that a choice is shared by the entire YOLO family.

**Blocking errors**: Assign the original YOLO to all generations.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [YOLOv3, §2.1 : anchors](https://arxiv.org/abs/1804.02767) ; [YOLOX, §2.1: anchor-free, decoupled head and assignment](https://arxiv.org/abs/2107.08430).
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-DETECTEURS-002 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-003

Objective: distinguish between the three assignments. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-003
Question: What is Hungarian matching used for during DETR training, and why is it different from NMS?
Reponse: **Expected answer**: It associates targets and queries to define supervision, with no-object for others; the NMS deletes predictions at inference.

**Further explanation**: The matching of the evaluator is still a separate step. The overall prediction can avoid NMS in this design.

**Conduct of supervision**: Query predictions are compared to targets to choose a minimal cost match. The loss uses this match to learn classes and boxes; the remaining queries learn the absence of an object depending on the formulation. This decision uses annotations during training.

**Contrast with Inference**: A NMS compares available predictions without annotations to reduce duplicates. The evaluator compares predictions and truth in the field in order to count errors and success. The three operations can be matching or boxes, but their inputs, objectives and times of use differ. In a constructed diagnosis, first examine at which stage an object is poorly supervised, deleted, or counted. Bi-party matching is therefore neither a universal postprocessing recipe nor an automatic proof of absence of duplicates for any variant deployed.

**Cost of Matching**: For $y_i$ targets and $\hat y_j$ predictions, we look for an injective assignment minimizing $\sum_i C(y_i,\hat y_{\sigma(i)})$, where the cost combines class compatibility and geometry according to the formulation. Swap the order in which annotations are presented should not change the overall problem. Once the assignment is selected, the losses supervise the pairs selected and the lack of subject matter of the other requests. Discreet pair selection and differentiable loss calculation are two operations. The number of requests also limits the number of possible exits; a scene denser than this ability requires an explicit examination of this constraint.

**Blocking errors**: Describe the three mechanisms as a single interchangeable matching.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [DETR, §3.1, fig. 1 and equations 1 – 2](https://arxiv.org/abs/2005.12872); [Carion et al., DETR, §3.1, matching and supervision; project protocols and calculations](https://arxiv.org/html/2005.12872v3), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-003 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-004

Objective: analyze small objects after resize. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-004
Question: Track A — diagnosis: with checkpoint and images fixed, small-object AP falls when $1920\times1080$ images are resized to a $640\times640$ input with preserved aspect ratio and centered padding. Some objects originally measure $12\times9$ pixels. Which checks distinguish possible causes?
Reponse: **Expected answer**: First check the return of boxes with resize and padding. Then measure their effective size and recall of these same objects before filtering, after score threshold, then after NMS possible. A GT covered before but after denotes a selection loss; if no correct candidate exists upstream, examine scale, features, and drive assignment.

**Further explanation**: The factor is $1/3$, the vertical padding 140 pixels per side, the object becomes $4\times3$. The reference note calculates a case where a perfect $0{,}8$ score box disappears in favor of a less well located $0{,}9$ score box. Keep classes, threshold IoU and original size strata to compare the recall. The small size alone does not prove a loss of information responsible for the failure.

**Controllable Transformation**: in this ideal letterbox, $x'=x/3$ and $y'=y/3+140$; the reverse is $x=3x'$ and $y=3(y'-140)$. A one-pixel error in the grid already corresponds to three pixels in the original, under this convention. For an object that has become $4\times3$, a displacement of one pixel represents a significant fraction of its width or height and can cause the IoU to drop sharply. Check the rounding actually applied by preprocessing rather than assuming this exact pattern for any image. Comparing candidates before filtering then makes it possible to distinguish between sensitive location and deletion of an initially correct prediction.

**Blocking errors**: Forget to reverse padding, count duplicates as reminder, or set thresholds on the test.

**Criteria for correction of the case**: three discriminatory controls (geometry, scale, filtering), explicit assumptions and conditional conclusion. Case built; geometric calculation verified, no field observations.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; project diagnosis and calculations; [FPN, version 2, §3](https://arxiv.org/html/1612.03144v2); [Soft-NMS, §4](https://arxiv.org/html/1704.04503).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-004 provenance::agent pole::A pole::C pole::E cas_pole::A::diagnostic
END

## CV-DETECTEURS-005

Objective: compare detection pipelines. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-005
Question: Which information should accompany a speed comparison between two detectors?
Reponse: **Expected answer**: Hardware, backend/precision, resolution, batch, number of objects, pre/postprocessing, transfers and latency/debit protocol.

**Further explanation**: Measure also quality at fixed thresholds and critical sizes. A single engine time is not a latency camera→decision.

**Compare the same size**: Batch rate measures the amount of images processed per unit of time; latency describes the delay experienced by an observation. An engine can improve the first while adding waiting time before processing an isolated image.

**Proposed Protocol**: announce warm-up, synchronization of measurements, inclusion of copies and decoding, then report a latencies distribution under representative load conditions. Check the quality with the same thresholds, especially for critical sizes and classes. The top-k or score settings can reduce the cost of postprocessing while changing the reminder: they are part of the configuration. A useful comparison to the product involves the same outputs, the same material target and the same decision requirement. An FPS isolated from an article does not demonstrate this comparability or compliance with a budget camera→decision.

**Measurement under load**: note for each image arrival, beginning of service and decision available. Full latency includes queue wait and service; maximum throughput does not explain this wait when arrivals are irregular. Dense scenes can increase decoding and NMS while the backbone time remains close. Compare a distribution of number of candidates, then percentiles of delay and the rate of decisions too late. A high batch can dampen the engine but wait for several images before starting. The protocol must therefore reproduce the pace and processing policy of the product, in addition to the equipment announced.

**Blocking errors**: Compare FPS with different perimeters.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; Comparison protocol proposed by the project; calculation scopes discussed in [Faster R-CNN, §4.1](https://arxiv.org/abs/1506.01497).
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-DETECTEURS-005 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-006

Objective: rebuild site assignment in FCOS. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-006
Question: In FCOS as described in paper §§3.1–3.2, how is a prediction location assigned its training target, including when several annotated boxes contain it?
Reponse: **Expected answer**: Hold the boxes containing the site and compatible with the distance range of the FPN level. If there are several, choose the smaller area; if there are none, the site is negative. The selected box provides the class and regression targets.

**Further explanation**: The beach covers the largest of the four distances to the edges. This is the formulation described in these sections, before the variants with center sampling: anchor-free does not mean "without assignment".

**Role of this decision**: The site does not receive a box simply because it exists in the image; it must be admissible in the geometry and level concerned. The selection resolves supervisory conflicts before the loss. The NMS does not fulfill this role, since it deals with predictions during the final selection.

**Constructed example**: Two overlapping objects may contain the same site, but the size and area rule chooses the target described by this formulation. Changing the assignment then changes the positive examples and the regressions learned. To diagnose missed objects, visualize sites that are actually supervised rather than limited to the overall loss curve.

**Site and Level**: The four target distances verify $l=x-x_0$, $t=y-y_0$, $r=x_1-x$ and $b=y_1-y$. Eligibility by level is for $\max(l,t,r,b)$ in the cited formulation, not just on the box area. Two sites in the same box can therefore have different maximum distances. The "smaller area" rule sets out which boxes are still eligible; it does not allow an out of range box. To audit the assignment, count and view positives by object and level, keeping the exact edge conventions of the implementation. This can reveal a rare oversight without immediately blaming the loss.

**Blocking errors**: Assign the target by NMS or assume that any indoor site is positive on all levels.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [FCOS, version 5, §§3.1 – 3.2](https://arxiv.org/html/1904.01355v5).
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-006 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-007

Objective: Calculate the distance regression targets. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-007
Question: In FCOS, image location $(x,y)=(40,30)$ is assigned to box $(x_0,y_0,x_1,y_1)=(20,10,90,70)$. Using continuous input-pixel coordinates with a top-left origin, what are its four targets $(l,t,r,b)$ to the left, top, right and bottom edges?
Reponse: **Expected answer**: $(l,t,r,b)=(x-x_0,y-y_0,x_1-x,y_1-y)=(20,20,50,40)$ pixels.

**Further explanation**: Decoding $(x-l,y-t,x+r,y+b)$ restores $(20,10,90,70)$. The site is already expressed in the image: do not multiply it again by the stride. Analytical example built and calculated, with no network executed.

**Geometric interpretation**: Each value is a length from the site to a face in the same coordinate frame. The left sum+right gives the width of the box, and high+low its height. The site is not necessarily the center, so distances can be asymmetrical.

**check**: Encode a known box, decode it, then apply the reverse of the resize/padding to find the original annotation. Also test a site near an edge. If a string normalization exists in another implementation, declare it and reverse it exactly once. A network can learn numeric values while producing false boxes if these conventions are mixed at the interface.

**Geometry of the site**: The given distances have sums $l+r=70$ and $t+b=60$, equal to the width and height of the box. The center of it is $(55,40)$, distinct from the $(40,30)$ site. The center-ness target described by FCOS is $\sqrt{\min(l,r)/\max(l,r)\;\min(t,b)/\max(t,b)}$, here $\sqrt{(20/50)(20/40)}=\sqrt{0,2}\simeq0,447$. It expresses a geometric centrality, not a guaranteed IoU of the predicted box. This reading links distance asymmetry, auxiliary target and ranking, while keeping separate the calculated target values and the actually learned outputs.

**Blocking errors**: Confound these distances with center/width/height, express them in feature map cells or add 1 to the continuous coordinate differences.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [FCOS, version 5, §3.1, equation 1 and decoding](https://arxiv.org/html/1904.01355v5); project calculation.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-DETECTEURS-007 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-008

Objective: Explain the modulation of easy negatives by Focal Loss. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-008
Question: In dense detection, how does Focal Loss reduce the dominance of many easy negatives beyond simple class weighting?
Reponse: **Expected answer**: It multiplies the cross entropy by $(1-p_t)^\gamma$, where $p_t$ is the probability of the correct label and $\gamma>0$. An easy negative has $p_t$ close to 1: its contribution decreases sharply. A class weighting alone does not distinguish between easy and difficult examples of this class.

**Further explanation**: The complete form is $-\alpha_t(1-p_t)^\gamma\log p_t$. $\alpha_t$ weights the class; $\gamma=0$ returns the weighted cross entropy. At $\gamma=2$ and $p_t=0{,}9$, the factor is $0{,}01$. The relative focus on difficult cases does not protect against poor annotations.

**Sense of modulation**: For a negative correctly classified as background, the probability of the correct label can be close to one. Its reduced loss prevents many easy cases from overwhelming learning of more difficult examples. Class weighting acts on another dimension of imbalance.

**Limit of diagnosis**: A difficult example can be informative or misannotated. Giving it greater relative importance therefore does not guarantee better supervision. In a built ablation, keep assignment and data, compare contribution distributions and errors by size and class. The formula describes a modification of the lens, not a promise of superior recall on any detector configuration.

**Contribution and gradient**: Comparing two examples of the same class with $p_t=0,99$ and $p_t=0,5$ gives, at $\gamma=2$, respective factors $10^{-4}$ and 0,25. The second is thus of much greater relative importance. The gradient does not correspond to that of a cross entropy multiplied by a fixed constant: the factor itself depends on $p_t$ and its derivative participates in the optimization. The numbers of positives, assignment rules and loss reduction in the lot still count. To interpret a workout, review these conventions before assigning an improvement or instability to the choice of $\gamma$ alone.

**Blocking errors**: Confound $p_t$ with object probability for a negative, or say that the loss eliminates all negatives.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [Focal Loss, version 2, §§2 and 3.1 – 3.2, equation 5](https://arxiv.org/html/1708.02002v2).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-008 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-009

Objective: explain the signal of GIoU for disjointed boxes. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-009
Question: Two axis-aligned rectangular boxes $A$ and $B$ remain strictly disjoint during a small displacement. Why does loss $1-\operatorname{IoU}$ provide no guidance for this displacement, and which term does GIoU add?
Reponse: **Expected answer**: The intersection remains zero, so IoU remains zero and its constant loss at 1. GIoU subtracts from IoU the empty fraction of the smallest rectangle aligned on the axes containing the two boxes: $|C\setminus(A\cup B)|/|C|$. This geometric term can vary even without overlap and provide a signal for regression.

**Further explanation**: For $A=(0,0,2,2)$ and $B=(3,0,5,2)$ in continuous coordinates, the union is 8 and $|C|=10$: GIoU $=-0{,}2$, loss $=1{,}2$. Approaching $B$ in $(2{,}5,0,4{,}5,2)$ gives a loss of $10/9$, IoU always zero. Synthetic calculation; no general guarantee of convergence.

**Why the Additional Term Helps**: Relative positions influence the empty space of the enclosing rectangle even when the intersection does not change. The loss thus has a geometric variation absent from the only overlap in this case. This does not mean that any direction of travel is perfectly informed.

**Proposed Validation**: check the calculation on simple boxes, then distinguish location signal and score ranking. A better loss on pairs of boxes does not imply a better AP if assignment, scores or annotations are a problem. Compare variants with the same data and recipe as much as possible, examining concrete location errors on reserved observations.

**Information still limited**: For two disjoint boxes whose union and enclosing rectangle keep the same area, GIoU can remain constant in certain local directions. The additional term provides a signal in many cases without becoming a complete and perfectly conditioned measure of all movements. Edges where intersection or enclosing rectangle change also introduce regime changes in the derivative. A small perturbation test of each coordinate makes it possible to compare the variations of loss to the expected geometry. This analysis concerns the regression of valid boxes; it does not correct a bad target matching or a wrong class.

**Blocking errors**: Claim that a non-overlay imposes GIoU null, or replace $C$ with the union of the two boxes.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [GIoU, version 2, §3.1 and algorithms 1 – 2](https://arxiv.org/html/1902.09630v2); project calculation.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-DETECTEURS-009 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-010

Objective: explain the contribution of the lateral connections of FPN. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-010
Question: For small-object detection, what do FPN's lateral connections provide beyond simply upsampling the backbone's final feature map?
Reponse: **Expected answer**: It combines the deep semantic representations brought up by the descending path with the finer and better localized features of the backbone. The map deep oversampling alone does not return spatial information from these fine levels.

**Further explanation**: In FPN original, side projection $1\times1$, addition at common resolution, then convolution $3\times3$. It is a pyramid of features from an image, not necessarily several resized images. It does not guarantee the recovery of details already lost by the input resize.

**Difference Between Calculation and Observation**: Interpolating a deep map increases its number of positions but does not recreate the details it no longer represents. The lateral connections, on the contrary, bring features from finer resolutions of the chain. Their fusion aims to combine location and semantic information.

**check**: Compare small objects and large objects with fixed input resolution, changing only access to fine levels. Review recall, location and cost. If the small object already covers almost no pixels in the input, a FPN does not restore the physical information destroyed by the acquisition or resize. The feature pyramid is a system brick, not a substitute for a suitable image contract.

**Recurrence of fusion**: note $M_l=L_l(C_l)+\operatorname{Upsample}(M_{l+1})$ the fused map of the descending path, then $P_l=\operatorname{Conv}_{3\times3}(M_l)$ the smoothed output of the level, where $C_l$ is the feature of the backbone at the $l$ level and $L_l$ the lateral projection of the channels. Spatial sizes and alignment must be compatible for addition. A mismatch error can keep tensor shapes valid while harming the location. The map therefore merges observed lateral information and a reassembled context; it does not create a high-resolution image. Linking the strides to the actual sizes of the objects helps to choose which outputs and which levels to analyze.

**Blocking errors**: Assign new observed details to interpolation alone, or confuse FPN with pyramid of images.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]] ; [FPN, version 2, §3 and figure 3](https://arxiv.org/html/1612.03144v2).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-010 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-011

Objective: Distinguish between class, location, and duplicate errors. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-011
Question: Three independent cases each have one “car” GT instance, without ignore/crowd annotations. With TIDE thresholds $t_b=0{,}1$ and $t_f=0{,}5$, which error describes each FP: (a) “truck,” IoU $0{,}8$; (b) “car,” IoU $0{,}3$; (c) “car,” IoU $0{,}8$, with the GT already matched to a higher-score box?
Reponse: **Expected answer**: (a) Classification: Sufficient localisation, bad class. (b) Location: good class, intermediate overlap. (c) Doubling: class and localisation sufficient, but the GT already has an associated detection.

**Further explanation**: TIDE also distinguishes between class/location combined error, background, and missed GT not already explained by classification/location. Orient checks to labels/classes, geometry or postprocessing as appropriate, without automatically inferring a cause. The number of FP alone does not measure the loss of AP: their score ranking also counts.

**Usefulness of the classification**: indicates where to look for an explanation, without automatically identifying the cause. A bad class can come from an ambiguous taxonomy or a model; a bad location can come from the network or a transformation of coordinates; a duplicate can reflect the postprocessing.

**Proposed Protocol**: Select examples of each family, retain image, annotations and output steps, and then test one hypothesis at a time. The rank of errors by score counts for the AP: correcting several errors of low score does not necessarily have the same effect as a very confident error. An oracle correction is a tool for diagnosing the protocol, not predicting the gain of an actual retraining.

**Counted error and cause**: In the duplicate case, removing the first correct prediction could turn the second into TP without improving the object recall. This shows that the categories also depend on matching's ranking and rules. Conversely, correcting a class can retrieve a GT and simultaneously delete a FP according to the protocol. The oracle gains of several families do not necessarily add up as independent error numbers. For a real intervention, freeze the initial predictions, apply a precise correction and recalculate the complete metric. Diagnosis refers to a family of observed errors; the causal mechanism remains to be established.

**Blocking errors**: Count (c) as a second TP, or assign (a) to a bad location.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [TIDE, version 2, §2.2: types and weighting of errors](https://arxiv.org/html/2008.08115v2); built cases of the project.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-011 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-012

Objective: Diagnose a false positive that may come from a missing annotation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-012
Question: A detector produces a highly confident box with no matched GT, although the image appears to contain an object of the target class. What should be checked before concluding that it confused the background with an object?
Reponse: **Expected answer**: Confronting the image with the annotation policy: real presence and class, box conventions, exclusions and crowd/ignore rules. If the object should have been annotated but was omitted, a non-ignored detection is counted FP despite its visual relevance. The trust of the model is not enough to prove the omission.

**Further explanation**: The project proposes to arbitrate ambiguous cases, version corrections and re-evaluate all models on the same corrected GT, keeping the old balance sheet. TIDE documents missing objects and erroneous crowd flags; this does not make all FP suspicious or all exhaustive annotations.

**Proposed Arbitration**: Have the case checked according to an annotation rule common to all models, with access to the image and the useful context. Keep objects intentionally excluded from accidental omissions. Document version and reasons for corrections.

**Limitation of conclusion**: a model can be very confident and false; the appearance of plausibility is not enough to create a new truth ground. Re-evaluating all systems on the same corrected version avoids favoring the one whose outputs triggered the review. The quality of the benchmark as well as that of the detector is investigated, and its result must be traceable.

**check of annotations**: A sample of disagreements from multiple models and regions drawn independently of their scores. An audit limited to very confident predictions of a system may favor its own biases. For each case, keep image, inclusion rule, old label, arbitration and new version of the game. A crowd or ignore zone does not necessarily follow the same count as an isolated object; apply the rules of the exact evaluator before qualifying a FP. After correction, recalculate all comparisons and keep previous results as historical, without mixing metrics produced on two different ground truths.

**Blocking errors**: Remove annoying FPs from a single model, or automatically turn any confident detection into annotation.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [TIDE, version 2, §3.4 and appendices D – E: ambiguous/missing annotations and ignored detections](https://arxiv.org/html/2008.08115v2); correction protocol proposed by the project.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-012 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-013

Objective: distinguish instances, classes, and labels by instance. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DETECTEURS-013
Question: A task requires localizing three cars and two bicycles, with one label per object. Is this necessarily multilabel classification per box? Distinguish the number of instances, classes present and labels per instance.
Reponse: **Expected answer**: No: there are five instances, two classes present, but one label per instance in this contract. Detection can produce multiple instances of the same class. Multi-tag means that multiple labels are valid for the same instance, depending on the taxonomy.

**Further explanation**: Hierarchical labels such as "vehicle" and "car" can coexist if annotations allow; two exclusive classes offered on the same object remain an ambiguity. YOLov3 uses independent logistic classifiers, but the labels actually rendered also depend on the thresholds and postprocessing. A NMS per class does not guarantee a single label per instance or a single box per class.

**Example of contract**: Five distinct objects in two categories require five location and class decisions, without imposing multiple labels on each. A hierarchical taxonomy can add another rule, but it must then be defined in the annotations and expected outputs.

**Impact on the pipeline**: Close boxes can represent duplicates, competing categories, or separate objects. NMS does not know this semantics directly. Examine labels by instance and annotation coverage before turning a multiclass output into a deletion rule. This distinction links supervision, postprocessing and evaluation, instead of deducting the contract from the number of labels present in the image alone.

**Probability and contract of labels**: A softmax per box requires that the probabilities of the chosen categories share a total mass, which corresponds to an exclusive choice in this set. Independent sigmoids can represent multiple labels simultaneously, but do not automatically make "vehicle", "car" and exclusive categories consistent. The game of annotations and the rule of decision must specify these relationships. At the image scale, aggregating the presence of a category can lose the number of instances; three cars become a single presence indicator. Maintaining instance identities and their boxes avoids confusing scene classification with object detection.

**Blocking errors**: Confuse multiple objects in an image with multiple labels for an object, or limit output to one box per category.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Full reference]]; [YOLov3, version 1, §§2.2 – 2.3](https://arxiv.org/html/1804.02767v1); [Torchvision 0.29, batched_nms: separation of categories](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html); examples of project contracts.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-013 provenance::agent pole::A pole::C pole::E
END
