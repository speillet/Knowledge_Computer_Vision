# Flashcards — Exposure, noise, color and sampling

reference note: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-ACQUISITION-001

Objective: Calculate a simplified blur. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-001
Question: An image detail moves at 800 px/s during a 5 ms exposure. What motion blur is expected under a uniform-motion model?
Reponse: **Expected answer**: About 4 px: 800 × 0,005. Doubling the exposure would give 8 px in this model.

**Further explanation**: The calculation excludes acceleration, rotation and vibration; it is used to design a test, not to certify a camera.

**Physical reading and built example**: The pixel receives light throughout the exposure, so it adds up the successive positions of the detail. The product $v_{px}t_e$ is a length in the image, not a distance in the world. For a two-pixel wide defect, a four-pixel trail can mix its signal with the background, even if the image retains proper brightness. A compensation for moving between frames does not automatically return this mixture inside a frame.

**Decision under constraint**: to aim at the most one pixel of displacement with the same speed, the model gives $t_e\le1/800$ s, or 1,25 ms. It's an analytical budget, not a guarantee of detection. Reducing exposure requires reconsidering lighting and noise. Measure movement in the useful area: an average speed over the entire image can hide a faster detail.

**Model that produces this calculation**: for a constant image translation, an ideal $I_0$ image gives a standardized observation $I_b(x)=t_e^{-1}\int_0^{t_e}I_0(x-v_{px}t)\,dt$, with $x$ in pixels, $t$ in seconds and a rectangular exposure of duration $t_e>0$. This is an average over a $|v_{px}|t_e$ length segment: it explains why blurring depends on speed during exposure, not just the number of frames per second. The formula here assumes a unique and neglectful optical direction, noise and saturation. In perspective, two depths can have different image speeds: a blur budget established on the background does not necessarily protect the part.

**Exposure chosen from a blur budget**: Invert the model before changing camera settings: a permitted blur of 1 px at 800 px/s requires $t_e\le1/800$ s, or 1.25 ms. More illumination can then restore signal while preserving this motion budget; digital gain cannot restore photons lost by shortening exposure. The velocity should be the largest relevant image velocity during acquisition, rather than a dataset average. Acceleration, rotation and depth variation require a more detailed exposure integral.

**Blocking errors**: Mix ms and s or conclude to a universal PSF.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6 – 2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); kinematic calculation of the project under uniform image movement. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-ACQUISITION-001 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-002

Objective: Distinguish between gain and exposure. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-002
Question: An inspection image is too dark. You can double camera gain or double the received light by increasing exposure time or illumination. How does each option affect SNR, motion blur and saturation?
Reponse: **Expected answer**: doubling light doubles photoelectrons and increases SNR: by a factor of $\sqrt2$ when photonic noise dominates, up to 2 when reading noise dominates; longer exposure also increases motion blur. Double the gain multiplies signal and noise already acquired: excluding quantization noise, the SNR does not change, and the maximum numerical value is reached with half the electrons, which reduces the dynamics. The gain does not create photonic information and does not repair saturation.

**Further explanation**: according to EMVA 1288, $\mathrm{SNR}=\eta\mu_p/\sqrt{\sigma_d^2+\sigma_q^2/K^2+\eta\mu_p}$: the system gain $K$ only plays by the quantification. $\eta$ is the quantum efficiency, $\mu_p$ the average number of photons received per pixel during exposure; $\eta\mu_p$ is the average number of photoelectrons. $K$ is the system gain in DN/e⁻, and $\sigma_q^2$ is the quantification variance in DN². The model assumes an unsaturated linear response at a fixed operating point. Example of the project with a reading noise $\sigma_d=5$ e⁻: 100 e⁻ give an SNR of 8,9, 200 e⁻ an SNR of 13,3, and double $K$ leaves 8,9. Reinforce lighting rather than exposure doubles the signal without lengthening the blur. The model describes an operating point: measure the SNR at each setting actually used.

**Link to the choice of acquisition**: Start by checking whether the useful defect is limited by the lack of photons, by movement or by a saturated area. In the first case, enhancing lighting can help; in the second, lengthening exposure can destroy detail; in the third, further amplifying aggravates clipping. This diagnosis leads to comparing the settings on the critical pixels, and not only on the average brightness of the image.

**Separate the regimes**: noting $N$ as the average of useful electrons, the simplified model becomes $SNR=N/\sqrt{N+\sigma_d^2}$ when the quantification is negligible. At low $N$, the denominator varies little and doubling the photons can almost double the SNR; at large $N$, it grows as $\sqrt N$ and the gain tends towards $\sqrt2$. For a defect, also examine the contrast between defect and background: illuminating more can saturate the background before obtaining the necessary contrast. An analog gain placed before certain noise sources can have a different real behavior than a simple digital scale change; the model and measurements must specify the stage concerned.

**Read noise changes the value of additional light**: Constructed calculation: with 25 electrons of read-noise variance, 25 signal electrons give $SNR=25/\sqrt{50}\approx3.54$; 50 electrons give $50/\sqrt{75}\approx5.77$, a factor 1.63. The improvement lies between the read-noise and shot-noise limits. These values assume unsaturated linear response and negligible quantization. Identify whether clipping occurs at sensor full well or after gain: both discard contrast, but their limiting stages and remedies differ.

**Blocking errors**: say that any gain improves SNR; forget that longer exposure increases blur.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [EMVA1288 Linear 4.0 (2021), §2.4, equations 13 – 14, §2.6, equations 21 – 22, and §2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); numerical example of the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-ACQUISITION-002 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-003

Objective: recognize aliasing and inconsistent preprocessing. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-003
Question: A fine pattern changes appearance abruptly after downsampling. What should be checked before blaming the model?
Reponse: **Expected answer**: Filtering before decimation, pattern scale, and resize convention; subsampling can create false low frequencies.

**Further explanation**: without a prefilter adapted to the reduction factor, the high frequencies fold back into the reduced image. Parmar et al. observe aliasing for the OpenCV, TensorFlow and PyTorch configurations evaluated in 2022, against adaptive PIL filters. This depends on the API, version and options; `torchvision.transforms.Resize` 0.24 enables antialiasing by default, unlike its older versions. Check interpolation, reduction factor and antialiasing in both chains. Compare controlled discounts on calibration target and keep the same train/test/inference chain.

**Example interpreted**: A pattern alternating light and dark bands can become uniform or produce wider bands depending on the sampling phase. The network then sees a new pattern that did not exist in the scene. A pre-filter attenuates the frequencies incompatible with the final grid, at the cost of a loss of detail. Then adding a more sophisticated interpolation does not rebuild the already folded information.

**check proposed discriminant**: compare several phases of the same pattern and several reduction factors, keeping the network and annotations fixed. If predictions change mostly with the resize phase, examine the image string before adding increases. The goal is to keep a useful and consistent signal, not to make any image visually smoother.

**Example built frequency**: A sine wave of frequency 0,4 cycle per pixel of origin exceeds the limit of 0,25 for a reduction of a factor of two. After decimation, it corresponds to 0,8 cycle per final pixel, indistinguishable on this grid with a folded frequency of 0,2 cycle per final pixel. The observed pattern is therefore an ambiguity of sampling, not a real movement. The prefilter must attenuate beyond the new Nyquist frequency before discarding the samples. Its support depends on the reduction factor; keeping only the name "bilinear" does not fully describe this treatment. This reasoning is an analytic case on a sinusoid, not a result on the network.

**Aliasing can survive apparently smooth output**: Consider a periodic input with spatial frequency just above the new Nyquist limit. Its sampled output can become a slowly varying false pattern, so visual smoothness after resizing does not establish correct sampling. A proposed check uses sinusoidal patterns at several phases and frequencies, keeping the requested output size fixed. Compare attenuation before decimation and the false low-frequency response afterward; merely changing interpolation names does not specify the effective prefilter.

**Blocking errors**: Suppose that more pixels of the sensor guarantee the detail after all resize.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]] ; [Parmar, Zhang and Zhu 2022, On Aliased Resizing and Surprising Subtleties in GAN Evaluation, CVPR, §§1, 2, 3.2 and 6.3](https://arxiv.org/abs/2104.11222) ; [torchvision 0.24, Resize, antialias](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html) ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-ACQUISITION-003 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-004

Objective: check an image entry. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ACQUISITION-004
Question: Which image checks are needed when a transferred model fails despite no apparent change in the scene?
Reponse: **Expected answer**: Check color order, range/normalization, gamma, bit depth, exposure and saturation in the actual received string.

**Further explanation**: Digitally compare the same image before and after each step, then the training and operation contracts.

**Why these checks separate the causes**: Two tables of the same shape can represent different colors or physical quantities. A red channel interpreted as blue changes the learned contrasts; an additional division by 255 changes the scale; an entire passage can clip values. A visualization that automatically adjusts its contrast can make these paintings almost identical to the eye.

**Proposed Reproducible Investigation**: choose a sample image, keep its original file and record, at each step, shape, type, minimum, maximum and values of a few known pixels. Then compare the tensor actually received by the model with that of the drive chain. Test only one correction at a time. An improvement after re-compliance supports a pre-processing cause; it does not exempt the evaluation of other images and difficult cases of the new sensor.

**Distinguish normalization and linearization**: Divide a value sRGB by 255 places it in a numeric range; this does not remove its transfer curve. For a normalized sRGB component $c>0,04045$, its relative linear value is $c_{lin}=((c+0,055)/1,055)^{2,4}$. Thus, $c=0,5$ represents about 0,214 in linear, and not 0,5. Applying this conversion to an already linear input would be another mistake. Document successively decoding, channel order, photometric transfer, resize and then standardization of the tensor. An equality of form or of minimum/maximum does not demonstrate the equality of the intermediate values or their physical sense.

**An interface check needs a known stimulus**: Feed a constructed color chart with distinct red, green and blue regions and a grayscale ramp through the exact deployment decode path. Compare intermediate arrays with the training path before normalization and after it. A red/blue swap is visible in channel identity; a range error changes the ramp slope; clipping creates flat regions. Equal tensor shape and similar mean brightness cannot distinguish these failures. This is a proposed interface test, not a measured model result.

**Blocking errors**: Rely only on a self-scaling visualization.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Full reference]]; [sRGB, §§A.7 – A.8 and B.1, linear conversion and transfer function](https://www.w3.org/Graphics/Color/srgb); [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6 – 2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); project diagnostic checklist. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-ACQUISITION-004 provenance::agent pole::A pole::B pole::C pole::E pole::F
END
