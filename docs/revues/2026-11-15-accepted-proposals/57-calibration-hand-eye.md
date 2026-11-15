# Review — Hand–eye calibration — solving AX = XB with consistent coordinate frames — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-HANDEYE-01. One card added, CV-HANDEYE-006;
the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/57-calibration-hand-eye.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 7 → 8.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-006 | Decomposition $R_AR_X=R_XR_B$, $(R_A-I)t_X=R_Xt_B-t_A$ and ill-conditioning of decoupled linear solutions: Horaud and Dornaika §3, eqs. 15–16. Rotation then translation versus both together, "the most stable solution": §5. Simulations (1,000 trials, $\|t\|=157$ mm, separable methods almost identical, nonlinear more accurate in all situations, decoupling "introduces a bias", 4% against 6.5% at four motions): §6. Default Tsai, separable and simultaneous classes: calib3d.hpp L2234–L2243, L640–L647. Translation step with the estimated rotation fixed and Tsai filter: calibration_handeye.cpp L307–L376; Andreff joint system L599–L624. Propagation $\delta\times(R_Xt_B)$, amplification $1/(2\sin(\theta/2))$, 3.0 mm and 1.05 mm, two-motion case and unit weighting: project derivations recomputed by the check script | Comparison: the solver choice for a translation tolerance, with the default solver failing silently | 3 expected criteria (rotation error enters through $R_Xt_B$ and is systematic; division by $2\sin(\theta/2)$ with the numbers; when and how to prefer a joint method); 586 lexical words | Notation $A$, $B$, $X$, $R_X$, $t_X$ as in the reference; consistent with worked example B | Comparison |

CV-HANDEYE-003 (design) already mentions that rotation errors enter the right-hand side and
that small rotations give weak leverage, as reasons to excite the motions. The new card
tests a distinct objective: why a separable solver biases the translation, how much, and
when to choose a joint method. It refers to CV-HANDEYE-003 for the pose plan instead of
repeating it.

## Reference findings

- The Alternatives section said "Prefer a simultaneous or nonlinear method (Daniilidis,
  Andreff, or a joint refinement of $X$ and $Y$) ... since decoupling biases the estimate
  in Horaud and Dornaika's simulations [§6]". This is imprecise: §6 compares Tsai–Lenz,
  Horaud and Dornaika's closed-form separable method and their joint nonlinear method only.
  Andreff (3DIM 1999) and Daniilidis (IJRR 18(3), dated 1998 in OpenCV's comment)
  postdate the 1995 paper (citation comments of `calibration_handeye.cpp` L570–L629) and
  were not part of the comparison. The
  bullet now recommends the joint nonlinear refinement on that evidence and asks for the
  linear simultaneous solvers to be compared on held-out closure.
- The reference stated the bias but not its mechanism. Worked example C now derives it, and
  the Mathematics section records which OpenCV methods are separable, that all three solve
  the translation with the estimated rotation fixed, and that OpenCV's Andreff returns the
  translation of the joint solve while projecting only the rotation block (L617–L624).

## Applied corrections

- `vault/50-calibration-geometrie/57-calibration-hand-eye.md`: CV-HANDEYE-006 appended.
- `vault/50-calibration-geometrie/references/57-calibration-hand-eye.md`, revision 7 → 8:
  separable and simultaneous classification and Horaud and Dornaika's §5 statement added;
  worked example C added; decoupling-bias property linked to its mechanism and to §3;
  Alternatives bullet corrected as above; Horaud implementation lines added to the sources;
  the card listed under related flashcards; closing provenance line extended.

## Proposals

P-CV-HANDEYE-01: accepted by the learner on 2026-11-15, completed as CV-HANDEYE-006.

## Sources

Scientific source:

- Horaud and Dornaika 1995, "Hand-Eye Calibration", IJRR 14(3), author copy
  [arXiv 2311.12655](https://arxiv.org/abs/2311.12655) (PDF, text extracted with
  `pdftotext`): §3 (eqs. 15–19 and the decoupling paragraph), §5 (rotation then translation;
  rotation and translation together), §6 (stability analysis).

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns HTTP 403
from this environment; Context7 is unavailable in this session):

- `modules/calib3d/include/opencv2/calib3d.hpp` L636–L647 (method enum), L2234–L2243
  (separable and simultaneous methods), L2318–L2353 (chains and minimum motions);
- `modules/calib3d/src/calibration_handeye.cpp` L270–L384 (Tsai), L425–L447 (Park
  translation), L520–L538 (Horaud translation), L570–L722 (Andreff and Daniilidis).

Not opened: Tsai and Lenz 1989, Park and Martin 1994, Andreff et al. 1999, Daniilidis 1999.

## Checks and limitations

`python3 -I checks/57-calibration-hand-eye.py` passes its 5 checks: the 1.047 mm
perturbation, $2\sin(\theta/2)$ at $20^\circ$ and $60^\circ$ and the Tsai filter bounds
(17.3° and 116.4°); a constructed single motion where the separable step returns $t_X$
exactly with the true rotation and 3.0 mm off with a $0.2^\circ$ error; 1.05 mm at
$60^\circ$; a two-motion stacked case (1.74 mm against 0.55 mm); the length-unit scaling of
Andreff's translation rows. The amplification is exact for one motion and an error in the
plane perpendicular to its axis; with many motions it depends on the axes. No solver was
run on noisy data, so the claim that unit choice changes Andreff's result on noisy data is a
least-squares deduction. AnkiDroid rendering of the card is not verified.
