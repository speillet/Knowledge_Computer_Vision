---
id: CV-ICP
type: pipeline
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SE3", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Global registration and local ICP

## Problem, data and assumptions

Estimate a rigid transformation source→target between clouds expressed in compatible units. Outputs: pose and overlap measures/residual under given threshold. A correct pose requires more than a low RMSE on a small subset.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md); [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Reduce by voxels, estimate normals and FPFH, search for matches and a robust global initialization; refine locally by ICP. ICP alternates associations and optimization with a sufficiently close initialization hypothesis.

## Mathematics, conventions and units

Point-to-point: $\sum_i\|Rp_i+t-q_i\|^2$. Point-to-plane: $\sum_i[n_i^T(Rp_i+t-q_i)]^2$, normal unit targets. residuals in meters if metric clouds, costs in m². A flat surface leaves some tangential displacements and rotations poorly constrained; a change of objective does not create the absent stresses.

## Parameters and properties

Voxel, neighbourhood radii, correspondence threshold, rejection and stop criteria are relative to scale and noise. The Open3D tutorial ratios are illustrative. FPFH 33D is a descriptor, not a pose.

## Cost and implementation

Look for neighbors, normal, features and iterations dominate. No real cloud processed; legacy and tensor Open3D APIs are not mixed into supposedly executable code.

## Evaluation and controlled variation

Analytical variation: same points and known matches, then remote initialization with nearest neighbors. Predict a risk of erroneous associations and local minimum. Compare pose reference, overlap and error out of consensus.

## Failure modes and diagnosis

Low RMSE but pose false: inspect symmetry, overlap area, threshold and stress distribution. A flat plate can slide without large residuals point-to-plane.

## Alternatives and applications

Initialization by features, odometry/IMU, business constraints or registration multiview. Always announce sense of pose and quality of reference.

## Guided reasoning and proposed checks

These constructed cases develop initialization, correspondences and directions with little constraint. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ICP-001

**Question of work**: Why combine FPFH/RANSAC with subsequent ICP instead of initializing ICP from any arbitrary pose?

**Reference Response**: The global initialization looks for a compatible zone from matches; ICP refines locally and can converge on bad associations.

**Why the initialization counts**: ICP builds or updates associations from the current pose. If this pose is far away, the nearest neighbors can represent other surfaces; optimizing on these pairs can reinforce a local misalignment. Global research uses other clues to propose a region of pose before refinement.

**Constructed example**: Two identical supports on a part can offer two plausible local alignments. A weak residual after ICP does not automatically indicate the correct support. check final orientation and translation, covering and reserved distinctive surfaces. Record direction source→target and units before any comparison. The geometric features and RANSAC provide useful hypotheses; they remain limited by geometric texture, symmetry and overlap. An odometry or business constraint can provide another initialization if it is justified and evaluated.

### Case linked to CV-ICP-005

**Question of work**: Is point-to-plane ICP always a better replacement for point-to-point ICP?

**Reference Response**: It exploits reliable normals and a geometry that constrains useful movements; it can be ill-posed on certain surfaces or normal noise.

**Comparison of the information used**: point-to-point penalizes a difference of positions according to three components; point-to-plane uses a local surface approximation. When normals and initialization are adjusted, this approximation can be effective. If the normals are unstable or the geometry poor, the criterion may lose its interest or leave some directions little constrained.

**Constructed ablation**: keep clouds, initial matches, threshold and reference, then compare variants by varying the noise of normals and overlap separately. Measure pose error, convergence, failures and cost. A drop in the residual specific to one variant is not directly comparable to the residual of another formulation. The right choice depends on the observed surface area and the accuracy required. Do not use a single favorable plan case to advertise superiority over all coins and all initializations.

**Documentary reference for this pass**: [Open3D 0.19, ICP registration](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html), Point-to-plane ICP and evaluation. The other developments are in the [flashcards](../62-recalage-global-icp.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ICP-001

**Situation**: Why combine FPFH/RANSAC with subsequent ICP instead of initializing ICP from any arbitrary pose?

**Concrete local loop**: At iteration $k$, transform each source point by $T_k$, search for target neighbors, reject incompatible pairs, and then estimate a $\Delta T_k$ fix. With a correction expressed in the target coordinate frame, dial $T_{k+1}=\Delta T_kT_k$. A correction in the source coordinate frame consists of the other side: mixing these conventions produces a poor optimization trajectory. The rapprochement of the neighbors and the resolution of pose are two different steps. A good initialization facilitates physical associations, while a threshold that is too wide can accept foreign surfaces and a threshold that is too strict removes the constraints necessary for refinement.

### CV-ICP-002

**Situation**: What does $n^T(Rp+t-q)$ measure in point-to-plane ICP?

**Linearization of the residual**: Put $s=Rp+t$ and apply a small disturbance to the left $s'\simeq s+\delta t+\delta\omega\times s$. The residual becomes $r'\simeq r+n^T\delta t+(s\times n)^T\delta\omega$. Its Jacobian is therefore a line of six components for the order translation then rotation. Stacking these lines directly shows the movements that the scene constrains. For all vertical normals, horizontal translations do not appear in this local model. This derivation assumes fixed matches and normals during the step; updating them to the next iteration makes the overall problem more complex than a single linear system.

### CV-ICP-003

**Situation**: ICP reports low RMSE but aligns only a corner of two point clouds. What should be reported?

**Effect of the threshold on statistics**: if the distances are $d_1,\ldots,d_m$, the RMSE is $\sqrt{\sum_i d_i^2/m}$. Removing all large distances can reduce it while greatly reducing $m$; the two experiments no longer focus on the same points. Also comparing the two directions source→target and target→source can reveal asymmetrical coverage, especially with different densities. An analysis by reserved physical regions prevents a dense area from dominating the score. These measurements complete the reference error of pose; they do not, on their own, remove the ambiguity of a perfectly symmetrical object.

### CV-ICP-004

**Situation**: Why does reusing an ICP threshold of 0.02 after converting point clouds from meters to millimeters change the problem?

**residuals and covariance**: if all lengths are multiplied by $a$, a metric residual becomes $r'=ar$ and its covariance becomes $\Sigma'=a^2\Sigma$. The normalized residual $r^T\Sigma^{-1}r$ then remains invariant. A robust loss set in meters also requires a converted scale, unlike a loss applied after properly processed whitening. Absolute displacement or cost tolerances can change direction with units; relative criteria must be interpreted according to their exact definition. This reasoning makes it possible to distinguish a coherent unit change from a voluntary change in physical weighting in a registration or a merger of constraints.

### CV-ICP-005

**Situation**: Is point-to-plane ICP always a better replacement for point-to-point ICP?

**Where do the normals come from**: A current local estimator centers the neighbors, calculates their covariance matrix and takes the eigenvector of smallest eigenvalue as the plane normal. A neighborhood too small becomes sensitive to noise; too large, it mixes edges and curved surfaces. If eigenvalues do not distinguish a normal direction, the local surface is itself ambiguous. For the residual point-to-plane isolated square, reversing the sign of a normal does not change the cost; a consistent orientation may nevertheless be required by other steps such as descriptors or rejection rules. Compare the quality of pose with this provenance of the explained normals.

**Passages consulted for these developments**: [Open3D 0.19.0](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html), Point-to-point and Point-to-plane ICP; project linearization and scale analyses; [Open3D 0.19.0](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html), FPFH and RANSAC; no Open3D execution.

## Sources and flashcards

- [Open3D 0.19.0, point-to-point and point-to-plane ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html).
- [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
- [Related flashcards](../62-recalage-global-icp.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
