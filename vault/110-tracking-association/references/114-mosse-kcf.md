---
id: CV-CORRELATION
type: methode
domaine: d11
poles: ["C", "D", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SOT", "CV-FILTRES"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MOSSE and KCF — tracking with correlation filters

This is the method note for discriminative correlation filters in single-object
tracking. The task contract, the comparison with MeanShift and Siamese trackers and
the benchmark protocols are in [CV-SOT](113-tracking-monoobjet.md); this note
develops how MOSSE and KCF learn, detect, update and fail.

## Problem and data contract

**Task.** From a box given in the first frame, estimate the target's translation in
each later frame by correlating a learned filter with a patch centred on the previous
position, and optionally report how trustworthy the peak is.

**Inputs.**

- MOSSE: a grayscale window with the target's support, $P$ pixels, preprocessed by a
  log transform, normalization to zero mean and unit norm, and a cosine window
  [MOSSE, §3.1]. OpenCV enlarges the box to an efficient DFT size
  [mosseTracker.cpp, L147–L148].
- KCF: a window 2.5 times the target, so that it contains context and negatives
  [KCF, App. A-A], described by raw pixels or by HOG cells of $4\times4$ pixels with
  31 orientation channels [§VIII-A, §VII-A]; the patch has $m\times n$ samples and
  $c$ channels.

**Outputs.** A real response map with the patch's size, in arbitrary units; the
position of its maximum gives the displacement in samples, which becomes frame pixels
after multiplying by the cell size, adding the crop origin and undoing any resize.
MOSSE also returns the peak-to-sidelobe ratio (PSR) [§3.5]. The base methods keep the
box size: neither estimates scale or orientation [MOSSE, §4.2].

**Role in a pipeline.** A short-term, CPU-cheap tracker for an operator-selected or
detector-initialized target, or a propagator between detector calls; it does not
create tracks or re-detect after a long absence (see [CV-SOT](113-tracking-monoobjet.md)).

## Intuition

A correlation filter is a template trained so that sliding it over the training patch
gives a sharp peak exactly at the target centre and low values at every other offset.
Every shifted copy of the patch is therefore a training example: the centred one is
positive and the others, which show the target off-centre with background, are
graded negatives. Correlation becomes an element-wise product in the Fourier domain,
so learning from all shifts and evaluating all offsets costs a few FFTs instead of a
large linear system [MOSSE, §3; KCF, §IV].

*Illustration (constructed example, recomputed by checks/114-mosse-kcf.py).* An
8-sample signal is the base patch, and the regression target is a Gaussian with its
maximum at shift 0. Solving the ridge regression directly over the 8 cyclic shifts and
solving it with three DFTs give the same filter to machine precision. Applied to its
own training patch, the filter peaks at index 0 with response 0.954; applied to the
patch shifted right by $s$ samples, it peaks at index $-s \bmod 8$. The same check
exposes a frequent bug: with the conjugate placed on the wrong factor, the filter is
time-reversed and peaks at index 6 with response 0.788 on its own training patch.

## Prerequisites and competencies

**Required prerequisites**: [CV-SOT](113-tracking-monoobjet.md) for the tracking
contract and [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md)
for convolution and correlation. Ridge regression and its normal equations are in
[CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md); the
Fourier-domain steps are explained below. **Target competencies**: explain the loop
of a tracking filter; distinguish MOSSE and KCF; interpret a PSR; look for
contamination of the model; define an honest comparison of trackers. Related notions
remain alternatives, not implicit dependencies.

## Assumptions, observability and degenerate cases

- **Translation between frames, small relative to the window.** A window of $a$
  target widths represents offsets up to $a/2$ widths because the response is cyclic,
  but keeps the whole target inside only up to $(a-1)/2$ widths: 0.75 for KCF's
  $a=2.5$, 0.5 for OpenCV KCF's $a=2$, and none for a window with the target's support
  (constructed relation, recomputed by checks/114-mosse-kcf.py). The cosine window
  further attenuates the border.
- **Cyclic shifts approximate translations.** Wrapped content appears at the opposite
  edge; padding and the cosine window mitigate the effect without removing it
  [KCF, §IV-B, Fig. 2; MOSSE, §3.1].
- **Slowly varying appearance.** The model follows change only through its update; a
  change faster than the update rate, or an update made on the wrong region, breaks it.
- **Same scale.** The filter is learned at one scale; a large size change spreads the
  peak and lowers its contrast.
- **Kernel compatibility.** Fast kernel training needs a kernel invariant to the same
  permutation of both arguments, such as Gaussian, polynomial or intersection kernels
  [KCF, Theorem 1, Example 2]. Fast kernel correlation by DFTs is derived only for
  dot-product and radial basis kernels; others need a slower sliding-window
  evaluation [§VI-C].

Observability and degenerate cases. A frequency with almost no energy in the training
windows makes the unregularized ratio unstable; MOSSE's sum over several windows and
the regularizer avoid near-zero denominators [MOSSE, §3.3]. A flat response gives a
zero sidelobe deviation and an undefined PSR. A target that left the window still
yields a maximum somewhere, so "peak found" never means "target found".

## Procedure

```text
MOSSE (Bolme et al., Sec. 3)
  init: f_i <- 8 random small affine warps of the first window, preprocessed
        g_i <- Gaussian peak (sigma = 2 px) at the target centre
        A <- sum G_i . conj(F_i);  B <- sum F_i . conj(F_i)       # Fourier domain
  each frame:
        F <- FFT(preprocess(window at previous centre))
        g <- IFFT(F . (A / B));  peak <- argmax g;  move centre to the peak   # A / B is H*
        if PSR(g) < gate: report occlusion or failure; skip the update
        A <- eta G . conj(F_new) + (1 - eta) A
        B <- eta F_new . conj(F_new) + (1 - eta) B                 # F_new at the new centre

KCF (Henriques et al., Sec. VIII-A, Algorithm 1)
  init: x <- features of the padded window (cosine-weighted); y <- Gaussian label
        alphaf <- FFT(y) / (FFT(kernel_correlation(x, x)) + lambda)
  each frame:
        z <- features at the previous position
        response <- real(IFFT(alphaf . FFT(kernel_correlation(z, x))))
        move to argmax(response)
        x_new, alphaf_new <- train at the new position
        x <- (1 - eta) x + eta x_new;  alphaf <- (1 - eta) alphaf + eta alphaf_new
```

Purpose of the steps. The random warps give MOSSE several training windows from a
single frame and make the initial filter stable [§3.4]. Preprocessing reduces the
effect of low contrast and of the artificial boundary [§3.1]. The Gaussian label
rewards a peak at the centre and penalizes offsets smoothly; Gaussian labels also
reduce ringing compared with binary ones [KCF, App. A-A]. The PSR test lets MOSSE
pause during occlusion and resume [MOSSE, abstract and §3.5]. KCF has no failure
test [§VIII-A]; its update interpolates both the dual coefficients and the stored
appearance, which gives the model a memory.

## Mathematics, conventions and units

**Conventions.** $\odot$ is the element-wise product, $^*$ the complex conjugate and a
hat the 2-D discrete Fourier transform (DFT). Responses are in arbitrary units.
Spatial bandwidths are in pixels for raw features and in cells for HOG.

**MOSSE.** With $F_i$ and $G_i$ the DFTs of the preprocessed training windows $f_i$
and of their desired outputs $g_i$, MOSSE minimizes the output error
$\sum_i |F_i\odot H^*-G_i|^2$ [eq. 3]. Each frequency decouples, giving [eq. 5]

$$H^*=\frac{\sum_i G_i\odot F_i^*}{\sum_i F_i\odot F_i^*}.$$

The numerator correlates inputs with desired outputs and the denominator is the
inputs' energy spectrum. A small $\epsilon$ added to that spectrum regularizes the
filter [§3.3]. Online, $A_i=\eta\,G_i\odot F_i^*+(1-\eta)A_{i-1}$,
$B_i=\eta\,F_i\odot F_i^*+(1-\eta)B_{i-1}$ and $H_i^*=A_i/B_i$, with $\eta=0.125$ in
the paper [eqs. 10–12]; recent frames dominate and older ones decay exponentially.

**KCF, linear case.** Ridge regression $\min_{\mathbf w}\sum_i(\mathbf w^T\mathbf x_i-y_i)^2+\lambda\|\mathbf w\|^2$
has the solution $\mathbf w=(X^TX+\lambda I)^{-1}X^T\mathbf y$, which costs
$O(n^3)$ in general [eqs. 1–2, §IV-D]. When the rows of $X$ are all cyclic shifts of
one base sample $\mathbf x$, $X$ is circulant [eq. 6] and the DFT diagonalizes it
[eq. 7], so the solution becomes element-wise [eq. 12]:

$$\hat{\mathbf w}=\frac{\hat{\mathbf x}^*\odot\hat{\mathbf y}}{\hat{\mathbf x}^*\odot\hat{\mathbf x}+\lambda}.$$

The denominator is the power spectrum of the base sample and $\lambda$ plays the role
of MOSSE's ad hoc regularizer [§IV-E]. Where the conjugate sits depends on the DFT
sign convention and on the shift direction. In the constructed check, which uses the
$e^{-2\pi i kt/n}$ convention of NumPy and OpenCV with the shifts of eq. 6, the direct
solve is reproduced with the conjugate on the denominator only; copying eq. 12
literally gives the time-reversed filter of the illustration above. Test any
transcription on a small 1-D case before trusting it.

**KCF, kernel case.** With a kernel $\kappa$, the solution is expressed in dual
coefficients $\boldsymbol\alpha$, and for circulant data [eqs. 17 and 22]

$$\hat{\boldsymbol\alpha}=\frac{\hat{\mathbf y}}{\hat{\mathbf k}^{\mathbf{xx}}+\lambda},\qquad \hat{\mathbf f}(\mathbf z)=\hat{\mathbf k}^{\mathbf{xz}}\odot\hat{\boldsymbol\alpha},$$

where the kernel correlation $\mathbf k^{\mathbf{xx}'}$ has elements
$k_i=\kappa(\mathbf x',P^{i-1}\mathbf x)$, the kernel evaluated at every relative
shift [eq. 18], and $\mathbf f(\mathbf z)$ is the detection response for all shifts of
the test patch $\mathbf z$. For the Gaussian kernel with bandwidth $\sigma$ and $c$
channels [eq. 31],
$\mathbf k^{\mathbf{xx}'}=\exp\!\big(-\tfrac{1}{\sigma^2}(\|\mathbf x\|^2+\|\mathbf x'\|^2-2\mathcal F^{-1}(\sum_c\hat{\mathbf x}_c^*\odot\hat{\mathbf x}'_c))\big)$,
computed in $O(n\log n)$ per channel. Algorithm 1 additionally divides the squared
distance by the number of elements, and Appendix A-A warns that most FFT libraries are
not unitary, so norms computed in the Fourier domain must be rescaled.

**MOSSE and KCF as two sides of one problem.** Element-wise solutions exist either
for several base samples with one channel, solved in the primal (MOSSE), or for one
base sample with several channels, solved in the dual (DCF and KCF), but not both at
once [KCF, §VII-B, App. A-F]. With a linear kernel and one channel, DCF is equivalent
to MOSSE [§VIII-A]. This is why KCF keeps memory by interpolating a single model
rather than by summing past frames like MOSSE.

**Label placement.** The Gaussian label must peak at the top-left element (zero
shift) and wrap around the corners; a label centred in the array shifts the output by
half a window, which some implementations correct with a quadrant swap [App. A-A].

**PSR.** With $g_{\max}$ the peak and $\mu_{sl}$, $\sigma_{sl}$ the mean and standard
deviation of the sidelobe, which is the response without an $11\times11$ window around
the peak [MOSSE, §3.5],

$$\mathrm{PSR}=\frac{g_{\max}-\mu_{sl}}{\sigma_{sl}}.$$

The paper reports 20–60 under normal tracking and about 7 at occlusion or failure,
and notes that the PSR of its naive filter, which stays between 3 and 10, does not
predict track quality [§3.5]. For a peak of 0.8 with sidelobe mean 0.2 and deviation
0.1, PSR $=(0.8-0.2)/0.1=6$ (card CV-CORRELATION-003). The PSR is unchanged by
$r'=ar+b$ with $a>0$ on the same support.

*Worked example B (constructed, recomputed by checks/114-mosse-kcf.py).* A response of
98 sidelobe values alternating 0.1 and 0.3 (mean 0.2, deviation 0.1) and one peak of
1.0 gives PSR 8.0 when the peak is excluded, as in the paper, but 6.2 when the mean
and deviation are computed over the whole map, peak included, as OpenCV 4.13's legacy
MOSSE does. A threshold is therefore attached to one definition of the statistic.

## Parameters and tuning

| Parameter | Paper value | OpenCV 4.13 value | Effect and interactions |
| --- | --- | --- | --- |
| Window size | MOSSE: target support; KCF: 2.5 × target [App. A-A] | MOSSE: box enlarged to a DFT size; KCF: 2 × box [trackerKCF.cpp L214–L218] | Capture range and context against distractors and cost; KCF speed depends directly on the tracked region's size [§VIII-C] |
| Update rate $\eta$ | MOSSE 0.125 [§3.4]; KCF 0.075 raw, 0.02 HOG [Table II] | MOSSE 0.2; KCF `interp_factor` 0.075 | Adaptation against memory; with a gate, a higher rate is safer ([update memory](113-tracking-monoobjet.md)) |
| Regularization | MOSSE $\epsilon$, near 0.1 in the initialization study [§3.3, Fig. 4]; KCF $\lambda=10^{-4}$ | KCF `lambda` 1e-4 | Stabilizes low-energy frequencies; depends on feature scaling |
| Label bandwidth | MOSSE $\sigma=2$ px [§3.2]; KCF $\sqrt{mn}/10$ [Table II] | MOSSE $\sigma=2$; KCF `output_sigma_factor` 1/16 of $\sqrt{wh}$ | Narrow labels sharpen the peak but penalize small misalignment |
| Kernel bandwidth $\sigma$ | 0.2 raw, 0.5 HOG [Table II] | `sigma` 0.2 | Smaller values make the kernel more selective |
| Features | MOSSE gray; KCF raw or HOG with 4-pixel cells | KCF gray plus compressed color names (`desc_npca`, `desc_pca`, `compressed_size` 2) | HOG cells make DFTs smaller and quantize the peak |
| Confidence gate | MOSSE PSR near 7 [§3.5]; KCF none | MOSSE PSR 5.7 on the whole map; KCF `detect_thresh` 0.5 on the raw maximum | A threshold belongs to one score definition (example B) |
| Initialization | MOSSE: 8 random affine perturbations [§3.4] | MOSSE: 8 random warps | Stability of the first filter |

Tuning approach (project method). On sequences from the deployment domain kept apart
from the test set: (1) size the window from measured per-frame displacement relative
to target size, using the inside-the-window relation of the assumptions; (2) choose
features and the label bandwidth on sequences without occlusion, watching centre
error; (3) sweep $\eta$ jointly with the gate on sequences with occlusions and
distractors, watching failures, false recoveries and the logged update crops;
(4) recalibrate the gate after any change of implementation or features.

## Properties and limits of guarantees

- **Exact closed form for a virtual training set.** The Fourier solution is the exact
  ridge-regression solution for all cyclic shifts (Example A), not for the real
  translations of the scene; nothing guarantees that the peak lies on the target.
- **Translation only.** The base filters estimate position; scale and orientation
  changes are not modelled [MOSSE, §4.2], and OpenCV's `TrackerKCF` returns a box of
  constant size [trackerKCF.cpp, L363–L367].
- **Kernels.** The Gaussian kernel gave KCF a clear gain over the linear DCF on raw
  pixels (56.0% against 45.1% precision at 20 px), while with HOG features the two
  were close (73.2% against 72.8%) [KCF, Table I, OTB 50 sequences]. A kernel adds
  non-linearity in feature space; it does not enlarge the search or make the score a
  probability.
- **Illumination.** The log transform and normalization of MOSSE reduce sensitivity
  to low contrast [§3.1]; they do not model shadows or saturation.
- **Adaptation.** The running average follows appearance change and, by the same
  mechanism, absorbs occluders; see card CV-CORRELATION-004 and the update-memory
  example in [CV-SOT](113-tracking-monoobjet.md).
- **PSR.** It is a contrast statistic, invariant to positive affine rescaling of the
  response on a fixed support, and not a calibrated probability of identity.

## Cost and implementation

- **MOSSE**: $O(P\log P)$ per frame for $P$ pixels, from the FFTs of correlation and
  update [§4.3]. Reported: about 250 updates/s in the original Python implementation
  and a median of 669 updates/s after moving slow parts to C, with a $64\times64$
  window on one core of a 2.4 GHz Core 2 Duo [§4.3].
- **KCF**: $O(n\log n)$ per channel for $n$ samples of the padded window, against
  $O(n^3)$ for a generic ridge regression [§IV-D]. Reported on the 50-sequence OTB set,
  in Matlab with feature computation included: KCF 172 and DCF 292 frames/s with HOG,
  KCF 154 and DCF 278 frames/s with raw pixels, against 615 frames/s for the original
  MOSSE tracker on its smaller region [§VIII-C, Table I]. HOG can be faster than raw
  pixels because $4\times4$ cells make the DFTs smaller [§VIII-C].
- Cost drivers: window area, number of channels, kernel type and the FFT library;
  speeds from different languages and hardware are orders of magnitude, not a ranking.

### OpenCV 4.13 contracts

Read in the 4.13.0 sources on GitHub (docs.opencv.org returned HTTP 403); no code was
executed for this note.

- `cv::TrackerKCF` (opencv_contrib `tracking`): `init(image, box)` and
  `update(image, box) -> bool` [tracking.hpp, L90–L149]. Defaults: `detect_thresh`
  0.5, `sigma` 0.2, `lambda` 1e-4, `interp_factor` 0.075, `output_sigma_factor` 1/16,
  `resize` true with `max_patch_size` $80\times80$, `split_coeff` true,
  `wrap_kernel` false, gray non-compressed and color-names compressed descriptors,
  `compressed_size` 2, `pca_learning_rate` 0.15 [trackerKCF.cpp, L900–L918]. The
  region is doubled around the box [L214–L218]. When the response maximum is below
  `detect_thresh`, `update` returns `false` before moving the region or updating the
  model [L353–L357]; otherwise appearance and coefficients are interpolated with
  `interp_factor` [L395–L396, L457–L458].
- `cv::legacy::TrackerMOSSE`: grayscale input; window equal to the box enlarged by
  `getOptimalDFTSize`; preprocessing $\log(1+I)$, normalization and a Hanning window;
  a Gaussian label with $\sigma=2$; eight random warps at initialization; learning
  rate 0.2; PSR from the mean and standard deviation of the whole response, compared
  with 5.7; below it `update` returns `false` without moving or updating
  [mosseTracker.cpp, L31–L33, L79–L109, L147–L185, L190–L225].
- opencv_contrib also ships `TrackerCSRT`, a correlation filter "with channel and
  spatial reliability" [tracking.hpp, L31–L34]; its mechanism is not covered here.

## Evaluation and controlled variation

The benchmark protocols (OTB precision and success, VOT resets, LaSOT long sequences)
are summarized in [CV-SOT](113-tracking-monoobjet.md). KCF was evaluated by one-pass
evaluation on the 50 OTB sequences with the precision curve, reporting precision at a
20 px centre-error threshold. The authors chose it over average centre error, which
depends on where a lost tracker wanders, and over overlap, which heavily penalizes
trackers that do not follow scale [KCF, §VIII-B]. Attribute subsets such as occlusion
and non-rigid deformation are reported separately [§VIII-D]. That choice favors
scale-blind filters; an overlap-based comparison can rank them differently.

**Proposed baseline and controlled variation (not executed).**

- *Data*: held-out sequences from the deployment domain with occlusions, crossings
  with similar objects and per-frame absence labels.
- *Baseline*: KCF with fixed parameters that updates at every frame, one-pass
  evaluation from the ground-truth first box, no reset.
- *Controlled variation*: the same tracker, sequences and initialization, but the
  update is skipped when the PSR, computed with a stated definition, falls below a
  threshold chosen on separate sequences.
- *Measurements*: success AUC, precision at 20 px, number of zero-overlap events,
  frames to recovery after each occlusion, false recoveries on a distractor, number of
  skipped updates, and per-frame latency.
- *Reading*: fewer failures after occlusion with similar precision before it supports
  contamination as the failure mechanism; slower adaptation to legitimate appearance
  change is the expected cost.

**Measurement limits.** The 20 px threshold is in pixels and depends on target size
and resolution. One-pass and reset-based scores are not comparable. Gains measured on
a few dozen sequences depend on their attribute mix. Speeds depend on window size,
features and implementation.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Box drifts onto the background after an occlusion | Updates made on the occluder | Compare a saved pre-occlusion model with the current one; replay with updates frozen from the occlusion onset | Gate the update on PSR, lower $\eta$, declare the loss (card CV-CORRELATION-004) |
| Box jumps to a nearby similar object | Competing peak inside the window | Inspect the response map for a second peak before the jump | Smaller window, motion prior, re-detection with a discriminative model |
| Lost after a fast motion | Displacement beyond the part of the window that contains the target | Measured displacement relative to the inside-the-window limit | Larger padding, motion prediction, higher frame rate |
| Peak in the right place but box size wrong | No scale estimation | Precision high, overlap low on scale-change sequences | Scale-adaptive variant or another tracker family |
| Systematic offset or half-window jump | Label centred instead of top-left, missing quadrant swap, or wrong crop-to-frame mapping | Synthetic translation of a known amount | Fix the label or the mapping [KCF, App. A-A] |
| Tracker moves the wrong way or the peak never sits at zero on the training patch | Conjugate on the wrong factor for the DFT convention | Apply the filter to its own training patch (Example A) | Correct the formula for the library's convention |
| Kernel values saturate or vanish when the patch size changes | Non-unitary FFT scaling in the Gaussian kernel | Compare the kernel's distances computed in the spatial and Fourier domains | Normalize as in Algorithm 1 and App. A-A |
| PSR never separates success from failure | Naive filter, different PSR definition or features | PSR distribution on frames labelled good and failed | Recalibrate the gate for this implementation (example B) |

## Alternatives and applications

- Prefer MOSSE when the target fits in a small grayscale window, the CPU budget is
  tight, and a PSR-based pause during occlusion is enough.
- Prefer KCF or DCF with HOG or color-names features when texture or color
  discriminates the target from its surroundings better than raw intensity, at a
  moderate extra cost.
- Prefer a scale-adaptive correlation filter, such as OpenCV's CSRT, or a Siamese
  tracker when scale changes matter; prefer [MeanShift/CamShift](115-meanshift-camshift.md)
  for a distinctive color blob; prefer detection plus association when several
  objects or re-detection after long absence are expected ([CV-SOT](113-tracking-monoobjet.md)).

Industrial uses (project reasoning): propagating a part's box on a conveyor between
detector frames on an embedded CPU, where window size and a PSR gate are tuned from
measured motion; following an operator-selected target on a PTZ camera, where a
reliable loss signal matters more than mean overlap.

## Guided reasoning and proposed checks

These constructed cases develop cyclic shifts, the search window and the risk of model contamination. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-CORRELATION-001

**Working question**: How does a correlation filter initialized from a box track the target in the next frame?

**Reference answer**: Extract a search region and its features, correlate with the model, locate the peak, check reliability and then adapt the model only according to the chosen policy. The answer is a location peak, not a semantic class.

**Interpretation of the answer**: Each candidate shift in the search region receives a score of similarity to the model. The peak locates the preferred hypothesis, but its contrast and the presence of competitors must be examined before an update. The search area already expresses a hypothesis about possible motion.

**Constructed example**: A target moving beyond this area can leave the background as the best available peak. Learning this background then turns a loss of localization into a persistent drift of the model. Define a loss and recovery policy, then test it on large motions and occlusions. Correlation speed is useful only if the search and update assumptions fit the need.

### Case linked to CV-CORRELATION-005

**Working question**: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?

**Reference answer**: Initialization and reset protocol, sequences, losses, overlap and center error, as well as full latency. A restart after error changes the evaluated task.

**Why resets change the task**: A reset provides the tracker with a new location after a failure. A system without this help must find the target or remain lost. The two protocols therefore do not expose the model to the same accumulation of errors or the same amount of external information.

**Proposed comparison**: Keep sequences, initialization, presence rule and loss criterion. Report failures and recovery periods in addition to location measurements. An average calculated only on successful frames can favor a method that abandons difficult cases. For a product, include the cost and time of the actual recovery procedure, whether automatic or human. Scores remain interpretable only with this evaluation contract.

**Source consulted for this pass**: [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf), §§3–4, filter and tracking. The remaining developments are in the [flashcards](../114-mosse-kcf.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-CORRELATION-001

**Situation**: How does a correlation filter initialized from a box track the target in the next frame?

**From the peak to the image**: The response is computed in the coordinates of the patch or of its features. Converting the offset of the maximum to the image requires the origin of the crop, its resizing and any stride. A circular correlation convention also requires interpreting near-edge indices as appropriate signed offsets. An error here can produce a jump despite a correctly computed peak. Check a known synthetic translation and map back to image coordinates before setting the confidence threshold. Subpixel localization refines the peak estimate; it does not guarantee equivalent physical accuracy on real images.

### CV-CORRELATION-002

**Situation**: What do cyclic shifts and kernels give KCF compared with a linear filter such as MOSSE?

**Structured regression**: a regularized linear regression solves $\min_w\|Xw-y\|^2+\lambda\|w\|^2$. If the rows of $X$ are the cyclic shifts of the same signal, the circulant structure makes it possible to diagonalize the corresponding operations by Fourier transform. In a kernel regression, the matrix of similarities must keep a compatible structure. This explains the efficiency without equating a kernel with a deep network. The regularization parameter stabilizes learning according to the feature scale; it does not compensate for a target missing from the patch or an artificial edge hypothesis ill-suited to the scene.

### CV-CORRELATION-003

**Situation**: A response has a peak of 0.8, an off-peak mean of 0.2 and an off-peak standard deviation of 0.1. What is the PSR, and what does it mean?

**Effect of a distractor**: If a second peak enters the area used to calculate the off-peak mean and standard deviation, it can change the PSR of the first peak, even if its height remains the same. The size of the excluded area and the edges of the patch therefore participate in the definition of the score. A positive affine transformation $r'=ar+b$, with the same support and $a>0$, ideally retains the PSR, because numerator and standard deviation are multiplied by $a$. On the other hand, clipping, quantizing or changing the support can break this invariance. The score is therefore comparable only with an identical calculation procedure and a threshold validated in its context.

### CV-CORRELATION-004

**Situation**: A correlation-filter tracker works before an occlusion, then persistently tracks the background. Which update error should be tested?

**Separate search and learning**: Freezing updates retains a target model, but does not change the region being searched. After a long occlusion or a large shift, the target may return elsewhere and remain untraceable despite an intact model. Compare two separate interventions: freezing the model with unchanged search, then an expanded search policy or detection with the same model. Measure false returns on distractors and recovery times, without using the true position to silently reset. This ablation distinguishes contamination, loss of spatial coverage and appearance ambiguity, which can produce a similar final box on the background.

### CV-CORRELATION-005

**Situation**: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?

**Measure of success**: A curve can report, for each threshold $\tau$, the proportion of frames where the IoU of the target exceeds $\tau$, under an announced presence policy. The area under this curve describes something other than the accuracy of the center at a fixed pixel threshold. Two boxes of the same center but of very different sizes can have a good center error and a bad IoU. The resets still change which periods are evaluated and what information is provided. Publishing the rules with the curve and the losses makes it possible to compare tradeoffs without retaining only the frames where the tracker has succeeded.

**Passages consulted for these developments**: [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf), §§3.1–3.2, preprocessing and filter learning; [Henriques et al., KCF](https://arxiv.org/html/1404.7584v3), §IV, regression and circulant structure; the mathematical complements and protocols are project constructions.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-CORRELATION-001 — A search crop defines the capture region

If the target moves entirely outside the sampled search crop, a response maximum still exists inside that crop but need not correspond to the target. A reliability check and an explicit failure outcome are therefore essential. Evaluate search size against expected frame-to-frame motion and distractors. A larger crop increases candidate context and computation and can introduce stronger competing peaks; it is not a free guarantee of reacquisition.

### CV-CORRELATION-002 — Cyclic training creates artificial boundary examples

A circular shift wraps one side of a patch onto the other, which can create an artificial seam absent from a physical translation. Windowing and search-region design reduce some boundary effects under their assumptions. The Fourier diagonalization exploits this structured training set; it does not make arbitrary independent patches circulant. Compare border-crossing and large-displacement cases when testing whether the efficient model remains suitable for the target sequence.

### CV-CORRELATION-003 — PSR is invariant to some response rescalings

If the response map is transformed by $r^{\prime}=ar+b$ with $a>0$ and the sidelobe region is unchanged, peak-minus-mean and standard deviation both scale by $a$, leaving PSR unchanged. A constant map instead has zero sidelobe standard deviation and requires a defined policy. This constructed relation explains why raw peak height and PSR measure different things, and why neither is a calibrated probability of correct identity.

### CV-CORRELATION-004 — A learned distractor can make confidence self-reinforcing

Once the update absorbs background appearance, later correlation peaks may look reliable relative to that altered model. Compare against a saved pre-occlusion model and inspect the update history before treating a high response as confirmation. A proposed intervention separates freezing updates from expanding search and reinitialization, since each changes a different mechanism. Evaluate false recovery as well as overlap after a successful reacquisition.

Consulted foundations: [KCF](https://arxiv.org/html/1404.7584v3): §IV circulant ridge regression and Appendix A-F MOSSE; [MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf): §§3.2–3.5 filter adaptation and PSR.

## Sources and flashcards

### Scientific sources

- [Bolme et al. 2010, MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf): abstract; §3 introduction (eq. 1); §3.1 preprocessing; §3.2 eqs. 3–5 and $\sigma=2$; §3.3 regularization and Fig. 4; §3.4 initialization and eqs. 10–12; §3.5 PSR; §4.2 scale and orientation; §4.3 timing.
- [Henriques et al. 2015, KCF](https://arxiv.org/html/1404.7584v3): §IV-A to §IV-E (eqs. 1–12, complexity, relation to MOSSE); §V-B and §V-C (Theorem 1, eqs. 16–22); §VI-A to §VI-C (eqs. 23–30); §VII-A and §VII-B (eqs. 31–32); §VIII-A (pipeline, Algorithm 1); §VIII-B (precision metric); §VIII-C (Table I, timing); Appendix A-A, A-F and Table II.

### Implementation sources

- [opencv_contrib 4.13.0, `modules/tracking/include/opencv2/tracking.hpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/include/opencv2/tracking.hpp#L31-L149): `TrackerCSRT` description and `TrackerKCF` with `Params`.
- [opencv_contrib 4.13.0, `modules/tracking/src/trackerKCF.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/trackerKCF.cpp#L900-L918): defaults (L900–L918), padding (L214–L218), gate (L353–L357), constant box size (L363–L367), interpolation (L395–L396, L457–L458).
- [opencv_contrib 4.13.0, `modules/tracking/src/mosseTracker.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/mosseTracker.cpp#L31-L225): constants, preprocessing, PSR, initialization and update.

### Related flashcards and references

- [Flashcards](../114-mosse-kcf.md): CV-CORRELATION-001 to 005.
- [CV-SOT](113-tracking-monoobjet.md) for the comparison and protocols; [CV-MEANSHIFT](115-meanshift-camshift.md) for color-distribution tracking.

Drafted by Agent Codex, 2026-10-24. Revision 6, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/114-mosse-kcf.md).
