# Review –  SO(3), SE(3) and transformation conventions –  2026-10-30

## Overview

6 enriched flashcards; reference note scope of revision 6 to 7, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | Deduction/Assumption Cases; Documentary Context Below | Block calculation: specifies the existing question | Finished core preserved; 206 → 326 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SE3-002 | Deduction/Assumption Cases; Documentary Context Below | From pixel to world ray: specifies the existing question | Finished core preserved; 195 → 312 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SE3-003 | Deduction/Assumption Cases; Documentary Context Below | Complete extension to poses: specifies the existing question | Finished core preserved; 206 → 330 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SE3-004 | Deduction/Assumption Cases; Documentary Context Below | check of representation: specifies the existing question | Finished core preserved; 212 → 329 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SE3-005 | Deduction/Assumption Cases; Documentary Context Below | More robust near-zero calculation: specifies the existing question | Finished core preserved; 222 → 340 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-SE3-006 | Deduction/Assumption Cases; Documentary Context Below | Change of bases on both sides: specifies the existing question | Finished core preserved; 240 → 354 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-SE3](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md); [flashcards](../../../vault/10-mathematiques-estimation/12-rotations-se3.md). reference note modified before the flashcards.

- **CV-SE3-001 –  Calculation by blocks**: a homogeneous pose is written $T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$, with $R\in SO(3)$, $t\in\mathbb R^3$ and homogeneous points $[p^T,1]^T$. Its reverse uses $R^T$ and $-R^Tt$. For the two poses on the front, the relative rotation is $R_{wc_1}^TR_{wc_2}$ and the translation is $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$. The latter is the movement between centers re-expressed in the 1 camera, not just a difference in world coordinates. A homogeneous direction vector has a last zero coordinate and must not receive this translation. This check distinguishes the application of a pose at a point of its application to a direction.

- **CV-SE3-002 –  From Pixel to World Ray**: After removing the distortion, a homogeneous pixel $\tilde u$ defines a camera direction proportional to $K^{-1}\tilde u$, where $K$ is the intrinsic matrix. Worldwide, the radius is written as $p_w(\lambda)=C_w+\lambda R^TK^{-1}\tilde u$, with a scale convention for $\lambda$. The center is its origin, the inverse rotation orients its direction and the depth remains unknown on a single view. This calculation shows the distinct role of the three elements: $t$ participates in the localization of the camera, $R$ in the change of axes and $K$ in the geometry in pixels. None of these elements alone provide the depth of a point.

- **CV-SE3-003 –  Complete extension to poses**: by ordering increment $\xi=(\rho,\phi)$, translation then rotation, the assistant of $T=(R,t)$ is $\operatorname{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}$, where $[t]_\times a=t\times a$. Switching from a right disturbance to the equivalent left disturbance uses $\xi_G=\operatorname{Ad}_T\xi_L$. A covariance follows $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ in this local approximation. The cross block reflects the fact that a small rotation around another origin also induces a displacement. A simple block-by-block rotation would forget this lever arm effect. The translation/rotation conventions must accompany the matrix to avoid swapping its blocks.

- **CV-SE3-004 –  check of representation**: A unit quaternion describes a rotation, but its multiplication is noncommutative. In Hamilton convention, an angle $\theta$ around a unit axis $a$ is represented, scalar first, by $(\cos(\theta/2),a\sin(\theta/2))$. This writing makes it possible to build a verifiable quarter turn without converting ambiguous Euler angles. A convention conversion must address the order, signs and meaning of application in a consistent way: swapping the four numbers is not always enough. Test successively the three axes of the base and a translated point makes it possible to verify the entire transformation; normalization does not repair either an inversion of pose or an incompatible product convention.

- **CV-SE3-005 –  More robust calculation near zero**: From a unitary relative quaternion in convention announced, $q_{rel}=(w,v)$, the main angle can be written as $\theta=2\operatorname{atan2}(\|v\|_2,|w|)\in[0,\pi]$. This shape exploits the vector part when the arccos becomes sensitive to rounding near 1. The absolute value processes double coverage, without erasing a true rotation error. Check that the two orientations express the same coordinate frame and the same direction before forming the relative rotation. For aggregations, report also quantiles and extreme cases: a low average error can hide some completely reversed orientations. These expressions give radians; explicitly convert only for display to degrees.

- **CV-SE3-006 –  Change of bases on both sides**: if $p'_c=B_c p_c$ and $p'_w=B_w p_w$, then a world matrix→camera becomes $T'_{cw}=B_cT_{cw}B_w^{-1}$, using homogeneous matrices $4\times4$. The kernel example changes only the camera base: $B_w=I$, hence the multiplication on the left. Changing the coordinate frame world also requires the second factor. This general rule avoids applying an "OpenGL conversion" without specifying which base changes. Camera coordinate conventions alone do not define clip space projection, depth buffer direction, or the origin of the framebuffer pixels: these additional contracts must be checked separately in the render.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9) –  §II-F, Deputy; §II-H, covariances; Appendices B and D. View on 2026-10-30.
- [Solà, Quaternion kinematics](https://arxiv.org/html/1711.02508v1) –  §§2.4 and 3.1, quaternion and conventions. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
