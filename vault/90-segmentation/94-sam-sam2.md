# Flashcards — SAM, SAM 2 and prompted video segmentation

reference note: [[90-segmentation/references/94-sam-sam2|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SAM-001

Objective: Set the output to SAM. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-001
Question: Does SAM automatically assign a semantic class to every pixel?
Reponse: **Expected answer**: No: its central contract is the prompt-guided mask, not a complete semantic taxonomy.

**Further explanation**: A class may come from another component or an annotation; do not assign the text prototype of the paper to any standard checkpoint.

**Reading the condition**: A dot, box or mask guides the region of interest. Segmentation responds to this conditioning; then assigning a class name requests another piece of information or component. A very precise mask can therefore be useful for annotating without directly providing a complete taxonomy.

**Constructed example**: A user designates a piece among several objects. The mask produced delineates a candidate region, but does not demonstrate that it is the right type of piece or that no other object has been forgotten. Evaluate border quality, ambiguities and correction effort with comparable prompts. If a pipeline adds text or a detector, specify this new string instead of assigning its outputs to SAM alone. The contract depends on the checkpoint and interface actually used; a possibility explored in a paper is not automatically an available function of each distributed model.

**Ambiguity of Prompt**: A point on a shirt may refer to the shirt, the person or a visible part of it. Multiple masks can be compatible with the same index; the choice depends on the contract of the task and additional information. The predicted quality score is used to rank proposals according to the model, without assigning a business category to the region. To compare two uses, freeze placement and number of prompts, policy of choice of mask and corrections allowed. Choosing a posteriori the best mask using the ground truth measures an oracle selection, different from the procedure actually available to the product.

**A correct mask can still be the wrong requested object**: A point on a person's sleeve can support a sleeve mask or a whole-person mask depending on the intended granularity. High predicted mask quality does not resolve which output the user needs or attach a semantic category by itself. A proposed evaluation fixes the prompt policy and target granularity, then measures both mask accuracy and selection errors among plausible masks. This separates segmentation quality from task interpretation.

**Blocking errors**: Confound object mask and business class.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]]; [SAM, §3 and proof of concept text-to-mask §7.5](https://arxiv.org/abs/2304.02643); [Kirillov et al., SAM, §2, ambiguity and conditioned task; §3, model; time protocols built without execution SAM 2](https://arxiv.org/html/2304.02643v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::comprehension cv_id::CV-SAM-001 provenance::agent pole::A pole::D
END

## CV-SAM-002

Objective: Find SAM 2 on video. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-002
Question: What does SAM 2 add compared with independently segmenting each frame?
Reponse: **Expected answer**: Memory and propagation of time-guided masks according to the protocol.

**Further explanation**: Specify prompts, corrections, causation, and version; this does not alone provide a self-contained and classified MOT of all objects.

**The role of memory**: Treating each frame in isolation requires reinterpreting the target from only the information of this frame and its prompt. A time memory can carry previous observations and interactions to produce a coherent mask sequence. This information can help, but can also keep confusion.

**Example of diagnosis**: After crossing two similar objects, a mask can remain well-drawn on the wrong object. It is then necessary to examine identity, visibility, prompt and memorized content rather than just the quality of contour. Compare independent propagation and segmentation with the same data and correction budget. The system does not automatically create all classes and births of tracks. Defining what the user initializes and what the model must discover is essential to compare to a stand-alone multiobject tracker or an interactive annotator.

**Temporal state**: A stored spread depends on the history, not just the current image. Two sequences arriving at the same frame with different initializations can therefore produce different outputs. To diagnose identity confusion, keep initialization frame, prompts, corrections, path order, and memory update instants. Comparing a recovery with reset memory and the original continuation is a proposed ablation, with announced information budget. A reset using the right target given by a human should not be counted as stand-alone recovery. The quality of an outline and the permanence of the identity remain two separate properties.

**History is part of the state being evaluated**: If an incorrect mask enters temporal memory, later frames can inherit its mistaken identity or extent. Logging only the final mask loses the evidence needed to distinguish current-image failure from propagated state. Preserve prompt timestamps, object identity assignments, memory reset events and output availability. Compare sequences with controlled initialization and occlusion events; a strong single-frame mask score does not quantify recovery after a long disappearance.

**Blocking errors**: Assimilate spread of masklets and complete object tracking system.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]]; [SAM 2, §4: memory, prompts and masklets](https://arxiv.org/abs/2408.00714); [Kirillov et al., SAM, §2, ambiguity and conditioned task; §3, model; time protocols built without execution SAM 2](https://arxiv.org/html/2304.02643v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SAM-002 provenance::agent pole::A pole::D
END

## CV-SAM-003

Objective: check the future in evaluation. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-003
Question: Why is interactive video annotation using corrections on future frames not directly comparable with a causal tracker?
Reponse: **Expected answer**: It has different information; interaction budget and time access change the task.

**Further explanation**: Report delay, frames viewed and final quality under the same contract before comparing.

**Difference of information**: Correcting a mask after seeing the sequel can resolve an ambiguity that was real at the time of the frame. The final annotation then benefits from observations and unavailable interventions for an immediate decision. Final quality and on-time availability are two distinct properties.

**Proposed Protocol**: Advertise frames viewed, number of clicks or corrections, authorized propagation and time when each output becomes available. Compare either with the same budget or as an explicitly different compromise. Keep losses and ambiguities instead of erasing them with an uncounted reset. An interactive tool can be great at producing ground truth without being a self-deployable tracker with the same performance. This distinction protects the conclusions of the benchmark and links human cost, time and quality to the actual use of the system.

**Two curves to report**: for each frame, measure the quality of the first available output and that obtained after all the corrections allowed. Associate each release with a moment of availability and a number of interactions. The difference between the curves describes what the offline revision brought; it should not be erased in a final average presented as causal. A mask corrected to $t+2$ s may be excellent for annotating a video and too late for decision to $t$. A common protocol must therefore set the access to frames, the accepted deadlines and the rule of counting corrections.

**Causal inputs can still have delayed outputs**: A sliding-window model may use only frames observed up to time $t$ and still return its estimate after a long computation. Causality therefore restricts information access, while timeliness restricts availability; they are independent axes. A proposed comparison records the latest input timestamp, initial output timestamp and any later revision timestamp for each mask. Evaluate mask quality only at the deadline relevant to the application rather than treating a causal architecture as proof of an on-time response.

**Blocking errors**: Present an offline evaluation as real-time performance without latency.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]]; Consequences of the time and interaction protocol proposed by the project; [SAM 2, §§3 – 4: task and model](https://arxiv.org/abs/2408.00714); [Kirillov et al., SAM, §2, ambiguity and conditioned task; §3, model; time protocols built without execution SAM 2](https://arxiv.org/html/2304.02643v1), Consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SAM-003 provenance::agent pole::A pole::D
END
