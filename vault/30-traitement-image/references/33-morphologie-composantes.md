---
id: CV-MORPHO
type: methode
domaine: d03
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 9
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Morphology and connected components

This method note covers binary mathematical morphology (erosion, dilation, opening,
closing and their combinations) and connected-component labeling, the two steps that
turn a thresholded mask into countable, measurable regions. It explains what each
operator does to shape and topology, how the structuring element encodes a physical
scale, how connectivity defines an object, and how OpenCV implements both.
Thresholding, distance transforms and watershed are developed in
[CV-WATERSHED](../../90-segmentation/references/91-otsu-distance-watershed.md).

## Problem and data contract

**Task.** Clean a binary mask (remove specks, fill pin-holes, close small gaps,
break thin bridges) and then group foreground pixels into regions that can be
counted and measured, without destroying the structures the task needs.

**Inputs.** A single-channel mask of $H\times W$ pixels with an explicit polarity
(which value is foreground) and range (0/1 or 0/255); a structuring element $B$
(shape, size in pixels, anchor); a border rule; a connectivity (4 or 8).

**Outputs.**

- *Morphology*: a mask of the same size and type.
- *Labeling*: an integer label image where 0 is the background and $1..N-1$ are
  components; OpenCV's `connectedComponents` "returns N, the total number of labels
  [0, N-1] where 0 represents the background label" [imgproc.hpp, L4009–L4040].
  `connectedComponentsWithStats` adds per-label bounding box (left, top, width,
  height), area in pixels and centroid [L399–L408, L4042–L4085].

**Conventions.** Pixel coordinates have their origin at the top-left, $x$ to the
right, $y$ down. Sizes and areas are in pixels and pixel²; physical values need the
footprint in mm/px. A label is an index within one image: it carries neither a class
nor an identity across frames.

**Role in a pipeline.** After thresholding or segmentation
([CV-WATERSHED](../../90-segmentation/references/91-otsu-distance-watershed.md),
[CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md))
and before counting, measuring, filtering by size or shape, or tracking blobs. Its
errors (merges, splits, lost small defects) propagate directly into counts and
measurements.

## Intuition

- **Erosion asks "does $B$ fit here?"** A pixel stays foreground only if the
  structuring element placed at it lies entirely in the foreground. Shapes shrink,
  thin parts vanish.
- **Dilation asks "does $B$ touch the foreground here?"** Shapes grow, small gaps
  close.
- **Opening = erosion then dilation**: the union of all placements of $B$ that fit
  inside the shape. Anything narrower than $B$ disappears for good; what survives
  gets its shape back. Opening with a disk "smooths the contour, breaks narrow
  isthmuses, and eliminates small islands and sharp peaks or capes" [Haralick et
  al., §III].
- **Closing = dilation then erosion**: the dual. It "fuses narrow breaks and long
  thin gulfs, eliminates small holes, and fills gaps on the contours" [§III].
- **Connected components** treat pixels as graph nodes joined to their 4 edge
  neighbours or 8 edge-and-corner neighbours; a component is a connected subgraph.

*Illustration (constructed).* Two machined parts lie 0.2 mm apart under a camera at
0.1 mm/px: a 2 px gap. A 3×3 closing used to fill pin-holes bridges the gap, and
labeling then correctly reports one connected region that is two parts. After a lens
change to 0.05 mm/px the same gap is 4 px and the same closing no longer merges them,
but now leaves pin-holes of 3–4 px unfilled. Worked example A recomputes this.

```mermaid
flowchart LR
    A["Threshold or segmentation<br/>binary mask, polarity"] --> B["Opening<br/>remove specks, thin bridges"]
    B --> C["Closing<br/>fill holes, small gaps"]
    C --> D["Labeling<br/>4- or 8-connectivity"]
    D --> E["Stats per label<br/>area, box, centroid"]
    E --> F["Filters<br/>size, shape"]
    F --> G["Count, measure,<br/>track"]
```

*Diagram: a common cleaning-then-labeling sequence (project synthesis). Opening and
closing can be swapped or omitted; each choice changes which errors dominate.*

## Prerequisites and competencies

**Required prerequisites**: [vault conventions](../../01-Parcours/Pre-requis.md).
Useful background:

- set operations (union, intersection, complement, translation);
- neighbourhood operators and borders: [CV-FILTRES](31-filtrage-gradients.md);
- thresholding and distance transforms:
  [CV-WATERSHED](../../90-segmentation/references/91-otsu-distance-watershed.md);
- graphs and union-find (disjoint sets).

**Target competencies**: predict the effect of erosion, dilation, opening and
closing on shape and topology, choose a structuring element from physical sizes,
choose and report a connectivity, read OpenCV labeling outputs correctly, and diagnose
merges, splits and lost defects.

## Assumptions, observability and degenerate cases

- **Binary, well-thresholded masks.** Morphology acts on the mask, not on the image;
  it cannot recover a defect lost by thresholding, nor tell a dust particle from a
  defect of the same size.
- **Scale separation.** Opening and closing help only when the structures to remove
  and the structures to keep differ in size or shape relative to $B$.
- **Origin and symmetry of $B$.** Erosion is anti-extensive only when the origin
  belongs to $B$, and dilation extensive under the same condition [Haralick et al.,
  §II, Proposition 20 and the discussion of dilation's extensivity]; opening and closing are
  anti-extensive and extensive "regardless of whether or not" $B$ contains its origin
  [§III, Propositions 41–42].
- **Borders.** Outside the image, a rule must decide whether pixels count as
  foreground. OpenCV's default border value is "magic": `DBL_MAX` for erosion,
  converted to `-DBL_MAX` for dilation [imgproc.hpp, L1514–L1515], so the image
  border neither erodes nor dilates objects.
- **Connectivity consistency.** Holes are only well defined when foreground and
  background use complementary connectivities (8 and 4, or 4 and 8); worked
  example B shows the ambiguity otherwise (project construction).

Observability and degenerate cases. A label number says nothing about which object
it is; labels can be renumbered. Two objects in contact are one component under any
connectivity; separating them requires extra information (markers, shape). An empty
mask yields only the background label ($N=1$). A structuring element larger than an
object erases it under opening; a single-pixel element leaves the mask unchanged.

## Procedure

```text
1. contract     fix polarity (foreground = nonzero), range, footprint (mm/px)
2. sizes        list the smallest structure to keep and the largest artefact
                to remove, in mm, then in pixels
3. element      choose shape (disk-like for isotropy, line for oriented gaps)
                and odd size between those two sizes; centre anchor
4. clean        opening for specks and bridges, closing for holes and gaps;
                order matters; log pixels removed and added
5. label        connectivity 4 or 8 chosen from the contact that defines an object
6. measure      stats per label; convert to physical units; filter by size/shape
7. check        compare counts and merges/splits with ground truth per size class
```

Purpose of the steps. Steps 1–3 tie the structuring element to physical sizes so
that it keeps meaning when resolution changes. Step 4 makes the sign of each error
explicit: opening removes pixels, closing adds them. Step 5 states what "connected"
means for the task. Steps 6–7 judge cleaning by counting and measurement errors, not
by appearance.

## Mathematics, conventions and units

**Set definitions** [Haralick et al., §II, Definitions 1 and 17]. For sets
$A,B\subset\mathbb Z^2$ (pixels), dilation is the Minkowski sum
$A\oplus B=\{a+b:a\in A,b\in B\}$ and erosion is
$A\ominus B=\{x: x+b\in A\ \forall b\in B\}$, the positions where $B$ translated to
$x$ fits in $A$. With the reflection $\check B=\{-b:b\in B\}$ and complement $A^c$,
erosion and dilation are dual: $(A\ominus B)^c=A^c\oplus\check B$ [Theorem 25].

**Opening and closing** [§III, Definitions 35–36]. $A\circ B=(A\ominus B)\oplus B$ and
$A\bullet B=(A\oplus B)\ominus B$. Properties: both are increasing; opening is
anti-extensive ($A\circ B\subseteq A$, Proposition 41) and closing extensive
($A\subseteq A\bullet B$, Proposition 42); both are idempotent (Theorems 38 and 40);
both are invariant to translations of the image and of the structuring element.

**Geometric characterization and duality** [§III, Theorem 43, Propositions 44–45]. The
opening is the union of all translates of $B$ contained in $A$,
$A\circ B=\bigcup\{B_y: B_y\subseteq A\}$: a pixel survives when some placement of $B$ that
covers it fits entirely in the foreground. The closing keeps a pixel $x$ when every
translate of the reflected element $\check B$ that covers $x$ meets $A$, which is $B$ itself
for a symmetric element. Opening and closing are dual,
$(A\bullet B)^c=A^c\circ\check B$: closing the foreground is opening the background with the
reflected element. The same propositions imply that the origin of $B$ does not change an
opening or closing of sets, unlike the shifted OpenCV result of worked example C.

**Chain rule and size** [§II, Proposition 3; §III, Corollary 31].
$A\oplus(B\oplus C)=(A\oplus B)\oplus C$ and $A\ominus(B\oplus C)=(A\ominus B)\ominus C$:
$n$ erosions by a $3\times3$ square equal one erosion by a $(2n+1)\times(2n+1)$
square, and a large rectangle decomposes into a row then a column. For a $k\times k$
square ($k$ odd), dilation grows a shape by $(k-1)/2$ pixels on each side, so a
closing bridges straight gaps of up to $k-1$ pixels and an opening removes strips
narrower than $k$ pixels (project derivation, worked example A).

**Grey-level form in OpenCV** [imgproc.hpp, L2325–L2382]. Erosion
$\mathrm{dst}(x,y)=\min_{(x',y'):\,B(x',y')\neq0}\mathrm{src}(x+x',y+y')$ and dilation
the same with $\max$, offsets relative to the anchor. On a 0/255 mask, erosion is the
set erosion above; dilation by $\max$ over the same offsets equals the set dilation by
$\check B$, so it matches $A\oplus B$ only for elements symmetric about the anchor
(project reading of the documented formulas).

**Connectivity.** The 4-neighbourhood of $(x,y)$ is $\{(x\pm1,y),(x,y\pm1)\}$; the
8-neighbourhood adds the four diagonals. A component is a maximal set of foreground
pixels connected by paths of neighbours.

**Two-pass labeling** [Wu et al., abstract and §1]. A forward scan gives each object
pixel a provisional label from its already-visited neighbours in a scan mask; label
equivalences are stored in a union-find structure; a second pass replaces provisional
labels by their representatives. The algorithm is linear in the number of pixels; a
decision tree reduces the neighbours inspected "by a factor of about 2" on average.

### Worked example A: gaps, kernel size and resolution

Constructed example, recomputed by checks/33-morphologie-composantes.py. Two 6×6
squares separated by a straight gap of $g$ pixels, closed with a $k\times k$ square:

| Gap $g$ (px) | $k=3$ | $k=5$ |
| --- | --- | --- |
| 2 | merged (1 component) | merged |
| 3 | separate (2) | merged |
| 4 | separate | merged |
| 5 | separate | separate |

A 0.2 mm gap is 2 px at 0.1 mm/px (merged by $k=3$) and 4 px at 0.05 mm/px
(separate with $k=3$, merged with $k=5$). Conversely, opening with $k=3$ removes a
scratch 2 px wide and keeps one 3 px wide; at the finer resolution the same physical
scratch is 4 px wide and survives.

### Worked example B: connectivity changes counts and holes

Constructed example, recomputed by checks/33-morphologie-composantes.py.

- Two pixels touching at a corner: 2 components under 4-connectivity, 1 under
  8-connectivity; OpenCV would return $N=3$ and $N=2$ labels, background included.
- A diagonal line of 10 pixels: 10 components under 4-connectivity, 1 under 8.
- A diamond ring (the four 4-neighbours of a centre pixel, centre empty): under
  8-connectivity the ring is one component; if the background also uses
  8-connectivity, the empty centre connects diagonally to the outside and the ring has
  no hole; with 4-connected background the centre is an enclosed hole.

### Worked example C: an asymmetric element in OpenCV

Constructed example, recomputed by checks/33-morphologie-composantes.py from the
documented formulas (no OpenCV call executed). In 1-D, take the foreground run
$\{0,\dots,4\}$ and a 2-pixel element with the default anchor at index 1 (offsets
$\{-1,0\}$). The set opening $(A\ominus B)\oplus B$ returns $\{0,\dots,4\}$. Applying
OpenCV's erosion then dilation with the same offsets returns $\{1,\dots,5\}$: shifted
by one pixel and no longer inside $A$. Even-sized or off-centre elements therefore
need care; odd, centred, symmetric elements avoid the issue.

### Worked example D: the order of opening and closing

Constructed example, recomputed by the 2026-11-16 check script
(`docs/revues/2026-11-16-card-depth/checks/33-morphologie-composantes.py`). In 1-D, take the
run $\{0,\dots,5\}$, a one-pixel speck at 7 and the centred element $\{-1,0,1\}$. Opening
first erodes the run to $\{1,\dots,4\}$ and the speck to nothing, then dilates back to
$\{0,\dots,5\}$; the closing that follows leaves it unchanged. Closing first dilates to
$\{-1,\dots,8\}$ and erodes to $\{0,\dots,7\}$, filling the gap at 6 and absorbing the speck;
the opening that follows keeps $\{0,\dots,7\}$. The object measures 6 or 8 pixels depending
only on the order (CV-MORPHO-001).

## Parameters and tuning

| Parameter | Unit | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Structuring-element size $k$ | px | Scale of removed specks or filled gaps | Convert from mm; changes meaning with resolution |
| Shape (rectangle, cross, ellipse, diamond) | — | Isotropy and direction of action | A square acts more along diagonals than a disk of the same width |
| Anchor | px | Shift of the result for asymmetric elements | Keep centred; even sizes shift (worked example C) |
| Iterations | — | Effective size $1+n(k-1)$ for a full rectangle | OpenCV's opening with 2 iterations is erode, erode, dilate, dilate |
| Operation order | — | Opening then closing versus the reverse | Different results; each removes or adds pixels first |
| Border rule | — | Whether objects touching the border are eroded | OpenCV default leaves borders neutral |
| Connectivity | 4 or 8 | Which contacts join pixels | Report it with every count; use the complement for holes |
| Size and shape filters | px² or mm² | Removal of residual specks | Applied after merges, they cannot split merged parts |

Tuning approach (project method). Write down, in millimetres, the smallest structure
to keep, the smallest gap that separates two legitimate objects, and the largest
artefact to remove; choose $k$ between them after conversion to pixels. If the
intervals overlap, morphology alone cannot meet the requirement: change acquisition,
thresholding or use markers. Sweep $k$ and shape on held-out masks with labelled
objects, and plot merges, splits and lost small defects against $k$.

## Properties and limits of guarantees

- **Order properties** (increasing, anti-extensive or extensive, idempotent) hold
  for the set definitions [Haralick et al., §III]; an implementation with an
  asymmetric element or a non-neutral border can violate them (worked example C).
- **Idempotence** means repeating the *same* opening changes nothing; increasing the
  number of erosions and dilations is a different, larger opening.
- **Topology is not preserved.** Opening can disconnect a component (break a thin
  bridge) and remove it; closing can connect components and fill holes. Counts can
  move in either direction.
- **Morphology has no semantics.** Size and shape relative to $B$ are the only
  criteria; a defect and a dust particle of the same size are treated alike.
- **Labels are arbitrary integers.** OpenCV notes that "SAUF algorithm forces a row
  major ordering of labels while Spaghetti and BBDT do not" [imgproc.hpp, L4009–L4020];
  the default is Spaghetti [L413–L420], so label order must not be relied on.
- **Discrete disks are approximations.** Pixel-grid ellipses and diamonds are not
  rotation-invariant; small elements are strongly anisotropic.

## Cost and implementation

Cost drivers. A naive binary erosion or dilation costs $|B|$ comparisons per pixel;
rectangular elements decompose into a row and a column pass (chain rule), and full
rectangles with several iterations are merged into one larger rectangle in OpenCV
[morph.dispatch.cpp, L1004–L1017]. Labeling is linear in the number of pixels
[Wu et al., abstract]; its constant depends on the scan mask, union-find and memory
access. Reported by Wu et al.: their two-pass algorithm up to 10 times faster than
the authors' contour-tracing program on their test platforms (empirical result, not
re-measured).

Implementation contracts in OpenCV 4.13.0 (read in the headers and sources on GitHub
because docs.opencv.org returned HTTP 403; no code was executed):

- `getStructuringElement(shape, ksize, anchor)`: `MORPH_RECT`, `MORPH_CROSS`,
  `MORPH_ELLIPSE` (inscribed in the rectangle) and `MORPH_DIAMOND` (Manhattan
  distance); "only the shape of a cross-shaped element depends on the anchor
  position. In other cases the anchor just regulates how much the result … is
  shifted" [imgproc.hpp, L234–L241, L1517–L1530].
- `erode`, `dilate`: min and max formulas above; default border `BORDER_CONSTANT` with
  the magic value; an empty kernel means a 3×3 rectangle [L2325–L2382].
- `morphologyEx`: `MORPH_OPEN` is erode then dilate and `MORPH_CLOSE` dilate then
  erode with the same kernel and anchor [morph.dispatch.cpp, L1236–L1247]; also
  gradient, top-hat, black-hat and hit-or-miss (binary `CV_8UC1` only)
  [imgproc.hpp, L216–L230]; "an opening operation (#MORPH_OPEN) with two iterations is
  equivalent to apply successively: erode -> erode -> dilate -> dilate" [L2405–L2407].
- `connectedComponents(image, labels, connectivity=8, ltype=CV_32S)`: 8-bit
  single-channel input, 4 or 8 connectivity, labels in `CV_32S` or `CV_16U`;
  `ccltype` selects Spaghetti (default), BBDT or SAUF, with parallel versions when the
  image has enough rows [L4009–L4040; L413–L420].

## Evaluation and controlled variation

Evaluate at object level: match predicted components to ground-truth objects (for
example by overlap), then count merges (one component, several objects), splits (one
object, several components), misses and false components, per size class; report
area or diameter errors in physical units. Pixel-level overlap can stay high while a
merge loses one object from the count.

### Proposed baseline and controlled variation (not executed)

- **Question**: does increasing the closing size to fill pin-holes cost more in merged
  parts than it gains in completeness?
- **Data**: held-out images of loose parts with labelled instances, including pairs at
  the minimum legitimate gap and parts with pin-holes; resolution in mm/px recorded.
- **Baseline**: fixed threshold, 3×3 opening, 3×3 closing, 8-connectivity labeling,
  size filter.
- **Controlled variation**: closing with a 5×5 square; everything else unchanged.
- **Measurements**: count error, merge rate and split rate per gap class, pin-holes
  remaining, area error in mm².
- **Expected effect (hypothesis)**: fewer pin-holes; merges appear for gaps of 3–4 px
  (worked example A).
- **Confound**: the size filter's threshold interacts with merged areas; keep it fixed
  and report its rejections.

Measurement limits. Ground-truth instances for touching objects are themselves
uncertain; counts on few images have wide intervals; results transfer only at the
same resolution.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Count too low: two parts are one component | Closing or dilation bridged a gap; 8-connectivity through a corner | Difference mask before/after; repeat with 4-connectivity | Smaller element; oriented element; markers and watershed |
| Count too high: one part in several components | Opening broke a thin bridge; 4-connectivity on diagonal structures | Difference mask; repeat with 8-connectivity | Smaller opening; closing first; 8-connectivity |
| Small real defects disappear | Opening element larger than the defect | Defect width in px versus $k$ | Smaller element; detect defects before cleaning |
| Results shift by one pixel | Even-sized or off-centre element | Apply to a single-pixel test image | Odd, centred element |
| Behaviour changes after a camera change | Element size fixed in pixels | Convert gaps and defects to pixels at both resolutions | Size the element in mm |
| Hole counts inconsistent | Same connectivity for foreground and background | Count holes with complementary connectivity | Use 8/4 or 4/8 consistently |
| Component count off by one | Background label counted as an object | Compare $N$ with the number of foreground labels | Use $N-1$ |
| Opening fills holes instead of removing specks | Inverted polarity: objects are 0 on a 255 background, so the operation acts on the background and, by duality, closes the objects [Theorem 43] | Apply the operation to a synthetic mask with one speck and one hole | Invert the mask or swap the operation; state the polarity |
| Objects at the image border shrink or grow | Non-neutral constant border | Compare with the default magic border | Neutral border or ignore border components |
| Label colours or IDs change between runs or versions | Label order depends on the algorithm | Compare SAUF and the default | Sort components by position or match by geometry |

## Alternatives and applications

- **Prefer opening** to remove isolated specks and thin protrusions smaller than the
  structures to keep; **prefer closing** to fill pin-holes and small gaps when objects
  are farther apart than the element; **prefer neither** when the size ranges overlap.
- **Prefer area filtering on components** when specks are isolated and of any shape,
  since it does not alter the shape of the remaining objects.
- **Prefer a distance transform and marker-based watershed**
  ([CV-WATERSHED](../../90-segmentation/references/91-otsu-distance-watershed.md)) to
  split touching convex objects; prefer instance segmentation
  ([CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md))
  when contact and appearance are too complex for geometric rules.
- **Prefer 8-connectivity** for thin or diagonal foreground structures and
  **4-connectivity** when diagonal contact should not join objects; report the choice.

Industrial uses (project reasoning, not published results): counting parts, cells or
particles; cleaning defect masks before measuring area and length; filling holes in
segmentation masks before computing areas; separating characters before OCR; blob
detection for simple tracking.

## Guided reasoning and proposed checks

These constructed cases develop geometric support, topology and the connectivity
convention. They explain or test reasoning; no image, video or hardware result is
claimed as measured. The method properties remain tied to the sources below.

### Case linked to CV-MORPHO-001

**Working question**: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?

**Reference answer**: Opening erodes then dilates and can remove small foreground structures; closing dilates then erodes and can fill holes or gaps. Choose the structuring element according to the sizes and shapes to keep.

**Geometric explanation**: Erosion requires the structuring element to fit inside the foreground; it therefore removes positions close to some borders. Dilation then extends the retained positions. In an opening, a structure too narrow to survive erosion does not reappear simply because dilation follows. In a closing, sufficiently small gaps can be filled.

**Choice of scale**: A size in pixels represents a physical size only if resolution and geometry are known. A structuring element suited to one camera can erase the target defects after a resolution change. In a constructed example, comparing a fine defect and a dust particle of similar size shows that morphology has no semantic information to distinguish them. Therefore evaluate removals and merges on critical cases, stating the mask polarity, the shape of the structuring element and the border handling.

### Case linked to CV-MORPHO-003

**Working question**: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?

**Reference answer**: The structuring element may have created a bridge; inspect the before/after mask and the distance between objects.

**Mechanism of the error**: dilation can join two regions separated by a gap smaller than the scale of the structuring element. The following erosion does not necessarily restore this gap; the closing may keep a common area. Connected-component labeling then correctly counts a single connected set, but this set no longer represents a single object in the world.

**Discriminating check**: Display the pixels added between the before and after masks, then vary the size and orientation of the structuring element on the same fixed image. If the number of objects changes when the bridge appears, the cause is localized. Area filtering after the merge does not recover the two parts: it acts on the region already grouped. Depending on the scene, preserve the gap, use separation markers or instance segmentation. Any correction must also be evaluated on genuinely contiguous objects, to avoid solving one case by fragmenting others.

**Source consulted for this pass**: [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html), erosion, dilation, opening, closing. The other developments are in the [flashcards](../33-morphologie-composantes.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-MORPHO-001

**Situation**: Which geometric effects distinguish binary opening and closing, and why must structuring-element size suit the task?

**Properties to know**: on ideal binary sets with the same structuring element, opening is anti-extensive: its result is included in the initial foreground. Closing is extensive: it can only add pixels. Both are idempotent: applying the complete operation a second time with the same structuring element does not change the theoretical result. Increasing the number of erosions and dilations, on the other hand, changes the effective support and is not "repeating an identical opening". Finite images, border values and anchors must be consistent for these properties to hold in an implementation. Opening can break a thin bridge and closing can create one; these topological changes can be decisive when counting objects.

### CV-MORPHO-002

**Situation**: A mask contains only two foreground pixels touching at one corner. How many components exist under 4-connectivity and 8-connectivity?

**Constructed labeling algorithm**: scan the mask; at each foreground pixel not yet visited, create a label and explore its eligible neighbors with a queue or a stack. All reached pixels receive the same label, then the scan resumes on the remaining pixels. This definition directly links the number of components to the number of explorations started. A practical implementation can use two passes and union-find without changing the defined connectivity. Beware of a library return value that counts the background as a label: two foreground components then give three labels in total. Holes and contacts also require a coherent neighborhood convention between background and foreground.

### CV-MORPHO-003

**Situation**: After morphological closing, two nearby parts are counted as one. Which assumption should be checked?

**Why the area filter is too late**: The area of a merged component is essentially the sum of the two parts plus the bridge pixels. It can therefore easily pass a minimum threshold, even when the count is wrong. Measuring separately the distance between borders before closing, the width of the bridge created and the maximum distance inside each part helps to choose a remedy. A marker-based watershed can use two reliable centers to restore the separation, but bad markers can oversegment a single part. In the evaluation, explicitly distinguish merge errors, split errors and boundary errors: an average pixel score can remain good despite an object lost in the count.

**Passages consulted for these developments**: [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html), §§1–4, erosion, dilation, opening and closing; [OpenCV 4.13, connectedComponents](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html), connectivity and labels.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-MORPHO-002 — Connectivity changes the object definition

On a checkerboard of isolated diagonal foreground pixels, 8-connectivity can join a long chain that 4-connectivity separates. Neither choice is universally correct: the relevant physical contact and expected pixel sampling determine the convention. Use complementary background connectivity when analyzing holes to avoid ambiguous digital topology. Count foreground components separately from the background label returned by a labeling routine.

### CV-MORPHO-003 — Kernel scale should follow physical separation

If the minimum legitimate gap is 0.2 mm and image resolution changes from 0.1 to 0.05 mm/px, the same physical gap changes from two to four pixels. Reusing an unchanged kernel therefore changes its physical action. A proposed sweep records both removal of isolated noise and merging of neighboring real parts as a function of kernel size and shape. Area filtering after merging cannot recover the lost instance boundary.

Consulted foundations: [OpenCV morphology](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html): erosion, dilation, opening, closing and structuring elements.

## Sources and flashcards

### Scientific sources

- [Haralick, Sternberg and Zhuang 1987, Image Analysis Using Mathematical Morphology, IEEE TPAMI 9(4): 532–550](https://doi.org/10.1109/TPAMI.1987.4767941): §II (Definition 1 dilation, Proposition 3 chain rule, Propositions 12 and 20, Definition 17 erosion, Proposition 22, Definition 24 reflection, Theorem 25 duality, Corollary 31), §III (Definitions 35–36, Theorems 38 and 40, Propositions 41–42, qualitative effects of disk openings and closings).
- [Wu, Otoo and Suzuki 2009, Optimizing two-pass connected-component labeling algorithms, Pattern Analysis and Applications 12(2): 117–135](https://doi.org/10.1007/s10044-008-0109-y): abstract and §1 (two-pass scheme, scan masks, union-find, linear complexity, decision tree, reported speed-ups).

The gap and strip thresholds of worked example A, the connectivity cases of worked
example B, the reading of OpenCV's formulas in worked example C and the evaluation
protocol are project derivations or proposals.

### Implementation sources

- [OpenCV 4.13.0, `modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L216-L241): `MorphTypes` and `MorphShapes` (L216–L241), `ConnectedComponentsTypes` and `ConnectedComponentsAlgorithmsTypes` (L399–L420), border value and `getStructuringElement` (L1514–L1530), `erode` and `dilate` (L2325–L2382), `morphologyEx` (L2384–L2412), `connectedComponents` (L4009–L4085).
- [OpenCV 4.13.0, `modules/imgproc/src/morph.dispatch.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/morph.dispatch.cpp#L1236-L1247): opening and closing composition (L1236–L1247), iterations merged into a larger rectangle (L1004–L1017).
- [OpenCV 4.13, Morphological Transformations tutorial](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html) and [structural analysis reference](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html): retained links, not re-read in this pass (HTTP 403).

### Related flashcards and references

- [Flashcards](../33-morphologie-composantes.md): CV-MORPHO-001 (opening versus closing), CV-MORPHO-002 (connectivity), CV-MORPHO-003 (merges after closing).
- Related references: [CV-WATERSHED](../../90-segmentation/references/91-otsu-distance-watershed.md), [CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md), [CV-FILTRES](31-filtrage-gradients.md).

Drafted by agent, 2026-10-18. Revision 8, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/33-morphologie-composantes.md).
Revision 9, 2026-11-16: Theorem 43 and Propositions 44–45, worked example D (order of opening and closing) and a polarity failure row added while deepening CV-MORPHO-001, by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-16-card-depth/33-morphologie-composantes.md).
