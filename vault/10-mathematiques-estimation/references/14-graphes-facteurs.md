---
id: CV-FACTEURS
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 11
prerequis: ["CV-SVD", "CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Factor graphs and incremental optimization

This method note covers the back-end of mapping and localization systems: how
measurements become a factor graph, how the graph becomes a sparse nonlinear
least-squares problem, how incremental solvers such as iSAM2 update it, and how false
loop closures are contained. Solver numerics are in [CV-SVD](11-moindres-carres-svd.md),
pose parameterizations in [CV-SE3](12-rotations-se3.md), and the camera-specific case of
bundle adjustment in [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md).

## Problem and data contract

**Task.** Estimate a set of variables $X$ — robot or camera poses, landmarks, velocities,
IMU biases, calibration parameters — from many measurements, each depending on a few
variables, and keep the estimate up to date as measurements arrive.

**Inputs.**

- *Variables* with a type and a tangent convention: a pose $T_i\in SE(3)$ has 6 degrees of
  freedom in metres and radians, a landmark 3 in metres, a velocity 3 in m/s, an IMU bias
  6, and so on.
- *Factors* $f_k(X_k)$, each with a residual $r_k(X_k)$ over its variables $X_k$, a noise
  model $\Sigma_k$ in the residual's units and optionally a robust loss: relative-pose
  factors from odometry (6-D residual), loop closures from place recognition (6-D), image
  reprojections (2-D, pixels), IMU preintegration, GNSS or prior factors.
- *Initial values* for every variable, which the nonlinear solver refines; GTSAM keeps them
  in a `Values` container separate from the graph [GTSAM tutorial, §§2.3–2.4].
- *A gauge choice*: which absolute frame, and for monocular systems which scale, the
  solution is expressed in.

**Outputs.** The maximum a posteriori (MAP) estimate of $X$, optionally marginal
covariances of selected variables, and per-factor residuals for diagnosis.

**Role in a pipeline.** The front-end extracts features, tracks them, proposes loop
candidates and verifies them geometrically; the back-end represented by the factor graph
fuses everything. Typical consumers are SLAM and visual-inertial odometry
([CV-VIO](../../60-vision-3d/references/63-slam-vio.md)), multi-camera calibration and
mapping. The graph describes a factorization, not an optimizer: associations, noise
models, initialization and gauge must still be supplied, and a wrong association produces
a structurally valid graph of the wrong problem.

## Intuition

A factor graph is a bipartite graph between variables and factors; each factor is a
term of a function, typically the posterior density, that depends only on the variables
it touches [GTSAM tutorial, §1; Kaess et al. 2012, §2]. Under Gaussian noise each factor
behaves like a spring whose stiffness is its information $\Sigma_k^{-1}$, and the optimum is
the configuration of minimum total spring energy. A loop closure is a long spring between
two distant poses: it pulls the accumulated drift back and spreads the correction along
the chain in proportion to the compliance of each spring.

### Worked example A: what a loop closure does to a drifting chain

Constructed example, recomputed by checks/14-graphes-facteurs.py. A 1-D robot makes ten
odometry steps, each measured with a 1 cm standard deviation; the odometry sums to 10.1 m
(1% drift) while the true distance back to the start is 10.0 m.

- *Correct loop* with a 1 cm standard deviation: least squares spreads the 0.1 m
  discrepancy in proportion to the variances, 1/11 to the loop and 1/11 (9.1 mm) to each
  odometry edge.
- *False loop* (perceptual aliasing) claiming 5.0 m with the same weight: every odometry
  edge is bent by 0.46 m, a whitened residual of about 46 on all eleven factors. The total
  cost after optimization is the smallest possible for this wrong graph; the map is wrong
  everywhere.

The second case explains the central risk of the back-end: one confident wrong factor
distorts the whole connected graph, while its own residual stays no larger than its
neighbours'.

## Prerequisites and competencies

**Required prerequisites**: [CV-SVD](11-moindres-carres-svd.md) (whitening, Gauss–Newton,
Levenberg–Marquardt, robust losses, covariance and gauge) and [CV-SE3](12-rotations-se3.md)
(pose composition, tangent increments, adjoint). Useful links:

- the filtering alternative and its consistency checks: [CV-FUSION](13-kalman-ekf-eskf.md);
- bundle adjustment and the Schur complement: [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md);
- loop closure, IMU preintegration and trajectory metrics: [CV-VIO](../../60-vision-3d/references/63-slam-vio.md);
- feature matching used to verify loop candidates: [CV-MATCHING](../../40-features-matching/references/43-detecteurs-matchers.md).

**Target competencies**: separate representation from solver, explain and anchor a gauge,
diagnose a loop closure, compare robust back-ends and explain what an incremental update
recomputes and at what cost.

## Assumptions, observability and degenerate cases

- **Conditional independence.** Factors must carry independent evidence given the
  variables. Inserting the same relative pose twice doubles its information and shrinks
  the reported standard deviation by $\sqrt2$ without new data (recomputed by the check
  script; see the 2026-11-08 appendix).
- **Noise model.** The quadratic cost is the negative log-likelihood only for Gaussian
  factors with fixed covariances; heavy-tailed errors need robust losses, and a covariance
  that depends on the state adds a log-determinant term.
- **Correct association.** Perceptual aliasing makes a front-end without false positives
  unrealistic [Agarwal et al. 2013, abstract]; the back-end must survive some wrong loops.
- **Initialization.** Gauss–Newton and Levenberg–Marquardt converge to a local minimum;
  a poor initial trajectory or a large loop correction may need several relinearizations.
- **Gauge.** Relative factors leave a common transformation free: 6 degrees of freedom
  for a 3-D pose graph (project deduction consistent with GTSAM §4.1), 7 for monocular bundle
  adjustment, defined up to a similarity [Ceres covariance, Gauge Invariance; Zhang et al.
  2018, §I], and 4 for visual-inertial estimation, where position and yaw are unobservable
  [Zhang et al. 2018, abstract]. Each disconnected component needs its own anchor.
- **Degenerate cases.** Insufficient excitation in visual-inertial systems (constant
  velocity, pure rotation) leaves further directions weakly observable; a landmark seen
  from one viewpoint has no depth constraint; a graph without loops cannot correct drift.

## Procedure

```text
graph  <- empty factor graph;  values <- empty initial estimate
anchor the gauge: prior on the first pose (and scale for monocular), or a free gauge
for each new keyframe:
    add variables with initial values from odometry or the IMU
    add odometry / IMU / projection factors with whitened noise models
    for each loop candidate from place recognition:
        geometric verification in the front-end (RANSAC, inlier count, covariance)
        add the loop factor with a robust treatment (robust loss, switch variable or DCS)
    update: batch LM/GN on the whole graph, or iSAM2 update on the affected part
    diagnose: whitened residuals per factor type; loops whose weight collapsed;
              odometry residuals that jumped after a loop was added
    optional: marginal covariances of selected variables, with the gauge declared
```

Purpose of the steps. *Anchoring* removes the gauge freedom or declares it. *Whitened
noise models* make factors of different units comparable (CV-SVD). *Front-end
verification* removes most false loops before they reach the back-end; the robust
treatment handles the rest. *Incremental updates* keep latency bounded in the common case.
*Diagnosis per factor type* is necessary because the total cost always decreases when a
factor is satisfied, even a wrong one.

## Mathematics, conventions and units

### From factor graph to sparse least squares

For factors $\phi_k(X_k)$, the posterior is $p(X\mid Z)\propto\prod_k\phi_k(X_k)$. With
Gaussian measurement models, $-\log$ turns the MAP into a nonlinear least-squares problem

$$X^*=\arg\min_X\sum_k\|r_k(X_k)\|^2_{\Sigma_k^{-1}}=\arg\min_X\sum_k r_k^T\Sigma_k^{-1}r_k ,$$

a sum of squared Mahalanobis norms whose residuals are whitened by their covariances.
Linearized at the current estimate, each step solves $\arg\min_\Delta\|A\Delta-b\|^2$, where
$A$ is the whitened Jacobian [Kaess et al. 2012, §2, eq. 5]. A factor depends only on its
own variables, so $A$ is sparse, with one block row per factor. Eliminating the variables
of a Gaussian factor graph one by one is equivalent to a sparse QR factorization of $A$
[§2, Gaussian case]; the resulting Bayes net is the square-root information matrix, and
iSAM2 organizes it as a Bayes tree of cliques [§3].

A relative-pose factor between $T_i$ and $T_j$ with measurement $Z_{ij}$ uses the tangent
residual $r_{ij}=\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)\in\mathbb R^6$, whose block order and
units (m and rad) must match its $6\times6$ covariance (CV-SE3, CV-FACTEURS-003 appendix).

### Gauge as a null space

If every factor depends only on relative quantities, transforming all poses by the same
$G$ leaves every residual unchanged: $(GT_i)^{-1}(GT_j)=T_i^{-1}T_j$. The linearized system
then has a null space. *Worked example B (constructed, recomputed by the check script)*:
three 1-D poses linked by three unit-weight relative factors give the information matrix
$\begin{bmatrix}2&-1&-1\\-1&2&-1\\-1&-1&2\end{bmatrix}$, whose rows sum to zero and whose
determinant is 0; adding a prior of weight $10^{-6}$ on the first pose makes the determinant
$3\cdot10^{-6}$. The system becomes solvable, but only because of a nearly uninformative prior:
invertibility is not absolute information. Zhang et al. compare three treatments — fixing
the unobservable states, adding a prior, or leaving the gauge free and using a
pseudo-inverse — and find similar accuracy and computation time, the free gauge being
slightly faster, and covariances that look very different but are related by a
transformation [abstract, Table I]. Gauge choices also shape how uncertainty looks: anchoring
the first frame makes later poses appear increasingly uncertain [Zhang et al., Fig. 1;
Triggs et al. 2000, §9].

### Robust back-ends for loop closures

- *Robust losses* (Huber, Cauchy, Geman–McClure) on loop factors down-weight large whitened
  residuals ([CV-SVD](11-moindres-carres-svd.md), CV-SVD-008).
- *Switchable constraints* multiply each loop residual by a switch function
  $\Psi(s_{ij})$, with the linear choice $\Psi(s)=s$ constrained to $[0,1]$, and add a switch
  prior $\|\gamma_{ij}-s_{ij}\|^2_{\Xi_{ij}}$ with $\gamma_{ij}=1$; the loop's information
  becomes $\Psi(s_{ij})^2\Lambda_{ij}^{-1}$ [Sünderhauf and Protzel 2012, eq. 1, §II-A, §II-B].
  $\Xi_{ij}$ sets the penalty for disabling a loop and influences the result [§IV-A].
- *Dynamic covariance scaling (DCS)* solves for the switch in closed form at each
  evaluation, $s=\min\big(1,\ \frac{2\Phi}{\Phi+\chi^2_l}\big)$, where $\chi^2_l$ is the loop's
  current whitened squared error and $\Phi:=\Xi^{-1}$, and scales the loop information by
  $s^2$ without extra variables [Agarwal et al. 2013, §III eq. 6, §IV eq. 14–15]. Without the
  bound $s\le1$ and with $\Phi=1$ its weight resembles the Geman–McClure M-estimator
  [§IV-A].
- *RRR* searches for the largest set of mutually consistent loops and rejects the others,
  whereas switchable constraints and DCS keep rejected loops with a low weight
  [Agarwal et al., §II].

*Worked example C (constructed, recomputed by the check script)*: with $\Phi=1$, a loop at
$\chi^2_l=9$ keeps $s=0.2$ and 4% of its information, and a correct 6-D loop sitting at its
expected $\chi^2$ of 6 already gets $s=2/7$. Applied as a fixed-point iteration to example A,
DCS switches off the false loop ($s\approx8\cdot10^{-6}$) but also nearly switches off the
*correct* one ($s\approx0.02$, drift left at 9.96 cm): its 10 cm residual is 10 standard
deviations of the loop factor, although it is only 3.2 standard deviations of the
accumulated odometry ($\sqrt{10}$ cm). With a 5 cm loop standard deviation the correct loop
keeps $s\approx0.45$ but removes only about 8% of the drift. The scale is in units of the
loop's own covariance, so an overconfident loop covariance makes DCS reject the large
corrections a loop exists to make. Agarwal et al. report small errors for
$0.1<\Phi<10$ on their datasets, which corrupt loops by injected outliers [§V-E]; the toy
shows why the loop covariance must be honest, not that DCS fails in general.

### Incremental update with iSAM2

A new factor changes only the Bayes-tree cliques on the paths between the cliques
containing its variables and the root. iSAM2 removes that top of the tree, re-interprets
it as a factor graph with the new factors, reorders, eliminates and reinserts the
unaffected "orphan" subtrees [Kaess et al. 2012, §3.3, Alg. 4]. Variable ordering governs
fill-in, hence clique sizes; finding the ordering with minimal fill-in is NP-hard, and
iSAM2 uses constrained COLAMD to push the most recently accessed variables to the end of
the ordering, i.e. close to the root, so that the next updates touch a smaller part of the
tree [§3.4]. *Fluid relinearization* relinearizes a variable only when its delta exceeds a
threshold $\beta$, and marks the cliques involving it and all their ancestors for
re-elimination [§4.1, Alg. 5–6]; because variables have different units, "one simple
solution is to take the minimum over all thresholds", and on the Manhattan dataset
$\beta=0.1$ gives a nearly exact solution at a significantly reduced cost [§4.1, Fig. 9].
*Partial state updates* stop the back-substitution in subtrees where the delta changes by
less than $\alpha$, a threshold on the change of $\Delta$ rather than on $\Delta$ itself
[§4.2, Alg. 7]. The paper's comparisons use $\alpha=0.001$ and $\beta=0.1$ [§5]. A loop
connecting distant parts of the trajectory affects a long path to the root, so the cost of
one update is not constant.

### Marginalization

Removing variables by marginalization is a Schur complement of the information matrix,
as in the reduced bundle system [Triggs et al. 2000, §6.1]. It keeps their information as a dense prior on the variables
they were connected to. The constraint is not deleted; it becomes a correlated factor
whose linearization point is frozen (project deduction from the Schur reduction).

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Factor noise models $\Sigma_k$ | From sensor characterization and front-end covariance | Relative weight of odometry, loops, projections, IMU | Overconfident loop covariances defeat DCS (example C); double counting shrinks uncertainty |
| Robust treatment of loops | Huber or Cauchy scale in whitened units; SC switch prior $\Xi$; DCS $\Phi=1$ suggested, small errors for $0.1<\Phi<10$ on the authors' datasets [Agarwal et al., §V-E] | Trade-off between rejecting false loops and keeping true ones | Large true corrections look like outliers at first; evaluate with a fixed front-end |
| Gauge treatment | Fixed first pose, prior, or free gauge [Zhang et al.] | Expression of the solution and of its covariance | A prior weight is not information; disconnected components need anchors |
| iSAM2 relinearization threshold $\beta$ | Paper 0.1; GTSAM 4.2 `relinearizeThreshold` default 0.1, scalar or per variable type and dimension | Accuracy versus relinearization cost | Units differ between rotations, translations and landmarks |
| iSAM2 partial-update threshold $\alpha$ | Paper 0.001; GTSAM 4.2 Gauss–Newton `wildfireThreshold` default 0.001 (Dogleg $10^{-5}$) | Accuracy versus back-substitution cost | Applies to the change of the delta |
| `relinearizeSkip` | GTSAM 4.2 default 10 updates | How often relinearization is checked | Larger values save time but delay corrections after a loop |
| Factorization | GTSAM 4.2 default Cholesky; QR "slower but more numerically stable" | Speed versus robustness to ill-conditioning | Cholesky may raise `IndefiniteLinearSystemException` when uncertainties span many orders |

Tuning approach (project method), on recorded sequences with ground truth and a frozen
front-end output:

1. Characterize factor noise from data (odometry residuals on straight segments,
   reprojection residuals, IMU Allan deviation) before touching the back-end.
2. Inject known false loops at controlled rates and patterns, following the outlier
   policies of the robust back-end papers (random, local, grouped) [Sünderhauf and Protzel,
   §III-C; Agarwal et al., §V], and sweep the robust parameter ($\Phi$, $\Xi$, loss scale)
   while watching both false-loop rejection and true-loop retention.
3. Sweep $\beta$ and $\alpha$ on the longest sequences and record the error against batch
   optimization and the latency distribution per update, not only its mean.

## Properties and limits of guarantees

- **MAP equivalence.** The least-squares solution is the MAP estimate only under the
  Gaussian, independent-factor model; robust losses change the model.
- **Local optimality.** Nonlinear solvers return a local minimum; robust kernels make the
  cost non-convex and depend on initialization.
- **Exactness of incremental solutions.** With relinearization and partial-update
  thresholds, iSAM2 approximates the batch solution; the approximation is controlled by
  $\beta$ and $\alpha$ and was nearly exact at $\beta=0.1$ on Manhattan [Kaess et al., §4.1].
- **Robust back-ends.** Switchable constraints and DCS never delete a loop; a rejected loop
  keeps a small weight. RRR makes an explicit accept/reject decision [Agarwal et al., §II].
  None of them repairs a front-end whose false loops are numerous and mutually consistent
  (project reasoning).
- **Gauge invariance.** Relative quantities are gauge-independent; absolute coordinates and
  their covariances are not.

## Cost and implementation

Cost drivers. Batch elimination cost depends on fill-in, i.e. on the variable ordering and
the graph topology; clique sizes grow with loops that couple distant variables. An iSAM2
update costs roughly the re-elimination of the affected top of the tree plus relinearized
cliques: small for odometry-only steps, large after a long loop [Kaess et al., §3.3–§4.3].
Marginal covariances require additional elimination work and are usually computed for a
few variables only. In bundle adjustment, the Schur complement on landmarks keeps the
reduced camera system small (CV-BA).

### Implementation contracts

Read in the cited versions; no solver was executed for this note, and the worked examples
were recomputed with the Python standard library only.

- **GTSAM 4.2, `ISAM2Params`** [gtsam/nonlinear/ISAM2Params.h]: `relinearizeThreshold`
  default 0.1, either a scalar or a map from variable type to per-dimension thresholds (the
  header's example uses 0.1 rad for rotations and 0.5 m for translations of a `Pose3`);
  `relinearizeSkip` 10; `enableRelinearization` true; factorization `CHOLESKY` by default,
  with `QR` recommended when Cholesky throws on a poorly conditioned problem;
  `ISAM2GaussNewtonParams::wildfireThreshold` 0.001 and
  `ISAM2DoglegParams::wildfireThreshold` $10^{-5}$; `enablePartialRelinearizationCheck`
  false by default, flagged "use with caution" (L35–L48, L67–L90, L135–L245).
- **GTSAM 4.2, `noiseModel::mEstimator::DCS`** [gtsam/linear/LossFunctions.cpp
  L353–L372]: weight $(2c/(c+e^2))^2$ when $e^2>c$ and 1 otherwise, with $e$ the whitened
  distance, i.e. $s^2$ of DCS with $\Phi=c$.
- **GTSAM 4.2, `Pose3`** tangent vectors are ordered rotation first, $[\omega,v]$, so
  covariance blocks of pose factors differ from the $[\rho,\theta]$ order of Solà et al.
  ([CV-SE3](12-rotations-se3.md)).
- **Ceres Solver 2.2.0, `Covariance`**: handling a gauge requires an SVD or custom
  inversion; `SPARSE_QR` fails on a rank-deficient Jacobian, `DENSE_SVD` handles it for
  small or moderate problems ([CV-SVD](11-moindres-carres-svd.md)).

## Evaluation and controlled variation

**Metrics.** Trajectory accuracy after the allowed alignment (absolute and relative
errors, see [CV-VIO](../../60-vision-3d/references/63-slam-vio.md)); distributions of
whitened residuals per factor type, which should match their dimension on average when
the model is right; loop-level decisions (true loops retained, false loops suppressed);
update latency percentiles and their spikes at loop closures.

**Proposed baseline and controlled variation (not executed).**

- *Question*: how much distortion does a fixed rate of false loops cause with each robust
  back-end?
- *Data*: recorded sequences with ground truth and a frozen set of verified loop
  candidates, so that only the back-end changes.
- *Baseline*: plain least squares with the verified loops only.
- *Controlled variation*: add the same set of false loops (for example 1, 10 and 100,
  random or grouped) to every configuration; compare least squares, a Cauchy loss,
  switchable constraints and DCS with $\Phi=1$.
- *Measurements*: relative pose error, fraction of true loops with a weight above 0.5,
  number of iterations and wall time.
- *Expected effect (hypothesis)*: least squares degrades with the first false loop; robust
  back-ends keep the error close to baseline for random outliers and degrade for grouped,
  mutually consistent ones; true loops with large corrections lose weight when their
  covariance is overconfident (example C).
- *Confound*: changing the front-end threshold at the same time would mix association
  quality with back-end robustness.

**Measurement limits.** A low total cost or a small residual on the added loop does not
validate it, because the loop moved the poses it is evaluated on. Ground-truth alignment
choices change absolute errors. Runtime comparisons depend on implementation, ordering and
hardware; DCS's reported speed advantage is specific to the authors' g2o setting.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Map bends after a loop while the total cost decreases | False loop accepted with high weight | Re-optimize without the loop; compare odometry residuals before and after | Stricter verification; robust back-end; loop covariance from the estimator |
| True loop has no effect | Loop down-weighted by DCS or a robust loss; overconfident loop covariance | Inspect the loop's final weight $s$; compare its residual with accumulated odometry uncertainty | Honest covariance; larger $\Phi$ or scale; staged acceptance after verification |
| Solver fails or returns huge covariances | Gauge not fixed; disconnected components | Rank of the linear system; connectivity of the graph | Anchor each component; free-gauge pseudo-inverse with declared gauge |
| Uncertainty too small after fusing several sources | Same evidence inserted twice; correlated factors treated as independent | Trace measurement provenance | Remove duplicates or model correlation |
| Latency spikes at some keyframes | Large loop affecting a long path to the root; relinearization wave | Log affected clique count and relinearized variables per update | Budget for spikes; tune $\beta$, `relinearizeSkip`; defer large loops |
| Slow drift of the estimate compared with batch | Thresholds $\alpha$ or $\beta$ too large; partial relinearization check enabled | Compare with a periodic batch solution | Lower thresholds; per-type thresholds; disable the partial check |
| Wrong poses with consistent residuals | Wrong tangent order or frame of a factor's covariance | Perturb one variable dimension and see which residual block responds | Align factor conventions with the library (CV-SE3) |
| `IndefiniteLinearSystemException` | Cholesky on a poorly conditioned problem | Condition and scale of variables | QR factorization; better scaling; fix the gauge |

## Alternatives and applications

Conditional choices:

- **Prefer a filter** ([CV-FUSION](13-kalman-ekf-eskf.md)) when only the current state is
  needed at minimal latency and past states will not be revised.
- **Prefer a pose graph** when the front-end summarizes local mapping into relative poses
  and global consistency after loops is the goal; **prefer full bundle adjustment** when
  landmark geometry and camera calibration must be refined jointly.
- **Prefer incremental smoothing (iSAM2)** for online systems with frequent small updates
  and occasional loops; **prefer periodic batch optimization** when updates are rare or
  latency spikes are unacceptable but a background thread is available.
- **Prefer robust kernels or DCS** when false loops are rare and independent; **prefer an
  explicit consistency test such as RRR** when an accept/reject decision is required;
  **prefer stronger front-end verification** when false loops are numerous or mutually
  consistent.

Industrial uses (project reasoning, not published results): warehouse robots and drones
whose maps must survive repetitive aisles; multi-camera rigs whose extrinsics are refined
jointly with trajectories; augmented-reality devices that close loops on revisited rooms
and need bounded update latency.

## Guided reasoning and proposed checks

These constructed cases develop the graph, the gauge and the cost of an elimination. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-FACTEURS-001

**Working question**: A factor graph is often described as a system's “SLAM.” What does it actually represent, and what must still be supplied or chosen to obtain a trajectory?

**Reference answer**: it is a bipartite graph between variables (poses, landmarks, biases) and factors (measurements, priors) that factorizes the posterior density. With Gaussian measurement models, the MAP becomes a nonlinear least-squares problem on residuals weighted by their covariance (squared Mahalanobis norms). It remains to provide the associations and loop closures coming from the front-end, the measurement models and their covariances, an initial estimate and an anchoring of the gauge. It is also necessary to choose the inference: batch optimization, iSAM2, robust losses.

**Constructed example**: adding a distance factor does not have the same meaning as adding an absolute pose. The two connect variables according to different information and do not remove the same ambiguities. Check the contract for each factor before concluding that a graph contains "enough" constraints.

### Case linked to CV-FACTEURS-005

**Working question**: When new measurements arrive, what does iSAM2 actually recompute in its Bayes tree, and which two thresholds limit relinearization and estimate updates?

**Reference answer**: Only the cliques on the paths between the root and the variables affected by new factors or selected for relinearization are removed, reordered and re-eliminated with these factors; unaffected subtrees are reinserted as is. Fluid relinearization: a variable is relinearized only if its delta from the linearization point exceeds a threshold $\beta$. Partial update: back-substitution stops in subtrees where the changes of the delta remain below a threshold $\alpha$.

**Product consequence**: measure latency peaks when significant constraints are added, not just the average during straight-line motion. A small usual update and a large loop closure do not necessarily touch the same portion of the system. The budget must provide for this variability and for the threshold trade-off.

**Source consulted for this pass**: [GTSAM, Introduction](https://gtsam.org/tutorials/intro.html), factor graph, Values and prior. The other developments are in the [flashcards](../14-graphes-facteurs.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-FACTEURS-001

**Situation**: A factor graph is often described as a system's “SLAM.” What does it actually represent, and what must still be supplied or chosen to obtain a trajectory?

**From probability to cost**: a factorization $p(X\mid Z)\propto\prod_k\phi_k(X_k)$ becomes, through the negative logarithm, a sum of local contributions. For Gaussian observations of fixed covariance $\Sigma_k$, each factor contributes $\tfrac12 r_k^T\Sigma_k^{-1}r_k$. The factor connects only the variables $X_k$ on which its observation depends; its Jacobian therefore has zero blocks elsewhere. This locality creates the sparse structure that the solver exploits. If a covariance itself depends on the parameters, its determinant no longer necessarily constitutes a constant in the likelihood: reusing the simple quadratic cost would require a justification. False associations can respect the structure of the graph while making it represent the wrong problem.

### CV-FACTEURS-002

**Situation**: Why can optimization of relative poses require an anchor despite having many observations?

**Seeing the gauge in a constraint**: for poses camera→world $T_i$, the relative prediction is $T_i^{-1}T_j$. Transforming all the poses by the same $G$ gives $(GT_i)^{-1}(GT_j)=T_i^{-1}T_j$. The cost cannot therefore choose $G$ from these measurements alone. The gauge appears as null directions of the linearized system, distinct from a merely poor precision on an observed direction. Fixing a pose eliminates this freedom; a finite-covariance prior adds stated information that can influence the solution. In a VIO, the theoretical gauge freedoms assume adequate excitation and a correct model: degenerate movements can leave other parameters little or not observable.

### CV-FACTEURS-003

**Situation**: After loop closure, the cost decreases but the map bends inconsistently. What should be tested?

**Defining a pose residual**: If $Z_{ij}$ is a measurement of $T_i^{-1}T_j$, a possible residual is $r_{ij}=\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, a tangent vector with six components in a stated order convention. Translation in meters and rotation in radians require consistent covariance and whitening. Inverting only the measurement without adapting its direction, frame and covariance changes the factor. After optimization, this residual depends on the poses it has itself moved; its small value can therefore hide a loop that has distorted the entire graph. Examine the other factors affected and an external reference, not just the error of the added loop.

### CV-FACTEURS-004

**Situation**: A place-recognition front end inevitably produces some false loop closures, for example in identical corridors. Which back-end strategies should be compared to prevent map distortion, and how should one be chosen?

**Constructed DCS weight example**: with $\Phi=1$ and a whitened squared error $\chi_l^2=9$, the formula gives $s=0.2$ and information multiplied by $s^2=0.04$. This is neither a probability that the loop is true nor a binary deletion: an erroneous constraint can still exert a force on the optimum. The weight should be recalculated with the current solution in the chosen scheme. A real loop initially very far away can be weakened, while a false loop compatible with an already deformed map can retain weight. The evaluation must therefore separate acceptance of real loops, resistance to false loops and behaviour as a function of initialization.

### CV-FACTEURS-005

**Situation**: When new measurements arrive, what does iSAM2 actually recompute in its Bayes tree, and which two thresholds limit relinearization and estimate updates?

**Why the elimination order matters**: Eliminating a variable creates a constraint between the variables that were connected to it. These extra links fill in the triangular factors; their structure determines the size of the cliques and the paths affected by an update. A long loop can make a lot of constraints coupled without adding a lot of variables. Incremental inference reuses the work compatible with the new information, but cannot ignore the dependencies actually created. Relinearization thresholds refer to increments of different types: meters, radians or other parameters must have consistent tolerances. A single number without scaling convention does not represent the same accuracy for each state.

**Passages consulted for these developments**: [GTSAM, Factor Graphs](https://gtsam.org/tutorials/intro.html), §§2.3–2.4, graph, Values and optimization; [Kaess et al. 2012, iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf), §§3–4, elimination and relinearization; [Agarwal et al. 2013, DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf), §§III–IV, equations 2 and 15.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FACTEURS-001 — Independent factors require independent evidence

If the same relative-pose estimate is inserted twice as if the factors were independent, its information matrix is effectively doubled. The optimizer may return an apparently better-conditioned system while understating uncertainty. A graph can therefore be structurally valid and statistically wrong. Track measurement provenance when visual odometry, loop closure and a fused pose share observations; either model their correlation or state the independence approximation rather than hiding it in factor count.

### CV-FACTEURS-002 — A disconnected graph needs more than one anchor

Constructed case: two independent pose chains each contain only relative constraints. Anchoring a pose in the first chain removes its global gauge but leaves the second chain free. A solver failure after adding an anchor can therefore indicate disconnected components rather than an insufficient prior weight. Inspect connectivity and the expected gauge of every component before increasing damping. A numerical prior can make the matrix invertible while concealing an unobserved relationship between maps.

### CV-FACTEURS-003 — A loop can win its own residual test

A heavily weighted false loop can force its endpoints together, making its own optimized residual small while spreading strain across many odometry factors. Compare whitened residual changes over the affected graph, and evaluate relative transformations against evidence not used by that loop. A useful proposed test keeps the front-end candidates fixed and varies only loop acceptance or covariance, so changed geometry can be attributed to the disputed constraint rather than another association run.

### CV-FACTEURS-004 — Convergence speed is a measured tradeoff

DCS avoids adding one optimized switch variable per loop, but this does not establish faster convergence for every graph, initialization or implementation. Compare wall time, iteration count and recovered geometry on a controlled set of true and false loops. Also inspect true loops that start with a large residual: aggressive downweighting can reject the very constraint needed to correct drift. The scaling parameter is a robustness choice in whitened error units, not a universal probability threshold.

### CV-FACTEURS-005 — A small update can still be globally expensive

Adding one loop between distant parts of a trajectory can affect cliques on a long path to the root. Incremental inference therefore does not imply constant work per frame. Proposed profiling should separate factor insertion, relinearization, reordering, elimination and back-substitution, while recording the size of the affected tree. Otherwise a long-tail latency spike may be misdiagnosed as merely too many incoming measurements rather than a change in graph dependencies.

Consulted foundations: [Kaess et al., iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf): abstract accessible on 2026-11-08 (§§3–4 re-read on 2026-11-14, see the body); [Agarwal et al., DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf): §IV dynamic covariance scaling; experimental convergence is dataset-specific.

## Sources and flashcards

### Scientific sources

- [Kaess, Johannsson, Roberts, Ila, Leonard and Dellaert 2012, iSAM2: Incremental Smoothing and Mapping Using the Bayes Tree, IJRR](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf): §2 (factor graphs, nonlinear least squares, eq. 5, Gaussian case: elimination equivalent to sparse QR), §3.3 and Alg. 4 (incremental inference), §3.4 (incremental variable ordering, CCOLAMD), §4.1 with Alg. 5–6 and Fig. 9 (fluid relinearization, $\beta$, units), §4.2 with Alg. 7 and Fig. 10 (partial state updates, $\alpha$), §5 (parameters $\alpha=0.001$, $\beta=0.1$).
- [Agarwal, Tipaldi, Spinello, Stachniss and Burgard 2013, Robust Map Optimization using Dynamic Covariance Scaling, ICRA](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf): abstract (perceptual aliasing), §II (RRR, max-mixtures), §III eq. 6 (switchable constraints, $\Phi:=\Xi^{-1}$), §IV eq. 14–15 and §IV-A (DCS, relation to Geman–McClure), §V and §V-E (g2o Gauss–Newton setting, outlier types, sensitivity to $\Phi$).
- [Sünderhauf and Protzel 2012, Switchable Constraints for Robust Pose Graph SLAM, IROS (authors' preprint)](https://nikosuenderhauf.github.io/assets/papers/IROS12-switchableConstraints.pdf): eq. 1, §II-A (linear switch function), §II-B (switch prior), §III-C (outlier policies), §IV-A (influence of $\Xi$).
- [Zhang, Gallego and Scaramuzza 2018, On the Comparison of Gauge Freedom Handling in Optimization-based Visual-Inertial State Estimation, RA-L (authors' preprint)](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf): abstract, Fig. 1, §I, Table I.
- [Triggs, McLauchlan, Hartley and Fitzgibbon 2000, Bundle Adjustment — A Modern Synthesis](https://inria.hal.science/inria-00548290): §6.1 (Schur complement), §9 (gauge freedom).

### Implementation sources

- [Dellaert, Factor Graphs and GTSAM: A Hands-on Introduction](https://gtsam.org/tutorials/intro.html): §1 (bipartite factor graph), §§2.3–2.4 (graph and `Values`), §4.1 (prior on the first pose), §7 (iSAM and Bayes tree); quoted in the 2026-10-23 report, not re-read.
- [GTSAM 4.2, `gtsam/nonlinear/ISAM2Params.h`](https://github.com/borglab/gtsam/blob/4.2/gtsam/nonlinear/ISAM2Params.h): Gauss–Newton and Dogleg parameters (L35–L90), `ISAM2Params` members and defaults (L135–L245).
- [GTSAM 4.2, `gtsam/linear/LossFunctions.cpp`](https://github.com/borglab/gtsam/blob/4.2/gtsam/linear/LossFunctions.cpp#L353-L372): `DCS::weight` and `DCS::loss` (L353–L372).
- [Ceres Solver 2.2.0, `docs/source/nnls_covariance.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_covariance.rst): Gauge Invariance, Rank of the Jacobian, `Covariance::Options`.

### Related flashcards and references

- [Flashcards](../14-graphes-facteurs.md): CV-FACTEURS-001 to CV-FACTEURS-005.
- Related references: [CV-SVD](11-moindres-carres-svd.md), [CV-SE3](12-rotations-se3.md), [CV-FUSION](13-kalman-ekf-eskf.md), [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md), [CV-VIO](../../60-vision-3d/references/63-slam-vio.md).

The 1-D graphs, the proposed protocol and the diagnostic tests are reasoning of the project; no SLAM run, image, video or hardware result is claimed as measured.

Drafted by agent, 2026-10-18. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation. Revision 11, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/14-graphes-facteurs.md).
