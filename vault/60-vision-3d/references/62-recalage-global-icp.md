---
id: CV-ICP
type: pipeline
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 9
prerequis: ["CV-SE3", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Global registration and local ICP

This is the pipeline note for rigid registration of 3D point clouds: a global stage
that needs no initial pose (geometric descriptors and robust estimation), followed
by a local stage that refines the pose with the Iterative Closest Point (ICP)
algorithm. Rotation parametrization lives in [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md),
least-squares conditioning in [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md)
and the RANSAC sampling budget in [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md);
this note links to them instead of repeating them.

## Problem and data contract

**Task.** Given a source cloud $P=\{p_i\}_{i=1}^{N_p}$ and a target cloud
$Q=\{q_j\}_{j=1}^{N_q}$ of the same rigid scene or object, estimate the transformation
$T=(R,t)\in SE(3)$ such that $Rp+t$ lands on the target surface for every source point
that lies in the overlap. Besl and McKay register a "data" shape to a "model" shape;
their example data shape "represents a major portion of the model shape", and they
treat the removal of statistical outliers as a preprocessing step [Besl and McKay,
abstract and §I]. Real scan pairs usually break both conditions: overlap is partial
and outliers remain.

**Data contract.**

- *Points*: $N\times3$ arrays of coordinates in one unit (meters for most LiDAR and
  depth sensors, millimeters for many metrology scanners); Open3D stores them as
  double-precision vectors. Every distance parameter below is in that unit.
- *Normals*: optional $N\times3$ unit vectors, required on the target for
  point-to-plane ICP and on both clouds for FPFH descriptors. They are estimated, so
  they carry noise and an arbitrary sign.
- *Initial guess*: a $4\times4$ homogeneous matrix applied to the source. Without
  one, the global stage must produce it.
- *Output*: $T_{\text{target}\leftarrow\text{source}}$ as a $4\times4$ matrix, the
  correspondence set (index pairs), and quality figures. Open3D's
  `registration_icp(source, target, ...)` returns the matrix that moves the source onto
  the target, with a `fitness` and an `inlier_rmse` whose exact definitions are given
  in the implementation section. Record the direction and the unit with every pose:
  an inverted transform or a meter/millimeter confusion produces a plausible-looking
  number that is wrong.

**Role in a pipeline.** Stitching partial scans into one model, aligning a scan to a
CAD model for inspection or bin picking, localizing a LiDAR scan in a prior map,
estimating the extrinsics between two depth sensors
([CV-MULTICALIB](../../50-calibration-geometrie/references/55-calibration-multicapteurs.md))
and producing odometry or loop-closure constraints for a pose graph
([CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md)).
Downstream consumers need more than a pose: a pose graph needs an information
matrix, an inspection report needs to know which regions were actually constrained,
and a robot needs a reject signal when registration is ambiguous.

## Intuition

ICP answers two questions in turn: *which target point corresponds to each source
point?* and *which rigid motion best aligns these pairs?* With the pose fixed, the
closest point is the best guess of a correspondence; with the pairs fixed, the best
rigid motion has a closed form or a small linear system. Alternating the two lowers
the mean squared distance at every iteration, but only down to the nearest local
minimum [Besl and McKay, §IV-B]. ICP therefore needs a start inside the right basin.

The global stage removes that requirement by matching on *shape* instead of
*position*. A descriptor such as FPFH summarizes how normals turn within a
neighborhood; it does not depend on where the cloud is or how it is rotated, so
descriptor matches can be formed between clouds that are far apart. Most of these
matches are wrong, and a robust estimator (RANSAC, TEASER++) keeps the subset that
agrees on one rigid motion.

*Illustration (constructed).* A machined bracket is scanned after being rotated by
90° on a fixture, and the scan is registered to its CAD model. From the identity pose,
the closest CAD points to the scanned flange belong to the wrong face; ICP shrinks
these distances and stops in a pose that is wrong by tens of degrees. FPFH matches the
bracket's edges and drilled holes regardless of the rotation, RANSAC finds three
mutually consistent matches, and ICP started from that pose converges to the
fixture's actual placement. If the bracket were symmetric, two placements would fit
equally well and neither stage could tell them apart from geometry alone.

```mermaid
flowchart LR
    A["Source and target clouds<br/>same unit, known direction"] --> B["Voxel downsampling"]
    B --> C["Normals<br/>radius about 2 voxels"]
    C --> D["FPFH descriptors<br/>radius about 5 voxels"]
    D --> E["Descriptor matches<br/>optional mutual filter"]
    E --> F["Robust estimate<br/>RANSAC or TEASER++"]
    F --> G["Local ICP<br/>point-to-plane, tight threshold"]
    G --> H["Checks: overlap, residual map,<br/>constraint eigenvalues, landmarks"]
    H -->|"ambiguous or poorly constrained"| I["Reject or ask for a prior"]
    H -->|"accepted"| J["Pose, direction, unit,<br/>quality figures"]
```

*Diagram: project synthesis of the Open3D 0.19.0 global-registration tutorial
pipeline and the acceptance checks developed below. The ratios to the voxel size are
those of the tutorial, not general rules.*

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md)
(composition order, small-angle rotations);
[CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md)
(normal equations, conditioning). Useful background, by mechanism:

- RANSAC budget and inlier ratio: [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md);
- nearest-neighbor search and kd-trees: [CV-FLANN](../../40-features-matching/references/48-flann.md);
- where clouds come from (depth, density, noise): [CV-STEREO](61-stereo-profondeur.md), [CV-BEV](64-nuages-bev-occupation.md);
- odometry or IMU priors as initial guesses: [CV-VIO](63-slam-vio.md);
- combining many pairwise registrations: [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md).

**Target competencies**: explain why each stage exists, apply the pipeline with
unit-consistent parameters, compare ICP variants under stated conditions, interpret
fitness and RMSE under their definitions, and diagnose a wrong or poorly
constrained pose.

## Assumptions, observability and degenerate cases

- **Rigidity and known scale.** One $SE(3)$ transform explains every overlapping
  point. Moving objects, a deforming part or LiDAR motion distortion violate it and
  appear as spatially clustered residuals. Unknown scale needs a similarity estimator;
  TEASER++ estimates scale separately [Yang et al., §V].
- **Overlap.** Besl and McKay's convergence proof pairs *every* data point with the
  model [§IV-B]. With partial overlap, points outside it must be rejected, and pairs
  involving mesh boundaries bias the pose systematically [Rusinkiewicz and Levoy, §3.4,
  Fig. 13].
- **Initialization inside the basin.** ICP converges to the local minimum whose
  "region of attraction" contains the start; Besl and McKay note that the only way to
  be sure of the global minimum is to try enough initial states, because the partition
  into basins differs for each shape [§V].
- **Geometric constraint.** The point-to-plane system constrains a motion only if some
  normals or torque arms oppose it. Gelfand et al. list shapes that leave motions
  unconstrained when aligned with a copy of themselves. Their simplest example, "two
  planes", is one planar surface aligned with another: it leaves the two in-plane
  translations and the rotation about the normal free [§2.2]. Their Fig. 3 shows a
  familiar shape for each combination: plane (2 translations, 1 rotation), sphere
  (3 rotations), cylinder (1 rotation, 1 translation), cone (1 rotation) and a profile
  extruded along a line (1 translation); a helix, with one free screw motion, is
  mentioned but not drawn [§2.2, Fig. 3]. A scene made of two *non-parallel* planes,
  such as a floor and a wall, is a different case: only the translation along their
  intersection line stays free (worked example B). A straight corridor of constant,
  non-circular cross-section is an extrusion and leaves only the translation along its
  axis free; a circular tunnel is a cylinder and also frees the rotation about its axis
  (application to these scenes: project deduction, worked example E). These are rank
  deficiencies: the cost is flat along them.
- **Symmetry.** A part with a discrete symmetry has several isolated minima with the
  same cost. This is not a rank deficiency, so the eigenvalue check below does not
  reveal it; only an asymmetric feature or a prior can.
- **Normals and sampling.** Normals come from neighborhoods of finite size: too small
  and noise dominates, too large and edges are smoothed. Two scans rarely sample the
  same surface points, so point-to-point distances keep a floor of the order of the
  point spacing even at the true pose, whereas point-to-plane distances do not
  (project deduction from the two objectives).

## Procedure

```text
# Global stage (no initial pose)
P', Q' <- voxel_downsample(P, Q, v)                  # equalize density, bound cost
estimate_normals(P', Q', radius = r_n)               # needed by FPFH and point-to-plane
F_P, F_Q <- fpfh(P', Q', radius = r_f)               # rotation-invariant local shape
C <- nearest_in_descriptor_space(F_P, F_Q, mutual)   # mostly wrong matches
T0 <- robust_rigid(C, eps)                           # RANSAC with pruning, or TEASER++
# Local stage (refinement)
T <- T0
repeat:
    pairs <- closest_target_point(T * P, Q, d_max)   # reject pairs beyond d_max
    dT <- argmin_dT  sum_i (n_i . (dT*T*p_i - q_i))^2 # linearized point-to-plane step
    T <- dT * T                                      # correction applied on the left
until change(fitness, rmse) small or max iterations
# Acceptance
check overlap, residual map, eigenvalues of the 6x6 system, held-out landmarks
```

Purpose of the steps. *Downsampling* makes density uniform, which descriptors and
residual statistics assume, and bounds the cost. *Normals* give the local plane used
by point-to-plane and by the FPFH angles. *Descriptor matching* creates hypotheses
without a pose. *Robust estimation* selects a geometrically consistent subset; three
non-collinear pairs fix a rigid motion. *ICP* turns a coarse pose into a tight one
on the full-resolution clouds; its threshold $d_{\max}$ encodes the expected residual
error of the initial pose. *Acceptance* is a separate step because a low residual
does not show that the pose is right.

Rusinkiewicz and Levoy classify ICP variants by the stage they change [§1]:

| Stage | Options in the literature [Rusinkiewicz and Levoy, §3] | What the paper reports |
| --- | --- | --- |
| Selection | All points, uniform or random subsampling, normal-space sampling | Similar on a well-conditioned scene; only normal-space sampling converged on the "incised plane" scene [§3.1, Figs. 2–3] |
| Matching | Closest point (kd-tree), normal shooting, projection into the range image | Projection converges less per iteration but costs constant time per point, hence converges faster in time on range images [§3.2] |
| Weighting | Constant, by distance, by normal compatibility, by sensor uncertainty | Effect on convergence "small and highly data-dependent" [§3.3] |
| Rejection | Fixed distance, worst $n\%$, $2.5\sigma$, pair consistency, mesh boundaries | Does not speed up convergence; boundary rejection avoids a systematic bias with partial overlap [§3.4] |
| Error metric | Point-to-point (closed form), point-to-plane (no closed form) | Point-to-plane converged much faster on the "fractal" and "incised plane" scenes [§3.5, Figs. 15–16] |
| Minimization | Iterate, extrapolate, restart from perturbations, random subsets | Extrapolation helps point-to-point; restarts avoid spurious minima [§3.5] |

## Mathematics, conventions and units

**Conventions.** A source point maps to the target frame as $x=Rp+t$, with
$R\in SO(3)$ dimensionless and $t$ in the cloud unit. A correction $\Delta T$ expressed
in the target frame is composed on the left, $T_{k+1}=\Delta T\,T_k$, as Open3D does.
Residuals are lengths, costs are squared lengths; rotation increments $\omega$ are in
radians.

**Point-to-point.** Besl and McKay minimize, for $N_p$ pairs $(p_i,x_i)$,

$$f(R,t)=\frac{1}{N_p}\sum_{i=1}^{N_p}\lVert x_i-Rp_i-t\rVert^2 .$$

With centroids $\mu_p,\mu_x$ and cross-covariance
$\Sigma_{px}=\frac{1}{N_p}\sum_i(p_i-\mu_p)(x_i-\mu_x)^T$, the optimal rotation is the
unit quaternion given by the eigenvector of the largest eigenvalue of a symmetric
$4\times4$ matrix built from $\Sigma_{px}$, and $t=\mu_x-R\mu_p$ [Besl and McKay,
eqs. 22–26]. SVD-based solutions of the same problem exist and differ little in
accuracy [Rusinkiewicz and Levoy, §3.5]; Open3D calls `Eigen::umeyama`.

**Monotone convergence.** Let $e_k$ be the mean squared distance to the closest points
at iteration $k$ and $d_k$ the value after the least-squares step on those pairs. Then
$0\le d_{k+1}\le e_{k+1}\le d_k\le e_k$: the step cannot increase the error for fixed
pairs, and re-pairing with closest points cannot increase it for a fixed pose
[Besl and McKay, §IV-B, eqs. 31–35]. The sequence converges, to a local minimum. The
proof uses all points and the true closest-point operator; with a distance threshold
or trimming, the set of pairs changes between iterations and the chain no longer
holds as stated (project deduction). Open3D's ICP is therefore not guaranteed to
decrease its reported RMSE at every iteration.

**Point-to-plane.** With target normals $n_i$ (unit, dimensionless),

$$E(R,t)=\sum_i\big(n_i^T(Rp_i+t-q_i)\big)^2 ,$$

which counts only the error along the normal and lets coincident surfaces slide
tangentially [Rusinkiewicz and Levoy, §3.5]. No closed form exists; the usual solution
linearizes the rotation, $R\approx I+[\omega]_\times$ ("$\sin\theta\sim\theta$,
$\cos\theta\sim1$"). Each pair then contributes one linear equation
$a_i^T\xi=b_i$ in $\xi=(\omega,t)\in\mathbb R^6$, with

$$a_i=\begin{pmatrix}p_i\times n_i\\ n_i\end{pmatrix},\qquad b_i=n_i^T(q_i-p_i),$$

solved in the least-squares sense from the $6\times6$ system $\big(\sum_i a_ia_i^T\big)\xi=\sum_i a_ib_i$
[Low, eqs. 4–8]. The rotation is rebuilt from $\omega$ and the step is iterated,
because the linear model is only valid for small rotations.

*Worked example A (constructed, recomputed by checks/62-recalage-global-icp.py).* For a
point 1 m from the rotation center, the linear model misplaces a rotated point by
$\lVert Rp-(I+[\omega]_\times)p\rVert\approx\theta^2/2$ times the lever arm: 3.8 mm for
a 5° step and 0.15 mm for 1°. A single linearized step from a 5° error therefore leaves
a millimeter-level error that later iterations must remove, and steps of tens of
degrees are not meaningful.

**Which motions are constrained.** The matrix $W=\sum_i a_ia_i^T$ is the
"covariance matrix" $C$ of Gelfand et al. [eq. 4]. Moving the source by a small
$x=(\delta\omega;\delta t)$ from the optimum raises the error by $\Delta E=x^TWx$
[eq. 5], so each eigenvalue is the cost of a unit motion along its eigenvector: an
eigenvector with a small eigenvalue is a screw motion along which the meshes can slide
with little increase of error, and the condition number
$c=\lambda_{\max}/\lambda_{\min}$ measures stability [Gelfand et al., §2.2, §3.1].
Rotation columns of $a_i$ carry the lever arm $p_i$ in length units, translation
columns do not, so the authors first move the centroid to the origin and scale the
points to a mean distance of 1 before comparing eigenvalues; this equalizes the
displacement a point can contribute by "torque" and by "force" [§3.1]. Centring and
scaling are an invertible change of coordinates, $W'=MWM^T$, so they preserve the rank
and an exactly free direction; they change every ratio between eigenvalues, which is
what a noisy, merely ill-conditioned scene must be judged on (project deduction,
worked example E). The paper gives no universal threshold: it reports a condition
number of 66.1 for two noisy planar patches with grooves, on which uniform sampling
failed to align the grooves, and 3.7 after its covariance-based selection of 30% of
the points [§5, Figs. 4–5]. Adding uniformly sampled points does not help, since they
are as likely to come from the flat areas as from the constraining features [§2.2].

*Worked example B (constructed, recomputed by checks/62-recalage-global-icp.py).*
Sample a $4\times4$ grid on each face of a corner of size 1 m:

- the floor alone ($n=(0,0,1)$) gives rows $(y,-x,0,0,0,1)$: rank 3, with
  $t_x$, $t_y$ and $\omega_z$ unconstrained;
- floor plus one wall gives rank 5: the translation along their intersection line
  stays free, whatever the sampling density;
- three orthogonal planes give rank 6;
- the full corner has a condition number of 32.7 in meters but $1.13\times10^7$ in
  millimeters, while the normalized version gives 5.34 in both. A raw condition
  number therefore mixes geometry and units.

*Worked example E (constructed, recomputed by the check script of the 2026-11-15
pass; CV-ICP-006).* A corridor along $x$, 10 m long, 2 m wide and 2.5 m high (floor,
ceiling, two walls), sampled every 0.1 m (9,494 points):

- normalized, $W$ has one eigenvalue exactly 0 with the pure translation $t_x$ as its
  eigenvector; the rotation about the axis comes next at 0.098 of the largest
  eigenvalue, constrained by the lever arms of the floor, ceiling and walls;
- floor plus one wall of the same corridor gives the same single free direction,
  $n_1\times n_2$, the intersection line;
- two door jambs facing along the corridor (42 points) make the smallest eigenvalue
  non-zero: normalized $c\approx125$, with an eigenvector whose $t_x$ component still
  exceeds 0.999.
  A 5 cm slide along $x$ raises $E$ by 0.105 m², a 5 cm vertical slide by 10.6 m²;
- without normalization, the same scan gives $c=4{,}456$ in meters with the origin at
  the entrance and $4.4\times10^9$ in millimeters. In a map frame whose origin lies
  100 m behind and 50 m beside the entrance, the weakest eigenvector is a rotation
  about that distant origin almost cancelled by a translation ($|t_x|<0.01$), not the
  corridor slide.

**FPFH.** For a point pair $(p_i,p_j)$ with normals $(n_i,n_j)$, Rusu et al. build a
Darboux frame $u=n_i$, $v=(p_j-p_i)\times u$, $w=u\times v$ and compute three angular
features, $\alpha=v\cdot n_j$, $\phi=u\cdot(p_j-p_i)/\lVert p_j-p_i\rVert$ and
$\theta=\arctan(w\cdot n_j,\,u\cdot n_j)$ [Rusu et al., eq. 1]. The simplified
histogram SPFH of a point bins these features over its $k$ neighbors within radius
$r$; the FPFH adds the neighbors' SPFHs weighted by distance,
$\mathrm{FPFH}(p)=\mathrm{SPF}(p)+\frac1k\sum_{k}\frac{1}{\omega_k}\mathrm{SPF}(p_k)$
[eq. 4], so its support extends to $2r$ [§III-A]. The three features are binned
separately and concatenated; Open3D uses 11 bins per feature, hence 33 dimensions.
All quantities are relative, so FPFH is invariant to rigid motion; it depends on the
radius, the normals (sign included) and the sampling density.

**Robust estimation.** With an inlier ratio $w$ among descriptor matches and samples
of $n=3$ pairs, the number of samples needed for an all-inlier sample with probability
$p$ is $k=\log(1-p)/\log(1-w^n)$; see [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).
TEASER++ replaces sampling by a truncated least-squares (TLS) cost and decouples the
unknowns: differences of matched points, $b_j-b_i=sR(a_j-a_i)+o_{ij}+\epsilon_{ij}$,
cancel the translation (translation-invariant measurements), and their norms cancel
the rotation; pairs whose lengths disagree beyond the noise bound cannot both be
inliers, so the maximum clique of the consistency graph prunes most outliers before
rotation and translation are estimated [Yang et al., abstract, §V-A, §V-B, §VI-D].

*Worked example C (constructed, recomputed by checks/62-recalage-global-icp.py).* With
$p=0.999$ and $n=3$: $w=0.5$ needs 52 samples, $w=0.1$ needs 6,905, $w=0.05$ needs
55,259, and $w=0.02$ needs about 863,000. Open3D's default cap of 100,000 iterations at
$w=0.02$ gives only a 55% chance of drawing one all-inlier sample. The inlier ratio of
descriptor matches, not the point count, sets the cost of RANSAC.

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Voxel size $v$ | 0.05 (5 cm) in the Open3D global tutorial | Density, noise averaging, cost | Every radius below is tied to it; too coarse erases the features FPFH needs |
| Normal radius, `max_nn` | $2v$, 30 | Normal noise versus edge smoothing | A line-like neighborhood has no defined normal (CV-ICP-005) |
| FPFH radius, `max_nn` | $5v$, 100 | Descriptor context | Must exceed the normal radius; larger is more distinctive and slower, and crosses object borders |
| Mutual filter | `True` in the tutorial | Keeps matches that are nearest neighbors both ways | Raises the inlier ratio $w$, may leave too few matches |
| RANSAC distance threshold | $1.5v$ ("liberal") | Inlier test of a hypothesis | In length units; must cover downsampling error |
| Edge-length checker | 0.9 | Rejects samples whose pairwise lengths differ by more than 10% | Cheap rigidity test before full validation |
| `RANSACConvergenceCriteria` | 100,000 iterations, confidence 0.999 | Budget and early stopping | Insufficient at low $w$ (example C) |
| ICP threshold $d_{\max}$ | 0.02 (ICP tutorial); $0.4v$ for refinement after RANSAC | Which pairs enter the objective | Too wide accepts foreign surfaces; too tight drops constraints and lowers fitness |
| `ICPConvergenceCriteria` | `relative_fitness=1e-6`, `relative_rmse=1e-6`, `max_iteration=30` | When ICP stops | Absolute differences; the RMSE one is in the cloud unit |
| Estimation | Point-to-point, point-to-plane, optional robust kernel | Speed of convergence, sliding | Point-to-plane needs target normals |

The voxel ratios come from the Open3D tutorial on one indoor dataset; they are a
starting point, not a validated rule.

Tuning approach (project method). Use scan pairs from the deployment domain with a
reference pose (fiducials, a calibrated fixture or a surveyed map), disjoint from the
final test set.

1. Measure the sensor noise and the point spacing in the overlap; choose $v$ above the
   noise and below the smallest feature that must be registered.
2. Set the radii as multiples of $v$ and check normal quality on known planes.
3. Measure the descriptor inlier ratio $w$ against the reference and size the RANSAC
   budget with example C, or switch to a maximum-clique method when $w$ is very low.
4. Sweep $d_{\max}$ against the distribution of initial errors left by the global
   stage; watch the success rate, not the final RMSE.
5. Fix acceptance thresholds on fitness, residual maps and the normalized condition
   number on held-out pairs, including symmetric and degenerate cases.

Rescale every length parameter when the unit changes (CV-ICP-004).

## Properties and limits of guarantees

- **Local, monotone, not global.** The convergence theorem guarantees a
  non-increasing mean squared error and convergence to a local minimum, for complete
  closest-point pairing [Besl and McKay, §IV-B]. It says nothing about the global
  minimum, which the authors approach by testing a set of initial registrations [§V].
  Empirically, they observed fast progress in the first iterations, then slow
  convergence, with 30–50 iterations reaching an error of about 0.1% of the model size
  in their tests [§IV-B].
- **Point-to-plane convergence.** Faster convergence of point-to-plane over
  point-to-point is an empirical result on synthetic range images, from single runs
  [Rusinkiewicz and Levoy, §2 and §3.5], not a theorem. The same mechanism that speeds
  convergence, sliding along surfaces, also leaves degenerate directions free.
- **Asymmetry.** Closest-point matching from source to target is not symmetric, and
  Open3D's fitness is normalized by the source size. Swapping source and target
  changes the correspondences, the fitness and possibly the result.
- **Invariances.** FPFH is invariant to rigid motion but not to density, radius,
  noise or normal sign. The closed-form point-to-point step is exact for given pairs;
  the whole ICP result depends on the initial pose.
- **Robust estimators.** RANSAC's stopping rule is probabilistic and relies on an
  estimate of $w$. TEASER's certificate concerns the optimality of the TLS problem it
  solves; with a symmetric scene, the largest consistent set can belong to a wrong
  pose: on a 3DMatch pair of a hotel shower, symmetries let a wrong pose collect 57
  consistent matches while the ground truth admits 3, and the maximum clique excludes
  the true inliers [Yang et al., §XI-E, Fig. 11 caption].
- **Quality figures.** Fitness and inlier RMSE are summaries of the accepted pairs.
  They are not probabilities of a correct pose and are comparable only for the same
  threshold, direction and density.

## Cost and implementation

Cost drivers, with their variables:

- **Closest points.** For $N_p$ source and $N_x$ target points, $O(N_pN_x)$ worst case
  and $O(N_p\log N_x)$ on average with a kd-tree; the registration step is $O(N_p)$
  [Besl and McKay, §IV-A]. Building the kd-tree is a fixed cost; projection matching
  on range images avoids it [Rusinkiewicz and Levoy, §3.2].
- **Point-to-plane step.** Accumulating the $6\times6$ system is $O(N)$; the solve is
  constant-size.
- **Descriptors.** PFH evaluates all pairs of a $k$-neighborhood, $O(nk^2)$; FPFH
  evaluates $k$ pairs per point, $O(nk)$ [Rusu et al., §III]. For $k=100$ that is
  4,950 pairs against 100 per point (recomputed by checks/62-recalage-global-icp.py).
- **RANSAC.** Each hypothesis costs a 3-point solve and, when it passes the checkers, a
  validation over the whole source cloud; the number of hypotheses grows as
  $1/w^3$ (example C).
- **Reported speeds.** Rusinkiewicz and Levoy align two range images with 2,000 point
  pairs used throughout the paper in about 30 ms with projection matching and
  point-to-plane, against more than one second for their baseline, on a 550 MHz
  Pentium III [§2, §4]. TEASER++ solves
  problems with many outliers "in less than 10ms" on a laptop with an i7-8850H CPU for
  the Bunny benchmark with 100 correspondences [Yang et al., §XI and §XI-B]. These figures depend
  on hardware, correspondence counts and implementation.

### Open3D 0.19.0 contracts

Read in the v0.19.0 sources and the 0.19.0 tutorials; no code was executed for this
note. Line numbers refer to the files listed in the implementation sources.

- `registration_icp` builds the correspondences as the nearest target point within
  `max_correspondence_distance` (kd-tree hybrid search with one neighbor), without a
  mutual check [Registration.cpp, L21–L69]. `fitness` is the number of
  correspondences divided by the number of **source** points and `inlier_rmse` is the
  RMSE of point-to-point distances over those correspondences [L59–L67]. The tutorial
  text says "# of points in target"; the code divides by the source size. The
  reported RMSE is point-to-point even when the estimation is point-to-plane.
- Each update is composed on the left, `transformation = update * transformation`
  [L143]. Iteration stops when both $|\Delta\text{fitness}|$ and
  $|\Delta\text{inlier\_rmse}|$ fall below `relative_fitness` and `relative_rmse`, or
  after `max_iteration` [L149–L154]; defaults are $10^{-6}$, $10^{-6}$ and 30
  [Registration.h, L45–L50]. Despite their names, these are absolute differences, as
  the header comment "relative change (difference)" concedes, and the RMSE tolerance
  is a length in the cloud unit.
- `TransformationEstimationPointToPoint` uses `Eigen::umeyama` [TransformationEstimation.cpp,
  L32–L44]. `TransformationEstimationPointToPlane` requires target normals, uses the
  residual $(p-q)\cdot n$ and the Jacobian row $(p\times n,\;n)$ (rotation first),
  weights each row with an optional robust kernel and solves one Gauss–Newton step
  per iteration [L79–L110, L114–L133].
- `compute_fpfh_feature` returns 33 values per point, 11 bins for each of the three
  angles [Feature.cpp, L85, L101–L111]. Neighbor SPFHs are weighted by the inverse
  *squared* distance and each sub-histogram is normalized to 100, following PCL rather
  than the paper's formula, as a code comment states [L119–L165].
- `registration_ransac_based_on_feature_matching` forms correspondences by nearest
  neighbor in FPFH space, optionally mutual [Feature.cpp, L167–L229], applies the
  checkers to each 3-point hypothesis, validates surviving hypotheses on the whole
  cloud, and lowers its iteration budget with
  $k=\log(1-p)/\log(1-w^{n})$, where $w$ is the inlier ratio of the correspondences
  under the best hypothesis [Registration.cpp, L159–L295]; the header comment names
  the fitness instead. Defaults: 100,000 iterations, confidence 0.999
  [Registration.h, L81–L84].
- `get_information_matrix_from_point_clouds` returns a $6\times6$ information matrix
  built from point-to-point correspondences, rotation first [Registration.cpp,
  L297–L346]; it is the input expected by Open3D's pose-graph tools.

## Evaluation and controlled variation

**Metrics.** With a reference pose $(R_{gt},t_{gt})$: the rotation error
$\arccos\big((\operatorname{tr}(R_{gt}^TR)-1)/2\big)$ in degrees, the translation error
$\lVert t-t_{gt}\rVert$ in the cloud unit (state the rotation center), the success rate
under joint thresholds, and the runtime. Rusinkiewicz and Levoy measure the RMS
distance between *true* corresponding points on synthetic data, because the
algorithm's own error estimate can disagree with ground truth: in their Fig. 3 the
ground-truth error increases briefly in early iterations, which the caption presents
as the difference between the two [§2, Fig. 3 caption]. Fitness and inlier RMSE are diagnostics, not accuracy.

*Worked example D (constructed, recomputed by checks/62-recalage-global-icp.py).* At one
fixed pose, 10 of 100 source points lie 1 mm from the target and 90 lie 30 mm away. A
5 mm threshold reports fitness 0.1 and inlier RMSE 1 mm; a 50 mm threshold reports
fitness 1.0 and RMSE 28.5 mm. If only 40% of a 10,000-point source overlaps the
target, fitness cannot exceed 0.4 even at the exact pose.

**Data.** Synthetic transforms of real scans give exact ground truth and controllable
noise, overlap and initial error; the test scenes of Rusinkiewicz and Levoy separate
low-frequency, all-frequency and high-frequency geometry [§2.1]. Real benchmarks such
as 3DMatch provide scan pairs with reference poses [Yang et al., §XI-E]. Industrial
references come from fixtures, fiducials or a coordinate measuring machine.

**Published results with their protocol.** On the Bunny with 100 synthetic
correspondences and known scale, TEASER, TEASER++, GORE and RANSAC with a 60-second
budget were robust up to 90% outliers and FGR up to 70%; with 1,000 correspondences,
TEASER++ remained robust up to 99%, largely because maximum-clique pruning removes
most outliers [Yang et al., §XI-B]. On the Open3D demo pair with threshold 0.02,
point-to-point ICP raises fitness from 0.175 to 0.372 in 30 iterations and to 0.621
with 2,000 iterations, while point-to-plane reaches 0.621 within 30 iterations
(documentation output, not re-executed).

### Proposed baseline and controlled variation (not executed)

- **Question**: in the local stage, does point-to-plane improve accuracy and
  convergence over point-to-point on the deployment data, and where?
- **Data**: held-out scan pairs with reference poses, stratified by the normalized
  condition number of example B (well-constrained, near-planar, symmetric parts).
- **Baseline**: Open3D 0.19.0, tutorial ratios scaled to the measured noise, FPFH and
  RANSAC global stage run once per pair with a fixed seed, then point-to-plane ICP
  with $d_{\max}=0.4v$ and `max_iteration` raised to 200.
- **Controlled variation**: replace the local estimator by point-to-point; reuse the
  same global poses, thresholds and criteria.
- **Measurements**: rotation and translation errors, success rate under joint
  thresholds, iterations to the stopping rule, runtime, and the eigenvalues of $W$ at
  the final pose.
- **Expected effect (hypothesis)**: fewer iterations for point-to-plane on
  well-constrained pairs; on near-planar pairs both may stay wrong along the
  unconstrained directions, which only the eigenvalue analysis reveals.
- **Confound**: the stopping rule compares absolute changes of fitness and of a
  point-to-point RMSE, so iteration counts partly measure the criterion. Report errors
  at a fixed iteration count as well.

**Measurement limits.** A reference pose has its own error, which bounds the
accuracy that can be claimed. Symmetric parts need a symmetry-aware error or an
explicit statement that ambiguity counts as failure. Results from single runs, as in
Rusinkiewicz and Levoy, do not give variability.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Low inlier RMSE, low fitness, wrong pose | Threshold too tight; ICP converged on one corner of the overlap | Fitness in both directions; residual map over the whole overlap; held-out landmarks | Coarse-to-fine thresholds from the global stage's error; better initialization; report overlap (CV-ICP-003) |
| High fitness and low RMSE, pose shifted along a plane, corridor or axis | Degenerate geometry; motion in the nullspace of $W$ | Eigenvalues of the normalized $W$ at the final pose (examples B and E; CV-ICP-006) | Normal-space sampling; odometry or IMU prior on the free directions; report the free directions instead of a pose |
| Part registered upside down or rotated by its symmetry | Several isolated minima with equal cost | Compare the best hypotheses of the global stage; check an asymmetric feature | Asymmetric landmarks, fixture constraints or an explicit ambiguity flag |
| RANSAC result varies between runs or is wrong | Low descriptor inlier ratio $w$; budget too small | Measure $w$ against a reference; compute $k$ (example C) | Mutual filter, retuned radii, larger budget, maximum-clique pruning (TEASER++) |
| Few or meaningless FPFH matches | Radius inconsistent with voxel size or density; noisy normals; different sensors | Feature-distance histogram of true versus random pairs; normal quality on planes | Retune $v$ and radii together; equalize density |
| Everything breaks after a unit change | Thresholds, voxel and radii left in the old unit; stopping tolerance in the old unit | Bounding-box size of the clouds versus parameter values | Scale every length parameter by the same factor (CV-ICP-004) |
| Point-to-plane raises an error or does nothing | Target without normals | `has_normals()` on the target | Estimate normals with a radius tied to $v$ |
| Few-millimeter bias with partial overlap | Pairs on boundaries or on surfaces seen by one scan only | Residuals concentrated near borders | Reject boundary pairs [Rusinkiewicz and Levoy, §3.4]; tighter final threshold |
| Residual clusters on some objects only | Moving objects, deformation, LiDAR motion distortion | Spatial clustering of residuals; timestamps | Mask dynamic regions; deskew scans before registration |

## Alternatives and applications

Conditional choices:

- **Prefer FPFH with RANSAC** when no prior pose exists, the surfaces have local
  structure at a resolvable scale, and the descriptor inlier ratio is moderate.
- **Prefer a maximum-clique or TLS method such as TEASER++** when the inlier ratio is
  very low or when a certificate of the robust problem's optimality is wanted; it does
  not resolve symmetric ambiguity.
- **Prefer an odometry, IMU, kinematic or fixture prior** when one exists: it removes
  the global search and constrains directions that the geometry leaves free.
- **Prefer point-to-plane ICP** for refinement on smooth surfaces with reliable
  normals; **point-to-point** when normals are unreliable, on very sparse clouds, or
  when the closed-form step is wanted inside another estimator.
- **Prefer intensity- or color-aided registration** when the geometry is degenerate but
  the texture is not; Rusinkiewicz and Levoy note that color can supply the missing
  constraints [§2]. Open3D's colored ICP follows Park et al. 2017, not reviewed here.
- **Prefer a pose graph over chained pairwise ICP** for many scans, so that loop
  constraints distribute the drift ([CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md)).

Industrial uses (project reasoning, not published results): CAD-to-scan
registration for dimensional inspection, where the deviation map is meaningful only
in regions that constrain the pose; bin picking, where symmetric parts need explicit
ambiguity handling; LiDAR localization in a prior map, where corridors and tunnels
produce degenerate directions that an odometry prior must cover; extrinsic
calibration between two depth sensors with a target that constrains all six motions.

## Guided reasoning and proposed checks

These constructed cases develop initialization, correspondences and weakly
constrained directions. They explain or test reasoning; no image, video or hardware
result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-ICP-001

**Working question**: Why combine FPFH/RANSAC with subsequent ICP instead of initializing ICP from any arbitrary pose?

**Reference answer**: The global initialization looks for a compatible zone from matches; ICP refines locally and can converge on bad associations.

**Why the initialization matters**: ICP builds or updates associations from the current pose. If this pose is far away, the nearest neighbors can belong to other surfaces; optimizing on these pairs can reinforce a local misalignment. Global search uses other cues to propose a pose region before refinement.

**Constructed example**: Two identical supports on a part can offer two plausible local alignments. A small residual after ICP does not by itself indicate the correct support. Check the final orientation and translation, the overlap and held-out distinctive surfaces. Record the source→target direction and the units before any comparison. Geometric features and RANSAC provide useful hypotheses; they remain limited by geometric texture, symmetry and overlap. An odometry or application constraint can provide another initialization if it is justified and evaluated.

### Case linked to CV-ICP-005

**Working question**: Is point-to-plane ICP always a better replacement for point-to-point ICP?

**Reference answer**: It exploits reliable normals and a geometry that constrains the useful motions; it can be ill-posed on some surfaces or with noisy normals.

**Comparison of the information used**: Point-to-point penalizes a position difference along all three components; point-to-plane uses a local planar approximation of the surface. When normals and initialization are suitable, this approximation can be effective. If the normals are unstable or the geometry poor, the criterion may lose its advantage or leave some directions weakly constrained.

**Constructed ablation**: Keep the clouds, initial correspondences, threshold and reference fixed, then compare the variants while varying normal noise and overlap separately. Measure pose error, convergence, failures and cost. A drop in the residual specific to one variant is not directly comparable to the residual of another formulation. The right choice depends on the observed surfaces and the required accuracy. Do not use a single favorable case to claim superiority for all parts and all initializations.

**Documentation consulted for this pass**: [Open3D 0.19.0, ICP registration](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html), point-to-plane ICP and evaluation. The other developments are in the [flashcards](../62-recalage-global-icp.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-ICP-001

**Situation**: Why combine FPFH/RANSAC with subsequent ICP instead of initializing ICP from any arbitrary pose?

**Concrete local loop**: At iteration $k$, transform each source point by $T_k$, search for target neighbors, reject incompatible pairs, and then estimate a correction $\Delta T_k$. With a correction expressed in the target coordinate frame, compose $T_{k+1}=\Delta T_kT_k$. A correction expressed in the source coordinate frame is composed on the other side, $T_{k+1}=T_k\Delta T_k$: mixing these conventions produces an incorrect optimization trajectory. Neighbor matching and pose solving are two different steps. A good initialization makes physically correct associations easier, while a threshold that is too wide can accept foreign surfaces and a threshold that is too strict removes the constraints needed for refinement.

### CV-ICP-002

**Situation**: What does $n^T(Rp+t-q)$ measure in point-to-plane ICP?

**Linearization of the residual**: Let $s=Rp+t$ and apply a small left perturbation $s'\simeq s+\delta t+\delta\omega\times s$. The residual becomes $r'\simeq r+n^T\delta t+(s\times n)^T\delta\omega$. Its Jacobian is therefore a row of six components, ordered translation then rotation. Stacking these rows shows directly which motions the scene constrains. If all normals are vertical, horizontal translations do not appear in this local model. This derivation assumes fixed matches and normals during the step; updating them at the next iteration makes the overall problem more complex than a single linear system.

### CV-ICP-003

**Situation**: ICP reports low RMSE but aligns only a corner of two point clouds. What should be reported?

**Effect of the threshold on statistics**: If the distances are $d_1,\ldots,d_m$, the RMSE is $\sqrt{\sum_i d_i^2/m}$. Removing all large distances can reduce it while greatly reducing $m$; the two experiments no longer concern the same points. Comparing the two directions, source→target and target→source, can also reveal asymmetric coverage, especially with different densities. An analysis per predefined physical region prevents a dense area from dominating the score. These measurements complement the pose error against a reference; they do not, on their own, remove the ambiguity of a perfectly symmetric object.

### CV-ICP-004

**Situation**: Why does reusing an ICP threshold of 0.02 after converting point clouds from meters to millimeters change the problem?

**Residuals and covariance**: If all lengths are multiplied by $a$, a metric residual becomes $r'=ar$ and its covariance becomes $\Sigma'=a^2\Sigma$. The normalized residual $r^T\Sigma^{-1}r$ then remains invariant. A robust loss whose scale is set in meters also requires a converted scale, unlike a loss applied after a correctly propagated whitening. Absolute displacement or cost tolerances change meaning with units; relative criteria must be interpreted according to their exact definition. In Open3D 0.19.0, for example, `relative_rmse` is an absolute change of the inlier RMSE in the cloud unit, so the default $10^{-6}$ becomes a thousand times stricter physically after a conversion to millimeters. This reasoning distinguishes a consistent unit change from a deliberate change of physical weighting in a registration or a fusion of constraints.

### CV-ICP-005

**Situation**: Is point-to-plane ICP always a better replacement for point-to-point ICP?

**Where the normals come from**: A common local estimator centers the neighbors, computes their covariance matrix and takes the eigenvector of the smallest eigenvalue as the plane normal. A neighborhood that is too small becomes sensitive to noise; one that is too large mixes edges and curved surfaces. If the eigenvalues do not single out a normal direction, the local surface is itself ambiguous. For the squared point-to-plane residual alone, reversing the sign of a normal does not change the cost; a consistent orientation may nevertheless be required by other steps such as descriptors or rejection rules. Report pose quality together with this explained provenance of the normals.

**Passages consulted for these developments**: [Open3D 0.19.0](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html), point-to-point and point-to-plane ICP; project linearization and scale analyses; [Open3D 0.19.0](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/global_registration.html), FPFH and RANSAC; no Open3D execution.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-ICP-001 — Global initialization is also a hypothesis

Repeated geometry can give a plausible global alignment to the wrong copy of a structure. ICP can then reduce local residuals while preserving that incorrect correspondence basin. Validate overlap extent and independently known landmarks after refinement, rather than accepting a lower ICP objective as confirmation of the initializer. In a proposed comparison, include large initial displacements and symmetric alternatives, and report rejected registrations as well as final errors.

### CV-ICP-002 — A plane leaves tangential motion unpenalized

For target normal $n=(0,0,1)^T$, the residual becomes the difference in height. Translating all transformed points parallel to the plane leaves it unchanged, as does rotation about the plane normal for an ideal infinite plane. A small point-to-plane residual can therefore coexist with substantial tangential pose error. This constructed nullspace example motivates inspecting normal diversity and the linearized system, not simply reducing the distance threshold.

### CV-ICP-003 — The denominator can improve the score by exclusion

Constructed example: retaining 10 close pairs with 1 mm error and rejecting 90 distant points yields 1 mm inlier RMSE but little evidence of whole-cloud alignment. Report accepted-pair fraction, the source/target direction of that fraction, coverage and threshold with RMSE. Evaluate pose error independently where possible. Changing the correspondence threshold changes both the accepted population and its conditional error, so two RMSE values are not automatically comparable.

### CV-ICP-004 — Scale changes affect normal estimation too

Converting meters to millimeters requires scaling correspondence thresholds, voxel size and normal-neighborhood radii by 1000. Unit normals remain dimensionless, but the neighborhoods used to estimate them change if their radius is left unchanged. Residual variance scales by $10^6$. Thus even when the transform translation is converted correctly, an inconsistent preprocessing radius can alter normals, matches and the convergence behavior.

### CV-ICP-005 — Normal reliability depends on neighborhood geometry

For a local point covariance with eigenvalues $\lambda_1\le\lambda_2\le\lambda_3$, a well-separated small $\lambda_1$ supports a plane normal. If both first eigenvalues are small, the neighborhood is line-like and its normal direction is ambiguous; if all are comparable, a plane may be a poor model. These are geometry diagnostics rather than universal cutoffs. Neighborhood scale, range noise and mixed surfaces must be evaluated for the intended registration.

Consulted foundations: [Open3D 0.19 ICP](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html): point-to-point versus point-to-plane objectives, initialization and evaluation; Context7 checked.

## Sources and flashcards

### Scientific sources

- [Besl and McKay 1992, "A Method for Registration of 3-D Shapes", IEEE TPAMI 14(2)](https://doi.org/10.1109/34.121791): abstract and §I (data and model shapes, outliers removed beforehand), eqs. 22–26 (closed-form quaternion solution), §IV-A (algorithm, costs, termination), §IV-B (convergence theorem, eqs. 31–35, observed iteration counts), §V (basins of attraction and initial registrations). Read in the scanned copy hosted by Stanford's CS164 course.
- [Rusinkiewicz and Levoy 2001, "Efficient Variants of the ICP Algorithm", 3DIM](https://www.cs.princeton.edu/~smr/papers/fasticp/fasticp_paper.pdf): §1 (six-stage taxonomy), §2 and §2.1 (methodology, test scenes, ground-truth error), §3.1–§3.5 (selection, matching, weighting, rejection, metrics and minimization; Figs. 2–3, 13, 15–16), §4 (high-speed combination, 30 ms).
- [Low 2004, "Linear Least-Squares Optimization for Point-to-Plane ICP", UNC TR04-004](https://www.comp.nus.edu.sg/~lowkl/publications/lowk_point-to-plane_icp_techrep.pdf): §2 eq. 1 (objective), §3 eqs. 4–8 (small-angle linear system).
- [Gelfand, Ikemoto, Rusinkiewicz and Levoy 2003, "Geometrically Stable Sampling for the ICP Algorithm", 3DIM](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf): §2 (6×6 covariance matrix for point-to-plane), §2.1 (error minimization, covariance matrix eq. 4, error increase eq. 5), §2.2 (two planes, eigenvectors of small eigenvalues, uniform points do not help; Fig. 3 shapes read on the rendered page), §3.1 (screw motions, condition number, normalization), §5 with Figs. 4–6 (condition numbers 66.1 and 26.9 before, 3.7 and 4.1 after covariance sampling).
- [Rusu, Blodow and Beetz 2009, "Fast Point Feature Histograms (FPFH) for 3D Registration", ICRA](https://www.cvl.iis.u-tokyo.ac.jp/class2016/2016w/papers/6.3DdataProcessing/Rusu_FPFH_ICRA2009.pdf): §II-A eq. 1 (Darboux frame and angles), §III (FPFH, eq. 4, $O(nk)$, $2r$ support, decorrelated histograms), §IV (SAC-IA).
- [Yang, Shi and Carlone 2020, "TEASER: Fast and Certifiable Point Cloud Registration", arXiv 2001.07715](https://arxiv.org/html/2001.07715): abstract, §I (RANSAC runtime and outliers), §V-A and §V-B (TIMs and TRIMs), §VI-D (maximum clique), §XI introduction (hardware), §XI-B (benchmarks, timing), §XI-E and Fig. 11 caption (3DMatch symmetric failure).
- Chen and Medioni 1992 (point-to-plane, normal shooting): not re-read; cited through Rusinkiewicz and Levoy §3.2 and §3.5 and through Low §1.

### Implementation sources

- [Open3D 0.19.0, ICP registration tutorial](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html): `evaluate_registration`, fitness and inlier RMSE text, point-to-point and point-to-plane runs.
- [Open3D 0.19.0, global registration tutorial](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/global_registration.html): preprocessing ratios, FPFH (33 dimensions), RANSAC checkers and criteria, refinement threshold.
- [Open3D v0.19.0, `cpp/open3d/pipelines/registration/Registration.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.cpp): correspondences and metrics (L21–L69), ICP loop and stopping rule (L108–L157), RANSAC (L159–L295), information matrix (L297–L346).
- [Open3D v0.19.0, `Registration.h`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.h): `ICPConvergenceCriteria` (L29–L62), `RANSACConvergenceCriteria` (L64–L93).
- [Open3D v0.19.0, `TransformationEstimation.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/TransformationEstimation.cpp): point-to-point (L20–L44), point-to-plane (L65–L133).
- [Open3D v0.19.0, `Feature.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Feature.cpp): SPFH bins (L80–L117), FPFH weighting (L119–L165), feature correspondences and mutual filter (L167–L229).

### Related flashcards and references

- [Flashcards](../62-recalage-global-icp.md): CV-ICP-001 (global initialization and refinement), CV-ICP-002 (point-to-plane residual), CV-ICP-003 (misleading consensus), CV-ICP-004 (units), CV-ICP-005 (choosing a variant), CV-ICP-006 (degenerate geometry from the normalized $6\times6$ matrix).
- Related references: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md), [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md), [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md), [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md), [CV-VIO](63-slam-vio.md), [CV-BEV](64-nuages-bev-occupation.md).

Drafted by agent, 2026-10-18. Revision 8, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/62-recalage-global-icp.md).
Revision 9, 2026-11-15: CV-ICP-006 added after the learner accepted P-CV-ICP-02, the Fig. 3 shapes and
the stability matrix aligned with Gelfand et al., and worked example E added, by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-15-accepted-proposals/62-recalage-global-icp.md).
