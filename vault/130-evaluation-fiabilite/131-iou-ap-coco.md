# Flashcards — IoU and AP — the COCO detection protocol

reference note: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP]]. Source: Agent.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-IOU-AP-001

Objective: calculate a overlap in the right contract. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-001
Question: Which conventions must be fixed before calculating the IoU of two boxes, and why can mixing `xyxy` and `xywh` make the result misleading?
Reponse: **Expected answer**: fix format, coordinate frame, unity, validity and continuous/inclusive agreement. In `xyxy`, the last two numbers are a corner; in `xywh`, they are width and height. Convert explicitly before intersection and union.

**Further explanation**: The IoU is $|A\cap B|/(|A|+|B|-|A\cap B|)$, without unit. For the driver's continuous boxes, area $(x_2-x_1)(y_2-y_1)$ without `+1`. Bring also standardized boxes, crop and padding in the same coordinate frame. A degenerate box is a contract error to deal with, not a reason to silently add an epsilon.

**Example of contract**: The numbers `(10,20,30,40)` describe either two corners, or one origin and two dimensions. The regions obtained then have different areas and positions. A correct intersection formula cannot compensate for this input ambiguity.

**check**: Convert a known box to the evaluator format, return to the original format and compare its corners. Repeat after resize and padding. If prediction and annotation undergo the same consistent geometric scaling, their IoU remains the same in the ideal case; if a single string is converted, the score changes artificially. The lack of unity of the ratio does not mean the absence of convention on its inputs.

**Calculation of sides**: in continuous coordinates, the intersection width is $\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B}))$, and the height follows the same formula in $y$. Their product gives the intersected area. An invertible affine transformation applied to both regions multiplies their areas by the same absolute determinant and retains their geometric IoU. Warning: if a rotation is followed by the replacement of the regions by their encompassing rectangles aligned on the axes, the regions have been changed and this invariance no longer applies automatically. The form contract is as important as the contact information.

**Normalization must precede a shared geometric comparison**: Two boxes can each use valid xyxy coordinates while one is in normalized input space and the other in original pixels. Their numeric intersection then has no physical meaning. Convert both through the recorded resize/crop/padding transform before calculating overlap. A constructed identity test compares a box with its round-trip conversion and expects IoU one, subject to declared rounding and clipping. This detects coordinate-contract errors separately from localization quality.

**Blocking errors**: Calculate directly between different conventions or coordinate frames.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO, format of results](https://cocodataset.org/#format-results); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-IOU-AP-001 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-002

Objective: Distinguish between local measurement and aggregated protocol. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-002
Question: How do a pair's IoU, AP50, AP75 and the main COCO AP metric differ?
Reponse: **Expected answer**: The IoU measures a region overlap. AP50 and AP75 evaluate the accuracy/recall ranking with a threshold set at 0,50 or 0,75. The main COCO AP averages ten thresholds from 0,50 to 0,95 per step of 0,05, as well as valid categories and protocol recall levels.

**Further explanation**: A AP score is not an average of the IoU nor an accuracy at a single score threshold. Always specify bbox/segm, subset of sizes and maximum number of predictions. AP75 requests a location stricter than AP50, without isolating all the causes of error.

**Reading a result**: AP50 can remain high when the boxes are close enough for a permissive criterion but lack the accuracy required at 0,75. This difference is informative for the location, without proving that the network is the cause: coordinate frames or annotations can also intervene.

**Proposed action**: View curves and errors by class and size, then choose the operating point on validation. A score threshold used in production selects a subset of the list; the AP summarizes a broader ranking protocol. The same AP can therefore accompany different business compromises. Keep the evaluator's conventions and the number of predictions retained before comparing versions.

**Ranking and confidence**: a set of fixed predictions, without filtering depending on the score and with the same tie-breaking, a strictly increasing common transformation of the scores retains their order and therefore the AP of ranking. However, it can change the number of outputs at the digital production threshold. This shows why AP and calibration of scores are distinct. Conversely, a differently applied transformation between images can change the overall classification of a category and its AP. Keep the scope of the postprocessing and any prediction limits in this analysis: the upstream rules may invalidate the set hypothesis.

**AP aggregation omits undefined categories according to protocol**: A category with no valid ground-truth instances does not have the same recall denominator as a present category with zero successful detections. The pinned evaluator uses undefined entries and excludes them in its summaries. Replacing those entries by zero changes the aggregate. Record the image/category subset and valid-category handling when comparing tools, rather than treating a change in mean AP as necessarily a change in detector predictions.

**Blocking errors**: interpret AP50 as 50% accuracy or as the average of recoveries.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [protocole officiel COCO](https://cocodataset.org/#detection-eval); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::comprehension cv_id::CV-IOU-AP-002 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-003

Objective: Explain the penalty for a duplicate. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-003
Question: Two well-localized predictions cover the same ordinary ground-truth instance. Why can detection evaluation count one as a TP and the other as an FP?
Reponse: **Expected answer**: the matching follows the protocol and the order of the scores; an ordinary GT can only justify a single TP. The second prediction is a duplicate even if its overlap is high.

**Further explanation**: A NMS is aimed at this redundancy but can remove real neighbors. The ignored crowd and GT have specific rules: do not generalize the ordinary rule to all COCO annotations. The classification of duplicates influences the precision/recall curve and therefore the AP.

**Why does the duplicate cost**: After the first TP, the second box increases the number of positive predictions without adding a found object. The accuracy may therefore decrease while the recall is not progressing. Its influence on the AP depends in particular on its rank with respect to the following detections.

**check**: Keep boxes and swap only duplicate and other detection scores. Observe the precision/recall curve under the same protocol. Do not conclude that a late false positive is costless in the product: it can still be issued at the operating threshold. Evaluation and postprocessing therefore have complementary roles, with an explicit exception for annotations to which crowd or ignore rules apply.

**Effect of a late duplicate**: for a single GT and a list TP then FP, the recall reaches 1 from the first detection and the interpolated accuracy can remain perfect on all levels of recall of this simple case. Duplicate is still a false positive if the operating threshold retains it. For TP, FP, TP on two GT, the duplicate appears before the recovery of the second object and can degrade part of the envelope. The position of the FP therefore explains its effect on the AP; it does not change its concrete cost in a counting or rejection system.

**Blocking errors**: count each prediction sufficiently covering the same GT as a new TP.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoeval.py, evaluateImg L235](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L235); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30.
Tags: cv::pilote cv::d13 famille::algorithme cv_id::CV-IOU-AP-003 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-004

Objective: rebuild a simple interpolated AP. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-004
Question: For two valid GT instances, one category, a fixed IoU threshold and no crowd/ignore annotations, ranked predictions are TP, duplicate FP, TP. How is AP interpolated over 101 recall levels calculated?
Reponse: **Expected answer**: recalls $0,5;0,5;1$, precisions $1;0,5;2/3$. The maximum envelope to the right is 1 up to and including the 0,5 recall, then $2/3$. So $AP=(51+50\times2/3)/101\approx0,834983$.

**Further explanation**: The 101 levels are $0;0,01;\ldots;1$, so 51 levels are at most 0,5. Unreachable reminders receive zero; only one GT detected out of two would give $51/101$, despite an accuracy of 1 for detection alone. Example executed; this simplified calculation does not implement all COCO.

**Reasoning for classification**: The second prediction does not find any new GT and raises the current accuracy to half. The third reaches the maximum recall with two-thirds accuracy; the envelope resumes this best level for accessible intermediate recalls.

**Variation interpreted**: placing the duplicate after the two TPs can keep a perfect envelope of AP in this small case, while the system always produces a duplicate. The score therefore summarizes a ranking under a specific convention and not all business consequences of the list. Also review the exits at the operating threshold, and then do not generalize this toy calculation to the crowd or other details of the full appraiser.

**Algorithm of the envelope**: After stacking TP and FP, go through the accuracy from right to left and replace each value with the maximum between it and the next. For each recall requested, then take the first level reached to its right according to the rules of the evaluator, or zero if it is not reached. This procedure explains the 51 levels included up to 0,50 in the case built. It differs from an arbitrary trapezoidal integration of three points. Categories without valid GT and ignored annotations follow other rules, so a ranking example is not a complete COCO re-implementation.

**The recall-grid endpoint changes the arithmetic**: For the front's precision envelope, recall levels 0.00 through 0.50 inclusive contribute 51 samples at precision one; 0.51 through 1.00 contribute 50 at two-thirds. Their mean is about 0.834983. Using only 50 lower samples or integrating a continuous curve yields another number. Keep discrete recall levels and envelope conventions explicit when reproducing an evaluator rather than describing every area-like summary as the same AP.

**Blocking errors**: average only the three raw precisions or replace the 101 reminders with a single operating point.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoeval.py, accumulate L353](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L353); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-IOU-AP-004 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-005

Objective: Compare evaluators with caution. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-005
Question: Two tools report different COCO AP values for the same outputs. What must be aligned before concluding that the model is wrong?
Reponse: **Expected answer**: align split/GT, categories, bbox or mask, coordinate conversions, score/NMS/top-k filters, maxDets, ignore/crowd, sizes, reviewer version and interpolation. Compare the same result file and the actual parameters.

**Further explanation**: in the pycocotools code pinned with `useCats=1`, maxDets is applied by image and category; the descriptive page evokes a global top-100 and some wrappers can do it upstream. Describe the string actually executed rather than a universal rule. Categories without valid GT are excluded, not counted as AP zero.

**Proposed reproduction**: archive a single prediction file and a single version of GT, and then vary only the evaluator or its suspicious parameter. First compare the number of valid images, categories, GTs and detections actually retained before the final score.

**Why these controls precede the model**: A difference of maxDets or ignored category changes the objects admitted in the calculation without changing the weights or the boxes of the detector. Looking for an inference regression when the deviation comes from the protocol would waste time. Proper attribution requires the complete string trace and the rules actually executed by the wrapper, not just the COCO name displayed.

**The First Observable Disagreement**: compare first the sets of images and categories, then the ordered lists retained by image, then the statuses TP/FP/ignore at each threshold. If these elements are identical, then look for accumulation, interpolation and averages. This progress avoids debugging a final average when the tools have not evaluated the same objects. Keep fingerprints of GT files and results, parameters, and code version in the report. Two outputs displayed with the same AP label can come from different wrapper filters; only the trace of the actual inputs and the matches can accurately assign the deviation.

**Identical boxes are insufficient without identical filtering**: An evaluator can see different prediction lists because one path applies a higher score cutoff, a different category mapping or a different per-image detection cap. Compare the actual serialized results after all filters, then per-image TP/FP/ignore assignments before final aggregation. Record stable tie order when scores coincide. This proposed comparison finds the first disagreement instead of debugging the network from an aggregate metric discrepancy.

**Blocking errors**: Call any house calculation “COCO” without matching rules, or compare sets of different categories without reporting it.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [cocoeval.py pinned](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-005 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-006

Objective: diagnose a deviation according to the location requirement. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-006
Question: AP50 remains high while AP75 falls sharply after new preprocessing. What should be checked before blaming the network?
Reponse: **Expected answer**: Check location accuracy and coordinate propagation through resize/crop/padding. Compare predictions and GT in the same coordinate frame, then analyze the results by size and class.

**Further explanation**: A small translation can leave the IoU above 0,50 and under 0,75, especially on small objects. Also check rounded, box format and postprocessing. The discrepancy suggests a sensitivity to the overlap criterion, but does not alone demonstrate a single cause.

**Example of signature**: A translation of two pixels can be small for a large box and represent a large fraction of a small defect. A constant padding or rounding error can therefore affect sizes and thresholds differently.

**Proposed investigation**: test some known boxes through the new preprocessing and its inverse, and then compare the predictions before and after postprocessing on the same images. Examine the error vectors and not just the averages of AP. If the coordinate contract is correct, continue towards acquisition, effective resolution or regression quality. This approach transforms a metric signature into testable hypotheses, without automatically assigning the drop to a specific bug.

**Sensitivity to translation**: for two side squares $a$ horizontally offset from $\delta$ with $0\le\delta<a$, the IoU is $(a-\delta)/(a+\delta)$. To stay above a threshold $\tau$, you need $\delta<a(1-\tau)/(1+\tau)$ if the comparison is strict. At $\tau=0,75$, this represents about $0,143a$; an error of 2 px therefore strongly penalizes a box of 10 px side. This constructed calculation does not point to the cause, but justifies the analysis by size and the check of the pretreatment curves and offsets before a new drive.

**Small objects have a smaller pixel-shift allowance**: For equal 10 px squares offset horizontally by one pixel, IoU is $9/11\approx0.818$; a two-pixel offset gives $8/12\approx0.667$. Thus a small preprocessing offset can preserve AP50 matching while breaking AP75 on this constructed object. Compare inverse coordinate transforms and residuals by object size before retraining. The same two-pixel shift has a different relative effect on a much larger box.

**Blocking errors**: Take AP75 for a geometry-independent classification metric, or conclude a specific bug without inspection.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO, metric definition](https://cocodataset.org/#detection-eval); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-IOU-AP-006 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-007

Objective: link average benchmark and business decision. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IOU-AP-007
Question: A detector has good mean AP but misses the most costly defects on small parts. How should evaluation be extended to decide whether it is ready for use?
Reponse: **Expected answer**: Review recall and false positives at operating threshold, critical classes/sizes and actual acquisition conditions, with business costs. An average on classes and thresholds can hide a rare but serious error.

**Further explanation**: set thresholds on validation, maintain a representative test, analyze uncertainty and out-of-distribution cases as required. Also measure latency and downstream behavior. The AP remains useful for comparing the classification and the location under fixed protocol, without certifying the reliability of the product.

**Decision contract**: Define the defects for which the lack of detection is costly, the acceptable load of false rejections and the behavior of uncertain cases. An average AP weighs categories according to its protocol; it does not automatically know this hierarchy of consequences.

**Proposed Validation**: maintain independent batches including small sizes and harsh conditions, then measure fixed threshold errors and performance of critical subgroups. Also consider the timeliness and errors introduced by the downstream steps. A gain of AP may be interesting without sufficient to allow commissioning. The conclusion must say what use has been validated, on what data and with what limits, rather than converting an aggregate score into a guarantee of reliability.

**Prevalence and burden of false releases**: In a binary model, if the defects have a prevalence of $\pi$, a recall of $r$ and a false positive rate of $f$ among the conformants, the accuracy of the alerts is $r\pi/[r\pi+f(1-\pi)]$. For $\pi=0,001$, $r=0,99$ and $f=0,01$, it is about 9%. This constructed case explains why a small proportion of false positives can saturate the review when defects are rare. The benchmark AP does not directly provide this load: it requires the operating threshold, the actual frequencies and the costs of the errors useful to the product.

**Blocking errors**: Accept the system on its average or set the threshold after observing the results of the final test.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP reference]]; [COCO, aggregations by category and size](https://cocodataset.org/#detection-eval); [COCO, pinned code, valuateImg and accumulate; invariances and geometric/probability examples constructed](https://raw.githubusercontent.com/cocodataset/cocoapi/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), see 2026-10-30.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-007 provenance::agent pole::A pole::C pole::E
END
