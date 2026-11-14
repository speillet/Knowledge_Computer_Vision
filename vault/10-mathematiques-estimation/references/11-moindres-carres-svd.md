---
id: CV-SVD
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 10
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Least squares, SVD and conditioning

This method note covers the linear algebra under most geometric estimators of the
vault: linear least squares, the homogeneous systems of direct linear transformation
(DLT) estimators, nonlinear refinement by Gauss–Newton and Levenberg–Marquardt (LM),
robust losses and the covariance of the result. Its central question is not only
"which solver" but "which parameter combinations do the data actually determine".
Model-specific details are linked rather than repeated:
[homography and RANSAC](../../50-calibration-geometrie/references/51-ransac-homographie.md),
[Zhang calibration](../../50-calibration-geometrie/references/52-calibration-zhang.md),
[epipolar geometry, PnP and triangulation](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md)
and [bundle adjustment](../../50-calibration-geometrie/references/54-bundle-adjustment.md).

## Problem and data contract

**Task.** Estimate $n$ parameters from $m$ noisy scalar observations ($m\ge n$ in the
identifiable case) and report how well each parameter combination is determined.
Three forms recur:

- *linear*: $\min_x\|Ax-b\|_2$ with $A\in\mathbb R^{m\times n}$ and $b\in\mathbb R^m$
  (line or plane fit, a calibration step that is linear in its unknowns);
- *homogeneous*: $\min_h\|Lh\|_2$ subject to $\|h\|_2=1$, with $h$ defined up to
  scale (homography DLT with $L\in\mathbb R^{2N\times9}$ for $N$ correspondences;
  eight-point algorithm for $F$ with $L\in\mathbb R^{N\times9}$);
- *nonlinear*: $\min_x\tfrac12\sum_i\rho_i(\|f_i(x)\|^2)$ over residual blocks $f_i$,
  such as 2-D reprojection errors, with Jacobian $J=\partial f/\partial x\in\mathbb R^{m\times n}$
  and robust losses $\rho_i$.

**Units and types.** Each row inherits the unit of its observation (pixels, metres,
radians) and each column the unit of its parameter, so $A_{ij}$ has the unit
[observation $i$]/[parameter $j$]. Singular values and condition numbers therefore
depend on the chosen units unless residuals are whitened and parameters scaled.
Pixel coordinates keep the caller's origin and axis convention, which must be the
same in both images and for every reported residual. Computations run in double
precision, with machine epsilon $\epsilon=2^{-52}\approx2.2\cdot10^{-16}$.

**Outputs.** The estimate $\hat x$ (or $\hat h$ up to scale); the residual vector and
its weighted norm; the singular values $\sigma_1\ge\dots\ge\sigma_n\ge0$ with the
numerical rank; the weakly determined directions, i.e. right singular vectors $v_i$
of small $\sigma_i$; and, when the rank allows, a covariance $C\in\mathbb R^{n\times n}$
whose entry $C_{jk}$ has the unit of parameter $j$ times parameter $k$.

**Role in a pipeline.** A typical geometric chain runs RANSAC on minimal samples, a
normalized DLT on the inliers, LM refinement of a geometric error with a robust loss,
then a covariance or perturbation check. The same algebra whitens heterogeneous
residuals in [sensor fusion](13-kalman-ekf-eskf.md) and
[factor graphs](14-graphes-facteurs.md). Upstream must deliver correspondences
already filtered for gross outliers, consistent coordinate conventions and a noise
model per observation type. Downstream needs the parameters *and* a statement of
which combinations are observable. A linearized model is valid only near its
linearization point, and outliers need a robust treatment distinct from the choice
of solver.

## Intuition

Least squares projects the observations onto the set of predictions the model can
produce. The SVD then rotates parameter space into orthogonal directions $v_i$, each
of which moves the predictions by $\sigma_i$ per unit step. A large $\sigma_i$ means
the data react strongly to that combination of parameters, so the data pin it down.
A small $\sigma_i$ means the combination barely changes any prediction: the residual
cannot distinguish its values, and noise is amplified by $1/\sigma_i$ along it. A
small residual says that the model *can* explain the data, not that the data
determine the model.

### Worked example A: focal length and depth from one planar view

Constructed example, recomputed by checks/11-moindres-carres-svd.py. A pinhole camera
with known principal point observes five points of a planar target, 0.1 m apart,
with the target centre at depth $Z_0=2$ m and a focal length $f=1000$ px. Keep only
the horizontal image coordinate $u=fX/Z$ (pixels from the principal point) and the
two unknowns $(f,Z)$.

- *Fronto-parallel target.* All points share the depth $Z$, so $u$ depends on $f/Z$
  only. The Jacobian columns satisfy $\partial u/\partial Z=-(f/Z)\,\partial u/\partial f$,
  $J$ has rank 1 and its null direction is $(\delta f,\delta Z)\propto(f,Z)$:
  scaling both by the same factor leaves every pixel unchanged, and every point of
  that line of solutions fits noise-free data exactly.
- *Target turned by 30° about the vertical axis.* Depths now differ by about
  ±0.1 m across the target and the columns stop being proportional. After scaling
  both columns to unit norm, $\sigma_{\min}/\sigma_{\max}\approx0.023$, a condition
  number near 44. With 0.5 px noise per point, $0.5^2(J^TJ)^{-1}$ predicts standard
  deviations of about 80 px on $f$ and 0.16 m on $Z$, with a correlation of 0.999.

The fit residual stays at the noise level in both cases. Only the spectrum and the
covariance reveal that $f$ is first unidentified, then weakly identified. This is the
one-dimensional version of why planar calibration needs target orientations that
change the plane normal ([CV-ZHANG](../../50-calibration-geometrie/references/52-calibration-zhang.md)).

## Prerequisites and competencies

**Required prerequisites**: [vault conventions](../../01-Parcours/Pre-requis.md);
orthogonal matrices, eigen-decomposition of symmetric matrices, matrix norms and the
Gaussian likelihood. Useful links by use:

- homogeneous coordinates, homographies and minimal samples: [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md);
- closed-form initialization followed by refinement: [CV-ZHANG](../../50-calibration-geometrie/references/52-calibration-zhang.md);
- fundamental matrix, PnP and triangulation: [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md);
- sparse normal equations and the Schur complement: [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md);
- rotation parameters inside LM: [CV-SE3](12-rotations-se3.md); the same costs as graphs: [CV-FACTEURS](14-graphes-facteurs.md).

**Target competencies**: explain why a good fit does not imply identifiable
parameters, apply a normalized DLT and an LM refinement, compare solvers under
accuracy and cost constraints, evaluate a covariance and diagnose rank deficiency
versus outliers.

## Assumptions, observability and degenerate cases

- **Noise model.** Least squares is the maximum-likelihood estimate when the
  observations follow $y=f(x)+\mathcal N(0,I)$. With covariance $S$, the cost becomes
  $f^TS^{-1}f$, and Ceres expects the user to return $S^{-1/2}f$ from the cost
  function [Ceres covariance, Introduction]. Equal, uncorrelated noise across rows is
  an assumption to state, not a default.
- **Errors only in the right-hand side.** The linear model puts all noise in $b$. A
  DLT matrix $L$ is built from noisy coordinates and their products, so this
  assumption fails and the algebraic minimum has no statistical meaning; the
  algebraic solution therefore serves to initialize a geometric refinement
  [Zhang 1998, §3.2] (the link between the two is a project deduction).
- **Near-linearity.** Gauss–Newton drops the second-derivative terms of the
  residuals, which is accurate when residuals are small or the model nearly linear.
  Bundle problems near their minimum usually qualify; robust costs, which add strong
  nonlinearity at the scale of the residuals, do not [Triggs et al., §4.3].
- **Rank and gauge.** A unique solution needs full column rank. Deficiency is either
  structural, a *gauge* such as the similarity ambiguity of a reconstruction
  [Ceres covariance, Gauge Invariance] or the scale of a homogeneous vector, or
  geometric, caused by degenerate data. The gauge also shapes how uncertainty looks:
  in an object-centred gauge the cameras appear uncertain and strongly correlated, in
  a camera-centred gauge the points do [Triggs et al., §9].
- **Degenerate configurations.** They depend on the model: collinear points for a
  homography; a dominant plane for $F$, where a seven-point sample with five coplanar
  correspondences yields an epipolar geometry consistent with every correspondence of
  that plane [Chum et al. 2005, abstract]; a single target orientation for
  calibration (example A). Normalization does not repair any of them.
- **Outliers.** One blunder pulls the whole least-squares solution. A robust loss
  limits its influence only when the initialization is already in the right basin.

## Procedure

```text
input: observations z_i with covariances S_i, residual model f_i(x)
1. whiten:      f_i <- S_i^(-1/2) f_i            # unitless, comparable residuals
2. normalize:   T, T' from centroid and mean distance; scale parameter columns
3. linear step: build A or L; SVD -> sigma_1 >= ... >= sigma_n
                rank r = #{ sigma_i > tol * sigma_1 }; inspect v_i of small sigma_i
                x0 = QR solve (full rank) | truncated SVD (r < n) | v_n for L h = 0
4. map back:    denormalize (H = T'^-1 H_hat T); project on constraints (rank 2 for F)
5. refine:      LM on geometric residuals with robust loss rho(., a)
                accept a step if actual / predicted decrease > threshold; adapt damping
6. covariance:  C = (J^T J)^-1 at x*, only with whitened residuals and a fixed gauge
7. validate:    held-out transfer error, spread under perturbation or resampling
```

Purpose of the steps. *Whitening* turns the cost into a sum of squared standard
scores, so units no longer choose the weights. *Normalization* improves the
conditioning of the linear step and, for the DLT, changes the estimator itself
[Hartley 1997, §3]. *Inspecting the spectrum* is the identifiability check; its
tolerance is a decision tied to noise and units, not a universal constant.
*Projection on constraints* gives the nearest valid matrix in the Frobenius norm
[Hartley, §2.3], not the geometrically best one. *Refinement* minimizes an error with
physical meaning. The *covariance* is meaningful only after whitening and gauge
fixing, and *validation* tests the assumptions that the covariance takes for granted.

## Mathematics, conventions and units

### Linear least squares and the SVD

We minimize $\|Ax-b\|_2^2$. Let $A=U\Sigma V^T$ be the thin SVD of a full-column-rank
$A$: $U\in\mathbb R^{m\times n}$ has orthonormal columns $u_i$ (directions in
observation space), $\Sigma=\operatorname{diag}(\sigma_i)$ and $V\in\mathbb R^{n\times n}$
is orthogonal with columns $v_i$ (directions in parameter space). Then
$\hat x=V\Sigma^{-1}U^Tb$, so

$$\delta\hat x=\sum_i\frac{u_i^T\delta b}{\sigma_i}\,v_i :$$

a perturbation of the measurements is amplified by $1/\sigma_i$ along $v_i$.
Conversely, $\|A(t\,v_i)\|=|t|\,\sigma_i$: along a direction of small singular value,
the parameters can move without changing the residual. In whitened units the
covariance is $(A^TA)^{-1}=V\Sigma^{-2}V^T$, so the standard deviation of the
parameter combination $v_i^Tx$ is exactly $1/\sigma_i$ (derivations of the project).
The condition number $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$ depends on the scale of
the columns, hence on parameter units. With full column rank,
$\kappa_2(A^TA)=\kappa_2(A)^2$: the normal equations square the condition number.
When $\sigma_n=0$, the pseudo-inverse $A^+=\sum_{\sigma_i>0}\sigma_i^{-1}v_iu_i^T$
returns the minimum-norm solution, one arbitrary member of a family of equally good
fits.

**Whitening.** For a residual $r$ with positive definite covariance $C$, the quadratic
form $r^TC^{-1}r$ is unitless. Whitening computes $z=L^{-1}r$ with $C=LL^T$ (Cholesky)
by solving $Lz=r$; the quadratic form is $\|z\|^2$. A singular covariance requires
treating the constrained and the observable subspaces separately. Adding pixels and
metres without weights changes the objective arbitrarily.

### Homogeneous systems, DLT and normalization

The linear estimation of a homography or a fundamental matrix is written $Lh=0$, with
$h$ defined up to scale. For a homography, each correspondence gives two linear
equations in the nine coefficients, hence $L\in\mathbb R^{2N\times9}$; for $F$, each
correspondence gives one equation and at least eight are needed. Minimizing $\|Lh\|$
under $\|h\|=1$ excludes the zero solution; the minimizer is the right singular vector
of the smallest singular value, equivalently the eigenvector of $L^TL$ with the
smallest eigenvalue [Zhang 1998, App. A; Hartley 1997, §2.2]. For $F$, rank 2 is then
imposed by zeroing the smallest singular value, which gives the nearest singular
matrix in Frobenius norm [Hartley, §2.3]. This cost is algebraic and has no direct
physical interpretation: Zhang uses it to initialize, then minimizes the reprojection
error [§3.2]. The solution direction is well separated only if the *second smallest*
singular value stays clearly above the smallest; Hartley expresses this through
$d_1/d_8$, the ratio of the largest to the eighth eigenvalue of the $9\times9$ matrix
$L^TL$ [§4].

On raw pixels, a row of $L$ mixes the constant 1, coordinates and products of
coordinates. For a typical point $(100,100)$ of a $200\times200$ image, the diagonal
entries of $L^TL$ range from $10^8$ down to 1; Hartley deduces a condition number of
at least about $10^4$ and usually far greater, so perturbations of the size of $d_8$
change the least eigenvector drastically [§4]. Zhang also notes that $L$ is
ill-conditioned on raw pixels [App. A]. Hartley's normalization is applied to each
image independently: translate the points so that their centroid is at the origin,
then scale them isotropically so that their average distance to the origin is
$\sqrt2$, making the "average" point $(1,1,1)^T$ [§5.1]. Estimate on the normalized
points $\hat x=Tx$, $\hat x'=T'x'$, then denormalize: $H=T'^{-1}\hat HT$ or
$F=T'^T\hat FT$ [§3]. The algebraic least-squares solution is not invariant to these
transformations [§3]: normalizing changes the estimator, not only the rounding. On
the "house" pair, the condition number improves by about $10^8$ [§7.3.1];
isotropic and non-isotropic scaling are "almost indistinguishable" [§7.3.5]; and the
normalized eight-point algorithm performs almost as well as the iterative
minimization of point displacement [§7.3.4].

### Gauss–Newton, Levenberg–Marquardt and damping as a spectral filter

For a nonlinear residual $r(x)$ with Jacobian $J$, Gauss–Newton linearizes
$r(x+\delta)\approx r(x)+J\delta$ and solves $J^TJ\delta=-J^Tr$. It replaces the
Hessian $J^TJ+\sum_ir_i\nabla^2r_i$ by $J^TJ$, a valid approximation if the residuals
are small or the model nearly linear; otherwise convergence slows down greatly
[Triggs et al., §4.3]. Levenberg–Marquardt damps the step,
$(J^TJ+\lambda D^TD)\delta=-J^Tr$, increasing $\lambda$ when the quadratic model
predicts the cost badly, which shortens the step towards gradient descent, and
decreasing it otherwise [§4.2]. Ceres writes the same regularization as
$\frac1\mu\|D\,\Delta x\|^2$ with a trust-region radius $\mu$, takes $D$ as the square
root of the diagonal of $J^TJ$, and judges each step by the ratio $\rho$ of the actual
to the predicted change in cost [Ceres solving, Trust Region Methods and
Levenberg–Marquardt]. These methods reach a local minimum at best: they need an
initialization in the right basin, usually a linear or closed-form solution.

With $D=I$, or after scaling the columns of $J$, the SVD of $J$ shows what damping
does to the step:

$$\delta=-\sum_i\frac{\sigma_i^2}{\sigma_i^2+\lambda}\;\frac{u_i^Tr}{\sigma_i}\;v_i .$$

The factor $\sigma_i^2/(\sigma_i^2+\lambda)$ keeps the Gauss–Newton step along
well-determined directions and suppresses it where $\sigma_i^2\ll\lambda$ (project
derivation). *Constructed example C, recomputed by checks/11-moindres-carres-svd.py*:
with $\lambda=10^{-4}$, the reciprocal of Ceres's default
`initial_trust_region_radius` of $10^4$, a direction with $\sigma=1$ keeps 99.99% of
its step and a direction with $\sigma=10^{-3}$ keeps 1/101 of it. LM therefore moves
slowly along weak directions instead of jumping along them, and a parameter that
"converged" there may simply have stayed near its initial value. Damping changes the
path, not the cost: unlike a prior or a regularization term, it does not move the
minimizer.

### Robust losses

A robust loss replaces the contribution $s=\|f\|^2$ of a residual block by
$\frac12\rho(s)$, with $\rho(0)=0$ and $\rho'(0)=1$ to mimic the quadratic cost near
zero, and $\rho'(s)<1$ in the outlier region to reduce the weight of large
residuals. With a scale $a>0$, $\rho(s,a)=a^2\rho(s/a^2)$: $a$ has the unit of the
residual norm [Ceres modeling, LossFunction]. Ceres defines Huber,
$\rho(s)=s$ for $s\le1$ and $2\sqrt s-1$ beyond, and Cauchy, $\rho(s)=\log(1+s)$.
Their weights $\rho'(s)$ decrease as $1/\|f\|$ and $1/\|f\|^2$ (project calculation).
Triggs et al. robustify each *irreducible group* of observations, such as both
coordinates of one image point, which is accepted, down-weighted or rejected as a
whole; they also note that an error affecting all observations about equally, such
as an incorrect projection model, cannot be fixed by data cleaning [§3.3]. A robust
loss provides no initialization: with many outliers, a RANSAC-type filter precedes it
(project reasoning).

### Uncertainty of the parameters

For $y=f(x)+\mathcal N(0,I)$, Ceres gives $C(x^*)=(J^TJ)^{-1}$ as the covariance of
the estimate, under two assumptions. The residuals must have identity covariance,
which the user obtains by returning $S^{-1/2}f$; and $J$ must have full column rank,
otherwise the covariance is rank deficient and given by the Moore–Penrose
pseudo-inverse [Ceres covariance, Introduction]. In structure from motion the
reconstruction is defined only up to a similarity, and handling this gauge requires
an SVD or a custom inversion [Gauge Invariance]. Triggs et al. recall that the
dispersion approaches the covariance of the estimator only asymptotically, and that
this is much less clear for small vision geometry problems and weak networks [§3.1].
This covariance measures neither model bias nor outliers.

### Worked example B: what forming $J^TJ$ costs

Constructed from the Ceres documentation and recomputed by
checks/11-moindres-carres-svd.py. Ceres illustrates `min_reciprocal_condition_number`
with $J=\begin{pmatrix}1&1\\1&1.0000001\end{pmatrix}$ and prints $(J^TJ)^{-1}$ with
entries $\pm2.0471\cdot10^{14}$ [Ceres covariance, `Covariance::Options`]. Here
$\kappa_2(J)\approx4\cdot10^7$, so $\kappa_2(J^TJ)\approx1.6\cdot10^{15}$ and
$\kappa^2\epsilon\approx0.36$.

- Exact rational arithmetic gives $(J^TJ)^{-1}_{11}=2.0000002\cdot10^{14}$.
- Forming $J^TJ$ in double precision and inverting it gives $2.0471\cdot10^{14}$,
  the documented value and 2.4% too large: rounding the entries of $J^TJ$, about
  $4\cdot10^{-16}$, is not small compared with $\det(J^TJ)=10^{-14}$.
- Inverting $J$ itself, whose condition number is only $4\cdot10^7$, reproduces the
  exact value to about $10^{-9}$ relative.

This matches the bounds quoted by Triggs et al.: a relative error of order
$\kappa\epsilon$ for QR against $\kappa^2\epsilon$ for the normal equations
[§4.3, footnote 6]. Beyond the arithmetic, a variance of $10^{14}$ in whitened units
means that the data do not constrain the direction $(1,-1)/\sqrt2$ at all; Ceres
therefore makes `Covariance::Compute` return `false` by default in such cases.

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Rank tolerance | NumPy 2.2 `lstsq`: `rcond` = machine precision × max(M, N), relative to $\sigma_1$; Ceres `DENSE_SVD` covariance fails when $\sigma_{\min}/\sigma_{\max}<\sqrt{10^{-14}}=10^{-7}$ | Decides which directions are declared undetermined | A tolerance near machine precision detects numerical, not physical, deficiency; it depends on column scaling |
| Coordinate normalization | Hartley: centroid at the origin, mean distance $\sqrt2$, per image; OpenCV 4.13 homography kernel: per-axis mean absolute deviation 1 | Conditions the linear step and changes the algebraic estimator | Compute it from the points actually fitted; denormalize before reporting pixel residuals |
| Parameter scaling | Ceres `jacobi_scaling = true`: columns scaled by their norm | Makes condition numbers, damping and rank tests comparable across parameters | Creates no information: example A keeps a scaled condition number of 44 |
| Loss scale $a$ | Residual-norm units: pixels for raw reprojection errors, standard deviations for whitened ones | Moves the transition from quadratic to down-weighted cost | Too small loses inlier efficiency; too large lets outliers act quadratically |
| LM start and stopping | Ceres 2.2.0: `initial_trust_region_radius` $10^4$ (initial $\lambda=10^{-4}$), `min_relative_decrease` $10^{-3}$, `max_num_iterations` 50, `function_tolerance` $10^{-6}$, `gradient_tolerance` $10^{-10}$, `parameter_tolerance` $10^{-8}$ | First step size, step acceptance and termination | Relative tolerances depend on scaling; read the termination type before trusting a result |
| Covariance algorithm | Ceres: `SPARSE_QR` (default, fails on a rank-deficient $J$); `DENSE_SVD` with `null_space_rank` | Whether a gauge-deficient problem returns a covariance | Fix the gauge, or declare the null-space dimension explicitly |

Tuning approach (project method), on data from the deployment setup that are
disjoint from the final test:

1. Estimate the noise of each observation type from repeated detections or from the
   residuals of a clean subset, and whiten with it.
2. Normalize, then inspect the spectrum on representative configurations. A
   direction is effectively undetermined when its standard deviation $1/\sigma_i$
   (whitened units) exceeds the tolerance of the application on that combination.
3. Sweep the loss scale $a$ over a few multiples of the inlier noise on data with
   labelled outliers; watch held-out errors and the parameter spread, not the
   training cost, which always decreases as $a$ shrinks.
4. Adjust LM tolerances last, checking that the termination reason is a cost or
   gradient criterion and not the iteration limit.

## Properties and limits of guarantees

- **Orthogonal invariance.** $\|Q(Ax-b)\|=\|Ax-b\|$ for an orthogonal $Q$: rotating the
  observation space changes nothing. Scaling rows does, because row weights define
  the estimator; they should come from the noise model (project derivation).
- **Column scaling.** With full column rank, rescaling the parameters $x=Dx'$ leaves
  the fitted predictions unchanged and maps the solutions onto each other. The
  condition number, rank decisions with a fixed tolerance, damping with $D=I$ and any
  regularization do change, so parameter units belong to the solver contract.
- **DLT and coordinate changes.** The algebraic solution depends on the image
  coordinate frame [Hartley, §3]. Because the normalizing transform is computed from
  the points themselves, translating or uniformly rescaling the input coordinates
  leaves the normalized points, hence the estimate, unchanged (project deduction from
  §5.1).
- **Statistical meaning.** Under Gaussian noise with identity covariance, least
  squares is the maximum-likelihood estimate [Ceres covariance, Introduction]; such
  estimates are asymptotically unbiased with minimum variance, and their dispersion
  approaches their covariance only asymptotically [Triggs et al., §3.1]. With errors
  in $L$ (DLT) or outliers, none of these properties applies as stated.
- **Convergence.** Gauss–Newton and LM give a local minimum at best; guaranteed
  descent requires step control [Triggs et al., §4.2].
- **Projection on constraints.** The rank-2 correction of $F$ is the nearest singular
  matrix in Frobenius norm, which treats all entries equally regardless of their
  magnitude [Hartley, §§2.3 and 6]; it is not the geometrically optimal correction.

## Cost and implementation

Cost drivers for a dense problem with $m$ rows and $n$ columns:

- *Normal equations*: forming the symmetric $A^TA$ costs about $mn^2$ flops and its
  Cholesky factorization about $n^3/3$ (project count). Ceres notes that QR cost grows
  linearly with the number of rows, so for $m\gg n$ Cholesky on $J^TJ$ is cheaper,
  at the price of a squared condition number and possible factorization failure
  [Ceres solving, `DENSE_NORMAL_CHOLESKY`].
- *QR*: up to a factor of two slower than the normal equations but much less
  sensitive to ill-conditioning [Triggs et al., §4.3]; relative error of order
  $\kappa\epsilon$ against $\kappa^2\epsilon$ [footnote 6]. With $\kappa_2(A)=10^6$,
  about 6 of the roughly 16 decimal digits of double precision are at risk with QR
  and about 12 with the normal equations (project order of magnitude).
- *SVD*: generally the most accurate and the slowest dense method [Eigen 3.4].
- *DLT*: $L$ has nine columns, so accumulating $L^TL$ is $O(N)$ and the $9\times9$
  eigenproblem has constant cost. Accuracy, not time, decides how to solve it.
- *Large sparse problems* reverse the arbitration. Ceres recommends `DENSE_QR` for
  small problems (a couple of hundred parameters, a few thousand residuals) with
  relatively dense Jacobians. For bundle adjustment it forms the normal equations and
  eliminates the points through the Schur complement: `DENSE_SCHUR` needs $O(p^2)$
  memory and $O(p^3)$ time in the number of cameras $p$ and is practical up to a few
  hundred cameras, while `SPARSE_SCHUR` reaches thousands [Ceres solving, Schur
  complement; Triggs et al., §6.1]. Scaling and preconditioning are therefore
  essential. Factor and solve; do not materialize an inverse.

### Implementation contracts

Read in the cited versions; no library call was executed for this note, and the
worked examples were recomputed with the Python standard library only.

- **OpenCV 4.13.0, `cv::solve`** [core.hpp L1944–L1968; base.hpp L133–L152]:
  `DECOMP_LU` and `DECOMP_CHOLESKY` return 0 when the matrix, or $A^TA$, is singular;
  `DECOMP_SVD` and `DECOMP_QR` accept over-determined or singular systems and return a
  pseudo-solution; `DECOMP_NORMAL` combines with any of them and solves the normal
  equations. For $\min_{\|x\|=1}\|Ax\|$ the header states that `solve` "will not do
  the work" and points to `SVD::solveZ` [core.hpp L2818–L2828].
- **OpenCV 4.13.0, `findHomography`** [calib3d/src/fundam.cpp]: the linear kernel
  shifts each point set to its centroid and scales $x$ and $y$ *separately* so that
  their mean absolute deviation is 1, not Hartley's isotropic $\sqrt2$; it accumulates
  $L^TL$ in double precision, takes the eigenvector of the smallest eigenvalue and
  scales the result to $h_{33}=1$ unless $|h_{33}|$ is below the float epsilon
  [L52–L57, L111–L189]. With method 0 or exactly four points the kernel runs on all
  points; with more than four points (except RHO), the inliers are then refined by
  LM, at most 10 iterations, on the transfer error in the second image
  [L231–L272, L401–L434].
- **OpenCV 4.13.0, eight-point $F$** [fundam.cpp L693–L790]: Hartley's isotropic
  normalization, eigen-decomposition of $A^TA$, failure if fewer than eight
  eigenvalues exceed `DBL_EPSILON`, rank 2 by zeroing the smallest singular value,
  $F=T_2^TF_0T_1$, then $F_{33}=1$ when it is not negligible.
- **NumPy 2.2, `numpy.linalg.lstsq`**: SVD-based (LAPACK `gelsd`); default `rcond`
  equal to machine precision times max(M, N) since NumPy 2.0; returns the
  minimum-norm solution, the rank and the singular values, and an *empty* residual
  array when the rank is below N.
- **Eigen 3.4**: `BDCSVD` most accurate but slowest, normal equations fastest but
  least accurate, QR in between; `HouseholderQR` has no pivoting and is unstable if
  the matrix is not of full rank, `ColPivHouseholderQR` is slower but more stable;
  the normal equations "lose roughly twice as many digits of accuracy".
- **Ceres 2.2.0**: `LossFunction` convention and scaling; `Covariance::Options`
  (`SPARSE_QR` default, `DENSE_SVD`, `min_reciprocal_condition_number` $10^{-14}$,
  `null_space_rank`, `apply_loss_function = true`); the `Solver::Options` defaults of
  the parameter table. The documentation's schematic trust-region loop doubles or
  halves $\mu$; the 2.2.0 LM strategy instead multiplies the radius by a factor
  between 1/2 and 3 that grows with $\rho$ after an accepted step, divides it by
  2, 4, 8… after successive rejections, and clamps the squared column norms used for
  $D$ to $[10^{-6},10^{32}]$ [levenberg_marquardt_strategy.cc L76–L97, L157–L170;
  solver.h L276–L295].

## Evaluation and controlled variation

**Metrics.** Report errors in the space where the result is used: transfer or
reprojection error in pixels on held-out points spread over the useful image region,
not the algebraic residual; the singular-value ratios that govern identifiability
($\sigma_{n-1}/\sigma_1$ for a homogeneous system, $\sigma_n/\sigma_1$ after scaling
otherwise); the spread of parameters under resampling of the inliers or small
coordinate perturbations; and, for a covariance, its calibration. A proposed
calibration test (project protocol) repeats the estimation on simulated noise drawn
from the assumed model and counts how often
$(\hat x-x)^TC^{-1}(\hat x-x)$ stays below the 95% quantile of a $\chi^2$ with $n$
degrees of freedom; a rate far below 95% means that $C$ is overconfident.

**Analytical case.** Two almost identical columns give a weakly constrained
direction. Slightly perturb $b$ with $A$ fixed: predict a large change of the
parameters along this direction even though the residual changes little. Compare QR
and SVD on stability, not only on minimal cost.

**Calculation executed by the project on 2026-10-23, outside the repository** (Python
3.10.13, NumPy 2.2.6, and recomputed with the standard library by
checks/11-moindres-carres-svd.py): $A$ has three rows and columns $(1,1,1)$ and
$(1,1.001,0.999)$, so $\sigma_2\approx10^{-3}$ and $\kappa_2(A)\approx2.4\cdot10^3$. A
perturbation of $b$ of norm $10^{-3}$ along $u_2$ moves $\hat x$ by a vector of norm
1.0 along $v_2\approx(1,-1)/\sqrt2$, while the residual stays of order $10^{-16}$.
The Ceres example of worked example B shows the same phenomenon in a covariance.
These are constructed cases, not measurements on images.

**Controlled variation of the DLT, executed in the same environment on 2026-10-23.**
Baseline: homography DLT on raw pixel coordinates. Varied factor: Hartley's
normalization only, with identical data. Constructed case: a known homography close
to the identity, Gaussian noise of 0.5 px, 200 draws per configuration. Prediction: a
sharp drop of $\sigma_1/\sigma_8$ in all cases, with an accuracy gain mostly when the
points are far from the origin relative to their extent. Measurement: median transfer
error on 200 points spread over the whole $1920\times1080$ image.

| Configuration | $\sigma_1/\sigma_8$ raw | $\sigma_1/\sigma_8$ normalized | Median error, raw | Median error, normalized |
| --- | --- | --- | --- | --- |
| 50 points over the whole image | $8.3\cdot10^6$ | 4.1 | 0.22 px | 0.20 px |
| 8 points over the whole image | $1.2\cdot10^7$ | 6.6 | 0.70 px | 0.67 px |
| 20 points in a 200 px square | $1.4\cdot10^8$ | 3.5 | 1013 px | 28 px |

Reading: in double precision, well-distributed points tolerate the absence of
normalization, while points concentrated far from the origin do not. Normalization
does not replace coverage: 28 px remains a fragile extrapolation. Limits: one model,
isotropic noise, no outliers, no real image; this Monte Carlo table was not re-run in
this pass.

**Measurement limits.** Held-out points must lie where the result will be used,
otherwise extrapolation errors stay invisible. Repeated estimates on the same images
share their detection biases, so their spread underestimates the error on a new
acquisition. A covariance validated on simulated noise says nothing about model error
such as unmodelled distortion.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Small residual but parameters that jump between runs | Weakly constrained direction; mixed units hiding it | Spectrum after whitening and column scaling; $v_i$ of the smallest $\sigma_i$ names the combination | Add independent measurements or views (example A); fix a gauge; add a justified prior |
| Unstable estimate after RANSAC | Remaining outliers, or near-degenerate inlier geometry | Refit after removing independently suspicious matches versus after small coordinate perturbations; spatial plot of inliers | Outliers: stricter gating or robust loss; degeneracy: better coverage or a model with fewer degrees of freedom |
| Large epipolar consensus but wrong egomotion | Dominant plane: an H-degenerate sample explains the whole plane [Chum et al., abstract] | Test whether most inliers also fit a homography | Degeneracy-aware sampling (DEGENSAC) or a planar model |
| DLT result poor only for clustered points | Unnormalized coordinates far from the origin relative to their spread | $\sigma_1/\sigma_8$ raw versus normalized; repeat with Hartley normalization | Normalize per image; widen the point distribution |
| Huge or negative variances | Inverting a near-singular $J^TJ$; gauge not fixed | $\sigma_{\min}/\sigma_{\max}$ of the whitened $J$; compare with $\sqrt{10^{-14}}$ | Fix the gauge, use `DENSE_SVD` with a stated null space, report relative quantities |
| LM stops at the iteration limit or with tiny steps | Bad initialization, bad scaling, residual model error | Termination type, gradient norm, actual/predicted decrease ratio over iterations | Better initialization; Jacobi scaling; check the model on synthetic data |
| Cholesky fails or results change with the library | Normal equations on an ill-conditioned problem | Compare with a QR or SVD solution on the same scaled system | Switch to QR/SVD, or rescale before forming $J^TJ$ |
| Covariance looks tight but held-out errors are large | Model bias, correlated or underestimated noise, outliers | Coverage test above; residual structure over the image | Model the bias (distortion, timing); inflate or estimate the noise; robustify |

## Alternatives and applications

Conditional choices:

- **Prefer QR** for a dense, full-rank, moderately sized problem when accuracy
  matters more than a factor-two speed difference.
- **Prefer the SVD** when the rank is in question, when the system is homogeneous,
  or when the singular directions themselves are a deliverable of the diagnosis.
- **Prefer the normal equations** only after scaling, for a well-conditioned
  problem, or inside sparse solvers whose structure (Schur complement in bundle
  adjustment) outweighs the squared conditioning.
- **Prefer a geometric cost refined by LM** over an algebraic one whenever the
  result feeds a metric decision; keep the normalized DLT as its initialization.
- **Prefer robust estimation** (RANSAC, then a robust loss) as soon as gross outliers
  are possible: least squares has no breakdown margin.
- **Prefer a prior or regularization** only when it encodes real knowledge (a
  nominal focal length, a gravity direction), and report it as an assumption: it
  removes a symptom without creating an observation.

The usual geometric chain is RANSAC on a minimal model, a normalized DLT on the
inliers, LM on the geometric error with a robust loss, then the covariance if the
rank allows. Industrial uses (project reasoning, not published results): a
homography for planar part inspection or a document scanner, where the inlier
spread over the part matters more than their count; intrinsic calibration acceptance
on a production line, using the spectrum and held-out reprojection error rather than
the training RMS; and multi-sensor extrinsics, where whitening is what makes pixel
and metre residuals commensurable.

## Guided reasoning and proposed checks

These constructed cases develop whitening, loss of rank and the distinction between fit and identifiability. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-SVD-002

**Working question**: To solve $\min_x\|Ax-b\|_2$ with a full-column-rank matrix $A$, when should you prefer QR or SVD factorization of $A$, and when are the normal equations $A^TAx=A^Tb$ solved by Cholesky still a defensible choice?

**Reference answer**: Forming $A^TA$ squares the condition number, $\kappa_2(A^TA)=\kappa_2(A)^2$, and loses about twice as many significant digits. QR, or the SVD (more accurate but slower, and useful for diagnosing rank), is required as soon as $A$ is even mildly ill-conditioned. Normal equations are generally the fastest, especially for tall and narrow $A$: they remain defensible if $A$ is well conditioned after scaling, and large sparse problems such as bundle adjustment exploit them through sparse Cholesky factorization and the Schur complement.

**Reading for a project**: choose the solver after examining rank, scales and sparse structure. A shorter solve time does not compensate for parameters that have become unusable. Also compare stability when observations are slightly disturbed, with the same objective and the same units.

### Case linked to CV-SVD-009

**Working question**: After nonlinear least squares, parameter uncertainty is inferred from $(J^TJ)^{-1}$, where $J$ is the Jacobian at the solution. Under which conditions is this interpretation valid, and what does it fail to measure?

**Reference answer**: whitened residuals with identity covariance and a $J$ of full column rank; the matrix obtained is then the local dispersion of the estimate, which approaches its covariance only asymptotically. If $J$ is deficient in rank (gauge, parameter not observable), $J^TJ$ is not invertible: fix the gauge, reparameterize or use a pseudo-inverse. It measures neither a model bias, like a mismodeled distortion, nor the effect of outliers: it assumes a correct model and noise model.

**Proposed action**: Compare the announced intervals to controlled repetitions or disturbances, keeping gauge and units. A low dispersion around a biased solution remains compatible with poor accuracy. Separate local uncertainty, variation between acquisitions and adequacy of the physical model.

**Source consulted for this pass**: [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), Introduction, Rank of the Jacobian and Gauge Invariance. The other developments are in the [flashcards](../11-moindres-carres-svd.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-SVD-001

**Situation**: A linear estimate $\hat x=\arg\min_x\|Ax-b\|_2$ has a very small residual, but $\hat x$ changes substantially when the measurements $b$ are slightly perturbed. For a full-column-rank thin SVD $A=U\Sigma V^T$, what relationship explains why a good fit does not guarantee reliable parameters?

**Reading subspaces**: For $m\ge n$ and a full column rank, $\hat b=A\hat x=UU^Tb$ is the projection of $b$ on the column space, while the orthogonal residual is $(I-UU^T)b$. A perturbation within this space can strongly change $\hat x$ without increasing this residual. This is precisely why the diagnosis must examine both fit and sensitivity. If a singular value is exactly zero, some components are no longer determined by observations: the pseudo-inverse chooses a solution of minimum norm, without establishing that this solution is physically true. These equalities are deductions from the SVD, with the columns of $U$ spanning the column space of $A$.

### CV-SVD-002

**Situation**: To solve $\min_x\|Ax-b\|_2$ with a full-column-rank matrix $A$, when should you prefer QR or SVD factorization of $A$, and when are the normal equations $A^TAx=A^Tb$ solved by Cholesky still a defensible choice?

**What QR does**: with the reduced factorization $A=QR$, $Q^TQ=I$ and upper triangular $R$, we form $Q^Tb$ and then solve $R\hat x=Q^Tb$ by substitution. Orthogonal transformations preserve norms and avoid forming the column products of $A^TA$. The SVD replaces the triangular factor with singular directions and makes a low numerical rank explicit. In a dense problem with $m\gg n$, costs scale mostly as $mn^2$ with different constants; in a sparse system, fill-in of the factors and elimination order can become decisive. Comparing only the dimensions of the system is therefore not enough to predict time and memory.

### CV-SVD-003

**Situation**: A calibration objective adds an error in pixels to an error in meters. How can you prevent the units from determining their relative weights?

**Why unit invariance works**: For an invertible linear change of units $r'=Dr$, the correct covariance becomes $C'=DCD^T$. Then $r'^TC'^{-1}r'=r^TC^{-1}r$. Changing the residuals without changing their covariance breaks this invariance. Whitening by Cholesky is calculated by solving $Lz=r$, rather than materializing $L^{-1}$. If two errors come from the same detection or sensor, correlations can make their naïve addition overconfident. Model them, or state independence as an approximation; a robust loss does not repair this double counting. The quadratic form is dimensionless, but the final covariances of the parameters retain their own units.

### CV-SVD-004

**Situation**: After RANSAC, a transformation fitted to a large consensus changes substantially between runs or inlier subsets. Which checks distinguish remaining outliers from a nearly degenerate configuration?

**What spectrum to examine**: for a homogeneous system with nine parameters whose scale is arbitrary, we expect a single solution direction. With enough points, a second near-zero singular value means that several transformations explain almost as much of the data. The ratio between the last singular values informs this separation; for the minimal eight-row system, the exact kernel must also be taken into account, because a reduced SVD may not return its vector. These diagnoses are specific to the model and its normalization: always using the same spectral threshold on arbitrary units would be misleading. A targeted test then examines the geometric effect of this ambiguity.

### CV-SVD-005

**Situation**: Describe direct linear transformation (DLT) estimation of a homography $H$ from $n\ge4$ point correspondences: which system is constructed, which constraint is imposed, and which vector is selected as the solution?

**Explicit construction of the rows**: for $(x,y)\mapsto(u,v)$, stack $h=(h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33})^T$. The projective relation gives the rows $[x,y,1,0,0,0,-ux,-uy,-u]$ and $[0,0,0,x,y,1,-vx,-vy,-v]$. These constraints are stacked and then the solution vector is put back into a $3\times3$ matrix. With exactly four pairs, the matrix is $8\times9$: you have to get the full right kernel, not blindly select the last vector of a truncated factorization. The four points must provide independent constraints. An arbitrary normalization of $h_{33}$ is not possible if this component is zero or too close to zero; the homogeneous geometry allows other scaling choices.

### CV-SVD-006

**Situation**: Why is DLT built from raw pixel coordinates on the order of $10^3$ poorly conditioned, and which normalization proposed by Hartley addresses this?

**Computing the normalization**: for points $p_i=(x_i,y_i)$, calculate $c=n^{-1}\sum_i p_i$, the average distance $\bar d=n^{-1}\sum_i\|p_i-c\|_2$, then $s=\sqrt2/\bar d$ if $\bar d>0$. The homogeneous transformation has rows $(s,0,-sc_x)$, $(0,s,-sc_y)$ and $(0,0,1)$. It must be calculated separately in each image. If all the points coincide, this operation is indefinite: it is not a simple rounding problem, but an absence of usable geometry. After denormalization, compare the residuals in pixels in the original images; a residual expressed in the normalized coordinates does not keep the same numerical threshold.

### CV-SVD-007

**Situation**: When refining calibration by minimizing nonlinear reprojection error, what does one Gauss–Newton iteration compute, how does Levenberg–Marquardt make the step safer, and what condition do both methods require?

**What Gauss–Newton neglects**: for $F(x)=\tfrac12\sum_i r_i(x)^2$, the exact Hessian is $J^TJ+\sum_i r_i\nabla^2r_i$. Large errors or a strong curvature of the model make the second term potentially important. The damping of LM makes the step more careful, without turning a wrong projection model into a good one. An iteration must compare the actual cost after the update with the decrease predicted by linearization, accept or reject the step, and then adjust its trust region. Stopping only because the parameters no longer move can also mean a blocked step: check cost convergence, gradient, scales and physical validity of the solution.

### CV-SVD-008

**Situation**: In Ceres, a `HuberLoss(a)` or `CauchyLoss(a)` is attached to reprojection residual blocks. Which quantity does the loss act on, and how should $a$ be chosen for pixel residuals versus whitened residuals?

**Interpretation of weights**: in an approximation of reweighted least squares, the block $f$ receives a weight related to $\rho'(\|f\|^2)$; we therefore apply approximately $\sqrt{\rho'}$ to its components and its Jacobian. The solver can also account for $\rho''$: this reasoning explains the influence without describing all its numerical corrections. For a 2-D reprojection error, treating $(e_x,e_y)$ as one block down-weights the whole observation together; two separate scalar losses are another objective. After whitening, the threshold refers to a multidimensional norm: "two standard deviations" on one axis does not automatically give a probability of rejection of the entire block.

### CV-SVD-009

**Situation**: After nonlinear least squares, parameter uncertainty is inferred from $(J^TJ)^{-1}$, where $J$ is the Jacobian at the solution. Under which conditions is this interpretation valid, and what does it fail to measure?

**Limit of the pseudo-inverse**: dropping a singular direction to construct a pseudo-inverse does not demonstrate zero physical variance in that direction. An unfixed gauge describes a family of equivalent solutions; state the coordinates or relative quantities in which an uncertainty makes sense. After a local reparameterization $y=g(x)$, the first-order propagation is $C_y\approx G C_xG^T$, $G=\partial g/\partial x$. Cross terms can then strongly influence a distance or a relative pose. Reading only the diagonal standard deviations loses these couplings. A local covariance resulting from a robust cost also requires stating the approximation convention, rather than automatically using the ordinary Gaussian formula.

**Passages consulted for these developments**: [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), Introduction, Gauge Invariance and Rank of the Jacobian; [Ceres, Solving Non-linear Least Squares](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), Linearization, Trust Region and Linear Solvers.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-SVD-001 — A fit with arbitrarily unstable parameters

Constructed example: let $A=\operatorname{diag}(1,10^{-6})$ and $b=(1,0)^T$. The least-squares solution is $(1,0)^T$. Perturb only the second observation by $10^{-6}$: the solution becomes $(1,1)^T$, while both fits have zero residual. Thus even an exact fit can move one parameter by one unit. These numbers assume compatible, fixed parameter units; rescaling a column changes the numerical condition number without supplying any missing measurement.

### CV-SVD-002 — Choosing a solver by error budget

A useful project decision is to compare $\kappa_2(A)\epsilon$ and $\kappa_2(A)^2\epsilon$, with machine precision $\epsilon$, to the tolerated relative numerical error. These are sensitivity indicators, not exact error predictions. For double precision and $\kappa_2(A)=10^8$, the second expression is of order one: explicitly forming normal equations can consume the useful precision. Solver success therefore needs a scaled residual and a stability check, rather than a successful Cholesky return alone.

### CV-SVD-003 — Correlated measurements do not count twice

For two unit-variance residuals with correlation $\rho$, take $C=\begin{bmatrix}1&\rho\\\rho&1\end{bmatrix}$. Along $r=(a,a)^T$, the weighted cost is $2a^2/(1+\rho)$; along $(a,-a)^T$, it is $2a^2/(1-\rho)$. As $\rho$ approaches one, common deviations carry almost one independent observation, while disagreement becomes very unlikely. This constructed example explains why dividing each component by its own standard deviation cannot replace full whitening when correlations matter.

### CV-SVD-004 — A diagnostic requires competing explanations

Refit the same normalized model after small coordinate perturbations and after removing candidate outliers, recording both parameter changes and predictions on spatially separated held-out points. Persistent variation along a weak singular direction supports poor geometric constraint; stabilization after rejecting independently suspicious matches supports contamination. Neither is a proof in isolation: outliers can form a coherent alternative model, and aggressive filtering can make coverage worse. A low residual histogram alone cannot distinguish these cases.

### CV-SVD-005 — An invertible homography can have a zero last coefficient

Constructed example: $H=\begin{bmatrix}1&0&1\\0&1&0\\1&0&0\end{bmatrix}$ has determinant $-1$ and $h_{33}=0$. For $x\ne0$, it maps $(x,y)$ to $((x+1)/x,y/x)$ and is a valid projective transform. An implementation that always normalizes by $h_{33}$ would reject or corrupt this solution despite its invertibility. Choose a valid homogeneous scale and check the projective denominator on the intended image region; invertible matrices can still send some finite points to infinity.

### CV-SVD-006 — Normalization is not geometric evidence

Consider four points lying almost on one line. Centering and scaling can make their coordinate magnitudes well behaved while leaving the near-collinearity intact. Normalization addresses numerical scale; it does not restore independent projective constraints. After denormalization, assess transfer errors and the location of held-out points in the original image. A small algebraic error in normalized coordinates is insufficient when extrapolation far from the observed support changes markedly under tiny perturbations.

### CV-SVD-007 — Accepted steps need model agreement

Define the local quadratic model $m(\delta)=\tfrac12\|r+J\delta\|^2$. When its predicted reduction is positive, compare it with the actual reduction using $\eta=[F(x)-F(x+\delta)]/[m(0)-m(\delta)]$. A negative ratio means the step increased the true cost despite a favorable prediction. This constructed interpretation explains shrinking the trust region and recomputing a step. The ratio does not certify global optimality, and its denominator requires care near termination.

### CV-SVD-008 — A robust scale changes influence, not the residual unit

For scalar residual magnitude $u$, the scaled Huber derivative with respect to $s=u^2$ is one when $|u|\le a$, then $a/|u|$. The corresponding residual influence saturates instead of growing indefinitely. A residual of $10a$ still exerts influence: it is downweighted, not deleted. For a whitened two-component residual, $a$ sets the transition radius for the joint norm; interpreting it as a per-axis confidence interval would impose a different acceptance region.

### CV-SVD-009 — More repeated data do not remove a gauge

For independent repeated measurements with unchanged geometry, information adds and an observable standard deviation can decrease approximately as $1/\sqrt N$. But a direction that is exactly unobservable contributes zero information in every repetition, so repetition leaves it unobservable. Likewise, a shared calibration bias is not averaged away as independent noise. This distinction separates local covariance under an assumed model from the uncertainty of deploying that model on another camera or temperature regime.

Consulted foundations: [Ceres covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html): Introduction, Gauge Invariance and Rank of the Jacobian; Context7 checked; [Ceres solving](https://ceres-solver.readthedocs.io/latest/nnls_solving.html): Trust Region Methods and Linear Solvers; [Ceres modeling](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html): LossFunction and scaling.

## Sources and flashcards

### Scientific sources

- [Hartley 1997, In Defense of the Eight-Point Algorithm, IEEE TPAMI 19(6)](https://doi.org/10.1109/34.601246): §2.2–§2.3 linear solution and rank-2 correction, §3 denormalization and non-invariance, §4 the $d_1/d_8$ argument and the $10^8$-to-1 diagonal, §5.1 isotropic normalization, §5.2 non-isotropic scaling, §6 equal treatment of entries by the Frobenius correction, §7.3.1 condition-number gain of about $10^8$, §§7.3.4–7.3.5 comparisons. Publisher's version paywalled; read on a course copy (pp. 583–589).
- [Zhang 1998, A Flexible New Technique for Camera Calibration, MSR-TR-98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf): §3.2 Levenberg–Marquardt refinement after the closed-form solution; Appendix A, DLT by singular vector and normalization.
- [Triggs, McLauchlan, Hartley and Fitzgibbon 2000, Bundle Adjustment — A Modern Synthesis](https://inria.hal.science/inria-00548290): §3.1 asymptotic properties and dispersion, §3.3 robustified least squares and irreducible observation groups, §4.2 step control, §4.3 Gauss–Newton, QR versus normal equations and footnote 6 ($O(C\epsilon)$ versus $O(C^2\epsilon)$), §6.1 Schur complement, §9 gauge freedom.
- [Chum, Werner and Matas 2005, Two-View Geometry Estimation Unaffected by a Dominant Plane, CVPR](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf) ([DOI](https://doi.org/10.1109/CVPR.2005.354)): abstract, §1 and Fig. 1 caption (H-degenerate samples, DEGENSAC).

### Implementation sources

- Ceres Solver 2.2.0 documentation sources: [`nnls_covariance.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_covariance.rst) (Introduction, Gauge Invariance, Rank of the Jacobian, `Covariance::Options`); [`nnls_solving.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_solving.rst) (Trust Region Methods, Levenberg–Marquardt, `DENSE_QR`, `DENSE_NORMAL_CHOLESKY`, `DENSE_SCHUR` and `SPARSE_SCHUR`, `Solver::Options`); [`nnls_modeling.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_modeling.rst) (`LossFunction`, scaling, Huber and Cauchy). Rendered pages: [covariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), [solving](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), [modeling](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) (development version).
- Ceres Solver 2.2.0 code: [`include/ceres/solver.h`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/include/ceres/solver.h) L276–L295 and [`internal/ceres/levenberg_marquardt_strategy.cc`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/internal/ceres/levenberg_marquardt_strategy.cc) L76–L97, L157–L170.
- [OpenCV 4.13.0, `modules/core/include/opencv2/core.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core.hpp): `solve` (L1944–L1968), `SVD::solveZ` (L2818–L2828); [`core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp): `DecompTypes` (L133–L152).
- [OpenCV 4.13.0, `modules/calib3d/src/fundam.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp): `scaleFor` (L52–L57), homography kernel (L111–L189), refinement residuals (L231–L272), `findHomography` dispatch and LM refinement (L401–L434), eight-point algorithm (L693–L790).
- [NumPy 2.2, `numpy.linalg.lstsq`](https://numpy.org/doc/2.2/reference/generated/numpy.linalg.lstsq.html): `rcond` default, minimum-norm solution, returned rank, singular values and residuals.
- [Eigen 3.4, Solving linear least squares systems](https://libeigen.gitlab.io/eigen/docs-3.4/group__LeastSquares.html): accuracy and speed of SVD, QR and normal equations; QR variants.

### Related flashcards and references

- [Flashcards](../11-moindres-carres-svd.md): CV-SVD-001 to CV-SVD-009.
- Applications: [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md), [CV-ZHANG](../../50-calibration-geometrie/references/52-calibration-zhang.md), [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md), [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md), [CV-FACTEURS](14-graphes-facteurs.md).

The perturbation cases, the identifiability example and the diagnostic tests are algebraic reasoning of the project, not published experiments.

Drafted by agent, 2026-10-18. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation. Revision 10, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/11-moindres-carres-svd.md).
