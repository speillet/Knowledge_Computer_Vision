# Flashcards — FLANN — approximate nearest-neighbor search and distance conventions

reference note: [[40-features-matching/references/48-flann|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FLANN-001

Objective: choose approximate or exhaustive search. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-001
Question: Why can a FLANN index be less attractive than exhaustive search for a small database used only once?
Reponse: **Expected answer**: The build cost and memory can exceed the gain on queries. Compare $T_{\text{construction}}+N_qT_{\text{query}}$ to the exhaustive cost for the actual number of queries, with the same recall goal.

**Further explanation**: Structures suited to large datasets do not guarantee a gain on a small database or on given hardware. A comparison should include database updates, transfers and batch processing. In OpenCV 4.13, the one-shot call `knnMatch(query, train, k)` builds a new index on every call; reuse requires `add`, `train()` once, then `knnMatch(query, k)`.

**Example of amortized cost**: With 2 s of construction and 1 ms per query, a hundred queries cost about 2.1 s, while an exhaustive search at 3 ms each costs 0.3 s. For ten thousand queries on the same database, the hypothetical costs become 12 s and 30 s. The values illustrate a calculation; they are not a FLANN benchmark.

**Interpretation**: The actual number of reuses of the index and its period of validity decide the amortization. A database rebuilt for each image can lose this advantage. Also compare the quality of the neighbors: reducing the time by accepting insufficient recall is not a gain at constant objective. The choice depends on volume, hardware, batching and protocol.

**What does the index cost?**: a forest of k-d trees divides vectors by coordinates; a search follows promising regions and then explores other branches according to a budget. A hierarchical k-means tree partitions by cluster centers instead. Stopping early explains both the saved work and the lack of a general exact-neighbor guarantee. In the time model above, the break-even condition is $2+0.001N_q<0.003N_q$, so $N_q>1000$; at a thousand queries the costs are equal. This threshold depends entirely on the assumed costs. Any rebuild, additional transfer or change of budget must be added back before concluding that the index is worthwhile.

**Amortization has an explicit break-even point**: Let index construction take $B$, exhaustive query time $E$, and indexed query time $A<E$. Ignoring updates, the index pays off only after $N_q>B/(E-A)$ queries. A rebuilt database resets that amortization. Memory and required neighbor recall can rule out an apparently favorable time comparison. This is a project cost model, so measure all three terms on the actual descriptor population and target hardware rather than treating an algorithm name as a latency estimate.

**Blocking errors**: Comparing only the query time, excluding index construction.
Source: [[40-features-matching/references/48-flann|Full reference]]; [Muja and Lowe 2009, §3.3 cost with build-time and memory weights, eq. 1](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf); [OpenCV 4.13.0 matchers.cpp, one-shot knnMatch and train](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L589-L598). Cost figures: project construction.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FLANN-001 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-002

Objective: preserve the metric of descriptors. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-002
Question: A FLANN matcher configured for SIFT vectors rejects ORB descriptors. Is converting them to floats sufficient for correct matching?
Reponse: **Expected answer**: No: storage does not define the metric. The usual binary descriptors ORB compare to Hamming; converting their bytes to floats for L2 changes the meaning of the distances. Choose a Hamming search, for example BF or a compatible LSH configuration.

**Further explanation**: In OpenCV 4.13, a k-d tree index requires `CV_32F` data and an LSH index forces plain Hamming, with no Hamming2 option. For ORB with WTA_K=3 or 4, LSH therefore compares 2-bit symbols bit by bit; use brute force with Hamming2 or keep WTA_K=2. LSH is not a universal answer for every variant.

**Counter-example of representation**: Two bytes that differ only by one bit of strong weight are close in Hamming but distant as numbers. Their conversion into floats maintains this numerical gap; it does not reconstruct the binary tests that the metric must compare.

**Proposed diagnosis**: first determine which representation was actually produced and which distance its extractor expects. Then test a few pairs of descriptors with an exhaustive reference using this distance, then compare the envisaged index. A type exception is an interface index, not a permission to change the mathematical problem. A configuration that works for ORB standard still needs to be re-examined for a variant with different symbols; the support announced by the API and the final quality remain to be checked.

**Normalization and metric form a contract**: for real unit vectors $a,b$, $\|a-b\|_2^2=2-2a^Tb$ connects L2 and cosine similarity. This equivalence requires normalization and does not extend to bytes encoding ORB bits. Even for real vectors, changing their normalization after index construction can change neighbors and invalidate the setting. Keeping the extractor, its version and configuration, the dimension and the expected metric with the database makes it possible to detect these incompatibilities before matching. A type conversion is sometimes necessary for an API; it must preserve the intended mathematical representation, and must not be used to bypass an incompatible distance contract.

**Metric compatibility survives no numeric cast**: A packed binary byte of 128 differs from zero in one test, while a byte of 3 differs in two tests. Float casting keeps numeric differences 128 and 3, reversing the Hamming ranking. A compatible binary index must operate on the intended test distance. Even then, verify its supported symbol semantics: ordinary Hamming support does not automatically establish correctness for ORB two-bit winner symbols requiring Hamming2.

**Blocking errors**: Treating bytes that encode several bits as L2 coordinates.
Source: [[40-features-matching/references/48-flann|Full reference]]; [Muja and Lowe 2014, §3.3 binary features and Hamming](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf); [OpenCV 4.13.0 miniflann.cpp, type check and LSH distance](https://github.com/opencv/opencv/blob/4.13.0/modules/flann/src/miniflann.cpp#L330-L446). Byte counter-example: project deduction.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FLANN-002 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-003

Objective: Evaluate an approximation of neighbors. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-003
Question: The ratio of two matching distances becomes more favorable when the FLANN search budget is reduced. Does this prove the matches are better?
Reponse: **Expected answer**: No: the second neighbor may have been missed. The ratio is then artificially smaller. Compare the two neighbors to an exact search on a sample and measure the geometric validation.

**Further explanation**: A good recall@1 alone does not guarantee a correct second neighbor. Keep the same distance convention or squared distance to apply a ratio threshold. Geometric confidence does not stem from the ratio alone.

**Analytical example**: If the true distances of the two neighbors are 10 and 11, the ratio is about 0.91. A search that finds the first but misses the second can return 10 and 30, a ratio of about 0.33. The best candidate did not become more distinctive; the relevant competitor simply disappeared from the search.

**Proposed check**: Compare the two rows on the same set of queries, then measure the effect on the accepted pairs and inliers. Maintain a consistent convention if an API returns squared distances: the threshold of the ratio must then be adapted. An approximation can be useful, but the budget is settled by measuring its effect on downstream reasoning, not just on its own duration.

**The inverse case**: Missing the best neighbor can also make the ratio less favorable or let another candidate be accepted; a search error has no single direction of effect on the final decision. Recall@1 only measures whether the exact first neighbor is found. For a filter using two neighbors, also measure the recall of the set of the two best and the agreement of the filtering decision. Ties require a convention: several indices can share the same distance and make an identity comparison too severe. An exhaustive reference must therefore state its metric, numerical precision and equality rule, and then remain the same for all budgets evaluated.

**A rank-gap bound can certify a ratio decision**: Constructed local bound: suppose the exact first distance is recovered and the returned second distance obeys $d_2\le\hat d_2\le(1+\varepsilon)d_2$. The measured ratio satisfies $r/(1+\varepsilon)\le\hat r\le r$, where $r=d_1/d_2$. Consequently $\hat r<\tau/(1+\varepsilon)$ guarantees $r<\tau$ under those assumptions, whereas merely $\hat r<\tau$ does not. Typical search budgets do not supply such a per-query guarantee; this derivation explains why empirical filter agreement remains necessary.

**Blocking errors**: Interpreting any smaller ratio as a gain in accuracy.
Source: [[40-features-matching/references/48-flann|Full reference]]; [Muja and Lowe 2014, §2.1 time-bound approximate search](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf); [Lowe 2004, §7.1–§7.2](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf). Ratio distortion and bound: project deductions.
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-FLANN-003 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-004

Objective: Measure the time-recall curve. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-004
Question: Which measurements help tune approximate-search effort without hiding degradation of the overall pipeline?
Reponse: **Expected answer**: Measure recall of neighbors against an exact baseline, latency, memory, build, and number and quality of final geometric inliers. Change one budget at a time on held-out data.

**Further explanation**: Recall describes fidelity to the exact search; it is not the semantic precision of the matches. Repetitions of texture and erroneous geometric pattern remain possible even with exact neighbors.

**Separate three measures**: Neighbor recall compares the index to an exact search in a descriptor space; match accuracy compares pairs to a matching truth; geometric success judges the resulting transformation. These levels can diverge on repetitive textures or poorly distributed regions.

**Proposed decision curve**: For several budgets, keep the database and queries fixed, then report total time, memory, recall of the first two neighbors and errors of the final registration. Add the maintenance cost if the database changes. Choose an operating region that meets the product's constraints, then check it on a held-out batch. The goal is not to maximize recall: exhaustive search can be unnecessarily expensive, but a very fast approximation can be insufficient.

**Read a quality–cost curve**: an operating point dominates another if it keeps at least the useful quality at lower cost for the resources considered. Between non-dominated points, the choice depends on the budget and the tolerance of the product, not on a single universal score. Separating build time, query latency, memory and database update frequency avoids hiding an extra cost. Testing queries without a real match is also essential: a neighbor search usually returns something even when the correct answer is "absent". Pair rejection and geometric verification provide this possibility of refusal, which neighbor recall alone does not measure.

**Search effort should be selected on a frontier**: Sweep search effort on fixed validation queries and retain points that improve no resource without sacrificing useful registration quality. Include index construction, update frequency, query tail latency and peak memory. Test queries from a shifted acquisition regime separately, because an index tuned on easy descriptors can lose recall on a different distribution. Freeze the chosen configuration before final test evaluation rather than selecting effort from the best test-set registration score.

**Blocking errors**: Equating neighbor accuracy with the physical validity of the correspondence.
Source: [[40-features-matching/references/48-flann|Full reference]]; [Muja and Lowe 2009, §3 precision definition and §4.4 speed-up versus precision](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf); [Muja and Lowe 2014, §4](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf). Decision curve: project construction.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FLANN-004 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-005

Objective: restructure `FlannBasedMatcher` calls so that the index is built once and reused. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-005
Question: With OpenCV 4.13, a localization service matches each camera frame, about 1,000 SIFT descriptors, against a fixed map of 200,000 descriptors. At startup it creates `flann = cv2.FlannBasedMatcher(index_params, search_params)`; for every frame it calls `flann.knnMatch(des_frame, des_map, k=2)`. In this constructed profile each call takes 1.02 s, and halving `checks` only brings it to 1.01 s, whereas the developer expected about 20 ms per frame at 10 frames per second. Why is the expected speed-up never obtained, how should the calls be restructured, and what does appending 5,000 new map descriptors once a minute cost after the change?
Reponse: **Expected answer**: (1) The overload that receives the train descriptors ignores the matcher's own collection: it clones an empty matcher with the same parameters, adds `des_map` to the clone, and the clone builds a new `flann::Index` over all 200,000 descriptors before searching, then is discarded. Each call therefore pays about 1 s of build for 20 ms of search, which is why the search budget hardly matters. (2) Add the map once with `flann.add([des_map])`, call `flann.train()` at startup, and match each frame with `flann.knnMatch(des_frame, k=2)`, without the train argument: one minute of video then costs about 13 s instead of 612 s. (3) Each `add` makes the next `train()` or match rebuild the whole index from all stored descriptors instead of inserting the new ones: one append per minute costs one full rebuild, with a latency spike of about 1 s on the frame that pays it, while appending on every frame brings back the per-call cost.

**Further explanation**: In OpenCV 4.13.0 the three-argument `knnMatch` is a `const` method, and its documentation states that the train set "is not added to the train descriptors collection stored in the class object". A matcher that was already trained ignores its index when called this way, so adding `train()` at startup while keeping the three-argument call fixes nothing. The two-argument `knnMatch(query, k)` calls `train()` itself, and `FlannBasedMatcher::train()` rebuilds only when no index exists or when descriptors were added since the last build. The explicit `train()` is therefore optional, but it moves the build out of the first frame and lets it be timed separately. The one-shot `match` and `radiusMatch` take the same clone path.

**Bookkeeping after the change**: matches now carry `imgIdx`, the position of the batch in the stored collection, and `trainIdx`, the row inside that batch. After several `add` calls, look up map keypoints with both indices, not with `trainIdx` alone.

**Update policy**: a rebuild copies all stored descriptors into one matrix and builds a new index. Batch the appends; if the spike matters, build a second matcher outside the frame loop and swap it in. Searching a small buffer of recent descriptors exhaustively and merging candidates by distance is another project option. Constructed timings, recomputed in the check script of this pass; they are not a FLANN benchmark.

**Blocking errors**: Believing that the matcher caches the index built during a previous call. Calling `train()` once but still passing the map to `knnMatch`. Lowering `checks` or the number of trees to speed up a build-dominated call. Expecting `add` to insert new descriptors into the existing index incrementally.
Source: [[40-features-matching/references/48-flann|Full reference]]; [OpenCV 4.13.0, matchers.cpp L589–L598: one-shot knnMatch through an empty clone](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L589-L598); [OpenCV 4.13.0, matchers.cpp L647–L661: knnMatch on the stored collection calls train()](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L647-L661); [OpenCV 4.13.0, matchers.cpp L1113–L1176: add counts descriptors, train rebuilds when the count grows](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L1113-L1176); [OpenCV 4.13.0, matchers.cpp L423–L470 and L1389–L1442: merged copy, clone with empty train data, imgIdx and trainIdx](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/matchers.cpp#L1389-L1442); [OpenCV 4.13.0, features2d.hpp L1044–L1092 and L1126–L1138: train and the two knnMatch overloads](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/include/opencv2/features2d.hpp#L1044-L1138). The timings and the update policy are project constructions.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-FLANN-005 provenance::agent pole::B pole::E pole::F
END
