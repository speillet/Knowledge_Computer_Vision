# Review — ORB — detection and oriented binary descriptors — 2026-11-08

## Overview

6 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | Orientation quality can limit binary matching: supported foundation; new case is a project deduction | rebuild the ORB mechanism. | 3 recall criteria; 306 → 382 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed orientation quality can limit binary matching |
| CV-ORB-002 | A byte example exposes the wrong metric: supported foundation; new case is a project deduction | Linking representation and distance. | 2 recall criteria; 314 → 388 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a byte example exposes the wrong metric |
| CV-ORB-003 | One symbol mismatch can contain two flipped bits: supported foundation; new case is a project deduction | select the norm after changing the variant. | 2 recall criteria; 306 → 379 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed one symbol mismatch can contain two flipped bits |
| CV-ORB-004 | Tie handling belongs to the acceptance rule: supported foundation; new case is a project deduction | distinguish between two matching filters. | 3 recall criteria; 314 → 393 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed tie handling belongs to the acceptance rule |
| CV-ORB-005 | A finer pyramid cannot undo the input sampling: supported foundation; new case is a project deduction | Diagnose a loss of repeatability. | 3 recall criteria; 325 → 402 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a finer pyramid cannot undo the input sampling |
| CV-ORB-006 | A memory estimate needs database lifetime: supported foundation; new case is a project deduction | articulating computational constraint and task success. | 3 recall criteria; 302 → 380 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a memory estimate needs database lifetime |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The original Willow Garage ORB PDF was inaccessible. The algorithm and norm contract were checked using the official OpenCV 4.13 documentation; historical paper-specific empirical claims are not re-certified.

## Sources

- [OpenCV ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) — oriented intensity-centroid descriptor and WTA_K norm contract; checked with Context7. Consulted 2026-11-08.

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
