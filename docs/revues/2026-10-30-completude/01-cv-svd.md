# Review –  Smaller squares, SVD and packaging –  2026-10-30

## Overview

9 enriched flashcards; reference note scope of revision 5 to 6, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | Deduction/Assumption Cases; Documentary Context Below | Reading subspaces: specifies the existing question | Finished core preserved; 184 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-002 | Deduction/Assumption Cases; Documentary Context Below | What QR does: clarifies the existing question | Finished core preserved; 217 → 334 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-003 | Deduction/Assumption Cases; Documentary Context Below | Why unit invariance works: clarifies the existing question | Finished core preserved; 213 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-004 | Deduction/Assumption Cases; Documentary Context Below | What spectrum to look at: specifies the existing question | Finished core preserved; 220 → 332 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-005 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Explicit construction of a line: specifies the existing question | Finished core preserved; 217 → 348 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-006 | Deduction/Assumption Cases; Documentary Context Below | Calculating normalization: specifies the existing question | Finished core preserved; 223 → 333 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-007 | Deduction/Assumption Cases; Documentary Context Below | Term neglected by Gauss-Newton: clarifies the existing question | Finished core preserved; 204 → 315 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-008 | Deduction/Assumption Cases; Documentary Context Below | Interpretation of weights: specifies the existing question | Finished core preserved; 200 → 307 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SVD-009 | Deduction/Assumption Cases; Documentary Context Below | Limit of the pseudo-inverse: specifies the existing question | Finished core preserved; 221 → 342 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SVD](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md); [flashcards](../../../vault/10-mathematiques-estimation/11-moindres-carres-svd.md). reference note modified before the flashcards.

- **CV-SVD-001 –  Reading subspaces**: For $m\ge n$ and a full column rank, $\hat b=A\hat x=UU^Tb$ is the projection of $b$ on the column space, while the orthogonal residual is $(I-UU^T)b$. A disturbance in this space can strongly change $\hat x$ without increasing this residual. This is precisely why the diagnosis must examine both fit and sensitivity. If a singular value is exactly zero, some components are no longer determined by observations: the pseudo-inverse chooses a solution of minimum norm, without establishing that this solution is physically true. These equalities are deductions from the SVD, with $U$ containing the singular observable columns.

- **CV-SVD-002 –  What QR does**: with the reduced factorization $A=QR$, $Q^TQ=I$ and upper triangular $R$, we project $b$ into $Q^Tb$ and then solve $R\hat x=Q^Tb$ by substitution. Orthogonal transformations preserve norms and avoid forming column products of $A^TA$. The SVD replaces this triangle with singular directions and allows a low numerical rank to be explicitly processed. In a dense problem with $m\gg n$, costs depend mostly on $mn^2$ at different constants; in a sparse system, factor filling and elimination order can become decisive. Comparing only the dimensions of the system is therefore not enough to predict time and memory.

- **CV-SVD-003 –  Why Unit Invariance Works**: For invertible linear transformation of $r'=Dr$ units, the correct covariance becomes $C'=DCD^T$. Then $r'^TC'^{-1}r'=r^TC^{-1}r$. Changing the residuals without changing their covariance breaks this invariance. Whitening by Cholesky is calculated by solving $Lz=r$, rather than materializing $L^{-1}$. If two errors come from the same detection or sensor, correlations can make their naïve addition overconfident. They must be modelled or independence announced as an approximation; a robust loss does not repair this double counting. The quadratic form is dimensionless, but the final covariances of the parameters retain their own units.

- **CV-SVD-004 –  What spectrum to examine**: for a homogeneous system with nine parameters whose scale is arbitrary, we expect a single solution direction. If the points are quite numerous, a second direction almost zero means that several transformations explain almost as much of the data. The ratio between the last singular values informs this separation; for the minimum eight-line system, the exact kernel must also be taken into account, because a reduced SVD may not return its vector. These diagnoses are specific to the model and its normalization: always using the same spectral threshold on arbitrary units would be misleading. A spot test then examines the geometric effect of this ambiguity.

- **CV-SVD-005 –  Explicit construction of a line**: for $(x,y)\mapsto(u,v)$, attach $h=(h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33})^T$. The projective relation gives lines $[x,y,1,0,0,0,-ux,-uy,-u]$ and $[0,0,0,x,y,1,-vx,-vy,-v]$. These constraints are stacked and then the solution vector is put back into a $3\times3$ matrix. With exactly four pairs, the matrix is $8\times9$: you have to get the full right kernel, not blindly select the last vector of a truncated factorization. The four points must provide independent constraints. An arbitrary normalization of $h_{33}$ is not possible if this component is zero or too close to zero; the homogeneous geometry allows other scaling choices.

- **CV-SVD-006 –  Calculate normalization**: for points $p_i=(x_i,y_i)$, calculate $c=n^{-1}\sum_i p_i$, the average distance $\bar d=n^{-1}\sum_i\|p_i-c\|_2$, then $s=\sqrt2/\bar d$ if $\bar d>0$. The homogeneous transformation has lines $(s,0,-sc_x)$, $(0,s,-sc_y)$ and $(0,0,1)$. It must be calculated separately in each image. If all the points coincide, this operation is indefinite: it is not a simple rounding problem, but an absence of usable geometry. After denormalization, compare the residuals in pixels in the original images; a residual expressed in the centered and reduced coordinates does not keep the same numerical threshold.

- **CV-SVD-007 –  Term neglected by Gauss-Newton**: for $F(x)=\tfrac12\sum_i r_i(x)^2$, the exact hessian is $J^TJ+\sum_i r_i\nabla^2r_i$. Large errors or a strong curvature of the model make the second term potentially important. The damping of LM makes the step more careful, without turning the wrong projection into a good model. An iteration must compare the actual cost after update to the decline predicted by linearization, accept or decline the step, and then adjust its trusted region. Stopping only because the parameters no longer move can also mean a blocked step: check cost convergence, gradient, scales and physical validity of the solution.

- **CV-SVD-008 –  Interpretation of weights**: in an approximation of reweighted least squares, the block $f$ receives a weight related to $\rho'(\|f\|^2)$; we therefore apply approximately $\sqrt{\rho'}$ to its components and its Jacobian. The exact solver can also take into account $\rho''$: this reasoning explains the influence without describing all its numerical corrections. For a reprojection error 2D, treat $(e_x,e_y)$ as a block together reduces the observation contribution; two separate scalar losses are another objective. After whitening, the threshold refers to a multidimensional norm: "two standard deviations" of an axis does not automatically give a probability of rejection of the entire block.

- **CV-SVD-009 –  Limit of pseudo-inverse**: undoing a singular direction to construct a pseudo-inverse does not demonstrate zero physical variance in that direction. An unfixed gauge describes a family of equivalent solutions; it is necessary to announce the coordinates or relative quantities in which an uncertainty makes sense. After a local reparameterization $y=g(x)$, the first-order propagation is $C_y\approx G C_xG^T$, $G=\partial g/\partial x$. Cross terms can then strongly influence a distance or a relative pose. Reading only the diagonal standard deviations loses these couplings. A local covariance resulting from a robust cost also requires announcing the chosen approximation convention, rather than automatically using the ordinary Gaussian formula.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) –  Introduction, Gauge Invariance and Rank of the Jacobian. View on 2026-10-30.
- [Ceres, Solving Non-linear Least Squares](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) –  linearization, Trust Region and Linear Solvers. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
