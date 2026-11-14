# Flashcards — FAST and BRIEF — detecting corners and describing their neighborhoods

reference note: [[40-features-matching/references/47-fast-brief|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FAST-BRIEF-001

Objective: Explain the FAST test. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-001
Question: Which intensity pattern passes the FAST segment test, and what do the subsequent steps produce?
Reponse: **Expected answer**: A contiguous arc of circle neighbors must be entirely lighter than the center plus a threshold, or darker than the center minus that threshold. The variant sets arc length and circle; non-maximum suppression keeps the locally strongest of adjacent responses.

**Further explanation**: The decision tree reduces the average number of comparisons. The output remains a keypoint position: a descriptor and a geometric check are distinct steps. An arbitrary number of scattered neighbors does not satisfy the arc test.

**Logical example**: In a given variant, several very bright neighbors scattered around the circle do not replace a long contiguous arc. The accepted pattern describes a spatial organization of the contrast around the center, not a simple histogram of neighboring values.

**Choice of implementation**: Record the threshold, the variant and the intensity unit in the protocol. A lower threshold can increase the candidates, including responses that are unstable under noise; non-maximum suppression then controls local redundancy. To diagnose a drop in matches, first check whether the same positions are detected. Fast candidate extraction does not yet provide a stable orientation, a distinctive signature or a transformation between images; these responsibilities belong to the later components of the pipeline.

**Implementation caveat (OpenCV 4.13.0 code)**: only `TYPE_9_16` follows the segment test for every arc position. A pretest written for the 16-pixel circle is shared by `TYPE_7_12` and `TYPE_5_8`, so it rejects most valid 7-of-12 arcs and every valid 5-of-8 arc; a probe with OpenCV 4.11.0, whose logic is identical, reproduced this. OpenCV also counts a circle pixel only if it differs from the center by strictly more than the threshold.

**Build an unambiguous test**: For a circle of 16 neighbors, label each position as brighter, darker or similar relative to the center and the threshold. Look for a sufficiently long contiguous run, including the wrap from the last position to the first; a simple implementation can concatenate the sequence with itself to check this wrap. This description is logical pseudocode, not a benchmarked program. Quick tests on a subset of positions can reject some candidates before the full test, depending on the variant. A lower threshold makes more differences compatible with an arc but also changes the noise sensitivity; choose the threshold in the effective intensity unit.

**The segment must wrap around the circle**: A bright arc spanning the last circle positions and the first ones is contiguous geometrically. A search that only checks a linear array can miss it, even though the intensity inequalities are correct. Conversely, counting bright samples without requiring adjacency admits separated fragments. These two constructed cases test the segment logic independently of threshold tuning or nonmaximum suppression, and avoid attributing a logical implementation error to detector sensitivity.

**Blocking errors**: Counting scattered neighbors; attributing a binary descriptor to FAST alone.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Rosten and Drummond 2006, §2.1 segment test, §2.2 decision tree, §2.3 non-maximal suppression](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [OpenCV 4.13.0 fast.cpp, FAST_t L56–L299](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/fast.cpp#L56-L299). Wrap-around and pretest cases: project constructions recomputed in the review checks.
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-FAST-BRIEF-001 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-002

Objective: Calculate a binary distance. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-002
Question: Two toy BRIEF descriptors are 101101 and 100001. Which distance should be used, and what is its value?
Reponse: **Expected answer**: The Hamming distance: XOR = 001100, so two different bits and $d_H=2$. Do not subtract integers represented by these strings.

**Further explanation**: Each bit codes a difference of intensity test on a smoothed patch. The pattern must be the same to compare descriptors. Simply converting bytes to floats does not preserve their Hamming geometry.

**Meaning of the measure**: Each position of the string holds the response to the same local test in both patches. The XOR equals one exactly where the responses differ; counting these positions therefore measures the disagreement between the tests. The binary weight used to store a bit in a byte has no geometric role in this count.

**Example and limit**: Moving or rotating a patch without adapting the pattern can change the tests while keeping the same physical object. A small distance then favors a resemblance in the chosen representation; it does not guarantee the identity of the point. Also check that the patches have used the same pattern, conventions and a compatible smoothing. The matching and its geometric verification are two complementary controls.

**Stability of one bit**: The test $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$ is particularly fragile when the difference $I_s(y_j)-I_s(x_j)$ is close to zero. Small noise can then flip the bit even though the patch shows the same point. Smoothing reduces some fluctuations but can remove the distinctive detail. Adding highly correlated bits does not bring as much information as complementary comparisons. The Hamming distance does not say whether disagreements come from noise, rotation or a different object: the data and the protocol determine its interpretation. A threshold on the number of differing bits is not automatically a match probability.

**Hamming distance is invariant to a shared bit permutation**: If both descriptor strings undergo the same permutation of test positions, their Hamming distance is unchanged: the number of disagreements is preserved. Numeric byte distance generally changes because bit significance changes. This property provides a small constructed metric check. It does not allow independently permuting descriptors from different extractors; matching requires the same physical comparison at each corresponding bit position.

**Blocking errors**: Using an L2 distance between the integers that encode the strings.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Calonder et al. 2010, §3 eqs. 1–2 and §3.3 Hamming distance distributions](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf). Permutation and bit-stability arguments: project deductions.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-FAST-BRIEF-002 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-003

Objective: separate FAST BRIEF and ORB. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-003
Question: Why are “FAST + BRIEF” and ORB not synonyms?
Reponse: **Expected answer**: FAST detects positions; BRIEF describes patches by binary tests; ORB constructs a chain including pyramid, orientation and binary tests oriented / selected. These additions change the properties of the pipeline.

**Further explanation**: A detector can remain stable while its descriptor fails under rotation. Evaluating the steps separately avoids assigning a property of the assembly to each component. The implementation variants must be named.

**Pipeline to reconstruct**: for each step, ask what goes in, what comes out and which variation it tries to handle. FAST handles candidate localization; BRIEF handles description by binary relations; orientation and scale define the frame in which these relations are compared.

**Proposed ablation**: on the same transformed scene, keep the detector and change the normalization of the descriptor orientation, then keep the description and change the selection of points. This attributes an improvement to the component actually changed. The name of a pipeline does not transfer all its properties to each building block. Even an oriented, multi-scale pipeline remains limited by visible detail, blur, and perspective distortions.

**Separate learned and computed parameters**: in ORB, the binary comparisons were selected offline on training data to be informative and weakly redundant; when a new image is processed, the orientation and the test responses are computed around each point. This is not a network trained online on the observed object. A BRIEF with a fixed pattern can have the same storage size without sharing this selection or the orientation compensation. To compare two strings, record the pattern, support, smoothing and sampling coordinates; the name of the detector does not identify the descriptor that was produced.

**An oriented pattern has its own failure source**: ORB uses an estimated orientation to rotate the comparison pattern. This improves tolerance to in-plane rotation when the estimate is repeatable, but introduces instability if orientation fluctuates on a symmetric patch. A fixed BRIEF pattern has a different tradeoff. Compare known-angle compensation with estimated-angle compensation while holding locations fixed; the gap isolates orientation estimation from the descriptor's behavior under an ideally normalized patch.

**Blocking errors**: Attributing an orientation or scale invariance to FAST alone.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Calonder et al. 2010, §3 and §4 orientation sensitivity](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf); [Rublee et al. 2011, ORB, §3.2 orientation and §4.3 learned tests](https://doi.org/10.1109/ICCV.2011.6126544). Ablation design: project construction.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FAST-BRIEF-003 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-004

Objective: Isolate a failure under rotation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-004
Question: After image rotation, FAST points remain well localized but BRIEF matching deteriorates. Which mechanism should be tested first?
Reponse: **Expected answer**: The fixed BRIEF test pattern does not necessarily follow the local orientation: pairs compare other structures after rotation. Check the orientation normalization of the patches with the detector held fixed.

**Further explanation**: Compare patches resampled into the same frame, then a descriptor oriented like ORB's. Separately rule out undetected points, patch borders and interpolation blur. This protocol isolates a cause; it does not guarantee a result at every stage. In Calonder et al.'s test, BRIEF degraded little up to 10–15° and then dropped sharply, and BRIEF applied to images derotated by SURF's orientation behaved almost like SURF: the rotation behavior depended mostly on the orientation estimate.

**Example of coordinate frame transformation**: A test that compares a pixel to the left of the center and a pixel above it no longer compares the same physical structures after rotation if the test positions remain fixed in the image. The binary result can change while the central keypoint is still correct.

**Constructed verification**: Use a known transformation, compare the same patches before and after rotation in a common frame, then examine distances with and without orientation compensation. Check the interpolation and exclude neighborhoods that leave the image. If the fault persists, test contrast, smoothing and localization stability. Orientation compensation is a useful hypothesis to isolate this cause, not a guarantee of invariance to any deformation or disappearance of texture.

**Expected compensation**: If a patch is rotated by $R_\theta$, the two sample positions of each test must be rotated consistently, or the patch must be resampled in a canonical frame before comparison. The first strategy rotates the pattern, the second transforms the local image; their interpolation and border effects may differ. With an exactly known rotation, they give a discriminating experiment that isolates the missing orientation. With an estimated orientation, its noise becomes a new cause of binary disagreement. An improvement in this ablation does not demonstrate invariance to perspective: an anisotropic deformation is not compensated by a single angle.

**Rotation near a boundary changes valid support**: An axis-aligned pattern may fit inside the image before rotation and extend beyond it afterward. Dropped descriptors or altered border sampling can then degrade matching even if the angle correction is correct. A proposed ablation keeps points well inside a margin large enough for the rotated support, then tests the original boundary population separately. This separates orientation failure from unavailable image content.

**Blocking errors**: Concluding that FAST is at fault while its points remain stable.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Calonder et al. 2010, §4 Orientation Sensitivity, Fig. 9 and O-BRIEF paragraph](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf). Verification protocol: project construction.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FAST-BRIEF-004 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-005

Objective: Measure the computation-repeatability trade-off. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-005
Question: For an embedded camera, which results should be compared before replacing SIFT with FAST/BRIEF?
Reponse: **Expected answer**: Compare repeatability, quality of matches validated, coverage, latency extraction+matching and memory, with resolution and budget of comparable points. Include representative rotations, scales and noise.

**Further explanation**: The cost of the segment test is not enough to predict the full cost. A quick extraction can create more ambiguous matches and increase geometric verification. A paper's historical numbers do not give the latency on the target hardware.

**Compare complete systems**: A gain in detection can be lost if more indistinguishable points multiply comparisons and robust-estimation samples. Conversely, a more expensive description can reduce the number of wrong hypotheses to process. The downstream cost therefore also depends on the quality and distribution of the features.

**Proposed criterion**: Set a registration tolerance and count the cases wrongly accepted, rejected and correctly registered, with the same reference transformations. Time index construction (if any), extraction, matching and geometry on the target CPU. Keep low-texture and strong-rotation cases. This protocol turns a historical speed claim into a verifiable decision for the current camera and product.

**Connecting precision and robust cost**: for a minimal solver of size $s$ and an inlier ratio $w$, the nominal number of RANSAC samples for confidence $p$ is $N\ge\log(1-p)/\log(1-w^s)$, assuming independent, non-degenerate samples. A cheaper extraction that yields a lower $w$ can therefore greatly increase the cost of geometry. This calculation is an analytical model, not an exact latency prediction: early termination, degeneracy handling and re-sampling variants change the actual behavior. Also measure time and memory on failures, where the maximum budget can be consumed, instead of timing only the easy pairs that register correctly.

**A faster front end can make geometry slower**: For homography samples of size four and nominal confidence 0.99, changing inlier fraction from 0.5 to 0.25 raises the ideal sample budget from about 72 to about 1177. This constructed calculation assumes independent nondegenerate samples and a fixed fraction. It explains why extraction latency alone is insufficient when replacing SIFT: ambiguous binary matches can transfer work to robust estimation and increase failure-path latency.

**Blocking errors**: Choosing from a published frame rate without its protocol; ignoring the cost after detection.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Rosten and Drummond 2006, §2.4 Table 1 and §3–§4](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [Calonder et al. 2010, §4 recognition rate and timing](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf). RANSAC budget and protocol: project calculation and construction.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FAST-BRIEF-005 provenance::agent pole::B pole::C pole::E
END
