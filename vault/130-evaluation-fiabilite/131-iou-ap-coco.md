# Flashcards — IoU and AP — the COCO detection protocol

reference note: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP]]. Source: Agent.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-IOU-AP-001

Objective: Compute an overlap under the right contract. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-001
Question: Which conventions must be fixed before calculating the IoU of two boxes, and why can mixing `xyxy` and `xywh` make the result misleading?
Reponse: **Expected answer**: Fix the format, coordinate frame, unit, validity and the continuous or inclusive pixel convention. In `xyxy`, the last two numbers are a corner; in `xywh`, they are width and height. Convert explicitly before intersection and union.

**Further explanation**: The IoU is $|A\cap B|/(|A|+|B|-|A\cap B|)$, without unit. For the pilot's continuous boxes, the area is $(x_2-x_1)(y_2-y_1)$ without `+1`. Also bring normalized boxes, crops and padding into the same coordinate frame. A degenerate box is a contract error to deal with, not a reason to silently add an epsilon.

**Contract example**: The numbers `(10,20,30,40)` describe either two corners, or one origin and two dimensions. The regions obtained then have different areas and positions. A correct intersection formula cannot compensate for this input ambiguity.

**Discriminating check**: Convert a known box to the evaluator format, convert it back to the original format and compare its corners. Repeat after resize and padding. If prediction and annotation undergo the same consistent geometric scaling, their IoU stays the same in the ideal case; if only one of the two processing chains converts its boxes, the score changes artificially. That the ratio has no unit does not mean that its inputs have no convention.

**Computing the sides**: In continuous coordinates, the intersection width is $\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B}))$, and the height follows the same formula in $y$. Their product gives the intersection area. An invertible affine transformation applied to both regions multiplies their areas by the same absolute determinant and preserves their geometric IoU. Warning: if a rotation is followed by replacing the regions with their axis-aligned bounding rectangles, the regions have changed and this invariance no longer holds automatically. The shape contract matters as much as the coordinates.

**Normalization must precede a shared geometric comparison**: Two boxes can each use valid xyxy coordinates while one is in normalized input space and the other in original pixels. Their numeric intersection then has no physical meaning. Convert both through the recorded resize/crop/padding transform before calculating overlap. A constructed identity test compares a box with its round-trip conversion and expects IoU one, subject to declared rounding and clipping. This detects coordinate-contract errors separately from localization quality.

**Blocking errors**: Calculate directly between different conventions or coordinate frames.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO results format, §1 Object Detection](https://cocodataset.org/#format-results); [cocoapi maskApi.c at 8c9bcc3, `bbIou` L109–L120](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c#L109-L120). Affine invariance, round-trip test and normalization case: project deductions.
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-IOU-AP-001 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-002

Objective: Distinguish between local measurement and aggregated protocol. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-002
Question: How do a pair's IoU, AP50, AP75 and the main COCO AP metric differ?
Reponse: **Expected answer**: The IoU measures the overlap of one pair of regions. AP50 and AP75 evaluate the precision/recall trade-off of a score ranking with the IoU threshold fixed at 0.50 or 0.75. The main COCO AP averages ten IoU thresholds from 0.50 to 0.95 in steps of 0.05, as well as valid categories and the protocol's recall levels.

**Further explanation**: An AP score is neither a mean IoU nor a precision at a single score threshold. Always specify bbox or segm, the size subset and the maximum number of predictions. AP75 requires stricter localization than AP50, without isolating all the causes of error.

**Reading a result**: AP50 can remain high when the boxes are close enough for a permissive criterion but lack the localization accuracy required at 0.75. This difference is informative about localization, without proving that the network is the cause: coordinate frames or annotations can also intervene.

**Proposed action**: View curves and errors by class and size, then choose the operating point on validation. A score threshold used in production selects a subset of the list; the AP summarizes a broader ranking protocol. The same AP can therefore accompany different business trade-offs. Keep the evaluator's conventions and the number of predictions retained before comparing versions.

**Ranking and confidence**: For a fixed set of predictions, without score-dependent filtering and with the same tie-breaking, a strictly increasing transformation applied to all scores preserves their order and therefore the ranking AP. It can, however, change the number of outputs above a fixed numeric production threshold. This shows why AP and score calibration are distinct. Conversely, a transformation that differs between images can change the global ranking of a category and its AP. Keep the scope of post-processing and any prediction caps in this analysis: upstream rules may invalidate the fixed-set assumption.

**AP aggregation omits undefined categories according to protocol**: A category with no valid ground-truth instances does not have the same recall denominator as a present category with zero successful detections. The pinned evaluator marks such entries as undefined ($-1$) and excludes them from its summaries. Replacing those entries by zero changes the aggregate. Record the image/category subset and valid-category handling when comparing tools, rather than treating a change in mean AP as necessarily a change in detector predictions.

**Blocking errors**: Interpreting AP50 as 50% precision or as a mean overlap.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO detection evaluation, §2 Metrics](https://cocodataset.org/#detection-eval); [cocoapi cocoeval.py at 8c9bcc3, `accumulate` L315–L420 and `summarize` L422–L493](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L315-L493). Ranking invariance and undefined-category case: project deductions.
Tags: cv::pilote cv::d13 famille::comprehension cv_id::CV-IOU-AP-002 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-003

Objective: Explain the penalty for a duplicate. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-003
Question: Two well-localized predictions cover the same ordinary ground-truth instance. Why can detection evaluation count one as a TP and the other as an FP?
Reponse: **Expected answer**: the matching follows the protocol and the order of the scores; an ordinary GT can only justify a single TP. The second prediction is a duplicate even if its overlap is high.

**Further explanation**: NMS targets this redundancy but can remove real neighbors. Crowd regions and ignored GT have specific rules: do not generalize the ordinary rule to all COCO annotations. In the pinned evaluator, detections claim objects in decreasing score order, so the higher-scored box becomes the TP even if the other overlaps more. The labelling of duplicates shapes the precision/recall curve and therefore the AP.

**Why the duplicate costs**: After the first TP, the second box increases the number of positive predictions without adding a found object. Precision can therefore decrease while recall does not progress. Its influence on the AP depends in particular on its rank with respect to the following detections.

**Discriminating check**: Keep the boxes and swap only the scores of the duplicate and of another detection. Observe the precision/recall curve under the same protocol. Do not conclude that a late false positive is costless in the product: it can still be emitted at the operating threshold. Evaluation and post-processing therefore have complementary roles, with an explicit exception for annotations to which crowd or ignore rules apply.

**Effect of a late duplicate**: For a single GT and a list TP then FP, recall reaches 1 at the first detection and the interpolated precision can remain perfect at all recall levels in this simple case. The duplicate is still a false positive if the operating threshold retains it. For TP, FP, TP on two GT, the duplicate appears before the second object is recovered and can degrade part of the envelope. The position of the FP therefore explains its effect on the AP; it does not change its concrete cost in a counting or rejection system.

**Blocking errors**: Counting each prediction that sufficiently covers the same GT as a new TP.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoapi cocoeval.py at 8c9bcc3, `evaluateImg` matching L272–L296](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L272-L296); [Everingham et al. 2010, §4.2, multiple detections counted as false](https://doi.org/10.1007/s11263-009-0275-4). Rank effects of the duplicate: project deductions.
Tags: cv::pilote cv::d13 famille::algorithme cv_id::CV-IOU-AP-003 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-004

Objective: rebuild a simple interpolated AP. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-004
Question: For two valid GT instances, one category, a fixed IoU threshold and no crowd/ignore annotations, ranked predictions are TP, duplicate FP, TP. How is AP interpolated over 101 recall levels calculated?
Reponse: **Expected answer**: Recalls $0.5;\,0.5;\,1$, precisions $1;\,0.5;\,2/3$. The right-to-left maximum envelope is 1 up to and including recall 0.5, then $2/3$. So $AP=(51+50\times2/3)/101\approx0.834983$.

**Further explanation**: The 101 levels are $0;\,0.01;\ldots;1$, so 51 levels are at most 0.5. Unreachable recall levels receive zero; detecting only one GT out of two would give $51/101$, despite a precision of 1 for that single detection. Example executed in `examples/pilot_math.py`; this simplified calculation does not implement all of COCO.

**Ranking reasoning**: The second prediction does not find any new GT and lowers the current precision to one half. The third reaches the maximum recall with a precision of two-thirds; the envelope carries this better level back to the reachable intermediate recalls.

**Interpreted variation**: Placing the duplicate after the two TPs can keep a perfect envelope, hence an AP of 1, in this small case, while the system still produces a duplicate. The score therefore summarizes a ranking under a specific convention and not all business consequences of the list. Also review the outputs at the operating threshold, and do not generalize this toy calculation to crowd regions or other details of the full evaluator.

**Envelope algorithm**: After accumulating TP and FP counts, go through the precision from right to left and replace each value with the maximum of itself and the next one. For each requested recall level, take the envelope value at the first rank whose recall reaches that level, or zero if it is never reached. This procedure explains the 51 levels up to and including 0.50 in the constructed case. It differs from an arbitrary trapezoidal integration of three points. Categories without valid GT and ignored annotations follow other rules, so a ranking example is not a complete COCO re-implementation.

**The recall-grid endpoint changes the arithmetic**: For the front's precision envelope, recall levels 0.00 through 0.50 inclusive contribute 51 samples at precision one; 0.51 through 1.00 contribute 50 at two-thirds. Their mean is about 0.834983. Using only 50 lower samples or integrating a continuous curve yields another number. Keep discrete recall levels and envelope conventions explicit when reproducing an evaluator rather than describing every area-like summary as the same AP.

**Blocking errors**: Averaging only the three raw precisions, or replacing the 101 recall levels with a single operating point.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoapi cocoeval.py at 8c9bcc3, `accumulate` L384–L408 (precision, recall, envelope, 101-level sampling)](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L384-L408) and `Params` L502–L511. Arithmetic recomputed by `examples/pilot_math.py`; variation: project deduction.
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-IOU-AP-004 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-005

Objective: Compare evaluators with caution. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-005
Question: Two tools report different COCO AP values for the same outputs. What must be aligned before concluding that the model is wrong?
Reponse: **Expected answer**: align split/GT, categories, bbox or mask, coordinate conversions, score/NMS/top-k filters, maxDets, ignore/crowd, sizes, evaluator version and interpolation. Compare the same result file and the actual parameters.

**Further explanation**: In the pycocotools code pinned with `useCats=1`, maxDets is applied per image and category; the descriptive page states a global top-100 per image across categories, and some wrappers apply it upstream. Describe the pipeline actually executed rather than a universal rule. Categories without valid GT are excluded, not counted as AP zero. At this commit, a custom `ignore` field is also overwritten by `iscrowd`, so only crowd regions are ignored.

**Proposed reproduction**: Archive a single prediction file and a single version of the GT, then vary only the evaluator or its suspect parameter. First compare the number of valid images, categories, GTs and detections actually retained before the final score.

**Why these controls precede the model**: A difference in maxDets or in ignored categories changes the objects admitted to the calculation without changing the detector's weights or boxes. Looking for an inference regression when the deviation comes from the protocol would waste time. Proper attribution requires the complete pipeline trace and the rules actually executed by the wrapper, not just the COCO name displayed.

**The first observable disagreement**: First compare the sets of images and categories, then the ordered lists retained per image, then the TP/FP/ignore statuses at each threshold. Only if these are identical, look at accumulation, interpolation and averages. This progression avoids debugging a final average when the tools have not evaluated the same objects. Keep checksums of the GT and result files, the parameters and the code version in the report. Two outputs displayed with the same AP label can come from different wrapper filters; only the trace of the actual inputs and matches can attribute the deviation accurately.

**Identical boxes are insufficient without identical filtering**: An evaluator can see different prediction lists because one path applies a higher score cutoff, a different category mapping or a different per-image detection cap. Compare the actual serialized results after all filters, then per-image TP/FP/ignore assignments before final aggregation. Record stable tie order when scores coincide. This proposed comparison finds the first disagreement instead of debugging the network from an aggregate metric discrepancy.

**Blocking errors**: Calling any in-house calculation “COCO” without its matching rules, or comparing different category sets without reporting it.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoapi cocoeval.py at 8c9bcc3, `_prepare` L107–L109, per-image cap L173–L176 and L362](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L107-L176); [COCO detection evaluation, §2 (global cap of 100 per image)](https://cocodataset.org/#detection-eval). Comparison procedure: project method.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-005 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-006

Objective: diagnose a deviation according to the location requirement. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-006
Question: AP50 remains high while AP75 falls sharply after new preprocessing. What should be checked before blaming the network?
Reponse: **Expected answer**: Check location accuracy and coordinate propagation through resize/crop/padding. Compare predictions and GT in the same coordinate frame, then analyze the results by size and class.

**Further explanation**: A small translation can leave the IoU above 0.50 and below 0.75, especially on small objects. Also check rounding, box format and post-processing. The discrepancy suggests a sensitivity to the overlap criterion, but does not alone demonstrate a single cause.

**Example signature**: A translation of two pixels can be small for a large box and represent a large fraction of a small defect. A constant padding or rounding error can therefore affect sizes and thresholds differently.

**Proposed investigation**: Pass some known boxes through the new preprocessing and its inverse, then compare the predictions before and after post-processing on the same images. Examine the error vectors and not just the AP averages. If the coordinate contract is correct, continue towards acquisition, effective resolution or regression quality. This approach turns a metric signature into testable hypotheses, without automatically attributing the drop to a specific bug.

**Sensitivity to translation**: For two squares of side $a$ offset horizontally by $\delta$ with $0\le\delta<a$, the IoU is $(a-\delta)/(a+\delta)$. To stay above a threshold $\tau$, you need $\delta<a(1-\tau)/(1+\tau)$ if the comparison is strict. At $\tau=0.75$, this is about $0.143a$; an error of 2 px therefore strongly penalizes a box of 10 px side. This constructed calculation does not identify the cause, but justifies an analysis by size and a check of preprocessing transforms and offsets before retraining.

**Small objects have a smaller pixel-shift allowance**: For equal 10 px squares offset horizontally by one pixel, IoU is $9/11\approx0.818$; a two-pixel offset gives $8/12\approx0.667$. Thus a small preprocessing offset can preserve AP50 matching while breaking AP75 on this constructed object. Compare inverse coordinate transforms and residuals by object size before retraining. The same two-pixel shift has a different relative effect on a much larger box.

**Blocking errors**: Taking AP75 for a geometry-independent classification metric, or concluding that a specific bug exists without inspection.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO detection evaluation, §2 Metrics (AP50, AP75, size ranges)](https://cocodataset.org/#detection-eval); [cocoapi cocoeval.py at 8c9bcc3, `evaluateImg` L235–L313](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L235-L313). Shift tolerances: constructed calculations.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-IOU-AP-006 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-007

Objective: Relate a benchmark average to a business decision. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-007
Question: A detector has good mean AP but misses the most costly defects on small parts. How should evaluation be extended to decide whether it is ready for use?
Reponse: **Expected answer**: Review recall and false positives at operating threshold, critical classes/sizes and actual acquisition conditions, with business costs. An average on classes and thresholds can hide a rare but serious error.

**Further explanation**: Set thresholds on validation, keep a representative test set, and analyze uncertainty and out-of-distribution cases as required. Also measure latency and downstream behavior. The AP remains useful for comparing ranking and localization under a fixed protocol, without certifying the reliability of the product.

**Decision contract**: Define the defects for which a missed detection is costly, the acceptable load of false rejections and the handling of uncertain cases. An average AP weighs categories according to its protocol; it does not know this hierarchy of consequences.

**Proposed validation**: Keep independent held-out batches that include small sizes and harsh conditions, then measure errors at a fixed threshold and the performance of critical subgroups. Also consider latency and the errors introduced by downstream steps. An AP gain may be useful without being sufficient to authorize commissioning. The conclusion must say which use was validated, on which data and with which limits, rather than converting an aggregate score into a guarantee of reliability.

**Prevalence and false-alarm burden**: In a binary model, if defects have a prevalence $\pi$, a recall $r$ and a false positive rate $f$ among conforming parts, the precision of the alerts is $r\pi/[r\pi+f(1-\pi)]$. For $\pi=0.001$, $r=0.99$ and $f=0.01$, it is about 9%. This constructed case explains why a small proportion of false positives can saturate the review when defects are rare. The benchmark AP does not provide this load directly: it requires the operating threshold, the actual frequencies and the costs of errors relevant to the product.

**Blocking errors**: Accepting the system on its average, or setting the threshold after observing the results of the final test.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO detection evaluation, §2 Metrics (averages over categories and sizes)](https://cocodataset.org/#detection-eval); [cocoapi cocoeval.py at 8c9bcc3, `summarize` L422–L493](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L422-L493). Prevalence calculation and acceptance protocol: project constructions.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-007 provenance::agent pole::A pole::C pole::E
END
