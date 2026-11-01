# Review –  Canny and Hough: contours, lines and segments –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CANNY-HOUGH-001 | Deduction/Assumption Cases; Documentary Context Below | Describe hysteresis as a journey: specifies the existing question | Finished core preserved; 202 → 316 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CANNY-HOUGH-002 | Deduction/Assumption Cases; Documentary Context Below | Angular accuracy and position: specifies the existing question | Finished core preserved; 208 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CANNY-HOUGH-003 | Deduction/Assumption Cases; Documentary Context Below | Find a finished support: specifies the existing question | Finished core preserved; 200 → 323 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CANNY-HOUGH-004 | Deduction/Assumption Cases; Documentary Context Below | Differentiate between vote and adjustment error: specifies the existing question | Finished core preserved; 186 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-CANNY-HOUGH](../../../vault/30-traitement-image/references/32-canny-hough.md); [flashcards](../../../vault/30-traitement-image/32-canny-hough.md). reference note modified before the flashcards.

- **CV-CANNY-HOUGH-001 –  Describe hysteresis as a journey**: after calculating the gradient and removing non-maxima, initialize a queue with pixels above the high threshold. Browse their neighbors and recursively keep those above the low threshold; discard other unrelated answers. This diagram explains how a long, small portion can be retained without a single pixel exceeding the high threshold. The direction of the gradient is a normal to the contour, calculated with a convention such as $\operatorname{atan2}(G_y,G_x)$; the suppression compares the amplitudes along this normal. Changing standard L1/L2, smoothing or digital depth changes the scale of scores and therefore the direction of the thresholds.

- **CV-CANNY-HOUGH-002 –  Angular accuracy and position**: A small $\delta\theta$ error causes $\rho$ to vary by about $(-x\sin\theta+y\cos\theta)\delta\theta$, with $\delta\theta$ in radians. The effect grows with distance at the origin: an angular bin does not represent a uniform tolerance in pixels everywhere. At a leverage of 500 px, a degree corresponds to an order of magnitude of 8,7 px. This derivation does not give the final error of a detector, but helps to choose a reasonable discretization and to understand an extrapolation. Couples $(\rho,\theta)$ and $(-\rho,\theta+\pi)$ represent the same straight line; the angle interval and the allowed sign of $\rho$ must be processed together.

- **CV-CANNY-HOUGH-003 –  Find a finished support**: from the normal $n=(\cos\theta,\sin\theta)$, take a point $p_0=\rho n$ and the unit direction $d=(-\sin\theta,\cos\theta)$. For each $p$ contour point, test its normal $|n^Tp-\rho|$ distance, then project the points compatible with $s=d^T(p-p_0)$. Contiguous groups in $s$ offer segments, whose ends are equal to $p_0+s_{min}d$ and $p_0+s_{max}d$. This process distinguishes perpendicular tolerance and longitudinal holes. The choice of support, the presence of occlusions and a possible re-estimation of the line on its points condition the ends. It is not enough to take the minimum and maximum of all the collinear points of the image.

- **CV-CANNY-HOUGH-004 –  Differentiate vote and adjustment error**: a long texture provides a lot of points and therefore votes, even if it is not the desired structure. For a candidate, calculate in addition the normal distances $r_i=x_i\cos\theta+y_i\sin\theta-\rho$ on her support points, their longitudinal extent and the fraction of the positions actually covered. A very precise short line and a long discontinuous line do not have the same use. Also compare its relationship to other expected edges: parallelism, intersections or distances, if these properties are legitimate for the room. These validations are choices of the proposed pipeline; the accumulator score is not a calibrated probability of the presence of a business edge.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Canny](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) –  gradient, Non-maximum Removal and Hysteresis Thresholding. View on 2026-10-30.
- [OpenCV 4.13, Hough](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html) –  How does it work; Standard and Probabilistic Hough. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
