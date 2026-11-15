# Review — Detection: Faster R-CNN, YOLO families and DETR — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-DETECTEURS-01. One card added,
CV-DETECTEURS-014; the thirteen existing cards were read to avoid a duplicate but not
re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/82-detection-fasterrcnn-yolo-detr.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 11 → 12.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-014 | RPN labelling (highest-IoU anchor or anchors of a box, or IoU "higher than 0.7"; negative "lower than 0.3 for all ground-truth boxes"; others "do not contribute") and eq. 2: confirmed in Faster R-CNN §III-A2 (§3.1.2 of the PDF). RetinaNet: positive at IoU 0.5, background in $[0,0.4)$, ignored in $[0.4,0.5)$, "the assignment rule from RPN … with adjusted thresholds", standard R-CNN box parameterization: confirmed in §4, "Anchors" and "Box Regression Subnet". torchvision v0.29.0: encoding multiplies by the weights (_utils.py L103–L116); decoding divides by them, then clamps $t_w,t_h$ at $\log(1000/16)$, with centres $x_1+0.5w$ (L183–L224); matcher $\ge$ high and $<$ low (L339–L345, L384–L387) with highest-IoU matches (L397–L416) enabled in rpn.py L169–L173 and retinanet.py L462–L467; weights $(1,1,1,1)$ in rpn.py L164 and retinanet.py L244, L470, $(10,10,5,5)$ in roi_heads.py L542–L544. Fast R-CNN §2.3: targets normalized to zero mean and unit variance. IoU 0.632, targets, wrong decodings and the $t=0$ invariance: project calculations, recomputed by the check script | Practice: anchor encoding and IoU-threshold assignment were untested (CV-DETECTEURS-006 and 007 cover FCOS locations and distances, 003 Hungarian matching); the coder-weight mismatch is a silent deployment error | 3 expected criteria (IoU and both labels; eq. 2 targets; head targets and the wrong decoded box with its cause); 497 lexical words | Notation $t$, $x_a$, $w_a$ of the reference; same anchor as worked example A, with a ground truth chosen so that the two labelling rules disagree (example A's IoU 0.432 is ignored by both) | Practice |

The question gives the weights of both coders, because applying them is the practice
objective; it does not say that the decoder divides by them.

## Reference findings

The numbers of worked example A were correct (IoU 0.432 recomputed here; its targets
were recomputed by the 2026-11-14 check script). Three imprecisions:

- Example A said that RetinaNet ignores the anchor "unless it is the best anchor of
  this box". The RetinaNet paper states only the adjusted thresholds and does not
  restate the RPN's highest-IoU clause (§4, "Anchors"); torchvision enables that clause
  for RetinaNet (retinanet.py L462–L467) and for the RPN (rpn.py L169–L173). The
  attribution is now explicit.
- The torchvision Faster R-CNN defaults gave "IoU 0.7 / 0.3" without the boundary:
  the matcher counts IoU $\ge0.7$ as positive (_utils.py L339–L345, L384–L387) where
  the paper says "higher than 0.7", and adds each box's highest-IoU anchors. Added.
- The box-coder paragraph said that the weights multiply the targets, but not that
  decoding divides the network output by them, nor that the clamp acts after that
  division (_utils.py L200–L208). Added, with Fast R-CNN's target normalization as
  context and the statement that the weights belong to a head's output contract.

Absent and added for the card: a second anchor and ground-truth pair on which the RPN
and RetinaNet labels disagree, and the two wrong decodings with their $t=0$
invariance.

## Applied corrections

- `vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md`: CV-DETECTEURS-014
  appended.
- `vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md`, revision
  11 → 12: box-coder paragraph (division at decoding, clamp order, Fast R-CNN
  normalization); worked example A (attribution of the highest-IoU clause; second pair
  from the card); torchvision contracts for the Faster R-CNN and RetinaNet matchers;
  Fast R-CNN added to the scientific sources; `_utils.py`, `rpn.py` and `retinanet.py`
  line ranges extended; the card listed under related flashcards; closing provenance
  line extended.

For the correction log (to be entered by the coordinator): CV-DETECTEURS revision 12;
highest-IoU exception attributed to RetinaNet's paper → stated for the RPN in Faster
R-CNN §III-A2 and enabled for RetinaNet by torchvision (retinanet.py L462–L467);
torchvision RPN matcher boundary $\ge0.7$ added; decoding by division and clamp order
added (_utils.py L200–L208). No existing card stated the RetinaNet clause or the
weights (search for "best anchor", "highest-IoU", "10,10,5,5" and "BoxCoder" over
`vault/`).

## Proposals

P-CV-DETECTEURS-01: accepted by the learner on 2026-11-15, completed as
CV-DETECTEURS-014.

## Sources

Scientific sources:

- Ren et al., Faster R-CNN, [arXiv 1506.01497v3](https://arxiv.org/html/1506.01497v3):
  PDF text of §3.1.2 "Loss Function" (labelling rule, eq. 1, eq. 2); the HTML table of
  contents confirms that this section is numbered §III-A2 there.
- Lin et al., Focal Loss, [arXiv 1708.02002v2](https://arxiv.org/html/1708.02002v2):
  PDF text of §4, paragraphs "Anchors" and "Box Regression Subnet"; HTML table of
  contents for the paragraph names.
- Girshick, Fast R-CNN, [arXiv 1504.08083v2](https://arxiv.org/abs/1504.08083): PDF
  text of §2.3, paragraph "Multi-task loss".

Implementation sources, read at tag v0.29.0 on GitHub raw (Context7 is unavailable in
this session):

- `torchvision/models/detection/_utils.py` L80–L225 (`encode_boxes`, `BoxCoder`) and
  L313–L420 (`Matcher`);
- `rpn.py` L160–L176 and L200–L227 (coder, matcher, anchor labels);
- `roi_heads.py` L536–L545 (matcher without low-quality matches, coder weights);
- `retinanet.py` L240–L245 and L455–L471 (coder weights, matcher);
- `faster_rcnn.py` L184–L200 (default thresholds, `bbox_reg_weights=None`).

No access failed.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-15-accepted-proposals/checks/82-detection-fasterrcnn-yolo-detr.py` | 10 checks passed |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 292 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 292 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md` | 14 cards, no anomaly; CV-DETECTEURS-014 497 lexical words |
| `git diff --check -- vault/80-detection-pose/` | No whitespace error |

The check script re-implements the torchvision formulas in the standard library; no
torchvision code or network was executed, and the C++ deployment of the question is a
constructed scenario. The card's answer is longer than its siblings (497 against at
most 438 lexical words) because it carries two labelling rules and two decoding
directions. Agent self-review only; the Obsidian rendering and the AnkiDroid rendering
of the card are not verified. Export status: to republish with `paquet-anki`. The
proposal register, the progress log and the generated catalogue are left to the
coordinator.
