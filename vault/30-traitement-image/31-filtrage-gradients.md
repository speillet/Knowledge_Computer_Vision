# Flashcards — Filters, gradients and pyramids

reference note: [[30-traitement-image/references/31-filtrage-gradients|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-FILTRES-001

Objective: Choose a filter based on the noise. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-001
Question: Why can a median filter suit impulse noise without universally replacing Gaussian filtering?
Reponse: **Expected answer**: It rejects local extreme values via order, while the Gaussian average; the effect depends on noise and structures.

**Further explanation**: Compare preservation of small details and downstream performance; the median remains non-linear and can change the geometry.

**Concrete mechanism**: in a neighborhood where most intensities are about 100 and a value is 255, an average propagates the influence of this pulse at its output, while a median can remain close to the majority level. On the other hand, a very thin real scratch can also become a minority in the neighborhood and disappear. The filter does not know how to distinguish a parasitic pulse from a useful defect on their size alone.

**Proposed choice**: compare multiple media on a batch containing noise, edges and critical details. Keep the downstream steps identical, and then measure missed defects and location errors. Larger support increases the scale of image modification. The median does not describe itself as a linear convolution; the Gaussian achieves a weighted average whose frequency behavior helps to build pyramids. These differences explain the choice, without establishing a universal ranking.

**Linking the operation to the noise**: for a normalized linear filter $J(p)=\sum_q k_q I(p-q)$ and independent noises of variance $\sigma_n^2$, the output variance is $\sigma_n^2\sum_q k_q^2$. A uniform average of nine samples therefore divides it by nine, under these assumptions, but also mixes their signals. The median depends on the rank of the values: an isolated pulse can stay away from the central rank without drawing the result towards it. Noise correlations, edges and fine details change these tradeoffs. The Gaussian is separable: two convolutions 1D replace a convolution 2D for the same kernel produced, without making a median equivalent to this operation.

**Blocking errors**: Advertise a better filter for all noises and tasks.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [OpenCV 4.12.0, Smoothing Images, Gaussian/Median/Bilateral Filter](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html); [OpenCV 4.13, Smoothing Images, Theory, Gaussian, Median and Bilateral Filter](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html), see 2026-10-30.
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-FILTRES-001 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-002

Objective: settle a bilateral in the right units. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-002
Question: When intensities are normalized from [0,255] to [0,1], what changes for a bilateral filter's photometric sigma?
Reponse: **Expected answer**: Divide the photometric sigma by 255, like the intensity differences, to maintain the same weights. Keeping the same number makes filtering less selective in intensity.

**Further explanation**: The spatial sigma is in pixels and follows another logic. Record beach and color space.

**derivation**: The photometric weight depends on the $|I(p)-I(q)|/\sigma_r$ ratio. If the intensity and $\sigma_r$ are divided by the same positive constant, this ratio remains the same and therefore the associated weight also, with support and numerical calculation unchanged. Changing only the intensity makes the gaps relatively smaller: more neighbors become photometrically similar.

**Constructed example**: A difference of 20 levels compared to a sigma of 10 represents two sigmas. After dividing by 255, the deviation is about 0,0784 and the consistent sigma is about 0,0392; the ratio remains two. Keeping a sigma of 10 in this new range overwhelms this distinction. This equivalence implies a linear transformation of the intensity: a gamma or a change of color space is not treated by a simple common division. Spatial sigma and boundary conventions remain separate.

**Complete form and role of standardization**: for a pixel $p$, write $J(p)=\sum_q w_{pq}I(q)/\sum_q w_{pq}$, with $w_{pq}=\exp(-\|p-q\|^2/(2\sigma_s^2))\exp(-(I(p)-I(q))^2/(2\sigma_r^2))$. The first factor favors nearby neighbors, the second one those whose intensity resembles that of the center. The denominator adapts the sum of the weights to the local content; without it, an edge could simply darken the result by rejecting neighbors. The weights depend on the image: it is a non-linear operation, even if the output looks like an average. The noise of the central pixel also influences which neighbors will be considered similar; preserving a contour remains conditional.

**Blocking errors**: Treat all sigma as quantities without unity.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [Tomasi and Manduchi 1998, Bilateral Filtering, §§2 – 3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf); [OpenCV 4.13, Smoothing Images, Theory, Gaussian, Median and Bilateral Filter](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html), see 2026-10-30.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-FILTRES-002 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-003

Objective: Protect a business detail. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-003
Question: Denoising improves PSNR but removes scratches. How should this preprocessing be evaluated?
Reponse: **Expected answer**: Measure defect recall and location error at relevant scale, with reserved images and annotations.

**Further explanation**: An overall rebuild gain can hide a small or rare defect; keep the baseline unfiltered.

**Origin of the paradox**: The PSNR summarizes a reconstruction error on all pixels. A large, more noise-free bottom area can dominate this measure, while a small scratch, however decisive for the trade, is erased. Improving the average similarity to a reference therefore does not guarantee to preserve the signal that the detector must use.

**Proposed experience**: Compare pipelines with and without filters on the same parts and annotations, isolating fine scratches, low contrasts and textured areas. Varying only the filter and its scale, then examining false negatives, false positives and location, at an explicit operating point. Keep some before/after intensity profiles on missed details. If the image looks cleaner but the recall drops, the filter introduces an unfavorable compromise to this task. The reserved test is not used to choose the parameters indefinitely.

**Make the compromise quantifiable**: $PSNR=10\log_{10}(L^2/MSE)$, with $L$ the maximum of the range announced and $MSE$ the average squared errors against a reference. Modifying $L$ or normalization without consistency changes the score. If a defect occupies a fraction $p$ of the pixels and undergoes an amplitude error $a$, its contribution to the MSE is only $pa^2$: it can remain small even if all its pixels are lost. Then measure the probability of detecting a defective part and the frequency of false alarms per part, with rules of association and constant thresholds. The reference to PSNR must itself be justified; a noisy image used as "clean" changes the problem.

**Blocking errors**: Decide on the PSNR alone.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [OpenCV 4.12.0, Smoothing Images, Gaussian/Median/Bilateral Filter](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html); downstream protocol proposed by the project; [OpenCV 4.13, PSNR/SSIM, definition of PSNR; built scarcity example](https://docs.opencv.org/4.13.0/d5/dc4/tutorial_video_input_psnr_ssim.html), consult the 2026-10-30.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-FILTRES-003 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-004

Objective: Explain a pyramid. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-004
Question: Why is simply retaining every other pixel insufficient for constructing a matching pyramid?
Reponse: **Expected answer**: Decimation without filtering can fold high frequencies into aliasing and change observed structures.

**Further explanation**: The filter and the chosen scale condition the repeatability of the features; they do not guarantee perfect invariance.

**Chain of reasoning**: Reducing the grid decreases the maximum representable spatial frequency. A rapid alternation of intensities can then be interpreted as a slower pattern if one decimates directly. Pre-smoothing attenuates components that are incompatible with the new grid; decimation then reduces the number of samples. The prefilter therefore chooses what is stored before the loss of resolution.

**Consequences for Matching**: The gradients and extrema used as features change if the texture is folded. Two views of the same object can produce unstable descriptors simply because of resampling. In a constructed test, compare the number of geometrically verified matches on a reduced calibration target with and without a prefilter, with constant detector. Better stability is not a perfect invariance at scale: too small a detail ends up disappearing even with a properly filtered pyramid.

**Building the Levels**: A Gaussian pyramid follows $I_{\ell+1}(x,y)=(G_\ell*I_\ell)(2x,2y)$ in an example of decimation by two. Coordinates are approximately converted by $p_0=2^\ell p_\ell$, respecting the exact pixel center conventions. A five-ray window at the $\ell=3$ level covers about forty pixels of radius in the initial image: its physical support has changed. This is useful for bringing back a large displacement in a local capture area, but it can mix objects or eliminate a fine structure. Propagate coordinates, descriptor radius, and geometric thresholds in the same system of units, rather than treating levels as independent images.

**Blocking errors**: Confusing undersampling and controlled loss of information.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]] ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
Tags: cv::pilote cv::d03 famille::comprehension cv_id::CV-FILTRES-004 provenance::agent pole::A pole::B pole::E pole::F
END
