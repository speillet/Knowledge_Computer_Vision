# Review — Otsu, distance transforms and watershed — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 4 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 2 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | A histogram has no knowledge of where defects lie: supported mechanism; additional case is a project deduction | interpret the Otsu objective. | 2 recall criteria; 281 → 355 lexical words | ID/front preserved; canonical wording aligned | Important | Restore Otsu objective rather than an optical lens in the expected answer; Developed a histogram has no knowledge of where defects lie |
| CV-WATERSHED-002 | Markers encode the intended number of basins: supported mechanism; additional case is a project deduction | Rebuild the marker pipeline. | 3 recall criteria; 271 → 346 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed markers encode the intended number of basins |
| CV-WATERSHED-003 | Labels must retain signed integer semantics: supported mechanism; additional case is a project deduction | distinguish background and unknown. | 2 recall criteria; 296 → 374 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed labels must retain signed integer semantics |
| CV-WATERSHED-004 | More markers can trade merges for splits: supported mechanism; additional case is a project deduction | Locate a sub-segmentation. | 2 recall criteria; 284 → 362 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed more markers can trade merges for splits |
| CV-WATERSHED-005 | Perfect foreground overlap can have the wrong count: retained explanation sufficient for this extension | Choose a classic instance metric. | 2 recall criteria; 267 → 266 lexical words | ID/front preserved; canonical wording aligned | Important | Restore foreground as the union being evaluated; Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-WATERSHED-001: Restore Otsu objective rather than an optical lens in the expected answer.
- CV-WATERSHED-005: Restore foreground as the union being evaluated.



## Sources

- [OpenCV watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html) — distance-transform markers, unknown regions and output boundaries; checked with Context7. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [OpenCV Otsu](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) — within-class variance criterion. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
