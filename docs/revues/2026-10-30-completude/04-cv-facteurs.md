# Review –  Factor Graphs and Incremental Optimization –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 6 to 7, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Deduction/Assumption Cases; Documentary Context Below | Probability at cost: specifies the existing question | Finished core preserved; 208 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FACTEURS-002 | Deduction/Assumption Cases; Documentary Context Below | See the gauge in a constraint: specifies the existing question | Finished core preserved; 206 → 318 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FACTEURS-003 | Deduction/Assumption Cases; Documentary Context Below | residual of pose to be defined: specifies the existing question | Finished core preserved; 211 → 320 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FACTEURS-004 | Deduction/Assumption Cases; Documentary Context Below | Example of weight DCS built: specifies the existing question | Finished core preserved; 215 → 327 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FACTEURS-005 | Deduction/Assumption Cases; Documentary Context Below | Why the elimination order matters: specifies the existing question | Finished core preserved; 228 → 344 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FACTEURS](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md); [flashcards](../../../vault/10-mathematiques-estimation/14-graphes-facteurs.md). reference note modified before the flashcards.

- **CV-FACTEURS-001 –  From probability to cost**: a factorization $p(X\mid Z)\propto\prod_k\phi_k(X_k)$ becomes, per negative logarithm, a sum of local contributions. For Gaussian observations of fixed covariance $\Sigma_k$, each variable contribution is $\tfrac12 r_k^T\Sigma_k^{-1}r_k$. The factor connects only the variables $X_k$ on which its observation depends; its Jacobian therefore has null blocks elsewhere. This locality creates the sparse structure that the solver exploits. If a covariance itself depends on the parameters, its determinant no longer necessarily constitutes a constant in the likelihood: reusing the simple quadratic cost would require a justification. False associations can respect the structure of the graph while making it represent the wrong problem.

- **CV-FACTEURS-002 –  See the gauge in a constraint**: for poses camera→world $T_i$, the relative prediction is $T_i^{-1}T_j$. Transforming all the poses by the same $G$ gives $(GT_i)^{-1}(GT_j)=T_i^{-1}T_j$. The cost cannot therefore choose $G$ from these measurements alone. The gauge results in zero directions of the linearized system, distinct from a simple wrong precision on an observed direction. Fixing a pose eliminates this freedom; a finite covariance prior adds announced information that can influence the solution. In a VIO, theoretical freedoms assume appropriate excitation and pattern: degenerate movements can leave other parameters little or not observable.

- **CV-FACTEURS-003 –  residual of pose to be defined**: If $Z_{ij}$ is a measurement of $T_i^{-1}T_j$, a possible residual is $r_{ij}=\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, a tangent vector with six components in an announced order convention. Translation in meters and rotation in radians require consistent covariance and whitening. Invert only the measurement without adapting direction, coordinate frame and covariance changes the factor. After optimization, this residual depends on the poses it has itself moved; its small value can therefore hide a loop that has distorted the entire graph. Examine the other factors affected and an external reference, not just the error of the added loop.

- **CV-FACTEURS-004 –  Example of weight DCS built**: with $\Phi=1$ and a squared blanked error $\chi_l^2=9$, the formula gives $s=0,2$ and information multiplied by $s^2=0,04$. This is neither a probability that the loop is true nor a binary deletion: an erroneous constraint can still exert a force on the optimum. The weight should be recalculated with the current solution in the chosen scheme. A real loop initially very far away can be weakened, while a false loop compatible with an already deformed flashcard can retain weight. The evaluation must therefore separate acceptance of real loops, resistance to fakes and behavior according to the initialization.

- **CV-FACTEURS-005 –  Why the elimination order matters**: Removing a variable transmits a constraint between the variables that remained related to it. These extra links fill in the triangular factors; their structure determines the size of the cliques and the paths affected by an update. A long loop can make a lot of constraints coupled without adding a lot of variables. The incremental reuses the work compatible with the new information, but cannot ignore the dependencies actually created. Relinearization thresholds refer to increments of different types: meters, radians or other parameters must have consistent tolerances. A single number without scaling convention does not represent the same accuracy for each state.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [GTSAM, Factor Graphs](https://gtsam.org/tutorials/intro.html) –  §§2.3 – 2.4, graph, Values and optimization. View on 2026-10-30.
- [Kaess et al. 2012, iSAM2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf) –  §§3 – 4, elimination and relinearization. View on 2026-10-30.
- [Agarwal et al. 2013, DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) –  §§III – IV, equations 2 and 15. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
