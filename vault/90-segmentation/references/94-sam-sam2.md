---
id: CV-SAM
type: methode
domaine: d09
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SEGMENTATION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# SAM, SAM 2 and prompted video segmentation

## Problem, data and assumptions

Produce masks conditioned by dots, boxes or masks depending on the model. SAM processes prompt image segmentation; SAM 2 adds video memory/propagation. Neither semantic classes nor automatic detection of all identities are guaranteed by these outputs.

## Prerequisites and competencies

**Required prerequisites**: [CV-SEGMENTATION](93-semantique-instances-panoptique.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

An image encoder and a prompt encoder condition a mask decoder; SAM can represent ambiguity by several propositions. SAM 2 exploits stored information to propagate masks with prompts and corrections.

## Mathematics, conventions and units

A mask and its predicted score remain conditioned by the prompt and the pattern; they do not constitute a class annotation. The time of a prompt includes encoding, cache and decoding according to use. In video, the protocol must tell if future frames or retroactive corrections are allowed.

## Parameters and properties

Checkpoint, resolution, prompt policy, mask selection and video memory. The text-to-mask prototype of the SAM paper is not the automatic contract of its standard checkpoint/API.

## Cost and implementation

Cache of the depreciable encoder on several prompts; video and memory have a cost. No model executed or mobile performance announced.

## Evaluation and controlled variation

Baseline: same prompts/interaction budget then spread to annotated video. Varier occlusion and movement; measure mask quality, corrections and delay in explicit causal or offline protocol.

## Failure modes and diagnosis

A mask follows the wrong object after crossing: inspect prompts, memory, visibility and identity; do not assimilate good segmentation of a frame to good time tracking.

## Alternatives and applications

Closed supervised segmentation, assisted annotation or promptable model according to available labels and interaction. Classification/association may require other components.

## Guided reasoning and proposed checks

These constructed cases develop prompt, mask ambiguity and temporal memory. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SAM-001

**Question of work**: Does SAM automatically assign a semantic class to every pixel?

**Reference Response**: No: its central contract is the prompt-guided mask, not a complete semantic taxonomy.

**Reading the condition**: A dot, box or mask guides the region of interest. Segmentation responds to this conditioning; then assigning a class name requests another piece of information or component. A very precise mask can therefore be useful for annotating without directly providing a complete taxonomy.

**Constructed example**: A user designates a piece among several objects. The mask produced delineates a candidate region, but does not demonstrate that it is the right type of piece or that no other object has been forgotten. Evaluate border quality, ambiguities and correction effort with comparable prompts. If a pipeline adds text or a detector, specify this new string instead of assigning its outputs to SAM alone. The contract depends on the checkpoint and interface actually used; a possibility explored in a paper is not automatically an available function of each distributed model.

### Case linked to CV-SAM-003

**Question of work**: Why is interactive video annotation using corrections on future frames not directly comparable with a causal tracker?

**Reference Response**: It has different information; interaction budget and time access change the task.

**Difference of information**: Correcting a mask after seeing the sequel can resolve an ambiguity that was real at the time of the frame. The final annotation then benefits from observations and unavailable interventions for an immediate decision. Final quality and on-time availability are two distinct properties.

**Proposed Protocol**: Advertise frames viewed, number of clicks or corrections, authorized propagation and time when each output becomes available. Compare either with the same budget or as an explicitly different compromise. Keep losses and ambiguities instead of erasing them with an uncounted reset. An interactive tool can be great at producing ground truth without being a self-deployable tracker with the same performance. This distinction protects the conclusions of the benchmark and links human cost, time and quality to the actual use of the system.

**Documentary reference for this pass**: [SAM 2](https://arxiv.org/html/2408.00714v2), architecture, masklets, prompts and memory. The other developments are in the [flashcards](../94-sam-sam2.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SAM-001

**Situation**: Does SAM automatically assign a semantic class to every pixel?

**Ambiguity of Prompt**: A point on a shirt may refer to the shirt, the person or a visible part of it. Multiple masks can be compatible with the same index; the choice depends on the contract of the task and additional information. The predicted quality score is used to rank proposals according to the model, without assigning a business category to the region. To compare two uses, freeze placement and number of prompts, policy of choice of mask and corrections allowed. Choosing a posteriori the best mask using the ground truth measures an oracle selection, different from the procedure actually available to the product.

### CV-SAM-002

**Situation**: What does SAM 2 add compared with independently segmenting each frame?

**Temporal state**: A stored spread depends on the history, not just the current image. Two sequences arriving at the same frame with different initializations can therefore produce different outputs. To diagnose identity confusion, keep initialization frame, prompts, corrections, path order, and memory update instants. Comparing a recovery with reset memory and the original continuation is a proposed ablation, with announced information budget. A reset using the right target given by a human should not be counted as stand-alone recovery. The quality of an outline and the permanence of the identity remain two separate properties.

### CV-SAM-003

**Situation**: Why is interactive video annotation using corrections on future frames not directly comparable with a causal tracker?

**Two curves to report**: for each frame, measure the quality of the first available output and that obtained after all the corrections allowed. Associate each release with a moment of availability and a number of interactions. The difference between the curves describes what the offline revision brought; it should not be erased in a final average presented as causal. A mask corrected to $t+2$ s may be excellent for annotating a video and too late for decision to $t$. A common protocol must therefore set the access to frames, the accepted deadlines and the rule of counting corrections.

**Passages consulted for these developments**: [Kirillov et al., SAM](https://arxiv.org/html/2304.02643v1), §2, ambiguity and conditioned task; §3, model; time protocols built without SAM 2 execution.

## Sources and flashcards

- [SAM, §3 and prototype text §7.5](https://arxiv.org/abs/2304.02643).
- [SAM 2, architecture and memory](https://arxiv.org/abs/2408.00714).
- [Related flashcards](../94-sam-sam2.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
