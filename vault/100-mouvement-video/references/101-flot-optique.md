---
id: CV-FLOT
type: methode
domaine: d10
poles: [B, C, D]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-MATCHING"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Optical flow: Lucas–Kanade, Farnebäck and RAFT

## Problem, data and assumptions

Estimate image displacements between frames, sparse or dense, without confusing them with object identities. Inputs: images with cadence, preprocessing and time direction; output: vectors in the coordinate frame pixel and indicators according to method.

## Prerequisites and competencies

**Required prerequisites**: [CV-MATCHING](../../40-features-matching/references/43-detecteurs-matchers.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Lucas – Kanade linearizes a photometric constancy and assumes a local coherent movement. The pyramid extends the useful displacements; Farnebäck proposes a dense estimation by local polynomial representation. RAFT leverages features, all-peer correlations and recurring updates.

## Mathematics, conventions and units

Linearization gives $I_xu+I_yv+I_t\approx0$, u,v in pixels between frames if the derivatives follow this step. The local system requires gradients in several directions. A flow between frames is a px/s speed only after division by the appropriate interval.

## Parameters and properties

Window, pyramid, texture, noise, resolution and occlusion. RAFT to two images does not intrinsically provide a long-term identity. Constantity of intensity and small displacements are hypotheses of the linearized method, not of any video vision.

## Cost and implementation

An all-pair correlation has a significant memory cost depending on the resolution of the features; an implementation can optimize it. No flow code executed; no FPS compared except hardware/protocol.

## Evaluation and controlled variation

Baseline: synthetic translation and displacement reference; vary illumination and then occlusion separately. Measure EPE on observable regions and occlusion masks, not just a color visualization.

## Failure modes and diagnosis

On an edge, the aperture problem leaves an ambiguous direction; under occlusion, the correspondence may disappear. `status=1` of an API does not prove the physical truth; check round trip and validity.

## Alternatives and applications

Tracked features, dense flow, object tracker or ReID depending on output. A mobile camera creates background flow even if no object moves in the world.

## Guided reasoning and proposed checks

These constructed cases develop a constraint of luminance, aperture and dense correspondence. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FLOT-001

**Question of work**: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?

**Reference Response**: An equation does not constrain two unknowns without assumptions/neighboring; an edge can keep a tangential ambiguity.

**Reading the constraint**: The spatial gradient provides a direction in which a variation in intensity informs displacement. The movement tangent to a uniform edge changes little the intensities: several vectors can then satisfy the same equation. This is a lack of local information, not necessarily a mistake of the solver.

**Example and Limit**: A vertical edge that slides upwards may seem almost unchanged in a small window. Adding pixels of the same edge does not create a second independent direction. A neighbourhood with a corner can better constrain the two components if the movement remains sufficiently coherent and the photometry stable. Examine conditioning, window size, and hypothesis validity before increasing iterations. A regularization can choose one of several plausible solutions; it then adds a hypothesis, and not a certain observation of the displacement.

### Case linked to CV-FLOT-004

**Question of work**: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?

**Reference Response**: As an estimate under the assumptions of the model, with no guaranteed observable correspondence; examine occlusion mask and consistency.

**Why density doesn’t prove anything**: A dense algorithm can fill regions where the data no longer contains a visible match. The value produced can come from context, regularization, or a learned model. These mechanisms give a useful hypothesis, but not a new observation of the hidden surface.

**check**: distinguish occlusion, field exit and matching error. For a round trip, evaluate the inverse flow at the position reached in the other image, taking into account the interpolation and the limits of the field. An inconsistency signals a possible problem; consistency does not guarantee identity on a repetitive texture. Measure regions separately according to an announced visibility protocol. At the inference, a ground truth of occlusion is not magically available: the trust policy must use only the information actually provided to the system.

**Documentary reference for this pass**: [OpenCV 4.13, Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), Lucas-Kanade, pyramids and dense flow. The other developments are in the [flashcards](../101-flot-optique.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FLOT-001

**Situation**: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?

**Lucas – Kanade System**: stack the window gradients in a $A$ matrix with each row equal to $(I_x,I_y)$, and set $b=-I_t$. The least squares give $A^TA\,d=A^Tb$, with $d=(u,v)^T$. Two sufficiently informative eigenvalues of $A^TA$ are required to constrain both directions; an edge typically produces a weak direction. Expanding the window may bring new gradients, but possibly violates the assumption of shared motion by mixing two objects. A good selection of points therefore simultaneously seeks spatial information and neighborhood coherence, not just a large gradient amplitude.

### CV-FLOT-002

**Situation**: An optical flow vector represents 4 pixels between two images. Does this imply a velocity of 4 px/s?

**Change of grid**: If the second string works on an image resized by $(s_x,s_y)$, the same displacement becomes $(s_xu,s_yv)$. To compare image speeds, first put the vectors in a common grid and then use the real acquisition intervals. A lost frame eventually doubles the interval, without the physical speed having doubled. In perspective, even a constant 3D translation produces depth-dependent image displacements; an apparent size variation can also change the field. The conversion pixels→meters therefore requires a scene and camera model, beyond a division by the nominal rate.

### CV-FLOT-003

**Situation**: What distinct roles do correlations and recurrent updates play in RAFT?

**Dimensions of Correlation**: for two feature maps $h\times w$, an all-peer compatibility connects each site of the first to each site of the second, $(hw)^2$ values before optimizations. The volume encodes candidate similarities, not a bijective assignment of pixels. Updates look at this volume around predicted positions and adjust the flow; multiple sources may target a nearby region, and occlusionss do not always offer a match. Separating memory from volume, cost per iteration, and number of iterations helps to understand the resolution compromise. The recurrence of refinement is not a guarantee of physical convergence or identity.

### CV-FLOT-004

**Situation**: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?

**residual round trip**: note $F_{12}$ moving the 1 image to 2 and $F_{21}$ back. For a pixel $x$ of the first image, calculate $e(x)=\|F_{12}(x)+F_{21}(x+F_{12}(x))\|$ in pixels, only when the return sampling is valid. A trust rule can compare this residual to a tolerance dependent on movement and noise, to be validated on reserved data. A periodic texture can produce an erroneous translation and then its exact opposite: the zero residual then proves nothing on the real surface. Keep the visibility failure distinct from a simple large digital residual.

**Passages consulted for these developments**: [OpenCV 4.13.0, Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), Lucas-Kanade equation and system; grid compositions and changes deduced; [Teed–Deng, RAFT](https://arxiv.org/html/2003.12039v3), figure 1 and presentation of all-pair and updated correlations.

## Sources and flashcards

- [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039).
- [Related flashcards](../101-flot-optique.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
