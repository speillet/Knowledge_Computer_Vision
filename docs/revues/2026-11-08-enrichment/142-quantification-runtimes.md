# Review — PTQ, QAT, INT8/FP8 and runtimes — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Fake quantization and actual execution have different contracts: supported mechanism; additional case is a project deduction | distinguish PTQ and QAT. | 2 recall criteria; 282 → 353 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed fake quantization and actual execution have different contracts |
| CV-QUANT-002 | Outliers trade range against resolution: supported mechanism; additional case is a project deduction | interpret scale and saturation. | 2 recall criteria; 306 → 382 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed outliers trade range against resolution |
| CV-QUANT-003 | Portable representation is not portable performance: retained explanation sufficient for this extension | Check the support of a runtime. | 3 recall criteria; 275 → 275 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-QUANT-004 | Amdahl bounds the useful acceleration: supported mechanism; additional case is a project deduction | diagnose an absence of gain INT8. | 3 recall criteria; 292 → 366 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed amdahl bounds the useful acceleration |
| CV-QUANT-005 | Near-threshold decisions can change after tiny perturbations: retained explanation sufficient for this extension | check quality and performance together. | 3 recall criteria; 276 → 276 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [ONNX Runtime quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html) — static calibration, QDQ representation and quantization debugging; Context7 checked. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [ONNX QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21) — scale, zero point, rounding and saturation. Accessed or attempted 2026-11-08, with failures qualified explicitly.

## Proposals

No new ID is created. See the [proposal register](../propositions.md) and
[overview](00-bilan.md) for the four existing pending decisions.

## Checks and limitations

Scope-wide checks and protected-field comparisons appear in the [overview](00-bilan.md).
The evidence concerns the named mechanisms and corrections, not every retained
historical sentence or implementation claim. [Pre-merge review](65-pre-merge-review.md)
removed redundant draft additions and corrected two new wording inaccuracies.
This is agent self-review, without independent scientific validation, learner
mastery, a new CV experiment or AnkiDroid rendering. Export status:
**to republish with `paquet-anki`**.
