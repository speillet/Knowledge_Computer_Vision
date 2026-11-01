---
id: CV-SEGMENTATION
type: comparaison
domaine: d09
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# Semantic, instance and panoptic segmentation

## Problem, data and assumptions

Define the output before choosing architecture and loss: class by pixel, accounting object masks or panoptical stuff/things partition without overlapping between segments. Inputs: consistent images and annotations; outputs: logits/masks/classes according to the contract.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

U-Net exploits encoder – decoder and resolution links; DeepLab exploits dilated convolutions and context depending on variant; Mask R-CNN combines detection and mask by instance. nnU-Net automates pipeline choices in medical, beyond a simple network name.

## Mathematics, conventions and units

Class IoU uses TP/(TP+FP+FN); binary Dice is $2TP/(2TP+FP+FN)$ under class/vacuum convention set. PQ combines instance overlap and recognition in a matching protocol. The averages and pixels ignored must be announced; the chosen losses are not these metrics automatically.

## Parameters and properties

Class, background/void, resolution, stride, consistent image – mask increases, imbalance, and thresholds. Small objects and borders require a specific protocol. Instance IDs have no semantic numeric value.

## Cost and implementation

Memory features dense, crops, overlap and complete reconstruction count. No workouts performed; do not confuse patch score and performance of the volume or the entire image.

## Evaluation and controlled variation

Baseline: simple model and protocol per scene/patient; vary size of the crops or resolution and inspect small structures. Evaluate overlap, instances, and boundaries according to usage, not just the average loss.

## Failure modes and diagnosis

Correct pixels but merged objects: The task/annotation can be semantic rather than instance. Tile seams: check overlap, padding and fusion before changing the architecture.

## Alternatives and applications

Conventional methods on stable acquisition; dense segmentation or prompt according to need and supervision. Algorithmic performance does not prove clinical utility.

## Guided reasoning and proposed checks

These constructed cases develop unit output and aggregation of segmentation errors. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SEGMENTATION-001

**Question of work**: How do semantic, instance and panoptic segmentation differ?

**Reference Response**: Semantic: class by pixel; instances: separate countable objects; panoptic segmentation: partition without overlap, with class and instance for things, class for stuff.

**Example of contract**: Two people who touch each other share the semantic label person but must have different instance IDs if you want to count them. A sky region is stuff in the usual panoptic contract and does not require the same separation into countable objects.

**Consequences for data**: A class mask does not necessarily contain the boundary between two instances of the same class. A model trained on these labels alone therefore does not explicitly receive this information. Instance identifiers can be renumbered without changing the partition; their numeric value does not express a quantity to be interpolated. Also set ignored pixels and overlay policy before evaluation. A per-class overlap score, an instance score and PQ test different aspects: choose the one that corresponds to the requested deliverable, with additional measures if several properties count.

### Case linked to CV-SEGMENTATION-004

**Question of work**: Why is high mean Dice insufficient to establish the usefulness of medical segmentation?

**Reference Response**: It measures an overlap according to protocol; external validation, borders, rare cases, physical units and intended use provide further evidence.

**Why the overlap is partial**: A large region can retain a strong Dice despite an error located on an important border. A small missed structure may also weigh little in some aggregations. The score must therefore be interpreted in its units, its level of aggregation and its empty conventions.

**Proposed technical evaluation**: separate patients and sites, measure boundaries in the appropriate physical geometry and retain rare or absent cases. Set the output effectively useful and an independent reference, and then examine the failures individually. An improvement on an internal validation may depend on the acquisition and not transfer to another site. These controls describe the technical validity of the model; they do not constitute medical advice or evidence of clinical utility. The senior reasoning keeps distinct segmentation performance, protocol reproducibility and consequence in the intended use.

**Documentary reference for this pass**: [Kirillov et al., Panoptic Segmentation](https://arxiv.org/html/1801.00868v3), task definition and Panoptic Quality. The other developments are in the [flashcards](../93-semantique-instances-panoptique.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SEGMENTATION-001

**Situation**: How do semantic, instance and panoptic segmentation differ?

**Lost information**: From a partition of classified instances, we can often merge the IDs of the same class to produce a semantic map. The reverse is not determined: multiple instance partitions can have exactly the same map of classes. IDs are arbitrary, but the relationship "these pixels belong to the same object" is not. In panoptic segmentation, each valid pixel belongs to a segment according to the contract, which requires a rule to solve the possible overlaps of predicted masks. Evaluating only classes after merging can therefore hide a major error in the identity or number of segments.

### CV-SEGMENTATION-002

**Situation**: A semantic model segments a pile of parts well but does not enable counting them. Is this necessarily a network failure?

**Test of information**: Compare two annotations with the same foreground union: a single region and two separate instances. A semantic loss per pixel receives the same classes in both cases and cannot distinguish these solutions by this supervision alone. A border index, distance field, or instance header can add a different target, if the data allows it to be annotated. For a classical baseline, markers provide a hypothesis of separation to be validated. Before choosing, check whether the occlusion makes certain objects invisible: a comprehensive count can then require another view or another sensor.

### CV-SEGMENTATION-003

**Situation**: Why must geometric image augmentation be applied differently, but consistently, to the class mask?

**Transforming the adapted representation**: for a geometric transformation $W$, image and annotation must use the same spatial correspondence, but an interpolation of discrete labels must retain the categorical contract. Interpolating real logits and then taking an argmax is another operation and usually does not switch with argmax and then interpolating labels. At crop borders, explicitly define the class or value ignores the padding. For an increase that destroys a region of the image, do not silently keep an annotation as if its content remains visible. A two-class synthetic mask and a void zone provides a simple witness of these invariants.

### CV-SEGMENTATION-004

**Situation**: Why is high mean Dice insufficient to establish the usefulness of medical segmentation?

**Physical scale of the defect**: The same boundary error of a voxel represents 0,5 mm on one axis and 3 mm on another if the spacings differ. Surface distances must therefore be calculated in the relevant physical geometry. An average per volume and an average per patient do not give the same weight to cases; also announce cases where the structure is absent. A test built with a large region and a small structure shows how an aggregated Dice can privilege the first. This analysis focuses on the technical metric and its assumptions, without inferring a clinical utility of a overlap value.

**Passages consulted for these developments**: [Cheng et al., Mask2Former](https://arxiv.org/html/2112.01527v3), Introduction, distinction of tasks and annotations; representational calculations and constructed metrics.

## Sources and flashcards

- [Reinke et al., 2024, metric traps, P1 – P3](https://www.nature.com/articles/s41592-023-02150-0): task, boundaries, small structures and aggregation.

- [U-Net](https://arxiv.org/abs/1505.04597).
- [DeepLabv3+](https://arxiv.org/abs/1802.02611).
- [Mask R-CNN](https://arxiv.org/abs/1703.06870).
- [Panoptic Segmentation, Task/PQ](https://arxiv.org/abs/1801.00868).
- [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
- [Related flashcards](../93-semantique-instances-panoptique.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
