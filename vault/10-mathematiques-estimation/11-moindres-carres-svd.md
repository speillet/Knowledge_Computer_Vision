# Flashcards — Least squares, SVD and conditioning

reference note: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SVD-001

Objective: distinguish residual and identifiability. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-001
Question: A linear estimate $\hat x=\arg\min_x\|Ax-b\|_2$ has a very small residual, but $\hat x$ changes substantially when the measurements $b$ are slightly perturbed. For a full-column-rank thin SVD $A=U\Sigma V^T$, what relationship explains why a good fit does not guarantee reliable parameters?
Reponse: **Expected answer**: $\delta\hat x=V\Sigma^{-1}U^T\delta b=\sum_i\frac{u_i^T\delta b}{\sigma_i}v_i$: the disturbance is amplified by $1/\sigma_i$ along the right singular vector $v_i$. Conversely, moving $x$ from $t\,v_i$ only changes $Ax$ from $|t|\,\sigma_i$ to norm: if $\sigma_i$ is small, the parameters move without the residual changing. A small residual therefore does not prove identifiability; it is necessary to inspect the small singular values and $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$.

**Further explanation**: case executed by the project: two columns that differ from $10^{-3}$ give $\sigma_2\approx10^{-3}$; disrupt $b$ of $10^{-3}$ according to $u_2$ moves $\hat x$ of a norm 1 according to $v_2\approx(1,-1)/\sqrt2$, residual always zero. Ceres shows the same effect on covariance: $(J^TJ)^{-1}$ reaches $\pm2\cdot10^{14}$ for an almost singular Jacobian. $\kappa_2$ depends on the units of the columns: scale the parameters before concluding.

**Reading subspaces**: For $m\ge n$ and a full column rank, $\hat b=A\hat x=UU^Tb$ is the projection of $b$ on the column space, while the orthogonal residual is $(I-UU^T)b$. A disturbance in this space can strongly change $\hat x$ without increasing this residual. This is precisely why the diagnosis must examine both fit and sensitivity. If a singular value is exactly zero, some components are no longer determined by observations: the pseudo-inverse chooses a solution of minimum norm, without establishing that this solution is physically true. These equalities are deductions from the SVD, with $U$ containing the singular observable columns.

**A fit with arbitrarily unstable parameters**: Constructed example: let $A=\operatorname{diag}(1,10^{-6})$ and $b=(1,0)^T$. The least-squares solution is $(1,0)^T$. Perturb only the second observation by $10^{-6}$: the solution becomes $(1,1)^T$, while both fits have zero residual. Thus even an exact fit can move one parameter by one unit. These numbers assume compatible, fixed parameter units; rescaling a column changes the numerical condition number without supplying any missing measurement.

**Blocking errors**: assimilate small residual and reliable parameters; assign sensitivity to large singular values; confuse the directions of $v_i$ parameters and $u_i$ measurements.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Ceres, Covariance Estimation, Rank of the Jacobian and `min_reciprocal_condition_number` (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); relation derived from the SVD by the project; [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SVD-001 provenance::agent pole::B pole::C
END

## CV-SVD-002

Objective: choose QR or normal equations. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-002
Question: To solve $\min_x\|Ax-b\|_2$ with a full-column-rank matrix $A$, when should you prefer QR or SVD factorization of $A$, and when are the normal equations $A^TAx=A^Tb$ solved by Cholesky still a defensible choice?
Reponse: **Expected answer**: Forming $A^TA$ raises the squared conditioning, $\kappa_2(A^TA)=\kappa_2(A)^2$, and loses about twice as many significant figures. QR, or SVD more accurate but slower and useful for diagnosing rank, is required as soon as $A$ is poorly conditioned, even moderately. Normal equations are generally the fastest, especially for high and narrow $A$: they remain defensible if $A$ is well conditioned after scaling, and large sparse problems such as bundle adjustment exploit them by Schur's Cholesky sparse and complement.

**Further explanation**: order of magnitude: with $\kappa_2(A)=10^6$, about 6 of the 16 digits of the double precision are threatened with QR, 12 with the normal equations. Ceres advises `DENSE_QR` for small, dense problems and `SPARSE_SCHUR` for BAs with thousands of cameras. Factor and then solve: the explicit inverse is useless.

**Reading for a project**: choose the solver after examining rank, scales and sparse structure. A lower resolution time does not compensate for parameters that have become unusable. Also compare stability when observations are slightly disturbed, with the same objective and the same units.

**What QR does**: with the reduced factorization $A=QR$, $Q^TQ=I$ and upper triangular $R$, we project $b$ into $Q^Tb$ and then solve $R\hat x=Q^Tb$ by substitution. Orthogonal transformations preserve norms and avoid forming column products of $A^TA$. The SVD replaces this triangle with singular directions and allows a low numerical rank to be explicitly processed. In a dense problem with $m\gg n$, costs depend mostly on $mn^2$ at different constants; in a sparse system, factor filling and elimination order can become decisive. Comparing only the dimensions of the system is therefore not enough to predict time and memory.

**Choosing a solver by error budget**: A useful project decision is to compare $\kappa_2(A)\epsilon$ and $\kappa_2(A)^2\epsilon$, with machine precision $\epsilon$, to the tolerated relative numerical error. These are sensitivity indicators, not exact error predictions. For double precision and $\kappa_2(A)=10^8$, the second expression is of order one: explicitly forming normal equations can consume the useful precision. Solver success therefore needs a scaled residual and a stability check, rather than a successful Cholesky return alone.

**Blocking errors**: say that two mathematically equivalent formulations are numerically identical; exclude normal equations in any circumstance, including for a sparse BA.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Triggs et al. 2000, §4.3, QR and normal equations](https://inria.hal.science/inria-00548290); [Eigen 5.0.1-dev, Solving linear least squares systems, Using normal equations (accessed on 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html); [Ceres, Solving Non-linear Least Squares, Linear Solvers and Schur complement trick (accessed 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html); [Ceres, Covariance Estimation, Introduction, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SVD-002 provenance::agent pole::B pole::C
END

## CV-SVD-003

Objective: weighting heterogeneous residuals. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-003
Question: A calibration objective adds an error in pixels to an error in meters. How can you prevent the units from determining their relative weights?
Reponse: **Expected answer**: Set the covariance $C$ of the residuals, assumed to be positive definite, and then whiten them: with $C=LL^T$, use $L^{-1}r$. Its norm squared is $r^TC^{-1}r$, dimensionless and weighted by uncertainty.

**Further explanation**: Changing meters to millimeters must not arbitrarily change the solution. Example calculated by the project: $r_{px}=0{,}8$ px with $\sigma_{px}=0{,}5$ px, $r=3$ mm with $\sigma=2$ mm. The gross sum of the squares is 0,64 in meters and 9,64 in millimeters: the unit chooses which term dominates. The amount cleared is 4,81 in both cases. Check noise pattern and correlations; a possible robust loss then applies to the whitened residual.

**Interpretation**: The whitening expresses each deviation relative to the noise attributed to it by the model. A two-pixel residual can be banal with an uncertainty of ten pixels and surprising with an uncertainty of 0,1 pixels. The off-diagonal terms of $C$ count if the observations are correlated: dividing each component by its standard deviation is then not a complete whitening. A weighting chosen to obtain a beautiful solution does not automatically become a justified noise model.

**Why Invariance to Units Works**: For invertible linear transformation of $r'=Dr$ units, the correct covariance becomes $C'=DCD^T$. Then $r'^TC'^{-1}r'=r^TC^{-1}r$. Changing the residuals without changing their covariance breaks this invariance. Whitening by Cholesky is calculated by solving $Lz=r$, rather than materializing $L^{-1}$. If two errors come from the same detection or sensor, correlations can make their naïve addition overconfident. They must be modelled or independence announced as an approximation; a robust loss does not repair this double counting. The quadratic form is dimensionless, but the final covariances of the parameters retain their own units.

**Correlated measurements do not count twice**: For two unit-variance residuals with correlation $\rho$, take $C=\begin{bmatrix}1&\rho\\\rho&1\end{bmatrix}$. Along $r=(a,a)^T$, the weighted cost is $2a^2/(1+\rho)$; along $(a,-a)^T$, it is $2a^2/(1-\rho)$. As $\rho$ approaches one, common deviations carry almost one independent observation, while disagreement becomes very unlikely. This constructed example explains why dividing each component by its own standard deviation cannot replace full whitening when correlations matter.

**Blocking errors**: Add the raw values and interpret their sum as a likelihood.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Ceres, Covariance Estimation, Introduction and Rank of the Jacobian (consulted on 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SVD-003 provenance::agent pole::B pole::C
END

## CV-SVD-004

Objective: distinguish outliers and deficient rank. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-004
Question: After RANSAC, a transformation fitted to a large consensus changes substantially between runs or inlier subsets. Which checks distinguish remaining outliers from a nearly degenerate configuration?
Reponse: **Expected answer**: remaining outliers may produce a residual tail or unstable fits; test whether removing independently suspicious matches stabilizes the estimate, without treating this as a guarantee. A quasi-degeneration is seen in the geometry of the inliers, aligned, concentrated or almost coplanar according to the model, and in a small singular value after normalization: the solution varies in the same direction even on own inliers. The rejection of outliers does not create the missing constraints: only a better cover or a more constrained model corrects this second case.

**Further explanation**: published case: with a dominant plane, a sample of seven correspondences of which at least five verify a homography gives an epipolar geometry compatible with the whole plane; hence a broad consensus for a poorly determined fundamental matrix (Chum, Werner and Matas 2005). For a homogeneous system $Lh=0$, it is the penultimate singular value that must remain clearly non-zero.

**check**: maintain the same observations, readjust to several subsets and visualize the direction of parameter variation. Then compare a better spatial distribution rather than a simple higher quota. The two causes can coexist: correcting the outliers does not yet validate the remaining geometry.

**What spectrum to examine**: for a homogeneous system with nine parameters whose scale is arbitrary, we expect a single solution direction. If the points are quite numerous, a second direction almost zero means that several transformations explain almost as much of the data. The ratio between the last singular values informs this separation; for the minimum eight-line system, the exact kernel must also be taken into account, because a reduced SVD may not return its vector. These diagnoses are specific to the model and its normalization: always using the same spectral threshold on arbitrary units would be misleading. A spot test then examines the geometric effect of this ambiguity.

**A diagnostic requires competing explanations**: Refit the same normalized model after small coordinate perturbations and after removing candidate outliers, recording both parameter changes and predictions on spatially separated held-out points. Persistent variation along a weak singular direction supports poor geometric constraint; stabilization after rejecting independently suspicious matches supports contamination. Neither is a proof in isolation: outliers can form a coherent alternative model, and aggressive filtering can make coverage worse. A low residual histogram alone cannot distinguish these cases.

**Blocking errors**: assume that a robust estimator corrects a degenerate geometry; conclude to outliers as soon as a solution is unstable.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Chum, Werner and Matas 2005, summary and theorem of the dominant plane](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf); [Hartley 1997, §4, role of $d_1/d_8$](https://doi.org/10.1109/34.601246); [Ceres, Covariance Estimation, Rank of the Jacobian (consulted on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); discriminatory tests proposed by the project; [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SVD-004 provenance::agent pole::B pole::C
END

## CV-SVD-005

Objective: Make a DLT estimate. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-005
Question: Describe direct linear transformation (DLT) estimation of a homography $H$ from $n\ge4$ point correspondences: which system is constructed, which constraint is imposed, and which vector is selected as the solution?
Reponse: **Expected answer**: each correspondence provides two homogeneous linear equations in the nine coefficients $h$ of $H$; they are stacked in $Lh=0$, with $L\in\mathbb R^{2n\times9}$. Since $H$ is only defined to one factor, $\|Lh\|$ is minimized under $\|h\|=1$, which excludes $h=0$. The solution is the right singular vector of $L$ associated with the smallest singular value, i.e. the eigenvector of $L^TL$ of smallest eigenvalue.

**Further explanation**: This algebraic cost makes no physical sense: Zhang uses it to initialize, then minimizes the Levenberg-Marquardt reprojection error. For $F$, each match gives an equation and requires at least eight; then we impose the rank 2 by canceling the smallest singular value of $F$. Normalize the coordinates before building $L$.

**Interpretation of the minimum**: norm constraint eliminates the trivial solution, but does not give a physical unit to the algebraic residual. A good linear initialization must therefore be controlled in the space where the product is used, for example with reprojection distances on reserved points.

**Explicit construction of a line**: for $(x,y)\mapsto(u,v)$, attach $h=(h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33})^T$. The projective relation gives lines $[x,y,1,0,0,0,-ux,-uy,-u]$ and $[0,0,0,x,y,1,-vx,-vy,-v]$. These constraints are stacked and then the solution vector is put back into a $3\times3$ matrix. With exactly four pairs, the matrix is $8\times9$: you have to get the full right kernel, not blindly select the last vector of a truncated factorization. The four points must provide independent constraints. An arbitrary normalization of $h_{33}$ is not possible if this component is zero or too close to zero; the homogeneous geometry allows other scaling choices.

**An invertible homography can have a zero last coefficient**: Constructed example: $H=\begin{bmatrix}1&0&1\\0&1&0\\1&0&0\end{bmatrix}$ has determinant $-1$ and $h_{33}=0$. For $x\ne0$, it maps $(x,y)$ to $((x+1)/x,y/x)$ and is a valid projective transform. An implementation that always normalizes by $h_{33}$ would reject or corrupt this solution despite its invertibility. Choose a valid homogeneous scale and check the projective denominator on the intended image region; invertible matrices can still send some finite points to infinity.

**Blocking errors**: hold the vector of the greatest singular value; solve $Lh=0$ by least squares without constraint; believe that the DLT minimizes the reprojection error.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Zhang 1998, MSR-TR-98-71, §3.2 and Annex A](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [Hartley 1997, §§2.2 – 2.3](https://doi.org/10.1109/34.601246); [Ceres, Covariance Estimation, Introduction, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::algorithme cv_id::CV-SVD-005 provenance::agent pole::B pole::C
END

## CV-SVD-006

Objective: linking standardization and conditioning of the DLT. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-006
Question: Why is DLT built from raw pixel coordinates on the order of $10^3$ poorly conditioned, and which normalization proposed by Hartley addresses this?
Reponse: **Expected answer**: a row of the matrix mixes terms of the order of 1, coordinates of the order of $10^3$ and products of the order of $10^6$; the inputs of $L^TL$ are spread over a dozen orders of magnitude and the solution vector becomes very sensitive to noise. For each image separately, translate the points to bring their centroid to the origin, then scale them isotropically for an average distance of $\sqrt2$; estimate $\hat H$ on these points, then denormalize: $H=T'^{-1}\hat HT$. Since the algebraic solution is not invariant to these transformations, normalization changes the estimator, not just the rounded ones.

**Further explanation**: Hartley measures an improved conditioning of about $10^8$ on the "house" pair. Case executed by the project: with 50 points spread over 1920×1080, $\sigma_1/\sigma_8$ Passing $8\cdot10^6$ To 4 But the error remains towards 0,2 px; with 20 points in a square of 200 px, the median error on the image is reduced from about 1000 px to 28 px. Normalization does not create the missing coverage. For $F$: $F=T'^T\hat FT$.

**Calculate the normalization**: for points $p_i=(x_i,y_i)$, calculate $c=n^{-1}\sum_i p_i$, the average distance $\bar d=n^{-1}\sum_i\|p_i-c\|_2$, then $s=\sqrt2/\bar d$ if $\bar d>0$. The homogeneous transformation has lines $(s,0,-sc_x)$, $(0,s,-sc_y)$ and $(0,0,1)$. It must be calculated separately in each image. If all the points coincide, this operation is indefinite: it is not a simple rounding problem, but an absence of usable geometry. After denormalization, compare the residuals in pixels in the original images; a residual expressed in the centered and reduced coordinates does not keep the same numerical threshold.

**Normalization is not geometric evidence**: Consider four points lying almost on one line. Centering and scaling can make their coordinate magnitudes well behaved while leaving the near-collinearity intact. Normalization addresses numerical scale; it does not restore independent projective constraints. After denormalization, assess transfer errors and the location of held-out points in the original image. A small algebraic error in normalized coordinates is insufficient when extrapolation far from the observed support changes markedly under tiny perturbations.

**Blocking errors**: forget about denormalization; present normalization as a simple rounding without effect on the solution; believe that it compensates for a bad distribution of points.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Hartley 1997, §§3 – 5 and 7.3.1](https://doi.org/10.1109/34.601246); [Zhang 1998, annexe A](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); calculation executed by the project; [Ceres, Covariance Estimation, Introduction, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SVD-006 provenance::agent pole::B pole::C
END

## CV-SVD-007

Objective: Gauss-Newton and Levenberg-Marquardt. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-007
Question: When refining calibration by minimizing nonlinear reprojection error, what does one Gauss–Newton iteration compute, how does Levenberg–Marquardt make the step safer, and what condition do both methods require?
Reponse: **Expected answer**: Gauss-Newton linearizes the residuals around the current estimate, $r(x+\delta)\approx r(x)+J\delta$, and solves the least linear square $J^TJ\delta=-J^Tr$: it approaches the Hessian by $J^TJ$, which assumes small residuals or a nearly linear model. Levenberg-Marquardt cushions the step, $(J^TJ+\lambda D^TD)\delta=-J^Tr$: $\lambda$ increases when the predicted drop in cost does not occur, which shortens the step towards the gradient descent, and otherwise decreases towards Gauss-Newton. Both are local: they require a close initialization, usually a linear solution like the DLT or Zhang's closed solution.

**Further explanation**: Ceres presents LM as a trust region of radius $\mu$, doubled if the actual drop follows the prediction and halved otherwise; $D$ is often the root of the diagonal of $J^TJ$. The system is solved as in CV-SVD-002, by QR, Cholesky or Schur. When neglected terms are not, Gauss-Newton converges much more slowly.

**Neglected by Gauss-Newton**: for $F(x)=\tfrac12\sum_i r_i(x)^2$, the exact hessian is $J^TJ+\sum_i r_i\nabla^2r_i$. Large errors or a strong curvature of the model make the second term potentially important. The damping of LM makes the step more careful, without turning the wrong projection into a good model. An iteration must compare the actual cost after update to the decline predicted by linearization, accept or decline the step, and then adjust its trusted region. Stopping only because the parameters no longer move can also mean a blocked step: check cost convergence, gradient, scales and physical validity of the solution.

**Accepted steps need model agreement**: Define the local quadratic model $m(\delta)=\tfrac12\|r+J\delta\|^2$. When its predicted reduction is positive, compare it with the actual reduction using $\eta=[F(x)-F(x+\delta)]/[m(0)-m(\delta)]$. A negative ratio means the step increased the true cost despite a favorable prediction. This constructed interpretation explains shrinking the trust region and recomputing a step. The ratio does not certify global optimality, and its denominator requires care near termination.

**Blocking errors**: Believe that LM finds the global minimum regardless of the initialization; confuse depreciation and robust loss; say that Gauss-Newton uses the exact hessian.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Triggs et al. 2000, §§4.2 – 4.3](https://inria.hal.science/inria-00548290); [Ceres, Solving Non-linear Least Squares, Trust Region Methods and Levenberg-Marquardt (accessed 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html); [Zhang 1998, §3.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf); [Ceres, Covariance Estimation, Introduction, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-SVD-007 provenance::agent pole::B pole::C
END

## CV-SVD-008

Objective: Adjust the scale of a robust loss. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-008
Question: In Ceres, a `HuberLoss(a)` or `CauchyLoss(a)` is attached to reprojection residual blocks. Which quantity does the loss act on, and how should $a$ be chosen for pixel residuals versus whitened residuals?
Reponse: **Expected answer**: $\rho$ loss applies to $s=\|f\|^2$, the square block norm of residuals; it mimics the quadratic cost for small residuals and reduces the weight of large ones. The $a$ scale has the norm unit of residual, $\rho(s,a)=a^2\rho(s/a^2)$: in pixels for residuals in pixels, in standard deviations for whitened residuals. It is chosen according to the expected noise of the inliers.

**Further explanation**: Huber remains quadratic until $\|f\|=a$ and then grows linearly; Cauchy is $a^2\log(1+s/a^2)$. The weight $\rho'(s)$ decreases in $1/\|f\|$ for Huber and in $1/\|f\|^2$ for Cauchy. Example of the project, with an insider noise of 0,5 px: $a=1$ in pixels begins to reduce the residuals beyond $2\sigma$, $a=1$ in whitened from $1\sigma$. Loss refines around an initialization: it does not replace RANSAC in front of many outliers, nor a model just when all observations are affected.

**Interpretation of weights**: in an approximation of reweighted least squares, the block $f$ receives a weight related to $\rho'(\|f\|^2)$; we therefore apply approximately $\sqrt{\rho'}$ to its components and its Jacobian. The exact solver can also take into account $\rho''$: this reasoning explains the influence without describing all its numerical corrections. For a reprojection error 2D, treat $(e_x,e_y)$ as a block together reduces the observation contribution; two separate scalar losses are another objective. After whitening, the threshold refers to a multidimensional norm: "two standard deviations" of an axis does not automatically give a probability of rejection of the entire block.

**A robust scale changes influence, not the residual unit**: For scalar residual magnitude $u$, the scaled Huber derivative with respect to $s=u^2$ is one when $|u|\le a$, then $a/|u|$. The corresponding residual influence saturates instead of growing indefinitely. A residual of $10a$ still exerts influence: it is downweighted, not deleted. For a whitened two-component residual, $a$ bounds the joint norm; interpreting it as a per-axis confidence interval would impose a different acceptance region.

**Blocking errors**: Express $a$ as a threshold on the norm squared; believe that a robust loss rejects outliers regardless of initialization.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Ceres, Modeling Non-linear Least Squares, LossFunction (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html); [Triggs et al. 2000, §3.3](https://inria.hal.science/inria-00548290); numerical example of the project; [Ceres, Covariance Estimation, Introduction, Gauge Invariance and Rank of the Jacobian](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SVD-008 provenance::agent pole::B pole::C
END

## CV-SVD-009

Objective: interpret an estimation covariance. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SVD-009
Question: After nonlinear least squares, parameter uncertainty is inferred from $(J^TJ)^{-1}$, where $J$ is the Jacobian at the solution. Under which conditions is this interpretation valid, and what does it fail to measure?
Reponse: **Expected answer**: whitened residuals, of identity covariance, and a $J$ of column rank full; the matrix obtained is then the local dispersion of the estimate, which approaches its covariance only asymptotically. If $J$ is deficient in rank (gauge, parameter not observable), $J^TJ$ is not invertible: fix the gauge, reparameterize or use a pseudo-inverse. It measures neither a model bias, like a mismodeled distortion, nor the effect of outliers: it assumes correct model and noise.

**Further explanation**: Triggs et al. find the asymptotic approximation much less safe for small geometry problems and weak networks. By default, Ceres fails on a deficient Jacobian (`Compute()` returns false); `DENSE_SVD` calculates a pseudo-inverse for small or medium problems. An almost singular Jacobian gives absurd variances, hence `min_reciprocal_condition_number`. Off-diagonal terms reveal parameters that the data do not separate (CV-ZHANG-006).

**Proposed action**: Compare the announced intervals to controlled repetitions or disturbances, keeping gauge and units. A low dispersion around a biased solution remains compatible with poor accuracy. Separate local uncertainty, variation between acquisitions and adequacy of the physical model.

**Limit of the pseudo-inverse**: undoing a singular direction to construct a pseudo-inverse does not demonstrate zero physical variance in that direction. An unfixed gauge describes a family of equivalent solutions; it is necessary to announce the coordinates or relative quantities in which an uncertainty makes sense. After a local reparameterization $y=g(x)$, the first-order propagation is $C_y\approx G C_xG^T$, $G=\partial g/\partial x$. Cross terms can then strongly influence a distance or a relative pose. Reading only the diagonal standard deviations loses these couplings. A local covariance resulting from a robust cost also requires announcing the chosen approximation convention, rather than automatically using the ordinary Gaussian formula.

**More repeated data do not remove a gauge**: For independent repeated measurements with unchanged geometry, information adds and an observable standard deviation can decrease approximately as $1/\sqrt N$. But a direction that is exactly unobservable contributes zero information in every repetition, so repetition leaves it unobservable. Likewise, a shared calibration bias is not averaged away as independent noise. This distinction separates local covariance under an assumed model from the uncertainty of deploying that model on another camera or temperature regime.

**Blocking errors**: read $(J^TJ)^{-1}$ without whitening or rank check; take a low variance for proof of model accuracy.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Full reference]]; [Ceres, Covariance Estimation, Introduction, Gauge Invariance, Rank of the Jacobian and Covariance::Options (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html); [Triggs et al. 2000, §3.1](https://inria.hal.science/inria-00548290); [Ceres, Solving Non-linear Least Squares, Linearization, Trust Region and Linear Solvers](https://ceres-solver.readthedocs.io/latest/nnls_solving.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::evaluation cv_id::CV-SVD-009 provenance::agent pole::B pole::C
END
