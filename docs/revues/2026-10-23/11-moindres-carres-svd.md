# Review –  Smaller squares, SVD and packaging –  2026-10-23

## Overview

Four flashcards audited, plus their reference note. No finding blocking: no claim is false. There are three important findings and one minor on the flashcards, and two minors on the reference note. Corrections are applied: reference note in revision 3, IDs and objectives unchanged. Five new flashcards and a supplement to further explanation were proposed, then accepted and drafted in revision 4: the subject goes from 4 to 9 flashcards.

The main flaw is not accuracy but alignment between question, family and purpose. Three flashcards asked a question that did not lead to the stated goal. The subject was also unaware, like all the vault, the DLT, the Hartley normalization, Gauss-Newton/Levenberg-Marquardt and the robust losses. These are everyday tools in geometry.

Self-review: Agent Claude Code (`revue-cartes`). The editorial status remains `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | Confirmed (Ceres, rank); "small singular values identify combinations" imprecise: these are the right singular vectors | Utile | Family reasoning, but the question required an unrelated diagnosis | Covers CV-SVD-004 | Important | $\delta\hat x$ relation to kernel; example executed |
| CV-SVD-002 | Confirmed to rank full column (Eigen) | Utile | Objective “choose”, question “why avoid”: only one side of the decision | Front in `AᵀA` Unicode; Eigen address redirected (301) | Important | Decision Question; Hollow BA Case (Ceres) |
| CV-SVD-003 | Confirmed (Ceres: $S^{-1/2}f$); "consistent with units" inaccurate | Utile | Net Core | Agreement reference note | Minor | Formulation "without dimension" |
| CV-SVD-004 | Diagnosis deduced, not contradicted | Utile | Diagnostic family without discriminating test | Covers CV-SVD-001 and CV-HOMOGRAPHIE-006 | Important | Discriminant controls; case DEGENSAC |

### Reference note

- Minor (FR-036): Numerical properties were only supported by implementation documentation (Eigen, Ceres). Hartley 1997 and Chum et al. 2005 are added. A numerical analysis manual, such as Golub and Van Loan, could not be accessed.
- Minor: the relationship of sensitivity and the choice of solver in big sparse problem was missing to support the corrected flashcards.

### Length

Corrected answers count 169 to 184 words according to inventory, against 139 at most elsewhere in the vault. The core remains at three notable points; most of the surplus comes from the formulas and the further explanation. Measure the actual load under revision before shortening further.

## Corrections applied

- `vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md`, revision 3 : relation $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)v_i$ and dependence of $\kappa_2$ units; arbitration QR/SVD/normal equations according to Eigen and Ceres, of which `DENSE_QR`, `DENSE_NORMAL_CHOLESKY` and Schur solvers; executed sensitivity calculation; residual outliers and quasi-degeneration tests; dominant plane theorem; sources Eigen (new address), Ceres Solving, Chum 2005, Hartley 1997.
- `vault/10-mathematiques-estimation/11-moindres-carres-svd.md` :
  - CV-SVD-001: question and kernel centered on the sensitivity relationship;
  - CV-SVD-002: two-sided decision question;
  - CV-SVD-003: "without dimension";
  - CV-SVD-004: Discriminant checks and published cases.
- `vault/01-Parcours/Suivi-pilote.md` correction log: one line per corrected flashcard.

No flashcard from another theme repeated a corrected statement (`grep` on normal equations, `A^TA`, `J^TJ` and conditioning).

## Enrichments accepted and applied

The learner has accepted all the proposals below the 2026-10-23. They are written in revision 4 of the reference note:

- CV-SVD-005 to 009 added, with `Provenance : agent`
- Example encrypted m/mm in CV-SVD-003;
- Triggs et al. 2000, §4.3, added as scientific source of CV-SVD-002;
- sections of the reference note: homogeneous system, DLT and normalization; nonlinear least squares and robust losses; parameter uncertainty; gross/normalized controlled variation; usual chain RANSAC → DLT → LM.

Current state totals change from 233 to 238 flashcards: regenerated catalog, `docs/vault-layout.md`, `Guide-Anki.md`, contract Obsidian – Anki and follow-up "Lot" header. Previous dated results are not modified.

For the verification of the news flashcards, Triggs, McLauchlan, Hartley and Fitzgibbon (2000) have been read in full text since HAL:

- §3.1: dispersion approaches covariance only asymptotically, which is less safe for small problems;
- §3.3: robustness on the weighted residual, and model error not correctable by cleaning;
- §4.2: damping and no gradient;
- §4.3: Gauss-Newton, and QR up to twice as slow as normal equations but much less sensitive to poor conditioning.

Ceres does not present $(J^TJ)^{-1}$ as an approximation; the asymptotic nuance comes from Triggs et al.

Length: The nine answers count between 133 and 223 words depending on the inventory. CV-SVD-006 is the longest; its core has three points. Measure in real revision before shortening.

Table of proposals as submitted:

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| CV-SVD-005: DLT, solution of $Lh=0$ under $\|h\|=1$ by the right singular vector of $\sigma_{\min}$, two equations by correspondence, then geometric refinement | No flashcard of the vault on the DLT, yet the basis of the homography, $F$, triangulation and Zhang | algorithm | 1 flashcard; core at 3 points | Zhang 1998, annexe A ; Hartley 1997, §2 |
| CV-SVD-006: Hartley normalization and why it changes the least squares solution, not just the rounded ones | Normalization only cited, without source, in CV-HOMOGRAPHIE-002 | reasoning | 1 flashcard; core at 3 points | Hartley 1997, §§3 – 5 and 7.3.1; Zhang 1998, annex A; executed calculation of the project |
| CV-SVD-007: Gauss-Newton and Levenberg-Marquardt, linear initialization and refinement | No non-linear solver in the vault, while calibration, refined PnP and BA depend on it | understanding | 1 flashcard; core at 3 points | Ceres, Solving, Levenberg-Marquardt ; Zhang 1998, §3.2 |
| CV-SVD-008: robust loss applied to the whitened residual, $a$ scale and complementarity with RANSAC | "Strong estimate" announced by the theme index, no flashcard on Huber or Cauchy | practice | 1 flashcard; core at 3 points | Ceres, Modeling, LossFunction ; Ceres, Covariance, Introduction |
| CV-SVD-009: covariance of $(J^TJ)^{-1}$ parameters, conditions and gauge | "Uncertainty" announced by the index; proposal of the 2026-10-18 remained pending | evaluation | 1 flashcard; core at 3 points | Ceres, Covariance Estimation : Introduction, Gauge Invariance, Rank of the Jacobian |
| CV-SVD-003: example encrypted m → mm | flashcard fair but abstract | further explanation alone | No new reminders | Calculation of the project |
| reference note: DLT sections and normalization, non-linear, robust losses, covariance; gross/normalized controlled variation (FR-033) | Headings absent | Mathematics, Evaluation, Sources | without flashcard | Hartley 1997 ; Zhang 1998 ; Ceres |

Calculations already executed for these proposals, excluding repository, Python 3.10.13 and NumPy 2.2.6, built cases and not field measurements:

- DLT of homography, 200 prints by configuration, noise 0,5 px:
  - 50 points on a 1920×1080 image: $\sigma_1/\sigma_8$ median $8{,}3\cdot10^6$ raw versus 4,1 normalized; median error on the entire image 0,22 px versus 0,20 px;
  - 20 points concentrated in a square of 200 px in corner: $1{,}4\cdot10^8$ against 3,5; median error 1013 px against 28 px. Normalization counts especially when the points are far from the origin relative to their extent; it does not remove the extrapolation error.
- Whitening: $r_{px}=0{,}8$, $\sigma_{px}=0{,}5$, $r=3$ mm, $\sigma=2$ mm. Gross sum 0,64 in meters, 9,64 in millimeters; whitened sum 4,81 in both cases.

## Sources

- [Ceres, Covariance Estimation (consulted on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html): hypothesis of identity covariance and scaling $S^{-1/2}f$, full rank, pseudo-inverse, gauge, example of Jacobian almost singular under `min_reciprocal_condition_number`.
- [Ceres, Solving Non-linear Least Squares (accessed 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html): Levenberg-Marquardt as regularized version of Gauss-Newton, `DENSE_QR`, `DENSE_NORMAL_CHOLESKY`, Schur solvers and their scales.
- [Ceres, Modeling Non-linear Least Squares (accessed on 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html): `LossFunction`, conditions on $\rho$, Huber, SoftLOne, Cauchy, scale $a$.
- [Eigen 5.0.1-dev, Solving linear least squares systems](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html): square packaging, loss of about twice as many digits, speed for $A$ high and narrow. The old eigen.tuxfamily.org address returns a 301 redirect to this page.
- [Zhang 1998, MSR-TR-98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), §3.2 and Appendix A: DLT per singular vector, mispackaging, standardization, Levenberg-Marquardt refinement.
- [Hartley 1997, IEEE TPAMI 19(6)](https://doi.org/10.1109/34.601246), §§3 – 5 and 7.3: denormalization, non-invariance of the solution, ratio $d_1/d_8$, medium-distance isotropic normalization $\sqrt2$, packaging gain of about $10^8$ on the "house" pair. Version of the paid editor; passages read on a copy hosted by the University of Crete.
- [Triggs, McLauchlan, Hartley and Fitzgibbon 2000, HAL inria-00548290](https://inria.hal.science/inria-00548290), §§3.1, 3.3, 4.2 and 4.3, full text.
- [Chum, Werner and Matas 2005](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf): abstract accessed via ML Anthology; full text of CVUT repository not read. The theorem cited is that of the summary.

## Checks and limitations

- After corrections: `check_vault.py` OK, 125 Markdown, 52 reference notes, 233 flashcards; 34 tests passed; up-to-date catalog.
- After additions: `check_vault.py` OK, 125 Markdown, 52 reference notes, 238 flashcards; 34 passed tests; `sync_catalog.py` regenerated and then `--check` without expired document on 18.
- Inventory compared to the initial state: only CV-SVD-005 to 009 appear; no ID disappeared, no identity Anki modified. The flashcards of the subject does not yet have an identity Anki.

Context7 is not available in this session: official documents consulted directly. Not verified: real export Anki, rendering Obsidian and AnkiDroid, control of the learner, independent scientific validation.
