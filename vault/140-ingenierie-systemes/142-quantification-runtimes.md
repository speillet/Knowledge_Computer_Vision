# Flashcards — PTQ, QAT, INT8/FP8 and runtimes

reference note: [[140-ingenierie-systemes/references/142-quantification-runtimes|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-QUANT-001

Objective: distinguish PTQ and QAT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-001
Question: Beyond the final numerical format, what distinguishes PTQ from QAT?
Reponse: **Expected answer**: PTQ is applied after training; QAT adapts training to a model of quantization.

**Further explanation**: Granularity, backend, data and operators determine the final quality; QAT is not automatically required or superior for every task.

**Reading the difference**: PTQ estimates quantization parameters from the already trained model with a suitable procedure. QAT simulates some numerical effects during training so that the weights can adapt. The final format therefore does not reveal on its own how the parameters were obtained.

**Proposed choice**: First compare a floating-point baseline and a PTQ model on the same held-out data, then consider QAT if the quality loss and the budget justify it. Check the representation, granularity and support of the backend actually used. The training simulation must match the inference contract closely enough to be interpretable. The gain also depends on the operators executed and on the hardware. Better robustness to quantization guarantees neither acceleration of the entire chain nor preservation of small defects: measuring these outputs at the fixed operating point is part of the decision.

**Simulation and gradients**: Quantization rounding is piecewise constant: its derivative is zero almost everywhere and gives no useful gradient. QAT therefore uses a training approximation, usually the straight-through estimator, while simulating rounding and saturation in the forward pass. The simulated scheme must match the scales, granularities and bounds expected at inference. Static PTQ estimates these parameters without adjusting the weights. Comparing the two requires freezing the final numerical contract: training with one simulated scheme and then exporting another can cancel the expected benefit. Neither better quality nor universal acceleration follows from the name QAT alone.

**Fake quantization and actual execution have different contracts**: QAT can simulate quantization effects while storing and computing training quantities in floating point. The final runtime still needs an exported representation and kernels that implement the intended precision. A QAT checkpoint alone does not establish INT8 execution or latency. Compare original, simulated-quantized and deployed outputs on fixed inputs to locate whether a discrepancy originates in training approximation, conversion or backend execution.

**Blocking errors**: Equating the word INT8 with a single training method.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [TensorRT 11.4.1, Quantization Workflows: PTQ and QAT](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-workflows.html), consulted 2026-11-14; [Jacob et al., quantization, §3 and §3.1, simulated quantization and Algorithm 1](https://arxiv.org/html/1712.05877v1); [Nagel et al., §4.1, straight-through estimator](https://arxiv.org/html/2106.08295). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-QUANT-001 provenance::agent pole::A pole::F
END

## CV-QUANT-002

Objective: interpret scale and saturation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-002
Question: What risk arises when the quantization scale is estimated from data that do not represent deployment images?
Reponse: **Expected answer**: Saturation or resolution unsuited to real activations, with significant errors on some outputs.

**Further explanation**: Measure distributions and performance case by case; do not look only at the calibration average.

**Numerical trade-off**: A very wide range coarsens the representation of frequent values; a range that is too narrow clips values met in operation. The chosen scale therefore couples resolution and saturation, according to the chosen scheme and granularity.

**Constructed example**: A calibration set made mostly of bright scenes may not represent the activations caused by a new sensor or a rare condition. Examine distributions and sensitive layers, then compare errors on these cases, without repeatedly tuning on the test set. Keep the data used to determine numerical parameters separate from the data used to evaluate the product. A number of images does not replace their representativeness. If mixed precision is tried, measure its quality and real cost rather than assuming that the same format everywhere is the best compromise.

Also record the origin of the images used, so that this numerical calibration can be reproduced.

**Rounding and clipping error**: With uniform quantization of step $s$ and round-to-nearest, the reconstruction error inside the range is at most $s/2$, under the stated convention. In saturation this bound no longer applies: an activation far beyond the range can be heavily clipped. Widening the range reduces this risk but increases $s$ for a fixed number of levels. Per-channel granularity allows different scales when amplitudes differ strongly between channels, subject to backend constraints. Measuring the actual distributions and output errors makes it possible to choose this trade-off without assuming that the largest observed range is always optimal.

**Outliers trade range against resolution**: For a fixed integer range, expanding the represented activation interval increases scale $s$, reducing clipping while making rounding coarser. Restricting the interval does the reverse. A small number of extreme activations can therefore degrade precision for the bulk if they determine the entire range. Inspect intermediate activation differences and critical output strata on held-out deployment-like images; a globally small tensor error need not preserve a threshold-sensitive detector decision.

**Blocking errors**: Assuming that a few arbitrary images give a universal calibration.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [Nagel et al., §2.2 and §3.1, rounding against clipping and range setting](https://arxiv.org/html/2106.08295); [TensorRT 11.4.1, PTQ and representative calibration data](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-workflows.html); [ONNX v1.16.0, QuantizeLinear (opset 21)](https://github.com/onnx/onnx/blob/v1.16.0/docs/Operators.md#QuantizeLinear); [ONNX Runtime, quantization, static calibration and Quantization Debugging](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consulted 2026-11-14. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-QUANT-002 provenance::agent pole::A pole::F
END

## CV-QUANT-003

Objective: Check the support of a runtime. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-003
Question: Why does exporting an ONNX model not guarantee identical accuracy and faster execution on every runtime?
Reponse: **Expected answer**: Supported operators, shapes, kernels, numerical precisions and hardware differ; conversions, fallbacks and preprocessing must be validated.

**Further explanation**: Version the export, the runtime, the target and the measurements; inspect the executed graph.

**Format and execution**: An exchange graph describes operations, but a runtime must support them and choose implementations for the target. Conversions or subgraphs on another device can change time, memory and sometimes numerical behavior. The presence of the file does not prove that the intended optimized path is used.

**Proposed validation**: Compare inputs, relevant intermediate outputs and the final output with a reference on known examples, then measure the complete system. Record versions, opset, shapes and precisions, as well as pre- and postprocessing. Examine the operators actually assigned to the target backend before blaming the architecture for a missing gain. A successful export is a compatibility step; putting the model into service still requires useful equivalence, resources and quality under the product's conditions. The same model can strike different trade-offs on CPU, GPU or another accelerator.

**Declared graph and executed graph**: A Q/DQ representation makes the conversions between quantized and reconstructed values explicit; the runtime then decides which sequences to fuse and which kernels to use for its target. Their presence in a file does not prove that each operation is accelerated end to end. A partition across several devices can add copies, synchronizations and conversions. First compare numerical outputs on reference inputs, then decision quality on held-out data, and finally performance under load. Set suitable output tolerances, because a small logit difference can change a detection or an NMS suppression close to a threshold.

**Format dialects**: Two runtimes can disagree on the same ONNX file. TensorRT 11.4.1 imports Q/DQ pairs but reports an import error for pre-quantized operators such as `QLinearConv`, `QLinearMatMul`, `ConvInteger` and `MatMulInteger`, which ONNX Runtime's QOperator format produces; TensorRT also uses a symmetric scheme only, while ONNX Runtime accepts zero-points and, on GPU, only signed 8-bit activations and weights. An exported file must therefore be checked against the target's documented format, not only against the ONNX checker.

**Blocking errors**: Equating an exchange format with universally optimized execution.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [TensorRT 11.4.1, Explicit Quantization: ONNX Support](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-explicit-quantization.html) and [Working with Quantized Types](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/work-with-quantized-types.html); [ONNX Runtime, Execution Providers and GetCapability](https://onnxruntime.ai/docs/execution-providers/); [ONNX Runtime, quantization: representation formats, data-type selection and Quantization Debugging](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consulted 2026-11-14.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-QUANT-003 provenance::agent pole::A pole::F
END

## CV-QUANT-004

Objective: Diagnose a missing INT8 gain. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-004
Question: Track F — diagnosis: INT8 does not reduce total vision-pipeline latency. How can the possible causes be distinguished?
Reponse: **Expected answer**: Full engine and pipeline profile, effective operators/precisions, fallback, CPU preprocessing and transfers.

**Further explanation**: Compare at the same load and quality; accelerating a small stage can be invisible at system level. Fix the observed bottleneck before compressing further.

**Decomposition of gain**: If only the engine accelerates while decoding or copying dominates, the total delay changes little. If the engine does not accelerate, examine which operators were quantized, the conversions and the kernels selected. The two situations lead to different interventions.

**Proposed ablation**: Keep the same images, batch, shapes and decision rule; compare engine time, transfers and total time with identical warm-up and load. Also check that quality is maintained, because a modified threshold can change the cost of downstream stages. Relate the diagnosis to Amdahl's simple model without using it as an identity for the p99 or for queues. The result may justify mixed precision or an optimization outside the network, but it does not support a universal conclusion for or against INT8.

**Net engine gain**: If the floating-point computation takes $T_f$, the quantized computation $T_q$ and the added conversions $T_c$, a local gain already requires $T_q+T_c<T_f$, before other system costs. Small layers can be dominated by launch or conversion costs rather than multiplications. Comparing the actual trace shows whether the missing gain comes from an unchanged engine, a new overhead or a dominant stage outside the engine. Dynamic shapes and batch size must remain comparable. A theoretical figure such as file size or operation count does not replace this decomposition of the time actually observed.

**Fusion and kernel conditions**: TensorRT 11.4.1 warns that performance can decrease when it cannot fuse operations with the surrounding Q/DQ layers, and that older devices may lack low-precision kernels for some layers; ONNX Runtime notes that quantize and dequantize add overhead and that it is not rare to get worse performance on old devices. Reading which layers run in which precision, and where Q/DQ nodes remain unfused, therefore belongs to the diagnosis before any conclusion about the model.

**Amdahl bounds the useful acceleration**: If inference occupies 20% of a sequential pipeline and INT8 makes it twice as fast without overhead, total speedup is $1/(0.8+0.2/2)\approx1.11$. A conversion cost of 10% of the old total would erase that gain in this constructed model. Measure the accelerated fraction and added transfers or layout conversions before concluding that quantization failed numerically or that INT8 must improve the entire system.

**Blocking errors**: Concluding that quantization is always useless or always poorly implemented.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating verification, limit of the conclusion. Constructed case, without field observation.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; diagnosis constructed by the project; [TensorRT 11.4.1, Explicit Quantization: Q/DQ Layer-Placement Recommendations](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-explicit-quantization.html) and [Performance Benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html); [ONNX Runtime, subgraphs by provider](https://onnxruntime.ai/docs/execution-providers/); [ONNX Runtime, quantization FAQ](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consulted 2026-11-14. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-QUANT-004 provenance::agent pole::A pole::F cas_pole::F::diagnostic
END

## CV-QUANT-005

Objective: check quality and performance together. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-005
Question: Which measurements should accompany a detector's memory reduction after quantization?
Reponse: **Expected answer**: Quality on held-out data and critical cases, plus full-system latency, throughput and memory at the fixed operating point.

**Further explanation**: Check small objects, domains and saturation; a smaller model does not establish that the deployment is acceptable.

**Different memory terms**: The on-disk size of the weights is not all the memory used: activations, buffers, runtime context and copies also count. Weight compression can therefore reduce storage without proportionally reducing peak memory in operation.

**Proposed protocol**: Keep data and decision thresholds fixed; measure AP or the relevant metrics, critical cases, peak memory, latency and throughput on the same target. Check small or low-contrast defects, because a small numerical change can alter a decision near the threshold. Report conversions and any operators left in another precision. The operating point must be comparable before deciding that compression improves the product. A smaller file is a resource result; it demonstrates neither acceleration, nor sufficient quality, nor robustness to acquisition conditions that the numerical calibration did not represent.

**Memory and discontinuous thresholds**: For a tensor of $n$ values of $b$ bytes each, raw storage is $nb$, but several copies, activations and workspaces can coexist. Quantizing only the weights does not divide the whole memory peak by the same factor. On the quality side, a score that goes from 0.501 to 0.499 around a threshold of 0.5 can remove a box despite a small numerical error. A change in score order can also change the NMS result. Comparing tensor errors, outputs after postprocessing and product metrics by object size reveals effects that the average numerical error hides.

**Constructed memory budget** (recomputed in the check script of this pass): a detector with 25 M parameters stores 100 MB of FP32 weights, and INT8 brings them to 25 MB, the factor 4 of 8-bit weights [Krishnamoorthi, abstract]. Suppose that two live $64\times320\times320$ activation maps, 26.2 MB each in FP32, and 200 MB of runtime context and workspace coexist at the peak. Weight-only INT8 then lowers the peak from 352 MB to 277 MB: 21% less, for a file 75% smaller. Quantizing the activations too brings each map to 6.6 MB and the peak to 238 MB, and the workspace, held fixed here, now dominates. Read the peak by component on the device; the file size does not predict it.

**Paired comparison on critical cases** (constructed): run the float and INT8 models on the same 200 critical defects. Float finds 190 and INT8 186, but only the discordant defects carry evidence: 6 are missed by INT8 alone and 2 by float alone. If either model were equally likely to miss a discordant defect, a split at least as uneven as 6 to 2 would occur with probability $2\times37/256\approx0.29$. This set therefore does not establish the 2-point recall drop, nor rule it out. Report the discordant counts and the flipped decisions next to the two recalls, and enlarge the critical set before concluding.

**Blocking errors**: Reporting only the bit width or the file size.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; joint quality and cost protocol proposed by the project; the memory budget and the paired comparison are project constructions; [Krishnamoorthi, abstract, factor-4 model size for 8-bit weights](https://arxiv.org/abs/1806.08342); [TensorRT 11.4.1, Working with Quantized Types](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/work-with-quantized-types.html); [ONNX Runtime, quantization, Quantization Debugging](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consulted 2026-11-14.
Tags: cv::pilote cv::d14 famille::evaluation cv_id::CV-QUANT-005 provenance::agent pole::A pole::F
END
