# Review –  Clouds, BEV and Occupational Representations –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BEV-001 | Deduction/Assumption Cases; Documentary Context Below | Cost of discretization: specifies the existing question | Finished core preserved; 188 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BEV-002 | Deduction/Assumption Cases; Documentary Context Below | Radius model: specifies the existing question | Finished core preserved; 193 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BEV-003 | Deduction/Assumption Cases; Documentary Context Below | Surface and units: specifies the existing question | Finished core preserved; 194 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BEV-004 | Deduction/Assumption Cases; Documentary Context Below | Aligning history: clarifies the existing question | Finished core preserved; 186 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BEV-005 | Deduction/Assumption Cases; Documentary Context Below | Testable grid contract: specifies the existing question | Finished core preserved; 222 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-BEV](../../../vault/60-vision-3d/references/64-nuages-bev-occupation.md); [flashcards](../../../vault/60-vision-3d/64-nuages-bev-occupation.md). reference note modified before the flashcards.

- **CV-BEV-001 –  Cost of discretization**: for a range $L_x\times L_y\times L_z$ and cells $\Delta x,\Delta y,\Delta z$, a dense volume contains about $(L_x/\Delta x)(L_y/\Delta y)(L_z/\Delta z)$ cells. Divide each step by two multiplies their number by eight; a horizontal grid alone is multiplied by four. The actual memory still depends on the channels, the precision and the sparse representation. The horizontal index of a point can be $i=\lfloor(x-x_{\min})/\Delta x\rfloor$ with out-of-ROI rejection. Defining this rounding and the convention of the terminals avoids the shifts of a cell between labels, sensors and network outputs.

- **CV-BEV-002 –  Radius model**: a geometric feedback can inform the space traversed before impact as free and a region near impact as occupied, under the model of the sensor. The portion behind the impact remains hidden. Beam width, distance uncertainty and moving objects limit this interpretation. In a binary probabilistic update, log-odds $\ell=\log(p/(1-p))$ make it possible to add the information of the measurements according to the assumptions of independence and the prior. Repeating a correlated measure does not create as much independent information. The flashcard must therefore retain provenance, visibility and seniority, in addition to the occupancy value.

- **CV-BEV-003 –  Surface and units**: For an implicit occupation function $o_\theta(x)$, a surface is extracted at a selected level $o_\theta(x)=\tau$. For an ideal SDF $s(x)$, the surface is $s(x)=0$ and $|s(x)|$ represents a distance, according to the sign convention. Far from singularities, a true signed distance satisfies $\|\nabla s\|=1$; a learned function does not automatically ensure this property. The coordinates can be normalized during learning: returning to the meters requires the corresponding transformation. A plausible surface level therefore does not validate the metric distances or the probabilistic calibration of an output used by another module.

- **CV-BEV-004 –  Aligning the Historical**: If $T_{w\leftarrow e(t)}$ gives the coordinate frame ego to the time $t$ in the world, a historical point is transported to the current time by $p_{e(t)}=T_{w\leftarrow e(t)}^{-1}T_{w\leftarrow e(t_0)}p_{e(t_0)}$. This compensation assumes the static point in the world. A moving pedestrian retains a residual displacement after correction of the ego-motion; treating it as an extrinsic defect would be another confusion. check first static structures, and then parse the moving objects separately. The time per point of a scan may require several transformations, and not a single pose for the entire frame, when the movement during the acquisition is significant.

- **CV-BEV-005 –  Testable grid contract**: accompany the tensor of its origin, its axes, its resolution, its terminals, its timestamp and its visibility mask. For a cell declared free, to be able to link the decision to observations that really forced this region. A constructed test places an obstacle behind a pallet, then changes the point of view: the cell must go from unknown to observed according to the new measurements, without considering the initial vacuum of the tensor as evidence. Also assess the shelf life of moving obstacles and the response to outdated data. These tests verify the semantics of the interface, beyond the average accuracy of the boxes.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OctoMap](https://octomap.github.io/) –  Full 3D model, free/occupied/unknown space. View on 2026-10-30.
- [Li et al., BEVFormer](https://arxiv.org/html/2203.17270v2) –  §3.4, time history; transformations and tests derived by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
