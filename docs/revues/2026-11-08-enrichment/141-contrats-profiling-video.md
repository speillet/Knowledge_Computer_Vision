# Review — Data contracts, profiling and video pipelines — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 3 enriched and 2
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Freshness has a capture-time denominator: retained explanation sufficient for this extension | separate latency flow and freshness. | 2 recall criteria; 277 → 277 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-PIPELINE-002 | Buffer capacity buys time, not steady-state capacity: supported mechanism; additional case is a project deduction | reasoning on a video file. | 2 recall criteria; 275 → 352 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed buffer capacity buys time, not steady-state capacity |
| CV-PIPELINE-003 | Overlapped stages need a dependency trace: supported mechanism; additional case is a project deduction | Set a complete benchmark. | 2 recall criteria; 284 → 357 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed overlapped stages need a dependency trace |
| CV-PIPELINE-004 | Tail latency should be measured for the whole path: retained explanation sufficient for this extension | Size eight streams under p99. | 3 recall criteria; 319 → 319 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |
| CV-PIPELINE-005 | Utilization alone does not identify the bottleneck: supported mechanism; additional case is a project deduction | Locate a bottleneck by trace. | 3 recall criteria; 278 → 356 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed utilization alone does not identify the bottleneck |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [GStreamer queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html) — queue limits, blocking, leaky behavior and current levels. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [TensorRT benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) — scope of latency, throughput and host/device timing; documentation consulted 2026-11-08. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
