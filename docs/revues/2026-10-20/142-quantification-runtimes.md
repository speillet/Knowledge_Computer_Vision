# Review –  PTQ, QAT, INT8/FP8 and runtimes –  2026-10-20

## Overview

5 flashcards audited. Scope of the entire formula and specified sources of support. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 1 large, 4 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Confirmed; source dated and targeted | distinguish PTQ and QAT. | 52 words at the entrance; Finished core, objective retained | reference note and controlled format | Minor | Specify source |
| CV-QUANT-002 | Confirmed; source dated and targeted | interpret scale and saturation. | 44 words at the entrance; Finished core, objective retained | reference note and controlled format | Minor | Specify source |
| CV-QUANT-003 | Confirmed with additional source | Check the support of a runtime. | 38 words at entry; Support contract completed | reference note and controlled format | important | Ajouter ONNX Runtime |
| CV-QUANT-004 | Deduction from the explicit project | diagnose an absence of gain INT8. | 80 words at entry; finite assumptions and measurement criteria | reference note and controlled format | Minor | Attributing Reasoning |
| CV-QUANT-005 | Deduction from the explicit project | check quality and performance together. | 54 words at entry; finite assumptions and measurement criteria | reference note and controlled format | Minor | Attributing Reasoning |

### reference note and flashcards claims

- Confirmed: PTQ after training with representative data; QAT simulates effects during training. The reference note does not regain a universal superiority of QAT.
- Specified formula: full affine quantification with terminals and contractual rounding; ONNX QuantizeLinear-21 explicit saturation and nearest-even. The FP8 remains a separate representation.
- Confirmed: ONNX Runtime assigns operators/subgraphs to Execution Providers according to GetCapability; the swap format does not promise a single optimized hardware graph.
- Confirmed: support TensorRT distinguishes between platforms, compatible versions and hardware compatibility modes; no universal portability or universal lack of compatibility is asserted.
- OpenVINO/LiteRT are named as runtimes, but no complete support matrix for these products has been audited. No orders or numerical acceleration announced.
- Diagnostics and quality/cost protocol: project proposals.

## Corrections applied

reference note revised, annotated formula; sources of the five targeted flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: algorithm, understanding, design. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [TensorRT, Quantization Workflows: PTQ/QAT, granularity and Q/DQ](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html).
- [TensorRT, Support Matrix : portability and compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [ONNX QuantizeLinear, version 21, Summary](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21).
- [ONNX Runtime, Execution Providers and GetCapability](https://onnxruntime.ai/docs/execution-providers/).
- [TensorRT, benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation. Pages last viewed on 20 October 2026; their content may change. No runtime environment built.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
