# Flashcards — Global registration and local ICP

reference note: [[60-vision-3d/references/62-recalage-global-icp|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-ICP-001

Objective: separate global initialization and refinement. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-001
Question: Why combine FPFH/RANSAC with subsequent ICP instead of initializing ICP from any arbitrary pose?
Reponse: **Expected answer**: The global initialization looks for a compatible zone from matches; ICP refines locally and can converge on bad associations.

**Further explanation**: FPFH describes the geometry; the pose must be estimated and then validated. Success also depends on overlap and symmetries.

**Why the initialization counts**: ICP builds or updates associations from the current pose. If this pose is far away, the nearest neighbors can represent other surfaces; optimizing on these pairs can reinforce a local misalignment. Global research uses other clues to propose a region of pose before refinement.

**Constructed example**: Two identical supports on a part can offer two plausible local alignments. A weak residual after ICP does not automatically indicate the correct support. check final orientation and translation, covering and reserved distinctive surfaces. Record direction source→target and units before any comparison. The geometric features and RANSAC provide useful hypotheses; they remain limited by geometric texture, symmetry and overlap. An odometry or business constraint can provide another initialization if it is justified and evaluated.

**Concrete local loop**: At iteration $k$, transform each source point by $T_k$, search for target neighbors, reject incompatible pairs, and then estimate a $\Delta T_k$ fix. With a correction expressed in the target coordinate frame, dial $T_{k+1}=\Delta T_kT_k$. A correction in the source coordinate frame consists of the other side: mixing these conventions produces a poor optimization trajectory. The rapprochement of the neighbors and the resolution of pose are two different steps. A good initialization facilitates physical associations, while a threshold that is too wide can accept foreign surfaces and a threshold that is too strict removes the constraints necessary for refinement.

**Blocking errors**: Present ICP as a guaranteed global solver.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, point-to-point and point-to-plane PKI](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::algorithme cv_id::CV-ICP-001 provenance::agent pole::B pole::C
END

## CV-ICP-002

Objective: interpret a residual point-to-plane. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-002
Question: What does $n^T(Rp+t-q)$ measure in point-to-plane ICP?
Reponse: **Expected answer**: The component of the misalignment according to the normal unit target, in unit length.

**Further explanation**: On a plane, a tangent displacement can change little that residual; check observable and pose, not just RMSE.

**Geometric reading**: The $Rp+t-q$ vector is a 3D error between a transformed source point and its target correspondent. The product with the normal retains only its component perpendicular to the local tangent plane. The square of this scalar thus penalizes the gap at this surface in a particular direction.

**Analytical example**: for a normal $(0,0,1)^T$, a displacement of ten centimeters according to $x$ does not directly change this residual, while a displacement according to $z$ changes it. On a scene composed of a single plane, some tangent translations can thus remain poorly constrained. Several surface orientations can provide additional stresses, if the associations and normals are correct. The point-to-plane choice exploits the local structure; it does not transform each match into three independent observations. Check the pose with constraints or a reference that covers useful movements.

**Linearization of the residual**: Put $s=Rp+t$ and apply a small disturbance to the left $s'\simeq s+\delta t+\delta\omega\times s$. The residual becomes $r'\simeq r+n^T\delta t+(s\times n)^T\delta\omega$. Its Jacobian is therefore a line of six components for the order translation then rotation. Stacking these lines directly shows the movements that the scene constrains. For all vertical normals, horizontal translations do not appear in this local model. This derivation assumes fixed matches and normals during the step; updating them to the next iteration makes the overall problem more complex than a single linear system.

**Blocking errors**: Take this scalar for a complete 3D error in all directions.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, point-to-point and point-to-plane PKI](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-ICP-002 provenance::agent pole::B pole::C
END

## CV-ICP-003

Objective: Reject a small, misleading consensus. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-003
Question: ICP reports low RMSE but aligns only a corner of two point clouds. What should be reported?
Reponse: **Expected answer**: Recovery, threshold, distribution of matches and error of pose on independent reference.

**Further explanation**: The RMSE conditions its result to the selected pairs; reducing the consensus can lower the number without improving the task.

**Why the measure can be wrongly improved**: A RMSE calculated on the selected matches summarizes only this set. A very strict threshold can keep a small corner well aligned and exclude almost everything else. The number then decreases without the pose explaining the important part of the scene.

**Proposed comparison**: announce threshold, units, number and distribution of pairs, recovery proportion according to protocol convention, then transformation error when reference exists. View unexplained regions and test the same settings on reserved scenes. If the piece is symmetrical, consider distinctive coordinate framess or additional stresses. The quality of a local adjustment is not the quality of the entire registration: it is necessary to define the useful area and what a failure costs the system before classifying two poses on a scalar.

**Effect of the threshold on statistics**: if the distances are $d_1,\ldots,d_m$, the RMSE is $\sqrt{\sum_i d_i^2/m}$. Removing all large distances can reduce it while greatly reducing $m$; the two experiments no longer focus on the same points. Also comparing the two directions source→target and target→source can reveal asymmetrical coverage, especially with different densities. An analysis by reserved physical regions prevents a dense area from dominating the score. These measurements complete the reference error of pose; they do not, on their own, remove the ambiguity of a perfectly symmetrical object.

**Blocking errors**: Classify the pose to RMSE alone.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, point-to-point and point-to-plane PKI](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-ICP-003 provenance::agent pole::B pole::C
END

## CV-ICP-004

Objective: keep the units of the registration. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-004
Question: Why does reusing an ICP threshold of 0.02 after converting point clouds from meters to millimeters change the problem?
Reponse: **Expected answer**: Threshold is a length in the unit of coordinates; the scale must be propagated to the relevant parameters.

**Further explanation**: Check voxel and neighborhoods too, then the noise pattern.

**Calculation of scale**: 0,02 m corresponds to 20 mm. If the coordinates are multiplied by a thousand but the threshold remains numerically 0,02, the permissible radius becomes a thousand times smaller in the physical scene. The number of matches and optimization behavior can change abruptly.

**check complete**: convert together the coordinates, translations, voxel sizes and neighbor radii expressed in length. Rotations remain unitless, while quadratic costs follow the square of the scale. In a constructed example, applying the same registration before and after consistent conversion must describe the same physical transformation, with numerical effects to the nearest. Check this simple case before changing the stop criteria or initialization. A normalization of the data must therefore be a traced contract transformation, not an isolated modification of the entry points.

**residuals and covariance**: if all lengths are multiplied by $a$, a metric residual becomes $r'=ar$ and its covariance becomes $\Sigma'=a^2\Sigma$. The normalized residual $r^T\Sigma^{-1}r$ then remains invariant. A robust loss set in meters also requires a converted scale, unlike a loss applied after properly processed whitening. Absolute displacement or cost tolerances can change direction with units; relative criteria must be interpreted according to their exact definition. This reasoning makes it possible to distinguish a coherent unit change from a voluntary change in physical weighting in a registration or a merger of constraints.

**Blocking errors**: Treat the threshold as a unitless number.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, point-to-point and point-to-plane PKI](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::pratique cv_id::CV-ICP-004 provenance::agent pole::B pole::C
END

## CV-ICP-005

Objective: Choose an ICP variant. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-005
Question: Is point-to-plane ICP always a better replacement for point-to-point ICP?
Reponse: **Expected answer**: It exploits reliable normals and a geometry that constrains useful movements; it can be poorly placed on certain surfaces or normal noise.

**Further explanation**: Compare initialization, normal estimation, and accuracy of pose in the target protocol.

**Comparison of the information used**: point-to-point penalizes a difference of positions according to three components; point-to-plane uses a local surface approximation. When normals and initialization are adjusted, this approximation can be effective. If the normals are unstable or the geometry poor, the criterion may lose its interest or leave some directions little constrained.

**Ablation construite**: keep clouds, initial matches, threshold and reference, then compare variants by varying the noise of normals and overlap separately. Measure pose error, convergence, failures and cost. A drop in the residual specific to one variant is not directly comparable to the residual of another formulation. The right choice depends on the observed surface area and the accuracy required. Do not use a single favorable plan case to advertise superiority over all coins and all initializations.

**Where do the normals come from**: A current local estimator centers the neighbors, calculates their covariance matrix and takes the eigenvector of smallest eigenvalue as the plane normal. A neighborhood too small becomes sensitive to noise; too large, it mixes edges and curved surfaces. If eigenvalues do not distinguish a normal direction, the local surface is itself ambiguous. For the residual point-to-plane isolated square, reversing the sign of a normal does not change the cost; a consistent orientation may nevertheless be required by other steps such as descriptors or rejection rules. Compare the quality of pose with this provenance of the explained normals.

**Blocking errors**: Announce universal domination of a variant.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, point-to-point and point-to-plane PKI](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-ICP-005 provenance::agent pole::B pole::C
END
