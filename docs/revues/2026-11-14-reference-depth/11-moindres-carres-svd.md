# Review — Least squares, SVD and conditioning — 2026-11-14

## Overview

9 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 9 to revision 10. Highest severity per card before correction:
0 blocking, 2 important, 7 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The body already held about 1,730 words, concentrated in the mathematics (linear
least squares, DLT and normalization, nonlinear least squares, robust losses,
covariance) and in an executed controlled variation. This pass kept those sections,
corrected their language and one imprecise implementation claim, and developed the
contract sections that were one to three sentences long. Model-specific depth stays
in CV-HOMOGRAPHIE, CV-ZHANG, CV-EPIPOLAIRE and CV-BA, which the note links.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)v_i$ and $\|A(tv_i)\|=\lvert t\rvert\sigma_i$: confirmed (SVD derivation). Executed example ($\sigma_2\approx10^{-3}$, $\kappa_2\approx2.4\cdot10^3$, $\|\delta\hat x\|=1.0$): recomputed by the check script. Expected answer garbled the second criterion ("moving $x$ from $t\,v_i$ only changes $Ax$ from $\lvert t\rvert\sigma_i$ to norm") | Reasoning: separates fit from identifiability | 3 criteria; 368 → 378 lexical words. Garbled criterion was not gradable as written | ID, question, tags unchanged; appendix wording aligned | Important | Meaning-restoring fix of the expected answer; language fixes in explanation and blocking errors |
| CV-SVD-002 | Squared condition number, about twice as many digits lost, "even mildly ill-conditioned", fastest for tall and skinny $A$: confirmed (Eigen 3.4). `DENSE_QR` for small problems, `SPARSE_SCHUR` for thousands of cameras: confirmed (Ceres 2.2.0). Error budget $\kappa\epsilon$ versus $\kappa^2\epsilon$: confirmed by Triggs et al. §4.3 footnote 6, previously labelled only as a project decision. Expected answer said "raises the squared conditioning" and "Schur's Cholesky sparse and complement" | Comparison: solver choice under accuracy and cost | 3 criteria; 391 → 416 words | Aligned with the reference appendix | Minor | Meaning-restoring fixes of the expected answer; Triggs footnote 6 cited in the explanation and Source line |
| CV-SVD-003 | Whitening by $S^{-1/2}f$: confirmed (Ceres covariance, Introduction). Numbers 0.64, 9.64 and 4.81: recomputed. French decimal commas | Practice: makes heterogeneous residuals commensurable | 2 criteria; 400 → 397 words | Aligned | Minor | Language and decimal fixes in the explanation and blocking errors |
| CV-SVD-004 | Chum et al. theorem: confirmed (abstract and §1), but the card said "compatible with the whole plane" and "poorly determined" where the paper says consistent with all correspondences related by the homography and *wrong*: imprecise. Expected answer said "even on own inliers" and "a better cover" | Diagnosis: outliers versus near-degeneracy | 3 criteria; 405 → 403 words | "**check**" label replaced by "**Discriminating check**" | Minor | Meaning-restoring fix of the expected answer; explanation aligned with the paper's wording |
| CV-SVD-005 | DLT construction, $\|h\|=1$, last right singular vector: confirmed (Zhang App. A, not re-read; Hartley §2.2 re-read). "Minimizes the Levenberg–Marquardt reprojection error" misattributed the cost to the method | Algorithm: core linear estimator of the vault | 3 criteria; 422 → 426 words | Aligned | Minor | Language fixes in explanation and blocking errors |
| CV-SVD-006 | Row magnitudes, per-image normalization to mean distance $\sqrt2$, denormalization and non-invariance, gain of about $10^8$ on "house": confirmed (Hartley §§3, 4, 5.1, 7.3.1, re-read on pp. 583–587). Expected answer said "the inputs of $L^TL$" and "not just the rounded ones" | Reasoning: why normalization changes the estimator | 3 criteria; 397 → 393 words | Aligned | Minor | Meaning-restoring fixes of the expected answer; garbled executed-case sentence rewritten |
| CV-SVD-007 | GN and LM mechanism: confirmed (Triggs §§4.2–4.3). "Ceres presents LM as a trust region of radius $\mu$, doubled if the actual drop follows the prediction and halved otherwise": imprecise; the documentation's *schematic* trust-region loop doubles or halves $\mu$, but the 2.2.0 LM strategy multiplies the radius by $1/\max(1/3,1-(2\rho-1)^3)$ after an accepted step and divides it by 2, 4, 8… after successive rejections. Expected answer: "solves the least linear square", "approaches the Hessian", "cushions"; blocking error "confuse depreciation and robust loss" (damping) | Understanding: local refinement and its preconditions | 3 criteria; 375 → 426 words | Aligned with the reference body | Important | Sourced correction of the explanation; meaning-restoring fixes of the expected answer and blocking errors; Source line cites the 2.2.0 code |
| CV-SVD-008 | $\rho$ acts on $s=\|f\|^2$, $\rho(s,a)=a^2\rho(s/a^2)$, $a$ in residual-norm units, Huber and Cauchy forms: confirmed (Ceres 2.2.0 `LossFunction`). Expected answer said "the square block norm of residuals" and "the norm unit of residual"; explanation said "insider noise" and "nor a model just" | Practice: choosing a robust scale | 2 criteria; 371 → 371 words | Aligned | Minor | Meaning-restoring fixes of the expected answer; language fixes |
| CV-SVD-009 | Identity covariance, full column rank, pseudo-inverse, `SPARSE_QR` failure and `DENSE_SVD`: confirmed (Ceres 2.2.0 covariance). Triggs §3.1 says the asymptotic case is "much less clear" for small problems; the card said "much less safe" | Evaluation: what a covariance does and does not measure | 3 criteria; 393 → 392 words | Aligned | Minor | Language fixes of the expected answer ("of column rank full"); explanation wording aligned with Triggs |

Expected-answer changes (meaning-restoring language fixes, old → new):

- CV-SVD-001: "the disturbance is amplified … Conversely, moving $x$ from $t\,v_i$ only changes $Ax$ from $|t|\,\sigma_i$ to norm" → "the perturbation is amplified … Conversely, moving $x$ by $t\,v_i$ changes $Ax$ only by a vector of norm $|t|\,\sigma_i$".
- CV-SVD-002: "raises the squared conditioning … significant figures. QR, or SVD more accurate but slower and useful for diagnosing rank, is required as soon as $A$ is poorly conditioned, even moderately. … for high and narrow $A$ … exploit them by Schur's Cholesky sparse and complement" → "squares the condition number … significant digits. QR, or the SVD (more accurate but slower, and useful for diagnosing rank), is required as soon as $A$ is even mildly ill-conditioned. … for tall and narrow $A$ … exploit them through sparse Cholesky factorization and the Schur complement".
- CV-SVD-004: "A quasi-degeneration is seen … even on own inliers. The rejection of outliers … only a better cover" → "A near-degeneracy shows … even on clean inliers. Rejecting outliers … only better coverage".
- CV-SVD-006: "the inputs of $L^TL$" → "the entries of $L^TL$"; "not just the rounded ones" → "not just the rounding".
- CV-SVD-007: "solves the least linear square … it approaches the Hessian … cushions the step … the predicted drop in cost" → "solves the linear least-squares problem … it approximates the Hessian … damps the step … the predicted decrease in cost".
- CV-SVD-008: "$\rho$ loss applies to $s=\|f\|^2$, the square block norm of residuals … The $a$ scale has the norm unit of residual" → "the loss $\rho$ applies to $s=\|f\|^2$, the squared norm of the residual block … The scale $a$ has the unit of the residual norm".
- CV-SVD-009: "whitened residuals, of identity covariance, and a $J$ of column rank full … it assumes correct model and noise" → "whitened residuals with identity covariance and a $J$ of full column rank … it assumes a correct model and noise model".

## Reference findings

Claims of revision 9 checked against their passages:

- Eigen (least-squares page): confirmed on the 3.4.1 documentation, which carries the
  same text as the 5.0.1-dev page previously cited.
- Ceres covariance, solving and modeling passages: confirmed on the 2.2.0
  documentation sources. The readthedocs "latest" pages are the unreleased
  development version (their version history starts with "Unreleased"), and the
  "Stable (2.2)" link returned HTTP 404; the 2.2.0 `.rst` sources at the release tag
  were used as the versioned reference.
- "Ceres the formula in trust region of radius $\mu$, doubled or halved according to
  the ratio between actual drop and predicted drop": imprecise, as for CV-SVD-007;
  corrected in the body (Mathematics and Implementation contracts).
- The documented $(J^TJ)^{-1}$ entries of $\pm2.0471\cdot10^{14}$ are what a
  floating-point inversion of the rounded $J^TJ$ produces; the exact value is
  $2.0000002\cdot10^{14}$ (worked example B). The revision-9 text "about
  $\pm2.05\cdot10^{14}$" reproduced the documentation correctly; the new example
  explains the 2.4% difference.
- Hartley 1997: §4 ($d_1/d_8$, eigenvalues of $A^TA$; diagonal from $10^8$ to 1 for a
  $200\times200$ image; condition number at least about $10^4$), §5.1, §6, §7.3.1,
  §7.3.4 and §7.3.5 confirmed on a course copy of the TPAMI article.
- Chum et al. 2005: abstract, §1 and Fig. 1 caption confirmed on the CTU repository
  full text (the 2026-10-23 report had read the abstract only).
- Triggs et al. 2000: §§3.1, 3.3, 4.2, 4.3 with footnote 6, 6.1 and 9 confirmed on the
  HAL full text.
- Language defects that obscured meaning in revision 9: "point of development"
  (linearization point), "reserved observations" (held-out), "breaks down" (separates),
  "adjustment error" (fit error), "rating $S^{-1/2}f$" (scaling), "the quadratic
  shape" (quadratic form), "Ceres the formula", "cushions the step" (damps),
  "standardization" (normalization), "inlays" (inliers), "Common string" (chain),
  "prints" (draws), "brut", "Gross error" (raw), "own inliers" (clean inliers),
  "least robust squares" (robust least squares), "Paid editor version"
  (publisher's version), "annex A", "summary" (abstract), "Question of work",
  "Reference Response", "material results" (hardware), and French decimal commas.

Implementation facts added and their disagreements with the papers (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| Homography DLT normalization | Hartley §5.1: isotropic, mean distance $\sqrt2$ | OpenCV 4.13.0 `findHomography` kernel: per-axis scaling to a mean absolute deviation of 1 (fundam.cpp L111–L189); Hartley §7.3.5 found isotropic and non-isotropic scaling almost indistinguishable for $F$ |
| Linear solve of $Lh=0$ | Smallest right singular vector of $L$ | OpenCV: eigenvector of the accumulated $L^TL$ (normal matrix formed after normalization) for both the homography kernel and the eight-point algorithm |
| Final scale | Any non-zero scale | OpenCV divides by $h_{33}$ or $F_{33}$ only when it exceeds a float epsilon (L52–L57, L780–L787) |
| LM radius update | Triggs §4.2: increase $\lambda$ when prediction is poor | Ceres 2.2.0 documentation sketch: $\mu\times2$ or $\times0.5$; code: factor in $(1/2,3]$ after acceptance, division by 2, 4, 8… after rejections |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 1,728 → 5,113. About
950 tokens are tables (parameters, DLT variation, failure modes) and the
pseudocode. The mathematics of revision 9 was
kept and cleaned rather than expanded, except for the LM spectral-filter derivation and
worked example B.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (two sentences) | Developed | Three problem forms with shapes; units of rows, columns and covariance entries; outputs; pipeline role; upstream and downstream contracts |
| Intuition | Shallow (merged with procedure) | Developed | Geometric reading of $\sigma_i$ and $v_i$; worked example A (focal length and depth from one planar view, recomputed) |
| Prerequisites | Shallow (one link) | Developed | Linear-algebra prerequisites; links to CV-HOMOGRAPHIE, CV-ZHANG, CV-EPIPOLAIRE, CV-BA, CV-SE3, CV-FACTEURS |
| Assumptions | Shallow (inside the problem paragraph) | Developed | Noise model and whitening (Ceres), errors in $L$, near-linearity (Triggs §4.3), rank and gauge (Ceres; Triggs §9), degenerate configurations (Chum et al.), outliers |
| Procedure | Shallow (one sentence) | Developed | Seven-step pseudocode with the purpose of each step |
| Mathematics | Developed | Developed | Cleaned; standard deviation $1/\sigma_i$ along $v_i$; pseudo-inverse; Hartley §4 magnitude argument and §§7.3.4–7.3.5; LM as a spectral filter with constructed example C; worked example B ($J^TJ$ rounding, recomputed) |
| Parameters | Shallow (three sentences) | Developed | Table of rank tolerance, normalization, scaling, loss scale, LM settings and covariance algorithm with versioned defaults; four-step tuning approach |
| Properties | Shallow (one sentence) | Developed | Orthogonal invariance, column scaling, DLT coordinate dependence, statistical meaning, convergence, Frobenius projection limits |
| Cost and implementation | Partly developed (no versions, no code contracts) | Developed | Cost drivers with variables and error orders; DLT cost; Schur solvers; contracts of OpenCV 4.13.0 `solve`, `SVD::solveZ`, `findHomography`, eight-point, NumPy 2.2 `lstsq`, Eigen 3.4, Ceres 2.2.0; execution status |
| Evaluation | Developed | Developed | Metrics and a proposed covariance-coverage protocol; existing executed variation kept with its limits; measurement limits |
| Failure modes and diagnosis | Partly developed (prose) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow; sources not split | Developed | Six conditional choices; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/11-moindres-carres-svd.py`](checks/11-moindres-carres-svd.py) (14 checks):
the rank-1 Jacobian of a fronto-parallel target and its null direction $(f,Z)$; the
scaled condition number of about 44 and the standard deviations (80 px, 0.16 m,
correlation 0.999) for a 30° tilt; the exact ($2.0000002\cdot10^{14}$),
normal-equation ($2.0471\cdot10^{14}$) and direct ($10^{-9}$ relative) inverses of the
Ceres example with $\kappa_2(J)\approx4\cdot10^7$; the digits-at-risk reading for
$\kappa=10^6$; the LM filter factors 0.9999 and 1/101; the 2026-10-23 executed
three-row example ($\sigma_2\approx10^{-3}$, $\kappa_2\approx2.4\cdot10^3$, shift of norm
1.0); the whitening sums 0.64, 9.64 and 4.81; Hartley's $10^8$-to-1 diagonal. The
2026-10-23 Monte Carlo DLT table was not re-run.

## Applied corrections

- [Reference](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md),
  revision 9 → 10: body rewritten and deepened as above; imprecise Ceres LM radius
  claim corrected; mistranslations fixed in the body and in all three appendices
  ("Question of work" → "Working question", "Reference Response" → "Reference answer",
  "Documentary reference" → "Source consulted", "Why Invariance to Units Works" →
  "Why unit invariance works", "Explicit construction of a line … lines" → "of the
  rows … rows", "Calculate the normalization" → "Computing the normalization",
  "Neglected by Gauss-Newton" → "What Gauss–Newton neglects", "trusted region" →
  "trust region", "undoing a singular direction" → "dropping a singular direction",
  "announce" → "state", "centered and reduced coordinates" → "normalized
  coordinates", "factor filling" → "fill-in of the factors", "a spot test" → "a
  targeted test", and the shared expected-answer fixes listed above); sources split
  into scientific and implementation sources; closing provenance line replaced. Front
  matter unchanged except `revision`; H1 and the nine `### CV-SVD-00N` headings kept.
- [Cards](../../../vault/10-mathematiques-estimation/11-moindres-carres-svd.md): the
  expected-answer fixes above; CV-SVD-007 explanation corrected for the Ceres radius
  update; CV-SVD-004 explanation aligned with Chum et al.'s wording; CV-SVD-009
  explanation aligned with Triggs §3.1; CV-SVD-002 explanation and Source line cite
  Triggs footnote 6; language fixes in explanations and blocking errors of all nine
  cards ("depreciation" → "damping", "insider" → "inlier", "**check**" →
  "**Discriminating check**", decimal commas); Source lines "consult the" / "see the"
  → "consulted". Questions, IDs, objectives, families, tags and target deck unchanged.

`rg` over `vault/` found no other card repeating the doubled/halved trust-region
claim; CV-BA (54-bundle-adjustment, edited by another agent in this pass) describes
the radius qualitatively and cites the same Ceres 2.2.0 sources.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SVD-01 | CV-SVD | Explain, from the SVD of the scaled Jacobian, why LM damping leaves a weakly determined parameter combination near its initial value, and name the check that separates "converged" from "not moved" | No card connects damping to the singular spectrum; CV-SVD-007 trains the GN/LM mechanism, CV-SVD-001 the sensitivity relation, neither the stagnation diagnosis | Reasoning; Mathematics, LM as a spectral filter | 1 card, 3 criteria (filter factor $\sigma_i^2/(\sigma_i^2+\lambda)$; minimizer unchanged by damping; restart from a different initialization or inspect $v_i$) | [Triggs et al. 2000, §4.2](https://inria.hal.science/inria-00548290); [Ceres 2.2.0 nnls_solving, Levenberg–Marquardt](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_solving.rst) |

A design card on acquisitions that break the focal-length/depth ambiguity was
considered and dropped: CV-ZHANG-006 (nearly frontal views) already trains it.

## Sources

Scientific sources, opened at the passages listed:

- Hartley 1997, [course copy of the TPAMI article](https://www.cse.unr.edu/~bebis/CS485/Handouts/hartley.pdf)
  (pages read as images; text extraction failed): pp. 583–584 (§4, §4.1, §5.1, §5.2,
  §6 opening), p. 587 (§7.3, §7.3.1), p. 589 (§§7.3.4–7.3.5).
- Triggs et al. 2000, [HAL full text](https://inria.hal.science/inria-00548290/document):
  §3.1, §3.3, §4.2, §4.3 with footnote 6, §6.1, §9 opening.
- Chum, Werner and Matas 2005, [CTU repository PDF](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf):
  abstract, §1, Fig. 1 caption.
- Zhang 1998 (§3.2, Appendix A): not re-opened; the passages were quoted in the
  2026-10-23 report and are used here for the same details.

Implementation sources:

- Ceres Solver 2.2.0 at the release tag: `docs/source/nnls_covariance.rst`
  (Introduction, Gauge Invariance, Rank of the Jacobian, `Covariance::Options`),
  `docs/source/nnls_solving.rst` (L84–L125 trust region, L142–L229
  Levenberg–Marquardt, L472–L552 `DENSE_QR` and `DENSE_NORMAL_CHOLESKY`, L740–L763
  Schur solvers, L1471–L1588 and L1845 options), `docs/source/nnls_modeling.rst`
  (L958–L1064 `LossFunction`, Huber and Cauchy), `include/ceres/solver.h` L276–L295,
  `internal/ceres/levenberg_marquardt_strategy.cc` L76–L97 and L157–L170.
- OpenCV 4.13.0: `modules/core/include/opencv2/core.hpp` L1944–L1968 and
  L2818–L2828; `modules/core/include/opencv2/core/base.hpp` L133–L152;
  `modules/calib3d/src/fundam.cpp` L52–L57, L111–L189, L231–L272, L401–L434,
  L693–L790.
- [NumPy 2.2 `lstsq` documentation](https://numpy.org/doc/2.2/reference/generated/numpy.linalg.lstsq.html)
  and `numpy/linalg/_linalg.py` at tag v2.2.0 (`rcond = finfo(t).eps * max(n, m)`).
- [Eigen 3.4.1 least-squares page](https://libeigen.gitlab.io/eigen/docs-3.4/group__LeastSquares.html).

Failed accesses and limits:

- Ceres readthedocs: `/en/2.2.0/`, `/en/latest/` and the "Stable (2.2)" link returned
  HTTP 404; the `/latest/` pages are the development version. The 2.2.0 `.rst`
  sources replaced them.
- Golub and Van Loan was not accessible; flop counts for the normal equations are a
  project count, and QR versus normal equations relies on Triggs et al. and Ceres.
- Context7 was not available in this session (see the scope record); versioned
  official documentation and code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/11-moindres-carres-svd.py` | 14 checks passed |
| `git diff --check -- vault/10-mathematiques-estimation/ <check script>` | No whitespace error |
| `inventaire_cartes.py vault/10-mathematiques-estimation/11-moindres-carres-svd.md` | 9 cards, 371 to 426 words, no anomaly; absent family: design |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 9` → `10`; nine `### CV-SVD-00N` headings unchanged; `$$` and code fences balanced |

No solver, OpenCV, NumPy, Eigen or Ceres call was executed in this pass; the check
script uses the Python standard library. Tables and the pseudocode were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-SVD revision 10; CV-SVD-007 sourced correction of the Ceres trust-region update;
meaning-restoring expected-answer fixes of CV-SVD-001, 002, 004, 006, 007, 008, 009;
Agent Claude Code self-review; to republish with `paquet-anki`) and the proposal
register (P-CV-SVD-01).
