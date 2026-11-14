# Flashcards — Otsu, distance transforms and watershed

reference note: [[90-segmentation/references/91-otsu-distance-watershed|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-WATERSHED-001

Objective: interpret the Otsu objective. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-001
Question: Why can an Otsu threshold that is optimal for the intensity histogram be poor for defect segmentation?
Reponse: **Expected answer**: The objective separates intensity levels by variance, not by application categories such as defect versus sound surface; lighting, class imbalance and noise can dominate it.

**Further explanation**: Test against annotated masks and defect sizes; compare local thresholding or another representation if the assumption fails.

**Reading the objective**: Otsu chooses a cut from the weights and means of the two intensity groups. A cut that separates two brightness levels may mainly separate shadow from lit area, while the defect spans both. The optimum belongs to the chosen statistical criterion, not to any knowledge of the parts.

**Constructed example**: A very small, low-contrast defect weighs little in the global histogram of a large image. A cut suited to the majority background can therefore miss it. Compare the mask with defect annotations, stratified by size and lighting. Test an acquisition correction or local thresholding if it matches the observed failure, without assuming that any automatic threshold is robust to every scene. For counting, the objects must still be separated: a correct binary partition does not provide their instance identities.

**Computable criterion**: At threshold $t$, form the weights $\omega_0,\omega_1$ of the two groups and their means $\mu_0,\mu_1$; Otsu maximizes $\omega_0\omega_1(\mu_0-\mu_1)^2$. Two well-separated groups, one of which contains very few pixels, may score lower than a cut that explains more of the overall variance. The criterion ignores positions: spatially permuting pixels keeps the histogram and the threshold but can destroy every object. This constructed case shows why neither shape, connectivity nor application class is guaranteed. An evaluation by defect and size must therefore complement the reading of the histogram.

**A histogram has no knowledge of where defects lie**: Two images with identical intensity histograms but different spatial arrangements receive the same Otsu objective. One can contain a coherent scratch and the other isolated speckles. This constructed permutation argument shows why histogram optimality cannot establish the desired spatial segmentation. Evaluate defect extent and connectivity after thresholding, and compare controlled illumination changes rather than selecting a threshold solely because its histogram classes look well separated.

**Blocking errors**: Inferring semantic optimality from the optimum of an intensity criterion.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [Otsu 1979, §I, §II eqs. 12–19 and §III-A](https://doi.org/10.1109/TSMC.1979.4310076) ; [OpenCV 4.13.0, thresh.cpp L1183–L1275, Otsu criterion](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/thresh.cpp#L1183-L1275). Permutation and small-defect cases: project constructions (worked example A of the reference).
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

**Successive roles**: The distance to the background reflects the local thickness of the foreground. Maxima can indicate region interiors, but become object markers only through a selection rule. The watershed then uses these seeds and the relief to assign the areas that are still unknown.

**Constructed example**: Two disks in contact can form a single binary component, while keeping two interiors separate enough to provide two markers. If the maxima merge, or if noise creates many of them, the partition can be under-segmented or fragmented. View the mask, distances, markers and labels in this order to locate the responsible step. The distance metric and the resolution also change the scale of the values. Success on simple shapes does not prove that every irregular or partially occluded object will produce a single useful maximum.

**Choice of topography**: For a binary mask with a positive distance inside, the centres of thick parts are maxima of $D$. A conceptual watershed on $-D$ turns them into minima; another variant floods a gradient image from fixed seeds. These constructions are not what the OpenCV API computes: `cv::watershed` (OpenCV 4.13) takes an 8-bit colour image and orders the flooding by the largest absolute channel difference between 4-neighbors, so in the tutorial pipeline the distance map only supplies the markers. The distance to a discrete background also depends on the chosen metric. On anisotropic pixels, a distance in index units is not a physical distance: include the pixel spacings if the shape or a threshold must be interpreted in millimetres rather than pixels.

**Markers encode the intended number of basins**: One marker per touching object supplies a separation hypothesis; two markers inside one physical object can instead split it. Distance maxima are only proxies for object centers and can multiply on elongated or irregular shapes. Inspect marker stability under small mask perturbations and object-size variation. A proposed protocol compares marker errors separately from boundary propagation, because a good foreground mask can still support the wrong instance partition.

**Blocking errors**: Presenting the distance transform as a standalone instance segmentation.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [Beucher and Meyer 1993, §IV.B.1 and §VI.B, markers from distance maxima](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf) ; [OpenCV 4.13.0, watershed tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown) ; [OpenCV 4.13.0, segmentation.cpp L151–L159, flooding priority](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/segmentation.cpp#L151-L159). Added reasoning: project deduction.
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-WATERSHED-002 provenance::agent pole::A pole::E
END

## CV-WATERSHED-003

Objective: distinguish background and unknown. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-003
Question: In the documented OpenCV watershed marker convention, why should known background and unknown regions not both be encoded as zero?
Reponse: **Expected answer**: Zero represents an area to be assigned; the already determined background must have a positive label like the other known markers.

**Further explanation**: Boundaries are set to −1 in the output; respect the type, size and in-place modification required by the API.

**Why distinction matters**: A marker represents a region whose identity is already fixed for propagation; the unknown designates a region that the algorithm must assign. Encoding a known background as unknown therefore removes information from the initialization instead of giving that region a background label.

**Discriminating check**: Create a small scene with one object and a sure-background area, display the markers before the call and the labels after it. Verify that the positive identifiers correspond to the intended regions and that the special boundary value keeps its final meaning. Keep a copy if you need to compare with the input, since the marker array is modified in place. These details belong to the documented OpenCV contract; they do not define every watershed implementation. An output of the right type does not yet prove that the markers describe the right physical objects.

**Example of a label table**: Assign 1 to the sure background, 2 and 3 to the two object interiors, then 0 to the areas to be decided. After propagation, the positive labels designate the basins and $-1$ the boundaries, according to the cited contract. The number 1 is therefore not universally the "object" class: here it is an identifier chosen for the background. Keep a dictionary between labels and physical meaning before producing a binary mask. Replacing all positive labels with a single one destroys precisely the instance distinction that the initialization was meant to provide, even if the overall region is unchanged.

**Labels must retain signed integer semantics**: The value $-1$ marks watershed boundaries in the documented output. Casting this map to an unsigned type before interpretation can turn that sentinel into a large positive number and make it look like an object label. Keep the signed label map separate from a display image and derive masks by explicit label rules. The background marker is a positive basin identifier; its number has no intrinsic semantic meaning outside the chosen contract. OpenCV 4.13 also writes $-1$ on the one-pixel image frame and resets other negative input values to 0, so $-1$ does not only mark dams between basins.

**Blocking errors**: Treating the value 0 as a definitively classified background.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [OpenCV 4.13.0, imgproc.hpp L3474–L3498, watershed contract](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L3474-L3498) ; [OpenCV 4.13.0, segmentation.cpp L161–L193, types, image frame and negative inputs](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/segmentation.cpp#L161-L193) ; [OpenCV 4.13.0, watershed tutorial source, marker labelling](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown). Added reasoning: project deduction.
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-WATERSHED-003 provenance::agent pole::A pole::E
END

## CV-WATERSHED-004

Objective: Locate an under-segmentation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-004
Question: Two objects remain in one basin despite a mask that covers them well. Which check distinguishes the cause?
Reponse: **Expected answer**: Visualize the markers: if both objects share a single seed, revisit how the maxima are separated and the shape assumptions.

**Further explanation**: Compare with manual markers on a copy to isolate the role of the seeds; raising thresholds at random does not identify the cause.

**Ablation on seeds**: Keep the image, mask and settings, then replace only the automatic markers with two consistent manual seeds on a copy. If the separation improves, this points to a marker-construction problem. If it remains wrong, also examine the relief, the mask and the object geometry.

**Reading the result**: Good binary coverage only shows that the foreground is present. The number of regions and their boundaries depend on other decisions. An irregular object can have several distance maxima without being several instances; conversely, two strongly fused objects can yield a single maximum. Choose a maxima rule from justified sizes and shapes, then measure merge and split errors on other images. The diagnosis should distinguish missing information, bad initialization and a bad rule, instead of multiplying thresholds without a check.

**Global threshold and different sizes**: Selecting all pixels where $D>\alpha\max D$ can remove the seeds of small objects, because the global maximum belongs to the thickest object. Two well-masked objects can receive one seed and none, respectively. Comparing a global threshold with maxima detection adapted to the expected sizes is a discriminating variation, without assuming that a local rule solves every case. Smoothing and suppressing close maxima also change the number of seeds. Counting seeds per annotated instance before the watershed distinguishes a lost small object from a merge of neighboring markers.

**More markers can trade merges for splits**: Lowering a peak-selection threshold may recover a missing center in a small object while introducing several centers in a large one. A proposed sweep records both merged ground-truth instances and fragmented single instances, stratified by size and shape. Do not choose the setting from the count alone: one merge and one split can cancel numerically while both object identities remain wrong. Retain the overlap relationships needed to diagnose them.

**Blocking errors**: Validating instances on binary mask quality alone.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [Beucher and Meyer 1993, §IV.A, §IV.B.1 and §VI.B](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf) ; [OpenCV 4.13.0, watershed tutorial source, 0.7 max D rule](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown). Global-threshold and size cases: project constructions (worked example B of the reference).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-WATERSHED-004 provenance::agent pole::A pole::E
END

## CV-WATERSHED-005

Objective: Choose a classic instance metric. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-WATERSHED-005
Question: Why can high binary IoU hide failure of a watershed counting pipeline?
Reponse: **Expected answer**: Merging multiple objects can retain almost the entire foreground region but lose the number and identity of instances.

**Further explanation**: Measure merges and splits with an explicit object-matching protocol, in addition to the global mask.

**Analytical example**: Two adjacent objects whose union is exactly predicted can give a perfect foreground mask. If the output has only one label for this union, the binary overlap equals one while the count of two objects fails. The metric does not contradict the failure: it measures another output.

**Proposed evaluation**: Define an association between predicted and ground-truth instances, then count found objects, merges, fragments and false objects. Keep the global mask as a complementary measure, stating thresholds and how contacts are handled. Check several densities and sizes, because separation errors can increase where the binary region remains good. The product contract, for example counting parts, must therefore guide annotations and measurements before the segmentation pipeline is chosen.

**Merges and fragmentation**: One ground-truth instance predicted as three fragments and three ground-truth instances predicted as one region have opposite counting errors but very similar foregrounds. A table of overlaps between ground-truth and predicted labels reveals one-to-many and many-to-one relations. One-to-one matching with a fixed threshold measures the objects found under a stated rule; it does not replace the analysis of merges. Report the per-image counting error with its sign and its absolute value, because a signed average can cancel large overcounts against large undercounts. The measure must keep these failure modes separate.

**Blocking errors**: Confusing foreground overlap with correct counting.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Full reference]] ; [Kirillov et al. 2019, §4.1 Theorem 1 and §4.2](https://arxiv.org/abs/1801.00868) ; [OpenCV 4.13.0, watershed tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown). Merge and fragmentation cases: project constructions (worked example C of the reference).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-WATERSHED-005 provenance::agent pole::A pole::E
END
