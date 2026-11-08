# Flashcards — ORB — detection and oriented binary descriptors

reference note: [[40-features-matching/references/42-orb|ORB]]. Source of writing: Agent.

TARGET DECK: CV::Pilote::40-features-matching

## CV-ORB-001

Objective: rebuild the ORB mechanism. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-001
Question: How does ORB turn an image into an oriented binary descriptor, and what is each component's role?
Reponse: **Expected answer**: FAST detects candidates in a pyramid; a ranking, Harris in the article, selects points; the center of mass of intensities provides orientation; oriented BRIEF tests form the binary descriptor.

**Further explanation**: rBRIEF selects high-variance, low-correlation tests offline. The pyramid gives discrete scale levels; the rotation of the pattern compensates for a local orientation. Matching and geometric verification are later steps, not guaranteed outputs of ORB.

**Interpreted mechanism**: Detecting a position is not enough to compare two turned neighborhoods. The orientation establishes a local coordinate frame in which the test pattern is moved; the binary responses then describe intensity relationships in this coordinate frame. The pyramid provides several sizes of observation, without making all the details identical to the different resolutions.

**Constructed diagnosis**: If keypoints are detected but matches disappear under rotation, inspect orientation stability and patch content before changing the number of points. If the keypoints disappear themselves, examine thresholds, blur and pyramid levels. This separation of steps makes it possible to attribute a failure to a specific mechanism instead of treating ORB as a black box.

**Calculate the orientation**: In a keypoint-centric patch, set the $m_{pq}=\sum_{x,y}x^py^qI(x,y)$ moments. The direction to the centroid is obtained by $\theta=\operatorname{atan2}(m_{01},m_{10})$ when these moments give an actionable direction. The pattern of comparisons is then rotated according to $\theta$ before the intensity readings. If the patch is almost symmetrical or noisy, a small disturbance can strongly change this orientation: the position can remain repeatable without the tests describing the same oriented neighborhood. The edges of the patch and the actual presence of the required pixels must also be managed, not silently supplemented by unrelated content.

**Orientation quality can limit binary matching**: For a test point at patch radius $r$, a small orientation error $\delta\theta$ displaces the sampled location by approximately $r|\delta\theta|$ pixels. At $r=15$ px, a $5^\circ$ error moves it about 1.31 px. This constructed calculation explains why accurate keypoint location alone does not ensure stable oriented tests. Peripheral comparisons can cross edges after a modest angle error, especially in small or nearly symmetric patches.

**Blocking errors**: Present ORB as only FAST, or say it directly provides a transformation between images.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al., §§3 – 4](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html); [OpenCV 4.13, Feature Matching, Standards, Cross Check and KnnMatch; verified with Context7](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-ORB-001 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-002

Objective: Linking representation and distance. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-002
Question: Why is L2 distance between bytes of a binary-test ORB descriptor different from Hamming distance?
Reponse: **Expected answer**: Bytes store test results bit by bit. Hamming counts different bits; L2 treats bytes as numbers whose value depends on the weight of binary positions.

**Further explanation**: between `00000000` and `10000000`, Hamming is 1 and the numerical difference is 128; a low bit would have another numerical difference despite a single test changed. The `uint8` type describes storage, not the semantics of distance. This reasoning concerns `WTA_K=2`.

**Analytical counter-example**: Comparing `00000000` to `00000011` gives two different bits, but a numerical difference of three. Comparing the same first byte to `10000000` gives a single different bit, but a numerical difference of 128. The two distances can therefore reverse the ranking of candidates.

**Consequences for an implementation**: Convert bytes to floats retains these numeric values and does not transform the comparison into Hamming. We must compare the symbols that carry the tests, with a variant compatible with their construction. A correct distance retains the sense of the descriptor; it still does not demonstrate that the two patches belong to the same physical point. Ambiguity filtering and geometry are still required.

**Computable version of Hamming**: for two binary suites $a,b$, $d_H(a,b)=\operatorname{popcount}(a\oplus b)$ adds the disagreements between tests. The operations are machine words or bytes, but the result does not depend on the numerical weight of the bits. A change in the placement of the same tests in the bytes therefore retains Hamming if applied to both descriptors; it can completely change L2 on the byte values. This reasoning gives a simple implementation check, without an image: build two patterns of which a single test differs in several positions. The expected distance remains one, which separates metric storage and metric representation.

**A byte example exposes the wrong metric**: Compare byte values 0, 128 and 3 as packed test results. Relative to 0, Hamming distances are one bit for 128 and two bits for 3, while scalar numeric distances are 128 and 3. The ranking reverses. Casting these bytes to floating-point numbers preserves the incorrect numeric ranking. The problem is therefore semantic, not a limitation of integer storage or a need to normalize byte magnitudes.

**Blocking errors**: justify L2 only by the presence of an array of bytes, or pretend that the two distances always rank neighbors in the same way.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [OpenCV 4.13, matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-ORB-002 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-003

Objective: select the norm after changing the variant. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-003
Question: In OpenCV 4.13, ORB changes from `WTA_K=2` to `WTA_K=4`. What must be checked in the matcher, and why?
Reponse: **Expected answer**: Switch from `NORM_HAMMING` to `NORM_HAMMING2`, or use `orb.defaultNorm()`. With three or four candidates, each result represents a symbol on two bits; Hamming2 compares the symbols.

**Further explanation**: Hamming2 does not mean Hamming squared. Keep the compatible descriptors and matcher throughout the index, without silently mixing variants or parameters. Then re-evaluate match accuracy and geometric success before assigning degradation to the images.

Illustrative excerpt not executed, OpenCV 4.13:

```python
orb = cv.ORB_create(WTA_K=4)
matcher = cv.BFMatcher(orb.defaultNorm(), crossCheck=True)
```

**Example of Symbols**: Two `00` and `11` win values are a single different symbol. Counting the different bits would yield two, while a comparison of the symbols must count a disagreement. This is the semantic reason for the change of norm; the name Hamming2 does not describe a simple arithmetic operation on the previous result.

**Proposed controlled migration**: Regenerate database descriptors with the same configuration as queries, then check matcher and index. Do not compare vectors from different constructs. A good API compatibility avoids a measurement error, but the final choice of the variant is still judged on the matches and the success of the registration.

**What the Winner Codes**: for each group of $K$ positions, the result indicates the index of the position of maximum intensity. With three or four candidates, the two bits are a categorical symbol, not two independent binary questions. The `00→01` and `00→11` disagreements must therefore count each for a different symbol. This logic explains why the change also requires reconstructing a persistent descriptor base: the same table length does not guarantee the same semantics. Also check that the approximate search index supports this metric; a correct norm in an exhaustive matcher does not automatically validate all binary indexes.

**Blocking errors**: Automatically keep Hamming simple or describe Hamming2 as the square of a distance.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [OpenCV ORB, WTA_K](https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html); [OpenCV 4.13, Feature Matching, Standards, Cross Check and KnnMatch; verified with Context7](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), see 2026-10-30.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ORB-003 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-004

Objective: distinguish between two matching filters. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-004
Question: For ORB descriptors, how do cross-checking and a ratio test differ, and what does neither guarantee?
Reponse: **Expected answer**: Cross-checking requires mutual neighbors; the ratio test requires the best neighbor to be better enough than the second. No one guarantees a correct physical match or a valid geometric pattern.

**Further explanation**: A mutual match may remain ambiguous in a repetitive pattern; a separate neighbor may be false. In BFMatcher OpenCV, the cross-check corresponds to reciprocity with a single neighbor, not to a transparent replacement of `knnMatch(k=2)`. Record the filtering before the geometric check.

**Examples of separating logics**: a neighbor can be the best choice in both directions while being almost ex æquo with another pattern. The cross-check can then accept it while a strict ratio refuses it. Conversely, a well-separated neighbor for one query may prefer another query in the other image and fail at the mutual check.

**Practical interpretation**: These tests filter relationships in the descriptor space; they do not know the depth or the projection constraints. Keeping track of rejected candidates and their coverage helps to settle the trade-off between ambiguity and number of geometric constraints. The protocol must announce which test is applied, in what order and with what number of neighbors available.

**Example of non-equivalent filter**: In a built-up distance matrix, request A can have candidates with distances 10 and 11; the former also prefers it to all other requests. The cross-check accepts it, while a ratio of 0,8 rejects it. A request B may have 10 and 30, but its best candidate prefers A: the ratio accepts it and reciprocity rejects it. These cases show that the two rules pose different questions. One can design an explicit combination, at the cost of additional calculations and reminders; it must define what to do with ex æquo and absent candidates, and then be geometrically validated.

**Tie handling belongs to the acceptance rule**: Binary distances are discrete, so ties are common. If the first and second distances are equal and nonzero, a strict ratio threshold below one rejects the match. Mutual-nearest matching can instead depend on which tied candidate the implementation chooses. Neither deterministic tie-breaking nor mutuality supplies physical evidence. Include repeated patterns and exact distance ties in a proposed comparison so changes in candidate ordering do not appear to improve geometric reliability.

**Blocking errors**: Present the tests as identical or as a geometric validation.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [OpenCV BFMatcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ORB-004 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-005

Objective: Diagnose a loss of repeatability. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-005
Question: ORB works at a fixed distance but fails when the camera moves away. Which assumptions should be examined before simply increasing the feature count?
Reponse: **Expected answer**: check the range and spacing of the pyramid scales, the effective resolution of details and the repeatability of keypoints. The number requested does not restore a missing information or an uncovered scale.

**Further explanation**: View levels and points detected, keep light and focus controlled, and then compare a pyramid variation to the initial protocol. Add perspective and blur separately. ORB does not have a perfect scale invariance; another method may be required after measurement.

**Physical example**: A small well-solved marking near the camera may only cover a few pixels after remoteness. Changing the density of the pyramid can help if a relevant size was sampled incorrectly, but not if the acquisition has already destroyed the contrast of the marking. Increasing the quota only adds points elsewhere.

**Proposed investigation**: track the same visible structures between distances, observe their detection levels and check the number of pixels actually devoted to the pattern. Test separately resolution, focus and pyramid. Then measure an error on the useful region, because more points on the bottom does not restore the location of the part. This reasoning links acquisition and features rather than assigning everything to the matcher.

**Scales and cost coverage**: with a pyramid factor $s>1$, a detail of size $r$ pixels at the initial level covers about $r/s^\ell$ pixels at the $\ell$ level. Increasing the number of levels extends the scales examined; reducing $s$ samples them more finely but increases the work for the same range. No level restores an already undersampled detail in the input image. In a constructed case, a three-pixel-wide tag reduced to one pixel no longer offers the same intensity tests, even if its overall position remains known. The detection thresholds and quotas distributed between levels must therefore be analysed with the resolution actually available on the target.

**Blocking errors**: announce that the pyramid solves any scale change or adjust only the matcher without looking at the detection.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al., conclusion](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV ORB](https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html); [OpenCV 4.13, Feature Matching, Standards, Cross Check and KnnMatch; verified with Context7](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), see the 2026-10-30.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ORB-005 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-006

Objective: articulating computational constraint and task success. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-006
Question: You must localize a marking on an embedded CPU with limited memory. How can an ORB baseline be built without assuming its final suitability?
Reponse: **Expected answer**: set variations and location tolerance, extract ORB with recorded parameters, match with its norm and then validate geometrically. Measure full cost and failures on representative data, and then compare an alternative if the need is not met.

**Further explanation**: Binary descriptors are compact but the number of points, matching and difficult cases also count. Predicting behavior when the registration is uncertain and not turning a strong consensus into certainty. This is a system proposal, with no field results announced.

**Usable baseline**: Explicitly predict three outcomes: accepted transformation, uncertain outcome, and no outcome. Set the acceptance from the residuals, cover and plausibility of the movement, and then evaluate the acceptance errors on reserved parts. A controlled refusal may be preferable to a poorly placed inspection region.

**Proposed comparison**: Keep the same inputs and tolerances for a SIFT alternative, including steps that actually change in cost. Measure maximum memory and latency in representative conditions, not just the time of an isolated call. The compact representation of ORB motivates the test; it is the balance of precision, robustness, cost and behavior in failure that decides its suitability.

**Establishing a concrete memory budget**: In the current OpenCV variant at 256 bits, a descriptor occupies 32 bytes; 2000 descriptors represent about 64 kB of raw data. This excludes keypoints, pyramid images, buffers, indexes, allocations, and program structures: this calculation is not a measure of memory peak. An exhaustive search between two sets of $n$ and $m$ points processes $nm$ pairs, even with a fast binary distance. Preparing behavior when there are no descriptors or too few pairs for the model prevents a speed optimization from turning a normal observation failure into an arbitrary result or execution error.

**A memory estimate needs database lifetime**: A persistent database amortizes descriptor extraction and index construction differently from a one-shot pair comparison. Estimate storage as descriptor bytes times retained points and reference views, then add image pyramids, keypoint metadata and matcher working memory. A proposed benchmark should include cold initialization and steady-state queries, recording peak resident memory separately from raw descriptor size. Reducing the feature cap may save memory while removing the coverage needed for reliable registration.

**Blocking errors**: Promise latency from the single article or ignore the failure rate to choose the fastest method.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al., §§4 – 6](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13, ORB, Theory and WTA_K](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html); [OpenCV 4.13, Feature Matching, Standards, Cross Check and KnnMatch; verified with Context7](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d04 famille::conception cv_id::CV-ORB-006 provenance::agent pole::B pole::E pole::F
END
