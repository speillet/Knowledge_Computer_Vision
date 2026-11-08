# Review — NeRF, 3D Gaussian Splatting and reconstruction — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 3 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Anisotropy changes primitive support, not object identity: supported mechanism; additional case is a project deduction | Implicit and primitive representation. | 2 recall criteria; 282 → 358 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed anisotropy changes primitive support, not object identity |
| CV-RENDU3D-002 | View synthesis can hide a scale gauge: supported mechanism; additional case is a project deduction | separating rendering and geometry. | 2 recall criteria; 259 → 336 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed view synthesis can hide a scale gauge |
| CV-RENDU3D-003 | Holdout viewpoint distance is part of the test: supported mechanism; additional case is a project deduction | Check out a little-observed scene. | 2 recall criteria; 273 → 353 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed holdout viewpoint distance is part of the test |

## Reference findings and applied corrections

Canonical revision 5 → 6; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [NeRF](https://arxiv.org/html/2003.08934v2) — §§3–4 position/direction-conditioned radiance and volume rendering. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [3D Gaussian Splatting](https://arxiv.org/html/2308.04079v1) — §§4–6 anisotropic primitives, density control and rasterization. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
