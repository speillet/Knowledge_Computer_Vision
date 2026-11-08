# Review — Line-scan imaging, remote sensing and medical volumes — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 3 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | A voxel step is not a fixed distance: supported mechanism; additional case is a project deduction | propagate units of a volume. | 2 recall criteria; 299 → 380 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a voxel step is not a fixed distance |
| CV-IMAGERIES-002 | Speed changes alter geometry at fixed line rate: supported mechanism; additional case is a project deduction | check is a line-scan acquisition. | 2 recall criteria; 298 → 376 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed speed changes alter geometry at fixed line rate |
| CV-IMAGERIES-003 | A deployment question determines the split: supported mechanism; additional case is a project deduction | Avoid a geographical flight. | 2 recall criteria; 292 → 366 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a deployment question determines the split |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The NIfTI qform/sform documentation returned HTTP 403 during this pass. The physical-coordinate claim was checked against the accessible DICOM image-plane specification; no new NIfTI API claim is made.

## Sources

- [DICOM image plane](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) — Image Position, Image Orientation and Pixel Spacing. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Basler line scan](https://docs.baslerweb.com/line-scan-gige-use-cases) — Use Case 1b encoder-controlled line triggering. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
