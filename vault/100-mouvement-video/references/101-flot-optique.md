---
id: CV-FLOT
type: methode
domaine: d10
poles: [B, C, D]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-MATCHING"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Optical flow: Lucas–Kanade, Farnebäck and RAFT

This is the method note for two-frame optical flow. It develops the differential
local method of Lucas and Kanade in its pyramidal form, which is the sparse point
tracker of most classical pipelines, and RAFT, a learned dense estimator built on an
all-pairs correlation volume. Farnebäck's polynomial-expansion method is the dense
classical baseline; its mechanism lives in [CV-FARNEBACK](103-farneback.md) and is
only compared here. Multi-frame point tracking and video understanding are in
[CV-VIDEO](102-points-actions-video.md).

## Problem and data contract

**Task.** Given two images $I_1$ and $I_2$ of the same scene, find for a pixel
$\mathbf x=(x,y)$ of $I_1$ the displacement $\mathbf d=(u,v)$ such that $\mathbf x+\mathbf d$
in $I_2$ shows the same surface point. *Sparse* flow answers for a list of points,
*dense* flow for every pixel of $I_1$. Optical flow is apparent 2-D motion in the
image: it mixes object motion, camera motion and depth, and carries no object
identity.

**Data contract.**

- *Coordinates.* Pixels with the origin at the top-left pixel, $x$ to the right and
  $y$ downwards; Bouguet's report places the upper-left pixel at $[0\ 0]^T$ and pixel
  values at integer coordinates [Bouguet, §1]. A flow vector is in pixels **per frame
  pair**, on the grid of the image it is attached to.
- *Direction.* Forward flow $F_{12}$ lives on the grid of $I_1$ and points into $I_2$.
  The backward flow $F_{21}$ lives on the grid of $I_2$; it is not $-F_{12}$ evaluated
  at the same index (see CV-FLOT-004 below).
- *Sparse output, OpenCV 4.13 `calcOpticalFlowPyrLK`.* Inputs are two 8-bit images
  of equal size and type (or pyramids), `prevPts` as single-precision $(x,y)$
  coordinates; outputs are `nextPts` (same type), a `status` byte per point (1 if
  "the flow for the corresponding features has been found") and an `err` value
  [tracking.hpp, L134–L186]. The displacement is `nextPts - prevPts`.
- *Dense output.* An $H\times W\times2$ float array; in OpenCV the first channel is
  $u$ (horizontal) and the second $v$ (vertical) [tracking.hpp, L488–L505]. RAFT maps
  each pixel of $I_1$ to $\mathbf x+\mathbf f(\mathbf x)$ in $I_2$ [RAFT, §3; the paper's
  sentence says "in $I_2$" twice, the code defines the flow on the $I_1$ grid as
  `coords1 - coords0`, raft.py L63–L70].
- *Photometry and time.* Methods compare intensities or learned features, so gain,
  exposure, compression and color conversion are part of the input contract. The
  time between the frames converts pixels per pair into pixels per second only with
  the actual timestamps of that pair ([CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md)).

**Role in a pipeline.** Sparse flow feeds feature tracks to visual odometry,
stabilization, homography or essential-matrix estimation, and speed measurement;
dense flow feeds motion segmentation, frame interpolation, warping-based checks and
temporal consistency. Downstream stages expect three things the estimator does not
guarantee: that each vector refers to the same surface point, that its validity is
known, and that it is expressed on the grid and time base they assume.

## Intuition

Lucas–Kanade asks: by how much must I shift a small window of $I_2$ so that it
matches the window of $I_1$ around my point? If the window's intensities have
gradients in two directions, the shift is determined; if they vary along one
direction only, as on a straight edge, only the shift across the edge is. A first-order
estimate is refined by re-sampling $I_2$ at the shifted position and repeating, and
a pyramid solves the problem first on blurred, downsampled images where a large
motion looks small.

RAFT asks the same question for every pixel with learned features: it compares each
feature of $I_1$ with every feature of $I_2$ once, then lets a recurrent unit
repeatedly look up the similarities around the current guess and propose a
correction. The comparison is computed once; the refinement is iterative.

*Illustration (constructed).* A camera pans over a brick wall while a person walks.
On brick corners, LK locks on; on a horizontal mortar line it can only measure the
vertical shift; on the periodic bricks it may jump by one brick if the pan exceeds
half a brick per frame (worked example B). RAFT gives a vector everywhere, including
where the person uncovers wall that was not visible in $I_1$; there the vector is an
inference, not an observation.

```mermaid
flowchart TB
    subgraph LK["Pyramidal Lucas–Kanade, per point"]
        A1["Pyramids of I1 and I2"] --> A2["Coarsest level: guess g = 0"]
        A2 --> A3["Gradient matrix G from I1 window"]
        A3 --> A4["Iterate: sample I2 at x + g + nu, solve G eta = b"]
        A4 --> A5["Propagate 2 (g + d) to the finer level"]
        A5 -->|"finer level exists"| A3
        A5 -->|"level 0"| A6["nextPt, status, err"]
    end
    subgraph RAFT["RAFT, all pixels at 1/8 resolution"]
        B1["Feature and context encoders"] --> B2["All-pairs correlation, 4 pooled levels"]
        B2 --> B3["Lookup around x + f_k"]
        B3 --> B4["ConvGRU update: f_k+1 = f_k + delta f"]
        B4 -->|"next iteration"| B3
        B4 --> B5["Convex 8x upsampling to H x W x 2"]
    end
```

*Diagram: data flow of the two methods, synthesized from Bouguet §2.4 and RAFT
§§3.1–3.3. LK repeats its solve per pyramid level; RAFT repeats lookups on one
precomputed volume.*

## Prerequisites and competencies

**Required prerequisites**: [CV-MATCHING](../../40-features-matching/references/43-detecteurs-matchers.md).
Useful background, by mechanism:

- image gradients and smoothing: [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md);
- the structure tensor and point selection by minimum eigenvalue: [CV-CORNERS](../../40-features-matching/references/46-harris-shi-tomasi.md);
- linear least squares, normal equations and conditioning: [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md);
- parametric intensity alignment, of which translational LK is the simplest case: [CV-ECC](../../40-features-matching/references/45-recalage-ecc.md);
- timestamps and rolling shutter when converting to speeds: [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md).

**Target competencies**: explain the brightness-constancy constraint and the LK
normal equations; apply the pyramid and its limits; compare LK, Farnebäck and RAFT
under constraints; interpret EPE and outlier rates under their protocol; diagnose
aperture, occlusion, large-motion and convention failures.

## Assumptions, observability and degenerate cases

- **Brightness (or feature) constancy.** The matched surface point has the same
  intensity in both images; LK minimizes a sum of squared differences that only
  makes sense under it [Bouguet, eq. 1]. Illumination changes, specularities,
  exposure changes and motion blur violate it; MPI-Sintel's "Final" pass adds such
  effects to the "Clean" pass on identical motion [Butler et al., §4].
- **Small residual motion.** The first-order Taylor expansion requires the displacement
  "to be small enough that this approximation is adequate" [Lucas and Kanade, §4.1].
  For a sinusoid, iteration converges for initial misregistrations up to half a
  wavelength [§4.3]; smoothing extends the range at the cost of accuracy, and a
  smoothing window much larger than the object can suppress it entirely [§4.3].
- **Coherent motion over the window.** All pixels of the window share one translation.
  A window straddling a motion boundary mixes two motions; Bouguet notes that small
  windows are preferable "at occluding areas" for this reason [§2].
- **Texture in two directions.** The solve needs an invertible gradient matrix, which
  "is equivalent to saying that the image ... contains gradient information in both
  $x$ and $y$ directions" [Bouguet, §2.3]. This is the aperture problem in matrix form.
- **Visibility.** The point must be visible in both images. Sintel reports that "nearly
  8.5%" of its pixels are seen in one image of a pair but not the other [Butler et al.,
  §4]; no vector exists for them in the physical sense.
- **For RAFT, additionally:** the test pair resembles the training distribution
  (synthetic FlyingChairs and FlyingThings, then dataset-specific fine-tuning
  [RAFT, §4]); motion is resolved at 1/8 resolution before learned upsampling
  [§3.3].

Degenerate cases: a flat window ($G\approx0$) gives no estimate; an edge gives rank 1
(worked example A); a periodic texture has several equally good minima (worked
example B); a point leaving the image has no match; a transparent or reflective surface
carries two motions in one window.

## Procedure

### Pyramidal Lucas–Kanade (Bouguet's formulation, used by OpenCV)

```text
build pyramids I^0..I^Lm and J^0..J^Lm             # pyrDown-style 5-tap low-pass, halve size
g <- (0, 0)                                        # guess at the coarsest level
for L = Lm down to 0:
    p <- u / 2^L                                   # point position at level L
    compute Ix, Iy on the window of I^L around p   # once per level
    G <- sum [Ix^2, IxIy; IxIy, Iy^2]              # 2x2 gradient (structure) matrix
    if min eigenvalue of G too small: mark untrackable at this level
    nu <- (0, 0)
    repeat up to K times:
        dI <- I^L(x) - J^L(x + g + nu)             # bilinear sampling, sub-pixel
        b  <- sum [dI Ix, dI Iy]
        eta <- G^-1 b ; nu <- nu + eta
        stop when |eta| < epsilon
    g <- 2 (g + nu)                                # initial guess for level L-1
d <- g / 2 ; v <- u + d                             # final displacement at level 0
```

Purpose of the steps. *Pyramids* make a large displacement small at coarse levels
so the linearization holds; each level only refines a residual [Bouguet, §2.2].
*Gradients and $G$ from $I_1$ only* make $G$ constant during iterations, so only the
mismatch vector $b_k$ is recomputed [§2.3]; Baker and Matthews later generalize this
constant-Hessian idea as the inverse compositional algorithm [Baker and Matthews,
§3.2]. *Iteration* is a Newton–Raphson (Gauss–Newton) correction of the first-order
step [Lucas and Kanade, §4.1; Bouguet, §2.3]. *Bilinear sampling* keeps sub-pixel
accuracy [Bouguet, §2.5]. *Declaring a point lost* covers leaving the image and
excessive patch change; Bouguet notes that a residual threshold is hard to set and
that pairwise tracking drifts over long sequences [§2.7]. Points are usually selected
where the minimum eigenvalue of $G$ is large, which is the Shi–Tomasi criterion
[§3; [CV-CORNERS](../../40-features-matching/references/46-harris-shi-tomasi.md)].

### RAFT

1. **Encode.** A shared encoder maps each image to features at 1/8 resolution with
   $D=256$ channels; a context encoder of the same architecture sees $I_1$ only
   [RAFT, §3.1].
2. **Correlate once.** All pairs of feature vectors are dotted into a 4-D volume
   (eq. 1), whose last two dimensions are average-pooled with kernels 1, 2, 4, 8 into a
   4-level pyramid; the $I_1$ dimensions keep full 1/8 resolution "to recover the
   motions of small fast-moving objects" [§3.2].
3. **Look up.** Around the current correspondence $\mathbf x+\mathbf f_k$, correlation
   values are bilinearly sampled within radius $r$ on every level and concatenated [§3.2].
4. **Update.** A convolutional GRU with tied weights takes correlation, flow and
   context features and outputs $\Delta\mathbf f$; $\mathbf f_{k+1}=\mathbf f_k+\Delta\mathbf f$,
   starting from $\mathbf f_0=0$ or from a forward-projected previous flow ("warm
   start") [§3.3].
5. **Upsample.** Each full-resolution vector is a learned convex combination of its
   $3\times3$ coarse neighbors [§3.3].

| | Pyramidal LK | Farnebäck ([CV-FARNEBACK](103-farneback.md)) | RAFT |
| --- | --- | --- | --- |
| Output | Sparse: chosen points | Dense | Dense |
| Local model | Constant intensity, translation of a window | Quadratic polynomial per neighborhood | Learned feature similarity |
| Large motion | Image pyramid, coarse to fine | Image pyramid | All-pairs volume pooled to 4 levels; single resolution for $I_1$ |
| Refinement | Gauss–Newton iterations per level | Iterations per level | Learned recurrent updates (12 in training) |
| Validity signal | `status`, `err`, minimum eigenvalue | None built in | None built in |
| Compute | CPU, per point | CPU, per pixel | GPU, memory quadratic in pixel count (precomputed volume) |

## Mathematics, conventions and units

**Brightness constancy.** With $I(x,y,t)$ in grey levels and $t$ in frames, constancy
$I(x+u,y+v,t+1)=I(x,y,t)$ linearized to first order gives

$$I_x u + I_y v + I_t \approx 0,$$

with $I_x,I_y$ in grey levels per pixel, $I_t$ in grey levels per frame and $(u,v)$ in
pixels per frame [OpenCV tutorial, "Optical Flow"]. One scalar equation per pixel
constrains only the flow component along $\nabla I$: the *normal flow*
$-I_t/\|\nabla I\|$. The tangential component is free.

**Lucas–Kanade normal equations.** Over a window $\mathcal W$ of $N$ pixels, with $A$
the first image, $B$ the second image pre-shifted by the current guess and
$\delta I=A-B$, minimizing $\sum_{\mathcal W}(A(\mathbf x)-B(\mathbf x+\boldsymbol\nu))^2$
after linearization gives [Bouguet, eqs. 13–25]

$$G\,\boldsymbol\nu=\mathbf b,\qquad
G=\sum_{\mathcal W}\begin{pmatrix}I_x^2 & I_xI_y\\ I_xI_y & I_y^2\end{pmatrix},\qquad
\mathbf b=\sum_{\mathcal W}\delta I\begin{pmatrix}I_x\\ I_y\end{pmatrix}.$$

$G$ is in (grey level/px)$^2$ summed over $N$ pixels and $\mathbf b$ in grey level$^2$/px,
so $\boldsymbol\nu$ is in pixels. Lucas and Kanade derive the same least-squares form
in $n$ dimensions and note that the 2-D case accumulates five products
[§4.5]; they also extend it to an affine warp [§4.6]. Their 1-D estimate weights each
pixel by $w(x)=1/|G'(x)-F'(x)|$ to down-weight places where the linear approximation is
poor [§4.1, eq. 5].

*Eigenvalues and uncertainty (derivation).* If $\delta I=\nabla I^T\boldsymbol\nu+n$
with independent noise of variance $\sigma^2$ and noise-free gradients, the
least-squares estimate has covariance $\sigma^2G^{-1}$. The eigenvector of the
smaller eigenvalue $\lambda_{\min}$ is the direction of largest uncertainty, with
standard deviation $\sigma/\sqrt{\lambda_{\min}}$. An edge gives $\lambda_{\min}=0$:
infinite uncertainty along the edge.

*Pyramid.* At level $L$ the point is $\mathbf u/2^L$; the guess propagates as
$\mathbf g^{L-1}=2(\mathbf g^L+\mathbf d^L)$ and the final flow is
$\mathbf d=\sum_L 2^L\mathbf d^L$ [Bouguet, eqs. 5–10]. If each level handles
$d_{\max}$, the pyramid handles $(2^{L_m+1}-1)\,d_{\max}$, a gain of 15 for $L_m=3$
[§2.2]. This is an upper bound under the assumption that every level converges.

**RAFT.** With $g_\theta(I)\in\mathbb R^{H\times W\times D}$ the features at 1/8 resolution,
the correlation volume is $C_{ijkl}=\sum_h g_\theta(I_1)_{ijh}\,g_\theta(I_2)_{klh}$
[eq. 1]; the official code divides it by $\sqrt D$ (corr.py L53–L60). The
lookup grid of the paper is $\mathcal N(\mathbf x')_r=\{\mathbf x'+\mathbf{dx}\mid
\mathbf{dx}\in\mathbb Z^2,\|\mathbf{dx}\|_1\le r\}$, sampled at $\mathbf x'/2^k$ on level
$k$ [eq. 2]. The GRU follows eqs. 3–6. Training minimizes
$\sum_{i=1}^N\gamma^{N-i}\|\mathbf f_{gt}-\mathbf f_i\|_1$ with $\gamma=0.8$ [eq. 7], so
later iterations weigh more. Flow is in full-resolution pixels after upsampling; at
1/8 resolution one cell is 8 px, which is why the code multiplies the coarse flow by 8
before the convex combination (raft.py L72–L84).

### Worked example A: one linearized step versus iterations

Constructed example, recomputed by checks/101-flot-optique.py. $I_1$ is a smooth blob
plus a ramp, $I_2$ is $I_1$ translated by $\mathbf d$ and sampled exactly; the window is
$7\times7$ and gradients are central differences.

- The window has $\lambda_{\min}/N\approx148$ and $\lambda_{\max}/N\approx315$
  (grey level/px)$^2$: both directions are observable.
- For $\mathbf d=(1.5,-0.8)$ px the single first-order step misses by 0.11 px; three
  iterations reduce the error below 0.001 px. For $\mathbf d=(3,1)$ px the first step
  misses by 0.52 px and four iterations converge.
- Replacing $I_1$ by an intensity that varies along $x$ only gives
  $\lambda_{\min}=\det G=0$: the $y$ component is unobservable whatever the number of
  iterations.

### Worked example B: periodic texture and the pyramid

Constructed example, recomputed by checks/101-flot-optique.py, after Lucas and Kanade
§4.3. For a sinusoid of wavelength 8 px, iterative 1-D LK recovers shifts of 3 and 3.9 px
exactly but converges to $-3.9$ px for a true shift of 4.1 px and to $-2$ px for 6 px:
beyond half a wavelength it locks on the aliased solution $h-\lambda$. Halving the
resolution halves both the shift and the wavelength, so the ratio $h/\lambda$ does not
change at any pyramid level. The pyramid helps because low-pass filtering removes the
fine periodic content and leaves coarser structures, such as an object outline, to
drive the coarse estimate. With OpenCV's defaults ($21\times21$ window, so a half-width
of 10 px, and `maxLevel=3`), Bouguet's rule "$d\le\omega$" per level and the gain of 15
give about 150 px; this is a heuristic, not a guarantee.

### Worked example C: size of RAFT's correlation volume

Constructed example, recomputed by checks/101-flot-optique.py. The official padder
pads each dimension to a multiple of 8 (utils.py L7–L24). A $1024\times436$ Sintel frame
becomes $1024\times440$, a $128\times55$ grid of 7,040 cells: the full volume holds
$7040^2\approx49.6$ M values, 198 MB in float32, and 261 MB with the pooled levels. At
$1088\times1920$ the grid has 32,640 cells and the first level alone needs 4.26 GB.
The lookup reads $4\times(2r+1)^2=324$ values per pixel in the code (corr.py L29–L50)
against $4\times41=164$ for the L1 ball of eq. 2, and radius 4 on the coarsest level
spans $4\times8\times8=256$ px, as the paper states [§3.2].

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| LK window $(2\omega+1)^2$ | Bouguet: $\omega$ typically 2–7 px [§1]; OpenCV default $21\times21$; `lk_track.py` sample $15\times15$ | Larger: more texture, larger convergence basin, lower noise; smaller: better at motion boundaries [§2] | Window also sets the image border needed at every level [§2.6] |
| Pyramid levels $L_m$ | Bouguet: 2–4, "no sense to go above a level 4" for typical sizes [§2.1]; OpenCV default `maxLevel=3`; sample 2 | Capture range grows like $2^{L_m+1}-1$ | Small or thin objects vanish at coarse levels; OpenCV stops building when a level is no larger than the window (lkpyramid.cpp L832–L837) |
| Iterations, stop | Bouguet: stop at 0.03 px or 20 iterations, about 5 on average [§2.3]; OpenCV default 30 iterations and 0.01 px | Sub-pixel accuracy | OpenCV clamps the count to 100 and squares epsilon before comparing it with the update (L1388–L1393, L694) |
| `minEigThreshold` | OpenCV default $10^{-4}$ | Rejects ill-conditioned windows before solving | Scaled by the implementation (worked example D); compare thresholds only within one implementation |
| Point selection | Bouguet: keep pixels above 5–10% of the best $\lambda_{\min}$, local maxima, minimum spacing 5–10 px [§3] | Feeds the tracker well-conditioned windows | See [CV-CORNERS](../../40-features-matching/references/46-harris-shi-tomasi.md) |
| RAFT updates | 12 unrolled in training; 32 on Sintel and 24 on KITTI at evaluation [§4, §4.3] | More updates refine; 200 updates do not diverge [Table 2] | Latency grows linearly with updates; gains saturate (EPE 1.61 at 8, 1.43 at 32 on Sintel clean, C+T) |
| RAFT lookup radius and levels | $r=4$, 4 levels; small model $r=3$ (raft.py L30–L39) | Radius 0 still gives "a rough estimate"; larger is better [§4.3] | Pooling captures large and small motions [§4.3] |

**Ablation evidence (RAFT, Table 2, trained C→T, Sintel train EPE clean/final).** Radius
0 gives 3.41/4.53 against 1.63/2.83 for $r=4$; a 32 px correlation range gives
2.91/4.48 and 128 px 1.64/2.81, so all-pairs mainly removes the need to choose a
range; replacing correlation by feature warping gives 2.27/3.73; convex upsampling gives
1.43/2.71 against 1.60/2.79 for bilinear. These are single-protocol results on
synthetic data.

**Tuning approach (project method).** On held-out sequences from the deployment
domain with reference motion (a synthetic or rigidly controlled scene, or a
forward-backward proxy):

1. Measure the displacement distribution per frame pair at the native frame rate,
   including camera motion; set $L_m$ so that $(2^{L_m+1}-1)\omega$ covers a high
   percentile with margin, and no higher than needed for the smallest relevant object.
2. Sweep the window size at fixed $L_m$; plot error separately for interiors and for
   points within a few pixels of motion boundaries.
3. Calibrate the rejection (minimum eigenvalue, `err`, forward-backward distance) on
   points labelled correct or wrong, and report the kept fraction with the error.
4. For RAFT, sweep the number of updates against latency on the target hardware.

## Properties and limits of guarantees

- **Translation model.** LK estimates a pure translation of the window; rotation,
  scale change and perspective inside the window are model errors, which the affine
  extension addresses [Lucas and Kanade, §4.6] at the cost of 6 instead of 2
  parameters [Bouguet, §2.7]. Bouguet reports that 2-D tracking is more accurate than affine tracking and
  recommends affine matching only for rejection [§2.7].
- **Photometric invariance.** SSD-based LK is not invariant to gain or offset changes.
  An additive offset $c$ between the images adds $c\sum\nabla I$ to $\mathbf b$, which
  biases the estimate unless the window's gradients sum to zero (derivation from the
  normal equations); a gain change scales $\delta I$ unevenly across the window. RAFT's learned features may tolerate some changes, which is an empirical property of
  its training data, not a guarantee.
- **Local optimum.** Gauss–Newton converges to the nearest minimum; the pyramid moves
  the starting point, it does not guarantee the global one (worked example B).
- **Sub-pixel accuracy** depends on interpolation, noise and the conditioning of $G$;
  its standard deviation scales like $\sigma/\sqrt{\lambda_{\min}}$ under the
  idealized noise model above.
- **No identity or visibility guarantee.** A `status` of 1 means that the solver ran to
  completion inside the image with a well-conditioned matrix, not that the point is the
  same surface point. RAFT returns a vector for every pixel, including unmatched ones.
- **RAFT behaviour.** Tied weights and bounded activations "encourage convergence to a
  fixed point"; the authors report no divergence up to 200 updates [§3.3, §4.3]. This is
  an empirical observation on their data, not a convergence proof.

## Cost and implementation

Cost drivers:

- **LK**: per point and level, building $G$ costs $O(N)$ for a window of $N$ pixels;
  each of $K$ iterations re-samples the window and accumulates $\mathbf b$ in $O(N)$,
  and solves a $2\times2$ system. Total $O(P\,(L_m+1)\,K\,N)$ for $P$ points, plus the
  pyramids. In the general Baker–Matthews form, with $n$ warp parameters, one iteration
  costs $O(n^2N+n^3)$ and the Hessian dominates [Baker and Matthews, §2.4]; the
  constant $G$ of the translational case removes that term from the loop.
- **Exhaustive search**, for comparison: $O(M^2N^2)$ for an $N\times N$ picture and an
  $M\times M$ search region [Lucas and Kanade, §3].
- **RAFT**: the all-pairs volume is $O(N_p^2)$ in time and memory for $N_p$ feature cells,
  computed once; each update costs a lookup and a small convolutional GRU. An equivalent
  on-demand implementation costs $O(N_pM)$ for $M$ updates [§3.2]. The authors measured
  the volume at 17% of inference time for $1088\times1920$ video [§3.2] and time their
  model on a GTX 1080Ti [§4.4].

### OpenCV 4.13 contracts

Read in the 4.13.0 header, sources and sample on GitHub, because docs.opencv.org
returned HTTP 403 during this pass. No code was executed for this note.

- `calcOpticalFlowPyrLK(prevImg, nextImg, prevPts, nextPts, status, err,
  winSize=Size(21,21), maxLevel=3, criteria=(COUNT+EPS, 30, 0.01), flags=0,
  minEigThreshold=1e-4)` [tracking.hpp, L134–L186]. Without
  `OPTFLOW_USE_INITIAL_FLOW`, `prevPts` is copied to `nextPts` as the initial
  estimate. By default `err` is the L1 distance between the patches divided by the
  number of pixels; with `OPTFLOW_LK_GET_MIN_EIGENVALS` it is the minimum eigenvalue
  [L157–L166].
- Derivatives are Scharr filters (lkpyramid.cpp L59–L155); the image must be 8-bit
  (`buildOpticalFlowPyramid` asserts `CV_8U`, L753).
- `status` is set to 0 only at level 0, when the window lies outside the image, when the
  normalized minimum eigenvalue is below the threshold or the determinant is below
  `FLT_EPSILON`, or when the moving window leaves the image (L244–L254, L496–L508,
  L519–L526, L706–L718). At coarser levels the same tests skip refinement without
  marking the point.
- Iterations stop when the squared update is below the squared epsilon; if two
  successive updates nearly cancel (oscillation), the code steps back by half the last
  update and stops (L694–L703).
- The Python sample `lk_track.py` ignores `status`, re-tracks from $I_2$ to $I_1$ and
  keeps a point only when the round trip returns within 1 px on both axes
  (samples/python/lk_track.py L56–L59); the tutorial calls this a "backward-check".
- `calcOpticalFlowFarneback` and `DISOpticalFlow` are OpenCV's dense CPU options
  [tracking.hpp, L188–L229, L652–L767]; see [CV-FARNEBACK](103-farneback.md).

### Worked example D: what `minEigThreshold` means

Constructed from the code, recomputed by checks/101-flot-optique.py. The Scharr
derivative returns 32 per grey level/px of true gradient; $G$ is accumulated from these
values and multiplied by $2^{-20}$, then the minimum eigenvalue is divided by the number
of window pixels (L190–L191, L455–L498). The reported value is therefore
$\lambda_{\min}(\sum\nabla I\nabla I^T)/(1024N)$, and the default $10^{-4}$ rejects
windows whose mean squared gradient along the weakest direction is below 0.1024
(grey level/px)$^2$, an RMS of about 0.32 grey level/px. The default removes flat and
purely one-dimensional windows, not merely weak corners.

### RAFT official code (princeton-vl/RAFT, commit 2888e15)

Inputs are RGB in 0–255, rescaled to $[-1,1]$ (raft.py L89–L90); images are padded
to multiples of 8 by replication, symmetrically in "sintel" mode and at the bottom
otherwise, and the output must be cropped back (utils.py L7–L24); `forward` defaults
to 12 iterations (raft.py L86). The code was read, not run.

## Evaluation and controlled variation

### Metrics and protocols

- **End-point error (EPE).** $\|\mathbf f_{est}(\mathbf x)-\mathbf f_{gt}(\mathbf x)\|_2$ in
  pixels, averaged over the evaluated pixels. MPI-Sintel reports it over all pixels,
  separately for matched and unmatched pixels, by distance to motion boundaries (under
  10, 10–60 and over 60 px) and by speed (under 10, 10–40 and over 40 px/frame), on
  $1024\times436$ frames in Clean and Final render passes [Butler et al., §§1, 3, 4, 6].
  Methods with EPE below 0.5 px on Middlebury had about 10 px on Sintel, and over 40 px in
  unmatched regions [§1].
- **Outlier rate (KITTI 2015).** A pixel counts as an error only if its EPE exceeds
  3 px **and** 5% of the true flow magnitude, evaluated at every pixel with valid ground
  truth; the flow rate "Fl" is reported for background, foreground and all pixels
  (bg, fg, bg+fg) [Menze and Geiger, §5]. RAFT's tables label the all-pixel rate
  "F1-all".
  Worked check, recomputed by checks/101-flot-optique.py: a 4 px error on a 100 px motion
  is an inlier, on a 20 px motion an outlier.
- **Sparse tracks.** For LK there is rarely dense ground truth; practical proxies are
  the forward-backward distance, the survival rate of tracks and the reprojection
  residual of a geometric model fitted to the tracks. Each proxy can be satisfied by a
  wrong but consistent track.

Published results, comparable only within their protocol: RAFT trained on FlyingChairs
then FlyingThings (C+T) reaches EPE 1.43 (Clean) and 2.71 (Final) on Sintel train and
EPE 5.04 with Fl-all 17.4% on KITTI-2015 train; after fine-tuning, 1.61/2.86 on Sintel
test with warm start and Fl-all 5.10% on KITTI test [RAFT, Table 1, §§4.1–4.2].

### Proposed baseline and controlled variation (not executed)

- **Question**: how much does photometric realism, at identical motion, degrade each
  estimator?
- **Data**: MPI-Sintel training sequences, whose Clean and Final passes share the same
  ground-truth flow [Butler et al., §4].
- **Baseline**: Clean pass; OpenCV 4.13 `calcOpticalFlowPyrLK` with defaults on
  Shi–Tomasi corners, `calcOpticalFlowFarneback` with the parameters of the OpenCV
  sample, and RAFT with the official C+T weights and 32 updates; EPE computed on the
  same pixels for every method (corner pixels for the sparse method).
- **Controlled variation**: switch to the Final pass; everything else identical.
- **Measurements**: EPE over all, matched and unmatched pixels, by speed band; for LK,
  the fraction of points with `status=1` and with a forward-backward distance below
  1 px, and the EPE of those kept points; runtime per frame pair on stated hardware.
- **Expected effect (hypothesis)**: intensity-constancy methods degrade more than
  RAFT; LK's kept-point EPE may stay low while its kept fraction falls.
- **Confound**: Final adds motion blur, defocus and atmospheric effects together
  [§4]; the variation tests photometric realism as a bundle, not one factor.

**Measurement limits.** EPE averages are dominated by large motions and unmatched
regions; report bands. Synthetic ground truth does not measure sensor noise, rolling
shutter or compression. KITTI evaluates only pixels with valid ground truth
[Menze and Geiger, §5], so regions without ground truth never enter the average. Evaluating a sparse method on its own
selected points is not comparable with dense averages.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Tracks slide along edges | Aperture: rank-deficient $G$ | Ratio $\lambda_{\min}/\lambda_{\max}$ of the window; motion of the point along the edge direction | Select corners; raise the eigenvalue threshold; use a larger window if motion is coherent |
| Points jump by a fixed period on repetitive textures | Multiple minima beyond half a wavelength (example B) | Error clusters at multiples of the texture period; forward-backward check passes for both directions | Better prior (motion model, IMU), larger-scale structure, reject periodic windows |
| Fast objects lost while background is fine | Displacement beyond pyramid range, or object too small for coarse levels | Per-object displacement against $(2^{L_m+1}-1)\omega$; object size at level $L_m$ | Higher frame rate, prediction as initial flow (`OPTFLOW_USE_INITIAL_FLOW`), detection-based association |
| `status=1` on an occluded point | Status tests conditioning and bounds, not visibility | Forward-backward distance; patch residual `err` | Reject on round-trip distance; re-detect points regularly as the OpenCV sample does |
| Long tracks drift slowly | Pairwise tracking re-initializes the reference each frame [Bouguet, §2.7] | Compare the patch with its first appearance | Fixed-reference check or affine verification for rejection [§2.7] |
| Error concentrated at motion boundaries | Window or receptive field mixes two motions | Error versus distance to boundary (Sintel bands) | Smaller window; dense method with context; bidirectional consistency mask |
| Flow wrong after illumination change | Brightness constancy violated | Same scene with constant exposure or Clean vs Final | Normalize patches, lock exposure, use learned features |
| Flow off by a constant factor or wrong orientation | Grid mismatch after resizing or padding; axes swapped; backward used as forward | Synthetic known translation through the full pipeline | Scale components with the resize factor; crop RAFT padding; follow $(u,v)$ channel order |
| RAFT good on benchmarks, poor in the plant | Domain shift from synthetic training | Error on a few annotated or synthetic in-domain pairs | Fine-tune or use a classical method with a validity test |

## Alternatives and applications

Conditional choices:

- **Prefer pyramidal LK** for a few hundred well-textured points per frame on a CPU,
  with moderate motion per frame and a geometric model downstream (homography,
  essential matrix) that can reject outliers.
- **Prefer a dense classical method** (Farnebäck, DIS) on a CPU when every pixel needs
  a vector and motion is smooth; see [CV-FARNEBACK](103-farneback.md).
- **Prefer RAFT or another learned estimator** when accuracy at motion boundaries and
  large displacements matters, a GPU is available and in-domain validation data exist.
- **Prefer descriptor matching** ([CV-MATCHING](../../40-features-matching/references/43-detecteurs-matchers.md))
  for wide baselines, large rotations or re-detection after loss, where local
  linearization cannot reach the solution.
- **Prefer parametric alignment** ([CV-ECC](../../40-features-matching/references/45-recalage-ecc.md))
  when the whole image follows one warp, and **long-term point tracking**
  ([CV-VIDEO](102-points-actions-video.md)) when trajectories must survive occlusions.
- Global variational methods add a smoothness term over the whole image to resolve the
  aperture problem (Horn and Schunck, 1981; not re-read in this pass).

Industrial uses (project reasoning, not published results): video stabilization from
LK tracks and a fitted homography; belt or web speed from the median flow on a
textured region, with timestamps per pair; front-end of visual odometry; detecting
unexpected motion in a fixed-camera inspection cell from dense flow magnitude.

## Guided reasoning and proposed checks

These constructed cases develop the brightness-constancy constraint, the aperture
problem and dense correspondence. They explain or test reasoning; no image, video or
hardware result is claimed as measured. Method properties remain tied to the sources
below.

### Case linked to CV-FLOT-001

**Working question**: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?

**Reference answer**: One equation cannot constrain two unknowns without extra assumptions or neighboring pixels; along an edge, the tangential component remains ambiguous.

**Reading the constraint**: The spatial gradient gives the direction in which a change of intensity informs the displacement. Motion tangent to a uniform edge barely changes the intensities, so several vectors satisfy the same equation. This is missing local information, not necessarily a solver error.

**Example and limit**: A vertical edge that slides upwards can look almost unchanged in a small window. Adding pixels of the same edge does not create a second independent direction. A neighborhood containing a corner constrains both components better if the motion stays coherent and the photometry stable. Examine conditioning, window size and the validity of the assumptions before increasing iterations. A regularization can choose one of several plausible solutions; it then adds an assumption, not a certain observation of the displacement.

### Case linked to CV-FLOT-004

**Working question**: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?

**Reference answer**: As an estimate under the assumptions of the model, with no guaranteed observable correspondence; examine the occlusion mask and consistency.

**Why density proves nothing**: A dense algorithm can fill regions where the data no longer contain a visible match. The value can come from context, regularization or a learned model. These mechanisms give a useful hypothesis, but not a new observation of the hidden surface.

**Discriminating check**: Distinguish occlusion, exit from the field of view and matching error. For a round trip, evaluate the backward flow at the position reached in the other image, taking interpolation and the field limits into account. An inconsistency signals a possible problem; consistency does not guarantee identity on a repetitive texture. Measure regions separately under a stated visibility protocol. At inference, no ground-truth occlusion is available: the confidence policy may use only the information actually given to the system.

**Source consulted for this pass**: [OpenCV 4.13.0 optical flow tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown), Lucas–Kanade, pyramids and dense flow. The remaining developments are in the [flashcards](../101-flot-optique.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-FLOT-001

**Situation**: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?

**Lucas–Kanade system**: Stack the window gradients in a matrix $A$ whose rows are $(I_x,I_y)$, and set $b=-I_t$. Least squares give $A^TA\,d=A^Tb$, with $d=(u,v)^T$. Both eigenvalues of $A^TA$ must be sufficiently large to constrain both directions; an edge typically produces one weak direction. Enlarging the window may bring new gradients, but may violate the assumption of shared motion by mixing two objects. Good point selection therefore seeks spatial information and neighborhood coherence together, not just a large gradient magnitude.

### CV-FLOT-002

**Situation**: An optical flow vector represents 4 pixels between two images. Does this imply a velocity of 4 px/s?

**Change of grid**: If a second pipeline works on an image resized by $(s_x,s_y)$, the same displacement becomes $(s_xu,s_yv)$. To compare image speeds, first put the vectors on a common grid, then use the real acquisition intervals. A dropped frame can double the interval without the physical speed having doubled. Under perspective, even a constant 3D translation produces depth-dependent image displacements, and a change of apparent size also changes the field. Converting pixels to meters therefore requires a scene and camera model, beyond a division by the nominal frame rate.

### CV-FLOT-003

**Situation**: What distinct roles do correlations and recurrent updates play in RAFT?

**Dimensions of the correlation**: For two feature maps of size $h\times w$, an all-pairs comparison links each site of the first to each site of the second, $(hw)^2$ values before optimizations. The volume encodes candidate similarities, not a one-to-one assignment of pixels. The updates read this volume around the predicted positions and adjust the flow; several source pixels may point to the same region, and occlusions do not always offer a match. Separating the volume's memory, the cost per iteration and the number of iterations helps to understand the resolution trade-off. Repeated refinement guarantees neither physical convergence nor identity.

### CV-FLOT-004

**Situation**: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?

**Round-trip residual**: Let $F_{12}$ map image 1 to image 2 and $F_{21}$ map back. For a pixel $x$ of the first image, compute $e(x)=\|F_{12}(x)+F_{21}(x+F_{12}(x))\|$ in pixels, only where the return sampling is valid. A confidence rule can compare this residual with a tolerance that depends on motion and noise, validated on held-out data. A periodic texture can produce a wrong translation and then its exact opposite: a zero residual then proves nothing about the real surface. Keep a visibility failure distinct from a merely large numerical residual.

**Passages consulted for these developments**: [OpenCV 4.13.0 optical flow tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown), Lucas–Kanade equation and system; grid changes and compositions are project deductions; [Teed and Deng, RAFT](https://arxiv.org/html/2003.12039v3), Figure 1 and §3, all-pairs correlation and updates.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FLOT-001 — Brightness constancy is a model assumption

A flashing light can change $I_t$ without any physical motion, while an edge translating along itself can produce almost no detectable intensity change. Both examples break a naive identification of brightness change with unique motion. Gradient diversity addresses local geometric observability; it does not repair a photometric model violated by lighting or reflections. A proposed diagnostic separates controlled illumination changes from known geometric translations.

### CV-FLOT-002 — The timestamp interval belongs to each pair

A fixed displacement of 4 px means 200 px/s at 20 ms but 80 px/s at 50 ms. Variable frame intervals therefore require pair-specific timestamps rather than a nominal frame rate. If timestamps refer to reception instead of exposure, packet jitter can create a spurious velocity variation. This is an image-plane average velocity under the temporal model; converting to object-space speed needs geometry and potentially ego-motion compensation.

### CV-FLOT-003 — A correlation maximum is not yet the flow field

For one pixel, several locations in a repeated pattern can have high feature correlation. A recurrent update combines lookup evidence with its current estimate and learned spatial context to refine the field. Taking an independent maximum from each correlation row would define another algorithm and can lose coherent motion. The architecture's dense output still requires evaluation at occlusions, boundaries and domain shifts rather than assuming correlation resolves every ambiguity.

Consulted foundations: [OpenCV optical flow tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown): brightness constancy, Lucas–Kanade local system and pyramids; [RAFT](https://arxiv.org/html/2003.12039v3): §3 all-pairs correlation, lookup and recurrent updates.

## Sources and flashcards

### Scientific sources

- [Lucas and Kanade 1981, An Iterative Image Registration Technique](https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf): §3 (exhaustive search cost), §4.1 eqs. 1–7 (linearization, weighting, Newton–Raphson iteration), §4.2 eq. 9 (least squares), §4.3 (convergence up to half a wavelength, smoothing trade-off), §4.5 (n-dimensional form), §4.6 (affine extension).
- [Bouguet, Pyramidal Implementation of the Lucas Kanade Feature Tracker](http://robots.stanford.edu/cs223b04/algo_tracking.pdf) (Intel report, served over HTTP only): §1 (problem, window, coordinates), §2.1–2.2 (pyramid, eqs. 5–10, gain $2^{L_m+1}-1$), §2.3 (eqs. 13–33, invertibility of $G$, stop rules), §2.5–2.7 (sub-pixel sampling, borders, lost features), §3 (feature selection).
- [Baker and Matthews, Lucas-Kanade 20 Years On, Part 1, CMU-RI-TR-02-16](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf): §2.1–2.2 (goal and Gauss–Newton derivation), §2.4 (cost $O(n^2N+n^3)$), §3.2 (constant Hessian, inverse compositional).
- [Teed and Deng 2020, RAFT](https://arxiv.org/abs/2003.12039) (v3 PDF): §3 and §§3.1–3.4 (eqs. 1–7, pyramid, lookup, efficient computation, upsampling), §4 (training, iterations), §§4.1–4.4, Tables 1–2.
- [Butler et al. 2012, MPI-Sintel](http://files.is.tue.mpg.de/black/papers/ButlerECCV2012.pdf): §1 (EPE, Middlebury comparison), §4 (render passes, unmatched pixels, resolution), §6 (evaluation bands).
- [Menze and Geiger 2015, KITTI 2015](https://www.cvlibs.net/publications/Menze2015CVPR.pdf): §5, evaluation protocol (3 px and 5% outlier rule; bg, fg, all).

### Implementation sources

- [OpenCV 4.13.0, `modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): `buildOpticalFlowPyramid` (L109–L128), `calcOpticalFlowPyrLK` (L134–L186), `calcOpticalFlowFarneback` (L188–L229), `readOpticalFlow`/`writeOpticalFlow` (L488–L505), `DISOpticalFlow` (L652–L767).
- [OpenCV 4.13.0, `modules/video/src/lkpyramid.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/lkpyramid.cpp): Scharr derivatives (L59–L155), LK invoker (L187–L745), pyramid construction (L747–L843), criteria clamping (L1388–L1393).
- [OpenCV 4.13.0, `samples/python/lk_track.py`](https://github.com/opencv/opencv/blob/4.13.0/samples/python/lk_track.py): parameters (L30–L37), backward check (L56–L59).
- [OpenCV 4.13.0, optical flow tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown): assumptions, optical flow equation, LK system, pyramids, dense flow.
- [princeton-vl/RAFT at commit 2888e15](https://github.com/princeton-vl/RAFT/tree/2888e15a51fa41140771d3f498ed8023cff098d1/core): `corr.py` (L12–L60), `raft.py` (L30–L39, L63–L90, L122–L139), `utils/utils.py` (L7–L24).

### Related flashcards and references

- [Flashcards](../101-flot-optique.md): CV-FLOT-001 (constraint and aperture), CV-FLOT-002 (units), CV-FLOT-003 (RAFT roles), CV-FLOT-004 (occluded points).
- [CV-FARNEBACK](103-farneback.md), [CV-VIDEO](102-points-actions-video.md), [CV-CORNERS](../../40-features-matching/references/46-harris-shi-tomasi.md), [CV-ECC](../../40-features-matching/references/45-recalage-ecc.md), [CV-SOT](../../110-tracking-association/references/113-tracking-monoobjet.md).

Drafted by agent, 2026-10-18. Revision 6, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/101-flot-optique.md).
