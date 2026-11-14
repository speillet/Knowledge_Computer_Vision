# Flashcards — SAM, SAM 2 and prompted video segmentation

reference note: [[90-segmentation/references/94-sam-sam2|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SAM-001

Objective: Define the SAM output. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-001
Question: Does SAM automatically assign a semantic class to every pixel?
Reponse: **Expected answer**: No: its central contract is the prompt-guided mask, not a complete semantic taxonomy.

**Further explanation**: A class may come from another component or from an annotation; do not attribute the paper's text prototype to every standard checkpoint.

**Reading the condition**: A point, box or mask designates the region of interest. Segmentation responds to this conditioning; assigning a class name afterwards requires other information or another component. A very precise mask can therefore be useful for annotation without directly providing a complete taxonomy.

**Constructed example**: A user designates one part among several objects. The mask produced delineates a candidate region, but does not show that it is the right type of part or that no other object has been missed. Evaluate boundary quality, ambiguities and correction effort with comparable prompts. If a pipeline adds text or a detector, describe this new chain instead of attributing its outputs to SAM alone. The contract depends on the checkpoint and interface actually used; a possibility explored in a paper is not automatically an available function of every distributed model.

**Prompt ambiguity**: A point on a shirt may refer to the shirt, the person or a visible part of it. Several masks can be compatible with the same prompt; the choice depends on the task contract and on additional information. The predicted quality score ranks the proposals according to the model, without assigning an application category to the region. To compare two uses, fix the placement and number of prompts, the mask-selection policy and the corrections allowed. Choosing the best mask a posteriori with the ground truth measures an oracle selection, different from the procedure actually available to the product.

**Blocking errors**: Confusing an object mask with an application class.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]] ; [Kirillov et al. 2023, §2–§3, promptable task, ambiguity and quality score](https://arxiv.org/abs/2304.02643) ; [Kirillov et al. 2023, §7.5 and §8, text-to-mask as an exploratory proof of concept](https://arxiv.org/abs/2304.02643) ; [segment-anything at dca509f, predictor.py L92–L135, outputs without class](https://github.com/facebookresearch/segment-anything/blob/dca509fe793f601edb92606367a655c15ac00fdf/segment_anything/predictor.py#L92-L135).
Tags: cv::pilote cv::d09 famille::comprehension cv_id::CV-SAM-001 provenance::agent pole::A pole::D
END

## CV-SAM-002

Objective: Situate SAM 2 for video. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-002
Question: What does SAM 2 add compared with independently segmenting each frame?
Reponse: **Expected answer**: Memory, and propagation of the prompted masks over time, according to the protocol.

**Further explanation**: Specify prompts, corrections, causality and version; on its own this does not provide an autonomous, classified multi-object tracking of all objects.

**The role of memory**: Treating each frame in isolation requires reinterpreting the target from the information of that frame and its prompt alone. A temporal memory can carry previous observations and interactions to produce a coherent mask sequence. This information can help, but it can also preserve a confusion.

**Example of diagnosis**: After two similar objects cross, a mask can remain well drawn on the wrong object. Identity, visibility, prompts and memory content must then be examined, not just contour quality. Compare propagation with independent per-frame segmentation under the same data and correction budget. The system does not automatically create classes or track births. Defining what the user initializes and what the model must discover is essential before comparing with an autonomous multi-object tracker or an interactive annotator.

**Temporal state**: A propagation from memory depends on the history, not only on the current image. Two sequences reaching the same frame with different initializations can therefore produce different outputs. To diagnose an identity confusion, record the initialization frame, the prompts, the corrections, the processing order and the times of memory updates. Comparing a recovery with reset memory against the original continuation is a proposed ablation, with a stated information budget. A reset in which a human designates the right target should not be counted as autonomous recovery. The quality of a contour and the persistence of identity remain two separate properties.

**Blocking errors**: Equating masklet propagation with a complete object-tracking system.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]] ; [Ravi et al. 2024, §4, memory attention, memory bank and object pointers; App. C, limitations](https://arxiv.org/abs/2408.00714). Diagnosis cases: project deduction.
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SAM-002 provenance::agent pole::A pole::D
END

## CV-SAM-003

Objective: Control access to future frames in evaluation. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SAM-003
Question: Why is interactive video annotation using corrections on future frames not directly comparable with a causal tracker?
Reponse: **Expected answer**: It has different information; interaction budget and time access change the task.

**Further explanation**: Report latency, frames viewed and final quality under the same contract before comparing.

**Difference of information**: Correcting a mask after seeing what follows can resolve an ambiguity that was real at the time of the frame. The final annotation then benefits from observations and interventions that are unavailable for an immediate decision. Final quality and on-time availability are two distinct properties.

**Proposed protocol**: Report the frames viewed, the number of clicks or corrections, the propagation allowed and the time when each output becomes available. Compare either at the same budget or as an explicitly different trade-off. Keep losses and ambiguities instead of erasing them with an uncounted reset. An interactive tool can be excellent at producing ground truth without being a deployable autonomous tracker with the same performance. This distinction protects the conclusions of the benchmark and ties human cost, time and quality to the actual use of the system.

**Two curves to report**: For each frame, measure the quality of the first available output and the quality obtained after all allowed corrections. Associate each output with the time it becomes available and a number of interactions. The difference between the curves describes what offline revision contributed; it should not be erased in a final average presented as causal. A mask corrected at $t+2$ s may be excellent for annotating a video and too late for a decision at $t$. A common protocol must therefore fix access to frames, the accepted deadlines and the rule for counting corrections.

**Causal inputs can still have delayed outputs**: A sliding-window model may use only frames observed up to time $t$ and still return its estimate after a long computation. Causality therefore restricts information access, while timeliness restricts availability; they are independent axes. A proposed comparison records the latest input timestamp, initial output timestamp and any later revision timestamp for each mask. Evaluate mask quality only at the deadline relevant to the application rather than treating a causal architecture as proof of an on-time response.

**Blocking errors**: Presenting an offline evaluation as real-time performance, without latency.
Source: [[90-segmentation/references/94-sam-sam2|Full reference]] ; [Ravi et al. 2024, §4, prompted frames from the future; §6.1, offline and online evaluation](https://arxiv.org/abs/2408.00714). Time and interaction protocols: project constructions.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SAM-003 provenance::agent pole::A pole::D
END
