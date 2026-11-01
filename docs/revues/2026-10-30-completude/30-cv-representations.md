# Review –  Visual representations, ViT, Swin, ConvNeXt and DINOv2 –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Example of dimensions: specifies the existing question | Finished core preserved; 188 → 292 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-REPRESENTATIONS-002 | Deduction/Assumption Cases; Documentary Context Below | Counting by windows: specifies the existing question | Finished core preserved; 188 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-REPRESENTATIONS-003 | Deduction/Assumption Cases; Documentary Context Below | From Token to Default Area: Specify the Existing Question | Finished core preserved; 185 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-REPRESENTATIONS-004 | Deduction/Assumption Cases; Documentary Context Below | Parametrisation LoRA: specifies the existing question | Finished core preserved; 194 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-REPRESENTATIONS-005 | Project Deduction/Protocol; no new external confirmation claimed | Invariant of pretreatment: specifies the existing question | Finished core preserved; 181 → 285 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-REPRESENTATIONS](../../../vault/70-reconnaissance-representations/references/71-representations-transfert.md); [flashcards](../../../vault/70-reconnaissance-representations/71-representations-transfert.md). reference note modified before the flashcards.

- **CV-REPRESENTATIONS-001 –  Sample dimensions**: a $224\times224$ image with $16\times16$ patches gives 196 image tokens; at $448\times448$, it gives 784. One attention per head typically calculates $QK^T$ of size $N\times N$, then a combination of values. The interaction term is of order $N^2d$, while the projections and the MLP introduce order terms $Nd^2$ for a width $d$. Depending on the plan, these contributions and memory access do not dominate in the same way. Memory-saving implementations can avoid storing the entire matrix without necessarily removing quadratic counting from calculated interactions.

- **CV-REPRESENTATIONS-002 –  Counting by windows**: If a window contains $M^2$ tokens and the image contains $N$ tokens, the internal interactions total about $(N/M^2)(M^2)^2=NM^2$, instead of $N^2$ for global attention, fixed width. This simplification assumes a fixed window size and ignores projections, MLP, padding, and hierarchical merge. The staggered windows allow successive blocks to communicate previously separated regions. The information field is therefore built over layers; a local layer does not instantly access the entire image. Comparing this organization to convolutions requires also examining resolution, number of channels and dense task head.

- **CV-REPRESENTATIONS-003 –  From Token to Default Zone**: Selecting local features retains a grid of patches, while a global vector aggregates the image. Interpolation of the grid to the original resolution increases the number of pixels of the score, without creating in itself a location accuracy absent from the features. Define how a patch covers the part and what defect size it should distinguish. A constructed baseline can freeze the extractor, index the nominal patches and use their distance as a score, before comparing to a supervised head. Keeping part masks, alignment, and aggregation policy allows errors to be attributed to the representation choice rather than to an implicit interface.

- **CV-REPRESENTATIONS-004 –  Parameterization LoRA**: For a layer $W\in\mathbb R^{d\times k}$, replace the complete update with $\Delta W=BA$, with $B\in\mathbb R^{d\times r}$ and $A\in\mathbb R^{r\times k}$, causes $r(d+k)$ parameters instead of $dk$, out of bias and other modules. Rank $r$ constrains the space of updates and is a compromise to validate. When the adaptation is linear and compatible with weight representation, one can form $W'=W+BA$ for inference; this differs from a non-linear adaptation kept in the computation path. The small number of parameters learned does not therefore, by itself, describe the graph actually deployed.

- **CV-REPRESENTATIONS-005 –  Pretreatment Invariant**: If the model waits for $z_c=(x_c/255-\mu_c)/\sigma_c$, giving it $x_c\in[0,255]$ directly before subtraction changes the scale by a factor close to 255, without being a variation of physical domain. Testing an artificial image with each channel is constant and different makes it possible to detect permutation RGB/BGR and repeated normalization. For a dense task, also check the transformation of labels and coordinates by crop, resize and padding. An identical input image is only a sufficient witness if all stochastic steps are neutralized and if weight, mode of evaluation and numerical precision are also fixed.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [ViT](https://arxiv.org/html/2010.11929v2) –  §3.1, sequence of patches; project counts and tests. View on 2026-10-30.
- [Liu et al., Swin](https://arxiv.org/html/2103.14030v2) –  §3.2, equations 1 – 2, windows and offset; counting explained by the project. View on 2026-10-30.
- [Oquab et al., DINOv2](https://arxiv.org/html/2304.07193v2) –  §7.4, patch tokens, flashcard low resolution and interpolation; proposed inspection baseline. View on 2026-10-30.
- [Hu et al., LoRA](https://arxiv.org/html/2106.09685v2) –  §4.1, W+BA parameterization and linear fusion. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
