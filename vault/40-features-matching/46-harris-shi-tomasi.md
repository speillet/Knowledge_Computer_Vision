# Flashcards — Harris and Shi–Tomasi — local structure and trackable points

reference note: [[40-features-matching/references/46-harris-shi-tomasi|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-CORNERS-001

Objective: Interpret local eigenvalues. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-001
Question: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?
Reponse: **Expected answer**: The second: its smallest eigenvalue is 20 instead of 1. Both directions are constrained; the first one behaves like an edge, even though its total gradient is stronger.

**Further explanation**: $E(d)\approx d^TMd$ approximates the intensity change for a small displacement $d$ in pixels. The direction associated with the small eigenvalue is difficult to observe. Photometric stability and the absence of occlusion still need checking.

**Interpretation of directions**: With the first matrix, a shift in the direction associated with the value 1 changes the patch little. The large value 100 does not compensate for this weak direction. With the second, a unit displacement in any direction produces the same quadratic change, 20.

**Proposed use**: Before Lucas–Kanade tracking, examine the smallest eigenvalue, which is the weakest constraint, and the spatial distribution of the points. A set of well-conditioned corners grouped in a small area does not guarantee a stable global registration. The numbers assume the local model of small translations and the same gradient units; matrices computed with different normalizations cannot be compared without aligning them.

**Deriving the local tensor**: for a small displacement $d$, $I(p+d)-I(p)\approx\nabla I(p)^Td$. The weighted sum of these squared differences gives $d^T(\sum_p w_p\nabla I_p\nabla I_p^T)d$, hence $M$. Contours of constant error are ellipses whose major axis lies along the direction in which the image changes little. If the photometric noise is independent with equal variance and the problem is well posed, the local displacement uncertainty is proportional to $M^{-1}$. A small eigenvalue then means a large uncertainty in that direction; this links the eigenvalues to trackability under these assumptions, not to future visibility.

**The error ellipse gives a quantitative comparison**: With equal unit photometric noise in the local linearized model, $M^{-1}$ for the first window is $\operatorname{diag}(0.01,1)$ and for the second is $\operatorname{diag}(0.05,0.05)$. The second window has a much smaller worst-direction variance despite lower total gradient energy. This constructed calculation explains choosing by the weakest direction. It assumes a shared local displacement and does not establish robustness to occlusion or an incorrect brightness model.

**Blocking errors**: Choosing by the largest eigenvalue only; confusing a strong corner with a certain match.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Harris and Stephens 1988, auto-correlation detector, pp. 149–150](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [Shi and Tomasi, TR 93-1399, ch. 3 eq. 3.10 and ch. 4 eq. 4.1](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf). Error-ellipse calculation: project derivation, recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-CORNERS-001 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-002

Objective: distinguish Harris and Shi – Tomasi scores. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-002
Question: How do Harris and Shi–Tomasi differ in corner selection, and can the same numerical threshold be retained?
Reponse: **Expected answer**: Harris takes $\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$; Shi – Tomasi takes $\min(\lambda_1,\lambda_2)$. The eigenvalues come from the local matrix of the gradient products. Scores have different scales and units: recalibrate thresholds.

**Further explanation**: Shi–Tomasi directly tests the least informative direction. Harris penalizes strong anisotropy through its parameter $k$. The choice depends on the pipeline; neither formula guarantees better performance at every stage.

**Scale derivation**: if the intensities are multiplied by a constant $a$, the gradients are multiplied by $a$ and the eigenvalues of $M$ by $a^2$, with identical operators. The Shi–Tomasi score follows this factor, while the Harris score follows $a^4$. The same numerical threshold cannot represent the same selectivity on these two scales.

**Proposed action**: fix the intensity range, the derivative scale and the window before setting the threshold. Then compare localization, coverage and stability under relevant perturbations. A difference in corner count can come from score normalization rather than from a better mechanism. Both criteria describe local information, not a probability of correct matching.

**Do not confuse score and model**: Harris can compute the determinant and trace directly without diagonalizing $M$; Shi–Tomasi evaluates the smallest eigenvalue, $(\operatorname{tr}M-\sqrt{(M_{11}-M_{22})^2+4M_{12}^2})/2$ for a symmetric $2\times2$ matrix. These are two summaries of the same tensor; neither is evidence of the point's identity. In the isotropic case $\lambda_1=\lambda_2=\lambda$, Harris gives $(1-4k)\lambda^2$ while Shi–Tomasi gives $\lambda$. Their behavior under changes of contrast and patch scale therefore differs even when the visual ranking of the best corners looks similar. Non-maximum suppression and spacing are separate steps, outside these formulas.

**Contrast scaling changes the response power**: If all intensities are multiplied by $\alpha$, gradients scale by $\alpha$ and tensor eigenvalues by $\alpha^2$. Shi–Tomasi then scales by $\alpha^2$, whereas Harris scales by $\alpha^4$. A fixed absolute threshold therefore changes its meaning with intensity units, and the two scores cannot share a numerical threshold. Relative-to-maximum selection can cancel a uniform scale, but clipping and spatially varying illumination do not preserve this ideal relation.

**Blocking errors**: Reusing the same threshold without normalization; claiming a universal ranking.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Harris and Stephens 1988, contrast factor and corner response, p. 150](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [Shi and Tomasi, TR 93-1399, ch. 4 eq. 4.1](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf); [OpenCV 4.13.0 corner.cpp, score formulas L52–L155](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/corner.cpp#L52-L155). Scaling argument: project deduction.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-CORNERS-002 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-003

Objective: Tune a corner selection. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-003
Question: In OpenCV 4.13 goodFeaturesToTrack, how do qualityLevel, minDistance and maxCorners differ?
Reponse: **Expected answer**: `qualityLevel` sets a threshold relative to the best score; `minDistance` imposes a minimum spacing in pixels; `maxCorners` limits the number returned. These settings serve three different constraints.

**Further explanation**: In a low-contrast image, a low relative threshold can keep points that are not trackable. Also check their spatial coverage and conditioning. The image and the derivative operator must match the detector's contract.

**Example of an interpreted setting**: If the best score is 100 and the relative threshold is 0.1, the selection threshold is 10 in this image; OpenCV keeps only scores strictly above it. This reasoning gives no absolute quality level valid across acquisitions: in an almost uniform image even the best score is low, and the relative threshold still accepts points.

**Separate effects**: Increasing the minimum distance spreads positions but can remove useful nearby details; increasing the quota does not create more acceptable candidates. Set each constraint with a spatial map of the points and a downstream measurement. To compare acquisitions, also record the absolute scores and the contrast. The selection meets a budget and a coverage target; trackability still requires a temporal check.

**Implementation conditions (OpenCV 4.13.0 sources)**: the maximum used by `qualityLevel` is computed inside the mask, so masking a high-contrast object changes the threshold everywhere else. With `useHarrisDetector=true`, the same `qualityLevel` applies to a response that scales with the fourth power of contrast instead of the square, so it rejects low-contrast regions much sooner. `maxCorners=0` means no limit; the header also describes negative values as unlimited, but the code asserts `maxCorners >= 0`. Returned positions are integer pixels until `cornerSubPix` refines them.

**Read the selection as a sequence of filters**: first compute the quality map, keep the local maxima, remove insufficient scores, then visit the candidates in descending order while enforcing the minimum distance and the budget. The quota therefore does not replace a quality threshold. In a constructed case where the only good points are close together, increasing the spacing can reject many of them and return fewer points than requested; this is not an API failure. To limit concentration, a region-of-interest mask or per-region quotas are system choices to compare, keeping the same score definition and the same distance units.

**Blocking errors**: Reading qualityLevel as a probability; expressing minDistance in intensity units.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [OpenCV 4.13.0 imgproc.hpp, goodFeaturesToTrack L2083–L2135](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L2083-L2135); [OpenCV 4.13.0 featureselect.cpp, L382–L547](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/featureselect.cpp#L382-L547).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-CORNERS-003 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-004

Objective: distinguish detection and matching ambiguity. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-004
Question: Strong corners on a repetitive grid still produce a poor homography. Which checks distinguish detection failure from incorrect association?
Reponse: **Expected answer**: Check repeatability and location of corners, then ambiguity of descriptors, distribution of matches and geometric residuals. Strong corners can resemble each other and produce false associations.

**Further explanation**: A constructed check keeps the detector fixed and changes the match filtering, then does the reverse. The local score verifies neither the identity of the point nor the homography model. A high spatial concentration can also leave the estimation poorly constrained.

**Why scores do not separate grid cells**: Each intersection of a grid can have two well-marked gradient directions. The corner criterion confirms the location of each intersection, but does not know which intersection in the second image is the same point in the world.

**Constructed test**: Keep the detected positions and visualize the candidates of each descriptor. Compare hypotheses shifted by one period against held-out distinctive landmarks. Then check that the inliers cover the surface to be registered, not a single strip. If the locations remain stable but the associations jump between grid cells, act on distinctive cues or on the problem's constraints. Better local selection can reduce noise; it does not resolve appearance symmetry on its own.

**Distinguish local from global observation**: $M$ describes the curvature of a small-translation cost around a given patch. It does not compare this patch with all other patches in an image. A grid can therefore give a strong curvature around each intersection while producing several distant minima for matching between images. A known initial displacement can make local tracking possible without solving the global identification of the correct grid cell. To evaluate the detector alone, use a reference transformation and check the distance to the projected position; for matching, then examine which identity is selected among the candidates. The two rates do not share a denominator.

**Repeatability and identity need separate denominators**: Given a known image transformation, first count whether a detected point has a nearby detected counterpart in the visible transformed region. Then, among described points, measure whether matching chooses that counterpart rather than a repeated intersection. This proposed decomposition separates missed detections from wrong identities. Exclude points truly outside shared visibility from repeatability denominators, and report exclusions so a method cannot appear robust simply by discarding difficult regions.

**Blocking errors**: Only increasing the number of corners; equating the Harris score with match confidence.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Harris and Stephens 1988, auto-correlation detector, p. 149](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [Schmid, Mohr and Bauckhage 2000, §3.1 repeatability rate](https://inria.hal.science/inria-00548302v1). Grid diagnosis and separate denominators: project construction.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-CORNERS-004 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-005

Objective: Evaluate a selection for tracking. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-005
Question: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?
Reponse: **Expected answer**: Measure survival, displacement error, spatial coverage and geometry error with comparable budget and resolution. A setting that produces more points can add noisy or redundant points.

**Further explanation**: Proposed variation: impose quotas per cell with the same total number of points. Separate tuning and evaluation sequences; record blur and occlusions. This protocol is a project proposal, not a published result.

**Example of comparison**: One hundred corners on a single textured patch can be redundant and leave the useful part of the object without observations. Fifty well-distributed points can better constrain the motion to be estimated, but only if they are tracked reliably. The count describes neither this coverage nor how long the points remain visible.

**Constructed protocol**: Set the resolution, total budget and tracking criteria, then vary the selection score and the spatial quotas separately. Measure errors on annotated point trajectories or on independent geometry, also counting lost points. A low photometric residual can be misleading on repeated patterns. Report performance under blur, low texture and occlusion, with the same rejection rules for all settings.

**Constructed forward–backward check**: Tracking $p_t$ to $\hat p_{t+1}$, then tracking the latter back to $\hat p_t$, gives a cycle error $e_{FB}=\|\hat p_t-p_t\|_2$ in pixels. A large error signals a useful inconsistency to reject; a small error can also come from the same wrong pattern found in both directions. It therefore complements a displacement reference rather than replacing it. Compare the fraction of valid points while keeping occlusions in the tally. If a setting rejects almost all difficult points, its mean error on survivors can drop while the registration becomes less available. Tracking reliability and the rejection policy must be evaluated together.

**Survivor-only error can reward excessive rejection**: Constructed comparison: method A retains 90 of 100 points with 1 px mean error; method B retains 10 with 0.5 px mean error. B has better conditional error but may fail to support the required geometry. Report survival and spatial coverage jointly with error, and count whether a valid transform is available. Forward/backward consistency is useful evidence, but repeated texture can generate a consistent wrong cycle in both directions.

**Blocking errors**: Concluding from the point count alone; changing several factors without recording them.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Shi and Tomasi, TR 93-1399, ch. 5 dissimilarity and ch. 7 non-overlapping windows](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf); [Schmid, Mohr and Bauckhage 2000, §3.1](https://inria.hal.science/inria-00548302v1). Protocol and comparison: project construction.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-CORNERS-005 provenance::agent pole::B pole::C pole::E
END
