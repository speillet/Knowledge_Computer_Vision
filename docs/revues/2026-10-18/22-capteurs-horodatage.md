# Review –  Sensors, rolling shutter and synchronization –  2026-10-18

## Overview

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 3 large, 1 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

Self-review: Agent Codex (`revue-cartes`). The editorial status remains `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | Confirmed: instants per line | separate exhibition and reading rolling shutter. | Finished core; 47 words | reference note and format | Minor | Explained Basler Version |
| CV-CAPTEURS-002 | Confirmed by calculation: 0,10 m | estimate a spatial time lag. | Finished core; 42 words | reference note and format | Important (attribution) | Calculation of the project |
| CV-CAPTEURS-003 | Conditional diagnosis; substantiated deskew | Calibration and time. | Finished core; 87 words | reference note and format | Important (source) | Source LOAM |
| CV-CAPTEURS-004 | Confirmed: relative radial velocity | interpret the output of sensors. | Finished core; 49 words | reference note and format | Important (source) | Dedicated radar source |

### reference note and flashcards claims

Confirmed: rolling shutter ≠ exposure time; radial velocity distinct from vector 3D; motion during a scan. Calculation executed: 2×0,050=0,10 m. Extrinsic/time diagnosis and transformation of covariances are deductions from the measurement model, without sensor benchmarks.

## Corrections applied

reference note revision 2; targeted sources of the four flashcards; no changes to objectives or IDs.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Building a Time Error Budget | Link precision, speed and drift of clocks | Design; a flashcard | 3 criteria; duration to be measured | LOAM §§III – V, Basler shutter; calculation of the project |

## Sources

- [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter).
- [Zhang and Singh 2014, LOAM, §§II and V, motion distortion correction](https://www.roboticsproceedings.org/rss10/p07.pdf): distortion of scans and compensation by movement; reading PDF.
- [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf): radial velocity and ego movement.
- [Forster, pre-integration](https://dellaert.github.io/files/Forster16tro.pdf) open; does not justify radar claims.

## Checks and limitations

Reference checks: 52 reference notes, 224 flashcards, 34 passed tests. Controls after modification and retention of identifiers are recorded in the [bilan commun](../2026-10-20/00-bilan.md). Context7 unavailable: direct access to official documentation when necessary.

Real export Anki, rendering Obsidian/AnkiDroid, mastery of the learner and independent scientific validation not verified. Scenarios and diagnostic recommendations are reasonings of the project, unless explicitly assigned. Absent families alone do not justify new flashcards.

The flashcard 003 contains 85 words and five case criteria in addition to the core: its actual load remains to be measured; these criteria serve the same diagnosis, without requiring a new flashcard.
