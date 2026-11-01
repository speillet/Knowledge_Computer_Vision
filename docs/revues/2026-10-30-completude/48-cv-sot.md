# Review –  Single-object tracking: correlation, Siamese and MeanShift –  2026-10-30

## Overview

2 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | Deduction/Assumption Cases; Documentary Context Below | Multi-tracking and exclusivity: specifies the existing question | Finished core preserved; 188 → 288 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SOT-002 | Deduction/Assumption Cases; Documentary Context Below | Memory of an update: specifies the existing question | Finished core preserved; 194 → 306 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SOT](../../../vault/110-tracking-association/references/113-tracking-monoobjet.md); [flashcards](../../../vault/110-tracking-association/113-tracking-monoobjet.md). reference note modified before the flashcards.

- **CV-SOT-001 –  Multi-tracking and exclusivity**: Multiple independent single-object trackers can converge on the same distractor, each satisfying its own local maximum. They do not necessarily have a common constraint preventing two IDs from representing the same object. A MOT must also define what new observations create a track and how to avoid duplicates. Launching N copies of an initialized tracker is therefore a possible brick, not a complete resolution of these decisions. In a constructed trial, crossing two similar targets and then introducing a third uninitialized target reveals both association ambiguity, exclusivity and birth management.

- **CV-SOT-002 –  Memory of an update**: For an interpolated model $m_t=(1-\eta)m_{t-1}+\eta\hat m_t$, the contribution of an erroneous observation then persists with a $\eta(1-\eta)^k$ factor after $k$ correct updates, in this simplified scheme. A large $\eta$ adapts quickly but integrates more the first error; a small $\eta$ protects better and follows less quickly a legitimate change. This formula describes an interpolation model, not all tracker variants. Examining regions that are actually learned and freezing rules can test for contamination; a fixed template can still be wrong on a distractor without following that wrong learning loop.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Bertinetto et al, SiamFC](https://arxiv.org/html/1606.09549v2) –  §4, unupdated template and built confusions; interpolation and multi-target cases. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
