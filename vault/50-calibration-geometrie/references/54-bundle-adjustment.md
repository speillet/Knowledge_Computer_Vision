---
id: CV-BA
type: methode
domaine: d05
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-SVD", "CV-EPIPOLAIRE", "CV-FACTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Bundle adjustment and the Schur complement

## Problem, data and assumptions

Refine poses and Landmarks by their common image observations. Inputs: 2D – 3D combinations, initial, intrinsic and noise parameters; outputs: optimized states and diagnostics of residuals. A bad association or gauge doesn’t go away with more iterations.

## Prerequisites and competencies

**Required prerequisites**: [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md); [CV-EPIPOLAIRE](53-epipolaire-pnp-triangulation.md); [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Linearize projections, solve a sparse increment, accept a step and then repeat. The observations each link a camera and a point; this structure makes it possible to effectively eliminate the increments of points with Schur, and then to find them.

## Mathematics, conventions and units

Minimize $\sum_{ij}\rho(r_{ij}^T\Sigma_{ij}^{-1}r_{ij})$, where $r_{ij}$ is a residual pixel, $\Sigma_{ij}$ its positive definite covariance and $\rho$ a robust loss applied to its squared whitened norm. For camera blocks/points B,E,C and right-hand sides v,w, solve $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$, and then recover $\delta_p=C^{-1}(w-E^T\delta_c)$. This writing assumes the blocks of $C$ invertibles; constraints and/or damping must process the singular directions. Noted inverses describe algebra; the implementation uses appropriate resolutions.

## Parameters and properties

Attach gauge, free intrinsic parameters, robust loss and stop criteria. Poor catch or correlated parameters may remain poorly identified. Robustification attenuates some large residuals without proving associations.

## Cost and implementation

Sparsity, number of observations and order of elimination dominate; Schur can generate interactions between cameras. No Ceres solver is executed here.

## Evaluation and controlled variation

Proposed variation: retain observations and gradually release intrinsic parameters. Predict a possible decrease in cost with less stability; measure on reserved views and check units.

## Failure modes and diagnosis

Low cost but incorrect scale: check metric reference and gauge. Camera that collapses after adding a track: inspect the association and the residuals by observation.

## Alternatives and applications

pose graph mainly optimizes poses/relative constraints; BA retains the observations of the marks. The choice depends on the unknowns and the information to be kept.

## Guided reasoning and proposed checks

These built cases develop gauge, robust residuals and optimization blocks. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-BA-001

**Question of work**: What does bundle adjustment optimize, and how does it differ from a pose graph?

**Reference Response**: The BA optimizes poses and points, possibly intrinsic, from reprojections; a pose graph is based on constraints between poses.

**Mechanism**: Each image observation links a camera and a landmark with a projection model. Changing a point influences its observations in several views; changing a camera influences the points it observes. The BA jointly searches for values that explain these observations, with weighting and possibly robustness.

**Constructed example**: A trajectory drift and erroneous point positions may partially compensate in one view, but be incompatible in the others. The joint optimization exploits these links. A pose graph already uses constraints summarized between poses and does not necessarily retain each reprojection. The costs, possible biases and structure of the unknowns therefore differ. Check gauge, initialization, associations and residuals per observation: a decrease in the overall cost proves neither the metric scale nor the physical validity of all optimized landmarks.

### Case linked to CV-BA-004

**Question of work**: Why can freeing additional camera coefficients reduce the optimization cost while degrading calibration?

**Reference Response**: Additional settings may over-adjust an uninformative dataset or be correlated.

**Why the cost goes down**: A larger parameter space can contain a solution that further adjusts training observations. This does not say if the additional parameters represent the camera or absorb noise, deformation of calibration target and mismatches. Several parameters can also produce similar effects on an uninformative capture.

**Constructed ablation**: Keep observations and release a group of parameters at once. Examine their dispersion in subsets, correlations and residuals on reserved views including edges. A better adjustment cost with out-of-sample degradation suggests an unfavorable trade-off. Conversely, a model that is too constrained can retain a real bias. The choice must be based on optics, diversity of data and usage, without making the mere reduction in cost a calibration criterion.

**Documentary reference for this pass**: [Ceres, Non-linear Least Squares Solving](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), Schur solvers and bundle adjustment. The other developments are in the [flashcards](../54-bundle-adjustment.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-BA-001

**Situation**: What does bundle adjustment optimize, and how does it differ from a pose graph?

**Complete objective to be explained**: On the $\mathcal O$ set of observations actually present, a BA can minimize $\sum_{(i,j)\in\mathcal O}\rho(\|L_{ij}^{-1}[\pi(K_i,T_i,X_j)-z_{ij}]\|_2^2)$, with $z_{ij}$ in pixels, $X_j$ a world point, $T_i$ a pose and $L_{ij}L_{ij}^T$ its measurement covariance. The projection function includes the expected distortion. The poses must be updated to its appropriate parameterization; the parameters set are not unknown to the solver. Points seen in a single image may lack depth constraint. Thus, the total number of observations alone does not describe the connectivity and observability of the reconstruction.

### CV-BA-002

**Situation**: Does eliminating points with the Schur complement mean ignoring them in bundle adjustment?

**Reduced system derivation**: Linearized problem gives $B\delta_c+E\delta_p=v$ and $E^T\delta_c+C\delta_p=w$. If $C$ is invertible, the second equation provides $\delta_p=C^{-1}(w-E^T\delta_c)$; its substitution in the first $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$ product. In a classic BA where each residual connects a camera and a point, the points do not interact directly with each other in this block: $C$ is diagonal block per point. A point seen by many cameras, on the other hand, creates couplings in the reduced system. Point – point constraints or other factors can change this structure; the factorization of the problem should be checked instead of assuming Schur to be always the same.

### CV-BA-003

**Situation**: Bundle adjustment converges at different scales with the same cost in a monocular reconstruction. Which check is missing?

**Proof of free scale**: with an ideal projection of $RX+t$, replace $X$ with $aX$ and $t$ with $at$, $a>0$, multiplies the three camera coordinates by $a$; the homogeneous division removes this factor. Monocular observations therefore do not distinguish these scales. A very strong digital prior on a translation can make the system invertible without this value being measured. If the system is to be metric, use a known length or source of motion and announce its uncertainty. A visual-inertial optimization can resolve scale ambiguity under the conditions of its model; it can also become ill-conditioned if the movements do not sufficiently excite the necessary variables.

### CV-BA-004

**Situation**: Why can freeing additional camera coefficients reduce the optimization cost while degrading calibration?

**Example of missing information**: In a polynomial radial model, the effects of high-order coefficients grow with normalized radius powers. Observations near the center can hardly constrain these terms; different values then produce almost the same pixels observed but diverge at the edge. Unleashing these coefficients increases flexibility without adding informative data. The damping of LM limits the current resolution pitch: it is not automatically a physical priority on the final parameters. Justify the free parameters, check the directions with little stress and test the geometry where it will be used. A reserved validation must keep poses and really different areas, not just neighboring points of the same catches.

**Passages consulted for these developments**: [Ceres, Solving Non-linear Least Squares](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), Schur complement trick and block systems; [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), Gauge Invariance and rank of Jacobian.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-BA-001 — Observation connectivity determines recoverable structure

A landmark observed by only one camera supplies a bearing but no independent triangulated depth without another constraint. Many such observations can increase residual count without making the map fully observable. Inspect the camera-landmark graph and visibility geometry before interpreting a successful optimization as recovered 3D structure. More observations at identical bearings or with negligible baseline can leave nearly the same weak directions as the original system.

### CV-BA-002 — Elimination creates camera-to-camera coupling

If two cameras observe the same point, eliminating that point introduces a relation between their increments in the reduced camera system. Long feature tracks can therefore improve geometric constraints while increasing fill and computational coupling. Schur elimination preserves the linearized problem when its blocks are treated correctly; it does not make point uncertainty disappear or replace nonlinear relinearization. Recover point increments using the same linearization after solving the reduced system.

### CV-BA-003 — A baseline prior adds evidence only if it is measured

Fixing a baseline length to one removes a computational scale freedom, but it establishes meters only if that length is independently known in meters. A measured baseline prior has finite uncertainty and can influence both scale and its uncertainty. Report this distinction when comparing trajectories or map dimensions. Aligning reconstructions by a similarity transform can intentionally remove scale error for one metric while hiding it for a metric deployment requirement.

### CV-BA-004 — A flexible lens can absorb another model error

Unmodeled rolling shutter, target nonplanarity or imperfect associations can be partly absorbed by extra lens coefficients. Lower training reprojection cost then measures increased fitting freedom rather than a better physical lens model. A proposed comparison freezes acquisition and associations, varies model complexity, and evaluates held-out poses and radial regions. Inspect parameter stability and plausible projection behavior beyond the fitted radius before accepting the additional coefficients.

Consulted foundations: [Ceres Schur solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html#the-schur-complement-trick): block normal equations, point elimination and camera coupling; Context7 solver sources consulted; [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html): gauge invariance and Jacobian rank.

## Sources and flashcards

- [Ceres, Covariance Estimation, Gauge Invariance, consulted on 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html)
- [Ceres, LossFunction, motivation and cost equation, consulted on 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html)

- [Ceres, Schur solvers and block equations](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
- [Related flashcards](../54-bundle-adjustment.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
