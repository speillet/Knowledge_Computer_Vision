# Review –  NMS: instances, classes and inclusion –  2026-10-21

## Overview

Three flashcards audited: NMS-003 and NMS-005 enriched, NMS-006 added to meet the explicit demand for multiple cases, multiclasses and different sizes. Two minor illustrative findings processed; no blocking or significant defects noted. reference note revision 4; Existing IDs and objectives retained. The other flashcards NMS remain unchanged, with their [Previous Audit](../2026-10-20/81-nms.md).

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-003 | Separation by category confirmed in Torchvision 0.29; outputs deducted from thresholds | Choose the scope of deletion | 101 → 136 words; exits finished and then compromised under contract | Exclusive classes and separate objects; multiple instances remain possible | Minor: abstract comparison | Add IoU, scores and counterexamples |
| CV-NMS-005 | Neighbor loss documented by Soft-NMS; recall effect conditioned to coverage GT | Locate a Disappearance | 110 → 139 words; check before/after unchanged in focus | Same class does not mean same instance; duplicate deleted separate from a lost GT | Minor: case of the same implicit class | Specify two people and cover by GT |
| CV-NMS-006 | Definition IoU confirmed; recalculated 0,04 result | Avoid the false rule “Inclusion ⇒ deletion” | 98 words; a decision justified by intersection/union | Continuous coordinates, explicit scores and class | No defects found | Ajouter |

The backs of the flashcards 003 and 005 are longer; the additional examples are in the further explanation. The actual recall time remains to be observed.

## Corrections applied

[NMS reference](../../../vault/80-detection-pose/references/81-nms.md) completed before [flashcards](../../../vault/80-detection-pose/81-nms.md): table of five situations, global/class difference, inclusion example 100×100/20×20, distinction IoU and intersection divided by small area. The result does not assume the identity of the objects from their boxes.

Documentation `batched_nms` pinned to 0.29 with consultation date; old consultation date of `nms` kept separately. Journal: one line per flashcard affected. Accounts and navigation updated with the following passage on [Classes and Sizes](82-detecteurs-classes-tailles.md).

## Proposed enrichments (pending agreement)

No additional proposals pending. The explicitly requested cases are implemented, with a new flashcard focused on inclusion and two specified existing objectives. No multiplication of flashcards to fill absent families.

## Sources

Passes actually consulted the 2026-10-21:

- [Soft-NMS, §§1, 3 and 4](https://arxiv.org/html/1704.04503): removal of real neighbors, processing by class, score and overlap. No performance gains from the article are attributed to the project cases.
- [Torchvision 0.29, batched_nms, description and settings](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html): no deletion between different categories and strict threshold. Context7 unavailable in this session; direct use of official documentation, without API execution.
- [GIoU v2, §3, equation 1](https://arxiv.org/html/1902.09630v2): definition of IoU whose inclusion area ratio is one derivation of the project.

No central source inaccessible. Object identities and scenario label policies are explicit assumptions, not observations.

## Checks and limitations

Controls common to the two passages of this supplement:

- `python3 scripts/check_vault.py`: OK, 125 Markdown, 52 reference notes, 233 flashcards.
- `python3 -m unittest discover -s tests`: 34 tests passed.
- `python3 scripts/sync_catalog.py --check`: 18 up to date documents.
- Inventory compared to the initial 231 flashcards: only CV-NMS-006 and CV-DETECTEURS-013 are added; no missing ID, lens or existing Anki identity modified. The previous flashcards are intact except for NMS-003 and NMS-005, enriched under their original objectives.
- Temporary calculations in Python, exact fractions: inclusion 1/25; translations 1/3, 19/21, 19/21, 1/3. No network or Torchvision call executed.
- Current accounts, local links and anchors added, tables, characters of check and diff checked. Dated evidence retained. The remaining old totals are historical or comparative references.

Self-reviewed by Agent Codex (`revue-cartes`); status `redige`. Real export, Obsidian/AnkiDroid rendering, benchmark, independent scientific validation, unverified control and recall load. The scenarios and diagnostic recommendations are reasonings of the project.
