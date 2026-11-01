# Flashcards — 3D detection, object pose and articulated pose

reference note: [[80-detection-pose/references/84-detection-pose-3d|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-POSE3D-001

Objective: name the output of pose. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-001
Question: Why should a 3D detection score not be compared directly with articulated-pose error?
Reponse: **Expected answer**: Boxes/classes and joints are different outputs with different annotations, matches and metrics.

**Further explanation**: Define the deliverable, coordinate frame, visibility and alignment before choosing the measurement.

**Difference of unknowns**: A 3D detection usually provides location, dimensions, and box orientation with a class. An articulated pose describes joint positions and their relationships; a rigid object pose connects a model to an observation. These outputs do not code the same geometry.

**Constructed example**: A box surrounding a pedestrian does not say where his wrists are. A well-fitting skeleton does not necessarily provide a metric 3D box in the coordinate frame sensor. First define the information consumed by the downstream module, its units and the processing of invisible points. Then choose the matches and alignment allowed in the evaluation. A comparison of heterogeneous scores can be misleading even when all articles use the word pose. A measure must be interpreted by its protocol, not by its title alone.

The reference and the unit must be chosen according to the information that the consumer actually uses.

**Define the comparative quantity**: An average 3D joint error can write $J^{-1}\sum_j\|\hat p_j-p_j\|$ in a length unit, with visible joints or all joints according to protocol. Allowing rigid alignment or similarity removes some errors and changes the evaluated question. A AP of boxes, it, depends on a threshold of matching and the ranking of the scores. A rigid object pose estimates $R,t$ of a known model, while a skeleton estimates several related points. Specifying these unknowns and allowed transformations avoids comparing two digits, one of which has precisely neutralized the defect as the other measures.

**Blocking errors**: Assimilate any problem called pose to the same metric.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [CenterPoint, summary and §4](https://arxiv.org/abs/2006.11275); [OpenPose, summary and fig. 2](https://arxiv.org/abs/1611.08050); [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-POSE3D-001 provenance::agent pole::A pole::C
END

## CV-POSE3D-002

Objective: check a box 3D. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-002
Question: What should be checked when 3D boxes have correct centers but inconsistent orientations or dimensions?
Reponse: **Expected answer**: coordinate frame, center anchor, dimension order, yaw axis/sign and radians/degrees.

**Further explanation**: Test a known box and its transformation between sensors; the problem can be a data contract.

**Example of a convention**: Swapping length and width can make a box turn a quarter turn, while its center remains correct. A defined center on the ground and a geometric center can also differ in height. These errors are located at the interface between representation and system, without requiring a feature defect.

**check**: build an asymmetric box of known dimensions, transform it between coordinate frames and return to the original coordinate frame. Check its corners, the axis of rotation, the direction of the yaw and the angle unit. Using an asymmetrical shape avoids masking a permutation. Then compare to the exact conventions of the dataset and visualization. A plausible rendering on an almost symmetrical car is not enough. Once the conventions are validated, analyze the model errors on reserved annotations.

Comparing the corners after round trip makes it possible to verify this consistency independently of a network.

**Construction of corners**: for a geometric center $c$, dimensions $(l,w,h)$ and rotation $R$, the eight corners are $c+R(\pm l/2,\pm w/2,\pm h/2)^T$. If the center is anchored to the ground, the vertical component must be adjusted before using this formula. Transforming corners between sensors is more general than keeping a simple yaw: an extrinsic with roll or pitch can produce a box that is no longer described by a rotation around the single vertical axis of the target coordinate frame. A test with all distinct dimensions and non-zero rotation makes visible permutations, angle sign and loss of information when converting to a simplified box.

**Blocking errors**: Retract without check the box convention.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; Diagnostic of conventions proposed by the project; [nuScenes, format and metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), consulted the 2026-10-20; [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), consulted the 2026-10-30.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-POSE3D-002 provenance::agent pole::A pole::C
END

## CV-POSE3D-003

Objective: distinguish nuScenes and COCO. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-003
Question: Why is nuScenes 3D AP not directly comparable with COCO bounding-box AP?
Reponse: **Expected answer**: The nuScenes association uses ground center distances and a specific protocol; COCO bbox uses overlaps and its own rules.

**Further explanation**: NDS also combines geometric/dynamic attribute errors; naming version, filters, and units.

**What the matching changes**: a distance criterion between centres on the ground does not penalize dimensions and orientation in the same way as a cover of boxes. Errors can therefore be addressed in other terms or benchmark indicators. The same word AP does not make the notion of true positive and its conditions identical.

**Proposed comparison**: Record matching classes, distance filters, units, thresholds, and rules in the protocol version, and then test some known predictions. Separately examine position, orientation, size and other attributes useful to the product. An improvement to the AP does not automatically guarantee a better geometry of all attributes. Do not copy a COCO threshold because it has a familiar name; choose a measure that is appropriate to the contract of the 3D output and announce what it does not test.

**Counter-example of geometry**: A prediction may have the exact center but doubled dimensions and a wrong yaw. A matching per center distance can still accept it according to its threshold, while a volume overlap can be bad. The nuScenes protocol reports other errors to characterize size, orientation, and movement; these must be read with the AP. Conversely, a small metric offset represents a very different part of a pedestrian and a large vehicle. Thresholds and classes therefore define what the measure prefers. Check a few built boxes before interpreting an aggregate score change.

**Blocking errors**: Transpose the IoU COCO thresholds to any 3D benchmark.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [nuScenes, Average Precision metric and nuScenes detection score](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), accessed on 2026-10-20; [COCO bbox](https://cocodataset.org/#detection-eval); [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), accessed on 2026-10-30.
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-POSE3D-003 provenance::agent pole::A pole::C
END

## CV-POSE3D-004

Objective: respect the symmetries of pose. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-004
Question: A cylindrical object is localized correctly, but its rotation around the cylinder axis varies. What should be checked?
Reponse: **Expected answer**: Visual symmetry and the definition of pose/evaluation: this component can be ambiguous with available observations.

**Further explanation**: Add a distinctive index if the product requires this angle; a more accurate solver does not create a visible absent coordinate frame.

**Intuition of Identifiable**: If several rotations of the object produce the same appearance under the available observations, the vision can not always choose a single orientation. The evaluation model must then specify how the symmetries are processed and which parts of the pose remain observable.

**Constructed example**: A cylinder without a distinctive mark can be invariant to a rotation around its axis. Visible marking may break this ambiguity; better optimization alone does not make it appear. If an assembly step requires this angle, provide additional information and measure it. A box oriented or a low pose score is not enough to slice a symmetrical degree of freedom. Reporting convention and uncertainty avoids arbitrarily penalizing visually equivalent solutions or, conversely, masking an observable error on a marked object.

**Equivalence of poses**: If $S$ belongs to the symmetry group of the model, the poses $T$ and $TS$ can represent the same observable object. A suitable error can minimize a geometric distance on these symmetries, instead of arbitrarily comparing two single matrices. The symmetry of the complete mesh and the indistinguishability of the only visible surfaces are not exactly the same notion; the protocol must specify the one it deals with. An observed marking may reduce the relevant group of symmetries. The validation must then take into account this new information and not maintain an equivalence tolerance that would hide an angle that has become effectively observable.

**Blocking errors**: Declare any variation of a symmetrical angle as an observable error.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [BOP, VSD/MSSD/MSPD metrics and symmetries](https://bop.felk.cvut.cz/tasks/), see 2026-10-20; application to cylinder: project reasoning.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-POSE3D-004 provenance::agent pole::A pole::C
END
