# Review –  registration global and local ICP –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ICP-001 | Deduction/Assumption Cases; Documentary Context Below | Concrete local loop: specifies the existing question | Finished core preserved; 193 → 297 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ICP-002 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Linearization of the residual: specifies the existing question | Finished core preserved; 192 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ICP-003 | Deduction/Assumption Cases; Documentary Context Below | Effect of the threshold on statistics: specifies the existing question | Finished core preserved; 184 → 287 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ICP-004 | Deduction/Assumption Cases; Documentary Context Below | residuals and covariance: specifies the existing question | Finished core preserved; 181 → 286 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ICP-005 | Deduction/Assumption Cases; Documentary Context Below | Where do the normals come from: specifies the existing question | Finished core preserved; 191 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ICP](../../../vault/60-vision-3d/references/62-recalage-global-icp.md); [flashcards](../../../vault/60-vision-3d/62-recalage-global-icp.md). reference note modified before the flashcards.

- **CV-ICP-001 –  Concrete local loop**: At iteration $k$, transform each source point by $T_k$, search for target neighbors, reject incompatible pairs, and then estimate a $\Delta T_k$ fix. With a correction expressed in the target coordinate frame, dial $T_{k+1}=\Delta T_kT_k$. A correction in the source coordinate frame consists of the other side: mixing these conventions produces a poor optimization trajectory. The rapprochement of the neighbors and the resolution of pose are two different steps. A good initialization facilitates physical associations, while a threshold that is too wide can accept foreign surfaces and a threshold that is too strict removes the constraints necessary for refinement.

- **CV-ICP-002 –  Linearization of the residual**: Put $s=Rp+t$ and apply a small disturbance to the left $s'\simeq s+\delta t+\delta\omega\times s$. The residual becomes $r'\simeq r+n^T\delta t+(s\times n)^T\delta\omega$. Its Jacobian is therefore a line of six components for the order translation then rotation. Stacking these lines directly shows the movements that the scene constrains. For all vertical normals, horizontal translations do not appear in this local model. This derivation assumes fixed matches and normals during the step; updating them to the next iteration makes the overall problem more complex than a single linear system.

- **CV-ICP-003 –  Effect of the threshold on statistics**: if the distances are $d_1,\ldots,d_m$, the RMSE is $\sqrt{\sum_i d_i^2/m}$. Removing all large distances can reduce it while greatly reducing $m$; the two experiments no longer focus on the same points. Also comparing the two directions source→target and target→source can reveal asymmetrical coverage, especially with different densities. An analysis by reserved physical regions prevents a dense area from dominating the score. These measurements complete the reference error of pose; they do not, on their own, remove the ambiguity of a perfectly symmetrical object.

- **CV-ICP-004 –  residuals and covariance**: if all lengths are multiplied by $a$, a metric residual becomes $r'=ar$ and its covariance becomes $\Sigma'=a^2\Sigma$. The normalized residual $r^T\Sigma^{-1}r$ then remains invariant. A robust loss set in meters also requires a converted scale, unlike a loss applied after properly processed whitening. Absolute displacement or cost tolerances can change direction with units; relative criteria must be interpreted according to their exact definition. This reasoning makes it possible to distinguish a coherent unit change from a voluntary change in physical weighting in a registration or a merger of constraints.

- **CV-ICP-005 –  Where do the normals come from**: A current local estimator centers the neighbors, calculates their covariance matrix and takes the eigenvector of smallest eigenvalue as the plane normal. A neighborhood too small becomes sensitive to noise; too large, it mixes edges and curved surfaces. If eigenvalues do not distinguish a normal direction, the local surface is itself ambiguous. For the residual point-to-plane isolated square, reversing the sign of a normal does not change the cost; a consistent orientation may nevertheless be required by other steps such as descriptors or rejection rules. Compare the quality of pose with this provenance of the explained normals.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Open3D 0.19.0](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) –  Point-to-point and Point-to-plane ICP; linearization and scale analyses of the project. View on 2026-10-30.
- [Open3D 0.19.0](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html) –  FPFH and RANSAC; no Open3D execution. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
