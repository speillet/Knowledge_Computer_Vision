# Review — Factor graphs and incremental optimization — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 10 to revision 11. Highest severity per card before correction:
0 blocking, 1 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

Revision 10 held about 835 words of body, with a truncated orphan line ("update of
iSAM2 (Kaess et al. 2012). A new factor affects only…", the remains of a lost
heading), mistranslations ("A false buckle closure", "stresses between poses",
"observed marks") and one-sentence sections. Its iSAM2 claims had not been re-verified
on 2026-11-08 because the paper's passages timed out; this pass re-read them and found
them correct. The switchable-constraints paper, previously read only through Agarwal
et al., was read directly.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Bipartite factorization of the posterior and Gaussian MAP as nonlinear least squares: confirmed (Kaess et al. §2, eq. 5; GTSAM tutorial §1, quoted 2026-10-23). Expected answer said "a graph divided between variables … and factors", "the density a posteriori", "a nonlinear least square … (Mahalanobis distance)" (squared norms) | Understanding: representation versus solver | 3 criteria; 396 → 398 words | Aligned with the reference appendix | Minor | Meaning-restoring language fix of the expected answer; language fixes |
| CV-FACTEURS-002 | Gauge counts 6 (pose graph, project deduction), 7 (monocular BA), 4 (visual-inertial): confirmed (Zhang et al. abstract and §I; Ceres Gauge Invariance); three gauge treatments with similar accuracy and time: confirmed (abstract, Table I) | Reasoning: anchoring and gauge | 2 criteria; 375 → 379 words | Aligned | Minor | Language fixes ("defined to a similarity", "set these parameters", "announcing the authorized alignment") |
| CV-FACTEURS-003 | Diagnosis of a false loop: consistent with Agarwal et al. (abstract, §III). Expected answer said "Check the combination of places" (French *association de lieux*); explanation garbled: "Encrypted test … the residual Bleached Square $\chi^2_l$ the quantile …", "this breaking factor" | Diagnosis: loop-closure verification | 3 criteria; 395 → 403 words | Aligned | Important | Meaning-restoring fix of the expected answer; garbled test sentence rewritten with the 95% quantile 12.59 for 6 degrees of freedom (recomputed) |
| CV-FACTEURS-004 | Switchable constraints (linear switch in $[0,1]$, prior towards 1, information scaled by $\Psi^2$): confirmed directly in Sünderhauf and Protzel (eq. 1, §II-A, §II-B); DCS eq. 15 and $s^2$ scaling: confirmed (Agarwal et al. §IV); RRR rejects, the others keep a low weight: confirmed (§II). "Close form", "recalled to 1", "Reasoning the project" | Comparison: robust back-ends | 3 criteria; 390 → 390 words | Aligned | Minor | Language fixes; Source line now cites the switchable-constraints paper itself |
| CV-FACTEURS-005 | Alg. 4 (affected paths to the root, orphans), §3.4 (ordering, CCOLAMD), §4.1 ($\beta$, $\beta=0.1$ nearly exact on Manhattan), §4.2 ($\alpha$ on the change of the delta): confirmed on the IJRR paper, pp. 8–10. Expected answer word order garbled ("paths between variables affected … and root") | Algorithm: what an incremental update recomputes | 3 criteria; 387 → 409 words | Decimal comma | Minor | Meaning-restoring fix of the expected answer; CCOLAMD detail added to the explanation |

Expected-answer changes (meaning-restoring language fixes, old → new):

- CV-FACTEURS-001: "a graph divided between variables … that factorizes the density a posteriori … a nonlinear least square on residuals weighted by their covariance (Mahalanobis distance)" → "a bipartite graph between variables … that factorizes the posterior density … a nonlinear least-squares problem on residuals weighted by their covariance (squared Mahalanobis norms)".
- CV-FACTEURS-003: "Check the combination of places, relative transformation, coordinate frames and the weight of the loop factor" → "Check the place association, the relative transformation, the coordinate frames and the weight of the loop factor".
- CV-FACTEURS-004: "recalled to 1 by a prior" → "pulled towards 1 by a prior"; "calculates this weight in close form" → "computes this weight in closed form".
- CV-FACTEURS-005: "Only cliques on paths between variables affected by new factors or selected for relinearization and root … A variable is only relinearized if its estimated deviation from its linearization point exceeds a $\beta$ threshold … where the changes remain below a $\alpha$ threshold" → "Only the cliques on the paths between the root and the variables affected by new factors or selected for relinearization … a variable is relinearized only if its delta from the linearization point exceeds a threshold $\beta$ … where the changes of the delta remain below a threshold $\alpha$".

## Reference findings

Claims of revision 10 checked against their passages:

- Kaess et al. 2012 (IJRR PDF): §2 Gaussian case (elimination equivalent to sparse QR),
  §3.3 Alg. 4, §3.4 (COLAMD comparison, CCOLAMD), §4.1 (fluid relinearization, $\beta=0.1$
  on Manhattan, units), §4.2 (partial updates, $\alpha$): confirmed. The 2026-11-08
  "not re-verified" status is lifted for these passages.
- Agarwal et al. 2013: eq. 15, $s^2$ scaling, RRR versus keeping low weights: confirmed;
  the perceptual-aliasing statement is in the abstract, not §II as cited.
- Zhang et al. 2018: gauge counts and comparison: confirmed.
- No scientific error was found. Language defects that obscured meaning: "A false buckle
  closure" (loop closure), "pose graph for stresses between poses, BA for poses and
  observed marks" (constraints, landmarks), "fluid relinearization … $\beta=0{,}1$",
  "Question of work", "Reference Response", "Probability at cost", "residual from pose
  to be defined", "Example of weight DCS built", "squared blanked error", decimal commas,
  and the orphan line without its heading.

Implementation facts added (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| Relinearization threshold | $\beta$; 0.1 in the experiments; units differ, "take the minimum over all thresholds" (§4.1) | GTSAM 4.2 `relinearizeThreshold` default 0.1, scalar or per variable type and dimension (ISAM2Params.h) |
| Partial-update threshold | $\alpha$ on the change of the delta; 0.001 in the experiments (§4.2, §5) | GTSAM 4.2 `wildfireThreshold` 0.001 (Gauss–Newton) or $10^{-5}$ (Dogleg) |
| Factorization | QR equivalence of elimination (§2) | GTSAM 4.2 default `CHOLESKY`, `QR` recommended for poorly conditioned problems |
| DCS | $s=\min(1,2\Phi/(\Phi+\chi^2_l))$, information $\times s^2$ (eq. 15) | GTSAM 4.2 `mEstimator::DCS` weight $(2c/(c+e^2))^2$ for $e^2>c$ (LossFunctions.cpp L353–L362) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 835 → 3,626. About
650 tokens are the two tables and the pseudocode.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (two sentences) | Developed | Variables with dimensions and units, factor types with residual dimensions, initial values, gauge choice, outputs, front-end/back-end role |
| Intuition | Partly developed | Developed | Spring analogy; worked example A (correct and false loop on a drifting 1-D chain, recomputed) |
| Prerequisites | Shallow (two links) | Developed | Links to CV-SVD, CV-SE3, CV-FUSION, CV-BA, CV-VIO, CV-MATCHING |
| Assumptions | Shallow | Developed | Conditional independence and double counting, noise model, association, initialization, gauge counts, degenerate cases |
| Procedure | Shallow | Developed | Pseudocode of graph construction, loop handling, update and diagnosis with the purpose of each step |
| Mathematics | Partly developed | Developed | MAP to whitened least squares (Kaess eq. 5), sparsity and QR equivalence, pose residual, gauge as null space with worked example B, robust back-ends (switchable constraints, DCS, RRR) with worked example C, iSAM2 update mechanics, marginalization |
| Parameters | Shallow (one sentence) | Developed | Table with noise models, robust parameters, gauge treatment, $\beta$, $\alpha$, `relinearizeSkip`, factorization; tuning approach with injected outliers |
| Properties | Shallow | Developed | MAP equivalence, local optimality, incremental exactness, robust back-end behaviour, gauge invariance |
| Cost and implementation | Partly developed (iSAM2 prose, orphan line) | Developed | Cost drivers; GTSAM 4.2 `ISAM2Params`, `DCS`, `Pose3` ordering and Ceres covariance contracts; execution status |
| Evaluation | Shallow (one constructed case) | Developed | Metrics; baseline and controlled variation with injected false loops; hypothesis and confound; measurement limits |
| Failure modes and diagnosis | Partly developed (prose and list) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow (one sentence) | Developed | Conditional choices among filter, pose graph, BA, incremental and batch, robust back-ends; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/14-graphes-facteurs.py`](checks/14-graphes-facteurs.py) (10 checks): the
singular Laplacian of a relative graph and its determinant $3\cdot10^{-6}$ with a $10^{-6}$
prior; the 1/11 spread of a correct loop and the whitened residual of about 46 caused by a
false loop; DCS weights ($s=0.2$, $s^2=0.04$, $s=2/7$ at $\chi^2=6$) and the GTSAM DCS weight;
the DCS fixed point that suppresses the false loop ($s\approx8\cdot10^{-6}$) but also the true
one ($s\approx0.02$) when the loop covariance is 1 cm, and keeps $s\approx0.45$ with 5 cm; the
$\sqrt2$ double-counting effect; the 95% $\chi^2_6$ quantile 12.59.

## Applied corrections

- [Reference](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md),
  revision 10 → 11: body rewritten and deepened as above; orphan line removed into the
  iSAM2 subsection; citation of the perceptual-aliasing statement moved to the abstract;
  mistranslations fixed in the body and all three appendices (including "Probability at
  cost" → "From probability to cost", "See the gauge" → "Seeing the gauge", "residual from
  pose to be defined" → "Defining a pose residual", "Example of weight DCS built" →
  "Constructed DCS weight example", "squared blanked error" → "whitened squared error",
  "Removing a variable transmits a constraint" → "Eliminating a variable creates a
  constraint", "The incremental reuses" → "Incremental inference reuses", "excitation and
  pattern" → "excitation and a correct model"); the 2026-11-08 note that iSAM2 passages
  timed out now points to this re-verification; sources split; closing provenance line
  replaced. Front matter unchanged except `revision`; H1, the five `### CV-FACTEURS-00N`
  headings and a `## Sources and flashcards` heading kept.
- [Cards](../../../vault/10-mathematiques-estimation/14-graphes-facteurs.md): the
  expected-answer fixes above; CV-FACTEURS-003 test sentence rewritten; CV-FACTEURS-005
  explanation completed with CCOLAMD; CV-FACTEURS-004 Source line cites Sünderhauf and
  Protzel directly; language fixes in explanations and blocking errors; Source lines
  "consult the" / "see" → "consulted". Questions, IDs, objectives, families, tags and
  target deck unchanged.

No other vault card repeats a claim corrected here (`rg` for "DCS", "switchable",
"iSAM2" and "relinearization" outside this subject finds only CV-VIO and CV-BA mentions
without contradicting statements).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FACTEURS-01 | CV-FACTEURS | Design an evaluation of a robust back-end with a frozen front-end: inject false loops by policy (random, local, grouped), compare least squares, a robust loss, switchable constraints and DCS, and measure relative pose error and true-loop retention | The evaluation family is absent for this subject; no card trains separating front-end and back-end effects | Evaluation; Evaluation and controlled variation | 1 card, 4 criteria | [Sünderhauf and Protzel 2012, §III-C, §IV](https://nikosuenderhauf.github.io/assets/papers/IROS12-switchableConstraints.pdf); [Agarwal et al. 2013, §V](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) |
| P-CV-FACTEURS-02 | CV-FACTEURS | Predict the DCS weight of a correct loop from its whitened residual and explain why an overconfident loop covariance can freeze drift instead of correcting it | CV-FACTEURS-004 names the risk qualitatively; no card trains the computation that reveals it | Reasoning; Mathematics, worked example C | 1 card, 3 criteria ($s=\min(1,2\Phi/(\Phi+\chi^2_l))$; residual measured in loop sigmas versus accumulated odometry sigmas; remedy) | [Agarwal et al. 2013, §IV eq. 15, §V-E](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) |

## Sources

Scientific sources, opened at the passages listed:

- Kaess et al. 2012, [IJRR PDF](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf): pages
  8–10 read as images (§3.3 Alg. 4, §3.4, §4 opening, §4.1 Alg. 5–6, §4.2 Alg. 7,
  Fig. 8 caption) and text extraction for §2 (eq. 5, Gaussian case) and §5 parameters.
- Agarwal et al. 2013, [ICRA PDF](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf):
  abstract, §I, §II, §III eq. 6, §IV eq. 14–16 and §IV-A, §V opening and §V-E.
- Sünderhauf and Protzel 2012, [authors' preprint](https://nikosuenderhauf.github.io/assets/papers/IROS12-switchableConstraints.pdf):
  eq. 1, §II-A, §II-B, §III-C heading, §IV-A.
- Zhang et al. 2018, [authors' preprint](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf): abstract,
  Fig. 1 caption, §I opening, Table I caption.
- Triggs et al. 2000: §6.1 and §9, read for CV-SVD in this pass.

Implementation sources:

- GTSAM 4.2 `gtsam/nonlinear/ISAM2Params.h` L30–L245; `gtsam/linear/LossFunctions.h`
  L375–L379 and `LossFunctions.cpp` L353–L372; `gtsam/geometry/Pose3.h` (read for
  CV-SE3).
- Ceres Solver 2.2.0 `docs/source/nnls_covariance.rst` (read for CV-SVD).
- GTSAM tutorial "Factor Graphs and GTSAM": not re-read; its passages were quoted in the
  2026-10-23 report and are used for the same details.

Failed accesses and limits:

- Dellaert and Kaess, "Factor graphs for robot perception", was not consulted; the factor
  graph material relies on Kaess et al. 2012 and the GTSAM tutorial.
- g2o was not consulted; DCS's reported convergence advantage is quoted only for the
  authors' g2o Gauss–Newton setting.
- Context7 was not available in this session (see the scope record); versioned official
  code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (after rewrapping one line that started with a bracketed citation followed by a colon) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/14-graphes-facteurs.py` | 10 checks passed |
| `git diff --check -- vault/10-mathematiques-estimation/ docs/revues/2026-11-14-reference-depth/` | No whitespace error |
| `inventaire_cartes.py vault/10-mathematiques-estimation/14-graphes-facteurs.md` | 5 cards, 379 to 409 words, no anomaly; absent families: practice, evaluation, design |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 10` → `11`; five `### CV-FACTEURS-00N` headings unchanged; `$$` and code fences balanced |

No solver was run; the proposed baseline and variation are protocols, not results. Tables
and display equations were not rendered in Obsidian, and AnkiDroid rendering of the
corrected cards is unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-FACTEURS
revision 11; meaning-restoring expected-answer fixes of CV-FACTEURS-001, 003, 004 and 005;
iSAM2 passages re-verified; Agent Claude Code self-review; to republish with
`paquet-anki`) and the proposal register (P-CV-FACTEURS-01, P-CV-FACTEURS-02).
