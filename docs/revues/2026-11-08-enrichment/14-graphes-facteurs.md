# Review — Factor graphs and incremental optimization — 2026-11-08

## Overview

5 cards reviewed in `approfondir` mode: 5 enriched and 0
retained because their existing explanations already cover the proposed addition.
Highest severity before correction: 0 blocking, 2 important, 0 minor, 3 no defect identified.
Self-review: Agent Codex (`revue-cartes`). Editorial status: `redige`.

## Findings by card

| Card | Accuracy: claim checked | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Independent factors require independent evidence: supported mechanism; additional case is a project deduction | separating representation and solver. | 3 recall criteria; 318 → 396 lexical words | ID/front preserved; canonical wording aligned | Important | Restore landmarks in the factor-graph variable definition; Developed independent factors require independent evidence |
| CV-FACTEURS-002 | A disconnected graph needs more than one anchor: supported mechanism; additional case is a project deduction | Explain a gauge. | 2 recall criteria; 294 → 375 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a disconnected graph needs more than one anchor |
| CV-FACTEURS-003 | A loop can win its own residual test: supported mechanism; additional case is a project deduction | Check for a loop closure. | 3 recall criteria; 313 → 395 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a loop can win its own residual test |
| CV-FACTEURS-004 | Convergence speed is a measured tradeoff: supported mechanism; additional case is a project deduction | Choose a robust back-end to fake loops. | 3 recall criteria; 300 → 390 lexical words | ID/front preserved; canonical wording aligned | Important | Restrict the empirical DCS speed comparison to its measured setting; Developed convergence speed is a measured tradeoff |
| CV-FACTEURS-005 | Not reverified: detailed iSAM2 update rules; source-passage requests timed out. New workload case is project reasoning | explain the incremental update of iSAM2. | 3 recall criteria; 308 → 387 lexical words | ID/front preserved; canonical wording aligned | No defect identified | Developed a small update can still be globally expensive |

## Reference findings and applied corrections

Canonical revision 9 → 10; status and provenance preserved.
New reasoning appears in the canonical reference before its dependent cards.
The review does not establish exhaustive subject coverage.

- CV-FACTEURS-001: Restore landmarks in the factor-graph variable definition.
- CV-FACTEURS-004: Restrict the empirical DCS speed comparison to its measured setting.

Detailed iSAM2 passage access failed after the initial PDF extraction. The unchanged relinearization rules retain their historical citation, with a not-reverified verdict in this pass. New graph workload cases are project reasoning, not a measured iSAM2 runtime.

## Sources

- [Kaess et al., iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf) — abstract accessible; follow-up requests for detailed §§3–4 timed out; historical iSAM2 update claims not freshly reverified. Accessed or attempted 2026-11-08, with failures qualified explicitly.
- [Agarwal et al., DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) — §IV dynamic covariance scaling; experimental convergence is dataset-specific. Accessed or attempted 2026-11-08, with failures qualified explicitly.

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
