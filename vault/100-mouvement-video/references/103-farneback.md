---
id: CV-FARNEBACK
type: methode
domaine: d10
poles: ["B", "C", "D"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-FLOT", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Farnebäck — dense optical flow through polynomial expansion

## Prerequisites and competencies

**Required prerequisites**: [CV-FLOT](101-flot-optique.md), [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md). **Target competencies**: explain the polynomial mechanism; solve an ideal local constraint; read the coordinate frame and the flow units; interpret a round-trip inconsistency; adjust the pyramid without masking failures. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Estimate the apparent dense displacement between two images, without resulting in a network. Inputs: frames compatible in size, photometry and instant; output: two displacement components per pixel. In OpenCV 4.13, `flow[y,x]` corresponds to the point $(x,y)$ of the previous image and gives its displacement towards the next image. These are pixels per pair of frames, not a metric speed, object identifier, or depth.

## Intuition and procedure

Farnebäck approximates each neighborhood by a quadratic polynomial. A displacement transforms its coefficients; we deduce a local constraint, spatially aggregated. A pyramid and iterations estimate a coarse movement and then refine it. The calculation produces a vector even in ill-informed regions: output density and reliability are not synonymous.

## Mathematics and conventions

Write $f_1(x)=x^TAx+b_1^Tx+c_1$ for local coordinates $x\in\mathbb R^2$, with $A$ symmetric $2\times2$. For a translation $d$ in pixels, $f_2(x)=f_1(x-d)$ gives $b_2=b_1-2Ad$, so $2Ad=b_1-b_2$. $A$ has the units intensity/pixel², $b$ intensity/pixel; both sides have the same units. Real coefficients are approximated and noisy: the method aggregates local constraints instead of assuming a reliable inversion in each pixel. A flat or essentially unidirectional neighborhood makes displacement unobservable.

## Parameters, assumptions and cost

Expansion and aggregation windows regulate noise resistance and smoothing of movement boundaries. Pyramid levels and ratios extend the range of catchable displacements, without guaranteeing any large movement; small structures can disappear at coarse levels. The iterations refine around the initialization. Cost depends on pixels, scales, neighborhoods, and iterations; measuring full time rather than abstractly opposing CPU and deep learning. API OpenCV checked with Context7; no video footage was processed for this batch.

## Evaluation and controlled variation

Proposed baseline: known translation of a textured image, with explicit edge masks. To vary only the amplitude of the displacement; measure endpoint error on valid pixels and errors at borders. check then noise, blur and occlusions separately. Analytical example: with $A=\mathrm{diag}(2,1)$ and $b_1-b_2=(8,-2)^T$, the ideal relationship gives $d=(2,-1)^T$ px. This calculation does not constitute an execution of the dense flow.

## Diagnosis and alternatives

Incoherent vectors on a uniform wall require a check of texture, not just more iterations. A global movement can come from the camera; subtracting it requires a model and validation adapted to the scene. The round trip test samples the inverse flow at the displaced position: it signals certain inconsistencies but does not prove a match. Compare Lucas – Kanade if only points are required and RAFT if data, calculation and domain conditions justify it.

## Guided reasoning and proposed checks

These constructed cases develop quadratic approximation and displacement capture domain. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FARNEBACK-001

**Question of work**: How does Farnebäck estimate displacement from two image neighborhoods without point descriptors?

**Reference Response**: It approximates neighborhoods by quadratic polynomials, connects their coefficient changes to a translation, and then aggregates constraints and refines to multiple scales. For an ideal model $f_2(x)=f_1(x-d)$, we have $2Ad=b_1-b_2$.

**Interpretation of the local model**: Quadratic coefficients describe the shape of the intensities in a neighborhood, rather than an independent signature to match. An ideal translation leaves a special relationship between the terms of the two polynomials. The aggregation exploits several constraints to limit the fragility of an isolated inversion.

**Example of limit**: A uniform wall does not provide informational curvature in both directions; a neighborhood straddling two objects can mix two movements. Growing the window can reduce noise but smooth this border. check these regions separately in an assessment. A dense method offers output anywhere according to its format; local accuracy always depends on the image information and the adequacy of the model.

### Case linked to CV-FARNEBACK-005

**Question of work**: Why can adding optical-flow pyramid levels help with large motions while degrading small objects?

**Reference Response**: The displacement is reduced to coarse levels, but the reduction can make small structures disappear and mix boundaries. Evaluate both catchable amplitude, error of small objects and limits of movement.

**Compromise of scale**: At coarse levels, a large displacement of the initial image represents fewer pixels, which facilitates a local search. But an object of a few pixels can mix at the bottom and no longer provide its own movement. Fine refinement then starts from a hypothesis already influenced by its neighborhood.

**Experience built**: Use a scene with large background movement and small independent object, then vary only the pyramid. Report error on the background, on the object and at its border, as well as invalid pixels. An average bottom-dominated improvement may mask the loss of the small object. This reasoning links the parameter to the useful signal, without assuming that a larger budget uniformly improves all regions.

**Documentary reference for this pass**: [Farnebäck 2003](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf), §§2 – 3, polynomial expansion and displacement estimation. The other developments are in the [flashcards](../103-farneback.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FARNEBACK-001

**Situation**: How does Farnebäck estimate displacement from two image neighborhoods without point descriptors?

**Development of translation**: Replace $x$ with $x-d$ in $x^TAx+b_1^Tx+c_1$ gives $x^TAx+(b_1-2Ad)^Tx+d^TAd-b_1^Td+c_1$ when $A$ is symmetrical. The comparison of linear terms therefore provides $b_2=b_1-2Ad$. This derivation is accurate for the built model; the real images do not have the same polynomial transported everywhere. We then look for an aggregated and weighted solution to local constraints, with a domain where translation is an acceptable approximation. Constant terms also change, but do not replace the directional information needed to identify the two components of displacement.

### CV-FARNEBACK-002

**Situation**: For an ideal quadratic model, $A=\mathrm{diag}(2,1)$ and $b_1-b_2=(8,-2)^T$. If $2Ad=b_1-b_2$, what displacement is obtained, and which limitation must be kept in mind?

**Directional Sensitivity**: with $A=\operatorname{diag}(2,\varepsilon)$, the ideal equations become $4d_x=\Delta b_x$ and $2\varepsilon d_y=\Delta b_y$. A small error on $\Delta b_y$ is amplified by $1/(2\varepsilon)$ when $\varepsilon$ is small. A weak residual can thus coexist with a strong error on $d_y$. Solving the system by proper factorization and inspecting its packaging is more informative than blindly applying an inverse. A regularization numerically stabilizes the weak direction by adding a preference; it does not transform this preference into certain observation. This is precisely what the diagonal example makes it possible to understand without executing a complete flow.

### CV-FARNEBACK-003

**Situation**: An OpenCV calculation returns flow[y,x]=(4,-2) between frames 40 ms apart. Where should the correspondence be sought, and what can be concluded about velocity?

**Transport relationship**: The front convention is written $I_1(x,y)\approx I_2(x+u(x,y),y+v(x,y))$ when photometry and visibility are compatible. To sample the second image on the grid of the first, we therefore use these destination positions. Creating a destination image by projecting all the source pixels can produce holes and collisions; it is not the same resampling operation. For vector $(4,-2)$, keep the mask of the positions reached out of field. This check sense distinguishes a valid displacement, a warp inversion and a simple display whose axes have been swapped.

### CV-FARNEBACK-004

**Situation**: To check forward flow $F(x)$, can you add backward flow $B(x)$ evaluated at the same pixel?

**Composition of fields**: dial a $F_{12}$ move and then $F_{23}$ gives $F_{13}(x)=F_{12}(x)+F_{23}(x+F_{12}(x))$, under valid matches. The return is the particular case where one hopes to return to the same point, hence the formula of the residual. Adding the fields to the same indices would assume that these indices already denote the same surfaces in all images. The interpolation of the second field can still mix two movements at a border; keep this source of error in the interpretation. Consistent composition across multiple frames also accumulates errors and does not automatically become long-term tracking with visibility and re-identification.

### CV-FARNEBACK-005

**Situation**: Why can adding optical-flow pyramid levels help with large motions while degrading small objects?

**Orders of magnitude**: With a spatial reduction of two at each level, a displacement of 32 px in the original image becomes 4 px after three reductions. A wide object of 6 px, on the other hand, occupies only 0,75 px before the effects of filtering and sampling: its own movement can disappear. Moving up the field requires resizing the grid and multiplying the components by the appropriate scaling factor. Interpolating only the array without adjusting the amplitude produces a contract defect. This constructed example explains the trade-off between capturing large displacement and preserving small structures, without setting an optimal universal number of levels.

**Passages consulted for these developments**: [OpenCV 4.13.0, Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), Dense Optical Flow; project specific quadratic derivations, original PDF inaccessible by timeout during this pass.

## Sources and flashcards

- [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
- [OpenCV 4.13, Optical Flow, Dense Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [Related flashcards](../103-farneback.md): CV-FARNEBACK-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
