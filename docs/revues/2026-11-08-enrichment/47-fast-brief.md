# Review — FAST and BRIEF — detecting corners and describing their neighborhoods — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 5 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 0 important, 0 minor, 5 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FAST-BRIEF-001 | The segment must wrap around the circle: supported mechanism; additional case is a project deduction | Explain the FAST test. | 2 recall criteria; 313 → 388 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed the segment must wrap around the circle |
| CV-FAST-BRIEF-002 | Hamming distance is invariant to a shared bit permutation: supported mechanism; additional case is a project deduction | Calculate a binary distance. | 2 recall criteria; 293 → 362 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed hamming distance is invariant to a shared bit permutation |
| CV-FAST-BRIEF-003 | An oriented pattern has its own failure source: supported mechanism; additional case is a project deduction | separate FAST BRIEF and ORB. | 3 recall criteria; 294 → 369 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed an oriented pattern has its own failure source |
| CV-FAST-BRIEF-004 | Rotation near a boundary changes valid support: supported mechanism; additional case is a project deduction | Isolate a failure under rotation. | 2 recall criteria; 313 → 383 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed rotation near a boundary changes valid support |
| CV-FAST-BRIEF-005 | A faster front end can make geometry slower: supported mechanism; additional case is a project deduction | measure the compromis calculation repeatability. | 3 recall criteria; 296 → 371 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a faster front end can make geometry slower |

## Reference findings and applied corrections

Canonical revision 4 → 5; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.




## Sources

- [Rosten and Drummond](https://www.edwardrosten.com/work/rosten_2006_machine.pdf) — segment test, learned decision tree and repeatability evaluation. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Calonder et al., BRIEF](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf) — §3 smoothed intensity tests and Hamming matching. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
