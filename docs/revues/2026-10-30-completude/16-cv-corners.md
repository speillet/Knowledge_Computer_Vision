# Review –  Harris and Shi – Tomasi –  local structure and followable points –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORNERS-001 | Deduction/Assumption Cases; Documentary Context Below | Derive the local tensor: specifies the existing question | Finished core preserved; 209 → 321 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORNERS-002 | Deduction/Assumption Cases; Documentary Context Below | Avoid confusing score and model: specifies the existing question | Finished core preserved; 205 → 319 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORNERS-003 | Deduction/Assumption Cases; Documentary Context Below | Read the selection as a suite of filters: specifies the existing question | Finished core preserved; 202 → 318 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORNERS-004 | Deduction/Assumption Cases; Documentary Context Below | Distinguish between local and global observation: specifies the existing question | Finished core preserved; 214 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORNERS-005 | Deduction/Assumption Cases; Documentary Context Below | check round trip built: specifies the existing question | Finished core preserved; 203 → 317 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-CORNERS](../../../vault/40-features-matching/references/46-harris-shi-tomasi.md); [flashcards](../../../vault/40-features-matching/46-harris-shi-tomasi.md). reference note modified before the flashcards.

- **CV-CORNERS-001 –  Derive the local tensor**: for a small displacement $d$, $I(p+d)-I(p)\approx\nabla I(p)^Td$. The weighted sum of these squared deviations gives $d^T(\sum_p w_p\nabla I_p\nabla I_p^T)d$, so $M$. Constant error contours are ellipses: their large axis corresponds to the direction in which the image changes little. If the photometric noise model is isotropic and the problem is correctly posed, the local uncertainty of displacement is related to a matrix proportional to $M^{-1}$. A small eigenvalue then becomes a great directional uncertainty; it is a link with the followability, under assumptions, not a guarantee of future visibility.

- **CV-CORNERS-002 –  Avoid confusing score and model**: Harris can calculate determinant and trace directly without diagonalizing $M$; Shi – Tomasi evaluates the smallest eigenvalue, $(\operatorname{tr}M-\sqrt{(M_{11}-M_{22})^2+4M_{12}^2})/2$ for a symmetric matrix $2\times2$. These are two summaries of the same tensor, not two new proofs of identity of the point. In the isotropic case $\lambda_1=\lambda_2=\lambda$, Harris gives $(1-4k)\lambda^2$ while Shi – Tomasi gives $\lambda$. Their evolution with the contrast and scale of the patch therefore differs even when the visual ranking of the best corners seems similar. Removing maxima and spacing remain separate steps of these formulas.

- **CV-CORNERS-003 –  Read selection as a filter suite**: first calculate the quality flashcard, retain the local maxima, eliminate insufficient scores, then consider the candidates in descending order respecting the minimum distance and budget. Therefore, the quota does not replace a quality threshold. In a built-in case, if the only good points are close, increasing the spacing can get a lot and leave less than the number requested; this is not necessarily a failure of the API. To limit concentration, a mask of interest or quotas by region are choices of system to compare, keeping the same notion of score and the same units of distance.

- **CV-CORNERS-004 –  Distinguish between local and global observation**: $M$ describes the curvature of a small translation cost around a given patch. It does not compare this patch to all other patches in an image. A grid can therefore give a strong curvature around each intersection, while producing several remote minima for matching between images. A known initial move can make local tracking possible without resolving the overall recognition of the correct box. To evaluate the detector alone, use a reference transformation and check the distance to the projected position; to match it, then examine which identity is selected among the candidates. Both rates do not have the same denominator.

- **CV-CORNERS-005 –  check round trip built**: Following $p_t$ to $\hat p_{t+1}$, then following the latter to $\hat p_t$ gives a $e_{FB}=\|\hat p_t-p_t\|_2$ cycle error in pixels. A big error signals a useful inconsistency to reject; a small error can also come from the same bad pattern found in both directions. It must therefore complete a displacement reference, not replace it. Compare the fraction of valid points by keeping the occlusions in the balance sheet. If a setting rejects almost all the hard points, its average error on survivors can drop while degrading the availability of the registration. Reliable monitoring and refusal policy must be evaluated together.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) –  Theory, tensor and response. View on 2026-10-30.
- [OpenCV 4.13, Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html) –  Theory and selection goodFeaturesToTrack. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
