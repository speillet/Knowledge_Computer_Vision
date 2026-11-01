# Review –  Exposure, noise, colour and sampling –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 6 to 7, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Project Deduction/Protocol; no new external confirmation claimed | Model that produces this calculation: specifies the existing question | Finished core preserved; 200 → 315 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ACQUISITION-002 | Deduction/Assumption Cases; Documentary Context Below | Separating Plans: Specifying the Existing Question | Finished core preserved; 329 → 439 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ACQUISITION-003 | Project Deduction/Protocol; no new external confirmation claimed | Built frequency example: specifies the existing question | Finished core preserved; 261 → 377 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ACQUISITION-004 | Deduction/Assumption Cases; Documentary Context Below | Distinguish between normalization and linearization: specifies the existing question | Finished core preserved; 184 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ACQUISITION](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md); [flashcards](../../../vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md). reference note modified before the flashcards.

- **CV-ACQUISITION-001 –  Model that produces this calculation**: for a constant image translation, an ideal $I_0$ image gives a standardized observation $I_b(x)=t_e^{-1}\int_0^{t_e}I_0(x-v_{px}t)\,dt$, with $x$ in pixels, $t$ in seconds and a rectangular exposure of duration $t_e>0$. This is an average over a $|v_{px}|t_e$ length segment: it explains why blurring depends on speed during exposure, not just the number of frames per second. The formula here assumes a unique and neglectful optical direction, noise and saturation. In perspective, two depths can have different image speeds: a blur budget established on the background does not necessarily protect the part.

- **CV-ACQUISITION-002 –  Separating schemes**: noting $N$ as the average of useful electrons, the simplified model becomes $SNR=N/\sqrt{N+\sigma_d^2}$ when the quantification is negligible. At low $N$, the denominator varies little and doubling the photons can almost double the SNR; at large $N$, it grows as $\sqrt N$ and the gain tends towards $\sqrt2$. For a defect, also examine the contrast between defect and background: illuminating more can saturate the background before obtaining the necessary contrast. An analog gain placed before certain noise sources can have a different real behavior than a simple digital scale change; the model and measurements must specify the stage concerned.

- **CV-ACQUISITION-003 –  Built frequency example**: A sine wave of frequency 0,4 cycle per pixel of origin exceeds the limit of 0,25 for a reduction of a factor of two. After decimation, it corresponds to 0,8 cycle per final pixel, indistinguishable on this grid with a folded frequency of 0,2 cycle per final pixel. The observed pattern is therefore an ambiguity of sampling, not a real movement. The prefilter must attenuate beyond the new Nyquist frequency before discarding the samples. Its support depends on the reduction factor; keeping only the name "bilinear" does not fully describe this treatment. This reasoning is an analytic case on a sinusoid, not a result on the network.

- **CV-ACQUISITION-004 –  Distinguish normalization and linearization**: Divide a value sRGB by 255 places it in a numeric range; this does not remove its transfer curve. For a normalized sRGB component $c>0,04045$, its relative linear value is $c_{lin}=((c+0,055)/1,055)^{2,4}$. Thus, $c=0,5$ represents about 0,214 in linear, and not 0,5. Applying this conversion to an already linear input would be another mistake. Document successively decoding, channel order, photometric transfer, resize and then standardization of the tensor. An equality of form or of minimum/maximum does not demonstrate the equality of the intermediate values or their physical sense.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) –  §§2.4, 2.6 – 2.7, signal, SNR and saturation. View on 2026-10-30.
- [sRGB, ICC interpretation](https://www.w3.org/Graphics/Color/srgb) –  §§A.8 and B.1, transfer function and reverse. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
