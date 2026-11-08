# Review — PTQ, QAT, INT8/FP8 and runtimes — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Fake quantization and actual execution have different contracts: supported foundation; new case is a project deduction | distinguish PTQ and QAT. | 2 recall criteria; 282 → 353 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed fake quantization and actual execution have different contracts |
| CV-QUANT-002 | Outliers trade range against resolution: supported foundation; new case is a project deduction | interpret scale and saturation. | 2 recall criteria; 306 → 382 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed outliers trade range against resolution |
| CV-QUANT-003 | Portable representation is not portable performance: supported foundation; new case is a project deduction | Check the support of a runtime. | 3 recall criteria; 275 → 346 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed portable representation is not portable performance |
| CV-QUANT-004 | Amdahl bounds the useful acceleration: supported foundation; new case is a project deduction | diagnose an absence of gain INT8. | 3 recall criteria; 292 → 366 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed amdahl bounds the useful acceleration |
| CV-QUANT-005 | Near-threshold decisions can change after tiny perturbations: supported foundation; new case is a project deduction | check quality and performance together. | 3 recall criteria; 276 → 355 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed near-threshold decisions can change after tiny perturbations |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [ONNX Runtime quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html) — static calibration, QDQ representation and quantization debugging; Context7 checked. Consulted 2026-11-08.
- [ONNX QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21) — scale, zero point, rounding and saturation. Consulted 2026-11-08.

## Proposals

No new ID is created in this pass. See the [proposal register](../propositions.md)
and [overview](00-bilan.md) for pending complementary cards and decisions.

## Checks and limitations

Scope-wide executed checks and identity/field comparisons are recorded in the
[overview](00-bilan.md). The source assessment concerns the mechanisms and
boundary cases identified above; it is not a fresh passage-by-passage
certification of every retained historical paragraph or implementation claim.
No CV experiment, hardware benchmark, independent review, learner mastery or
AnkiDroid rendering is established. Export status: to republish with `paquet-anki`.
