# Flashcards — MOSSE and KCF — tracking with correlation filters

reference note: [[110-tracking-association/references/114-mosse-kcf|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-CORRELATION-001

Objective: Explain the loop of a tracking filter. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-001
Question: How does a correlation filter initialized from a box track the target in the next frame?
Reponse: **Expected answer**: Extract a search region and its features, correlate with the model, locate the peak, check reliability and then adapt the model only according to the chosen policy. The answer is a location peak, not a semantic class.

**Further explanation**: Initialization provides the target and synthetic responses around it. The search is local; a target that has left this region does not reappear by adapting the filter alone. Do not confuse single-object tracking with detection of all objects.

**Interpretation of the answer**: Each candidate shift in the search region receives a score of similarity to the model. The peak locates the preferred hypothesis, but its contrast and the presence of competitors must be examined before an update. The search area already expresses a hypothesis about possible motion.

**Constructed example**: A target moving beyond this area can leave the background as the best available peak. Learning this background then turns a loss of localization into a persistent drift of the model. Define a loss and recovery policy, then test it on large motions and occlusions. Correlation speed is useful only if the search and update assumptions fit the need.

**From the peak to the image**: The response is computed in the coordinates of the patch or of its features. Converting the offset of the maximum to the image requires the origin of the crop, its resizing and any stride. A circular correlation convention also requires interpreting near-edge indices as appropriate signed offsets. An error here can produce a jump despite a correctly computed peak. Check a known synthetic translation and map back to image coordinates before setting the confidence threshold. Subpixel localization refines the peak estimate; it does not guarantee equivalent physical accuracy on real images.

**A search crop defines the capture region**: If the target moves entirely outside the sampled search crop, a response maximum still exists inside that crop but need not correspond to the target. A reliability check and an explicit failure outcome are therefore essential. Evaluate search size against expected frame-to-frame motion and distractors. A larger crop increases candidate context and computation and can introduce stronger competing peaks; it is not a free guarantee of reacquisition.

**Blocking errors**: Updating the model on every predicted box without a check; promising global detection.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, §3 introduction and §§3.4–3.5: correlation, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §VIII-A: tracking pipeline](https://arxiv.org/html/1404.7584v3). The capture-region and coordinate reasoning is a project deduction.
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-CORRELATION-001 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-002

Objective: distinguish MOSSE and KCF. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-002
Question: What do cyclic shifts and kernels give KCF compared with a linear filter such as MOSSE?
Reponse: **Expected answer**: KCF structures the examples as cyclic shifts of the patch; the circulant matrix allows efficient Fourier computations, including for compatible kernels. MOSSE learns a linear correlation filter adapted online.

**Further explanation**: The computational gain depends on this structure and on the features. Cyclic shifts create artificial examples at the edges: speed does not remove these biases. No frame rate reported in a paper predicts the rate on the target hardware. MOSSE is not outside this structure: its Fourier solution is ridge regression over the cyclic shifts of several base samples with a single channel, solved in the primal, whereas KCF and its linear variant DCF use one base sample in the dual, which admits kernels and several feature channels with element-wise operations. With a linear kernel and one channel, DCF is equivalent to MOSSE.

**Why structure helps**: Shifts of the same patch are strongly related; treating them as a structured family avoids a generic procedure that would be expensive for all of them. The Fourier domain exploits this organization in the chosen formulation. The gain does not prove that the examples are realistically diverse.

**Concrete limit**: A cyclic shift makes an edge reappear on the other side of the patch. This artificial example may differ from the actual motion of a target in front of a background. Check region size, features, edges and adaptation policy in a comparison with MOSSE. Measure quality and cost on the same protocol; using a kernel does not turn local search into global re-detection or a peak score into a certain identity.

**Structured regression**: a regularized linear regression solves $\min_w\|Xw-y\|^2+\lambda\|w\|^2$. If the rows of $X$ are the cyclic shifts of the same signal, the circulant structure makes it possible to diagonalize the corresponding operations by Fourier transform. In a kernel regression, the matrix of similarities must keep a compatible structure. This explains the efficiency without equating a kernel with a deep network. The regularization parameter stabilizes learning according to the feature scale; it does not compensate for a target missing from the patch or an artificial edge hypothesis ill-suited to the scene.

**Cyclic training creates artificial boundary examples**: A circular shift wraps one side of a patch onto the other, which can create an artificial seam absent from a physical translation. Windowing and search-region design reduce some boundary effects under their assumptions. The Fourier diagonalization exploits this structured training set; it does not make arbitrary independent patches circulant. Compare border-crossing and large-displacement cases when testing whether the efficient model remains suitable for the target sequence.

**Blocking errors**: Presenting KCF as a deep detector; claiming that a kernel removes the limits of local search.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Henriques et al., KCF, §§IV–V: circulant structure and kernels; §VII-B, §VIII-A and Appendix A-F: relation to MOSSE](https://arxiv.org/html/1404.7584v3); [Bolme et al., MOSSE, §§3.1–3.2: boundary preprocessing and filter learning](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf). Boundary and protocol reasoning is a project deduction.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-CORRELATION-002 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-003

Objective: interpret a PSR. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-003
Question: A response has a peak of 0.8, an off-peak mean of 0.2 and an off-peak standard deviation of 0.1. What is the PSR, and what does it mean?
Reponse: **Expected answer**: PSR $=(0.8-0.2)/0.1=6$. The peak exceeds the mean of the off-peak (sidelobe) region by six standard deviations of that region. It measures response contrast, not a calibrated probability that the target is correct.

**Further explanation**: Define the excluded area and the treatment of a zero standard deviation. The threshold depends on the tracker, the patch and the protocol. Distractors can produce a sharp peak on the wrong object. Implementations differ: the MOSSE paper excludes an $11\times11$ window around the peak, whereas OpenCV 4.13's legacy MOSSE computes the mean and standard deviation over the whole response, peak included, and compares the result with 5.7; the two scales are not interchangeable.

**Interpreting the calculation**: Subtracting the off-peak mean measures the deviation from the background response; dividing by its standard deviation expresses this deviation in units of the background variation. Multiplying the whole response by a positive constant does not change this ideal ratio if the region and the calculation remain the same.

**Proposed diagnosis**: View the response map and competing peaks, precisely define the excluded area and process a zero or near zero dispersion. On a repeated pattern, the wrong object can produce a narrow, high peak. The PSR then correctly describes response contrast without knowing the true identity. Its threshold is therefore validated against actual successes, losses and distractors, rather than used as a universal confidence level.

**Effect of a distractor**: If a second peak enters the area used to calculate the off-peak mean and standard deviation, it can change the PSR of the first peak, even if its height remains the same. The size of the excluded area and the edges of the patch therefore participate in the definition of the score. A positive affine transformation $r'=ar+b$, with the same support and $a>0$, ideally retains the PSR, because numerator and standard deviation are multiplied by $a$. On the other hand, clipping, quantizing or changing the support can break this invariance. The score is therefore comparable only with an identical calculation procedure and a threshold validated in its context.

**PSR is invariant to some response rescalings**: If the response map is transformed by $r^{\prime}=ar+b$ with $a>0$ and the sidelobe region is unchanged, peak-minus-mean and standard deviation both scale by $a$, leaving PSR unchanged. A constant map instead has zero sidelobe standard deviation and requires a defined policy. This constructed relation explains why raw peak height and PSR measure different things, and why neither is a calibrated probability of correct identity.

**Blocking errors**: Interpreting PSR $=6$ as 60% confidence; applying a historical threshold to any method.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, MOSSE, §3.5: PSR definition, 11×11 exclusion and typical values](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [opencv_contrib 4.13.0, mosseTracker.cpp L31–L33 and L104–L109: whole-map PSR and threshold 5.7](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/mosseTracker.cpp#L31-L109). The invariance and distractor reasoning is a project deduction.
Tags: cv::pilote cv::d11 famille::raisonnement cv_id::CV-CORRELATION-003 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-004

Objective: Look for contamination of the model. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-004
Question: A correlation-filter tracker works before an occlusion, then persistently tracks the background. Which update error should be tested?
Reponse: **Expected answer**: It may have learned the background during frames where the target was hidden. Compare the model before/after occlusion, freeze low confidence updates and check competitor peaks and search region.

**Further explanation**: A quick adaptation follows changes in appearance but also learns localization errors. A detector or an explicit reset may be required; freezing alone does not guarantee recovery.

**Chain of failure**: A first error places the window on the background; an unchecked update integrates it; the adapted model then responds better to this background. Watching only the last box does not show when this loop started.

**Constructed ablation**: Keep the same initialization and frames, then freeze only during a period of uncertainty. Compare the crops learned, the response contrast, the losses and the eventual return of the target. If the search region no longer contains the target, freezing is not enough: a relaunch or other observation is necessary. Also assess the legitimate appearance changes that freezing may fail to follow, in order to choose an adaptation/protection tradeoff based on the actual need.

**Separate search and learning**: Freezing updates retains a target model, but does not change the region being searched. After a long occlusion or a large shift, the target may return elsewhere and remain untraceable despite an intact model. Compare two separate interventions: freezing the model with unchanged search, then an expanded search policy or detection with the same model. Measure false returns on distractors and recovery times, without using the true position to silently reset. This ablation distinguishes contamination, loss of spatial coverage and appearance ambiguity, which can produce a similar final box on the background.

**A learned distractor can make confidence self-reinforcing**: Once the update absorbs background appearance, later correlation peaks may look reliable relative to that altered model. Compare against a saved pre-occlusion model and inspect the update history before treating a high response as confirmation. A proposed intervention separates freezing updates from expanding search and reinitialization, since each changes a different mechanism. Evaluate false recovery as well as overlap after a successful reacquisition.

**Blocking errors**: Systematically increasing the learning rate to correct drift.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, MOSSE, §3.4 eqs. 10–12 and §3.5: running-average update and PSR-based pause](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §VIII-A: interpolated model update without failure detection](https://arxiv.org/html/1404.7584v3). The ablations are project protocols.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-CORRELATION-004 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-005

Objective: Define an honest comparison of trackers. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-005
Question: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?
Reponse: **Expected answer**: Initialization and reset protocol, sequences, losses, overlap and center error, as well as full latency. A restart after error changes the evaluated task.

**Further explanation**: Keep the same frames and occlusion conditions. Distinguish a one-pass protocol without restarts from a protocol with resets. An average over successful frames only hides the most costly failures.

**Why resets change the task**: A reset provides the tracker with a new location after a failure. A system without this help must find the target or remain lost. The two protocols therefore do not expose the model to the same accumulation of errors or the same amount of external information.

**Proposed comparison**: Keep sequences, initialization, presence rule and loss criterion. Report failures and recovery periods in addition to location measurements. An average calculated only on successful frames can favor a method that abandons difficult cases. For a product, include the cost and time of the actual recovery procedure, whether automatic or human. Scores remain interpretable only with this evaluation contract.

**Measure of success**: A curve can report, for each threshold $\tau$, the proportion of frames where the IoU of the target exceeds $\tau$, under an announced presence policy. The area under this curve describes something other than the accuracy of the center at a fixed pixel threshold. Two boxes of the same center but of very different sizes can have a good center error and a bad IoU. The resets still change which periods are evaluated and what information is provided. Publishing the rules with the curve and the losses makes it possible to compare tradeoffs without retaining only the frames where the tracker has succeeded.

**Blocking errors**: Compare scores obtained with different reset rules without reporting it.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Wu, Lim and Yang 2013, OTB, §4: one-pass evaluation, precision and success plots](https://openaccess.thecvf.com/content_cvpr_2013/papers/Wu_Online_Object_Tracking_2013_CVPR_paper.pdf); [Kristan et al. 2016, VOT methodology, §3.1: failures, re-initialization and burn-in](https://arxiv.org/abs/1503.01313). The comparison protocol is a project construction.
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-CORRELATION-005 provenance::agent pole::C pole::D pole::E pole::F
END
