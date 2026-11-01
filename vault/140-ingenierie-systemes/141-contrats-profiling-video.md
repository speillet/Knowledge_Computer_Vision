# Flashcards — Data contracts, profiling and video pipelines

reference note: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-PIPELINE-001

Objective: separate latency flow and freshness. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-001
Question: A pipeline sustains 240 images/s but makes decisions on old frames. Does it necessarily meet its real-time requirement?
Reponse: **Expected answer**: No: the debit does not guarantee the age of the observation or the deadline by decision.

**Further explanation**: Measure capture timestamps to output, latency distribution, queue and drops under representative load.

**Two distinct quantities**: A bitrate counts outputs per second; the age of a frame compares its capture time to when its decision is available. A system can process a lot of images while accumulating a significant expectation before the calculation. The real-time term must therefore be linked to a defined useful time.

**Constructed example**: A queue already contains several seconds of images when the engine reaches its rated speed. The exits arrive regularly, but describe a past too old for downstream action. Measure wait and freshness, then choose a charging policy consistent with the need. Abandoning old frames can reduce seniority, but affects tracking and short events; processing all frames can preserve completeness by violating delay. The right compromise cannot be deduced from the FPS alone: it belongs to the product contract and must be tested under load.

**Age and waiting**: For a frame, note $t_c$ capture, $t_s$ start processing and $t_o$ output. The capture→exit delay is $(t_s-t_c)+(t_o-t_s)$: speeding up the calculation does not cancel an already accumulated wait. A receiving timestamp replaces only part of this contract if the transport or camera adds a delay. Check that the compared clocks are consistent and that the units are identical. Also measure the share of outputs exceeding the useful time; two systems with the same throughput can serve the product very differently depending on their queue and abandonment policy.

**Blocking errors**: Validate the product at the average SPF only.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; Distinction of measures of the project; [TensorRT, Reported Performance Metrics](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) and [GStreamer, tail](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consult the 2026-10-20.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-PIPELINE-001 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-002

Objective: reasoning on a video file. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-002
Question: What happens if sustained input at 240 images/s exceeds processing capacity at 200 images/s and no frames are dropped?
Reponse: **Expected answer**: Delay and queue size increase in this model; a larger buffer only delays saturation.

**Further explanation**: Choose capacity, admission or abandonment according to freshness/completeness and measure the actual behavior.

**Analytical order of magnitude**: In the announced constant model, an additional forty frames accumulate every second. A buffer can absorb a temporary spike, but not a lasting overload without further change. Its ability alters when you run out of memory or when you block, not the sustainable capacity gap.

**Proposed action**: define whether the product favors all observations or their freshness, then compare load reduction, additional capacity, controlled admission and abandonment. Measure the effects on temporal errors and tracking losses. If a producer is blocked, also check what happens in the upstream camera or decoding buffers. A bounded queue alone does not guarantee good end-to-end latency. Stability is judged on the actual flow, its variations and the complete policy, not just on the setting of an isolated buffer.

**Growth of queue**: at constant rates and without blocking or abandonment, $Q(t)=Q(0)+(\lambda-\mu)t$ as long as the model remains applicable. An additional capacity buffer $C$ frames therefore absorbs approximately $C/(\lambda-\mu)$ seconds of overload before saturation. With a deficit of 40 frames/s, 400 places only give 10 s of margin. If the queue becomes bounded and blocks the producer, the delay can move upstream; if it drops, it is necessary to define which events and which frames are lost. This arithmetic distinguishes absorption from a temporary peak and insufficient capacity under sustained regime.

**Blocking errors**: Believing that increasing the tail solves the long-lasting flow deficit.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; Analytical flow report of the project, 240−200 = 40 images/s of deficit; [GStreamer tail, block and leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consulted the 2026-10-20, describes the policies of a limited queue; [NVIDIA TensorRT, benchmarking, scope of measurement; page lastis consulted on 2026-10-30, no new API command imposed](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consulted the 2026-10-30.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-PIPELINE-002 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-003

Objective: Set a complete benchmark. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-003
Question: Why is GPU time reported by an inference engine insufficient to validate camera-to-decision latency?
Reponse: **Expected answer**: Decoding, pre/postprocessing, transfers, queues and transmission may be excluded from this measure.

**Further explanation**: Check version/options of the benchmark and measure the product perimeter; correctly synchronize asynchronous operations.

**Perimeter of measurement**: The engine can measure only part of the calculation, with entries already in memory or transfers excluded depending on the options. The real camera adds acquisition, transport, decoding and waiting. An asynchronous operation can also only be started when the stopwatch stops.

**Proposed Protocol**: associate each result with the capture time of its frame and measure to the useful output, with a clock or consistent synchronization. Also keep step-by-step measurements to locate the cost. Test load, batch size, objects and representative duration. Latency distribution and drops describe the service better than a single average kernel time. Benchmark tools are still useful for comparing a component; their options and versions define what they measure. It is therefore necessary to link their output to the contract of the product rather than implicitly attribute all the steps to it.

**Critical Path and Asynchronous**: covered steps do not contribute to the delay as a simple sum of their isolated durations. Tracing dependencies, launches, and real endings helps identify the path that determines the availability of the decision. A CPU stopwatch around an asynchronous GPU launch can measure above all the submission; a global synchronization added everywhere can, conversely, destroy the overlap that one wants to study. Choose the instrumentation according to the question, then confirm the end-to-end latency without artificially altering the pipeline. The component measurements and the product measurement complement each other, with an explicitly announced perimeter.

**Blocking errors**: Compare asynchronous GPU durations to contract-free user latency.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; [TensorRT, Measure End-to-End Performance, Metrics and Synchronized Measurements](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), accessed on 2026-10-20; [GStreamer, tail, limits and blocking; built flow calculations and protocols](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), accessed on 2026-10-30.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-PIPELINE-003 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-004

Objective: Size eight streams under p99. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-004
Question: Track F — design: process eight 1080p streams at 30 frames/s on an embedded module with a defined p99 latency budget. Which process makes the hardware choice verifiable?
Reponse: **Expected answer**: Set freshness, drops and quality; profile each stage and then the full stream at 240 images/s; test batch/competition/tails and load/thermal scenarios before choosing material or optimization.

**Further explanation**: Keep latency, throughput, memory and quality together. Provide an explicit overload rather than an infinite buffer; no product throughput is guaranteed here.

**Proposed sizing**: Start with a single-stream baseline to check contracts and instrumentation, and then increase the load up to eight simultaneous streams. Observe which resource and file saturate, keeping model, accuracy and thresholds. The aggregated throughput of 240 images/s does not tell if each stream receives a fair service.

**System criteria**: compare distributions by flow and age of observations with the decision budget. A global p99 can hide a disadvantaged stream; the sum of the p99 steps is not usually the p99 of the full path. Include thermal regime, peaks and restart in a documented protocol. These measures make it possible to choose an optimization that treats the actual loophole, rather than blindly oversizing or compressing the only network.

**Rafals and equity**: Eight cameras with the same average frame rate can deliver their frames simultaneously or in a staggered manner. The average bitrate remains 240 images/s, but queue peaks and delay per stream may change. Testing these two configurations, and then a momentarily more charged flow, reveals the effects of scheduling. An overall average can hide a rarely served stream or losses concentrated on a single camera. Report latency, seniority, drops and quality per stream, as well as aggregate. The p99 budget must be measured on the full path and a defined load, without mechanically adding the percentiles of the floors.

**Blocking errors**: Sizing on an FPS isolated from the model or mechanically adding p99s.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; Built sizing case of the project; [TensorRT benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) and [GStreamer tail](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consult the 2026-10-20.
Tags: cv::pilote cv::d14 famille::conception cv_id::CV-PIPELINE-004 provenance::agent pole::C pole::E pole::F cas_pole::F::conception
END

## CV-PIPELINE-005

Objective: Locate a bottleneck by trace. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-005
Question: GPU utilization is low while latency is high. Which measurements distinguish CPU decoding, transfers and queues?
Reponse: **Expected answer**: Trace CPU/GPU time, H2D/D2H, expectations and age of frames with representative load.

**Further explanation**: Change one floor at a time and keep the same quality contract. An average occupation alone does not locate the cause.

**Interpretation of traces**: A low-busy GPU can wait for decoded images, copies, or a step-by-step dependency. A usage average masks the computational and waiting alternations; it does not directly say which component should be accelerated.

**Proposed deletion**: Instrument the timeline, then temporarily replace the decoding with prepared inputs or compare an isolated transfer, with an explicit measurement objective. Then reintroduce the complete chain to check the product gain. check also batch and file size, as reducing a cost can move the drop. The quality of the inputs and outputs must remain the same. This approach relates a hypothesis to a discriminating measurement and avoids modifying architecture or precision when the model constitutes only a fraction of the observed delay. The tests described are proposed, without any physical trace executed here.

**Locate a drop by substitution**: Replacing decoding with prepared frames approximately retains the downstream work and tests a hypothesis of data provision. Replacing the network temporarily with a saved result tests another limit, provided you keep the cost of postprocessing and the number of candidates. These tests are not product performance: they isolate contributions. If the drop moves after correction, re-trace the entire track rather than adding the isolated gains. check also includes copy dependencies and involuntary serialization; low GPU usage may come from repeated short waits and not from a lack of network capacity.

**Blocking errors**: Optimize the network without measuring the other steps.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; Diagnosis proposed by the project; [TensorRT, Reported Performance Metrics and profiling](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), Consulted the 2026-10-20; [GStreamer, tail, limits and blocking; built flow calculations and protocols](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), Consulted the 2026-10-30.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-PIPELINE-005 provenance::agent pole::C pole::E pole::F
END
