# Review –  FAST and BRIEF –  detect a corner and then describe its vicinity –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 2 to 3, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 1 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FAST-BRIEF-001 | Deduction/Assumption Cases; Documentary Context Below | Building an unambiguous test: specifies the existing question | Finished core preserved; 222 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FAST-BRIEF-002 | Deduction/Assumption Cases; Documentary Context Below | Stability of a bit: specifies the existing question | Finished core preserved; 200 → 314 words, optional addition | Same addition in reference note; ID/deck/tags retained | minor (reference) | Applied Supplement |
| CV-FAST-BRIEF-003 | Deduction/Assumption Cases; Documentary Context Below | Separate learned and calculated parameters: specifies the existing question | Finished core preserved; 201 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FAST-BRIEF-004 | Deduction/Assumption Cases; Documentary Context Below | Compensation expected: clarifies the existing question | Finished core preserved; 220 → 327 words, optional addition | Same addition in reference note; ID/deck/tags retained | minor (reference) | Applied Supplement |
| CV-FAST-BRIEF-005 | Deduction/Assumption Cases; Documentary Context Below | Linking accuracy and robust cost: specifies the existing question | Finished core preserved; 206 → 318 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FAST-BRIEF](../../../vault/40-features-matching/references/47-fast-brief.md); [flashcards](../../../vault/40-features-matching/47-fast-brief.md). reference note modified before the flashcards.

The BRIEF tests and smoothing were attributed to the §2; the passage consulted describes them in the §3. reference note and the flashcards in question have been corrected without changing their purpose.

- **CV-FAST-BRIEF-001 –  Build an unambiguous test**: For a circle of 16 neighbors, code each position as light, dark or similar to the center depending on the threshold. Look for a fairly long contiguous sequence, taking into account the connection between the last and the first position of the circle; a naive implementation can double the sequence to verify this connection. This description is a logical pseudocode, not a benchmark program. Rapid tests of a subset of positions may reject some candidates before the full test, depending on the variant. A lower threshold makes more differences compatible with an arc, but also changes the noise sensitivity; choose the threshold in the effective intensity unit.

- **CV-FAST-BRIEF-002 –  Stability of one bit**: The $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$ test is particularly fragile if the $I_s(y_j)-I_s(x_j)$ difference is close to zero. A low noise can then return the bit, even if the patch represents the same point. Smoothing reduces some fluctuations but can remove the distinctive detail. Adding highly correlated bits does not provide as much information as complementary comparisons. Hamming's distance does not tell what disagreements arise from noise, rotation, or other object: it is the data and protocol that determine its interpretation. A threshold relating to the number of bits is not automatically a match probability.

- **CV-FAST-BRIEF-003 –  Separate learned and calculated parameters**: in a ORB assembly, the selection of binary comparisons aims at informative and little redundant tests on learning data; at the extraction of a new image, the orientation and answers of these tests are calculated around each point. This is not an online trained network on the observed part. A BRIEF with a fixed pattern can share the same storage without sharing this selection or the orientation compensation. To compare two strings, record the pattern, support, smoothing and sampling coordinates; the name of the detector does not identify the descriptor that was produced.

- **CV-FAST-BRIEF-004 –  Compensation expected**: If a patch is rotated by $R_\theta$, the positions of the two readings of a test must undergo a consistent transformation, or the patch must be resampled in a canonical coordinate frame before comparison. The first strategy rotates the pattern, the second transforms the local image; their interpolations and edges may differ. With an exact known rotation, they give a discriminating experience to isolate the absence of orientation. With an estimated orientation, its noise becomes a new cause of binary disagreement. An improvement in this ablation does not demonstrate an invariance in perspective: anisotropic deformation is not compensated by a single angle.

- **CV-FAST-BRIEF-005 –  Connecting Accuracy and Robust Cost**: for a minimum solver of size $s$ and a rate of inliers $w$, the nominal number of prints RANSAC with confidence $p$ is $N\ge\log(1-p)/\log(1-w^s)$ under independent and non-degenerate prints. A cheaper extraction but producing a lower $w$ can therefore greatly increase the cost of geometry. This calculation is an analytical model, not an exact latency prediction: stop, degeneration and repetition variants change the actual behavior. Also measure the time and memory for failures, where the maximum budget can be consumed, instead of only timing the easy pairs correctly registered.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13, FAST](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html) –  segment testing and deletion of non-maxima; folding after timeout of the author PDF. View on 2026-10-30.
- [Calonder et al. 2010, BRIEF](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf) –  §3, tests, smoothing and patterns. View on 2026-10-30.
- [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) –  rBRIEF orientation and selection. View on 2026-10-30.

The Rosten – Drummond PDF expired during this pass; the FAST test was confronted with the official OpenCV tutorial. The PDF BRIEF is accessible.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
