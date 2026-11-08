# Existing-card enrichment — overview — 2026-11-08

## Result

All **282 existing cards** were reviewed: **235 enriched** with
question-specific reasoning and **47 retained** because their existing explanations
already cover the proposed extension. All 60 references were checked for
alignment; **58 revisions increase once**, while two already complete subjects
(single-object tracking and GrabCut) retain their original content and revision.
All keep `statut: redige`. The final additions contribute **17,997 lexical words** to
answers, with the finite recall core separate from optional development. Length
is an editorial signal, not proof of relevance or correctness.

No card is added or removed. All IDs, derived Anki GUIDs, legacy synchronization
comments, questions, objectives, families, provenance, tags and target decks
are preserved. Eleven expected answers receive sourced corrections; the other
271 remain unchanged. This is agent self-review, not independent validation.

| Highest severity per card before correction | Cards |
| --- | ---: |
| Blocking | 0 |
| Important | 11 |
| Minor | 0 |
| No defect identified | 271 |
| Total | 282 |

## Main corrections

- **CV-SVD-004**: Qualify outlier residual signatures and stabilization; contamination can be coherent and filtering can worsen coverage. See [CV-SVD](11-moindres-carres-svd.md).
- **CV-FACTEURS-001**: Restore landmarks in the factor-graph variable definition. See [CV-FACTEURS](14-graphes-facteurs.md).
- **CV-FACTEURS-004**: Restrict the empirical DCS speed comparison to its measured setting. See [CV-FACTEURS](14-graphes-facteurs.md).
- **CV-CANNY-HOUGH-002**: Restore the geometric meaning of Hough voting after mistranslation. See [CV-CANNY-HOUGH](32-canny-hough.md).
- **CV-CANNY-HOUGH-002**: Specify the origin and sign of the Hough distance. See [CV-CANNY-HOUGH](32-canny-hough.md).
- **CV-SIFT-006**: Restore the geometric meaning of inlier count. See [CV-SIFT](41-sift.md).
- **CV-FLANN-004**: Restore inliers as the final geometric matching measure. See [CV-FLANN](48-flann.md).
- **CV-DETECTEURS-004**: Restore the missing before/after coverage condition in the small-object diagnosis. See [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md).
- **CV-DETECTEURS-011**: Use the TIDE duplicate-error category instead of a mistranslated label. See [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md).
- **CV-WATERSHED-001**: Restore Otsu objective rather than an optical lens in the expected answer. See [CV-WATERSHED](91-otsu-distance-watershed.md).
- **CV-WATERSHED-005**: Restore foreground as the union being evaluated. See [CV-WATERSHED](91-otsu-distance-watershed.md).
- **CV-IOU-AP-004**: Restore recall and precision as the quantities used in AP101. See [CV-IOU-AP](131-iou-ap-coco.md).

The developments remain useful to senior engineering because they connect a
mechanism to a constrained decision or a discriminating check: singular-vector
sensitivity, physical units and timing, detector/descriptor/geometry contracts,
calibration observability, visibility and identity, metric denominators and
aggregation, and deployment resource limits. Constructed examples and proposed
experiments are identified explicitly; no new empirical model result is claimed.

## Answer depth

| Lexical words per answer | Before | After |
| --- | ---: | ---: |
| Minimum | 253 | 263 |
| Median | 295 | 366.5 |
| Maximum | 406 | 490 |

The [pre-merge review](65-pre-merge-review.md) removed redundant draft additions.
The recall core is still sufficient for grading; the expanded explanations do
not require verbatim recitation. Existing cards already contained substantial
material, so additions target another mechanism, boundary case or decision
rather than replacing those explanations with summaries.

## Proposals awaiting decisions

The four existing proposals remain useful and **pending** in the
[register](../propositions.md); this request to improve existing cards does not
create new IDs or resolve those decisions.

| Priority | Proposal | Purpose | Additional review cost |
| --- | --- | --- | --- |
| 1 | P-CV-FUSION-01 | Distinguish NIS consistency from small or biased innovations | 1 evaluation card |
| 2 | P-CV-SE3-01 | Recall covariance transport with the SE(3) adjoint explicitly | 1 reasoning card |
| 3 | P-CV-SEGMENTATION-01 | Work through PQ matching and TP/FP/FN numerically | 1 evaluation card |
| 4 | P-CV-METRIQUES-TEMPS-01 | Calculate IDF1 consequences on a short sequence | 1 reasoning card |

No additional proposal duplicates these objectives. The learner may accept,
reject or defer each; no decision is inferred from silence. The existing
119 curriculum further-study items remain open. Improving every present card
does not establish exhaustive coverage of computer vision.

## Checks performed

| Executed check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 vault Markdown files, 60 references, 282 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: prerequisite order and answer-depth checks; minimum 263 words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` and comparison with starting inventory | 282 cards, no format/conversion/depth anomalies; no identity changes |
| Protected fields and canonical metadata comparison | All invariants pass; 58 changed references incremented once; 2 retained |
| `python3 docs/revues/2026-11-08-enrichment/62-numerical-checks.py` | 59 arithmetic checks pass |
| Local Markdown-link audit | 2,440 local links checked; no missing file or heading |
| `git diff --check` | No whitespace errors |

Detailed evidence: [protected-field comparison](63-invariants.json),
[reproducible numerical checks](62-numerical-checks.py),
[numerical results](62-numerical-results.json),
[source access and fallbacks](61-source-access.md), and
[local-link audit](64-link-checks.json).

## Subject reports

| Subject | Cards | Reference revision | Report |
| --- | ---: | --- | --- |
| CV-SVD | 9 | 8 → 9 | [11-moindres-carres-svd](11-moindres-carres-svd.md) |
| CV-SE3 | 6 | 9 → 10 | [12-rotations-se3](12-rotations-se3.md) |
| CV-FUSION | 6 | 8 → 9 | [13-kalman-ekf-eskf](13-kalman-ekf-eskf.md) |
| CV-FACTEURS | 5 | 9 → 10 | [14-graphes-facteurs](14-graphes-facteurs.md) |
| CV-ACQUISITION | 4 | 9 → 10 | [21-exposition-bruit-echantillonnage](21-exposition-bruit-echantillonnage.md) |
| CV-CAPTEURS | 4 | 6 → 7 | [22-capteurs-horodatage](22-capteurs-horodatage.md) |
| CV-IMAGERIES | 3 | 6 → 7 | [23-imageries-specialisees](23-imageries-specialisees.md) |
| CV-FILTRES | 4 | 6 → 7 | [31-filtrage-gradients](31-filtrage-gradients.md) |
| CV-CANNY-HOUGH | 4 | 6 → 7 | [32-canny-hough](32-canny-hough.md) |
| CV-MORPHO | 3 | 6 → 7 | [33-morphologie-composantes](33-morphologie-composantes.md) |
| CV-SIFT | 7 | 7 → 8 | [41-sift](41-sift.md) |
| CV-ORB | 6 | 7 → 8 | [42-orb](42-orb.md) |
| CV-MATCHING | 4 | 6 → 7 | [43-detecteurs-matchers](43-detecteurs-matchers.md) |
| CV-MATCH-APPRIS | 5 | 6 → 7 | [44-superpoint-lightglue-loftr](44-superpoint-lightglue-loftr.md) |
| CV-ECC | 3 | 5 → 6 | [45-recalage-ecc](45-recalage-ecc.md) |
| CV-CORNERS | 5 | 5 → 6 | [46-harris-shi-tomasi](46-harris-shi-tomasi.md) |
| CV-FAST-BRIEF | 5 | 4 → 5 | [47-fast-brief](47-fast-brief.md) |
| CV-FLANN | 4 | 5 → 6 | [48-flann](48-flann.md) |
| CV-HOMOGRAPHIE | 7 | 7 → 8 | [51-ransac-homographie](51-ransac-homographie.md) |
| CV-ZHANG | 7 | 7 → 8 | [52-calibration-zhang](52-calibration-zhang.md) |
| CV-EPIPOLAIRE | 5 | 6 → 7 | [53-epipolaire-pnp-triangulation](53-epipolaire-pnp-triangulation.md) |
| CV-BA | 4 | 6 → 7 | [54-bundle-adjustment](54-bundle-adjustment.md) |
| CV-MULTICALIB | 3 | 6 → 7 | [55-calibration-multicapteurs](55-calibration-multicapteurs.md) |
| CV-FISHEYE | 5 | 5 → 6 | [56-calibration-fisheye](56-calibration-fisheye.md) |
| CV-HANDEYE | 5 | 5 → 6 | [57-calibration-hand-eye](57-calibration-hand-eye.md) |
| CV-STEREO | 4 | 5 → 6 | [61-stereo-profondeur](61-stereo-profondeur.md) |
| CV-ICP | 5 | 6 → 7 | [62-recalage-global-icp](62-recalage-global-icp.md) |
| CV-VIO | 5 | 6 → 7 | [63-slam-vio](63-slam-vio.md) |
| CV-BEV | 5 | 5 → 6 | [64-nuages-bev-occupation](64-nuages-bev-occupation.md) |
| CV-REPRESENTATIONS | 5 | 6 → 7 | [71-representations-transfert](71-representations-transfert.md) |
| CV-CLIP | 4 | 6 → 7 | [72-clip-siglip](72-clip-siglip.md) |
| CV-ANOMALIES | 4 | 6 → 7 | [73-patchcore-padim](73-patchcore-padim.md) |
| CV-OCR | 3 | 6 → 7 | [74-ocr-documents](74-ocr-documents.md) |
| CV-BIOMETRIE | 2 | 6 → 7 | [75-embeddings-biometrie](75-embeddings-biometrie.md) |
| CV-NMS | 6 | 8 → 9 | [81-nms](81-nms.md) |
| CV-DETECTEURS | 13 | 9 → 10 | [82-detection-fasterrcnn-yolo-detr](82-detection-fasterrcnn-yolo-detr.md) |
| CV-OPENVOC | 3 | 6 → 7 | [83-detection-open-vocabulary](83-detection-open-vocabulary.md) |
| CV-POSE3D | 4 | 6 → 7 | [84-detection-pose-3d](84-detection-pose-3d.md) |
| CV-WATERSHED | 5 | 4 → 5 | [91-otsu-distance-watershed](91-otsu-distance-watershed.md) |
| CV-GRABCUT | 3 | 4 → 4 | [92-grabcut-regions](92-grabcut-regions.md) |
| CV-SEGMENTATION | 4 | 6 → 7 | [93-semantique-instances-panoptique](93-semantique-instances-panoptique.md) |
| CV-SAM | 3 | 6 → 7 | [94-sam-sam2](94-sam-sam2.md) |
| CV-FLOT | 4 | 4 → 5 | [101-flot-optique](101-flot-optique.md) |
| CV-VIDEO | 4 | 7 → 8 | [102-points-actions-video](102-points-actions-video.md) |
| CV-FARNEBACK | 5 | 5 → 6 | [103-farneback](103-farneback.md) |
| CV-SORT | 8 | 7 → 8 | [111-sort](111-sort.md) |
| CV-ASSOCIATION | 4 | 5 → 6 | [112-deepsort-bytetrack](112-deepsort-bytetrack.md) |
| CV-SOT | 2 | 5 → 5 | [113-tracking-monoobjet](113-tracking-monoobjet.md) |
| CV-CORRELATION | 5 | 4 → 5 | [114-mosse-kcf](114-mosse-kcf.md) |
| CV-MEANSHIFT | 4 | 5 → 6 | [115-meanshift-camshift](115-meanshift-camshift.md) |
| CV-VLM | 4 | 5 → 6 | [121-vlm-grounding](121-vlm-grounding.md) |
| CV-DIFFUSION | 3 | 6 → 7 | [122-generation-restauration](122-generation-restauration.md) |
| CV-RENDU3D | 3 | 5 → 6 | [123-nerf-gaussian-splatting](123-nerf-gaussian-splatting.md) |
| CV-IOU-AP | 7 | 7 → 8 | [131-iou-ap-coco](131-iou-ap-coco.md) |
| CV-METRIQUES-TEMPS | 5 | 5 → 6 | [132-tracking-trajectoires](132-tracking-trajectoires.md) |
| CV-FIABILITE | 5 | 6 → 7 | [133-donnees-generalisation](133-donnees-generalisation.md) |
| CV-METRIQUES-APPLIQUEES | 4 | 5 → 6 | [134-metriques-applications](134-metriques-applications.md) |
| CV-PIPELINE | 5 | 6 → 7 | [141-contrats-profiling-video](141-contrats-profiling-video.md) |
| CV-QUANT | 5 | 5 → 6 | [142-quantification-runtimes](142-quantification-runtimes.md) |
| CV-DEPLOIEMENT | 4 | 7 → 8 | [143-edge-reproductibilite](143-edge-reproductibilite.md) |

## Limitations and export status

Source verification concerns the named mechanisms, corrections and added
boundary cases. It is not a fresh passage-by-passage verification of every
retained historical sentence or implementation claim. Source failures and
fallbacks are recorded rather than silently treated as confirmations.

No independent scientific review, learner mastery, image/video experiment,
hardware benchmark, Obsidian display test or AnkiDroid import is established.
The arithmetic script evaluates constructed numbers only. Validators and unit
tests do not measure pedagogical value or application rendering.

No Anki package is rebuilt or published in this content pass. Corrected content
reaches the phone through a new package: **to republish with `paquet-anki`**,
then check import/update and rendering on the learner's device. Existing dated
export evidence remains historical. The requested delivery is a reviewed
content commit through a PR and merge; an Anki release is a separate operation.
