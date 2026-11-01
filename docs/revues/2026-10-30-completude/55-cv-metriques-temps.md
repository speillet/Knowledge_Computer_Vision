# Review –  Evaluate identities, trajectories and location 3D –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Deduction/Assumption Cases; Documentary Context Below | Decomposition of monitoring: specifies the existing question | Finished core preserved; 185 → 295 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-TEMPS-002 | Deduction/Assumption Cases; Documentary Context Below | Average and covariance of components: specifies the existing question | Finished core preserved; 195 → 291 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-TEMPS-003 | Deduction/Assumption Cases; Documentary Context Below | Authorized processing: specifies the existing question | Finished core preserved; 194 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-TEMPS-004 | Deduction/Assumption Cases; Documentary Context Below | Explicit relative error: specifies the existing question | Finished core preserved; 184 → 284 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-TEMPS-005 | Deduction/Assumption Cases; Documentary Context Below | Interpolation and Time: Specifying the Existing Question | Finished core preserved; 182 → 284 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-METRIQUES-TEMPS](../../../vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md); [flashcards](../../../vault/130-evaluation-fiabilite/132-tracking-trajectoires.md). reference note modified before the flashcards.

- **CV-METRIQUES-TEMPS-001 –  Decomposition of monitoring**: An absence of a box on the right target is a detection error, while a correct box with a bad ID is the association according to the protocol. Fragmentation divides a real identity into several predicted trackss; merging identities links several objects to a track. A simple number of switches does not necessarily describe their duration or all these relationships. Building the same boxes with multiple ID schemes allows you to check what each metric penalizes. Presenting components and temporal examples helps explain the gain of a tracker instead of classifying two systems on a single scalar.

- **CV-METRIQUES-TEMPS-002 –  Average and covariance of components**: for positive $D_k,A_k$, Cauchy – Schwarz gives $\frac1n\sum_k\sqrt{D_kA_k}\le\sqrt{(\frac1n\sum_kD_k)(\frac1n\sum_kA_k)}$. Reconstructing the score from the average components can therefore overestimate the average of the combinations per threshold. Equality requires a compatible ratio between sequences, with zeros being processed. This algebraic property applies to the level of aggregation considered; the other means between classes or sequences have their own conventions. The numerical counter-example of the flashcard demonstrates this order of operations, without claiming to represent feasible components of a particular benchmark.

- **CV-METRIQUES-TEMPS-003 –  Authorized processing**: a similarity written $p'=sRp+t$ and has a freedom of scale $s$ absent from a rigid transformation. If a metric estimate is everywhere $\hat p=2p$, choose $s=1/2$ removes this error entirely in an ideal case. For a system with only one global origin and one global yaw, the alignment must preserve the other physical information that you want to test. Document the adjusted parameters and report, if useful, the estimated scale factor as a separate diagnosis. Do not confuse correction of coordinate frame and correction of a property that the system was precisely supposed to provide correctly.

- **CV-METRIQUES-TEMPS-004 –  Explicit relative error**: for poses bodies→world $T_i$ real and $\hat T_i$ estimated, form $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$. The ideal is identity. Report standard translation and angle of rotation with the chosen interval $i,j$. A common global coordinate frame transformation cancels out in relative displacements, while a drift between moments persists. An interval set in frames is not a fixed interval in seconds if the cadence varies. This formula and its conventions must accompany the name RPE for a result to be interpretable and reproducible.

- **CV-METRIQUES-TEMPS-005 –  Interpolation and time**: A trajectory sampled at different times of the reference requires a matching or announced interpolation. Interpolating a translation is different from directly interpolating the components of a rotation matrix, which can then leave $SO(3)$. A constant time shift produces a speed-dependent error and can be mistaken for a wrong trajectory. Testing a synthetic movement at known speed with an imposed offset allows to verify this signature. Also keep the number of poses excluded by time tolerance: a drop in error obtained by removing difficult segments does not measure the same coverage.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Luiten et al., HOTA](https://arxiv.org/html/2009.07736v2) –  §5, threshold combination; inferred aggregation inequality. View on 2026-10-30.
- [Zhang–Scaramuzza](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) –  §IV, ATE and relative error; RPE formula and time controls explained by the project. View on 2026-10-30.

The URL HOTA HTML v3 returned 404; the v2 and the Zhang – Scaramuzza PDF were consulted. Aggregation inequality is an algebraic deduction, not a result on a tracker.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
