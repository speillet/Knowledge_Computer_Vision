# Review –  SuperPoint, LightGlue and LoFTR –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Deduction/Assumption Cases; Documentary Context Below | Why these bricks are learned together or separately: specifies the existing question | Finished core preserved; 185 → 295 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCH-APPRIS-002 | Deduction/Assumption Cases; Documentary Context Below | From coarse to fine: clarifies the existing question | Finished core preserved; 199 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCH-APPRIS-003 | Deduction/Assumption Cases; Documentary Context Below | Learned Contract and Adaptive Budget: Specifying the Existing Question | Finished core preserved; 190 → 303 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCH-APPRIS-004 | Deduction/Assumption Cases; Documentary Context Below | Differentiate between location accuracy and quantity: specifies the existing question | Finished core preserved; 198 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MATCH-APPRIS-005 | Deduction/Assumption Cases; Documentary Context Below | Compose pre-processing matrices: specifies the existing question | Finished core preserved; 191 → 310 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-MATCH-APPRIS](../../../vault/40-features-matching/references/44-superpoint-lightglue-loftr.md); [flashcards](../../../vault/40-features-matching/44-superpoint-lightglue-loftr.md). reference note modified before the flashcards.

- **CV-MATCH-APPRIS-001 –  Why These Bricks Are Learned Together or Separately**: SuperPoint shares an encoder between a detection head and a description head; the homographic adaptation matches predictions of transformed views to build more repeatable supervision. LightGlue shares features already extracted and contextualizes them between the two sets. A point is therefore no longer only compared by an isolated distance to each descriptor: its compatibility may depend on the other observations of the pair. This dependence justifies freezing extractor and matching for a reproducible baseline. If an image does not offer enough points or overlap, the context does not create new physical observations.

- **CV-MATCH-APPRIS-002 –  Coarse at the end**: LoFTR computes multi-resolution representations, uses intra-image and inter-image interactions to establish coarse-level candidates, and then refines positions in local neighborhoods. The coarse level reduces the search space but quantifies the locations; the refinement aims to recover a finer precision than this grid. A gross match error does not become correct simply because the refinement produces a subpixel position. “Subpixel” describes a digital location resolution, not guaranteed accuracy. The density of the candidates and their concentration must be evaluated with the visibility mask and the final geometry, including in areas with little texture.

- **CV-MATCH-APPRIS-003 –  Learned contract and adaptive budget**: LightGlue can stop certain steps earlier or remove points that have become unhelpful according to its internal criteria. These decisions are based on the statistics of the features and the planned checkpoint; a representation of the same size but excluding distribution can therefore change both the matches and the calculation time. For comparison, also record thresholds and adaptive policy, not just the weight file. Check the latency dispersion between easy and difficult pairs. Disabling an adaptation for an ablation can help assign the change, but does not alone provide an exact match reference or an optimal setting for the new domain.

- **CV-MATCH-APPRIS-004 –  Distinguish location and quantity accuracy**: A pose can be estimated with few precise and distributed matches, or fail with many pairs close to a single line. Compare to fixed point budget isolates certain causes; compare to the best quality – cost point achievable by each pipeline answers another question, to be announced. Images very close to training or pairs of the same sequence can also favor a learned model: separate groups according to future use. For a measurement of pose, specify calibration, geometric threshold, alignment group and failure processing. The name of a benchmark does not guarantee that these conventions are common to two publications.

- **CV-MATCH-APPRIS-005 –  Compose preprocessing matrices**: if $A$ and $B$ respectively send the original images to the network inputs and if $H_{net}$ connects these two inputs, the original homography is $H_{orig}=B^{-1}H_{net}A$. This relationship comes from the original path A→network A→network B→original B. It also deals with distinct horizontal and vertical factors or a crop expressed in a homogeneous affine. Padding pixels are not observations of the scene: their validity must be managed, rather than converted to image coordinates as if they were from a sensor. The subpixel positions and pixel center conventions finally require testing a digital round trip on known points.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [SuperPoint](https://arxiv.org/html/1712.07629v4) –  §§3 and 5, two heads and homographic adaptation. View on 2026-10-30.
- [LightGlue, official deposit](https://github.com/cvg/LightGlue) –  README Use and Advanced configuration, calculation adaptation. View on 2026-10-30.
- [LoFTR](https://arxiv.org/html/2104.00680v1) –  §§3.1 – 3.4, context and bracket-to-fine. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
