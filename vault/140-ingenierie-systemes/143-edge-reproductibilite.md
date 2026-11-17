# Flashcards — Edge deployment, compression and monitoring

reference note: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-DEPLOIEMENT-001

Objective: Bound a system gain. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-001
Question: Inference accounts for 10% of mean processing time and becomes twice as fast with no other cost. What is the ideal overall speedup?
Reponse: **Expected answer**: Approximately 1/0.95 ≈ 1.053×, under the stated Amdahl model.

**Further explanation**: The p99 and the queues can react differently; check by a full measurement rather than extrapolating the gain of one kernel.

**Calculation interpreted**: Normalize the initial time to one. The non-accelerated share is 0.9; inference goes from 0.1 to 0.05. The total time becomes 0.95, a 5% reduction, and the speedup is its inverse. The accelerated stage occupied only a small part of the total work.

**Product consequence**: Profiling before compressing avoids investing in an optimization whose overall gain is limited in this model. Added conversion costs can even cancel the gain. Conversely, relieving a critical resource in a system with contention can change queues in ways this additive calculation does not describe. It is therefore reasoning under explicit assumptions, not a prediction of the whole latency distribution. Confirm the gain under the same load and quality contract.

**Bound and added cost**: In the same sequential model, even an infinite acceleration of the fraction $f=0.1$ limits the overall factor to $1/(1-f)=1/0.9\simeq1.111$. If the optimization adds a normalized cost $c$, the time becomes $(1-f)+f/s+c$; for $s=2$, any $c\ge0.05$ cancels the gain of this example. These calculations guide the choice of what to optimize. They do not predict queueing under contention: near saturation, a small change in service time can change the wait a lot. Measuring the sustained regime, timing and quality then confirms the practical scope of this analytical estimate.

**Inverting the bound** (constructed, recomputed in the check script of this pass): solving $1/S=(1-f)+f/s$ for $s$ gives the stage speedup that a target $S$ requires, $s=f/(1/S-(1-f))$. With $f=0.1$, an overall 1.05× needs $s\approx1.91$, 1.10× needs $s=11$, and 1.111× needs an infinite $s$. With $f=0.6$, merely doubling inference gives $1/(0.4+0.3)\approx1.43$×. The measured fraction $f$ matters more than the kernel speedup $s$, which is why profiling comes first.

**Latency adds, pipelined throughput does not** (worked example A of the reference): on a 40 ms path of decoding 8, preprocessing 6, inference 20 and postprocessing 6 ms, an INT8 engine 2.5 times faster that adds 2 ms of reformatting gives 30 ms, a 1.33× latency gain. If the four stages run as a pipeline on successive frames, throughput follows the slowest stage instead: 20 ms before, 10 ms after with the reformatting inside the inference stage, so 50 → 100 frames/s. Conversely, when another stage is slower than inference, accelerating inference leaves pipelined throughput unchanged, whatever its effect on latency. State which quantity the speedup refers to.

**Blocking errors**: Announcing a pipeline twice as fast.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; algebraic derivation by the project for the sequential model of the reference note: normalized time after the change $(1-f)+f/s$, i.e. $0.9+0.1/2=0.95$, and its inverse for the required $s$; the 40 ms path is the reference's constructed worked example A; [Amdahl (1967), p. 483](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf) for the limit imposed by the non-accelerated part, stated in words in the paper; [NVIDIA TensorRT 11.4.1, Performance Benchmarking, measurement scope](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html), consulted 2026-11-14.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-DEPLOIEMENT-001 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-002

Objective: Linking compression and acceleration. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-002
Question: Why does reducing the number of weights through pruning not guarantee faster inference?
Reponse: **Expected answer**: The backend must exploit the sparsity structure and available kernels; conversions or memory access may dominate.

**Further explanation**: Measure the executed graph on the target hardware, including quality; on-disk size and execution time are different quantities.

**Why counting is not enough**: A zero weight is not automatically a multiplication skipped by the kernel. The sparsity pattern, the tensor shapes and the available operations determine whether the hardware can exploit the removal. A sparse representation can also add indexing and transfers.

**Proposed comparison**: Inspect the graph actually executed and measure the same task on the target hardware, with quality and memory. Distinguish structured pruning, which can change the dimensions of the computation, from unstructured sparsity, whose execution requires appropriate support. Check which layers really dominate the time. Fewer parameters can remain useful for storage or distribution without speeding up inference. Speed claims should therefore come with the sparsity pattern, backend and protocol, rather than be inferred from a percentage of zeros independent of the implementation.

**Dimensions and zeros**: Removing entire channels can reduce tensor dimensions and the work of dense kernels, if all dependent layers are adapted. Setting isolated weights to zero often keeps the same dimensions and the same number of operations performed by a dense kernel. A sparse representation can skip computations but adds index metadata and less regular memory access. Compare the pattern actually supported and the execution trace, not just the number of non-zero parameters. Distillation can help a smaller model regain quality, but it is another training intervention, to be evaluated separately from pruning.

**Hardware-supported pattern**: TensorRT 11.4.1 accelerates only 2:4 structured sparsity on Ampere and later GPUs: for each output channel and kernel position, every four input channels need at least two zeros, the layer must run in FP16 or INT8, and the builder still picks a dense tactic when it is faster (22 of 53 eligible layers in the documentation's example). Forcing the pattern can cost accuracy that fine-tuning must recover.

**Blocking errors**: Deducing speed and energy automatically from the fraction of zero weights.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; [TensorRT 11.4.1, Data Formats and Tensors, Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/data-formats-tensors.html): sparse tactics are not always selected because they can be slower, consulted 2026-11-14; [Li et al. 2017, Pruning Filters for Efficient ConvNets, abstract](https://arxiv.org/abs/1608.08710): irregular sparsity against filter pruning.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-DEPLOIEMENT-002 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-003

Objective: version a complete system. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-003
Question: Beyond model weights, what must be versioned to reproduce a vision system's output?
Reponse: **Expected answer**: Preprocessing and coordinate frames, architecture, taxonomy, postprocessing and thresholds, runtime and relevant dependencies, as well as a reference input.

**Further explanation**: Test compatibility and rollback before deployment; a difference in resizing or in BGR/RGB order may change the decision.

**Example of regression**: Identical weights may produce another decision if the input changes from RGB to BGR, if the boxes are decoded in another coordinate frame, or if the class indices change. The deployed model is therefore a set of contracts and artifacts around the network.

**Proposed procedure**: Keep a reference input with outputs at several stages, then compare a new version against it before deploying. Version the parameters and dependencies that change these outputs, together with the format expected by the consumer. Plan compatibility and rollback of the entire chain, not just the weights. Exact equality may not be realistic across all numerical targets; define a tolerance tied to the use and review decisions close to the threshold. This check makes it easier to attribute a regression and lets another engineer reproduce it.

**Reproducible manifest**: Tie a version to hashes of the weights and configuration, input and output contracts, the taxonomy, postprocessing parameters and the execution environment. Keeping a reference input with the relevant intermediate results helps locate the first divergence between versions. Define a numerical tolerance and a decision tolerance; they are not equivalent near a threshold. A rollback must restore the compatible set, because returning to old weights alone with new class indices can keep a regression. A rollback rehearsal on a test bench verifies this contract without assuming that it will work in production.

**A reproducibility fixture should locate the first divergence**: Keep a versioned input fixture with decoded image properties, transformed coordinates and selected intermediate/final outputs under stated tolerances. When a deployment changes, compare these stages in order to distinguish decoding, preprocessing, inference and postprocessing discrepancies. Record runtime, device and relevant configuration with artifact hashes. Identical weights can still produce another system output when class mapping, threshold or coordinate inversion changes.

**Engine portability**: The runtime belongs to the versioned set. A TensorRT 11.4.1 plan records the TensorRT version and the GPU compute capability and fails to deserialize when either differs; hardware-compatible builds are not supported on JetPack, so an embedded fleet needs one engine per device type and runtime version, listed in the manifest. PyTorch 2.11 likewise states that completely reproducible results are not guaranteed across releases, commits, platforms, or CPU and GPU executions, which is why tolerances replace bitwise equality across versions.

**Blocking errors**: Treating the weights as the only artifact of the deployed model.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; [The ML Test Score, Infra 1, Infra 6, Infra 7 and Monitor 3](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf); [Sculley et al. 2015, §2 (CACE) and §6 (configuration debt)](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf); [TensorRT 11.4.1, Engine Compatibility](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/engine-compatibility.html); [PyTorch 2.11, Reproducibility](https://docs.pytorch.org/docs/2.11/notes/randomness.html), consulted 2026-11-14; list of contracts adapted by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-DEPLOIEMENT-003 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-004

Objective: Test sustained edge operation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-004
Question: A short benchmark passes, but throughput drops after an hour on an edge device. Which traces should be collected?
Reponse: **Expected answer**: Temperature/frequency, load/memory, transfers and queues, with quality and end-to-end timestamps.

**Further explanation**: Distinguish throttling, a memory leak or an accumulation of delay; repeat the representative scenario after the fix.

**Why duration matters**: Thermal state, memory occupation and queues can change after boot. A short measurement on a cold device does not necessarily describe its sustained regime. A frequency drop, a leak or a build-up of waiting time produce different signatures.

**Proposed investigation**: Plot temperature, clock frequencies, memory, per-stage rates and frame age together, over a representative load and duration. Identify which change precedes the degradation, then change one hypothesis at a time. For example, compare a bounded queue with the initial policy without changing the model, or check the device's thermal behaviour. Then confirm full quality and timing. A computational cause does not rule out a data cause; the system must keep inputs and configuration to explain failures, without settling on a single diagnosis from the final FPS alone.

**Temporal signatures**: A frequency drop correlated with a temperature rise supports a hypothesis of power or thermal limitation; continuous memory growth points to another investigation; stable memory with increasing frame age may signal a queue overload. These correlations guide the tests without establishing a single cause. Replaying the same load for long enough and changing one factor at a time makes it possible to compare start-up and steady-state rates. Also record accuracy, drops and outputs, because holding the rate by dropping more images changes the service delivered. Validation concerns the complete sustained behaviour, not just the time of the first network pass.

**Platform counters**: On Jetson Linux r36.4, software clock throttling starts when a sensor crosses a passive trip point (99.0 °C for the CPU zone of AGX Orin and the Orin NX and Nano series), hardware throttling handles power and thermal transients, the `oc*_event_cnt` nodes under `/sys/class/hwmon` count overcurrent events, and `tegrastats` reports CPU, GPU and EMC frequencies with thermal-zone temperatures. Logging these beside latency separates thermal throttling from power throttling and from causes outside the device.

**Sustained validation needs time-correlated traces**: A proposed long-duration test logs frame arrival/output times, queue depth, temperature, clock frequency, memory and power/load indicators on a common time axis. A throughput drop correlated with throttling supports one diagnosis; monotonic memory growth or growing queues supports others. Repeat a controlled intervention before claiming causality. Report the warmup and sustained interval, since a short cold-device benchmark does not establish an hour-long operating point.

**Blocking errors**: Declaring the hardware sufficient from an isolated cold test.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; diagnosis proposed by the project; [Jetson Linux r36.4, Platform Power and Performance: Software Clock Throttling, Hardware Throttling, Thermal Specifications, Overcurrent Event Status](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html) for the thermal mechanism, without assuming this platform in all deployments; [NVIDIA TensorRT 11.4.1, Performance Benchmarking: power and thermal throttling](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html), consulted 2026-11-14. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-DEPLOIEMENT-004 provenance::agent pole::A pole::C pole::E pole::F
END
