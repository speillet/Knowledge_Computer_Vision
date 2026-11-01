# Review –  Segmentation, inspection and application metrics –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-APPLIQUEES-001 | Project Deduction/Protocol; no new external confirmation claimed | Link and difference of units: specifies the existing question | Finished core preserved; 196 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-APPLIQUEES-002 | Project Deduction/Protocol; no new external confirmation claimed | Weighting by region: specifies the existing question | Finished core preserved; 191 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-APPLIQUEES-003 | Deduction/Assumption Cases; Documentary Context Below | Dimensional propagation: specifies the existing question | Finished core preserved; 193 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-METRIQUES-APPLIQUEES-004 | Project Deduction/Protocol; no new external confirmation claimed | Pre-measured case table: specifies the existing question | Finished core preserved; 192 → 297 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-METRIQUES-APPLIQUEES](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md); [flashcards](../../../vault/130-evaluation-fiabilite/134-metriques-applications.md). reference note modified before the flashcards.

- **CV-METRIQUES-APPLIQUEES-001 –  Link and difference of units**: for two non-empty binary masks under the same count, $Dice=2IoU/(1+IoU)$. These two overlaps are therefore linked for the same pair, while a surface distance uses the geometric positions of the borders and a unit of length. Aggregating the Dice per case is not necessarily equivalent to converting a global IoU by this formula, because the conversion is nonlinear and the weights change. HD95 also requires a precise convention of directions and percentile. The choice of metrics must thus announce both the quantity per pair and the level at which the averages are calculated.

- **CV-METRIQUES-APPLIQUEES-002 –  Weighting by region**: A region-by-region overlap measure can assign to each annotated defect the fraction of its pixels found, and then average those fractions. A fault of 10 pixels then receives the same region weight as a fault of 1 000 pixels, unlike a pooling of all the defective pixels. This convention makes certain small regions visible without solving all the ambiguities of location. An area under a curve must specify the axis of false positives, its range and its normalization. Completing by decision by part and entirely missed defects retains the link with the actual load of rejects and business risks.

- **CV-METRIQUES-APPLIQUEES-003 –  Dimensional propagation**: for a simplified flat measurement $L=s\,p$ with $p$ pixel length and $s$ scale in mm/px, $\delta L\simeq p\delta s+s\delta p$. Under centered independent errors, $\sigma_L^2\simeq p^2\sigma_s^2+s^2\sigma_p^2$; otherwise add covariances. A repeatable location in pixels can therefore coexist with a dominant scale bias. This calculation assumes a plane geometry and a scale adapted, not a perspective camera of any kind. Repeating the measurement and varying the conditions predicted by the study then makes it possible to estimate contributions that the only calibration RMS does not represent.

- **CV-METRIQUES-APPLIQUEES-004 –  Case table defined before measurement**: if both reference and prediction are empty, the denominator of Dice is zero and a convention is required. If only the prediction is empty with present reference, the overlap is zero; if only the reference is empty with present prediction, it is also zero, but the business error is a false positive rather than a missed object. A surface distance may lack a set of points in each of these cases. Keeping counters of these situations and announcing their inclusion or exclusion prevents a filtered epsilon or `NaN` from silently changing the evaluated population.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [NIST, repeatability](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm) –  repeatability analysis; Dice/IoU relationships, region counts, voids, and uncertainty propagation derived by the project. View on 2026-10-30.

Reinke et al.’s Nature page redirects to authentication inaccessible to the tool; this earlier source has not been reconfirmed. The algebraic identities, counts and empty cases of the complement are distinguished from this documentary validation.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
