# Review –  SORT –  multiobject tracking by movement and association –  2026-10-30

## Overview

8 enriched flashcards; reference note scope of revision 4 to 5, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | Deduction/Assumption Cases; Documentary Context Below | Causal order: specifies the existing question | Finished core preserved; 222 → 327 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-002 | Deduction/Assumption Cases; Documentary Context Below | Back to the box: specifies the existing question | Finished core preserved; 239 → 354 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-003 | Deduction/Assumption Cases; Documentary Context Below | Merging scalar information: specifies the existing question | Finished core preserved; 212 → 309 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-004 | Deduction/Assumption Cases; Documentary Context Below | Physical duration and issuance: specifies the existing question | Finished core preserved; 229 → 338 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-005 | Deduction/Assumption Cases; Documentary Context Below | Explicit non-assignment: specifies the existing issue | Finished core preserved; 221 → 328 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-006 | Deduction/Assumption Cases; Documentary Context Below | Discriminant Chronology: Specifying the Existing Question | Finished core preserved; 223 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-007 | Deduction/Assumption Cases; Documentary Context Below | Spatial Invariance to IDs: Specifying the Existing Question | Finished core preserved; 219 → 325 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SORT-008 | Deduction/Assumption Cases; Documentary Context Below | Overload policy: specifies the existing issue | Finished core preserved; 228 → 334 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SORT](../../../vault/110-tracking-association/references/111-sort.md); [flashcards](../../../vault/110-tracking-association/111-sort.md). reference note modified before the flashcards.

- **CV-SORT-001 –  Causal order**: For each frame, the prediction advances all states even if the detector provides nothing. The association then compares measures and predicted tracks; only accepted pairs cause a correction. The remaining detections and the remaining trackss finally pass into rules of creation, confirmation, memorization or deletion. Invert correction and association would use a measure whose identity is not yet decided. A useful trace therefore also preserves the non-associations, and not only the couples retained. The internal state of the filter, the ID of track and the box actually emitted are three related but distinct elements of the output contract.

- **CV-SORT-002 –  Back to the box**: with area $s>0$ and report $r=w/h>0$, rebuild $w=\sqrt{sr}$ and $h=\sqrt{s/r}$, then corners $(u\pm w/2,v\pm h/2)$. The positive domains of $s$ and $r$ are therefore essential; a linear extrapolation of the area can produce a non-physical state if it is not managed. For an explicit step $\Delta t$, the center transition becomes $u'=u+\dot u\Delta t$ and $v'=v+\dot v\Delta t$, with speeds now in pixels/s. Adapting only this transition without adapting the process noise and life cycle times still leaves inconsistent time conventions.

- **CV-SORT-003 –  Merging scalar information**: For independent Gaussian errors in this model, the a posteriori variance checks $1/P^+=1/P^-+1/R$. The corrected average can be written as $P^+(u^-/P^-+z/R)$: each estimate is weighted by its precision, inverse of variance. This writing explains the decrease in uncertainty under assumptions, but not a certainty of identity. If the measurement belongs to another object, the probabilistic model used for this merge is violated; announcing a small $P^+$ does not detect it automatically. The gating and the association must therefore precede this interpretation of precision.

- **CV-SORT-004 –  Physical Duration and Issue**: at 30 frames, a maximum age of one frame is approximately 33 ms between regular calls; at 10 images/s, approximately 100 ms. The exact deletion rule and updates still condition the timeline. A stored but not issued track can regain its old ID, while a consumer has not received any boxes during the absence. If the product requires a predicted box during this period, it is another contract that must be defined and evaluated, with a predicted status and appropriate uncertainty. Extending memory does not automatically provide this output or re-identification after expiration.

- **CV-SORT-005 — Non-affectation explicite**: An issue can introduce fictitious rows or columns representing a track without measurement and detection without track, with announced costs. This makes it possible to express that a poor association may be less desirable than a lack of correction. The choice of these costs determines the preference, and is not inferred from the use of Hungarian alone. If the priority objective is the cardinality of the allowable pairs, it must be represented explicitly before distinguishing by similarity. The counterexample of the flashcard therefore does not prescribe a universal formulation: it learns to verify the objective really solved and its temporal consequences.

- **CV-SORT-006 –  Discriminant Chronology**: build an array with time, internal ID, associated detection, age since last correction and issue status. A new track after deleting the old one is not the same event as an exchange between two still active trackss. Replaying the same detections isolates this difference from the detector. If the track was active but the real box has a IoU too low, test prediction, cadence and gating; if two boxes are eligible, examine the complete matrix and assignment objective. This procedure links an intervention to an observed cause and makes it possible to measure the false supports that it can introduce elsewhere.

- **CV-SORT-007 –  Spatial Invariance to IDs**: Renaming the identifiers of all predictions to each frame does not change their boxes or classes. A detection metric calculated image by image can therefore remain exactly the same while identity continuity is destroyed. A ReID representation evaluated on isolated pairs also does not test the exclusivity constraints or the life cycle of a sequence. Constructing this ID permutation as a counterexample makes it possible to verify that the chosen metric penalizes the defect promised by the system. Measuring location, presence and temporal association separately avoids replacing one output with another.

- **CV-SORT-008 –  Overload policy**: Processing all frames in a queue retains the sequence but can continuously increase their seniority if the service throughput is insufficient. Keeping only the most recent one reduces the wait but increases the intervals and movements between calls from the tracker. The two policies simultaneously change the time budget and the conditions of association. Compare them with actual timestamps, same detector and same scene, then measure late decisions, lost tracks and full cost. Acceleration of the single assignment solver may be ineffective if the drop is the decoding or the detector; a step-by-step trace identifies the truly limiting resource.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Bewley et al., SORT](https://arxiv.org/html/1602.00763v2) –  §3, estimation, association and cycle; state calculations, timelines and project protocols. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
