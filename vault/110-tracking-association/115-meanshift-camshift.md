# Flashcards — MeanShift and CamShift — tracking an appearance distribution

reference note: [[110-tracking-association/references/115-meanshift-camshift|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-MEANSHIFT-001

Objective: Explain a MeanShift iteration. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-001
Question: What does one MeanShift iteration compute on a backprojection image, and what should happen if the window contains no mass?
Reponse: **Expected answer**: Calculate the centroid of scores in the window, and then move the window to that center. If the total mass $M_{00}$ is zero, the centroid is indefinite: do not divide and apply an explicit loss/search policy.

**Further explanation**: $x_c=M_{10}/M_{00}$ and $y_c=M_{01}/M_{00}$ use weighted moments. The process looks for a local concentration and depends on initialization. The backprojection does not certify the identity of the object. OpenCV 4.13's `meanShift` does not report a zero mass: it stops and leaves the window unchanged, so the caller must compute $M_{00}$ to detect the loss.

**Reading moments**: The backprojection assigns a mass to each position according to its compatibility with the reference appearance. The weighted centroid gives a window shift towards this concentration. With two masses 1 and 3 placed at 10 and 14 pixels, the center is $(10+42)/4=13$ pixels: it is not the unweighted average of positions.

**Decision limit**: If the whole mass is zero, no mean position is defined by these observations. An arbitrary numerical output would mask a lack of information. Report the loss or apply a declared search policy, and then evaluate this policy. Even with a positive mass, a background of similar color can attract the window, so the concentration found does not verify the identity of the initialized object.

**Weighted iteration**: For scores $p(x,y)\ge0$ in window $W$, the displacement of the current center $c$ is $m(c)=\sum_Wp(x,y)(x,y)^T/\sum_Wp(x,y)-c$, in this uniform window model. Multiplying all scores by the same positive constant does not change the centroid; adding a uniform mass can instead move it towards the geometric center of the window. This distinction explains why normalizing the histogram and changing its contrast are not always equivalent operations. The stopping criterion measures a displacement or an iteration budget, without establishing that the mode found represents the original object.

**Total mass and centroid convey different evidence**: Multiplying every nonnegative backprojection score in a window by the same positive constant leaves its centroid unchanged while changing total mass. A weak diffuse response can therefore point to the same centroid as a strong response. Record both support and mass under the chosen score normalization, with a distinct zero-mass outcome. A converged window position alone does not establish that the target remains visible.

**Blocking errors**: Dividing by a zero mass; presenting the reached mode as a guaranteed global maximum.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13.0, camshift.cpp L44–L107: centroid iteration, integer shift and silent stop on zero mass](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L107); [Comaniciu et al. 2003, §4.1–4.2, eqs. 11–13: mean-shift step as a weighted average and local maximum](https://www.cs.ucf.edu/courses/cap6412/2003/Kernel-based%20object%20tracking.pdf). Added reasoning: project deduction.
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-MEANSHIFT-001 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-002

Objective: distinguish MeanShift and CamShift. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-002
Question: The target approaches the camera, but the tracking window remains too small. What does CamShift add compared with usual MeanShift?
Reponse: **Expected answer**: The usual MeanShift moves a window of fixed size; CamShift adapts size and orientation to the observed distribution, using its moments. This treats a projected appearance variation, not a metric estimate of pose.

**Further explanation**: An adaptation can also include background or a distractor if the backprojection is poor. Compare the two with an identical histogram and initialization, measuring overlap and losses, without concluding universal robustness. In OpenCV 4.13, the returned box spans 4 times the square root of each eigenvalue, that is $\pm2$ standard deviations of the weights, so it is about 1.15 times larger than a uniform blob.

**Why the scale changes**: When the target occupies a larger area in the image, a fixed window may contain only a portion of it or lose its appearance center. The moments of the distribution provide the information needed to adapt the window to the observed projected extent.

**Example of limit**: If a distractor of the same color enters the region, it also contributes to the moments. The window can expand for a bad reason, without the algorithm detecting this confusion. Compare position, overlap and size on scale-change sequences with a constant histogram. Then check illumination and occlusion separately. The adaptation solves one dimension of the tracking contract; it provides no depth or guaranteed identity, and a rotated box in the image is not a 3-D pose.

**Moments of extent**: Around the centroid, the matrix of normalized central moments $\begin{bmatrix}\mu_{20}&\mu_{11}\\\mu_{11}&\mu_{02}\end{bmatrix}/M_{00}$ describes the 2-D dispersion of the mass. Its eigenvectors give the principal axes; its eigenvalues give the extent according to a window conversion convention. Close eigenvalues make the orientation undetermined, as for an almost circular distribution. These quantities describe the backprojection in the image plane, not the 3-D physical axes of the part. A distractor can change center, orientation and size simultaneously. The appearance mask should therefore be inspected before interpreting an adapted window as a reliable geometric measurement of the target.

**Moment orientation becomes ambiguous for a round distribution**: If the two eigenvalues of the normalized second-moment matrix are nearly equal, its dominant axis is weakly defined. Small changes in scores can rotate the fitted ellipse greatly without much change in the underlying nearly circular distribution. Avoid interpreting that angle as stable object orientation or metric pose. A proposed validation separates center/scale tracking from orientation reliability on elongated and symmetric targets.

**Blocking errors**: Confusing a 2-D oriented box with a 3-D orientation; claiming reliable adaptation under any occlusion.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13.0, camshift.cpp L110–L218: CamShift moments, box size and orientation](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L110-L218); [Bradski, US patent 6,394,557 B2: continuously adapting window from the moments](https://patents.google.com/patent/US6394557B2/en). Added reasoning: project deduction.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-MEANSHIFT-002 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-003

Objective: Diagnose a color distractor. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-003
Question: CamShift jumps to another part of the same color. Why can increasing the number of iterations make the problem worse?
Reponse: **Expected answer**: The histogram model does not necessarily distinguish the two parts. More iterations may converge more firmly on the wrong concentration. Inspect the backprojection, the ROI and the target/background separation before tuning the stopping criterion.

**Further explanation**: Keep a loss policy, and add texture information or a detector if identity matters. A strong color peak can be correct for the statistical model and wrong for the application need.

**Distinction between model and application objective**: The distribution may have a strong mode on the distractor because it matches the histogram. Converging to this mode is compatible with the appearance criterion, while being false for the desired identity. The problem then comes from the information that distinguishes the targets, not just the number of iterations.

**Proposed investigation**: Display the backprojection and the window at the moment of the jump, then compare a mask or a more discriminating representation with the tracker unchanged. Test reacquisition after occlusion and the cases where the background changes. A texture addition or a detection can bring a new observation; it is still necessary to check its association. If the parts remain visually identical, acknowledge the ambiguity and define a loss policy rather than turning a color score into certainty.

**Identity missing from histogram**: A histogram retains color frequencies and loses most of their spatial arrangement. Two different objects can therefore produce very similar distributions, even with a high backprojection mass. An ROI containing more pixels of the desired color can attract the window without being the target. Testing a background of the same color and then a textured distractor makes it possible to verify this hypothesis. Adding a spatial descriptor or detection changes the information used and requires a new evaluation; increasing the number of iterations does not restore the spatial relationships that the histogram model has discarded.

**Convergence can strengthen a semantically wrong mode**: Two same-color parts can create two backprojection modes. MeanShift moves according to the local score mass, with no built-in physical identity label. More iterations can reduce numerical movement while converging to the wrong part. Test controlled distractors and inspect the mode structure before changing stopping criteria. A geometric motion limit or richer appearance model is a project intervention that needs its own measured tradeoff.

**Blocking errors**: Equating MeanShift convergence with correct identity.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [Comaniciu et al. 2003, §4.2: basin of attraction and assumption of a unique local maximum](https://www.cs.ucf.edu/courses/cap6412/2003/Kernel-based%20object%20tracking.pdf); [OpenCV 4.13.0, imgproc.hpp L3322–L3360: back-projection of a histogram](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L3322-L3360). Added reasoning: project deduction.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-MEANSHIFT-003 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-004

Objective: Evaluate color and adaptation separately. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-004
Question: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?
Reponse: **Expected answer**: Keep the same histogram, frames, and initialization; compare fixed window and adaptive window on a scale change. Measure center, overlap, size, and losses, and then separately test a histogram change.

**Further explanation**: Then add illumination and distractors one factor at a time. Low-saturation pixels make hue uninformative; document the masks and channels used. These variations are proposed and have not been executed on video here.

**The logic of ablation**: Changing only the window adaptation tests its effect on the location contract. Modifying the histogram at the same time changes the masses on which the displacement is calculated, which prevents assigning the improvement to a single mechanism.

**Constructed experiment**: Use one sequence where the target gradually grows, then another where a distractor appears without scaling. Keep the same loss and reset criteria, and report errors on all frames. An adaptive window can help the first case and harm the second if the mass of the distractor distorts it. The comparison must make this tradeoff visible. Channels, bins and masks are parameters of the appearance model; their setting requires another ablation and held-out data.

**Two factors, four tests**: To distinguish adaptation and appearance, compare histogram H1 with fixed/adaptive window, then histogram H2 with the same two policies. Measure overlap, center error and losses with identical initialization and sequences. The interaction can be important: an adaptive window benefits from a clean backprojection but encompasses more background with a poorly separated histogram. A change of binning modifies the trade-off between color discrimination and noise robustness; a low-saturation mask further changes the retained pixels. These choices must be recorded separately to make the result reproducible and attributable to the mechanism actually modified.

**Constructed example (reading the four tests)**: take mean IoU on the scale-change sequence of 0.48 for histogram H1 with a fixed window, 0.60 for H1 with CamShift, 0.56 for H2 fixed and 0.62 for H2 with CamShift (recomputed in the check script of this pass). Changing both at once gains 0.14, which a report might credit to CamShift. Adaptation is worth 0.12 with H1 but 0.06 with H2 (main effect 0.09); the histogram is worth 0.08 with a fixed window and 0.02 with CamShift (main effect 0.05); the interaction, $-0.06$, says that the better histogram already recovers part of what adaptation brought. The single comparison cannot split the gain, since $0.14=0.12+0.02=0.08+0.06$.

**A box convention that mimics an effect**: OpenCV's CamShift returns $4\sqrt{\lambda}$ per principal axis, that is $\pm2$ standard deviations of the weights [camshift.cpp L172–L173]. For a uniformly weighted $40\times20$ px blob this gives $46.2\times23.1$ px, so even a perfectly centred box has an IoU of 0.75 with a tight annotation, against 1 for a fixed window of the right size. On a sequence without scale change, the adaptive arm therefore loses about 0.25 IoU by convention alone. Report centre error and the box-to-target area ratio beside IoU, or calibrate a box factor on frames without distractors, before attributing an IoU change to adaptation.

**Blocking errors**: Changing histogram, mask and tracker at the same time and attributing the result to CamShift alone. Reading an IoU loss of CamShift at constant scale as an adaptation failure without accounting for its $\pm2\sigma$ box.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13.0, samples/python/camshift.py L82–L102: mask, hue histogram and CamShift call](https://github.com/opencv/opencv/blob/4.13.0/samples/python/camshift.py#L82-L102); [OpenCV 4.13.0, camshift.cpp L110–L218: adaptive window, box length and width $4\sqrt{\lambda}$ at L172–L173](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L110-L218). The factorial protocol, its numbers and the uniform-blob IoU are project constructions.
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-MEANSHIFT-004 provenance::agent pole::C pole::D pole::E
END
