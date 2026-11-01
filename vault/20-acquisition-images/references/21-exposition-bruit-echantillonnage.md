---
id: CV-ACQUISITION
type: methode
domaine: d02
poles: [A, B, C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 9
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Exposure, noise, color and sampling

## Problem, data and assumptions

Get an image whose useful details are measurable. Inputs: Stage, lighting, optics, exposure and sensor; Output: sampled intensities with known saturation, noise and coordinate frames. A network does not automatically retrieve information destroyed by the acquisition.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

The photons become a noise measurement and then digitized. Exposure, aperture, lighting and gain have different effects. Filtering before decimation limits aliasing; applying a gamma photometric operation is not equivalent to applying it in linear light.

## Mathematics, conventions and units

Simplified model: blur $b_{px}\approx v_{px}t_e$, image speed in px/s and exposure in s. The ideal photonic noise has variance equal to the average number of photoelectrons; it does not sum up all the noise of the sensor. EMVA 1288 (§2.4, equations 13 – 14) adds a reading noise variance $\sigma_d^2$ to e⁻² (its standard deviation $\sigma_d$ is in e⁻), and a quantization noise $\sigma_q^2=1/12$ DN². $\eta$ is the quantum efficiency, $\mu_p$ the average number of photons received per pixel during exposure; $\eta\mu_p$ is the average number of photoelectrons. $K$ is the system gain in DN/e⁻, and $\sigma_q^2$ is the quantification variance in DN². The model assumes an unsaturated linear response at a fixed operating point. The SNR is written $\eta\mu_p/\sqrt{\sigma_d^2+\sigma_q^2/K^2+\eta\mu_p}$ (§2.6, equation 21). Excluding quantification, the gain system $K$ cancels itself out: increasing the gain does not change the SNR, while doubling the photons multiplies it by $\sqrt2$ in photonic regime and up to 2 in read noise regime (equation 22). A stronger gain reaches the maximum numerical value with fewer electrons, hence a reduced saturation capacity (§2.7). Example of the project, $\sigma_d=5$ e⁻: SNR 8,9 to 100 e⁻, 13,3 to 200 e⁻, unchanged if we double $K$. Nyquist requires less than half the sampling for a band-limited signal, without guaranteeing detection of any two-pixel faults. Reducing an image without a prefilter adapted to the reduction factor folds the high frequencies in the result. Parmar et al. (2022, §§2 and 3.2) recall this, and observe aliasing in the OpenCV, TensorFlow and PyTorch configurations studied in 2022, opposite the adaptive filters of PIL (§1, §6.3). This result is not a timeless property of a library: check API, version, interpolation and antialiasing. For example, `torchvision.transforms.Resize` 0.24 enables `antialias=True`, the default value introduced in 0.17.

## Parameters and properties

Check range, bit depth, gamma, BGR/RGB, white balance and saturation. Digital gain does not create photons. Rolling shutter and exposure time are two distinct temporal dimensions. To brighten an image, doubling the lighting doubles the signal in the unsaturated linear model without lengthening the blur, unlike a longer exposure.

## Cost and implementation

Resolution and sensor throughput require transfers and calculation; measure the full cost. No hardware capture executed; equations are announced models, not universal camera properties.

## Evaluation and controlled variation

Analytical variation: doubling the exposure at constant image speed doubles the expected blur. On reserved images, compare sharpness and saturation before/after, with controlled lighting. A better average intensity can mask a useful loss of resolution.

## Failure modes and diagnosis

Failure on fast parts: Measure blur, saturation and contrast at critical locations before retraining. A changing pattern after resize can indicate aliasing and not semantic drift.

## Alternatives and applications

Synchronized lighting, shorter exposure, adapted optics or different cadence: arbitrate signal, blur, heat, cost and line constraints.

## Guided reasoning and proposed checks

These constructed cases develop exposure, noise and sampling related to the task. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ACQUISITION-001

**Question of work**: An image detail moves at 800 px/s during a 5 ms exposure. What motion blur is expected under a uniform-motion model?

**Reference Response**: About 4 px: 800 × 0,005. Doubling the exposure would give 8 px in this model.

**Physical reading and built example**: The pixel receives light throughout the exposure, so it adds up the successive positions of the detail. The product $v_{px}t_e$ is a length in the image, not a distance in the world. For a two-pixel wide defect, a four-pixel trail can mix its signal with the background, even if the image retains proper brightness. A compensation for moving between frames does not automatically return this mixture inside a frame.

**Decision under constraint**: to aim at the most one pixel of displacement with the same speed, the model gives $t_e\le1/800$ s, or 1,25 ms. It's an analytical budget, not a guarantee of detection. Reducing exposure requires reconsidering lighting and noise. Measure movement in the useful area: an average speed over the entire image can hide a faster detail.

### Case linked to CV-ACQUISITION-004

**Question of work**: Which image checks are needed when a transferred model fails despite no apparent change in the scene?

**Reference Response**: Check color order, range/normalization, gamma, bit depth, exposure and saturation in the actual received string.

**Why these checks separate the causes**: Two tables of the same shape can represent different colors or physical quantities. A red channel interpreted as blue changes the learned contrasts; an additional division by 255 changes the scale; an entire passage can clip values. A visualization that automatically adjusts its contrast can make these paintings almost identical to the eye.

**Proposed Reproducible Investigation**: choose a sample image, keep its original file and record, at each step, shape, type, minimum, maximum and values of a few known pixels. Then compare the tensor actually received by the model with that of the drive chain. Test only one correction at a time. An improvement after re-compliance supports a pre-processing cause; it does not exempt the evaluation of other images and difficult cases of the new sensor.

**Documentary reference for this pass**: [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf), §§2.4, 2.6 and 2.7, noise and signal model. The other developments are in the [flashcards](../21-exposition-bruit-echantillonnage.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ACQUISITION-001

**Situation**: An image detail moves at 800 px/s during a 5 ms exposure. What motion blur is expected under a uniform-motion model?

**Model that produces this calculation**: for a constant image translation, an ideal $I_0$ image gives a standardized observation $I_b(x)=t_e^{-1}\int_0^{t_e}I_0(x-v_{px}t)\,dt$, with $x$ in pixels, $t$ in seconds and a rectangular exposure of duration $t_e>0$. This is an average over a $|v_{px}|t_e$ length segment: it explains why blurring depends on speed during exposure, not just the number of frames per second. The formula here assumes a unique and neglectful optical direction, noise and saturation. In perspective, two depths can have different image speeds: a blur budget established on the background does not necessarily protect the part.

### CV-ACQUISITION-002

**Situation**: An inspection image is too dark. You can double camera gain or double the received light by increasing exposure time or illumination. How does each option affect SNR, motion blur and saturation?

**Separate the regimes**: noting $N$ as the average of useful electrons, the simplified model becomes $SNR=N/\sqrt{N+\sigma_d^2}$ when the quantification is negligible. At low $N$, the denominator varies little and doubling the photons can almost double the SNR; at large $N$, it grows as $\sqrt N$ and the gain tends towards $\sqrt2$. For a defect, also examine the contrast between defect and background: illuminating more can saturate the background before obtaining the necessary contrast. An analog gain placed before certain noise sources can have a different real behavior than a simple digital scale change; the model and measurements must specify the stage concerned.

### CV-ACQUISITION-003

**Situation**: A fine pattern changes appearance abruptly after downsampling. What should be checked before blaming the model?

**Example built frequency**: A sine wave of frequency 0,4 cycle per pixel of origin exceeds the limit of 0,25 for a reduction of a factor of two. After decimation, it corresponds to 0,8 cycle per final pixel, indistinguishable on this grid with a folded frequency of 0,2 cycle per final pixel. The observed pattern is therefore an ambiguity of sampling, not a real movement. The prefilter must attenuate beyond the new Nyquist frequency before discarding the samples. Its support depends on the reduction factor; keeping only the name "bilinear" does not fully describe this treatment. This reasoning is an analytic case on a sinusoid, not a result on the network.

### CV-ACQUISITION-004

**Situation**: Which image checks are needed when a transferred model fails despite no apparent change in the scene?

**Distinguish normalization and linearization**: Divide a value sRGB by 255 places it in a numeric range; this does not remove its transfer curve. For a normalized sRGB component $c>0,04045$, its relative linear value is $c_{lin}=((c+0,055)/1,055)^{2,4}$. Thus, $c=0,5$ represents about 0,214 in linear, and not 0,5. Applying this conversion to an already linear input would be another mistake. Document successively decoding, channel order, photometric transfer, resize and then standardization of the tensor. An equality of form or of minimum/maximum does not demonstrate the equality of the intermediate values or their physical sense.

**Passages consulted for these developments**: [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf), §§2.4, 2.6 – 2.7, signal, SNR and saturation; [sRGB, ICC interpretation](https://www.w3.org/Graphics/Color/srgb), §§A.8 and B.1, transfer function and reverse.

## Sources and flashcards

- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html). The tutorial describes Gaussian blur before decimation, not aliasing.
- [Parmar, Zhang and Zhu 2022, On Aliased Resizing and Surprising Subtleties in GAN Evaluation, CVPR, §§1 – 3.2 and 6.3](https://arxiv.org/abs/2104.11222): Nyquist criterion, prefilter and resize conventions depending on the library.
- [sRGB, §§A.7 – A.8 and B.1, linear conversion and transfer function](https://www.w3.org/Graphics/Color/srgb).

The $b_{px}=v_{px}t_e$ calculation is a kinematic deduction of the project for a constant image speed; EMVA documents the sensor, not this blur formula. The check training/inference coherence is a project approach.

- [EMVA1288 Linear 4.0, 16 June 2021, §2.4, equations 13 – 15, §2.6, equations 20 – 23, §2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf): noise model, SNR and saturation.
- [Edmund Optics, resolution](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/). Page inaccessible to automated tools the 2026-10-23: not reverified.
- [torchvision 0.24, Resize, antialias parameter and fault change to 0.17 (accessed on 2026-10-24)](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html).
- [Related flashcards](../21-exposition-bruit-echantillonnage.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, correction and enrichment accepted by the learner, without independent validation.
