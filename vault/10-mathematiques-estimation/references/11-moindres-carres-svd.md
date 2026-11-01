---
id: CV-SVD
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 7
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Least squares, SVD and conditioning

## Problem, data and assumptions

Estimate geometric parameters from noisy observations. Inputs: $A\in\mathbb R^{m\times n}$, $b\in\mathbb R^m$ and their unit contract; output: parameters and rank diagnosis. A linearized model is only valid near its point of development. Outliers require a robust treatment distinct from the choice of solver.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Project observations onto the space explained by the model; solve by QR or SVD, inspect singular values and residuals, and then confront the solution with reserved observations. The SVD breaks down well or badly constrained directions; a small adjustment error does not attest to identifiability.

## Mathematics, conventions and units

We minimize $\|Ax-b\|_2^2$. If $A=U\Sigma V^T$ is the thin SVD with a full column rank, $\hat x=V\Sigma^{-1}U^Tb$, so $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)\,v_i$: a perturbation of the measurements is amplified by $1/\sigma_i$ along the right singular vector $v_i$. Conversely, $\|A(t\,v_i)\|=|t|\,\sigma_i$: along a direction of small singular value, the parameters can move without changing the residual. This relationship is an algebraic derivation of the project. The conditioning $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$ depends on the scale of the columns, therefore the units of the parameters. With a full column rank, $\kappa_2(A^TA)=\kappa_2(A)^2$: normal equations amplify the conditioning. For a residual $r$ and its positive definite covariance $C$, $r^TC^{-1}r$ is without unit. Whitening means forming $L^{-1}r$ with $C=LL^T$; the quadratic shape is its squared norm. A singular covariance requires processing the constraints or subspace observable separately; mixing pixels and meters without weighting arbitrarily modifies the objective.

## Homogeneous system, DLT and standardization

The linear estimation of a homography or a fundamental matrix is written $Lh=0$, with $h$ defined to one factor. For a homography, each correspondence provides two linear equations in the nine coefficients, hence $L\in\mathbb R^{2n\times9}$; for $F$, a correspondence equation and at least eight points. We minimize $\|Lh\|$ under $\|h\|=1$ to exclude the zero solution; the solution is the right singular vector of the smallest singular value, or the minimal eigenvector of $L^TL$ (Zhang 1998, Appendix A; Hartley 1997, §2.2). For $F$, we then impose the rank 2 by cancelling the smallest singular value: the matrix obtained is the closest in Frobenius norm (Hartley 1997, §2.3). This cost is algebraic and has no direct physical interpretation: Zhang uses it to initialize, then minimizes the reprojection error (§3.2).

On raw pixels, a line of $L$ mixes 1, coordinates of the order of $10^3$ and products of the order of $10^6$; Zhang notes that $L$ is then poorly packaged. Hartley (§4) shows that such a spread makes the clean vector very sensitive to noise, according to the ratio $d_1/d_8$. Its normalization (§5.1) processes each image separately: translation of the centroid at the origin, then isotropic scaling for an average distance of $\sqrt2$. It is estimated on the normalized points $\hat x=Tx$, $\hat x'=T'x'$, then we denormalize: $H=T'^{-1}\hat HT$, or $F=T'^T\hat FT$ (§3). The algebraic least squares solution is not invariant to these transformations (§3): normalizing changes the estimator. On the pair "house", the conditioning improves by about $10^8$ (§7.3.1).

## Less nonlinear squares and robust losses

For a nonlinear residual $r(x)$ of Jacobian $J$, Gauss-Newton linearizes $r(x+\delta)\approx r(x)+J\delta$ and resolves $J^TJ\delta=-J^Tr$. It replaces the hessian with $J^TJ$, a valid approximation if the residuals are small or the model almost linear; otherwise the convergence slows down strongly (Triggs et al. 2000, §4.3). Levenberg-Marquardt cushions the step: $(J^TJ+\lambda D^TD)\delta=-J^Tr$. $\lambda$ grows when the prediction is wrong, which shortens the step towards the gradient descent, and otherwise decreases (§4.2). Ceres the formula in trust region of radius $\mu$, doubled or halved according to the ratio between actual drop and predicted drop; $D$ is often the root of the diagonal of $J^TJ$. These methods find a local minimum: they require an initialization, linear or closed, in the right basin.

A robust loss replaces the $s=\|f\|^2$ contribution of a block by $\frac12\rho(s)$, with $\rho(0)=0$ and $\rho'(0)=1$, to mimic the near-zero quadratic cost and reduce the weight of the large residuals. With the scale $a$, $\rho(s,a)=a^2\rho(s/a^2)$: $a$ has the standard unit of the residual. Ceres defines Huber, $\rho(s)=s$ for $s\le1$ and $2\sqrt s-1$ beyond, and Cauchy, $\rho(s)=\log(1+s)$. Their weights $\rho'(s)$ decrease to $1/\|f\|$ and $1/\|f\|^2$, project calculation. Triggs et al. apply $\rho$ to the weighted residual $\Delta z^TW\Delta z$, each group of observations being accepted or reduced in bulk (§3.3). They also note that an error affecting all observations, such as a false projection model, is not corrected by simply cleaning up the data. A robust loss also does not provide initialization: with a lot of outliers, a filtering like RANSAC precedes it. This articulation is a reasoning of the project.

## Uncertainty of parameters

Ceres gives $C(x^*)=(J^TJ)^{-1}$ as covariance of the estimated, under two assumptions. The residuals must have an identity covariance, which the user gets by rating $S^{-1/2}f$. $J$ must have a full column rank; otherwise the covariance is deficient and given by the pseudo-inverse. In SfM, the reconstruction is only defined with one similarity: this gauge requires a SVD or a suitable inversion. The default algorithm, `SPARSE_QR`, does not handle a deficient Jacobian: `Compute()` returns false. `DENSE_SVD` treats it, for small or medium problems. Triggs et al. (§3.1) recall that dispersion approaches the covariance of the estimator only asymptotically; this is much less safe for small geometry problems and weak networks. This covariance measures neither model bias nor outliers.

## Parameters and properties

Center/scale variables, set rank tolerance and justify regularization. Poor rank, poor conditioning and poor physical fitness are three different diagnoses. Regularizing adds a hypothesis; it does not create an observation.

## Cost and implementation

SVD makes it easy to diagnose rank but can cost more than a suitable QR. Eigen ranks the SVD as generally the most accurate but the slowest. It presents the normal equations as in general the fastest, especially for $A$ high and narrow, but not recommended as soon as $A$ is even moderately ill conditioned, because they lose about twice as many digits. Order of magnitude of the project: with $\kappa_2(A)=10^6$, about 6 of the 16 digits of double precision are threatened with QR, about 12 with normal equations.

The great sparse problems overturn the arbitration. Ceres recommends `DENSE_QR` for small, dense issues and warns that `DENSE_NORMAL_CHOLESKY` may fail for a poorly packaged Jacobian. For the bundle adjustment, however, it forms the normal equations and eliminates the points by Schur complement: `DENSE_SCHUR` remains passable up to a few hundred cameras, `SPARSE_SCHUR` targets thousands. Scaling the parameters and preconditioning are therefore essential. No Eigen/Ceres calls are executed here; avoid materializing an inverse as the default recipe.

## Evaluation and controlled variation

Analytical case: two almost identical columns give a direction with little constraint. Slightly disturb b by keeping A fixed: predict a strong variation of the parameters in this direction, even if the residuals changes little. Compare QR/SVD and stability, not just minimal cost.

Calculation executed by the project the 2026-10-23 out of the repository (Python 3.10.13, NumPy 2.2.6): $A$ of three rows, of columns $(1,1,1)$ and $(1;1{,}001;0{,}999)$, a $\sigma_2\approx10^{-3}$ and $\kappa_2(A)\approx2{,}4\cdot10^3$. A $b$ disturbance of $10^{-3}$ aligned to $u_2$ moves $\hat x$ from a 1,0 standard to $v_2\approx(1,-1)/\sqrt2$; the residual remains in the order of $10^{-16}$. Ceres illustrates the same phenomenon with $J=\begin{pmatrix}1&1\\1&1{,}0000001\end{pmatrix}$: $(J^TJ)^{-1}$ has terms of about $\pm2{,}05\cdot10^{14}$, a result that the documentation deems unusable. These are constructed cases, not measurements on images.

Controlled variation of the DLT, performed in the same environment. Baseline: DLT of homography on raw pixel coordinates. Varied factor: Hartley's only normalization, with identical data. The case is built: homography known close to the identity, Gaussian noise of 0,5 px, 200 prints by configuration. Prediction: sharp drop of $\sigma_1/\sigma_8$ in all cases, gain of precision especially when the points are far from the origin compared to their extent. Measurement: median transfer error on 200 points distributed throughout the image 1920×1080.

| Configuration | $\sigma_1/\sigma_8$ brut | Standardized | Gross error | Standardized |
| --- | --- | --- | --- | --- |
| 50 points on the whole image | $8{,}3\cdot10^6$ | 4,1 | 0,22 px | 0,20 px |
| 8 points on the whole image | $1{,}2\cdot10^7$ | 6,6 | 0,70 px | 0,67 px |
| 20 points in a square of 200 px | $1{,}4\cdot10^8$ | 3,5 | 1013 px | 28 px |

Reading: in double precision, well distributed points tolerate the absence of normalization; points concentrated far from the origin do not tolerate it. Normalizing does not replace coverage: 28 px remains a fragile extrapolation. Limitations: a single model, isotropic noise, no outliers, no real image.

## Failure modes and diagnosis

Huge parameters with small residual suggest ambiguity, units or conditioning. Inspect singular spectrum and physical constraints; inject independent measurements before only increasing the number of iterations.

After a robust estimator, two causes of instability are separated. Outliers remaining among the inliers leave a tail of residuals near the threshold; removing them stabilizes the estimate. A quasi-degeneration is due to the geometry of the inliers, aligned, concentrated or almost coplanar depending on the model: the solution varies along the same direction even on clean inliers. The rejection of outliers does not change anything; only a better cover or a more constrained model remedy it. Chum, Werner and Matas (2005) give a case: with a dominant plane, a sample of seven correspondences of which at least five verify a homography produces an epipolar geometry compatible with this whole plane. Their theorem explains why RANSAC often fails on epipolar geometry in the presence of a dominant plane. For a homogeneous system $Lh=0$, the solution is carried by the smallest singular value: it is the penultimate one that must remain clearly non-zero, which Hartley (1997, §4) expresses by the ratio $d_1/d_8$. The residuals tail, cover and resampling tests are project proposals.

## Alternatives and applications

QR for a well-established problem, SVD for rank diagnosis and homogeneous systems, sparse solver for large reconstructions, robust estimation against outliers. Common string in geometry: RANSAC on a minimal model, DLT standardized on the inlays, then Levenberg-Marquardt on the geometric error with a robust loss, and finally reading the covariance if the rank allows. The choice depends on the data and the linear system.

## Guided reasoning and proposed checks

These constructed cases develop whitening, loss of rank and distinction adjustment – identification. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SVD-002

**Question of work**: To solve $\min_x\|Ax-b\|_2$ with a full-column-rank matrix $A$, when should you prefer QR or SVD factorization of $A$, and when are the normal equations $A^TAx=A^Tb$ solved by Cholesky still a defensible choice?

**Reference Response**: Forming $A^TA$ raises the squared conditioning, $\kappa_2(A^TA)=\kappa_2(A)^2$, and loses about twice as many significant figures. QR, or SVD more accurate but slower and useful for diagnosing rank, is required as soon as $A$ is poorly conditioned, even moderately. Normal equations are generally the fastest, especially for high and narrow $A$: they remain defensible if $A$ is well conditioned after scaling, and large sparse problems such as bundle adjustment exploit them by Schur's Cholesky sparse and complement.

**Reading for a project**: choose the solver after examining rank, scales and sparse structure. A lower resolution time does not compensate for parameters that have become unusable. Also compare stability when observations are slightly disturbed, with the same objective and the same units.

### Case linked to CV-SVD-009

**Question of work**: After nonlinear least squares, parameter uncertainty is inferred from $(J^TJ)^{-1}$, where $J$ is the Jacobian at the solution. Under which conditions is this interpretation valid, and what does it fail to measure?

**Reference Response**: whitened residuals, of identity covariance, and a $J$ of column rank full; the matrix obtained is then the local dispersion of the estimate, which approaches its covariance only asymptotically. If $J$ is deficient in rank (gauge, parameter not observable), $J^TJ$ is not invertible: fix the gauge, reparameterize or use a pseudo-inverse. It measures neither a model bias, like a mismodeled distortion, nor the effect of outliers: it assumes correct model and noise.

**Proposed action**: Compare the announced intervals to controlled repetitions or disturbances, keeping gauge and units. A low dispersion around a biased solution remains compatible with poor accuracy. Separate local uncertainty, variation between acquisitions and adequacy of the physical model.

**Documentary reference for this pass**: [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), Introduction, Rank of the Jacobian and Gauge Invariance. The other developments are in the [flashcards](../11-moindres-carres-svd.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SVD-001

**Situation**: A linear estimate $\hat x=\arg\min_x\|Ax-b\|_2$ has a very small residual, but $\hat x$ changes substantially when the measurements $b$ are slightly perturbed. For a full-column-rank thin SVD $A=U\Sigma V^T$, what relationship explains why a good fit does not guarantee reliable parameters?

**Reading subspaces**: For $m\ge n$ and a full column rank, $\hat b=A\hat x=UU^Tb$ is the projection of $b$ on the column space, while the orthogonal residual is $(I-UU^T)b$. A disturbance in this space can strongly change $\hat x$ without increasing this residual. This is precisely why the diagnosis must examine both fit and sensitivity. If a singular value is exactly zero, some components are no longer determined by observations: the pseudo-inverse chooses a solution of minimum norm, without establishing that this solution is physically true. These equalities are deductions from the SVD, with $U$ containing the singular observable columns.

### CV-SVD-002

**Situation**: To solve $\min_x\|Ax-b\|_2$ with a full-column-rank matrix $A$, when should you prefer QR or SVD factorization of $A$, and when are the normal equations $A^TAx=A^Tb$ solved by Cholesky still a defensible choice?

**What QR does**: with the reduced factorization $A=QR$, $Q^TQ=I$ and upper triangular $R$, we project $b$ into $Q^Tb$ and then solve $R\hat x=Q^Tb$ by substitution. Orthogonal transformations preserve norms and avoid forming column products of $A^TA$. The SVD replaces this triangle with singular directions and allows a low numerical rank to be explicitly processed. In a dense problem with $m\gg n$, costs depend mostly on $mn^2$ at different constants; in a sparse system, factor filling and elimination order can become decisive. Comparing only the dimensions of the system is therefore not enough to predict time and memory.

### CV-SVD-003

**Situation**: A calibration objective adds an error in pixels to an error in meters. How can you prevent the units from determining their relative weights?

**Why Invariance to Units Works**: For invertible linear transformation of $r'=Dr$ units, the correct covariance becomes $C'=DCD^T$. Then $r'^TC'^{-1}r'=r^TC^{-1}r$. Changing the residuals without changing their covariance breaks this invariance. Whitening by Cholesky is calculated by solving $Lz=r$, rather than materializing $L^{-1}$. If two errors come from the same detection or sensor, correlations can make their naïve addition overconfident. They must be modelled or independence announced as an approximation; a robust loss does not repair this double counting. The quadratic form is dimensionless, but the final covariances of the parameters retain their own units.

### CV-SVD-004

**Situation**: After RANSAC, a transformation fitted to a large consensus changes substantially between runs or inlier subsets. Which checks distinguish remaining outliers from a nearly degenerate configuration?

**What spectrum to examine**: for a homogeneous system with nine parameters whose scale is arbitrary, we expect a single solution direction. If the points are quite numerous, a second direction almost zero means that several transformations explain almost as much of the data. The ratio between the last singular values informs this separation; for the minimum eight-line system, the exact kernel must also be taken into account, because a reduced SVD may not return its vector. These diagnoses are specific to the model and its normalization: always using the same spectral threshold on arbitrary units would be misleading. A spot test then examines the geometric effect of this ambiguity.

### CV-SVD-005

**Situation**: Describe direct linear transformation (DLT) estimation of a homography $H$ from $n\ge4$ point correspondences: which system is constructed, which constraint is imposed, and which vector is selected as the solution?

**Explicit construction of a line**: for $(x,y)\mapsto(u,v)$, attach $h=(h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33})^T$. The projective relation gives lines $[x,y,1,0,0,0,-ux,-uy,-u]$ and $[0,0,0,x,y,1,-vx,-vy,-v]$. These constraints are stacked and then the solution vector is put back into a $3\times3$ matrix. With exactly four pairs, the matrix is $8\times9$: you have to get the full right kernel, not blindly select the last vector of a truncated factorization. The four points must provide independent constraints. An arbitrary normalization of $h_{33}$ is not possible if this component is zero or too close to zero; the homogeneous geometry allows other scaling choices.

### CV-SVD-006

**Situation**: Why is DLT built from raw pixel coordinates on the order of $10^3$ poorly conditioned, and which normalization proposed by Hartley addresses this?

**Calculate the normalization**: for points $p_i=(x_i,y_i)$, calculate $c=n^{-1}\sum_i p_i$, the average distance $\bar d=n^{-1}\sum_i\|p_i-c\|_2$, then $s=\sqrt2/\bar d$ if $\bar d>0$. The homogeneous transformation has lines $(s,0,-sc_x)$, $(0,s,-sc_y)$ and $(0,0,1)$. It must be calculated separately in each image. If all the points coincide, this operation is indefinite: it is not a simple rounding problem, but an absence of usable geometry. After denormalization, compare the residuals in pixels in the original images; a residual expressed in the centered and reduced coordinates does not keep the same numerical threshold.

### CV-SVD-007

**Situation**: When refining calibration by minimizing nonlinear reprojection error, what does one Gauss–Newton iteration compute, how does Levenberg–Marquardt make the step safer, and what condition do both methods require?

**Neglected by Gauss-Newton**: for $F(x)=\tfrac12\sum_i r_i(x)^2$, the exact hessian is $J^TJ+\sum_i r_i\nabla^2r_i$. Large errors or a strong curvature of the model make the second term potentially important. The damping of LM makes the step more careful, without turning the wrong projection into a good model. An iteration must compare the actual cost after update to the decline predicted by linearization, accept or decline the step, and then adjust its trusted region. Stopping only because the parameters no longer move can also mean a blocked step: check cost convergence, gradient, scales and physical validity of the solution.

### CV-SVD-008

**Situation**: In Ceres, a `HuberLoss(a)` or `CauchyLoss(a)` is attached to reprojection residual blocks. Which quantity does the loss act on, and how should $a$ be chosen for pixel residuals versus whitened residuals?

**Interpretation of weights**: in an approximation of reweighted least squares, the block $f$ receives a weight related to $\rho'(\|f\|^2)$; we therefore apply approximately $\sqrt{\rho'}$ to its components and its Jacobian. The exact solver can also take into account $\rho''$: this reasoning explains the influence without describing all its numerical corrections. For a reprojection error 2D, treat $(e_x,e_y)$ as a block together reduces the observation contribution; two separate scalar losses are another objective. After whitening, the threshold refers to a multidimensional norm: "two standard deviations" of an axis does not automatically give a probability of rejection of the entire block.

### CV-SVD-009

**Situation**: After nonlinear least squares, parameter uncertainty is inferred from $(J^TJ)^{-1}$, where $J$ is the Jacobian at the solution. Under which conditions is this interpretation valid, and what does it fail to measure?

**Limit of the pseudo-inverse**: undoing a singular direction to construct a pseudo-inverse does not demonstrate zero physical variance in that direction. An unfixed gauge describes a family of equivalent solutions; it is necessary to announce the coordinates or relative quantities in which an uncertainty makes sense. After a local reparameterization $y=g(x)$, the first-order propagation is $C_y\approx G C_xG^T$, $G=\partial g/\partial x$. Cross terms can then strongly influence a distance or a relative pose. Reading only the diagonal standard deviations loses these couplings. A local covariance resulting from a robust cost also requires announcing the chosen approximation convention, rather than automatically using the ordinary Gaussian formula.

**Passages consulted for these developments**: [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), Introduction, Gauge Invariance and Rank of the Jacobian; [Ceres, Solving Non-linear Least Squares](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), Linearization, Trust Region and Linear Solvers.

## Sources and flashcards

- [Ceres, Covariance Estimation, Introduction and Rank of the Jacobian (consulted on 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
- [Ceres, Modeling Non-linear Least Squares, Introduction (accessed on 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html).

These documents support solvers, whitening and outlier treatment. The case of perturbation and the diagnosis of geometry are algebraic reasonings of the project; they do not constitute a published experiment.

- [Eigen 5.0.1-dev, Solving linear least squares systems, Using the SVD decomposition / Using normal equations (documentation accessed on 2026-10-23; the old eigen.tuxfamily.org address redirects here)](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html).
- [Ceres, Solving Non-linear Least Squares, Linear Solvers and Schur complement trick (accessed 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
- [Chum, Werner and Matas 2005, Two-View Geometry Estimation Unaffected by a Dominant Plane, CVPR, summary](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf) ; [DOI](https://doi.org/10.1109/CVPR.2005.354).
- [Hartley 1997, In Defense of the Eight-Point Algorithm, IEEE TPAMI 19(6)](https://doi.org/10.1109/34.601246): §§2.2 – 2.3 linear solution and rank 2, §3 denormalization and non-invariance, §4 ratio $d_1/d_8$, §5.1 isotropic standardization, §7.3.1 packaging gain. Paid editor version; passages read on a university copy.
- [Zhang 1998, A Flexible New Technique for Camera Calibration, MSR-TR-98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf): §3.2 refinement Levenberg-Marquardt after closed solution, annex A DLT and standardization.
- [Triggs, McLauchlan, Hartley and Fitzgibbon 2000, Bundle Adjustment –  A Modern Synthesis](https://inria.hal.science/inria-00548290): §3.1 asymptotic covariance, §3.3 least robust squares, §4.2 step check, §4.3 Gauss-Newton, QR and normal equations.
- [Ceres, Modeling Non-linear Least Squares, LossFunction (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html): conditions on $\rho$, Huber, Cauchy, scale $a$.
- [Ceres, Covariance Estimation, Gauge Invariance and Covariance::Options (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) : gauge, `SPARSE_QR`, `DENSE_SVD`, `min_reciprocal_condition_number`.
- [Related flashcards](../11-moindres-carres-svd.md): CV-SVD-001 to 009.

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation.
