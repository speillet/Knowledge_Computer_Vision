# Flashcards — Morphology and connected components

reference note: [[30-traitement-image/references/33-morphologie-composantes|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-MORPHO-001

Objective: distinguish between opening and closing. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MORPHO-001
Question: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?
Reponse: **Expected answer**: The opening erodes then expands and can remove small foreground structures; the closure expands then erodes and can fill holes or gaps. Choose the structurer according to the sizes and shapes to keep.

**Further explanation**: Removing a small object can clean up noise or clear a defect; validate on critical sizes and shapes.

**Geometric explanation**: Erosion requires the structurer to hold in the foreground; it therefore removes positions close to certain borders. The dilation then extends the retained positions. In an opening, a structure too narrow to survive erosion does not reappear simply because dilation follows. In a closure, sufficiently small intervals can be filled.

**Choice of scale**: A pixel size represents a physical size only if resolution and geometry are known. A useful structurator on a camera can erase the defects sought after a resolution change. In a constructed example, comparing a fine defect and a dust of similar size shows that the morphology does not have any semantic information to distinguish them. Evaluate therefore suppressions and mergers on critical cases, with polarity of the mask, shape of the structurer and treatment of the edge explained.

**Properties to know**: on ideal binary sets with the same structuring element, the opening is anti-extensive: its result is included in the initial foreground. The closure is extensive: it can be added. They are idempotent: applying a second time the complete operation with the same structuring element should no longer change the theoretical set obtained. Increasing the number of erosions and dilations on the other hand changes the effective support, and is not "repeat an identical opening". Finite images, edge values, and anchors must be consistent to find these properties in an implementation. Opening can break a thin bridge, closing can create a bridge; these topological changes can be decisive for counting objects.

**Blocking errors**: Describe these operations as guaranteed semantic filters.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]] ; [OpenCV 4.13.0, Morphological Transformations, §§1 – 4](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
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

**Reasoning by Neighbourhood**: in 4 connectivity, one can advance towards neighbors sharing one side; no foreground path here connects the two pixels. In 8 connectivity, a diagonal step is also permissible, and the pixels belong to the same connected set. The difference comes from the definition of the neighborhood graph, not the class of pixels.

**Practical consequence**: The same mask can therefore produce different numbers of objects without a single pixel changing. To count pieces or cells, decide which convention corresponds to the contacts that one wishes to consider. Keep this convention when measuring and separately report the background when the API counts it as a label. Label numbers are identifiers internal to the image: their order does not indicate a class or the identity of the same object to the next frame. The latter problem would require a temporal association.

**Built labeling algorithm**: browse the mask; at each foreground pixel not yet visited, create a label and explore by queue or stack its eligible neighbors. All affected pixels receive the same label, then the path resumes on the remaining pixels. This definition directly links the number of components to the number of routes launched. A practical implementation can use multiple passes or union-find, without changing the connectivity defined. Beware of the return of a library that includes the background in its number of labels: two components of foreground then give three labels in total. The properties of holes and contact also require a coherent neighborhood convention between background and foreground.

**Connectivity changes the object definition**: On a checkerboard of isolated diagonal foreground pixels, 8-connectivity can join a long chain that 4-connectivity separates. Neither choice is universally correct: the relevant physical contact and expected pixel sampling determine the convention. Use complementary background connectivity when analyzing holes to avoid ambiguous digital topology. Count foreground components separately from the background label returned by a labeling routine.

**Blocking errors**: Announce a number without connectivity.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]]; [OpenCV 4.13.0, connectedComponents, connectivity settings and labels](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html); countdown deducted from connectivity. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-MORPHO-002 provenance::agent pole::A pole::E
END

## CV-MORPHO-003

Objective: Explaining a merger of parts. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MORPHO-003
Question: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?
Reponse: **Expected answer**: The structurer may have created a bridge; inspect the before/after mask and the distance between objects.

**Further explanation**: Reduce or adjust the operation under check, then consider a marker separation; do not just change the area filter.

**Mechanism of Error**: dilation can join two regions separated by an interval smaller than the structurant scale. The following erosion does not necessarily restore this interval; closure may retain a common area. The related labeling then correctly counts a single connected set, but this set no longer represents a single object of the world.

**check**: Display the pixels added between the before and after masks, and then vary the size and orientation of the still image structurer. If the number of objects changes when the bridge appears, the cause is localized. A filtering by area after fusion does not find the two pieces: it acts on the region already grouped. Depending on the scene, preserve the interval, use separation markers or instance segmentation. Any correction must also be evaluated on truly contiguous objects, to avoid solving one case by fragmenting the others.

**Why the area filter is too late**: The area of a merged component essentially adds those of the two parts and the pixels of the bridge. It can therefore perfectly pass a minimum threshold, even when the count is false. Separately measuring the distance between borders before closing, the width of the bridge created and the maximum distance inside each part helps to choose a remedy. A marker watershed can use two reliable centers to provide separation, but bad markers can oversegment a single piece. In the evaluation, explicitly distinguish merge error, division error and boundary error: an average pixel score can remain good despite an object lost on counting.

**Kernel scale should follow physical separation**: If the minimum legitimate gap is 0.2 mm and image resolution changes from 0.1 to 0.05 mm/px, the same physical gap changes from two to four pixels. Reusing an unchanged kernel therefore changes its physical action. A proposed sweep records both removal of isolated noise and merger of neighboring real parts as a function of kernel size and shape. Area filtering after merger cannot recover the lost instance boundary.

**Blocking errors**: Take a related component for a guaranteed object.
Source: [[30-traitement-image/references/33-morphologie-composantes|Full reference]]; [OpenCV 4.13.0, Morphological Transformations, §§1 – 4](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html); bridge diagnosis built by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-MORPHO-003 provenance::agent pole::A pole::E
END
