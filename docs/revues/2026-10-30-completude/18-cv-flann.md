# Review –  FLANN –  close search and distance contract –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLANN-001 | Deduction/Assumption Cases; Documentary Context Below | What the Index Costs: Specifying the Existing Question | Finished core preserved; 207 → 321 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLANN-002 | Deduction/Assumption Cases; Documentary Context Below | Standardization and metric form a contract: specifies the existing question | Finished core preserved; 221 → 334 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLANN-003 | Deduction/Assumption Cases; Documentary Context Below | Inverse case not to be forgotten: specifies the existing question | Finished core preserved; 209 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FLANN-004 | Deduction/Assumption Cases; Documentary Context Below | Read a quality-cost curve: specifies the existing question | Finished core preserved; 206 → 322 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FLANN](../../../vault/40-features-matching/references/48-flann.md); [flashcards](../../../vault/40-features-matching/48-flann.md). reference note modified before the flashcards.

- **CV-FLANN-001 –  What does the index cost**: a forest of kd-trees divides vectors by coordinates; a search follows promising regions and then explores other branches according to a budget. A hierarchical k-mean tree partitions rather by group centers. Stopping early explains both the labor economy and the lack of an accurate general neighbor guarantee. In the time model already built, the damping threshold checks $2+0,001N_q<0,003N_q$, so $N_q>1000$; at a thousand queries the costs are equal. This threshold depends entirely on the assumed costs. Any reconstruction, additional transfer or change in the budget must be reinstated before concluding that the index is of interest.

- **CV-FLANN-002 –  Standardization and metric form a contract**: for real unit vectors $a,b$, $\|a-b\|_2^2=2-2a^Tb$ connects L2 and cosine similarity. This equivalence requires normalization and does not extend to bytes encoding ORB bits. Even for real vectors, changing their normalization after index construction can change neighbors and invalidate the setting. Keeping the extractor, its version/configuration, the dimension and the expected metric with the base makes it possible to detect these incompatibilities before the matching. A type conversion is sometimes necessary for an API; it must preserve the desired mathematical representation, and is not used to bypass an incompatible distance contract.

- **CV-FLANN-003 –  Inverse case not to be forgotten**: Missing the best neighbor can also make the ratio less favorable or make another candidate accept; the search error does not have a single direction on the final decision. The call@1 measures only if the first exact neighbor is found. For a filter using two neighbors, also measure the recall of the set of the two best and the agreement of the filtering decision. Ex-æquo require a convention: several clues can have the same distance and make an identity comparison too severe. An exhaustive reference must therefore announce metric, numerical precision and equality rule, and then remain the same for all budgets evaluated.

- **CV-FLANN-004 –  Read a quality – cost curve**: an operating point dominates another if it retains at least the useful quality by costing less depending on the resources considered. Between undominated points, the choice depends on the budget and tolerance produced, not on a single universal score. Separating build time, query latency, memory, and update frequency from the base avoids masking a misplaced extra cost. Testing queries without a real match is also essential: a neighbor search will usually return someone even if the correct answer is "absent". The rejection of pairs and the geometric verification define this possibility of refusal, which the only reminder of the neighbors does not measure.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Muja and Lowe 2009](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf) –  §§3.1 – 3.3, structures, budget and configuration. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
