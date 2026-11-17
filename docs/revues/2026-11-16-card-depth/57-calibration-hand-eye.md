# Review — Hand–eye calibration — solving AX = XB with consistent coordinate frames — 2026-11-16

## Overview

1 card audited and deepened in `approfondir` mode (CV-HANDEYE-005), and one figure added
to CV-HANDEYE-001. Highest severity before correction: 0 blocking, 0 important, 1 minor
(CV-HANDEYE-005 wrote the eye-to-hand chain but not the relative motion it implies, the
OpenCV input recipe or how an error in $X$ shows in the task), 0 with no defect
identified. CV-HANDEYE-006 (written on 2026-11-15) is unchanged.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 8 → 9.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-005 | Existing claims confirmed: eye-to-hand estimates camera→base from a target on the end-effector (calib3d.hpp L2248–L2250); the chain $G_i^{-1}XC_i=Y$ matches OpenCV's eye-to-hand equations (L2336–L2346), which use ${}^gT_b$ in place of ${}^bT_g$. Missing: the relative motion of eye-to-hand, the meaning of OpenCV's slot names in that case, and the error signature that distinguishes the two configurations in the task | Comparison: rebuild the chain when the mounting changes | 3 expected criteria, unchanged; 322 → 573 lexical words (the counter includes the Source line) | Consistent with the reference's Mathematics section and its implementation contract ("eye-to-hand by passing base-to-gripper poses") | Minor | Deepened: $A=G_jG_i^{-1}$ in the base frame against $G_j^{-1}G_i$ in the gripper frame, the input recipe through `inv(Hg[j])*Hg[i]`, the closure in the gripper frame, a constructed error signature; Source line extended |
| CV-HANDEYE-001 | Not re-audited (checked on 2026-11-14) | — | 357 → 461 lexical words | The figure uses the card's notation and arrow directions | — | Figure added with a three-sentence reading |

The addition to CV-HANDEYE-005 does not repeat CV-HANDEYE-002, which covers the
eye-in-hand input contract and matrix checks, nor CV-HANDEYE-004, which tests closure
for eye-in-hand only.

## Added figure

`vault/99-Ressources/cv-handeye-loop.svg`: schematic frame graph of eye-in-hand
calibration at two stations. Each arrow from frame $b$ to frame $a$ is ${}^aT_b$, the
reference's convention: green measured $G_i$, $G_j$ (gripper → base) and $C_i$, $C_j$
(target → camera); red unknown $X$ (camera → gripper) at both stations, inside dashed
station groups; violet $A=G_j^{-1}G_i$ (gripper $i$ → gripper $j$) and $B=C_jC_i^{-1}$
(camera $i$ → camera $j$). The check script builds the same graph from random rigid
transforms and verifies the closure $G_iXC_i=Y$, $AX=XB$, and that $A$ maps gripper-$i$
coordinates to gripper-$j$ coordinates.

The coordinator suggested CV-HANDEYE-005 or the card the figure serves best. It is
embedded in CV-HANDEYE-001, whose expected answer is exactly the loop drawn, and in the
reference under "Chain and equation (eye-in-hand)". It draws only eye-in-hand; the
eye-to-hand comparison of CV-HANDEYE-005 stays in text.

Rendering check: `rsvg-convert` at 380 px and 1080 px, both inspected. The first render
showed the centre annotation touching the dashed station borders and a missing space in
"$G_i\,X\,C_i$" after a subscript; the annotation was set to 14 px on two lines and the
space restored with `dx`. The second render is clean. The file parses with
`xml.dom.minidom`.

## Applied corrections

- `vault/50-calibration-geometrie/57-calibration-hand-eye.md`, card CV-HANDEYE-005: new
  paragraphs **Relative motions side by side** and **Error signature in the task**;
  Source line extended with `calibration_handeye.cpp` L297–L304.
- Same file, card CV-HANDEYE-001: **Reading the diagram** paragraph with the figure.
- `vault/50-calibration-geometrie/references/57-calibration-hand-eye.md`, revision
  8 → 9: the frames of $A$ and $B$ and the figure with its caption under "Chain and
  equation (eye-in-hand)"; the eye-to-hand relative motion, input recipe and error
  signature under "Eye-to-hand"; closing provenance line extended.

Expected answers, questions, objectives, families, tags and IDs are unchanged. No
reference claim was found false, so no correction-log entry is needed.

## Claims added and their passages

| Claim | Passage | Verdict |
| --- | --- | --- |
| OpenCV's eye-to-hand equation is $({}^gT_b^{(2)})^{-1}\,{}^gT_b^{(1)}\,{}^bT_c={}^bT_c\,{}^cT_t^{(2)}({}^cT_t^{(1)})^{-1}$ | calib3d.hpp L2336–L2346 | Confirmed; it equals $(G_jG_i^{-1})X=X(C_jC_i^{-1})$ |
| The implementation forms `Hgij = homogeneousInverse(Hg[j]) * Hg[i]` and `Hcij = Hc[j] * homogeneousInverse(Hc[i])` from the inputs as given | calibration_handeye.cpp L297, L304 (Tsai; the same lines at L395–L396 for Park) | Confirmed |
| Passing $G_i^{-1}$ makes that product $G_jG_i^{-1}$, and the output is camera→base | Deduction from the two passages; recomputed | Recomputed |
| Translation error $e$ shifts grasps by $R_Xe$ (eye-to-hand) or $R_{G_i}R_Xe$ (eye-in-hand); 2.83 mm for 2 mm and a 90° wrist roll | Constructed | Recomputed |

## Sources

Scientific sources: none newly consulted; the comparison rests on the chain algebra and
the OpenCV contract. Horaud and Dornaika (read on 2026-11-14 and 2026-11-15) remain the
reference's scientific source.

Implementation sources (official code at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L2234-L2358): L2234–L2250 (methods, eye-to-hand configuration), L2323–L2346 (eye-in-hand and eye-to-hand equations), L2352–L2358 (minimum motions, signature).
- [`calibration_handeye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp#L275-L376): L275–L376 (Tsai), L395–L396 (Park pairs).

Failed accesses: none in this pass. Context7 is unavailable in this session.

## Checks and limitations

`python3 -I docs/revues/2026-11-16-card-depth/checks/57-calibration-hand-eye.py`: 4 checks
pass (the eye-in-hand graph of the figure; eye-to-hand $AX=XB$ with $A=G_jG_i^{-1}$ and
OpenCV's product on inverted inputs; the non-constant ${}^gT_c$ of a fixed camera; the
error signature). No robot or solver was run. SVG rendering in AnkiDroid's WebView and in
Obsidian is not verified, only with `rsvg-convert`. Export status: **to republish with
`paquet-anki`**.
