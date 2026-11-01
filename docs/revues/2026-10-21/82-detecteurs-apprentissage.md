# Review –  Detectors: learning and FPN –  2026-10-21

## Overview

Five new flashcards audited and added after explicit agreement of the learner: CV-DETECTEURS-006 to 010. No blocking, significant or minor defects remaining on these additions. The reference note changes from the revision 2 to 3, retained `redige` status. The five previous flashcards remain unchanged; their audit remains in the [previous report](../2026-10-20/82-detection-fasterrcnn-yolo-detr.md).

The earlier conclusion "No Priority Addition" was too limited for the senior objective: assignment, targets, loss and multi-scale merger deserve a clean reminder. This new decision completes the dated report without rewriting it. The two equally accepted diagnostic flashcards will be dealt with in the following passage. No assertion of completeness.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-006 | Confirmed: FCOS §§3.1 – 3.2 | Rebuild assignment without anchors | 105 words on verso; eligibility, arbitration and target; optional variant details | Distance ranges, not just area; specified version | No defects remaining noted | Ajouter |
| CV-DETECTEURS-007 | Equation 1 confirmed; calculation redone | Applying a Box Encoding | 84 words; four expected values, optional decoding | Continuous coordinates and explicit input pixels | No defects remaining noted | Ajouter |
| CV-DETECTEURS-008 | Equation 5 and role of confirmed parameters | Explain the imbalance in dense detection | 117 words; factor and effect suffice, optional full formula | Probability of the correct label, including a negative | No defects remaining noted | Ajouter |
| CV-DETECTEURS-009 | Plate IoU and penalty confirmed; calculation redone | Linking geometry and regression signal | 131 words; kernel mechanism, optional numerical example | Axis-aligned all-encompassing rectangle; no universal warranty | No defects remaining noted | Ajouter |
| CV-DETECTEURS-010 | §3 and figure 3 confirmed | Understanding the features useful to small objects | 103 words; two contributions to distinguish, details of optional convolutions | Do not confuse pyramid of features and images | No defects remaining noted | Ajouter |

The versoes are more developed than the 40 to 82 words of the previous flashcards. The calculation of GIoU remains in the further explanation: it is not required to successfully recall the mechanism. Unmeasured load and duration of revision. The design family remains absent: no artificial flashcard added to fill this category.

## Corrections applied

- [Reference note](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md): assignment FCOS, coordinate convention, Focal Loss, GIoU and FPN developed before the writing of the flashcards. Digital cases are assigned to the project.
- [Flashcards](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md): Five new lenses, IDs 006 to 010, no synchronization identifier invented.
- Current accounts, index and navigation by recalculated poles: 52 reference notes, 229 flashcards. Log: one line per add accepted, export "Unsynchronized".
- Cross-sectional search FCOS/Focal/GIoU/FPN/anchor-free in the vault: no contradictory or duplicate core of these five objectives identified.

## Proposed enrichments (pending agreement)

No new proposals pending agreement. The seven proposed flashcards have been accepted; this delivery achieves the five flashcards on learning. The decomposition of errors, annotations and the case of small objects remain to be carried out in the second passage already authorized.

## Sources

Primary passages actually consulted the 2026-10-21:

- [FCOS v5, §§3.1 – 3.3](https://arxiv.org/html/1904.01355v5): equation 1, choice of smaller area box after level filtering, distinction with center sampling variants.
- [Focal Loss v2, §2 and §§3.1 – 3.2](https://arxiv.org/html/1708.02002v2): difficulty versus class weighting, equations 3 – 5; this is not a robust loss to outliers.
- [GIoU v2, §3.1 and algorithms 1 – 2](https://arxiv.org/html/1902.09630v2): rectangular envelope, tray without covering. The flashcard does not extend ownership to a convergence guarantee.
- [FPN v2, §3 and figure 3](https://arxiv.org/html/1612.03144v2): Descending semantic input and lateral localization.

The articles were viewed on arXiv in pinned versions; no central passage inaccessible. No library APIs introduced or executed. The numerical examples are synthetic derivations, not published measurements.

## Checks and limitations

- `python3 scripts/check_vault.py`: OK, 125 Markdown, 52 reference notes and 229 flashcards.
- `python3 -m unittest discover -s tests`: 34 tests passed.
- `python3 scripts/sync_catalog.py --check`: 18 up to date documents.
- Complete inventory compared to pre-enrichment: five expected additions, no missing ID or modified Anki identity; objectives and tags of the 224 flashcards preserved. The comparator reports the additions, which are expected.
- Temporary Python calculations with exact fractions: distances (20,20,50,40), exact decoding; factors 1/100 and 81/100; losses GIoU 6/5 then 10/9. No network executed.
- Diff, local links, check characters and retention of verified dated evidence sections. The remaining occurrences of 224 describe the history or comparison reference.

Self-reviewed by Agent Codex (`revue-cartes`). Export Anki real, rendered Obsidian/AnkiDroid, independent scientific validation and mastery of the learner remain unverified. The old parser tests do not constitute an export validation of the new flashcards.
