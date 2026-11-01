# Flashcards — Optical flow: Lucas–Kanade, Farnebäck and RAFT

reference note: [[100-mouvement-video/references/101-flot-optique|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-FLOT-001

Objective: interpret the constraint of the flow. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-001
Question: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?
Reponse: **Expected answer**: An equation does not constrain two unknowns without assumptions/neighboring; an edge can keep a tangential ambiguity.

**Further explanation**: Lucas – Kanade aggregates locally and depends on conditioning; the pyramid does not create the missing texture.

**Reading the constraint**: The spatial gradient provides a direction in which a variation in intensity informs displacement. The movement tangent to a uniform edge changes little the intensities: several vectors can then satisfy the same equation. This is a lack of local information, not necessarily a mistake of the solver.

**Example and Limit**: A vertical edge that slides upwards may seem almost unchanged in a small window. Adding pixels of the same edge does not create a second independent direction. A neighbourhood with a corner can better constrain the two components if the movement remains sufficiently coherent and the photometry stable. Examine conditioning, window size, and hypothesis validity before increasing iterations. A regularization can choose one of several plausible solutions; it then adds a hypothesis, and not a certain observation of the displacement.

**Lucas – Kanade System**: stack the window gradients in a $A$ matrix with each row equal to $(I_x,I_y)$, and set $b=-I_t$. The least squares give $A^TA\,d=A^Tb$, with $d=(u,v)^T$. Two sufficiently informative eigenvalues of $A^TA$ are required to constrain both directions; an edge typically produces a weak direction. Expanding the window may bring new gradients, but possibly violates the assumption of shared motion by mixing two objects. A good selection of points therefore simultaneously seeks spatial information and neighborhood coherence, not just a large gradient amplitude.

**Blocking errors**: Saying that a high gradient guarantees two precise components.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html); [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039); [Teed – Deng, RAFT, figure 1 and presentation of all-pair correlations and updates](https://arxiv.org/html/2003.12039v3), see 2026-10-30.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FLOT-001 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-002

Objective: respect the temporal unity. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-002
Question: An optical flow vector represents 4 pixels between two images. Does this imply a velocity of 4 px/s?
Reponse: **Expected answer**: No: it takes the time interval, for example 4 px at 20 ms gives 200 px/s in this model.

**Further explanation**: Keep flow direction, resolution, timestamp and masks; compare moves at different rates without conversion is misleading.

**Breakdown of units**: The stream connects a position of the source image to a position of the destination image. Dividing the displacement by the difference of the timestamps gives an average image speed over this interval, provided that the match is valid. It is not automatically an instantaneous speed or a movement in the world.

**Constructed example**: four pixels in 40 ms give 100 px/s, half as many as four pixels in 20 ms. A resize by a factor of two also changes the number of moving pixels, without doubling the physical speed of the object. To pass in m/s, it takes a geometry and a scale adapted, often related to the depth. A moving camera can produce flow on a motionless object. Retaining this information avoids interpreting a large vector as evidence of rapid object movement.

**Change of grid**: If the second string works on an image resized by $(s_x,s_y)$, the same displacement becomes $(s_xu,s_yv)$. To compare image speeds, first put the vectors in a common grid and then use the real acquisition intervals. A lost frame eventually doubles the interval, without the physical speed having doubled. In perspective, even a constant 3D translation produces depth-dependent image displacements; an apparent size variation can also change the field. The conversion pixels→meters therefore requires a scene and camera model, beyond a division by the nominal rate.

**Blocking errors**: Confound frame displacement and speed per second.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html); [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039); [Teed – Deng, RAFT, figure 1 and presentation of all-pair correlations and updates](https://arxiv.org/html/2003.12039v3), see 2026-10-30.
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FLOT-002 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-003

Objective: situer RAFT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-003
Question: What distinct roles do correlations and recurrent updates play in RAFT?
Reponse: **Expected answer**: Correlations represent cross-position compatibility; updates refine the flow estimate.

**Further explanation**: Output is a dense movement between two images, not the persistence of an object ID on any video.

**Roles in the calculation**: Correlation representation gathers compatibility between positions of the two images. Recurring updates query this information and context to gradually correct a displacement estimate. The repetition of the updates is about the refinement of the observed pair; it is not enough to define an identity memory on an entire sequence.

**Example of distinction**: Two people crossing each other can produce a useful field of motion between two frames without an identity being retained after a long occlusion. A tracking system will still have to define objects, associations and life cycle. To evaluate the flow, use reference displacements, visible and occulted regions, and image units. Increasing the number of iterations changes a computational compromise; this does not guarantee the disappearance of all physical ambiguities.

**Dimensions of Correlation**: for two feature maps $h\times w$, an all-peer compatibility connects each site of the first to each site of the second, $(hw)^2$ values before optimizations. The volume encodes candidate similarities, not a bijective assignment of pixels. Updates look at this volume around predicted positions and adjust the flow; multiple sources may target a nearby region, and occlusionss do not always offer a match. Separating memory from volume, cost per iteration, and number of iterations helps to understand the resolution compromise. The recurrence of refinement is not a guarantee of physical convergence or identity.

**Blocking errors**: Describe a recurring memory of refinement as a guaranteed re-identification.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html); [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039); [Teed – Deng, RAFT, figure 1 and presentation of all-pair correlations and updates](https://arxiv.org/html/2003.12039v3), see 2026-10-30.
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-FLOT-003 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-004

Objective: process a occlusion. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-004
Question: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?
Reponse: **Expected answer**: As an estimate under the assumptions of the model, with no guaranteed observable correspondence; examine occlusion mask and consistency.

**Further explanation**: Compare round trip and reference when possible, without using true visibility at inference.

**Why density doesn’t prove anything**: A dense algorithm can fill regions where the data no longer contains a visible match. The value produced can come from context, regularization, or a learned model. These mechanisms give a useful hypothesis, but not a new observation of the hidden surface.

**check**: distinguish occlusion, field exit and matching error. For a round trip, evaluate the inverse flow at the position reached in the other image, taking into account the interpolation and the limits of the field. An inconsistency signals a possible problem; consistency does not guarantee identity on a repetitive texture. Measure regions separately according to an announced visibility protocol. At the inference, a ground truth of occlusion is not magically available: the trust policy must use only the information actually provided to the system.

**residual round trip**: note $F_{12}$ moving the 1 image to 2 and $F_{21}$ back. For a pixel $x$ of the first image, calculate $e(x)=\|F_{12}(x)+F_{21}(x+F_{12}(x))\|$ in pixels, only when the return sampling is valid. A trust rule can compare this residual to a tolerance dependent on movement and noise, to be validated on reserved data. A periodic texture can produce an erroneous translation and then its exact opposite: the zero residual then proves nothing on the real surface. Keep the visibility failure distinct from a simple large digital residual.

**Blocking errors**: Declare any vector calculated as validated physical displacement.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html); [RAFT, §§3.1 – 3.3](https://arxiv.org/abs/2003.12039); [Teed – Deng, RAFT, figure 1 and presentation of all-pair correlations and updates](https://arxiv.org/html/2003.12039v3), see 2026-10-30.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FLOT-004 provenance::agent pole::B pole::C pole::D
END
