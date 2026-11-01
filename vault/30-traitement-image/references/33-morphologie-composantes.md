---
id: CV-MORPHO
type: methode
domaine: d03
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Morphology and connected components

## Problem, data and assumptions

Modify a binary geometry and group its regions according to connectivity. Inputs: mask with defined polarity, structuring, anchoring and edge; outputs: transformed mask or labels. A component label is neither a semantic class nor a temporal identity.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Erosion removes points without compatible neighborhood; expansion extends the support. Opening and closing make up these operations in different orders. The related components then group connected pixels according to 4 or 8 neighbors.

## Mathematics, conventions and units

For a symmetrical B-centered structuring, $A\ominus B=\{x:x+B\subseteq A\}$ and $A\oplus B=\{a+b:a\in A,b\in B\}$. An opening is $(A\ominus B)\oplus B$. B expresses a scale in pixels: a variation in resolution changes its physical meaning.

## Parameters and properties

Fix B size/shape, iterations, connectivity and hole processing. Two regions in contact can merge; a useful operation against noise can remove a real small defect.

## Cost and implementation

The cost depends on the image, the structuring and the algorithm. Labels are internal to an image and can be renumbered. Illustrative pseudocode: clean → label → measure → check missing objects; no image execution announced.

## Evaluation and controlled variation

Analytical variation: two pixels that only touch diagonally are two components in 4-connectivity and one in 8-connectivity. On real image, measure merge/separation errors before filtering small regions.

## Failure modes and diagnosis

Counting too low: look at the bridges added by expansion/closure and connectivity. Counting too high: inspect fragments, noise and structuring; do not consider size as semantic truth.

## Alternatives and applications

Watershed with markers to separate joined objects; instance segmentation if the appearance and contacts exceed a simple geometric pattern.

## Guided reasoning and proposed checks

These constructed cases develop geometric support, topology and connectivity convention. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-MORPHO-001

**Question of work**: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?

**Reference Response**: The opening erodes then expands and can remove small foreground structures; the closure expands then erodes and can fill holes or gaps. Choose the structurer according to the sizes and shapes to keep.

**Geometric explanation**: Erosion requires the structurer to hold in the foreground; it therefore removes positions close to certain borders. The dilation then extends the retained positions. In an opening, a structure too narrow to survive erosion does not reappear simply because dilation follows. In a closure, sufficiently small intervals can be filled.

**Choice of scale**: A pixel size represents a physical size only if resolution and geometry are known. A useful structurator on a camera can erase the defects sought after a resolution change. In a constructed example, comparing a fine defect and a dust of similar size shows that the morphology does not have any semantic information to distinguish them. Evaluate therefore suppressions and mergers on critical cases, with polarity of the mask, shape of the structurer and treatment of the edge explained.

### Case linked to CV-MORPHO-003

**Question of work**: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?

**Reference Response**: The structurer may have created a bridge; inspect the before/after mask and the distance between objects.

**Mechanism of Error**: dilation can join two regions separated by an interval smaller than the structurant scale. The following erosion does not necessarily restore this interval; closure may retain a common area. The related labeling then correctly counts a single connected set, but this set no longer represents a single object of the world.

**check**: Display the pixels added between the before and after masks, and then vary the size and orientation of the still image structurer. If the number of objects changes when the bridge appears, the cause is localized. A filtering by area after fusion does not find the two pieces: it acts on the region already grouped. Depending on the scene, preserve the interval, use separation markers or instance segmentation. Any correction must also be evaluated on truly contiguous objects, to avoid solving one case by fragmenting the others.

**Documentary reference for this pass**: [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html), erosion, dilation, opening, closing. The other developments are in the [flashcards](../33-morphologie-composantes.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-MORPHO-001

**Situation**: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?

**Properties to know**: on ideal binary sets with the same structuring, the opening is anti-extensive: its result is included in the initial first plane. The closure is extensive: it can be added. They are idempotent: applying a second time the complete operation with the same structuring should no longer change the theoretical set obtained. Increasing the number of erosions and dilations on the other hand changes the effective support, and is not "repeat an identical opening". Finite images, edge values, and anchors must be consistent to find these properties in an implementation. Opening can break a thin bridge, closing can create a bridge; these topological changes can be decisive for counting objects.

### CV-MORPHO-002

**Situation**: A mask contains only two foreground pixels touching at one corner. How many components exist under 4-connectivity and 8-connectivity?

**Built labeling algorithm**: browse the mask; at each foreground pixel not yet visited, create a label and explore by queue or stack its eligible neighbors. All affected pixels receive the same label, then the path resumes on the remaining pixels. This definition directly links the number of components to the number of routes launched. A practical implementation can use multiple passes or union-find, without changing the connectivity defined. Beware of the return of a library that includes the background in its number of labels: two components of foreground then give three labels in total. The properties of holes and contact also require a coherent neighborhood convention between background and foreground.

### CV-MORPHO-003

**Situation**: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?

**Why the air filter is too late**: The area of a merged component essentially adds those of the two rooms and the pixels of the bridge. It can therefore perfectly pass a minimum threshold, even when the count is false. Separately measuring the distance between borders before closing, the width of the bridge created and the maximum distance inside each room helps to choose a remedy. A marker watershed can use two reliable centers to provide separation, but bad markers can oversegment a single piece. In the evaluation, explicitly distinguish merge error, division error and boundary error: an average pixel score can remain good despite an object lost on counting.

**Passages consulted for these developments**: [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html), §§1 – 4, erosion, dilation, opening and closing; [OpenCV 4.13, connectedComponents](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html), connectivity and labels.

## Sources and flashcards

- [OpenCV 4.13.0, connectedComponents, connectivity settings and labels](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html).

For the ensemblist morphology with the announced conventions, the opening is anti-extensive and the closure extensive: they can remove small structures foreground or fill small intervals. On a finished image, the edge processing must remain explicit.

- [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
- [Related flashcards](../33-morphologie-composantes.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
