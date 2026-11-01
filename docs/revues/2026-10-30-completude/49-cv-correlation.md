# Review –  MOSSE and KCF –  Correlation filter tracking –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORRELATION-001 | Deduction/Assumption Cases; Documentary Context Below | From pic to image: specifies the existing question | Finished core preserved; 222 → 328 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORRELATION-002 | Deduction/Assumption Cases; Documentary Context Below | Structured regression: specifies the existing question | Finished core preserved; 218 → 320 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORRELATION-003 | Deduction/Assumption Cases; Documentary Context Below | Effect of a distractor: specifies the existing question | Finished core preserved; 214 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORRELATION-004 | Deduction/Assumption Cases; Documentary Context Below | Separating research and learning: clarifies the existing question | Finished core preserved; 210 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CORRELATION-005 | Deduction/Assumption Cases; Documentary Context Below | Measure of success: specifies the existing question | Finished core preserved; 209 → 317 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-CORRELATION](../../../vault/110-tracking-association/references/114-mosse-kcf.md); [flashcards](../../../vault/110-tracking-association/114-mosse-kcf.md). reference note modified before the flashcards.

- **CV-CORRELATION-001 –  From pic to image**: The answer is calculated in the coordinates of the patch or its features. Converting the maximum offset to the image requires the origin of the crop, its resizing, and any stride. A circular correlation convention also requires interpreting near-edge indices as appropriate signed offsets. An error here can produce a jump despite a correctly calculated peak. Check a known synthetic translation and return to the coordinate frame image before setting the trust. The possible subpixel location refines the peak estimation; it does not guarantee equivalent physical accuracy on real images.

- **CV-CORRELATION-002 –  Structured regression**: a regularized linear regression solves $\min_w\|Xw-y\|^2+\lambda\|w\|^2$. If the lines of $X$ are the cyclic shifts of the same signal, the circulant structure makes it possible to diagonalize the corresponding operations by Fourier transform. In a kernel regression, we work on a matrix of similarities whose structure must remain compatible. This explains the efficiency without assimilating a core to a deep network. The regularization parameter stabilizes learning according to the feature scale; it does not compensate for a target missing from the patch or an artificial edge hypothesis ill-suited to the scene.

- **CV-CORRELATION-003 –  Effect of a distractor**: If a second peak enters the area used to calculate average and standard deviation off peak, it can change the PSR of the first, even if its height remains the same. The size of the excluded area and the edges of the patch therefore participate in the definition of the score. A positive affine transformation $r'=ar+b$, with the same support and $a>0$, ideally retains the PSR, because numerator and standard deviation are multiplied by $a$. On the other hand, clipping, quantifying or changing the medium can break this invariance. The score is therefore comparable only with an identical calculation procedure and a threshold validated in its context.

- **CV-CORRELATION-004 –  Separate research and learning**: Freeze updates retains a target model, but does not automatically change the region being crawled. After a long occlusion or a large shift, the target may return elsewhere and remain untraceable despite an intact model. Compare two separate interventions: freezing the model with unchanged search, then expanded search policy or detection with the same model. Measure false returns on distractors and recovery times, without using the true position to silently reset. This ablation distinguishes contamination, loss of spatial coverage and appearance ambiguity, which can produce a similar final box on the bottom.

- **CV-CORRELATION-005 –  Measure of success**: A curve can report, for each $\tau$ threshold, the proportion of frames where the IoU of the target exceeds $\tau$, under an announced presence policy. The area under this curve describes something other than the accuracy of the center at a fixed pixel threshold. Two boxes of the same center but of very different sizes can have a good center error and a bad IoU. The resets still change which periods are evaluated and what information is provided. Publishing the rules with the curve and the losses allows to compare the compromises without retaining only the frames where the tracker has succeeded.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) –  §3.1 – 3.2, edges and learning; mathematical complements and built protocols. View on 2026-10-30.
- [Henriques et al., KCF](https://arxiv.org/html/1404.7584v1) –  §IV, regression and circulant structure; project deductions. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
