# Flashcards — Bundle adjustment and the Schur complement

reference note: [[50-calibration-geometrie/references/54-bundle-adjustment|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-BA-001

Objective: Identify the unknowns of a BA. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-BA-001
Question: What does bundle adjustment optimize, and how does it differ from a pose graph?
Reponse: **Expected answer**: The BA optimizes poses and points, and possibly intrinsic parameters, from reprojection errors; a pose graph is based on constraints between poses.

**Further explanation**: The level of information and the sparsity differ. A low reprojection error can still hide a gauge freedom or a bias.

**Mechanism**: Each image observation links a camera and a landmark through a projection model. Changing a point affects its observations in several views; changing a camera affects the points it observes. BA jointly searches for values that explain these observations, with weighting and possibly a robust loss.

**Constructed example**: A trajectory drift and erroneous point positions may partially compensate each other in one view but be incompatible in the others. The joint optimization exploits these links. A pose graph uses constraints already summarized between poses and does not necessarily retain each reprojection. The costs, possible biases and structure of the unknowns therefore differ. Check the gauge, initialization, associations and per-observation residuals: a decrease in the overall cost proves neither the metric scale nor the physical validity of all optimized landmarks.

**Full objective**: Over the set $\mathcal O$ of observations actually present, a BA can minimize $\sum_{(i,j)\in\mathcal O}\rho(\|L_{ij}^{-1}[\pi(K_i,T_i,X_j)-z_{ij}]\|_2^2)$, with $z_{ij}$ in pixels, $X_j$ a world point, $T_i$ a pose and $L_{ij}L_{ij}^T$ its measurement covariance. The projection function includes the modeled distortion. Poses must be updated through an appropriate local parameterization, and parameters held constant are not unknowns of the solver. A point seen in a single image lacks a depth constraint unless another factor provides one. Thus, the total number of observations alone does not describe the connectivity and observability of the reconstruction.

**Observation connectivity determines recoverable structure**: A landmark observed by only one camera supplies a bearing but no independent triangulated depth without another constraint. Many such observations can increase residual count without making the map fully observable. Inspect the camera-landmark graph and visibility geometry before interpreting a successful optimization as recovered 3D structure. More observations at identical bearings or with negligible baseline can leave nearly the same weak directions as the original system.

**Blocking errors**: Presenting BA as simple smoothing of camera positions.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Triggs et al. 2000, §1, §2.1 and §5](https://hal.science/inria-00548290/document); [Agarwal et al. 2010, §2.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/10/Agarwal-ECCV10.pdf). Pose-graph contrast and connectivity cases: project deductions.
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-BA-001 provenance::agent pole::B pole::C
END

## CV-BA-002

Objective: Explain Schur elimination. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-BA-002
Question: Does eliminating points with the Schur complement mean ignoring them in bundle adjustment?
Reponse: **Expected answer**: No: their effect is transmitted to the reduced system of the cameras, then their increments are recovered by substitution.

**Further explanation**: The structure of the observations makes the points block exploitable; this does not remove non-linearity or local minima.

**Reading the system in blocks**: Camera and point increments are coupled. Solving the point block algebraically and substituting it into the camera equations gives the Schur complement. The reduced system keeps the effect of the points on the cameras; after solving it, back-substitution recovers the point increments.

**Consequence of sparsity**: Cameras that see the same landmark become coupled in the reduced system. The cost therefore depends on the connections and not only on the total number of points. In a constructed example, two datasets of the same size but different visibility may have different memory costs. The inverses in the derivation denote algebraic operations; an implementation uses appropriate factorizations and solves. Elimination refers to the current linearized problem and does not remove the need to relinearize or the initialization dependency.

**Reduced system derivation**: The linearized problem gives $B\delta_c+E\delta_p=v$ and $E^T\delta_c+C\delta_p=w$. If $C$ is invertible, the second equation gives $\delta_p=C^{-1}(w-E^T\delta_c)$, and substituting it into the first yields $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$. In a classic BA where each residual connects one camera and one point, points do not interact directly with each other: $C$ is block diagonal, with one block per point. A point seen by many cameras, on the other hand, creates couplings in the reduced system. Point–point constraints or other factors can change this structure; check the factor structure of the problem instead of assuming that the elimination always takes this form.

**A shared landmark can create a camera clique**: Constructed sparsity example: one landmark seen by $k$ cameras contributes to each of their pose blocks. Eliminating that landmark can create up to $k(k-1)/2$ pairwise off-diagonal camera-block connections, subject to rank and existing connections. A five-camera track can therefore connect ten camera pairs; a two-camera track connects one. Long tracks can improve geometric constraints while increasing reduced-system coupling. This counts a possible sparsity pattern, not independent measurements or a prediction of exact factorization time.

**Blocking errors**: Say that Schur removes the 3D observations from the problem.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Agarwal et al. 2010, §2.2, eqs. 5–8](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/10/Agarwal-ECCV10.pdf); [Ceres 2.2.0, `nnls_solving.rst` L669–L767](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_solving.rst#L669-L767). Camera-clique count: project deduction.
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

**Example of invariance**: If all camera positions and points are multiplied by the same factor, the projection directions of a monocular reconstruction may remain the same. The image does not automatically provide the length corresponding to a unit of the model. Convergence at different scales is compatible with this gauge.

**Proposed validation**: Identify the constraint that actually provides the scale, if the product needs it, and check its unit. To compare reconstructions, allow only the alignment justified by the task. A similarity may be appropriate for free-scale monocular reconstruction, but mask a scale defect in a system that is supposed to be metric. Setting a point or baseline to make the calculation unique is a convention as long as its value does not come from a measurement. Metric accuracy therefore requires an independent reference.

**Proof of free scale**: For an ideal projection of $RX+t$, replacing $X$ by $aX$ and $t$ by $at$, with $a>0$, multiplies the three camera coordinates by $a$; the perspective division removes this factor. Monocular observations therefore do not distinguish these scales. A very strong numerical prior on a translation can make the system invertible without that value being measured. If the system must be metric, use a known length or a metric motion source and report its uncertainty. A visual-inertial optimization can resolve the scale ambiguity under the conditions of its model; it can also become ill-conditioned if the motion does not sufficiently excite the necessary variables.

**A baseline prior adds evidence only if it is measured**: Fixing a baseline length to one removes a computational scale freedom, but it establishes meters only if that length is independently known in meters. A measured baseline prior has finite uncertainty and can influence both scale and its uncertainty. Report this distinction when comparing trajectories or map dimensions. Aligning reconstructions by a similarity transform can intentionally remove scale error for one metric while hiding it for a metric deployment requirement.

**Blocking errors**: Automatically attributing the multiplicity of solutions to a solver failure.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Triggs et al. 2000, §9.1](https://hal.science/inria-00548290/document); [Ceres 2.2.0, `nnls_covariance.rst` L67–L74](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_covariance.rst#L67-L74). Scale proof, validation and prior cases: project deductions.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-BA-003 provenance::agent pole::B pole::C
END

## CV-BA-004

Objective: Check an overly free model. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-BA-004
Question: Why can freeing additional camera coefficients reduce the optimization cost while degrading calibration?
Reponse: **Expected answer**: Additional parameters may overfit an uninformative dataset or be correlated with each other.

**Further explanation**: Measure stability by subsets and error on independent observations; choose the constraints of the model physically.

**Why the cost goes down**: A larger parameter space can contain a solution that fits the training observations more closely. This does not tell whether the additional parameters represent the camera or absorb noise, calibration-target deformation and mismatches. Several parameters can also produce similar effects on an uninformative capture.

**Constructed ablation**: Keep the observations fixed and free one group of parameters at a time. Examine their spread across data subsets, their correlations and the residuals on held-out views, including image borders. A better fitting cost with out-of-sample degradation suggests an unfavorable trade-off. Conversely, an overly constrained model can retain a real bias. The choice must rest on the optics, data diversity and intended use, without making the mere reduction in cost a calibration criterion.

**Example of missing information**: In a polynomial radial model, the effects of high-order coefficients grow with powers of the normalized radius. Observations near the center can hardly constrain these terms; different values then produce almost the same observed pixels but diverge at the edge. Freeing these coefficients increases flexibility without adding informative data. Levenberg–Marquardt damping limits the current step size: it is not a physical prior on the final parameters. Justify the free parameters, check weakly constrained directions and test the geometry where it will be used. A held-out validation set must contain genuinely different poses and image regions, not just neighboring points from the same captures.

**A flexible lens can absorb another model error**: Unmodeled rolling shutter, target nonplanarity or imperfect associations can be partly absorbed by extra lens coefficients. Lower training reprojection cost then measures increased fitting freedom rather than a better physical lens model. A proposed comparison freezes acquisition and associations, varies model complexity, and evaluates held-out poses and radial regions. Inspect parameter stability and plausible projection behavior beyond the fitted radius before accepting the additional coefficients.

**Blocking errors**: Comparing only fitting costs.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Full reference]]; [Triggs et al. 2000, §10.5 and §11](https://hal.science/inria-00548290/document); [Schönberger and Frahm 2016, §4.4](https://openaccess.thecvf.com/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf). Effect of free parameters and validation protocol: project deductions.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-BA-004 provenance::agent pole::B pole::C
END
