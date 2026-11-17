# Flashcards — Semantic, instance and panoptic segmentation

reference note: [[90-segmentation/references/93-semantique-instances-panoptique|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SEGMENTATION-001

Objective: Select the segmentation output. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-001
Question: How do semantic, instance and panoptic segmentation differ?
Reponse: **Expected answer**: Semantic: class by pixel; instances: separate countable objects; panoptic segmentation: partition without overlap, with class and instance for things, class for stuff.

**Further explanation**: The mask of a classless object does not automatically fulfill the panoptic contract.

**Example of contract**: Two people who touch each other share the semantic label person but must have different instance IDs if you want to count them. A sky region is stuff in the usual panoptic contract and does not require the same separation into countable objects.

**Consequences for data**: A class mask does not necessarily contain the boundary between two instances of the same class. A model trained on these labels alone therefore does not explicitly receive this information. Instance identifiers can be renumbered without changing the partition; their numeric value does not express a quantity to be interpolated. Also define ignored pixels and the overlap policy before evaluation. A per-class overlap score, an instance score and PQ test different aspects: choose the one that corresponds to the requested deliverable, with additional measures if several properties count.

**Lost information**: From a partition of classified instances, the IDs of each class can be merged to produce a semantic map. The reverse is not determined: several instance partitions can have exactly the same class map. IDs are arbitrary, but the relation "these pixels belong to the same object" is not. In panoptic segmentation, each valid pixel belongs to one segment according to the contract, which requires a rule to resolve possible overlaps of predicted masks. Evaluating only classes after merging can therefore hide a major error in the identity or number of segments.

**Instance IDs are local identities unless stated otherwise**: Two masks with identical geometry and class but permuted instance numbers represent the same per-image instance partition. Across video frames, however, stable identity is an additional tracking requirement. A panoptic image output therefore does not automatically establish temporally consistent IDs. State whether the evaluation concerns per-frame segmentation, video panoptic identity or object trajectories before interpreting label continuity as a property of the segmentation model.

**Blocking errors**: Equating the same class with the same instance identity.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]] ; [Kirillov et al. 2019, §3, format, stuff and things, no overlap](https://arxiv.org/abs/1801.00868) ; [Cheng et al. 2022, Mask2Former, §3.1, masks and labels for every task](https://arxiv.org/abs/2112.01527). Added reasoning: project deduction.
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SEGMENTATION-001 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-002

Objective: Detect a badly defined task. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-002
Question: A semantic model segments a pile of parts well but does not enable counting them. Is this necessarily a network failure?
Reponse: **Expected answer**: No: output may not separate instances. Check task, labels, and metric before network capacity.

**Further explanation**: Depending on the acquisition, add an instance pipeline or markers, then evaluate merges and splits.

**Why the output can be correct**: If the training labels describe only the extent of a class, merging touching parts can be consistent with the supervision. The network has not necessarily been trained to place a boundary between these instances. A defect in the task definition can therefore precede any capacity problem.

**Proposed investigation**: Check the annotations and the expected output, then examine whether the image contains separation cues. Compare connected components, markers and instance methods on the same scenes, counting merges and fragments. Perfectly superimposed parts can also remain ambiguous in a single view. An improvement in mIoU does not automatically fix the count: it can come from better background pixels or from regions that were already easy. Tying the measurement to the number and positions of the objects of interest avoids chasing an indicator that does not represent the need.

**Information test**: Compare two annotations with the same foreground union: a single region and two separate instances. A per-pixel semantic loss receives the same classes in both cases and cannot distinguish these solutions from this supervision alone. A boundary cue, a distance field or an instance head can add a different target, if the data allows it to be annotated. For a classical baseline, markers provide a separation hypothesis to be validated. Before choosing, check whether occlusion makes some objects invisible: an exhaustive count may then require another view or another sensor.

**Diagnosis before training**: Count the connected components of the ground-truth semantic map and compare them with the true number of parts. If touching parts already form one component in the labels, no network trained on them can learn to count; the defect is in the task, not in the capacity. State the connectivity, because two parts that touch only at a corner form one component under 8-connectivity and two under 4-connectivity.

**Constructed share of pixels** (recomputed in the check script of this pass): two $50\times50$ parts touch along 50 px. If the annotation carves a one-pixel separating line, the part class has 4,950 pixels in two components; a prediction that fills the line scores a class IoU of $4{,}950/5{,}000=0.99$ and reports one part. One per cent of the IoU decides a count error of one part in two, which is why mIoU barely sees it. Reinke et al. show the same inversion: a prediction that recognizes all three structures can score a lower pixel Dice than one that recognizes only one [P1, Fig. 3].

**What the U-Net remedy changes**: U-Net labels the separating lines as background and adds the weight $w_0\exp(-(d_1+d_2)^2/2\sigma^2)$, with $w_0=10$, $\sigma\approx5$ px and $d_1$, $d_2$ the distances to the nearest and second-nearest cell [Ronneberger et al., §3, eq. 2]. In a gap where $d_1=d_2=1$ px the weight is $10e^{-0.08}=9.2$; where $d_1+d_2=20$ px it is $10e^{-8}=0.003$. The fix changes the target and the loss, not the capacity, and computing $d_1$ and $d_2$ needs instance annotations.

**Blocking errors**: Inferring the number of objects from a good mIoU.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]] ; [Ronneberger et al. 2015, U-Net, §1 and §3, eq. 2, separation borders between touching cells and their weight](https://arxiv.org/abs/1505.04597) ; [Reinke et al. 2024, P1 and Figs. 1 and 3, metric and problem category](https://www.nature.com/articles/s41592-023-02150-0), read in [arXiv 2302.01790v4](https://arxiv.org/abs/2302.01790), whose figure numbers are used here. Application to counting, the ground-truth component check and the pixel-share example: project reasoning.
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-SEGMENTATION-002 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-003

Objective: Propagate a dense augmentation. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-003
Question: Why must geometric image augmentation be applied differently, but consistently, to the class mask?
Reponse: **Expected answer**: The geometry must remain aligned; the interpolation of the mask must preserve the discrete labels according to the contract.

**Further explanation**: Also check void, crops and padding, and the reconstruction of the full image. Continuous interpolation can create artificial labels.

**Two types of values**: An intensity can represent a continuous measurement that may be interpolated; a class ID represents a category. The average of labels 1 and 3 does not mean class 2. The spatial transformation must, however, place each class at the same location as the corresponding image content.

**Discriminating check**: Transform a simple image and mask whose boundary is known, display their overlay and examine the unique values of the resulting mask. Check the ignored pixels and the padding value. Distinguish this operation on discrete labels from a possible interpolation of logits or probabilities before the decision, which concerns another representation. For tiling, also check how each crop is placed back into the full image. An alignment error can degrade training even if each file looks plausible on its own, so consistency must be tested on the image–annotation pair.

**Transforming the appropriate representation**: For a geometric transformation $W$, image and annotation must use the same spatial correspondence, but the resampling of discrete labels must preserve the categorical contract. Interpolating real-valued logits and then taking an argmax is another operation, and it generally does not commute with taking the argmax and then interpolating labels. At crop borders, explicitly define the class or the ignore value of the padding. For an augmentation that destroys a region of the image, do not silently keep an annotation as if its content remained visible. A synthetic two-class mask with a void zone is a simple test case for these invariants.

**Padding requires an explicit ignored-label policy**: A geometric augmentation can create output pixels with no source annotation. Assigning them an ordinary background class may teach a false label if the intended contract uses ignore regions. Transform image and mask with the same geometry while handling categorical interpolation, padding and ignore values explicitly. A constructed small labeled grid with a translation or rotation is a useful alignment check; smooth-looking overlays can conceal a one-pixel systematic shift.

**Blocking errors**: Transforming the image alone, or interpolating class IDs as intensities.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]] ; [Kirillov et al. 2019, §3, classes, instance IDs and void](https://arxiv.org/abs/1801.00868) ; [torchvision v0.24.0, segmentation/_utils.py L28–L35, bilinear upsampling of logits](https://github.com/pytorch/vision/blob/v0.24.0/torchvision/models/segmentation/_utils.py#L28-L35). Discrete-label contract: project deduction.
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-SEGMENTATION-003 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-004

Objective: Evaluate medical segmentation. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-004
Question: Why is high mean Dice insufficient to establish the usefulness of medical segmentation?
Reponse: **Expected answer**: It measures an overlap according to protocol; external validation, boundaries, rare cases, physical units and intended use provide further evidence.

**Further explanation**: Separate patients/sites and report empty cases or failures; no single score demonstrates a useful clinical decision.

**Why the overlap is partial**: A large region can retain a high Dice despite an error located on an important boundary. A small missed structure may also weigh little in some aggregations. The score must therefore be interpreted with its units, its level of aggregation and its conventions for empty masks.

**Proposed technical evaluation**: Separate patients and sites, measure boundaries in the appropriate physical geometry and retain rare or absent cases. Define the output actually used and an independent reference, then examine the failures individually. An improvement on an internal validation may depend on the acquisition and not transfer to another site. These controls describe the technical validity of the model; they do not constitute medical advice or evidence of clinical utility. Senior reasoning keeps segmentation performance, protocol reproducibility and consequences in the intended use distinct.

**Physical scale of the defect**: The same one-voxel boundary error represents 0.5 mm on one axis and 3 mm on another if the spacings differ. Surface distances must therefore be computed in the relevant physical geometry. An average per volume and an average per patient do not give the same weight to cases; also report cases where the structure is absent. A constructed test with a large region and a small structure shows how an aggregated Dice can favor the first. This analysis concerns the technical metric and its assumptions, without inferring clinical utility from an overlap value.

**A small structure can vanish inside a favorable average**: Constructed example: deleting a tiny lesion has little influence on an overlap score dominated by a large organ, yet it can fail a lesion-detection requirement. Report the relevant structure-level sensitivity and physical boundary errors, with aggregation and empty-mask policy declared. Use patient or acquisition groups for external validation as appropriate. A score establishes performance only for the annotated output and sampled setting; it cannot independently establish usefulness for a different clinical decision.

**Blocking errors**: Inferring clinical utility from a single internal benchmark.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]] ; [Reinke et al. 2024, P2.1–P2.3, P3.2 and discussion](https://www.nature.com/articles/s41592-023-02150-0) ; [Cordts et al. 2016, §3.1, dataset-level IoU and iIoU](https://arxiv.org/abs/1604.01685). External protocol by patient and site: project proposal.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SEGMENTATION-004 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-005

Objective: Calculate PQ through explicit segment matching and SQ/RQ decomposition. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-005
Question: One image is the whole evaluation set of a panoptic benchmark scored with panopticapi, the COCO panoptic evaluator. Category car (thing) has ground-truth segments $g_1$ (90 px), $g_2$ (60 px) and $g_3$ (60 px) and predicted segments $p_1$ (90 px), $p_2$ (90 px), $p_3$ (60 px) and $p_4$ (30 px). The only car overlaps are $|p_1\cap g_1|=80$, $|p_2\cap g_2|=45$ and $|p_3\cap g_3|=40$ px; 30 px of $p_2$ are void in the ground truth, $p_4$ lies entirely on road pixels, and there is no crowd region. Category road (stuff) has one ground-truth and one predicted segment, with IoU 0.9. Match the car segments and give TP, FP and FN, compute SQ, RQ and PQ for car and the overall PQ the evaluator reports, and say what the decomposition tells you about the car errors.
Reponse: **Expected answer**: (1) A predicted and a ground-truth segment of the same category match only if their IoU is strictly above 0.5, with the prediction's void pixels removed from the union; each segment then has at most one match. $p_1/g_1$: $80/(90+90-80)=0.8$, match. $p_2/g_2$: $45/(90-30+60-45)=45/75=0.6$, match. $p_3/g_3$: $40/(60+60-40)=0.5$, no match. Car: TP $=2$, FP $=2$ ($p_3$, $p_4$), FN $=1$ ($g_3$). (2) Car: $\mathrm{SQ}=(0.8+0.6)/2=0.7$, $\mathrm{RQ}=2/(2+\tfrac12\cdot2+\tfrac12\cdot1)=4/7\approx0.571$, $\mathrm{PQ}=1.4/3.5=0.4=\mathrm{SQ}\times\mathrm{RQ}$. Road: SQ $0.9$, RQ $1$, PQ $0.9$. PQ is computed per category, then averaged: overall PQ $=(0.4+0.9)/2=0.65$. (3) SQ is the mean IoU of matched segments only and RQ is the F1 score of segment detection. Car loses more to recognition (RQ $0.571$) than to mask quality (SQ $0.7$): the borderline $p_3$ costs an FP and leaves $g_3$ as an FN, and the 30-pixel $p_4$ costs a full FP, whatever its area.

**Further explanation**: For disjoint predictions $p_a,p_b$ and one ground-truth segment $g$, each union is at least $|g|$ and the two intersections share $g$ without overlapping, so $\mathrm{IoU}(p_a,g)+\mathrm{IoU}(p_b,g)\le1$ (Theorem 1). Above 0.5, at most one match exists per segment in each direction, so greedy and optimal matching agree; panopticapi simply counts every same-category pair above 0.5 as a TP. At exactly 0.5 uniqueness fails: a 2-pixel segment split between two 1-pixel predictions gives two pairs at 0.5.

**Void and crowd**: The evaluator subtracts the prediction's void pixels from the union, so $p_2$ is scored where the ground truth is defined. Keeping them gives $45/105\approx0.43$, turns one TP into an FP and an FN, and drops car PQ to $0.8/3.5\approx0.229$. Crowd segments are neither matched nor counted as FN, and an unmatched prediction is not an FP when its void pixels plus its pixels in a crowd region of its own category exceed half its area. The paper states the void and group rules separately; the code adds the two fractions.

**Averaging**: The evaluator accumulates each category's IoU sum and counts over all images, computes PQ, SQ and RQ per category, skips categories with no TP, FP or FN, and averages each of the three separately, also for things and stuff. The reported SQ $0.8$ and RQ $11/14\approx0.786$ multiply to $0.629$, not to PQ $0.65$: the product holds per category. One road segment weighs as much as all the cars.

**What the decomposition does not say**: SQ and RQ are not independent, since SQ is measured only on matched segments. If $p_3$ reached IoU $0.55$, car SQ would fall to $0.65$ while RQ rose to $6/7$ and PQ to $1.95/3.5\approx0.557$. Removing only $p_4$ would raise car PQ to $1.4/3\approx0.467$, although $p_4$ covers 30 px. Constructed example, recomputed by the check script of this pass.

**Blocking errors**: Matching at IoU $\ge0.5$, which counts $p_3$ and gives car PQ $1.9/3.5\approx0.543$. Keeping void pixels in the union. Reporting the mean IoU of matched pairs, or a mean IoU over all segments, as PQ. Pooling both categories into one count ($2.3/4.5\approx0.511$) or computing overall PQ as mean SQ times mean RQ. Counting a prediction that lies mostly in void or in a same-category crowd region as an FP.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]] ; [Kirillov et al. 2019, §4.1 Theorem 1, §4.2 eqs. 1–2, void and group labels, §6 Table 1 caption](https://arxiv.org/abs/1801.00868) ; [panopticapi evaluation.py at 7bb4655, L121–L163 matching, void and crowd; L49–L73 per-category PQ, SQ, RQ and separate averages](https://github.com/cocodataset/panopticapi/blob/7bb4655548f98f3fedc07bf37e9040a992b054b0/panopticapi/evaluation.py#L49-L163). Segments, pixel counts and variants: constructed project example; tie case: project derivation from Theorem 1.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SEGMENTATION-005 provenance::agent pole::A pole::E
END
