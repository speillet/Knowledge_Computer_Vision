# Review –  PTQ, QAT, INT8/FP8 and runtimes –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Deduction/Assumption Cases; Documentary Context Below | Simulation and gradients: specifies the existing question | Finished core preserved; 199 → 307 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-QUANT-002 | Deduction/Assumption Cases; Documentary Context Below | Rounding and clipping error: specifies the existing question | Finished core preserved; 192 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-QUANT-003 | Deduction/Assumption Cases; Documentary Context Below | declared graph and executed graph: specifies the existing question | Finished core preserved; 183 → 287 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-QUANT-004 | Deduction/Assumption Cases; Documentary Context Below | Net engine gain: specifies the existing question | Finished core preserved; 209 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-QUANT-005 | Deduction/Assumption Cases; Documentary Context Below | Memory and discontinuous thresholds: specifies the existing question | Finished core preserved; 194 → 299 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-QUANT](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md); [flashcards](../../../vault/140-ingenierie-systemes/142-quantification-runtimes.md). reference note modified before the flashcards.

- **CV-QUANT-001 –  Simulation and gradients**: The rounding of quantification is constant in pieces and does not directly provide a useful gradient almost everywhere. A QAT therefore uses a suitable learning approximation, often a substitution gradient in the variants concerned, while simulating rounding and forward saturation. The simulated schema must match the scales, granularities and bounds expected at the inference. A static PTQ estimates these parameters without this weight adjustment. Comparing the two requires freezing the final digital contract: training with a simulation and then exporting another schema can cancel the expected interest. No better quality or universal acceleration comes from the name QAT alone.

- **CV-QUANT-002 –  Rounding and clipping error**: with a uniform quantification of steps $s$ and rounded to the nearest, the reconstruction error out of saturation is at most $s/2$, under the announced convention. In saturation, this limit no longer applies: an activation far beyond the range can be strongly clipped. Expanding the range reduces this risk but increases $s$ for a set number of levels. A granularity per channel allows different scales when the amplitudes differ strongly between channels, at the price of the constraints of the backend. Measuring the actual distributions and output errors makes it possible to choose this compromise without assuming that the maximum range observed is always optimal.

- **CV-QUANT-003 –  Declared graph and executed graph**: A Q/DQ representation can materialize conversions between quantized and reconstructed values; the runtime then decides which sequences to merge and which kernels to use according to its target. Their presence in a file does not prove that each operation is accelerated in its entirety. A partition between multiple resources can add copies, synchronizations, and conversions. First compare digital outputs on control inputs, then decision quality on reserved data and finally performance under load. Set appropriate tolerances for output, as a small logit difference can change a detection or deletion close to a threshold.

- **CV-QUANT-004 –  Net engine gain**: If a floating calculation takes $T_f$, a quantified $T_q$ calculation and additional $T_c$ conversions, the local gain already requires $T_q+T_c<T_f$, before other system costs. Small layers can be dominated by launch or conversion rather than multiplication. Comparing the actual trace reveals whether the lack of gain comes from an unchanged engine, a new extra cost or a dominant outdoor stage. The dynamic shapes and the batch must remain comparable. A theoretical measurement of file size or number of operations does not replace this decomposition of the time actually observed.

- **CV-QUANT-005 –  Memory and discontinuous thresholds**: For a tensor of $n$ values on $b$ bytes, raw storage is $nb$, but multiple copies, activations, and workspaces can coexist. Quantifying only the weights does not divide the whole memory peak by the same factor. On the quality side, a score that goes from 0,501 to 0,499 around a threshold 0,5 can remove a box despite a small numerical error. A change in rank can also change a NMS. Comparing both tensor errors, output after postprocessing and business metrics by size reveals these effects as the numerical error average masks.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Jacob et al., quantification](https://arxiv.org/html/1712.05877v1) –  §3.1, quantification simulation and Algorithm 1; general comment on the substitution gradient without backend guarantee. View on 2026-10-30.
- [ONNX Runtime, quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html) –  Quantization Overview, Q/DQ and Quantization Debugging; digital terminals and project scenarios, page consulted on the 2026-10-30. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
