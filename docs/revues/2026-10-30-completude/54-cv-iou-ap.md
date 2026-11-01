# Review –  IoU and AP –  COCO detection protocol –  2026-10-30

## Overview

7 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Deduction/Assumption Cases; Documentary Context Below | Calculation of the sides: specifies the existing question | Finished core preserved; 212 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-002 | Deduction/Assumption Cases; Documentary Context Below | Ranking and confidence: specifies the existing question | Finished core preserved; 240 → 342 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-003 | Deduction/Assumption Cases; Documentary Context Below | Effect of a Late Duplicate: Specify the Existing Question | Finished core preserved; 218 → 323 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-004 | Deduction/Assumption Cases; Documentary Context Below | Envelope algorithm: specifies the existing question | Finished core preserved; 225 → 334 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-005 | Deduction/Assumption Cases; Documentary Context Below | First observable disagreement: clarifies the existing question | Finished core preserved; 228 → 333 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-006 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Sensitivity to translation: specifies the existing question | Finished core preserved; 219 → 317 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IOU-AP-007 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Prevalence and burden of false releases: specifies the existing question | Finished core preserved; 226 → 331 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-IOU-AP](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md); [flashcards](../../../vault/130-evaluation-fiabilite/131-iou-ap-coco.md). reference note modified before the flashcards.

- **CV-IOU-AP-001 –  Calculation of sides**: in continuous coordinates, the intersection width is $\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B}))$, and the height follows the same formula in $y$. Their product gives the intersected area. An invertible affine transformation applied to both regions multiplies their areas by the same absolute determinant and retains their geometric IoU. Warning: if a rotation is followed by the replacement of the regions by their encompassing rectangles aligned on the axes, the regions have been changed and this invariance no longer applies automatically. The form contract is as important as the contact information.

- **CV-IOU-AP-002 –  Ranking and confidence**: a set of fixed predictions, without filtering depending on the score and with the same tie-breaking, a strictly increasing common transformation of the scores retains their order and therefore the AP of ranking. However, it can change the number of outputs at the digital production threshold. This shows why AP and calibration of scores are distinct. Conversely, a differently applied transformation between images can change the overall classification of a category and its AP. Keep the scope of the postprocessing and any prediction limits in this analysis: the upstream rules may invalidate the set hypothesis.

- **CV-IOU-AP-003 –  Effect of a late duplicate**: for a single GT and a list TP then FP, the recall reaches 1 from the first detection and the interpolated accuracy can remain perfect on all levels of recall of this simple case. Duplicate is still a false positive if the operating threshold retains it. For TP, FP, TP on two GT, the duplicate appears before the recovery of the second object and can degrade part of the envelope. The position of the FP therefore explains its effect on the AP; it does not change its concrete cost in a counting or rejection system.

- **CV-IOU-AP-004 –  Envelope algorithm**: After stacking TP and FP, go through the accuracy from right to left and replace each value with the maximum between it and the next. For each recall requested, then take the first level reached to its right according to the rules of the evaluator, or zero if it is not reached. This procedure explains the 51 levels included up to 0,50 in the case built. It differs from an arbitrary trapezoidal integration of three points. Categories without valid GT and ignored annotations follow other rules, so a ranking example is not a complete COCO re-implementation.

- **CV-IOU-AP-005 –  First observable disagreement**: compare first the sets of images and categories, then the ordered lists retained by image, then the statuses TP/FP/ignore at each threshold. If these elements are identical, then look for accumulation, interpolation and averages. This progress avoids debugging a final average when the tools have not evaluated the same objects. Keep fingerprints of GT files and results, parameters, and code version in the report. Two outputs displayed with the same AP label can come from different wrapper filters; only the trace of the actual inputs and the matches can accurately assign the deviation.

- **CV-IOU-AP-006 –  Sensitivity to translation**: for two side squares $a$ horizontally offset from $\delta$ with $0\le\delta<a$, the IoU is $(a-\delta)/(a+\delta)$. To stay above a threshold $\tau$, you need $\delta<a(1-\tau)/(1+\tau)$ if the comparison is strict. At $\tau=0,75$, this represents about $0,143a$; an error of 2 px therefore strongly penalizes a box of 10 px side. This constructed calculation does not point to the cause, but justifies the analysis by size and the check of the pretreatment curves and offsets before a new drive.

- **CV-IOU-AP-007 –  Prevalence and burden of false discharges**: In a binary model, if the defects have a prevalence of $\pi$, a recall of $r$ and a false positive rate of $f$ among the conformants, the accuracy of the alerts is $r\pi/[r\pi+f(1-\pi)]$. For $\pi=0,001$, $r=0,99$ and $f=0,01$, it is about 9%. This constructed case explains why a small proportion of false positives can saturate the review when defects are rare. The benchmark AP does not directly provide this load: it requires the operating threshold, the actual frequencies and the costs of the errors useful to the product.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [COCO, pinned code](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py) –  evaluateImg and accumulate; invariances and geometric/probability examples constructed. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
