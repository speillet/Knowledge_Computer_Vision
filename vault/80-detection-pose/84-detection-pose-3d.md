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

**Different unknowns**: A 3D detection usually provides location, dimensions, and box orientation with a class. An articulated pose describes joint positions and their relationships; a rigid object pose connects a model to an observation. These outputs do not code the same geometry.

**Constructed example**: A box surrounding a pedestrian does not say where the pedestrian's wrists are. A well-fitting skeleton does not necessarily provide a metric 3D box in the sensor coordinate frame. First define the information consumed by the downstream module, its units and the treatment of invisible points. Then choose the matches and alignment allowed in the evaluation. A comparison of heterogeneous scores can be misleading even when all papers use the word pose. A measure must be interpreted by its protocol, not by its title alone.

The reference frame and the unit must be chosen according to the information that the consumer actually uses.

**Define the compared quantity**: A mean 3D joint error can be written $J^{-1}\sum_j\|\hat p_j-p_j\|$ in a length unit, over visible joints or all joints depending on the protocol. Allowing a rigid or similarity alignment removes some errors and changes the question evaluated. A box AP, by contrast, depends on a matching threshold and on score ranking. A rigid object pose estimates $R,t$ of a known model, while a skeleton estimates several connected points. Specifying these unknowns and the allowed transformations avoids comparing two numbers, one of which has neutralized precisely the defect that the other measures.

**Pose alignment changes the meaning of an error**: Joint-position error after root alignment, rigid alignment or similarity alignment removes different parts of the prediction error. A similarity-aligned articulated pose can look accurate while having the wrong absolute scale or global orientation. State the alignment group and visibility policy alongside units. A 3D detection metric instead requires its own instance matching and box/class definitions; a shared word such as pose does not make the outputs comparable.

**Blocking errors**: Treating every problem called pose as having the same metric.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [CenterPoint, summary and §4](https://arxiv.org/abs/2006.11275); [OpenPose, summary and fig. 2](https://arxiv.org/abs/1611.08050); [Martinez et al., §4: Human3.6M protocols #1 and #2](https://arxiv.org/html/1705.03098v2); [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-POSE3D-001 provenance::agent pole::A pole::C
END

## CV-POSE3D-002

Objective: Check a 3D box. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-002
Question: What should be checked when 3D boxes have correct centers but inconsistent orientations or dimensions?
Reponse: **Expected answer**: coordinate frame, center anchor, dimension order, yaw axis/sign and radians/degrees.

**Further explanation**: Test a known box and its transformation between sensors; the problem can be a data contract.

**Example of a convention**: Swapping length and width can make a box look rotated by a quarter turn, while its center remains correct. A defined center on the ground and a geometric center can also differ in height. These errors are located at the interface between representation and system, without requiring a feature defect.

**Proposed check**: Build an asymmetric box of known dimensions, transform it between coordinate frames and return to the original frame. Check its corners, the axis of rotation, the direction of the yaw and the angle unit. Using an asymmetric shape avoids masking a permutation. Then compare with the exact conventions of the dataset and of the visualization. A plausible rendering on an almost symmetric car is not enough. Once the conventions are validated, analyze the model errors on held-out annotations.

Comparing the corners after a round trip verifies this consistency independently of any network.

**Construction of corners**: for a geometric center $c$, dimensions $(l,w,h)$ and rotation $R$, the eight corners are $c+R(\pm l/2,\pm w/2,\pm h/2)^T$. If the center is anchored to the ground, the vertical component must be adjusted before using this formula. Transforming corners between sensors is more general than keeping a simple yaw: an extrinsic with roll or pitch can produce a box that is no longer described by a rotation around the single vertical axis of the target coordinate frame. A test with all distinct dimensions and non-zero rotation makes visible permutations, angle sign and loss of information when converting to a simplified box.

**Dimension swaps can pass a center-only check**: Constructed example: a box with dimensions $(4,2,1)$ m and zero yaw occupies a different region from one with dimensions $(2,4,1)$ m, despite an identical center. A yaw convention change can partly hide that swap on selected examples. Compare all eight transformed corners against known axes and a non-square box. Include a nonzero yaw and explicit center-versus-bottom anchor so identity cases do not conceal interface errors.

**Blocking errors**: Retraining without checking the box convention.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; Diagnostic of conventions proposed by the project; [nuScenes, format and metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), consulted the 2026-10-20; [nuScenes devkit b40adc4, results format: size as width, length, height](https://github.com/nutonomy/nuscenes-devkit/blob/b40adc467b919192899405d9b77871afee8efa07/python-sdk/nuscenes/eval/detection/README.md#results-format), consulted 2026-11-14; [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-POSE3D-002 provenance::agent pole::A pole::C
END

## CV-POSE3D-003

Objective: distinguish nuScenes and COCO. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-003
Question: Why is nuScenes 3D AP not directly comparable with COCO bounding-box AP?
Reponse: **Expected answer**: nuScenes matching uses 2D center distances on the ground plane and a specific protocol; COCO bbox matching uses overlaps (IoU) and its own rules.

**Further explanation**: NDS also combines geometric and dynamic attribute errors; name the version, filters and units.

**What the matching changes**: A distance criterion between centres on the ground does not penalize dimensions and orientation in the same way as a box overlap does. These errors are therefore captured by other terms or indicators of the benchmark. The same word AP does not make the notion of true positive and its conditions identical.

**Proposed comparison**: Record matching classes, distance filters, units, thresholds, and rules in the protocol version, and then test some known predictions. Separately examine position, orientation, size and other attributes useful to the product. An improvement to the AP does not automatically guarantee a better geometry of all attributes. Do not copy a COCO threshold because it has a familiar name; choose a measure that is appropriate to the contract of the 3D output and announce what it does not test.

**Geometric counter-example**: A prediction may have the exact center but doubled dimensions and a wrong yaw. Center-distance matching can still accept it, depending on its threshold, while the volume overlap can be poor. The nuScenes protocol reports other errors to characterize size, orientation and motion; these must be read together with the AP. Conversely, the same metric offset represents a very different fraction of a pedestrian and of a large vehicle. Thresholds and classes therefore define what the measure favours. Check a few constructed boxes before interpreting a change of an aggregate score.

**Localization matching leaves other box errors to other metrics**: A prediction with the correct ground-plane center can pass a center-distance match while having poor dimensions, yaw or velocity. nuScenes reports additional true-positive error terms for such properties, so its AP should be interpreted within that full protocol. COCO box IoU incorporates extent overlap directly in matching. Neither score alone establishes suitability for collision geometry or fine pose control without a task-specific error tolerance.

**Blocking errors**: Transposing COCO IoU thresholds to any 3D benchmark.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [nuScenes, Average Precision metric and nuScenes detection score](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), accessed on 2026-10-20; [COCO bbox](https://cocodataset.org/#detection-eval); [BOP, Model-based 6D localization, pose definition, and VSD/MSSD/MSPD errors; building boxes and project examples](https://bop.felk.cvut.cz/tasks/), accessed on 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-POSE3D-003 provenance::agent pole::A pole::C
END

## CV-POSE3D-004

Objective: respect the symmetries of pose. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-POSE3D-004
Question: A cylindrical object is localized correctly, but its rotation around the cylinder axis varies. What should be checked?
Reponse: **Expected answer**: Visual symmetry and the definition of pose/evaluation: this component can be ambiguous with available observations.

**Further explanation**: Add a distinctive mark if the product requires this angle; a more accurate solver does not create a visible landmark that is absent.

**Identifiability intuition**: If several rotations of the object produce the same appearance under the available observations, vision cannot always choose a single orientation. The evaluation model must then specify how symmetries are handled and which parts of the pose remain observable.

**Constructed example**: A cylinder without a distinctive mark can be invariant to a rotation around its axis. Visible marking may break this ambiguity; better optimization alone does not make it appear. If an assembly step requires this angle, provide additional information and measure it. An oriented box or a low pose score is not enough to settle a symmetric degree of freedom. Reporting the convention and the uncertainty avoids arbitrarily penalizing visually equivalent solutions or, conversely, masking an observable error on a marked object.

**Equivalence of poses**: If $S$ belongs to the symmetry group of the model, the poses $T$ and $TS$ can represent the same observable object. A suitable error can minimize a geometric distance over these symmetries, instead of arbitrarily comparing two single matrices. The symmetry of the complete mesh and the indistinguishability of the visible surfaces alone are not exactly the same notion; the protocol must specify which one it uses. An observed marking may reduce the relevant symmetry group. The validation must then take this new information into account and not keep an equivalence tolerance that would hide an angle that has become observable.

**Blocking errors**: Declaring any variation of a symmetric angle an observable error.
Source: [[80-detection-pose/references/84-detection-pose-3d|Full reference]]; [BOP, VSD/MSSD/MSPD metrics and symmetries](https://bop.felk.cvut.cz/tasks/), see 2026-10-20; [BOP 2020, §2.3: symmetries not resolved by texture](https://arxiv.org/html/2009.07378v2); application to cylinder: project reasoning.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-POSE3D-004 provenance::agent pole::A pole::C
END
