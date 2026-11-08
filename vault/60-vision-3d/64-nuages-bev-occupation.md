# Flashcards — Point clouds, BEV and occupancy representations

reference note: [[60-vision-3d/references/64-nuages-bev-occupation|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-BEV-001

Objective: distinguish voxel pillar and BEV. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-BEV-001
Question: Why do a vertical pillar and a 3D voxel preserve different spatial organization?
Reponse: **Expected answer**: The voxel also discretizes the height; the pillar groups the points of a column, then encoded in pseudo-image.

**Further explanation**: A BEV representation may come from images or LiDAR; it does not identify a single modality.

**Reading of representations**: a grid of voxels discretizes the three spatial dimensions; a pillar groups a vertical column before producing features. A pseudo-image BEV then organizes information in the horizontal plane. The grouping can encode the height without keeping an explicit box for each altitude.

**Constructed example**: a low obstacle and a height structure can occupy the same horizontal coordinates. Their distinction depends on the vertical information actually retained and exploited, not on the single word BEV. Set origin, resolution in meters, extent, and coordinate frame before comparing tensors. A BEV from cameras also requires projection and depth assumptions. The choice of representation is therefore a compromise between information, memory, calculation and perception interface, and not a simple universal conversion of a cloud into an image.

**Cost of discretization**: for a range $L_x\times L_y\times L_z$ and cells $\Delta x,\Delta y,\Delta z$, a dense volume contains about $(L_x/\Delta x)(L_y/\Delta y)(L_z/\Delta z)$ cells. Divide each step by two multiplies their number by eight; a horizontal grid alone is multiplied by four. The actual memory still depends on the channels, the precision and the sparse representation. The horizontal index of a point can be $i=\lfloor(x-x_{\min})/\Delta x\rfloor$ with out-of-ROI rejection. Defining this rounding and the convention of the terminals avoids the shifts of a cell between labels, sensors and network outputs.

**A pillar can encode height without retaining height cells**: A pillar encoder may include point heights and relative offsets in its learned features, so collapsing the grid's vertical axis does not mean all height information is absent. What changes is the explicit spatial organization and the bottleneck through which vertical structure is represented. Compare two objects stacked in the same horizontal cell as a constructed stress case, rather than concluding from the word BEV that every method preserves or discards the same information.

**Blocking errors**: Say that any BEV is an identical flattened LiDAR cloud.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Full reference]]; [Lang et al., PointPillars, §2.1](https://arxiv.org/abs/1812.05784); [Li et al., BEVFormer, §§3.3 – 3.4](https://arxiv.org/abs/2203.17270); [OctoMap, Full 3D model, free/occupied/unknown space](https://octomap.github.io/); [Li et al., BEVFormer, §3.4, temporal history; transformations and tests derived by the project](https://arxiv.org/html/2203.17270v2), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-BEV-001 provenance::agent pole::C
END

## CV-BEV-002

Objective: Preserving the unknown. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-BEV-002
Question: Why does the absence of a return or detection not establish that a volume is free?
Reponse: **Expected answer**: The area may be masked, out of range or never observed; free and unknown must be distinguished according to the measurement model.

**Further explanation**: Measure visibility and raycasting; a downstream interface must know which regions have actually been constrained.

**Reasoning for observation**: Not seeing a return can mean no obstacle, occlusion by another object, insufficient reach or difficult material. These causes do not have the same implication on space. A free representation must be based on a measurement model and an area actually observed.

**Constructed example**: behind a detected pallet, a region without a LiDAR point has not been crossed by a free observation; it may contain another obstacle. Marking this region as unknown retains useful information for the downstream interface. Test visibility, field limits, and where updates come from instead of filling in any empty free space. The uncertainty of a map and the decisions of displacement remain additional problems: this perception map does not alone certify the traversability or the safety of the whole robot.

**Radius Model**: a geometric feedback can inform the space traversed before impact as free and a region near impact as occupied, under the model of the sensor. The portion behind the impact remains hidden. Beam width, distance uncertainty and moving objects limit this interpretation. In a binary probabilistic update, log-odds $\ell=\log(p/(1-p))$ make it possible to add the information of the measurements according to the assumptions of independence and the prior. Repeating a correlated measure does not create as much independent information. The map must therefore retain provenance, visibility and seniority, in addition to the occupancy value.

**Repeated absence needs a visibility model**: If an opaque obstacle blocks a ray, repeated scans from the same viewpoint do not directly observe the region behind it. Treating every missing return as free would become more confident in an unsupported conclusion with each repetition. A proposed mapping check distinguishes traversed free space, a supported surface hit and unobserved space behind it. Sensor range, transparent materials and invalid returns require their own measurement assumptions.

**Blocking errors**: Assimilate undetected and without obstacle.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Full reference]]; [OctoMap, Full 3D model, viewed on 2026-10-20](https://octomap.github.io/); [Li et al., BEVFormer, §3.4, temporal history; transformations and tests derived by the project](https://arxiv.org/html/2203.17270v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::comprehension cv_id::CV-BEV-002 provenance::agent pole::C
END

## CV-BEV-003

Objective: Separate the sense of occupation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-BEV-003
Question: How does a robotic occupancy grid differ from an Occupancy Network for reconstruction?
Reponse: **Expected answer**: The first represents a belief in observed/free/occupied space; the second models a continuous function inside/outside a form.

**Further explanation**: A SDF represents yet another mathematical object; check signs, units and labels.

**Separate mathematical contracts**: A map of occupation for robotics merges observations and must define what means observed, free or unknown. An implicit representation of form seeks an internal/external boundary in a reconstruction space. A signed distance describes yet another quantity, with a unit of length and a sign convention.

**Constructed example**: A high indoor score of a learned form does not automatically express the probability that a robot will collide there in its current environment. It lacks visibility context, score calibration, robot geometry and validity time. So look at inputs, learning targets, and sense of output before connecting two modules. Representations can be converted or combined, but the interface must explain what information is retained and which is added by a system hypothesis.

**Surface and units**: For an implicit occupation function $o_\theta(x)$, a surface is extracted at a selected level $o_\theta(x)=\tau$. For an ideal SDF $s(x)$, the surface is $s(x)=0$ and $|s(x)|$ represents a distance, according to the sign convention. Far from singularities, a true signed distance satisfies $\|\nabla s\|=1$; a learned function does not automatically ensure this property. The coordinates can be normalized during learning: returning to the meters requires the corresponding transformation. A plausible surface level therefore does not validate the metric distances or the probabilistic calibration of an output used by another module.

**An inside probability is not a signed distance**: A value from an occupancy classifier does not directly give meters to the nearest surface. A signed distance function additionally encodes distance under its modeling assumptions; a reconstructed implicit function need not be an exact distance field everywhere. Collision checking based on a distance margin therefore requires the right output contract and validation. Likewise, learned shape completion can suggest unseen geometry without converting it into a direct sensor observation.

**Blocking errors**: Use the score of an implied shape as a calibrated collision probability.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Full reference]]; [OctoMap, Full 3D model, viewed on 2026-10-20](https://octomap.github.io/); [Mescheder et al., Occupancy Networks, §3.1](https://arxiv.org/abs/1812.03828); [Park et al., DeepSDF, §3](https://arxiv.org/abs/1901.05103); [Li et al., BEVFormer, §3.4, temporal history; transformations and tests derived by the project](https://arxiv.org/html/2203.17270v2), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-BEV-003 provenance::agent pole::C
END

## CV-BEV-004

Objective: check a BEV merge. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-BEV-004
Question: BEV objects are localized correctly at rest but displaced during rotation. Which data should be examined?
Reponse: **Expected answer**: Timestamps, ego-motion, deskew and transformation to the coordinate frame BEV before changing the architecture.

**Further explanation**: Stratify error by speed, distance and angle; a time offset can hide in static tests.

**Why Movement Reveals Error**: A spatial transformation applied to different time observations does not necessarily place them in the same instant scene. During a rotation of the wearer, the apparent error may depend on the distance and direction observed. Immobility can therefore mask a temporal defect.

**Verification built**: compare sensor alone, static fusion then fusion on controlled translations and rotations. Record capture time, receive time and time per point or frame, then check the direction of the transformations to the BEV. Examine the residuals according to angular velocity. If a temporal correction improves these signatures on a reserved sequence, this supports this cause without excluding a residual spatial defect. Changing the backbone before this check might ask the network to absorb a data inconsistency rather than improve perception.

**Aligning the historical**: If $T_{w\leftarrow e(t)}$ gives the coordinate frame ego to the time $t$ in the world, a historical point is transported to the current time by $p_{e(t)}=T_{w\leftarrow e(t)}^{-1}T_{w\leftarrow e(t_0)}p_{e(t_0)}$. This compensation assumes the static point in the world. A moving pedestrian retains a residual displacement after correction of the ego-motion; treating it as an extrinsic defect would be another confusion. check first static structures, and then parse the moving objects separately. The time per point of a scan may require several transformations, and not a single pose for the entire frame, when the movement during the acquisition is significant.

**Ego compensation does not make moving objects static**: Transforming historical points into the current ego frame corrects the platform's motion under the pose estimate. A moving pedestrian still changes position during the interval, so history can leave multiple positions or a blurred feature footprint. Distinguish ego-motion error from object-motion accumulation with static landmarks and independently moving targets. This proposed check prevents solving a dynamic-scene issue by repeatedly adjusting a fixed sensor extrinsic.

**Blocking errors**: Conclude from the outset to an insufficient capacity of the backbone.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Full reference]]; [Li et al., BEVFormer, §§3.3 – 3.4](https://arxiv.org/abs/2203.17270); temporal diagnosis deduced by the project; [OctoMap, Full 3D model, free/occupied/unknown space](https://octomap.github.io/); [Li et al., BEVFormer, §3.4, temporal history; transformations and tests derived by the project](https://arxiv.org/html/2203.17270v2), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-BEV-004 provenance::agent pole::C
END

## CV-BEV-005

Objective: Designing a warehouse perception. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-BEV-005
Question: Track C — design: a warehouse robot uses cameras and LiDAR. Which perception interface and evaluation protocol should be built?
Reponse: **Expected answer**: Define expected objects/occupation, coordinate frames/time, visibility and uncertainty; design fusion and behavior in case of loss and then test rare obstacles, occlusions and latency.

**Further explanation**: A box absence is not equal to free space; separate perception validation and robot control/safety requirements.

**Proposed interface**: provide for each output the coordinate frame, the time of validity, the observed area, the classes or occupancy states and an indication of usable uncertainty. Predict what happens if a sensor disappears or the data becomes old. A list of boxes and a map of free space do not meet the same need.

**Transfer Protocol**: build cases with partially hidden obstacle, rare object, low-reflective material and controlled desynchronization. Measure errors by distance, unknown areas wrongly treated as free, and end-to-end latency. Compare single terms and merger to identify the actual contribution of each. The criteria are those of the collection and its contract; the validation of the order and the global security requires a separate perimeter and is not deducted from an average AP.

**Testable Grid Contract**: accompany the tensor of its origin, its axes, its resolution, its terminals, its timestamp and its visibility mask. For a cell declared free, to be able to link the decision to observations that really forced this region. A constructed test places an obstacle behind a pallet, then changes the point of view: the cell must go from unknown to observed according to the new measurements, without considering the initial vacuum of the tensor as evidence. Also assess the shelf life of moving obstacles and the response to outdated data. These tests verify the semantics of the interface, beyond the average accuracy of the boxes.

**The output needs age and unknown-state semantics**: A warehouse planner needs to know when evidence was acquired and which cells were unobserved, rather than receiving an undated occupied/free bitmap alone. A project contract can carry frame, timestamp, validity, uncertainty and state-age limits with the geometry. Evaluate thin obstacles, low returns and temporary sensor loss under that contract. Detection AP alone does not measure whether missing or stale observations lead to inappropriate free-space decisions.

**Blocking errors**: Ensure overall security with a single detection metric.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Full reference]]; [OctoMap, Full 3D model, viewed on 2026-10-20](https://octomap.github.io/); design protocol proposed by the project; [Li et al., BEVFormer, §3.4, temporal history; transformations and tests derived by the project](https://arxiv.org/html/2203.17270v2), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-BEV-005 provenance::agent pole::C cas_pole::C::conception
END
