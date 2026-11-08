# Review — Biometric recognition, ArcFace and PAD — 2026-11-08

## Overview

2 cards reviewed in `approfondir` mode: 2 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 2 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BIOMETRIE-001 | Identity similarity and presentation validity can disagree: supported mechanism; additional case is a project deduction | Distinguish between identity and presentation. | 2 recall criteria; 263 → 341 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed identity similarity and presentation validity can disagree |
| CV-BIOMETRIE-002 | Low prevalence changes the fraction of accepted errors: supported mechanism; additional case is a project deduction | Choose an operating point. | 2 recall criteria; 278 → 358 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed low prevalence changes the fraction of accepted errors |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.


The ArcFace PDF exceeded the browsing tool size limit; its accessible arXiv HTML was used instead. The prevalence calculation is a constructed probability model, not a measured biometric deployment result.

## Sources

- [ArcFace](https://arxiv.org/html/1801.07698v4) — §III-A normalized identity embeddings and angular margin. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [NIST FRTE 1:1](https://pages.nist.gov/frvt/html/frvt11.html) — verification operating points, FMR and FNMR. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
