# Review — Bundle adjustment and the Schur complement — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for bundle adjustment. Initialization stays in
[CV-EPIPOLAIRE](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md)
and the factor-graph, pose-graph and incremental-smoothing view in
[CV-FACTEURS](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md);
this note links to them instead of restating them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BA-001 | BA jointly refines structure and viewing parameters (pose and/or calibration): confirmed by Triggs et al. §1 and §2.1; bipartite camera–point structure confirmed by §5. Expected answer "possibly intrinsic, from reprojections" left a dangling adjective; "a weak reprojection" meant a *low* reprojection error | Understanding: unknowns and information content of BA versus a pose graph | 2 expected criteria; 361 → 374 lexical words | ID, question, tags unchanged; appendix wording aligned | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |
| CV-BA-002 | Elimination of the block-diagonal point block and back-substitution: confirmed by Agarwal et al. §2.2 eqs. 5–8 and Ceres 2.2.0 `nnls_solving.rst` L669–L767 ($S_{ij}\neq0$ iff images $i$, $j$ share a point). "Camera and dot increments", "complement of Schur", "diagonal block per point", "its substitution in the first … product" obscured the derivation | Reasoning: why elimination is exact and how it creates camera coupling | 1 expected criterion with 2 parts; 403 → 399 lexical words | Notation aligned with the reference ($B$, $E$, $C$, $v$, $w$) | Minor | Language fixes in explanation and derivation; Source line given exact passages |
| CV-BA-003 | 7-dimensional similarity gauge for Euclidean reconstruction: confirmed by Triggs et al. §9.1; Ceres covariance documentation, Gauge Invariance (L67–L74). Blocking error "Automatically assign multiplicity to a solver failure" was unintelligible; "digital prior" for a numerical prior; "homogeneous division" for perspective division | Diagnosis: separate a gauge freedom from a solver failure and a convention from a measurement | 2 expected criteria; 375 → 380 lexical words | Consistent with the reference Mathematics and Assumptions sections | Minor | Language fixes; blocking error made intelligible; Source line given exact sections |
| CV-BA-004 | Over-general models "tend to be noisy and unstable", over-special ones biased: confirmed by Triggs et al. §10.5; self-calibration needs varied views (§11); COLMAP keeps the principal point fixed as ill-posed (Schönberger and Frahm §4.4). Expected answer "Additional settings may over-adjust" mistranslated *paramètres* and *sur-ajuster*; "release a group of parameters at once" inverted "one group at a time"; "resolution pitch" and "physical priority" for step size and prior | Evaluation: refuse a cost decrease as evidence of a better camera model | 2 expected criteria; 342 → 352 lexical words | Consistent with reference worked example E and the nested-model test | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |

Expected-answer changes (meaning-restoring language fixes):

- CV-BA-001: "The BA optimizes poses and points, possibly intrinsic, from reprojections;
  a pose graph is based on constraints between poses." → "The BA optimizes poses and
  points, and possibly intrinsic parameters, from reprojection errors; a pose graph is
  based on constraints between poses."
- CV-BA-004: "Additional settings may over-adjust an uninformative dataset or be
  correlated." → "Additional parameters may overfit an uninformative dataset or be
  correlated with each other."

The objective line of CV-BA-004 ("check a model too free") and of CV-BA-002 ("Explain
the elimination of Schur") are awkward but are protected fields; proposed wording for a
future learner-approved edit: "Reject an over-free camera model" and "Explain Schur
elimination".

## Reference findings

Claims of revision 7 checked against their passages:

- Cost $\sum\rho(r^\top\Sigma^{-1}r)$ with robust $\rho$ on the squared whitened norm:
  confirmed (Triggs et al. eqs. 2–3; Ceres `loss_function.h` uses $\tfrac12\rho(s)$).
- Reduced camera system and back-substitution: confirmed (Triggs et al. eq. 20;
  Agarwal et al. eqs. 5–8).
- Inverses denote algebra, implementations factorize: confirmed (Triggs et al. §4.5).
- No scientific error found. The body was shallow (one to three sentences per
  section) and contained mistranslations: "Landmarks" capitalized, "2D – 3D
  combinations" for correspondences, "Poor catch" for poor capture, "Attach gauge" for
  fix the gauge, "reserved views" for held-out views, "Question of work",
  "Reference Response", "Documentary reference", "Complete objective to be explained",
  "dot" for point, "digital prior", "resolution pitch", "physical priority",
  "Unleashing", "catches".

New claims verified for revision 8 (main ones):

- Definition, parametrization of points (homogeneous for distant points) and
  rotations (local perturbations): Triggs et al. §1, §2.1, §2.2.
- Locality of blunders and limits of data cleaning under a wrong model (§3.3);
  robustified Gauss–Newton with rank-one curvature reduction (eq. 10, §4.3);
  quadratic convergence in 5–6 iterations (§4.1); first-order iteration counts
  16/350/3,700 and Fig. 5 (11 Gauss–Newton steps versus 200 resection–intersection
  steps) (§7); 7-dimensional similarity and 15-dimensional projective gauge groups
  (§9.1); gauge-dependent covariances (§1, §9); bias of fitted residuals of order
  $1/(n_z-n_x)$ (§10.1); redundancy numbers (§10.4); nested-model $\chi^2_k$ test and
  "over-special … biased, over-general … noisy and unstable" (§10.5); four views per
  point, 30–45° cone for self-calibration (§11); "Kalman filtering is only the first
  half-iteration", realistic inlier dispersion (§12).
- Agarwal et al.: LM with $D=\sqrt{\operatorname{diag}(J^\top J)}$ (eq. 3); block sizes
  $c=6$–9, $s=3$; $O(p^2)$ memory and $O(p^3)$ time for dense $S$; implicit $Sx$ (eq. 12);
  Wright–Holt convergence of truncated LM; $\kappa(S)\le\kappa(H)$; 9-parameter camera;
  scaling because parameters differ by up to 20 orders of magnitude in sensitivity;
  hardware and results; recommendation of dense Cholesky for small to medium problems
  (§1, §2.1, §2.2, §3, §4, §5.1–§5.3).
- Schönberger and Frahm §4.4: local BA after each registration, global BA after growth
  by a percentage, Cauchy loss, sparse direct solver up to a few hundred cameras and
  PCG beyond, fixed principal point, filtering, minimum triangulation angle,
  re-triangulation and iterative refinement.
- Ceres 2.2.0: see Sources.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 344 → 4,307. About a
quarter of the tokens are tables, the pseudocode and the Mermaid diagram. The length
comes from the parameter table, five worked examples and the solver contracts;
pose graphs, initialization and factor graphs are linked, not restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Definition (Triggs §1); camera, point and observation blocks with frames, units and covariances; outputs; BAL sign and centre conventions; pipeline roles (COLMAP local/global BA, SLAM, calibration) |
| Intuition | Shallow (merged with procedure) | Developed | Spring analogy; constructed two-view illustration (13.3 px); bipartite elimination; Mermaid diagram of one LM–Schur iteration |
| Prerequisites | Developed (3 links) | Developed | Added CV-SE3, CV-ZHANG, CV-FISHEYE, CV-CAPTEURS with the reason for each |
| Assumptions | Shallow (one sentence) | Developed | Associations, noise model, projection model, basin of convergence; 7/15-dimensional gauge; worked example A (point counts); single-view points, parallax, pure rotation, distant points, self-calibration geometry, reliability |
| Procedure | Shallow | Developed | Pseudocode of LM with Schur elimination and outer filtering loop; purpose of whitening, local parametrization, damping, elimination and iterative refinement |
| Mathematics | Shallow (one equation) | Developed | Projection with radial model; cost and Ceres convention; Gauss–Newton and LM; robustified curvature (Triggs eq. 10); block system and Schur complement; worked example B (sizes and costs) |
| Parameters | Shallow | Developed | Nine-row table with Ceres 2.2.0 defaults and source values; worked examples D (Huber/Cauchy weights) and E ($k_3$ identifiability); five-step tuning approach |
| Properties | Shallow (merged) | Developed | Asymptotic ML optimality and its limits; local convergence; gauge-dependent covariance; exactness of elimination; inexact-step convergence and $\kappa(S)\le\kappa(H)$; optimistic residuals; limits of robustness |
| Cost and implementation | Shallow | Developed | Cost drivers in $p$, $q$, $m$, track length; reported results with hardware; Ceres 2.2.0 contracts (BAL camera, Schur solvers, ordering, covariance, gradient check); execution status |
| Evaluation | Shallow (one sentence) | Developed | Training versus held-out residuals; $\chi^2$ and nested-model tests; alignment choice; solver time-to-tolerance protocol; baseline and robust-loss controlled variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (dense, sparse, iterative Schur; pose graph; sliding window and filtering; resection–intersection); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/54-bundle-adjustment.py`](checks/54-bundle-adjustment.py) (15 assertions):
minimum point counts for two and three calibrated views (5 and 4); system sizes for
$p=100$, $c=9$, $q=50{,}000$, track length 6 ($n=150{,}900$; 182 GB versus 6.48 MB;
$1.15\times10^{15}$ versus $2.43\times10^8$ flops; 15 camera pairs per point); exact
invariance of pixels under a 7-parameter similarity; Huber and Cauchy weights for
$a=2$ (1/0.8 at $1\sigma$, 0.2/0.0385 at $10\sigma$, influence 2 and 0.385); $k_3$
shifts of 0.0013, 0.78 and 21 px at $\bar r=0.2$, 0.5, 0.8; the two-view depth
illustration (13.3 px); Triggs's first-order iteration counts; the $\chi^2_1$ 5%
threshold 3.84.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/54-bundle-adjustment.md),
  revision 7 → 8: body rewritten and deepened as above; mistranslations fixed in the
  appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "Documentary reference for this pass" → "Source consulted for
  this pass", "Complete objective to be explained" → "Full objective", and the card
  text fixes below applied identically); sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1, per-card headings and `## Sources and flashcards` kept.
- [Cards](../../../vault/50-calibration-geometrie/54-bundle-adjustment.md): the two
  expected-answer fixes quoted above. Further explanations and blocking errors:
  "A weak reprojection can still hide a gauge or bias" → "A low reprojection error can
  still hide a gauge freedom or a bias"; "Camera and dot increments" → "Camera and point
  increments"; "Algebraically solve the block of points and then replace it … gives the
  complement of Schur" → "Solving the point block algebraically and substituting it …
  gives the Schur complement"; "can be paired" → "become coupled"; "its substitution in
  the first … product" → "substituting it into the first yields"; "$C$ is diagonal block
  per point" → "$C$ is block diagonal, with one block per point"; "the homogeneous
  division" → "the perspective division"; "digital prior" → "numerical prior";
  "announce its uncertainty" → "report its uncertainty"; "Automatically assign
  multiplicity to a solver failure" → "Automatically attributing the multiplicity of
  solutions to a solver failure"; "release a group of parameters at once" → "free one
  group of parameters at a time"; "reserved views including edges" → "held-out views,
  including image borders"; "Unleashing" → "Freeing"; "The damping of LM limits the
  current resolution pitch: it is not automatically a physical priority" →
  "Levenberg–Marquardt damping limits the current step size: it is not a physical
  prior"; "A reserved validation must keep poses and really different areas, not just
  neighboring points of the same catches" → "A held-out validation set must contain
  genuinely different poses and image regions, not just neighboring points from the
  same captures". Source lines now cite Triggs et al. §§1, 2.1, 5, 9.1, 10.5, 11,
  Agarwal et al. §2.2, Schönberger and Frahm §4.4 and Ceres 2.2.0 files with lines.
  Questions, IDs, objectives, families, tags and target deck unchanged.

No scientific correction was needed, so no other vault file had to be checked for a
repeated wrong claim; `rg` over `vault/` for "Schur", "gauge" and "7-dimensional"
found no contradiction with the revised note.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-BA-01 | CV-BA | Given whitened residuals of 1σ and 10σ and a loss scale $a$, compute Huber and Cauchy weights and state when a robust loss cannot protect BA (structured outliers, wrong model) | Robust losses are central to every BA but no card tests their mechanism or limits | Reasoning; Parameters, worked example D | 1 card, 3 criteria (weights; bounded versus redescending influence; locality assumption) | [Triggs et al. §3.3 and eq. 10](https://hal.science/inria-00548290/document); [Ceres 2.2.0 `loss_function.h` L91–L210](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/include/ceres/loss_function.h) |
| P-CV-BA-02 | CV-BA | Choose `DENSE_SCHUR`, `SPARSE_SCHUR` or `ITERATIVE_SCHUR` from the camera count and the visibility structure of $S$, and predict the coupling created by long tracks | Solver choice is untested; refines the unregistered 2026-10-20 idea "Choose elimination order and measure fill-in" (practice) | Design; Cost and implementation | 1 card, 3 criteria | [Agarwal et al. §2.2 and §5.3](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/10/Agarwal-ECCV10.pdf); [Ceres 2.2.0 `nnls_solving.rst` L669–L821](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_solving.rst) |

## Sources

Scientific sources, opened at the passages listed:

- Triggs, McLauchlan, Hartley and Fitzgibbon, Bundle Adjustment — A Modern Synthesis,
  [HAL PDF](https://hal.science/inria-00548290/document) (text extracted with
  `pdftotext`): §1, §2.1, §2.2, §3 introduction, §3.1–§3.3, §4.1–§4.5, §5 (Fig. 3),
  §6.1, §7 introduction and Fig. 5, §9 and §9.1, §10 introduction, §10.1, §10.4,
  §10.5, §11, §12.
- Agarwal, Snavely, Seitz and Szeliski, Bundle Adjustment in the Large,
  [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/10/Agarwal-ECCV10.pdf):
  abstract, §1, §2.1, §2.2, §3, §4, §5.1–§5.3.
- Schönberger and Frahm, Structure-from-Motion Revisited,
  [CVF open access PDF](https://openaccess.thecvf.com/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf):
  §4.4.

Implementation sources (official code and documentation sources at tag 2.2.0, the
latest Ceres tag):

- [`docs/source/nnls_solving.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_solving.rst): L142–L229, L669–L821, L973–L1032, L1070–L1156.
- [`include/ceres/solver.h`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/include/ceres/solver.h): L232–L333, L595–L631, L736–L749.
- [`include/ceres/loss_function.h`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/include/ceres/loss_function.h): L64–L73, L91–L112, L137–L170, L203–L210.
- [`include/ceres/problem.h`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/include/ceres/problem.h): L195–L199.
- [`docs/source/nnls_covariance.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_covariance.rst): L38–L39, L60–L110, L151–L188.
- [`examples/snavely_reprojection_error.h`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/examples/snavely_reprojection_error.h): L49–L100, L106–L114.

Failed accesses and limits:

- `lear.inrialpes.fr` returned an HTML page instead of the Triggs PDF; the HAL copy was
  used. `grail.cs.washington.edu/projects/bal/bal.pdf` was unavailable; the Microsoft
  Research copy was used.
- `ceres-solver.org` returned HTTP 502 and `ceres-solver.readthedocs.io/en/2.2.0/`
  HTTP 404; the versioned `.rst` sources at tag 2.2.0 were read instead. The
  `latest` rendered pages remain cited as consulted in earlier passes.
- Context7 was not available in this session.
- Not re-verified: the Kanatani–Morris gauge reference cited by Ceres, and the
  Wright–Holt convergence proof (cited through Agarwal et al. §3).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/54-bundle-adjustment.py` | 15 checks passed |
| `git diff --check -- vault/50-calibration-geometrie/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/54-bundle-adjustment.md` | 4 cards, 374, 399, 380 and 352 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 0 errors: card headings, objectives, IDs, questions, tags, `START`/`CV-Pilote`/`END`, target deck identical; 2 expected answers changed as recorded; front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged |
| Local link and anchor check over `vault/50-calibration-geometrie` | 110 local links, 0 errors |

No solver, Ceres program or reconstruction was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-BA revision 8, CV-BA-001 to CV-BA-004, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-BA-01, P-CV-BA-02).
