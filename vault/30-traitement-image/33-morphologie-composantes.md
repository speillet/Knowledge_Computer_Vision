# Flashcards — Morphology and connected components

reference note: [[30-traitement-image/references/33-morphologie-composantes|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-MORPHO-001

Objective: distinguish between opening and closing. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MORPHO-001
Question: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?
Reponse: **Expected answer**: Opening erodes then dilates and can remove small foreground structures; closing dilates then erodes and can fill holes or gaps. Choose the structuring element according to the sizes and shapes to keep.

**Further explanation**: Removing a small object can clean up noise or erase a defect; validate on critical sizes and shapes.

**Geometric explanation**: Erosion requires the structuring element to fit inside the foreground; it therefore removes positions close to some borders. Dilation then extends the retained positions. In an opening, a structure too narrow to survive erosion does not reappear simply because dilation follows. In a closing, sufficiently small gaps can be filled.

**Choice of scale**: A size in pixels represents a physical size only if resolution and geometry are known. A structuring element suited to one camera can erase the target defects after a resolution change. In a constructed example, comparing a fine defect and a dust particle of similar size shows that morphology has no semantic information to distinguish them. Therefore evaluate removals and merges on critical cases, stating the mask polarity, the shape of the structuring element and the border handling.

**Properties to know**: on ideal binary sets with the same structuring element, opening is anti-extensive: its result is included in the initial foreground. Closing is extensive: it can only add pixels. Both are idempotent: applying the complete operation a second time with the same structuring element does not change the theoretical result. Increasing the number of erosions and dilations, on the other hand, changes the effective support and is not "repeating an identical opening". Finite images, border values and anchors must be consistent for these properties to hold in an implementation. Opening can break a thin bridge and closing can create one; these topological changes can be decisive when counting objects.

**Blocking errors**: Describing these operations as guaranteed semantic filters.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]] ; [Haralick, Sternberg and Zhuang 1987, §III, Definitions 35–36, Theorems 38 and 40, Propositions 41–42](https://doi.org/10.1109/TPAMI.1987.4767941) ; [OpenCV 4.13.0 imgproc.hpp, `MorphTypes` and `morphologyEx`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L216-L230).
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-MORPHO-001 provenance::agent pole::A pole::E
END

## CV-MORPHO-002

Objective: Choose connectivity. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-MORPHO-002
Question: A mask contains only two foreground pixels touching at one corner. How many components exist under 4-connectivity and 8-connectivity?
Reponse: **Expected answer**: Two in 4 connectivity; one in 8.

**Further explanation**: The convention must be retained in the evaluation and measurements of holes/objects.

**Reasoning by neighbourhood**: in 4 connectivity, one can advance towards neighbors sharing one side; no foreground path here connects the two pixels. In 8 connectivity, a diagonal step is also permissible, and the pixels belong to the same connected set. The difference comes from the definition of the neighborhood graph, not the class of pixels.

**Practical consequence**: The same mask can therefore produce different numbers of objects without a single pixel changing. To count pieces or cells, decide which convention corresponds to the contacts that one wishes to consider. Keep this convention when measuring and separately report the background when the API counts it as a label. Label numbers are identifiers internal to the image: their order does not indicate a class or the identity of the same object to the next frame. The latter problem would require a temporal association.

**Constructed labeling algorithm**: scan the mask; at each foreground pixel not yet visited, create a label and explore its eligible neighbors with a queue or a stack. All reached pixels receive the same label, then the scan resumes on the remaining pixels. This definition directly links the number of components to the number of explorations started. A practical implementation can use two passes and union-find without changing the defined connectivity. Beware of a library return value that counts the background as a label: two foreground components then give three labels in total. Holes and contacts also require a coherent neighborhood convention between background and foreground.

**Connectivity changes the object definition**: On a checkerboard of isolated diagonal foreground pixels, 8-connectivity can join a long chain that 4-connectivity separates. Neither choice is universally correct: the relevant physical contact and expected pixel sampling determine the convention. Use complementary background connectivity when analyzing holes to avoid ambiguous digital topology. Count foreground components separately from the background label returned by a labeling routine.

**Blocking errors**: Stating a count without its connectivity.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]]; [OpenCV 4.13.0 imgproc.hpp, `connectedComponents`: N labels including background 0, connectivity 4 or 8](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L4009-L4040); [Wu, Otoo and Suzuki 2009, §1, two-pass labeling](https://doi.org/10.1007/s10044-008-0109-y); count deduced from the connectivity definition. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-MORPHO-002 provenance::agent pole::A pole::E
END

## CV-MORPHO-003

Objective: Explain merged parts. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MORPHO-003
Question: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?
Reponse: **Expected answer**: The structuring element may have created a bridge; inspect the before/after mask and the distance between objects.

**Further explanation**: Reduce or adjust the operation in a controlled test, then consider marker-based separation; do not just change the area filter.

**Mechanism of the error**: dilation can join two regions separated by a gap smaller than the scale of the structuring element. The following erosion does not necessarily restore this gap; the closing may keep a common area. Connected-component labeling then correctly counts a single connected set, but this set no longer represents a single object in the world.

**Discriminating check**: Display the pixels added between the before and after masks, then vary the size and orientation of the structuring element on the same fixed image. If the number of objects changes when the bridge appears, the cause is localized. Area filtering after the merge does not recover the two parts: it acts on the region already grouped. Depending on the scene, preserve the gap, use separation markers or instance segmentation. Any correction must also be evaluated on genuinely contiguous objects, to avoid solving one case by fragmenting others.

**Why the area filter is too late**: The area of a merged component is essentially the sum of the two parts plus the bridge pixels. It can therefore easily pass a minimum threshold, even when the count is wrong. Measuring separately the distance between borders before closing, the width of the bridge created and the maximum distance inside each part helps to choose a remedy. A marker-based watershed can use two reliable centers to restore the separation, but bad markers can oversegment a single part. In the evaluation, explicitly distinguish merge errors, split errors and boundary errors: an average pixel score can remain good despite an object lost in the count.

**Kernel scale should follow physical separation**: If the minimum legitimate gap is 0.2 mm and image resolution changes from 0.1 to 0.05 mm/px, the same physical gap changes from two to four pixels. Reusing an unchanged kernel therefore changes its physical action. A proposed sweep records both removal of isolated noise and merging of neighboring real parts as a function of kernel size and shape. Area filtering after merging cannot recover the lost instance boundary.

**Blocking errors**: Taking a connected component for a guaranteed object.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]]; [Haralick, Sternberg and Zhuang 1987, §III, closing "fuses narrow breaks" and is extensive (Proposition 42)](https://doi.org/10.1109/TPAMI.1987.4767941); bridge diagnosis constructed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-MORPHO-003 provenance::agent pole::A pole::E
END
