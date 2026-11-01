# Review –  SLAM, VIO, pre-integration IMU and loopback –  2026-10-20

## Overview

5 flashcards audited. 0 blocking, 0 important; 1 minor shared (definitions and references). Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

5 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 0 minor, 5 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Confirmed: relative constraints and bias | situate the preintegration. | 52 words at the entrance; unique role | reference note and controlled format | None | Keep; Targeted source |
| CV-VIO-002 | Confirmed: revisit factor; risk deducted | distinguish odometry and loop. | 54 words at input; function and limit | reference note and controlled format | None | Keep; Targeted source |
| CV-VIO-003 | Confirmed: 4 DoF gauge separate from the scale | Identify the VIO gauges. | 64 words at the entrance; two distinguished ambiguities | reference note and controlled format | None | Keep; Targeted source |
| CV-VIO-004 | Proposed Design Case | design a VIO for augmented reality. | 82 words at input; large but consistent core; duration to be measured | reference note and controlled format | None | Keep; Targeted source |
| CV-VIO-005 | Proposed diagnosis | Diagnose a drift in the corridor. | 86 words at the entrance; causes to be separated; no forced single solution | reference note and controlled format | None | Keep; Targeted source |

### reference note and flashcards claims

Definitions of Δv/Δp conform to world states and R body→world; units added. Forster deals with covariance and correction of bias, not a complete system obtained by a single integration. Zhang – Scaramuzza confirms the group to four degrees of freedom of the inertial case. MSCKF/WINE-MONO/OKVIS are only mentioned: their variants are not audited here. DBoW2/NetVLAD are not detailed; their role of proposing places remains to be documented by their in-depth articles.

## Corrections applied

reference note revision 2; symbols and sources of the five flashcards specified.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Distinguish First Order Corrected Bias and Reintegration | Practical Limit of Preintegration | Reasoning | One flashcard, three criteria; duration to be measured | Forster, VI-C and Appendix B |

Absent families: algorithm, evaluation, practice. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [Forster et al., §§V – VI, equations 31 – 34 and VI-C](https://dellaert.github.io/files/Forster16tro.pdf)
- [Zhang – Scaramuzza 2018, §III and Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf)
- [GTSAM, §4.1 Loop Closure Constraints, Viewed on 2026-10-20](https://gtsam.org/tutorials/intro.html)

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
