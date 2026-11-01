# Review –  NeRF, 3D Gaussian Splatting and Reconstruction –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Deduction/Assumption Cases; Documentary Context Below | Weight along the radius: specifies the existing question | Finished core preserved; 191 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-RENDU3D-002 | Deduction/Assumption Cases; Documentary Context Below | Built scale gauge: specifies the existing question | Finished core preserved; 190 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-RENDU3D-003 | Deduction/Assumption Cases; Documentary Context Below | Coverage and causality of the defect: specifies the existing question | Finished core preserved; 182 → 288 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-RENDU3D](../../../vault/120-generatif-multimodal/references/123-nerf-gaussian-splatting.md); [flashcards](../../../vault/120-generatif-multimodal/123-nerf-gaussian-splatting.md). reference note modified before the flashcards.

- **CV-RENDU3D-001 –  Weight along the radius**: for a radius $r(t)=o+td$, the ideal volume rendering uses $C(r)=\int T(t)\sigma(r(t))c(r(t),d)\,dt$, with $T(t)=\exp[-\int_{t_n}^t\sigma(r(s))ds]$. If $t$ is a length and $d$ unit, $\sigma$ has an inverse length unit; $T$ is without unit. The density depends on the position, while the radiance may depend on the direction in the original NeRF. This integration differs from a single opaque mesh and explains how multiple density/appearance distributions can contribute to the same pixels. The useful geometry does not automatically read as a certified metric surface.

- **CV-RENDU3D-002 –  Scale gauge built**: Multiplying camera positions and scene coordinates by a single factor can retain projection directions and similar images, if the representation and rendering are transformed consistently. Therefore, a view synthesis measurement does not set an absolute length on its own. A metric calibration, a known baseline, or a dimension reference must anchor this scale if necessary. Even fixed scale, surface errors can remain compensated by appearance. Compare geometric errors, cover and reserved images thus measures complementary properties, instead of improperly converting a PSNR into millimeter accuracy.

- **CV-RENDU3D-003 –  Coverage and causation of defect**: Reserve views close to those of training mainly tests local interpolation, while more distant angles can reveal less constrained regions. Announce this angular distance and the visibility of the surfaces before talking about generalization. A controlled perturbation of the input poses makes it possible to distinguish sensitivity to calibration and coverage inadequacy, at still images. If the scene moves or the exhibition changes, a representation can absorb the inconsistency in artificial structures. Examine these factors separately before increasing the iterations; a better adjustment of the same rays does not constitute a new observation of the hidden faces.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Mildenhall et al., NeRF](https://arxiv.org/html/2003.08934v2) –  §4, rendering and transmittance; dimensional calculation, gauge and project protocol. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
