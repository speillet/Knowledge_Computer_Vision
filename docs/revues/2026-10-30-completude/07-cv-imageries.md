# Review –  Line-scan, remote sensing and medical volumes –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | Deduction/Assumption Cases; Documentary Context Below | Complete geometry: specifies the existing question | Finished core preserved; 202 → 311 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IMAGERIES-002 | Deduction/Assumption Cases; Documentary Context Below | Constructed sizing: specifies the existing question | Finished core preserved; 196 → 311 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-IMAGERIES-003 | Deduction/Assumption Cases; Documentary Context Below | Define the unit of the test: specifies the existing question | Finished core preserved; 189 → 313 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-IMAGERIES](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md); [flashcards](../../../vault/20-acquisition-images/23-imageries-specialisees.md). reference note modified before the flashcards.

- **CV-IMAGERIES-001 –  Complete geometry**: A physical position is written $p=o+A i$, with index $i$, physical origin $o$ and columns of $A$ describing directions and spacings. The distance between indices follows $\|A\Delta i\|_2$; the formula with only spacings assumes orthogonal axes. DICOM distinguishes the nominal cutting thickness from the distance between centers: systematically using the thickness as spacing can be wrong. For a stack, check the positions and orientations of the cuts, regularity and order before making a single affine. The calculation of HD95 then requires a precise definition of the surfaces, directed distances and percentiles, with explicit policy if one of the surfaces is empty.

- **CV-IMAGERIES-002 –  Built sizing**: for a desired longitudinal resolution of 0,1 mm/line and a speed of 500 mm/s, it is necessary $f_l=v/s=5000$ lines/s in the slip-free model. A long piece of 20 mm then occupies about 200 lines. If an encoder imposes a line per displacement of 0,1 mm, the frequency must follow the speed variations within the range allowed by the sensor. A maximum speed exceeded or a lost impulse breaks this contract. It is also necessary to limit the displacement during the exposure of a line: correct spatial triggering and low blur are two distinct constraints. The above calculations are analytical sizing, without conveyor testing.

- **CV-IMAGERIES-003 –  Set test unit**: Ten thousand tiles from ten scenes do not represent ten thousand independent contexts. Build a table linking each tile to the scene, site, date, and footprint; assign groups to scores before any increase or extraction of patches. The normalization statistics learned and the choice of thresholds must follow the same separation. A geographical margin can help remove recoveries, without guaranteeing the independence of all acquisition factors. To compare two methods, also aggregate their deviations by representative group of the deployment: a result dominated by a very cut site can tell a story other than the average sites. This is a proposed protocol, not an audit of SpaceNet.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [DICOM PS3.3 2026d](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) –  C.7.6.2, position, orientation and spacing. View on 2026-10-30.
- [Basler, GigE Line Scan](https://docs.baslerweb.com/line-scan-gige-use-cases) –  Box 1 b, trigger encoder. View on 2026-10-30.
- [SpaceNet7](https://www.spacenet.ai/sn7-challenge/) –  The Problem and The Data; geographical separation deduced by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
