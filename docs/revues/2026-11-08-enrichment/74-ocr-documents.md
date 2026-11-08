# Review — OCR and document understanding — 2026-11-08

## Overview

3 cards reviewed in `approfondir` mode: 2 enriched and 1
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | Field association can fail with perfect characters: supported mechanism; additional case is a project deduction | Separate recognition and structure. | 2 recall criteria; 281 → 360 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed field association can fail with perfect characters |
| CV-OCR-002 | Micro and macro CER answer different questions: supported mechanism; additional case is a project deduction | Interpreting CER. | 2 recall criteria; 284 → 359 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed micro and macro cer answer different questions |
| CV-OCR-003 | Layout errors need region and order annotations: retained explanation sufficient for this extension | locate a reading order defect. | 2 recall criteria; 263 → 263 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Retained; redundant draft addition removed |

## Reference findings and applied corrections

Canonical revision 6 → 7; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [OCR-D evaluation](https://ocr-d.de/en/spec/ocrd_eval.html) — Text Evaluation, Levenshtein alignment, normalization and CER/WER. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
