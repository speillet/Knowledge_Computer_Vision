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

**Further explanation**: Detection decides where to describe; the description represents the neighborhood. We can use distance L2, ratio test then RANSAC/homography, with inspection of the residuals and spatial coverage. The choice of a homography depends on the scene, not on the use of SIFT.

**Constructed decision chain**: For a known flat label, keep the keypoint coordinates in each image, calculate the candidates and inspect their distribution before estimating the warp. Four misplaced matches or several ambiguous pairs do not become reliable because they come from SIFT. A concentrated consensus in one corner may also misconstraint extrapolation to the other edge.

**Interpretation of the result**: check a geometry on points not used for its adjustment and in the area where the product must act. A piece in relief may require a different model than a single homography. The responsibility of SIFT is local representation; that of the pipeline is to establish that a transformation sufficiently explains the observations for the announced use.

**Linking Outputs to an Estimate**: represent the points by two tables $P_A\in\mathbb R^{n\times2}$ and $P_B\in\mathbb R^{m\times2}$, and their descriptors by two tables with 128 columns. The matcher returns $(i,j)$ indices, not directly the coordinates of a transformation. A robust estimate then uses the $(P_A[i],P_B[j])$ pairs in the same pixel contract as its threshold. If the extraction was done on a resized image, the estimated matrix connects these resized images; composing it with the preprocessing transformations is necessary to return to the initial images. Maintaining these associations of indices avoids confusing the quality of the descriptor and the error of manipulation of the coordinates.

**Blocking errors**: say that the descriptor directly estimates the pose or that each nearest neighbor is a true match.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe 2004, §§3 – 7](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-SIFT-001 provenance::agent pole::B pole::E
END

## CV-SIFT-002

Objective: Explain the search for a characteristic scale. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-002
Question: In SIFT, what does the difference of Gaussians compare, and why are extrema also sought across scale?
Reponse: **Expected answer**: $D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma)$ compares two neighboring smoothings, with $L=G_\sigma*I$. Looking for a spatial and scale extremum aims to find a structure at its characteristic scale, rather than at an arbitrarily fixed radius.

**Further explanation**: $\sigma$ is a pixel scale, $k>1$ is the ratio between levels, and $G_\sigma$ is a normalized Gaussian kernel. The DoG approximates a Laplacian normalized in scale. The candidate is compared to 26 neighbors: eight in his level and nine in each of the adjacent levels. Sampling, noise and loss of detail limit repeatability.

**Why the scale intervenes**: The same detail covers more pixels as the camera gets closer. Looking only for maxima in a smoothed fixed-radius image then imposes a different neighborhood in both views. The search in the levels is aimed at a characteristic size of the structure, which is then used to calculate the descriptor.

**Example interpreted**: A small spot and the same enlarged spot can be selected at different levels. If the reduced image no longer contains enough samples to represent it, no level recreates the spot. The mechanism therefore helps to find a structure that is still observable; it does not remove the role of optics or pre-filtering before reduction.

**Why DoG is Approaching a Laplacian**: for $k$ close to 1, a scale development gives $L(k\sigma)-L(\sigma)\approx(k-1)\sigma\,\partial L/\partial\sigma$. The Gaussian diffusion equation links this derivative to $\sigma\nabla^2L$: the difference is therefore proportional to a Laplacian normalized by $\sigma^2$. This approximation implies a suitable spacing of scales, not an exact identity for any $k$. Detecting an extremum is just the beginning: local refinement estimates position and scale between samples, then low-contrast and edge-dominated rejections avoid describing unstable points. The same number of candidates does not mean the same number of reliable keypoints.

**Blocking errors**: confuse scale and orientation, or announce perfect invariance for any change in resolution.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, §3](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
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

**Example of limit**: A saturated zone can make several intensities identical and remove an edge. Normalization of the vector cannot restore this absent gradient. To diagnose a match drop, distinguish then undetected keypoint, unstable orientation and undistinctive descriptor. The 128 dimension explains the chosen structure, but does not constitute a measure of match quality or a guarantee of identification.

**Understanding normalization**: For a non-zero $d$ histogram, division by $\|d\|_2$ cancels out a common multiplicative gain; subtracting a constant from all intensities does not already change their differences in the ideal model. On the other hand, if a few gradients dominate, they can crush the contribution of other cells. A clipping followed by a new normalization limits this domination. Constructed example: two patches with a single edge becoming much stronger can keep a similar directional layout while changing the raw norm. Interpolation between cells and orientation bins also prevents a small geometric variation from abruptly shifting the entire contribution on one side of a discrete boundary.

**Blocking errors**: Describe 128 raw pixels, or claim that normalization guarantees invariance to any lighting.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, §§5 – 6](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-SIFT-003 provenance::agent pole::B pole::E
END

## CV-SIFT-004

Objective: interpret the ratio test. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-004
Question: Two query descriptors have L2 distances $(20,21)$ and $(35,80)$ to their two nearest neighbors. With a ratio-test threshold of 0.8, which query is retained, and what does this test establish?
Reponse: **Expected answer**: reject the first ($20/21\approx0,952$), keep the second ($35/80=0,4375$). The test looks for a neighbor that is significantly more distinctive than its competitor; a small absolute distance is not enough.

**Further explanation**: we check $d_1<0,8d_2$ with $d_1\le d_2$. The choice of the threshold is a matter of validation. Even accepted, the match can be wrong in a repetitive structure: a geometric check remains necessary. Explicitly deal with the absence of two neighbors and the distances both zero.

**Reading the test**: The first candidate is close in absolute value but its competitor is almost as close: the query mischaracterizes the two. The second candidate is further away, but clearly separated from his competitor. The ratio compares this relative ambiguity and does not provide a probability of correct matching.

**Case built for adjustment**: On a repetitive texture, hardening the threshold can remove a large fraction of the dots and leave too little coverage for homography. On a distinctive image, an overly permissive threshold can increase false candidates. So choose the setting on geometric success and projection errors, keeping an exact reference of the two neighbors when the search is approached.

**Beware of squared distances**: If a routine provides $s_1=d_1^2$ and $s_2=d_2^2$, the criterion equivalent to $d_1<\tau d_2$ is $s_1<\tau^2s_2$, not $s_1<\tau s_2$. With $\tau=0,8$, directly comparing squares to 0,8 would be tolerating a distance ratio close to 0,894. This transformation is algebraically inferred for positive distances; it does not say which convention uses a particular API. Read the contract of the function and test a small known couple before reusing a threshold. The "second" neighbor must also come from the same set of candidates provided by the protocol; changing the base changes the measured ambiguity.

**Blocking errors**: Automatically keep the 20 distance match, reverse the ratio, or interpret acceptance as a physical truth.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, §7.1](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-SIFT-004 provenance::agent pole::B pole::E
END

## CV-SIFT-005

Objective: Distinguish between the limits of invariances. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-005
Question: A planar object is first rotated within the image, then viewed from a very oblique angle. Why do these changes pose different challenges for SIFT?
Reponse: **Expected answer**: SIFT explicitly normalizes local orientation and scale. A strong oblique view distorts the patch in an affine/projective way and can change its visibility; it is not usually compensated by a simple rotation and a scale.

**Further explanation**: the invariances sought remain limited by detection and sampling. The existence of a homography between image planes does not mean that the descriptor is invariant to this homography. Evaluate the actual angular range and compare a suitable strategy if the match rate becomes insufficient.

**Geometric decomposition**: A rotation in the plane preserves the local shape to within one rotation. An oblique view compresses the directions of the patch differently and may cause certain surfaces to appear or disappear. Gradients are no longer only expressed in a different orientation; their arrangement may change.

**Proposed test**: Take a flat label, fix lighting and sharpness, then separate rotation in the plane and tilt of the camera. Measure re-detection and accuracy of matches for each variation, instead of a single overall rate. A homography can describe the projection of the plan while being difficult to estimate for lack of reliable matches. Distinguishing the validity of the scene model and the robustness of the descriptor avoids looking for the wrong fix.

**Analyze local deformation**: In the vicinity of a point, a regular projective transformation is linearized by a matrix $2\times2$ which can have two different singular values. A rotation and an isotropic scale only compensate for a part of it; the ratio of the singular values measures a local anisotropy. Example built: a disc observed more and more obliquely becomes an ellipse, even after returning its main axis to the right orientation. The described neighborhood therefore changes shape. Rectifying can help if the geometry is known, but estimating this rectification from the same difficult matches is not a free solution. The occlusion additionally removes information that no coordinate transformation restores.

**Blocking errors**: announce a universal projective invariance or deduce that of the descriptor from that of the geometric model.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, summary and §§5 – 6](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-SIFT-005 provenance::agent pole::B pole::E
END

## CV-SIFT-006

Objective: Diagnose a misleading consensus. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-006
Question: A repetitive facade produces many SIFT matches and a high inlier ratio, but localization is displaced by one window. What diagnosis should be proposed, and how can it be checked?
Reponse: **Expected answer**: Repetition can produce consistent but semantically offset matches. Check match positions, coverage and points or clues independent of consensus; do not conclude from the number of players alone.

**Further explanation**: inspect ratios and residuals, test distinctive zones or position constraint, and then validate the transformation on unused observations. A threshold drop can remove random outliers without resolving a geometrically consistent ambiguity. This is a case of proposed reasoning, not a measured experiment.

**Why RANSAC is not enough here**: its residuals test the consistency with a model, not the sense of the recognized pattern. A period shift on a façade can produce a set of pairs that supports another transformation almost as well. Adding more observations of the same motive may reinforce this ambiguity.

**Independent verification built**: choose a sign, border or point whose absolute position is known, without using it for the initial adjustment. Compare candidate transformations on this observation, as well as on the useful area. A maximum displacement constraint can help if it is justified by the installation; it would be misleading if the actual motion exceeds this domain. A weak residual therefore does not replace the identifiability of the problem.

**Ambiguity to several solutions**: A periodic pattern allows $H_0,H_1,\ldots$ candidate transformations that shift the alignment of a period while retaining small residuals on repeated windows. We must compare information that does not have this symmetry, or announce that the problem remains ambiguous. Then construct an acceptance rule including an absolute reference or a justified motion marker. A better score of a few inliers is not proof when all the observations are repeated. Examine several assumptions and their margin may be more informative than returning only the best model, provided you evaluate this rule on ambiguous reserved cases.

**Blocking errors**: affirm that a majority consensus guarantees the right window or prescribe more points without discriminating test.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, §7](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-SIFT-006 provenance::agent pole::B pole::E
END

## CV-SIFT-007

Objective: Build a comparison under constraint. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SIFT-007
Question: When choosing SIFT or ORB for industrial part registration, which measurements make the comparison useful to the product?
Reponse: **Expected answer**: use the same representative pairs and reference geometry; measure success of registration, errors, coverage and full cost on the target hardware. Set to validation and then freeze for the test.

**Further explanation**: Laminate by rotation, scale, blur and light; include extraction, matching and geometric validation in latency and examine rare failures. The number of points or the time published on another material is not enough. The protocol is proposed; no winners or industrial results are announced here.

**Proposed product criteria**: Convert the registration error to business-related, such as an inspection region offset from the fault. Set a tolerance and count successes, refusals and dangerous mistakes. Two methods at residuals mean neighbors can differ greatly on oblique views or sparsely textured pieces.

**Complete measurement**: record resolution, number of points and same steps included in the timing. A faster extractor that produces a lot of ambiguous candidates can shift the cost towards matching and RANSAC. Also examine memory and latency of difficult cases. The right decision depends on the compromise observed on the target hardware and the consequences of a failure, not a general preference for a conventional or binary method.

**Break down the causes of failure**: separately measure repeatability of detection, match accuracy, recall of useful matches and registration rate accepted to business tolerance. A ratio of players can increase simply because almost all matches have been withdrawn; you have to keep its denominator and coverage. The exhaustive cost between $n$ and $m$ descriptors of dimension $d$ is of the order of $nmd$ scalar operations; varying the quota of points therefore also changes the matcher and the budget RANSAC. Comparing a quality-cost boundary for multiple settings is more instructive than confronting two default parameters, without announcing a winner before the measurements.

**Blocking errors**: choose only the number of matches or compare times that do not include the same stages.
Source: [[40-features-matching/references/41-sift|reference note SIFT]] ; [Lowe, §§6.2 – 6.4 and 8](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) ; [Rublee et al., §§4.4, 5.3 and 6.1](https://doi.org/10.1109/ICCV.2011.6126544).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-SIFT-007 provenance::agent pole::B pole::E
END
