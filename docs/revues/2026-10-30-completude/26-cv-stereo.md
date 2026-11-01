# Review –  Corrected stereo, SGM and depth –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Construction of triangles: specifies the existing question | Finished core preserved; 195 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-STEREO-002 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Propagation of several uncertainties: specifies the existing question | Finished core preserved; 189 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-STEREO-003 | Deduction/Assumption Cases; Documentary Context Below | Order of operations: specifies the existing question | Finished core preserved; 180 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-STEREO-004 | Deduction/Assumption Cases; Documentary Context Below | Constructed bidirectional verification: specifies the existing question | Finished core preserved; 194 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-STEREO](../../../vault/60-vision-3d/references/61-stereo-profondeur.md); [flashcards](../../../vault/60-vision-3d/61-stereo-profondeur.md). reference note modified before the flashcards.

- **CV-STEREO-001 –  Construction of triangles**: With horizontally separated centers of $B$, even focal length and even main abscissa $c_x$, the ideal projections are $x_g=fX/Z+c_x$ and $x_d=f(X-B)/Z+c_x$. The subtraction eliminates $X$ and gives $d=fB/Z$. If the main abscissas differ, it is $d-(c_{x,g}-c_{x,d})$ that enters into this simplified geometry. This derivation explains why using the corresponding rectified image/reprojection matrix torque is essential. The result $Z$ is the depth along the rectified optical axis; the Euclidean distance to the camera center is $\sqrt{X^2+Y^2+Z^2}$ and can be greater for an off-axis point.

- **CV-STEREO-002 –  Spread of several uncertainties**: for $Z=fB/d$ and small disturbances, $\delta Z/Z\simeq\delta f/f+\delta B/B-\delta d/d$. If these errors are independent and centered, the relative variances add up; otherwise their covariances count. A baseline bias thus produces a relative error of scale, while a fixed disparity bias further penalizes long distances. Almost $d=0$, linearization becomes fragile and a symmetrical distribution in disparity gives a very asymmetrical distribution in depth. Also evaluate the intervals in depth or use a depth inverse representation according to the estimator, instead of assuming constant Gaussian metric uncertainty.

- **CV-STEREO-003 –  Order of Operations**: Conceptually, retain the mask provided by the matcher's contract, convert the fixed disparity to real, then apply $[X_h,Y_h,Z_h,W_h]^T=Q[x,y,d,1]^T$ and divide by $W_h$ when the projection is valid. These are homogeneous coordinates, not yet meters before this division and the interpretation of the units of $Q$. Do not build the mask only after filling the holes: an interpolation can replace a sentinel with a plausible value. Keep the original measurement, its validity and any depth completed separate. Testing a known pixel makes it possible to distinguish storage factor, disparity convention, and baseline unit.

- **CV-STEREO-004 –  Built bidirectional verification**: Set $d_g(x)=x_g-x_d$ and a positive straight disparity $d_d(x_d)=x_g-x_d$ for the same point. A consistent pair must check $|d_g(x)-d_d(x-d_g(x))|<\tau$, subject to interpolation and visibility. If the right field uses the opposite sign, the equation changes in sum: the conventions must be explicit. This test rejects some inconsistencies, but two false matches on a repetitive texture can remain mutually compatible. Geometric validation, the distinction between holes and regularized values, and an independent reference remain necessary. The threshold $\tau$ is in pixels of disparity of the grid considered.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, stereo](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html) –  Basics, triangles and disparity; uncertainty derivations and bidirectional test built. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
