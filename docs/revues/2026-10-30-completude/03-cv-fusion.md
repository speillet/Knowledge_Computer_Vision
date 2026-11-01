# Review –  Kalman, EKF, UKF and ESKF for merger –  2026-10-30

## Overview

6 enriched flashcards; reference note scope of revision 6 to 7, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | Deduction/Assumption Cases; Documentary Context Below | Common basis of calculation: specifies the existing question | Finished core preserved; 203 → 319 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FUSION-002 | Deduction/Assumption Cases; Documentary Context Below | Non-reverse calculation and selection effect: specifies the existing question | Finished core preserved; 224 → 336 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FUSION-003 | Deduction/Assumption Cases; Documentary Context Below | Preserving Correlation: Specifying the Existing Question | Finished core preserved; 216 → 337 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FUSION-004 | Deduction/Assumption Cases; Documentary Context Below | Do not mix density and discrete variance: specifies the existing question | Finished core preserved; 205 → 338 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FUSION-005 | Deduction/Assumption Cases; Documentary Context Below | Example of a minimum error state: specifies the existing question | Finished core preserved; 233 → 356 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-FUSION-006 | Deduction/Assumption Cases; Documentary Context Below | Joseph's Origin: Specifying the Existing Question | Finished core preserved; 231 → 348 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-FUSION](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md); [flashcards](../../../vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md). reference note modified before the flashcards.

- **CV-FUSION-001 –  Common basis of calculation**: in an approximation EKF, $x^-=f(x^+,u)$ and $P^-=FP^+F^T+Q$, then $K=P^-H^T(HP^-H^T+R)^{-1}$. $F$ and $H$ are the Jacobians of dynamics and measurement; $Q$ and $R$ describe their uncertainties in the coordinates and no time announced. We correct with innovation, by solving a system to calculate the gain rather than an explicit inverse. The UKF replaces some of these linearizations by the propagation of weighted points; the ESKF changes the coordinates in which the small correction is estimated. A truly multimodal distribution, like two possible visual associations, is not rendered unimodal by this change of calculation.

- **CV-FUSION-002 –  Calculation without reverse and selection effect**: if $S=LL^T$, solve $Le=\nu$ and then calculate $e^Te$ gives the score. For independent measurements of fixed dimensions, its nominal expectation is $m$, before selection. On the other hand, keeping only observations that have passed the gating artificially reduces the average observed; it can no longer be naively compared to $m$ to conclude a too great covariance. Similarly, testing multiple candidates and then retaining the best changes the distribution. Check noise consistency on baseline observations and consider releases. A succession of innovations of the same sign also reveals a temporal structure that a histogram of norms can mask.

- **CV-FUSION-003 –  Also preserve correlations**: If the error is split into $\theta$ orientation and other $a$ variables, the reset transforms $P_{\theta a}$ into $G_\theta P_{\theta a}$ and $P_{a\theta}$ into $P_{a\theta}G_\theta^T$, not just the $P_{\theta\theta}$ block. These terms can transfer information from a visual observation to position, speed, or bias at the next correction. Erroneously canceling them changes the filter. A constructed check consists of comparing the distribution of small perturbations before and after injection in their respective coordinates: the numerical description changes, while the physical states represented must remain close. Testing the reset separately avoids confusing it with the legitimate reduction of uncertainty due to measurement.

- **CV-FUSION-004 –  Do not mix density and discrete variance**: for a position – speed state subjected to a continuous white acceleration of spectral density $q$, the ideal integration gives $Q_d=q\begin{bmatrix}\Delta t^3/3&\Delta t^2/2\\\Delta t^2/2&\Delta t\end{bmatrix}$. If we assume instead a constant random acceleration on each interval, of variance $\sigma_a^2$, the block becomes $\sigma_a^2\begin{bmatrix}\Delta t^4/4&\Delta t^3/2\\\Delta t^3/2&\Delta t^2\end{bmatrix}$. These two analytical cases describe different noises; replacing one with the other with an unchanged numerical value is false. The powers of $\Delta t$ are therefore not chosen by copying a matrix: they come from the noise model and its integration, with their units.

- **CV-FUSION-005 –  Example of minimum error state**: A nominal inertial state can hold position $p$, speed $v$, quaternion $q$, accelerometer bias $b_a$ and gyro bias $b_g$. This represents 16 stored components, but an error of dimension 15 when the orientation uses three local coordinates and the gravity is known here. A typical correction injects $p\leftarrow p+\delta p$, $v\leftarrow v+\delta v$, $R\leftarrow R\operatorname{Exp}(\delta\theta)$, then the additive biases. The IMU measures a specific force and angular velocity, not directly a position: you have to remove the biases, express the acceleration in the correct coordinate frame and process the gravity according to the model. The exact size and content change if one also estimates gravity or calibration.

- **CV-FUSION-006 –  Origin of Joseph**: if the error before measurement is $e^-$ and the measurement noise $n$, the linear correction gives $e^+=(I-KH)e^- -Kn$. Taking the covariance and assuming their independence, the two crossed terms cancel each other out and we find the sum of Joseph. If measurement and prediction share the same information, these terms are no longer automatically zero: the stability of the algebraic form does not validate the statistical hypothesis. A square-root alternative propagates a covariance factor rather than $P$ directly; it improves the numerical properties in its frame, but requires a consistent implementation of prediction, correction, and reset. Adding an arbitrary diagonal to each failure can hide an invalid template.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Solà, Quaternion kinematics](https://arxiv.org/html/1711.02508v1) –  §§5 – 6, status, correction and reset; Annex E, noise integration. View on 2026-10-30.
- [Chin/JPL 2023](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf) –  §III-A, form of Joseph; square-root sections. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
