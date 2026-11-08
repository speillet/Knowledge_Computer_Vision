# Flashcards — Bundle adjustment and the Schur complement

reference note: [[50-calibration-geometrie/references/54-bundle-adjustment|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-BA-001

Objective: Identify the unknowns of a BA. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-BA-001
Question: What does bundle adjustment optimize, and how does it differ from a pose graph?
Reponse: **Expected answer**: The BA optimizes poses and points, possibly intrinsic, from reprojections; a pose graph is based on constraints between poses.

**Further explanation**: The level of information and the sparsity differ. A weak reprojection can still hide a gauge or bias.

**Mechanism**: Each image observation links a camera and a landmark with a projection model. Changing a point influences its observations in several views; changing a camera influences the points it observes. The BA jointly searches for values that explain these observations, with weighting and possibly robustness.

**Constructed example**: A trajectory drift and erroneous point positions may partially compensate in one view, but be incompatible in the others. The joint optimization exploits these links. A pose graph already uses constraints summarized between poses and does not necessarily retain each reprojection. The costs, possible biases and structure of the unknowns therefore differ. Check gauge, initialization, associations and residuals per observation: a decrease in the overall cost proves neither the metric scale nor the physical validity of all optimized landmarks.

**Complete objective to be explained**: On the $\mathcal O$ set of observations actually present, a BA can minimize $\sum_{(i,j)\in\mathcal O}\rho(\|L_{ij}^{-1}[\pi(K_i,T_i,X_j)-z_{ij}]\|_2^2)$, with $z_{ij}$ in pixels, $X_j$ a world point, $T_i$ a pose and $L_{ij}L_{ij}^T$ its measurement covariance. The projection function includes the expected distortion. The poses must be updated to its appropriate parameterization; the parameters set are not unknown to the solver. Points seen in a single image may lack depth constraint. Thus, the total number of observations alone does not describe the connectivity and observability of the reconstruction.

**Observation connectivity determines recoverable structure**: A landmark observed by only one camera supplies a bearing but no independent triangulated depth without another constraint. Many such observations can increase residual count without making the map fully observable. Inspect the camera-landmark graph and visibility geometry before interpreting a successful optimization as recovered 3D structure. More observations at identical bearings or with negligible baseline can leave nearly the same weak directions as the original system.

**Blocking errors**: Present BA as a simple smoothing of camera positions.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Ceres, Schur solvers and block equations](https://ceres-solver.readthedocs.io/latest/nnls_solving.html); [Ceres, Covariance Estimation, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-BA-001 provenance::agent pole::B pole::C
END

## CV-BA-002

Objective: Explain the elimination of Schur. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-BA-002
Question: Does eliminating points with the Schur complement mean ignoring them in bundle adjustment?
Reponse: **Expected answer**: No: their effect is transmitted to the reduced system of the cameras, then their increments are recovered by substitution.

**Further explanation**: The structure of the observations makes the points block exploitable; this does not remove non-linearity or local minima.

**Reading the system in blocks**: Camera and dot increments are coupled. Algebraically solve the block of points and then replace it in the camera equations gives the complement of Schur. The reduced system retains the effect of the points on the cameras; after resolution, a substitution recovers the increments of points.

**Consequence of sparsity**: Multiple cameras that see the same landmark can be paired in the reduced system. The cost therefore depends on the connections and not only on the total number of points. In a constructed example, two datasets of the same size but different visibility may have different memory costs. The inverses in derivation refer to algebraic operations; an implementation uses appropriate factorizations or resolutions. Elimination refers to the current linearized problem and does not remove the need to relinearize or the initialization dependency.

**Reduced system derivation**: Linearized problem gives $B\delta_c+E\delta_p=v$ and $E^T\delta_c+C\delta_p=w$. If $C$ is invertible, the second equation provides $\delta_p=C^{-1}(w-E^T\delta_c)$; its substitution in the first $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$ product. In a classic BA where each residual connects a camera and a point, the points do not interact directly with each other in this block: $C$ is diagonal block per point. A point seen by many cameras, on the other hand, creates couplings in the reduced system. Point – point constraints or other factors can change this structure; the factorization of the problem should be checked instead of assuming Schur to be always the same.

**Elimination creates camera-to-camera coupling**: If two cameras observe the same point, eliminating that point introduces a relation between their increments in the reduced camera system. Long feature tracks can therefore improve geometric constraints while increasing fill and computational coupling. Schur elimination preserves the linearized problem when its blocks are treated correctly; it does not make point uncertainty disappear or replace nonlinear relinearization. Recover point increments using the same linearization after solving the reduced system.

**Blocking errors**: Say that Schur removes the 3D observations from the problem.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Ceres, Schur solvers and block equations](https://ceres-solver.readthedocs.io/latest/nnls_solving.html); [Ceres, Covariance Estimation, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-BA-002 provenance::agent pole::B pole::C
END

## CV-BA-003

Objective: Do not hide a gauge. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-BA-003
Question: Bundle adjustment converges at different scales with the same cost in a monocular reconstruction. Which check is missing?
Reponse: **Expected answer**: Check the scale gauge and the presence of a metric reference; setting a convention is not measuring this scale.

**Further explanation**: Evaluate parameters with an alignment allowed by the task; a pixel cost can remain invariant to an overall transformation.

**Example of Invariance**: If all camera positions and points are multiplied by the same factor, the projection directions of a monocular reconstruction may remain the same. The image does not automatically provide the length corresponding to a unit of the model. Convergence at different scales is compatible with this gauge.

**Proposed Validation**: identify the constraint that actually provides the scale, if the product needs it, and check its unit. To compare reconstructions, allow only the alignment justified by the task. A similarity may be appropriate for free-scale monocular reconstruction, but mask a scale defect in a system that is supposed to be metric. Setting a point or baseline to make the calculation unique is a convention as long as its value does not come from a measurement. Metric accuracy therefore requires an independent reference.

**Proof of free scale**: with an ideal projection of $RX+t$, replace $X$ with $aX$ and $t$ with $at$, $a>0$, multiplies the three camera coordinates by $a$; the homogeneous division removes this factor. Monocular observations therefore do not distinguish these scales. A very strong digital prior on a translation can make the system invertible without this value being measured. If the system is to be metric, use a known length or source of motion and announce its uncertainty. A visual-inertial optimization can resolve scale ambiguity under the conditions of its model; it can also become ill-conditioned if the movements do not sufficiently excite the necessary variables.

**A baseline prior adds evidence only if it is measured**: Fixing a baseline length to one removes a computational scale freedom, but it establishes meters only if that length is independently known in meters. A measured baseline prior has finite uncertainty and can influence both scale and its uncertainty. Report this distinction when comparing trajectories or map dimensions. Aligning reconstructions by a similarity transform can intentionally remove scale error for one metric while hiding it for a metric deployment requirement.

**Blocking errors**: Automatically assign multiplicity to a solver failure.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Ceres, Covariance Estimation, Gauge Invariance, consulted on 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Ceres, Solving Non-linear Least Squares, Schur complement trick and block systems](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-BA-003 provenance::agent pole::B pole::C
END

## CV-BA-004

Objective: check a model too free. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-BA-004
Question: Why can freeing additional camera coefficients reduce the optimization cost while degrading calibration?
Reponse: **Expected answer**: Additional settings may over-adjust an uninformative dataset or be correlated.

**Further explanation**: Measure stability by subsets and error on independent observations; choose the constraints of the model physically.

**Why the cost goes down**: A larger parameter space can contain a solution that further adjusts training observations. This does not say if the additional parameters represent the camera or absorb noise, deformation of calibration target and mismatches. Several parameters can also produce similar effects on an uninformative capture.

**Constructed ablation**: Keep observations and release a group of parameters at once. Examine their dispersion in subsets, correlations and residuals on reserved views including edges. A better adjustment cost with out-of-sample degradation suggests an unfavorable trade-off. Conversely, a model that is too constrained can retain a real bias. The choice must be based on optics, diversity of data and usage, without making the mere reduction in cost a calibration criterion.

**Example of missing information**: In a polynomial radial model, the effects of high-order coefficients grow with normalized radius powers. Observations near the center can hardly constrain these terms; different values then produce almost the same pixels observed but diverge at the edge. Unleashing these coefficients increases flexibility without adding informative data. The damping of LM limits the current resolution pitch: it is not automatically a physical priority on the final parameters. Justify the free parameters, check the directions with little stress and test the geometry where it will be used. A reserved validation must keep poses and really different areas, not just neighboring points of the same catches.

**A flexible lens can absorb another model error**: Unmodeled rolling shutter, target nonplanarity or imperfect associations can be partly absorbed by extra lens coefficients. Lower training reprojection cost then measures increased fitting freedom rather than a better physical lens model. A proposed comparison freezes acquisition and associations, varies model complexity, and evaluates held-out poses and radial regions. Inspect parameter stability and plausible projection behavior beyond the fitted radius before accepting the additional coefficients.

**Blocking errors**: Compare only adjustment costs.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Ceres, Covariance Estimation, Gauge Invariance, consulted on 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); effect of free parameters and validation protocol: deductions from the project; [Ceres, Solving Non-linear Least Squares, Schur complement trick and block systems](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-BA-004 provenance::agent pole::B pole::C
END
