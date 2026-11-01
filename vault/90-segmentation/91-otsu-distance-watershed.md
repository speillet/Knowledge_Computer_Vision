# Flashcards — Otsu, distance transforms and watershed

reference note: [[90-segmentation/references/91-otsu-distance-watershed|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-WATERSHED-001

Objective: interpret the Otsu objective. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-001
Question: Why can an Otsu threshold that is optimal for the intensity histogram be poor for defect segmentation?
Reponse: **Expected answer**: The lens separates intensities according to variance, not business categories; lighting, imbalance and noise can dominate.

**Further explanation**: Test an annotated mask and defect size; compare local thresholding or other representation if hypothesis fails.

**Reading the objective**: Otsu chooses a cut according to the weights and averages of the intensity groups. A score that separates two levels of brightness can especially distinguish shadow and illuminated area, while the defect crosses both. The optimum belongs to the statistical criterion chosen, not to a knowledge of the parts.

**Constructed example**: a very small and low contrast defect weighs little in the overall histogram of a large image. A cut adapted to the majority bottom can therefore miss it. Compare the mask to defect annotations, stratifying sizes and lighting. Test an acquisition correction or local thresholding if it matches the observed assumption, without assuming that any automatic threshold is robust to any scene. For counting, it will still be necessary to separate the objects: a correct binary partition does not provide their instance identities.

**Computable criterion**: at threshold $t$, form the weights $\omega_0,\omega_1$ of the two groups and their averages $\mu_0,\mu_1$; Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$. Two very separate groups but one of which contains very few pixels may be less favored than a break explaining more about the overall variation. The criterion ignores positions: Spatially swapping pixels retains the histogram and threshold, but can destroy all objects. This built case shows why neither form, connectivity, nor business class are guaranteed. A default and size evaluation therefore necessarily completes the reading of the histogram.

**Blocking errors**: Deducing the semantic optimality of the optimum from a criterion of intensity.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::raisonnement cv_id::CV-WATERSHED-001 provenance::agent pole::A pole::E
END

## CV-WATERSHED-002

Objective: Rebuild the marker pipeline. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-002
Question: How can a distance transform and watershed separate touching objects?
Reponse: **Expected answer**: Build a mask, estimate centers/markers from distances, identify background/unknown and then propagate labels.

**Further explanation**: The same mask can produce different separations depending on the markers; validate each step.

**Successive roles**: the distance to the bottom reflects the local thickness of the foreground. Maxima can indicate interiors of regions, but only become object markers with a selection rule. The watershed then uses these germs and topography to distribute the still unknown areas.

**Constructed example**: Two disks in contact can form a single binary component, while keeping two interiors separate enough to provide two markers. If the maxima are merged or if the noise creates a lot of them, the partition can be sub-segmented or fragmented. View mask, distances, markers, and labels in this order to locate the responsible step. The distance metric and resolution also change the scale of values. Success on simple forms does not prove that each irregular or partially occulted object will naturally produce a single useful maximum.

**Choice of topography**: For a binary mask and a positive distance inside, the thick centers are maxima of $D$. A conceptual watershed on $-D$ transforms them into a minima; another variant can use a gradient image with fixed germs. These constructs are not automatically identical to the OpenCV API taking a color image. The distance to a discrete background also depends on the chosen metric. On anisotropic pixels, a distance in indices is not directly a physical distance: integrate the spacings if the shape or threshold should be interpreted in millimeters rather than pixels.

**Blocking errors**: Present the transform distance as a standalone instance segmentation.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-WATERSHED-002 provenance::agent pole::A pole::E
END

## CV-WATERSHED-003

Objective: distinguish background and unknown. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-003
Question: In the documented OpenCV watershed marker convention, why should known background and unknown regions not both be encoded as zero?
Reponse: **Expected answer**: Zero represents an area to be assigned; the already determined background must have a positive label like the other known markers.

**Further explanation**: The produced borders are worth −1; keep type, shape and modification on site according to the API.

**Why distinction matters**: A marker represents a region whose identity is already fixed for propagation; the unknown designates a region that the algorithm must assign. Code a background known as unknown therefore removes information from the initialization instead of giving it a background label.

**check**: create a small scene with an object and a certain background area, display the markers before the call and then the labels after. Verify that the positive identifiers correspond to the intended regions and reserve the special border value in its final sense. Keep a copy if you need to compare the entry, since the table in question is changed. These details are specific to the documented OpenCV contract; they do not define all watershed implementations. An exit of the right type does not yet prove that the markers describe the right physical objects.

**Example of a label table**: assign 1 to the certain background, 2 and 3 to the two object interiors, then 0 to the areas to be decided. After propagation, the positive labels designate the basins and $-1$ the borders according to the contract cited. The number 1 is therefore not universally the "object" class: it is here an identifier chosen for the background. Keep a dictionary between labels and physical meaning before producing a binary mask. If we replace all positive labels with a single one, we destroy precisely the distinction of instances that the initialization should bring, even if the global region remains unchanged.

**Blocking errors**: Assimilate 0 value to a permanently classified background.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-WATERSHED-003 provenance::agent pole::A pole::E
END

## CV-WATERSHED-004

Objective: Locate a sub-segmentation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-004
Question: Two objects remain in one basin despite a mask that covers them well. Which check distinguishes the cause?
Reponse: **Expected answer**: Visualize markers: if there is only one common germ, review the separation of maxima and form hypotheses.

**Further explanation**: Compare to manual markers on a copy to isolate the role of germs; randomly increasing thresholds does not identify the cause.

**Ablation on germs**: Keep image, mask, and settings, and then replace only automatic markers with two consistent manual germs on a copy. If the separation improves, this supports a marker construction problem. If it remains bad, also examine topography, mask and geometry of objects.

**Reading the result**: A good binary cover only indicates that the foreground is present. The number of regions and their borders depend on other decisions. An irregular object can have several maxima of distance without representing several instances; two very joined objects can on the contrary offer only a concentration. Choose a maxima rule according to justified sizes and shapes, and then measure merge and separation errors on other images. The diagnosis should distinguish lack of information, bad initialization and bad rule, instead of multiplying the thresholds without check.

**Overall threshold and different sizes**: Select all pixels where $D>\alpha\max D$ can remove germs from small objects, because the global maximum belongs to the thickest. Two properly masked objects can receive a germ and none, respectively. Comparing an overall threshold to a maxima detection adapted to the expected sizes is a discriminating variation, without assuming that a local rule solves all cases. Smoothing and removing close maxima also alters the number of germs. Viewing their number per annotated instance before the watershed makes it possible to distinguish a loss of small object and a merger of neighboring markers.

**Blocking errors**: Validate instances on binary mask quality only.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-WATERSHED-004 provenance::agent pole::A pole::E
END

## CV-WATERSHED-005

Objective: Choose a classic instance metric. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-005
Question: Why can high binary IoU hide failure of a watershed counting pipeline?
Reponse: **Expected answer**: Merging multiple objects can retain almost the entire top-tier region but lose the number and identity of instances.

**Further explanation**: Measure fusions/separations and matching protocol of objects, in addition to the global mask.

**Analytical example**: Two adjacent objects whose union is exactly predicted can give a perfect foreground mask. If the output has only one label for this union, the binary overlap is worth one while the counting of two objects fails. The metric does not contradict the failure: it measures another output.

**Proposed evaluation**: Set an association between predicted and real instances, then count found objects, merges, fragments, and fake objects. Keep the global mask as a complementary measure, announcing thresholds and processing of contacts. Check multiple densities and sizes, as separation errors can increase in areas where the binary region remains good. The contract of the product, for example counting parts, must therefore guide the annotations and measurements before choosing the segmentation pipeline.

**Merger and fragmentation**: An actual instance predicted in three fragments and three actual instances predicted as a single region may have opposite counting errors but a very close foreground. Using a table of overlaps between real and predicted labels reveals one-to-many and many-to-one relationships. A one-on-one matching with a fixed threshold measures objects found according to an announced rule; it does not replace the analysis of mergers. Also report the image counting error with its sign, because a signed average can undo important overcounts and undercounts. The measure must keep these failure modes separate.

**Blocking errors**: Confound semantic overlap and correct counting.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV Otsu, theory](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, markers and API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-WATERSHED-005 provenance::agent pole::A pole::E
END
