# Journal –  Semantic segmentation, instances and panopticon –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Deduction/Assumption Cases; Documentary Context Below | Lost information: specifies the existing question | Finished core preserved; 194 → 299 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SEGMENTATION-002 | Deduction/Assumption Cases; Documentary Context Below | Information test: specifies the existing question | Finished core preserved; 193 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SEGMENTATION-003 | Deduction/Assumption Cases; Documentary Context Below | Transforming the adapted representation: clarifies the existing question | Finished core preserved; 201 → 306 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SEGMENTATION-004 | Deduction/Assumption Cases; Documentary Context Below | Physical scale of the defect: specifies the existing question | Finished core preserved; 194 → 304 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SEGMENTATION](../../../vault/90-segmentation/references/93-semantique-instances-panoptique.md); [flashcards](../../../vault/90-segmentation/93-semantique-instances-panoptique.md). reference note modified before the flashcards.

- **CV-SEGMENTATION-001 –  Lost information**: From a partition of classified instances, we can often merge the IDs of the same class to produce a semantic flashcard. The reverse is not determined: multiple instance partitions can have exactly the same flashcard of classes. IDs are arbitrary, but the relationship "these pixels belong to the same object" is not. In panopticon, each valid pixel belongs to a segment according to the contract, which requires a rule to solve the possible overlaps of predicted masks. Evaluating only classes after merging can therefore hide a major error in the identity or number of segments.

- **CV-SEGMENTATION-002 –  Information test**: Compare two annotations with the same foreground union: a single region and two separate instances. A semantic loss per pixel receives the same classes in both cases and cannot distinguish these solutions by this supervision alone. A border index, distance field, or instance header can add a different target, if the data allows it to be annotated. For a classical baseline, markers provide a hypothesis of separation to be validated. Before choosing, check whether the occlusion makes certain objects invisible: a comprehensive count can then require another view or another sensor.

- **CV-SEGMENTATION-003 –  Transforming the adapted representation**: for a geometric transformation $W$, image and annotation must use the same spatial correspondence, but an interpolation of discrete labels must retain the categorical contract. Interpolating real logs and then taking an argmax is another operation and usually does not switch with argmax and then interpolating labels. At crop borders, explicitly define the class or value ignores the padding. For an increase that destroys a region of the image, do not silently keep an annotation as if its content remains visible. A two-class synthetic mask and a void zone provides a simple witness of these invariants.

- **CV-SEGMENTATION-004 –  Physical scale of the defect**: The same boundary error of a voxel represents 0,5 mm on one axis and 3 mm on another if the spacings differ. Surface distances must therefore be calculated in the relevant physical geometry. An average per volume and an average per patient do not give the same weight to cases; also announce cases where the structure is absent. A test built with a large region and a small structure shows how an aggregated Dice can privilege the first. This analysis focuses on the technical metric and its assumptions, without inferring a clinical utility of a recovery value.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Cheng et al., Mask2Former](https://arxiv.org/html/2112.01527v3) –  Introduction, distinction of tasks and annotations; representational calculations and constructed metrics. View on 2026-10-30.

The Nature page of Reinke et al. is inaccessible after redirection; clinical conclusions are not re-evaluated. The complements relate to technical contracts and built reasonings.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
