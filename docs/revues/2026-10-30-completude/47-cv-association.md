# Review –  DeepSORT, ByteTrack and multiobject association –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 1 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | Deduction/Assumption Cases; Documentary Context Below | Two cost geometries: specifies the existing question | Finished core preserved; 184 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ASSOCIATION-002 | Deduction/Assumption Cases; Documentary Context Below | Two uses of the score: specifies the existing question | Finished core preserved; 207 → 315 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-ASSOCIATION-003 | Deduction/Assumption Cases; Documentary Context Below | Separability test: specifies the existing question | Finished core preserved; 186 → 292 words, optional addition | Same addition in reference note; ID/deck/tags retained | minor (reference) | Applied Supplement |
| CV-ASSOCIATION-004 | Deduction/Assumption Cases; Documentary Context Below | Minimum factorial plan: specifies the existing question | Finished core preserved; 195 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-ASSOCIATION](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md); [flashcards](../../../vault/110-tracking-association/112-deepsort-bytetrack.md). reference note modified before the flashcards.

The source of the pedestrian descriptor indicated §2.3; the paper DeepSORT describes it at §2.4. Source of corrected CV-ASSOCIATION-003.

- **CV-ASSOCIATION-001 –  Two Cost Geometry**: in the measurement space, $d_M^2=(z-\hat z)^TS^{-1}(z-\hat z)$ takes into account the predicted covariance $S$; for unitary embeddings, $d_C=1-a^Tb$ describes the angular deviation. The first is without unit after normalization, but does not have the same distribution or the same threshold as the second. High motion uncertainty widens plausible positions; it does not make appearance more discriminating. The waterfall also organizes the priority of the tracks according to their history. Checking costs, eligibility constraints and sequence of steps separately helps to understand what the combination actually brings.

- **CV-ASSOCIATION-002 –  Two uses of the score**: A threshold can be used to decide that an observation is reliable enough to initiate an identity, while allowing less confident observations to extend an already constrained track. These decisions do not have the same false positive cost. If a filter upstream of the detector removes all weak boxes, the second association no longer has the data it is supposed to exploit. So keep the contract thresholds of the entire chain, including NMS and top-k. Testing a real box whose score varies only allows to observe the transitions between priority association, recovery and rejection, without changing its geometry.

- **CV-ASSOCIATION-003 –  Separability test**: build positive pairs of the same piece at several moments and negative pairs of different pieces under comparable conditions. Examine their distance distributions and overlap cases, especially after occlusion. If they overlap strongly, a threshold ReID cannot simultaneously eliminate all false matches and keep all true ones. A gallery contaminated by a bad crop can also make a track permanently close to a distractor. Then check the policy of update of the embeddings, and not just their weight in the cost. Movement or marking can provide additional information that is truly observable.

- **CV-ASSOCIATION-004 — Plan factoriel minimal**: compare association A and B on the same detector D1, then repeat on D2 if we want to study their interaction. The four systems reveal whether an association gain depends on more complete boxes or differently distributed scores. Keep the validation settings separate from the final evaluation. Report loss and recovery events, because an average can hide that a method wins only on sequences without occlusion. The shared detection file must keep timestamps and frame order, including empty frames; removing them changes the time problem instead of only check upstream.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Wojke et al., DeepSORT](https://arxiv.org/html/1703.07402v1) –  §2.2, equations 1 – 4 and gating; §2.4, descriptor. View on 2026-10-30.
- [Zhang et al., ByteTrack](https://arxiv.org/html/2110.06864v3) –  §3, two associations and creation; built protocols. View on 2026-10-30.
- [Bewley et al., SORT](https://arxiv.org/html/1602.00763v2) –  §3, estimation, association and cycle; state calculations, timelines and project protocols. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
