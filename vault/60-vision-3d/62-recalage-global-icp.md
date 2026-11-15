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

**Further explanation**: FPFH describes local geometry; the pose must still be estimated and then validated. Success also depends on overlap and symmetries.

**Why the initialization matters**: ICP builds or updates associations from the current pose. If this pose is far away, the nearest neighbors can belong to other surfaces; optimizing on these pairs can reinforce a local misalignment. Global search uses other cues to propose a pose region before refinement.

**Constructed example**: Two identical supports on a part can offer two plausible local alignments. A small residual after ICP does not by itself indicate the correct support. Check the final orientation and translation, the overlap and held-out distinctive surfaces. Record the source→target direction and the units before any comparison. Geometric features and RANSAC provide useful hypotheses; they remain limited by geometric texture, symmetry and overlap. An odometry or application constraint can provide another initialization if it is justified and evaluated.

**Concrete local loop**: At iteration $k$, transform each source point by $T_k$, search for target neighbors, reject incompatible pairs, and then estimate a correction $\Delta T_k$. With a correction expressed in the target coordinate frame, compose $T_{k+1}=\Delta T_kT_k$. A correction expressed in the source coordinate frame is composed on the other side, $T_{k+1}=T_k\Delta T_k$: mixing these conventions produces an incorrect optimization trajectory. Neighbor matching and pose solving are two different steps. A good initialization makes physically correct associations easier, while a threshold that is too wide can accept foreign surfaces and a threshold that is too strict removes the constraints needed for refinement.

**Global initialization is also a hypothesis**: Repeated geometry can give a plausible global alignment to the wrong copy of a structure. ICP can then reduce local residuals while preserving that incorrect correspondence basin. Validate overlap extent and independently known landmarks after refinement, rather than accepting a lower ICP objective as confirmation of the initializer. In a proposed comparison, include large initial displacements and symmetric alternatives, and report rejected registrations as well as final errors.

**Blocking errors**: Presenting ICP as a solver with a global guarantee.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Besl and McKay 1992, §IV-B and §V](https://doi.org/10.1109/34.121791) ; [Open3D 0.19.0, global registration tutorial, FPFH and RANSAC](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/global_registration.html). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::algorithme cv_id::CV-ICP-001 provenance::agent pole::B pole::C
END

## CV-ICP-002

Objective: interpret a residual point-to-plane. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-002
Question: What does $n^T(Rp+t-q)$ measure in point-to-plane ICP?
Reponse: **Expected answer**: The component of the misalignment along the target's unit normal, in length units.

**Further explanation**: On a plane, a tangential displacement barely changes this residual; check observability and the pose, not just the RMSE.

**Geometric reading**: The vector $Rp+t-q$ is a 3D error between a transformed source point and its target correspondence. The dot product with the normal retains only its component perpendicular to the local tangent plane. The square of this scalar thus penalizes the distance to this surface along one particular direction.

**Analytical example**: For a normal $(0,0,1)^T$, a displacement of ten centimeters along $x$ does not directly change this residual, while a displacement along $z$ changes it. On a scene composed of a single plane, some tangential translations can thus remain poorly constrained. Several surface orientations can provide additional constraints, if the associations and normals are correct. The point-to-plane choice exploits the local structure; it does not turn each match into three independent observations. Check the pose with constraints or a reference that covers the useful motions.

**Linearization of the residual**: Let $s=Rp+t$ and apply a small left perturbation $s'\simeq s+\delta t+\delta\omega\times s$. The residual becomes $r'\simeq r+n^T\delta t+(s\times n)^T\delta\omega$. Its Jacobian is therefore a row of six components, ordered translation then rotation. Stacking these rows shows directly which motions the scene constrains. If all normals are vertical, horizontal translations do not appear in this local model. This derivation assumes fixed matches and normals during the step; updating them at the next iteration makes the overall problem more complex than a single linear system.

**A plane leaves tangential motion unpenalized**: For target normal $n=(0,0,1)^T$, the residual becomes the difference in height. Translating all transformed points parallel to the plane leaves it unchanged, as does rotation about the plane normal for an ideal infinite plane. A small point-to-plane residual can therefore coexist with substantial tangential pose error. This constructed nullspace example motivates inspecting normal diversity and the linearized system, not simply reducing the distance threshold.

**Blocking errors**: Taking this scalar for a complete 3D error in all directions.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Rusinkiewicz and Levoy 2001, §3.5](https://www.cs.princeton.edu/~smr/papers/fasticp/fasticp_paper.pdf) ; [Low 2004, eqs. 4–8](https://www.comp.nus.edu.sg/~lowkl/publications/lowk_point-to-plane_icp_techrep.pdf) ; [Gelfand et al. 2003, §2.2](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-ICP-002 provenance::agent pole::B pole::C
END

## CV-ICP-003

Objective: Reject a small, misleading consensus. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-003
Question: ICP reports low RMSE but aligns only a corner of two point clouds. What should be reported?
Reponse: **Expected answer**: Overlap, threshold, distribution of matches and pose error against an independent reference.

**Further explanation**: The RMSE is conditioned on the selected pairs; shrinking the consensus can lower the number without improving the task.

**Why the measure can be wrongly improved**: An RMSE computed on the selected matches summarizes only this set. A very strict threshold can keep a small corner well aligned and exclude almost everything else. The number then decreases without the pose explaining the important part of the scene.

**Proposed comparison**: Report the threshold, units, number and distribution of pairs, the overlap fraction under the protocol's convention, then the transformation error when a reference exists. Visualize unexplained regions and test the same settings on held-out scenes. If the part is symmetric, consider distinctive landmarks or additional constraints. The quality of a local fit is not the quality of the entire registration: define the useful region and the cost of a failure for the system before ranking two poses by one scalar.

**Effect of the threshold on statistics**: If the distances are $d_1,\ldots,d_m$, the RMSE is $\sqrt{\sum_i d_i^2/m}$. Removing all large distances can reduce it while greatly reducing $m$; the two experiments no longer concern the same points. Comparing the two directions, source→target and target→source, can also reveal asymmetric coverage, especially with different densities. An analysis per predefined physical region prevents a dense area from dominating the score. These measurements complement the pose error against a reference; they do not, on their own, remove the ambiguity of a perfectly symmetric object.

**The denominator can improve the score by exclusion**: Constructed example: retaining 10 close pairs with 1 mm error and rejecting 90 distant points yields 1 mm inlier RMSE but little evidence of whole-cloud alignment. Report accepted-pair fraction, the source/target direction of that fraction, coverage and threshold with RMSE. Evaluate pose error independently where possible. Changing the correspondence threshold changes both the accepted population and its conditional error, so two RMSE values are not automatically comparable.

**Blocking errors**: Ranking poses by RMSE alone.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D v0.19.0, Registration.cpp L59–L67, fitness and inlier RMSE](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.cpp#L59-L67) ; [Rusinkiewicz and Levoy 2001, §2, ground-truth error](https://www.cs.princeton.edu/~smr/papers/fasticp/fasticp_paper.pdf). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-ICP-003 provenance::agent pole::B pole::C
END

## CV-ICP-004

Objective: keep the units of the registration. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-004
Question: Why does reusing an ICP threshold of 0.02 after converting point clouds from meters to millimeters change the problem?
Reponse: **Expected answer**: The threshold is a length in the coordinate unit; the scale change must be propagated to the relevant parameters.

**Further explanation**: Also check the voxel size and neighborhood radii, then the noise model.

**Scale calculation**: 0.02 m corresponds to 20 mm. If the coordinates are multiplied by a thousand but the threshold remains numerically 0.02, the admissible radius becomes a thousand times smaller in the physical scene. The number of matches and the optimization behavior can change abruptly.

**Complete check**: Convert together the coordinates, translations, voxel sizes and neighbor radii expressed as lengths. Rotations remain unitless, while quadratic costs scale with the square of the scale factor. In a constructed example, the same registration run before and after a consistent conversion must describe the same physical transformation, up to numerical effects. Check this simple case before changing the stopping criteria or initialization. A data normalization must therefore be a traced transformation of the data contract, not an isolated change of the input points.

**Residuals and covariance**: If all lengths are multiplied by $a$, a metric residual becomes $r'=ar$ and its covariance becomes $\Sigma'=a^2\Sigma$. The normalized residual $r^T\Sigma^{-1}r$ then remains invariant. A robust loss whose scale is set in meters also requires a converted scale, unlike a loss applied after a correctly propagated whitening. Absolute displacement or cost tolerances change meaning with units; relative criteria must be interpreted according to their exact definition. In Open3D 0.19.0, for example, `relative_rmse` is an absolute change of the inlier RMSE in the cloud unit, so the default $10^{-6}$ becomes a thousand times stricter physically after a conversion to millimeters. This reasoning distinguishes a consistent unit change from a deliberate change of physical weighting in a registration or a fusion of constraints.

**Scale changes affect normal estimation too**: Converting meters to millimeters requires scaling correspondence thresholds, voxel size and normal-neighborhood radii by 1000. Unit normals remain dimensionless, but the neighborhoods used to estimate them change if their radius is left unchanged. Residual variance scales by $10^6$. Thus even when the transform translation is converted correctly, an inconsistent preprocessing radius can alter normals, matches and the convergence behavior.

**Blocking errors**: Treating the threshold as a unitless number.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Open3D 0.19.0, global registration tutorial, voxel-based radii](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/global_registration.html) ; [Open3D v0.19.0, Registration.h L45–L50, ICP stopping tolerances](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.h#L45-L50). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::pratique cv_id::CV-ICP-004 provenance::agent pole::B pole::C
END

## CV-ICP-005

Objective: Choose an ICP variant. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-005
Question: Is point-to-plane ICP always a better replacement for point-to-point ICP?
Reponse: **Expected answer**: It exploits reliable normals and a geometry that constrains the useful motions; it can be ill-posed on some surfaces or with noisy normals.

**Further explanation**: Compare initialization, normal estimation and pose accuracy in the target protocol.

**Comparison of the information used**: Point-to-point penalizes a position difference along all three components; point-to-plane uses a local planar approximation of the surface. When normals and initialization are suitable, this approximation can be effective. If the normals are unstable or the geometry poor, the criterion may lose its advantage or leave some directions weakly constrained.

**Constructed ablation**: Keep the clouds, initial correspondences, threshold and reference fixed, then compare the variants while varying normal noise and overlap separately. Measure pose error, convergence, failures and cost. A drop in the residual specific to one variant is not directly comparable to the residual of another formulation. The right choice depends on the observed surfaces and the required accuracy. Do not use a single favorable case to claim superiority for all parts and all initializations.

**Where the normals come from**: A common local estimator centers the neighbors, computes their covariance matrix and takes the eigenvector of the smallest eigenvalue as the plane normal. A neighborhood that is too small becomes sensitive to noise; one that is too large mixes edges and curved surfaces. If the eigenvalues do not single out a normal direction, the local surface is itself ambiguous. For the squared point-to-plane residual alone, reversing the sign of a normal does not change the cost; a consistent orientation may nevertheless be required by other steps such as descriptors or rejection rules. Report pose quality together with this explained provenance of the normals.

**Normal reliability depends on neighborhood geometry**: For a local point covariance with eigenvalues $\lambda_1\le\lambda_2\le\lambda_3$, a well-separated small $\lambda_1$ supports a plane normal. If both first eigenvalues are small, the neighborhood is line-like and its normal direction is ambiguous; if all are comparable, a plane may be a poor model. These are geometry diagnostics rather than universal cutoffs. Neighborhood scale, range noise and mixed surfaces must be evaluated for the intended registration.

**Blocking errors**: Claiming that one variant dominates universally.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Rusinkiewicz and Levoy 2001, §3.5](https://www.cs.princeton.edu/~smr/papers/fasticp/fasticp_paper.pdf) ; [Gelfand et al. 2003, §2.2](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf) ; [Open3D 0.19.0, ICP registration tutorial](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html). Constructed cases: project deduction.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-ICP-005 provenance::agent pole::B pole::C
END

## CV-ICP-006

Objective: detect a degenerate registration and name its free motion. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ICP-006
Question: A robot registers consecutive LiDAR scans with point-to-plane ICP in a straight corridor 10 m long, 2 m wide and 2.5 m high (floor, ceiling, two plain walls). Every registration converges with fitness 0.97 and an inlier RMSE of 5 mm, yet the integrated trajectory disagrees with wheel odometry by 0.6 m after 20 m. Using only the matched points and their normals at the final pose, what do you compute to decide whether the geometry itself leaves a motion unconstrained, how must the points be prepared before you read it, and which motion do you expect it to flag here? Which motion would it flag if the scans saw only the floor and one wall?
Reponse: **Expected answer**: (1) The $6\times6$ point-to-plane matrix $C=\sum_i a_ia_i^\top$ with $a_i=(p_i\times n_i;\,n_i)$, rotation first, and its eigen-decomposition. An eigenvalue that is small relative to the largest marks a motion, its eigenvector, along which the surfaces slide with almost no change of error. (2) Before building $C$, move the centroid of the points to the origin and scale them to a mean distance of 1, then compare $\lambda_{\min}/\lambda_{\max}$ (or $c=\lambda_1/\lambda_6$) with a threshold calibrated on held-out scans. Raw coordinates make the ratio depend on the unit and the origin. (3) In the corridor, one near-zero eigenvalue whose eigenvector is the pure translation along the corridor axis; the rotation about the axis stays constrained. With the floor and one wall, the translation along their intersection line, direction $n_1\times n_2$.

**Further explanation**: For a small motion $x=(\delta\omega;\delta t)$ from the optimum, the point-to-plane error grows by $\Delta E=x^\top Cx$. Each eigenvalue is therefore the cost of a unit motion along its eigenvector, in general a screw motion. Fitness and RMSE summarize the accepted pairs, so a sliding solution scores as well as the true one. The rotation entries carry the lever arm $p_i$ in length units, the translation entries do not. Centring and scaling equalize the displacement a point can contribute by torque and by force. An exactly zero eigenvalue survives any unit or origin, because the change of coordinates is invertible, but noise never leaves an exact zero, and the ratio that must be thresholded depends on both.

**Constructed example** (recomputed by this pass's check script): the corridor sampled every 0.1 m gives 9,494 points. After normalization one eigenvalue is exactly 0, the axis translation; the rotation about the axis comes next at 0.098 of the largest. Two door jambs facing along the corridor (42 points) make the smallest eigenvalue non-zero: $c\approx125$, eigenvector still the axis translation. A 5 cm slide along the corridor raises $E$ by 0.105 m² against 10.6 m² for a 5 cm vertical slide. Without normalization the same scan gives 4,456 in metres from the corridor entrance and $4.4\times10^9$ in millimetres. In a map frame whose origin lies 100 m behind and 50 m beside the entrance, the weakest eigenvector becomes a rotation about the distant origin cancelled by a translation, not the corridor slide.

**Limits and remedies**: the test is linearized at the final pose with fixed pairs and cannot reveal a discrete symmetry, which leaves isolated minima rather than a flat direction. Report the free direction, add an odometry or IMU prior on it, or sample the points that constrain it. Adding uniformly sampled points does not help, because they are as likely to come from the flat areas as from the features that constrain the motion.

**Blocking errors**: Treating fitness or RMSE as evidence of a constrained pose. Reading eigenvalues or the condition number of the raw matrix in millimetres or in a distant map frame. Naming the rotation about the corridor axis as free, which holds for a circular tunnel, or giving two translations and a rotation for the floor and one wall, which is the nullspace of a single plane. Expecting denser uniform sampling to remove the degeneracy.
Source: [[60-vision-3d/references/62-recalage-global-icp|Full reference]] ; [Gelfand et al. 2003, §2.1 eqs. 4–5, §2.2 and Fig. 3, §3.1 condition number and normalization](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf). The corridor, two-plane and door-jamb scenes and their numbers are project constructions, recomputed in the check script of this pass.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-ICP-006 provenance::agent pole::B pole::C
END
