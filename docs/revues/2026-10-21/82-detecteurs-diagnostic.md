# Review –  Detectors: diagnostics and small objects –  2026-10-21

## Overview

Three flashcards audited: two additions accepted (CV-DETECTEURS-011 and 012) and enrichment of CV-DETECTEURS-004. A minor observation of cases too abstract treated; no blocking defect or important observation. Goal, ID and tags of 004 retained. reference note in revision 4, status `redige`.

This passage completes the seven approved additions, after the five flashcards of the [First Passage](82-detecteurs-apprentissage.md). The subject has 12 flashcards, the vault 231. The reference note also describes a controlled experiment on resolution, explicitly not executed. No comprehensive detection coverage or independent validation announced.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-004 | Recalculated geometry; suppression mechanism confirmed in Soft-NMS §4 | Objective of diagnosis after retained resize | 82 words before, 180 after; three kernel checks, values and case NMS in further explanation | coordinate frame, ratio, padding and explicit steps; no causal generalization | Minor: abstract initial case | Specify scenario and verifications |
| CV-DETECTEURS-011 | Three categories confirmed by TIDE §2.2 | Differentiate between FPs that require different controls | 100 words; three independent cases, one GT each, no border case | Thresholds given, ignore/crowd excluded; six families developed in the reference note | No defects found | Ajouter |
| CV-DETECTEURS-012 | Omission and ambiguities documented by TIDE §3.4 and appendices D – E | Avoid attributing any error to the model | 124 words; check policy and image then conditionally conclude | High score distinct from proof; correction protocol assigned to the project | No defects found | Ajouter |

004 has the longest verso of the subject; calculations remain optional to successfully recall the diagnosis. The actual load is to be observed with the learner, without imposing an arbitrary ceiling. The other nine flashcards of the subject are unchanged and are not the subject of a new self-review here.

## Corrections applied

- [Reference note](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) enriched before flashcards: six TIDE families, effects of scores and limits of oracles; missing, ambiguous or ignored annotations; case resize/padding/NMS; controlled factor experiment with baseline, prediction, measurements and limits.
- [Flashcards](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md): add 011 – 012 and specify 004 without changing its lens. No synchronization identity invented.
- The diagnostic tracks, the annotation correction protocol and the proposed experiment are decisions of the project, separated from the results of the articles.
- Updated accounts and navigation: 52 reference notes and 231 flashcards. Journal: two additions, one enriched case and one protocol, each plotted; dated evidence preserved.
- Consistency verified with the reference notes NMS and IoU/AP: score threshold, NMS threshold and separate evaluation threshold; matching and crowd/ignore rules of the protocol retained. Table TIDE does not replace the COCO assessor.

## Proposed enrichments (pending agreement)

No additional proposals pending. The seven accepted flashcards, the case of small objects and the implementation protocol are written. The execution of this protocol on a checkpoint and annotated images remains a learning activity to be carried out, with no result manufactured.

## Sources

Passes actually consulted the 2026-10-21:

- [TIDE v2, §2.2](https://arxiv.org/html/2008.08115v2): six categories, thresholds, duplicates and importance of rank by score.
- Same article, §2.3 and appendix A.1: oracles from the same baseline and general non-additivity; these idealized interventions do not guarantee the effect of a model modification.
- Same article, §3.4 and appendices D – E: errors and ambiguities of annotations, flags crowd, effect of ignored detections on the diagnosis. The percentages of their study are not generalized to the dataset of the project.
- [Soft-NMS, §4](https://arxiv.org/html/1704.04503): A better localized box can be removed by a higher-scoring box; the calculations of the case are those of the project. Equalitys at thresholds are avoided, in accordance with the distinction documented in reference note NMS.
- [FPN v2, §3](https://arxiv.org/html/1612.03144v2), consulted on the first passage of the same day: roles of the fine and deep features, without guarantee of recall.

No central passage inaccessible. No new library APIs or TIDE implementations introduced; these are the mechanisms described in the articles.

## Checks and limitations

- `python3 scripts/check_vault.py`: OK, 125 Markdown, 52 reference notes and 231 flashcards.
- `python3 -m unittest discover -s tests`: 34 tests passed.
- `python3 scripts/sync_catalog.py --check`: 18 up to date documents.
- Comparative inventory before/after this passage: only 011 and 012 added. Global comparison to the 224 flashcards reference: seven accepted additions, no deleted IDs and modified Anki identity; existing objectives and tags retained.
- Calculations with exact fractions in temporary Python: factor 1/3, padding 140, transformed box (300,290,304,293), exact round trip, size 4×3. IoU(P,Q) = IoU(Q,G) = 5/11, greater than 0,4 and less than 0,5; recall 1→0 in the only case built.
- Complete diff, local links, tables, check characters and audited accounts; sections of previous evidence, including those of the first passage, retained. The old totals that remain are historical or serve as a comparison reference.

Self-reviewed by Agent Codex (`revue-cartes`). Real export Anki, rendering Obsidian/AnkiDroid, training or benchmark, control, recall load and independent scientific validation not performed. Analytical calculations are not worth experimenting with on images.
