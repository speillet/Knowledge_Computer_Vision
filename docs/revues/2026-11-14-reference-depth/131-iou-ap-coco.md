# Review — IoU and AP — the COCO detection protocol — 2026-11-14

## Overview

7 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 4 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a metric and protocol note. Detector mechanisms, GIoU as a loss and
the TIDE error types stay in
[CV-DETECTEURS](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md)
and NMS in [CV-NMS](../../../vault/80-detection-pose/references/81-nms.md); this note
links to them. The 2026-11-08 report of this subject keeps its `## Sources` heading
(linked from `Suivi-pilote.md`); this report also has one.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Continuous-box IoU without `+1`: confirmed by `bbIou` (maskApi.c L109–L120); results boxes are `[x,y,width,height]` from the top-left corner (results format §1): confirmed. Expected answer said "unity" (unit) and "continuous/inclusive agreement" (convention); explanation said "driver's" (pilot's); Source label misspelled `valuateImg` and attributed constructed examples to the code | Practice: fix a box contract before computing an overlap | 3 criteria; 388 → 393 lexical words | Aligned with reference worked example A | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact lines |
| CV-IOU-AP-002 | Ten thresholds 0.50:0.05:0.95, 101 recall levels, categories with valid GT: confirmed (detection eval §2; `Params` L502–L511; `summarize` L452–L455). Expected answer said "accuracy/recall ranking" for the precision/recall trade-off, with French decimal commas; blocking error "average of recoveries" for mean overlap | Understanding: separates a pairwise measure from an aggregated protocol | 3 criteria; 395 → 408 | "uses undefined entries" corrected to "marks such entries as undefined ($-1$)" (L334, L452–L455) | Important | Meaning-restoring fix of the expected answer; language fixes; Source line given exact lines |
| CV-IOU-AP-003 | One ordinary GT justifies one TP; duplicates are FPs: confirmed (`evaluateImg` L272–L296; VOC §4.2 "5 detections of a single object counted as 1 correct detection and 4 false detections"). Missing condition: the TP is the higher-*scored* box, not the better-overlapping one (code and VOC assign in decreasing confidence; TIDE §2.1 describes the opposite rule) | Algorithm: duplicate handling and its rank effect | 2 criteria; 306 → 331 | "accuracy" used for precision; "the ignored crowd and GT" | Minor | Score-order condition added to the explanation; language fixes; Source line now cites L272–L296 and VOC §4.2 |
| CV-IOU-AP-004 | AP101 $=(51+50\cdot2/3)/101\approx0.834983$: recomputed (checks script, check 9; `examples/pilot_math.py`). Explanation said the duplicate "raises the current accuracy to half": the precision *falls* from 1 to 0.5. "Reminders" for recall levels | Reasoning: reconstruct an interpolated AP | 3 criteria; 403 → 415 | Decimal commas in the expected answer | Important | Meaning-restoring fix of decimals in the expected answer; direction of the precision change corrected; language fixes; Source line cites `accumulate` L384–L408 |
| CV-IOU-AP-005 | Per-image-and-category cap in code versus "at most 100 top-scoring detections per image (across all categories)" on the COCO page: confirmed (L173–L176, L362; detection eval §2). Missing condition: at `8c9bcc3` a dataset's `ignore` field is overwritten by `iscrowd` (L107–L109). Expected answer said "reviewer version" for evaluator version | Evaluation: attribute a metric discrepancy before blaming the model | 3 criteria; 385 → 407 | "string" used for pipeline (French *chaîne*) | Important | Meaning-restoring fix of the expected answer; `ignore` condition added; language fixes; Source line cites the lines |
| CV-IOU-AP-006 | $(a-\delta)/(a+\delta)$ and $\delta<a(1-\tau)/(1+\tau)$; $9/11$, $8/12$: recomputed (checks 4–8) | Diagnosis: AP50/AP75 gap as a localization and coordinate signature | 2 criteria; 365 → 363 | "pretreatment", "new drive" (retraining), decimal commas in the explanation | Minor | Language fixes; Source line cites §2 and `evaluateImg` |
| CV-IOU-AP-007 | Alert precision $r\pi/[r\pi+f(1-\pi)]\approx0.090$: recomputed (check 22). The explanation called this quantity "accuracy of the alerts": it is precision (positive predictive value) | Evaluation: link a benchmark average to an acceptance decision | 3 criteria; 319 → 316 | "false releases", "timeliness" (latency) | Important | Terminology corrected in the explanation; language fixes; Source line cites `summarize` and labels constructions |

Expected-answer changes (meaning-restoring language fixes; no sourced scientific change):

- CV-IOU-AP-001: "fix format, coordinate frame, unity, validity and continuous/inclusive
  agreement." → "Fix the format, coordinate frame, unit, validity and the continuous or
  inclusive pixel convention."
- CV-IOU-AP-002: "AP50 and AP75 evaluate the accuracy/recall ranking with a threshold
  set at 0,50 or 0,75. The main COCO AP averages ten thresholds from 0,50 to 0,95 per
  step of 0,05, as well as valid categories and protocol recall levels." → "AP50 and
  AP75 evaluate the precision/recall trade-off of a score ranking with the IoU
  threshold fixed at 0.50 or 0.75. The main COCO AP averages ten IoU thresholds from
  0.50 to 0.95 in steps of 0.05, as well as valid categories and the protocol's recall
  levels." The first sentence "measures a region overlap" became "measures the overlap
  of one pair of regions".
- CV-IOU-AP-004: "recalls $0,5;0,5;1$, precisions $1;0,5;2/3$. The maximum envelope to
  the right is 1 up to and including the 0,5 recall, then $2/3$. So
  $AP=(51+50\times2/3)/101\approx0,834983$." → "Recalls $0.5;\,0.5;\,1$, precisions
  $1;\,0.5;\,2/3$. The right-to-left maximum envelope is 1 up to and including recall
  0.5, then $2/3$. So $AP=(51+50\times2/3)/101\approx0.834983$."
- CV-IOU-AP-005: "reviewer version" → "evaluator version".

## Reference findings

Claims of revision 8 checked against their passages, all confirmed: ten IoU thresholds
and 101 recall levels (`Params` L502–L507); envelope and zero for unreachable recalls
(L398–L408); `maxDets` per image and category with `useCats=1` (L173–L176, L260, L362)
against the page's global cap (§2); crowd overlap $|D\cap G|/|D|$ (`bbIou` L117,
`rleIou` L93); unmatched detections outside the area range ignored (L297–L299);
categories without valid GT excluded (L372–L374, L452–L455) and categories with GT
but no detection at 0. No scientific error was found in the body; it was shallow and
mistranslated ("classified" for ranked, "reminders" for recall levels, "accuracy" for
precision, "AP null", "Protocol corners not to be erased", French table header
"Explication", "Connexions", "Competences", French link label "Description officielle",
decimal commas).

New claims verified for revision 9 (main ones): COCO area as mask pixels, size shares,
AR definition, no AP/mAP distinction (detection eval §2); results and data formats
(results format §1, data format §1); `loadRes` sets box area $w\cdot h$, `iscrowd=0`
and asserts image ids (coco.py L323–L340); mask pairs of different sizes get IoU $-1$
(`rleIou` L84); `ignore` overwritten by `iscrowd` (L107–L109); closed area intervals
(L251); `summarize` default-only (L425, L436); `np.float` (L378–L379) and its expiry
in NumPy 1.24.0; VOC 11-point AP, "must exceed 0.5", threshold set low for box
inaccuracies, duplicates false, assignment by decreasing confidence (Everingham et al.
§4.2), "difficult" exclusion (§3.3); GIoU definition and properties, $1-\text{IoU}$ a
metric, scale invariance (Rezatofighi et al. §3, Alg. 1); LVIS federated sets and the
"not evaluated" rule (§2.2), per-category AP instability and non-exhaustive flags
(§2.3), score-threshold effect (App. B, Table 3a); TIDE error types, oracles and
progressive-error bias (§§2.1–2.3); torchvision 0.29.0 `box_iou` formats and missing
epsilon, `generalized_box_iou` contract.

Source disagreements recorded in the note (FR-036):

| Aspect | Source A | Source B |
| --- | --- | --- |
| Match criterion | VOC: overlap "must exceed 0.5" (§4.2, eq. 3) | COCO code: $\operatorname{IoU}\ge t$ (L276, L286) |
| Detection cap | COCO page: 100 per image across categories (§2) | Code: per image and per category (L173–L176, L362) |
| Which duplicate becomes TP | TIDE §2.1: "the one with the highest overlap" | VOC §4.2 and COCO code: decreasing confidence order |
| Size-bucket bounds | Page: strict inequalities | Code: closed intervals, boundary areas in both buckets (L251) |
| Degenerate boxes | `bbIou`: 0 when overlap width or height ≤ 0 | torchvision `box_iou`: $0/0$ for two zero-area boxes (code reading, not executed) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 815 → 4,855. The length comes from the protocol's
many rules (matching, crowd, area, caps, accumulation), four worked examples and the
diagnosis table; detector and loss content was linked to 81 and 82 instead of restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Ground-truth and results contracts (fields, origin, units, mask area, category mapping); output arrays and shapes; pipeline role; what AP does not measure |
| Intuition | Shallow (absent) | Developed | Retrieval reading of AP; constructed duplicate-rank illustration; Mermaid data flow of `COCOeval` |
| Prerequisites | Shallow (three links) | Developed | Links to CV-DETECTEURS, CV-NMS, CV-SEGMENTATION, SORT, CV-FIABILITE, CV-METRIQUES-APPLIQUEES; target competencies |
| Assumptions | Absent | Developed | Exhaustive annotation and LVIS federated alternative; annotation noise; shared frame; comparable scores; category independence; seven degenerate cases with code lines; observability |
| Procedure | Shallow | Developed | Pseudocode of evaluate, accumulate and summarize; purpose of each step with VOC and code citations |
| Mathematics | Shallow | Developed | IoU, crowd overlap, mask IoU, GIoU, OKS; precision, recall, envelope, AP101 with bound; averages and AR; VOC 11-point; worked examples A–D |
| Parameters | Absent | Developed | Table of `iouThrs`, `recThrs`, `maxDets`, `areaRng`, `useCats`, `iouType`, subsets; upstream parameters; four-step protocol-fixing approach |
| Properties | Absent | Developed | IoU metric and invariances; ranking invariance; greedy versus maximum matching; tail behavior; macro-averaging and rare-category noise; annotation dependence |
| Cost and implementation | Shallow (two sentences) | Developed | Cost drivers with variables; array size; pycocotools `8c9bcc3` contracts (cap, `ignore`, area, `np.float`, `summarize`); torchvision 0.29.0 contracts; execution status |
| Evaluation | Shallow | Developed | Evaluator validation tests; paired bootstrap for uncertainty; baseline and score-threshold variation with expected effect and limits |
| Failure modes and diagnosis | Shallow (three rows) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (COCO, VOC, LVIS, TIDE, operating-point, mask and identity metrics); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/131-iou-ap-coco.py`](checks/131-iou-ap-coco.py) (22 checks): format ambiguity
(IoU 1/3, areas 400 and 1,200 px²), scale invariance, shift allowances
(1/3, 1/7, 1/39; 3.33/1.43/0.26, 10.67/4.57/0.82, 32.0/13.71/2.46 px), size-ratio
allowances (1.414, 1.155, 1.026), AP101 per threshold (0.834983 ×5, 0.504950 ×2, 0 ×3;
mean 0.518482), VOC 11-point 0.848485, tail examples (56/101, 76.4/101, unchanged with
FPs only), AP bound, crowd overlap, greedy matching, array size 969,600 and alert
precision 0.0902.

## Applied corrections

- [Reference](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md),
  revision 8 → 9: body rewritten and deepened as above; mistranslations fixed in the
  appendices, identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Example of contract" → "Contract
  example", "**check**" → "**Discriminating check**", "Calculation of sides" →
  "Computing the sides", "encompassing rectangles aligned on the axes" → "axis-aligned
  bounding rectangles", "The form contract is as important as the contact information"
  → "The shape contract matters as much as the coordinates", "digital production
  threshold" → "fixed numeric production threshold", "Algorithm of the envelope" →
  "Envelope algorithm", "fingerprints" → "checksums", "pretreatment curves … new
  drive" → "preprocessing transforms … retraining", "burden of false releases" →
  "false-alarm burden", "accuracy of the alerts" → "precision of the alerts",
  "timeliness" → "latency", decimal commas); the 2026-11-08 appendix now says the
  evaluator "marks such entries as undefined ($-1$)"; sources split into scientific and
  implementation sources; closing provenance line added (the note had none). Front
  matter unchanged except `revision`; H1, the twelve `### CV-IOU-AP-…` headings and
  "## Sources and flashcards" kept.
- [Cards](../../../vault/130-evaluation-fiabilite/131-iou-ap-coco.md): expected answers
  of 001, 002, 004 and 005 as quoted above. Further explanations: language fixes in all
  seven; CV-IOU-AP-003 gains the score-order condition; CV-IOU-AP-004 "raises the
  current accuracy to half" → "lowers the current precision to one half";
  CV-IOU-AP-005 gains the `ignore`-overwrite condition; CV-IOU-AP-007 "accuracy of the
  alerts" → "precision of the alerts". Blocking errors rephrased as gerunds with
  "precision", "mean overlap" and "recall levels". Source lines now cite exact files,
  lines or sections and label project constructions. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for maxDets,
top-100, crowd, 11-point, "exceed 0.5", AP/IoU confusions). The TIDE section number
cited by CV-DETECTEURS (§2.2 for the six error types) is correct.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-IOU-AP-01 | CV-IOU-AP | Explain why lowering the inference score threshold (or raising the per-image cap) cannot lower COCO AP, why deployed precision and recall do not change, and what to report for an acceptance decision | No card trains the tail behavior of interpolated AP or separates benchmark AP from the operating point with a mechanism | Reasoning; Mathematics, worked example D; Evaluation | 1 card, 3 criteria (old points kept, envelope over a superset; operating point unchanged; report P/R at the deployed threshold) | [LVIS, App. B Table 3a](https://arxiv.org/abs/1908.03195); [cocoeval.py `accumulate` L384–L408](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L384-L408) |
| P-CV-IOU-AP-02 | CV-IOU-AP | Compare COCO-style exhaustive evaluation with LVIS federated evaluation for a dataset whose labels are verified per category, and state which detections each protocol counts as FP | The exhaustive-annotation assumption is untested; the comparison family is absent from this subject | Comparison; Assumptions and Alternatives | 1 card, 3 criteria (positive and negative sets; detections outside them not evaluated; non-exhaustive flag suppresses FPs but keeps recall) | [LVIS §2.2–§2.3](https://arxiv.org/abs/1908.03195) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- COCO detection evaluation page, text of
  [`cocodataset.org/dataset/detection-eval.htm`](https://cocodataset.org/#detection-eval):
  §1, §2 (12 metrics, IoU thresholds, AP/mAP, size shares, mask area, AR, cap of 100
  per image across categories), §3 parameters and structures, §4 `analyze()` curves.
- COCO [results format](https://cocodataset.org/#format-results) §1 and
  [data format](https://cocodataset.org/#format-data) §1 (`iscrowd`, RLE, `categories`).
- Everingham et al. 2010, PASCAL VOC, IJCV 88,
  [DOI](https://doi.org/10.1007/s11263-009-0275-4); PDF fetched over HTTP from
  `host.robots.ox.ac.uk` (the HTTPS endpoint failed through the proxy) and extracted
  with `pdftotext`: §3.3 and Fig. 3, §4.2 eqs. 1–3 and "Bounding Box Evaluation".
- Gupta, Dollár and Girshick, LVIS, [arXiv 1908.03195v2](https://arxiv.org/abs/1908.03195)
  (PDF text): §2.2, §2.3, App. A and B, Table 3a.
- Rezatofighi et al., GIoU, [arXiv 1902.09630v2](https://arxiv.org/abs/1902.09630)
  (PDF text): §3, Alg. 1, Alg. 2, properties 1–4.
- Bolya et al., TIDE, [arXiv 2008.08115v2](https://arxiv.org/abs/2008.08115) (PDF
  text): §2.1, §2.2 (error types, oracles, eq. 2–3), §2.3 (eq. 4, Fig. 2).

Implementation sources:

- [cocoapi `cocoeval.py` at `8c9bcc3`](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py):
  L1–L534 read in full; commit date 2020-02-20 and head of master from the GitHub API.
- [cocoapi `coco.py` at `8c9bcc3`](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/coco.py#L305-L364): `loadRes` L305–L364.
- [cocoapi `maskApi.c` at `8c9bcc3`](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c): L72–L120.
- [torchvision `ops/boxes.py` at `v0.29.0`](https://github.com/pytorch/vision/blob/v0.29.0/torchvision/ops/boxes.py): L279–L436; release list from the GitHub API.
- [NumPy 1.24.0 release notes](https://github.com/numpy/numpy/blob/v1.24.0/doc/source/release/1.24.0-notes.rst): expired deprecations.

Failed accesses and limits:

- `https://host.robots.ox.ac.uk/...` returned a proxy error (HTTP 503 on CONNECT); the
  same PDF was read over HTTP and is cited through its DOI.
- Context7 was not available in this session (scope record); official versioned code
  and documentation replaced it.
- Not executed: pycocotools, torchvision and any detector. The torchvision NaN case is a
  code-reading deduction.
- Not re-verified: the COCO paper itself (Lin et al. 2014), which the note does not cite.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (an earlier run failed only on another subject's file in progress) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/131-iou-ap-coco.py` | 22 checks passed |
| `git diff --check -- vault/130-evaluation-fiabilite/ …/checks/131-iou-ap-coco.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/131-iou-ap-coco.md` | 7 cards, 316–415 words, no anomaly; absent families: comparison, design |
| Protected-field comparison with the pre-edit copy | 57 protected card lines identical; front matter identical except `revision: 8` → `9`; H1 and 12 per-card headings unchanged; `$$` and fences balanced |

No evaluator, detector or dataset was run; the proposed baseline and variation are
protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-IOU-AP revision 9, CV-IOU-AP-001 to 007, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-IOU-AP-01, P-CV-IOU-AP-02).
