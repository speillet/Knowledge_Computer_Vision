# Review –  Filters, gradients and pyramids –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FILTRES-001 | Deduction/Assumption Cases; Documentary Context Below | Linking the operation to noise: specifies the existing question | Finished core preserved; 202 → 315 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FILTRES-002 | Deduction/Assumption Cases; Documentary Context Below | Complete form and role of standardization: specifies the existing question | Finished core preserved; 198 → 319 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FILTRES-003 | Deduction/Assumption Cases; Documentary Context Below | Make the trade-off quantifiable: clarifies the existing question | Finished core preserved; 189 → 307 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FILTRES-004 | Deduction/Assumption Cases; Documentary Context Below | Building Levels: Specifying the Existing Question | Finished core preserved; 189 → 306 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FILTRES](../../../vault/30-traitement-image/references/31-filtrage-gradients.md); [flashcards](../../../vault/30-traitement-image/31-filtrage-gradients.md). reference note modified before the flashcards.

- **CV-FILTRES-001 –  Link the operation to the noise**: for a normalized linear filter $J(p)=\sum_q k_q I(p-q)$ and independent noises of variance $\sigma_n^2$, the output variance is $\sigma_n^2\sum_q k_q^2$. A uniform average of nine samples therefore divides it by nine, under these assumptions, but also mixes their signals. The median depends on the rank of the values: an isolated pulse can stay away from the central rank without drawing the result towards it. Noise correlations, edges and fine details change these tradeoffs. The Gaussian is separable: two convolutions 1D replace a convolution 2D for the same kernel produced, without making a median equivalent to this operation.

- **CV-FILTRES-002 –  Complete form and role of standardization**: for a pixel $p$, write $J(p)=\sum_q w_{pq}I(q)/\sum_q w_{pq}$, with $w_{pq}=\exp(-\|p-q\|^2/(2\sigma_s^2))\exp(-(I(p)-I(q))^2/(2\sigma_r^2))$. The first factor favors nearby neighbors, the second one those whose intensity resembles that of the center. The denominator adapts the sum of the weights to the local content; without it, an edge could simply darken the result by rejecting neighbors. The weights depend on the image: it is a non-linear operation, even if the output looks like an average. The noise of the central pixel also influences which neighbors will be considered similar; preserving a contour remains conditional.

- **CV-FILTRES-003 –  Make the compromise quantifiable**: $PSNR=10\log_{10}(L^2/MSE)$, with $L$ the maximum of the range announced and $MSE$ the average squared errors against a reference. Modifying $L$ or normalization without consistency changes the score. If a defect occupies a fraction $p$ of the pixels and undergoes an amplitude error $a$, its contribution to the MSE is only $pa^2$: it can remain small even if all its pixels are lost. Then measure the probability of detecting a defective part and the frequency of false alarms per part, with rules of association and constant thresholds. The reference to PSNR must itself be justified; a noisy image used as "clean" changes the problem.

- **CV-FILTRES-004 –  Build levels**: A Gaussian pyramid follows $I_{\ell+1}(x,y)=(G_\ell*I_\ell)(2x,2y)$ in an example of decimation by two. Coordinates are approximately converted by $p_0=2^\ell p_\ell$, respecting the exact pixel center conventions. A five-ray window at the $\ell=3$ level covers about forty pixels of radius in the initial image: its physical support has changed. This is useful for bringing back a large displacement in a local capture area, but it can mix objects or eliminate a fine structure. Propagate coordinates, descriptor radius, and geometric thresholds in the same system of units, rather than treating levels as independent images.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, Smoothing Images](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html) –  Theory, Gaussian, Median and Bilateral Filter. View on 2026-10-30.
- [OpenCV 4.13, PSNR/SSIM](https://docs.opencv.org/4.13.0/d5/dc4/tutorial_video_input_psnr_ssim.html) –  definition of PSNR; built rarity example. View on 2026-10-30.
- [OpenCV 4.13, Image Pyramids](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html) –  Gaussian Pyramid, filtering and decimation. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
