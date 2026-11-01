---
id: CV-NMS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: ["CV-IOU-AP"]
revision: 7
tags: [cv/d08, detection, nms]
---
# NMS — suppressing redundant detections

## Problem and data

Several hypotheses of a detector can designate the same object. The greyy hard NMS (*Non-Maximum Suppression*) successively retains the best score box and removes candidates who overwhelm it. It assumes that score and recovery make it possible to distinguish duplicates from true neighbors; this hypothesis may fail in a crowd. [Soft-NMS, §4][paper]

Entries: `xyxy` valid boxes in a common coordinate frame, scalar scores, classes if we separate the categories. Outputs: preserved clues, not merged boxes. Scores are used for ranking; their probabilistic calibration is not a necessary condition for calculation. Standardized coordinates or pixels may be appropriate if all boxes share the same convention.

**Required prerequisites**: [IoU](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md). **Connexions**: [SORT](../../110-tracking-association/references/111-sort.md), AP, dense detection and detector sets. **Competences**: unroll the algorithm and set the thresholds without confusing them.

## Procedure and parameters

Pseudocode **Pedagogy**, materialized by the Python example of the repository:

```text
sort indices by decreasing score as long as candidates remain: keep the first remove others if their IoU with him exceeds the threshold
```

The driver variant deletes for $\operatorname{IoU}>\tau_{nms}$. Equality is preserved. In the case of equal scores, it uses the input index as deterministic ranking. Another implementation may not guarantee the same CPU/GPU choice; record the backend. [Torchvision NMS][api]

The sources do not treat equality the same way: the article writes the deletion for $\operatorname{IoU}(M,b_i)\ge N_t$ [§4][paper], while Torchvision and the original code delete for a strictly superior IoU. [Torchvision NMS][api]; [code original][softcode] The case of a IoU exactly equal to the threshold therefore depends on the implementation: specify it in a boundary test.

- Score Threshold: Filters confidence before/after the chosen post-processing.
- Threshold NMS: decides the redundancy between two predictions.
- Evaluation threshold IoU: compares a prediction to the ground truth.

These three thresholds have neither the same pair of objects nor the same role. A class-separated NMS avoids interclass deletion, but can leave multiple incompatible labels on the same object. The global NMS has the opposite compromise. Choose according to the semantics of the annotations. [Batched NMS][batched]

## Executed example and variation

Continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$, $C=(20,0,30,10)$, respective scores $0,9;0,8;0,7$. Intersection $A\cap B=80$ px², union 120 px², IoU $=2/3$. At $\tau_{nms}=0,5$, keep $A,C$; at 0,7, keep $A,B,C$. This result is executed in `examples/pilot_math.py`, without reproducing a detector.

**Interpretation of controlled variation**: increasing the threshold here keeps more boxes; this can save a real neighbor or keep a duplicate. The boxes alone do not say which one: it takes the annotations of the task. A AP measured on a real game remains necessary to settle the compromise.

## Multiple detections, classes and sizes of boxes

An image can contain multiple instances of the same class. Their detections must be kept separate; NMS does not select "only one object per class". Conversely, several candidates may designate a single instance. The deletion uses recovery as an indication of redundancy, without knowing the real identity of the objects. A crowd is precisely putting this hypothesis in default. [Soft-NMS, §§1 and 3 – 4][paper]

### Same geometry, different semantic decisions

The following scenarios are built for reasoning; the correct business output depends on the annotations and is not deduced from the IoU alone.

| Situation | Possible effect of NMS | check required |
| --- | --- | --- |
| Several candidates of the same class around a single object | Reduction of duplicates if the recovery exceeds the threshold | Check the associated GT and the location of the holding box |
| Two distinct people whose boxes overlap strongly | Possible deletion of a real neighbor, even with NMS per class | Coverage of each of the two GT before/after NMS |
| Two objects of different classes, for example person and bicycle | A global NMS can have one removed by the other if the IoU exceeds the threshold | Contract of the objects to be detected; NMS per class if both are to be kept |
| An instance receives two exclusive classes, for example two room types. | NMS per class can keep both assumptions | Resolve class decision according to contract; maximum score is not proof of accuracy |
| A small box is entirely in a large | Inclusion is not enough to cause deletion | Calculate the IoU, then distinguish object/part, two instances, or wrong location |

For only two candidates, from IoU $0{,}8$, scores $0{,}9$ and $0{,}8$ and different classes, hard NMS overall to $0{,}5$ retains only the first. One NMS per class retains both. If they have the same class, class separation does not protect them from each other. Nor does it merge their labels and impose their exclusivity. [Batched NMS, description and parameters][batched]

### Inclusion and boxes of very different sizes

For valid continuous rectangles, if $B\subset A$, the intersection is $B$ and the union is $A$: $\operatorname{IoU}(A,B)=|B|/|A|$. Thus, $A=(0,0,100,100)$ and $B=(40,40,60,60)$ give $400/10000=0{,}04$. With scores $0{,}9$ and $0{,}8$, same class and hard NMS to $0{,}5$, both remain. A large box does not automatically delete all the small boxes it contains. Project analytical calculation, derived from the definition of IoU [GIoU, §3, equation 1][giou].

The ratio "intersection / area of the small box" here is 1: it is not the IoU. Replacing it with the IoU would change the deletion rule and could eliminate legitimate detections of nested objects or parts. Conversely, a large mislocalized box and a small box on the same object can both remain; their survival does not prove two instances. See also [size cases and aspect ratios](82-detection-fasterrcnn-yolo-detr.md#box-sizes-aspect-ratios-and-accuracy).

## Soft-NMS: alternative and limits

Soft-NMS lowers scores instead of immediately eliminating any strong overlay. For example, the Gaussian variant uses

$$
s_i\leftarrow s_i\exp\left(-\frac{\operatorname{IoU}(M,b_i)^2}{\sigma}\right).
$$

$M$ is the selected box, $b_i$ a candidate, $s_i$ its score and $\sigma>0$ a parameter without a unit. The Gaussian penalty applies to all remaining candidates, with no $N_t$ threshold. [Article, §4][paper] Look again for the maximum among the penalized scores, as the original code does. After each iteration, the detections passed below a score threshold are discarded: "Soft-NMS never deletes" is false. [Article, §5][paper]; [code original][softcode]

The original code uses inclusive coordinates with `+1`, while the driver uses continuous coordinates. A numerical comparison requires the same convention. The score of a box does not become a probability calibrated by this postprocessing alone. [Official implementation][softcode]

## Cost, evaluation and diagnosis

Sorting costs $O(n\log n)$ and naive removal up to $O(n^2)$ comparisons. An upstream top-k reduces the cost but can lose objects; log this filtering in the AP protocol. No Torchvision extract is executed in this batch.

Set thresholds on validation, freeze before testing, analyze by class, size and density. Also observe the effect on the downstream tracker: deleted boxes can cause missed tracks.

| Symptom | Causes to be distinguished | Validation |
| --- | --- | --- |
| A pedestrian disappears in a crowd | NMS too aggressive, detector never proposing the box | Compare outputs before and after NMS with GT |
| Several boxes around a room | Overly permissive threshold, different classes, false convention | Journal scores/classes/IoU and contact information contract |
| Different results with equal scores | Non-deterministic order or backend | Explicit separation, targeted testing without concluding a gap in the network |

A detector trained to produce a non-redundant set, such as DETR, can do without NMS: do not apply it as a universal obligation. [DETR, summary][detr]

## Guided reasoning and proposed checks

These constructed cases develop suppression, equality threshold and recall of nearby objects. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-NMS-001

**Question of work**: Three continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$ and $C=(20,0,30,10)$ have scores $0,9;0,8;0,7$. Which boxes are retained by hard NMS that suppresses candidates with IoU greater than 0.5?

**Reference Response**: select $A$, delete $B$ because their intersection is 80, union 120 and IoU $2/3>0,5$; then keep $C$, disjoint. The output is $A,C$.

**Reasoning on instances**: Overlay is used as an index of redundancy between predictions, without knowing the real identity of the objects. If A and B represent two close people, deleting B can remove a real instance; if they represent the same room, the deletion can instead be useful.

**check**: keep the outputs before and after the operation and check which annotations remain covered. The threshold therefore settles a compromise depending on the scene. A remote box remains candidate even with a lower score, as long as it passes the other filters in the pipeline. This reading avoids turning the gluton selection into a "one box per image" or "one box per class" rule.

### Case linked to CV-NMS-006

**Question of work**: Two continuous boxes of the same class, $A=(0,0,100,100)$ and $B=(40,40,60,60)$, have scores $0{,}9$ and $0{,}8$. Does B being contained in A imply suppression by hard NMS at IoU threshold $>0{,}5$? Justify the answer.

**Reference Response**: No. The intersection has the area of B, 400, and the union that of A, 10000: IoU $=0{,}04$. A is selected, then B remains since the threshold is not exceeded.

**Geometric reading**: A small box entirely contained in a large one has an intersection equal to its own area, but a union equal to the large area. The cover for the small box and the IoU therefore answer two different questions. Replacing one with the other would change the deletion rule.

**Consequences of diagnosis**: Two surviving boxes do not prove two instances: they can be two very different locations of the same room. Conversely, both object and part of object can be legitimate if the taxonomy so provides. Check annotations, scores, and the exit contract before changing the collection action. This analytical case shows a limit to the slogan “big boxes eliminate small ones”.

**Documentary reference for this pass**: [Soft-NMS](https://arxiv.org/html/1704.04503v2), method and decrease of scores. The other developments are in the [flashcards](../81-nms.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-NMS-001

**Situation**: Three continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$ and $C=(20,0,30,10)$ have scores $0,9;0,8;0,7$. Which boxes are retained by hard NMS that suppresses candidates with IoU greater than 0.5?

**Selection is not transitive**: build three boxes of the same size with $A=(0,0,10,10)$, $B=(3,0,13,10)$ and $C=(6,0,16,10)$. The IoU $A/B$ and $B/C$ are worth $7/13>0,5$, but $A/C=4/16=0,25$. With decreasing scores A, B, C, NMS keeps A, deletes B then keeps C: B deleted does not in turn delete its neighbors. This distinguishes the gluttony algorithm from a grouping into related components of the overlap graph. The result depends on the ranking and does not automatically look for the set of maximum score sum boxes.

### CV-NMS-002

**Situation**: In object detection, how do the score threshold, NMS IoU threshold and evaluation IoU threshold differ?

**Separate setting and measurement**: take a candidate with a score of 0,4, from IoU 0,8 with another prediction, but from IoU 0,6 with a score of GT. A score threshold at 0,5 discards it before any measurement; at an allowable score, a NMS at 0,7 can remove it; if it survives, it satisfies a localization requirement at 0,5 but not at 0,75, under the other rules of matching. These three comparisons relate to different objects. To assign a recall drop, keep counters after each step with constant evaluation protocol, rather than simultaneously changing the three thresholds.

### CV-NMS-003

**Situation**: Two candidates from different classes have scores $0{,}9$ and $0{,}8$ and IoU $0{,}8$. With NMS threshold $0{,}5$, what tradeoff distinguishes global suppression from per-class suppression?

**Conflict of taxonomy built**: If the same instance receives the scores 0,8 for "vehicle" and 0,75 for "car", the two labels can be consistent in a hierarchical taxonomy but redundant in a single category contract. Set this policy before choosing deletion. With the same geometry, a person holding a bike and a room receiving two exclusive classes ask for different decisions. Separately testing interclass conflicts and neighbors of the same class helps to measure what class separation actually protects. The highest score does not indicate, by construction, whether two hypotheses share a physical identity.

### CV-NMS-004

**Situation**: How does Gaussian Soft-NMS differ from hard NMS, and why must candidates be reordered after a score penalty?

**Calculated change in rank**: after selection of A, a box B with a score of 0,8 and IoU 0,8 becomes $0,8e^{-0,8^2/0,5}\simeq0,222$ for $\sigma=0,5$. A disjointed box C of score 0,5 remains at 0,5 and thus passes before B. With a final threshold of 0,25, B can be removed. This constructed case makes explicit the roles of the decay parameter and the score threshold. Reusing a selected threshold for initial scores without further validation can change the recall, since the values have been transformed by postprocessing.

### CV-NMS-005

**Situation**: An object disappears from final outputs in a dense region. How can NMS be identified as the cause and a verifiable intervention chosen?

**Deletion log**: For each candidate removed, keep their ID, the one in the box that deleted it, the classes, scores and the IoU calculated in the common coordinate frame. Then replaying the selection on the same predictions makes it possible to isolate the postprocessing without retraining the network. Measure the coverage of the GT with a defined matching, because two candidates on a GT are not two objects recalled. If a top-k precedes NMS, consider also the candidates lost there: increasing the threshold NMS does not recover a box eliminated by this upstream filter.

### CV-NMS-006

**Situation**: Two continuous boxes of the same class, $A=(0,0,100,100)$ and $B=(40,40,60,60)$, have scores $0{,}9$ and $0{,}8$. Does B being contained in A imply suppression by hard NMS at IoU threshold $>0{,}5$? Justify the answer.

**Condition of inclusion**: for $B\subset A$ and a strict deletion at threshold $\tau$, B can only be deleted by A if $|B|>\tau|A|$, provided that A is actually selected before it. At $\tau=0,5$, a contained box covering 4% of the large area therefore remains very far from the condition. Reversing the scores does not change the IoU, but changes the first box retained; with more candidates, it can change the whole gluttonous suite. This reasoning distinguishes the symmetry of the overlap measure and the algorithm's dependence on ranking.

**Passages consulted for these developments**: [Bodla et al., Soft-NMS](https://arxiv.org/html/1704.04503v2), §4, selection and decay; geometric counterexamples constructed.

## Sources and flashcards

- [Bodla et al., Soft-NMS 2017][paper]: §1 limits of the NMS, §4 hard/soft and penalty functions, §5 score threshold after each iteration.
- [Torchvision `nms`][api]: API agreement accessed on 2026-10-18; no software benchmark claimed.
- [Code original Soft-NMS, commit b8e69bd][softcode]: coordinates, maximum search and final threshold.
- [Carion et al., DETR 2020][detr]: assembly detection without NMS.
- [Torchvision 0.29 `batched_nms`][batched]: separation by category and threshold, additional consultation on 2026-10-21; Context7 unavailable, official documentation consulted directly. No software calls executed.
- [GIoU, §3, equation 1][giou]: Definition used for inclusion calculation.
- [flashcards NMS](../81-nms.md).

[paper]: https://arxiv.org/abs/1704.04503
[api]: https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html
[batched]: https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html
[softcode]: https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx
[detr]: https://arxiv.org/abs/2005.12872

[giou]: https://arxiv.org/html/1902.09630v2
