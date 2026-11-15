# Review — SORT — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-SORT-01. One card added, CV-SORT-009;
the eight existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/111-sort.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 9 → 10.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-SORT-009 | Unmatched detection → new tracker "with the velocity set to zero" and large velocity covariance: Bewley et al. §3.4. IoU cost against predicted boxes, rejection below $\mathrm{IoU}_{\min}$: §3.3. Only `x[:4]` set from the box: sort.py L114; state starts at zero: filterpy L397; prediction $Fx$: sort.py L105, L133–L145. Shortcut on `> iou_threshold`, rejection on `< iou_threshold`: L154–L196. Defaults `max_age=1`, `min_hits=3`, `iou_threshold=0.3`: L200. Output only with `hit_streak >= min_hits` or `frame_count <= min_hits`, deletion when `time_since_update > max_age`: L243–L250. First-update gains 0.9999 and 0.9988: recomputed from the code settings. $\mathrm{IoU}=(w-d)/(w+d)$, $d\le0.538w$, the ball sequences, the acceleration case, the diagonal case and the `iou_threshold=0.2` case: project constructions recomputed on a port of the pinned loop | Diagnosis: a frequent field failure (balls, drones, distant vehicles) whose cause sits in the birth rule, not in the detector or the noise settings | 3 expected criteria (zero-velocity birth; IoU budget with the number; displacement/width or consecutive-detection IoU check); 462 lexical words | Notation $u,v,s,r$, $w$, $d$ and worked example B of the reference; distinct from CV-SORT-006, which separates a missed detection, an expired track and a wrong association after an occlusion, and from CV-SORT-004 (life cycle) | Diagnosis |

The question gives the box width, the speed and the frame rate needed to compute
$d/w$; it does not name the initial velocity, the IoU budget or the check.

## Reference findings

No error found on the card's point: worked example B (IoU budget, zero-velocity birth,
frame-rate effect) agrees with §3.3–§3.4 and the pinned code. Added to worked example B:
why a newborn track predicts exactly its birth box (sort.py L114, filterpy L397), the
consecutive-detection IoU as a check that also covers diagonal motion, and the
constructed results showing that the birth, not the speed, fails (accelerating track
kept, `iou_threshold=0.2` admitting the birth at the cost of a wider gate). The
failure-mode row "Small fast objects never confirmed" now names both checks and the
card.

## Applied corrections

- `vault/110-tracking-association/111-sort.md`: CV-SORT-009 appended.
- `vault/110-tracking-association/references/111-sort.md`, revision 9 → 10: worked
  example B extended; failure-mode row extended; filterpy source entry given the zero
  initial state and the Joseph-form update lines; the card listed under related
  flashcards; closing provenance line extended (placed before the link definitions).

## Proposals

P-CV-SORT-01: accepted by the learner on 2026-11-15, completed as CV-SORT-009.

## Sources

Scientific sources:

- Bewley, Ge, Ott, Ramos and Upcroft 2016, [arXiv 1602.00763](https://arxiv.org/abs/1602.00763),
  PDF text extracted with `pdftotext`: §3.2, §3.3, §3.4, §4 opening.

Implementation sources (Context7 is not available in this session):

- abewley/sort at commit 2236dff5019565958b84df7d871d41cc1db58ac7,
  [`sort.py`](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py)
  L36–L270.
- rlabbe/filterpy at commit 5df4e095fac07684a05c495bd72d3424f7c68c9c,
  [`kalman_filter.py`](https://github.com/rlabbe/filterpy/blob/5df4e095fac07684a05c495bd72d3424f7c68c9c/filterpy/kalman/kalman_filter.py)
  L385–L410 and L483–L554.

No access failed.

## Checks and limitations

`python3 -I docs/revues/2026-11-15-accepted-proposals/checks/111-sort.py` passes its
8 checks: the IoU formula and the 0.5385 bound; the diagonal case (0.22); a newborn
track predicting its birth box; 20 tracks in 20 frames at 10 px/frame for a 16 px box,
output only under IDs 1–3; one ID at 5 px/frame; first-update gains and learned
velocity; one ID for a track born at 5 px/frame and accelerating to 10 px/frame; one ID
with `iou_threshold=0.2`. The port reproduces the pinned control flow and Kalman
settings in pure Python with an enumerated optimal assignment instead of `lap` or
`scipy`; it was not compared with a run of `sort.py` itself: filterpy is not installed
in this environment, and installing it to execute the downloaded `sort.py` was refused by
the session's permission policy. No video or detector was used. AnkiDroid rendering of the card is not verified.
