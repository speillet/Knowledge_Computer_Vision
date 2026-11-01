# Flashcards — FAST and BRIEF — detecting corners and describing their neighborhoods

reference note: [[40-features-matching/references/47-fast-brief|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FAST-BRIEF-001

Objective: Explain the FAST test. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-001
Question: Which intensity pattern passes the FAST segment test, and what do the subsequent steps produce?
Reponse: **Expected answer**: A contiguous arc of circle neighbors must be entirely lighter than the center plus a threshold, or darker than the center minus that threshold. The variant sets arc length and circle; removing maxima selects neighboring responses.

**Further explanation**: The decision tree reduces the average number of comparisons. The output remains a keypoint position: a descriptor and a geometric check are distinct steps. An arbitrary number of scattered neighbors does not satisfy the arc test.

**Logical example**: In a given variant, several very clear neighbors distributed throughout the circle do not replace a long contiguous arc. The accepted pattern describes a spatial organization of the contrast around the center, not a simple histogram of neighboring values.

**Choice of implementation**: keep threshold, variant and unit of intensity in the protocol. A lower threshold potentially increases candidates, including unstable responses under noise; deletion of maxima check then local redundancy. To diagnose a drop in matches, first observe if the same positions are detected. A rapid extraction of candidates does not yet give any stable orientation, distinctive signature, or transformation between images. These responsibilities belong to the following components of the chain.

**Build an unambiguous test**: For a circle of 16 neighbors, code each position as light, dark or similar to the center depending on the threshold. Look for a fairly long contiguous sequence, taking into account the connection between the last and the first position of the circle; a naive implementation can double the sequence to verify this connection. This description is a logical pseudocode, not a benchmark program. Rapid tests of a subset of positions may reject some candidates before the full test, depending on the variant. A lower threshold makes more differences compatible with an arc, but also changes the noise sensitivity; choose the threshold in the effective intensity unit.

**Blocking errors**: Count scattered neighbors; assign a binary descriptor to FAST alone.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Rosten and Drummond 2006, §§2 – 3, test and learning segment](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [OpenCV 4.13, FAST, non-maxima testing and deletion segment; fallback after timeout of author PDF](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html), see 2026-10-30.
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

**Sense of measurement**: Each position of the string represents the response to the same local test in both patches. The XOR is worth one exactly when the answers differ; counting these positions therefore measures the test’s disagreement. The binary weight used to store a bit in a byte has no geometric role in this count.

**Example and Limit**: Moving or rotating a patch without adapting the pattern can change the tests while keeping the same physical object. A small distance then favors a resemblance in the chosen representation; it does not guarantee the identity of the point. Also check that the patches have used the same pattern, conventions and a compatible smoothing. The matching and its geometric verification are two complementary controls.

**Stability of one bit**: The $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$ test is particularly fragile if the $I_s(y_j)-I_s(x_j)$ difference is close to zero. A low noise can then return the bit, even if the patch represents the same point. Smoothing reduces some fluctuations but can remove the distinctive detail. Adding highly correlated bits does not provide as much information as complementary comparisons. Hamming's distance does not tell what disagreements arise from noise, rotation, or other object: it is the data and protocol that determine its interpretation. A threshold relating to the number of bits is not automatically a match probability.

**Blocking errors**: Use a distance L2 between integers encoding strings.
Source: [[40-features-matching/references/47-fast-brief|Full reference]] ; [Calonder et al. 2010, §3, BRIEF tests and smoothing](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
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

**Chain to rebuild**: ask for each step what comes in, what comes out and what variation it tries to process. FAST responds to the location of candidates; BRIEF to the description by binary relations; orientation and scales organize the coordinate frame in which these relations are compared.

**Proposed deletion**: on the same transformed scene, keep the detector and change the normalization of the descriptor orientation, then keep the description and change the selection of points. This makes it possible to attribute an improvement to the actually changed component. The name of an assembly does not allow all its properties to be transferred to each brick. Even an oriented, multi-scale pipeline remains limited by visible detail, blur, and perspective distortions.

**Separate learned and calculated parameters**: in a ORB assembly, the selection of binary comparisons aims at informative and little redundant tests on learning data; at the extraction of a new image, the orientation and answers of these tests are calculated around each point. This is not an online trained network on the observed part. A BRIEF with a fixed pattern can share the same storage without sharing this selection or the orientation compensation. To compare two strings, record the pattern, support, smoothing and sampling coordinates; the name of the detector does not identify the descriptor that was produced.

**Blocking errors**: Assign orientation or invariance of universal scale to FAST alone.
Source: [[40-features-matching/references/47-fast-brief|Full reference]] ; [OpenCV 4.13, ORB, orientation and rBRIEF](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FAST-BRIEF-003 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-004

Objective: Isolate a failure under rotation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-004
Question: After image rotation, FAST points remain well localized but BRIEF matching deteriorates. Which mechanism should be tested first?
Reponse: **Expected answer**: The fixed BRIEF test pattern does not necessarily follow the local orientation: pairs compare other structures after rotation. check the orientation/normalization of patches with constant detector.

**Further explanation**: Compare patches put in the same coordinate frame, then a descriptor oriented like ORB. Separately remove undetected dots, patch edges, and interpolation blur. This protocol serves to isolate a cause, without guaranteeing a result on any stage.

**Example of coordinate frame transformation**: A test that compares a pixel to the left of the center and a pixel above it no longer compares the same physical structures after rotation if the test positions remain fixed in the image. The binary result can change while the central keypoint is still correct.

**Verification built**: Use a known transformation, compare the same patches before and after delivery in a common coordinate frame, and then examine distances with and without orientation compensation. check the interpolation and exclude the neighborhoods out of the image. If the fault persists, test for contrast, smoothing and stability of the location. Orientation compensation is a useful hypothesis to isolate this cause, not a guarantee of invariance to any deformation or disappearance of texture.

**Compensation expected**: If a patch is rotated by $R_\theta$, the positions of the two readings of a test must undergo a consistent transformation, or the patch must be resampled in a canonical coordinate frame before comparison. The first strategy rotates the pattern, the second transforms the local image; their interpolations and edges may differ. With an exact known rotation, they give a discriminating experience to isolate the absence of orientation. With an estimated orientation, its noise becomes a new cause of binary disagreement. An improvement in this ablation does not demonstrate an invariance in perspective: anisotropic deformation is not compensated by a single angle.

**Blocking errors**: Conclude that FAST is necessarily at fault while his points are stable.
Source: [[40-features-matching/references/47-fast-brief|Full reference]] ; [Calonder et al. 2010, §3, BRIEF tests and smoothing](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FAST-BRIEF-004 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-005

Objective: measure the compromis calculation repeatability. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-005
Question: For an embedded camera, which results should be compared before replacing SIFT with FAST/BRIEF?
Reponse: **Expected answer**: Compare repeatability, quality of matches validated, coverage, latency extraction+matching and memory, with resolution and budget of comparable points. Include representative rotations, scales and noise.

**Further explanation**: The cost of a test segment is not enough to predict the full cost. A quick extraction can create more ambiguous matches and increase geometric verification. The historical numbers of an article do not give the latency of the target hardware.

**Compare complete systems**: A gain on detection can be lost if more undistinguishable points multiply comparisons and robust estimation samples. Conversely, a more expensive description can reduce the number of bad assumptions to be addressed. The downstream cost therefore also depends on the quality and distribution of the features.

**Proposed criterion**: set a tolerance of registration and measure cases that are wrongly accepted, refused and correctly located, with the same reference transformations. Time any index construction, extraction, matching and geometry on the target CPU. Keep cases of low texture and strong rotation. This protocol turns a promise of historic speed into a verifiable decision for the current camera and product.

**Connecting precision and robust cost**: for a minimum solver of size $s$ and a rate of inliers $w$, the nominal number of prints RANSAC with confidence $p$ is $N\ge\log(1-p)/\log(1-w^s)$ under independent and non-degenerate prints. A cheaper extraction but producing a lower $w$ can therefore greatly increase the cost of geometry. This calculation is an analytical model, not an exact latency prediction: stop, degeneration and repetition variants change the actual behavior. Also measure the time and memory for failures, where the maximum budget can be consumed, instead of only timing the easy pairs correctly registered.

**Blocking errors**: Choose on a published FPS without protocol; ignore cost after detection.
Source: [[40-features-matching/references/47-fast-brief|Full reference]]; [Rosten and Drummond 2006, §§2 – 3, test and learning segment](https://www.edwardrosten.com/work/rosten_2006_machine.pdf); [Calonder et al. 2010, BRIEF, §3, tests, smoothing and patterns](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf), see 2026-10-30.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FAST-BRIEF-005 provenance::agent pole::B pole::C pole::E
END
