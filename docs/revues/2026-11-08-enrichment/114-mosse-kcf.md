# Review — MOSSE and KCF — tracking with correlation filters — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORRELATION-001 | A search crop defines the capture region: supported foundation; new case is a project deduction | Explain the loop of a tracking filter. | 3 recall criteria; 296 → 372 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a search crop defines the capture region |
| CV-CORRELATION-002 | Cyclic training creates artificial boundary examples: supported foundation; new case is a project deduction | distinguish MOSSE and KCF. | 3 recall criteria; 302 → 378 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed cyclic training creates artificial boundary examples |
| CV-CORRELATION-003 | PSR is invariant to some response rescalings: supported foundation; new case is a project deduction | interpret a PSR. | 2 recall criteria; 323 → 400 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed psr is invariant to some response rescalings |
| CV-CORRELATION-004 | A learned distractor can make confidence self-reinforcing: supported foundation; new case is a project deduction | Look for contamination of the model. | 3 recall criteria; 279 → 351 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed a learned distractor can make confidence self-reinforcing |
| CV-CORRELATION-005 | Resets inject new localization information: supported foundation; new case is a project deduction | Define an honest comparison of trackers. | 3 recall criteria; 285 → 354 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed resets inject new localization information |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The first MOSSE author-site URL returned HTTP 403. The draper-hosted author copy was accessible and used; see the [source-access log](61-source-access.md).

## Sources

- [KCF](https://arxiv.org/html/1404.7584v1) — §IV circulant ridge regression and Appendix F MOSSE. Consulted 2026-11-08.
- [MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) — §§3.2–3.5 filter adaptation and PSR. Consulted 2026-11-08.

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
