---
id: CV-WATERSHED
type: pipeline
domaine: d09
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-MORPHO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# Otsu, distance transforms and watershed

## Problem, data and assumptions

Separate objects on contact from a classic pattern of intensity and markers. Inputs: image, mask and polarity; successive outputs: binary partition, distances then instance labels. These are different steps, not three names of the same algorithm.

## Prerequisites and competencies

**Required prerequisites**: [CV-MORPHO](../../30-traitement-image/references/33-morphologie-composantes.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Otsu chooses a threshold according to the intensity distributions. The transform distance measures the distance of a pixel from the mask to the background. Its maxima can provide markers; watershed propagates basins according to a topography/implementation. Good markers matter as much as thresholding.

## Mathematics, conventions and units

Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$ for a threshold, class weights and averages, equivalent to minimizing the weighted intra-class variance. The distance $D(p)=\min_{q\in fond}\|p-q\|$ depends on the metric and resolution. It does not directly measure an identity or object class.

## Parameters and properties

Threshold, lighting, morphology, maxima and connectivity. In documented watershed OpenCV, image 8 bits 3 channels and int32 markers: unknown 0, positive labels, final borders −1; the marker array is modified. The known background is distinct from the unknown.

## Cost and implementation

Segmentation and propagation cost related to the image/markers. No OpenCV call executed; an Otsu calculation on toy histogram is proposed in the arithmetic examples, not an image validation.

## Evaluation and controlled variation

Baseline: Disjoint objects and then controlled contact; compare single components and watershed to markers. Predict that a merged marker can maintain subsegmentation. Measure instance errors, not just cover the global mask.

## Failure modes and diagnosis

Two grains remain fused: inspect markers and topography. Too many fragments: inspect noise and maxima parasites. A good bimodal histogram does not prove a good semantic separation.

## Alternatives and applications

Local setting for variable lighting, GrabCut for interaction, instance model if variations exceed simple assumptions.

## Guided reasoning and proposed checks

These constructed cases develop histogram, distance and role of markers. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-WATERSHED-001

**Question of work**: Why can an Otsu threshold that is optimal for the intensity histogram be poor for defect segmentation?

**Reference Response**: The lens separates intensities according to variance, not business categories; lighting, imbalance and noise can dominate.

**Reading the objective**: Otsu chooses a cut according to the weights and averages of the intensity groups. A score that separates two levels of brightness can especially distinguish shadow and illuminated area, while the defect crosses both. The optimum belongs to the statistical criterion chosen, not to a knowledge of the parts.

**Constructed example**: a very small and low contrast defect weighs little in the overall histogram of a large image. A cut adapted to the majority bottom can therefore miss it. Compare the mask to defect annotations, stratifying sizes and lighting. Test an acquisition correction or local thresholding if it matches the observed assumption, without assuming that any automatic threshold is robust to any scene. For counting, it will still be necessary to separate the objects: a correct binary partition does not provide their instance identities.

### Case linked to CV-WATERSHED-005

**Question of work**: Why can high binary IoU hide failure of a watershed counting pipeline?

**Reference Response**: Merging multiple objects can retain almost the entire top-tier region but lose the number and identity of instances.

**Analytical example**: Two adjacent objects whose union is exactly predicted can give a perfect foreground mask. If the output has only one label for this union, the binary overlap is worth one while the counting of two objects fails. The metric does not contradict the failure: it measures another output.

**Proposed evaluation**: Set an association between predicted and real instances, then count found objects, merges, fragments, and fake objects. Keep the global mask as a complementary measure, announcing thresholds and processing of contacts. Check multiple densities and sizes, as separation errors can increase in areas where the binary region remains good. The contract of the product, for example counting parts, must therefore guide the annotations and measurements before choosing the segmentation pipeline.

**Documentary reference for this pass**: [OpenCV 4.13, Watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html), markers, distance transform and borders. The other developments are in the [flashcards](../91-otsu-distance-watershed.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-WATERSHED-001

**Situation**: Why can an Otsu threshold that is optimal for the intensity histogram be poor for defect segmentation?

**Computable criterion**: at threshold $t$, form the weights $\omega_0,\omega_1$ of the two groups and their averages $\mu_0,\mu_1$; Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$. Two very separate groups but one of which contains very few pixels may be less favored than a break explaining more about the overall variation. The criterion ignores positions: Spatially swapping pixels retains the histogram and threshold, but can destroy all objects. This built case shows why neither form, connectivity, nor business class are guaranteed. A default and size evaluation therefore necessarily completes the reading of the histogram.

### CV-WATERSHED-002

**Situation**: How can a distance transform and watershed separate touching objects?

**Choice of topography**: For a binary mask and a positive distance inside, the thick centers are maxima of $D$. A conceptual watershed on $-D$ transforms them into a minima; another variant can use a gradient image with fixed germs. These constructs are not automatically identical to the OpenCV API taking a color image. The distance to a discrete background also depends on the chosen metric. On anisotropic pixels, a distance in indices is not directly a physical distance: integrate the spacings if the shape or threshold should be interpreted in millimeters rather than pixels.

### CV-WATERSHED-003

**Situation**: In the documented OpenCV watershed marker convention, why should known background and unknown regions not both be encoded as zero?

**Example of a label table**: assign 1 to the certain background, 2 and 3 to the two object interiors, then 0 to the areas to be decided. After propagation, the positive labels designate the basins and $-1$ the borders according to the contract cited. The number 1 is therefore not universally the "object" class: it is here an identifier chosen for the background. Keep a dictionary between labels and physical meaning before producing a binary mask. If we replace all positive labels with a single one, we destroy precisely the distinction of instances that the initialization should bring, even if the global region remains unchanged.

### CV-WATERSHED-004

**Situation**: Two objects remain in one basin despite a mask that covers them well. Which check distinguishes the cause?

**Overall threshold and different sizes**: Select all pixels where $D>\alpha\max D$ can remove germs from small objects, because the global maximum belongs to the thickest. Two properly masked objects can receive a germ and none, respectively. Comparing an overall threshold to a maxima detection adapted to the expected sizes is a discriminating variation, without assuming that a local rule solves all cases. Smoothing and removing close maxima also alters the number of germs. Viewing their number per annotated instance before the watershed makes it possible to distinguish a loss of small object and a merger of neighboring markers.

### CV-WATERSHED-005

**Situation**: Why can high binary IoU hide failure of a watershed counting pipeline?

**Merger and fragmentation**: An actual instance predicted in three fragments and three actual instances predicted as a single region may have opposite counting errors but a very close foreground. Using a table of overlaps between real and predicted labels reveals one-to-many and many-to-one relationships. A one-on-one matching with a fixed threshold measures objects found according to an announced rule; it does not replace the analysis of mergers. Also report the image counting error with its sign, because a signed average can undo important overcounts and undercounts. The measure must keep these failure modes separate.

**Passages consulted for these developments**: [OpenCV 4.13.0, watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html), Theory and example of transform distance; size and metric analyses of the project.

## Sources and flashcards

- [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html).
- [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
- [Related flashcards](../91-otsu-distance-watershed.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
