# Initial cover mapping

**Status**: editorial proposal enriched after reviews and addition of business divisions, 2026-10-18.

This cartography organizes an evolutionary catalog. The methods cited are entries to be documented, not reference notes already produced or an exhaustive list of all algorithms. The original names are retained.

## Proposed priorities

- **V0**: Gaps expressed –  classical methods, matching, calibration, geometry, tracking and detection.
- **V1**: complete the general basis and the connections between problems.
- **V2**: deepen advanced families and specializations, without excluding them.
- **Transverse**: data, evaluation and industrial constraints from the first reference notes.

Priorities refer to an educational order, not a scientific ranking. They are rated V0 to V2 (waves) so as not to be confused with the P1/P2 priorities of the routes of the spec. The semantic segmentation already mastered remains covered, with an adapted depth.

## Depth Levels and Skills

The priority indicates when to work on a topic; the depth indicates the expected result. This information is distinct from the state of writing and personal mastery.

| Target level | Observable result |
| --- | --- |
| Positioning | Identify the problem, the in/out, the family and the main limits |
| Operational use | Explain the steps, use a reference, adjust the parameters and interpret an evaluation |
| Further explanation | Justify hypotheses, reconstruct central reasoning, compare and diagnose a new case |

The generalist base aims at least at the operational use of the families selected. The priority gaps relate to the further explanation. Specializations can begin to locate if this depth is displayed: their presence in a list does not mean that they are mastered.

Each entry will specify the skills worked: explain, reason, apply, compare, evaluate and diagnose. A jurisdiction is only covered if a corresponding artifact exists; a non-applicability is justified.

## Domains and first entries

| Domaine | Methods and concepts to be inventoried | Proposed orientation |
| --- | --- | --- |
| 1. Mathematics and Estimation for Vision | SVD, least squares, robust estimation, non-linear optimization, conditioning, observability, uncertainty | Contextualized reminders; ML prerequisites already acquired |
| 2. Training and acquisition of images | Projection perspective, optical, radiometry, color/gamma, noise, exposure, sampling/aliasing, rolling/global shutter, synchronization | V1; acquisition and processing failures |
| 3. Classic image processing | Convolution, Gaussian/median/bilateral filters, gradients, Fourier, pyramids, morphology, Canny, Hough, histograms, restoration/deconvolution | V0; noise, resolution, frequencies and parameters |
| 4. Features, matching and registration | Harris, Shi – Tomasi, FAST, BRIEF, SIFT, ORB, AKAZE; brute-force, FLANN, ratio test, cross-check, RANSAC; SuperPoint, SuperGlue/LightGlue, LoFTR; registration per intensities/ECC | V0; classical/learned, sparse/dense and geometric validation |
| 5. Calibration and multiview geometry | Intrinsic, extrinsic, distortion, calibration target, fisheye, stereo/rectification, hand-eye, multisensor camera calibration – LiDAR/IMU, homography, fundamental/essential matrices, PnP, triangulation, bundle adjustment | V0; coordinate frames, units, observability and degenerations |
| 6. Vision 3D | StereoBM/SGBM, depth, SfM, odometry, SLAM/looping; normal, voxels, FPFH, RANSAC global, point-to-point/point-to-plane ICP, meshes; multisensor fusion to deepen | V1; scale, initialization and matches |
| 7. Recognition and representations | HOG, global descriptors, classification, CNN/ResNet, ViT, metric learning, autosupervision/DINO, retrieval; open-set and anomaly detection/location, including PatchCore | V1; visual properties, anomalies and transfer |
| 8. Detection and pose | R-CNN/Faster R-CNN, families YOLO, DETR; one-stage/two-stage, anchors/anchor-free, feature pyramids, assignment, NMS, key points, articulated pose 2D/3D and object pose | V0; Targets, Specific Losses, and Location |
| 9. Segmentation | Global/adaptive/Otsu settings, related components, distance transform, watershed, region growing, graph cuts/GrabCut, active contours, superpixels; U-Net/DeepLab, Mask R-CNN, semantics, instances, panoptics, prompts and video | V0 for the classic; V1/V2 for the less mastered variants |
| 10. Movement and video comprehension | Lucas – Kanade pyramidal, Farnebäck, RAFT, split/dense flow; point tracking/CoTracker, visibility; two-stream, 3D CNN, time models, actions | V0 for bases; causal/offline and temporal tasks |
| 11. Tracking and association | MeanShift/CamShift, single object trackers by correlation/siam; Kalman, gating, assignment/Hungarian, SORT, DeepSORT, ByteTrack, ReID and tracks life cycle | V0; identity, occlusion, mobile camera, online/offline |
| 12. Generative and multimodal vision | VAE, GAN, broadcast, restore/super-resolution, vision-language, grounding, open vocabulary, foundation models, implicit/explicit representations and neural rendering | V2; objectives, supervision, capabilities and limitations |
| 13. Data, evaluation and reliability | Annotation, ambiguity of ground truth, splits by scene/sequence, leaks, IoU/AP, geometric errors, MOTA/IDF1/HOTA, calibration of scores, uncertainty, OOD, drift and subgroups | Transverse; protocols, thresholds and rare errors |
| 14. Engineering of vision systems | Baselines, reproducibility, testing, pre/postprocessing, consistent increases, profiling, latency/flow, memory/transfers, quantification, deployment and monitoring; end-to-end design, from requirements to classic/learned choice and validation | Transverse; data contracts and comprehensive measures |

The entries specific to the business units, described below, complete this table; each is linked to a single host domain.

## Axes to be checked in each relevant family

| Axe | Question of coverage |
| --- | --- |
| Acquisition and representation | What effects do light, color, exposure, cadence, sampling and sensor have? |
| Data contract | Which coordinate frames, types, ranges, units, normalizations and transformations are assumed? |
| Geometry and numerical calculation | What ambiguities, degenerations, sensitivities and initialization conditions? |
| Supervision | What data, annotations, targets, and task-specific bones? |
| Generalization | What variations, never-before-seen scenes, rare errors and domain shifts? |
| Evaluation | What simple reference, what protocol, what thresholds and what limits of metrics? |
| Exploitation | What is the full cost, what is the diagnosis and what is the alternative under stress? |

These focus on the peculiarities of vision. They do not require a new general course of ML or the reproduction of each heavy training.

## Depth in priority areas

### Matching and registration

Document the role of each step, supported transformations, exact or approximate descriptor properties, distances, parameters, match filters, and geometric verification. Relate failures to observations: ambiguities, texture, appearance, geometry, noise and distribution of correspondences.

A large number of matches is not sufficient to demonstrate the validity of an estimate. Each filtering step must have its justification.

### Calibration, pose and geometry

Explain what is estimated, from what observations and in what coordinate frames. Process units, transformations, distortions, identifiability, degenerate conditions, and model limitations. The minimum conditions must be given for the variant concerned, without abusive generalization.

Distinguish error on fit observations and validation on other observations. Explain what a reprojection error measures and what conclusions it alone cannot draw.

### Tracking

Distinguish single/multi-object, motion/appearance, detection/association, prediction/update, gating/assignment, creation/confirmation/end of track. Relate motion assumptions to cadence, camera, and missing observations. Dealing with identity exchanges, fragmentation, occlusion, field inputs/outputs and detector dependencies.

### Detection

Document box representation, coordinate frames and normalization, assignment, location/classification, exit policies and postprocessing. Link architecture and learning objective to the task without giving back a general DL course. Include small objects, overlap, imbalance, scaling, and the consequences of thresholds on the downstream pipeline.

## Connections to make explicit

- Calibration, estimate of pose and registration: separate objectives that can occur in the same pipeline.
- optical flow, tracking and re-identification: separate outputs and assessments, with connections to explain.
- Geometry, classical methods and learning: approaches that combine.
- Transverse methods and metrics: a canonical reference note linked from several domains, rather than divergent explanations.

## Business divisions

The six poles below describe specialization axes and the corresponding business families, at the request of the learner (2026-10-18). They form an overlay of domains: each entry specific to a pole is inventoried in a single host domain, indicated in parentheses, and a subject shared between poles keeps a single canonical reference note.

Job titles are indicative; their content varies between companies. Covering a pole means having the reference notes, flashcards and corresponding cases, not being ready for a position.

**Base first**: The V0 wave remains devoted to the gaps expressed. In each pole, the key inputs are aimed at V1 and operational use; the further study are in V2, at the default location. The priority of a pole is a decision of the learner, recorded in the spec. A notion already in V0 retains its priority: its attachment to a pole does not artificially postpone it in V1.

| Pole | Perimeter | Indicative occupations | Areas mobilized |
| --- | --- | --- | --- |
| A. Deep Learning & Image Understanding | Classification, Detection, Segmentation, Recognition, Vision Transformers and Visual Foundation Models | 2D CV Engineer, Visual Recognition Engineer, Vision Foundation Model Engineer | 7, 8, 9, 12, 13 |
| B. Geometric Vision & Spatial AI | Reconstruction 3D, calibration, estimation of pose, SLAM, VIO and multiview geometry | 3D Vision Engineer, VIO Engineer, SLAM Engineer, Spatial AI Engineer | 1, 2, 4, 5, 6, 12, 13 |
| C. Robotics & Autonomous Perception | Sensor fusion, real-time perception, environmental estimation and navigation | Robotics Perception Engineer, Autonomous Perception Engineer, Sensor Fusion Engineer | 1, 2, 5, 6, 8, 11, 13, 14 |
| D. Multimodal AI & Video Intelligence | VLM, image-to-text alignment, video comprehension, grounding and vision-language-action models | Multimodal AI Engineer, Video AI Engineer, VLM Research Engineer | 7, 10, 12, 13 |
| E. Applied Computer Vision | Remote sensing, medical imaging, industrial inspection, biometrics and document analysis | Remote Sensing AI Engineer, Medical Imaging AI Engineer, Industrial Vision Engineer | 2, 7, 9, 13, 14 |
| F. Vision Systems & Deployment | GPU optimization, embedded deployment, quantification and low-latency video pipelines | Edge AI Engineer, Computer Vision Systems Engineer, Inference Optimization Engineer | 2, 3, 13, 14 |

### A — Deep Learning & Image Understanding

- **Key inputs (V1/U)** : ViT, Swin and ConvNeXt (d07) ; DINOv2 and self-supervised features (d07); image-text alignment CLIP/SigLIP, shared with D (d07); SAM and SAM 2 (d09); open-vocabulary grounding detection DINO and OWL-ViT (d08); adaptation by linear probing, fine-tuning and LoRA/adapters (d07); long-tail, annotation strategy and active learning (d13); mIoUPQ and AP by object size (d13).
- **Further study (V2/R)**: masked pretraining MAE and scale effects (d07); multitasking foundation models like Florence-2 (d12). Distillation is attached to the F pole (d14).
- **Cas propres**: design –  choose between a retrained closed detector and an open-vocabulary detection for a product catalog that changes every month; diagnosis –  AP of small objects that drops after a reduction in input resolution.

### B — Geometric Vision & Spatial AI

- **Key inputs (V1/U)** : SO(3)/SE(3) groups and parameterizations of rotations (d01); factor graphs, GTSAM and iSAM2 (d01); sparse bundle adjustment and Schur complement (d05); VIO Pre-Integration IMU, MSCKF, VINS-Mono and OKVIS (d06); loop closure and location recognition, DBoW2 and NetVLAD (d06); dense reconstruction MVS and merger TSDF (d06) ; ATE and RPE (d13).
- **Further study (V2/R)**: DUSt3R and MASt3R (d06); monocular depth, Depth Anything (d06); NeRF and 3D Gaussian Splatting (d12); event cameras (d02).
- **Cas propres**: design –  location of an indoor augmented reality headset, with cameras and IMU, under latency constraint; diagnosis –  scale and yaw drift of a VIO in a poorly textured corridor, separating estimation errors, insufficient excitation and overall gauge of yaw.

### C — Robotics & Autonomous Perception

- **Key inputs (V1/U)** Filters EKF, UKF and ESKF for the merger (d01); LiDAR, radar and ToF, measurement and noise formation (d02); hardware timestamp and synchronization (d02); extrinsic camera calibration –LiDAR–radar–IMU and time offset (d05); point cloud representations, PointNet++ and voxels (d06); odometry and localization LiDAR, LOAM and NDT (d06); top view (BEV) and occupancy grids, Lift-Splat-Shoot, BEVFormer and BEVFusion (d06); detection 3D PointPillars and CenterPoint (d08) ; suivi 3D multiobject, AB3DMOT (d11); NDS and mAP 3D (d13) ; ROS 2 and real-time latency budgets (d14).
- **Further study (V2/R)**: free space and traversability (d06); representations of implicit surfaces occupied/SDF (d06), distinguished from free/occupied/unknown probabilistic grids used by a robot.
- **Perimeter**: The trajectory planning and the check are out of scope; only the perception that feeds them is covered.
- **Cas propres**: design –  perception of a warehouse mobile robot with cameras and LiDAR, under security requirements; diagnosis –  double obstacles after camera fusion – LiDAR when the robot rotates.

### D — Multimodal AI & Video Intelligence

- **Key inputs (V1/U)** : CLIP/SigLIP (reference note d07 shared with A); architectures VLM BLIP-2, LLaVA and Flamingo, visual tokenization (d12); grounding and referential segmentation (d12); TimeSformer, ViViT and VideoMAE video transformations (d10); temporal location of actions (d10); VLM hallucination, contamination of benchmarks and sensitivity to prompt (d13).
- **Further study (V2/R)**: video-LLM and long video, frame and memory sampling (d10); vision-language-action models RT-2, OpenVLA and π0 (d12). The VLA are studied as a perception/action boundary: their outputs and limits are explained, without implementing a robotic control policy or extending the perimeter to the check.
- **Cas propres**: design –  index hours of surveillance video with a generalist VLM or pipeline detection, tracking and rules; diagnostic –  VLM that describes absent objects on off-distribution industrial images.

### E — Applied Computer Vision

- **Key Inputs (V1/U), Industrial Inspection**: lighting, telecentric optics and line-scan cameras (d02); golden template and anomaly detection PatchCore, PaDiM (d07); metrology and Gauge R&R (d13). The inspection is retained as a central industrial case.
- **further study (V2/R), per application** :
  - Remote sensing: multispectral imaging and SAR, georeferencing (d02); change detection (d09); large image tuiling (d14).
  - Medical imaging: formats DICOM/NifTI and volumes (d02); nnU-Net (d09); Dice, HD95, external validation and distinction between algorithmic performance and clinical utility (d13).
  - Biometrics: ArcFace facial recognition and attack detection by presentation, ISO/IEC 30107 framework to be versioned during its study (d07); FMR/FNMR, FAR/FRR according to protocol, ERA, PAD metrics and subgroups (d13).
  - Documents: OCR CRNN/CTC and TrOCR, layout LayoutLM, Donut without OCR (d07); CER and WER (d13).
- **Cas propres**: design –  inspection of rare defects on a timed line with very few defective examples; diagnosis –  remote sensing model that degrades from one season to the next.

### F — Vision Systems & Deployment

- **Key inputs (V1/U)** GPU runtime, memory hierarchy, transfers and Nsight profiling (d14); runtimes TensorRT, ONNX Runtime, OpenVINO and LiteRT (d14); PTQ/QATgranularity and representative calibration, with INT8/FP8 according to operators, runtime and hardware (d14); pruning and distillation, also useful to pole A (d14); video pipelines: hardware decoding NVDEC, GStreamer/DeepStream, zero-copy, batching and counter-pressure (d14); end-to-end latency budget, p50/p99 and jitter (d14).
- **Further study (V2/R)**: Jetson and NPU embedded targets, consumption and thermal (d14); serving with Triton (d14); OTA updates and edge monitoring (d14).
- **Cas propres**: design –  eight streams 1080p to 30 frames/s on an embedded module, with a constrained p99; diagnostic –  INT8 quantification without latency gain because the neck is CPU preprocessing or transfers.

## Proposed pedagogical pilot

| Subject | What it allows to check in the design |
| --- | --- |
| SIFT | reference note developed, invariances, equations and parameters |
| ORB | Comparison, representation, distance and calculation constraints |
| RANSAC applied to a homography | Assumptions, Robust Estimation and Geometric Diagnosis |
| Calibration on calibration target, Zhang method | coordinate frames, camera settings and validation |
| SORT and its limits | State Estimation, Association, Identities and Pipeline Diagram |
| NMS in detection | Post-processing, thresholds, failure cases and evaluation |
| IoU and AP, COCO protocol | reference note metric/protocol type, canonical and bound since detection, segmentation and association of SORT |

This first floor checks the format on the immediate gaps. A second contrasting floor is proposed before generalization:

| Extension of the pilot | Proven educational risk |
| --- | --- |
| Otsu, distance transform and watershed | Classic pipeline, separate tasks and diagnostics of markers |
| SuperPoint + LightGlue in front of a classic reference | Learned method, components, protocol and comparable costs |
| Local ICP and initialization by registration global | Geometry 3D, coordinate frames, local minimum and evaluation |

The driver consists of seven initial subjects and three extensions, not ten reference notes in the required format. A comparison or pipeline can link several canonical reference notess. The two floors remain proposals to be validated.

## Monitoring of coverage during production

Each chosen method will have an identifiable entry, beyond a mention in the line of a domain. Expected fields: identifier, domain, served poles, problem/family, method/variant, mandatory prerequisites, related notions, priority, target depth, targeted skills, sources, canonical reference note, flashcards or associated cases and editorial states.

Mandatory prerequisites are distinct from thematic links. The apparent prerequisite loops are resolved by an explicit shared base. An entrance is covered only for the skills and depth supported by its artifacts; the remaining gaps are retained.

The specializations are described by poles C (robotics and autonomy) and E (remote sensing, medical imaging, inspection, biometrics and documents). Their detailed inventory remains to be enriched with each batch.

## Framing Sources

- [Classic CMU Course](https://www.cs.cmu.edu/~16385/s14/): image formation, processing, geometry, movement and correspondences.
- [Stanford CS231n](https://cs231n.stanford.edu/schedule): learning, recognition, detection, segmentation, video, 3D and multimodality.
- [OpenCV 4.13 –  features and matching](https://docs.opencv.org/4.13.0/db/d27/tutorial_py_table_of_contents_feature2d.html).
- [OpenCV 4.13 –  calibration and geometry](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [OpenCV 4.13 –  movement and tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
- [ByteTrack –  author's filing](https://github.com/FoundationVision/ByteTrack).

The additions and their sources are detailed in [the Relevance Review](review.md). The catalog should not be limited to the methods of a particular library.

These sources support the cutting and inventory. Each reference note produced will have to cite its own primary sources and verify the characteristics of the variant explained; no universal preference between methods is assumed.
