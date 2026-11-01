---
id: CV-IOU-AP
type: metrique-protocole
domaine: d13
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 6
tags: [cv/d13, evaluation, iou, ap]
---
# IoU and AP — the COCO detection protocol

## Problem and data

The IoU measures a overlap; the AP measures the precision/reminder compromise of a list of detections classified in a given protocol. Neither of these measures alone the temporal identity, latency or business gravity of an error. This reference note is a reference to **metric/protocol**, not a feature extraction algorithm. [COCO, evaluation][cocodoc]

Inputs: predictions with image, category, box/mask and score; annotations with categories, area, ignore/crowd according to protocol. The COCO bbox results use `xywh`. Keep even coordinate frame and same transformations as annotations. Category identifiers are not necessarily contiguous indices. [Format of results][format]

**Required prerequisites**: [Boxes and coordinate frames](../../01-Parcours/Pre-requis.md). **Connexions**: [NMS](../../80-detection-pose/references/81-nms.md), [SORT](../../110-tracking-association/references/111-sort.md), segmentation. **Competences**: calculate, interpret, compare only compatible protocols.

## IoU: definition and limits

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}.
$$

$A,B$ are two positive area regions; $|\cdot|$ measures an area, in square pixels if the coordinates are in pixels. The IoU is unitless and between 0 and 1. For continuous boxes `xyxy`, the intersection multiplies the width and height of overlap truncated to zero; do not add `+1` to a continuous convention. A degenerate box should be treated explicitly, not masked by an epsilon.

The same translation in pixels further penalizes a small box: the IoU is not an absolute metric error. For masks, the calculation is for segmented regions, not their encompassing rectangles. A mIoU of semantic segmentation and a AP of instances respond to different protocols.

## Precision assignment/recall

At a threshold of IoU and for a category, order predictions by score. The rules of the protocol determine the matching to the GT. An ordinary GT already associated does not give a second TP: a duplicate can therefore become FP. In COCO code, ignored GT/crowds require special processing. [Implementation, `evaluateImg`][code]

After accumulation, $P=TP/(TP+FP)$ and $R=TP/N_{GT}$: $N_{GT}$ counts the valid GT of the category and subset evaluated. The overall ranking of detections of this category between images matters; a transformation of the scores that changes this ranking can change the AP.

## AP COCO: average and interpolation

At each IoU threshold, form the $P_{interp}(r)=\max_{\tilde r\ge r}P(\tilde r)$ precision envelope, with zero for unreachable reminders. The code samples 101 reminders $r\in\{0,0{,}01,\ldots,1\}$. The main AP also averages ten IoU thresholds from 0,50 to 0,95 in steps of 0,05, and valid categories. AP50 fixed 0,50; AP75 fixed 0,75. This is neither a single-threshold accuracy nor an average of IoU. [COCO][cocodoc], [code `accumulate`][code]

A category with GT valid but without detection has AP null; without GT valid, it is indefinite and excluded from the average in this reference. Report categories, sizes, maximum number of detections and type bbox/segm.

## Protocol corners not to be erased

The Python reference pinned `8c9bcc3` with `useCats=1` applies `maxDets=100` **by image and category** before accumulation. The COCO descriptive page announces a global ceiling for all classes; a wrapper or server can also perform this global filtering. This divergence is explained: compare only executions of which version and pre-filtering are known. [Code, `evaluateImg` and `Params`][code]

For a crowd, multiple predictions can be absorbed and ignored; the overlap used can be $|D\cap G|/|D|$ for a $D$ detection and a $G$ crowd region, instead of the regular IoU. Non-associated predictions outside the range can also be ignored. Do not replace these rules with a simple one-to-one match to announce a “AP COCO”. [Implementation of recovery][mask]

## Executed example, baseline and variation

Analytical example without ignore/crowd, a category and a threshold IoU set: two valid GT; detections classified TP, FP duplicates, TP. Reminders are $0,5;0,5;1$ and $1;0,5;2/3$ details. The envelope gives

$$
AP_{101}=\frac{51\times1+50\times(2/3)}{101}\approx0,834983.
$$

There are 51 recall thresholds from 0 to 0,50 included. The FP intermediate lowers the accuracy of higher reminders. If we detect only one of the two GT, $AP_{101}=51/101\approx0,504950$: it is not a AP of 1 despite an accuracy of 1 for the single prediction. Calculations executed in `examples/pilot_math.py`; this program is not a complete reimplementation of pycocotools.

**Controlled variation**: Place the duplicate after the two TPs instead of them. In this case built, the envelope can keep a AP of 1; this shows that the rank of an error counts. This is not proof that late FPs are cost-free at a given operating threshold.

## Cost, evaluation and diagnosis

Sorting and comparisons to GTs depend on the number of predictions and thresholds/categories. Set score filtering, NMS, top-k, versions and split. No training or pycocotools call on a real game is run here.

| Symptom | Explication possible | Validation |
| --- | --- | --- |
| AP50 good, AP75 low | Imprecise location, coordinates transformed incorrectly | Box errors and results by size, coordinate frame after resize/padding |
| Difference between two evaluators | maxDets, ignore/crowd, interpolation, categories | Same results file, version and explicit parameters |
| AP good, failed critical flaws | Medium masking rare classes/sizes, inadequate business threshold | Sub-groups and operating point curve |

## Guided reasoning and proposed checks

These built cases develop matching, COCO classification and conventions. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-IOU-AP-001

**Question of work**: Which conventions must be fixed before calculating the IoU of two boxes, and why can mixing `xyxy` and `xywh` make the result misleading?

**Reference Response**: fix format, coordinate frame, unity, validity and continuous/inclusive agreement. In `xyxy`, the last two numbers are a corner; in `xywh`, they are width and height. Convert explicitly before intersection and union.

**Example of contract**: The numbers `(10,20,30,40)` describe either two corners, or one origin and two dimensions. The regions obtained then have different areas and positions. A correct intersection formula cannot compensate for this input ambiguity.

**check**: Convert a known box to the evaluator format, return to the original format and compare its corners. Repeat after resize and padding. If prediction and annotation undergo the same consistent geometric scaling, their IoU remains the same in the ideal case; if a single string is converted, the score changes artificially. The lack of unity of the ratio does not mean the absence of convention on its inputs.

### Case linked to CV-IOU-AP-007

**Question of work**: A detector has good mean AP but misses the most costly defects on small parts. How should evaluation be extended to decide whether it is ready for use?

**Reference Response**: Review recall and false positives at operating threshold, critical classes/sizes and actual acquisition conditions, with business costs. An average on classes and thresholds can hide a rare but serious error.

**Decision contract**: Define the defects for which the lack of detection is costly, the acceptable load of false rejections and the behavior of uncertain cases. An average AP weighs categories according to its protocol; it does not automatically know this hierarchy of consequences.

**Proposed Validation**: maintain independent batches including small sizes and harsh conditions, then measure fixed threshold errors and performance of critical subgroups. Also consider the timeliness and errors introduced by the downstream steps. A gain of AP may be interesting without sufficient to allow commissioning. The conclusion must say what use has been validated, on what data and with what limits, rather than converting an aggregate score into a guarantee of reliability.

**Documentary reference for this pass**: [COCO API, cocoeval.py to commit 8c9bcc3](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), evaluateImg, accumulate and summarize. The other developments are in the [flashcards](../131-iou-ap-coco.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-IOU-AP-001

**Situation**: Which conventions must be fixed before calculating the IoU of two boxes, and why can mixing `xyxy` and `xywh` make the result misleading?

**Calculation of sides**: in continuous coordinates, the intersection width is $\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B}))$, and the height follows the same formula in $y$. Their product gives the intersected area. An invertible affine transformation applied to both regions multiplies their areas by the same absolute determinant and retains their geometric IoU. Warning: if a rotation is followed by the replacement of the regions by their encompassing rectangles aligned on the axes, the regions have been changed and this invariance no longer applies automatically. The form contract is as important as the contact information.

### CV-IOU-AP-002

**Situation**: How do a pair's IoU, AP50, AP75 and the main COCO AP metric differ?

**Ranking and confidence**: a set of fixed predictions, without filtering depending on the score and with the same tie-breaking, a strictly increasing common transformation of the scores retains their order and therefore the AP of ranking. However, it can change the number of outputs at the digital production threshold. This shows why AP and calibration of scores are distinct. Conversely, a differently applied transformation between images can change the overall classification of a category and its AP. Keep the scope of the postprocessing and any prediction limits in this analysis: the upstream rules may invalidate the set hypothesis.

### CV-IOU-AP-003

**Situation**: Two well-localized predictions cover the same ordinary ground-truth instance. Why can detection evaluation count one as a TP and the other as an FP?

**Effect of a late duplicate**: for a single GT and a list TP then FP, the recall reaches 1 from the first detection and the interpolated accuracy can remain perfect on all levels of recall of this simple case. Duplicate is still a false positive if the operating threshold retains it. For TP, FP, TP on two GT, the duplicate appears before the recovery of the second object and can degrade part of the envelope. The position of the FP therefore explains its effect on the AP; it does not change its concrete cost in a counting or rejection system.

### CV-IOU-AP-004

**Situation**: For two valid GT instances, one category, a fixed IoU threshold and no crowd/ignore annotations, ranked predictions are TP, duplicate FP, TP. How is AP interpolated over 101 recall levels calculated?

**Algorithm of the envelope**: After stacking TP and FP, go through the accuracy from right to left and replace each value with the maximum between it and the next. For each reminder requested, then take the first level reached to its right according to the rules of the evaluator, or zero if it is not reached. This procedure explains the 51 levels included up to 0,50 in the case built. It differs from an arbitrary trapezoidal integration of three points. Categories without valid GT and ignored annotations follow other rules, so a ranking example is not a complete COCO re-implementation.

### CV-IOU-AP-005

**Situation**: Two tools report different COCO AP values for the same outputs. What must be aligned before concluding that the model is wrong?

**The First Observable Disagreement**: compare first the sets of images and categories, then the ordered lists retained by image, then the statuses TP/FP/ignore at each threshold. If these elements are identical, then look for accumulation, interpolation and averages. This progress avoids debugging a final average when the tools have not evaluated the same objects. Keep fingerprints of GT files and results, parameters, and code version in the report. Two outputs displayed with the same AP label can come from different wrapper filters; only the trace of the actual inputs and the matches can accurately assign the deviation.

### CV-IOU-AP-006

**Situation**: AP50 remains high while AP75 falls sharply after new preprocessing. What should be checked before blaming the network?

**Sensitivity to translation**: for two side squares $a$ horizontally offset from $\delta$ with $0\le\delta<a$, the IoU is $(a-\delta)/(a+\delta)$. To stay above a threshold $\tau$, you need $\delta<a(1-\tau)/(1+\tau)$ if the comparison is strict. At $\tau=0,75$, this represents about $0,143a$; an error of 2 px therefore strongly penalizes a box of 10 px side. This constructed calculation does not point to the cause, but justifies the analysis by size and the check of the pretreatment curves and offsets before a new drive.

### CV-IOU-AP-007

**Situation**: A detector has good mean AP but misses the most costly defects on small parts. How should evaluation be extended to decide whether it is ready for use?

**Prevalence and burden of false releases**: In a binary model, if the defects have a prevalence of $\pi$, a recall of $r$ and a false positive rate of $f$ among the conformants, the accuracy of the alerts is $r\pi/[r\pi+f(1-\pi)]$. For $\pi=0,001$, $r=0,99$ and $f=0,01$, it is about 9%. This constructed case explains why a small proportion of false positives can saturate the review when defects are rare. The benchmark AP does not directly provide this load: it requires the operating threshold, the actual frequencies and the costs of the errors useful to the product.

**Passages consulted for these developments**: [COCO, pinned code](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), evaluateImg and accumulate; invariances and geometric/probabilistic examples built.

## Sources and flashcards

- [Description officielle COCO][cocodoc] and [format][format].
- [Code officiel `cocoeval.py`, commit 8c9bcc3][code]: `evaluateImg` L235, `accumulate` L353, `Params` L502; version checked the 2026-10-18.
- [Collection code, same commit][mask]: `bbIou` and crowd.
- [flashcards IoU/AP](../131-iou-ap-coco.md).

[cocodoc]: https://cocodataset.org/#detection-eval
[format]: https://cocodataset.org/#format-results
[code]: https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py
[mask]: https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c
