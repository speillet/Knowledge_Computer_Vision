---
id: CV-MEANSHIFT
type: methode
domaine: d11
poles: ["C", "D", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 8
prerequis: ["CV-SOT", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MeanShift and CamShift — tracking an appearance distribution

This is the method note for mode-seeking trackers that follow a color distribution.
The tracking contract and the comparison with correlation filters and Siamese
trackers are in [CV-SOT](113-tracking-monoobjet.md). Two formulations coexist and
must not be confused: the kernel-based tracker of Comaniciu, Ramesh and Meer, which
maximizes a Bhattacharyya similarity between kernel-weighted histograms, and the
back-projection tracker of Bradski's CAMSHIFT and of OpenCV, which climbs to the
centroid of a per-pixel color likelihood image.

## Problem and data contract

**Task.** From an initial region around the target, follow the local mode of its
color distribution from frame to frame; CamShift also re-estimates the region's size
and orientation in the image.

**Inputs (OpenCV pipeline).** An 8-bit BGR frame converted to HSV, where OpenCV stores
hue in $[0,180)$ for 8-bit images; a model histogram computed once on the initial
region, for example 16 hue bins normalized to $[0,255]$, with a mask that discards
pixels of low saturation or value; and, per frame, a back-projection: a single-channel
image with the frame's size and depth in which each pixel receives the scaled value of
its histogram bin [imgproc.hpp, L3322–L3360]. The OpenCV sample masks pixels outside
$S\ge60$, $V\ge32$ and uses 16 hue bins [samples/python/camshift.py, L82–L100].

**Inputs (kernel-based tracker).** A target ellipse normalized to a unit circle by
the half-axes $(h_x,h_y)$, a quantized feature space of $m$ bins, for example RGB at
$16\times16\times16$, and a kernel profile $k$ [Comaniciu et al., §2.1, §5].

**Outputs.** `cv::meanShift` returns the iteration count and moves an integer
`Rect` in place, with fixed size; `cv::CamShift` returns a `RotatedRect` (centre,
length and width in pixels, angle in degrees) and updates the search window
[video/tracking.hpp, L64–L107]. The kernel-based tracker returns the new centre and,
with scale adaptation, a bandwidth $h$; the Bhattacharyya coefficient computed after
convergence measures the similarity between model and final candidate [§4.2].

**Role in a pipeline.** Very cheap single-object tracking of a color-distinctive
target, historically face tracking for user interfaces (Bradski) and object tracking
in surveillance video (Comaniciu et al.); also a refinement step after a coarse
detection.

## Intuition

Each pixel votes for "target colour" with a weight; the window moves to the weighted
centre of the votes it covers and repeats until it stops moving. In the kernel-based
tracker the weights are $w_i=\sqrt{q_u/p_u(\mathbf y_0)}$ for a pixel of bin $u$: a
colour that is under-represented in the current window relative to the model pulls
harder, and a colour absent from the model has weight 0 [eq. 10]. CamShift then reads
the spread of the weights to resize and rotate the window.

*Illustration (constructed example, recomputed by checks/115-meanshift-camshift.py).*
Two masses 1 and 3 at $x=10$ and $x=14$ px have their centroid at 13 px, not at the
midpoint. Multiplying both by 5 keeps it at 13; adding 1 to both moves it to 12.67:
a uniform background weight pulls the centroid toward the window centre.

## Prerequisites and competencies

**Required prerequisites**: [CV-SOT](113-tracking-monoobjet.md),
[CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md)
for color, exposure and saturation. Image moments and connected components, used to
clean a back-projection, are in
[CV-MORPHO](../../30-traitement-image/references/33-morphologie-composantes.md).
**Target competencies**: explain a MeanShift iteration; distinguish MeanShift and
CamShift; diagnose a color distractor; evaluate color and adaptation separately.
Related notions remain alternatives, not implicit dependencies.

## Assumptions, observability and degenerate cases

- **Overlap between frames.** The kernel-based tracker's operational basin of
  attraction is at least the size of the target model: if the target centre stays in
  the area the model covered in the previous frame, the local maximum is a reliable
  indicator [Comaniciu et al., §4.2]. Faster motion needs prediction, for example the
  Kalman extension of the same paper [§6.2].
- **Discriminative color.** The authors assume that the representation gives a unique
  maximum of the similarity in the local neighbourhood [§4.2]; a same-color distractor
  violates it.
- **Reliable hue.** Hue is undefined or noisy at low saturation or brightness; Bradski's
  patent accumulates hue only above saturation and value thresholds, with S above 20
  and V above 15 as example values [US 6,394,557].
- **Small appearance change between frames.** The linear approximation of the
  Bhattacharyya coefficient behind the mean-shift step holds when the candidate
  histogram does not change drastically between consecutive frames [§4.1].
- **No spatial layout.** A histogram discards where colours are; the kernel only
  down-weights peripheral pixels [§2.1].

Degenerate cases. A window with zero mass has no centroid: OpenCV's `meanShift` then
stops and leaves the window unchanged without reporting it, and `CamShift` returns an
empty `RotatedRect` [camshift.cpp, L86–L87, L150–L151]. A round blob has equal
eigenvalues and an undefined orientation. A candidate bin with $p_u(\mathbf y_0)=0$
must be skipped in eq. 10 [§4.1]. The mean-shift step can also stop at a saddle point
of the similarity surface, which the authors consider unstable under image noise [§4.2].

## Procedure

```text
OpenCV CamShift pipeline (sample camshift.py and camshift.cpp, 4.13.0)
  init: hsv <- BGR2HSV(frame_0); mask <- inRange(hsv, (0, 60, 32), (180, 255, 255))
        hist <- calcHist(hsv[roi], hue channel, mask[roi], 16 bins); normalize to [0, 255]
  each frame:
        prob <- calcBackProject(hsv, hue, hist) AND mask
        meanShift: repeat up to maxCount: centroid of prob in window -> move window
                   (integer shift); stop if shift^2 < round(eps^2) or mass is zero
        CamShift:  enlarge window by 10 px per side; moments M00, mu20, mu02, mu11
                   box <- centre, length = 4 sqrt(lambda1), width = 4 sqrt(lambda2), angle
                   next window <- axis-aligned extent of the box + 2 px
        if M00 (or box area) is too small: report loss; do not trust the box

Kernel-based tracker (Comaniciu et al. 2003, Sec. 4)
  model: q_u <- kernel-weighted histogram of the initial ellipse
  each frame, from y0 = previous centre:
        p_u(y0) <- kernel-weighted histogram of the candidate
        w_i <- sqrt(q_u / p_u(y0)) for the bin u of pixel i
        y1 <- sum(w_i x_i) / sum(w_i)                     # Epanechnikov profile
        stop when |y1 - y0| < 1 px or after N_max = 20 iterations (about 4 on average)
  scale: rerun with h_prev and h_prev +/- 10%; keep the largest Bhattacharyya coefficient;
         h_new = 0.1 h_opt + 0.9 h_prev
```

Purpose of the steps. The mask removes pixels whose hue is unreliable before they
enter the histogram and the back-projection. Normalizing the histogram to $[0,255]$
fits the 8-bit back-projection. The integer stopping test of OpenCV makes `epsilon` a
pixel threshold. The 10-pixel margin lets CamShift see mass just outside the
converged window so that the window can grow. In the kernel-based tracker, the
smoothed scale update avoids oversensitive bandwidth changes [§4.3].

## Mathematics, conventions and units

**Back-projection centroid (OpenCV).** For non-negative weights $p(x,y)$ in the window
$W$, $M_{00}=\sum_W p$, $M_{10}=\sum_W x\,p$, $M_{01}=\sum_W y\,p$ and the centroid is
$(M_{10}/M_{00},\,M_{01}/M_{00})$ in pixels, defined for $M_{00}>0$. OpenCV moves the
window by the rounded offset between this centroid and the window centre and stops
when the squared integer shift is below the rounded $\epsilon^2$
[camshift.cpp, L68–L102]. With the sample's `epsilon` of 1 px, iteration stops only
when the rounded shift is zero.

**Kernel-based tracker.** With normalized pixel locations $\mathbf x_i^\star$ of the
model region, bin index $b(\cdot)$, Kronecker $\delta$ and normalization constants
$C$ and $C_h$, the model and the candidate centred at $\mathbf y$ with bandwidth $h$
are [eqs. 2 and 4]

$$\hat q_u=C\sum_{i}k\big(\|\mathbf x_i^\star\|^2\big)\,\delta[b(\mathbf x_i^\star)-u],\qquad \hat p_u(\mathbf y)=C_h\sum_{i}k\Big(\Big\|\tfrac{\mathbf y-\mathbf x_i}{h}\Big\|^2\Big)\,\delta[b(\mathbf x_i)-u].$$

Their similarity is the Bhattacharyya coefficient
$\rho(\mathbf y)=\sum_u\sqrt{\hat p_u(\mathbf y)\,\hat q_u}$, the cosine between the
unit vectors $(\sqrt{\hat p_u})$ and $(\sqrt{\hat q_u})$, and
$d(\mathbf y)=\sqrt{1-\rho(\mathbf y)}$ is a metric [eqs. 6–7]. A first-order
expansion of $\rho$ around $\mathbf y_0$ turns its maximization into a kernel density
estimate with weights $w_i=\sum_u\sqrt{\hat q_u/\hat p_u(\mathbf y_0)}\,\delta[b(\mathbf x_i)-u]$
[eqs. 8–10], whose mode is reached by the mean-shift step
$\mathbf y_1=\sum_i\mathbf x_i w_i\,g(\cdot)/\sum_i w_i\,g(\cdot)$ with $g=-k'$
[eq. 11]. For the Epanechnikov profile, $g$ is constant and the step is the weighted
average $\mathbf y_1=\sum_i\mathbf x_i w_i/\sum_i w_i$ [eqs. 12–13].

*Worked example (constructed, recomputed by checks/115-meanshift-camshift.py).* For a
model $q=(0.5,0.3,0.2,0)$ and a candidate $p=(0.2,0.3,0.2,0.3)$ over four bins,
$\rho=\sqrt{0.10}+0.3+0.2+0=0.816$ and $d=0.429$. The weights are 1.581 for the first
colour, under-represented in the candidate, 1 for the matched colours and 0 for the
colour absent from the model: the step moves toward pixels of the missing colour.

**CamShift moments (OpenCV).** With central moments $\mu_{20},\mu_{11},\mu_{02}$ over
the enlarged window and $a=\mu_{20}/M_{00}$, $b=\mu_{11}/M_{00}$, $c=\mu_{02}/M_{00}$,
the orientation is $\theta=\operatorname{atan2}\big(2b,\;a-c+\sqrt{4b^2+(a-c)^2}\big)$
and the box length and width are $4\sqrt{\lambda_1}$ and $4\sqrt{\lambda_2}$, with
$\lambda_1\ge\lambda_2$ the variances along and across the principal axis
[camshift.cpp, L153–L181]. The box therefore spans $\pm2$ standard deviations of the
weight distribution. Bradski's patent instead sets the window side proportional to the
square root of the zeroth moment and the orientation from the second moments
[US 6,394,557, eqs. 4–7].

*Worked example B (constructed, recomputed by the same script).* A uniformly weighted
$40\times20$ px rectangle has variances $(40^2-1)/12$ and $(20^2-1)/12$ on the pixel
grid, so CamShift returns a $46.2\times23.1$ px box: about $4/\sqrt{12}=1.155$ times
the blob. If the back-projection is uniform over a larger area of the same colour, the
moments are taken over the window enlarged by 10 px per side and the next window is the
box length plus 2 px, so a 40 px window grows to about 71, 107, 149 and 197 px over
four frames. A disc gives equal eigenvalues, so its angle carries no information.

## Parameters and tuning

| Parameter | Source values | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Feature space and bins | Hue, 16 bins (OpenCV sample); RGB $16\times16\times16$ (Comaniciu et al., §5) | Discrimination against noise and illumination robustness | Few bins merge target and background colours; many bins make sparse, noisy histograms |
| Saturation and value mask | $S\ge60$, $V\ge32$ (sample); S above 20, V above 15 as patent example | Removes unreliable hue | Too strict empties dark or pale targets; too loose lets grey background vote |
| Histogram normalization and back-projection scale | Min-max to $[0,255]$ (sample); `scale` argument | Range of the 8-bit weights | Saturation of the 8-bit back-projection flattens differences |
| Initial region | User box or detector box | Defines $q$ | Background inside the box enters the model |
| Stopping criteria | Sample: 10 iterations, $\epsilon=1$ px; paper: 1 px, $N_{\max}=20$, about 4 iterations on average | Latency against convergence | More iterations converge more firmly on the current basin, right or wrong |
| Kernel and bandwidth | Epanechnikov profile; $h\pm10\%$, smoothing 0.1 (§4.3) | Weighting of peripheral pixels and scale tracking | Faster scale smoothing follows growth but reacts to clutter |
| CamShift margin | 10 px, hard-coded (`TOLERANCE`, camshift.cpp L115) | Lets the window grow | Combined with a same-colour background, makes the window bloom (example B) |

Tuning approach (project method). On held-out sequences from the deployment scenes:
(1) inspect hue and saturation histograms of target and background and choose
channels, bins and mask thresholds that maximize their separation, for example the
Bhattacharyya distance between target and surrounding-ring histograms; (2) set the
iteration budget from the latency budget; (3) choose a loss rule on $M_{00}$, the box
area or the final Bhattacharyya coefficient using frames labelled absent;
(4) evaluate window adaptation separately from appearance (card CV-MEANSHIFT-004).

## Properties and limits of guarantees

- **Local optimum.** The mean-shift step climbs to a local maximum of the similarity
  or a stationary point of the centroid iteration; it is not a global search
  [Comaniciu et al., §4.2].
- **Invariances.** A histogram is invariant to in-plane rotation and to non-rigid
  deformation that preserves the colour proportions; the Bhattacharyya distance uses
  discrete densities and is therefore scale-invariant up to quantization [§3,
  property 3]. The centroid is invariant to a positive rescaling of the weights but
  not to an added constant (illustration above).
- **Convergence in practice.** The step can fail to increase $\rho$ because of the
  linear approximation; the authors observed this in 0.1% of cases and dropped the
  corresponding safeguard [§4.2].
- **Geometry.** The CamShift box describes the second moments of the weight image in
  the image plane, spanning $\pm2$ standard deviations; it is not a 3-D pose and is
  1.155 times larger than a uniform blob (example B).
- **No identity.** Two objects with the same colour statistics are indistinguishable
  to the model; convergence on the wrong one is a valid optimum of the criterion.

## Cost and implementation

- **Kernel-based tracker.** About $N\,n_h\,c_S$ per frame and scale, with $N$ the mean
  number of iterations, $n_h$ the candidate pixels and $c_S$ the cost of an addition, a
  square root and a division. For a $50\times50$ target and $N=4.19$, this is about 24
  times cheaper than an exhaustive search over the basin of attraction [§4.4].
  Reported: 150 frames/s on a 1 GHz PC with scale adaptation, which runs the
  localization three times per frame [§4.4].
- **OpenCV pipeline.** One colour conversion and one back-projection per frame, each
  linear in the processed pixels (whole frame unless restricted to a region), then one
  moment computation over the window per iteration.

### OpenCV 4.13 contracts

Read in the 4.13.0 sources on GitHub (docs.opencv.org returned HTTP 403); no code was
executed for this note.

- `cv::meanShift(probImage, window, criteria)`: single-channel input; the window is
  clipped to the image; each iteration computes `moments` of the window and moves it by
  the rounded centroid offset, clamped inside the image; a zero `m00` breaks the loop
  silently; the return value is the number of iterations [camshift.cpp, L44–L107].
- `cv::CamShift(probImage, window, criteria)`: runs `meanShift`, enlarges the window by
  10 px per side, computes the moments, returns an empty `RotatedRect` if `m00` is zero,
  otherwise the box of the previous section; the angle is reported in degrees in
  $[0,180)$ and the next window is the box's axis-aligned extent plus 2 px
  [camshift.cpp, L110–L218].
- `cv::calcBackProject`: reads each pixel's histogram bin value, multiplies it by
  `scale` and writes it to an output of the same size and depth as the input
  [imgproc.hpp, L3322–L3360].

## Evaluation and controlled variation

Benchmark protocols are summarized in [CV-SOT](113-tracking-monoobjet.md). The
kernel-based tracker was demonstrated on sequences with qualitative results, iteration
counts and similarity surfaces rather than benchmark scores [§5].

**Proposed baseline and controlled variation (not executed).**

- *Data*: held-out sequences with per-frame boxes, including a target that grows or
  shrinks, a same-colour distractor and low-saturation lighting.
- *Baseline*: `meanShift` with a fixed window, one histogram and mask recipe, the same
  initialization and the same loss rule.
- *Controlled variation*: `CamShift` with exactly the same histogram, mask,
  initialization, stopping criteria and loss rule.
- *Measurements*: centre error, IoU of the window or of the box's bounding rectangle
  with the ground truth, ratio of window area to target area, losses and recoveries,
  and the final Bhattacharyya coefficient as a confidence trace.
- *Reading*: CamShift should improve IoU on scale change; if its area ratio climbs on
  the distractor or low-saturation sequences, the gain comes with blooming (example B).
  Histogram changes are tested afterwards as a separate factor (card CV-MEANSHIFT-004).

**Measurement limits.** IoU against an axis-aligned ground truth penalizes a rotated
box; a ±2σ box is systematically larger than a tight annotation of a uniform blob; the
results depend on the scenes' colour statistics more than on the algorithm.

*Worked example C (constructed, recomputed by the 2026-11-16 check script).* The box of
example B, $46.2\times23.1$ px around a uniformly weighted $40\times20$ px blob, has an
IoU of 0.75 with a tight annotation even when perfectly centred, $(\sqrt{12}/4)^2$ in the
continuous limit, while a fixed MeanShift window of the right size scores 1. On a
sequence without scale change, the adaptive arm therefore loses about 0.25 IoU by box
convention alone. Report centre error and the box-to-target area ratio beside IoU, or
calibrate a box factor on frames without distractors (project recipe), before reading an
IoU difference as an effect of adaptation. For the second factor, a $2\times2$ design
with constructed mean IoU on the scale-change sequence of 0.48 (histogram H1, fixed
window), 0.60 (H1, CamShift), 0.56 (H2, fixed) and 0.62 (H2, CamShift) shows how a joint
change misleads: switching both at once gains 0.14, but adaptation is worth 0.12 with H1
and 0.06 with H2 (main effect 0.09), the histogram 0.08 with a fixed window and 0.02
with CamShift (main effect 0.05), and the interaction is $-0.06$. Since
$0.14=0.12+0.02=0.08+0.06$, the single comparison cannot split the gain.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Window drifts onto a same-colour object or region | Histogram cannot separate target and distractor | Back-projection shows a second mass of similar weight | Better channels or mask, texture cue, motion prior or detector |
| CamShift window grows over the background | Uniform same-colour area; the 10 px margin and ±2σ box feed growth | Window area ratio over time against example B | Threshold or clean the back-projection, cap the size, mask the background colour |
| Window stops moving although the target left | Zero mass: OpenCV keeps the window without an error | Compute $M_{00}$ in the window each frame | Explicit loss rule and re-detection |
| Tracking collapses in dim or pale light | Hue unreliable at low saturation or value | Fraction of masked pixels in the target region | Adjust mask thresholds, use other channels or exposure control |
| Box angle jumps from frame to frame | Nearly equal eigenvalues (round blob) | Ratio $\lambda_1/\lambda_2$ near 1 | Ignore the angle for round targets |
| Tracking lost after fast motion | Target left the basin of attraction | Displacement against the target size | Motion prediction (Kalman) or larger search |

## Alternatives and applications

- Prefer the kernel-based tracker over plain back-projection when the target is small
  or the background shares some colours: kernel weighting and the Bhattacharyya
  criterion compare whole distributions instead of per-pixel likelihoods.
- Prefer CamShift when the projected size changes and an oriented blob is a sufficient
  output; prefer fixed-window MeanShift when the background contains the target colour.
- Prefer [correlation filters](114-mosse-kcf.md) when texture, not colour,
  discriminates the target, and a Siamese tracker or detection plus association when
  identity matters ([CV-SOT](113-tracking-monoobjet.md)).

Industrial uses (project reasoning): following a coloured marker or a coloured part on
a controlled-light conveyor at very low compute; hand or face tracking for interaction
under stable lighting, the original application of CAMSHIFT.

## Guided reasoning and proposed checks

These constructed cases develop back-projection, the local mode and window adaptation. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-MEANSHIFT-001

**Working question**: What does one MeanShift iteration compute on a backprojection image, and what should happen if the window contains no mass?

**Reference answer**: Calculate the centroid of scores in the window, and then move the window to that center. If the total mass $M_{00}$ is zero, the centroid is indefinite: do not divide and apply an explicit loss/search policy.

**Reading moments**: The backprojection assigns a mass to each position according to its compatibility with the reference appearance. The weighted centroid gives a window shift towards this concentration. With two masses 1 and 3 placed at 10 and 14 pixels, the center is $(10+42)/4=13$ pixels: it is not the unweighted average of positions.

**Decision limit**: If the whole mass is zero, no mean position is defined by these observations. An arbitrary numerical output would mask a lack of information. Report the loss or apply a declared search policy, and then evaluate this policy. Even with a positive mass, a background of similar color can attract the window, so the concentration found does not verify the identity of the initialized object.

### Case linked to CV-MEANSHIFT-004

**Working question**: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?

**Reference answer**: Keep the same histogram, frames, and initialization; compare fixed window and adaptive window on a scale change. Measure center, overlap, size, and losses, and then separately test a histogram change.

**The logic of ablation**: Changing only the window adaptation tests its effect on the location contract. Modifying the histogram at the same time changes the masses on which the displacement is calculated, which prevents assigning the improvement to a single mechanism.

**Constructed experiment**: Use one sequence where the target gradually grows, then another where a distractor appears without scaling. Keep the same loss and reset criteria, and report errors on all frames. An adaptive window can help the first case and harm the second if the mass of the distractor distorts it. The comparison must make this tradeoff visible. Channels, bins and masks are parameters of the appearance model; their setting requires another ablation and held-out data.

**Source consulted for this pass**: [OpenCV 4.13.0, `camshift.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L218), centroid iteration and CamShift window; [OpenCV 4.13.0 CamShift sample](https://github.com/opencv/opencv/blob/4.13.0/samples/python/camshift.py#L82-L102), histogram, mask and back-projection. The remaining developments are in the [flashcards](../115-meanshift-camshift.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-MEANSHIFT-001

**Situation**: What does one MeanShift iteration compute on a backprojection image, and what should happen if the window contains no mass?

**Weighted iteration**: For scores $p(x,y)\ge0$ in window $W$, the displacement of the current center $c$ is $m(c)=\sum_Wp(x,y)(x,y)^T/\sum_Wp(x,y)-c$, in this uniform window model. Multiplying all scores by the same positive constant does not change the centroid; adding a uniform mass can instead move it towards the geometric center of the window. This distinction explains why normalizing the histogram and changing its contrast are not always equivalent operations. The stopping criterion measures a displacement or an iteration budget, without establishing that the mode found represents the original object.

### CV-MEANSHIFT-002

**Situation**: The target approaches the camera, but the tracking window remains too small. What does CamShift add compared with usual MeanShift?

**Moments of extent**: Around the centroid, the matrix of normalized central moments $\begin{bmatrix}\mu_{20}&\mu_{11}\\\mu_{11}&\mu_{02}\end{bmatrix}/M_{00}$ describes the 2-D dispersion of the mass. Its eigenvectors give the principal axes; its eigenvalues give the extent according to a window conversion convention. Close eigenvalues make the orientation undetermined, as for an almost circular distribution. These quantities describe the backprojection in the image plane, not the 3-D physical axes of the part. A distractor can change center, orientation and size simultaneously. The appearance mask should therefore be inspected before interpreting an adapted window as a reliable geometric measurement of the target.

### CV-MEANSHIFT-003

**Situation**: CamShift jumps to another part of the same color. Why can increasing the number of iterations make the problem worse?

**Identity missing from histogram**: A histogram retains color frequencies and loses most of their spatial arrangement. Two different objects can therefore produce very similar distributions, even with a high backprojection mass. An ROI containing more pixels of the desired color can attract the window without being the target. Testing a background of the same color and then a textured distractor makes it possible to verify this hypothesis. Adding a spatial descriptor or detection changes the information used and requires a new evaluation; increasing the number of iterations does not restore the spatial relationships that the histogram model has discarded.

### CV-MEANSHIFT-004

**Situation**: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?

**Two factors, four tests**: To distinguish adaptation and appearance, compare histogram H1 with fixed/adaptive window, then histogram H2 with the same two policies. Measure overlap, center error and losses with identical initialization and sequences. The interaction can be important: an adaptive window benefits from a clean backprojection but encompasses more background with a poorly separated histogram. A change of binning modifies the trade-off between color discrimination and noise robustness; a low-saturation mask further changes the retained pixels. These choices must be recorded separately to make the result reproducible and attributable to the mechanism actually modified.

**Passages consulted for these developments**: [OpenCV 4.13.0, `camshift.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L218), centroid and moments; the moment interpretation and the factorial plan are project deductions.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-MEANSHIFT-001 — Total mass and centroid convey different evidence

Multiplying every nonnegative backprojection score in a window by the same positive constant leaves its centroid unchanged while changing total mass. A weak diffuse response can therefore point to the same centroid as a strong response. Record both support and mass under the chosen score normalization, with a distinct zero-mass outcome. A converged window position alone does not establish that the target remains visible.

### CV-MEANSHIFT-002 — Moment orientation becomes ambiguous for a round distribution

If the two eigenvalues of the normalized second-moment matrix are nearly equal, its dominant axis is weakly defined. Small changes in scores can rotate the fitted ellipse greatly without much change in the underlying nearly circular distribution. Avoid interpreting that angle as stable object orientation or metric pose. A proposed validation separates center/scale tracking from orientation reliability on elongated and symmetric targets.

### CV-MEANSHIFT-003 — Convergence can strengthen a semantically wrong mode

Two same-color parts can create two backprojection modes. MeanShift moves according to the local score mass, with no built-in physical identity label. More iterations can reduce numerical movement while converging to the wrong part. Test controlled distractors and inspect the mode structure before changing stopping criteria. A geometric motion limit or richer appearance model is a project intervention that needs its own measured tradeoff.

Consulted foundations: [OpenCV 4.13.0, `camshift.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L218): back-projection centroid iteration and moment-based adaptive window.

## Sources and flashcards

### Scientific sources

- [Comaniciu, Ramesh and Meer 2003, Kernel-based object tracking, IEEE TPAMI 25(5)](https://www.cs.ucf.edu/courses/cap6412/2003/Kernel-based%20object%20tracking.pdf) (course-hosted copy): §2.1–2.2 eqs. 2–5, §3 eqs. 6–7 and properties, §4.1 eqs. 8–11 and algorithm, §4.2 eqs. 12–13, basin of attraction and stopping rule, §4.3 eq. 14, §4.4 cost and speed, §5 settings, §6.2 Kalman extension.
- [Comaniciu, Ramesh and Meer 2000, Real-time tracking of non-rigid objects using mean shift, CVPR](https://comaniciu.net/Papers/MsTracking.pdf): preliminary version of the same method.
- [Bradski, US patent 6,394,557 B2, continuously adapting mean shift](https://patents.google.com/patent/US6394557B2/en): window size from the zeroth moment, orientation from second moments, hue thresholds on saturation and value. The Intel Technology Journal paper (1998) could not be retrieved in this pass.

### Implementation sources

- [OpenCV 4.13.0, `modules/video/src/camshift.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L218): `meanShift` (L44–L107) and `CamShift` (L110–L218).
- [OpenCV 4.13.0, `modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp#L64-L107): documented contracts of both functions.
- [OpenCV 4.13.0, `modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L3322-L3360): `calcBackProject`.
- [OpenCV 4.13.0, `samples/python/camshift.py`](https://github.com/opencv/opencv/blob/4.13.0/samples/python/camshift.py#L82-L102): mask thresholds, 16-bin hue histogram, normalization and stopping criteria.

### Related flashcards and references

- [Flashcards](../115-meanshift-camshift.md): CV-MEANSHIFT-001 to 004.
- [CV-SOT](113-tracking-monoobjet.md) for the comparison; [CV-CORRELATION](114-mosse-kcf.md) for template-based tracking.

Drafted by Agent Codex, 2026-10-24. Revision 7, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/115-meanshift-camshift.md).
Revision 8, 2026-11-16: worked example C (IoU ceiling of the ±2σ box and the reading of a 2 × 2 design)
added while deepening CV-MEANSHIFT-004, by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-16-card-depth/115-meanshift-camshift.md).
