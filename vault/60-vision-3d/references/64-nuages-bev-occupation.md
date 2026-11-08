---
id: CV-BEV
type: comparaison
domaine: d06
poles: [C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SE3", "CV-CAPTEURS", "CV-MULTICALIB"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Point clouds, BEV and occupancy representations

## Problem, data and assumptions

Representing the environment for robotic perception. Distinguish between irregular clouds, voxels, pillars, tensor BEV and semantic volume. Inputs: synchronized points/images and poses; output: representation with resolution, visibility and coordinate frame explained.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md); [CV-MULTICALIB](../../50-calibration-geometrie/references/55-calibration-multicapteurs.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

PointNet++ aggregates point neighborhoods; voxels/pillars organize the space. Lift-Splat-Shoot projects image features in a spatial coordinate frame with depth assumptions; BEVFormer aggregates views and time; BEVFusion combines modalities according to its design. These methods do not make calibration optional.

## Mathematics, conventions and units

A grid uses a cell size in meters and an origin/extension. Probabilistic mapping separates free, busy, and unknown. An Occupancy Network approximates a continuous indoor/outdoor function; a SDF uses a signed distance and a zero-level surface. None of these representations is automatically a calibrated probability of collision.

## Parameters and properties

Resolution, spatial limits, ego compensation, visibility masks and classes must be chosen. Increasing fineness increases memory and sparsity; an unobserved voxel does not become free by default.

## Cost and implementation

Cost of points, dense/split volume and time windows; transfers and merge count. No model BEV or robot executed.

## Evaluation and controlled variation

Proposed variation: mask a sensor or increase the time offset by keeping the scene and model fixed. Measure coverage, duplicates, and errors per distance, including unknown space.

## Failure modes and diagnosis

Ghost objects: check for synchronization and ego-motion. empty map: check axes, ROI, units and FOV. Free traversability requires more than a detected box absence.

## Alternatives and applications

geometric occupancy map, semantic prediction, reconstructed surface and list of objects fill separate contracts; the choice depends on the downstream interface.

## Guided reasoning and proposed checks

These constructed cases develop visibility, unknown and limits of spatial representation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-BEV-001

**Question of work**: Why do a vertical pillar and a 3D voxel preserve different spatial organization?

**Reference Response**: The voxel also discretizes the height; the pillar groups the points of a column, then encoded in pseudo-image.

**Reading of representations**: a grid of voxels discretizes the three spatial dimensions; a pillar groups a vertical column before producing features. A pseudo-image BEV then organizes information in the horizontal plane. The grouping can encode the height without keeping an explicit box for each altitude.

**Constructed example**: a low obstacle and a height structure can occupy the same horizontal coordinates. Their distinction depends on the vertical information actually retained and exploited, not on the single word BEV. Set origin, resolution in meters, extent, and coordinate frame before comparing tensors. A BEV from cameras also requires projection and depth assumptions. The choice of representation is therefore a compromise between information, memory, calculation and perception interface, and not a simple universal conversion of a cloud into an image.

### Case linked to CV-BEV-005

**Question of work**: Track C — design: a warehouse robot uses cameras and LiDAR. Which perception interface and evaluation protocol should be built?

**Reference Response**: Define expected objects/occupation, coordinate frames/time, visibility and uncertainty; design fusion and behavior in case of loss and then test rare obstacles, occlusions and latency.

**Proposed interface**: provide for each output the coordinate frame, the time of validity, the observed area, the classes or occupancy states and an indication of usable uncertainty. Predict what happens if a sensor disappears or the data becomes old. A list of boxes and a map of free space do not meet the same need.

**Transfer Protocol**: build cases with partially hidden obstacle, rare object, low-reflective material and controlled desynchronization. Measure errors by distance, unknown areas wrongly treated as free, and end-to-end latency. Compare single terms and merger to identify the actual contribution of each. The criteria are those of the collection and its contract; the validation of the order and the global security requires a separate perimeter and is not deducted from an average AP.

**Documentary reference for this pass**: [OctoMap, documentation officielle](https://octomap.github.io/octomap/doc/index.html), presentation of the probabilistic occupation model. The other developments are in the [flashcards](../64-nuages-bev-occupation.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-BEV-001

**Situation**: Why do a vertical pillar and a 3D voxel preserve different spatial organization?

**Cost of discretization**: for a range $L_x\times L_y\times L_z$ and cells $\Delta x,\Delta y,\Delta z$, a dense volume contains about $(L_x/\Delta x)(L_y/\Delta y)(L_z/\Delta z)$ cells. Divide each step by two multiplies their number by eight; a horizontal grid alone is multiplied by four. The actual memory still depends on the channels, the precision and the sparse representation. The horizontal index of a point can be $i=\lfloor(x-x_{\min})/\Delta x\rfloor$ with out-of-ROI rejection. Defining this rounding and the convention of the terminals avoids the shifts of a cell between labels, sensors and network outputs.

### CV-BEV-002

**Situation**: Why does the absence of a return or detection not establish that a volume is free?

**Radius Model**: a geometric feedback can inform the space traversed before impact as free and a region near impact as occupied, under the model of the sensor. The portion behind the impact remains hidden. Beam width, distance uncertainty and moving objects limit this interpretation. In a binary probabilistic update, log-odds $\ell=\log(p/(1-p))$ make it possible to add the information of the measurements according to the assumptions of independence and the prior. Repeating a correlated measure does not create as much independent information. The map must therefore retain provenance, visibility and seniority, in addition to the occupancy value.

### CV-BEV-003

**Situation**: How does a robotic occupancy grid differ from an Occupancy Network for reconstruction?

**Surface and units**: For an implicit occupation function $o_\theta(x)$, a surface is extracted at a selected level $o_\theta(x)=\tau$. For an ideal SDF $s(x)$, the surface is $s(x)=0$ and $|s(x)|$ represents a distance, according to the sign convention. Far from singularities, a true signed distance satisfies $\|\nabla s\|=1$; a learned function does not automatically ensure this property. The coordinates can be normalized during learning: returning to the meters requires the corresponding transformation. A plausible surface level therefore does not validate the metric distances or the probabilistic calibration of an output used by another module.

### CV-BEV-004

**Situation**: BEV objects are localized correctly at rest but displaced during rotation. Which data should be examined?

**Aligning the historical**: If $T_{w\leftarrow e(t)}$ gives the coordinate frame ego to the time $t$ in the world, a historical point is transported to the current time by $p_{e(t)}=T_{w\leftarrow e(t)}^{-1}T_{w\leftarrow e(t_0)}p_{e(t_0)}$. This compensation assumes the static point in the world. A moving pedestrian retains a residual displacement after correction of the ego-motion; treating it as an extrinsic defect would be another confusion. check first static structures, and then parse the moving objects separately. The time per point of a scan may require several transformations, and not a single pose for the entire frame, when the movement during the acquisition is significant.

### CV-BEV-005

**Situation**: Track C — design: a warehouse robot uses cameras and LiDAR. Which perception interface and evaluation protocol should be built?

**Testable Grid Contract**: accompany the tensor of its origin, its axes, its resolution, its terminals, its timestamp and its visibility mask. For a cell declared free, to be able to link the decision to observations that really forced this region. A constructed test places an obstacle behind a pallet, then changes the point of view: the cell must go from unknown to observed according to the new measurements, without considering the initial vacuum of the tensor as evidence. Also assess the shelf life of moving obstacles and the response to outdated data. These tests verify the semantics of the interface, beyond the average accuracy of the boxes.

**Passages consulted for these developments**: [OctoMap](https://octomap.github.io/), Full 3D model, free/occupied/unknown space; [Li et al., BEVFormer](https://arxiv.org/html/2203.17270v2), §3.4, time history; transformations and tests derived by the project.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-BEV-001 — A pillar can encode height without retaining height cells

A pillar encoder may include point heights and relative offsets in its learned features, so collapsing the grid's vertical axis does not mean all height information is absent. What changes is the explicit spatial organization and the bottleneck through which vertical structure is represented. Compare two objects stacked in the same horizontal cell as a constructed stress case, rather than concluding from the word BEV that every method preserves or discards the same information.

### CV-BEV-002 — Repeated absence needs a visibility model

If an opaque obstacle blocks a ray, repeated scans from the same viewpoint do not directly observe the region behind it. Treating every missing return as free would become more confident in an unsupported conclusion with each repetition. A proposed mapping check distinguishes traversed free space, a supported surface hit and unobserved space behind it. Sensor range, transparent materials and invalid returns require their own measurement assumptions.

### CV-BEV-003 — An inside probability is not a signed distance

A value from an occupancy classifier does not directly give meters to the nearest surface. A signed distance function additionally encodes distance under its modeling assumptions; a reconstructed implicit function need not be an exact distance field everywhere. Collision checking based on a distance margin therefore requires the right output contract and validation. Likewise, learned shape completion can suggest unseen geometry without converting it into a direct sensor observation.

### CV-BEV-004 — Ego compensation does not make moving objects static

Transforming historical points into the current ego frame corrects the platform's motion under the pose estimate. A moving pedestrian still changes position during the interval, so history can leave multiple positions or a blurred feature footprint. Distinguish ego-motion error from object-motion accumulation with static landmarks and independently moving targets. This proposed check prevents solving a dynamic-scene issue by repeatedly adjusting a fixed sensor extrinsic.

### CV-BEV-005 — The output needs age and unknown-state semantics

A warehouse planner needs to know when evidence was acquired and which cells were unobserved, rather than receiving an undated occupied/free bitmap alone. A project contract can carry frame, timestamp, validity, uncertainty and state-age limits with the geometry. Evaluate thin obstacles, low returns and temporary sensor loss under that contract. Detection AP alone does not measure whether missing or stale observations lead to inappropriate free-space decisions.

Consulted foundations: [OctoMap](https://octomap.github.io/): explicit distinction between occupied, free and unknown space; [PointPillars](https://arxiv.org/pdf/1812.05784): §2 learned pillar encoding and pseudo-image representation; [Occupancy Networks](https://arxiv.org/html/1812.03828v1): §3 continuous inside/outside occupancy function.

## Sources and flashcards

- [Qi et al., PointNet++, summary](https://arxiv.org/abs/1706.02413)
- [Philion – Fidler, Lift-Splat-Shoot, summary](https://arxiv.org/abs/2008.05711)
- [Liu et al., BEVFusion, summary (version v3)](https://arxiv.org/abs/2205.13542)
- [Park et al., DeepSDF, §3](https://arxiv.org/abs/1901.05103)

- [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html).
- [BEVFormer, method](https://arxiv.org/abs/2203.17270).
- [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html).
- [Occupancy Networks, implicit surface](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
- [Related flashcards](../64-nuages-bev-occupation.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
