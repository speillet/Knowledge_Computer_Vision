# Review –  Detectors: instances, classes and sizes –  2026-10-21

## Overview

A new audited and added flashcard, CV-DETECTEURS-013, to meet the demand for multiple detection and multiclass cases. No blocking, significant or minor defects noted on this addition. reference note revision 5: output contract and examples of sizes / aspect ratios developed. The previous twelve flashcards remain unchanged; their audits remain in the [Apprenticeship](82-detecteurs-apprentissage.md) and [diagnosis](82-detecteurs-diagnostic.md) reports, as well as the [rapport initial](../2026-10-20/82-detection-fasterrcnn-yolo-detr.md).

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-013 | Multi-tag distinction confirmed by YOLov3 §2.2; instance case built; scope NMS confirmed | Separate number of objects, categories and labels by object | 129 words; five instances, two classes and one label per instance in the given case | Does not generalize YOLov3 to the whole family; explicit annotation and post-treatment | No defects found | Ajouter |

The choices of supervision and output are not deduced from the only number of classes present in the image. The core is limited to this distinction; the head and NMS details are further study.

## Corrections applied

[Reference note](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) completed before [flashcard](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md): multiple instances of the same class, multiple classes per image, multiple or exclusive labels per instance; references to NMS scenarios.

The geometric field calculates the effect of a two-pixel error on boxes 4×4, 40×40 and 40×4, depending on the axis of displacement. It distinguishes size, aspect ratio and common scale change. This calculation expands the diagnostic recall already present in CV-IOU-AP-006; no new redundant flashcard on the latter objective is added.

reference note NMS and flashcard NMS-006 handle the other case of different sizes: inclusion without strong IoU. The two reference notes refer to each other. Current accounts: 52 reference notes, 233 flashcards, including six NMS and thirteen detectors; recalculated log and navigation. No Anki identifier invented.

## Proposed enrichments (pending agreement)

No additional proposals pending. The supplement requested is written. Scenarios do not claim to cover all annotation architectures or policies. Their empirical interpretation remains to be tested on images.

## Sources

Passes actually consulted the 2026-10-21:

- [YOLov3 v1, §§2.1 – 2.3](https://arxiv.org/html/1804.02767v1): dimension regression, independent logistic classification and multi-scale predictions. The examples of car/bike and vehicle/car are those of the project.
- [GIoU v2, §3, equation 1 and scale property](https://arxiv.org/html/1902.09630v2): the starting point for synthetic calculations. Translation fixed in pixels and common resizing of the two boxes are distinguished.
- [Torchvision 0.29, batched_nms, description](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html): separation of categories, without label exclusivity or constraint of one box per class. Context7 unavailable; official documentation accessed directly.

Cross-sectional search in detection and IoU/AP: the objectives of box format, evaluation duplicates and location sensitivity are already present and remain distinct. No contradictions identified. No central passage inaccessible; no library calls or networks executed.

## Checks and limitations

Controls common to the two passages of this supplement:

- `python3 scripts/check_vault.py`: OK, 125 Markdown, 52 reference notes, 233 flashcards.
- `python3 -m unittest discover -s tests`: 34 tests passed.
- `python3 scripts/sync_catalog.py --check`: 18 up to date documents.
- Inventory compared to the initial 231 flashcards: only CV-NMS-006 and CV-DETECTEURS-013 are added; no missing ID, lens or existing Anki identity modified. The previous flashcards are intact except for NMS-003 and NMS-005, enriched under their original objectives.
- Temporary calculations in Python, exact fractions: inclusion 1/25; translations 1/3, 19/21, 19/21, 1/3. No network or Torchvision call executed.
- Current accounts, local links and anchors added, tables, characters of check and diff checked. Dated evidence retained. The remaining old totals are historical or comparative references.

Self-reviewed by Agent Codex (`revue-cartes`); status `redige`. Real export, Obsidian/AnkiDroid rendering, benchmark, independent scientific validation, unverified control and recall load. The scenarios and diagnostic recommendations are reasonings of the project.
