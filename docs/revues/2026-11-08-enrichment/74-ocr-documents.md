# Review — OCR and document understanding — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode; all receive question-specific
reasoning. Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | Field association can fail with perfect characters: supported foundation; new case is a project deduction | Separate recognition and structure. | 2 recall criteria; 281 → 360 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed field association can fail with perfect characters |
| CV-OCR-002 | Micro and macro CER answer different questions: supported foundation; new case is a project deduction | Interpreting CER. | 2 recall criteria; 284 → 359 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed micro and macro cer answer different questions |
| CV-OCR-003 | Layout errors need region and order annotations: supported foundation; new case is a project deduction | locate a reading order defect. | 2 recall criteria; 263 → 341 lexical words | Canonical explanation aligned; ID and front preserved | No defect identified | Developed layout errors need region and order annotations |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
Each new calculation, assumption and boundary case appears in the reference
before the corresponding card. The additions follow the existing objectives
and do not establish coverage of the whole subject.



## Sources

- [OCR-D evaluation](https://ocr-d.de/en/spec/ocrd_eval.html) — Text Evaluation, Levenshtein alignment, normalization and CER/WER. Consulted 2026-11-08.

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
