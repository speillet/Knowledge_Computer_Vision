---
id: CV-FACTEURS
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 9
prerequis: ["CV-SVD", "CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Factor graphs and incremental optimization

## Problem, data and assumptions

Representing poses, speeds, biases and observations as an inference problem. Inputs: states, factors, covariance and initialization; output: joint estimation. A factor graph describes a factorization, not an optimizer by itself.

## Prerequisites and competencies

**Required prerequisites**: [CV-SVD](11-moindres-carres-svd.md); [CV-SE3](12-rotations-se3.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

A factor graph is a bipartite graph between factors and variables; it factorizes a function, typically a posteriori density (GTSAM, §1; Kaess et al. 2012, §2). Each factor connects the variables needed for an observation; a solver linearizes and optimizes. GTSAM separates the graph from the `Values`, which carries the initial estimate of the MAP (§§2.3 – 2.4). In a pose graph, the prior on the first pose is the only factor that ties the graph to a global coordinate frame (§4.1). GTSAM provides these abstractions and iSAM2 an incremental strategy with selective relinearization (§7). It remains to provide the front-end loop associations and closures, models and covariances, initialization and gauge. A false buckle closure can distort the entire graph.

## Mathematics, conventions and units

For conditionally independent Gaussian factors, with positive definite fixed covariances, a MAP form is $\min_x\sum_k\|r_k(x_k)\|^2_{\Sigma_k^{-1}}$. $x_k$ groups the variables of the factor; the residual is whitened by its covariance. A prior or convention sets the global gauges; a solver does not invent an absolute reference absent from the measurements. Gauge size: 7 for a monocular BA, defined only up to a similarity transform (Ceres, Gauge Invariance; Zhang et al. 2018, §I), 4 in visual-inertial, the position and the yaw not being observable (Zhang et al. 2018, summary). For a pose graph of relative measurements in 3D, the 6 degrees of a common rigid transformation are free, deduction of the project consistent with GTSAM §4.1. Zhang et al. compare three treatments: setting parameters, adding a prior, leaving the gauge free with a pseudo-inverse (Table I). They find similar precision and time, the free gauge being a little faster, and covariances of very different appearance but connected.

## Parameters and properties

Choose factors, robust losses, priors, marginalized variables, and thresholds for relinearization. Marginalizing creates correlated constraints; this does not mean deleting information from past states without effect.

## Cost and implementation

Sparsity and elimination order change time/memory. In the Gaussian case, the elimination of the variables is equivalent to a sparse factorization QR of the measurement Jacobian (Kaess et al. 2012, §2, Gaussian Case). A bad order creates fill-in; iSAM2 incrementally reorders the affected part, with results close to a COLAMD  batch (§3.4). Incremental does not mean constant cost. No GTSAM calls are executed; the notions are conceptual and related to the BA.

update of iSAM2 (Kaess et al. 2012). A new factor affects only the paths between the cliques of its variables and the root (§3.3). The 4 algorithm removes these cliques, adds new factors, reorders, eliminates, and then reinserts orphaned subtrees. The relinearized variables also cause their cliques and ancestors to be recalculated (algorithms 5 – 6), even without a new factor on them. Fluid relinearization only relinearizes a variable if its deviation at the point of linearization exceeds a threshold $\beta$ (§4.1); on Manhattan, $\beta=0{,}1$ gives an almost exact solution for a significantly reduced cost. The partial update stops the retro-substitution in subtrees whose change remains below a threshold $\alpha$ (§4.2). A large loop affects a large part of the tree.

## Evaluation and controlled variation

Constructed case: add a correct loop constraint and then a false one. Predict drift reduction in the first case and possible deformation in the second; inspect residuals by factor and reserved reference, not only convergence of the solver.

## Failure modes and diagnosis

A solver converges with an absurd trajectory: check coordinate frames, information about priors, associations and inconsistent factors; a stricter tolerance is not a diagnosis.

False loop closures. Perceptual aliasing makes a front-end without false positives unrealistic (Agarwal et al. 2013, §II). Heuristic test of the project: follow the weighted residual $\chi^2_l$ of the loop factor. After optimization on the same measurements, its distribution depends on the adjustment and correlations; a quantile $\chi^2$ of dimension 6 does not automatically provide a calibrated false rejection rate. To diagnose, look at the rise of neighboring residuals odometry, and then re-optimize without this factor. Robust back-ends:

- robust loss on loops (CV-SVD-008);
- switchable constraints of Sünderhauf and Protzel: one variable $s_{ij}\in[0,1]$ per loop, with a prior that reminds it to 1;
- DCS, which gives the value in close form, $s=\min(1, 2\Phi/(\Phi+\chi^2_l))$, and scales the loop information by $s^2$ without additional variables (§IV, equation 15);
- RRR, which rejects the loops out of the larger coherent set instead of keeping them with a low weight (§II).

## Alternatives and applications

pose graph for stresses between poses, BA for poses and observed marks; filter for current state. Compare memory, re-estimation and latency.

## Guided reasoning and proposed checks

These constructed cases develop graph, gauge and cost of an elimination. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FACTEURS-001

**Question of work**: A factor graph is often described as a system's “SLAM.” What does it actually represent, and what must still be supplied or chosen to obtain a trajectory?

**Reference Response**: it is a graph divided between variables (poses, bitters, bias) and factors (measurements, priors) that factorizes the density a posteriori. With Gaussian measurement models, the MAP becomes a nonlinear least square on residuals weighted by their covariance (Mahalanobis distance). It remains to provide the associations and loop closures coming from the front-end, the measurement models and their covariances, an initial estimate and an anchoring of the gauge. It is also necessary to choose the inference: batch optimization, iSAM2, robust losses.

**Constructed example**: adding a distance factor does not have the same meaning as adding an absolute pose. The two connect variables according to different information and do not remove the same ambiguities. Check the contract for each factor before concluding that a graph contains "enough" constraints.

### Case linked to CV-FACTEURS-005

**Question of work**: When new measurements arrive, what does iSAM2 actually recompute in its Bayes tree, and which two thresholds limit relinearization and estimate updates?

**Reference Response**: Only cliques on paths between variables affected by new factors or selected for relinearization and root are removed, reordered, and re-eliminated with these factors; unaffected subtrees are reinserted as is. Fluid relinearization: A variable is only relinearized if its estimated deviation from its linearization point exceeds a $\beta$ threshold. Partial update: the back-substitution stops in subtrees where the changes remain below a $\alpha$ threshold.

**Product consequence**: measure latency peaks by adding significant constraints, not just the straight-line average. A small usual update and a large loop closure do not necessarily touch the same portion of the system. The budget must provide for this variability and compromise of thresholds.

**Documentary reference for this pass**: [GTSAM, Introduction](https://gtsam.org/tutorials/intro.html), factor graph, Values and prior. The other developments are in the [flashcards](../14-graphes-facteurs.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FACTEURS-001

**Situation**: A factor graph is often described as a system's “SLAM.” What does it actually represent, and what must still be supplied or chosen to obtain a trajectory?

**Probability at cost**: a factorization $p(X\mid Z)\propto\prod_k\phi_k(X_k)$ becomes, per negative logarithm, a sum of local contributions. For Gaussian observations of fixed covariance $\Sigma_k$, each variable contribution is $\tfrac12 r_k^T\Sigma_k^{-1}r_k$. The factor connects only the variables $X_k$ on which its observation depends; its Jacobian therefore has null blocks elsewhere. This locality creates the sparse structure that the solver exploits. If a covariance itself depends on the parameters, its determinant no longer necessarily constitutes a constant in the likelihood: reusing the simple quadratic cost would require a justification. False associations can respect the structure of the graph while making it represent the wrong problem.

### CV-FACTEURS-002

**Situation**: Why can optimization of relative poses require an anchor despite having many observations?

**See the gauge in a constraint**: for poses camera→world $T_i$, the relative prediction is $T_i^{-1}T_j$. Transforming all the poses by the same $G$ gives $(GT_i)^{-1}(GT_j)=T_i^{-1}T_j$. The cost cannot therefore choose $G$ from these measurements alone. The gauge results in zero directions of the linearized system, distinct from a simple wrong precision on an observed direction. Fixing a pose eliminates this freedom; a finite covariance prior adds announced information that can influence the solution. In a VIO, theoretical freedoms assume appropriate excitation and pattern: degenerate movements can leave other parameters little or not observable.

### CV-FACTEURS-003

**Situation**: After loop closure, the cost decreases but the map bends inconsistently. What should be tested?

**residual from pose to be defined**: If $Z_{ij}$ is a measurement of $T_i^{-1}T_j$, a possible residual is $r_{ij}=\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, a tangent vector with six components in an announced order convention. Translation in meters and rotation in radians require consistent covariance and whitening. Invert only the measurement without adapting direction, coordinate frame and covariance changes the factor. After optimization, this residual depends on the poses it has itself moved; its small value can therefore hide a loop that has distorted the entire graph. Examine the other factors affected and an external reference, not just the error of the added loop.

### CV-FACTEURS-004

**Situation**: A place-recognition front end inevitably produces some false loop closures, for example in identical corridors. Which back-end strategies should be compared to prevent map distortion, and how should one be chosen?

**Example of weight DCS built**: with $\Phi=1$ and a squared blanked error $\chi_l^2=9$, the formula gives $s=0,2$ and information multiplied by $s^2=0,04$. This is neither a probability that the loop is true nor a binary deletion: an erroneous constraint can still exert a force on the optimum. The weight should be recalculated with the current solution in the chosen scheme. A real loop initially very far away can be weakened, while a false loop compatible with an already deformed map can retain weight. The evaluation must therefore separate acceptance of real loops, resistance to fakes and behavior according to the initialization.

### CV-FACTEURS-005

**Situation**: When new measurements arrive, what does iSAM2 actually recompute in its Bayes tree, and which two thresholds limit relinearization and estimate updates?

**Why the elimination order matters**: Removing a variable transmits a constraint between the variables that remained related to it. These extra links fill in the triangular factors; their structure determines the size of the cliques and the paths affected by an update. A long loop can make a lot of constraints coupled without adding a lot of variables. The incremental reuses the work compatible with the new information, but cannot ignore the dependencies actually created. Relinearization thresholds refer to increments of different types: meters, radians or other parameters must have consistent tolerances. A single number without scaling convention does not represent the same accuracy for each state.

**Passages consulted for these developments** : [GTSAM, Factor Graphs](https://gtsam.org/tutorials/intro.html), §§2.3–2.4, graph, Values and optimization; [Kaess et al. 2012, iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf), §§3–4, elimination and relinearization; [Agarwal et al. 2013, DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf), §§III – IV, equations 2 and 15.

## Sources and flashcards

- [Ceres, Covariance Estimation, Gauge Invariance (accessed on 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance).

- [Dellaert, Factor Graphs and GTSAM, §§1, 2.3 – 2.4, 4.1 and 7 (accessed on 2026-10-23)](https://gtsam.org/tutorials/intro.html): bipartite definition, `Values`, first pose, iSAM and Bayes tree. The page does not explicitly say that the Gaussian MAP is a least square: this equivalence is sourced by Kaess et al.
- [Kaess et al. 2012, iSAM2, §2 Gaussian Case, §3.4 and §§4.1 – 4.2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf): non-linear least squares, elimination by sparse QR, incremental order, fluid relinearization and partial updates.
- [Zhang, Gallego and Scaramuzza 2018, On the Comparison of Gauge Freedom Handling in Optimization-based Visual-Inertial State Estimation, RA-L](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf): prepublication of authors; summary, §I and table I.
- [Agarwal, Tipaldi, Spinello, Stachniss and Burgard 2013, Robust Map Optimization using Dynamic Covariance Scaling, ICRA](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf): §II related works including RRR, §III switchable constraints, §IV equation 15. The article by Sünderhauf and Protzel 2012 has not been read directly.
- [Related flashcards](../14-graphes-facteurs.md): CV-FACTEURS-001 to 005.

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation.
