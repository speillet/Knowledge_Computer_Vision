# Review — Global registration and local ICP — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the pipeline note for rigid point-cloud registration. Rotation
parametrization, least-squares conditioning and the RANSAC sampling budget stay in
[CV-SE3](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md),
[CV-SVD](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md)
and [CV-HOMOGRAPHIE](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md);
the note links to them. No card was found to contain a scientific error; the defects
were mistranslations that obscured meaning and imprecise source lines.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ICP-001 | ICP converges to the local minimum of the basin containing the start: confirmed (Besl and McKay §IV-B theorem, §V basins). Left composition $T_{k+1}=\Delta T_kT_k$ for a target-frame correction: confirmed as Open3D's convention (`Registration.cpp` L143). Mistranslations obscured the loop ("dial", "consists of the other side", "rapprochement of the neighbors", "Global research", "covering and reserved") | Algorithm: separates global hypothesis generation from local refinement | 2 expected criteria; 355 → 368 lexical words | Source line cited only the moving `docs/release` tutorials | Minor | Language fixes in explanation and blocking errors; Source line given Besl §IV-B/§V and the pinned 0.19.0 global tutorial |
| CV-ICP-002 | $n^T(Rp+t-q)$ is the error component along the target normal: confirmed (Rusinkiewicz and Levoy §3.5; Low eq. 1). Linearized row $[(s\times n)^T, n^T]$: confirmed (Low eqs. 4–8; Open3D `TransformationEstimation.cpp` L86–L95 with rotation first). Plane nullspace (two translations, rotation about the normal): confirmed (Gelfand et al. §2.2). Expected answer "according to the normal unit target, in unit length" obscured the meaning | Reasoning: interpret a residual and its unconstrained directions | 2 expected criteria; 375 → 372 | Ordering translation-then-rotation in the card versus rotation-first in Open3D noted in the reference as a convention, not an error | Minor | Meaning-restoring fix of the expected answer; language fixes ("according to", "stresses", "Put", "line"); Source line given Rusinkiewicz §3.5, Low eqs. 4–8, Gelfand §2.2 |
| CV-ICP-003 | The RMSE summarizes only the accepted pairs: confirmed; Open3D's `inlier_rmse` is computed over correspondences within the threshold and `fitness` divides by the source size (`Registration.cpp` L59–L67). "Coordinate frames" was a mistranslation of *landmarks*; "reserved" of *predefined/held-out* | Diagnosis: reject a small, misleading consensus | 3 expected criteria; 347 → 348 | Wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given Open3D code lines and Rusinkiewicz §2 (ground-truth error) |
| CV-ICP-004 | Length parameters scale with the unit: confirmed by definition and by the tutorial's voxel-tied radii. French decimal commas ("0,02"); "change direction with units" altered the meaning (*change meaning*). Missing implementation condition: Open3D's `relative_rmse` is an absolute change in the cloud unit (`Registration.h` L45–L50, `Registration.cpp` L149–L154) | Practice: keep the unit contract of a registration | 2 expected criteria; 337 → 378 | Added one sentence to the "Residuals and covariance" paragraph, identical in the card and the reference appendix | Minor | Expected-answer language fix; decimal points; one sentence added for the missing condition; Source line given the tutorial and `Registration.h` lines |
| CV-ICP-005 | Point-to-plane needs reliable normals and constraining geometry: confirmed (Rusinkiewicz and Levoy §3.5, empirical convergence; Gelfand et al. §2.2, sliding). Mistranslations: "coins" (*parts*), "plan case", "current local estimator" (*common*), "isolated square" (*squared residual alone*) | Comparison: choose an ICP variant under stated conditions | 2 expected criteria; 362 → 369 | Wording aligned with the reference appendices | Minor | Expected-answer language fix; language fixes; Source line given exact sections |

Expected-answer changes (meaning-restoring language fixes, no change of criteria):

- CV-ICP-002: "The component of the misalignment according to the normal unit target,
  in unit length." → "The component of the misalignment along the target's unit
  normal, in length units."
- CV-ICP-003: "overlap, threshold, distribution of matches and error of pose on
  independent reference." → "Overlap, threshold, distribution of matches and pose
  error against an independent reference."
- CV-ICP-004: "Threshold is a length in the unit of coordinates; the scale must be
  propagated to the relevant parameters." → "The threshold is a length in the
  coordinate unit; the scale change must be propagated to the relevant parameters."
- CV-ICP-005: "It exploits reliable normals and a geometry that constrains useful
  movements; it can be ill-posed on certain surfaces or normal noise." → "It exploits
  reliable normals and a geometry that constrains the useful motions; it can be
  ill-posed on some surfaces or with noisy normals."

## Reference findings

Claims of revision 7 checked against their passages:

- Point-to-point and point-to-plane objectives: confirmed (Besl and McKay eq. 22;
  Rusinkiewicz and Levoy §3.5; Open3D 0.19.0 ICP tutorial).
- "A flat surface leaves some tangential displacements and rotations poorly
  constrained": confirmed (Gelfand et al. §2.2: two planes leave two translations and
  the rotation about the normal free).
- "FPFH 33D is a descriptor, not a pose": the 33 dimensions are confirmed by the
  0.19.0 global tutorial and `Feature.cpp` L85, L101–L111 (3 × 11 bins).
- Appendix composition rule $T_{k+1}=\Delta T_kT_k$: confirmed as Open3D's convention
  (`Registration.cpp` L143).
- The 2026-11-08 appendix line "Context7 checked" is a historical statement of that
  pass; Context7 was not available in this session and the line was not re-verified.

No scientific error was found in revision 7. Its body held one to three sentences
per section, and its English obscured meaning: "Look for neighbors" (*neighbor
search*), "stresses" (*constraints*), "Always announce sense of pose" (*state the
pose direction*), "remote initialization" (*distant initialization*), "error out of
consensus".

New claims verified for revision 8 (main ones):

- Besl and McKay: closed-form quaternion solution (eqs. 22–26); algorithm costs
  $O(N_pN_x)$ worst and $O(N_p\log N_x)$ average (§IV-A); monotone convergence to a
  local minimum with the inequality chain $0\le d_{k+1}\le e_{k+1}\le d_k\le e_k$
  (§IV-B, eqs. 31–35); 30–50 iterations to about 0.1% of the model size (§IV-B); basins
  of attraction and testing initial states (§V). The statement that thresholded ICP
  loses the monotonicity guarantee is a project deduction from the proof's
  assumptions.
- Rusinkiewicz and Levoy: six-stage taxonomy (§1); ground-truth error and single runs
  (§2); test scenes (§2.1); normal-space sampling and the incised plane (§3.1);
  projection matching (§3.2); weighting effect "small and highly data-dependent"
  (§3.3); boundary rejection and systematic bias (§3.4, Fig. 13); point-to-plane has no
  closed form, small-angle linearization, faster convergence on the fractal and
  incised-plane scenes (§3.5, Figs. 15–16); color supplies constraints (§2); 30 ms
  high-speed combination on a 550 MHz Pentium III (§4).
- Low 2004: linear system $a_i=[(p_i\times n_i)^T, n_i^T]$, $b_i=n_i^T(q_i-p_i)$
  (eqs. 4–8).
- Gelfand et al. 2003: $6\times6$ covariance matrix (§2.1), sliding along eigenvectors
  of small eigenvalues and the two-plane example (§2.2), condition number and
  normalization to unit mean distance (§3.1). The list "tunnel, cylinder, sphere" is
  labelled as a project deduction because the shapes of Fig. 3 were not read in text.
- Rusu et al. 2009: Darboux frame and angles (eq. 1), FPFH weighting (eq. 4), $O(nk)$
  versus $O(nk^2)$, $2r$ support, decorrelated histograms (§III).
- Yang et al. (TEASER): TLS cost, TIMs and TRIMs (§V-A, §V-B), maximum clique
  (§VI-D), Bunny benchmarks (robust to 90% with 100 correspondences; 99% with 1,000,
  largely due to maximum-clique pruning; under 10 ms) (§XI-B), i7-8850H laptop (§XI),
  3DMatch hotel-shower failure where the maximum clique excludes the 3 ground-truth
  inliers (§XI-E, Fig. 11 caption).

Disagreements between Open3D 0.19.0 documentation, code and papers, recorded in the
note (FR-036):

| Aspect | Paper or documentation | Open3D v0.19.0 code |
| --- | --- | --- |
| `fitness` denominator | Tutorial: "# of inlier correspondences / # of points in target" | Number of **source** points (`Registration.cpp` L65) |
| `inlier_rmse` | Tutorial: "RMSE of all inlier correspondences" | Point-to-point distances, also when the estimator is point-to-plane (L42–L46, L66) |
| ICP stopping rule | Names `relative_fitness`, `relative_rmse` | Absolute differences of fitness and RMSE (L149–L154); the header says "relative change (difference)" |
| RANSAC early stop | Header comment: $k$ from the fitness | Code uses the inlier ratio of the correspondence set under the best hypothesis (L228–L231) |
| FPFH neighbor weights | Rusu et al. eq. 4: $1/\omega_k$ with $\omega_k$ a distance, then $\frac1k$ | Inverse squared distance, each sub-histogram normalized to 100, following PCL (comment in `Feature.cpp` L153–L159) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 302 → 4,965. The
length comes from covering a two-stage pipeline (descriptors, robust estimation,
ICP), its implementation contract and its evaluation; RANSAC budgeting, rotation
algebra and least squares are linked rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Source/target notation; data contract (points, units, normals, initial guess, output direction); Besl and McKay's original setting; pipeline roles and downstream needs |
| Intuition | Shallow | Developed | Alternation mechanism and why it is local; shape-based matching; constructed bracket illustration with symmetry caveat; Mermaid pipeline with acceptance step |
| Prerequisites | Shallow (two links) | Developed | Links to CV-SE3, CV-SVD, CV-HOMOGRAPHIE, CV-FLANN, CV-STEREO, CV-BEV, CV-VIO, CV-FACTEURS |
| Assumptions | Shallow (one sentence) | Developed | Rigidity and scale; overlap and boundary bias; basin of attraction; rank deficiencies (Gelfand); symmetry versus rank deficiency; normals and sampling floor |
| Procedure | Shallow | Developed | Pseudocode of global and local stages with the purpose of each step; six-stage variant table with what Rusinkiewicz and Levoy report |
| Mathematics | Shallow (two formulas) | Developed | Conventions; closed form; convergence chain and its conditions; point-to-plane linear system; worked example A (small-angle error); stability matrix and worked example B (rank 3/5/6, unit dependence of the condition number); FPFH definitions; RANSAC budget and TEASER invariants; worked example C (RANSAC samples) |
| Parameters | Shallow (one sentence) | Developed | Ten-row parameter table with tutorial values and interactions; five-step tuning approach |
| Properties | Absent (merged with parameters) | Developed | Local monotone convergence and its limits; empirical status of point-to-plane speed; asymmetry; invariances; limits of RANSAC and TEASER certificates; meaning of quality figures |
| Cost and implementation | Shallow | Developed | Cost drivers with variables; reported speeds with hardware; Open3D 0.19.0 contracts from code (correspondences, fitness, RMSE, composition, stopping rule, estimators, FPFH, RANSAC, information matrix); execution status |
| Evaluation | Shallow | Developed | Pose-error metrics; ground-truth versus self-reported error; worked example D (fitness and RMSE under two thresholds); data sources; published results with protocol; proposed baseline and controlled variation (point-to-plane versus point-to-point) with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (FPFH+RANSAC, TEASER++, priors, point-to-plane versus point-to-point, color, pose graphs); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/62-recalage-global-icp.py`](checks/62-recalage-global-icp.py) (17 assertions):
RANSAC samples for $w$ = 0.5, 0.1, 0.05, 0.02 (52; 6,905; 55,259; about 863,000) and the
55% success probability at the 100,000-iteration cap; small-angle error (3.8 mm at
5°, 0.15 mm at 1°, 1 m lever arm); rank 3/5/6 for one, two and three orthogonal
planes and the free directions; condition number 32.7 (m) versus $1.13\times10^7$ (mm)
versus 5.34 after normalization; fitness ceiling 0.4 at 40% overlap; RMSE 1 mm versus
28.5 mm for the same pose under two thresholds; unit change of a 0.02 threshold;
4,950 versus 100 pair evaluations for PFH and SPFH at $k=100$.

## Applied corrections

- [Reference](../../../vault/60-vision-3d/references/62-recalage-global-icp.md),
  revision 7 → 8: body rewritten and deepened as above; mistranslations fixed in the
  appendices, identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Why the initialization counts" →
  "Why the initialization matters", "Global research" → "Global search", "dial" →
  "compose", "rapprochement of the neighbors" → "neighbor matching", "**check**" →
  "Check", "covering and reserved" → "the overlap and held-out", "stresses" →
  "constraints", "isolated square" → "squared residual alone", "coins" → "parts",
  "Documentary reference" → "Documentation consulted"); tutorial links pinned from
  `docs/release` to `docs/0.19.0`; sources split into scientific and implementation
  sources; closing provenance line replaced. Front matter unchanged except
  `revision`; H1, per-card headings and appendix headings kept.
- [Cards](../../../vault/60-vision-3d/62-recalage-global-icp.md): four expected
  answers given meaning-restoring language fixes (quoted above); further
  explanations and blocking errors corrected for language (all five cards); one
  sentence added to CV-ICP-004 on Open3D's absolute, unit-bearing stopping tolerance;
  Source lines given exact sections, equations or code lines. Questions, IDs,
  objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`fitness`, `inlier_rmse`, `relative_rmse`, `FPFH` and `point-to-plane`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run; the register is a shared file). No CV-ICP proposal is
registered yet; the 2026-10-20 report contains an unregistered proposal that P-CV-ICP-01
takes up with new code evidence.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ICP-01 | CV-ICP | State what Open3D's `fitness` and `inlier_rmse` measure after point-to-plane ICP (source-normalized fraction; point-to-point RMSE over thresholded pairs) and why neither validates the pose | Evaluation family absent; the optimized cost and the reported figures differ (revives the unregistered 2026-10-20 proposal) | Evaluation; Cost and implementation | 1 card, 3 criteria | [Open3D v0.19.0 `Registration.cpp` L59–L67, L149–L154](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.cpp#L59-L67) |
| P-CV-ICP-02 | CV-ICP | Diagnose a degenerate registration from the eigenvalues of the normalized $6\times6$ point-to-plane matrix and name the free motion for a given scene (two planes, corridor) | No card trains the discriminating check for sliding; CV-ICP-002 explains the residual but not the test | Diagnosis; Mathematics, worked example B | 1 card, 3 criteria (matrix, normalization, free direction) | [Gelfand et al. 2003, §2.2 and §3.1](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf) |

## Sources

Scientific sources, opened at the passages listed:

- Besl and McKay 1992, [DOI 10.1109/34.121791](https://doi.org/10.1109/34.121791),
  read in the scanned copy hosted at
  `graphics.stanford.edu/courses/cs164-09-spring/Handouts/paper_icp.pdf` (pages
  rendered as images): abstract, §I, eqs. 21–30, §IV-A, §IV-B (eqs. 31–35), §IV-C, §V
  opening (eqs. 42–43).
- Rusinkiewicz and Levoy 2001, [PDF](https://www.cs.princeton.edu/~smr/papers/fasticp/fasticp_paper.pdf)
  (text extracted with `pdftotext`): abstract, §1, §2, §2.1, §3.1–§3.5, §4, Figs. 3 and
  13 captions.
- Low 2004, [UNC TR04-004](https://www.comp.nus.edu.sg/~lowkl/publications/lowk_point-to-plane_icp_techrep.pdf): §1–§3, eqs. 1–8.
- Gelfand et al. 2003, [PDF](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf):
  §2, §2.1, §2.2, §3.1.
- Rusu et al. 2009, [PDF](https://www.cvl.iis.u-tokyo.ac.jp/class2016/2016w/papers/6.3DdataProcessing/Rusu_FPFH_ICRA2009.pdf):
  §II-A (eq. 1), §III (eq. 4), §IV (SAC-IA).
- Yang, Shi and Carlone, TEASER, [arXiv HTML 2001.07715](https://arxiv.org/html/2001.07715):
  abstract, §I, §V-A, §V-B, §VI-D, §XI introduction, §XI-B, §XI-E with Fig. 11 caption.

Implementation sources (official code and documentation at version 0.19.0):

- [Open3D 0.19.0 ICP tutorial](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/icp_registration.html)
  and [global registration tutorial](https://www.open3d.org/docs/0.19.0/tutorial/pipelines/global_registration.html).
- [`Registration.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.cpp):
  L21–L69, L108–L157, L159–L295, L297–L346.
- [`Registration.h`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Registration.h):
  L29–L93.
- [`TransformationEstimation.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/TransformationEstimation.cpp):
  L20–L133.
- [`Feature.cpp`](https://github.com/isl-org/Open3D/blob/v0.19.0/cpp/open3d/pipelines/registration/Feature.cpp):
  L46–L229.

Failed accesses and limits:

- Chen and Medioni 1992 was not opened; point-to-plane and normal shooting are cited
  through Rusinkiewicz and Levoy and Low.
- Arun et al. 1987, Horn 1987 and Umeyama 1991 were not opened; the closed form is
  cited from Besl and McKay's equations and Open3D's call to `Eigen::umeyama`.
- Fast Global Registration (Zhou et al. 2016), colored ICP (Park et al. 2017) and Go-ICP
  are mentioned only as alternatives named by Open3D or TEASER, without claims about
  their mechanism.
- Context7 was not available in this session; official versioned code and
  documentation replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | One failure, outside this subject: `40-features-matching/references/46-harris-shi-tomasi.md` (another agent's file in progress); no error in CV-ICP files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/62-recalage-global-icp.py` | 17 checks passed |
| `git diff --check -- vault/60-vision-3d/ docs/revues/2026-11-14-reference-depth/checks/62-recalage-global-icp.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/60-vision-3d/62-recalage-global-icp.md` | 5 cards, 348–378 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 7` → `8`; H1 and the 12 per-card headings unchanged; `$$` balanced |

No Open3D call, registration or timing was executed; the proposed baseline and
variation are protocols, not results, and tutorial figures are documentation outputs.
The Mermaid diagram and tables were not rendered in Obsidian, and AnkiDroid
rendering of the corrected cards is unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export
status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-ICP revision 8, CV-ICP-001 to CV-ICP-005, language and source corrections listed
above, four expected-answer language fixes, one sentence added to CV-ICP-004, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-ICP-01, P-CV-ICP-02).
