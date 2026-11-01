# Complete flashcards –  2026-10-30

The **282 flashcards** have each received a development specific to their question. The corresponding **60 reference notes** have been aligned, each to the next revision and still to the `redige` status. The 14 themes and the course remain structured by the existing prerequisites.

## Pedagogical outcome

Additions include DLT lines and SVD subspaces, covariances and coordinate frames of pose, temporal noise patterns, SIFT/ORB steps, hand-eye chains, fisheye projection, ICP Jacobians, depth contracts, detection assignment, watershed markers, compositional mechanisms. The diagnostic and design flashcards receive a more precise calculation, decomposition or protocol related to their question.

Answers: **284 to 439 lexical words**, median **311,5**, versus 180 at 329 and median 200,5 before this pass. The length is measured, with no new quota. The finite core remains the rule of recall; developments serve to understand and reconstruct the response, without requiring integral recitation.

## Scope of evidence

The passages actually consulted are listed by subject. New cases, protocols and derivations are distinguished from the results of articles and measurements performed. This pass does not announce a new exhaustive scientific verification of each pre-existing sentence. Two section references are corrected (BRIEF §3; descriptor DeepSORT §2.4). The added FPN recurrence scheme has been specified before delivery to separate fusion and output smoothing.

Failed accesses (FAST original, Farnebäck original, Nature page, some HTML arXiv versions) are declared in the relevant reports; successful folds are identified. Context7 was used for the relevant OpenCV contracts and then the primary documentation. `latest` runtime documents are dated, with no new hardware support or suspected API failure.

The **119 further study of the backlog remain open**: making existing flashcards deeper does not mean covering all computer vision algorithms. No new ID, no flashcard removed, no question or lens changes.

## Verifications

| check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown, 60 reference notes, 282 flashcards |
| `python3 scripts/learning_path.py` | OK: 60 subjects, 282 flashcards; controlled order and length |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, no expired |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 56 successful tests |
| Inventory compared to the beginning of the pass | No ID or identity plugin changed |
| Detailed Fields Comparison | Questions, kernels, blocking errors, tags, decks and objectives retained for 282 flashcards |
| Revisions and status of reference notes | +1 for each of the 60 reference notes; `redige` |
| [Synthetic calculations](61-controles-numeriques.json) | 33 verified results in Python, standard library; no CV template executed |
| [Invariants](62-invariants.json) | 282 GUIDs and model Anki preserved |
| Build and proofread the local package | 282 notes/flashcards, 14 decks, one SVG; ganaki 0.13.1 |
| Comparing to the original local manifesto | 282 modified; 0 added, 0 removed |
| Engine simulation Anki 26.9.3, Python 3.12 | Import, reimport without duplicates, update; history retained on three revised flashcards test runs |
| `git diff --check` | Without error |

The local package `dist/CV-Pilote.apkg` comes from the modified work tree on `docs/deepen-cv-mechanisms-20261030`: it is not a published release. The manifest comparison is about the local copy of the start pass, not about a last remote release not searched for in this task. The "reference note" links in the package target `main` and will match this revision of the reference notes after integrating the changes into this main branch.

Android rendering, review time, delayed recall, and real project forwarding remain to be checked. The Anki simulation in disposable collection does not validate the display in AnkiDroid or a real synchronization by the plugin.

## Reports by subject

| Subject | Reference note | flashcards | Revision |
| --- | --- | --- | --- |
| [CV-SVD](01-cv-svd.md) | Least squares, SVD and conditioning | 9 | 5 → 6 |
| [CV-SE3](02-cv-se3.md) | SO(3), SE(3) and processing conventions | 6 | 6 → 7 |
| [CV-FUSION](03-cv-fusion.md) | Kalman, EKF, UKF and ESKF for fusion | 6 | 6 → 7 |
| [CV-FACTEURS](04-cv-facteurs.md) | Factor Graphs and Incremental Optimization | 5 | 6 → 7 |
| [CV-ACQUISITION](05-cv-acquisition.md) | Exposure, noise, colour and sampling | 4 | 6 → 7 |
| [CV-CAPTEURS](06-cv-capteurs.md) | Sensors, rolling shutter and synchronization | 4 | 3 → 4 |
| [CV-IMAGERIES](07-cv-imageries.md) | Line-scan, remote sensing and medical volumes | 3 | 3 → 4 |
| [CV-FILTRES](08-cv-filtres.md) | Filters, gradients and pyramids | 4 | 3 → 4 |
| [CV-CANNY-HOUGH](09-cv-canny-hough.md) | Canny and Hough: contours, lines and segments | 4 | 3 → 4 |
| [CV-MORPHO](10-cv-morpho.md) | Morphology and related components | 3 | 3 → 4 |
| [CV-SIFT](11-cv-sift.md) | SIFT –  local points and description on several scales | 7 | 4 → 5 |
| [CV-ORB](12-cv-orb.md) | ORB –  detection and binary oriented descriptor | 6 | 4 → 5 |
| [CV-MATCHING](13-cv-matching.md) | Local detectors, descriptors and matchers | 4 | 3 → 4 |
| [CV-MATCH-APPRIS](14-cv-match-appris.md) | SuperPoint, LightGlue and LoFTR | 5 | 3 → 4 |
| [CV-ECC](15-cv-ecc.md) | registration by intensities and ECC | 3 | 3 → 4 |
| [CV-CORNERS](16-cv-corners.md) | Harris and Shi – Tomasi –  local structure and followable points | 5 | 2 → 3 |
| [CV-FAST-BRIEF](17-cv-fast-brief.md) | FAST and BRIEF –  detect a corner and then describe its vicinity | 5 | 2 → 3 |
| [CV-FLANN](18-cv-flann.md) | FLANN –  close search and distance contract | 4 | 2 → 3 |
| [CV-HOMOGRAPHIE](19-cv-homographie.md) | RANSAC applied to a homography | 7 | 4 → 5 |
| [CV-ZHANG](20-cv-zhang.md) | Camera calibration on calibration target –  Zhang's method | 7 | 4 → 5 |
| [CV-EPIPOLAIRE](21-cv-epipolaire.md) | Epipolar, PnP and triangulation | 5 | 3 → 4 |
| [CV-BA](22-cv-ba.md) | Bundle adjustment and complement of Schur | 4 | 3 → 4 |
| [CV-MULTICALIB](23-cv-multicalib.md) | Multisensor calibration, hand-eye and time | 3 | 3 → 4 |
| [CV-FISHEYE](24-cv-fisheye.md) | Calibration fisheye –  Angular projection and off-centre validation | 5 | 2 → 3 |
| [CV-HANDEYE](25-cv-handeye.md) | Hand-eye calibration –  solve AX = XB without mixing the coordinate frames | 5 | 2 → 3 |
| [CV-STEREO](26-cv-stereo.md) | Rectified stereo, SGM and depth | 4 | 3 → 4 |
| [CV-ICP](27-cv-icp.md) | registration global and local ICP | 5 | 3 → 4 |
| [CV-VIO](28-cv-vio.md) | SLAM, VIO, pre-integration IMU and loopback | 5 | 3 → 4 |
| [CV-BEV](29-cv-bev.md) | Clouds, BEV and occupancy representations | 5 | 3 → 4 |
| [CV-REPRESENTATIONS](30-cv-representations.md) | Visual representations, ViT, Swin, ConvNeXt and DINOv2 | 5 | 3 → 4 |
| [CV-CLIP](31-cv-clip.md) | CLIP, SigLIP and text recognition | 4 | 3 → 4 |
| [CV-ANOMALIES](32-cv-anomalies.md) | Inspection: golden template, PatchCore and PaDiM | 4 | 3 → 4 |
| [CV-OCR](33-cv-ocr.md) | OCR and Documentary Understanding | 3 | 3 → 4 |
| [CV-BIOMETRIE](34-cv-biometrie.md) | Biometric recognition, ArcFace and PAD | 2 | 3 → 4 |
| [CV-NMS](35-cv-nms.md) | NMS –  remove redundant detections | 6 | 5 → 6 |
| [CV-DETECTEURS](36-cv-detecteurs.md) | Detection: Faster R-CNN, YOLO and DETR families | 13 | 6 → 7 |
| [CV-OPENVOC](37-cv-openvoc.md) | Open-vocabulary detection and grounding | 3 | 3 → 4 |
| [CV-POSE3D](38-cv-pose3d.md) | Detection 3D, object pose and articulated pose | 4 | 3 → 4 |
| [CV-WATERSHED](39-cv-watershed.md) | Otsu, distance transform and watershed | 5 | 2 → 3 |
| [CV-GRABCUT](40-cv-grabcut.md) | GrabCut, regions and models of appearance | 3 | 2 → 3 |
| [CV-SEGMENTATION](41-cv-segmentation.md) | Semantic segmentation, instances and panoptic segmentation | 4 | 3 → 4 |
| [CV-SAM](42-cv-sam.md) | SAM, SAM 2 and video guided segmentation | 3 | 3 → 4 |
| [CV-FLOT](43-cv-flot.md) | optical flow: Lucas – Kanade, Farnebäck and RAFT | 4 | 2 → 3 |
| [CV-VIDEO](44-cv-video.md) | Monitoring of points, actions and video comprehension | 4 | 4 → 5 |
| [CV-FARNEBACK](45-cv-farneback.md) | Farnebäck –  dense flow by polynomial expansion | 5 | 2 → 3 |
| [CV-SORT](46-cv-sort.md) | SORT –  multiobject tracking by movement and association | 8 | 4 → 5 |
| [CV-ASSOCIATION](47-cv-association.md) | DeepSORT, ByteTrack and multiobject association | 4 | 3 → 4 |
| [CV-SOT](48-cv-sot.md) | Single Object Tracking: Correlation, Siamese and MeanShift | 2 | 3 → 4 |
| [CV-CORRELATION](49-cv-correlation.md) | MOSSE and KCF –  Correlation filter tracking | 5 | 2 → 3 |
| [CV-MEANSHIFT](50-cv-meanshift.md) | MeanShift and CamShift –  follow an appearance distribution | 4 | 2 → 3 |
| [CV-VLM](51-cv-vlm.md) | VLM, grounding and frontier vision – action | 4 | 3 → 4 |
| [CV-DIFFUSION](52-cv-diffusion.md) | VAE, GAN and broadcast for generation/restoration | 3 | 3 → 4 |
| [CV-RENDU3D](53-cv-rendu3d.md) | NeRF, 3D Gaussian Splatting and Reconstruction | 3 | 3 → 4 |
| [CV-IOU-AP](54-cv-iou-ap.md) | IoU and AP –  COCO detection protocol | 7 | 4 → 5 |
| [CV-METRIQUES-TEMPS](55-cv-metriques-temps.md) | Evaluate identities, trajectories and location 3D | 5 | 3 → 4 |
| [CV-FIABILITE](56-cv-fiabilite.md) | Splits, annotations, scoring calibration and drift | 5 | 3 → 4 |
| [CV-METRIQUES-APPLIQUEES](57-cv-metriques-appliquees.md) | Segmentation, inspection and application metrics | 4 | 3 → 4 |
| [CV-PIPELINE](58-cv-pipeline.md) | Data contracts, profiling and video pipelines | 5 | 3 → 4 |
| [CV-QUANT](59-cv-quant.md) | PTQ, QAT, INT8/FP8 and runtimes | 5 | 3 → 4 |
| [CV-DEPLOIEMENT](60-cv-deploiement.md) | Edge deployment, compression and monitoring | 4 | 4 → 5 |

[Cadrage](00-cadrage.md) · [Journal of vault](../../../vault/01-Parcours/Suivi-pilote.md).
