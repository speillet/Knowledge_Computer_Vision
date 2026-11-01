---
id: CV-DEPLOIEMENT
type: pipeline
domaine: d14
poles: [A, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-PIPELINE", "CV-QUANT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# Edge deployment, compression and monitoring

## Problem, data and assumptions

Deliver a reproducible and observable vision system, with update mastered. Inputs: Artifacts, Contracts, Versions and Target; Output: Service Tested with Fault/Return Policy. Deploying involves more than copying weights.

## Prerequisites and competencies

**Required prerequisites**: [CV-PIPELINE](141-contrats-profiling-video.md); [CV-QUANT](142-quantification-runtimes.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Version pre-processing, model, post-processing and taxonomy; test on reference inputs and then actual load. Distillation transfers supervision/output structure; pruning removes components according to scheme. Serving, temperature and video file are part of the system.

## Mathematics, conventions and units

In the additive sequential model, Amdahl's simplified law limits an overall gain to $1/((1-f)+f/s)$ if a fraction f of the time is accelerated by a factor s, without new additional costs. Accelerating a stage of 10% of the time by 2 yields only about 1,053× overall in this model. Not to be confused with P99.

## Parameters and properties

Artifacts/runtime, shapes, thresholds, cold start, thermal, consumption, observability and rollback. OTA and version management must maintain output compatibility and return capability, without modifying a personal device here.

## Cost and implementation

Unstructured pluming only accelerates if kernels/hardware exploit its sparsity; distilling may require training but does not automatically change transfers. No equipment/server modified or consumption measured.

## Evaluation and controlled variation

Full fixed baseline; vary load, duration and ambient temperature under protocol. Measure stability, quality, and queues, including boot, disconnect, and restore. A short run does not prove a stable thermal regime.

## Failure modes and diagnosis

A regression after update may come from normalization or classes, not just weight; use reference entries and traces to compare versions. Keep anonymized field errors without private data.

## Alternatives and applications

Central, edge or hybrid serving depending on constraints; score monitoring must be linked to labelled feedback to demonstrate quality drift.

## Guided reasoning and proposed checks

These constructed cases develop sequential bottleneck, thermal regime and reproducibility. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-DEPLOIEMENT-001

**Question of work**: Inference accounts for 10% of mean processing time and becomes twice as fast with no other cost. What is the ideal overall speedup?

**Reference Response**: Approximately 1/0,95 = 1,053×, depending on Amdahl model announced.

**Calculation interpreted**: normalize the initial time to one. The non-accelerated share is 0,9; the inference goes from 0,1 to 0,05. The total time becomes 0,95, a reduction of 5%, and the speed factor is its inverse. The accelerated floor occupied only a small part of the total work.

**Product consequence**: profiling before compressing avoids investing in optimization whose overall gain is limited in this model. New additional conversion costs can even nullify the profit. Conversely, reducing a critical resource in a competing system can modify queues in a way that this additive calculation does not describe. It is therefore a line of reasoning under explicit assumptions, not a prediction of the entire latency distribution. Confirm the gain on the same load and quality contract.

### Case linked to CV-DEPLOIEMENT-004

**Question of work**: A short benchmark passes, but throughput drops after an hour on an edge device. Which traces should be collected?

**Reference Response**: Temperature/frequency, load/memory, transfers and queues, with quality and end-to-end timestamps.

**Why Duration Matters**: Thermal state, memory occupation and queues can change after boot. A short measurement on a cold device does not necessarily describe its sustainable diet. A drop in frequency, a leak, or a build-up of waiting time produce different signatures.

**Proposed investigation**: simultaneously plotting temperature, frequencies, memory, step rates and frame age, over a representative load and duration. Identify which change precedes the degradation, and then modify one hypothesis at a time. For example, compare a limited queue to the initial policy without changing the model, or check the thermal regime according to the device. Then confirm full quality and time. A computational cause does not rule out a data cause; the system must retain inputs and configuration to explain failures, without announcing a single diagnosis from the final FPS alone.

**Documentary reference for this pass**: [Amdahl 1967](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf), p. 1. 483, unaccelerated fraction. The other developments are in the [flashcards](../143-edge-reproductibilite.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-DEPLOIEMENT-001

**Situation**: Inference accounts for 10% of mean processing time and becomes twice as fast with no other cost. What is the ideal overall speedup?

**Boundary and additional cost**: in the same sequential model, even an infinite acceleration of the fraction $f=0,1$ limits the global factor to $1/(1-f)=1/0,9\simeq1,111$. If the optimization adds a standardized cost $c$, the time becomes $(1-f)+f/s+c$; for $s=2$, all $c\ge0,05$ cancels the gain of this example. These calculations guide the choice of work to be optimized. They do not predict a competing queue: near saturation, a small reduction in service can greatly change the wait. Then measuring sustained regime, time and quality confirms the practical scope of this analytical marker.

### CV-DEPLOIEMENT-002

**Situation**: Why does reducing the number of weights through pruning not guarantee faster inference?

**Dimensions and zeros**: Removing entire channels can reduce the dimensions of tensors and the work of dense kernels, if all dependent layers are adapted. Setting isolated weights to zero often retains the same dimensions and the same number of operations performed by a dense kernel. A sparse representation can avoid calculations but add less regular clues and memory access. Compare the actually supported pattern and run trace, not just the number of non-zero parameters. Distillation can help a smaller model regain quality, but it is another learning intervention to be evaluated separately from pruning.

### CV-DEPLOIEMENT-003

**Situation**: Beyond model weights, what must be versioned to reproduce a vision system's output?

**Manifeste reproductible**: Link a version to weight and configuration footprints, input/output contracts, taxonomy, postprocessing parameters, and execution environment. Keeping a sample entry with the relevant intermediate results helps locate the first divergence between versions. Define numerical tolerance and decision tolerance; they are not equivalent near a threshold. The rollback must restore the compatible set, as returning to old weights alone with new class indices can retain a regression. A back-test on a test line verifies this contract without assuming that it will work properly in production.

### CV-DEPLOIEMENT-004

**Situation**: A short benchmark passes, but throughput drops after an hour on an edge device. Which traces should be collected?

**Signatures temporelles**: A frequency drop correlated with a thermal rise supports a hypothesis of power or temperature limitation; continuous memory growth suggests another investigation; stable memory with increasing frame age may signal a queue overload. These correlations guide the trials without establishing a single cause. Replaying the same load over a sufficient period of time and changing one factor at a time makes it possible to compare start and steady speed. Also keep accurate, drops and outputs, because holding the rate by abandoning more images changes the service rendered. Validation is about complete sustainable behavior, not just about the time of the first network pass.

**Passages consulted for these developments**: [NVIDIA TensorRT, benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), measurements and perimeter, consulted on the 2026-10-30; Amdahl, manifesto and signatures built by the project.

## Sources and flashcards

- [Amdahl (1967), p. 483: limit due to non-accelerated fraction](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf). The numerical calculation above is a derivation of the project.

- [TensorRT 8.6.1, §6.10 Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/developer-guide/index.html#structured-sparsity): versioned example of supported patterns and sometimes less fast tactics.
- [Hinton et al., Distilling the Knowledge in a Neural Network, introduction](https://arxiv.org/abs/1503.02531): supervision by output of the teaching model.
- [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html): versioned example of frequency reduction under thermal stress.

- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
- [TensorRT, support and portability](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Related flashcards](../143-edge-reproductibilite.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
