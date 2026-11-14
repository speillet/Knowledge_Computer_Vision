# Flashcards — Optical flow: Lucas–Kanade, Farnebäck and RAFT

reference note: [[100-mouvement-video/references/101-flot-optique|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-FLOT-001

Objective: interpret the constraint of the flow. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-001
Question: Why does $I_xu+I_yv+I_t=0$ fail to determine a unique 2D motion at a pixel?
Reponse: **Expected answer**: One equation cannot constrain two unknowns without extra assumptions or neighboring pixels; along an edge, the tangential component remains ambiguous.

**Further explanation**: Lucas–Kanade aggregates locally and depends on conditioning; the pyramid does not create the missing texture.

**Reading the constraint**: The spatial gradient gives the direction in which a change of intensity informs the displacement. Motion tangent to a uniform edge barely changes the intensities, so several vectors satisfy the same equation. This is missing local information, not necessarily a solver error.

**Example and limit**: A vertical edge that slides upwards can look almost unchanged in a small window. Adding pixels of the same edge does not create a second independent direction. A neighborhood containing a corner constrains both components better if the motion stays coherent and the photometry stable. Examine conditioning, window size and the validity of the assumptions before increasing iterations. A regularization can choose one of several plausible solutions; it then adds an assumption, not a certain observation of the displacement.

**Lucas–Kanade system**: Stack the window gradients in a matrix $A$ whose rows are $(I_x,I_y)$, and set $b=-I_t$. Least squares give $A^TA\,d=A^Tb$, with $d=(u,v)^T$. Both eigenvalues of $A^TA$ must be sufficiently large to constrain both directions; an edge typically produces one weak direction. Enlarging the window may bring new gradients, but may violate the assumption of shared motion by mixing two objects. Good point selection therefore seeks spatial information and neighborhood coherence together, not just a large gradient magnitude.

**Brightness constancy is a model assumption**: A flashing light can change $I_t$ without any physical motion, while an edge translating along itself can produce almost no detectable intensity change. Both examples break a naive identification of brightness change with unique motion. Gradient diversity addresses local geometric observability; it does not repair a photometric model violated by lighting or reflections. A proposed diagnostic separates controlled illumination changes from known geometric translations.

**Blocking errors**: Claiming that a large gradient magnitude guarantees both components precisely.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [Lucas and Kanade 1981, §4.1 linearization and §4.5 two-dimensional least squares](https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf); [Bouguet, pyramidal LK report, §2.3 invertibility of G](http://robots.stanford.edu/cs223b04/algo_tracking.pdf); [OpenCV 4.13.0 optical flow tutorial source, optical flow equation and Lucas–Kanade method](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FLOT-001 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-002

Objective: Respect the time unit. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-002
Question: An optical flow vector represents 4 pixels between two images. Does this imply a velocity of 4 px/s?
Reponse: **Expected answer**: No: the time interval between the two frames is needed; for example, 4 px over 20 ms gives 200 px/s in this model.

**Further explanation**: Keep the flow direction, resolution, timestamps and masks; comparing displacements measured at different frame rates without conversion is misleading.

**Breakdown of units**: The flow links a position in the source image to a position in the destination image. Dividing the displacement by the timestamp difference gives an average image-plane speed over this interval, provided that the match is valid. It is not automatically an instantaneous speed or a motion in the world.

**Constructed example**: Four pixels in 40 ms give 100 px/s, half the speed of four pixels in 20 ms. Resizing the image by a factor of two also changes the displacement in pixels without changing the physical speed of the object. Converting to m/s requires geometry and an appropriate scale, often depth-dependent. A moving camera can produce flow on a motionless object. Keeping this information avoids reading a large vector as evidence of fast object motion.

**Change of grid**: If a second pipeline works on an image resized by $(s_x,s_y)$, the same displacement becomes $(s_xu,s_yv)$. To compare image speeds, first put the vectors on a common grid, then use the real acquisition intervals. A dropped frame can double the interval without the physical speed having doubled. Under perspective, even a constant 3D translation produces depth-dependent image displacements, and a change of apparent size also changes the field. Converting pixels to meters therefore requires a scene and camera model, beyond a division by the nominal frame rate.

**The timestamp interval belongs to each pair**: A fixed displacement of 4 px means 200 px/s at 20 ms but 80 px/s at 50 ms. Variable frame intervals therefore require pair-specific timestamps rather than a nominal frame rate. If timestamps refer to reception instead of exposure, packet jitter can create a spurious velocity variation. This is an image-plane average velocity under the temporal model; converting to object-space speed needs geometry and potentially ego-motion compensation.

**Blocking errors**: Confusing the displacement per frame pair with a speed per second.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [OpenCV 4.13.0 optical flow tutorial source, optical flow equation with $u=dx/dt$](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown); [Teed and Deng 2020, RAFT, §3.3 upsampling of 1/8-resolution flow](https://arxiv.org/abs/2003.12039). Unit conversions and grid changes are project deductions; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FLOT-002 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-003

Objective: Situate RAFT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-003
Question: What distinct roles do correlations and recurrent updates play in RAFT?
Reponse: **Expected answer**: Correlations represent cross-position compatibility; updates refine the flow estimate.

**Further explanation**: The output is a dense motion field between two images, not the persistence of an object identity across a video.

**Roles in the computation**: The correlation volume gathers the compatibility between positions of the two images. Recurrent updates query this information and context to correct a displacement estimate step by step. Repeating the updates refines the observed pair; it does not define an identity memory over a whole sequence.

**Example of the distinction**: Two people crossing can produce a useful motion field between two frames without any identity being kept after a long occlusion. A tracking system still has to define objects, associations and the track life cycle. To evaluate the flow, use reference displacements, visible and occluded regions, and image units. Increasing the number of iterations changes a computational trade-off; it does not remove every physical ambiguity.

**Dimensions of the correlation**: For two feature maps of size $h\times w$, an all-pairs comparison links each site of the first to each site of the second, $(hw)^2$ values before optimizations. The volume encodes candidate similarities, not a one-to-one assignment of pixels. The updates read this volume around the predicted positions and adjust the flow; several source pixels may point to the same region, and occlusions do not always offer a match. Separating the volume's memory, the cost per iteration and the number of iterations helps to understand the resolution trade-off. Repeated refinement guarantees neither physical convergence nor identity.

**A correlation maximum is not yet the flow field**: For one pixel, several locations in a repeated pattern can have high feature correlation. A recurrent update combines lookup evidence with its current estimate and learned spatial context to refine the field. Taking an independent maximum from each correlation row would define another algorithm and can lose coherent motion. The architecture's dense output still requires evaluation at occlusions, boundaries and domain shifts rather than assuming correlation resolves every ambiguity.

**Blocking errors**: Describing the recurrent refinement state as a guaranteed re-identification memory.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [Teed and Deng 2020, RAFT, §3.2 correlation volume and lookup, §3.3 iterative updates, §4.3 inference updates](https://arxiv.org/abs/2003.12039); [RAFT official code, core/corr.py at commit 2888e15](https://github.com/princeton-vl/RAFT/blob/2888e15a51fa41140771d3f498ed8023cff098d1/core/corr.py). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-FLOT-003 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-004

Objective: Handle an occlusion. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FLOT-004
Question: A point becomes invisible, but the optical flow model still returns a vector. How should this output be interpreted?
Reponse: **Expected answer**: As an estimate under the assumptions of the model, with no guaranteed observable correspondence; examine occlusion mask and consistency.

**Further explanation**: Compare round trip and reference when possible, without using true visibility at inference.

**Why density proves nothing**: A dense algorithm can fill regions where the data no longer contain a visible match. The value can come from context, regularization or a learned model. These mechanisms give a useful hypothesis, but not a new observation of the hidden surface.

**Discriminating check**: Distinguish occlusion, exit from the field of view and matching error. For a round trip, evaluate the backward flow at the position reached in the other image, taking interpolation and the field limits into account. An inconsistency signals a possible problem; consistency does not guarantee identity on a repetitive texture. Measure regions separately under a stated visibility protocol. At inference, no ground-truth occlusion is available: the confidence policy may use only the information actually given to the system.

**Round-trip residual**: Let $F_{12}$ map image 1 to image 2 and $F_{21}$ map back. For a pixel $x$ of the first image, compute $e(x)=\|F_{12}(x)+F_{21}(x+F_{12}(x))\|$ in pixels, only where the return sampling is valid. A confidence rule can compare this residual with a tolerance that depends on motion and noise, validated on held-out data. A periodic texture can produce a wrong translation and then its exact opposite: a zero residual then proves nothing about the real surface. Keep a visibility failure distinct from a merely large numerical residual.

**Blocking errors**: Declaring every computed vector a validated physical displacement.
Source: [[100-mouvement-video/references/101-flot-optique|Full reference]]; [Butler et al. 2012, MPI-Sintel, §4 unmatched pixels](http://files.is.tue.mpg.de/black/papers/ButlerECCV2012.pdf); [OpenCV 4.13.0 lk_track.py, backward check L56–L59](https://github.com/opencv/opencv/blob/4.13.0/samples/python/lk_track.py#L56-L59); [Teed and Deng 2020, RAFT, §3](https://arxiv.org/abs/2003.12039). The round-trip rule is a project construction.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FLOT-004 provenance::agent pole::B pole::C pole::D
END
