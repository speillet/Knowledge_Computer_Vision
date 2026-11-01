# Review –  OCR and documentary understanding –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | Deduction/Assumption Cases; Documentary Context Below | Example of weighting: specifies the existing question | Finished core preserved; 193 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-OCR-002 | Deduction/Assumption Cases; Documentary Context Below | Calculation of distance: specifies the existing question | Finished core preserved; 197 → 310 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-OCR-003 | Deduction/Assumption Cases; Documentary Context Below | Order model: specifies the existing question | Finished core preserved; 188 → 293 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-OCR](../../../vault/70-reconnaissance-representations/references/74-ocr-documents.md); [flashcards](../../../vault/70-reconnaissance-representations/74-ocr-documents.md). reference note modified before the flashcards.

- **CV-OCR-001 –  Example of weighting**: A document of 2 000 characters with a substitution on the total amount may have a CER of 0,05% and remain unusable for accounting processing. A field metric can compare the numerical value after a predicted normalization of separators, currencies, and decimals; a document metric can require all the correct critical fields. Also keep the raw string and image region allows to distinguish recognition error, field association and normalization. Arithmetic checks between lines, taxes and totals provide additional consistency, without proving that a plausible value actually corresponds to that printed.

- **CV-OCR-002 –  Calculation of distance**: Dynamic programming uses $D_{i,j}=\min(D_{i-1,j}+1,D_{i,j-1}+1,D_{i-1,j-1}+\mathbf1[a_i\ne b_j])$, with $D_{i,0}=i$ and $D_{0,j}=j$ edges. It looks for the minimum editing cost, not a simple count of different fixed-position characters. To aggregate several pages, the ratio $\sum_k(S_k+D_k+I_k)/\sum_kN_k$ weights by reference length, while the average of CER per page weights the pages as well. Both answer different questions. Defining Unicode units and processing empty references before this calculation avoids incompatible score comparisons.

- **CV-OCR-003 –  Order template**: represent regions as nodes and relationships "must be read before" as edges allows to explain a partial order. Topological sorting produces a compatible order if these constraints are cycle-free; column rules, arrays, and inserts determine edges, not the confidence of the recognizer. A simple global sorting by height can intertwine two well-detected columns. To locate the fault, successively compare reference regions, reference transcriptions and reference order by replacing only one output at a time. This ablation identifies what each component brings to the final document error.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OCR-D](https://ocr-d.de/en/spec/ocrd_eval.html) –  Text Evaluation, distance from Levenshtein, CER/WER; examples and order model built. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
