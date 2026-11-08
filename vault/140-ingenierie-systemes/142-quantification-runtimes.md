# Flashcards — PTQ, QAT, INT8/FP8 and runtimes

reference note: [[140-ingenierie-systemes/references/142-quantification-runtimes|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-QUANT-001

Objective: distinguish PTQ and QAT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-001
Question: Beyond the final numerical format, what distinguishes PTQ from QAT?
Reponse: **Expected answer**: PTQ comes after training; QAT adapts learning to a quantification model.

**Further explanation**: Granularity, backend, data and operators determine the final quality; QAT is not automatically required or superior for any task.

**Reading the difference**: a PTQ estimates quantization parameters from the model already learned and a suitable procedure. A QAT simulates certain digital effects during learning to allow for adaptation. The final format therefore does not alone reveal how the parameters were obtained.

**Proposed choice**: First compare a floating baseline and a PTQ on the same reserved data, then consider the QAT if the quality loss and the budget justify it. Check the representation, granularity and support of the backend actually used. A training simulation must match the inference contract well enough to be interpretable. The gain also depends on the operators executed and the equipment. Better robustness at quantification does not guarantee acceleration of the entire chain or preservation of small defects: measuring these outputs at the fixed operating point is part of the decision.

**Simulation and gradients**: The rounding of quantification is constant in pieces and does not directly provide a useful gradient almost everywhere. A QAT therefore uses a suitable learning approximation, often a substitution gradient in the variants concerned, while simulating rounding and forward saturation. The simulated schema must match the scales, granularities and bounds expected at the inference. A static PTQ estimates these parameters without this weight adjustment. Comparing the two requires freezing the final digital contract: training with a simulation and then exporting another schema can cancel the expected interest. No better quality or universal acceleration comes from the name QAT alone.

**Fake quantization and actual execution have different contracts**: QAT can simulate quantization effects while storing and computing training quantities in floating point. The final runtime still needs an exported representation and kernels that implement the intended precision. A QAT checkpoint alone does not establish INT8 execution or latency. Compare original, simulated-quantized and deployed outputs on fixed inputs to locate whether a discrepancy originates in training approximation, conversion or backend execution.

**Blocking errors**: Assimilate the word INT8 to a single learning method.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [TensorRT, Quantization Workflows: PTQ and QAT](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html), accessed on 2026-10-20; [Jacob et al., quantification, §3.1, quantification simulation and Algorithm 1; general comment on the substitution gradient without backend guarantee](https://arxiv.org/html/1712.05877v1), accessed on 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-QUANT-001 provenance::agent pole::A pole::F
END

## CV-QUANT-002

Objective: interpret scale and saturation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-002
Question: What risk arises when the quantization scale is estimated from data that do not represent deployment images?
Reponse: **Expected answer**: Inadequate digital saturation or resolution for real-world activations, with sensitive errors on some outputs.

**Further explanation**: Measure distributions and performance on a case-by-case basis; don’t just look at the calibration average.

**Digital Compromise**: a very wide range can reduce the fineness of the representation of frequent values; a too narrow range can limit the values encountered in operation. The chosen scale therefore links resolution and saturation, according to the chosen scheme and granularity.

**Constructed example**: A calibration dataset consisting mostly of clear scenes may not accurately represent the activations caused by a new sensor or a rare condition. Examine distributions and sensitive layers, then compare errors on these cases, without setting the test indefinitely. Maintain a separation between data used to determine numerical parameters and data used to evaluate the product. A number of images does not replace their representativeness. If mixed precision is tried, measure its quality and real cost rather than assuming that the same format everywhere is the best compromise.

Also keep the origin of the images used to be able to reproduce this digital calibration.

**Rounding and clipping error**: with a uniform quantification of steps $s$ and rounded to the nearest, the reconstruction error out of saturation is at most $s/2$, under the announced convention. In saturation, this limit no longer applies: an activation far beyond the range can be strongly clipped. Expanding the range reduces this risk but increases $s$ for a set number of levels. A granularity per channel allows different scales when the amplitudes differ strongly between channels, at the price of the constraints of the backend. Measuring the actual distributions and output errors makes it possible to choose this compromise without assuming that the maximum range observed is always optimal.

**Outliers trade range against resolution**: For a fixed integer range, expanding the represented activation interval increases scale $s$, reducing clipping while making rounding coarser. Restricting the interval does the reverse. A small number of extreme activations can therefore degrade precision for the bulk if they determine the entire range. Inspect intermediate activation differences and critical output strata on held-out deployment-like images; a globally small tensor error need not preserve a threshold-sensitive detector decision.

**Blocking errors**: Suppose that some arbitrary images give a universal calibration.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [TensorRT, PTQ and representative data](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html); [ONNX QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21), view 2026-10-20; [ONNX Runtime, quantization, Quantization Overview, Q/DQ and Quantization Debugging; digital terminals and project scenarios, page consulted on 2026-10-30](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), view 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-QUANT-002 provenance::agent pole::A pole::F
END

## CV-QUANT-003

Objective: Check the support of a runtime. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-003
Question: Why does exporting an ONNX model not guarantee identical accuracy and faster execution on every runtime?
Reponse: **Expected answer**: Supported operators, shapes, kernels, accuracy and hardware differ; conversions/fallbacks and preprocessing must be validated.

**Further explanation**: Versioner export, runtime, target and measures; inspect the executed graph.

**Format and execution**: An exchange graph describes operations, but a runtime must support them and choose implementations for the target. Conversions or subgraphs on another resource can change time, memory, and sometimes digital behavior. The presence of the file does not prove that the desired optimized path is being used.

**Proposed Validation**: compare inputs, relevant intermediate outputs and final output with a reference on known examples, then measure the complete system. Record versions, opset, shapes and details, as well as pre/post-processing. Examine the operators actually assigned to the target backend before assigning a lack of gain to the architecture. A successful export is a step of compatibility; a commissioning still requires useful equivalence, resources and quality under the conditions of the product. The same model can have different compromises depending on CPU, GPU or other accelerator.

**Declared graph and executed graph**: A Q/DQ representation can materialize conversions between quantized and reconstructed values; the runtime then decides which sequences to merge and which kernels to use according to its target. Their presence in a file does not prove that each operation is accelerated in its entirety. A partition between multiple resources can add copies, synchronizations, and conversions. First compare digital outputs on control inputs, then decision quality on reserved data and finally performance under load. Set appropriate tolerances for output, as a small logit difference can change a detection or deletion close to a threshold.

**Blocking errors**: Assimilate exchange format and universal optimized execution.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; [TensorRT, Matrix Support and Portability](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html); [ONNX Runtime, Execution Providers and GetCapability](https://onnxruntime.ai/docs/execution-providers/), view 2026-10-20; [ONNX Runtime, quantization, Quantization Overview, Q/DQ and Quantization Debugging; digital terminals and project scenarios, page consulted on 2026-10-30](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), view 2026-10-30.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-QUANT-003 provenance::agent pole::A pole::F
END

## CV-QUANT-004

Objective: diagnose an absence of gain INT8. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-004
Question: Track F — diagnosis: INT8 does not reduce total vision-pipeline latency. How can the possible causes be distinguished?
Reponse: **Expected answer**: Full engine and pipeline profile, effective operators/precisions, fallback, CPU preprocessing and transfers.

**Further explanation**: Compare same load and quality; a small-stage acceleration can be invisible across the system. Correct the observed neck before further compression.

**Decomposition of gain**: If only the engine accelerates while decoding or copying dominates, the total delay can change little. If the engine does not accelerate, consider coverage of selected operators, conversions, and kernels. The two situations lead to different interventions.

**Proposed ablation**: maintain the same images, batch, shapes and decision rule; compare engine time, transfers and full time with identical warm-up and load. Also check that quality is maintained, as a modified threshold can change the cost of downstream steps. Connect the diagnosis to Amdahl's simple model without using it as an identity for the p99 or the queues. The result may justify mixed precision or off-grid optimization, but does not allow a universal conclusion for or against INT8.

**Net engine gain**: If a floating calculation takes $T_f$, a quantified $T_q$ calculation and additional $T_c$ conversions, the local gain already requires $T_q+T_c<T_f$, before other system costs. Small layers can be dominated by launch or conversion rather than multiplication. Comparing the actual trace reveals whether the lack of gain comes from an unchanged engine, a new extra cost or a dominant outdoor stage. The dynamic shapes and the batch must remain comparable. A theoretical measurement of file size or number of operations does not replace this decomposition of the time actually observed.

**Amdahl bounds the useful acceleration**: If inference occupies 20% of a sequential pipeline and INT8 makes it twice as fast without overhead, total speedup is $1/(0.8+0.2/2)\approx1.11$. A conversion cost of 10% of the old total would erase that gain in this constructed model. Measure the accelerated fraction and added transfers or layout conversions before concluding that quantization failed numerically or that INT8 must improve the entire system.

**Blocking errors**: Conclude that quantification is always useless or always poorly implemented.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; Diagnostic built project; [TensorRT benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) and [ONNX Runtime, subgraphs by provider](https://onnxruntime.ai/docs/execution-providers/), consult the 2026-10-20; [ONNX Runtime, quantization, Quantization Overview, Q/DQ and Quantization Debugging; digital terminals and project scenarios, page consulted on 2026-10-30](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-QUANT-004 provenance::agent pole::A pole::F cas_pole::F::diagnostic
END

## CV-QUANT-005

Objective: check quality and performance together. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-QUANT-005
Question: Which measurements should accompany a detector's memory reduction after quantization?
Reponse: **Expected answer**: Quality on reserved data and critical cases, plus full system latency/flow/memory at the set operating point.

**Further explanation**: check small objects, domains and saturation; a reduced model size does not establish an acceptable commissioning.

**Different memories**: The size of the disk weights is not all the memory used: activations, buffers, runtime context and copies can count. A weight compression can therefore produce a gain in storage without proportionally reducing the peak memory in operation.

**Proposed Protocol**: Keep data and decision thresholds, measure AP or useful metrics, critical cases, maximum memory, latency and throughput on the same target. check small or low contrast defects, as a limited numerical variation can change a decision near the threshold. Report conversions and possible operators remaining in other precision. The operating point must be comparable before deciding that compression improves the product. A smaller file is a resource result; it demonstrates neither acceleration, nor sufficient quality, nor robustness to acquisitions that digital calibration has not represented.

**Memory and discontinuous thresholds**: For a tensor of $n$ values on $b$ bytes, raw storage is $nb$, but multiple copies, activations, and workspaces can coexist. Quantifying only the weights does not divide the whole memory peak by the same factor. On the quality side, a score that goes from 0,501 to 0,499 around a threshold 0,5 can remove a box despite a small numerical error. A change in rank can also change a NMS. Comparing both tensor errors, output after postprocessing and business metrics by size reveals these effects as the numerical error average masks.

**Blocking errors**: Report only the number of bits or weight of the file.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Full reference]]; Joint quality/cost protocol proposed by the project; [TensorRT, compromise of quantification](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html), consulted on 2026-10-20; [ONNX Runtime, quantization, Quantization Overview, Q/DQ and Quantization Debugging; digital terminals and project scenarios, page consulted on 2026-10-30](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), consulted on 2026-10-30.
Tags: cv::pilote cv::d14 famille::evaluation cv_id::CV-QUANT-005 provenance::agent pole::A pole::F
END
