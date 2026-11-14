---
id: CV-CORNERS
type: methode
domaine: d04
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-FILTRES", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Harris and Shi–Tomasi — local structure and trackable points

This is the method note for corner detectors built on the local gradient structure
tensor: the Harris–Stephens response, the Shi–Tomasi minimum-eigenvalue criterion,
and OpenCV's `goodFeaturesToTrack`, which implements both. Related mechanisms live
in sibling notes: segment-test detection in [FAST and BRIEF](47-fast-brief.md),
scale-space detection and the Hessian edge test in [SIFT](41-sift.md), the Harris
response used to rank FAST corners in [ORB](42-orb.md), the comparison of
detector–descriptor–matcher pipelines in [CV-MATCHING](43-detecteurs-matchers.md),
and the Lucas–Kanade tracker that consumes these points in
[CV-FLOT](../../100-mouvement-video/references/101-flot-optique.md).

## Problem and data contract

**Task.** Select image locations whose small displacement can be measured in both
directions, so that a tracker or a matcher can find them again. Harris and Stephens
wanted discrete feature points for tracking because edges suffer from the aperture
problem and fragment differently from one frame to the next [Harris 1988,
pp. 147–148]. Shi and Tomasi define a good feature as one "that can be tracked
well" by the tracker that will use it [Shi–Tomasi, ch. 4].

**Data contract.**

- *Input*: one single-channel image $I$ of $H\times W$ pixels. OpenCV 4.13 accepts
  `CV_8UC1` or `CV_32FC1` only [corner.cpp L254]; color is converted upstream. Pixel
  $(x,y)$ has its centre at integer coordinates, with the origin at the top-left
  pixel, $x$ rightward and $y$ downward.
- *Intermediate data*: gradient images $I_x, I_y$ in intensity levels per pixel, three
  tensor fields $A$, $B$, $C$ (defined below), and a `CV_32FC1` score map of size
  $H\times W$ [imgproc.hpp L1943–L1981].
- *Output of `goodFeaturesToTrack`*: at most `maxCorners` points, stored as `CV_32F`
  $(x,y)$ pairs whose values are integer pixel positions, sorted by decreasing score;
  an overload also returns the scores [featureselect.cpp L424–L547; imgproc.hpp
  L2138–L2167]. A point carries no scale, orientation or descriptor. Subpixel
  positions need `cornerSubPix`.
- *Units*: the absolute score depends on the intensity range, the derivative operator,
  the window and the image depth (worked example C). Only relative thresholds transfer
  between images and settings.

**Role in a pipeline.** Seed points for pyramidal Lucas–Kanade (KLT) tracking in
visual odometry, stabilization and structure-from-motion front ends; a ranking score
inside ORB; initial positions refined by `cornerSubPix`. Downstream expects points
spread over the region to be estimated, away from the image border, and well
conditioned *for the tracker's own window*. Shi and Tomasi's argument ties the
selection to the tracker: the criterion is computed on the matrix the tracker inverts
[ch. 3–4]. OpenCV's defaults break that link, since selection uses
`blockSize=3` while `calcOpticalFlowPyrLK` tracks $21\times21$ windows
[imgproc.hpp L2127–L2130; video/tracking.hpp L181–L186]. The selection is then a
proxy, and the tracker applies its own minimum-eigenvalue gate, `minEigThreshold`,
on its window [video/tracking.hpp L163–L167].

## Intuition

Shift a small window by a few pixels and measure how much its content changes.
Harris lists three cases [p. 149]: on a flat patch, every shift changes little; on an
edge, a shift along the edge changes little and a shift across it changes a lot; on
a corner or isolated point, every shift changes a lot. The $2\times2$ tensor $M$
summarizes this change for every small shift at once. Its eigenvectors give the
directions of largest and smallest change and its eigenvalues measure them. Harris
scores the pair of eigenvalues without computing them; Shi–Tomasi keeps only the
smaller one, because a displacement estimate is as poor as its worst direction.

*Illustration (constructed).* In a road scene, the sky gives two eigenvalues at the
noise level, a lane-marking edge one large and one near zero, and the tip of a
painted arrow two large ones. The sources add two cases that pass the test yet are
poor features: a horizontal twig in front of a vertical twig forms an image corner
that "occurs only in the image, not in the world" [Shi–Tomasi, ch. 5], and features
on a car body are often reflections that slide over the surface [ch. 1].

```mermaid
flowchart LR
    A["Gray image I<br/>8-bit or float32"] --> B["Gradients Ix, Iy<br/>Sobel ksize or Scharr"]
    B --> C["Products<br/>Ix·Ix, Ix·Iy, Iy·Iy"]
    C --> D["Window sum<br/>box blockSize in OpenCV<br/>Gaussian in Harris 1988"]
    D --> E["Score map<br/>min eigenvalue or Harris R"]
    E --> F["Relative threshold<br/>qualityLevel · max"]
    F --> G["3×3 non-maximum<br/>suppression"]
    G --> H["Sort by score"]
    H --> I["Greedy spacing minDistance<br/>stop at maxCorners"]
    I --> J["Optional cornerSubPix"]
    J --> K["Tracker or matcher"]
```

*Diagram: data flow of `goodFeaturesToTrack` in OpenCV 4.13 [corner.cpp L237–L321;
featureselect.cpp L409–L541]. The Gaussian window is the choice of the Harris paper
[p. 149].*

## Prerequisites and competencies

**Required prerequisites**: [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md)
and [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md).
Useful background, by mechanism:

- discrete derivatives, Sobel and Scharr kernels, smoothing: [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md);
- eigen-decomposition and conditioning of a symmetric matrix: [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md);
- the Lucas–Kanade normal equations, which contain the same matrix: [CV-FLOT](../../100-mouvement-video/references/101-flot-optique.md);
- sensor noise, which sets the floor of a usable eigenvalue: [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md);
- non-maximum suppression and edge thinning: [CV-CANNY-HOUGH](../../30-traitement-image/references/32-canny-hough.md);
- homographies, used to evaluate repeatability: [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).

**Target competencies**: interpret local eigenvalues; distinguish the Harris and
Shi–Tomasi scores; configure a corner selection; separate detection failure from
matching ambiguity; evaluate a selection intended for tracking. FAST, SIFT and ORB are
alternatives, not implicit dependencies.

## Assumptions, observability and degenerate cases

- **Local translation and brightness constancy.** The tensor comes from a first-order
  expansion of $I(p+d)$ for a small $d$. Shi and Tomasi's motion model
  $I(x,y,t+\tau)=I(x-\xi,y-\eta)$ "is by and large satisfied at surface markings that
  are away from occluding contours" [ch. 2, eq. 2.1]. Over many frames, translation
  no longer describes a window's change, which is why they monitor features with an
  affine model [ch. 3, ch. 5].
- **One scale.** The derivative scale (`ksize`) and the integration scale
  (`blockSize`) are fixed. In Schmid et al.'s evaluation, repeatability of every
  detector tested, improved Harris included, was "very poor" beyond a scale factor of
  1.5 at a 0.5 px tolerance, or 2 at 1.5 px [Schmid 2000, §3.3.3].
- **Rotation.** The eigenvalues form a rotation-invariant description of $M$
  [Harris, pp. 149–150], but discrete derivative masks are not isotropic: a Harris
  implementation with the mask $[-2,-1,0,1,2]$ was least repeatable near 45°, and
  Gaussian derivatives removed that dependence [Schmid 2000, §3.3.1].
- **Contrast.** Multiplying the contrast by $\alpha$ multiplies both eigenvalues by
  $\alpha^2$ [Harris, p. 150]. A constant brightness offset leaves gradients
  unchanged unless pixels clip.
- **Noise floor.** Two small eigenvalues mean a roughly constant patch, and the
  threshold must exceed the eigenvalues measured on uniform regions with the same
  camera [Shi–Tomasi, ch. 4].

**Observability.** On an edge, the displacement component along the edge is not
observable: "only the vertical component of motion can be determined for a horizontal
intensity edge" [ch. 4]. On a repeated pattern, each corner is locally well
conditioned but globally ambiguous: $M$ describes the curvature of the matching cost
at zero shift and says nothing about its other minima (card CV-CORNERS-004).

**Degenerate cases.** Depth-discontinuity junctions, specular highlights and
occlusion boundaries pass the eigenvalue test without being world points [ch. 1,
ch. 5]. Lettering at the scale of a pixel aliases and tracks erratically [ch. 7].
Salt-and-pepper texture passes the test [ch. 4], and so does sensor noise above the
threshold. Saturated areas have zero gradient. OpenCV never returns a point on the
outermost row or column [featureselect.cpp L424–L437], and gradients near the border
use reflected pixels, since the default border mode is `BORDER_REFLECT_101`
[base.hpp L337–L341].

## Procedure

```text
goodFeaturesToTrack(I, maxCorners, q, minDistance, mask, blockSize, ksize, useHarris, k):
    Ix, Iy <- Sobel(I, ksize) * s       # s = 1 / (2^(ksize-1) * blockSize), / 255 more if 8-bit
    A <- boxsum(Ix*Ix); B <- boxsum(Iy*Iy); C <- boxsum(Ix*Iy)   # blockSize^2, unnormalized
    if useHarris: score <- A*B - C*C - k*(A+B)^2
    else:         score <- (A+B)/2 - sqrt(((A-B)/2)^2 + C^2)     # smaller eigenvalue
    t <- q * max(score inside mask)
    cand <- { p inside mask, not on the 1-pixel border :
              score(p) > t and score(p) == max of score over the 3x3 neighborhood }
    sort cand by decreasing score            # equal scores ordered by memory address
    kept <- []
    for p in cand:
        if minDistance >= 1 and some r in kept has |p - r| < minDistance: continue
        kept.append(p)
        if maxCorners > 0 and len(kept) == maxCorners: break
    return kept                              # integer pixel positions stored as float32
```

Purpose of each step:

1. **Gradients** measure local change; the operator fixes the derivative scale and the
   isotropy of the response.
2. **Window sum** integrates over a neighborhood so that no single pixel decides; the
   window is the integration scale and, for Shi and Tomasi, the tracker's support.
3. **Score** reduces $M$ to one number: Harris avoids "the explicit eigenvalue
   decomposition" [p. 150], while the minimum eigenvalue is the tracker's
   worst-direction information.
4. **Relative threshold** adapts to the global contrast of the image, so a single
   high-contrast region can set it for the whole image (worked example D).
5. **Non-maximum suppression** keeps one response per corner. Harris selects 8-way
   local maxima [p. 151]; OpenCV compares the map with its 3×3 dilation, which keeps
   every pixel of a flat plateau [featureselect.cpp L417–L437].
6. **Sorting and greedy spacing** favor strong points and prevent clusters. Shi and
   Tomasi forbade overlapping windows in their experiment [ch. 7]. The greedy order
   means that a strong point can suppress a slightly weaker but better placed one.
7. **Subpixel refinement** (`cornerSubPix`) iterates $q=G^{-1}b$ from the condition that
   the vector from the corner to each nearby point is orthogonal to the gradient there
   [imgproc.hpp L2039–L2081].

## Mathematics, conventions and units

**Conventions.** $I$ is in intensity levels (DN; 0–255 for 8-bit images), $p$ is a
pixel position, $d=(u,v)^T$ a displacement in pixels and
$\nabla I_p=(I_x,I_y)^T$ the gradient in DN/px. The window weights $w_p\ge0$ are a
Gaussian $e^{-(u^2+v^2)/2\sigma^2}$ in Harris [p. 149] and 1 on a
`blockSize`$\times$`blockSize` square in OpenCV.

**From window change to tensor.** Harris [p. 149] expands the change produced by a
shift $d$:

$$E(d)=\sum_p w_p\,[I(p+d)-I(p)]^2\approx\sum_p w_p\,(\nabla I_p^Td)^2=d^TMd,$$

$$M=\sum_p w_p\,\nabla I_p\nabla I_p^T=\begin{pmatrix}A & C\\ C & B\end{pmatrix},\qquad A=\sum_p w_pI_x^2,\ B=\sum_p w_pI_y^2,\ C=\sum_p w_pI_xI_y.$$

$M$ is symmetric positive semidefinite, in DN²/px² times the weight sum. $E$ "is
closely related to the local autocorrelation function, with M describing its shape at
the origin" [p. 149]. Its eigenvalues

$$\lambda_{1,2}=\frac{A+B}{2}\pm\sqrt{\left(\frac{A-B}{2}\right)^2+C^2},\qquad\lambda_1\ge\lambda_2\ge0,$$

are proportional to the principal curvatures of that function [pp. 149–150].

**Harris response.** $R_H=\det M-k(\operatorname{tr}M)^2=\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$,
in DN⁴/px⁴ for a dimensionless $k$. It is positive in the corner region, negative in
the edge regions and small in the flat region, which is identified by
$\operatorname{tr}M$ below a threshold [pp. 150–151]. The paper gives no value for $k$;
OpenCV defaults to 0.04 [imgproc.hpp L2127–L2130] and Schmid et al. used 0.06
[§2.2].

### Worked example A: the sign of $R_H$ depends only on the eigenvalue ratio

Constructed example, recomputed by checks/46-harris-shi-tomasi.py. With
$r=\lambda_2/\lambda_1\in[0,1]$, $R_H=\lambda_1^2\,[\,r-k(1+r)^2\,]$. The sign depends
only on $r$, and the boundary is the smaller root of $kr^2+(2k-1)r+k=0$:

| $k$ | Positive response requires $\lambda_2/\lambda_1>$ | Isotropic corner $\lambda_1=\lambda_2=\lambda$ |
| --- | --- | --- |
| 0.04 (OpenCV default) | 0.0436 | $0.84\,\lambda^2$ |
| 0.06 (Schmid et al.) | 0.0685 | $0.76\,\lambda^2$ |

So $k$ is an anisotropy tolerance: a larger $k$ labels more elongated structures as
edges, and an isotropic corner stays positive only for $k<1/4$. The magnitude still
grows with $\lambda_1^2$, so ranking by $R_H$ mixes shape and contrast. For the matrices
of card CV-CORNERS-001, $R_H(\mathrm{diag}(100,1))=-308.04$ and
$R_H(\mathrm{diag}(20,20))=336$ with $k=0.04$.

**Shi–Tomasi criterion.** For pure translation, the tracker solves $Zd=e$ [eq. 3.10],
where $Z$ is $M$ computed over the tracking window and $e$ collects the image
difference weighted by the gradients. A window is accepted when [eq. 4.1]

$$\min(\lambda_1,\lambda_2)>\lambda,$$

because $Z$ must be "both above the image noise level and well-conditioned"; when the
smaller eigenvalue meets the noise requirement, $Z$ is usually also well conditioned,
since intensities are bounded and so is the larger eigenvalue [ch. 4]. The authors
set $\lambda$ halfway between eigenvalues measured on a uniform region (lower bound)
and on corners and textures (upper bound), and found the value "not critical"
[ch. 4].

### Worked example B: the minimum eigenvalue bounds the worst-direction error

Project derivation under stated assumptions; numbers recomputed by
checks/46-harris-shi-tomasi.py. Assume $J(p)=I(p-d)+n_p$ with independent noise of
variance $\sigma^2$ (DN²), binary weights and an exact linearization. The
least-squares estimate $\hat d=Z^{-1}e$ then has

$$\operatorname{cov}(\hat d)=\sigma^2Z^{-1},\qquad\text{since}\quad\operatorname{cov}\Big(\sum_p\nabla I_p\,n_p\Big)=\sigma^2\sum_p\nabla I_p\nabla I_p^T=\sigma^2Z.$$

The worst-direction standard deviation is $\sigma/\sqrt{\lambda_2}$, so the threshold
of eq. 4.1 bounds it by $\sigma/\sqrt{\lambda}$. With $\sigma=1$ in the units of the
card's matrices, $\mathrm{diag}(100,1)$ gives 0.1 px along its strong direction but
1.0 px along the weak one, while $\mathrm{diag}(20,20)$ gives 0.224 px in every
direction. Shi and Tomasi draw the inverse picture, a "confidence ellipse" whose
half-axes are $\lambda_1$ and $\lambda_2$ [ch. 4, Fig. 4.1].

**Contrast and relative thresholds.** Scaling intensities by $\alpha$ scales the
eigenvalues by $\alpha^2$ [Harris, p. 150], hence $\min(\lambda_1,\lambda_2)$ by
$\alpha^2$ and $R_H$ by $\alpha^4$. OpenCV's `qualityLevel` divides out a global
$\alpha$, but not a contrast difference between regions of the same image.

### Worked example C: OpenCV score units

Constructed example, recomputed by checks/46-harris-shi-tomasi.py. OpenCV multiplies
the Sobel output by $1/(2^{\text{ksize}-1}\cdot\text{blockSize})$, by a further 1/2 for
Scharr and 1/255 for 8-bit input, then sums the products over the block without
normalization [corner.cpp L247–L252, L313–L314]. For an 8-bit image with `ksize=3` and
`blockSize=3`:

- a vertical step of 255 levels gives $A=2/3$, $B=C=0$: $\lambda_1=2/3$, $\lambda_2=0$,
  $R_H=-0.0178$;
- an ideal right-angle corner (bright quadrant $x\ge0$, $y\ge0$) gives at pixel
  $(0,0)$ $A=B=13/36$ and $C=1/9$: $\lambda_1=17/36$, $\lambda_2=1/4$, $R_H=0.0972$.
  That pixel holds the largest $\lambda_2$ of its $5\times5$ neighborhood, so the
  integer detection lies 0.71 px from the geometric corner at $(-0.5,-0.5)$;
- the same image passed as `CV_32F` in $[0,255]$ skips the 1/255 factor and yields
  65,025 times the minimum eigenvalue and $255^4$ times $R_H$.

An absolute threshold copied between an 8-bit and a float pipeline, or between two
`ksize` or `blockSize` settings, therefore changes meaning.

### Worked example D: one relative threshold, two scores

Constructed example, recomputed by checks/46-harris-shi-tomasi.py. An image contains
a calibration target whose corners have 255 levels of contrast and scene corners of
the same shape with 40 levels, and `qualityLevel=0.01`. With the minimum eigenvalue,
scene corners score $(40/255)^2=0.0246$ of the maximum and are kept. With
`useHarrisDetector=true` they score $(40/255)^4=0.0006$ and are all rejected. Against
a 255-level corner, the smallest contrast kept is 25.5 levels for the minimum
eigenvalue ($255\sqrt{q}$) and 80.6 levels for Harris ($255\,q^{1/4}$). Switching the
score without retuning `qualityLevel` changes which regions receive points; masking
the target out of the maximum restores them, because the maximum is computed inside
the mask [featureselect.cpp L415].

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Derivative operator (`gradientSize`) | Harris: $(-1,0,1)$ [p. 149]; Schmid's standard Harris $[-2,-1,0,1,2]$, improved Harris a Gaussian derivative with $\sigma=1$ [§2.2]; OpenCV Sobel 3 by default, Scharr with $-1$ | Derivative scale, noise, isotropy | Anisotropic masks create rotation dependence [§3.3.1]; changes the absolute score scale (example C) |
| Window (`blockSize` or Gaussian $\sigma$) | Harris: Gaussian; Schmid: Gaussian $\sigma=2$; OpenCV box of 3; Shi–Tomasi experiment: $25\times25$ windows [ch. 7] | Integration scale | Larger windows are more stable but merge structures and blur localization; match the tracker's window to keep Shi and Tomasi's argument |
| $k$ (Harris only) | Not given in Harris 1988; OpenCV 0.04; Schmid 0.06 | Anisotropy boundary (example A) | Also changes the ranking among corners |
| `qualityLevel` $q$ | Must be $>0$ [featureselect.cpp L389]; header example 0.01; Schmid: 1% of the maximum | Floor relative to the best score in the mask | Acts on $\alpha^2$ or $\alpha^4$ depending on the score (example D) |
| `minDistance` | Pixels; spacing only if $\ge1$ [L451] | Spread of the points | Greedy; with spacing $d$ at most about $2HW/(\sqrt3\,d^2)$ points fit, so a budget of 500 in $640\times480$ is unreachable beyond 26.6 px |
| `maxCorners` | 0 means no limit | Point budget and downstream cost | The header says `maxCorners <= 0` means no limit [imgproc.hpp L2107], but a negative value fails the assertion of L389 |
| `mask` | `CV_8UC1`, image size | Restricts both the maximum and the candidates [L415, L424–L437] | Masking a high-contrast object changes the threshold elsewhere |
| `cornerSubPix` | `winSize` is a half-size: $(5,5)$ gives $11\times11$; `zeroZone` $(-1,-1)$ disables the dead zone [imgproc.hpp L2039–L2081] | Subpixel position | The window must contain only the corner's own edges |

Tuning approach (project method), on sequences from the deployment domain kept apart
from the final test set:

1. Fix the image contract first: depth, intensity scaling, pyramid level and any
   pre-smoothing, since each changes the scores.
2. Measure the noise floor as Shi and Tomasi did: the score distribution on uniform
   regions from the deployment camera, and on genuine corners. If a relative threshold
   is unstable across frames, add an absolute floor between the two.
3. Choose the window from the image scale and the tracker's window; sweep `blockSize`
   in {3, 5, 7} and `gradientSize` in {3, 5} at a fixed budget.
4. Set `maxCorners` from the downstream budget and `minDistance` from the required
   coverage, below the packing limit above.
5. Judge every setting downstream (survival, coverage, geometry error), never by the
   number of corners (card CV-CORNERS-005).

## Properties and limits of guarantees

- **Rotation.** Both scores are functions of the eigenvalues, hence rotation-invariant
  in the continuous model [Harris, p. 150]. Discrete derivatives break this. With
  Gaussian derivatives, Schmid et al. measured 91% and 89% repeatability at 1.5 px
  for rotations of 38° and 116° [Fig. 7 caption].
- **Contrast and offset.** Scores scale as $\alpha^2$ (minimum eigenvalue) or $\alpha^4$
  (Harris); offsets cancel in the gradients; a relative threshold cancels only a global
  gain.
- **Translation.** The detector commutes with integer image shifts away from the
  border; positions are integers until refined.
- **Scale and viewpoint.** No invariance: repeatability fell to 54% for a 1.5 scale
  change and 1% for 4.1 at 1.5 px tolerance [Schmid 2000, §3.3.3, Fig. 11 caption].
- **Localization.** For an ideal corner, the integer maximum is offset from the
  geometric corner (example C); `cornerSubPix` refines it under its gradient
  orthogonality model.
- **Optimality.** Shi and Tomasi call their criterion "optimal by construction"
  [abstract, ch. 4], relative to their tracker's translation model and window. It
  guarantees neither a world point [ch. 5] nor persistence; they detect bad features
  afterwards by affine dissimilarity [ch. 5] and note that "rigidity is not a local
  feature" [ch. 8].
- **Distinctiveness.** Neither score compares a patch with other image locations, so
  neither predicts match ambiguity; Schmid et al. measure distinctiveness separately
  as the information content of local descriptors [§4].

## Cost and implementation

Cost drivers, with $H\times W$ pixels, derivative size $s$, window size $b$, $N_c$
candidates and $N$ kept points:

- gradients: two separable convolutions, $O(HWs)$;
- products and window sums: three box sums, $O(HW)$ per channel when computed with
  running sums, otherwise $O(HWb^2)$;
- score: a few multiply-adds per pixel for Harris, plus one square root for the
  minimum eigenvalue, the cost Harris avoided [p. 150];
- non-maximum suppression: one 3×3 dilation, $O(HW)$;
- selection: sorting, $O(N_c\log N_c)$, then greedy spacing on a grid of cells of size
  `round(minDistance)`, where each candidate checks the 3×3 neighboring cells
  [featureselect.cpp L451–L527].

The dense passes dominate unless $N_c$ approaches $HW$.

### OpenCV 4.13 contracts

Read in the 4.13.0 headers and sources on GitHub, because docs.opencv.org returned
HTTP 403 during this pass. No code was executed for this note.

- `cornerMinEigenVal(src, dst, blockSize, ksize=3, borderType)` and
  `cornerHarris(src, dst, blockSize, ksize, k, borderType)` return a `CV_32FC1` map of
  the input size; `BORDER_WRAP` is not supported [imgproc.hpp L1943–L1981]. Both
  call `cornerEigenValsVecs`, which scales derivatives, builds $(A,C,B)$, applies an
  unnormalized box filter and evaluates the score [corner.cpp L237–L321; formulas
  L52–L155]. `cornerHarris` may run an IPP path for `ksize` 3 or 5, and UMat inputs
  run OpenCL [corner.cpp L637–L651]; results can differ slightly between back ends
  (project deduction).
- `goodFeaturesToTrack` asserts `qualityLevel > 0`, `minDistance >= 0` and
  `maxCorners >= 0` [featureselect.cpp L389]. It keeps scores strictly above
  `qualityLevel` times the masked maximum (`THRESH_TOZERO`) [L414–L416;
  imgproc.hpp L329], applies 3×3 dilation equality [L417], skips the 1-pixel border
  [L424–L437], sorts deterministically [L55–L60, L449], spaces points with a strict
  `<` test [L451–L527] and returns `CV_32F` coordinates [L544–L547]. An OpenVX Harris
  path exists but is "disabled due to bad accuracy" [L404–L407].
- The header documents that raising `qualityLevel` returns a prefix of the list
  obtained with a lower value [imgproc.hpp L2100–L2102]: the candidates are sorted, and
  a higher threshold removes only a suffix.
- `calcOpticalFlowPyrLK` defaults to $21\times21$ windows, 3 pyramid levels and
  `minEigThreshold=1e-4`, applied to the minimum eigenvalue of the spatial gradient
  matrix divided by the number of window pixels [video/tracking.hpp L134–L186].

## Evaluation and controlled variation

### Protocols

- **Repeatability of the detector** [Schmid 2000, §3.1]. Use planar scenes with a
  known homography $H_{1i}$, keep only points in the common region, and count a point
  as repeated when a detection lies within $\varepsilon$ of its projection. The rate
  is $r_i(\varepsilon)=|R_i(\varepsilon)|/\min(n_1,n_i)$, where $n_1$ and $n_i$ count
  the points in the common region. With points about 10 px apart, a tolerance of
  1.5 px makes accidental repeats unlikely [§3.3].
- **Tracking quality**: survival after $k$ frames, track length, endpoint error
  against ground truth (synthetic warps or annotated tracks), forward–backward error,
  spatial coverage, and downstream geometry error on held-out points. Shi and Tomasi
  monitor each feature with its affine dissimilarity to the first frame [ch. 5].
- **Published reference points.** On their "Van Gogh" scene, Schmid et al. report for
  improved Harris 610, 595 and 586 points with 91% and 89% repeatability under
  rotation [Fig. 7 caption], and 54% and 1% under scale changes of 1.5 and 4.1
  [Fig. 11 caption], both at $\varepsilon=1.5$ px. These numbers belong to their
  implementation (Gaussian derivatives, $k=0.06$) and scenes, not to OpenCV.

### Proposed baseline and controlled variation (not executed)

- **Question**: does enforcing spatial coverage at a fixed budget improve downstream
  geometry, at the cost of weaker points?
- **Data**: held-out sequences from the deployment domain with ground-truth motion or
  homographies, including low-texture areas, a high-contrast object and motion blur.
- **Baseline**: `goodFeaturesToTrack` with the minimum eigenvalue, `blockSize=3`,
  `gradientSize=3`, `qualityLevel=0.01`, `minDistance=10`, `maxCorners=400`, then
  `calcOpticalFlowPyrLK` with its defaults.
- **Controlled variation**: the same score map, threshold and total budget, but
  candidates chosen as the strongest in each cell of an $8\times6$ grid, at most 9 per
  cell (implemented from the quality-returning overload with `maxCorners=0`).
- **Measurements**: survival at 10 and 30 frames; forward–backward error; endpoint
  error; fraction of grid cells with at least one surviving point; homography or pose
  error and RANSAC inlier ratio; the score distribution of the selected points.
- **Expected effect (hypothesis)**: weaker median scores and slightly larger per-point
  error, but better-conditioned geometry when texture is uneven.
- **Confound**: per-cell selection admits weaker points; the recorded score
  distribution separates "worse points" from "better placement".

**Measurement limits.** Repeatability needs a known transformation, which planar
scenes provide; 3-D scenes add occlusion. Tracking metrics depend on the tracker and
its window, so a detector comparison holds only for one tracker configuration.
Survivor-only errors reward excessive rejection (card CV-CORNERS-005).

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Points cluster on one textured patch; pose or homography poorly constrained | Relative threshold and greedy ranking favor the strongest region | Coverage map; geometry error with points removed region by region | Per-cell quotas, mask, or a local threshold (proposed variation) |
| Almost no points in low-contrast areas while a bright target is visible | Maximum set by the target (example D), worse with Harris | Score histogram per region; rerun with the target masked | Mask the target from the maximum, use the minimum eigenvalue, per-cell selection |
| Tracks slide along edges | Weak direction at the tracker's window | Minimum eigenvalue recomputed over the tracker's window | Select with the tracker's window; raise `minEigThreshold` |
| Tracks drift on junctions, highlights or occlusion boundaries | Image corners that are not world points [Shi–Tomasi, ch. 5] | Growth of affine dissimilarity or forward–backward error | Monitor and drop features; robust geometry (RANSAC) downstream |
| Strong corners, wrong matches on a repeated grid | Global ambiguity, not detection failure | Repeatability and match identity measured separately (card CV-CORNERS-004) | Distinctive cues, geometric constraints, motion priors |
| Repeatability drops after zoom | Single-scale detector | Repeatability against scale factor on a planar target | Detect per pyramid level, or use [SIFT](41-sift.md) or [ORB](42-orb.md) |
| Repeatability depends on rotation angle, worst near 45° | Anisotropic derivative masks | Rotate a synthetic image and plot repeatability against angle | Scharr or Gaussian derivatives |
| An absolute threshold works on one pipeline and not on another | Score units (example C): depth, `ksize`, `blockSize`, contrast | Compare the score maximum on the same image in both pipelines | Relative threshold, or normalize the input and fix the operators |
| Corners in dark or noisy frames | Noise eigenvalues above the threshold | Score distribution on a flat-field capture | Absolute floor from that capture; denoise; longer exposure |
| Fewer points than `maxCorners` | Spacing and threshold constraints, not an error | Count candidates before spacing (overload with scores) | Lower `minDistance` or `qualityLevel` only if downstream metrics improve |

## Alternatives and applications

Conditional choices:

- **Prefer the minimum eigenvalue (Shi–Tomasi)** when points feed a translation
  Lucas–Kanade tracker: the score is the tracker's worst-direction information.
- **Prefer the Harris response** for a cheap ranking without a square root, or to
  reproduce ORB or older literature; retune $k$ and `qualityLevel`.
- **Prefer [FAST](47-fast-brief.md)** when the per-pixel budget is tight; rank its
  candidates with Harris as [ORB](42-orb.md) does.
- **Prefer a scale-space detector with a descriptor** ([SIFT](41-sift.md),
  [ORB](42-orb.md)) for matching across zoom, rotation or a wide baseline rather than
  tracking small inter-frame motion; see [CV-MATCHING](43-detecteurs-matchers.md).
- **Prefer learned matching** ([CV-MATCH-APPRIS](44-superpoint-lightglue-loftr.md))
  under strong illumination or modality changes, validated on the target domain.
- **Prefer direct registration** ([CV-ECC](45-recalage-ecc.md)) or
  [optical flow](../../100-mouvement-video/references/101-flot-optique.md) when a region
  has gradients but few corners.

Industrial uses (project reasoning, not published results): the front end of visual
odometry on an embedded CPU ([CV-VIO](../../60-vision-3d/references/63-slam-vio.md)),
where Shi–Tomasi plus pyramidal Lucas–Kanade is cheap and its points are spread by
quotas; video stabilization; displacement monitoring of structures or conveyors from
painted markers; and subpixel refinement of calibration-target corners with
`cornerSubPix` ([CV-ZHANG](../../50-calibration-geometrie/references/52-calibration-zhang.md)).

## Guided reasoning and proposed checks

These constructed cases develop the structure tensor, observable directions and
repeatability. They explain or test reasoning; no image, video or hardware result is
claimed as measured. The method properties remain tied to the sources below.

### Case linked to CV-CORNERS-001

**Working question**: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?

**Reference answer**: The second: its smallest eigenvalue is 20 instead of 1. Both directions are constrained; the first one behaves like an edge, even though its total gradient is stronger.

**Interpretation of directions**: With the first matrix, a shift in the direction associated with the value 1 changes the patch little. The large value 100 does not compensate for this weak direction. With the second, a unit displacement in any direction produces the same quadratic change, 20.

**Proposed use**: Before Lucas–Kanade tracking, examine the smallest eigenvalue, which is the weakest constraint, and the spatial distribution of the points. A set of well-conditioned corners grouped in a small area does not guarantee a stable global registration. The numbers assume the local model of small translations and the same gradient units; matrices computed with different normalizations cannot be compared without aligning them.

### Case linked to CV-CORNERS-005

**Working question**: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?

**Reference answer**: Measure survival, displacement error, spatial coverage and geometry error with comparable budget and resolution. A setting that produces more points can add noisy or redundant points.

**Example of comparison**: One hundred corners on a single textured patch can be redundant and leave the useful part of the object without observations. Fifty well-distributed points can better constrain the motion to be estimated, but only if they are tracked reliably. The count describes neither this coverage nor how long the points remain visible.

**Constructed protocol**: Set the resolution, total budget and tracking criteria, then vary the selection score and the spatial quotas separately. Measure errors on annotated point trajectories or on independent geometry, also counting lost points. A low photometric residual can be misleading on repeated patterns. Report performance under blur, low texture and occlusion, with the same rejection rules for all settings.

**Documentation consulted in that pass**: [OpenCV 4.13, Harris Corner Detection](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), theory, local matrix and eigenvalues (not re-read in the 2026-11-14 pass: HTTP 403). The other developments are in the [flashcards](../46-harris-shi-tomasi.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-CORNERS-001

**Situation**: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?

**Deriving the local tensor**: for a small displacement $d$, $I(p+d)-I(p)\approx\nabla I(p)^Td$. The weighted sum of these squared differences gives $d^T(\sum_p w_p\nabla I_p\nabla I_p^T)d$, hence $M$. Contours of constant error are ellipses whose major axis lies along the direction in which the image changes little. If the photometric noise is independent with equal variance and the problem is well posed, the local displacement uncertainty is proportional to $M^{-1}$. A small eigenvalue then means a large uncertainty in that direction; this links the eigenvalues to trackability under these assumptions, not to future visibility.

### CV-CORNERS-002

**Situation**: How do Harris and Shi–Tomasi differ in corner selection, and can the same numerical threshold be retained?

**Do not confuse score and model**: Harris can compute the determinant and trace directly without diagonalizing $M$; Shi–Tomasi evaluates the smallest eigenvalue, $(\operatorname{tr}M-\sqrt{(M_{11}-M_{22})^2+4M_{12}^2})/2$ for a symmetric $2\times2$ matrix. These are two summaries of the same tensor; neither is evidence of the point's identity. In the isotropic case $\lambda_1=\lambda_2=\lambda$, Harris gives $(1-4k)\lambda^2$ while Shi–Tomasi gives $\lambda$. Their behavior under changes of contrast and patch scale therefore differs even when the visual ranking of the best corners looks similar. Non-maximum suppression and spacing are separate steps, outside these formulas.

### CV-CORNERS-003

**Situation**: In OpenCV 4.13 goodFeaturesToTrack, how do qualityLevel, minDistance and maxCorners differ?

**Read the selection as a sequence of filters**: first compute the quality map, keep the local maxima, remove insufficient scores, then visit the candidates in descending order while enforcing the minimum distance and the budget. The quota therefore does not replace a quality threshold. In a constructed case where the only good points are close together, increasing the spacing can reject many of them and return fewer points than requested; this is not an API failure. To limit concentration, a region-of-interest mask or per-region quotas are system choices to compare, keeping the same score definition and the same distance units.

### CV-CORNERS-004

**Situation**: Strong corners on a repetitive grid still produce a poor homography. Which checks distinguish detection failure from incorrect association?

**Distinguish local from global observation**: $M$ describes the curvature of a small-translation cost around a given patch. It does not compare this patch with all other patches in an image. A grid can therefore give a strong curvature around each intersection while producing several distant minima for matching between images. A known initial displacement can make local tracking possible without solving the global identification of the correct grid cell. To evaluate the detector alone, use a reference transformation and check the distance to the projected position; for matching, then examine which identity is selected among the candidates. The two rates do not share a denominator.

### CV-CORNERS-005

**Situation**: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?

**Constructed forward–backward check**: Tracking $p_t$ to $\hat p_{t+1}$, then tracking the latter back to $\hat p_t$, gives a cycle error $e_{FB}=\|\hat p_t-p_t\|_2$ in pixels. A large error signals a useful inconsistency to reject; a small error can also come from the same wrong pattern found in both directions. It therefore complements a displacement reference rather than replacing it. Compare the fraction of valid points while keeping occlusions in the tally. If a setting rejects almost all difficult points, its mean error on survivors can drop while the registration becomes less available. Tracking reliability and the rejection policy must be evaluated together.

**Passages consulted for these developments**: [OpenCV 4.13, Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), theory, tensor and response; [OpenCV 4.13, Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html), theory and goodFeaturesToTrack selection (both not re-read in the 2026-11-14 pass: HTTP 403).

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-CORNERS-001 — The error ellipse gives a quantitative comparison

With equal unit photometric noise in the local linearized model, $M^{-1}$ for the first window is $\operatorname{diag}(0.01,1)$ and for the second is $\operatorname{diag}(0.05,0.05)$. The second window has a much smaller worst-direction variance despite lower total gradient energy. This constructed calculation explains choosing by the weakest direction. It assumes a shared local displacement and does not establish robustness to occlusion or an incorrect brightness model.

### CV-CORNERS-002 — Contrast scaling changes the response power

If all intensities are multiplied by $\alpha$, gradients scale by $\alpha$ and tensor eigenvalues by $\alpha^2$. Shi–Tomasi then scales by $\alpha^2$, whereas Harris scales by $\alpha^4$. A fixed absolute threshold therefore changes its meaning with intensity units, and the two scores cannot share a numerical threshold. Relative-to-maximum selection can cancel a uniform scale, but clipping and spatially varying illumination do not preserve this ideal relation.

### CV-CORNERS-004 — Repeatability and identity need separate denominators

Given a known image transformation, first count whether a detected point has a nearby detected counterpart in the visible transformed region. Then, among described points, measure whether matching chooses that counterpart rather than a repeated intersection. This proposed decomposition separates missed detections from wrong identities. Exclude points truly outside shared visibility from repeatability denominators, and report exclusions so a method cannot appear robust simply by discarding difficult regions.

### CV-CORNERS-005 — Survivor-only error can reward excessive rejection

Constructed comparison: method A retains 90 of 100 points with 1 px mean error; method B retains 10 with 0.5 px mean error. B has better conditional error but may fail to support the required geometry. Report survival and spatial coverage jointly with error, and count whether a valid transform is available. Forward/backward consistency is useful evidence, but repeated texture can generate a consistent wrong cycle in both directions.

Consulted foundations: [OpenCV Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html): structure tensor, eigenvalue interpretation and Harris response; [OpenCV 4.13.0 `imgproc.hpp`, `goodFeaturesToTrack`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L2083-L2135): quality and spacing contract (the earlier link pointed to the video tracking group, which does not document this function).

## Sources and flashcards

### Scientific sources

- [Harris and Stephens 1988, A combined corner and edge detector](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf), Alvey Vision Conference, doi:10.5244/C.2.23: introduction and edge-tracking problem (pp. 147–148); "Moravec revisited" and "Auto-correlation detector" (p. 149: three cases, analytic expansion, Gaussian window, matrix $M$); eigenvalues, contrast factor and "Corner/edge response function" (p. 150); 8-way local maxima (p. 151).
- [Shi and Tomasi, Good Features to Track, Cornell TR 93-1399 (1993)](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf), technical-report version of the CVPR 1994 paper: abstract; ch. 1 (poor features: depth junctions, reflections); ch. 2 (eq. 2.1); ch. 3 (eqs. 3.1–3.10); ch. 4 (aperture problem, eq. 4.1, threshold choice, confidence ellipse, Figs. 4.1–4.2); ch. 5 (dissimilarity, twig junction); ch. 7 (non-overlapping $25\times25$ windows, aliasing); ch. 8 (conclusion).
- [Schmid, Mohr and Bauckhage 2000, Evaluation of interest point detectors](https://inria.hal.science/inria-00548302v1), IJCV 37(2): §2.2 (Harris implementations, $k=0.06$, 1% threshold), §3.1 (repeatability rate), §3.3 and §3.3.1 (tolerance, derivative masks), §3.3.2 (rotation, Fig. 7 caption), §3.3.3 (scale change, Fig. 11 caption), §3.4 and §4 (information content).

### Implementation sources

- [OpenCV 4.13.0, `modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1943-L2167): `cornerMinEigenVal` and `cornerHarris` (L1943–L1981), `cornerEigenValsAndVecs` (L1983–L2011), `cornerSubPix` (L2039–L2081), `goodFeaturesToTrack` (L2083–L2167); `THRESH_TOZERO` (L329).
- [OpenCV 4.13.0, `modules/imgproc/src/corner.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/corner.cpp#L237-L321): score formulas (L52–L155), derivative scaling, input types and box filter (L237–L321), IPP and OpenCL paths (L550–L572, L634–L654).
- [OpenCV 4.13.0, `modules/imgproc/src/featureselect.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/featureselect.cpp#L382-L547): deterministic comparator (L55–L60), CPU path of `goodFeaturesToTrack` (L382–L547).
- [OpenCV 4.13.0, `modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp#L134-L186): `calcOpticalFlowPyrLK` defaults and `minEigThreshold`.
- [OpenCV 4.13.0, `modules/core/include/opencv2/core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp#L337-L341): `BORDER_DEFAULT` is `BORDER_REFLECT_101`.
- [OpenCV 4.13 tutorials, Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) and [Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html): retained links, not re-read in this pass (HTTP 403).

### Related flashcards and references

- [Flashcards](../46-harris-shi-tomasi.md): CV-CORNERS-001 to 005.
- Sibling methods: [CV-FAST-BRIEF](47-fast-brief.md), [CV-ORB](42-orb.md), [CV-SIFT](41-sift.md), [CV-MATCHING](43-detecteurs-matchers.md); tracking: [CV-FLOT](../../100-mouvement-video/references/101-flot-optique.md).

Drafted by Agent Codex, 2026-10-24. Revision 7, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/46-harris-shi-tomasi.md).
