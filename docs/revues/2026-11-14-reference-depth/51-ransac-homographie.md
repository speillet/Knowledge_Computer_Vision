# Review — RANSAC for homography estimation — 2026-11-14

## Overview

7 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 0 important, 7 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for the planar homography and its robust estimation.
It now separates the model (validity, DLT, degeneracy, parallax) from the estimator
(sampling budget, consensus, refinement), documents the OpenCV 4.13 path line by line, and
quantifies the effects that the cards reason about. Epipolar geometry and PnP stay in
CV-EPIPOLAIRE; learned matching in CV-MATCH-APPRIS.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Plane or pure rotation, parallax under translation: confirmed (OpenCV tutorial, Basic theory and Demo 5); plane-induced $H\sim K'(R+tn^\top/d)K^{-1}$ recomputed (check 6), sign convention differs from the tutorial's $R-tn^\top/d$, as the card warns. "Bottom" for *background*, "plan" for *plane*, "**check model**", "more prints RANSAC" | Comparison: choose the geometric model before tuning the estimator | 2 expected criteria; 402 → 397 lexical words | ID, question, tags unchanged; aligned with the reference appendix | Minor | Language fixes; Source line moved to the 4.13.0 tutorial source |
| CV-HOMOGRAPHIE-002 | Rank 8 for four points in general position, rank drop for collinear triples: recomputed (check 9); OpenCV rejects collinear samples (fundam.cpp L74–L109). Expected answer "minimum stress" mistranslated *minimum constraint*; "enlarge the core" for *null space*, "homographs", "digital conditioning" | Reasoning: degrees of freedom versus information | 2 expected criteria; 372 → 373 lexical words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given code lines |
| CV-HOMOGRAPHIE-003 | Sample, fit, score all pairs, refit on inliers: confirmed (Fischler and Bolles §II; OpenCV refits, refines with LM and recomputes the mask, fundam.cpp L415–L452). "The draw protects certain outliers" inverted the meaning (small samples keep outliers *out*); pseudocode collapsed on one line; "Absentee treatment", "lack of prints" | Algorithm: reconstruct a robust iteration | 2 expected criteria; 405 → 410 lexical words | Pseudocode restored identically in card and appendix | Minor | Expected answer wording ("undegenerate minimum set" → "non-degenerate minimal set"); language fixes; Source line given exact passages |
| CV-HOMOGRAPHIE-004 | $N=72$ for $w=0.5$, $p=0.99$; 9 for $w=0.8$; 567 for $w=0.3$: recomputed (check 1); formula in Fischler and Bolles §II.B. Expected answer used French decimal commas (0,99; 0,5) and "ask"; blocking error spoke of a *pose* for a homography. OpenCV rounds (71) and caps at `maxIters` (checks 2–3): missing implementation condition | Reasoning: meaning of a nominal confidence | 2 expected criteria; 429 → 461 lexical words. The question front itself contains "$w=0,5$" (see Proposals) | Aligned with the reference worked example A | Minor | Meaning-restoring fixes of the expected answer and blocking errors; one sentence on OpenCV's rounding and cap; Source line given §II.B and code lines |
| CV-HOMOGRAPHIE-005 | Residual in destination pixels, threshold rescaling under resize: confirmed (calib3d.hpp L794–L797; ptsetreg.cpp L86–L100); anisotropic gate and covariance propagation consistent (check 12). "Half-uniform resize", "resetting the detection", "Local spread of uncertainty" | Practice: units of a residual threshold | 2 expected criteria; 413 → 414 lexical words | Aligned with the appendix | Minor | Language fixes; Source line given code lines |
| CV-HOMOGRAPHIE-006 | Local consensus versus extrapolation: supported by the projective-term sensitivity (check 11: 0.1 px at 100 px versus 35.4 px at 1900 px). Expected answer "reserved points" for *held-out*; "check for lack of alignment" (meaning: points not nearly collinear); "Experience built" | Diagnosis: consensus quality versus registration quality | 2 expected criteria; 379 → 384 lexical words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |
| CV-HOMOGRAPHIE-007 | Parallax $fB/Z$, 40 px at 2 m and 8 px at 10 m, 32 px transfer error between them: recomputed (check 7). "Bottom" for *background*, "multi-plane assembly", "call 'inliers' points poorly explained" | Diagnosis: model incompatibility before threshold tuning | 2 expected criteria; 391 → 393 lexical words | Aligned with the appendix | Minor | Language fixes; Source line moved to the 4.13.0 tutorial source |

Expected-answer changes (meaning-restoring language fixes):

- CV-HOMOGRAPHIE-002: "Four pairs provide the minimum stress only in the general
  position." → "Four pairs provide the minimum number of constraints only in general
  position."
- CV-HOMOGRAPHIE-003: "draw an undegenerate minimum set" → "draw a non-degenerate
  minimal set".
- CV-HOMOGRAPHIE-004: "Under the independent model, ask $1-(1-w^4)^N\ge0,99$ gives
  $N=\lceil\log(1-0,99)/\log(1-0,5^4)\rceil=72$" → "Under the independent model,
  requiring $1-(1-w^4)^N\ge0.99$ gives $N=\lceil\log(1-0.99)/\log(1-0.5^4)\rceil=72$";
  blocking error "99% probability that the pose is correct" → "99% probability that the
  estimated homography is correct".
- CV-HOMOGRAPHIE-006: "error on reserved points" → "error on held-out points".

## Reference findings

Claims of revision 8 checked:

- Homography valid for a plane or a pure rotation, parallax otherwise: confirmed (tutorial,
  Basic theory, Demo 3 and Demo 5).
- Budget formula and the values 72 (w = 0.5) and 9 (w = 0.8): confirmed (Fischler and
  Bolles §II.B; check 1). "Results executed in `examples/pilot_math.py`": the function
  `ransac_trials` exists there; this pass recomputed the values in its own check script.
- Inlier boundary ("specify the inequality"): OpenCV uses $e_i^2\le t^2$ (inlier at equality)
  and documents $e_i>t$ as outlier.
- Normalization improves the linear computation without repairing degeneracy: consistent
  with the OpenCV kernel, which normalizes each axis by its mean absolute deviation; the
  textbook isotropic scheme (Hartley 1997) could not be read and is not described.
- No scientific error in revision 8. Language defects: French decimal commas
  ("$w=0,5$", "3,0"), "dots" for points, "plan" for plane, "bottom" for background, "prints"
  for draws, "Question of work", "Reference Response", "Tutoriel officiel", a pseudocode
  block collapsed on one line, and no closing provenance line.

New claims verified for revision 9 (main ones):

- OpenCV 4.13 `findHomography`: signature and defaults (threshold 3, `maxIters` 2000,
  confidence 0.995), methods 0, RANSAC, LMEDS, RHO and `USAC_*`; LMedS needs more than 50%
  inliers; RANSAC and RHO "can handle practically any ratio of outliers"; $h_{33}=1$; empty
  result on failure (calib3d.hpp L551–L560, L782–L853).
- Source path: at least four points; threshold $\le0$ replaced by 3; direct DLT for four
  points or method 0; RANSAC registrator with sample checks (collinearity and triangle
  orientation); adaptive iteration count with rounding and cap; fixed RNG seed; refit, 10 LM
  iterations, mask recomputed on all points (fundam.cpp, ptsetreg.cpp).
- Fischler and Bolles: $E(k)=w^{-n}$, $SD(k)$, the 35.7-draw example, the threshold $t$ and
  the "better than 95 percent" argument for $t-n=5$ (§II.B–§II.C).
- MAGSAC and MAGSAC++ abstracts: threshold-free scoring by marginalization over noise
  scales.

Paper–implementation differences (FR-036):

| Aspect | Paper or textbook formula | OpenCV 4.13.0 |
| --- | --- | --- |
| Iteration count | $\lceil\log(1-p)/\log(1-w^m)\rceil$ (Fischler and Bolles give $k$ unrounded) | `cvRound` of the same ratio, updated from the best inlier ratio, capped at `maxIters` (ptsetreg.cpp L55–L76, L229–L234) |
| Sample validity | Non-degenerate minimal set | Collinearity in either image and triangle-orientation consistency (fundam.cpp L74–L109) |
| Final model | Smoothing on the consensus set (§II) | DLT refit, 10 Levenberg–Marquardt iterations, mask recomputed with the refined model (L415–L452) |
| MAGSAC | No user-defined noise scale (abstract) | `USAC_MAGSAC` still receives `ransacReprojThreshold` (fundam.cpp L363–L365) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 818 → 3,684.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task; OpenCV data contract (types, order, output scaling, empty result, units); validity cases from the tutorial; pipeline roles upstream and downstream |
| Intuition | Shallow | Developed | Why least squares fails; hypothesize-and-verify; model versus estimator; constructed poster illustration; Mermaid diagram of the OpenCV path |
| Prerequisites | Shallow | Developed | Links to CV-SVD, CV-SE3, SIFT, ORB, CV-MATCHING, CV-EPIPOLAIRE, CV-ZHANG by mechanism |
| Assumptions | Shallow | Developed | Plane-induced derivation with sign conventions; one-sided error model; minimal-sample validity including the orientation test; structured outliers; spatial support; degenerate cases |
| Procedure | Shallow (collapsed pseudocode) | Developed | Multi-line pseudocode matching OpenCV 4.13 with the purpose of each step |
| Mathematics | Developed (model, residual, budget) | Developed | DLT system and normalization; refinement objective; $E(k)$, $SD(k)$ and finite-population probability; parallax formula; threshold units; worked examples A–E |
| Parameters | Shallow | Developed | Parameter table with 4.13 defaults and interactions; four-step tuning approach |
| Properties | Shallow | Developed | Nominal guarantee and its limits; consensus versus truth; reproducibility; robustness range; conditioning; external model validity |
| Cost and implementation | Shallow | Developed | Cost drivers; OpenCV 4.13 contracts with line numbers; illustrative call with failure handling |
| Evaluation | Shallow | Developed | Metrics ranked by informativeness; baseline and second-plane variation with a threshold confound; limits |
| Failure modes and diagnosis | Three-column table | Developed | Seven-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Short paragraph | Developed | Affine, epipolar or PnP, MAGSAC++, symmetric error, ECC, local warps; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/51-ransac-homographie.py`](checks/51-ransac-homographie.py) (12 checks): budgets
72, 9, 567 and 52,981; OpenCV's 71 and 82 (against 83) and its cap of 2000; Fischler and
Bolles' $E(k)=16$, $SD(k)\approx15.5$ and 35.7; the finite-population probability 0.0587 and
77 draws; the plane-induced homography, the 32 px parallax error and the rotation-only
case; DLT ranks 8 and 7; the triangle-orientation test; the 0.1 px versus 35.4 px
extrapolation; threshold rescaling.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md),
  revision 8 → 9: body rewritten and deepened as above; appendices corrected identically
  to the card text ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "bottom" → "background", "**check model**" → "**Model check**",
  "Regaining dependence on the plan" → "Recovering the dependence on the plane", "Link to
  DLT Rank" → "Link to the DLT rank", "enlarge the core" → "enlarge the null space",
  "homographs" → "homographies", pseudocode restored on several lines, "Absentee treatment
  is a normal exit" → "Returning no model is a normal outcome", "Correcting the
  interpretation of a finished print" → "Exact probability for a finite set", "guided
  prints" → "guided sampling", "all-in" → "all-inlier", "warranty" → "guarantee", "Local
  spread of uncertainty" → "Local propagation of uncertainty", "multi-plane assembly" →
  "multi-plane composition", "Documentary reference" → "Documentation consulted"). The
  `[tutorial]` and `[api]` link definitions now point to the 4.13.0 sources on GitHub;
  sources split into scientific and implementation; a closing provenance line was added
  (the file had none) with the drafting date 2026-10-18 from the git history. Front matter
  unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/50-calibration-geometrie/51-ransac-homographie.md): expected
  answers of -002, -003, -004 and -006 as quoted above; further explanations and blocking
  errors of all seven cards corrected as in the appendix, plus "pre-treatment" →
  "preprocessing", "digital" → "numerical", "dots" → "points", "The draw protects certain
  outliers instead of including them all in an initial estimate" → "Small samples keep
  outliers out of a candidate estimate instead of including all of them in an initial
  fit", "sense of warp" → "direction of the warp", "lack of prints" → "too few draws", "nine
  runs" → "nine draws", "The stop trust" → "The stopping confidence", "Experience built" →
  "Constructed experiment", "check for lack of alignment and model plane" → "check that
  points are not nearly collinear and that they lie on the model plane". CV-HOMOGRAPHIE-004
  gained one sentence on OpenCV's rounding and iteration cap. All Source lines cite exact
  sections or code lines. Questions, IDs, objectives, families, tags and target deck
  unchanged.

Other subjects repeating the budget formula (`47-fast-brief`, `62-recalage-global-icp`)
state it consistently; no wrong claim was found there.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (shared file, not
edited here). P-CV-HOMOGRAPHIE-01 carries forward the 2026-10-20 proposal "residual
symmetric and uncertainty in both images", which was never registered.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-HOMOGRAPHIE-01 | CV-HOMOGRAPHIE | Compare the one-sided transfer error used by `findHomography` with a symmetric or reprojection error when both images are noisy, and say when the difference matters | Error model of the residual; only destination noise is tested today | Reasoning; Assumptions and Alternatives | 1 card, 3 criteria | [OpenCV 4.13.0 calib3d.hpp L794–L812](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); a multiple-view geometry textbook chapter on homography estimation (to be read) |
| P-CV-HOMOGRAPHIE-02 | CV-HOMOGRAPHIE | Choose among `RANSAC`, `LMEDS`, `RHO` and `USAC_MAGSAC` from the expected inlier ratio, the knowledge of the noise scale and the time budget | No card trains the estimator choice exposed by OpenCV 4.13 | Design; Parameters | 1 card, 3 criteria | [OpenCV 4.13.0 calib3d.hpp L551–L560, L824–L831](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); [MAGSAC++ abstract](https://arxiv.org/abs/1912.05909) |

Defective question (not edited; questions are verbatim invariants): the front of
CV-HOMOGRAPHIE-004 writes "$w=0,5$" with a French decimal comma. Proposed wording: "For
homography estimation with an assumed inlier proportion $w=0.5$, why are 72 draws targeted
for nominal confidence 0.99, and what does this confidence mean?"

## Sources

Scientific sources:

- Fischler and Bolles 1981, [CACM 24(6) PDF](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf)
  (text extracted with `pdftotext`): §II, §II.A, §II.B (including the 35.7-draw example),
  §II.C.
- Barath, Matas and Noskova, MAGSAC, [arXiv 1803.07469](https://arxiv.org/abs/1803.07469),
  and Barath et al., MAGSAC++, [arXiv 1912.05909](https://arxiv.org/abs/1912.05909):
  abstracts only.

Implementation sources (official code at tag 4.13.0):

- [`modules/calib3d/include/opencv2/calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L551–L560, L775–L853.
- [`modules/calib3d/src/fundam.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fundam.cpp): L71–L463.
- [`modules/calib3d/src/ptsetreg.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/ptsetreg.cpp): L55–L260.
- [`doc/tutorials/features2d/homography/homography.markdown`](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/features2d/homography/homography.markdown): Basic theory (L30–L90), Demo 3 (L248–L425), Demo 5 (L527–L600).

Failed accesses and limits:

- docs.opencv.org returned HTTP 403; the tutorial and API pages were read from their 4.13.0
  sources instead. The docs.opencv.org links kept in the 2026-10-30 and 2026-11-08
  appendices are historical records and were not re-read.
- **Not verifiable**: Hartley 1997, "In Defense of the Eight-Point Algorithm" (the only
  open PDF found has an unreadable text layer); Hartley and Zisserman's textbook (not
  accessible). No claim of the note relies on them.
- Zhang's MSR-TR-98-71, cited in the 2026-11-08 appendix, was not re-read for this subject
  (Microsoft's server refused `curl`); see the CV-ZHANG report of this pass.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/51-ransac-homographie.py` | 12 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/51-ransac-homographie.md` | 7 cards, 373–461 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 57 protected card lines identical; front matter identical except `revision: 8` → `9`; H1 and 14 per-card headings unchanged; `$`, `$$` and fences balanced; reference-style link definitions kept |

No OpenCV call or image experiment was executed; the snippet is illustrative and the
proposed baseline is a protocol, not a result. Mermaid and tables were not rendered in
Obsidian; AnkiDroid rendering of the multi-line pseudocode restored in CV-HOMOGRAPHIE-003
is unverified. This is agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-HOMOGRAPHIE
revision 9, CV-HOMOGRAPHIE-001 to -007, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-HOMOGRAPHIE-01, P-CV-HOMOGRAPHIE-02).
