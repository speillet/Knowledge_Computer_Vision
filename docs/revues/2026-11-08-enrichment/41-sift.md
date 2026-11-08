# Review — SIFT — local features and multiscale descriptors — 2026-11-08

## Overview

7 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 1 important, 0 minor, 6 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SIFT-001 | Match count does not establish spatial support: supported foundation; new case is a project deduction | Explain the components of a correspondence pipeline. | 3 recall criteria; 329 → 410 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed match count does not establish spatial support |
| CV-SIFT-002 | Scale sampling and octave boundaries: supported foundation; new case is a project deduction | Explain the search for a characteristic scale. | 2 recall criteria; 338 → 421 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed scale sampling and octave boundaries |
| CV-SIFT-003 | Orientation ambiguity can create multiple descriptors: supported foundation; new case is a project deduction | justify the construction of the descriptor. | 3 recall criteria; 310 → 383 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed orientation ambiguity can create multiple descriptors |
| CV-SIFT-004 | The second neighbor depends on the search population: supported foundation; new case is a project deduction | interpret the ratio test. | 2 recall criteria; 323 → 400 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed the second neighbor depends on the search population |
| CV-SIFT-005 | Viewpoint normalization cannot recover occlusion: supported foundation; new case is a project deduction | Distinguish between the limits of invariances. | 2 recall criteria; 336 → 411 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed viewpoint normalization cannot recover occlusion |
| CV-SIFT-006 | A geometric consensus can support the wrong period: supported foundation; new case is a project deduction | Diagnose a misleading consensus. | 2 recall criteria; 312 → 387 lexical words | Canonical explanation aligned; ID and front preserved | Important | Restore the geometric meaning of inlier count; Developed a geometric consensus can support the wrong period |
| CV-SIFT-007 | Compare refusal as well as successful localization: supported foundation; new case is a project deduction | Build a comparison under constraint. | 3 recall criteria; 312 → 386 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed compare refusal as well as successful localization |

## Reference findings and applied corrections

Canonical revision 7 → 8; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

- CV-SIFT-006: Restore the geometric meaning of inlier count.



## Sources

- [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) — §§3–7 scale-space, localization, orientation, descriptor and matching. Consulted 2026-11-08.

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
