# Flashcards — Harris and Shi–Tomasi — local structure and trackable points

reference note: [[40-features-matching/references/46-harris-shi-tomasi|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-CORNERS-001

Objective: Interpreting local values. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-001
Question: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?
Reponse: **Expected answer**: The second: its smallest eigenvalue is 20 instead of 1. The two directions are constrained; the first one looks like an edge, even if its total gradient is stronger.

**Further explanation**: $E(d)\approx d^TMd$ approximates the intensity variation for a small $d$ displacement in pixels. The direction associated with the small eigenvalue is difficult to observe. It remains to check photometric stability and absence of occlusion.

**Interpretation of directions**: With the first matrix, a shift in the direction associated with the value 1 changes the patch little. The large 100 value does not compensate for this weak direction. With the second, a unit displacement in any proper direction produces the same local curvature of 20.

**Proposed use**: Before a Lucas – Kanade follow-up, examine the smallest binding term and the distribution of points. A set of well-conditioned corners but grouped in a small area does not guarantee a stable overall registration. The numbers assume the local model of small translations and the same gradient units; comparing matrices from different normalizations without aligning them would not have the same meaning.

**Diverting the local tensor**: for a small displacement $d$, $I(p+d)-I(p)\approx\nabla I(p)^Td$. The weighted sum of these squared deviations gives $d^T(\sum_p w_p\nabla I_p\nabla I_p^T)d$, so $M$. Constant error contours are ellipses: their large axis corresponds to the direction in which the image changes little. If the photometric noise model is isotropic and the problem is correctly posed, the local uncertainty of displacement is related to a matrix proportional to $M^{-1}$. A small eigenvalue then becomes a great directional uncertainty; it is a link with the followability, under assumptions, not a guarantee of future visibility.

**The error ellipse gives a quantitative comparison**: With equal unit photometric noise in the local linearized model, $M^{-1}$ for the first window is $\operatorname{diag}(0.01,1)$ and for the second is $\operatorname{diag}(0.05,0.05)$. The second window has a much smaller worst-direction variance despite lower total gradient energy. This constructed calculation explains choosing by the weakest direction. It assumes a shared local displacement and does not establish robustness to occlusion or an incorrect brightness model.

**Blocking errors**: Choose only the highest eigenvalue; confuse strong corner and certain match.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Harris and Stephens 1988, self-correlation and corner response](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [OpenCV 4.13, Harris, Theory, tensor and response](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html); [OpenCV 4.13, Shi – Tomasi, Theory and selection goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-CORNERS-001 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-002

Objective: distinguish Harris and Shi – Tomasi scores. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-002
Question: How do Harris and Shi–Tomasi differ in corner selection, and can the same numerical threshold be retained?
Reponse: **Expected answer**: Harris takes $\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$; Shi – Tomasi takes $\min(\lambda_1,\lambda_2)$. The eigenvalues come from the local matrix of the gradient products. Scores have different scales and units: recalibrate thresholds.

**Further explanation**: Shi – Tomasi directly tests the least informative direction. Harris penalizes a strong anisotropy via his parameter $k$. The choice depends on the pipeline; no formula imposes a better performance on any stage.

**derivation Scale**: if the intensities are multiplied by a constant $a$, the gradients are multiplied by $a$ and the eigenvalues of $M$ by $a^2$, with identical operators. The Shi – Tomasi score follows this factor, while the Harris score follows $a^4$. The same numerical threshold cannot represent the same selectivity in these two spaces.

**Proposed action**: set intensity range, scale of derivatives and window before setting the threshold. Then compare location, coverage and stability under relevant disturbances. A difference in coin count can come from normalizing scores rather than a superiority of the mechanism. Both criteria describe local information, not a probability of correct matching.

**Avoid confusing score and model**: Harris can calculate determinant and trace directly without diagonalizing $M$; Shi – Tomasi evaluates the smallest eigenvalue, $(\operatorname{tr}M-\sqrt{(M_{11}-M_{22})^2+4M_{12}^2})/2$ for a symmetric matrix $2\times2$. These are two summaries of the same tensor, not two new proofs of identity of the point. In the isotropic case $\lambda_1=\lambda_2=\lambda$, Harris gives $(1-4k)\lambda^2$ while Shi – Tomasi gives $\lambda$. Their evolution with the contrast and scale of the patch therefore differs even when the visual ranking of the best corners seems similar. Removing maxima and spacing remain separate steps of these formulas.

**Contrast scaling changes the response power**: If all intensities are multiplied by $\alpha$, gradients scale by $\alpha$ and tensor eigenvalues by $\alpha^2$. Shi–Tomasi then scales by $\alpha^2$, whereas Harris scales by $\alpha^4$. A fixed absolute threshold therefore changes its meaning with intensity units, and the two scores cannot share a numerical threshold. Relative-to-maximum selection can cancel a uniform scale, but clipping and spatially varying illumination do not preserve this ideal relation.

**Blocking errors**: Reuse the same threshold without normalization; announce a universal ranking.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [OpenCV 4.13, Shi – Tomasi, Theory and goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html); [OpenCV 4.13, Harris, Theory, tensor and response](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-CORNERS-002 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-003

Objective: Set a selection of corners. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-003
Question: In OpenCV 4.13 goodFeaturesToTrack, how do qualityLevel, minDistance and maxCorners differ?
Reponse: **Expected answer**: `qualityLevel` sets a threshold relative to the best score; `minDistance` imposes a minimum spacing in pixels; `maxCorners` limits the number returned. These settings serve three different constraints.

**Further explanation**: A low contrast image can retain points with a low relative threshold without making them followable. Also check their space cover and conditioning. The image and the derivation must comply with the detector contract.

**Example of an interpreted setting**: If the best score is 100 and the relative threshold is 0,1, the selection threshold is bound to 10 in this image. This reasoning does not give an absolute level of quality that is valid on all acquisitions. An almost uniform image can have a better low score, despite a relative threshold being respected.

**Separate effects**: Increasing the minimum distance distributes positions but can remove useful close details; increasing the quota does not create more satisfactory candidates. Set each stress with a spatial map of points and a downstream measurement. To compare acquisitions, also raise the absolute scores and the contrast. The selection meets a budget and coverage; the followability still requires a temporal verification.

**Read the selection as a suite of filters**: first calculate the quality map, retain the local maxima, eliminate insufficient scores, then consider the candidates in descending order respecting the minimum distance and budget. Therefore, the quota does not replace a quality threshold. In a built-in case, if the only good points are close, increasing the spacing can get a lot and leave less than the number requested; this is not necessarily a failure of the API. To limit concentration, a mask of interest or quotas by region are choices of system to compare, keeping the same notion of score and the same units of distance.

**A relative threshold can accept uniformly weak images**: If the best response in a blurred image is small, a fixed fraction of that response is also small. Thus qualityLevel does not provide an absolute guarantee of trackability. Record the best score and retained-score distribution as well as the returned count. minDistance may then exclude clustered candidates and maxCorners may truncate the survivors; increasing the cap cannot create strong points where the image lacks usable gradients.

**Blocking errors**: Read qualityLevel as a probability; convert minDistance to intensity.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [OpenCV 4.13, Shi – Tomasi, Theory and goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html); [OpenCV 4.13, Harris, Theory, tensor and response](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-CORNERS-003 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-004

Objective: distinguish detection and matching ambiguity. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-004
Question: Strong corners on a repetitive grid still produce a poor homography. Which checks distinguish detection failure from incorrect association?
Reponse: **Expected answer**: Check repeatability and location of corners, then ambiguity of descriptors, distribution of matches and geometric residuals. Strong corners can resemble each other and produce false associations.

**Further explanation**: A check built consists of keeping the detector and changing the filtering of matches, and then reversing the experience. The local score does not verify the identity of the point or model of homography. A high spatial concentration can also constrain the estimation.

**Why scores don't separate the boxes**: Each intersection of a grid can have two well marked gradient directions. The corner criterion confirms the location of each intersection, but does not know which intersection of the second image represents the same point in the world.

**Constructed test**: Keep the detected positions and visualize the candidates of each descriptor. Compare period offset assumptions with held-out distinctive landmarks. Then check that the inlays cover the surface at register and not a single strip. If the locations remain stable but the associations change boxes, act on the distinctive clues or constraints of the problem. Better local selection can reduce noise; it does not solve appearance symmetry on its own.

**Distinguish between local and global observation**: $M$ describes the curvature of a small translation cost around a given patch. It does not compare this patch to all other patches in an image. A grid can therefore give a strong curvature around each intersection, while producing several remote minima for matching between images. A known initial move can make local tracking possible without resolving the overall recognition of the correct box. To evaluate the detector alone, use a reference transformation and check the distance to the projected position; to match it, then examine which identity is selected among the candidates. Both rates do not have the same denominator.

**Repeatability and identity need separate denominators**: Given a known image transformation, first count whether a detected point has a nearby detected counterpart in the visible transformed region. Then, among described points, measure whether matching chooses that counterpart rather than a repeated intersection. This proposed decomposition separates missed detections from wrong identities. Exclude points truly outside shared visibility from repeatability denominators, and report exclusions so a method cannot appear robust simply by discarding difficult regions.

**Blocking errors**: Increase only the number of corners; assimilate Harris score and match confidence.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [Harris and Stephens 1988, self-correlation and corner response](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [OpenCV 4.13, Harris, Theory, tensor and response](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html); [OpenCV 4.13, Shi – Tomasi, Theory and selection goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-CORNERS-004 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-005

Objective: Evaluate a selection for tracking. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CORNERS-005
Question: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?
Reponse: **Expected answer**: Measure survival, displacement error, spatial coverage and geometry error with comparable budget and resolution. A setting that produces more dots can add noise or redundant dots.

**Further explanation**: Proposed variation: impose quotas per cell with the same total number of points. Separate adjustment and evaluation sequences; note blur and occlusions. This protocol is a project proposal, not a published result.

**Example of comparison**: One hundred corners on a single texture can be redundant and leave the piece useful without observations. Fifty distributed points can best constrain the requested movement, but only if their movements are reliable. The number does not describe this coverage or how long the dots remain visible.

**Protocol built**: Set resolution, total budget and tracking criteria, then vary selection score and space quotas separately. Measure errors on annotated point trajectories or on independent geometry, also counting points lost. A low photometric residual can remain misleading in case of repetition. Report performance on blur, low texture and occlusion, with the same rejection rules for all settings.

**check round trip built**: Following $p_t$ to $\hat p_{t+1}$, then following the latter to $\hat p_t$ gives a $e_{FB}=\|\hat p_t-p_t\|_2$ cycle error in pixels. A big error signals a useful inconsistency to reject; a small error can also come from the same bad pattern found in both directions. It must therefore complete a displacement reference, not replace it. Compare the fraction of valid points by keeping the occlusions in the balance sheet. If a setting rejects almost all the hard points, its average error on survivors can drop while degrading the availability of the registration. Reliable monitoring and refusal policy must be evaluated together.

**Survivor-only error can reward excessive rejection**: Constructed comparison: method A retains 90 of 100 points with 1 px mean error; method B retains 10 with 0.5 px mean error. B has better conditional error but may fail to support the required geometry. Report survival and spatial coverage jointly with error, and count whether a valid transform is available. Forward/backward consistency is useful evidence, but repeated texture can generate a consistent wrong cycle in both directions.

**Blocking errors**: Conclude on the single point counter; change several factors without recording them.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Full reference]]; [OpenCV 4.13, Shi – Tomasi, Theory and goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html); [OpenCV 4.13, Harris, Theory, tensor and response](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-CORNERS-005 provenance::agent pole::B pole::C pole::E
END
