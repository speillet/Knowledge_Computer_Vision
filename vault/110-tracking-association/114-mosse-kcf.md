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

**Further explanation**: Initialization provides the target and synthetic responses around it. The search is local; a target exited from this region does not reappear by adapting the filter alone. Do not confuse mono-object tracking and detection of all objects.

**Interpretation of the answer**: Each candidate move in the search region receives a model-like score. The peak locates the preferred hypothesis, but its contrast and the presence of competitors must be examined before an update. The search area already expresses a hypothesis about possible movement.

**Constructed example**: A target moving beyond this area can leave the background with the best available peak. Learning then this background transforms a loss of location into a persistent drift of the model. Define a loss and recovery policy, then test it on big moves and occlusions. Correlation speed is useful only if the research and update assumptions are suitable as needed.

**From the pic to the image**: The answer is calculated in the coordinates of the patch or its features. Converting the maximum offset to the image requires the origin of the crop, its resizing, and any stride. A circular correlation convention also requires interpreting near-edge indices as appropriate signed offsets. An error here can produce a jump despite a correctly calculated peak. Check a known synthetic translation and return to the coordinate frame image before setting the trust. The possible subpixel location refines the peak estimation; it does not guarantee equivalent physical accuracy on real images.

**A search crop defines the capture region**: If the target moves entirely outside the sampled search crop, a response maximum still exists inside that crop but need not correspond to the target. A reliability check and an explicit failure outcome are therefore essential. Evaluate search size against expected frame-to-frame motion and distractors. A larger crop increases candidate context and computation and can introduce stronger competing peaks; it is not a free guarantee of reacquisition.

**Blocking errors**: Update without check on any predicted box; promise global detection.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §IV, regression and circulant structure; project deductions](https://arxiv.org/html/1404.7584v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-CORRELATION-001 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-002

Objective: distinguish MOSSE and KCF. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-002
Question: What do cyclic shifts and kernels give KCF compared with a linear filter such as MOSSE?
Reponse: **Expected answer**: KCF structures the examples as cyclic offsets of the patch; the circulating matrix allows efficient Fourier calculations, including for compatible kernels. MOSSE learns a linear correlation filter adapted online.

**Further explanation**: The calculation gain depends on this structure and features. Cyclical shifts create artificial examples at the edges: speed does not remove biases. No paper SPF predicts that of the target material.

**Why Structure Helps**: offsets from the same patch are strongly related; treating them as a structured family avoids building a general procedure that is expensive for everyone. The Fourier domain exploits this organization in the chosen formulation. The gain is not a proof of realistic diversity of examples.

**Concrete limit**: A cyclic shift causes an edge on the other side of the patch to reappear. This artificial example may differ from the actual movement of a target in front of a background. check region size, features, edge and adaptation policy in a comparison to MOSSE. Measure quality and cost on the same protocol; using a kernel does not turn local search into global redetection or a peak score into a certain identity.

**Structured regression**: a regularized linear regression solves $\min_w\|Xw-y\|^2+\lambda\|w\|^2$. If the lines of $X$ are the cyclic shifts of the same signal, the circulant structure makes it possible to diagonalize the corresponding operations by Fourier transform. In a kernel regression, we work on a matrix of similarities whose structure must remain compatible. This explains the efficiency without assimilating a core to a deep network. The regularization parameter stabilizes learning according to the feature scale; it does not compensate for a target missing from the patch or an artificial edge hypothesis ill-suited to the scene.

**Cyclic training creates artificial boundary examples**: A circular shift wraps one side of a patch onto the other, which can create an artificial seam absent from a physical translation. Windowing and search-region design reduce some boundary effects under their assumptions. The Fourier diagonalization exploits this structured training set; it does not make arbitrary independent patches circulant. Compare border-crossing and large-displacement cases when testing whether the efficient model remains suitable for the target sequence.

**Blocking errors**: Present KCF as a deep detector; say that a kernel removes local search limits.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Henriques et al., KCF, §§4 – 5, circulant structure and kernels](https://arxiv.org/pdf/1404.7584); [Bolme et al., MOSSE, §3.1 – 3.2, edges and learning; mathematical complements and built protocols](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §IV, regression and circulant structure; project deductions](https://arxiv.org/html/1404.7584v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-CORRELATION-002 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-003

Objective: interpret a PSR. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-003
Question: A response has a peak of 0.8, an off-peak mean of 0.2 and an off-peak standard deviation of 0.1. What is the PSR, and what does it mean?
Reponse: **Expected answer**: PSR=$(0,8-0,2)/0,1=6$. The peak exceeds the bottom average by six standard deviations depending on the region outside the selected peak. It measures a response contrast, with no calibrated probability of a good target.

**Further explanation**: Define the excluded area and the treatment of a zero standard deviation. The threshold depends on the tracker, patch, and protocol. Distractors can produce a sharp spike for the wrong object.

**Calculation interpreted**: subtracting the off-peak mean measures the deviation from the background response; dividing by its standard deviation expresses this deviation in the background variation scale. A common multiplication of the response by a positive constant does not change this ideal ratio, if the region and the calculation remain the same.

**Proposed diagnosis**: View the response map and competing peaks, precisely define the excluded area and process a zero or near zero dispersion. On a repeat, the wrong object can produce a narrow, high peak. The PSR then correctly describes a contrast of response, without knowing the truth of identity. Its threshold is therefore assessed with real success, loss and distractors, rather than as a universal level of trust.

**Effect of a distractor**: If a second peak enters the area used to calculate average and standard deviation off peak, it can change the PSR of the first, even if its height remains the same. The size of the excluded area and the edges of the patch therefore participate in the definition of the score. A positive affine transformation $r'=ar+b$, with the same support and $a>0$, ideally retains the PSR, because numerator and standard deviation are multiplied by $a$. On the other hand, clipping, quantifying or changing the medium can break this invariance. The score is therefore comparable only with an identical calculation procedure and a threshold validated in its context.

**PSR is invariant to some response rescalings**: If the response map is transformed by $r\prime=ar+b$ with $a>0$ and the sidelobe region is unchanged, peak-minus-mean and standard deviation both scale by $a$, leaving PSR unchanged. A constant map instead has zero sidelobe standard deviation and requires a defined policy. This constructed relation explains why raw peak height and PSR measure different things, and why neither is a calibrated probability of correct identity.

**Blocking errors**: Interpret PSR=6 as 60 % confidence; apply a historical threshold to any method.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §IV, regression and circulant structure; project deductions](https://arxiv.org/html/1404.7584v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::raisonnement cv_id::CV-CORRELATION-003 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-004

Objective: Look for contamination of the model. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-004
Question: A correlation-filter tracker works before an occlusion, then persistently tracks the background. Which update error should be tested?
Reponse: **Expected answer**: It may have learned the background during frames where the target was hidden. Compare the model before/after occlusion, freeze low confidence updates and check competitor peaks and search region.

**Further explanation**: A quick adaptation tracks changes in appearance but also learns location errors. A detector or explicit reset may be required; freezing alone does not guarantee recovery.

**Chain of Failure**: a first error places the window on the background; an uncontrolled update integrates it; the adapted model then responds better to this background. Watching only the last box doesn’t say when this loop started.

**Constructed ablation**: Keep the same initialization and frames, then freeze only during a period of uncertainty. Compare the crops learned, the response contrast, the losses and the eventual return of the target. If the search region no longer contains the target, freezing is not enough: a relaunch or other observation is necessary. Also assess the legitimate appearance changes that the gel may misfollow, in order to choose an adaptation/protection compromise on the actual need.

**Separate research and learning**: Freeze updates retains a target model, but does not automatically change the region being crawled. After a long occlusion or a large shift, the target may return elsewhere and remain untraceable despite an intact model. Compare two separate interventions: freezing the model with unchanged search, then expanded search policy or detection with the same model. Measure false returns on distractors and recovery times, without using the true position to silently reset. This ablation distinguishes contamination, loss of spatial coverage and appearance ambiguity, which can produce a similar final box on the bottom.

**A learned distractor can make confidence self-reinforcing**: Once the update absorbs background appearance, later correlation peaks may look reliable relative to that altered model. Compare against a saved pre-occlusion model and inspect the update history before treating a high response as confirmation. A proposed intervention separates freezing updates from expanding search and reinitialization, since each changes a different mechanism. Evaluate false recovery as well as overlap after a successful reacquisition.

**Blocking errors**: Systematically increase the learning rate to correct drift.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §IV, regression and circulant structure; project deductions](https://arxiv.org/html/1404.7584v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-CORRELATION-004 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-005

Objective: Define an honest comparison of trackers. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CORRELATION-005
Question: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?
Reponse: **Expected answer**: Initialization and reset protocol, sequences, losses, overlap and center error, as well as full latency. A restart after error changes the evaluated task.

**Further explanation**: Keep the same frames and conditions of occlusion. Distinguish a one-pass protocol without restarting a protocol with resets. An average on only successful frames hides the most expensive failures.

**Why Resets Change the Task**: A reset provides the tracker with a new location after a failure. A system without this help must find the target or remain lost. The two protocols therefore do not expose the model to the same accumulation of errors or the same amount of external information.

**Proposed comparison**: keep sequences, initialization, presence rule and loss criterion. Report failures and recovery periods in addition to location measurements. An average calculated only on successful frames can favor a method that abandons difficult cases. For a product, include the cost and time of the actual recovery procedure, whether automatic or human. Scores remain interpretable only with this evaluation contract.

**Measure of success**: A curve can report, for each $\tau$ threshold, the proportion of frames where the IoU of the target exceeds $\tau$, under an announced presence policy. The area under this curve describes something other than the accuracy of the center at a fixed pixel threshold. Two boxes of the same center but of very different sizes can have a good center error and a bad IoU. The resets still change which periods are evaluated and what information is provided. Publishing the rules with the curve and the losses allows to compare the compromises without retaining only the frames where the tracker has succeeded.

**Resets inject new localization information**: Reinitializing a failed tracker from a ground-truth box supplies information unavailable to an uninterrupted tracker. Report reset rules, skipped frames, failure definitions and whether reset frames enter the score. A high post-reset overlap can coexist with frequent failures. Compare uninterrupted success and reset-based robustness under their respective protocols rather than pooling the resulting numbers as though they described the same task.

**Blocking errors**: Compare scores obtained with different reset rules without reporting it.
Source: [[110-tracking-association/references/114-mosse-kcf|Full reference]]; [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf); [Henriques et al., KCF, §IV, regression and circulant structure; project deductions](https://arxiv.org/html/1404.7584v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-CORRELATION-005 provenance::agent pole::C pole::D pole::E pole::F
END
