# Review –  ORB –  detection and binary oriented descriptor –  2026-10-30

## Overview

6 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | Deduction/Assumption Cases; Documentary Context Below | Calculate orientation: specifies the existing question | Finished core preserved; 216 → 328 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ORB-002 | Deduction/Assumption Cases; Documentary Context Below | Computable version of Hamming: specifies the existing question | Finished core preserved; 219 → 328 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ORB-003 | Deduction/Assumption Cases; Documentary Context Below | What the Winner Codes: Specifying the Existing Question | Finished core preserved; 217 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ORB-004 | Deduction/Assumption Cases; Documentary Context Below | Example of non-equivalent filter: specifies the existing question | Finished core preserved; 220 → 331 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ORB-005 | Deduction/Assumption Cases; Documentary Context Below | Scale and cost coverage: specifies the existing question | Finished core preserved; 229 → 347 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ORB-006 | Deduction/Assumption Cases; Documentary Context Below | Establishing a concrete memory budget: clarifies the existing question | Finished core preserved; 227 → 335 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ORB](../../../vault/40-features-matching/references/42-orb.md); [flashcards](../../../vault/40-features-matching/42-orb.md). reference note modified before the flashcards.

- **CV-ORB-001 –  Calculate orientation**: In a keypoint-centric patch, set the $m_{pq}=\sum_{x,y}x^py^qI(x,y)$ moments. The direction to the centroid is obtained by $\theta=\operatorname{atan2}(m_{01},m_{10})$ when these moments give an actionable direction. The pattern of comparisons is then rotated according to $\theta$ before the intensity readings. If the patch is almost symmetrical or noisy, a small disturbance can strongly change this orientation: the position can remain repeatable without the tests describing the same oriented neighborhood. The edges of the patch and the actual presence of the required pixels must also be managed, not silently supplemented by unrelated content.

- **CV-ORB-002 –  Computable version of Hamming**: for two binary suites $a,b$, $d_H(a,b)=\operatorname{popcount}(a\oplus b)$ adds the disagreements between tests. The operations are machine words or bytes, but the result does not depend on the numerical weight of the bits. A change in the placement of the same tests in the bytes therefore retains Hamming if applied to both descriptors; it can completely change L2 on the byte values. This reasoning gives a simple implementation check, without an image: build two patterns of which a single test differs in several positions. The expected distance remains one, which separates metric storage and metric representation.

- **CV-ORB-003 –  What the Winner Codes**: for each group of $K$ positions, the result indicates the index of the position of maximum intensity. With three or four candidates, the two bits are a categorical symbol, not two independent binary questions. The `00→01` and `00→11` disagreements must therefore count each for a different symbol. This logic explains why the change also requires reconstructing a persistent descriptor base: the same table length does not guarantee the same semantics. Also check that the approximate search index supports this metric; a correct norm in an exhaustive matcher does not automatically validate all binary indexes.

- **CV-ORB-004 –  Example of non-equivalent filter**: In a built-up distance matrix, request A can have candidates with distances 10 and 11; the former also prefers it to all other requests. The cross-check accepts it, while a ratio of 0,8 rejects it. A request B may have 10 and 30, but its best candidate prefers A: the ratio accepts it and reciprocity rejects it. These cases show that the two rules pose different questions. One can design an explicit combination, at the cost of additional calculations and reminders; it must define what to do with ex æquo and absent candidates, and then be geometrically validated.

- **CV-ORB-005 –  Scale and cost coverage**: with a pyramid factor $s>1$, a detail of size $r$ pixels at the initial level covers about $r/s^\ell$ pixels at the $\ell$ level. Increasing the number of levels extends the scales examined; reducing $s$ samples them more finely but increases the work for the same range. No level restores an already undersampled detail in the input image. In a constructed case, a three-pixel-wide tag reduced to one pixel no longer offers the same intensity tests, even if its overall position remains known. The detection thresholds and quotas distributed between levels must therefore be analysed with the resolution actually available on the target.

- **CV-ORB-006 –  Establishing a concrete memory budget**: In the current OpenCV variant at 256 bits, a descriptor occupies 32 bytes; 2000 descriptors represent about 64 kB of raw data. This excludes keypoints, pyramid images, buffers, indexes, allocations, and program structures: this calculation is not a measure of memory peak. An exhaustive search between two sets of $n$ and $m$ points processes $nm$ pairs, even with a fast binary distance. Preparing behavior when there are no descriptors or too few pairs for the model prevents a speed optimization from turning a normal observation failure into an arbitrary result or execution error.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) –  Theory and WTA_K. View on 2026-10-30.
- [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) –  norms, cross-check and knnMatch; verified with Context7. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
