# Flashcards — FLANN — approximate nearest-neighbor search and distance conventions

reference note: [[40-features-matching/references/48-flann|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FLANN-001

Objective: choose approximate or exhaustive search. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-001
Question: Why can a FLANN index be less attractive than exhaustive search for a small database used only once?
Reponse: **Expected answer**: The build cost and memory can exceed the gain on queries. Compare $T_{construction}+N_qT_{requête}$ to the full cost for the actual number of queries, with the same recall goal.

**Further explanation**: Structures suitable for large games do not guarantee a win on a small base or on a given material. A comparison should include database updates, transfers, and batch processing.

**Example of amortized cost**: With 2 s of construction and 1 ms per query, a hundred queries cost about 2,1 s, while an exhaustive search at 3 ms each costs 0,3 s. For ten thousand queries on the same basis, the hypothetical costs become 12 s and 30 s. The values illustrate a calculation, without constituting a benchmark FLANN.

**Interpretation**: The actual number of re-uses of the index and its period of validity decide the depreciation. A reconstructed base with each image can lose this advantage. Also compare the quality of the neighbors: reducing the time by accepting an insufficient reminder is not a gain to constant objective. The choice depends on volume, material, batches and protocol.

**What does the index cost?**: a forest of kd-trees divides vectors by coordinates; a search follows promising regions and then explores other branches according to a budget. A hierarchical k-mean tree partitions rather by group centers. Stopping early explains both the labor economy and the lack of an accurate general neighbor guarantee. In the time model already built, the damping threshold checks $2+0,001N_q<0,003N_q$, so $N_q>1000$; at a thousand queries the costs are equal. This threshold depends entirely on the assumed costs. Any reconstruction, additional transfer or change in the budget must be reinstated before concluding that the index is of interest.

**Blocking errors**: Compare only the query time excluding indexing.
Source: [[40-features-matching/references/48-flann|Full reference]] ; [Muja and Lowe 2009, §§2 – 3, approximate search and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FLANN-001 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-002

Objective: preserve the metric of descriptors. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-002
Question: A FLANN matcher configured for SIFT vectors rejects ORB descriptors. Is converting them to floats sufficient for correct matching?
Reponse: **Expected answer**: No: storage does not define the metric. The usual binary descriptors ORB compare to Hamming; converting their bytes to floats for L2 changes the direction of the distances. Choose a Hamming search, for example BF or a compatible LSH configuration.

**Further explanation**: OpenCV 4.13 illustrates kd-tree for SIFT and LSH for ORB. For ORB WTA_K=3 or 4, check the need for Hamming2 and the actual matcher support; LSH is not a universal response to any variant.

**Counter-example of representation**: Two bytes that differ only by one bit of strong weight are close in Hamming but distant as numbers. Their conversion into floats maintains this numerical gap; it does not reconstruct the binary tests that the metric must compare.

**Proposed diagnosis**: determine first which representation has actually been produced and how far its manufacturer is waiting. Then test a few pairs of descriptors with an exhaustive reference using this distance, then compare the envisaged index. A type exception is an interface index, not a permission to change the mathematical problem. A configuration that works for ORB standard still needs to be re-examined for a variant with different symbols; the support announced by the API and the final quality remain to be checked.

**Standardization and metric form a contract**: for real unit vectors $a,b$, $\|a-b\|_2^2=2-2a^Tb$ connects L2 and cosine similarity. This equivalence requires normalization and does not extend to bytes encoding ORB bits. Even for real vectors, changing their normalization after index construction can change neighbors and invalidate the setting. Keeping the extractor, its version/configuration, the dimension and the expected metric with the base makes it possible to detect these incompatibilities before the matching. A type conversion is sometimes necessary for an API; it must preserve the desired mathematical representation, and is not used to bypass an incompatible distance contract.

**Blocking errors**: Process bytes encoding multiple bits as L2 coordinates.
Source: [[40-features-matching/references/48-flann|Full reference]]; [OpenCV 4.13, Feature Matching, BF and FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html); [Muja and Lowe 2009, §§3.1 – 3.3, structures, budget and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf), see 2026-10-30.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FLANN-002 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-003

Objective: Evaluate an approximation of neighbors. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-003
Question: The ratio of two matching distances becomes more favorable when the FLANN search budget is reduced. Does this prove the matches are better?
Reponse: **Expected answer**: No: the second neighbor may have been missed. The ratio is then artificially smaller. Compare the two neighbors to an exact search on a sample and measure the geometric validation.

**Further explanation**: A good call@1 alone does not guarantee a correct second neighbor. Keep the same distance convention or squared distance to apply a ratio threshold. Geometric confidence does not stem from the ratio alone.

**Analytical example**: If the true distances of the two neighbors are 10 and 11, the ratio is about 0,91. A search that finds the first but misses the second can return 10 and 30, a ratio of about 0,33. The best candidate did not become more distinctive; the relevant competitor simply disappeared from the search.

**check**: Compare the two rows on the same set of queries, then measure the effect on the accepted pairs and inliers. Maintain a consistent convention if an API returns squared distances: the threshold of the ratio must then be adapted. An approximation can be useful, but the budget is settled by measuring its effect on downstream reasoning, not just on its own duration.

**Inverse case not to be forgotten**: Missing the best neighbor can also make the ratio less favorable or make another candidate accept; the search error does not have a single direction on the final decision. The call@1 measures only if the first exact neighbor is found. For a filter using two neighbors, also measure the recall of the set of the two best and the agreement of the filtering decision. Ex-æquo require a convention: several clues can have the same distance and make an identity comparison too severe. An exhaustive reference must therefore announce metric, numerical precision and equality rule, and then remain the same for all budgets evaluated.

**Blocking errors**: Interpret any smaller ratio as a gain in accuracy.
Source: [[40-features-matching/references/48-flann|Full reference]] ; [Muja and Lowe 2009, §§2 – 3, approximate search and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-FLANN-003 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-004

Objective: measure the recall time curve. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FLANN-004
Question: Which measurements help tune approximate-search effort without hiding degradation of the overall pipeline?
Reponse: **Expected answer**: Measure recall of neighbors against an exact baseline, latency, memory, build, and number/quality of final inlays. Change one budget at a time on reserved data.

**Further explanation**: The call describes fidelity to the exact search; it is not the semantic precision of the matches. Repetitions of texture and erroneous geometric pattern remain possible even with exact neighbors.

**Separate three measures**: Neighbor recall compares the index to an exact search in a descriptor space; match accuracy compares pairs to a matching truth; geometric success judges the resulting transformation. These levels can diverge on repetitive textures or poorly distributed regions.

**Proposed Decision Curve**: for several budgets, keep base and queries then report full time, memory, reminder of the first two neighbors and errors of the final registration. Add the maintenance cost if the base changes. Choose an operating region that meets the constraints of the product, and then check it on a reserved lot. This result is not limited to maximising recall: exhaustive research can be unnecessarily expensive, but a very fast approximation can be insufficient.

**Read a quality – cost curve**: an operating point dominates another if it retains at least the useful quality by costing less depending on the resources considered. Between undominated points, the choice depends on the budget and tolerance produced, not on a single universal score. Separating build time, query latency, memory, and update frequency from the base avoids masking a misplaced extra cost. Testing queries without a real match is also essential: a neighbor search will usually return someone even if the correct answer is "absent". The rejection of pairs and the geometric verification define this possibility of refusal, which the only reminder of the neighbors does not measure.

**Blocking errors**: Assimilate the accuracy of the neighbor to the physical validity of the correspondence.
Source: [[40-features-matching/references/48-flann|Full reference]] ; [Muja and Lowe 2009, §§2 – 3, approximate search and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FLANN-004 provenance::agent pole::B pole::E pole::F
END
