# Review — Intensity-based registration and ECC — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-ECC-01. One card added,
CV-ECC-004; the three existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/45-recalage-ecc.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 7 → 8.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-ECC-004 | Warp direction $x'=W(x,y,1)^\top$ from template to input: confirmed in tracking.hpp L338–L346. Advice to warp the input with `WARP_INVERSE_MAP`: tracking.hpp L353–L359. Inverse-map semantics of `warpAffine` and `warpPerspective`: imgproc.hpp L2457–L2507. OpenCV's internal warps use the flag: ecc.cpp L514–L531. The doubled motion $T(W^{-2}\mathbf x)$ is a project derivation, recomputed by the check script | Practice: a silent production error. The overlay is wrong and $\rho$ cannot reveal it, because it is computed on OpenCV's correctly warped image | 2 expected criteria plus one number (20 px); 411 lexical words | Aligned with the reference's data contract, now corrected (see below); notation $T$, $I$, $W$ as in the reference | Practice |

The question names the default-flag call, because predicting its result is part
of the objective. It does not name `WARP_INVERSE_MAP`.

## Reference findings

The data contract said that warping without `WARP_INVERSE_MAP` "applies the
inverse motion". This is imprecise. Without the flag, the matrix is inverted
before sampling, so at the solution the result is $T(W^{-2}\mathbf x)$: the
motion is applied a second time (imgproc.hpp L2457–L2473). The paragraph now
states this and adds the mapping of points in both directions.

## Applied corrections

- `vault/40-features-matching/45-recalage-ecc.md`: CV-ECC-004 appended.
- `vault/40-features-matching/references/45-recalage-ecc.md`, revision 7 → 8:
  warp-direction paragraph corrected and developed; the card is listed under
  related flashcards; imgproc.hpp lines added to the implementation sources;
  closing provenance line extended.

## Proposals

P-CV-ECC-01: accepted by the learner on 2026-11-15, completed as CV-ECC-004.

## Sources

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org
returns HTTP 403 from this environment; Context7 is unavailable in this session):

- `modules/video/include/opencv2/video/tracking.hpp` L314–L375
  (`findTransformECC` documentation and declarations);
- `modules/video/src/ecc.cpp` L505–L535 (iteration loop and warp flags);
- `modules/imgproc/include/opencv2/imgproc.hpp` L2457–L2510 (`warpAffine` and
  `warpPerspective`).

No scientific source carries this card: the convention belongs to the
implementation. Evangelidis and Psarakis (2008) remains readable only as an
abstract, as recorded in the previous pass.

## Checks and limitations

`python3 -I checks/45-recalage-ecc.py` passes its 6 checks: the 10 px example,
the flag-free result $T(W^{-2}\mathbf x)$ for a Euclidean warp (8° residual for
an estimated 4°), the homography case and point mapping. Images are modelled as
functions of coordinates; no OpenCV call was executed. AnkiDroid rendering of
the inline matrix is not verified.
