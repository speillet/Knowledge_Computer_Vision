# Review — Local detectors, descriptors and matchers — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-MATCHING-02. One card added,
CV-MATCHING-005; the four existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/43-detecteurs-matchers.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-MATCHING-005 | Default `method=0` as least squares on all pairs: calib3d.hpp L788–L789, L812–L816, L841–L844; code path fundam.cpp L401–L405 (normalized DLT on all pairs) and L415–L434 (Levenberg–Marquardt on all pairs). Exceptions only for malformed input: fundam.cpp L378–L390, L412–L413; empty matrix only when no model: L448–L462 and calib3d.hpp L835. Iteration cap: ptsetreg.cpp L166 (start at `maxIters`), L228–L234 (update), L74 (the cap is returned when the requirement exceeds it). Best hypothesis returned without any confidence report: L238–L253; acceptance needs at least four inliers: L228. Mask recomputed after refinement for every method except RHO, method 0 included: fundam.cpp L415–L446 at 4.13.0, absent at 4.11.0 (L401–L447). Sample redraws: fundam.cpp L74–L106, ptsetreg.cpp L104–L158, L206–L215. Fixed seed: ptsetreg.cpp L171. "A minimal sample fits its own four pairs" and "redraws raise the empirical success rate above the nominal one": project deductions, supported by check 6 of the script and by the synthetic check below. Numbers 10,464, 0.637, 1.01 and 0.227: recomputed | Diagnosis of a silent production failure: a non-empty $H$ with no exception is the normal return in both failure modes, and the requested 0.995 is never reported as missed | 3 expected criteria; 492 lexical words, above the siblings (346–359) because each criterion carries its mechanism | Aligned with worked example C (now qualified) and with CV-HOMOGRAPHIE-004 on the update rule; notation $w$, $N$, $p$ as in the reference | Diagnosis |

The question names the `cv2.RANSAC` call and the default values of `maxIters` and
`confidence`, because the learner needs them to quantify the second failure. It does not
name least squares, the cap, the confidence reached or the mask checks.

Overlap check: CV-HOMOGRAPHIE-001 to 007 were read. CV-HOMOGRAPHIE-004 trains the
budget formula at $w=0.5$, the meaning of the confidence and, in its explanation, the
existence of the cap. CV-MATCHING-005 does not ask for that derivation; it trains the
diagnosis of a returned but unreliable model: the default non-robust method, the
cap reached without notice, and the acceptance checks a caller must add. CV-MATCHING-004
(repeated logos) concerns symmetry, not the estimator's defaults.

## Reference findings

- Worked example C said that a lower inlier ratio "can turn a reliable registration
  into a coin flip". This is imprecise. The 0.637 is the nominal guarantee under
  independent uniform sampling. OpenCV redraws collinear or orientation-inconsistent
  minimal samples before they count as iterations (fundam.cpp L74–L106; ptsetreg.cpp
  L104–L158, L206–L215). In the synthetic check below, 289 of 300 sets with $w=0.15$
  were still registered. The example now separates the lost guarantee from the observed
  success rate, adds the threshold $w<0.227$ at which the default cap binds, and gives
  the synthetic counts as measurements.
- The failure-mode table ("Inlier ratio per pair; iterations used") and the proposed
  baseline ("RANSAC iterations used") relied on a quantity that `findHomography` does
  not return: the function returns only $H$ and the mask (calib3d.hpp L841–L844;
  fundam.cpp L357–L463). Both now use $N(\hat w)$ against `maxIters` and a rerun on
  permuted input.
- The `findHomography` contract bullet was correct but too short for the card. Two
  bullets now state what counts as failure, the method-0 refinement, the mask
  recomputation and its version history, and the RANSAC loop behavior.

Finding outside this subject, not edited (CV-HOMOGRAPHIE belongs to another agent):
`vault/50-calibration-geometrie/references/51-ransac-homographie.md` L336 states that
"Exactly four points, or method 0, give a direct DLT with all points marked inliers
[fundam.cpp L401–L405]", and L340–L342 attribute the refinement and the new mask to
robust fits only. At 4.13.0, method 0 with more than four pairs also goes through
Levenberg–Marquardt on all pairs and a mask recomputed at `ransacReprojThreshold`
(fundam.cpp L415–L446); only exactly four pairs keep a mask of ones. No card repeats
the claim (`grep` for "marked inliers" in `vault/` finds only that line).

## Applied corrections

- `vault/40-features-matching/43-detecteurs-matchers.md`: CV-MATCHING-005 appended.
- `vault/40-features-matching/references/43-detecteurs-matchers.md`, revision 8 → 9:
  worked example C extended and qualified (one expected all-inlier sample, the 0.227
  threshold, silent return, nominal versus observed success); two contract bullets on
  failure semantics, method 0, the recomputed mask (since 4.12.0,
  [opencv#26742](https://github.com/opencv/opencv/pull/26742)) and the RANSAC loop;
  the "iterations used" check replaced in the failure table and the baseline; method-0
  row extended; `fundam.cpp` and `ptsetreg.cpp` added to the implementation sources; the
  card listed under related flashcards; the "no code executed" sentence qualified;
  closing provenance line extended.

## Proposals

P-CV-MATCHING-02: accepted by the learner on 2026-11-15, completed as CV-MATCHING-005.

## Sources

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns
HTTP 403 from this environment and was not retried; Context7 is unavailable in this
session):

- `modules/calib3d/include/opencv2/calib3d.hpp` L551–L560 (method flags), L776–L860
  (`findHomography` documentation and declarations);
- `modules/calib3d/src/fundam.cpp` L70–L220 (`HomographyEstimatorCallback`: subset
  checks, normalized DLT, transfer error), L355–L470 (`findHomography`);
- `modules/calib3d/src/ptsetreg.cpp` L50–L290 (`RANSACUpdateNumIters`, `findInliers`,
  `getSubset`, RANSAC loop).

Version history: `fundam.cpp` at tag 4.11.0 (L398–L448, and a full diff against 4.13.0:
only the mask recomputation and an unrelated `sampsonDistance` assertion differ), at tag
4.12.0 (the recomputation is present at L436), `ptsetreg.cpp` at 4.11.0 (diff: only a new
translation estimator), and the GitHub API record of PR #26742 ("Bug fix for #25546 -
Updating inliers for homography estimation", merged into 4.x on 2025-01-11).

No scientific source carries this card: its claims belong to the implementation. The
RANSAC budget formula is the one sourced in CV-HOMOGRAPHIE (Fischler and Bolles 1981,
§II.B), not re-opened in this pass.

## Checks and limitations

`python3 -I checks/43-detecteurs-matchers.py` passes its 7 checks: the inlier ratio
and $w^4$, the 10,464 nominal samples, a port of `RANSACUpdateNumIters` returning the cap
(and 82 at $w=0.5$, as in CV-HOMOGRAPHIE), the 0.637 confidence and 1.01 expected
all-inlier samples, the 0.227 threshold, the exact fit of a minimal sample to its own
four pairs on 50 random clutter samples, and the nominal confidences quoted in the
reference.

Synthetic check, executed with the OpenCV 4.11.0 Python package installed in this
environment (no 4.13.0 build was available). The RANSAC loop and the homography callback
are identical in the two versions; the RNG implementation in `core` was not compared.
Setup: a fixed homography, 400 pairs in a 640×480 frame, inliers with 0.5 px Gaussian
noise, outliers uniform; success means a maximum transfer error below 5 px against the
true homography on a 3×3 grid of the frame. Results: with $w=0.15$ the default call
(method 0) returned a non-empty matrix with a 430 px error and a mask of 400 ones (4.11.0
semantics); `RANSAC` at 3 px returned the same matrix on a rerun; 289, 150 and 38
successes of 300 at $w=0.15$, 0.10 and 0.075, every call returning a non-empty matrix,
with 5 to 31 mask inliers on the failures inspected; pure clutter returned a non-empty
matrix with 5 mask inliers. The script stays in the session scratchpad and is not part
of the repository; the counts are not a benchmark.

`python3 scripts/check_vault.py`: OK (142 Markdown documents, 60 references, 292 cards at
the last run, including concurrent additions by other agents). `python3 scripts/learning_path.py`: OK,
0 errors. Inventory of the card file: 5 cards, no anomaly. `git diff --check` on the
subject's files: clean. Front matter unchanged except `revision`; H1 and existing
per-card headings unchanged.

Agent self-review, without independent scientific validation. Obsidian and AnkiDroid
rendering of the card are not verified. Export status: **to republish with
`paquet-anki`**. Shared files left to the coordinator: the proposal register
(P-CV-MATCHING-02), the correction log of `vault/01-Parcours/Suivi-pilote.md` (CV-MATCHING
revision 9: example C qualification and the "iterations used" correction), the
generated catalogue and card counts, and the CV-HOMOGRAPHIE finding above.
