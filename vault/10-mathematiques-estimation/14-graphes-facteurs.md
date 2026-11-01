# Flashcards — Factor graphs and incremental optimization

reference note: [[10-mathematiques-estimation/references/14-graphes-facteurs|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FACTEURS-001

Objective: separating representation and solver. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-FACTEURS-001
Question: A factor graph is often described as a system's “SLAM.” What does it actually represent, and what must still be supplied or chosen to obtain a trajectory?
Reponse: **Expected answer**: it is a graph divided between variables (poses, bitters, bias) and factors (measurements, priors) that factorizes the density a posteriori. With Gaussian measurement models, the MAP becomes a nonlinear least square on residuals weighted by their covariance (Mahalanobis distance). It remains to provide the associations and loop closures coming from the front-end, the measurement models and their covariances, an initial estimate and an anchoring of the gauge. It is also necessary to choose the inference: batch optimization, iSAM2, robust losses.

**Further explanation**: GTSAM separates the graph from the `Values` that carry the initial estimate. The structure of the graph fixes the sparsity: in the Gaussian case, eliminating the variables is equivalent to a sparse factorization QR of the Jacobian, the cost of which depends on the order of elimination. A well-constructed graph does not make a false factor correct.

**Constructed example**: adding a distance factor does not have the same meaning as adding an absolute pose. The two connect variables according to different information and do not remove the same ambiguities. Check the contract for each factor before concluding that a graph contains "enough" constraints.

**Probability at cost**: a factorization $p(X\mid Z)\propto\prod_k\phi_k(X_k)$ becomes, per negative logarithm, a sum of local contributions. For Gaussian observations of fixed covariance $\Sigma_k$, each variable contribution is $\tfrac12 r_k^T\Sigma_k^{-1}r_k$. The factor connects only the variables $X_k$ on which its observation depends; its Jacobian therefore has null blocks elsewhere. This locality creates the sparse structure that the solver exploits. If a covariance itself depends on the parameters, its determinant no longer necessarily constitutes a constant in the likelihood: reusing the simple quadratic cost would require a justification. False associations can respect the structure of the graph while making it represent the wrong problem.

**Blocking errors**: infer a reliable path from the mere presence of a graph; confuse representation and solver.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Full reference]] ; [Dellaert, Factor Graphs and GTSAM, §§1, 2.3 – 2.4, 4.1 and 7 (accessed on 2026-10-23)](https://gtsam.org/tutorials/intro.html) ; [Kaess et al. 2012, iSAM2, §2, Gaussian Case](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FACTEURS-001 provenance::agent pole::B pole::C
END

## CV-FACTEURS-002

Objective: Explain a gauge. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FACTEURS-002
Question: Why can optimization of relative poses require an anchor despite having many observations?
Reponse: **Expected answer**: Relative observations do not necessarily define the global coordinate frame; common transformations may leave the residuals unchanged.

**Further explanation**: Attaching a gauge removes representational ambiguity, without adding an absolute measure. The number of free degrees depends on the sensors: 6 for a pose graph of relative measurements in 3D, 7 for a monocular BA, defined to a similarity, 4 in visual-inertial, where gravity makes roll and pitch observable but not the position or yaw. Three treatments exist: set these parameters, add a prior or leave the gauge free. Zhang et al. get similar precision and time, and covariances look very different but related.

**Example of Ambiguity**: Moving and rotating all poses of a relative graph together can leave the predictions between poses unchanged. The optimizer then has no reason from the measures to prefer a global origin or orientation. Fixing a first pose chooses a convenient convention; this does not turn this pose into a ground truth. Evaluating trajectories therefore implies also announcing the authorized alignment and the absolute information actually available, especially when a metric scale is expected.

**See the gauge in a constraint**: for poses camera→world $T_i$, the relative prediction is $T_i^{-1}T_j$. Transforming all the poses by the same $G$ gives $(GT_i)^{-1}(GT_j)=T_i^{-1}T_j$. The cost cannot therefore choose $G$ from these measurements alone. The gauge results in zero directions of the linearized system, distinct from a simple wrong precision on an observed direction. Fixing a pose eliminates this freedom; a finite covariance prior adds announced information that can influence the solution. In a VIO, theoretical freedoms assume appropriate excitation and pattern: degenerate movements can leave other parameters little or not observable.

**Blocking errors**: Interpret an arbitrary prior as evidence of global accuracy.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Full reference]]; [Ceres, Covariance Estimation, Gauge Invariance (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance); [Zhang, Gallego and Scaramuzza 2018, RA-L, summary, §I and table I](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf); 6 degrees of the pose graph deduced by the project; [GTSAM, Factor Graphs, §§2.3 – 2.4, graph, Values and optimization](https://gtsam.org/tutorials/intro.html); [Kaess et al. 2012, iSAM2, §§3 – 4, elimination and relinearization](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf), consult the 2026-10-30.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FACTEURS-002 provenance::agent pole::B pole::C
END

## CV-FACTEURS-003

Objective: Check for a loop closure. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FACTEURS-003
Question: After loop closure, the cost decreases but the map bends inconsistently. What should be tested?
Reponse: **Expected answer**: Check the combination of places, relative transformation, coordinate frames and the weight of the loop factor.

**Further explanation**: A strong false constraint can be satisfied at the expense of the rest. Encrypted test: after optimization, compare the residual Bleached Square $\chi^2_l$ the quantile of the loop factor $\chi^2$ of its size, 6 for one pose relative 3D, and look at the rise in residuals odometry neighbors. After adjustment on the same measurements, this threshold is a heuristic: the residual depends on the estimate and correlations, its covariance is not simply that of the measurement. A calibrated $\chi^2_6$ law requires an appropriate residual model; do not automatically assign it a false rejection rate. Re-optimize without this breaking factor: if the map recovers, the loop is suspect. Keep geometric verification and independent observations; a robust back-end is processed in CV-FACTEURS-004.

**Constructed ablation**: keep all other factors and compare with and without the suspicious loop. Examine the effect on neighbouring observations and on a reserved reference. A decrease in the total cost may simply reflect the overemphasis on the new factor; it does not establish its physical validity.

**residual from pose to be defined**: If $Z_{ij}$ is a measurement of $T_i^{-1}T_j$, a possible residual is $r_{ij}=\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, a tangent vector with six components in an announced order convention. Translation in meters and rotation in radians require consistent covariance and whitening. Invert only the measurement without adapting direction, coordinate frame and covariance changes the factor. After optimization, this residual depends on the poses it has itself moved; its small value can therefore hide a loop that has distorted the entire graph. Examine the other factors affected and an external reference, not just the error of the added loop.

**Blocking errors**: Increase iterations without inspecting the added factor.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Full reference]]; [Dellaert, Factor Graphs and GTSAM, §§2.3 – 2.4, 4.1 and 7 (accessed on 2026-10-23)](https://gtsam.org/tutorials/intro.html); [Agarwal et al. 2013, DCS, §III, equation 1](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf); fake factor scenario and tests proposed by the project; [Kaess et al. 2012, iSAM2, §§3 – 4, elimination and relinearization](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf), consult the 2026-10-30.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FACTEURS-003 provenance::agent pole::B pole::C
END

## CV-FACTEURS-004

Objective: Choose a robust back-end to fake loops. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FACTEURS-004
Question: A place-recognition front end inevitably produces some false loop closures, for example in identical corridors. Which back-end strategies should be compared to prevent map distortion, and how should one be chosen?
Reponse: **Expected answer**: Robust loss on loop factors reduces the weight of large residuals; it is simple, but sensitive to initialization and chosen scale. Switchable constraints add a $s_{ij}\in[0,1]$ variable per loop, optimized with the map and recalled to 1 by a prior: they disable inconsistent loops, at the price of more variables and slower convergence. DCS calculates this weight in close form, $s=\min\left(1,\frac{2\Phi}{\Phi+\chi^2_l}\right)$, based on the current loop error $\chi^2_l$: same idea, no variables added and with faster convergence. Choose according to the expected false loop rate, calculation budget and the need for an explicit decision.

**Further explanation**: DCS scales the information matrix of each loop by $s^2$; $\Phi$ sets the tolerance. These methods keep a rejected loop with a low weight; RRR instead looks for the largest set of mutually consistent loops and rejects the others. Reasoning the project: none compensates a front-end whose false loops are numerous and consistent with each other.

**Example of weight DCS built**: with $\Phi=1$ and a squared blanked error $\chi_l^2=9$, the formula gives $s=0,2$ and information multiplied by $s^2=0,04$. This is neither a probability that the loop is true nor a binary deletion: an erroneous constraint can still exert a force on the optimum. The weight should be recalculated with the current solution in the chosen scheme. A real loop initially very far away can be weakened, while a false loop compatible with an already deformed map can retain weight. The evaluation must therefore separate acceptance of real loops, resistance to fakes and behavior according to the initialization.

**Blocking errors**: believing that a robust back-end makes front-end geometric verification unnecessary; reducing DCS to a binary threshold.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Full reference]]; [Agarwal et al. 2013, Robust Map Optimization using Dynamic Covariance Scaling, summary, §§II – IV, equations 2 and 15](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf); switchable constraints of Sünderhauf and Protzel 2012 read through their presentation by Agarwal et al.
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-FACTEURS-004 provenance::agent pole::B pole::C
END

## CV-FACTEURS-005

Objective: explain the incremental update of iSAM2. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-FACTEURS-005
Question: When new measurements arrive, what does iSAM2 actually recompute in its Bayes tree, and which two thresholds limit relinearization and estimate updates?
Reponse: **Expected answer**: Only cliques on paths between variables affected by new factors or selected for relinearization and root are removed, reordered, and re-eliminated with these factors; unaffected subtrees are reinserted as is. Fluid relinearization: A variable is only relinearized if its estimated deviation from its linearization point exceeds a $\beta$ threshold. Partial update: the back-substitution stops in subtrees where the changes remain below a $\alpha$ threshold.

**Further explanation**: the order of the variables of the affected part is recalculated at each update, with a quality close to a COLAMD  batch, to limit the filling. A large loop closure affects a large part of the tree: incremental does not mean constant cost. On Manhattan, $\beta=0{,}1$ gives an almost exact solution at a significantly reduced cost; the thresholds exchange precision and calculation.

**Product consequence**: measure latency peaks by adding significant constraints, not just the straight-line average. A small usual update and a large loop closure do not necessarily touch the same portion of the system. The budget must provide for this variability and compromise of thresholds.

**Why the elimination order matters**: Removing a variable transmits a constraint between the variables that remained related to it. These extra links fill in the triangular factors; their structure determines the size of the cliques and the paths affected by an update. A long loop can make a lot of constraints coupled without adding a lot of variables. The incremental reuses the work compatible with the new information, but cannot ignore the dependencies actually created. Relinearization thresholds refer to increments of different types: meters, radians or other parameters must have consistent tolerances. A single number without scaling convention does not represent the same accuracy for each state.

**Blocking errors**: to believe that iSAM2 never re-linearizes or repeats everything at every step; to promise a constant cost per measure.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Full reference]]; [Kaess et al. 2012, iSAM2, §3.3, algorithm 4, §3.4 and §§4.1 – 4.2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf); [GTSAM, Factor Graphs, §§2.3 – 2.4, graph, Values and optimization](https://gtsam.org/tutorials/intro.html), see 2026-10-30.
Tags: cv::pilote cv::d01 famille::algorithme cv_id::CV-FACTEURS-005 provenance::agent pole::B pole::C
END
