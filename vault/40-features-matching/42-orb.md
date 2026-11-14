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

**Interpreted mechanism**: Detecting a position is not enough to compare two rotated neighborhoods. The orientation establishes a local frame in which the test pattern is placed; the binary responses then describe intensity relationships in this frame. The pyramid provides several observation sizes, without making details identical across resolutions.

**Constructed diagnosis**: If keypoints are detected but matches disappear under rotation, inspect orientation stability and patch content before changing the number of points. If the keypoints themselves disappear, examine thresholds, blur and pyramid levels. This separation of steps attributes a failure to a specific mechanism instead of treating ORB as a black box.

**Calculate the orientation**: In a patch centered on the keypoint, define the moments $m_{pq}=\sum_{x,y}x^py^qI(x,y)$. The direction to the centroid is obtained by $\theta=\operatorname{atan2}(m_{01},m_{10})$ when these moments give a usable direction. The comparison pattern is then rotated by $\theta$ before the intensities are read. If the patch is almost symmetric or noisy, a small perturbation can change this orientation strongly: the position can remain repeatable without the tests describing the same oriented neighborhood. The patch borders and the actual availability of the required pixels must also be handled, not silently filled with unrelated content.

**Orientation quality can limit binary matching**: For a test point at patch radius $r$, a small orientation error $\delta\theta$ displaces the sampled location by approximately $r|\delta\theta|$ pixels. At $r=15$ px, a $5^\circ$ error moves it about 1.31 px. This constructed calculation explains why accurate keypoint location alone does not ensure stable oriented tests. Peripheral comparisons can cross edges after a modest angle error, especially in small or nearly symmetric patches.

**Blocking errors**: Presenting ORB as FAST alone, or saying it directly provides a transformation between images.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al. 2011, §3.1 FAST and Harris ranking, §3.2 intensity centroid, §4.1–§4.3 steered and learned BRIEF](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13.0 orb.cpp, L826–L1001](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp#L826-L1001). Orientation-error calculation: project deduction.
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

**Consequences for an implementation**: Converting bytes to floats keeps these numeric values and does not turn the comparison into Hamming. The symbols that carry the tests must be compared, with a variant compatible with their construction. A correct distance retains the sense of the descriptor; it still does not demonstrate that the two patches belong to the same physical point. Ambiguity filtering and geometry are still required.

**Computable version of Hamming**: for two binary strings $a,b$, $d_H(a,b)=\operatorname{popcount}(a\oplus b)$ counts the disagreements between tests. The operations run on machine words or bytes, but the result does not depend on the numerical weight of the bits. Rearranging the same tests within the bytes therefore preserves Hamming if applied to both descriptors; it can completely change L2 on the byte values. This reasoning gives a simple implementation check without an image: build two descriptors that differ in a single test, placed at several different bit positions. The expected distance remains one, which separates storage from the metric of the representation.

**A byte example exposes the wrong metric**: Compare byte values 0, 128 and 3 as packed test results. Relative to 0, Hamming distances are one bit for 128 and two bits for 3, while scalar numeric distances are 128 and 3. The ranking reverses. Casting these bytes to floating-point numbers preserves the incorrect numeric ranking. The problem is therefore semantic, not a limitation of integer storage or a need to normalize byte magnitudes.

**Blocking errors**: Justifying L2 by the mere presence of a byte array, or claiming that the two distances always rank neighbors the same way.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al. 2011, §4.1 eqs. 4–5](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13.0 core/base.hpp, NORM_HAMMING](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp#L195-L205). Byte counter-examples: project deduction.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-ORB-002 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-003

Objective: select the norm after changing the variant. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-003
Question: In OpenCV 4.13, ORB changes from `WTA_K=2` to `WTA_K=4`. What must be checked in the matcher, and why?
Reponse: **Expected answer**: Switch from `NORM_HAMMING` to `NORM_HAMMING2`, or use `orb.defaultNorm()`. With three or four candidates, each result represents a symbol on two bits; Hamming2 compares the symbols.

**Further explanation**: Hamming2 does not mean Hamming squared. Keep descriptors, matcher and index consistent, without silently mixing variants or parameters. Then re-evaluate match accuracy and geometric success before assigning degradation to the images.

Illustrative excerpt not executed, OpenCV 4.13:

```python
orb = cv.ORB_create(WTA_K=4)
matcher = cv.BFMatcher(orb.defaultNorm(), crossCheck=True)
```

**Example of symbols**: Winner values `00` and `11` are a single differing symbol. Counting the differing bits would give two, while a comparison of symbols must count one disagreement. This is the semantic reason for the change of norm; the name Hamming2 does not describe a simple arithmetic operation on the previous result.

**Implementation detail (OpenCV 4.13.0 code)**: the descriptor stays 32 bytes, so `WTA_K=3` or 4 yields 128 two-bit symbols instead of 256 binary tests, and `NORM_HAMMING2` ranges from 0 to 128. Their tuples are drawn with a fixed seed from the 512 points of the learned pattern rather than learned themselves. The variant therefore changes both the number and the selection of comparisons, not only the distance.

**Proposed controlled migration**: Regenerate the database descriptors with the same configuration as the queries, then check the matcher and the index. Do not compare vectors built differently. API compatibility avoids a measurement error, but the final choice of variant is still judged on the matches and on registration success.

**What the winner encodes**: for each group of $K$ positions, the result is the index of the position of maximum intensity. With three or four candidates, the two bits form a categorical symbol, not two independent binary questions. The disagreements `00→01` and `00→11` must therefore each count as one different symbol. This logic explains why the change also requires rebuilding a persistent descriptor database: the same array length does not guarantee the same semantics. Also check that the approximate search index supports this metric; a correct norm in an exhaustive matcher does not automatically validate every binary index.

**Blocking errors**: Keeping plain Hamming automatically, or describing Hamming2 as the square of a distance.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [OpenCV 4.13.0 features2d.hpp, ORB WTA_K and BFMatcher norms](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp#L423-L461); [OpenCV 4.13.0 orb.cpp, WTA_K encoding and defaultNorm](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp#L220-L350); [core/base.hpp, NORM_HAMMING2](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp#L195-L205).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ORB-003 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-004

Objective: distinguish between two matching filters. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-004
Question: For ORB descriptors, how do cross-checking and a ratio test differ, and what does neither guarantee?
Reponse: **Expected answer**: Cross-checking requires mutual neighbors; the ratio test requires the best neighbor to be sufficiently better than the second. Neither guarantees a correct physical match or a valid geometric model.

**Further explanation**: A mutual match may remain ambiguous in a repetitive pattern; a well-separated neighbor may be wrong. In BFMatcher OpenCV, the cross-check corresponds to reciprocity with a single neighbor, not to a transparent replacement of `knnMatch(k=2)`. Record the filtering before the geometric check.

**Examples of separating logics**: a neighbor can be the best choice in both directions while being almost tied with another candidate. The cross-check can then accept it while a strict ratio refuses it. Conversely, a well-separated neighbor for one query may prefer another query in the other image and fail at the mutual check.

**Practical interpretation**: These tests filter relationships in the descriptor space; they do not know the depth or the projection constraints. Keeping track of rejected candidates and their coverage helps to settle the trade-off between ambiguity and number of geometric constraints. The protocol must announce which test is applied, in what order and with what number of neighbors available.

**Example of non-equivalent filters**: In a constructed distance matrix, query A has candidates at distances 10 and 11, and the first also prefers A to every other query. The cross-check accepts it, while a ratio of 0.8 rejects it. Query B has 10 and 30, but its best candidate prefers A: the ratio accepts it and reciprocity rejects it. These cases show that the two rules ask different questions. An explicit combination can be designed, at the cost of additional computation and lower recall; it must define what to do with ties and missing candidates, and then be validated geometrically.

**Tie handling belongs to the acceptance rule**: Binary distances are discrete, so ties are common. If the first and second distances are equal and nonzero, a strict ratio threshold below one rejects the match. Mutual-nearest matching can instead depend on which tied candidate the implementation chooses. Neither deterministic tie-breaking nor mutuality supplies physical evidence. Include repeated patterns and exact distance ties in a proposed comparison so changes in candidate ordering do not appear to improve geometric reliability.

**Blocking errors**: Presenting the tests as identical, or as a geometric validation.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [OpenCV 4.13.0 features2d.hpp, BFMatcher crossCheck](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp#L1255-L1280); [Lowe 2004, §7.1 ratio test](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf). Distance-matrix and tie cases: project constructions.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ORB-004 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-005

Objective: Diagnose a loss of repeatability. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-005
Question: ORB works at a fixed distance but fails when the camera moves away. Which assumptions should be examined before simply increasing the feature count?
Reponse: **Expected answer**: check the range and spacing of the pyramid scales, the effective resolution of details and the repeatability of keypoints. The number requested does not restore a missing information or an uncovered scale.

**Further explanation**: Visualize the levels and the detected points, keep lighting and focus controlled, then compare a pyramid variation with the initial protocol. Add perspective and blur separately. ORB does not have perfect scale invariance: with OpenCV's defaults (8 levels, factor 1.2) the pyramid spans only $1.2^7\approx3.6$, and the authors state that scale invariance was not adequately addressed. Another method may be required after measurement.

**Physical example**: A small, well-resolved marking near the camera may cover only a few pixels once the camera moves away. Changing the density of the pyramid can help if a relevant size was sampled incorrectly, but not if the acquisition has already destroyed the contrast of the marking. Increasing the quota only adds points elsewhere.

**Proposed investigation**: track the same visible structures across distances, observe their detection levels and check the number of pixels actually covering the pattern. Test separately resolution, focus and pyramid. Then measure an error on the useful region, because more points on the bottom does not restore the location of the part. This reasoning links acquisition and features rather than assigning everything to the matcher.

**Scale coverage and cost**: with a pyramid factor $s>1$, a detail of size $r$ pixels at the initial level covers about $r/s^\ell$ pixels at level $\ell$. Increasing the number of levels extends the scales examined; reducing $s$ samples them more finely but increases the work for the same range. No level restores a detail already undersampled in the input image. In a constructed case, a three-pixel-wide tag reduced to one pixel no longer offers the same intensity tests, even if its overall position remains known. The detection thresholds and the quotas distributed between levels must therefore be analyzed against the resolution actually available on the target.

**Blocking errors**: Claiming that the pyramid handles any scale change, or tuning only the matcher without looking at detection.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al. 2011, §3.1 pyramid and §7 scale invariance](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13.0 orb.cpp, per-level budget and pyramid](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp#L842-L855). Scale-coverage reasoning: project deduction.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ORB-005 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-006

Objective: Relate computational constraints to task success. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-ORB-006
Question: You must localize a marking on an embedded CPU with limited memory. How can an ORB baseline be built without assuming its final suitability?
Reponse: **Expected answer**: set variations and location tolerance, extract ORB with recorded parameters, match with its norm and then validate geometrically. Measure full cost and failures on representative data, and then compare an alternative if the need is not met.

**Further explanation**: Binary descriptors are compact, but the number of points, the matching and the difficult cases also count; on the authors' 1 GHz phone, matching about 400 points (72.8 ms) cost more than ORB extraction (66.6 ms). Define the behavior when the registration is uncertain, and do not turn a strong consensus into certainty. This is a system proposal, with no field results announced.

**Usable baseline**: Explicitly plan for three outcomes: accepted transformation, uncertain outcome and no outcome. Set acceptance from the residuals, the coverage and the plausibility of the motion, then evaluate acceptance errors on held-out parts. A controlled refusal may be preferable to a misplaced inspection region.

**Proposed comparison**: Keep the same inputs and tolerances for a SIFT alternative, including every step whose cost actually changes. Measure peak memory and latency in representative conditions, not just the time of an isolated call. ORB's compact representation motivates the test; the balance of accuracy, robustness, cost and failure behavior decides its suitability.

**Establishing a concrete memory budget**: In the current OpenCV variant at 256 bits, a descriptor occupies 32 bytes; 2000 descriptors represent about 64 kB of raw data. This excludes keypoints, pyramid images, buffers, indexes, allocations, and program structures: this calculation is not a measure of memory peak. An exhaustive search between two sets of $n$ and $m$ points processes $nm$ pairs, even with a fast binary distance. Defining the behavior when there are no descriptors or too few pairs for the model prevents a speed optimization from turning a normal observation failure into an arbitrary result or a runtime error.

**A memory estimate needs database lifetime**: A persistent database amortizes descriptor extraction and index construction differently from a one-shot pair comparison. Estimate storage as descriptor bytes times retained points and reference views, then add image pyramids, keypoint metadata and matcher working memory. A proposed benchmark should include cold initialization and steady-state queries, recording peak resident memory separately from raw descriptor size. Reducing the feature cap may save memory while removing the coverage needed for reliable registration.

**Blocking errors**: Promising a latency from the paper alone, or ignoring the failure rate to choose the fastest method.
Source: [[40-features-matching/references/42-orb|reference note ORB]]; [Rublee et al. 2011, §6.1 and §6.3 timings](https://doi.org/10.1109/ICCV.2011.6126544); [OpenCV 4.13.0 features2d.hpp, ORB::kBytes](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp#L423-L461). Baseline and memory estimate: project construction.
Tags: cv::pilote cv::d04 famille::conception cv_id::CV-ORB-006 provenance::agent pole::B pole::E pole::F
END
