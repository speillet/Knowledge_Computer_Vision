# Review –  DeepSORT, ByteTrack and multiobject association –  2026-10-20

## Overview

4 flashcards audited. Confirmed mechanisms; attribution and sources specified. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 0 large, 4 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | Confirmed; source specified | Identify the addition of DeepSORT. | 44 words at the entrance; Goal retained | reference note and controlled format | Minor | Cibler source |
| CV-ASSOCIATION-002 | Confirmed; source specified | understand the use of low scores ByteTrack. | 62 words at the entrance; Goal retained | reference note and controlled format | Minor | Cibler source |
| CV-ASSOCIATION-003 | Conditional deduction of the project | check the transfer ReID. | 48 words at entry; check precise domain | reference note and controlled format | Minor | Assign diagnostic |
| CV-ASSOCIATION-004 | Project Protocol | separate detector and association. | 49 words at entry; variables to fix finite | reference note and controlled format | Minor | Quote Detector Effect |

### reference note and flashcards claims

- Confirmed: DeepSORT uses motion distance, gating Mahalanobis, smaller distance cosine to memory and cascade favoring the tracks views recently. The reference note does not claim that all these distances are probabilities.
- Confirmed: ByteTrack Algorithm 1 first associates strong detections, then weak to the remaining tracks; the new tracks comes from strong not associated.
- Confirmed: AB3DMOT combines detections 3D, Kalman 3D and Hungarian (summary/introduction); the need for conventions 3D follows.
- Transfer to industrial parts is a hypothesis to be tested, not a measure of paper. The impossibility of distinguishing objects by an identical appearance is conditioned by this information alone.
- SORT table 1 demonstrates that changing the detector changes the result of the tracker; the proposed controlled protocol is consistent.

## Corrections applied

reference note revised, bibliography completed for the effect of the detector; sources of the four targeted flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| Explain the priority of the DeepSORT waterfall | The flashcard 001 names the waterfall without recalling its mechanism | algorithm | 1 flashcard; priority to recently observed tracks | DeepSORT §2.2 Listing 1 |

Absent families: understanding, design, practice, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [DeepSORT, §§2.1 – 2.3, equation 3 and Listing 1](https://arxiv.org/abs/1703.07402).
- [ByteTrack, §3 Algorithm 1 and creation paragraph](https://arxiv.org/abs/2110.06864).
- [AB3DMOT, summary and introduction](https://arxiv.org/abs/2008.08063).
- [SORT, §3.1 and table 1](https://arxiv.org/abs/1602.00763).

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
