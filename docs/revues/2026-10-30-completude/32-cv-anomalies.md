# Review –  Inspection: golden template, PatchCore and PaDiM –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ANOMALIES-001 | Deduction/Assumption Cases; Documentary Context Below | Distance geometry: specifies the existing question | Finished core preserved; 191 → 297 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ANOMALIES-002 | Deduction/Assumption Cases; Documentary Context Below | Greedy selection: specifies the existing question | Finished core preserved; 183 → 286 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ANOMALIES-003 | Project Deduction/Protocol; no new external confirmation claimed | Matched experience: specifies the existing question | Finished core preserved; 189 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ANOMALIES-004 | Project Deduction/Protocol; no new external confirmation claimed | Translation in industrial load: specifies the existing question | Finished core preserved; 214 → 319 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ANOMALIES](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md); [flashcards](../../../vault/70-reconnaissance-representations/73-patchcore-padim.md). reference note modified before the flashcards.

- **CV-ANOMALIES-001 –  Geometry of distance**: In PaDiM, a direction of high nominal variance is less penalized by the Mahalanobis distance than a direction of low variance. Covariance is therefore not only used to change the global scale; it also represents correlations between features. When there are few observations relative to their size, regularizing $\Sigma$ for example with a diagonal term is necessary to avoid an unstable inversion, under a documented choice. A pixel template can be more interpretable but very sensitive to registration. Comparing the three approaches thus imposes of check both the spatial coordinate frame and the representation of the acceptable variations.

- **CV-ANOMALIES-002 –  Greedy selection**: After a defined initialization, a hedging policy chooses the nominal point currently furthest from its neighbor in the subset already selected. It thus seeks to cover the space of features rather than to keep only the frequent examples. The paper uses a projection to speed up the selection; the approximation must remain distinguished from a perfect cover. With $m$ features of dimension $d$ stored on $b$ bytes, the bank alone costs about $mdb$ bytes, excluding indexes. Reducing $m$ acts directly on this storage, but searching, extracting, and transferring memory can limit full latency differently.

- **CV-ANOMALIES-003 –  Matched Experience**: Pick up the same compliant parts before and after the light change and compare their scores by region. Then do the same for known defects. This makes it possible to study the displacement of the nominal and the separation between conformity and defect, instead of arbitrarily moving an overall threshold. If the two populations get closer, restoring the rate of false releases by increasing the threshold can greatly degrade the recall of defects. Documenting also exposure, saturation and white balance: a normalization of features does not recover visual information lost in saturated pixels. The result must be checked on other parts and lots.

- **CV-ANOMALIES-004 –  Translation in industrial load**: at a rate of $\lambda$ pieces/s and average processing time $T$ s/piece, a service capacity of less than $\lambda$ accumulates a queue even with a good detection score. For the point of operation, report false discharges among the conformants, missed defects among the defectives and number of batch checks. Zero defects missed on a small sample does not prove a zero rate: the size of the test and the diversity of defects limit the conclusion. Defining set-aside sets and critical cases before threshold setting connects the learning metrics to the actual process being evaluated.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Defard et al., PaDiM](https://arxiv.org/html/2011.08785v1) –  §III-B, equation 1, covariance and regularization; geometric interpretation deduced. View on 2026-10-30.
- [Roth et al., PatchCore](https://arxiv.org/html/2106.08265v2) –  §3.2, Algorithm 1, gluton selection; scenarios and cost calculations of the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
