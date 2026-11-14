# Flashcards — Filters, gradients and pyramids

reference note: [[30-traitement-image/references/31-filtrage-gradients|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-FILTRES-001

Objective: Choose a filter based on the noise. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-001
Question: Why can a median filter suit impulse noise without universally replacing Gaussian filtering?
Reponse: **Expected answer**: It rejects local extreme values through ranking, whereas the Gaussian averages them into the output; the effect depends on the noise and the structures.

**Further explanation**: Compare preservation of small details and downstream performance; the median remains non-linear and can change the geometry.

**Concrete mechanism**: in a neighborhood where most intensities are about 100 and one value is 255, an average carries the influence of this pulse into its output, while a median can stay close to the majority level. On the other hand, a very thin real scratch can also become a minority in the neighborhood and disappear. The filter cannot distinguish a parasitic pulse from a useful defect by their size alone.

**Proposed choice**: compare several window sizes on a batch containing noise, edges and critical details. Keep the downstream steps identical, then measure missed defects and localization errors. A larger support increases the scale at which the image is modified. The median cannot be written as a linear convolution; the Gaussian computes a weighted average whose frequency behavior helps to build pyramids. These differences explain the choice, without establishing a universal ranking.

**Linking the operation to the noise**: for a normalized linear filter $J(p)=\sum_q k_q I(p-q)$ and independent noise of variance $\sigma_n^2$ per pixel, the output variance is $\sigma_n^2\sum_q k_q^2$. A uniform average of nine samples therefore divides it by nine, under these assumptions, but also mixes their signals. The median depends on the rank of the values: an isolated pulse can stay away from the central rank without drawing the result towards it. Noise correlations, edges and fine details change these tradeoffs. The Gaussian is separable: two 1-D convolutions replace one 2-D convolution with the same product kernel, which does not make a median equivalent to this operation.

**Robustness to impulses has a geometric price**: In a nine-value neighborhood with eight values of 10 and one impulse of 250, the median remains 10 while the mean becomes about 36.7. If the single high value is a genuine one-pixel bright defect, however, removing it is an error. The filter cannot identify which interpretation is correct from rank alone. This constructed counterexample connects the noise assumption directly to the smallest structure the inspection task must retain.

**Blocking errors**: Claiming that one filter is best for all noise types and tasks.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [OpenCV 4.13.0 imgproc.hpp, `medianBlur` and `GaussianBlur`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1538-L1578); [Tomasi and Manduchi, Bilateral Filtering, Introduction (linear smoothing blurs edges)](https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/MANDUCHI1/Bilateral_Filtering.html). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-FILTRES-001 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-002

Objective: Tune a bilateral filter in the right units. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-002
Question: When intensities are normalized from [0,255] to [0,1], what changes for a bilateral filter's photometric sigma?
Reponse: **Expected answer**: Divide the photometric sigma by 255, like the intensity differences, to maintain the same weights. Keeping the same number makes filtering less selective in intensity.

**Further explanation**: The spatial sigma is in pixels and follows another logic. Record the intensity range and the color space.

**Derivation**: The photometric weight depends on the ratio $|I(p)-I(q)|/\sigma_r$. If the intensity and $\sigma_r$ are divided by the same positive constant, this ratio remains the same and therefore the associated weight also, with support and numerical calculation unchanged. Changing only the intensity makes the gaps relatively smaller: more neighbors become photometrically similar.

**Constructed example**: A difference of 20 levels compared to a sigma of 10 represents two sigmas. After dividing by 255, the difference is about 0.0784 and the consistent sigma about 0.0392; the ratio remains two. Keeping a sigma of 10 in this new range erases this distinction. This equivalence implies a linear transformation of the intensity: a gamma or a change of color space is not treated by a simple common division. Spatial sigma and boundary conventions remain separate.

**Complete form and role of normalization**: for a pixel $p$, write $J(p)=\sum_q w_{pq}I(q)/\sum_q w_{pq}$, with $w_{pq}=\exp(-\|p-q\|^2/(2\sigma_s^2))\exp(-(I(p)-I(q))^2/(2\sigma_r^2))$. The first factor favors nearby neighbors, the second those whose intensity resembles that of the center. The denominator adapts the sum of the weights to the local content; without it, an edge could simply darken the result by rejecting neighbors. The weights depend on the image: it is a non-linear operation, even if the output looks like an average. The noise of the central pixel also influences which neighbors are considered similar; preserving a contour remains conditional.

**Only affine intensity scaling preserves this ratio**: For $I^{\prime}=\alpha I+\beta$ with nonzero $\alpha$, intensity differences scale by $|\alpha|$, so preserving Gaussian range weights requires $\sigma_r^{\prime}=|\alpha|\sigma_r$. The offset cancels. A nonlinear gamma transform does not have one global scale factor for all differences, so adjusting a single sigma cannot generally reproduce the old weights. Also preserve the spatial sigma in the same pixel geometry; resizing changes that contract separately.

**Blocking errors**: Treating every sigma as a unitless quantity.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [Tomasi and Manduchi 1998, Bilateral Filtering, §§2–3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf); [Tomasi and Manduchi, authors' summary, The Gaussian Case (range filter insensitive to additive intensity changes)](https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/MANDUCHI1/Bilateral_Filtering.html); [OpenCV 4.13.0 imgproc.hpp, `bilateralFilter`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1580-L1610). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-FILTRES-002 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-003

Objective: Protect a task-critical detail. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FILTRES-003
Question: Denoising improves PSNR but removes scratches. How should this preprocessing be evaluated?
Reponse: **Expected answer**: Measure defect recall and localization error at the relevant scale, with held-out images and annotations.

**Further explanation**: An overall reconstruction gain can hide a small or rare defect; keep the unfiltered pipeline as a baseline.

**Origin of the paradox**: PSNR summarizes a reconstruction error over all pixels. A large background area with less noise can dominate this measure, while a small scratch, however decisive for the inspection task, is erased. Improving the average similarity to a reference therefore does not guarantee that the signal the detector must use is preserved.

**Proposed experiment**: Compare pipelines with and without filters on the same parts and annotations, isolating fine scratches, low contrasts and textured areas. Vary only the filter and its scale, then examine false negatives, false positives and localization at an explicit operating point. Keep some before/after intensity profiles on missed details. If the image looks cleaner but the recall drops, the filter introduces an unfavorable compromise to this task. The held-out test set is not used to choose the parameters repeatedly.

**Make the compromise quantifiable**: $PSNR=10\log_{10}(L^2/MSE)$, with $L$ the maximum of the stated range and $MSE$ the mean squared error against a reference. Changing $L$ or the normalization inconsistently changes the score. If a defect occupies a fraction $p$ of the pixels and undergoes an amplitude error $a$, its contribution to the MSE is only $pa^2$: it can remain small even if all its pixels are lost. Then measure the probability of detecting a defective part and the frequency of false alarms per part, with fixed association rules and thresholds. The reference used for PSNR must itself be justified; a noisy image used as "clean" changes the problem.

**A task metric needs the same operating point**: Compare preprocessing variants at a fixed false-alarm budget per inspected part, then measure defect recall by width, contrast and position. Holding an arbitrary detector score threshold fixed may confound preprocessing with changed score distributions. Use validation to choose thresholds and an untouched test set to estimate the resulting tradeoff. This proposed protocol distinguishes improved appearance from an operational improvement on the rare defects that matter.

**Blocking errors**: Deciding on PSNR alone.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]]; [OpenCV 4.13, PSNR/SSIM tutorial, definition of PSNR (consulted 2026-10-30; not re-read, HTTP 403 in 2026-11-14)](https://docs.opencv.org/4.13.0/d5/dc4/tutorial_video_input_psnr_ssim.html); constructed rarity example and downstream protocol proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
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

**Chain of reasoning**: Reducing the grid decreases the maximum representable spatial frequency. A rapid alternation of intensities can then be interpreted as a slower pattern if one decimates directly. Pre-smoothing attenuates components that are incompatible with the new grid; decimation then reduces the number of samples. The prefilter therefore chooses what is kept before the loss of resolution.

**Consequences for matching**: The gradients and extrema used as features change if the texture is folded. Two views of the same object can produce unstable descriptors simply because of resampling. In a constructed test, compare the number of geometrically verified matches on a downscaled calibration target with and without a prefilter, with a constant detector. Better stability is not perfect scale invariance: a detail that is too small eventually disappears even with a properly filtered pyramid.

**Building the levels**: A Gaussian pyramid follows $I_{\ell+1}(x,y)=(G_\ell*I_\ell)(2x,2y)$ for decimation by two. Coordinates are approximately converted by $p_0=2^\ell p_\ell$, respecting the exact pixel-centre conventions. A window of radius five at level $\ell=3$ covers a radius of about forty pixels in the original image: its physical support has changed. This is useful for bringing a large displacement into a local capture area, but it can mix objects or eliminate a fine structure. Propagate coordinates, descriptor radius and geometric thresholds in the same system of units, rather than treating levels as independent images.

**A coarse-level displacement changes its unit**: After three reductions by two, an 8 px full-resolution displacement is approximately 1 px at the coarse level. This helps a local matcher only if the relevant texture survives filtering and neighboring motions do not merge within the window. A 1 px localization error at that level also becomes about 8 px when transferred back. Pyramid depth therefore changes both capture range and localization precision; it cannot be chosen solely from maximum motion.

**Blocking errors**: Confusing plain subsampling with a controlled loss of information.
Source: [[30-traitement-image/references/31-filtrage-gradients|Full reference]] ; [Burt and Adelson 1983, Gaussian Pyramid Generation and The Generating Kernel](https://doi.org/10.1109/TCOM.1983.1095851) ; [OpenCV 4.13.0 imgproc.hpp, `pyrDown` (blur then reject even rows and columns)](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L3194-L3214). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::comprehension cv_id::CV-FILTRES-004 provenance::agent pole::A pole::B pole::E pole::F
END
