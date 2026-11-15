# Flashcards — Local detectors, descriptors and matchers

reference note: [[40-features-matching/references/43-detecteurs-matchers|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-MATCHING-001

Objective: interpret the structure matrix. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-001
Question: In a gradient-based model, why does a corner constrain 2D displacement better than an isolated edge?
Reponse: **Expected answer**: Two directions of variation constrain the movement; on an edge, the tangent displacement is hardly observable.

**Further explanation**: Inspect the eigenvalues of the local matrix, not just the number of points detected.

**Local model**: for a small displacement $d$, the photometric variation is close to a quadratic form $d^TMd$. The matrix $M$ gathers the products of the gradients in the neighborhood. Its eigenvectors indicate the directions of displacement that change the appearance much or little.

**Constructed example**: On a uniform vertical edge, moving the patch horizontally changes its contents; moving it along the edge can leave it almost unchanged. A visible corner shows changes in two directions, which helps localize a displacement. This does not imply that it is unique in the image: the corners of a grid can all look the same. Distinguish local localization information from association ambiguity between images. A poorly lit, occluded or too large window can also invalidate the small-displacement photometric model despite favorable eigenvalues.

**Link to the aperture problem**: Linearized brightness constancy gives $I_xu+I_yv+I_t=0$, one equation for two displacement components. On an edge, the neighboring gradients are almost parallel, so stacking their equations does not add a second independent direction. A corner brings different gradient orientations and can make the local system invertible. This reasoning assumes a motion shared by the whole patch and small changes between images. A window straddling two objects can have a well-conditioned tensor but violate the single-motion assumption. The corner score should be read with this model, not as a universal utility score for all estimators.

**Local uncertainty follows the weakest direction**: Under an ideal independent equal-variance photometric model, the displacement covariance is approximately $\sigma_I^2M^{-1}$. If $M=\operatorname{diag}(100,1)$, uncertainty along the second direction is one hundred times the first in variance, or ten times in standard deviation. This is a local linearized result, not a guarantee of correct correspondence. A repeated corner can constrain small motion precisely while still matching a distant copy incorrectly.

**Blocking errors**: Confusing one strong gradient with two independent constraints.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [Harris and Stephens 1988, auto-correlation detector, p. 149](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf); [Shi and Tomasi, TR 93-1399, ch. 4 aperture problem and eq. 4.1](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf). Covariance calculation: project derivation.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-MATCHING-001 provenance::agent pole::B pole::E
END

## CV-MATCHING-002

Objective: separate detector and descriptor. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-002
Question: Why are FAST and BRIEF not alternatives that perform exactly the same role?
Reponse: **Expected answer**: FAST locates points; BRIEF describes a patch in binary tests.

**Further explanation**: A pipeline can combine them, with orientation and scale depending on the method; then a matcher remains necessary.

**Breakdown of inputs and outputs**: FAST takes an image and returns candidate positions in its frame from local comparisons. BRIEF takes neighborhoods around selected positions and produces binary test strings. A matcher then compares these strings, and then a geometric step examines whether the pairs explain a plausible transformation.

**Constructed diagnosis example**: If no position is detected on a blurred part, changing the matcher's distance cannot create the missing keypoints. If the points are stable but the descriptors degrade when the part rotates, the defect may be in the description or its frame. Describing each step by its contract avoids replacing a component that does not address the observed cause. A complete pipeline like ORB adds pyramid and orientation choices; it does not make FAST and BRIEF synonymous.

**Expected equivariance and invariance**: If an image is geometrically transformed by $T$, a repeatable detector should find the transformed positions $T(p)$; it should therefore not produce the same numerical coordinates. Conversely, the descriptor aims at a comparable representation of the corresponding neighborhoods after the planned normalizations. Confusing these two properties misreads a rotation test: the coordinates should change, while the description should stay close enough. Too much invariance can also remove distinctive information and make several patches similar. The aim is not to make all descriptors identical under any transformation, but to keep discrimination over the useful range of variations.

**Descriptor support can invalidate a detected point**: A detector can return a valid point close to an image boundary, yet a descriptor may lack enough neighborhood support there. Rotation or scale normalization can move required sample positions outside the image as well. Record which points survive description and how coordinates and orientations are retained. Comparing only detector counts can otherwise attribute descriptor-border exclusions to matching, even though no usable descriptor was ever produced.

**Blocking errors**: Attributing geometrically verified matches to a detector alone.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [Rosten and Drummond 2006, §2.1 segment test](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [Calonder et al. 2010, §3 binary tests](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf); [OpenCV 4.13.0 brief.cpp, border removal](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/xfeatures2d/src/brief.cpp#L270-L289). Diagnosis cases: project constructions.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-MATCHING-002 provenance::agent pole::B pole::E
END

## CV-MATCHING-003

Objective: Measure an approximate search. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-003
Question: What should be checked if FLANN accelerates matching but degrades registration?
Reponse: **Expected answer**: Index and distance compatibility, neighbor recall, match filter and final geometric success.

**Further explanation**: Compare build time and queries, memory, and total cost; faster search can change the neighbor ratio.

**Why the approximation matters**: A fast index explores fewer candidates than an exhaustive search. It may miss the best neighbor or the competitor used to estimate ambiguity. A seemingly better ratio can thus result from a second neighbor that is too far away, and not from a more reliable match.

**Proposed ablation**: keep the descriptors and images, recompute the two neighbors by exact search on a sample, and then compare the pairs before and after filtering. Finally examine the inliers and the error on the useful region. Change the search budget without changing the detector simultaneously. Include index construction and possible reconstructions in total time. A setback in geometric success may come from approximation, poor metrics, or ambiguous data; the controlled comparison serves to separate them rather than declaring FLANN incorrect in general.

**Measuring the cascade effect**: on the same queries, record successively the identity of the two neighbors, the ratio-filter decision, the inlier status and the geometric error on held-out points. This trace locates where a search difference becomes a product error. If the index finds the exact neighbors but the registration changes, consider the order of matches, tie-breaking and the randomness of the robust estimate. If the neighbors differ, increasing only the search budget, or recomputing exact distances on additional candidates, is a more targeted ablation. An identical mean recall can still hide the loss of rare distinctive points that are decisive for breaking a symmetry.

**Approximation can change the robust solver budget**: If approximate search reduces the true inlier fraction, robust geometric estimation may need many more samples even when each match query becomes faster. Measure neighbor errors, accepted matches and geometric solver effort on the same image pairs. This proposed decomposition identifies whether the cost was saved in search and spent again in geometry, rather than assuming that a lower matching latency implies a faster reliable registration pipeline.

**Blocking errors**: Evaluating only the query time or the number of matches.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [Lowe 2004, §7.1–§7.2 ratio test and approximate search](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf); [OpenCV 4.13.0 features2d.hpp, FlannBasedMatcher](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp#L1290-L1306). Cascade protocol and effect on the ratio: project reasoning.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCHING-003 provenance::agent pole::B pole::E
END

## CV-MATCHING-004

Objective: choose a geometric check. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-004
Question: Two repeated logos produce similar descriptors. Which component can test a physical model of the correspondences?
Reponse: **Expected answer**: A geometric check adapted to the scene, with residuals, thresholds and coverage; the matcher alone does not guarantee it.

**Further explanation**: A symmetry can remain consistent; look for a distinctive observation or independent constraint.

**What the geometry tests**: A homography for a plane, or an appropriate multiview constraint, links candidate positions in the images. The residual expresses their disagreement with this model in a defined unit. A matcher chooses neighbors in an appearance representation; these two problems are different.

**Constructed limitation**: Two identical logos on the same support can produce a coherent group of matches and a consistent transformation that aligns the wrong logo. A geometric model does not necessarily resolve a symmetry of the scene. Look for a unique mark, an expected position or an additional observation that distinguishes the hypotheses. Also check the spatial support of the points and held-out observations. This step provides reasons for accepting a transformation for a specific purpose, without automatically turning the consensus into proof of the object's identity.

**Choosing the right residual**: for a homography $H$ mapping image A to B, $e_i=\|\pi(H\tilde p_i)-q_i\|_2$ is a transfer error in pixels of B, with $\pi$ the homogeneous division. Epipolar geometry imposes another constraint, and PnP combines 3-D points with a calibrated projection. Reusing a threshold without stating the residual changes what "inlier" means. The geometric test checks compatibility conditional on the model; a symmetry can provide another set that is equally compatible. Adding an independent constraint changes the available information, while tightening the threshold only changes the tolerance of the same test.

**Model compatibility is weaker than unique identity**: A planar repeated texture can support two different homographies with similarly small transfer errors. A physically meaningful residual rejects pairs inconsistent with a chosen model, but cannot resolve a symmetry that preserves the measurements. Independent appearance, a motion bound or another sensor can break that ambiguity when justified. Otherwise return competing hypotheses or refuse the registration instead of treating a large consensus as proof of absolute alignment.

**Blocking errors**: Inferring physical validity from the reciprocity of nearest neighbors.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [OpenCV 4.13.0 calib3d.hpp, findHomography transfer error and RANSAC](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L776-L844); [Rey-Otero and Delbracio 2014, IPOL §5 repeated structures](https://doi.org/10.5201/ipol.2014.82). Symmetry scenario and independent verification: project reasoning.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCHING-004 provenance::agent pole::B pole::E
END

## CV-MATCHING-005

Objective: diagnose a homography that `findHomography` returns without error but cannot be trusted. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-005
Question: With OpenCV 4.13, an alignment service calls `H, mask = cv2.findHomography(src, dst)` on 400 ratio-filtered pairs; ground truth shows that only 60 of them are correct. The call raises no exception and returns a $3\times3$ matrix, but the warped image is visibly misplaced. After the call becomes `cv2.findHomography(src, dst, cv2.RANSAC, 3.0)`, with `maxIters` and `confidence` left at their defaults of 2000 and 0.995, most image pairs align, yet some still fail on similar data, again with a non-empty matrix. Explain both silent failures, quantify what the second call can promise, and state what the service should check after each call before accepting $H$.
Reponse: **Expected answer**: (1) The default `method=0` is not robust: all 400 pairs, 340 of them wrong, enter one normalized DLT followed by Levenberg–Marquardt refinement, so the outliers pull the model. The function raises an exception only for malformed input, such as fewer than four pairs, and returns an empty matrix only when no matrix can be computed; a biased $H$ is a normal return. (2) With RANSAC, $w=60/400=0.15$ would need $N=\lceil\log(0.005)/\log(1-0.15^4)\rceil=10{,}464$ samples for confidence 0.995, but the loop stops at `maxIters`=2000, where the nominal confidence is only $1-(1-0.15^4)^{2000}\approx0.637$. OpenCV still returns the best hypothesis found, which always exists because a minimal sample fits its own four pairs, and reports neither the cap nor the confidence reached. (3) After each call: make the robust `method` explicit; from the returned mask, compute the inlier count and $\hat w$, and refuse, or re-run with a larger `maxIters`, when the count is below a validated minimum or $N(\hat w)$ exceeds `maxIters` (with the defaults, whenever $\hat w<0.227$); validate $H$ on held-out points across the useful region.

**Further explanation**: On the method-0 path every pair has the same weight, so the estimate is a compromise between the true plane and 340 unrelated positions; more iterations cannot help, because nothing is sampled. In 4.13.0 the output mask is then recomputed at `ransacReprojThreshold` for every method except RHO, method 0 included. In 4.11.0, method 0 returned a mask of ones, which reads as 100% inliers. With RANSAC, the iteration count starts at `maxIters` and only decreases when a larger consensus implies fewer samples; at $\hat w=0.15$ the update returns the cap itself. The whole budget then contains about $2000\times0.15^4\approx1.01$ all-inlier sample in expectation.

**Why the observed rate can differ**: OpenCV redraws minimal samples with collinear points or inconsistent orientations before they count as iterations, which discards many contaminated samples, so the empirical success rate can exceed 0.637. What the cap removes is the guarantee, not necessarily the result, and the shortfall grows quickly as $w$ falls.

**Diagnosis**: The random generator has a fixed seed, so re-running the same call returns the same $H$; permuting the pairs changes the draws and exposes an unstable estimate. A hypothesis fitted to clutter keeps few inliers: its four sample pairs and chance agreements. A minimum inlier count set on validation pairs therefore rejects it. Constructed scenario; numbers recomputed in the check script of this pass.

**Blocking errors**: Assuming that `findHomography` uses RANSAC by default. Treating a non-empty matrix, the absence of an exception or a mask of ones as success. Reading the requested 0.995 as the confidence achieved. Raising the threshold to obtain more inliers instead of raising the budget or the inlier ratio.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [OpenCV 4.13.0, calib3d.hpp L782–L844: methods, method 0 as least squares on all pairs, empty matrix when no model can be estimated, defaults](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L782-L844); [OpenCV 4.13.0, fundam.cpp L357–L463: input errors, method dispatch, refinement, recomputed mask and empty result](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp#L357-L463); [OpenCV 4.13.0, fundam.cpp L74–L106: collinearity and orientation checks of minimal samples](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp#L74-L106); [OpenCV 4.13.0, ptsetreg.cpp L55–L75 and L104–L254: capped iteration update, redrawn samples, fixed seed, best hypothesis returned](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/ptsetreg.cpp#L55-L254); [OpenCV 4.11.0, fundam.cpp L401–L447: method 0 with a mask of ones](https://github.com/opencv/opencv/blob/4.11.0/modules/calib3d/src/fundam.cpp#L401-L447). The 400-pair scenario, the 0.227 threshold and the acceptance checks are project constructions.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCHING-005 provenance::agent pole::B pole::E
END
