# Flashcards — Edge deployment, compression and monitoring

reference note: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-DEPLOIEMENT-001

Objective: Limiting a system gain. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-001
Question: Inference accounts for 10% of mean processing time and becomes twice as fast with no other cost. What is the ideal overall speedup?
Reponse: **Expected answer**: Approximately 1/0,95 = 1,053×, depending on Amdahl model announced.

**Further explanation**: The p99 and the queues can react differently; check by full measurement rather than extrapolate the gain of a kernel.

**Calculation interpreted**: normalize the initial time to one. The non-accelerated share is 0,9; the inference goes from 0,1 to 0,05. The total time becomes 0,95, a reduction of 5%, and the speed factor is its inverse. The accelerated floor occupied only a small part of the total work.

**Product consequence**: profiling before compressing avoids investing in optimization whose overall gain is limited in this model. New additional conversion costs can even nullify the profit. Conversely, reducing a critical resource in a competing system can modify queues in a way that this additive calculation does not describe. It is therefore a line of reasoning under explicit assumptions, not a prediction of the entire latency distribution. Confirm the gain on the same load and quality contract.

**Boundary and additional cost**: in the same sequential model, even an infinite acceleration of the fraction $f=0,1$ limits the global factor to $1/(1-f)=1/0,9\simeq1,111$. If the optimization adds a standardized cost $c$, the time becomes $(1-f)+f/s+c$; for $s=2$, all $c\ge0,05$ cancels the gain of this example. These calculations guide the choice of work to be optimized. They do not predict a competing queue: near saturation, a small reduction in service can greatly change the wait. Then measuring sustained regime, time and quality confirms the practical scope of this analytical marker.

**Blocking errors**: Announce a pipeline twice as fast.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; derivation project algebraic for the sequential model of the reference note: normalized time after change $(1-f)+f/s$, i.e. $0,9+0,1/2=0,95$; [Amdahl (1967), p. 483](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf) for the limit imposed by the non-accelerated part; [NVIDIA TensorRT, benchmarking, measurements and perimeter, consulted on 2026-10-30; Amdahl, manifesto and signatures built by the project](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consult the 2026-10-30.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-DEPLOIEMENT-001 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-002

Objective: Linking compression and acceleration. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-002
Question: Why does reducing the number of weights through pruning not guarantee faster inference?
Reponse: **Expected answer**: The backend must exploit the sparsity structure and available kernels; conversions or memory access may dominate.

**Further explanation**: Measure real graph and target hardware, including quality; disk size and time are different sizes.

**Why counting is not enough**: A zero weight is not automatically a multiplication avoided by the kernel. The pattern of sparsity, the shape of the tensors and the operations available determine whether the equipment can exploit this removal. A sparse representation can also add indexing and transfers.

**Proposed comparison**: inspect the graph actually executed and measure the same task on the target hardware, with quality and memory. Distinguish structured pruning, which can change the dimensions of the calculation, and unstructured sparsity, which operation requires appropriate support. Check the layers that really dominate time. A reduction in the number of parameters can remain useful for storage or distribution without speeding up inference. Speed statements should therefore be accompanied by the schema, backend, and protocol, rather than inferred from an implementation-independent zero percentage.

**Dimensions and zeros**: Removing entire channels can reduce the dimensions of tensors and the work of dense kernels, if all dependent layers are adapted. Setting isolated weights to zero often retains the same dimensions and the same number of operations performed by a dense kernel. A sparse representation can avoid calculations but add less regular clues and memory access. Compare the actually supported pattern and run trace, not just the number of non-zero parameters. Distillation can help a smaller model regain quality, but it is another learning intervention to be evaluated separately from pruning.

**Blocking errors**: Automatically deducts speed and energy from the zero weight ratio.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; [TensorRT 8.6.1, §6.10 Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/developer-guide/index.html#structured-sparsity): Hollow tactics are not systematically selected because they can be slower; [NVIDIA TensorRT, benchmarking, measurements and perimeter, consulted on 2026-10-30; Amdahl, manifesto and signatures built by the project](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consult the 2026-10-30.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-DEPLOIEMENT-002 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-003

Objective: version a complete system. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-003
Question: Beyond model weights, what must be versioned to reproduce a vision system's output?
Reponse: **Expected answer**: Pre-processing/coordinate frames, architecture, taxonomy, post-processing/thresholds, runtime and relevant dependencies, as well as a reference entry.

**Further explanation**: Test compatibility and rollback before deployment; a difference in resize or BGR/RGB may change the decision.

**Example of regression**: Identical weights may produce another decision if the input changes from RGB to BGR, if the boxes are decoded in another coordinate frame, or if the class indices change. The model used is therefore a set of contracts and artifacts around the network.

**Proposed procedure**: Keep a multi-step reference input and outputs, then compare a new version before deploying it. Version parameters and dependencies that change these outputs, with the format expected by the consumer. Provide compatibility and backtracking of the entire chain, not just weights. An exact equality may not be realistic between all numerical targets; define usage-related tolerance and review decisions close to the threshold. This check facilitates the assignment of a regression and reproduction by another engineer.

**Manifeste reproductible**: Link a version to weight and configuration footprints, input/output contracts, taxonomy, postprocessing parameters, and execution environment. Keeping a sample entry with the relevant intermediate results helps locate the first divergence between versions. Define numerical tolerance and decision tolerance; they are not equivalent near a threshold. The rollback must restore the compatible set, as returning to old weights alone with new class indices can retain a regression. A back-test on a test line verifies this contract without assuming that it will work properly in production.

**A reproducibility fixture should locate the first divergence**: Keep a versioned input fixture with decoded image properties, transformed coordinates and selected intermediate/final outputs under stated tolerances. When a deployment changes, compare these stages in order to distinguish decoding, preprocessing, inference and postprocessing discrepancies. Record runtime, device and relevant configuration with artifact hashes. Identical weights can still produce another system output when class mapping, threshold or coordinate inversion changes.

**Blocking errors**: Consider the weights as the only artifact of the model exploited.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; [The ML Test Score, Model/Infra tests and rollback](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf); list of contracts adapted by the project; [NVIDIA TensorRT, benchmarking, measurements and perimeter, consulted on 2026-10-30; Amdahl, manifesto and signatures built by the project](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-DEPLOIEMENT-003 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-004

Objective: Test the edge. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-004
Question: A short benchmark passes, but throughput drops after an hour on an edge device. Which traces should be collected?
Reponse: **Expected answer**: Temperature/frequency, load/memory, transfers and queues, with quality and end-to-end timestamps.

**Further explanation**: Distinguish throttling, leakage or accumulation of delay; repeat the representative scenario after correction.

**Why Duration Matters**: Thermal state, memory occupation and queues can change after boot. A short measurement on a cold device does not necessarily describe its sustainable diet. A drop in frequency, a leak, or a build-up of waiting time produce different signatures.

**Proposed investigation**: simultaneously plotting temperature, frequencies, memory, step rates and frame age, over a representative load and duration. Identify which change precedes the degradation, and then modify one hypothesis at a time. For example, compare a limited queue to the initial policy without changing the model, or check the thermal regime according to the device. Then confirm full quality and time. A computational cause does not rule out a data cause; the system must retain inputs and configuration to explain failures, without announcing a single diagnosis from the final FPS alone.

**Signatures temporelles**: A frequency drop correlated with a thermal rise supports a hypothesis of power or temperature limitation; continuous memory growth suggests another investigation; stable memory with increasing frame age may signal a queue overload. These correlations guide the trials without establishing a single cause. Replaying the same load over a sufficient period of time and changing one factor at a time makes it possible to compare start and steady speed. Also keep accurate, drops and outputs, because holding the rate by abandoning more images changes the service rendered. Validation is about complete sustainable behavior, not just about the time of the first network pass.

**Sustained validation needs time-correlated traces**: A proposed long-duration test logs frame arrival/output times, queue depth, temperature, clock frequency, memory and power/load indicators on a common time axis. A throughput drop correlated with throttling supports one diagnosis; monotonic memory growth or growing queues supports others. Repeat a controlled intervention before claiming causality. Report the warmup and sustained interval, since a short cold-device benchmark does not establish an hour-long operating point.

**Blocking errors**: Declare sufficient material on an isolated cold test.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Full reference]]; Diagnosis proposed by the project; [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html) for the thermal mechanism, without assuming this platform in all deployments; [NVIDIA TensorRT, benchmarking, measurements and perimeter, consulted on 2026-10-30; Amdahl, manifesto and signatures built by the project](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-DEPLOIEMENT-004 provenance::agent pole::A pole::C pole::E pole::F
END
