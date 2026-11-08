# Review — Line-scan imaging, remote sensing and medical volumes — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | A voxel step is not a fixed distance: supported foundation; new case is a project deduction | propagate units of a volume. | 2 recall criteria; 299 → 380 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a voxel step is not a fixed distance |
| CV-IMAGERIES-002 | Speed changes alter geometry at fixed line rate: supported foundation; new case is a project deduction | check is a line-scan acquisition. | 2 recall criteria; 298 → 376 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed speed changes alter geometry at fixed line rate |
| CV-IMAGERIES-003 | A deployment question determines the split: supported foundation; new case is a project deduction | Avoid a geographical flight. | 2 recall criteria; 292 → 366 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a deployment question determines the split |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The NIfTI qform/sform documentation returned HTTP 403 during this pass. The physical-coordinate claim was checked against the accessible DICOM image-plane specification; no new NIfTI API claim is made.

## Sources

- [DICOM image plane](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) — Image Position, Image Orientation and Pixel Spacing. Consulted 2026-11-08.
- [Basler line scan](https://docs.baslerweb.com/line-scan-gige-use-cases) — Use Case 1b encoder-controlled line triggering. Consulted 2026-11-08.

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
