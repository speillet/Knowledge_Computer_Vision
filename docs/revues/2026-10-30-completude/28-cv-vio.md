# Review –  SLAM, VIO, pre-integration IMU and loopback –  2026-10-30

## Overview

5 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Deduction/Assumption Cases; Documentary Context Below | Constraints between states: specifies the existing question | Finished core preserved; 190 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VIO-002 | Deduction/Assumption Cases; Documentary Context Below | Relative Constraint: specifies the existing issue | Finished core preserved; 195 → 303 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VIO-003 | Deduction/Assumption Cases; Documentary Context Below | Invariance and metric: specifies the existing question | Finished core preserved; 206 → 316 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VIO-004 | Deduction/Assumption Cases; Documentary Context Below | pose seniority budget: specifies the existing question | Finished core preserved; 208 → 314 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-VIO-005 | Deduction/Assumption Cases; Documentary Context Below | Bias drift, simplified case: clarifies the existing question | Finished core preserved; 214 → 324 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-VIO](../../../vault/60-vision-3d/references/63-slam-vio.md); [flashcards](../../../vault/60-vision-3d/63-slam-vio.md). reference note modified before the flashcards.

- **CV-VIO-001 –  Constraints between states**: with $R_i$ body→world, $p_i,v_i$ in world coordinates, $g$ in gravity acceleration and $\Delta t=t_j-t_i$, the ideal increments check $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ and $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$. They are expressed in the starting coordinate frame and must be compared with the pre-integrated IMU increments, with covariance and bias correction. These relationships make the additional states visible: positions, speeds, orientations and biases. Pre-integration is therefore a factor in joint estimation, not a replacement for these unknowns or the visual observations that constrain them.

- **CV-VIO-002 –  Relative Constraint**: For poses $T_i,T_j$ sending local coordinate frames to the world, the predicted transformation from $j$ to $i$ is $T_i^{-1}T_j$. A loop provides a $Z_{ij}$ measurement of this relation; a possible residual is $\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)$, depending on the conventions and the graph model. Its weighting reflects the accuracy of the verified measurement. Appearance detection alone does not provide this geometric accuracy. A graph can redistribute an inconsistency over many poses: a moderate final cost does not clear a false loop. Comparing before/after consistency and independent observations remains essential.

- **CV-VIO-003 –  Invariance and metric**: applying the same translation and rotation around gravity to the entire trajectory and the flashcard retains the relative observations of a VIO without global reference. Changing the scale uniformly, however, modifies the predicted metric accelerations; the IMU can therefore constrain this scale when the movement provides the necessary information. Degenerate movement or misjudged biases can make this strain weak. For evaluation, document the freedoms withdrawn and keep an explicit metric check. An alignment Sim(3), which also adjusts the scale, is suitable for some monocular comparisons but can hide a scale error of a VIO declared metric.

- **CV-VIO-004 –  Seniority budget of pose**: distinguish capture instant $t_c$, estimation availability $t_e$ and display instant $t_a$. A correct pose for $t_c$ comes already old from $t_a-t_c$ on the screen. The IMU propagation can predict up to $t_a$ under a motion model, with increasing uncertainty; it does not transform a future measurement into available observation. Measure the error at the time actually requested and report the time frames step by step with their percentiles. In a test built at 100°/s, 20 ms represents 2° of uncompensated rotation. This calculation directly links synchronization, prediction and visual stabilization requirement of the helmet.

- **CV-VIO-005 –  Bias drift, simplified case**: If a constant acceleration bias $b_a$ remains uncorrected in a fixed world direction, it produces approximately a speed error $b_at$ and position error $\tfrac12b_at^2$. A constant gyroscope bias produces an angular error of the order of $b_\omega t$; this error can also incorrectly orient gravity and contaminate translation. These constructed laws assume a simplified orientation and conditions, they do not predict a real trajectory. Looking for these time signatures in parallel with feature losses and loop corrections helps to propose discriminating essays rather than a single cause in view of the final plot.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Qin et al., VINS-Mono](https://arxiv.org/html/1708.03852v1) –  §IV-B, preintegration and bias; §V-B, metric initialization; algebraic add-ins and project scenarios. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
