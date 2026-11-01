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

**Further explanation**: $x_c=M_{10}/M_{00}$ and $y_c=M_{01}/M_{00}$ use weighted moments. The process looks for local concentration and depends on initialization. The backprojection does not certify the identity of the object.

**Reading moments**: The backprojection assigns a mass to each position according to its compatibility with the reference appearance. The weighted centroid gives a window shift towards this concentration. With two masses 1 and 3 placed at 10 and 14 pixels, the center is $(10+42)/4=13$ pixels: it is not the unweighted average of positions.

**Decision limit**: If the whole mass is zero, no mean position is defined by these observations. An arbitrary digital output would mask a lack of information. Report the loss or apply an advertised search, and then evaluate this policy. Even with a positive mass, a background of similar color can attract the window, so the concentration found does not verify the identity of the initialized object.

**Weighted iteration**: For $p(x,y)\ge0$ scores in window $W$, the current center displacement $c$ is $m(c)=\sum_Wp(x,y)(x,y)^T/\sum_Wp(x,y)-c$, in this uniform window model. A common multiplication of all scores by a positive constant does not change the centroid; adding a uniform mass can instead move it towards the geometric center of the window. This distinction explains why normalizing the histogram and changing its contrast are not always equivalent operations. The stop criterion measures a move or budget of iterations, without establishing that the found mode represents the original object.

**Blocking errors**: Divide by zero mass; present the achieved mode as a guaranteed global maximum.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-MEANSHIFT-001 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-002

Objective: distinguish MeanShift and CamShift. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-002
Question: The target approaches the camera, but the tracking window remains too small. What does CamShift add compared with usual MeanShift?
Reponse: **Expected answer**: The usual MeanShift moves a window of fixed size; CamShift adapts size and orientation to the observed distribution, using its moments. This treats a projected appearance variation, not a metric estimate of pose.

**Further explanation**: An adaptation can also include background or distractor if the backprojection is bad. Compare the two to identical histogram and initialization, measuring overlap and losses, without concluding to universal robustness.

**Why the scale is evolving**: When the target occupies a larger area in the image, a fixed window may contain only a portion of it or lose its center of appearance. The timings of the distribution provide indications for adapting a window to the projected extent observed.

**Example of limit**: If a distractor of the same color enters the region, it also contributes to the moments. The window can expand for a bad reason, without the algorithm detecting this confusion. Compare position, overlap, and size on scale-shifting sequences at constant histogram. Then check illumination and occlusion separately. The adaptation solves one dimension of the tracking contract; it provides no depth or guaranteed identity, and a box shot in the image is not a pose 3D.

**Moments of extent**: Around the centroid, the matrix of normalized central moments $\begin{bmatrix}\mu_{20}&\mu_{11}\\\mu_{11}&\mu_{02}\end{bmatrix}/M_{00}$ describes the dispersion 2D of the mass. Its own directions give main axes; their values inform the extent according to a window conversion convention. Close values make the orientation undetermined, as for an almost circular distribution. These quantities describe the backprojection in the image plane, not the physical axes 3D of the part. A distractor can change center, orientation and size simultaneously. The appearance mask should therefore be inspected before interpreting a suitable window as a reliable geometric measurement of the target.

**Blocking errors**: Confound box oriented 2D and orientation 3D; announce a reliable adaptation in any occlusion.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-MEANSHIFT-002 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-003

Objective: Diagnose a color distractor. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-003
Question: CamShift jumps to another part of the same color. Why can increasing the number of iterations make the problem worse?
Reponse: **Expected answer**: The histogram model does not necessarily distinguish the two pieces. More iterations may converge more towards the wrong concentration. Inspect the backprojection, ROI, and target/bottom separation before setting the stop.

**Further explanation**: Keep a loss policy, add texture information or a detector if identity matters. A strong color peak can be correct for the statistical model and false for the business need.

**Distinction between model and business objective**: The distribution may have a strong mode on the distractor because it matches the histogram. Converging to this mode is compatible with the appearance criterion, while being false for the desired identity. The problem then comes from the information that distinguishes the targets, not just the number of iterations.

**Proposed investigation**: display backprojection and window at the moment of the jump, then compare a mask or a more discriminating representation to constant tracker. Test the return after occlusion and the cases where the background changes. A texture addition or a detection can bring a new observation; it is still necessary to check its association. If the pieces remain visually identical, recognize ambiguity and define a policy of loss rather than turning a color score into certainty.

**Identity missing from histogram**: A histogram retains color frequency and loses much of their spatial arrangement. Two different objects can therefore produce very similar distributions, even with a high backprojection mass. An ROI containing more pixels of the desired color can attract the window without being the target. Testing a background of the same color and then a textured distractor makes it possible to verify this hypothesis. Adding a spatial descriptor or detection changes the information used and requires a new evaluation; increasing the number of iterations does not restore the spatial relationships that the histogram model has deleted.

**Blocking errors**: Assimilate convergence of MeanShift and good identity.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-MEANSHIFT-003 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-004

Objective: Evaluate color and adaptation separately. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-MEANSHIFT-004
Question: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?
Reponse: **Expected answer**: Keep the same histogram, frames, and initialization; compare fixed window and adaptive window on a scale change. Measure center, overlap, size, and losses, and then separately test a histogram change.

**Further explanation**: Then add illumination and distractors one factor at a time. Low-saturated pixels make the shade little informative; document the masks and channels used. These variations are proposed and have not been executed on video here.

**The logic of ablation**: Changing only the window adaptation tests its effect on the location contract. Modifying the histogram at the same time changes the masses on which the displacement is calculated, which prevents assigning the improvement to a single mechanism.

**Experience built**: Use one sequence where the target gradually grows, then another where a distractor appears without scaling. Keep the same loss and reset criteria, and report errors on all frames. An adaptive window can help the first case and harm the second if the mass of the distractor distorts it. The comparison must make this compromise visible. Channels, bins and masks are parameters of the appearance model; their setting requires another ablation and reserved data.

**Two factors, four tests**: To distinguish adaptation and appearance, compare histogram H1 with fixed/adaptive window, then histogram H2 with the same two policies. Measure overlap, center error and initialization losses and identical sequences. The interaction can be important: an adaptive window benefits from a clean backprojection but encompasses more background with a poorly separated histogram. A change of binning modifies the trade-off between color discrimination and noise robustness; a low-saturation mask further changes the retained pixels. These choices must be recorded separately to make the result reproducible and attributable to the mechanism actually modified.

**Blocking errors**: Simultaneously edit histogram, mask and tracker and assign the result to CamShift alone.
Source: [[110-tracking-association/references/115-meanshift-camshift|Full reference]] ; [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-MEANSHIFT-004 provenance::agent pole::C pole::D pole::E
END
