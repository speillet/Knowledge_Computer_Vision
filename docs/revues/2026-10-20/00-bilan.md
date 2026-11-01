# Review of flashcards –  2026-10-20

Consolidated balance sheet on 21 October 2026.

## Perimeter and result

The **52 subjects and 224 existing flashcards** have an individual report and an assessment of the four axes of the `revue-cartes` skill: accuracy, relevance, correctability and consistency. The 12 reports of 18 October (50 flashcards), already present at the takeover, are included in the balance sheet; the remaining 40 subjects (174 flashcards) were examined on 20 October. The sources of the first 12 reports are not presented as newly consulted on 20 October. The summaries and links of these reports have been harmonized with consolidation.

The perimeter is the existing content, not the entire computer vision program. No additions, deletions, lens changes or IDs; no Anki sync IDs were present. The modified reference notess have an incremental revision and remain `statut: redige`, source `agent`. Current accounts (52 reference notes, 224 flashcards) remain unchanged.

| Maximum gravity per flashcard before correction | Flashcards |
| --- | ---: |
| Bloquante | 0 |
| Importante | 46 |
| Minor | 92 |
| No defects found in the audited passage | 86 |
| Total | 224 |

This count counts every flashcard once; it does not count independent errors or defects limited to reference notes. "No defects found" is not a certification of accuracy. Corrections mainly concern insufficient sources, implicit assumptions and conventions, as well as too vague response criteria. The [Correction Log](../../../vault/01-Parcours/Suivi-pilote.md#follow-up-and-corrections) records each intervention and its revision.

## Main corrections

- Weighting and whitening of residuals; joint EKF/ESKF, coordinate frames and units; response criteria for Hough and morphology.
- Contracts `solvePnP`/`solveP3P`, hand – eye relative movements, Schur conditions and disparity convention for stereo depth.
- Convention CER classic distinguished from that of OCR-D benchmarks; panoptic partition without overlap; sources specific to method variants, pose and symmetries.
- Contract SORT without detection, empty input form `(0, 5)`; distinction between fixed template SiamFC and update in an adaptive tracker.
- Noise margin DDPM distinguished from a transition; density NeRF dependent on the position, color also dependent on the direction.
- Boundary and distinct integer quantification of FP8; material limits of sparsity and thermal regime; explicit Amdahl sequential model.
- Passes from sources targeted by flashcard; dates or versions of specified documentation; reasoning, diagnostics and project protocols distinguished from published results and actually performed experiments.

## Mapping of reports

| Subject and canonical reference note | Flashcards | Rapport |
| --- | ---: | --- |
| [Lesser squares, SVD and packaging](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md) | [4](../../../vault/10-mathematiques-estimation/11-moindres-carres-svd.md) | [2026-10-18](../2026-10-18/11-moindres-carres-svd.md) |
| [SO(3), SE(3) and processing conventions](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md) | [4](../../../vault/10-mathematiques-estimation/12-rotations-se3.md) | [2026-10-18](../2026-10-18/12-rotations-se3.md) |
| [Kalman, EKF, UKF and ESKF for fusion](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) | [4](../../../vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md) | [2026-10-18](../2026-10-18/13-kalman-ekf-eskf.md) |
| [Factor Graphs and Incremental Optimization](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md) | [3](../../../vault/10-mathematiques-estimation/14-graphes-facteurs.md) | [2026-10-18](../2026-10-18/14-graphes-facteurs.md) |
| [Exposure, noise, colour and sampling](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) | [4](../../../vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md) | [2026-10-18](../2026-10-18/21-exposition-bruit-echantillonnage.md) |
| [Sensors, rolling shutter and synchronization](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md) | [4](../../../vault/20-acquisition-images/22-capteurs-horodatage.md) | [2026-10-18](../2026-10-18/22-capteurs-horodatage.md) |
| [Line-scan, remote sensing and medical volumes](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md) | [3](../../../vault/20-acquisition-images/23-imageries-specialisees.md) | [2026-10-18](../2026-10-18/23-imageries-specialisees.md) |
| [Filters, gradients and pyramids](../../../vault/30-traitement-image/references/31-filtrage-gradients.md) | [4](../../../vault/30-traitement-image/31-filtrage-gradients.md) | [2026-10-18](../2026-10-18/31-filtrage-gradients.md) |
| [Canny and Hough: contours, lines and segments](../../../vault/30-traitement-image/references/32-canny-hough.md) | [4](../../../vault/30-traitement-image/32-canny-hough.md) | [2026-10-18](../2026-10-18/32-canny-hough.md) |
| [Morphology and related components](../../../vault/30-traitement-image/references/33-morphologie-composantes.md) | [3](../../../vault/30-traitement-image/33-morphologie-composantes.md) | [2026-10-18](../2026-10-18/33-morphologie-composantes.md) |
| [SIFT –  local points and description on several scales](../../../vault/40-features-matching/references/41-sift.md) | [7](../../../vault/40-features-matching/41-sift.md) | [2026-10-18](../2026-10-18/41-sift.md) |
| [ORB –  detection and binary oriented descriptor](../../../vault/40-features-matching/references/42-orb.md) | [6](../../../vault/40-features-matching/42-orb.md) | [2026-10-18](../2026-10-18/42-orb.md) |
| [Local detectors, descriptors and matchers](../../../vault/40-features-matching/references/43-detecteurs-matchers.md) | [4](../../../vault/40-features-matching/43-detecteurs-matchers.md) | [2026-10-20](43-detecteurs-matchers.md) |
| [SuperPoint, LightGlue and LoFTR](../../../vault/40-features-matching/references/44-superpoint-lightglue-loftr.md) | [5](../../../vault/40-features-matching/44-superpoint-lightglue-loftr.md) | [2026-10-20](44-superpoint-lightglue-loftr.md) |
| [registration by intensities and ECC](../../../vault/40-features-matching/references/45-recalage-ecc.md) | [3](../../../vault/40-features-matching/45-recalage-ecc.md) | [2026-10-20](45-recalage-ecc.md) |
| [RANSAC applied to a homography](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md) | [7](../../../vault/50-calibration-geometrie/51-ransac-homographie.md) | [2026-10-20](51-ransac-homographie.md) |
| [Camera calibration on calibration target –  Zhang's method](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md) | [7](../../../vault/50-calibration-geometrie/52-calibration-zhang.md) | [2026-10-20](52-calibration-zhang.md) |
| [Epipolar, PnP and triangulation](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md) | [5](../../../vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md) | [2026-10-20](53-epipolaire-pnp-triangulation.md) |
| [Bundle adjustment and complement of Schur](../../../vault/50-calibration-geometrie/references/54-bundle-adjustment.md) | [4](../../../vault/50-calibration-geometrie/54-bundle-adjustment.md) | [2026-10-20](54-bundle-adjustment.md) |
| [Multisensor calibration, hand-eye and time](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md) | [3](../../../vault/50-calibration-geometrie/55-calibration-multicapteurs.md) | [2026-10-20](55-calibration-multicapteurs.md) |
| [Rectified stereo, SGM and depth](../../../vault/60-vision-3d/references/61-stereo-profondeur.md) | [4](../../../vault/60-vision-3d/61-stereo-profondeur.md) | [2026-10-20](61-stereo-profondeur.md) |
| [registration global and local PKI](../../../vault/60-vision-3d/references/62-recalage-global-icp.md) | [5](../../../vault/60-vision-3d/62-recalage-global-icp.md) | [2026-10-20](62-recalage-global-icp.md) |
| [SLAM, VIO, pre-integration IMU and loopback](../../../vault/60-vision-3d/references/63-slam-vio.md) | [5](../../../vault/60-vision-3d/63-slam-vio.md) | [2026-10-20](63-slam-vio.md) |
| [Clouds, BEV and occupancy representations](../../../vault/60-vision-3d/references/64-nuages-bev-occupation.md) | [5](../../../vault/60-vision-3d/64-nuages-bev-occupation.md) | [2026-10-20](64-nuages-bev-occupation.md) |
| [Visual representations, ViT, Swin, ConvNeXt and DINOv2](../../../vault/70-reconnaissance-representations/references/71-representations-transfert.md) | [5](../../../vault/70-reconnaissance-representations/71-representations-transfert.md) | [2026-10-20](71-representations-transfert.md) |
| [CLIP, SigLIP and text recognition](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md) | [4](../../../vault/70-reconnaissance-representations/72-clip-siglip.md) | [2026-10-20](72-clip-siglip.md) |
| [Inspection: golden template, PatchCore and PaDiM](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md) | [4](../../../vault/70-reconnaissance-representations/73-patchcore-padim.md) | [2026-10-20](73-patchcore-padim.md) |
| [OCR and Documentary Understanding](../../../vault/70-reconnaissance-representations/references/74-ocr-documents.md) | [3](../../../vault/70-reconnaissance-representations/74-ocr-documents.md) | [2026-10-20](74-ocr-documents.md) |
| [Biometric recognition, ArcFace and PAD](../../../vault/70-reconnaissance-representations/references/75-embeddings-biometrie.md) | [2](../../../vault/70-reconnaissance-representations/75-embeddings-biometrie.md) | [2026-10-20](75-embeddings-biometrie.md) |
| [NMS –  remove redundant detections](../../../vault/80-detection-pose/references/81-nms.md) | [5](../../../vault/80-detection-pose/81-nms.md) | [2026-10-20](81-nms.md) |
| [Detection: Faster R-CNN, YOLO and DETR families](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) | [5](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) | [2026-10-20](82-detection-fasterrcnn-yolo-detr.md) |
| [Open-vocabulary detection and grounding](../../../vault/80-detection-pose/references/83-detection-open-vocabulary.md) | [3](../../../vault/80-detection-pose/83-detection-open-vocabulary.md) | [2026-10-20](83-detection-open-vocabulary.md) |
| [Detection 3D, object pose and articulated pose](../../../vault/80-detection-pose/references/84-detection-pose-3d.md) | [4](../../../vault/80-detection-pose/84-detection-pose-3d.md) | [2026-10-20](84-detection-pose-3d.md) |
| [Otsu, distance transform and watershed](../../../vault/90-segmentation/references/91-otsu-distance-watershed.md) | [5](../../../vault/90-segmentation/91-otsu-distance-watershed.md) | [2026-10-20](91-otsu-distance-watershed.md) |
| [GrabCut, regions and models of appearance](../../../vault/90-segmentation/references/92-grabcut-regions.md) | [3](../../../vault/90-segmentation/92-grabcut-regions.md) | [2026-10-20](92-grabcut-regions.md) |
| [Semantic segmentation, instances and panopticon](../../../vault/90-segmentation/references/93-semantique-instances-panoptique.md) | [4](../../../vault/90-segmentation/93-semantique-instances-panoptique.md) | [2026-10-20](93-semantique-instances-panoptique.md) |
| [SAM, SAM 2 and video guided segmentation](../../../vault/90-segmentation/references/94-sam-sam2.md) | [3](../../../vault/90-segmentation/94-sam-sam2.md) | [2026-10-20](94-sam-sam2.md) |
| [optical flow: Lucas – Kanade, Farnebäck and RAFT](../../../vault/100-mouvement-video/references/101-flot-optique.md) | [4](../../../vault/100-mouvement-video/101-flot-optique.md) | [2026-10-20](101-flot-optique.md) |
| [Monitoring of points, actions and video comprehension](../../../vault/100-mouvement-video/references/102-points-actions-video.md) | [4](../../../vault/100-mouvement-video/102-points-actions-video.md) | [2026-10-20](102-points-actions-video.md) |
| [SORT –  multiobject tracking by movement and association](../../../vault/110-tracking-association/references/111-sort.md) | [8](../../../vault/110-tracking-association/111-sort.md) | [2026-10-20](111-sort.md) |
| [DeepSORT, ByteTrack and multiobject association](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md) | [4](../../../vault/110-tracking-association/112-deepsort-bytetrack.md) | [2026-10-20](112-deepsort-bytetrack.md) |
| [Single Object Tracking: Correlation, Siamese and MeanShift](../../../vault/110-tracking-association/references/113-tracking-monoobjet.md) | [2](../../../vault/110-tracking-association/113-tracking-monoobjet.md) | [2026-10-20](113-tracking-monoobjet.md) |
| [VLM, grounding and frontier vision – action](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md) | [4](../../../vault/120-generatif-multimodal/121-vlm-grounding.md) | [2026-10-20](121-vlm-grounding.md) |
| [VAE, GAN and broadcast for generation/restoration](../../../vault/120-generatif-multimodal/references/122-generation-restauration.md) | [3](../../../vault/120-generatif-multimodal/122-generation-restauration.md) | [2026-10-20](122-generation-restauration.md) |
| [NeRF, 3D Gaussian Splatting and Reconstruction](../../../vault/120-generatif-multimodal/references/123-nerf-gaussian-splatting.md) | [3](../../../vault/120-generatif-multimodal/123-nerf-gaussian-splatting.md) | [2026-10-20](123-nerf-gaussian-splatting.md) |
| [IoU and AP –  COCO detection protocol](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md) | [7](../../../vault/130-evaluation-fiabilite/131-iou-ap-coco.md) | [2026-10-20](131-iou-ap-coco.md) |
| [Evaluate identities, trajectories and location 3D](../../../vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md) | [5](../../../vault/130-evaluation-fiabilite/132-tracking-trajectoires.md) | [2026-10-20](132-tracking-trajectoires.md) |
| [Splits, annotations, scoring calibration and drift](../../../vault/130-evaluation-fiabilite/references/133-donnees-generalisation.md) | [5](../../../vault/130-evaluation-fiabilite/133-donnees-generalisation.md) | [2026-10-20](133-donnees-generalisation.md) |
| [Segmentation, inspection and application metrics](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md) | [4](../../../vault/130-evaluation-fiabilite/134-metriques-applications.md) | [2026-10-20](134-metriques-applications.md) |
| [Data contracts, profiling and video pipelines](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md) | [5](../../../vault/140-ingenierie-systemes/141-contrats-profiling-video.md) | [2026-10-20](141-contrats-profiling-video.md) |
| [PTQ, QAT, INT8/FP8 and runtimes](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md) | [5](../../../vault/140-ingenierie-systemes/142-quantification-runtimes.md) | [2026-10-20](142-quantification-runtimes.md) |
| [Edge deployment, compression and monitoring](../../../vault/140-ingenierie-systemes/references/143-edge-reproductibilite.md) | [4](../../../vault/140-ingenierie-systemes/143-edge-reproductibilite.md) | [2026-10-20](143-edge-reproductibilite.md) |

## Proposed Priority Enrichments

No new flashcard has been written. The detailed proposals are in the reports; the priority below is an editorial choice to be discussed, not a measure of mastery of the learner.

| Proposition | Gap filled | Family | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| check NIS and residuals biased | Distinguish between low residual and coherent covariance | Evaluation | 1 flashcard, 3 criteria; duration to be measured | [Gamse et al., §§2.2.2 and 3.4](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) |
| Transporting a covariance by the assistant | Avoid mixing uncertainty coordinate frames | Reasoning | 1 flashcard, 3 criteria; duration to be measured | [Solà et al., §II-H](https://arxiv.org/abs/1812.01537) |
| Calculate PQ on a mini-matching | Make the panoptic metric operational | Evaluation | 1 flashcard, TP/FP/FN and IoU average | [Panoptic Segmentation, §4](https://arxiv.org/abs/1801.00868) |
| Calculate the effect of an ID switch on IDF1 | Moving from qualitative distinction to a calculated case | Reasoning | 1 flashcard in a short sequence | [Ristani et al., identity metrics](https://arxiv.org/abs/1609.01775) |

## Controls carried out

Checks executed on 20 October, then checked on delivery on 21 October:

| check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 125 documents Markdown, 52 reference notes, 224 flashcards |
| `python3 -m unittest discover -s tests` | 34 successful tests |
| `python3 scripts/sync_catalog.py --check` | 18 generated documents, no expired |
| `inventaire_cartes.py vault --comparer <inventaire_base.json>` | No ID added/disappeared, no Anki identity changed |
| `python3 examples/pilot_math.py` | IoU 2/3; NMS [0,2] then [0,1,2]; RANSAC 72/9; Kalman and AP consistent |
| `python3 examples/curriculum_math.py` | Otsu 1→21 with identical score; coherent projection/associations; stereo 10/20 m; 240 fps; gain 1,05263 |
| `git diff --check` and review of the diff | No spacing error; perimeter changes re-read |

The initial comparison of 20 October was supplemented with a comparison to the inventory of the original `e5b41f0`, extracted from the repository. One-time checks also verified: a report row by flashcard (224 separate IDs in 52 reports), local balance sheet and report links, table columns, no check characters, unchanged objectives, incremental revisions, and preserved historical sections. These one-time checks are not an IC or a new order from the repository.

## Limits and Open Points

- Agent self-review, without independent scientific proofreading. The reference notes are not promoted to "reread" status.
- [UKF](../2026-10-18/13-kalman-ekf-eskf.md): mechanism of sigma-points not verified in the full primary text accessible during the passage. [ECC](45-recalage-ecc.md): primary summary and OpenCV documentation consulted; derivation completes non-verifiable paper during review.
- More local access limits (including HOG summary and GrabCut mechanism verified in official documentation) are indicated in their reports. An absent source has not been confirmed.
- Context7 unavailable: direct use of official documentation, with recorded versions and dates. `latest` links remain scalable.
- No actual export, update Anki or Obsidian/AnkiDroid rendering attempts during this review; evidence dated October 18 has not been rewritten. The content is not synchronized.
- Control, recall time and real cost of unmeasured flashcards. Analytical counterexamples do not constitute image benchmarks or measured performance on hardware.
