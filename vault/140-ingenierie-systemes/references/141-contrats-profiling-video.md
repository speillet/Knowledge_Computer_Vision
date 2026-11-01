---
id: CV-PIPELINE
type: pipeline
domaine: d14
poles: [C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 6
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# Data contracts, profiling and video pipelines

## Problem, data and assumptions

Keep an end-to-end decision requirement under flow. Inputs: frames with timestamps, metadata and contracts; output: result in the correct coordinate frame before the required time. Latency, flow and freshness are not the same amount.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Decompose acquisition, decoding, preprocessing, transfers, inference, postprocessing and transmission. Profile CPU, GPU and queues with consistent timestamps. Batching and overlapping work can increase throughput without improving individual latency; a queue accumulates delay if the service is insufficient.

## Mathematics, conventions and units

For eight streams at 30 frames/s, the inflow rate is 240 frames/s. This average does not give a P99. A line with $\lambda$ arrival rate higher than the sustainable service $\mu$ grows without limit in a model without abandonment. A budget p99 sum of p99 steps is not a general statistical identity.

## Parameters and properties

Batch, concurrency, cadence, drop policy, buffers and measuring point. Zero-copy describes some avoided transfers, not a universal lack of copy. Hardware decoding and color conversion can still be bottlenecks.

## Cost and implementation

Measure engine time and transfers separately, then complete system; Nsight can help depending on hardware. No benchmark executed. `trtexec`'s commands and defaults evolve: check the version before assuming what's included. Documentation `latest` accessed the 2026-10-20; no universal default command or value is set here.

## Evaluation and controlled variation

Baseline: a stream and then increasing load to fixed model; measure p50/p99, frame age, drops, throughput and memory. The load variation tests queues and concurrency, not just the average kernel.

## Failure modes and diagnosis

Stable FPS but old frames: inspect queues/backpressure and timestamps. Low-busy GPU: Profile CPU/decoding/transfers. Do not conclude that the model is too small or too large without a trace.

## Alternatives and applications

GStreamer/DeepStream/NVDEC depending on the environment; ROS 2 for robot interfaces with QoS/clocks contract. A freshness policy may abandon old frames but must be consistent with tracking and temporality.

## Guided reasoning and proposed checks

These constructed cases develop contracts, queues and information age. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-PIPELINE-001

**Question of work**: A pipeline sustains 240 images/s but makes decisions on old frames. Does it necessarily meet its real-time requirement?

**Reference Response**: No: the throughput does not guarantee the age of the observation or the deadline by decision.

**Two distinct quantities**: A bitrate counts outputs per second; the age of a frame compares its capture time to when its decision is available. A system can process a lot of images while accumulating a significant expectation before the calculation. The real-time term must therefore be linked to a defined useful time.

**Constructed example**: A queue already contains several seconds of images when the engine reaches its rated speed. The exits arrive regularly, but describe a past too old for downstream action. Measure wait and freshness, then choose a charging policy consistent with the need. Abandoning old frames can reduce frame age, but affects tracking and short events; processing all frames can preserve completeness by violating delay. The right compromise cannot be deduced from the FPS alone: it belongs to the product contract and must be tested under load.

### Case linked to CV-PIPELINE-005

**Question of work**: GPU utilization is low while latency is high. Which measurements distinguish CPU decoding, transfers and queues?

**Reference Response**: Trace CPU/GPU time, H2D/D2H, waits and age of frames with representative load.

**Interpretation of traces**: A low-busy GPU can wait for decoded images, copies, or a step-by-step dependency. A usage average masks the computational and waiting alternations; it does not directly say which component should be accelerated.

**Proposed ablation**: Instrument the timeline, then temporarily replace the decoding with prepared inputs or compare an isolated transfer, with an explicit measurement objective. Then reintroduce the complete chain to check the product gain. check also batch and file size, as reducing a cost can move the drop. The quality of the inputs and outputs must remain the same. This approach relates a hypothesis to a discriminating measurement and avoids modifying architecture or precision when the model constitutes only a fraction of the observed delay. The tests described are proposed, without any physical trace executed here.

**Documentary reference for this pass**: [GStreamer, tail](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), limits, blocking, leaky and current levels. The other developments are in the [flashcards](../141-contrats-profiling-video.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-PIPELINE-001

**Situation**: A pipeline sustains 240 images/s but makes decisions on old frames. Does it necessarily meet its real-time requirement?

**Age and waiting**: For a frame, note $t_c$ capture, $t_s$ start processing and $t_o$ output. The capture→exit delay is $(t_s-t_c)+(t_o-t_s)$: speeding up the calculation does not cancel an already accumulated wait. A receiving timestamp replaces only part of this contract if the transport or camera adds a delay. Check that the compared clocks are consistent and that the units are identical. Also measure the share of outputs exceeding the useful time; two systems with the same throughput can serve the product very differently depending on their queue and abandonment policy.

### CV-PIPELINE-002

**Situation**: What happens if sustained input at 240 images/s exceeds processing capacity at 200 images/s and no frames are dropped?

**Growth of queue**: at constant rates and without blocking or abandonment, $Q(t)=Q(0)+(\lambda-\mu)t$ as long as the model remains applicable. An additional capacity buffer $C$ frames therefore absorbs approximately $C/(\lambda-\mu)$ seconds of overload before saturation. With a deficit of 40 frames/s, 400 places only give 10 s of margin. If the queue becomes bounded and blocks the producer, the delay can move upstream; if it drops, it is necessary to define which events and which frames are lost. This arithmetic distinguishes absorption from a temporary peak and insufficient capacity under sustained regime.

### CV-PIPELINE-003

**Situation**: Why is GPU time reported by an inference engine insufficient to validate camera-to-decision latency?

**Critical Path and Asynchronous**: covered steps do not contribute to the delay as a simple sum of their isolated durations. Tracing dependencies, launches, and real endings helps identify the path that determines the availability of the decision. A CPU stopwatch around an asynchronous GPU launch can measure above all the submission; a global synchronization added everywhere can, conversely, destroy the overlap that one wants to study. Choose the instrumentation according to the question, then confirm the end-to-end latency without artificially altering the pipeline. The component measurements and the product measurement complement each other, with an explicitly announced perimeter.

### CV-PIPELINE-004

**Situation**: Track F — design: process eight 1080p streams at 30 frames/s on an embedded module with a defined p99 latency budget. Which process makes the hardware choice verifiable?

**Rafals and equity**: Eight cameras with the same average frame rate can deliver their frames simultaneously or in a staggered manner. The average bitrate remains 240 images/s, but queue peaks and delay per stream may change. Testing these two configurations, and then a momentarily more charged flow, reveals the effects of scheduling. An overall average can hide a rarely served stream or losses concentrated on a single camera. Report latency, seniority, drops and quality per stream, as well as aggregate. The p99 budget must be measured on the full path and a defined load, without mechanically adding the percentiles of the floors.

### CV-PIPELINE-005

**Situation**: GPU utilization is low while latency is high. Which measurements distinguish CPU decoding, transfers and queues?

**Locate a drop by substitution**: Replacing decoding with prepared frames approximately retains the downstream work and tests a hypothesis of data provision. Replacing the network temporarily with a saved result tests another limit, provided you keep the cost of postprocessing and the number of candidates. These tests are not product performance: they isolate contributions. If the drop moves after correction, re-trace the entire track rather than adding the isolated gains. check also includes copy dependencies and involuntary serialization; low GPU usage may come from repeated short waits and not from a lack of network capacity.

**Passages consulted for these developments**: [GStreamer, tail](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), limits and blocking; built flow calculations and protocols; [NVIDIA TensorRT, benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), scope of measurement; page lastest accessed the 2026-10-30, no new API command imposed.

## Sources and flashcards

- [TensorRT, performance benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).
- [GStreamer tail, limits and leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html).
- [Related flashcards](../141-contrats-profiling-video.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
