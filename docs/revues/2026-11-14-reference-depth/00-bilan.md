# Reference-note deepening — overview — 2026-11-14

## Result

All **60 canonical references** were deepened, and their **282 cards** were
reviewed against them. Each reference revision increases once and keeps
`statut: redige`. The body of each reference (front matter excluded, up to
the per-card appendices) grew from 280–2,417 words, median 335, to
1,862–8,654 words, median 3,675. Whole notes grew from 118,599 to 332,545
words. Of the 720 contract sections (12 per reference), 628 were shallow, 43
absent, 28 developed and 21 partly developed or brief before the pass; all
720 are now developed. Length is an editorial signal, not proof of
relevance or correctness.

No card is added or removed. IDs, derived Anki GUIDs, families, provenance,
tags and target decks are preserved. Every card file changed: 154 expected
answers were corrected, almost all to restore meaning lost in the English
migration. 97 `Objective:` lines were retranslated from the pre-migration
French, and 5 questions lost French decimal commas. Two curriculum notes,
`Cas-transfert.md` and the learning-path source behind `Parcours-senior.md`,
also had mistranslations fixed. This is agent self-review by Claude Code,
not independent validation.

| Highest severity per card before correction | Cards |
| --- | ---: |
| Blocking | 0 |
| Important | 38 |
| Minor | 244 |
| No defect identified | 0 |
| Total | 282 |

Every card had at least a language or source defect, which is why no card is
counted as defect-free. No expected answer contained a scientific error that
inverted its recall objective. The important findings are imprecise claims,
missing conditions, unsupported citations and mistranslations that changed
technical meaning.

## What the references now contain

Each body follows the contract of
`specs/001-cv-knowledge-base/learning-design.md`:

- **Problem, data contract and assumptions:** inputs and outputs with shapes,
  types, value ranges, coordinate frames and units, plus observability limits
  and degenerate cases.
- **Procedure and mathematics:** ordered steps, pseudocode, equations with
  every symbol and unit defined, and short derivations.
- **Parameters and properties:** the effect of each parameter, a tuning
  approach, invariances and the limits of guarantees.
- **Cost and implementation:** cost drivers and the contract of a named
  library version, with the places where the code departs from the paper.
- **Evaluation:** protocol, metrics, one baseline and one controlled
  variation (FR-033), all labelled as proposed and not executed.
- **Failure modes:** symptom, possible causes, discriminating check and
  conditional remedy.
- **Alternatives and sources:** conditional choices and industrial uses
  labelled as project reasoning, with scientific and implementation sources
  separated (FR-036).

Every worked number is a constructed example recomputed by
`checks/<subject>.py` (60 stdlib scripts). Sibling notes are linked rather
than restated, for example CV-SOT links CV-CORRELATION and CV-MEANSHIFT.

## Main corrections

The [correction log](../../../vault/01-Parcours/Suivi-pilote.md#reference-note-deepening--2026-11-14)
has one row per substantive correction; each subject report lists every
expected answer changed, with old and new text.

- **Overstated or imprecise claims:** Joseph-form stability (CV-FUSION-006),
  BRIEF rotation behaviour (CV-FAST-BRIEF), FMR/FNMR threshold side
  (CV-BIOMETRIE), strict versus non-strict NMS comparisons in the original
  Soft-NMS code (CV-NMS), the OpenCV hand–eye minimum (CV-MULTICALIB),
  preintegration (CV-VIO-001), the Cauchy–Schwarz equality condition in HOTA
  (CV-METRIQUES-TEMPS-002).
- **Explanations contradicted by code:** a duplicate lowers COCO precision
  rather than raising it (CV-IOU-AP-004); Ceres's trust-region radius update
  (CV-SVD-007).
- **Missing implementation conditions with silent failures:** OpenCV's Tsai
  hand–eye path returns an identity transform without raising
  (CV-HANDEYE-003); `cv::watershed` floods colour differences, not $-D$
  (CV-WATERSHED-002); one-shot `knnMatch` rebuilds the FLANN index on every
  call (CV-FLANN-001); OpenCV FAST `TYPE_7_12` and `TYPE_5_8` reject valid
  arcs (CV-FAST-BRIEF-001); SORT hides a track for three frames after one miss
  (CV-SORT-004).
- **Unsupported citations:** Source lines that cited passages that do not make
  the claim were replaced in CV-ACQUISITION, CV-CAPTEURS, CV-VIO,
  CV-METRIQUES-TEMPS, CV-CORRELATION, CV-SOT and CV-FLOT.
- **Mistranslations that changed meaning:** "radius" for ray (CV-FISHEYE-004,
  CV-RENDU3D), "indoor/outdoor" for inside/outside occupancy (CV-BEV-003),
  "retract" for retrain (CV-IMAGERIES-002, CV-POSE3D-002), "music video" for
  clip (CV-VIDEO-001), "default recall" for defect recall
  (CV-METRIQUES-APPLIQUEES-002), "valeurs propres" lost from an objective
  (CV-CORNERS-001), and an inverted RANSAC sentence (CV-HOMOGRAPHIE-003).

The references also record many documented differences between papers and
OpenCV 4.13.0, torchvision 0.29, Ceres 2.2.0, Open3D 0.19.0, pycocotools,
TrackEval and the official code of SORT, DeepSORT, ByteTrack, PatchCore, SAM
and RAFT. These are implementation facts, not errors in the cards.

## Subjects

Word counts are body words before → after. Cards are those audited; the
important column counts cards whose highest severity was important.

| Reference | Revision | Body words | Cards | Important | Report |
| --- | --- | --- | ---: | ---: | --- |
| CV-SVD | 9 → 10 | 1,728 → 5,113 | 9 | 2 | [11-moindres-carres-svd](11-moindres-carres-svd.md) |
| CV-SE3 | 10 → 11 | 757 → 3,975 | 6 | 1 | [12-rotations-se3](12-rotations-se3.md) |
| CV-FUSION | 9 → 10 | 880 → 3,965 | 6 | 4 | [13-kalman-ekf-eskf](13-kalman-ekf-eskf.md) |
| CV-FACTEURS | 10 → 11 | 835 → 3,626 | 5 | 1 | [14-graphes-facteurs](14-graphes-facteurs.md) |
| CV-ACQUISITION | 10 → 11 | 595 → 4,435 | 4 | 0 | [21-exposition-bruit-echantillonnage](21-exposition-bruit-echantillonnage.md) |
| CV-CAPTEURS | 7 → 8 | 327 → 3,854 | 4 | 0 | [22-capteurs-horodatage](22-capteurs-horodatage.md) |
| CV-IMAGERIES | 7 → 8 | 329 → 3,313 | 3 | 0 | [23-imageries-specialisees](23-imageries-specialisees.md) |
| CV-FILTRES | 7 → 8 | 333 → 3,348 | 4 | 0 | [31-filtrage-gradients](31-filtrage-gradients.md) |
| CV-CANNY-HOUGH | 7 → 8 | 326 → 3,175 | 4 | 0 | [32-canny-hough](32-canny-hough.md) |
| CV-MORPHO | 7 → 8 | 315 → 3,126 | 3 | 0 | [33-morphologie-composantes](33-morphologie-composantes.md) |
| CV-SIFT | 8 → 9 | 847 → 3,957 | 7 | 1 | [41-sift](41-sift.md) |
| CV-ORB | 8 → 9 | 739 → 3,445 | 6 | 0 | [42-orb](42-orb.md) |
| CV-MATCHING | 7 → 8 | 328 → 3,335 | 4 | 0 | [43-detecteurs-matchers](43-detecteurs-matchers.md) |
| CV-MATCH-APPRIS | 7 → 8 | 328 → 5,708 | 5 | 0 | [44-superpoint-lightglue-loftr](44-superpoint-lightglue-loftr.md) |
| CV-ECC | 6 → 7 | 324 → 4,001 | 3 | 0 | [45-recalage-ecc](45-recalage-ecc.md) |
| CV-CORNERS | 6 → 7 | 497 → 4,381 | 5 | 0 | [46-harris-shi-tomasi](46-harris-shi-tomasi.md) |
| CV-FAST-BRIEF | 5 → 6 | 487 → 4,359 | 5 | 2 | [47-fast-brief](47-fast-brief.md) |
| CV-FLANN | 6 → 7 | 417 → 3,041 | 4 | 2 | [48-flann](48-flann.md) |
| CV-HOMOGRAPHIE | 8 → 9 | 818 → 3,684 | 7 | 0 | [51-ransac-homographie](51-ransac-homographie.md) |
| CV-ZHANG | 8 → 9 | 853 → 3,429 | 7 | 0 | [52-calibration-zhang](52-calibration-zhang.md) |
| CV-EPIPOLAIRE | 7 → 8 | 328 → 3,440 | 5 | 0 | [53-epipolaire-pnp-triangulation](53-epipolaire-pnp-triangulation.md) |
| CV-BA | 7 → 8 | 344 → 4,307 | 4 | 0 | [54-bundle-adjustment](54-bundle-adjustment.md) |
| CV-MULTICALIB | 7 → 8 | 343 → 3,289 | 3 | 0 | [55-calibration-multicapteurs](55-calibration-multicapteurs.md) |
| CV-FISHEYE | 6 → 7 | 500 → 3,132 | 5 | 0 | [56-calibration-fisheye](56-calibration-fisheye.md) |
| CV-HANDEYE | 6 → 7 | 502 → 2,674 | 5 | 1 | [57-calibration-hand-eye](57-calibration-hand-eye.md) |
| CV-STEREO | 6 → 7 | 365 → 2,615 | 4 | 0 | [61-stereo-profondeur](61-stereo-profondeur.md) |
| CV-ICP | 7 → 8 | 302 → 4,974 | 5 | 0 | [62-recalage-global-icp](62-recalage-global-icp.md) |
| CV-VIO | 7 → 8 | 343 → 3,973 | 5 | 0 | [63-slam-vio](63-slam-vio.md) |
| CV-BEV | 6 → 7 | 315 → 4,351 | 5 | 0 | [64-nuages-bev-occupation](64-nuages-bev-occupation.md) |
| CV-REPRESENTATIONS | 7 → 8 | 337 → 3,683 | 5 | 0 | [71-representations-transfert](71-representations-transfert.md) |
| CV-CLIP | 7 → 8 | 314 → 3,174 | 4 | 0 | [72-clip-siglip](72-clip-siglip.md) |
| CV-ANOMALIES | 7 → 8 | 326 → 5,171 | 4 | 0 | [73-patchcore-padim](73-patchcore-padim.md) |
| CV-OCR | 7 → 8 | 332 → 4,152 | 3 | 0 | [74-ocr-documents](74-ocr-documents.md) |
| CV-BIOMETRIE | 7 → 8 | 298 → 3,560 | 2 | 0 | [75-embeddings-biometrie](75-embeddings-biometrie.md) |
| CV-NMS | 9 → 10 | 1,237 → 3,942 | 6 | 0 | [81-nms](81-nms.md) |
| CV-DETECTEURS | 10 → 11 | 2,417 → 8,654 | 13 | 0 | [82-detection-fasterrcnn-yolo-detr](82-detection-fasterrcnn-yolo-detr.md) |
| CV-OPENVOC | 7 → 8 | 280 → 4,360 | 3 | 0 | [83-detection-open-vocabulary](83-detection-open-vocabulary.md) |
| CV-POSE3D | 7 → 8 | 305 → 4,207 | 4 | 1 | [84-detection-pose-3d](84-detection-pose-3d.md) |
| CV-WATERSHED | 5 → 6 | 333 → 4,657 | 5 | 1 | [91-otsu-distance-watershed](91-otsu-distance-watershed.md) |
| CV-GRABCUT | 4 → 5 | 292 → 3,895 | 3 | 0 | [92-grabcut-regions](92-grabcut-regions.md) |
| CV-SEGMENTATION | 7 → 8 | 316 → 3,595 | 4 | 0 | [93-semantique-instances-panoptique](93-semantique-instances-panoptique.md) |
| CV-SAM | 7 → 8 | 310 → 3,556 | 3 | 0 | [94-sam-sam2](94-sam-sam2.md) |
| CV-FLOT | 5 → 6 | 331 → 5,027 | 4 | 0 | [101-flot-optique](101-flot-optique.md) |
| CV-VIDEO | 8 → 9 | 321 → 3,354 | 4 | 1 | [102-points-actions-video](102-points-actions-video.md) |
| CV-FARNEBACK | 6 → 7 | 462 → 3,450 | 5 | 0 | [103-farneback](103-farneback.md) |
| CV-SORT | 8 → 9 | 918 → 3,037 | 8 | 2 | [111-sort](111-sort.md) |
| CV-ASSOCIATION | 6 → 7 | 322 → 3,166 | 4 | 1 | [112-deepsort-bytetrack](112-deepsort-bytetrack.md) |
| CV-SOT | 5 → 6 | 330 → 4,753 | 2 | 0 | [113-tracking-monoobjet](113-tracking-monoobjet.md) |
| CV-CORRELATION | 5 → 6 | 492 → 3,472 | 5 | 2 | [114-mosse-kcf](114-mosse-kcf.md) |
| CV-MEANSHIFT | 6 → 7 | 424 → 2,859 | 4 | 1 | [115-meanshift-camshift](115-meanshift-camshift.md) |
| CV-VLM | 6 → 7 | 351 → 2,663 | 4 | 1 | [121-vlm-grounding](121-vlm-grounding.md) |
| CV-DIFFUSION | 7 → 8 | 337 → 2,073 | 3 | 1 | [122-generation-restauration](122-generation-restauration.md) |
| CV-RENDU3D | 6 → 7 | 322 → 1,862 | 3 | 0 | [123-nerf-gaussian-splatting](123-nerf-gaussian-splatting.md) |
| CV-IOU-AP | 8 → 9 | 815 → 4,855 | 7 | 4 | [131-iou-ap-coco](131-iou-ap-coco.md) |
| CV-METRIQUES-TEMPS | 6 → 7 | 345 → 4,673 | 5 | 3 | [132-tracking-trajectoires](132-tracking-trajectoires.md) |
| CV-FIABILITE | 7 → 8 | 319 → 3,652 | 5 | 2 | [133-donnees-generalisation](133-donnees-generalisation.md) |
| CV-METRIQUES-APPLIQUEES | 6 → 7 | 325 → 3,667 | 4 | 1 | [134-metriques-applications](134-metriques-applications.md) |
| CV-PIPELINE | 7 → 8 | 363 → 5,043 | 5 | 2 | [141-contrats-profiling-video](141-contrats-profiling-video.md) |
| CV-QUANT | 6 → 7 | 328 → 4,069 | 5 | 1 | [142-quantification-runtimes](142-quantification-runtimes.md) |
| CV-DEPLOIEMENT | 8 → 9 | 327 → 3,628 | 4 | 0 | [143-edge-reproductibilite](143-edge-reproductibilite.md) |

## Proposals awaiting decisions

The pass registers **106 new-card proposals** as `pending` in the
[register](../propositions.md#review-of-2026-11-14): one or two per subject.
Each tests a mechanism, decision, diagnosis or evaluation that the deepened
reference now explains but no card trains. Adding all of them would increase
the deck from 282 to about 388 cards; accept few. The four earlier proposals
remain pending.

The most useful, in order, favour the learner's priority topics (matching,
calibration, registration, tracking, detection) and silent production
failures:

| Priority | Proposal | Purpose | Review cost |
| ---: | --- | --- | --- |
| 1 | P-CV-ECC-01 | State which frame a `findTransformECC` warp maps from and to, and the effect of omitting `WARP_INVERSE_MAP` | 1 card, 2 criteria |
| 2 | P-CV-PIPELINE-02 | Map a detector box back through a 1920×1080 → 640×640 letterbox and recognize a forgotten padding term | 1 card, 3 criteria |
| 3 | P-CV-MATCHING-02 | Explain why `findHomography` can return a poor model without error (default least squares, iteration cap) | 1 card, 3 criteria |
| 4 | P-CV-EPIPOLAIRE-01 | Diagnose a two-view initialization under pure rotation or a planar scene; test a homography first | 1 card, 3 criteria |
| 5 | P-CV-SORT-01 | Explain why a small fast object never gets a stable SORT identity (zero birth velocity, IoU budget) | 1 card, 3 criteria |
| 6 | P-CV-ICP-02 | Detect degenerate registration from the eigenvalues of the normalized point-to-plane matrix | 1 card, 3 criteria |
| 7 | P-CV-STEREO-01 | Explain what SGM's $P_1$ and $P_2$ penalize and the effect of raising $P_2$ | 1 card, 3 criteria |
| 8 | P-CV-WATERSHED-01 | State which relief `cv::watershed` floods and what follows for the distance-transform pipeline | 1 card, 3 criteria |
| 9 | P-CV-FLANN-01 | Explain why one-shot `knnMatch(query, train, k)` never amortizes the FLANN index | 1 card, 2–3 criteria |
| 10 | P-CV-HANDEYE-01 | Explain why a separable hand–eye solver biases translation and when to refine jointly | 1 card, 3 criteria |
| 11 | P-CV-DETECTEURS-01 | Compute anchor labels and regression targets; explain wrong boxes from mismatched coder weights | 1 card, 3 criteria |
| 12 | P-CV-IOU-AP-01 | Explain why lowering the score threshold cannot lower COCO AP, and what to report for acceptance | 1 card, 3 criteria |

Other decisions reported by the subject reviews, not registered as card
proposals:

- **Questions that hint at their answer:** CV-SOT-002 says the distractor is
  already in the template; CV-MATCH-APPRIS-005 names padding. Proposed
  wording is in the [CV-SOT](113-tracking-monoobjet.md) and
  [CV-MATCH-APPRIS](44-superpoint-lightglue-loftr.md) reports. Questions are
  left unchanged until the learner decides.
- **Overlapping cards:** CV-MATCHING-001 tests the same structure-tensor
  mechanism as CV-CORNERS-001, and CV-MATCHING-002 the same detector/descriptor
  split as CV-FAST-BRIEF-003 ([CV-MATCHING report](43-detecteurs-matchers.md)).
  Retiring a card would remove an Anki note, which has not been tested.

## Objective and question wording

`Objective:` lines are Obsidian metadata and are not exported to Anki. The
English migration had mistranslated many of them, and left three in French.
Each new line translates the French objective at `b7142bb^` and keeps the
same recall objective. The [2026-11-01 translation pass](../2026-11-01-traduction/00-bilan.md)
(commit `5d73d30`) had already corrected objective lines the same way.

<details><summary>97 objective lines: before → after</summary>

| Card | Before | After |
| --- | --- | --- |
| CV-SVD-005 | Make a DLT estimate | Walk through a DLT estimate |
| CV-SVD-006 | linking standardization and conditioning of the DLT | Relate normalization and conditioning of the DLT |
| CV-SVD-007 | Gauss-Newton and Levenberg-Marquardt | Situate Gauss-Newton and Levenberg-Marquardt |
| CV-SE3-001 | deal with named coordinate frames | Compose transforms between named coordinate frames |
| CV-SE3-002 | Reverse a rigid pose | Invert a rigid pose |
| CV-SE3-003 | distinguish between local and global disturbances | Distinguish local and global perturbations |
| CV-SE3-005 | Measuring a rotation gap | Measure a rotation difference |
| CV-FUSION-002 | interpret a standardized innovation | Interpret a normalized innovation |
| CV-FUSION-003 | preserve the covariance ESKF | Preserve the ESKF covariance |
| CV-FUSION-004 | Processing time and missing data | Handle timing and missing data |
| CV-FUSION-005 | justify the formulation at the state of error | Justify the error-state formulation |
| CV-FACTEURS-003 | Check for a loop closure | Verify a loop closure |
| CV-FACTEURS-004 | Choose a robust back-end to fake loops | Choose a back-end robust to false loops |
| CV-FLOT-002 | respect the temporal unity | Respect the time unit |
| CV-FLOT-003 | situer RAFT | Situate RAFT |
| CV-FLOT-004 | process a occlusion | Handle an occlusion |
| CV-VIDEO-003 | check causation and delay | Check causality and delay |
| CV-VIDEO-004 | check the use of the time order | Check the use of temporal order |
| CV-FARNEBACK-003 | read the coordinate frame and the units of the stream | Read the coordinate frame and units of the flow |
| CV-SORT-003 | interpret the weight of a measure | Interpret the weight of a measurement |
| CV-SORT-004 | Distinguish between memory and transmission | Distinguish track memory from output |
| CV-ASSOCIATION-002 | understand the use of low scores ByteTrack | Understand ByteTrack's use of low scores |
| CV-ASSOCIATION-003 | check the transfer ReID | Check ReID transfer |
| CV-VLM-001 | locate encoder VLM and VLA | Situate encoder, VLM and VLA |
| CV-VLM-002 | Locate a visual connector | Situate a visual connector |
| CV-VLM-003 | Create a video index | Design a video index |
| CV-VLM-004 | Distinct hallucination and insufficient observation | Distinguish hallucination from insufficient observation |
| CV-DIFFUSION-001 | separating learning and sampling | Separate training and sampling |
| CV-DIFFUSION-002 | locate the latent diffusion | Situate latent diffusion |
| CV-DIFFUSION-003 | to protect an industrial observation | Protect an industrial observation |
| CV-RENDU3D-001 | Implicit and primitive representation | Distinguish implicit and primitive-based representations |
| CV-RENDU3D-002 | separating rendering and geometry | Separate rendering and geometry |
| CV-RENDU3D-003 | Check out a little-observed scene | Check a poorly observed scene |
| CV-IOU-AP-001 | calculate a overlap in the right contract | Compute an overlap under the right contract |
| CV-IOU-AP-007 | link average benchmark and business decision | Relate a benchmark average to a business decision |
| CV-FIABILITE-005 | Avoiding certainty outside the field | Avoid out-of-domain certainty |
| CV-METRIQUES-APPLIQUEES-001 | Distinguish between border and border | Distinguish overlap and boundary |
| CV-METRIQUES-APPLIQUEES-002 | Measure the small flaws | Measure small defects |
| CV-METRIQUES-APPLIQUEES-004 | Treat the empty masks | Handle empty masks |
| CV-PIPELINE-001 | separate latency flow and freshness | Separate latency, throughput and freshness |
| CV-PIPELINE-002 | reasoning on a video file | Reason about a video queue |
| CV-PIPELINE-003 | Set a complete benchmark | Define a complete benchmark |
| CV-QUANT-004 | diagnose an absence of gain INT8 | Diagnose a missing INT8 gain |
| CV-DEPLOIEMENT-001 | Limiting a system gain | Bound a system gain |
| CV-DEPLOIEMENT-004 | Test the edge | Test sustained edge operation |
| CV-ACQUISITION-004 | check an image entry | Check an image input |
| CV-CAPTEURS-001 | separate exhibition and reading rolling shutter | Separate exposure and readout in a rolling shutter |
| CV-CAPTEURS-003 | Calibration and time | Separate calibration and timing errors |
| CV-IMAGERIES-002 | check is a line-scan acquisition | Check a line-scan acquisition |
| CV-IMAGERIES-003 | Avoid a geographical flight | Avoid geographic leakage |
| CV-FILTRES-002 | settle a bilateral in the right units | Tune a bilateral filter in the right units |
| CV-FILTRES-003 | Protect a business detail | Protect a task-critical detail |
| CV-CANNY-HOUGH-003 | Distinguish between right and segment | Distinguish a line from a segment |
| CV-MORPHO-003 | Explaining a merger of parts | Explain merged parts |
| CV-ECC-003 | Choose a movement model | Choose a motion model |
| CV-HOMOGRAPHIE-002 | Connecting degrees of freedom and degeneration | Relate degrees of freedom and degeneracy |
| CV-HOMOGRAPHIE-005 | interpret the unit of a threshold of residual | Interpret the unit of a residual threshold |
| CV-ZHANG-001 | There are three geometric objectives | Distinguish three geometric objectives |
| CV-ZHANG-005 | Spreading a pixel transformation | Propagate a pixel transformation |
| CV-EPIPOLAIRE-005 | meet the minimum variant of pose | Respect the minimal pose variant |
| CV-BA-002 | Explain the elimination of Schur | Explain Schur elimination |
| CV-BA-004 | check a model too free | Check an overly free model |
| CV-MULTICALIB-001 | Interpreting hand-eye | Interpret hand-eye calibration |
| CV-MULTICALIB-003 | separating intrinsic extrinsic and time | Separate intrinsic, extrinsic and temporal calibration |
| CV-FISHEYE-004 | Propagating the contract after rectification | Propagate the contract after rectification |
| CV-HANDEYE-001 | drift the relative movements | Derive the relative motions |
| CV-HANDEYE-002 | respect the meaning of the poses API | Respect the direction of poses in the API |
| CV-HANDEYE-003 | Exciting the observable directions | Excite the observable directions |
| CV-STEREO-002 | Interpreting the uncertainty of depth | Interpret depth uncertainty |
| CV-BEV-001 | distinguish voxel pillar and BEV | Distinguish voxels, pillars and BEV |
| CV-BEV-003 | Separate the sense of occupation | Separate the meanings of occupancy |
| CV-BEV-004 | check a BEV merge | Check a BEV fusion |
| CV-BEV-005 | Designing a warehouse perception | Design warehouse perception |
| CV-REPRESENTATIONS-002 | Swin and ConvNeXt | Situate Swin and ConvNeXt |
| CV-REPRESENTATIONS-005 | check preprocessing a backbone | Check a backbone's preprocessing |
| CV-CLIP-003 | distinguer objectifs contrastifs | Distinguish contrastive objectives |
| CV-OCR-002 | Interpreting CER | Interpret CER |
| CV-NMS-002 | There are three thresholds | Distinguish three thresholds |
| CV-DETECTEURS-001 | Find the sharing of features | Situate feature sharing |
| CV-DETECTEURS-006 | rebuild site assignment in FCOS | Reconstruct location assignment in FCOS |
| CV-DETECTEURS-009 | explain the signal of GIoU for disjointed boxes | Explain the GIoU signal for disjoint boxes |
| CV-DETECTEURS-011 | Distinguish between class, location, and duplicate errors | Distinguish class, localization and duplicate errors |
| CV-DETECTEURS-013 | distinguish instances, classes, and labels by instance | Distinguish instances, classes and per-instance labels |
| CV-OPENVOC-002 | choose a system with a scalable catalog | Choose a system for an evolving catalog |
| CV-POSE3D-002 | check a box 3D | Check a 3D box |
| CV-WATERSHED-004 | Locate a sub-segmentation | Locate an under-segmentation |
| CV-GRABCUT-002 | check is an initialization constraint | Check an initialization constraint |
| CV-SEGMENTATION-002 | Detecting a bad job definition | Detect a badly defined task |
| CV-SEGMENTATION-003 | Propagating a dense increase | Propagate a dense augmentation |
| CV-SAM-001 | Set the output to SAM | Define the SAM output |
| CV-SAM-002 | Find SAM 2 on video | Situate SAM 2 for video |
| CV-SAM-003 | check the future in evaluation | Control access to future frames in evaluation |
| CV-ORB-006 | articulating computational constraint and task success | Relate computational constraints to task success |
| CV-CORNERS-001 | Interpreting local values | Interpret local eigenvalues |
| CV-CORNERS-003 | Set a selection of corners | Tune a corner selection |
| CV-FAST-BRIEF-005 | measure the compromis calculation repeatability | Measure the computation-repeatability trade-off |
| CV-FLANN-004 | measure the recall time curve | Measure the time-recall curve |

</details>

Questions changed only by decimal points, so a list such as $0,9;0,8;0,7$
cannot be misread: CV-NMS-001, CV-NMS-003, CV-NMS-006, CV-HOMOGRAPHIE-004 and
CV-DETECTEURS-011. Their copies in the reference appendices were aligned.

## Checks performed

| Executed check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 vault Markdown files, 60 references, 282 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: prerequisite order and answer depth; minimum 260 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` and `--compare` with the starting inventory | 282 cards, no anomalies; no difference in ID or Anki identity |
| `tools/compare_protected.py` against `76fda5a` | 102 protected-field differences, exactly the 97 logged objectives and 5 logged questions; 60 references at revision +1; H1, front matter and per-card headings unchanged ([evidence](invariants.json)) |
| `tools/check_anchors.py` on `vault/` and this directory | 3,841 local links and heading anchors resolve |
| `python3 -I checks/<subject>.py` for the 60 subjects | 60 scripts pass |
| `tools/check_github.py` on the URLs added to `vault/` | The 245 GitHub source files cited at a tag or commit exist, and all 396 cited line ranges fall inside them; only this repository's new reports are not yet on `main` |
| arXiv API query for the 143 arXiv identifiers added | All resolve; every labelled link names the matching paper or its authors |
| `git diff --check` | No whitespace errors |

The baseline for the comparison can be rebuilt with
`git archive 76fda5a vault | tar -x -C <dir>`.

## Sources and access

Agents opened the cited passages of primary papers and the source code of the
libraries at a release tag or commit. Each subject report lists the passages
read and the failures. Recurrent limits:

- **docs.opencv.org** returned HTTP 403 throughout. OpenCV claims were checked
  in the 4.13.0 headers and sources on GitHub, cited with line ranges; older
  tutorial links remain and are marked as not re-read.
- **Context7** was unavailable in this session, so library contracts rest on
  versioned code and official documentation, as `AGENTS.md` allows.
- **Paywalled or unreachable:** ISO/IEC 19795-1 and 30107-3, IEEE 1588,
  Little (1961), Hartley and Zisserman, Szeliski (download form), Tsai and
  Lenz, Park and Martin, Daniilidis, Evangelidis and Psarakis (abstract only),
  Horn and Schunck, Vincent and Soille, Furgale et al. 2013 (read through
  Rehder's thesis), Canny 1986 (abstract only). Claims that relied on them
  are qualified, cited through a secondary source that was read, or removed.
- **Executed code:** besides the stdlib recomputation scripts, one probe of
  the FAST pretest ran with a locally installed OpenCV 4.11.0; the report
  states that equivalence with 4.13.0 rests on a source diff.

## Limitations and export status

This is agent self-review. It establishes neither independent scientific
validation (FR-037) nor learner proficiency. No image, video, model or
hardware experiment was run: baselines and controlled variations are
proposed protocols. Obsidian rendering, including the Mermaid diagrams added
to 49 references, and AnkiDroid rendering are not verified; the
multi-line pseudocode restored in CV-HOMOGRAPHIE-003 deserves a look on the
phone.

The verification covers the claims the agents added or corrected and the
passages they cite. It is not a fresh line-by-line verification of every
retained sentence in the per-card appendices. Retained historical reports are
not rewritten; the 2026-10-20 NMS report still contains the strict-`>` claim
corrected here.

No Anki package is rebuilt. Corrected cards reach the phone through a new
package: **to republish with `paquet-anki`**, then check import, update and
rendering on the device.
