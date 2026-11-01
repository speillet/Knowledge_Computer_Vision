# Review –  Multisensor calibration, hand-eye and time –  2026-10-30

## Overview

3 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MULTICALIB-001 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Useable writing: specifies the existing question | Finished core preserved; 188 → 289 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MULTICALIB-002 | Deduction/Assumption Cases; Documentary Context Below | Non-constrained component: specifies the existing question | Finished core preserved; 185 → 290 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-MULTICALIB-003 | Deduction/Assumption Cases; Documentary Context Below | Time order of magnitude: specifies the existing question | Finished core preserved; 185 → 300 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-MULTICALIB](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md); [flashcards](../../../vault/50-calibration-geometrie/55-calibration-multicapteurs.md). reference note modified before the flashcards.

- **CV-MULTICALIB-001 –  Useable writing**: Note $G_i={}^bT_{g_i}$, $C_i={} ^{c_i}T_t$ and $X={}^gT_c$, where the top coordinate frame receives the coordinates. The fixed calibration target imposes $G_iXC_i=Y$, with $Y={}^bT_t$ constant. Between two catches, multiply the equality left by $G_j^{-1}$ and right by $C_i^{-1}$ gives $(G_j^{-1}G_i)X=X(C_jC_i^{-1})$. The indices and the assembly therefore determine exactly $A$ and $B$. The case built with translations alone checks the units, but noncommutative rotations are needed to detect many order errors. The $X$ matrix must remain the same on all synchronized captures.

- **CV-MULTICALIB-002 –  Unconstrained component**: by developing homogeneous transformations, we obtain $(R_A-I)t_X=R_Xt_B-t_A$. For a rotation around a unit axis $n$, $(R_A-I)n=0$: this equation alone does not determine the component of $t_X$ following $n$. Repeating the same axis leaves this structural defect. Stacking movements of different axes can lift it, subject to a rotation $R_X$ itself correctly estimated. Examine the singular values of this system after scaling and compare the solutions by subsets of poses. A large number of correlated pairs does not transform into as many independent directions of information.

- **CV-MULTICALIB-003 –  Order of temporal magnitude**: in a local rigid displacement model, the deviation of a point expressed in the same coordinate frame is of the order of $\delta p\simeq(v+\omega\times p)\delta t$, with speed $v$ in m/s, angular speed $\omega$ in rad/s and delay $\delta t$ in s. The sign depends on the sense of comparison. At 10 m/s, 20 ms already represent 20 cm of translation; the angular contribution increases with the lever arm. The image projection then adds its Jacobian and depends on the depth. This built-in calculation explains why testing multiple speeds, distances, and direction of rotation helps distinguish a delay from a constant extrinsic.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [OpenCV 4.13.0, calibration hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) –  calibrateHandEye, coordinate frames, eye-in-hand and eye-to-hand strings and non-parallel axes; algebraic complements of the project. View on 2026-10-30.
- [Zhang–Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf) –  context acquisition in motion; approximation speed, delay and lever arm deduced by the project. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
