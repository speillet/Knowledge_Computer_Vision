# Review — Rectified stereo, SGM and depth — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-STEREO-01. One card added, CV-STEREO-005;
the four existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/61-stereo-profondeur.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 7 → 8.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-STEREO-005 | $P_1$ for $\lvert D_p-D_q\rvert=1$, $P_2$ for larger changes, slanted surfaces and discontinuities, path recursion, at least eight directions, $P_2=P_2'/\lvert I_{bp}-I_{bq}\rvert$ and "it has always to be ensured that $P_2\ge P_1$": Hirschmüller 2008, §2.2, eqs. 11–14. OpenCV's description of P1 and P2, "requires P2 > P1", suggested $8cb^2$ and $32cb^2$: calib3d.hpp L3723–L3729; five directions by default: L3671–L3688. Silent replacement of $P_2$ by $\max(P_2,P_1+1)$ in every mode: stereosgbm.cpp L500, L977–L978, L1229–L1230, L1639; constant $P_2$ in the aggregation loops: L676–L811; block sums of Birchfield–Tomasi costs: L558–L655. Inertness of $P_1$ when $P_2<P_1$, the single-path condition $w\Delta>2P_2$ and the toy sweep: project derivations recomputed by the check script | Algorithm: the two parameters every SGBM user tunes, with a silent implementation correction and a visible trade-off between speckle and narrow structures | 3 expected criteria (what each penalty charges and allows; why $P_2\ge P_1$; effect of raising $P_2$ with the toy numbers); 475 lexical words | Energy and recursion written as in the reference Mathematics section; penalties 200 and 800 as in worked example C | Algorithm |

The card carries forward the unregistered 2026-10-20 idea "Explain the penalties SGM
P1/P2". The question gives the penalties and the scene but does not say what each penalty
charges for or what raising $P_2$ does.

## Reference findings

- The parameter table said that "when 0 the code uses 2 and $\max(5,P_1+1)$" for `P1` and
  `P2`. This is incomplete: the code computes `P2 = std::max(params.P2 > 0 ? params.P2 : 5,
  P1+1)` (stereosgbm.cpp L500 and the three other modes), so any `P2` not larger than `P1`,
  not only zero, is silently raised to $P_1+1$. The row now states this.
- The table's effect "Too large $P_2$ erases thin structures; too small leaves noise" had no
  source or example. Worked example F now supports it with a single-path condition and a
  constructed eight-direction toy, labelled as such.
- The reference did not explain why $P_2\ge P_1$ is required. A paragraph now gives the
  reason from the recursion, Hirschmüller's requirement and OpenCV's enforcement, the units
  of the penalties and the constant $P_2$ of OpenCV.

## Applied corrections

- `vault/60-vision-3d/61-stereo-profondeur.md`: CV-STEREO-005 appended.
- `vault/60-vision-3d/references/61-stereo-profondeur.md`, revision 7 → 8: paragraph on
  $P_2\ge P_1$ and the effect of $P_2$ with worked example F; parameter-table row
  corrected; discontinuity-preservation property extended with OpenCV's constant $P_2$;
  stereosgbm.cpp lines added to the implementation sources; the card listed under related
  flashcards; closing provenance line extended.

## Proposals

P-CV-STEREO-01: accepted by the learner on 2026-11-15, completed as CV-STEREO-005.

## Sources

Scientific source:

- Hirschmüller 2008, "Stereo Processing by Semiglobal Matching and Mutual Information",
  IEEE TPAMI 30(2), [PDF](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf)
  (text extracted with `pdftotext`): §2.2 (eqs. 11–14 and surrounding text) and §2.5.2
  (placement of discontinuities in untextured areas, read but not used in the card).

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns HTTP 403
from this environment; Context7 is unavailable in this session):

- `modules/calib3d/include/opencv2/calib3d.hpp` L3668–L3735 (`StereoSGBM` description and
  `create` parameters);
- `modules/calib3d/src/stereosgbm.cpp` L490–L512, L558–L655, L676–L811, L970–L980,
  L1226–L1232, L1639.

## Checks and limitations

`python3 -I checks/61-stereo-profondeur.py` passes its 5 checks: suggested penalties 200 and
800 and the silent correction of `P2=150` to 201; identical path costs for $P_1=800,P_2=200$
and $P_1=P_2=200$; the exact one-dimensional optimum keeping a 6 px structure for
$P_2=800$ and 1000 and losing it for 1300 and 3200; an eight-direction toy SGM in which 3×3
speckle blobs survive at $P_2=250$ and vanish at 800, while a 6 px upright survives at 800
and 1600 and vanishes at 3200; horizontal paths alone losing the upright at 1600 while
vertical paths keep it at 3200. The toy uses a constructed cost volume (0 at the true
disparity, 400 elsewhere) and models eqs. 12–14, not OpenCV's block matching, five-direction
default or post-filters; the thresholds would differ on real images. No OpenCV call was
executed. AnkiDroid rendering of the card is not verified.
