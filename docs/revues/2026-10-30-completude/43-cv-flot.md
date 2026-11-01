# Review –  optical flow: Lucas – Kanade, Farnebäck and RAFT –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | Deduction/Assumption Cases; Documentary Context Below | Lucas – Kanade system: specifies the existing question | Finished core preserved; 188 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLOT-002 | Deduction/Assumption Cases; Documentary Context Below | Change of grid: specifies the existing question | Finished core preserved; 196 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLOT-003 | Deduction/Assumption Cases; Documentary Context Below | Dimensions of the correlation: specifies the existing question | Finished core preserved; 195 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLOT-004 | Deduction/Assumption Cases; Documentary Context Below | residual round trip: specifies the existing question | Finished core preserved; 190 → 295 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FLOT](../../../vault/100-mouvement-video/references/101-flot-optique.md); [flashcards](../../../vault/100-mouvement-video/101-flot-optique.md). reference note modified before the flashcards.

- **CV-FLOT-001 –  Lucas – Kanade system**: stack the window gradients in a $A$ matrix with each row equal to $(I_x,I_y)$, and set $b=-I_t$. The least squares give $A^TA\,d=A^Tb$, with $d=(u,v)^T$. Two sufficiently informative eigenvalues of $A^TA$ are required to constrain both directions; an edge typically produces a weak direction. Expanding the window may bring new gradients, but possibly violates the assumption of shared motion by mixing two objects. A good selection of points therefore simultaneously seeks spatial information and neighborhood coherence, not just a large gradient amplitude.

- **CV-FLOT-002 –  Grid change**: If the second string works on an image resized by $(s_x,s_y)$, the same displacement becomes $(s_xu,s_yv)$. To compare image speeds, first put the vectors in a common grid and then use the real acquisition intervals. A lost frame eventually doubles the interval, without the physical speed having doubled. In perspective, even a constant 3D translation produces depth-dependent image displacements; an apparent size variation can also change the field. The conversion pixels→meters therefore requires a scene and camera model, beyond a division by the nominal rate.

- **CV-FLOT-003 –  Dimensions of Correlation**: for two feature maps $h\times w$, an all-peer compatibility connects each site of the first to each site of the second, $(hw)^2$ values before optimizations. The volume encodes candidate similarities, not a bijective assignment of pixels. Updates look at this volume around predicted positions and adjust the flow; multiple sources may target a nearby region, and occlusionss do not always offer a match. Separating memory from volume, cost per iteration, and number of iterations helps to understand the resolution compromise. The recurrence of refinement is not a guarantee of physical convergence or identity.

- **CV-FLOT-004 –  residual round trip**: note $F_{12}$ moving the 1 image to 2 and $F_{21}$ back. For a pixel $x$ of the first image, calculate $e(x)=\|F_{12}(x)+F_{21}(x+F_{12}(x))\|$ in pixels, only when the return sampling is valid. A trust rule can compare this residual to a tolerance dependent on movement and noise, to be validated on reserved data. A periodic texture can produce an erroneous translation and then its exact opposite: the zero residual then proves nothing on the real surface. Keep the visibility failure distinct from a simple large digital residual.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) –  Lucas – Kanade equation and system; deduced grid compositions and changes. View on 2026-10-30.
- [Teed–Deng, RAFT](https://arxiv.org/html/2003.12039v3) –  figure 1 and presentation of all-pair and updated correlations. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
