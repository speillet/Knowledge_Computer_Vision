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

**Local model**: for a small displacement $d$, the photometric variation is close to a quadratic form $d^TMd$. The matrix $M$ gathers the products of the gradients in the vicinity. Its own directions indicate the directions of movement that change the appearance much or little.

**Constructed example**: On a uniform vertical edge, moving the patch horizontally changes its contents; moving it along the edge can almost leave it the same. A visible corner shows changes in two directions, which helps locate a move. This does not imply that it is unique in the image: the corners of a grid can all look the same. So distinguish local location information and ambiguity of association between images. A poorly lit, obscured or too large window can also invalidate the small photometric model despite favorable eigenvalues.

**Link to the aperture problem**: The linearized luminance constant gives $I_xu+I_yv+I_t=0$, an equation for two displacement components. On an edge, the neighboring gradients are almost parallel, so stacking their equations does not add a second independent direction. A corner brings different gradient orientations and can make the local system invertible. This reasoning assumes a movement common to the patch and small variations between images. A window through two objects can have a well-conditioned tensor but no longer respect the single movement. The corner score should be read with this model, and not as a universal utility score for all estimators.

**Blocking errors**: Confound a strong single gradient and two independent stresses.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]] ; [OpenCV Harris, theory](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) ; [OpenCV Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html) ; [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
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

**Breakdown of Inputs and Outputs**: FAST takes an image and coordinate frame candidate positions from local comparisons. BRIEF takes neighborhoods around selected positions and produces binary test strings. A matcher then compares these strings, and then a geometric step examines whether the pairs explain a plausible transformation.

**Example of a built diagnosis**: If no position is detected on a fuzzy piece, changing the distance of the matcher cannot create the missing keypoints. If the points are stable but the descriptors go wrong with the part, the defect may be in the description or its coordinate frame. Describing each step by its contract avoids replacing a component that does not address the observed cause. A complete string like ORB adds pyramid and orientation choices; it does not make FAST and BRIEF synonymous.

**Expected equivariance and invariance**: If an image is geometrically transformed by $T$, a repeatable detector should find the transformed positions $T(p)$; it should therefore not produce the same numerical coordinates. On the contrary, the descriptor aims at a comparable representation of the corresponding neighborhoods after the planned standardizations. Confusing these two properties misconstrues a rotation test: the coordinates should change, while the description should stay close enough. Too much invariance can also remove distinctive information and make several patches similar. The aim is not to make all descriptors identical under any transformation, but to keep discrimination in the field of variations useful.

**Blocking errors**: Assign geometrically verified matches to a detector alone.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [OpenCV 4.13.0, FAST, Feature Detection](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html); [OpenCV 4.13.0, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html); [OpenCV 4.13, Feature Matching, BF/FLANN, metrics and filters; Context7 check](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), see 2026-10-30.
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

**Why the approximation is taking place**: A fast index explores fewer candidates than a comprehensive search. He may miss the best neighbor or competitor used to estimate ambiguity. A seemingly better ratio can thus result from a second neighbor that is too far away, and not from a more reliable match.

**Proposed deletion**: preserve descriptors and images, recalculate the two neighbors by exact search on a sample, and then compare the pairs before and after filtering. Finally examine the inliers and the error on the useful region. Change the search budget without changing the detector simultaneously. Include index construction and possible reconstructions in total time. A setback in geometric success may come from approximation, poor metrics, or ambiguous data; the controlled comparison serves to separate them rather than declaring FLANN incorrect in general.

**Measuring the Cascade Effect**: on the same requests, keep successively the identity of the two neighbors, the decision of the ratio filter, the insider status and the reserved geometric error. This track allows you to locate where a search difference becomes a product error. If the index finds the exact neighbors but the registration changes, consider order of matches, separation of the ex æquo and randomness of the robust estimate. If neighbors differ, only increasing the budget or redoing the exact distances on additional candidates is a more targeted ablation. An identical recall average may still mask the loss of rare distinguishing points that are decisive for lifting a symmetry.

**Blocking errors**: Evaluate only the request time or the number of matches.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html); downstream protocol and effect on ratio: project reasonings.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCHING-003 provenance::agent pole::B pole::E
END

## CV-MATCHING-004

Objective: choose a geometric check. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-MATCHING-004
Question: Two repeated logos produce similar descriptors. Which component can test a physical model of the correspondences?
Reponse: **Expected answer**: A geometric check adapted to the scene, with residuals, thresholds and cover; the matcher alone does not guarantee it.

**Further explanation**: A symmetry can remain consistent; look for a distinctive observation or independent constraint.

**What the Geometry Tests**: A homography for a plane, or an appropriate multiview constraint, links candidate positions in images. The residual expresses their disagreement with this model in a defined unit. A matcher chooses neighbors in an appearance representation; these two problems are different.

**Limite construite**: Two identical logos on the same medium can produce a coherent group of matches and a transformation that matches the wrong logo. A geometric model does not necessarily resolve a symmetry of the scene. Look for a single brand, an expected position, or an additional observation that distinguishes assumptions. check also supports spatial points and reserved observations. This step provides reasons for accepting a transformation for a specific purpose, without automatically transforming the consensus into proof of the object's identity.

**Choosing the right residual**: for a $H$ homography sending the image A to B, $e_i=\|\pi(H\tilde p_i)-q_i\|_2$ is a transfer error in B pixels, with $\pi$ the homogeneous division. An epipolar geometry imposes another constraint, and PnP combines points 3D and calibrated projection. Reusing a threshold without announcing the residual changes what “inlier” means. The geometric test checks for compatibility conditional to the model; one symmetry can provide another set equally compatible. Adding an independent constraint is then a change in available information, while tightening the threshold only changes the tolerance of the same test.

**Blocking errors**: Deduct the physical validity of the reciprocity of the nearest neighbors.
Source: [[40-features-matching/references/43-detecteurs-matchers|Full reference]]; [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html); symmetry scenario and independent verification: project reasoning.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCHING-004 provenance::agent pole::B pole::E
END
