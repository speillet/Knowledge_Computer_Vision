---
id: CV-POSE3D
type: comparaison
domaine: d08
poles: [A, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SE3", "CV-BEV", "CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# 3D detection, object pose and articulated pose

## Problem, data and assumptions

Compare outputs often called "pose": box 3D, rigid object transformation, articulated skeleton 2D/3D. Inputs/annotations and metrics differ. An oriented box is not a complete reconstruction of the shape.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-BEV](../../60-vision-3d/references/64-nuages-bev-occupation.md); [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

PointPillars encodes pillars as pseudo-images for a detection head; CenterPoint predicts 3D centers and attributes according to its variant. The object pose estimates a transformation of a model; the articulated pose estimates keypoints and their structure.

## Mathematics, conventions and units

Define coordinate frame, unit of dimensions, box anchor and yaw axis/sign, usually meters/radians in metric data. For a rigid pose, a symmetry of the object can make several rotations visually equivalent. A joint error must specify 2D pixels or 3D length and possible alignment.

## Parameters and properties

ROI, discretization, angles, visibility, taxonomy and point association. Do not mix conventions of datasets. Future data and ego compensation are protocol choices.

## Cost and implementation

Number of points, voxels/pillars, BEV resolution and postprocessing cost differently. No 3D network, skeleton or solver of pose executed.

## Evaluation and controlled variation

Proposed variation: rarefy points with distance, then hide joints separately. Evaluate outputs in the original coordinate frame and report symmetry/visibility. The AP nuScenes is not just the AP COCO with a IoU 3D.

## Failure modes and diagnosis

Yaw offset from 90°: check length/width order and axis convention before the model. pose of ambiguous object: test symmetry and measure really observable.

## Alternatives and applications

PnP if known 3D points, model learned if adapted observations, occupancy representation for other needs; retain separate tasks.

## Guided reasoning and proposed checks

These constructed cases develop metric contract and pose/symmetry ambiguities. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-POSE3D-001

**Question of work**: Why should a 3D detection score not be compared directly with articulated-pose error?

**Reference Response**: Boxes/classes and joints are different outputs with different annotations, matches and metrics.

**Difference of unknowns**: A 3D detection usually provides location, dimensions, and box orientation with a class. An articulated pose describes joint positions and their relationships; a rigid object pose connects a model to an observation. These outputs do not code the same geometry.

**Constructed example**: A box surrounding a pedestrian does not say where his wrists are. A well-fitting skeleton does not necessarily provide a metric 3D box in the coordinate frame sensor. First define the information consumed by the downstream module, its units and the processing of invisible points. Then choose the matches and alignment allowed in the evaluation. A comparison of heterogeneous scores can be misleading even when all articles use the word pose. A measure must be interpreted by its protocol, not by its title alone.

### Case linked to CV-POSE3D-004

**Question of work**: A cylindrical object is localized correctly, but its rotation around the cylinder axis varies. What should be checked?

**Reference Response**: Visual symmetry and the definition of pose/evaluation: this component can be ambiguous with available observations.

**Intuition of Identifiable**: If several rotations of the object produce the same appearance under the available observations, the vision can not always choose a single orientation. The evaluation model must then specify how the symmetries are processed and which parts of the pose remain observable.

**Constructed example**: A cylinder without a distinctive mark can be invariant to a rotation around its axis. Visible marking may break this ambiguity; better optimization alone does not make it appear. If an assembly step requires this angle, provide additional information and measure it. A box oriented or a low pose score is not enough to slice a symmetrical degree of freedom. Reporting convention and uncertainty avoids arbitrarily penalizing visually equivalent solutions or, conversely, masking an observable error on a marked object.

**Documentary reference for this pass**: [BOP, Tasks](https://bop.felk.cvut.cz/tasks/), task definition and pose metrics. The other developments are in the [flashcards](../84-detection-pose-3d.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-POSE3D-001

**Situation**: Why should a 3D detection score not be compared directly with articulated-pose error?

**Define the comparative quantity**: An average 3D joint error can write $J^{-1}\sum_j\|\hat p_j-p_j\|$ in a length unit, with visible joints or all joints according to protocol. Allowing rigid alignment or similarity removes some errors and changes the evaluated question. A AP of boxes, it, depends on a threshold of matching and the ranking of the scores. A rigid object pose estimates $R,t$ of a known model, while a skeleton estimates several related points. Specifying these unknowns and allowed transformations avoids comparing two digits, one of which has precisely neutralized the defect as the other measures.

### CV-POSE3D-002

**Situation**: What should be checked when 3D boxes have correct centers but inconsistent orientations or dimensions?

**Construction of corners**: for a geometric center $c$, dimensions $(l,w,h)$ and rotation $R$, the eight corners are $c+R(\pm l/2,\pm w/2,\pm h/2)^T$. If the center is anchored to the ground, the vertical component must be adjusted before using this formula. Transforming corners between sensors is more general than keeping a simple yaw: an extrinsic with roll or pitch can produce a box that is no longer described by a rotation around the single vertical axis of the target coordinate frame. A test with all distinct dimensions and non-zero rotation makes visible permutations, angle sign and loss of information when converting to a simplified box.

### CV-POSE3D-003

**Situation** : Why is nuScenes 3D AP not directly comparable with COCO bounding-box AP?

**Counter-example of geometry**: A prediction may have the exact center but doubled dimensions and a wrong yaw. A matching per center distance can still accept it according to its threshold, while a volume overlap can be bad. The nuScenes protocol reports other errors to characterize size, orientation, and movement; these must be read with the AP. Conversely, a small metric offset represents a very different part of a pedestrian and a large vehicle. Thresholds and classes therefore define what the measure prefers. Check a few built boxes before interpreting an aggregate score change.

### CV-POSE3D-004

**Situation**: A cylindrical object is localized correctly, but its rotation around the cylinder axis varies. What should be checked?

**Equivalence of poses**: If $S$ belongs to the symmetry group of the model, the poses $T$ and $TS$ can represent the same observable object. A suitable error can minimize a geometric distance on these symmetries, instead of arbitrarily comparing two single matrices. The symmetry of the complete mesh and the indistinguishability of the only visible surfaces are not exactly the same notion; the protocol must specify the one it deals with. An observed marking may reduce the relevant group of symmetries. The validation must then take into account this new information and not maintain an equivalence tolerance that would hide an angle that has become effectively observable.

**Passages consulted for these developments**: [BOP](https://bop.felk.cvut.cz/tasks/), Model-based 6D localization, pose definition and VSD/MSSD/MSPD errors; build boxes and project examples.

## Sources and flashcards

- [BOP, VSD/MSSD/MSPD tasks and metrics](https://bop.felk.cvut.cz/tasks/), accessed 2026-10-20: symmetries and visibility.
- [OpenPose, summary and fig. 2](https://arxiv.org/abs/1611.08050): points and association for the articulated pose 2D.

- [PointPillars, architecture](https://arxiv.org/abs/1812.05784).
- [CenterPoint, method](https://arxiv.org/abs/2006.11275).
- [nuScenes, detection evaluation](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
- [Related flashcards](../84-detection-pose-3d.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
