# Review –  Splits, annotations, score calibration and drift –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Project Deduction/Protocol; no new external confirmation claimed | Graph of data dependency: specifies the existing question | Finished core preserved; 184 → 295 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FIABILITE-002 | Deduction/Assumption Cases; Documentary Context Below | Reliability diagram: specifies the existing question | Finished core preserved; 195 → 302 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FIABILITE-003 | Project Deduction/Protocol; no new external confirmation claimed | Test become development: specifies the existing question | Finished core preserved; 202 → 310 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FIABILITE-004 | Project Deduction/Protocol; no new external confirmation claimed | Comparison plan: specifies the existing question | Finished core preserved; 208 → 316 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FIABILITE-005 | Project Deduction/Protocol; no new external confirmation claimed | Risk and coverage: specifies the existing question | Finished core preserved; 187 → 296 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FIABILITE](../../../vault/130-evaluation-fiabilite/references/133-donnees-generalisation.md); [flashcards](../../../vault/130-evaluation-fiabilite/133-donnees-generalisation.md). reference note modified before the flashcards.

- **CV-FIABILITE-001 –  Data Dependency Graph**: Link images from the same acquisition, part, patient, or space zone, then assign groups to the split before creating tiles and augmentations. A validation tile that covers a training tile can directly transmit common textures and objects. The relevant size of a group depends on the generalization announced: new point of view, new object or new site are not the same tests. To estimate the uncertainty of a metric, resample coherent groups rather than all pixels or frames as if they were independent. The large number of files does not replace the diversity of acquisition units.

- **CV-FIABILITE-002 –  Reliability diagram**: first define the correct event, e.g. correct class and sufficiently precise location under a given matching. In score bins, compare the frequency of this event and average confidence with their numbers. A typical CDE averages the absolute differences weighted by the bin population; it depends on the binning and can hide subgroups. Geometric calibration compares projections to point measurements and estimates other parameters. A temperature transformation can change the scores without changing the order of the classes, while a change of intrinsics changes the geometry: these are two interventions of different nature.

- **CV-FIABILITE-003 –  Test become development**: After several cycles where the errors of the same test guide the choices, this set brings information to the selection process, even without direct training on it. The best result selected among many essays then incorporates this adaptation. Keep for each cycle the version of the data, the decisions made and the validation used; provide for an independent evaluation after freezing of the selected version. A targeted set of difficult cases remains useful as a regression, but does not necessarily replace a representative test of frequency of errors in operation. Naming these uses separately makes it impossible to interpret a gain on an adaptive collection as a general proof.

- **CV-FIABILITE-004 –  Comparison plan**: cross known/new region and known/new season to separate as much as possible spatial and temporal novelty. check tapes, physical resolution, alignment and label policy in each box. A seasonal change can make an object really different or only its appearance different; the definition of the class must remain explicit. Examining paired areas helps to isolate the acquisition, but does not alone evaluate an area never seen before. Keeping the results per square and per class prevents a change in the proportion of easy terrain from artificially explaining the overall average. This plan remains a proposed protocol, not a measured remote sensing result.

- **CV-FIABILITE-005 –  Risk and coverage**: For a rule that denies scores below a threshold, coverage is the fraction of cases where a decision is issued; risk is the error among those decisions according to the protocol. One method can reduce the risk by refusing more, without improving the perception on the remaining cases. Compare risk-coverage curves and critical layers, with labels representative of the new sensor. A change in the distribution of features can serve as an alarm, but it does not directly give the error rate without reference. Check separately the entry contract and the relevance of the rule of refusal after change of domain.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Guo et al., calibration](https://arxiv.org/html/1706.04599v2) –  §2, ECE and diagrams; detection protocol, splits and cover risk built. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
