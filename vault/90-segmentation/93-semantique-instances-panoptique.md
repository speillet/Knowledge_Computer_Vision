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

**Consequences for data**: A class mask does not necessarily contain the boundary between two instances of the same class. A model trained on these labels alone therefore does not explicitly receive this information. Instance identifiers can be renumbered without changing the partition; their numeric value does not express a quantity to be interpolated. Also set ignored pixels and overlay policy before evaluation. A per-class overlap score, an instance score and PQ test different aspects: choose the one that corresponds to the requested deliverable, with additional measures if several properties count.

**Lost information**: From a partition of classified instances, we can often merge the IDs of the same class to produce a semantic map. The reverse is not determined: multiple instance partitions can have exactly the same map of classes. IDs are arbitrary, but the relationship "these pixels belong to the same object" is not. In panoptic segmentation, each valid pixel belongs to a segment according to the contract, which requires a rule to solve the possible overlaps of predicted masks. Evaluating only classes after merging can therefore hide a major error in the identity or number of segments.

**Instance IDs are local identities unless stated otherwise**: Two masks with identical geometry and class but permuted instance numbers represent the same per-image instance partition. Across video frames, however, stable identity is an additional tracking requirement. A panoptic image output therefore does not automatically establish temporally consistent IDs. State whether the evaluation concerns per-frame segmentation, video panoptic identity or object trajectories before interpreting label continuity as a property of the segmentation model.

**Blocking errors**: Assimilate identical class and identical instance identity.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]]; [Panoptic Segmentation, §3: format, stuff/things and no overlap](https://arxiv.org/abs/1801.00868); [Cheng et al., Mask2Former, Introduction, distinction of tasks and annotations; representational calculations and constructed metrics](https://arxiv.org/html/2112.01527v3), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SEGMENTATION-001 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-002

Objective: Detecting a bad job definition. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-002
Question: A semantic model segments a pile of parts well but does not enable counting them. Is this necessarily a network failure?
Reponse: **Expected answer**: No: output may not separate instances. Check task, labels, and metric before network capacity.

**Further explanation**: Add a pipeline of instances or markers based on acquisition, and then evaluate mergers/separations.

**Why the output can be correct**: If the learning labels describe the whole subject of a class, merging pieces in contact can respect supervision. The network has not necessarily been trained to place a boundary between these instances. A task interface defect can therefore precede any capacity problem.

**Proposed investigation**: Check annotations and expected output, and then examine if the image contains separation cues. Compare single components, markers, and instance methods on the same scenes, counting merges and fragments. Perfectly superimposed parts can also remain ambiguous in a single view. An improvement to mIoU does not automatically set the count: it can come from better background pixels or already easy regions. Linking the measurement to the number and positions of useful objects avoids chasing an indicator that does not represent the need.

**Test of information**: Compare two annotations with the same foreground union: a single region and two separate instances. A semantic loss per pixel receives the same classes in both cases and cannot distinguish these solutions by this supervision alone. A border index, distance field, or instance header can add a different target, if the data allows it to be annotated. For a classical baseline, markers provide a hypothesis of separation to be validated. Before choosing, check whether the occlusion makes certain objects invisible: a comprehensive count can then require another view or another sensor.

**Semantic supervision cannot choose an instance partition**: If two touching parts share a class, both a merged mask and correctly separated instance masks produce the same semantic class at every foreground pixel. No semantic pixel loss can distinguish those two outputs from class labels alone. Extra instance supervision, shape assumptions or validated postprocessing must supply that information. Improving the semantic backbone may help boundary features, but it does not change the declared output contract by itself.

**Blocking errors**: Deduct the number of objects from a good mIoU.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]]; [Reinke et al., P1 et fig. 1/3: metric and problem category](https://www.nature.com/articles/s41592-023-02150-0); application to counting: reasoning of the project; [Cheng et al., Mask2Former, Introduction, distinction of tasks and annotations; representational calculations and constructed metrics](https://arxiv.org/html/2112.01527v3), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-SEGMENTATION-002 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-003

Objective: Propagating a dense increase. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-003
Question: Why must geometric image augmentation be applied differently, but consistently, to the class mask?
Reponse: **Expected answer**: The geometry must remain aligned; the interpolation of the mask must preserve the discreet labels according to the contract.

**Further explanation**: check also void, crops/padding and reconstruction of the complete image. Continuous interpolation can create artificial labels.

**Two Types of Values**: an intensity can represent a continuous measure that is interpolated; a class ID represents a category. An average between 1 and 3 labels does not automatically mean the class 2. The spatial transformation must, however, place the class in the same place as the corresponding content in the image.

**check**: Transform a simple image and mask whose border is known, display their overlay and examine the unique values of the mask obtained. Check ignored pixels and padding value. Distinguish this operation on discrete labels from a possible interpolation of logits or probabilities before decision, which concerns another representation. For the tile, check also returns the crop in the complete image. An alignment error can degrade the learning even if each file seems visually plausible taken separately, so consistency must be tested on the image – annotation pair.

**Transforming the adapted representation**: for a geometric transformation $W$, image and annotation must use the same spatial correspondence, but an interpolation of discrete labels must retain the categorical contract. Interpolating real logits and then taking an argmax is another operation and usually does not switch with argmax and then interpolating labels. At crop borders, explicitly define the class or value ignores the padding. For an increase that destroys a region of the image, do not silently keep an annotation as if its content remains visible. A two-class synthetic mask and a void zone provides a simple witness of these invariants.

**Padding requires an explicit ignored-label policy**: A geometric augmentation can create output pixels with no source annotation. Assigning them an ordinary background class may teach a false label if the intended contract uses ignore regions. Transform image and mask with the same geometry while handling categorical interpolation, padding and ignore values explicitly. A constructed small labeled grid with a translation or rotation is a useful alignment check; smooth-looking overlays can conceal a one-pixel systematic shift.

**Blocking errors**: Transform the image alone or smooth class IDs as intensities.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]]; Consequence of the discreet label contract of the reference note; [Panoptic Segmentation, §3: classes and IDs](https://arxiv.org/abs/1801.00868); [Cheng et al., Mask2Former, Introduction, distinction of tasks and annotations; representational calculations and constructed metrics](https://arxiv.org/html/2112.01527v3), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-SEGMENTATION-003 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-004

Objective: Evaluate medical segmentation. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SEGMENTATION-004
Question: Why is high mean Dice insufficient to establish the usefulness of medical segmentation?
Reponse: **Expected answer**: It measures an overlap according to protocol; external validation, borders, rare cases, physical units and intended use provide further evidence.

**Further explanation**: Separate patients/sites and report empty cases or failures; no single score demonstrates a useful clinical decision.

**Why the overlap is partial**: A large region can retain a strong Dice despite an error located on an important border. A small missed structure may also weigh little in some aggregations. The score must therefore be interpreted in its units, its level of aggregation and its empty conventions.

**Proposed technical evaluation**: separate patients and sites, measure boundaries in the appropriate physical geometry and retain rare or absent cases. Set the output effectively useful and an independent reference, and then examine the failures individually. An improvement on an internal validation may depend on the acquisition and not transfer to another site. These controls describe the technical validity of the model; they do not constitute medical advice or evidence of clinical utility. The senior reasoning keeps distinct segmentation performance, protocol reproducibility and consequence in the intended use.

**Physical scale of the defect**: The same boundary error of a voxel represents 0,5 mm on one axis and 3 mm on another if the spacings differ. Surface distances must therefore be calculated in the relevant physical geometry. An average per volume and an average per patient do not give the same weight to cases; also announce cases where the structure is absent. A test built with a large region and a small structure shows how an aggregated Dice can privilege the first. This analysis focuses on the technical metric and its assumptions, without inferring a clinical utility of a overlap value.

**A small structure can vanish inside a favorable average**: Constructed example: deleting a tiny lesion has little influence on an overlap score dominated by a large organ, yet it can fail a lesion-detection requirement. Report the relevant structure-level sensitivity and physical boundary errors, with aggregation and empty-mask policy declared. Use patient or acquisition groups for external validation as appropriate. A score establishes performance only for the annotated output and sampled setting; it cannot independently establish usefulness for a different clinical decision.

**Blocking errors**: Deducing clinical utility from the single internal benchmark.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Full reference]]; [Reinke et al., P2.1 – P2.3, P3.2 and discussion](https://www.nature.com/articles/s41592-023-02150-0); external protocol/patients/sites proposed by the project; [Cheng et al., Mask2Former, Introduction, distinction of tasks and annotations; representational calculations and constructed metrics](https://arxiv.org/html/2112.01527v3), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SEGMENTATION-004 provenance::agent pole::A pole::E
END
