---
id: CV-FLANN
type: methode
domaine: d04
poles: ["B", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-MATCHING"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# FLANN — approximate nearest-neighbor search and distance conventions

## Prerequisites and competencies

**Required prerequisites**: [CV-MATCHING](43-detecteurs-matchers.md). **Target competencies**: choose approximate or exhaustive search; preserve the metric of descriptors; evaluate an approximation of neighbors; measure the recall time curve. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Quickly search for neighbors among many descriptors. The entry includes base, queries, metric and research budget; the exit contains candidates with their distances, with no general guarantee of exact neighbor. An index for floating vectors in L2 is not interchangeable with an index for binary strings in Hamming.

## Mechanism, parameters and cost

FLANN includes several search structures and configuration choices, not a single matching algorithm. Muja and Lowe study random kd-tree forests and hierarchical k-mean trees. The index builds an organization of the database; the query explores a fraction of the candidates. Trees and visiting budget exchange memory, construction, request time and recall. OpenCV 4.13 shows a kd-tree for SIFT and an LSH index for common binary ORB descriptors. These configurations do not make any metric compatible.

## Mathematics and conventions

On a sample, compare the approximate neighbor $\hat n(q)$ to the exact neighbor $n^*(q)$ calculated with the same distance. The call@1 is the fraction of requests whose exact neighbor is found; treat the ex æquo according to an announced protocol. The amortized cost is $T_{construction}+N_qT_{requête}$ for $N_q$ queries. The distance of each match retains the sense of the metric used; also check distance or squared distance in the API before any ratio. The search of the two neighbors must be reliable enough for a relevant ratio test.

## Evaluation and controlled variation

Proposed baseline: comprehensive research on a representative subset. Change the search budget, keeping base, queries and metrics; measure call@1/2, build time, batch latency, memory and geometric inliers. Constructed example: 2 s build plus 100 queries at 1 ms cost 2,1 s; brute force at 3 ms costs 0,3 s. With 10 000 queries, costs become 12 s versus 30 s. The index does not win for any use.

## Diagnosis and alternatives

A type error with ORB does not allow blindly converting bytes to float for L2: keep the Hamming metric or choose a suitable index. A drop in the inliers after acceleration may come from the recall of the two neighbors, not the detector. A small base can support comprehensive research. An evolutionary basis also requires measuring reconstruction and invalidation of the index. No FLANN benchmark executed; the above costs are hypothetical.

## Guided reasoning and proposed checks

These constructed cases develop neighbor recall, index ratio and damping. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FLANN-001

**Question of work**: Why can a FLANN index be less attractive than exhaustive search for a small database used only once?

**Reference Response**: The build cost and memory can exceed the gain on queries. Compare $T_{construction}+N_qT_{requête}$ to the full cost for the actual number of queries, with the same recall goal.

**Example of amortized cost**: With 2 s of construction and 1 ms per query, a hundred queries cost about 2,1 s, while an exhaustive search at 3 ms each costs 0,3 s. For ten thousand queries on the same basis, the hypothetical costs become 12 s and 30 s. The values illustrate a calculation, without constituting a benchmark FLANN.

**Interpretation**: The actual number of re-uses of the index and its period of validity decide the depreciation. A reconstructed base with each image can lose this advantage. Also compare the quality of the neighbors: reducing the time by accepting an insufficient recall is not a gain to constant objective. The choice depends on volume, material, batches and protocol.

### Case linked to CV-FLANN-004

**Question of work**: Which measurements help tune approximate-search effort without hiding degradation of the overall pipeline?

**Reference Response**: Measure recall of neighbors against an exact baseline, latency, memory, build, and number and quality of final geometric inliers. Change one budget at a time on reserved data.

**Separate three measures**: Neighbor recall compares the index to an exact search in a descriptor space; match accuracy compares pairs to a matching truth; geometric success judges the resulting transformation. These levels can diverge on repetitive textures or poorly distributed regions.

**Proposed Decision Curve**: for several budgets, keep base and queries then report full time, memory, recall of the first two neighbors and errors of the final registration. Add the maintenance cost if the base changes. Choose an operating region that meets the constraints of the product, and then check it on a reserved lot. This result is not limited to maximising recall: exhaustive research can be unnecessarily expensive, but a very fast approximation can be insufficient.

**Documentary reference for this pass**: [Muja and Lowe 2009](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf), §§2 – 3, index and search compromise. The other developments are in the [flashcards](../48-flann.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FLANN-001

**Situation**: Why can a FLANN index be less attractive than exhaustive search for a small database used only once?

**What does the index cost?**: a forest of kd-trees divides vectors by coordinates; a search follows promising regions and then explores other branches according to a budget. A hierarchical k-mean tree partitions rather by group centers. Stopping early explains both the labor economy and the lack of an accurate general neighbor guarantee. In the time model already built, the damping threshold checks $2+0,001N_q<0,003N_q$, so $N_q>1000$; at a thousand queries the costs are equal. This threshold depends entirely on the assumed costs. Any reconstruction, additional transfer or change in the budget must be reinstated before concluding that the index is of interest.

### CV-FLANN-002

**Situation**: A FLANN matcher configured for SIFT vectors rejects ORB descriptors. Is converting them to floats sufficient for correct matching?

**Standardization and metric form a contract**: for real unit vectors $a,b$, $\|a-b\|_2^2=2-2a^Tb$ connects L2 and cosine similarity. This equivalence requires normalization and does not extend to bytes encoding ORB bits. Even for real vectors, changing their normalization after index construction can change neighbors and invalidate the setting. Keeping the extractor, its version/configuration, the dimension and the expected metric with the base makes it possible to detect these incompatibilities before the matching. A type conversion is sometimes necessary for an API; it must preserve the desired mathematical representation, and is not used to bypass an incompatible distance contract.

### CV-FLANN-003

**Situation**: The ratio of two matching distances becomes more favorable when the FLANN search budget is reduced. Does this prove the matches are better?

**Inverse case not to be forgotten**: Missing the best neighbor can also make the ratio less favorable or make another candidate accept; the search error does not have a single direction on the final decision. The call@1 measures only if the first exact neighbor is found. For a filter using two neighbors, also measure the recall of the set of the two best and the agreement of the filtering decision. Ex-æquo require a convention: several clues can have the same distance and make an identity comparison too severe. An exhaustive reference must therefore announce metric, numerical precision and equality rule, and then remain the same for all budgets evaluated.

### CV-FLANN-004

**Situation**: Which measurements help tune approximate-search effort without hiding degradation of the overall pipeline?

**Read a quality – cost curve**: an operating point dominates another if it retains at least the useful quality by costing less depending on the resources considered. Between undominated points, the choice depends on the budget and tolerance produced, not on a single universal score. Separating build time, query latency, memory, and update frequency from the base avoids masking a misplaced extra cost. Testing queries without a real match is also essential: a neighbor search will usually return someone even if the correct answer is "absent". The rejection of pairs and the geometric verification define this possibility of refusal, which the only recall of the neighbors does not measure.

**Passages consulted for these developments**: [Muja and Lowe 2009](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf), §§3.1 – 3.3, structures, budget and configuration.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FLANN-001 — Amortization has an explicit break-even point

Let index construction take $B$, exhaustive query time $E$, and indexed query time $A<E$. Ignoring updates, the index pays off only after $N_q>B/(E-A)$ queries. A rebuilt database resets that amortization. Memory and required neighbor recall can rule out an apparently favorable time comparison. This is a project cost model, so measure all three terms on the actual descriptor population and target hardware rather than treating an algorithm name as a latency estimate.

### CV-FLANN-002 — Metric compatibility survives no numeric cast

A packed binary byte of 128 differs from zero in one test, while a byte of 3 differs in two tests. Float casting keeps numeric differences 128 and 3, reversing the Hamming ranking. A compatible binary index must operate on the intended test distance. Even then, verify its supported symbol semantics: ordinary Hamming support does not automatically establish correctness for ORB two-bit winner symbols requiring Hamming2.

### CV-FLANN-003 — A rank-gap bound can certify a ratio decision

Constructed local bound: suppose the exact first distance is recovered and the returned second distance obeys $d_2\le\hat d_2\le(1+\varepsilon)d_2$. The measured ratio satisfies $r/(1+\varepsilon)\le\hat r\le r$, where $r=d_1/d_2$. Consequently $\hat r<\tau/(1+\varepsilon)$ guarantees $r<\tau$ under those assumptions, whereas merely $\hat r<\tau$ does not. Typical search budgets do not supply such a per-query guarantee; this derivation explains why empirical filter agreement remains necessary.

### CV-FLANN-004 — Search effort should be selected on a frontier

Sweep search effort on fixed validation queries and retain points that improve no resource without sacrificing useful registration quality. Include index construction, update frequency, query tail latency and peak memory. Test queries from a shifted acquisition regime separately, because an index tuned on easy descriptors can lose recall on a different distribution. Freeze the chosen configuration before final test evaluation rather than selecting effort from the best test-set registration score.

Consulted foundations: [Muja and Lowe 2014](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf): §§2–3 approximate search, search budget and data-dependent index selection.

## Sources and flashcards

- [Muja and Lowe 2009, §§2 – 3, approximate search and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
- [OpenCV 4.13, Feature Matching, BF and FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
- [Related flashcards](../48-flann.md): CV-FLANN-001 to 004.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
