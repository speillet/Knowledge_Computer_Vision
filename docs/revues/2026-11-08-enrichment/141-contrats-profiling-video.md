# Review — Data contracts, profiling and video pipelines — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Freshness has a capture-time denominator: supported foundation; new case is a project deduction | separate latency flow and freshness. | 2 recall criteria; 277 → 345 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed freshness has a capture-time denominator |
| CV-PIPELINE-002 | Buffer capacity buys time, not steady-state capacity: supported foundation; new case is a project deduction | reasoning on a video file. | 2 recall criteria; 275 → 352 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed buffer capacity buys time, not steady-state capacity |
| CV-PIPELINE-003 | Overlapped stages need a dependency trace: supported foundation; new case is a project deduction | Set a complete benchmark. | 2 recall criteria; 284 → 357 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed overlapped stages need a dependency trace |
| CV-PIPELINE-004 | Tail latency should be measured for the whole path: supported foundation; new case is a project deduction | Size eight streams under p99. | 3 recall criteria; 319 → 399 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed tail latency should be measured for the whole path |
| CV-PIPELINE-005 | Utilization alone does not identify the bottleneck: supported foundation; new case is a project deduction | Locate a bottleneck by trace. | 3 recall criteria; 278 → 356 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed utilization alone does not identify the bottleneck |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [GStreamer queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html) — queue limits, blocking, leaky behavior and current levels. Consulted 2026-11-08.
- [TensorRT benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) — scope of latency, throughput and host/device timing; documentation consulted 2026-11-08. Consulted 2026-11-08.

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
