---
id: CV-VIDEO
type: comparaison
domaine: d10
poles: [D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 8
prerequis: ["CV-FLOT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Point tracking, actions and video understanding

## Problem, data and assumptions

Distinguish between point trajectories, clip classification and temporal location of actions. Inputs: time-stamped frames and possibly points/prompts; outputs: trajectories/visibility, clip labels or intervals. Their causal protocol and supervision differ.

## Prerequisites and competencies

**Required prerequisites**: [CV-FLOT](101-flot-optique.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

CoTracker uses spatial/temporal interactions to predict points and visibility. TimeSformer and ViViT handle video patches with attention according to their architecture. VideoMAE pretrains by reconstruction of hidden tubes; a final task must then be defined.

## Mathematics, conventions and units

Sampling a frame every $\Delta t$ seconds limits directly observed events. A shorter event can be missed depending on its phase. A window of L frames at frequency f covers about $(L-1)/f$ seconds between first and last timestamp; the duration convention must be announced.

## Parameters and properties

Version CoTracker/CoTracker3, online/offline mode, stride, window, visibility and access to the future. An online window mode can introduce a delay. VideoMAE’s high masking ratios are a choice of method, not a universal rule.

## Cost and implementation

Frames, time-space tokens, window and memory dominate. No models executed; do not compare clip time and streaming decision latency.

## Evaluation and controlled variation

Baseline: Aggregate image model and then time model, same frames and data. Reverse order or rarefied sampling to test time usage; measure short events, visibility, and action boundaries.

## Failure modes and diagnosis

Good clip score but poorly localized action: check that the output is a global label and not an interval. Correct points but wrong object: A point path is not an object class.

## Alternatives and applications

Pipeline detection/tracking/rules for defined events; video model or VLM depending on context and annotations. check leak between clips of the same sequence.

## Guided reasoning and proposed checks

These constructed cases develop point trajectories, visibility and time horizon. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-VIDEO-001

**Question of work**: How do CoTracker, video classification and temporal action localization differ?

**Reference Response**: CoTracker tracks points with visibility; classification labels a clip; localization also estimates time intervals.

**Contracts to distinguish**: A point path answers “where is this observation over time?” A music video label answers “what action characterizes this excerpt?”. A time interval adds a start and end estimate. One output may be correct for one of these contracts and insufficient for another.

**Constructed example**: recognizing that a person sits in a clip does not necessarily provide the instant of contact with the chair. Following a garment point also does not automatically provide the action class. Define the useful output before choosing architecture and metric: point error, visibility, classification, or time boundaries. Specify the frames accessible to the model and the decision time. A performance obtained with the full clip does not validate an alarm to be triggered before the end of the event.

### Case linked to CV-VIDEO-004

**Question of work**: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?

**Reference Response**: Compare to an image/context baseline, check labels and actions that actually require order.

**Alternative Hypothesis**: The presence of a tool, a decor or a characteristic posture can be enough to predict the label of the clip. Frame swapping preserves many of these clues. A high accuracy does not, therefore, alone allow to attribute the decision to the temporal order.

**Proposed ablation**: Compare the model to an aggregation of image predictions, and then select cases where the same visual states in a different order correspond to different events. check sampling, labels, background and leakage between neighboring clips. If the performance remains the same on tasks that are really sensitive to order, look at the information used. A fall after permutation sustains a temporal dependence, but does not prove any form of causal understanding. Reasoning must remain tied to the tasks and controls performed, not just in the name of the architecture.

**Documentary reference for this pass**: [CoTracker3](https://arxiv.org/abs/2410.11831), summary, point tracking task. The other developments are in the [flashcards](../102-points-actions-video.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-VIDEO-001

**Situation**: How do CoTracker, video classification and temporal action localization differ?

**Axis of annotations**: A point path can be represented by $(x_t,y_t,v_t)$, where $v_t$ describes a visibility according to the protocol. A clip label is a category associated with a window; a time location provides at least one category and an interval $[t_d,t_f]$. Cutting a long video into tagged clips can give rough time cues, but does not automatically create precise boundaries. To compare systems, keep timestamps and match rules with actual events. A point followed on a person is neither a complete identity of the person nor an annotation of action without an additional definition.

### CV-VIDEO-002

**Situation**: A video is summarized with one frame per second. Why can detection of a 100 ms event not be guaranteed?

**Sampling phase**: In a constructed model where an event of duration $d<\Delta$ begins with a uniform phase with respect to a grid of steps $\Delta$, and where an instantaneous capture is sufficient, the probability that at least one sample falls into the event is $d/\Delta$. For 100 ms and a step of 1 s, it is 0,1 under these assumptions. This is not a predicted performance of a real model: exposure, visibility, and persistent clues change the problem. The calculation shows, however, why varying the phase is essential and why a demonstration where the event falls exactly on a frame does not validate a guaranteed recall.

### CV-VIDEO-003

**Situation**: A point tracker uses a window containing future frames. Can its output be compared directly with a zero-delay causal model?

**Minimum time for context**: if an estimate for $t$ uses a frame at $t+h$, its availability cannot precede $t+h$, even before transfer and calculation. A latency measurement limited to the network pass would therefore omit at least this context delay. With sliding windows, specify which exits are temporary and which are revised afterwards. Evaluating the first decision and the final trajectory separately makes the comparison readable. A method can remain useful in line with an accepted deadline; the word causal, on the other hand, requires that each decision at the time in question uses only the observations already available according to the announced contract.

### CV-VIDEO-004

**Situation**: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?

**Permutation and reverse order**: An average $z=L^{-1}\sum_t f(I_t)$ aggregation is mathematically invariant to permutation; a good score obtained in this way can come from visual states or context, without encoding their order. Building pairs like take/pose an object, with close states but a different order, tests another property. check also that permutation does not create an unusual artifact that would cause the model to fall for the wrong reason. Comparing inversion, permutation and cadence by changing only one factor helps to support the use of time without assimilating any temporal sensitivity to a complete understanding of the scene.

**Passages consulted for these developments**: algebraic complements and protocols built by the project; the previous references of the subject remain below, without new full validation of their claims.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-VIDEO-001 — Point identity is additional information across time

A collection of independent per-frame point detections does not establish which observation belongs to the same physical point. Conversely, a continuous point track does not by itself assign an action label or its start/end times. Build evaluation around the output actually needed: visibility-aware trajectories, clip class or temporal intervals. Combining these modules is a system decision and requires checking their spatial and temporal interfaces.

### CV-VIDEO-002 — Sampling phase creates a measurable miss probability

Under an explicitly constructed model of instantaneous regular sampling every second and uniformly random event start phase, a 0.1 s event is sampled with probability 0.1 and missed with probability 0.9. This does not predict a real dataset without its event distribution and exposure model. To guarantee observing every event of a minimum duration, sampling and acquisition need a spacing condition appropriate to that duration, not a favorable average-case example.

### CV-VIDEO-003 — Future context imposes a latency floor

At 30 frames/s, using five future frames imposes at least about 167 ms of waiting before computation and transfer. The model may be appropriate for retrospective analysis but incompatible with a tighter online decision budget. A proposed comparison reports quality versus total output delay under a common information window, including whether later frames revise earlier outputs. Timing only the network call omits the cost of waiting for its input.

### CV-VIDEO-004 — Order sensitivity should match the task labels

Opening and closing a door can share many static frames while differing in order; recognizing a sport from a field may require much less temporal evidence. A proposed controlled set includes reverse-order pairs with changed labels and static-context baselines. Shuffle invariance alone is not proof of failure on an order-insensitive task, but a high shuffled score cannot establish that the model learned the dynamics needed for an order-sensitive decision.

Consulted foundations: [CoTracker3](https://arxiv.org/html/2410.11831v1): point-track/visibility outputs, online and offline protocols.

## Sources and flashcards

- [ViViT, summary](https://arxiv.org/abs/2103.15691): spatiotemporal tokens and video classification.
- [CoTracker3, summary and introduction](https://arxiv.org/abs/2410.11831): offline (single window) and online (slippery windows) variants.

- [CoTracker, §3](https://arxiv.org/abs/2307.07635).
- [TimeSformer](https://arxiv.org/abs/2102.05095).
- [VideoMAE](https://arxiv.org/abs/2203.12602).
- [Related flashcards](../102-points-actions-video.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
