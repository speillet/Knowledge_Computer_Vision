---
id: CV-CANNY-HOUGH
type: methode
domaine: d03
poles: [B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Canny and Hough: edges, lines and segments

## Problem, data and assumptions

Locate contours and then search for a geometric structure. Canny produces an edge map; Hough accumulates votes for a family of primitives. A photometric boundary is not automatically an object edge, and a straight line is not a segment.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Canny exploits gradients, local suppression of non-maxima and hysteresis between two thresholds. Smoothing is a design step to be explained. Hough turns each contour point into votes in a parameter space, and then searches for maxima.

## Mathematics, conventions and units

For a straight line, $\rho=x\cos\theta+y\sin\theta$, with x,y and $\rho$ in pixels and $\theta$ in radians in the chosen convention. The discretization of the accumulator determines its resolution. The gradient combines spatial derivatives; its standard L1 or L2 is not the same score.

## Parameters and properties

Two Canny thresholds, gradient scale, rho/theta pitch, votes, minimum length and maximum deviation for a segment variant. Do not promise a Gaussian smoothing 5×5 internal to each Canny API.

## Cost and implementation

The number of active points and bins dominates the cost of naïve Hough; a probabilistic variant reduces labor under his assumptions. No library calls or real images executed.

## Evaluation and controlled variation

Proposed variation: add texture and blur separately to a room with known edges. Predict stray or lost contours; measure repeatability and line error, not just contour density.

## Failure modes and diagnosis

Too many lines on texture: check first outlines, useful region and bins. Interrupted contour: check contrast and hysteresis before lowering all thresholds.

## Alternatives and applications

LSD, robust fit and models learned according to continuity, noise and segment need. A business geometric constraint can limit false positives.

## Guided reasoning and proposed checks

These constructed cases develop connecting contours, votes and geometric validation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-CANNY-HOUGH-001

**Question of work**: Why does Canny use two thresholds instead of a single gradient threshold?

**Reference Response**: Strong contours initiate structures; weaker responses can be retained when they are related to strong ones according to hysteresis.

**Interpreted procedure**: The gradient measures a local variation in intensity. The removal of non-maxima keeps the ridges in the direction of the gradient in order to avoid thick bands. The hysteresis then decides which weak ridges extend a sufficiently strong structure. The low threshold allows for conditional continuity; it does not make all weak responses admissible.

**Constructed example**: An unevenly lit edge has a contrasting portion and a weak portion. A high single threshold fragments the edge; a low single threshold also retains a lot of texture. The two thresholds make it possible to keep certain small portions connected to the strong portion. If the entire contour is weak and without a strong primer, it may remain absent. The setting depends on the smoothing scale, contrast, and gradient definition; none of these steps single-handedly distinguishes part edges and background texture.

### Case linked to CV-CANNY-HOUGH-004

**Question of work**: Hough detects many lines on a textured surface. Which check avoids blindly tuning the voting threshold?

**Reference Response**: Inspect Canny edge map, angular distribution, useful region and spatial support of candidates.

**Proposed investigation**: Overlapping the lines and their support points to the image. If the votes come from repeated streaks, the detector may respond correctly to contours that are simply not those of the room. Then examine the distribution of angles and the number of fragments: this distinguishes a structured texture from a dispersed noise.

**Ablation construite**: Set the bins and thresholds, restrict a region of interest, and then separately change the smoothing and the expected orientation constraint. Measure business lines found, false candidates and position error. Increasing only the voting threshold can eliminate a useful edge that is not very contrasting while retaining a long and repetitive texture. A geometric constraint helps only if it remains valid for the orientations actually encountered. The accumulator has a photometric support; the validation of the part model is an additional decision of the pipeline.

**Documentary reference for this pass**: [OpenCV 4.13, Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html), polar parametrization and votes. The other developments are in the [flashcards](../32-canny-hough.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-CANNY-HOUGH-001

**Situation**: Why does Canny use two thresholds instead of a single gradient threshold?

**Describe hysteresis as a journey**: after calculating the gradient and removing non-maxima, initialize a queue with pixels above the high threshold. Browse their neighbors and recursively keep those above the low threshold; discard other unrelated answers. This diagram explains how a long, small portion can be retained without a single pixel exceeding the high threshold. The direction of the gradient is a normal to the contour, calculated with a convention such as $\operatorname{atan2}(G_y,G_x)$; the suppression compares the amplitudes along this normal. Changing norm L1/L2, smoothing or digital depth changes the scale of scores and therefore the direction of the thresholds.

### CV-CANNY-HOUGH-002

**Situation**: What do $\rho$ and $\theta$ represent in $\rho=x\cos\theta+y\sin\theta$?

**Angular accuracy and position**: A small $\delta\theta$ error causes $\rho$ to vary by about $(-x\sin\theta+y\cos\theta)\delta\theta$, with $\delta\theta$ in radians. The effect grows with distance at the origin: an angular bin does not represent a uniform tolerance in pixels everywhere. At a leverage of 500 px, a degree corresponds to an order of magnitude of 8,7 px. This derivation does not give the final error of a detector, but helps to choose a reasonable discretization and to understand an extrapolation. Couples $(\rho,\theta)$ and $(-\rho,\theta+\pi)$ represent the same straight line; the angle interval and the allowed sign of $\rho$ must be processed together.

### CV-CANNY-HOUGH-003

**Situation**: Why does HoughLines not directly return the endpoints of a real line segment?

**Find a Finished Support**: from the normal $n=(\cos\theta,\sin\theta)$, take a point $p_0=\rho n$ and the unit direction $d=(-\sin\theta,\cos\theta)$. For each $p$ contour point, test its normal $|n^Tp-\rho|$ distance, then project the points compatible with $s=d^T(p-p_0)$. Contiguous groups in $s$ offer segments, whose ends are equal to $p_0+s_{min}d$ and $p_0+s_{max}d$. This process distinguishes perpendicular tolerance and longitudinal holes. The choice of support, the presence of occlusions and a possible re-estimation of the line on its points condition the ends. It is not enough to take the minimum and maximum of all the collinear points of the image.

### CV-CANNY-HOUGH-004

**Situation**: Hough detects many lines on a textured surface. Which check avoids blindly tuning the voting threshold?

**Differentiating Vote and Adjustment Error**: a long texture provides a lot of points and therefore votes, even if it is not the desired structure. For a candidate, calculate in addition the normal distances $r_i=x_i\cos\theta+y_i\sin\theta-\rho$ on her support points, their longitudinal extent and the fraction of the positions actually covered. A very precise short line and a long discontinuous line do not have the same use. Also compare its relationship to other expected edges: parallelism, intersections or distances, if these properties are legitimate for the room. These validations are choices of the proposed pipeline; the accumulator score is not a calibrated probability of the presence of a business edge.

**Passages consulted for these developments**: [OpenCV 4.13, Canny](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html), gradient, Non-maximum Suppression and Hysteresis Thresholding; [OpenCV 4.13, Hough](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html), How does it work; Standard and Probabilistic Hough.

## Sources and flashcards

The tutorial describes a string with smoothing; its explanations do not constitute proof of an internal smoothing with each overload API. The edge map and the business constraints of the texture case are a constructed diagnosis.

- [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html).
- [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
- [Related flashcards](../32-canny-hough.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
