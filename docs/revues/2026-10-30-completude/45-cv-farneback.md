# Review –  Farnebäck –  dense flow by polynomial expansion –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FARNEBACK-001 | Deduction/Assumption Cases; Documentary Context Below | Development of translation: specifies the existing question | Finished core preserved; 209 → 309 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FARNEBACK-002 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Directional Sensitivity: specifies the existing question | Finished core preserved; 200 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FARNEBACK-003 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Transport relationship: specifies the existing question | Finished core preserved; 214 → 321 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FARNEBACK-004 | Deduction/Assumption Cases; Documentary Context Below | Field composition: specifies the existing question | Finished core preserved; 220 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FARNEBACK-005 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Orders of magnitude: specifies the existing question | Finished core preserved; 212 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FARNEBACK](../../../vault/100-mouvement-video/references/103-farneback.md); [flashcards](../../../vault/100-mouvement-video/103-farneback.md). reference note modified before the flashcards.

- **CV-FARNEBACK-001 –  Development of translation**: Replace $x$ with $x-d$ in $x^TAx+b_1^Tx+c_1$ gives $x^TAx+(b_1-2Ad)^Tx+d^TAd-b_1^Td+c_1$ when $A$ is symmetrical. The comparison of linear terms therefore provides $b_2=b_1-2Ad$. This derivation is accurate for the built model; the real images do not have the same polynomial transported everywhere. We then look for an aggregated and weighted solution to local constraints, with a domain where translation is an acceptable approximation. Constant terms also change, but do not replace the directional information needed to identify the two components of displacement.

- **CV-FARNEBACK-002 –  Directional Sensitivity**: with $A=\operatorname{diag}(2,\varepsilon)$, the ideal equations become $4d_x=\Delta b_x$ and $2\varepsilon d_y=\Delta b_y$. A small error on $\Delta b_y$ is amplified by $1/(2\varepsilon)$ when $\varepsilon$ is small. A weak residual can thus coexist with a strong error on $d_y$. Solving the system by proper factorization and inspecting its packaging is more informative than blindly applying an inverse. A regularization numerically stabilizes the weak direction by adding a preference; it does not transform this preference into certain observation. This is precisely what the diagonal example makes it possible to understand without executing a complete flow.

- **CV-FARNEBACK-003 –  Transport relationship**: The front convention is written $I_1(x,y)\approx I_2(x+u(x,y),y+v(x,y))$ when photometry and visibility are compatible. To sample the second image on the grid of the first, we therefore use these destination positions. Creating a destination image by projecting all the source pixels can produce holes and collisions; it is not the same resampling operation. For vector $(4,-2)$, keep the mask of the positions reached out of field. This check sense distinguishes a valid displacement, a warp inversion and a simple display whose axes have been swapped.

- **CV-FARNEBACK-004 –  Field composition**: dial a $F_{12}$ move and then $F_{23}$ gives $F_{13}(x)=F_{12}(x)+F_{23}(x+F_{12}(x))$, under valid matches. The return is the particular case where one hopes to return to the same point, hence the formula of the residual. Adding the fields to the same indices would assume that these indices already denote the same surfaces in all images. The interpolation of the second field can still mix two movements at a border; keep this source of error in the interpretation. Consistent composition across multiple frames also accumulates errors and does not automatically become long-term tracking with visibility and re-identification.

- **CV-FARNEBACK-005 –  Orders of magnitude**: With a spatial reduction of two at each level, a displacement of 32 px in the original image becomes 4 px after three reductions. A wide object of 6 px, on the other hand, occupies only 0,75 px before the effects of filtering and sampling: its own movement can disappear. Moving up the field requires resizing the grid and multiplying the components by the appropriate scaling factor. Interpolating only the array without adjusting the amplitude produces a contract defect. This constructed example explains the trade-off between capturing large displacement and preserving small structures, without setting an optimal universal number of levels.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) –  Dense Optical Flow; project-specific quadratic derivations, original PDF inaccessible by timeout during this pass. View on 2026-10-30.

The original PDF Farnebäck has expired during this time. The quadratic expansion is a derivation of the written model, verified algebraically; the dense format is documented by OpenCV. No new successful access to the original full text is claimed.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
