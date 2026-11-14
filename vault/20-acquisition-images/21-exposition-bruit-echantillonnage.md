# Flashcards — Exposure, noise, color and sampling

reference note: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-ACQUISITION-001

Objective: Calculate a simplified blur. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-001
Question: An image detail moves at 800 px/s during a 5 ms exposure. What motion blur is expected under a uniform-motion model?
Reponse: **Expected answer**: About 4 px: 800 × 0.005. Doubling the exposure would give 8 px in this model.

**Further explanation**: The calculation excludes acceleration, rotation and vibration; it is used to design a test, not to certify a camera.

**Physical reading and constructed example**: The pixel receives light throughout the exposure, so it sums the successive positions of the detail. The product $v_{px}t_e$ is a length in the image, not a distance in the world. For a two-pixel wide defect, a four-pixel trail can mix its signal with the background, even if the image keeps a correct brightness. Compensating motion between frames does not undo this mixing within a frame.

**Decision under constraint**: to keep the displacement during exposure to at most one pixel at the same speed, the model gives $t_e\le1/800$ s, or 1.25 ms. It is an analytical budget, not a guarantee of detection. Reducing exposure requires reconsidering lighting and noise. Measure motion in the useful area: an average speed over the entire image can hide a faster detail.

**Model that produces this calculation**: for a constant image translation, an ideal image $I_0$ gives a normalized observation $I_b(x)=t_e^{-1}\int_0^{t_e}I_0(x-v_{px}t)\,dt$, with $x$ in pixels, $t$ in seconds and a rectangular exposure of duration $t_e>0$. This is an average over a segment of length $|v_{px}|t_e$: it explains why blur depends on the speed during exposure, not on the number of frames per second. The formula assumes a single motion direction and neglects optics, noise and saturation. Under perspective projection, points at different depths can have different image speeds: a blur budget established on the background does not necessarily protect the part.

**Exposure chosen from a blur budget**: Invert the model before changing camera settings: a permitted blur of 1 px at 800 px/s requires $t_e\le1/800$ s, or 1.25 ms. More illumination can then restore signal while preserving this motion budget; digital gain cannot restore photons lost by shortening exposure. The velocity should be the largest relevant image velocity during acquisition, rather than a dataset average. Acceleration, rotation and depth variation require a more detailed exposure integral.

**Blocking errors**: Mixing ms and s, or treating this box blur as a universal point spread function (PSF).
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [EMVA 1288 Linear 4.0 (2021), §1.2 eq. 1 (exposure integrates irradiance over the exposure time) and §2.1 eq. 6 (signal proportional to exposure time)](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); blur formula: kinematic calculation of the project under uniform image motion. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-ACQUISITION-001 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-002

Objective: Distinguish between gain and exposure. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-002
Question: An inspection image is too dark. You can double camera gain or double the received light by increasing exposure time or illumination. How does each option affect SNR, motion blur and saturation?
Reponse: **Expected answer**: Doubling the light doubles the photoelectrons and increases the SNR: by a factor of $\sqrt2$ when photon shot noise dominates, up to 2 when read noise dominates; a longer exposure also increases motion blur. Doubling the gain multiplies the signal and the noise already acquired: excluding quantization noise, the SNR does not change, and the maximum digital value is reached with half the electrons, which reduces the dynamic range. The gain does not create photon information and does not repair saturation.

**Further explanation**: according to EMVA 1288, $\mathrm{SNR}=\eta\mu_p/\sqrt{\sigma_d^2+\sigma_q^2/K^2+\eta\mu_p}$: the system gain $K$ enters only through the quantization term. $\eta$ is the quantum efficiency, $\mu_p$ the mean number of photons received per pixel during exposure; $\eta\mu_p$ is the mean number of photoelectrons. $K$ is the system gain in DN/e⁻, and $\sigma_q^2$ is the quantization variance in DN². The model assumes an unsaturated linear response at a fixed operating point. Project example with read noise $\sigma_d=5$ e⁻ and negligible quantization: 100 e⁻ give an SNR of 8.9, 200 e⁻ an SNR of 13.3, and doubling $K$ leaves 8.9. Increasing illumination rather than exposure doubles the signal without lengthening the blur. The model describes one operating point: measure the SNR at each setting actually used.

**Link to the choice of acquisition**: Start by checking whether the useful defect is limited by a lack of photons, by motion or by a saturated area. In the first case, more lighting can help; in the second, a longer exposure can destroy detail; in the third, more amplification aggravates clipping. This diagnosis leads to comparing settings on the critical pixels, not only on the mean brightness of the image.

**Separate the regimes**: writing $N$ for the mean number of signal electrons, the simplified model becomes $SNR=N/\sqrt{N+\sigma_d^2}$ when quantization is negligible. At low $N$, the denominator varies little and doubling the photons can almost double the SNR; at large $N$, it grows as $\sqrt N$ and the improvement tends towards $\sqrt2$. For a defect, also examine the contrast between defect and background: more light can saturate the background before giving the necessary contrast. An analog gain placed before some noise sources can behave differently from a simple digital scaling; the model and the measurements must specify the stage concerned.

**Read noise changes the value of additional light**: Constructed calculation: with read-noise standard deviation 5 electrons (variance 25 e⁻²), 25 signal electrons give $SNR=25/\sqrt{50}\approx3.54$; 50 electrons give $50/\sqrt{75}\approx5.77$, a factor 1.63. The improvement lies between the read-noise and shot-noise limits. These values assume unsaturated linear response and negligible quantization. Identify whether clipping occurs at sensor full well or after gain: both discard contrast, but their limiting stages and remedies differ.

**Blocking errors**: Saying that any gain improves the SNR; forgetting that a longer exposure increases blur.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [EMVA 1288 Linear 4.0 (2021), §2.1 eq. 5, §2.4 eqs. 13–14, §2.6 eqs. 21–22 and §2.7 eq. 24](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); numerical example of the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-ACQUISITION-002 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-003

Objective: recognize aliasing and inconsistent preprocessing. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-003
Question: A fine pattern changes appearance abruptly after downsampling. What should be checked before blaming the model?
Reponse: **Expected answer**: Filtering before decimation, pattern scale, and resize convention; subsampling can create false low frequencies.

**Further explanation**: without a prefilter adapted to the reduction factor, high frequencies fold back into the reduced image. Parmar et al. observe aliasing with the default flags of OpenCV 4.5.5 `cv2.resize`, TensorFlow 2.0 and PyTorch 1.9 `F.interpolate`, against the adaptive filters of PIL. This depends on the API, version and options; `torchvision.transforms.Resize` 0.24 antialiases tensor inputs by default in bilinear and bicubic modes, a default introduced in 0.17 (PIL inputs were already antialiased). Check interpolation, reduction factor and antialiasing in both pipelines. Compare controlled downscalings of a calibration target and keep the same train/test/inference pipeline.

**Interpreted example**: A pattern alternating light and dark bands can become uniform or produce wider bands depending on the sampling phase. The network then sees a pattern that did not exist in the scene. A prefilter attenuates the frequencies incompatible with the final grid, at the cost of a loss of detail. Adding a more sophisticated interpolation afterwards does not rebuild information that has already folded.

**Proposed discriminating check**: compare several phases of the same pattern and several reduction factors, keeping the network and annotations fixed. If predictions change mostly with the resize phase, examine the image pipeline before adding augmentations. The goal is to keep a useful and consistent signal, not to make every image visually smoother.

**Constructed frequency example**: A sine wave of 0.4 cycle per original pixel exceeds the limit of 0.25 for a reduction by a factor of two. After decimation, it becomes 0.8 cycle per final pixel, indistinguishable on this grid from a folded frequency of 0.2 cycle per final pixel. The observed pattern is therefore a sampling ambiguity, not a real change in the scene. The prefilter must attenuate beyond the new Nyquist frequency before the samples are discarded. Its support depends on the reduction factor; the name "bilinear" alone does not fully describe this processing. This reasoning is an analytical case on a sinusoid, not a result on the network.

**Aliasing can survive apparently smooth output**: Consider a periodic input with spatial frequency just above the new Nyquist limit. Its sampled output can become a slowly varying false pattern, so visual smoothness after resizing does not establish correct sampling. A proposed check uses sinusoidal patterns at several phases and frequencies, keeping the requested output size fixed. Compare attenuation before decimation and the false low-frequency response afterward; merely changing interpolation names does not specify the effective prefilter.

**Blocking errors**: Assuming that more sensor pixels guarantee the detail after any resize.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]] ; [Parmar, Zhang and Zhu 2022, On Aliased Resizing and Surprising Subtleties in GAN Evaluation, CVPR, §§1, 2, 3.2 and 6.3](https://arxiv.org/abs/2104.11222) ; [torchvision 0.24, Resize, antialias](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html) ; [OpenCV 4.13.0 imgproc.hpp, `INTER_AREA` for decimation, `resize` and `pyrDown`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L249-L263). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-ACQUISITION-003 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-004

Objective: Check an image input. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-004
Question: Which image checks are needed when a transferred model fails despite no apparent change in the scene?
Reponse: **Expected answer**: Check color order, range/normalization, gamma, bit depth, exposure and saturation in the pipeline that actually feeds the model.

**Further explanation**: Compare the same image numerically before and after each step, then compare the training and deployment contracts.

**Why these checks separate the causes**: Two arrays of the same shape can represent different colors or physical quantities. A red channel interpreted as blue changes the learned contrasts; an extra division by 255 changes the scale; a conversion to integers can clip values. A visualization that automatically adjusts its contrast can make these images look almost identical.

**Proposed reproducible investigation**: choose a sample image, keep its original file and record, at each step, shape, type, minimum, maximum and the values of a few known pixels. Then compare the tensor actually received by the model with that of the training pipeline. Test only one correction at a time. An improvement after realigning the pipeline supports a preprocessing cause; it does not exempt you from evaluating other images and the difficult cases of the new sensor.

**Distinguish normalization and linearization**: Dividing an sRGB value by 255 places it in a numeric range; it does not remove its transfer curve. For a normalized sRGB component $c>0.04045$, its relative linear value is $c_{lin}=((c+0.055)/1.055)^{2.4}$. Thus $c=0.5$ represents about 0.214 in linear light, not 0.5. Applying this conversion to an already linear input would be another mistake. Document in order decoding, channel order, photometric transfer, resizing and then normalization of the tensor. Equal shapes or equal minimum/maximum do not show that the intermediate values or their physical meaning are equal.

**An interface check needs a known stimulus**: Feed a constructed color chart with distinct red, green and blue regions and a grayscale ramp through the exact deployment decode path. Compare intermediate arrays with the training path before normalization and after it. A red/blue swap is visible in channel identity; a range error changes the ramp slope; clipping creates flat regions. Equal tensor shape and similar mean brightness cannot distinguish these failures. This is a proposed interface test, not a measured model result.

**Blocking errors**: Relying only on a self-scaling visualization.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [sRGB, A.8 and B.1, transfer function and its inverse](https://www.w3.org/Graphics/Color/srgb); [OpenCV 4.13.0 imgcodecs.hpp, `imread` (B G R order, 8-bit conversion, EXIF orientation)](https://github.com/opencv/opencv/blob/4.13.0/modules/imgcodecs/include/opencv2/imgcodecs.hpp#L323-L375); [EMVA 1288 Linear 4.0 (2021), §1.2 and §2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); project diagnostic checklist. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-ACQUISITION-004 provenance::agent pole::A pole::B pole::C pole::E pole::F
END
