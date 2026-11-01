---
id: CV-QUANT
type: methode
domaine: d14
poles: [A, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-PIPELINE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# PTQ, QAT, INT8/FP8 and runtimes

## Problem, data and assumptions

Reduce the cost of inference while preserving the error useful to the product. Inputs: model, calibration/validation data, backend and hardware; output: compatible model/engine and quality – performance measures. A file format is not a guarantee of acceleration.

## Prerequisites and competencies

**Required prerequisites**: [CV-PIPELINE](141-contrats-profiling-video.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

PTQ selects parameters after training; QAT exposes learning to quantification simulation. Explicit Q/DQ, granularity, operator coverage, and kernels define the actual execution. TensorRT, ONNX Runtime, OpenVINO and LiteRT have separate support matrices.

## Mathematics, conventions and units

Schematic whole affine quantification: $q=clip(round(x/s)+z, q_{min}, q_{max})$ and $\hat x=s(q-z)$, scale $s>0$, whole zero-point $z$ and terminals of type $q_{min},q_{max}$. The rounding rule depends on the contract; this entire scheme does not define the FP8 representation. Ranges, saturation and per-tensor/per-channel granularity count. INT8 integer and FP8 floating have different representations/constraints; they are not interchangeable by a simple label.

## Parameters and properties

Calibration distribution, sensitive layers, mixed precision, dynamic shapes and operators. Check runtime/version/GPU or NPU before announcing support for PTQ/QAT or gain; a serialized motor is not universally portable.

## Cost and implementation

Conversions, fallbacks, transfers, and non-network bottlenecks can undo the gain. No engine built or acceleration measured; `latest` runtime documentation accessed again the 2026-10-20, no fixed universal control.

## Evaluation and controlled variation

Baseline float and then even test, acquisition and operating point after quantification. Calibration representativeness and accuracy; measure small objects, subgroups, latency/memory, and full cost.

## Failure modes and diagnosis

No gain after INT8: inspect truly quantified operators, CPU fallback, copies and preprocessing. Recall loss: inspect saturation/distributions and critical layers before changing the business threshold.

## Alternatives and applications

Mixed accuracy, distillation, structured compression and pipeline optimization depending on the bottleneck; file size does not predict processing time.

## Guided reasoning and proposed checks

These constructed cases develop scale, saturation, and real runtime execution. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-QUANT-001

**Question of work**: Beyond the final numerical format, what distinguishes PTQ from QAT?

**Reference Response**: PTQ comes after training; QAT adapts learning to a quantification model.

**Reading the difference**: a PTQ estimates quantization parameters from the model already learned and a suitable procedure. A QAT simulates certain digital effects during learning to allow for adaptation. The final format therefore does not alone reveal how the parameters were obtained.

**Proposed choice**: First compare a floating baseline and a PTQ on the same reserved data, then consider the QAT if the quality loss and the budget justify it. Check the representation, granularity and support of the backend actually used. A training simulation must match the inference contract well enough to be interpretable. The gain also depends on the operators executed and the equipment. Better robustness at quantification does not guarantee acceleration of the entire chain or preservation of small defects: measuring these outputs at the fixed operating point is part of the decision.

### Case linked to CV-QUANT-005

**Question of work**: Which measurements should accompany a detector's memory reduction after quantization?

**Reference Response**: Quality on reserved data and critical cases, plus full system latency/flow/memory at the set operating point.

**Different memories**: The size of the disk weights is not all the memory used: activations, buffers, runtime context and copies can count. A weight compression can therefore produce a gain in storage without proportionally reducing the peak memory in operation.

**Proposed Protocol**: Keep data and decision thresholds, measure AP or useful metrics, critical cases, maximum memory, latency and throughput on the same target. check small or low contrast defects, as a limited numerical variation can change a decision near the threshold. Report conversions and possible operators remaining in other precision. The operating point must be comparable before deciding that compression improves the product. A smaller file is a resource result; it demonstrates neither acceleration, nor sufficient quality, nor robustness to acquisitions that digital calibration has not represented.

**Documentary reference for this pass**: [ONNX, QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21), Summary, scale, zero-point and rounded. The other developments are in the [flashcards](../142-quantification-runtimes.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-QUANT-001

**Situation**: Beyond the final numerical format, what distinguishes PTQ from QAT?

**Simulation and gradients**: The rounding of quantification is constant in pieces and does not directly provide a useful gradient almost everywhere. A QAT therefore uses a suitable learning approximation, often a substitution gradient in the variants concerned, while simulating rounding and forward saturation. The simulated schema must match the scales, granularities and bounds expected at the inference. A static PTQ estimates these parameters without this weight adjustment. Comparing the two requires freezing the final digital contract: training with a simulation and then exporting another schema can cancel the expected interest. No better quality or universal acceleration comes from the name QAT alone.

### CV-QUANT-002

**Situation**: What risk arises when the quantization scale is estimated from data that do not represent deployment images?

**Rounding and clipping error**: with a uniform quantification of steps $s$ and rounded to the nearest, the reconstruction error out of saturation is at most $s/2$, under the announced convention. In saturation, this limit no longer applies: an activation far beyond the range can be strongly clipped. Expanding the range reduces this risk but increases $s$ for a set number of levels. A granularity per channel allows different scales when the amplitudes differ strongly between channels, at the price of the constraints of the backend. Measuring the actual distributions and output errors makes it possible to choose this compromise without assuming that the maximum range observed is always optimal.

### CV-QUANT-003

**Situation**: Why does exporting an ONNX model not guarantee identical accuracy and faster execution on every runtime?

**Declared graph and executed graph**: A Q/DQ representation can materialize conversions between quantized and reconstructed values; the runtime then decides which sequences to merge and which kernels to use according to its target. Their presence in a file does not prove that each operation is accelerated in its entirety. A partition between multiple resources can add copies, synchronizations, and conversions. First compare digital outputs on control inputs, then decision quality on reserved data and finally performance under load. Set appropriate tolerances for output, as a small logit difference can change a detection or deletion close to a threshold.

### CV-QUANT-004

**Situation**: Track F — diagnosis: INT8 does not reduce total vision-pipeline latency. How can the possible causes be distinguished?

**Net engine gain**: If a floating calculation takes $T_f$, a quantified $T_q$ calculation and additional $T_c$ conversions, the local gain already requires $T_q+T_c<T_f$, before other system costs. Small layers can be dominated by launch or conversion rather than multiplication. Comparing the actual trace reveals whether the lack of gain comes from an unchanged engine, a new extra cost or a dominant outdoor stage. The dynamic shapes and the batch must remain comparable. A theoretical measurement of file size or number of operations does not replace this decomposition of the time actually observed.

### CV-QUANT-005

**Situation**: Which measurements should accompany a detector's memory reduction after quantization?

**Memory and discontinuous thresholds**: For a tensor of $n$ values on $b$ bytes, raw storage is $nb$, but multiple copies, activations, and workspaces can coexist. Quantifying only the weights does not divide the whole memory peak by the same factor. On the quality side, a score that goes from 0,501 to 0,499 around a threshold 0,5 can remove a box despite a small numerical error. A change in rank can also change a NMS. Comparing both tensor errors, output after postprocessing and business metrics by size reveals these effects as the numerical error average masks.

**Passages consulted for these developments**: [Jacob et al., quantification](https://arxiv.org/html/1712.05877v1), §3.1, quantification simulation and Algorithm 1; general comment on the substitution gradient without backend guarantee; [ONNX Runtime, quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html), Quantization Overview, Q/DQ and Quantization Debugging; numerical terminals and project scenarios, page consulted on the 2026-10-30.

## Sources and flashcards

- [ONNX QuantizeLinear, operator version 21, Summary](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21): scale, zero-point, saturation and rounding.
- [ONNX Runtime, Execution Providers](https://onnxruntime.ai/docs/execution-providers/), accessed on 2026-10-20: assignment of operators/subgraphs according to capabilities.

- [TensorRT, Quantization Workflows, Viewed on 2026-10-24](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html).
- [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Related flashcards](../142-quantification-runtimes.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
