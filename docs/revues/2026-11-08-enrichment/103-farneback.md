# Review — Farnebäck — dense optical flow through polynomial expansion — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FARNEBACK-001 | Constant terms provide a consistency check: supported foundation; new case is a project deduction | Explain the polynomial mechanism. | 3 recall criteria; 299 → 374 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed constant terms provide a consistency check |
| CV-FARNEBACK-002 | The equation is sensitive to coefficient scale and rank: supported foundation; new case is a project deduction | Solve an ideal local constraint. | 2 recall criteria; 302 → 380 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the equation is sensitive to coefficient scale and rank |
| CV-FARNEBACK-003 | Image array indices and vector components have different order: supported foundation; new case is a project deduction | read the coordinate frame and the units of the stream. | 3 recall criteria; 299 → 379 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed image array indices and vector components have different order |
| CV-FARNEBACK-004 | Composing flows requires transporting the lookup point: supported foundation; new case is a project deduction | interpret a round-trip inconsistency. | 2 recall criteria; 329 → 408 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed composing flows requires transporting the lookup point |
| CV-FARNEBACK-005 | Coarse scales can mix motions across a thin object: supported foundation; new case is a project deduction | Adjust the pyramid without masking the failures. | 2 recall criteria; 306 → 385 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed coarse scales can mix motions across a thin object |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The original Farnebäck PDF was accessible in this pass and §§2–3 were consulted; see the [source-access log](61-source-access.md). The polynomial identities in this pass are explicit project derivations, not claimed execution of Farnebäck or OpenCV.

## Sources

- [OpenCV dense flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) — Dense Optical Flow: polynomial neighborhood approximation; original Farnebäck equations are checked algebraically here. Consulted 2026-11-08.

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
