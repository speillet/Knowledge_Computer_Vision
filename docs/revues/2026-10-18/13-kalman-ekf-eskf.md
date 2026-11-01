# Review –  Kalman, EKF, UKF and ESKF for merger –  2026-10-18

## Overview

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 2 large, 2 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

Self-review: Agent Codex (`revue-cartes`). The editorial status remains `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | EKF/ESKF confirmed and specified; UKF unverifiable | distinguish filter variants. | Finished core; 77 words | reference note and format | Important | Explicit recovery, separate source UKF |
| CV-FUSION-002 | Confirmed: NIS Eq.7 | interpret a standardized innovation. | Finished core; 55 words | reference note and format | Important | Symbols and source added |
| CV-FUSION-003 | Confirmed: reset covariance Eq.286 | preserve the covariance ESKF. | Finished core; 50 words | reference note and format | Minor | Section specified |
| CV-FUSION-004 | Confirmed: propagation in Δt; diagnosis deduced | Processing time and missing data. | Finished core; 53 words | reference note and format | Minor | Specified passages |

### reference note and flashcards claims

Confirmed: ESKF steps, covariance reset, propagation with time pitch; innovation covariance and weighting. Fixed: ESKF is not exclusive to EKF. Unverifiable in the primary text searchable: detail of sigma-points UKF. Delay/bias/correlation diagnostics are the reasonings of the project. The variation of R must be included in a fixed model, not as a component-by-component universal order.

## Corrections applied

reference note revision 2, flashcards 001 – 004: targeted sources; 001 distinguishes the axes of comparison; 002 defines the symbols and corrects "innovation". No goals or IDs changed.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| check Consistency NIS and residuals biased | Evaluate covariance, beyond the low residual | Evaluation; a flashcard | 3 criteria; duration to be measured | Gamse et al., §§2.2.2 and 3.4 |

## Sources

- [Solà, §§5.2 and 6.1 – 6.3](https://arxiv.org/pdf/1711.02508): nominal/error status, correction and reset. §5.4/Annex E: discretization.
- [Gamse et al. 2014, §2.2.2, equations 5 – 7](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/): innovation and score without unit.
- [Julier and Uhlmann 2004, Unscented Filtering and Nonlinear Estimation](https://doi.org/10.1109/JPROC.2003.823141): only summary available; IEEE access blocked and PDF copies 1997/2004 unavailable. Do not consider the UKF mechanism as confirmed by Solà.

## Checks and limitations

Reference checks: 52 reference notes, 224 flashcards, 34 passed tests. Controls after modification and retention of identifiers are recorded in the [bilan commun](../2026-10-20/00-bilan.md). Context7 unavailable: direct access to official documentation when necessary.

Real export Anki, rendering Obsidian/AnkiDroid, mastery of the learner and independent scientific validation not verified. Scenarios and diagnostic recommendations are reasonings of the project, unless explicitly assigned. Absent families alone do not justify new flashcards.
