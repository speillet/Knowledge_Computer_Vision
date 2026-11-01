# English migration pre-merge review — 2026-11-01

## Result

The Standards and Spec reviews identified translation defects that structural
tests could not detect. Corrections restore mathematical and computer vision
terminology, assumptions, transformation frames, instructions and gradable
expected answers. This pass covers 49 affected subjects and increments
44 canonical revisions. No pedagogical ID is added or removed.

Key corrections: adjoint, conditioning, eigenvectors, relinearization, overlap,
greedy selection, recall, joints, logits, EER, queues and pruning; stationary
versus moving sequences; flat-patch response; gripper→base input; positive-definite
covariance; joint box scaling; delayed-measurement warning and SORT time step.
Specifications again require separately sourced claims and explicit value ranges.
The stable Rappel template and 00-Accueil.md path are restored in instructions.

## Standards review

The original findings concerned technical meaning, geometry, recall criteria,
compatibility instructions and English prose. A focused recheck confirmed the
main corrections and mathematical preservation; its remaining terminology
occurrences were corrected afterward. No code refactor was required.

## Spec review

The original findings concerned lost technical meaning, qualifications and an
API input, altered requirement wording and untranslated visible prose. A focused
recheck confirmed the main fixes; the remaining overlap-score, sparse-detector,
higher-scoring-box and training-assignment wording was then corrected. No scope
creep was identified.

## Integration

The latest main change, PR #24, is retained: default answer deepening, audit-only
mode, proposal decisions, report conventions, Anki GUIDs, package conversion and
answer-length inventory checks. Four regression tests exercise that integration.

## Subject reports

| Subject | Report | Revision |
| --- | --- | --- |
| CV-SVD | [11-moindres-carres-svd.md](11-moindres-carres-svd.md) | 7 → 8 |
| CV-SE3 | [12-rotations-se3.md](12-rotations-se3.md) | 8 → 9 |
| CV-FUSION | [13-kalman-ekf-eskf.md](13-kalman-ekf-eskf.md) | 8 → 8 |
| CV-FACTEURS | [14-graphes-facteurs.md](14-graphes-facteurs.md) | 8 → 9 |
| CV-VIDEO | [102-points-actions-video.md](102-points-actions-video.md) | 6 → 7 |
| CV-FARNEBACK | [103-farneback.md](103-farneback.md) | 4 → 5 |
| CV-SORT | [111-sort.md](111-sort.md) | 6 → 7 |
| CV-CORRELATION | [114-mosse-kcf.md](114-mosse-kcf.md) | 4 → 4 |
| CV-MEANSHIFT | [115-meanshift-camshift.md](115-meanshift-camshift.md) | 4 → 5 |
| CV-DIFFUSION | [122-generation-restauration.md](122-generation-restauration.md) | 5 → 6 |
| CV-IOU-AP | [131-iou-ap-coco.md](131-iou-ap-coco.md) | 6 → 7 |
| CV-FIABILITE | [133-donnees-generalisation.md](133-donnees-generalisation.md) | 5 → 6 |
| CV-PIPELINE | [141-contrats-profiling-video.md](141-contrats-profiling-video.md) | 5 → 6 |
| CV-QUANT | [142-quantification-runtimes.md](142-quantification-runtimes.md) | 5 → 5 |
| CV-DEPLOIEMENT | [143-edge-reproductibilite.md](143-edge-reproductibilite.md) | 6 → 7 |
| CV-ACQUISITION | [21-exposition-bruit-echantillonnage.md](21-exposition-bruit-echantillonnage.md) | 8 → 9 |
| CV-IMAGERIES | [23-imageries-specialisees.md](23-imageries-specialisees.md) | 5 → 6 |
| CV-CAPTEURS | [22-capteurs-horodatage.md](22-capteurs-horodatage.md) | 5 → 6 |
| CV-CANNY-HOUGH | [32-canny-hough.md](32-canny-hough.md) | 5 → 6 |
| CV-MORPHO | [33-morphologie-composantes.md](33-morphologie-composantes.md) | 5 → 6 |
| CV-FILTRES | [31-filtrage-gradients.md](31-filtrage-gradients.md) | 5 → 6 |
| CV-SIFT | [41-sift.md](41-sift.md) | 6 → 7 |
| CV-ORB | [42-orb.md](42-orb.md) | 6 → 7 |
| CV-MATCHING | [43-detecteurs-matchers.md](43-detecteurs-matchers.md) | 5 → 6 |
| CV-MATCH-APPRIS | [44-superpoint-lightglue-loftr.md](44-superpoint-lightglue-loftr.md) | 5 → 6 |
| CV-CORNERS | [46-harris-shi-tomasi.md](46-harris-shi-tomasi.md) | 4 → 5 |
| CV-FAST-BRIEF | [47-fast-brief.md](47-fast-brief.md) | 4 → 4 |
| CV-FLANN | [48-flann.md](48-flann.md) | 4 → 5 |
| CV-HOMOGRAPHIE | [51-ransac-homographie.md](51-ransac-homographie.md) | 6 → 7 |
| CV-ZHANG | [52-calibration-zhang.md](52-calibration-zhang.md) | 6 → 7 |
| CV-EPIPOLAIRE | [53-epipolaire-pnp-triangulation.md](53-epipolaire-pnp-triangulation.md) | 5 → 6 |
| CV-BA | [54-bundle-adjustment.md](54-bundle-adjustment.md) | 5 → 6 |
| CV-MULTICALIB | [55-calibration-multicapteurs.md](55-calibration-multicapteurs.md) | 5 → 6 |
| CV-FISHEYE | [56-calibration-fisheye.md](56-calibration-fisheye.md) | 4 → 5 |
| CV-HANDEYE | [57-calibration-hand-eye.md](57-calibration-hand-eye.md) | 4 → 5 |
| CV-STEREO | [61-stereo-profondeur.md](61-stereo-profondeur.md) | 5 → 5 |
| CV-ICP | [62-recalage-global-icp.md](62-recalage-global-icp.md) | 5 → 6 |
| CV-VIO | [63-slam-vio.md](63-slam-vio.md) | 5 → 6 |
| CV-REPRESENTATIONS | [71-representations-transfert.md](71-representations-transfert.md) | 5 → 6 |
| CV-CLIP | [72-clip-siglip.md](72-clip-siglip.md) | 5 → 6 |
| CV-ANOMALIES | [73-patchcore-padim.md](73-patchcore-padim.md) | 5 → 6 |
| CV-OCR | [74-ocr-documents.md](74-ocr-documents.md) | 5 → 6 |
| CV-BIOMETRIE | [75-embeddings-biometrie.md](75-embeddings-biometrie.md) | 5 → 6 |
| CV-NMS | [81-nms.md](81-nms.md) | 7 → 8 |
| CV-DETECTEURS | [82-detection-fasterrcnn-yolo-detr.md](82-detection-fasterrcnn-yolo-detr.md) | 8 → 9 |
| CV-OPENVOC | [83-detection-open-vocabulary.md](83-detection-open-vocabulary.md) | 5 → 6 |
| CV-POSE3D | [84-detection-pose-3d.md](84-detection-pose-3d.md) | 5 → 6 |
| CV-SEGMENTATION | [93-semantique-instances-panoptique.md](93-semantique-instances-panoptique.md) | 5 → 6 |
| CV-SAM | [94-sam-sam2.md](94-sam-sam2.md) | 5 → 6 |

## Validation and limits

Validation results are recorded in [validation.json](validation.json): 62 tests,
282 cards, 60 references, 14 decks and 3,135 local links pass. French-to-English
package update preserves all note IDs and the three reviewed cards' history;
a second import creates no duplicates. Standard content and style updates also pass. The
original migration record remains dated 2026-10-31 and describes the earlier
58-test state; this pass includes four additional integration tests. Reference
revision changes are recorded in [revisions.json](revisions.json).

The review compares translation against the original French material and retains
existing scientific sources. It is not a complete native-speaker proofread or a
new independent scientific audit. Actual AnkiDroid rendering and phone reimport
remain untested. Local packages are validation artifacts, not published releases.
