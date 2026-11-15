# Review — IoU and AP — the COCO detection protocol — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-IOU-AP-01. One card added,
CV-IOU-AP-008; the seven existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/131-iou-ap-coco.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 9 → 10.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-008 | `evaluate` passes `maxDets[-1]` to `evaluateImg` (L153–L154), which sorts one image's detections of a category by score with a stable sort and keeps the first 100 (L259–L260), then matches them greedily in that order (L272–L296); `accumulate` cuts each image's list at the cap, merges and stable-sorts by score (L362–L370), then computes recall, precision, the right-to-left envelope and the 101-level sampling (L384–L408): confirmed at commit 8c9bcc3. Greedy NMS removes only lower-scoring boxes: torchvision ops/boxes.py L25–L27. LVIS Table 3a (Mask R-CNN R50-FPN, mask AP with the LVIS evaluator): 14.8 at threshold 0.05 and 100 detections per image, 15.7 at 300, 20.8 at 300 and 0.001: confirmed in App. B.1. AP $51/101$ and $63.5/101$, operating point $2/3$ and $1/2$, the monotonicity argument and the cap counterexample ($1\to0.835$): project derivations, recomputed by the check script | Reasoning: separates benchmark AP from the deployed operating point with a mechanism. Distinct from CV-IOU-AP-004 (computing the envelope of a fixed list) and CV-IOU-AP-007 (subgroups and error costs for acceptance), which the card cites | 3 expected criteria (AP before and after with the reason it cannot fall; operating point unchanged; numbers to report); 514 lexical words | Notation $R_i$, $P_i$ and the envelope of the reference; worked example D aligned with the card | Reasoning |

The question gives the ranked outcomes of the new detections "among themselves", so
that placing them after the old ones is part of the answer.

## Reference findings

Worked example D stated the right condition ("scores below every retained score"),
but then wrote that it "explains why benchmark submissions use a very low score
threshold and the full cap". The second half is not covered by the argument: raising
a per-image cap can lower AP, because a detection cut from one image can outscore
detections kept in other images. Constructed counterexample, recomputed: two images
with one object each; image A has a TP at 0.95 and an FP at 0.90, image B a TP at
0.50; one detection per image gives AP 1, two give $(51+50\cdot2/3)/101\approx0.835$.
The randomized check also finds such drops, while it finds none for a lower score
threshold. The measurement-limits bullet said that a binding cap "alters the
comparison" without saying how; it drops the additions beyond the cap and cannot
lower AP. The LVIS figures are now labelled as mask AP from the LVIS evaluator, with
the 100-detection row that isolates the cap change.

The proposal text itself said that "raising the per-image cap" cannot lower COCO AP.
The card states the precise condition instead (every added detection scores below
every detection already evaluated in its category, across images), shows that a lower
global threshold satisfies it, and gives the counterexample for the cap.

## Applied corrections

- `vault/130-evaluation-fiabilite/131-iou-ap-coco.md`: CV-IOU-AP-008 appended.
- `vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md`, revision 9 → 10:
  worked example D (condition and the code lines that guarantee it, per-image cap
  counterexample, LVIS rows and evaluator, the card's operating point); tail-behaviour
  property; measurement-limits bullet; torchvision `nms` lines added to the
  implementation sources; the card listed under related flashcards; closing provenance
  line extended.

For the correction log (to be entered by the coordinator): CV-IOU-AP revision 10;
"a very low score threshold and the full cap" → the tail argument covers a lower
global threshold, not a larger per-image cap (counterexample $1\to0.835$, cocoeval.py
at 8c9bcc3 L259–L260 and L362–L408); "the per-image cap … alters the comparison" →
drops the additions beyond it without lowering AP. No existing card repeats the cap
claim (search for "full cap", "per-image cap" and "maxDets" over `vault/` cards).

## Proposals

P-CV-IOU-AP-01: accepted by the learner on 2026-11-15, completed as CV-IOU-AP-008,
with the parenthetical "(or raising the per-image cap)" corrected as above.

## Sources

Scientific sources:

- Gupta, Dollár and Girshick, LVIS, [arXiv 1908.03195v2](https://arxiv.org/abs/1908.03195):
  PDF text of App. B, B.1 and Table 3 with its caption and the paragraph that comments
  Table 3a.

Implementation sources (Context7 is unavailable in this session):

- cocoapi `PythonAPI/pycocotools/cocoeval.py` at commit
  8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9, GitHub raw: L140–L161 (`evaluate`),
  L163–L180 (`computeIoU` truncation), L235–L313 (`evaluateImg`), L355–L420
  (`accumulate`).
- torchvision v0.29.0, GitHub raw: `torchvision/ops/boxes.py` L20–L42 (`nms`
  docstring); `torchvision/models/detection/roi_heads.py` L705–L735 (score threshold,
  per-class NMS, then the top `detections_per_img`), read to check that a lower score
  threshold cannot displace a higher-scoring output in that postprocessing.

No access failed.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-15-accepted-proposals/checks/131-iou-ap-coco.py` | 8 checks passed, including 3000 randomized instances |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 292 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 292 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/131-iou-ap-coco.md` | 8 cards, no anomaly; CV-IOU-AP-008 514 lexical words |
| `git diff --check -- vault/130-evaluation-fiabilite/` | No whitespace error |

The check script re-implements `evaluateImg` and `accumulate` for one category and one
IoU threshold with exact fractions and a simplified matcher (each detection names the
object it would match); pycocotools itself was not executed. The argument assumes a
postprocessing in which lower-scoring candidates cannot change higher-scoring outputs;
greedy NMS and top-$k$ satisfy it, and other postprocessing must be checked case by
case. The card is longer than its siblings (514 against at most 415 lexical words)
because it carries both the guarantee and its limit. Agent self-review only; the
Obsidian rendering and the AnkiDroid rendering of the card are not verified. Export
status: to republish with `paquet-anki`. The proposal register, the progress log and
the generated catalogue are left to the coordinator.
