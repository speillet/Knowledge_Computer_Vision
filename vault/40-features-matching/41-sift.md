# Flashcards — SIFT — local features and multiscale descriptors

reference note: [[40-features-matching/references/41-sift|SIFT]]. Source of writing: Agent. Experimental format, not yet synchronized or evaluated in deferred recall.

TARGET DECK: CV::Pilote::40-features-matching

## CV-SIFT-001

Objective: Explain the components of a correspondence pipeline. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-001
Question: When registering two photos of a planar label, what does SIFT provide, and which additional steps are required to obtain a reliable transformation?
Reponse: **Expected answer**: SIFT provides keypoints and their local descriptors. The matcher offers pairs; filtering limits ambiguities; a geometric estimate tests a transformation adapted to the plane. The matches are not proof of registration.

**Further explanation**: Detection decides where to describe; the descriptor represents the neighborhood. A typical chain uses the L2 distance, the ratio test, then RANSAC with a homography, with inspection of the residuals and spatial coverage. The choice of a homography depends on the scene, not on the use of SIFT.

**Constructed decision chain**: For a known flat label, keep the keypoint coordinates in each image, compute the candidates and inspect their distribution before estimating the warp. Four misplaced matches or several ambiguous pairs do not become reliable because they come from SIFT. A consensus concentrated in one corner can also leave the extrapolation to the opposite edge poorly constrained.

**Interpretation of the result**: Check the geometry on points not used to fit it and in the area where the product must act. A part with relief may require a different model than a single homography. SIFT is responsible for the local representation; the pipeline must establish that a transformation explains the observations well enough for the stated use.

**Linking outputs to an estimate**: represent the points by two arrays $P_A\in\mathbb R^{n\times2}$ and $P_B\in\mathbb R^{m\times2}$, and their descriptors by two arrays with 128 columns. The matcher returns index pairs $(i,j)$, not the coordinates of a transformation. A robust estimate then uses the pairs $(P_A[i],P_B[j])$ in the same pixel contract as its threshold. If the extraction was done on a resized image, the estimated matrix relates these resized images; it must be composed with the preprocessing transformations to return to the original images. Keeping these index associations avoids confusing descriptor quality with coordinate-handling errors.

**Match count does not establish spatial support**: A constructed set of fifty matches concentrated on one tiny logo can constrain the logo while allowing large extrapolation error across the label. Record the convex-hull area or a spatial coverage statistic alongside inlier count, then evaluate transfer on independent corners of the whole target. Such a coverage rule is a project acceptance choice. It supplements residual checks because a small fitted error at observed points does not bound error outside their support.

**Blocking errors**: Saying that the descriptor directly estimates the pose, or that every nearest neighbor is a true match.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §1 and §7, recognition pipeline: matching, clustering and geometric verification](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf). Coordinate contract and coverage rule: project deductions.
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-SIFT-001 provenance::agent pole::B pole::E
END

## CV-SIFT-002

Objective: Explain the search for a characteristic scale. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-002
Question: In SIFT, what does the difference of Gaussians compare, and why are extrema also sought across scale?
Reponse: **Expected answer**: $D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma)$ compares two neighboring smoothings, with $L=G_\sigma*I$. Looking for a spatial and scale extremum aims to find a structure at its characteristic scale, rather than at an arbitrarily fixed radius.

**Further explanation**: $\sigma$ is a pixel scale, $k>1$ is the ratio between levels, and $G_\sigma$ is a normalized Gaussian kernel. The DoG approximates a Laplacian normalized in scale. The candidate is compared with 26 neighbors: eight in its level and nine in each adjacent level. Sampling, noise and loss of detail limit repeatability.

**Why scale matters**: The same detail covers more pixels as the camera gets closer. Looking only for maxima in a smoothed fixed-radius image then imposes a different neighborhood in both views. The search in the levels is aimed at a characteristic size of the structure, which is then used to calculate the descriptor.

**Interpreted example**: A small spot and the same enlarged spot can be selected at different levels. If the reduced image no longer contains enough samples to represent it, no level recreates the spot. The mechanism therefore helps to find a structure that is still observable; it does not remove the role of optics or pre-filtering before reduction.

**Why the DoG approximates a Laplacian**: for $k$ close to 1, a first-order expansion in scale gives $L(k\sigma)-L(\sigma)\approx(k-1)\sigma\,\partial L/\partial\sigma$. The Gaussian diffusion equation links this derivative to $\sigma\nabla^2L$: the difference is therefore proportional to a Laplacian normalized by $\sigma^2$. This approximation assumes a suitable spacing of scales; it is not an exact identity for every $k$. Detecting an extremum is only the beginning: local refinement estimates position and scale between samples, then low-contrast and edge-dominated rejections avoid describing unstable points. The same number of candidates does not mean the same number of reliable keypoints.

**Scale sampling and octave boundaries**: If an octave spans a factor of two and contains $s$ scale intervals, adjacent smoothing scales differ by $k=2^{1/s}$. Increasing $s$ samples scale more finely but increases the images and comparisons required per octave. Scale-space extrema also need adjacent scale levels, so boundary levels serve neighborhood construction rather than all yielding detections. This relationship explains a cost/repeatability tradeoff; it does not imply that arbitrarily fine sampling recovers detail already lost in the input.

**Blocking errors**: Confusing scale and orientation, or claiming perfect invariance to any change of resolution.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §3 eq. 1 and DoG approximation, §3.1 26 neighbors, §3.2](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [Rey-Otero and Delbracio 2014, IPOL §2–§3](https://doi.org/10.5201/ipol.2014.82). Interpreted example: project deduction.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-SIFT-002 provenance::agent pole::B pole::E
END

## CV-SIFT-003

Objective: justify the construction of the descriptor. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-003
Question: Once a SIFT keypoint is localized, how is its classical descriptor built, and what do the main steps seek to stabilize?
Reponse: **Expected answer**: Assign a dominant orientation, describe gradients in a scale-adapted and oriented neighborhood, and then form $4\times4$ cells with eight orientations, or 128 components. Normalize, trim large components and then renormalize.

**Further explanation**: Histogram representation and interpolation reduce sensitivity to small shifts. The orientation and scale give a local coordinate frame. Normalization mitigates some contrast changes, but does not recreate gradients lost by saturation or blur. A structure with several dominant orientations can give several descriptors.

**Reading the representation**: The components represent a distribution of gradient directions in neighboring cells, expressed with respect to local orientation. Two slightly offset patches can keep close histograms without having identical pixels. The spatial division, however, maintains a layout information: a simple global histogram would lose this organization more.

**Example of limit**: A saturated zone can make several intensities identical and remove an edge. Normalizing the vector cannot restore this missing gradient. To diagnose a drop in matches, distinguish an undetected keypoint, an unstable orientation and a non-distinctive descriptor. The 128 dimension explains the chosen structure, but does not constitute a measure of match quality or a guarantee of identification.

**Understanding normalization**: For a non-zero histogram vector $d$, dividing by $\|d\|_2$ cancels a common multiplicative gain; adding a constant to all intensities does not change their differences in the ideal model in the first place. On the other hand, if a few gradients dominate, they can swamp the contribution of other cells. Clipping followed by a new normalization limits this domination. Constructed example: two patches in which a single edge becomes much stronger can keep a similar directional layout while their raw norm changes. Interpolation between cells and orientation bins also prevents a small geometric variation from abruptly moving a whole contribution across a discrete boundary.

**Orientation ambiguity can create multiple descriptors**: A patch can contain two strong orientation modes. Keeping multiple supported orientations at one localized point creates several descriptors for that location, increasing matching opportunities but also descriptor count. These are alternative normalized views of the same local structure, rather than independent spatial observations for geometric fitting. Deduplicate or track point provenance when interpreting an apparent increase in match support, especially around repeated corners or symmetric markings.

**Blocking errors**: Describing 128 raw pixels, or claiming that normalization guarantees invariance to any lighting.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §5 orientation and §6.1 descriptor, normalization and 0.2 clipping](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf). Saturation example: project deduction.
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-SIFT-003 provenance::agent pole::B pole::E
END

## CV-SIFT-004

Objective: interpret the ratio test. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-004
Question: Two query descriptors have L2 distances $(20,21)$ and $(35,80)$ to their two nearest neighbors. With a ratio-test threshold of 0.8, which query is retained, and what does this test establish?
Reponse: **Expected answer**: reject the first ($20/21\approx0.952$), keep the second ($35/80=0.4375$). The test looks for a neighbor that is significantly more distinctive than its competitor; a small absolute distance is not enough.

**Further explanation**: we check $d_1<0.8\,d_2$ with $d_1\le d_2$. The choice of the threshold is a matter of validation. Even accepted, the match can be wrong in a repetitive structure: a geometric check remains necessary. Explicitly deal with the absence of two neighbors and the distances both zero.

**Reading the test**: The first candidate is close in absolute value but its competitor is almost as close: the query does not discriminate between the two. The second candidate is further away, but clearly separated from its competitor. The ratio compares this relative ambiguity and does not provide a probability of correct matching.

**Constructed tuning case**: On a repetitive texture, tightening the threshold can remove a large fraction of the points and leave too little coverage for a homography. On a distinctive image, an overly permissive threshold can increase false candidates. So choose the setting on geometric success and projection errors, keeping an exact reference for the two neighbors when the search is approximate.

**Beware of squared distances**: If a routine provides $s_1=d_1^2$ and $s_2=d_2^2$, the criterion equivalent to $d_1<\tau d_2$ is $s_1<\tau^2s_2$, not $s_1<\tau s_2$. With $\tau=0.8$, comparing squared distances directly with 0.8 would accept distance ratios up to about 0.894. This transformation is derived algebraically for positive distances; it does not say which convention a particular API uses. Read the function's contract and test a small known pair before reusing a threshold. The "second" neighbor must also come from the set of candidates defined by the protocol; changing the database changes the measured ambiguity.

**The second neighbor depends on the search population**: A ratio test compares distinctiveness within the descriptor population actually searched. Removing competing near-duplicate descriptors can make a match pass without changing its appearance. Conversely, a larger database can introduce legitimate close competitors. Record the database composition and nearest-neighbor approximation when transferring a threshold. If fewer than two valid neighbors exist, define a separate rejection or fallback policy; there is no measured second-neighbor ratio to apply.

**Blocking errors**: Automatically keeping the match at distance 20, inverting the ratio, or treating acceptance as physical truth.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §7.1 ratio test and Fig. 11](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [Rey-Otero and Delbracio 2014, IPOL §5](https://doi.org/10.5201/ipol.2014.82). Squared-distance algebra: project deduction.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-SIFT-004 provenance::agent pole::B pole::E
END

## CV-SIFT-005

Objective: Distinguish between the limits of invariances. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-005
Question: A planar object is first rotated within the image, then viewed from a very oblique angle. Why do these changes pose different challenges for SIFT?
Reponse: **Expected answer**: SIFT explicitly normalizes local orientation and scale. A strong oblique view distorts the patch in an affine/projective way and can change its visibility; it is not usually compensated by a simple rotation and a scale.

**Further explanation**: the invariances sought remain limited by detection and sampling. The existence of a homography between image planes does not mean that the descriptor is invariant to this homography. Lowe measured final matching accuracy above 50% only up to about a 50° tilt of a plane on his synthetic tests. Evaluate the actual angular range and compare a suitable strategy if the match rate becomes insufficient.

**Geometric decomposition**: A rotation in the plane preserves the local shape to within one rotation. An oblique view compresses the directions of the patch differently and may cause certain surfaces to appear or disappear. Gradients are no longer only expressed in a different orientation; their arrangement may change.

**Proposed test**: Take a flat label, fix lighting and sharpness, then separate rotation in the plane and tilt of the camera. Measure re-detection and match accuracy for each variation, instead of a single overall rate. A homography can describe the projection of the plane while being difficult to estimate for lack of reliable matches. Distinguishing the validity of the scene model and the robustness of the descriptor avoids looking for the wrong fix.

**Analyze local deformation**: Near a point, a regular projective transformation is linearized by a $2\times2$ matrix that can have two different singular values. A rotation and an isotropic scale compensate for only part of it; the ratio of the singular values measures a local anisotropy. Constructed example: a disc viewed more and more obliquely becomes an ellipse, even after its major axis is rotated back to the reference orientation. The described neighborhood therefore changes shape. Rectifying can help if the geometry is known, but estimating this rectification from the same difficult matches is not free. Occlusion additionally removes information that no coordinate transformation restores.

**Viewpoint normalization cannot recover occlusion**: Even a perfect local affine normalization cannot reconstruct the surface region hidden in one view. Separate anisotropic deformation of a visible patch from visibility loss and specular appearance changes when diagnosing viewpoint failures. A proposed controlled check uses a textured planar target over increasing tilt, records the common visible area, and evaluates correspondence only where the physical surface is jointly observable. Otherwise reduced overlap may be mistaken for descriptor failure.

**Blocking errors**: Claiming universal projective invariance, or inferring the descriptor's invariance from the geometric model's.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §6.1 and §6.3 sensitivity to affine change, Fig. 9](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf). Local linearization argument: project deduction.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-SIFT-005 provenance::agent pole::B pole::E
END

## CV-SIFT-006

Objective: Diagnose a misleading consensus. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-006
Question: A repetitive facade produces many SIFT matches and a high inlier ratio, but localization is displaced by one window. What diagnosis should be proposed, and how can it be checked?
Reponse: **Expected answer**: Repetition can produce consistent but semantically offset matches. Check match positions, coverage and points or clues independent of consensus; do not conclude from the number of inliers alone.

**Further explanation**: inspect ratios and residuals, test distinctive zones or position constraint, and then validate the transformation on unused observations. A threshold drop can remove random outliers without resolving a geometrically consistent ambiguity. This is a case of proposed reasoning, not a measured experiment.

**Why RANSAC is not enough here**: its residuals test the consistency with a model, not the sense of the recognized pattern. A period shift on a façade can produce a set of pairs that supports another transformation almost as well. Adding more observations of the same motif may reinforce this ambiguity.

**Constructed independent verification**: choose a sign, border or point whose absolute position is known, without using it for the initial adjustment. Compare candidate transformations on this observation, as well as on the useful area. A maximum displacement constraint can help if it is justified by the installation; it would be misleading if the actual motion exceeds this domain. A weak residual therefore does not replace the identifiability of the problem.

**Ambiguity with several solutions**: A periodic pattern admits candidate transformations $H_0,H_1,\ldots$ that shift the alignment by one period while keeping small residuals on the repeated windows. Information without this symmetry must be compared, or the problem must be reported as ambiguous. Then build an acceptance rule that includes an absolute reference or a justified motion prior. A few more inliers are not proof when all observations are repeated. Examining several hypotheses and their margins can be more informative than returning only the best model, provided this rule is evaluated on held-out ambiguous cases.

**A geometric consensus can support the wrong period**: Construct a reference containing four identical windows and one unique sign. A one-window translation can fit most window features while misplacing the sign. Reserve that sign as independent evidence when testing the fitted transformation. If no nonperiodic evidence is available, the honest output is an ambiguity set or rejection according to the product contract. Tightening RANSAC residual thresholds cannot by itself distinguish two exactly periodic explanations.

**Blocking errors**: Asserting that a majority consensus guarantees the right window, or prescribing more points without a discriminating test.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §7.1 and §7.3–§7.4](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [Rey-Otero and Delbracio 2014, IPOL §5, repeated structures](https://doi.org/10.5201/ipol.2014.82). Periodic-ambiguity test: project construction.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-SIFT-006 provenance::agent pole::B pole::E
END

## CV-SIFT-007

Objective: Build a comparison under constraint. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-007
Question: When choosing SIFT or ORB for industrial part registration, which measurements make the comparison useful to the product?
Reponse: **Expected answer**: use the same representative pairs and reference geometry; measure success of registration, errors, coverage and full cost on the target hardware. Tune on validation, then freeze the settings for the test.

**Further explanation**: Stratify by rotation, scale, blur and lighting; include extraction, matching and geometric validation in the latency and examine rare failures. The number of points or a time published on other hardware is not enough. The protocol is proposed; no winners or industrial results are announced here.

**Proposed product criteria**: Convert the registration error into a business quantity, such as the offset of an inspection region relative to the defect. Set a tolerance and count successes, refusals and dangerous errors. Two methods with similar mean residuals can differ greatly on oblique views or weakly textured parts.

**Complete measurement**: Record the resolution and the number of points, and include the same steps in the timing. A faster extractor that produces many ambiguous candidates can shift the cost toward matching and RANSAC. Also examine memory and the latency of difficult cases. The right decision depends on the tradeoff observed on the target hardware and on the consequences of a failure, not on a general preference for a classical or binary method.

**Break down the causes of failure**: Measure separately the detection repeatability, match precision, recall of useful matches and the rate of registrations accepted at the business tolerance. An inlier ratio can increase simply because almost all matches were removed; keep its denominator and the coverage. The exhaustive cost between $n$ and $m$ descriptors of dimension $d$ is of the order of $nmd$ scalar operations; changing the point budget therefore also changes the matching and RANSAC budgets. Comparing a quality–cost frontier over several settings is more instructive than comparing two default configurations, without announcing a winner before the measurements.

**Compare refusal as well as successful localization**: A pipeline that returns a pose on every image can have lower availability-adjusted quality than one that rejects unsupported cases. Define a success as both producing an estimate and meeting geometric tolerance, then separately report incorrect acceptances and justified refusals. Include feature extraction, matching, robust estimation and validation in timing. A faster descriptor can lose its advantage if its ambiguous matches repeatedly exhaust the geometry budget.

**Blocking errors**: Choosing on the number of matches alone, or comparing times that do not include the same stages.
Source: [[40-features-matching/references/41-sift|reference note SIFT]]; [Lowe 2004, §§6.2–6.4 and §7.2](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [Rublee et al. 2011, §§4.4, 5.3 and 6.1](https://doi.org/10.1109/ICCV.2011.6126544). Product protocol: project construction.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-SIFT-007 provenance::agent pole::B pole::E
END
