---
id: CV-FILTRES
type: methode
domaine: d03
poles: [A, B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 6
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Filters, gradients and pyramids

## Problem, data and assumptions

Mitigate certain disturbances without destroying the structures needed for the pipeline. Input: image, type/range and assumed noise; Output: filtered or derived image. Edge conditions and kernel scale are part of the algorithm.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Gaussian: linear spatial weighted average. Median: Nonlinear order statistics useful for pulses. Bilateral: weight of proximity and photometric similarity. Differentiation amplifies certain high frequencies; smoothing before differentiation selects an analysis scale.

## Mathematics, conventions and units

The discrete convolution writes $J(p)=\sum_q K(q)I(p-q)$, with normalized kernel for an average. For a scalar intensity, in a Gaussian bilateral, the weight is proportional to $\exp(-\|p-q\|^2/(2\sigma_s^2)-|I(p)-I(q)|^2/(2\sigma_r^2))$ and then renormalized. $\sigma_s$ is in pixels; $\sigma_r$ in the unit of intensity. For $I'=I/255$, maintaining photometric weights requires $\sigma_r'=\sigma_r/255$. The color case replaces the scalar difference with a distance in the chosen color space.

## Parameters and properties

Size, sigma, edge and photometric range must be fixed. A relatively contour-preserving filter does not retain all the small defects. A pyramid requires proper filtering before decimation.

## Cost and implementation

The separable Gaussian allows two 1D passes; a naive bilateral visits each neighbor of the support for each pixel. No benchmark or OpenCV call executed here.

## Evaluation and controlled variation

Proposed variation: same image with Gaussian noise then impulse, fixed protocol. Compare residual noise and recall a small defect; optimize the quality of the downstream pipeline, not just a visually smooth image.

## Failure modes and diagnosis

Contours disappear: inspect filter scale and detail contrast. A shade changes at the edge: check padding and color space before changing the network.

## Alternatives and applications

Choosing the noise pattern and task; learned restoration or specialized denoise may help but need to be compared to a simple baseline.

## Guided reasoning and proposed checks

These constructed cases develop support effect, bilateral units and subsampling. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FILTRES-001

**Question of work**: Why can a median filter suit impulse noise without universally replacing Gaussian filtering?

**Reference Response**: It rejects local extreme values via order, while the Gaussian average; the effect depends on noise and structures.

**Concrete mechanism**: in a neighborhood where most intensities are about 100 and a value is 255, an average propagates the influence of this pulse at its output, while a median can remain close to the majority level. On the other hand, a very thin real scratch can also become a minority in the neighborhood and disappear. The filter does not know how to distinguish a parasitic pulse from a useful defect on their size alone.

**Proposed choice**: compare multiple media on a batch containing noise, edges and critical details. Keep the downstream steps identical, and then measure missed defects and location errors. Larger support increases the scale of image modification. The median does not describe itself as a linear convolution; the Gaussian achieves a weighted average whose frequency behavior helps to build pyramids. These differences explain the choice, without establishing a universal ranking.

### Case linked to CV-FILTRES-004

**Question of work**: Why is simply retaining every other pixel insufficient for constructing a matching pyramid?

**Reference Response**: Decimation without filtering can fold high frequencies into aliasing and change observed structures.

**Chain of reasoning**: Reducing the grid decreases the maximum representable spatial frequency. A rapid alternation of intensities can then be interpreted as a slower pattern if one decimates directly. Pre-smoothing attenuates components that are incompatible with the new grid; decimation then reduces the number of samples. The prefilter therefore chooses what is stored before the loss of resolution.

**Consequences for Matching**: The gradients and extrema used as features change if the texture is folded. Two views of the same object can produce unstable descriptors simply because of resampling. In a constructed test, compare the number of geometrically verified matches on a reduced calibration target with and without a prefilter, with constant detector. Better stability is not a perfect invariance at scale: too small a detail ends up disappearing even with a properly filtered pyramid.

**Documentary reference for this pass**: [OpenCV 4.13, Smoothing Images](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html), Median Blur and Bilateral Filter. The other developments are in the [flashcards](../31-filtrage-gradients.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FILTRES-001

**Situation**: Why can a median filter suit impulse noise without universally replacing Gaussian filtering?

**Linking the operation to the noise**: for a normalized linear filter $J(p)=\sum_q k_q I(p-q)$ and independent noises of variance $\sigma_n^2$, the output variance is $\sigma_n^2\sum_q k_q^2$. A uniform average of nine samples therefore divides it by nine, under these assumptions, but also mixes their signals. The median depends on the rank of the values: an isolated pulse can stay away from the central rank without drawing the result towards it. Noise correlations, edges and fine details change these tradeoffs. The Gaussian is separable: two convolutions 1D replace a convolution 2D for the same kernel produced, without making a median equivalent to this operation.

### CV-FILTRES-002

**Situation**: When intensities are normalized from [0,255] to [0,1], what changes for a bilateral filter's photometric sigma?

**Complete form and role of standardization**: for a pixel $p$, write $J(p)=\sum_q w_{pq}I(q)/\sum_q w_{pq}$, with $w_{pq}=\exp(-\|p-q\|^2/(2\sigma_s^2))\exp(-(I(p)-I(q))^2/(2\sigma_r^2))$. The first factor favors nearby neighbors, the second one those whose intensity resembles that of the center. The denominator adapts the sum of the weights to the local content; without it, an edge could simply darken the result by rejecting neighbors. The weights depend on the image: it is a non-linear operation, even if the output looks like an average. The noise of the central pixel also influences which neighbors will be considered similar; preserving a contour remains conditional.

### CV-FILTRES-003

**Situation**: Denoising improves PSNR but removes scratches. How should this preprocessing be evaluated?

**Make the compromise quantifiable**: $PSNR=10\log_{10}(L^2/MSE)$, with $L$ the maximum of the range announced and $MSE$ the average squared errors against a reference. Modifying $L$ or normalization without consistency changes the score. If a defect occupies a fraction $p$ of the pixels and undergoes an amplitude error $a$, its contribution to the MSE is only $pa^2$: it can remain small even if all its pixels are lost. Then measure the probability of detecting a defective part and the frequency of false alarms per part, with rules of association and constant thresholds. The reference to PSNR must itself be justified; a noisy image used as "clean" changes the problem.

### CV-FILTRES-004

**Situation**: Why is simply retaining every other pixel insufficient for constructing a matching pyramid?

**Building the Levels**: A Gaussian pyramid follows $I_{\ell+1}(x,y)=(G_\ell*I_\ell)(2x,2y)$ in an example of decimation by two. Coordinates are approximately converted by $p_0=2^\ell p_\ell$, respecting the exact pixel center conventions. A five-ray window at the $\ell=3$ level covers about forty pixels of radius in the initial image: its physical support has changed. This is useful for bringing back a large displacement in a local capture area, but it can mix objects or eliminate a fine structure. Propagate coordinates, descriptor radius, and geometric thresholds in the same system of units, rather than treating levels as independent images.

**Passages consulted for these developments**: [OpenCV 4.13, Smoothing Images](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html), Theory, Gaussian, Median and Bilateral Filter; [OpenCV 4.13, PSNR/SSIM](https://docs.opencv.org/4.13.0/d5/dc4/tutorial_video_input_psnr_ssim.html), PSNR definition; built rarity example; [OpenCV 4.13, Image Pyramids](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html), Gaussian Pyramid, filtering and decimation.

## Sources and flashcards

- [Tomasi and Manduchi 1998, Bilateral Filtering, §§2 – 3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf).
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).

The defect recall protocol rather than PSNR alone is a project evaluation choice, with no experimental results announced.

- [OpenCV, smoothing images : Theory](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html).
- [Related flashcards](../31-filtrage-gradients.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
