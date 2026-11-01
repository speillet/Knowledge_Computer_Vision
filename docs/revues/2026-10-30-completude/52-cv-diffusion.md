# Review –  VAE, GAN and broadcast for generation/restoration –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DIFFUSION-001 | Deduction/Assumption Cases; Documentary Context Below | Noise target: specifies the existing question | Finished core preserved; 210 → 314 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DIFFUSION-002 | Deduction/Assumption Cases; Documentary Context Below | Spatial assessment: clarifies the existing question | Finished core preserved; 190 → 295 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-DIFFUSION-003 | Project Deduction/Protocol; no new external confirmation claimed | Non-unique inverse problem: specifies the existing question | Finished core preserved; 197 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-DIFFUSION](../../../vault/120-generatif-multimodal/references/122-generation-restauration.md); [flashcards](../../../vault/120-generatif-multimodal/122-generation-restauration.md). reference note modified before the flashcards.

- **CV-DIFFUSION-001 –  Noise target**: In the current DDPM parameterization, draw a level $t$ and a noise $\epsilon$, build $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, then minimize an error in predicting this noise. With this convention, an estimate of the clean image can be written $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))/\sqrt{\bar\alpha_t}$. This relationship alone is not a complete sampler: transitions, variances, levels traveled and conditioning remain to be defined. Other settings predict another target. Naming the one used avoids applying an output interpretation formula to the wrong tensor.

- **CV-DIFFUSION-002 — Bilan spatial**: If the encoder reduces each image dimension by a factor of $f$, the latent grid has about $HW/f^2$ positions, with a different number of channels. This reduction alone does not predict time savings, as decoder, attention and iterations have their own costs. Note $\tilde x=D(E(x))$ and compare $x$ to $\tilde x$ isolates the reconstruction of the autoencoder before diffusion. Specially evaluate structures smaller than the effective compression support. A good average reconstruction can preserve the large shapes while modifying a rare detail that the product precisely seeks to measure.

- **CV-DIFFUSION-003 –  Non-unique inverse problem**: If the acquisition is $y=Hx+n$, multiple high-resolution $x$ images can produce almost the same $y$ when $H$ loses high frequencies. For a detail $\delta$ such as $H\delta\simeq0$, $x$ and $x+\delta$ are difficult to distinguish from the measurement. The generative model then chooses with its learned preferences, without proof that the crack added or removed is real. Consistency $H\hat x\simeq y$ is useful but insufficient to validate the details of the poorly observed kernel. This derivation explains why keeping the raw measurement and a physical reference remains essential for inspection.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Ho et al., DDPM](https://arxiv.org/html/2006.11239v2) –  Algorithm 1 – 2 and §3.2, noise prediction; project algebraic inversion. View on 2026-10-30.
- [Rombach et al., Latent Diffusion](https://arxiv.org/html/2112.10752v2) –  §3.1, compression and reconstruction; spatial balance and inverse problem deduced. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
