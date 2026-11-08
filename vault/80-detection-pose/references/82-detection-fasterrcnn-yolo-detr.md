---
id: CV-DETECTEURS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 10
prerequis: ["CV-IOU-AP", "CV-NMS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Detection: Faster R-CNN, YOLO families and DETR

## Problem, data and assumptions

Locate and classify objects according to boxes, scores and labels. Inputs: images and annotations with coordinate frames/sizes; outputs: detection set. The peculiarities are assignment, localization and post-processing, beyond the DL bases already acquired.

### Multiple instances, multiple classes, multiple labels

The number of objects and the number of classes are two distinct dimensions. Detecting three cars and two bicycles requires five instance locations, divided into two categories present in the image. A multiclass detection model can therefore produce several objects of each class; it does not reduce to a label for the entire image or to a box per class.

The **Multi-label** classification concerns several valid labels for the same instance, if the taxonomy so provides. For example, a contract can retain both "vehicle" and "car"; other datasets only annotate the most specific category. Two exclusive labels offered on the same object represent an ambiguity to be solved, not automatically two objects. The cases and their annotation policy are examples of the project.

YOLov3 §2.2 illustrates the distinction: its independent logistic classifiers allow a multi-label formulation, unlike a softmax modeling exclusive classes. This is not enough to determine the final labels: supervision, thresholds, possible choice of the best class and post-processing must follow the contract. Do not assign this choice to all YOLO versions. [YOLov3 v1, §2.2](https://arxiv.org/html/1804.02767v1)

For inference and evaluation, keep the triplet box, score and class for each hypothesis, as well as its original image. Then distinguish: several hypotheses of an instance, several instances of the same class and objects of different classes that overlap. The [NMS multi-class and multi-instance cases](81-nms.md#multiple-detections-classes-and-sizes-of-boxes) show why overlap alone does not slice this identity.

## Prerequisites and competencies

**Required prerequisites**: [CV-IOU-AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md); [CV-NMS](81-nms.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Faster R-CNN offers regions with RPN and then treats them with a head sharing features. YOLO brings together several one-stage designs whose variant must be named. DETR predicts a set and uses bipartite matching during training.

### Dense assignment: example FCOS

In FCOS described in §§3.1 – 3.2 of the article, the prediction sites replace the anchors, but must still receive supervision. A site is eligible for a box if it is inside and its greatest distance to the four edges belongs to the range of level FPN. Among several eligible boxes, the smaller box is retained; without eligible box, the site is negative. Size filtering reduces ambiguity between superimposed objects. This mechanism is neither a NMS nor a common rule for all anchor-free detectors; variants with center sampling modify site selection.

### Features Pyramid: FPN

The descending path propagates deep semantic representations to finer resolutions. Side connections add the features of the backbone, less undersampled and better localized. In the original construction, a $1\times1$ projection aligns the channels, then an addition merges feature maps of the same size; a convolution $3\times3$ follows the merge. The pyramid thus constructed from an image helps to process several scales, including small objects, without being a guarantee of recall. Simply magnifying the last feature map does not return the information of the fine levels. No pyramid guarantees recovery of deleted details in the input image.

## Mathematics, conventions and units

A loss combines class terms and location according to the assignment. For DETR, choose a minimum cost bijection links targets and queries; requests without a target learn no-object. This learning matching is neither the NMS nor the evaluation matching. Standardized boxes must be returned in the correct coordinate frame.

### Targets of boxes in distances

For FCOS, use continuous coordinates in the input image: origin at the top left, $x$ to the right, $y$ to the bottom, units in pixels. At the $(x,y)$ site associated with the $(x_0,y_0,x_1,y_1)$ box, the targets are

$$
(l,t,r,b)=(x-x_0,\;y-y_0,\;x_1-x,\;y_1-y).
$$

Decoding returns $(x-l,y-t,x+r,y+b)$. First, the feature map site must be returned to the coordinate frame image; any normalization by the stride must be reversed. Analytical example of the project: site $(40,30)$ and box $(20,10,90,70)$ give $(20,20,50,40)$ pixels, then exactly the initial box to decoding. Continuous widths do not use a $+1$ term.

### Dense classification : Focal Loss

With $p_t$ the probability assigned to the correct binary label, the weighted form is

$$
\mathrm{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t.
$$

$\alpha_t$ weighs the class; $\gamma\geq0$ modulates the contribution according to the difficulty. For $\gamma=0$, we find the weighted cross entropy. For $\gamma>0$, already well-ranked examples weigh less, which limits the accumulation of many easy negatives in dense detection. At $\gamma=2$, the multiplicative factors are $0{,}01$ for $p_t=0{,}9$ and $0{,}81$ for $p_t=0{,}1$; they modulate the loss, not directly its gradient. The method does not remove negatives and is not designed to neutralize erroneous annotations among difficult cases.

### Location without overlap : GIoU

For two rectangular boxes aligned on the axes, positive areas, $A$ and $B$, $C$ is the smallest rectangle aligned on the axes that contains them. With $|\cdot|$ the area,

$$
\operatorname{GIoU}(A,B)=\operatorname{IoU}(A,B)-\frac{|C\setminus(A\cup B)|}{|C|},\qquad L_{\mathrm{GIoU}}=1-\operatorname{GIoU}(A,B).
$$

If the boxes remain strictly disjoint, $1-\operatorname{IoU}$ remains at 1: this term alone does not indicate how to bring them together. GIoU adds a geometric penalty on the empty part of the enclosing rectangle. Analytical example in continuous coordinates: $A=(0,0,2,2)$ and $B=(3,0,5,2)$ have a union of area 8 and a rectangle $C$ of area 10, hence GIoU $=-0{,}2$ and loss $=1{,}2$. Moving $B$ to $(2{,}5,0,4{,}5,2)$ reduces the loss to $10/9$, while IoU remains zero. This illustrates the additional signal, without guaranteeing a convergence or a superior AP for any recipe.

## Parameters and properties

Resolution, Assign, Weight of Losses, Anchors or Centers, Scores, NMS/top-k. The output rules vary: the DETR design makes it possible to do without NMS. Recipes from a YOLO version do not define the whole family.

## Cost and implementation

Backbone, multiscale, number of regions/requests and postprocessing count; measure the entire chain. No trained model or benchmark executed.

## Evaluation and controlled variation

### Proposed experiment: only vary the resolution

This project protocol is **to be executed**; no image results are available.

1. **Baseline**: choose a checkpoint and a backend accepting both sizes, freeze weights, classes and annotated validation dataset, separated from the training by scene. Record the versions and the annotation policy. Use an entry letterbox $1280\times1280$.
2. **Variation**: upgrade to $640\times640$, without retraining. Keep interpolation, standardization, padding policy, score threshold, possible NMS and identical detection ceilings. Only the resulting dimensions and coordinate transformations change. Archive decoded predictions before filtering, after score threshold, and after NMS or model-specific postprocessing.
3. **Prediction to confront**: Small objects could lose details or be less well located; the cost of the network could drop. These are assumptions, neither a necessary AP drop nor a promise of total latency.
4. **Measurements**: return all boxes to the original image. Compare AP50, AP75, AP per size and recall to score/IoU set, with the same ignore/crowd and cap rules. Define the size strata only once from the original annotations, depending on the protocol chosen; do not move a stratum object because the entry has been reduced. For each filtering step, measure the coverage of the same GT, of good class and at the same threshold IoU, not counting duplicates as additional objects.
5. **Diagnosis and cost**: Examine errors by class, size, density, and step, as well as corresponding images. Time decoding, resize/transfers, network and postprocessing on the same hardware, accuracy and batch, with warm-up and documented repetitions; report full latency and dispersion. A case where the GT is no longer covered after NMS distinguishes a selection problem from a lack of a correct proposal.
6. **Limited conclusion**: formulate a hypothesis from the cases and then test a single correction on validation. Freeze the choices before testing. A win on this dataset and this checkpoint does not rank universally Faster R-CNN, YOLO and DETR.

The AP framework is that of the [reference note IoU/AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md); the score, NMS and evaluation thresholds remain distinct.

## Failure modes and diagnosis

Correct boxes before postprocessing but missing outputs: inspect thresholds/NMS. Loss good but weak recall: check assignment, labels, stride, scale and protocol before changing the backbone.

### Read errors beyond the global AP

TIDE §2.2 separates six families. In simple cases without ignorance/crowd, the thresholds $t_b=0{,}1$ and $t_f=0{,}5$ serve here as an illustration, as in the article; they are not universal. The table avoids boundary equalities and conflicts between multiple GTs, which require the full rules of the tool.

| Family | Reading a simple case | Verification proposed by the project |
| --- | --- | --- |
| Classification | Good location, poor class | Close classes, definition of labels and annotations |
| Location | Good class, intermediate overlap between $t_b$ and $t_f$ | coordinate frame, Targets, Box Accuracy and Scale |
| Classification and localization | Poor class and intermediate overlap | Examine jointly image, label and box |
| Duplicate | Good class and sufficient coverage, GT already associated with better scoring detection | Class, scores and post-processing; do not count two TP |
| Background | Cover less than $t_b$ with all GT | False object or unannotated real object |
| GT missed | GT not detected and not already explained by classification/location errors | Coverage before/after filtering, scale, occlusion and data |

Three independent situations with a single GT "car": IoU $0{,}8$ and class "truck" give a classification error; IoU $0{,}3$ and class "car", a location error; a second "car" box of IoU $0{,}8$ after a higher-scoring box already associated, a duplicate. These classifications use case assumptions, not a causality deduced from an aggregated score.

The raw number of errors does not measure their effect on the AP: their rank by score counts. TIDE estimates effects by oracle corrections applied separately to the same baseline (§§2.2 – 2.3). These gains generally do not add up (Appendix A.1) and do not predict the gain of an actual retraining. The controls proposed above are tracks, not taxonomically proven causes.

### Quality of annotations

A detection not associated with a GT and not ignored is counted FP by the protocol, even if an inspection confirms an omitted real object. A high score is not enough: check the image, the expected class, partial objects, box conventions, exclusions and crowd/ignore processing. TIDE §3.4 and Appendix D show examples of missing or ambiguous annotations; Appendix E also shows that the management of ignored detections influences diagnosis.

Protocol proposed by the project: review a documented sample without privileging a model, apply stable annotation rules, arbitrate ambiguous cases, and then version corrections. Re-evaluate all models compared on the same version, keeping the previous results. Do not selectively remove the FP from a model to improve its score. An object omission is different from an intentional exclusion by the dataset’s policy.

### Box sizes, aspect ratios and accuracy

The same image can simultaneously contain small and large boxes, square or elongated. A fixed input size does not impose fixed box dimensions: coordinates are regressed; feature levels and, depending on the method, anchor shapes organize predictions. YOLov3 describes for example its regression to §2.1 and its multi-scale predictions to §2.3; FCOS uses the distances and ranges already presented here.

The relative size of the boxes also counts as **after** prediction. An inclusion may have a low IoU: see [calcul NMS](81-nms.md#inclusion-and-boxes-of-very-different-sizes). On evaluation, the same absolute error can penalize objects very differently. Analytical case of the project, rectangles aligned on the axes, continuous coordinates in the same coordinate frame in pixels, predicted box of the same width/height as its GT but translated:

| GT size and prediction | Translation $(\Delta x,\Delta y)$ | Intersection / union | IoU |
| --- | --- | --- | --- |
| $4\times4$ | $(2,0)$ pixels | $8/24$ | $1/3$ |
| $40\times40$ | $(2,0)$ pixels | $1520/1680$ | $19/21\approx0{,}905$ |
| $40\times4$ | $(2,0)$ pixels | $152/168$ | $19/21\approx0{,}905$ |
| $40\times4$ | $(0,2)$ pixels | $80/240$ | $1/3$ |

Two error pixels represent a different fraction of the dimension involved. An elongated box here is much more sensitive to displacement on its short axis. This is not a contradiction with the invariance of IoU when we resize the two boxes **together**: here the error remains fixed at two pixels. derivation of the definition of IoU, [GIoU v2, §3, equation 1](https://arxiv.org/html/1902.09630v2), verified calculations without detector executed.

In the proposed protocol, cross-class, size, aspect ratio, and density on the same annotations, and then inspect the score distributions and post-processing losses. Do not conclude that a setting is good for small boxes from the only average AP; do not change coordinate frame or area convention between sizes.

### Analytical case: resize, padding and NMS

For an image of width 1920 and height 1080 resized without deformation in $640\times640$, the factor is $1/3$. The useful image becomes $640\times360$; the centered padding adds 140 pixels at the top and bottom. With continuous coordinates, origin top left: $x'=x/3$, $y'=y/3+140$; the reverse is $x=3x'$, $y=3(y'-140)$.

The box GT $(900,450,912,459)$, size $12\times9$, becomes $G=(300,290,304,293)$, size $4\times3$. The round trip must return exactly the original box. This geometry alone does not prove why a model fails: it is necessary to examine its outputs at the different stages.

Constructed example, a GT, a class, no area ignored, two candidates only, score threshold $0{,}1$, hard NMS for IoU $>0{,}4$, evaluation at IoU $0{,}5$:

| Candidate in the Entrance | Score | IoU with $G$ | Before NMS | After NMS |
| --- | --- | --- | --- | --- |
| $P=(300,290,304,293)$ | $0{,}8$ | 1 | Covers the GT | Deleted |
| $Q=(301{,}5,290,305{,}5,293)$ | $0{,}9$ | $5/11\approx0{,}455$ | Does not cover the GT at the assessment threshold | Preserved |

Both candidates pass the score threshold. Their mutual IoU is worth $5/11>0{,}4$: Q, better scored, removes P. The recall of this GT goes from 1 to 0; here, the loss lies in the postprocessing, because a correct proposal existed at this resolution. This does not show that any drop in AP after resize comes from NMS. If no correct candidate exists before filtering, look instead at the actual size, features, data, and training assignment. The deletion mechanism is documented by Soft-NMS §4; the numbers are a calculation of the project, without network inference.

## Alternatives and applications

Compare architecture + recipe + supervision + full cost; the one/two-stage category alone does not predict quality or latency.

## Guided reasoning and proposed checks

These built cases develop architectural contracts, matching and decomposition of errors. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-DETECTEURS-001

**Question of work**: In Faster R-CNN, does processing regions require running the entire backbone again on each crop?

**Reference Response**: No: the design shares features between RPN and head by region, with extraction of regional representations.

**Reading the calculation share**: the backbone transforms the image into common feature maps. The network of proposals and the head then exploit these representations according to the variant. Regional processing adds a cost related to the number and size of regional representations, without requiring that all extraction be repeated on the raw image for each.

**Example of comparison built**: Two implementations can have the same backbone but different number of proposals, and therefore different lead times. Measure extraction, proposals, regional operations and postprocessing separately to identify the drop. A two-stage category describes the organization of decisions; it does not give a universal latency formula. Keep resolution, batch and thresholds in the protocol, and also compare quality on small objects and dense scenes. The product choice is based on this complete balance sheet, rather than just the number of steps announced.

### Case linked to CV-DETECTEURS-013

**Question of work**: A task requires localizing three cars and two bicycles, with one label per object. Is this necessarily multilabel classification per box? Distinguish the number of instances, classes present and labels per instance.

**Reference Response**: No: there are five instances, two classes present, but one label per instance in this contract. Detection can produce multiple instances of the same class. Multi-tag means that multiple labels are valid for the same instance, depending on the taxonomy.

**Example of contract**: Five distinct objects in two categories require five location and class decisions, without imposing multiple labels on each. A hierarchical taxonomy can add another rule, but it must then be defined in the annotations and expected outputs.

**Impact on the pipeline**: Close boxes can represent duplicates, competing categories, or separate objects. NMS does not know this semantics directly. Examine labels by instance and annotation coverage before turning a multiclass output into a deletion rule. This distinction links supervision, postprocessing and evaluation, instead of deducting the contract from the number of labels present in the image alone.

**Documentary reference for this pass**: [DETR](https://arxiv.org/html/2005.12872v3), §3, ensemble prediction and matching. The other developments are in the [flashcards](../82-detection-fasterrcnn-yolo-detr.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-DETECTEURS-001

**Situation**: In Faster R-CNN, does processing regions require running the entire backbone again on each crop?

**Cost scales**: If the backbone produces a map of $H'\times W'\times C$ features, this extraction is shared. A head then processes $K$ regions reduced to a fixed spatial representation; its work grows with the number of proposals selected, according to the architecture. Increasing K can improve coverage while weighing down head and post-processing, without changing the backbone’s main cost. Measuring the recall of proposals before classification is therefore useful: a region never proposed will not be found by a better head. A poor final score may come from RPN coverage or from the decision on already correct regions.

### CV-DETECTEURS-002

**Situation**: Why must a version be named when describing a YOLO model's anchors, losses or NMS?

**Versioned Decoding**: An anchor offset representation, edge distances, and distance distribution do not describe the same regression tensor. Box conversion requires sites or anchors, strides, activations, and conventions of the exact variant. An export can move this decoding in the graph and remove a Python step without changing its mathematical necessity. For a given revision, make a known output and then check decoded box and back into the original image. This interface test separates a decoder error from a drive difference, without claiming that a choice is shared by the entire YOLO family.

### CV-DETECTEURS-003

**Situation**: What is Hungarian matching used for during DETR training, and why is it different from NMS?

**Cost of Matching**: For $y_i$ targets and $\hat y_j$ predictions, we look for an injective assignment minimizing $\sum_i C(y_i,\hat y_{\sigma(i)})$, where the cost combines class compatibility and geometry according to the formulation. Swap the order in which annotations are presented should not change the overall problem. Once the assignment is selected, the losses supervise the pairs selected and the lack of subject matter of the other requests. Discreet pair selection and differentiable loss calculation are two operations. The number of requests also limits the number of possible exits; a scene denser than this ability requires an explicit examination of this constraint.

### CV-DETECTEURS-004

**Situation**: Track A — diagnosis: with checkpoint and images fixed, small-object AP falls when $1920\times1080$ images are resized to a $640\times640$ input with preserved aspect ratio and centered padding. Some objects originally measure $12\times9$ pixels. Which checks distinguish possible causes?

**Controllable Transformation**: in this ideal letterbox, $x'=x/3$ and $y'=y/3+140$; the reverse is $x=3x'$ and $y=3(y'-140)$. A one-pixel error in the grid already corresponds to three pixels in the original, under this convention. For an object that has become $4\times3$, a displacement of one pixel represents a significant fraction of its width or height and can cause the IoU to drop sharply. Check the rounding actually applied by preprocessing rather than assuming this exact pattern for any image. Comparing candidates before filtering then makes it possible to distinguish between sensitive location and deletion of an initially correct prediction.

### CV-DETECTEURS-005

**Situation**: Which information should accompany a speed comparison between two detectors?

**Measurement under load**: note for each image arrival, beginning of service and decision available. Full latency includes queue wait and service; maximum throughput does not explain this wait when arrivals are irregular. Dense scenes can increase decoding and NMS while the backbone time remains close. Compare a distribution of number of candidates, then percentiles of delay and the rate of decisions too late. A high batch can dampen the engine but wait for several images before starting. The protocol must therefore reproduce the pace and processing policy of the product, in addition to the equipment announced.

### CV-DETECTEURS-006

**Situation**: In FCOS as described in paper §§3.1–3.2, how is a prediction location assigned its training target, including when several annotated boxes contain it?

**Site and Level**: The four target distances verify $l=x-x_0$, $t=y-y_0$, $r=x_1-x$ and $b=y_1-y$. Eligibility by level is for $\max(l,t,r,b)$ in the cited formulation, not just on the box area. Two sites in the same box can therefore have different maximum distances. The "smaller area" rule sets out which boxes are still eligible; it does not allow an out of range box. To audit the assignment, count and view positives by object and level, keeping the exact edge conventions of the implementation. This can reveal a rare oversight without immediately blaming the loss.

### CV-DETECTEURS-007

**Situation**: In FCOS, image location $(x,y)=(40,30)$ is assigned to box $(x_0,y_0,x_1,y_1)=(20,10,90,70)$. Using continuous input-pixel coordinates with a top-left origin, what are its four targets $(l,t,r,b)$ to the left, top, right and bottom edges?

**Geometry of the site**: The given distances have sums $l+r=70$ and $t+b=60$, equal to the width and height of the box. The center of it is $(55,40)$, distinct from the $(40,30)$ site. The center-ness target described by FCOS is $\sqrt{\min(l,r)/\max(l,r)\;\min(t,b)/\max(t,b)}$, here $\sqrt{(20/50)(20/40)}=\sqrt{0,2}\simeq0,447$. It expresses a geometric centrality, not a guaranteed IoU of the predicted box. This reading links distance asymmetry, auxiliary target and ranking, while keeping separate the calculated target values and the actually learned outputs.

### CV-DETECTEURS-008

**Situation**: In dense detection, how does Focal Loss reduce the dominance of many easy negatives beyond simple class weighting?

**Contribution and gradient**: Comparing two examples of the same class with $p_t=0,99$ and $p_t=0,5$ gives, at $\gamma=2$, respective factors $10^{-4}$ and 0,25. The second is thus of much greater relative importance. The gradient does not correspond to that of a cross entropy multiplied by a fixed constant: the factor itself depends on $p_t$ and its derivative participates in the optimization. The numbers of positives, assignment rules and loss reduction in the lot still count. To interpret a workout, review these conventions before assigning an improvement or instability to the choice of $\gamma$ alone.

### CV-DETECTEURS-009

**Situation**: Two axis-aligned rectangular boxes $A$ and $B$ remain strictly disjoint during a small displacement. Why does loss $1-\operatorname{IoU}$ provide no guidance for this displacement, and which term does GIoU add?

**Information still limited**: For two disjoint boxes whose union and enclosing rectangle keep the same area, GIoU can remain constant in certain local directions. The additional term provides a signal in many cases without becoming a complete and perfectly conditioned measure of all movements. Edges where intersection or enclosing rectangle change also introduce regime changes in the derivative. A small perturbation test of each coordinate makes it possible to compare the variations of loss to the expected geometry. This analysis concerns the regression of valid boxes; it does not correct a bad target matching or a wrong class.

### CV-DETECTEURS-010

**Situation**: For small-object detection, what do FPN's lateral connections provide beyond simply upsampling the backbone's final feature map?

**Recurrence of fusion**: note $M_l=L_l(C_l)+\operatorname{Upsample}(M_{l+1})$ the fused map of the descending path, then $P_l=\operatorname{Conv}_{3\times3}(M_l)$ the smoothed output of the level, where $C_l$ is the feature of the backbone at the $l$ level and $L_l$ the lateral projection of the channels. Spatial sizes and alignment must be compatible for addition. A mismatch error can keep tensor shapes valid while harming the location. The map therefore merges observed lateral information and a reassembled context; it does not create a high-resolution image. Linking the strides to the actual sizes of the objects helps to choose which outputs and which levels to analyze.

### CV-DETECTEURS-011

**Situation**: Three independent cases each have one “car” GT instance, without ignore/crowd annotations. With TIDE thresholds $t_b=0{,}1$ and $t_f=0{,}5$, which error describes each FP: (a) “truck,” IoU $0{,}8$; (b) “car,” IoU $0{,}3$; (c) “car,” IoU $0{,}8$, with the GT already matched to a higher-score box?

**Counted error and cause**: In the duplicate case, removing the first correct prediction could turn the second into TP without improving the object recall. This shows that the categories also depend on matching's ranking and rules. Conversely, correcting a class can retrieve a GT and simultaneously delete a FP according to the protocol. The oracle gains of several families do not necessarily add up as independent error numbers. For a real intervention, freeze the initial predictions, apply a precise correction and recalculate the complete metric. Diagnosis refers to a family of observed errors; the causal mechanism remains to be established.

### CV-DETECTEURS-012

**Situation**: A detector produces a highly confident box with no matched GT, although the image appears to contain an object of the target class. What should be checked before concluding that it confused the background with an object?

**check of annotations**: A sample of disagreements from multiple models and regions drawn independently of their scores. An audit limited to very confident predictions of a system may favor its own biases. For each case, keep image, inclusion rule, old label, arbitration and new version of the dataset. A crowd or ignore zone does not necessarily follow the same count as an isolated object; apply the rules of the exact evaluator before qualifying a FP. After correction, recalculate all comparisons and keep previous results as historical, without mixing metrics produced on two different ground truths.

### CV-DETECTEURS-013

**Situation**: A task requires localizing three cars and two bicycles, with one label per object. Is this necessarily multilabel classification per box? Distinguish the number of instances, classes present and labels per instance.

**Probability and contract of labels**: A softmax per box requires that the probabilities of the chosen categories share a total mass, which corresponds to an exclusive choice in this set. Independent sigmoids can represent multiple labels simultaneously, but do not automatically make "vehicle", "car" and exclusive categories consistent. The dataset of annotations and the rule of decision must specify these relationships. At the image scale, aggregating the presence of a category can lose the number of instances; three cars become a single presence indicator. Maintaining instance identities and their boxes avoids confusing scene classification with object detection.

**Passages consulted for these developments** : [Carion et al., DETR](https://arxiv.org/html/2005.12872v3), §3.1, matching and supervision; project protocols and calculations; [Tian et al., FCOS](https://arxiv.org/html/1904.01355v5), §3.3center-ness, equation 3 ; example calculated by project; [Lin et al., Focal Loss](https://arxiv.org/html/1708.02002v2), §3, modulation of the loss; factors and commentary on the gradient deduced; [Rezatofighi et al., GIoU](https://arxiv.org/html/1902.09630v2), Algorithme 1 and §3.1 ; example of built sensitivity; [Lin et al., FPN](https://arxiv.org/html/1612.03144v2), §3, flashcards Merged and Smoothed 3×3 outings, figure 3.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-DETECTEURS-001 — Shared features do not make proposal count free

After a shared backbone, increasing the retained proposal count still increases work in region pooling, per-region heads and downstream filtering. A project timing decomposition should therefore hold proposal limits fixed or report them explicitly when comparing two-stage detectors. Include crowded images where the retained population approaches its cap. A backbone-only benchmark misses the portion of cost that changes with the number of candidate regions.

### CV-DETECTEURS-002 — A checkpoint name needs an export contract

Record repository and revision, checkpoint, preprocessing, tensor layout, box decoding and postprocessing together. Two implementations carrying the same family name can expose decoded boxes or raw regression tensors and may include different filtering stages in exported graphs. A proposed parity check compares intermediate and final outputs on the same images before interpreting deployment differences as an architectural property of YOLO.

### CV-DETECTEURS-003 — Matching cost and optimized loss have different roles

The Hungarian cost chooses which prediction supervises each target; the subsequent loss updates the model using those assignments, including no-object supervision for unmatched queries. Changing cost weights can change assignment discontinuously even if prediction tensors are unchanged. This assignment operates with annotations during training. It is not an inference algorithm for identifying and suppressing duplicate boxes, and does not require ground truth at deployment.

### CV-DETECTEURS-004 — The effective object can be only a few pixels

With scale $640/1920=1/3$, a $12\times9$ px object becomes approximately $4\times3$ px before padding, and the resized image height is 360 px with 140 px padding above and below. A box-coordinate inversion can be tested independently of feature resolution. Even a correct inversion cannot restore details lost by sampling. Compare upstream candidate coverage on the same small-object subset before attributing the entire AP drop to NMS.

### CV-DETECTEURS-005 — Throughput and single-image latency are different measurements

A batch can increase completed images per second while making each arriving image wait for batch formation. GPU kernels can also complete asynchronously with respect to host timing. Use an explicit start/end contract and appropriate synchronization or device events for the quantity measured. Report warmup, queueing and latency quantiles under realistic arrival rates; dividing batch time by batch size is not a measurement of request-to-result latency.

### CV-DETECTEURS-006 — The training location is not an object center requirement

In the cited FCOS rule, an eligible location inside an assigned box predicts distances to its four edges; it need not coincide with the box center. Feature-pyramid range constraints and any center-sampling variant must be stated separately. A site inside two overlapping boxes can receive different targets after the tie-breaking rule. This makes annotation assignment a training policy, distinct from the decoder that reconstructs a box from distances.

### CV-DETECTEURS-007 — A site on the boundary has a zero distance

Constructed boundary case: moving the site to $(20,30)$ on the same box gives distances $(0,20,70,40)$ px. Algebraic decoding still recovers the box, while the geometric centerness target becomes zero. Whether this boundary site is eligible depends on strict versus non-strict containment in the training implementation and any center-sampling rule. Separate that assignment convention from the distance formula, and test sites just inside and outside rather than inferring eligibility from nonnegative decoded lengths.

### CV-DETECTEURS-008 — The logit gradient includes a second term

For binary cross entropy with $p_t=\operatorname{sigmoid}(z_t)$ and no alpha factor, $FL=-(1-p_t)^\gamma\log p_t$ has derivative $\partial FL/\partial z_t=(1-p_t)^\gamma[\gamma p_t\log p_t-(1-p_t)]$. This project derivation follows the product and chain rules. At $\gamma=0$ it becomes $p_t-1$. Detaching the modulator drops the logarithmic term, so it is a different optimization rule even when the forward values are identical. The sign of $z_t$ must encode the correct binary target.

### CV-DETECTEURS-009 — Enclosing geometry distinguishes some disjoint positions

Constructed example: two unit boxes separated horizontally by a one-unit gap have enclosing area three and union area two, giving GIoU $=-1/3$. Increasing that gap to two units makes the enclosing area four and GIoU $=-1/2$. The IoU loss remains one in both cases while the generalized term changes. This does not promise a nonzero gradient in every possible local movement direction.

### CV-DETECTEURS-010 — Upsampling adds locations, not recovered measurements

A coarse feature map interpolated to a finer grid still derives from the same coarse samples. Lateral features supply separately computed finer spatial evidence, which is why the fusion differs from interpolation alone. Test thin or small objects at matched input resolution and training protocol when assessing that contribution. No feature-pyramid mechanism can recover a physical defect that acquisition and input resizing have already removed.

### CV-DETECTEURS-011 — An error category is not a causal diagnosis

The same localization-type false positive can result from poor box regression, incorrect inverse resizing or an annotation convention mismatch. TIDE-style categories organize observed evaluation errors; identifying the cause requires intermediate outputs or controlled ablations. A duplicate category similarly depends on score ordering and prior matching. Keep the evaluator fixed when comparing interventions so changed category counts are not mistaken for proof of one internal failure mechanism.

### CV-DETECTEURS-012 — Annotation fixes must follow the declared policy

A visually plausible detection can lie outside the annotation policy, for example an excluded tiny object or category boundary. Review the policy and an independently sampled set of disagreements before relabeling. If an omission is confirmed, record and version the dataset correction, then reevaluate all compared systems consistently. Editing labels only where one favored model disagrees would bias the comparison even if some individual corrections are valid.

### CV-DETECTEURS-013 — Multiple instances and multiple valid labels are separate axes

A single box can have several valid attributes such as car, red and damaged, while an image can contain many boxes each with one exclusive object class. The output schema should specify which labels describe an instance and which refer to the whole image. This determines loss and decision policy; the mere presence of two object categories does not force independent multilabel classification for every detection.

Consulted foundations: [DETR](https://arxiv.org/html/2005.12872v3): §3.1 bipartite assignment and set loss; [FCOS](https://arxiv.org/html/1904.01355v5): §§3.1–3.3 target distances, level assignment and centerness; [Focal Loss](https://arxiv.org/html/1708.02002v2): §3.2 modulating factor; [GIoU](https://arxiv.org/html/1902.09630v2): §3 enclosing geometry; [FPN](https://arxiv.org/html/1612.03144v2): §3 lateral/top-down fusion; [TIDE](https://arxiv.org/html/2008.08115v2): §2.2 error taxonomy and annotation limitations; [Faster R-CNN](https://arxiv.org/html/1506.01497v3): §3 shared convolutional features.

## Sources and flashcards

- [YOLOv3, §2.1 : anchors](https://arxiv.org/abs/1804.02767) and [YOLOX, §2.1: anchor-free passage](https://arxiv.org/abs/2107.08430), concrete examples of variants.

- [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497).
- [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html).
- [DETR, §§3.1 – 3.2](https://arxiv.org/abs/2005.12872).
- [FCOS, version 5, §§3.1 – 3.3: sites, distances, levels and selection variants](https://arxiv.org/html/1904.01355v5).
- [Focal Loss, version 2, §§2 and 3.1 – 3.2: imbalance, weighting and difficulty](https://arxiv.org/html/1708.02002v2).
- [GIoU, version 2, §3 and algorithms 1 – 2: geometry and loss](https://arxiv.org/html/1902.09630v2).
- [FPN, version 2, §3 and figure 3: descending and lateral paths](https://arxiv.org/html/1612.03144v2).
- [TIDE, version 2, §§2.2 – 2.3, 3.4 and appendices A.1, D – E: errors, oracles and annotations](https://arxiv.org/html/2008.08115v2).
- [Soft-NMS, §4: interaction scores, deletion and location quality](https://arxiv.org/html/1704.04503), accessed on 2026-10-21.
- [YOLov3, version 1, §§2.1 – 2.3: regression, classes and scales](https://arxiv.org/html/1804.02767v1), supplement consulted on 2026-10-21.
- [Related flashcards](../82-detection-fasterrcnn-yolo-detr.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.

Enrichment of the 2026-10-21: flashcards CV-DETECTEURS-006 to 010, learning mechanisms and FPN. Scientific sources consulted; synthetic calculations verified, without training or benchmark.

Enrichment of the diagnosis of 2026-10-21: flashcards CV-DETECTEURS-011 and 012, specified case 004 and proposed resolution variation protocol. Geometric case/NMS calculated; experiment on images not executed.

2026-10-21 add-in: instances/classes/tags distinction, flashcard CV-DETECTEURS-013, aspect ratios and sizes; cross-references to NMS multiclass and nested cases. Synthetic calculations, without measurement on images.
