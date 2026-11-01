# Review –  Bundle adjustment and complement of Schur –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BA-001 | Deduction/Assumption Cases; Documentary Context Below | Complete objective to be explained: specifies the existing question | Finished core preserved; 190 → 309 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BA-002 | Deduction/Assumption Cases; Documentary Context Below | derivation of the reduced system: specifies the existing question | Finished core preserved; 188 → 311 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BA-003 | Deduction/Assumption Cases; Documentary Context Below | Proof of free scale: specifies the existing question | Finished core preserved; 198 → 310 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BA-004 | Deduction/Assumption Cases; Documentary Context Below | Example of missing information: specifies the existing question | Finished core preserved; 181 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-BA](../../../vault/50-calibration-geometrie/references/54-bundle-adjustment.md); [flashcards](../../../vault/50-calibration-geometrie/54-bundle-adjustment.md). reference note modified before the flashcards.

- **CV-BA-001 –  Complete objective to be explained**: On the $\mathcal O$ set of observations actually present, a BA can minimize $\sum_{(i,j)\in\mathcal O}\rho(\|L_{ij}^{-1}[\pi(K_i,T_i,X_j)-z_{ij}]\|_2^2)$, with $z_{ij}$ in pixels, $X_j$ a world point, $T_i$ a pose and $L_{ij}L_{ij}^T$ its measurement covariance. The projection function includes the expected distortion. The poses must be updated to its appropriate parameterization; the parameters set are not unknown to the solver. Points seen in a single image may lack depth constraint. Thus, the total number of observations alone does not describe the connectivity and observability of the reconstruction.

- **Reduced System CV-BA-002 –  derivation**: Linearized problem gives $B\delta_c+E\delta_p=v$ and $E^T\delta_c+C\delta_p=w$. If $C$ is invertible, the second equation provides $\delta_p=C^{-1}(w-E^T\delta_c)$; its substitution in the first $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$ product. In a classic BA where each residual connects a camera and a point, the points do not interact directly with each other in this block: $C$ is diagonal block per point. A point seen by many cameras, on the other hand, creates couplings in the reduced system. Point – point constraints or other factors can change this structure; the factorization of the problem should be checked instead of assuming Schur to be always the same.

- **CV-BA-003 –  Proof of free scale**: with an ideal projection of $RX+t$, replace $X$ with $aX$ and $t$ with $at$, $a>0$, multiplies the three camera coordinates by $a$; the homogeneous division removes this factor. Monocular observations therefore do not distinguish these scales. A very strong digital prior on a translation can make the system invertible without this value being measured. If the system is to be metric, use a known length or source of motion and announce its uncertainty. A visual-inertial optimization can resolve scale ambiguity under the conditions of its model; it can also become ill-conditioned if the movements do not sufficiently excite the necessary variables.

- **CV-BA-004 –  Example of missing information**: In a polynomial radial model, the effects of high-order coefficients grow with normalized radius powers. Observations near the center can hardly constrain these terms; different values then produce almost the same pixels observed but diverge at the edge. Unleashing these coefficients increases flexibility without adding informative data. The damping of LM limits the current resolution pitch: it is not automatically a physical priority on the final parameters. Justify the free parameters, check the directions with little stress and test the geometry where it will be used. A reserved validation must keep poses and really different areas, not just neighboring points of the same catches.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Ceres, Solving Non-linear Least Squares](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) –  Schur complement trick and block systems. View on 2026-10-30.
- [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) –  Gauge Invariance and rank of Jacobian. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
