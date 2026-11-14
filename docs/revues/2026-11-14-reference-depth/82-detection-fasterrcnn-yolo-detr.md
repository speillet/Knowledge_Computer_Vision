# Review — Detection: Faster R-CNN, YOLO families and DETR — 2026-11-14

## Overview

13 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 10 to revision 11. Highest severity per card before correction:
0 blocking, 0 important, 13 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method and comparison note of the detection topic, a learner
priority. Before this pass it held 2,417 body words, of which roughly 1,800 were
already developed (multi-instance contract, FCOS, FPN, focal loss, GIoU, the
resolution experiment, TIDE, annotation quality, box sizes and the resize/NMS case);
the problem, intuition, assumptions, procedure for Faster R-CNN, YOLO and DETR,
parameters, properties, cost, failure table and alternatives held one or two
sentences each, or nothing. Those sections were filled; the developed ones were kept
with language corrections and small sourced additions. NMS and AP mechanics stay in
[CV-NMS](../../../vault/80-detection-pose/references/81-nms.md) and
[CV-IOU-AP](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md)
and are linked, not restated.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | RPN and detector share convolutional features: confirmed (Faster R-CNN §III, §III-B; 10 ms proposals §I, Table V). Expected answer garbled ("shares features between RPN and head by region"); source cited "§3" of the abs page | Understanding: where the two-stage cost lies | 2 criteria; 366 → 382 words | Notation $K$ for regions clashed with $K$ classes in the reference; changed to $R$ | Minor | Meaning-restoring fix of the expected answer; language fixes; source given §III, §III-B, Table V |
| CV-DETECTEURS-002 | Family members differ in anchors, assignment and NMS: confirmed (YOLOv3 §2.1; YOLOX §2.1; YOLOv10 §1, §3.1 for NMS-free YOLO). "bones", "monitoring policy", "drive difference", "his contract" obscured meaning | Comparison: do not generalize one version | 1 criterion; 328 → 330 words | Aligned with the reference appendix | Minor | Language fixes; YOLOv10 added to the source line |
| CV-DETECTEURS-003 | Hungarian matching assigns supervision; NMS removes duplicates at inference; evaluation matching is distinct: confirmed (DETR §3.1, eqs. 1–2, §4.2). "truth in the field", "Bi-party", "lack of subject matter of the other requests", "overall prediction" (set prediction) | Algorithm: three different matchings | 2 criteria; 360 → 352 words | Aligned with the appendix | Minor | Language fixes in explanation |
| CV-DETECTEURS-004 | Letterbox factor 1/3, 140 px padding, 12 × 9 → 4 × 3, NMS case: recomputed (checks script). Expected answer said "return of boxes" (inverse mapping) and "drive assignment" (training assignment); French decimal commas | Diagnosis: separate geometry, scale and selection losses | 3 criteria; 359 → 375 words | Aligned with the appendix; COCO size-strata source added | Minor | Meaning-restoring fix of the expected answer; decimals; labels |
| CV-DETECTEURS-005 | Throughput versus latency, measurement scope: consistent with Faster R-CNN Table V (per-stage timing). Expected answer said "latency/debit"; source cited "§4.1" | Evaluation: comparable speed claims | 1 list criterion; 351 → 356 words | Aligned with the appendix | Minor | Meaning-restoring fix ("throughput"); language; source given §IV-A, Table V |
| CV-DETECTEURS-006 | FCOS: inside the box, largest distance in the level range, smallest area wins: confirmed (FCOS §3.1, §3.2). "The beach covers" (range), "indoor site", "Hold the boxes" | Algorithm: anchor-free still needs assignment | 3 criteria; 385 → 403 words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-DETECTEURS-007 | $(l,t,r,b)=(20,20,50,40)$ and centre-ness $\sqrt{0.2}$: recomputed. "string normalization" (stride normalization), "**check**", decimals | Practice: distance targets | 1 criterion; 379 → 379 words | Aligned with the appendix | Minor | Language and decimal fixes |
| CV-DETECTEURS-008 | Modulating factor, $\gamma=2$ values, logit gradient: confirmed (focal loss §3.2) and recomputed. "modification of the lens" (objective), "workout", decimals | Understanding: easy-negative dominance | 3 criteria; 403 → 412 words | Aligned with the appendix | Minor | Language and decimal fixes |
| CV-DETECTEURS-009 | GIoU definition and examples: confirmed (GIoU §3) and recomputed. Expected answer "its constant loss at 1"; decimals | Reasoning: signal for disjoint boxes | 2 criteria; 403 → 411 words | Aligned with the appendix | Minor | Language and decimal fixes in the expected answer and explanation |
| CV-DETECTEURS-010 | Top-down path, lateral $1\times1$, addition, $3\times3$: confirmed (FPN §3; nearest-neighbour upsampling by 2 added). Expected answer "The map deep oversampling alone does not return..." garbled | Understanding: lateral connections | 2 criteria; 394 → 399 words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language |
| CV-DETECTEURS-011 | Classification, localization and duplicate definitions: confirmed (TIDE §2.2). Expected answer used "Location" for TIDE's localization error and omitted "higher-scoring" in the duplicate definition. The question uses French decimal commas (see Proposals) | Diagnosis: TIDE categories | 3 criteria; 386 → 397 words | Aligned with the appendix | Minor | Sourced terminology fix of the expected answer; language |
| CV-DETECTEURS-012 | Unmatched confident detection may be an annotation omission: confirmed (TIDE §3.4, App. D, E). Expected answer "The trust of the model" (confidence) | Diagnosis: annotation versus model error | 2 criteria; 309 → 321 words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language |
| CV-DETECTEURS-013 | Instances, classes and labels are distinct; YOLOv3 logistic classifiers: confirmed (YOLOv3 §2.2). Expected answer "Multi-tag"; explanation implied that a per-box softmax yields exclusive outputs, whereas torchvision 0.29's Faster R-CNN outputs every class above 0.05 as a separate detection (roi_heads.py L680–L735) | Understanding: output contract | 3 criteria; 396 → 438 words | Aligned with the appendix | Minor | "Multi-label" fix; one sentence on score versus output exclusivity; torchvision source added |

Expected-answer changes (language or sourced terminology; no scientific error was
found in an expected answer):

- CV-DETECTEURS-001: "No: the design shares features between RPN and head by region,
  with extraction of regional representations." → "No: the RPN and the per-region head
  share the convolutional feature maps computed once by the backbone; each region's
  representation is pooled from those shared maps."
- CV-DETECTEURS-004: "First check the return of boxes with resize and padding. Then
  measure their effective size and recall of these same objects before filtering, after
  score threshold, then after NMS possible. … examine scale, features, and drive
  assignment." → "First check that boxes are mapped back correctly through the resize
  and the padding. Then measure the objects' effective size and the recall of these same
  objects before filtering, after the score threshold, then after NMS if any. …
  examine scale, features and training assignment."
- CV-DETECTEURS-005: "… transfers and latency/debit protocol." → "… transfers and the
  latency/throughput protocol."
- CV-DETECTEURS-006: "Hold the boxes containing the site and compatible with the
  distance range of the FPN level. If there are several, choose the smaller area; …" →
  "Keep the boxes that contain the site and whose largest edge distance falls in the FPN
  level's range. If there are several, choose the box with the smallest area; …"
- CV-DETECTEURS-009: "… so IoU remains zero and its constant loss at 1. GIoU subtracts
  from IoU the empty fraction of the smallest rectangle aligned on the axes containing
  the two boxes" → "… so IoU remains zero and the loss stays constant at 1. GIoU
  subtracts from IoU the empty fraction of the smallest axis-aligned rectangle
  containing the two boxes".
- CV-DETECTEURS-010: "It combines the deep semantic representations brought up by the
  descending path with the finer and better localized features of the backbone. The map
  deep oversampling alone does not return spatial information from these fine levels."
  → "They combine the semantically strong deep features brought down by the top-down
  path with the finer, better-localized backbone features of the same level. Upsampling
  the deep map alone does not restore the spatial information of these finer levels."
- CV-DETECTEURS-011: "(a) Classification: Sufficient localisation, bad class. (b)
  Location: good class, intermediate overlap. (c) Duplicate: class and localisation
  sufficient, but the GT already has an associated detection." → "(a) Classification:
  sufficient localization, wrong class. (b) Localization: correct class, intermediate
  overlap. (c) Duplicate: class and localization sufficient, but the GT is already
  matched to a higher-scoring detection." Source: TIDE §2.2 names the "Localization
  Error" and defines a duplicate by "another higher-scoring detection already matched".
- CV-DETECTEURS-012: "Confronting the image … counted FP … The trust of the model is not
  enough …" → "Compare the image … counted as an FP … The model's confidence is not
  enough …"
- CV-DETECTEURS-013: "Multi-tag means …" → "Multi-label means …"

## Reference findings

Claims of revision 10 checked against their passages (none found false):

- Multi-label logistic classifiers in YOLOv3 §2.2, box regression §2.1, three scales
  §2.3: confirmed.
- FCOS location rule, minimal-area tie-break, level ranges, centre-ness eq. 3:
  confirmed (§3.1–§3.3); the ranges $m_2..m_7=(0,64,128,256,512,\infty)$ are now stated.
- FPN lateral $1\times1$, element-wise addition, $3\times3$ smoothing: confirmed (§3);
  nearest-neighbour $2\times$ upsampling and $d=256$ added.
- Focal loss factors 0.01 and 0.81 at $\gamma=2$: recomputed; the paper's "100× lower
  at $p_t=0.9$" and "1000× at 0.968" agree (§3.2).
- GIoU definition and constructed values: recomputed.
- TIDE six types, thresholds $t_b=0.1$, $t_f=0.5$, individual oracles, non-additivity
  (App. A.1), annotation examples (§3.4, App. D, E): confirmed.
- Imprecise citations: "Faster R-CNN §3" (the paper numbers sections in Roman
  numerals; the passages are §III, §III-B and Table V of §IV-A) and the card-005
  pointer "§4.1" (timing is Table V in §IV-A).

New claims verified for revision 11 (main ones): Faster R-CNN anchors, eq. 2,
labelling 0.7/0.3, 256 sampled anchors, cross-boundary anchors, proposal NMS 0.7 and
the 6000-proposal ablation, Table V timing, Table VIII anchors, Table IX $\lambda$;
YOLO v1 grid, tensor, loss weights, 98 boxes, NMS +2–3% mAP, §2.4 limitations, §4.2
error profile; YOLOv3 box decoding; YOLOX anchor-free and edge-device remark; YOLOv10
dual assignments; RetinaNet anchors, 0.5/0.4 assignment, normalization by assigned
anchors, inference filters, prior $\pi=0.01$, $\alpha$/$\gamma$ coupling, §3.4
two-stage sampling; FCOS BPR and ambiguous-sample percentages; ATSS §3.3 equal-AP
result and §4.1 algorithm; DETR eqs. 1–2, box loss, $\varnothing$ weight, $N=100$,
loss weights, architecture, auxiliary losses, NMS-per-layer result, second-class
override (+2 AP), Table 1, App. A.3 complexity, App. A.5 saturation; Deformable DETR
convergence, complexity and defaults; DINO abstract; COCO evaluation (mask-area
strata, 100 detections, 41% small objects).

Disagreements between papers and torchvision 0.29.0, recorded in the note (FR-036):

| Aspect | Paper | torchvision v0.29.0 |
| --- | --- | --- |
| FCOS location point | $\lfloor s/2\rfloor+ks$ (FCOS §3.1) | $ks$ (`anchor_utils.py` L101–L103) |
| FCOS positives | Every interior location whose largest distance is in $[m_{i-1},m_i]$ (§3.1–§3.2) | Centre sampling within 1.5 strides and open bounds $(4s,8s)$ (`fcos.py` L455–L482): 9 positives instead of 70 for the constructed $70\times60$ box |
| FCOS ranking score | class score × centre-ness (§3.3) | $\sqrt{\sigma(\text{cls})\sigma(\text{ctr})}$, threshold 0.2, NMS 0.6 (`fcos.py` L370–L381, L516–L519); same ranking, different threshold scale |
| RPN proposals | One feature map; NMS 0.7 leaving ~2000 (§III-C) | Pre-NMS top-n and NMS per FPN level; 2000/2000 train, 1000/1000 test (`rpn.py` L231–L240, L276–L292) |
| Box coder | Eq. 2 unweighted | Weights $(10,10,5,5)$ in the R-CNN head and a clamp at $\log(1000/16)$ (`roi_heads.py` L542–L544, `_utils.py` L183–L213) |
| Input scale | Shorter side 600 px (§III-C) | 800 / 1333 px, bottom-right zero padding to a multiple of 32 (`transform.py`) |
| RetinaNet detections per image | Not stated; COCO evaluates 100 | 300 (`retinanet.py` L430–L435) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 2,417 → 8,654. Of these, about 7,100 are prose,
1,230 table cells and 280 pseudocode and Mermaid lines. Of the prose, about 1,800 words
are the previously developed subsections, kept with language fixes. The size reflects
three detector families, their assignment and post-processing rules, the
torchvision contracts and a failure table; method depth for NMS and AP stays in the
sibling notes.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (one sentence plus the multi-label subsection) | Developed | Output set definition, COCO object statistics, coordinate and box-encoding conventions, torchvision input, target and output contract, pipeline role; multi-label subsection kept, plus the softmax-versus-output exclusivity point |
| Intuition | Shallow (three sentences) | Developed | Slots, assignment and post-processing as the common frame; one paragraph per family; assignment-determines-NMS and ATSS results; constructed pallet illustration; Mermaid data flow |
| Prerequisites | Developed (two links) | Developed | Links to CV-REPRESENTATIONS, CV-ACQUISITION, CV-FIABILITE, CV-PIPELINE, CV-QUANT and downstream notes |
| Assumptions | Absent | Developed | Closed label set and annotation exhaustiveness (TIDE §3.4 figures), box representation, scale coverage per family, output capacity (YOLO grid, DETR saturation, caps), separable duplicates, train-deploy consistency, degenerate cases |
| Procedure | Partial (FCOS and FPN only) | Developed | Faster R-CNN pseudocode and purpose of each step; YOLO v1, v3, YOLOX, YOLOv10, RetinaNet, ATSS; FCOS ranges and ambiguity figures; DETR pseudocode, NMS-per-layer and second-class override; Deformable DETR, DINO |
| Mathematics | Developed (FCOS targets, focal loss, GIoU) | Developed | Box parameterizations (eq. 2, coder weights, YOLOv3, DETR); worked examples A (anchor IoU, labels, encoding), B (FCOS levels, paper versus torchvision), C (Hungarian versus greedy), D (easy-negative dominance); DETR matching cost and loss; candidate counts |
| Parameters | Shallow (one line) | Developed | Eight-row table with source values, effects and interactions; five-step tuning approach |
| Properties | Absent | Developed | Translation, scale, permutation, anchor-free equivalence (ATSS), score calibration, error profiles and DETR/Faster R-CNN results under one protocol, training cost |
| Cost and implementation | Shallow (two sentences) | Developed | Cost drivers with variables, Table V timing, DETR complexity and FLOPs, real-time figures with hardware; torchvision 0.29 contracts with line numbers and execution status |
| Evaluation | Developed (resolution experiment) | Developed | COCO protocol details (mask-area strata), per-stage recall, published comparison caveat; experiment language fixed, confound added; measurement limits |
| Failure modes and diagnosis | Partial (two sentences plus TIDE and annotation subsections) | Developed | Ten-row Symptom / Causes / Check / Remedy table; TIDE, annotation, box-size and resize/NMS subsections kept and corrected |
| Alternatives and sources | Shallow (one sentence; sources not split) | Developed | Six conditional choices including non-learned localization; four industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/82-detection-fasterrcnn-yolo-detr.py`](checks/82-detection-fasterrcnn-yolo-detr.py)
(32 assertions): anchor IoU 0.432 and its labels, eq. 2 targets and the weighted coder,
decoding round trip, clamp $e^{\log(1000/16)}=62.5$; FCOS targets, centre-ness and
level membership (70 paper positives versus 9 torchvision positives, boundary at
64 px); Hungarian 0.55 versus greedy 1.10 and duplicate argmin; focal factors, the
14.5× and 172× dominance ratios and the prior bias $-4.595$; GIoU values; the four
box-size IoUs; letterbox geometry, round trip and the $5/11$ NMS case; torchvision's
0.694 scale and COCO small strata; YOLO v1 tensor, RetinaNet anchor count, Faster
R-CNN anchor count, DETR token ratio 16 and Table V sums.

## Applied corrections

- [Reference](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md),
  revision 10 → 11: body rewritten and deepened as above; mistranslations fixed in the
  body and appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "Documentary reference" → "Source consulted", "Reading the
  calculation share" → "How the computation is shared", "Example of comparison built"
  → "Constructed comparison", "Cost scales" → "Cost scaling", "Versioned Decoding" →
  "Versioned decoding", "Cost of Matching" → "Matching cost", "Recurrence of fusion" →
  "Fusion recurrence", "check of annotations" → "Annotation audit", "Probability and
  contract of labels" → "Probability and label contract", "ignorance/crowd" →
  "ignore or crowd regions", "entry letterbox" → "letterboxed input", "accuracy and
  batch" → "numeric precision and batch", "YOLov3" → "YOLOv3", French decimal commas
  in prose, tables and math); the appendix copy of the CV-DETECTEURS-011 question uses
  decimal points; the line "[eq. 2]:" that the validator parsed as a link definition
  was rephrased; sources split; closing provenance line replaced while keeping the
  2026-10-18 drafting date and the 2026-10-21 enrichment. Front matter unchanged except
  `revision`; H1, per-card headings and `### Box sizes, aspect ratios and accuracy`
  kept verbatim.
- [Cards](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md): the
  expected-answer changes listed above; identical language fixes in the explanations
  and appendices (73 replacements, each matched exactly once). Source lines of
  CV-DETECTEURS-001, 002, 004, 005 and 013 now give exact sections or code lines.
  Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` for the corrected terms and
for NMS-free, anchor-free, Hungarian and COCO size-strata statements; CV-IOU-AP already
states mask-area strata).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-DETECTEURS-01 | CV-DETECTEURS | Given an anchor and a ground-truth box, compute their IoU, the RPN and RetinaNet labels, and the eq. 2 targets; explain why decoding with another variant's coder weights gives a wrong box | Anchor-based encoding and IoU-threshold assignment are untested; only FCOS distances have a practice card | Practice; Mathematics, worked example A | 1 card, 3 criteria | [Faster R-CNN §III-A2, eq. 2](https://arxiv.org/html/1506.01497v3); [RetinaNet §4](https://arxiv.org/html/1708.02002v2); [torchvision 0.29 `_utils.py` L183–L213](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/models/detection/_utils.py#L183-L213) |
| P-CV-DETECTEURS-02 | CV-DETECTEURS | Choose among a two-stage, a dense one-stage and a DETR-family detector under stated constraints (crowded overlapping objects, NPU latency budget, small objects, training budget) and name one discriminating test | The design family is absent; no card trains the decision this comparison note exists for | Design; Alternatives and applications | 1 card, 3–4 criteria | [DETR §4.1–§4.2, Table 1](https://arxiv.org/html/2005.12872v3); [Deformable DETR §1](https://arxiv.org/html/2010.04159v4); [YOLOv10 §3.1](https://arxiv.org/html/2405.14458v2) |

Question proposal (not applied; questions are verbatim invariants): CV-DETECTEURS-011
uses French decimal commas in math ($t_b=0{,}1$, $t_f=0{,}5$, IoU $0{,}8$ and $0{,}3$),
rendered "0,1" on the card front. Proposed wording: "Three independent cases each have
one “car” GT instance, without ignore/crowd annotations. With TIDE thresholds
$t_b=0.1$ and $t_f=0.5$, which error describes each FP: (a) “truck,” IoU $0.8$; (b)
“car,” IoU $0.3$; (c) “car,” IoU $0.8$, with the GT already matched to a higher-score
box?"

## Sources

Scientific sources, opened at the passages listed (arXiv HTML converted to text):

- Ren et al., Faster R-CNN, [arXiv HTML v3](https://arxiv.org/html/1506.01497v3): §I,
  §III, §III-A, §III-A1, §III-A2 (eqs. 1–2), §III-A3, §III-C, §IV-A (Tables II, V,
  VIII, IX and ablation text), §IV-B.
- Redmon et al., YOLO, [arXiv HTML v5](https://arxiv.org/html/1506.02640v5): §1, §2,
  §2.2, §2.3, §2.4, §4.1, §4.2.
- Redmon and Farhadi, YOLOv3, [arXiv HTML v1](https://arxiv.org/html/1804.02767v1):
  §2.1–§2.3.
- Ge et al., YOLOX, [arXiv HTML v2](https://arxiv.org/html/2107.08430v2): §2.1.
- Wang et al., YOLOv10, [arXiv HTML v2](https://arxiv.org/html/2405.14458v2): abstract,
  §1, §3.1.
- Lin et al., FPN, [arXiv HTML v2](https://arxiv.org/html/1612.03144v2): §1, §3, §4.1,
  §4.2 (eq. 1).
- Lin et al., focal loss, [arXiv HTML v2](https://arxiv.org/html/1708.02002v2): §3.2,
  §3.3, §3.4, §4, §4.1 (including its "Initialization" paragraph), Table 1 caption and
  §5.1 (prior and $\gamma$ ablations).
- Tian et al., FCOS, [arXiv HTML v5](https://arxiv.org/html/1904.01355v5): §3.1–§3.3,
  §4.1 (Tables 1–3 text).
- Zhang et al., ATSS, [arXiv HTML v4](https://arxiv.org/html/1912.02424v4): abstract,
  §1, §3.3, §4.1.
- Carion et al., DETR, [arXiv HTML v3](https://arxiv.org/html/2005.12872v3): §2.1,
  §2.3, §3, §3.1, §3.2, §4, §4.1 (Table 1), §4.2 (Figure 4), §4.3, App. A.3, A.4, A.5.
- Zhu et al., Deformable DETR, [arXiv HTML v4](https://arxiv.org/html/2010.04159v4):
  abstract, §1, §3, §4.1, §5, App. A.1.
- Zhang et al., DINO, [arXiv abstract page](https://arxiv.org/abs/2203.03605): abstract
  only.
- Rezatofighi et al., GIoU, [arXiv HTML v2](https://arxiv.org/html/1902.09630v2): §1,
  §3.
- Bolya et al., TIDE, [arXiv HTML v2](https://arxiv.org/html/2008.08115v2): §2.1–§2.3,
  §3.4, App. A.1 heading and text, App. D and E headings.
- COCO detection evaluation, [cocodataset.org/#detection-eval](https://cocodataset.org/#detection-eval):
  the page content was read from `https://cocodataset.org/dataset/detection-eval.htm`,
  which the site loads into that anchor.

Implementation sources (official code at tag v0.29.0, read as raw files):
`faster_rcnn.py`, `transform.py`, `generalized_rcnn.py`, `rpn.py`, `roi_heads.py`,
`_utils.py`, `retinanet.py`, `fcos.py` and `anchor_utils.py` under
[torchvision/models/detection](https://github.com/pytorch/vision/tree/v0.29.0/torchvision/models/detection),
at the line ranges cited in the note.

Failed accesses and limits:

- `https://cocodataset.org/detection-eval.htm` returned HTTP 404; the
  `dataset/detection-eval.htm` path worked.
- Context7 was not available in this session; official versioned code replaced it.
- Not re-read in this pass: Soft-NMS §4 (accessed on 2026-10-21; only the suppression
  mechanism is cited); the original YOLO CVF page (the arXiv HTML was read instead);
  the full DINO paper (only its abstract supports the one sentence used).
- DETR's frame rates in Table 1 are cited without hardware because the passage read
  does not state it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | FAIL only on `40-features-matching/references/45-recalage-ecc.md` ("missing local link or outside vault: ECC"), a file of another subject being edited in parallel; no error in this subject's files (an earlier run before that edit returned OK: 142 Markdown documents, 60 references, 282 cards) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 268 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/82-detection-fasterrcnn-yolo-detr.py` | 32 checks passed |
| `git diff --check -- vault/80-detection-pose/ docs/revues/2026-11-14-reference-depth/checks/82-detection-fasterrcnn-yolo-detr.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md` | 13 cards, 321 to 438 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 10` → `11`; H1, per-card headings and the linked heading unchanged; `$$` and code fences balanced; every appendix paragraph identical to its card paragraph; local links and anchors resolve |

No detector, torchvision call or benchmark was executed; the resolution experiment is a
protocol, not a result. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-DETECTEURS revision 11, cards 001, 004, 005, 006, 009, 010, 011, 012 and 013 for
expected-answer fixes and all 13 cards for language fixes, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-DETECTEURS-01, P-CV-DETECTEURS-02).
