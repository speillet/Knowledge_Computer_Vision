# Review — SuperPoint, LightGlue and LoFTR — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Unmatched points are a necessary output: supported foundation; new case is a project deduction | Assign the role of components. | 2 recall criteria; 271 → 345 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed unmatched points are a necessary output |
| CV-MATCH-APPRIS-002 | Detector-free does not mean confidence-free: supported foundation; new case is a project deduction | Distinguish between detector-free and dense flow. | 2 recall criteria; 278 → 353 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed detector-free does not mean confidence-free |
| CV-MATCH-APPRIS-003 | Coordinate metadata is part of feature compatibility: supported foundation; new case is a project deduction | Keep the features compatible. | 2 recall criteria; 283 → 360 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed coordinate metadata is part of feature compatibility |
| CV-MATCH-APPRIS-004 | Adaptive computation needs latency distributions: supported foundation; new case is a project deduction | Build a comparable baseline. | 3 recall criteria; 286 → 360 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed adaptive computation needs latency distributions |
| CV-MATCH-APPRIS-005 | One landmark gives a preprocessing round trip: supported foundation; new case is a project deduction | check the coordinates of the matching. | 2 recall criteria; 294 → 366 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed one landmark gives a preprocessing round trip |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The LoFTR HTML endpoint returned 404; its arXiv PDF was accessible and used instead. No new checkpoint API or runtime result is asserted.

## Sources

- [LightGlue](https://arxiv.org/html/2306.13643v1) — §3 contextual matching, matchability, adaptive depth/width. Consulted 2026-11-08.
- [SuperPoint](https://arxiv.org/html/1712.07629v4) — §3 joint detection/description and §5 homographic adaptation. Consulted 2026-11-08.
- [LoFTR](https://arxiv.org/pdf/2104.00680) — §3 coarse-to-fine correspondence pipeline. Consulted 2026-11-08.

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
