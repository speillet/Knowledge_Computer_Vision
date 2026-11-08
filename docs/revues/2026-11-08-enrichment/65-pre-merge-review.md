# Pre-merge review — 2026-11-08

The `code-review` skill ran its Standards and Spec axes in separate parallel
agents against `main` (`e214ec64ba6862fce0027bb788dac2d574597a88`). The reviewed
draft commit was `a5e7997`. These are agent reviews, not independent human
scientific validation. Line references in the findings concern that draft.

## Standards

- **Important — redundant enrichment.** `revue-cartes` §4 and the review grid
  prohibit padding by paraphrase. Several draft additions repeated existing
  examples or protocols, including fixed-point disparity, the late duplicate
  with AP equal to one, and the scale-two trajectory example.
- **Minor — source traceability.** Farnebäck and iSAM2 reports needed to
  distinguish accessible initial extraction from detailed passage requests
  that timed out. A cited paper is not evidence that every named section was
  read successfully in this pass.
- **Minor — prime notation.** New formulas used baseline `\prime` instead of
  a superscript prime. Existing questions and historical math were to be preserved.

No applicable software-smell finding beyond the documented pedagogical
redundancy rule. No numerical error was found in the checked derivations.

## Spec

- **P2 — repeated explanations.** The scope requires additional information.
  Repeating existing GrabCut interaction protocols, Q-Former explanations or
  threshold-crossing examples does not meet that requirement.
- **P3 — read-noise units.** The new acquisition example incorrectly called
  a variance of 25 “electrons”; the standard deviation is 5 electrons and the
  variance is 25 e⁻². Its numerical SNR values were correct.
- **P3 — Huber scale wording.** The new explanation incorrectly said the
  scale bounds residual norm. It sets the joint-norm transition radius;
  larger residuals remain possible and influential.

No other definite mathematical blocker or unauthorized structural change was
identified in the draft. The user-requested PR and merge remained in progress.

## Resolutions

Forty-seven cards retain their already sufficient explanations; their redundant
draft paragraphs and source annotations are removed from both card and canonical
copies. Two subjects, single-object tracking and GrabCut, consequently retain
their entire original content and canonical revisions.

Three other additions retain new information through explicit derivations:

- CV-CANNY-HOUGH-002 derives the Hough rho conversion from ROI to full-image
  coordinates, rather than repeating axis-angle examples.
- CV-BA-002 counts possible camera-block connections induced by eliminating
  a landmark observed by several cameras.
- CV-METRIQUES-TEMPS-002 expresses the HOTA aggregation discrepancy through
  the angle between square-root component vectors.

The acquisition units and Huber transition wording are corrected in both
copies. New prime notation is superscripted. The source-access record and
subject reports qualify the Farnebäck/iSAM2 limitations; detailed iSAM2 update
rules are marked not freshly reverified. Numerical checks include a finite
difference check of the new focal-loss derivative. Reports, revision counts,
answer lengths and the progress log are recalculated from the final content.

The final scope is **282 cards reviewed, 235 enriched, 47 retained**, with
**58 canonical revisions incremented once** and two references retained.
Questions, IDs, GUIDs, tags, decks and recall objectives remain protected.

## Follow-up

Both axes checked correction commit
`bc0193a82daf98b49917d7b64477e36fa2a7407d` and found no remaining introduced
blocker in the targeted follow-up. Both re-executed the 59 numerical checks.
The Spec axis independently counted the protected content/revision totals and
confirmed that the two retained subjects match `main` exactly. This agreement
between agents is not independent human scientific validation.

Standards: 3 draft findings resolved; worst was redundant material. Spec: 3
draft findings resolved; worst was repeated explanations presented as additional
depth. No remaining blocker identified in either targeted follow-up.
