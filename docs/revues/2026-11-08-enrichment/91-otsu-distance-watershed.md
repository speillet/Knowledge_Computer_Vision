# Review — Otsu, distance transforms and watershed — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 2 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | A histogram has no knowledge of where defects lie: supported foundation; new case is a project deduction | interpret the Otsu objective. | 2 recall criteria; 281 → 355 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore Otsu objective rather than an optical lens in the expected answer; Developed a histogram has no knowledge of where defects lie |
| CV-WATERSHED-002 | Markers encode the intended number of basins: supported foundation; new case is a project deduction | Rebuild the marker pipeline. | 3 recall criteria; 271 → 346 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed markers encode the intended number of basins |
| CV-WATERSHED-003 | Labels must retain signed integer semantics: supported foundation; new case is a project deduction | distinguish background and unknown. | 2 recall criteria; 296 → 374 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed labels must retain signed integer semantics |
| CV-WATERSHED-004 | More markers can trade merges for splits: supported foundation; new case is a project deduction | Locate a sub-segmentation. | 2 recall criteria; 284 → 362 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed more markers can trade merges for splits |
| CV-WATERSHED-005 | Perfect foreground overlap can have the wrong count: supported foundation; new case is a project deduction | Choose a classic instance metric. | 2 recall criteria; 267 → 338 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore foreground as the union being evaluated; Developed perfect foreground overlap can have the wrong count |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-WATERSHED-001: Restore Otsu objective rather than an optical lens in the expected answer.
- CV-WATERSHED-005: Restore foreground as the union being evaluated.



## Sources

- [OpenCV watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html) — distance-transform markers, unknown regions and output boundaries; checked with Context7. Consulted 2026-11-08.
- [OpenCV Otsu](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) — within-class variance criterion. Consulted 2026-11-08.

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
