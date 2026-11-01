# Review –  SIFT –  local points and multi-scale description –  2026-10-30

## Overview

7 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SIFT-001 | Deduction/Assumption Cases; Documentary Context Below | Linking outputs to an estimate: specifies the existing question | Finished core preserved; 228 → 344 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-002 | Deduction/Assumption Cases; Documentary Context Below | Why the DoG is approaching a Laplacian: clarifies the existing question | Finished core preserved; 236 → 356 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-003 | Deduction/Assumption Cases; Documentary Context Below | Understanding standardization: clarifies the existing question | Finished core preserved; 226 → 338 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-004 | Deduction/Assumption Cases; Documentary Context Below | Beware of squared distances: specifies the existing question | Finished core preserved; 219 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-005 | Deduction/Assumption Cases; Documentary Context Below | Analyzing local deformation: specifies the existing question | Finished core preserved; 226 → 344 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-006 | Deduction/Assumption Cases; Documentary Context Below | Ambiguity to several solutions: specifies the existing question | Finished core preserved; 230 → 339 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SIFT-007 | Deduction/Assumption Cases; Documentary Context Below | Break down the causes of failure: specifies the existing question | Finished core preserved; 222 → 329 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SIFT](../../../vault/40-features-matching/references/41-sift.md); [flashcards](../../../vault/40-features-matching/41-sift.md). reference note modified before the flashcards.

- **CV-SIFT-001 –  Link outputs to an estimate**: represent the points by two tables $P_A\in\mathbb R^{n\times2}$ and $P_B\in\mathbb R^{m\times2}$, and their descriptors by two tables with 128 columns. The matcher returns $(i,j)$ indices, not directly the coordinates of a transformation. A robust estimate then uses the $(P_A[i],P_B[j])$ pairs in the same pixel contract as its threshold. If the extraction was done on a resized image, the estimated matrix connects these resized images; composing it with the preprocessing transformations is necessary to return to the initial images. Maintaining these associations of indices avoids confusing the quality of the descriptor and the error of manipulation of the coordinates.

- **CV-SIFT-002 –  Why DoG is approaching a Laplacian**: for $k$ close to 1, a scale development gives $L(k\sigma)-L(\sigma)\approx(k-1)\sigma\,\partial L/\partial\sigma$. The Gaussian diffusion equation links this derivative to $\sigma\nabla^2L$: the difference is therefore proportional to a Laplacian normalized by $\sigma^2$. This approximation implies a suitable spacing of scales, not an exact identity for any $k$. Detecting an extremum is just the beginning: local refinement estimates position and scale between samples, then low-contrast and edge-dominated rejections avoid describing unstable points. The same number of candidates does not mean the same number of reliable keypoints.

- **CV-SIFT-003 –  Understanding standardizations**: For a non-zero $d$ histogram, division by $\|d\|_2$ cancels out a common multiplicative gain; subtracting a constant from all intensities does not already change their differences in the ideal model. On the other hand, if a few gradients dominate, they can crush the contribution of other cells. A clipping followed by a new normalization limits this domination. Constructed example: two patches with a single edge becoming much stronger can keep a similar directional layout while changing the raw norm. Interpolation between cells and orientation bins also prevents a small geometric variation from abruptly shifting the entire contribution on one side of a discrete boundary.

- **CV-SIFT-004 –  Watch out for squared distances**: If a routine provides $s_1=d_1^2$ and $s_2=d_2^2$, the criterion equivalent to $d_1<\tau d_2$ is $s_1<\tau^2s_2$, not $s_1<\tau s_2$. With $\tau=0,8$, directly comparing squares to 0,8 would be tolerating a distance ratio close to 0,894. This transformation is algebraically inferred for positive distances; it does not say which convention uses a particular API. Read the contract of the function and test a small known couple before reusing a threshold. The "second" neighbor must also come from the same set of candidates provided by the protocol; changing the base changes the measured ambiguity.

- **CV-SIFT-005 –  Analyze local deformation**: In the vicinity of a point, a regular projective transformation is linearized by a matrix $2\times2$ which can have two different singular values. A rotation and an isotropic scale only compensate for a part of it; the ratio of the singular values measures a local anisotropy. Example built: a disc observed more and more obliquely becomes an ellipse, even after returning its main axis to the right orientation. The described neighborhood therefore changes shape. Rectifying can help if the geometry is known, but estimating this rectification from the same difficult matches is not a free solution. The occlusion additionally removes information that no coordinate transformation restores.

- **CV-SIFT-006 –  Ambiguity to several solutions**: A periodic pattern allows $H_0,H_1,\ldots$ candidate transformations that shift the alignment of a period while retaining small residuals on repeated windows. We must compare information that does not have this symmetry, or announce that the problem remains ambiguous. Then construct an acceptance rule including an absolute reference or a justified motion marker. A better score of a few inliers is not proof when all the observations are repeated. Examine several assumptions and their margin may be more informative than returning only the best model, provided you evaluate this rule on ambiguous reserved cases.

- **CV-SIFT-007 –  Break down the causes of failure**: separately measure repeatability of detection, match accuracy, recall of useful matches and registration rate accepted to business tolerance. A ratio of players can increase simply because almost all matches have been withdrawn; you have to keep its denominator and coverage. The exhaustive cost between $n$ and $m$ descriptors of dimension $d$ is of the order of $nmd$ scalar operations; varying the quota of points therefore also changes the matcher and the budget RANSAC. Comparing a quality-cost boundary for multiple settings is more instructive than confronting two default parameters, without announcing a winner before the measurements.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) –  §§3 – 7.1, scale space, location, description and matching. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
