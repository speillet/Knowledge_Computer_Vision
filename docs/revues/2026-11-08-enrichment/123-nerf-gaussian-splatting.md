# Review — NeRF, 3D Gaussian Splatting and reconstruction — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Anisotropy changes primitive support, not object identity: supported foundation; new case is a project deduction | Implicit and primitive representation. | 2 recall criteria; 282 → 358 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed anisotropy changes primitive support, not object identity |
| CV-RENDU3D-002 | View synthesis can hide a scale gauge: supported foundation; new case is a project deduction | separating rendering and geometry. | 2 recall criteria; 259 → 336 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed view synthesis can hide a scale gauge |
| CV-RENDU3D-003 | Holdout viewpoint distance is part of the test: supported foundation; new case is a project deduction | Check out a little-observed scene. | 2 recall criteria; 273 → 353 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed holdout viewpoint distance is part of the test |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [NeRF](https://arxiv.org/html/2003.08934v2) — §§3–4 position/direction-conditioned radiance and volume rendering. Consulted 2026-11-08.
- [3D Gaussian Splatting](https://arxiv.org/html/2308.04079v1) — §§4–6 anisotropic primitives, density control and rasterization. Consulted 2026-11-08.

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
