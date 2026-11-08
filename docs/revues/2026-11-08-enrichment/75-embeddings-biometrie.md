# Review — Biometric recognition, ArcFace and PAD — 2026-11-08

## Overview

2 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 2 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BIOMETRIE-001 | Identity similarity and presentation validity can disagree: supported foundation; new case is a project deduction | Distinguish between identity and presentation. | 2 recall criteria; 263 → 341 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed identity similarity and presentation validity can disagree |
| CV-BIOMETRIE-002 | Low prevalence changes the fraction of accepted errors: supported foundation; new case is a project deduction | Choose an operating point. | 2 recall criteria; 278 → 358 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed low prevalence changes the fraction of accepted errors |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.

The ArcFace PDF exceeded the browsing tool size limit; its accessible arXiv HTML was used instead. The prevalence calculation is a constructed probability model, not a measured biometric deployment result.

## Sources

- [ArcFace](https://arxiv.org/html/1801.07698v4) — §III-A normalized identity embeddings and angular margin. Consulted 2026-11-08.
- [NIST FRTE 1:1](https://pages.nist.gov/frvt/html/frvt11.html) — verification operating points, FMR and FNMR. Consulted 2026-11-08.

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
