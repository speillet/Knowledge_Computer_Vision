# Flashcards — Data contracts, profiling and video pipelines

reference note: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-PIPELINE-001

Objective: Separate latency, throughput and freshness. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-001
Question: A pipeline sustains 240 images/s but makes decisions on old frames. Does it necessarily meet its real-time requirement?
Reponse: **Expected answer**: No: throughput guarantees neither the age of the observation nor the per-decision deadline.

**Further explanation**: Measure the delay from capture timestamp to output, its distribution, queue depths and drops under representative load.

**Two distinct quantities**: Throughput counts outputs per second; the age of a frame compares its capture time with the moment its decision is available. A system can process many images while accumulating a long wait before processing. The term real time must therefore be tied to a defined deadline.

**Constructed example**: A queue already holds several seconds of images when the engine reaches its rated speed. The outputs arrive regularly but describe a past too old for downstream action. Measure waiting and freshness, then choose a load-shedding policy consistent with the need. Dropping old frames can reduce frame age but affects tracking and short events; processing every frame preserves completeness at the cost of the deadline. The right compromise cannot be deduced from the FPS alone: it belongs to the product contract and must be tested under load.

**Age and waiting**: For a frame, write $t_c$ for capture, $t_s$ for the start of processing and $t_o$ for output. The capture-to-output delay is $(t_s-t_c)+(t_o-t_s)$: speeding up processing does not cancel a wait already accumulated. A reception timestamp covers only part of this delay when the camera or the transport adds its own. Check that the compared clocks are consistent and that the units are identical. Also measure the share of outputs that exceed the deadline; two systems with the same throughput can serve the product very differently depending on their queue and drop policy.

**Blocking errors**: Validating the product on average FPS alone.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; measurement distinction constructed by the project; [Yates and Kaul, arXiv 1608.08622, §I (definition of age)](https://arxiv.org/abs/1608.08622); [TensorRT 11.4.1, Reported Performance Metrics](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html) and [GStreamer, queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consulted 2026-11-14.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-PIPELINE-001 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-002

Objective: Reason about a video queue. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-002
Question: What happens if sustained input at 240 images/s exceeds processing capacity at 200 images/s and no frames are dropped?
Reponse: **Expected answer**: Delay and queue size increase in this model; a larger buffer only delays saturation.

**Further explanation**: Choose capacity, admission control or dropping according to the freshness or completeness requirement, and measure the actual behavior.

**Analytical order of magnitude**: In the stated constant-rate model, forty additional frames accumulate every second. A buffer can absorb a temporary spike, but not a lasting overload without another change. Its size only changes when memory runs out or when the producer blocks; it does not change the sustained capacity gap.

**Proposed action**: Define whether the product favors every observation or their freshness, then compare load reduction, additional capacity, admission control and dropping. Measure the effects on timing errors and tracking losses. If a producer is blocked, also check what happens in the upstream camera or decoder buffers. A bounded queue alone does not guarantee good end-to-end latency. Stability is judged on the actual arrival process, its variations and the complete policy, not just on the setting of an isolated buffer.

**Queue growth**: At constant rates and without blocking or dropping, $Q(t)=Q(0)+(\lambda-\mu)t$ as long as the model applies. An additional buffer of capacity $C$ frames therefore absorbs about $C/(\lambda-\mu)$ seconds of overload before saturation. With a deficit of 40 frames/s, 400 slots give only 10 s of margin. If the queue is bounded and blocks the producer, the delay can move upstream; if it drops, the events and frames that are lost must be defined. This arithmetic separates absorbing a temporary peak from a capacity shortfall under sustained load.

**Buffer capacity buys time, not steady-state capacity**: With arrivals at 240 frames/s and service at 200, backlog grows by 40 frames/s under the front's no-drop model. An extra 400-frame buffer absorbs about ten seconds before filling. By then it represents about two seconds of service work at 200 frames/s. Backpressure or dropping changes the model and must be measured explicitly; allocating memory alone cannot make the sustained arrival rate feasible.

**Blocking errors**: Believing that enlarging the queue solves a sustained throughput deficit.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; analytical flow calculation by the project, 240 − 200 = 40 images/s of deficit; [GStreamer queue, blocking and leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), describing the policies of a bounded queue, consulted 2026-11-14; [NVIDIA TensorRT 11.4.1, Performance Benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html), scope of measurement, consulted 2026-11-14. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-PIPELINE-002 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-003

Objective: Define a complete benchmark. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-003
Question: Why is GPU time reported by an inference engine insufficient to validate camera-to-decision latency?
Reponse: **Expected answer**: Decoding, pre/postprocessing, transfers, queues and transmission may be excluded from this measure.

**Further explanation**: Check the version and options of the benchmark, measure the product's scope, and synchronize asynchronous operations correctly.

**Measurement scope**: The engine may measure only part of the computation, with inputs already in memory or transfers excluded depending on the options. The real camera adds acquisition, transport, decoding and waiting. An asynchronous operation may also have only been launched, not completed, when the stopwatch stops.

**Proposed protocol**: Associate each result with the capture time of its frame and measure up to the usable output, with one clock or consistent synchronization. Also keep per-stage measurements to locate the cost. Test with representative load, batch size, object counts and duration. The latency distribution and drops describe the service better than a single average kernel time. Benchmark tools remain useful for comparing a component; their options and versions define what they measure. Their output must therefore be related to the product contract rather than implicitly credited with every stage.

**Critical path and asynchrony**: Overlapped stages do not contribute to the delay as a simple sum of their isolated durations. Tracing dependencies, launches and actual completions identifies the path that determines when the decision is available. A CPU stopwatch around an asynchronous GPU launch may mostly measure the submission; conversely, a global synchronization added everywhere can destroy the overlap one wants to study. Choose the instrumentation according to the question, then confirm the end-to-end latency without artificially altering the pipeline. Component measurements and the product measurement complement each other, each with an explicitly stated scope.

**Overlapped stages need a dependency trace**: Decode, transfer and inference can overlap across frames, so adding their separately timed durations can overstate throughput cost while still omitting queue age. Trace each frame's dependencies and the moment its result becomes usable. A host launch timestamp is not device completion. Distinguish an isolated synchronous latency benchmark from a pipelined load test, and report both when the system requires sustained streams and per-frame deadlines.

**Version-specific scope in TensorRT 11.4.1**: trtexec defines Host Latency as the sum of H2D latency, GPU compute time and D2H latency, and calls it the end-to-end latency of a single inference; since TensorRT 11.0 the H2D and D2H transfers are excluded by default, pre- and postprocessing are always outside it, and trtexec keeps one inference enqueued ahead, so its latency is measured under back-to-back load rather than camera-rate arrivals with queueing. "End-to-end" there means the engine call, not camera to decision.

**Blocking errors**: Comparing asynchronous GPU durations with a user-facing latency whose measurement contract is undefined.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; [TensorRT 11.4.1, Performance Benchmarking: How trtexec Schedules Inferences and Reports Metrics, Inference Phase Flags, Advanced Performance Measurement Techniques](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html), consulted 2026-11-14; [PyTorch 2.11, CUDA semantics, asynchronous execution](https://docs.pytorch.org/docs/2.11/notes/cuda.html#asynchronous-execution); [GStreamer, queue, limits and blocking](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html). Constructed flow calculations and protocols: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-PIPELINE-003 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-004

Objective: Size eight streams under p99. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-004
Question: Track F — design: process eight 1080p streams at 30 frames/s on an embedded module with a defined p99 latency budget. Which process makes the hardware choice verifiable?
Reponse: **Expected answer**: Set freshness, drop and quality requirements; profile each stage and then the full load of 240 images/s; test batching, concurrency, queues and load and thermal scenarios before choosing hardware or an optimization.

**Further explanation**: Keep latency, throughput, memory and quality together. Plan an explicit overload policy rather than an unbounded buffer; no product throughput is guaranteed here.

**Proposed sizing**: Start with a single-stream baseline to check contracts and instrumentation, then increase the load up to eight simultaneous streams. Observe which resource and which queue saturate, keeping the model, its precision and its thresholds fixed. The aggregate throughput of 240 images/s does not tell whether each stream receives fair service.

**System criteria**: Compare per-stream distributions of latency and observation age with the decision budget. A global p99 can hide a disadvantaged stream; the sum of per-stage p99s is generally not the p99 of the full path, and an empirical per-stream p99 needs enough samples (one minute at 30 frames/s leaves only 18 values above it). Include thermal steady state, peaks and restarts in a documented protocol. These measurements make it possible to choose an optimization that treats the actual bottleneck, rather than blindly oversizing the hardware or compressing only the network.

**Bursts and fairness**: Eight cameras with the same average frame rate can deliver their frames simultaneously or staggered. The aggregate rate remains 240 frames/s, but queue peaks and per-stream delay may change. Testing both configurations, then a temporarily heavier-loaded stream, reveals scheduling effects. An overall average can hide a rarely served stream or losses concentrated on one camera. Report latency, frame age, drops and quality per stream as well as in aggregate. The p99 budget must be measured on the full path under a defined load, without mechanically adding the percentiles of the stages.

**Blocking errors**: Sizing from the model's isolated FPS, or adding per-stage p99s mechanically.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating verification, limit of the conclusion. Constructed case, without field observation.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; sizing case constructed by the project; [Dean and Barroso 2013, The Tail at Scale, Component-Level Variability Amplified By Scale](https://www.barroso.org/publications/TheTailAtScale.pdf); [TensorRT 11.4.1, Performance Benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html) and [GStreamer queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consulted 2026-11-14.
Tags: cv::pilote cv::d14 famille::conception cv_id::CV-PIPELINE-004 provenance::agent pole::C pole::E pole::F cas_pole::F::conception
END

## CV-PIPELINE-005

Objective: Locate a bottleneck by trace. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-005
Question: GPU utilization is low while latency is high. Which measurements distinguish CPU decoding, transfers and queues?
Reponse: **Expected answer**: Trace CPU/GPU time, H2D/D2H, waits and age of frames with representative load.

**Further explanation**: Change one stage at a time and keep the same quality contract. Average utilization alone does not locate the cause.

**Interpretation of traces**: An underutilized GPU may be waiting for decoded images, for copies or for a dependency between stages. Average utilization hides the alternation of computing and waiting; it does not say which component should be accelerated.

**Proposed ablation**: Instrument the timeline, then temporarily replace decoding with prepared inputs, or measure an isolated transfer, with an explicit measurement objective. Then reintroduce the complete chain to check the product gain. Also check batch size and queue size, because reducing one cost can move the bottleneck. The quality of inputs and outputs must remain the same. This approach ties a hypothesis to a discriminating measurement and avoids changing architecture or precision when the model accounts for only a fraction of the observed delay. The tests described are proposals; no hardware trace was executed here.

**Locate a bottleneck by substitution**: Replacing decoding with prepared frames roughly preserves the downstream work and tests the hypothesis that input supply is the limit. Temporarily replacing the network with a saved result tests another limit, provided the postprocessing cost and the number of candidates are kept. These tests are not product performance: they isolate contributions. If the bottleneck moves after a fix, re-trace the entire path rather than adding up isolated gains. Also check copy dependencies and unintended serialization; low GPU utilization may come from repeated short waits rather than from a lack of network capacity.

**Launch-bound case**: TensorRT 11.4.1 notes that when trtexec's Enqueue Time exceeds the GPU Compute Time, the GPU can be underutilized and throughput dominated by host-side overhead; CUDA graphs, enabled by default in trtexec and disabled with `--noCudaGraph`, reduce that overhead. A low utilization can therefore come from kernel launches rather than from decoding or copies; on a timeline this would appear as gaps between kernels while the host thread is busy launching them (project reading of the trace).

**Utilization alone does not identify the bottleneck**: A GPU can be idle because decode starves it, because the CPU waits on a transfer, or because a concurrency policy serializes work. A proposed controlled substitution replaces one stage at a time while retaining downstream input shapes and transfer requirements. Compare timeline gaps, queue depths and output age. Artificial inputs that bypass too much work can exaggerate a stage's apparent benefit, so state exactly which cost the substitution removes.

**Blocking errors**: Optimizing the network without measuring the other stages.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; diagnosis proposed by the project; [TensorRT 11.4.1, Performance Benchmarking: Reported Performance Metrics, Performance Profiling Tools and H2D/D2H Data Transfers](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html), consulted 2026-11-14; [GStreamer, queue, limits and blocking](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html). Constructed flow calculations and protocols: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-PIPELINE-005 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-006

Objective: Map a detector box back through a letterbox and recognize a forgotten padding term. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-PIPELINE-006
Question: A $1920\times1080$ camera frame is resized with its aspect ratio preserved, then padded equally on both sides to the $640\times640$ input of a detector. The detector returns the box $(x_1,y_1,x_2,y_2)=(320,290,416,350)$ in input pixels, as continuous coordinates with the origin at the top-left corner of the first pixel. Which scale and padding did the preprocessing apply, and where is the box in the source frame? If the postprocessing omits the padding from the inverse map, what pattern do the overlays show on the source frames?
Reponse: **Expected answer**: (1) Scale: $r=\min(640/1920,\,640/1080)=1/3$, so the content occupies $640\times360$. (2) Padding: $p_x=0$ and $p_y=(640-360)/2=140$ rows above and below. Forgetting it moves every box down by $p_y/r=420$ source pixels: a constant vertical offset, identical for all boxes, with correct widths, heights and $x$. (3) Inverse: $x=(x'-p_x)/r$ and $y=(y'-p_y)/r$, hence $(960,450,1248,630)$; without the padding term the overlay reads $(960,870,1248,1050)$.

**Further explanation**: The forward map is $x'=rx+p_x$, $y'=ry+p_y$; the inverse removes the padding in input pixels before dividing by the scale. Reversing that order, $y=y'/r-p_y$, leaves $p_y(1/r-1)=280$ px of offset. The scale to invert is the one actually applied on each axis: when `cv2.resize` receives an output size, it computes the factor from the integer sizes, content over source, which equals $r$ here because $1920/3$ and $1080/3$ are integers. An odd padding total needs a recorded split rule; half an input pixel is 1.5 source pixels at $r=1/3$.

**Pixel-centre convention**: In this frame, index $u$ denotes the pixel centre $u+0.5$. OpenCV's bilinear resize samples source index $(d+0.5)s-0.5$ for destination index $d$ and scale $s=1/r$, which is the continuous map above written for centres. Box corners therefore map without half-pixel terms, while an integer index such as a keypoint row maps as $u=(u'+0.5-p_y)/r-0.5$: row 290 returns to 451, not 450. Dropping the half-pixel terms shifts indices by $(1/r-1)/2=1$ source pixel, negligible for boxes but visible on keypoints and masks.

**Diagnosis**: With the padding forgotten, content rows $y'\in[140,500]$ land at $[420,1500]$. No box ever appears in the top 420 rows, and any box coordinate whose true $y$ exceeds 660 px lands below the 1080 px edge, where clipping squashes the box or a validity filter may drop it. A forgotten or wrong scale has another signature: an error that grows with position and changes box sizes. Inverting this letterboxed input with the stretch factors 3 and 1.6875, for instance, puts $y_1$ and $y_2$ at 489.4 and 590.6 instead of 450 and 630. Pass a synthetic frame with a known box through the whole path and compare. Constructed example; recomputed in the check script of this pass.

**Blocking errors**: Taking $r=\max(640/1920,\,640/1080)$, which would crop instead of pad. Dividing by $r$ before subtracting the padding. Placing the padding on the $x$ axis. Expecting the forgotten padding to change box sizes. Blaming the detector for the 420 px offset.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Full reference]]; [OpenCV 4.13.0, resize.cpp L4096–L4103: bilinear source index $(d+0.5)s-0.5$](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp#L4096-L4103); [OpenCV 4.13.0, resize.cpp L4216–L4221: scale computed from the destination and source sizes](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp#L4216-L4221). The letterbox maps, the box, the offsets and the diagnostic signatures are project constructions.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-PIPELINE-006 provenance::agent pole::C pole::E pole::F
END
