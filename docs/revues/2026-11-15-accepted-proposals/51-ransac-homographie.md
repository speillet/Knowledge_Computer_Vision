# Review — RANSAC and homography — 2026-11-15

## Overview

One reference correction found while writing CV-MATCHING-005 (see the
[CV-MATCHING report](43-detecteurs-matchers.md)). No card of this subject was
changed or re-audited; no card repeats the corrected claim.
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 9 → 10.

## Reference findings

The implementation section said that "exactly four points, or method 0, give a
direct DLT with all points marked inliers", and limited the later refit,
Levenberg–Marquardt refinement and mask recomputation to robust fits. In
OpenCV 4.13.0, `findHomography` with method 0 and more than four pairs does
start from a DLT on all pairs with a mask of ones (`fundam.cpp` L401–L405).
It then enters the same post-processing as RANSAC and LMeDS, which skips only
RHO (L415): 10 Levenberg–Marquardt iterations on all pairs, scaling to
$h_{33}=1$, and a new mask over all input points with $e_i^2\le t^2$
(L415–L446). The returned mask can therefore mark outliers that still weighed
fully in the method-0 fit.

The recomputation is version-dependent. The "find new inliers" block is absent
from `fundam.cpp` at 4.11.0 and present at 4.12.0. It comes from
[opencv#26742](https://github.com/opencv/opencv/pull/26742), "Bug fix for
#25546 - Updating inliers for homography estimation", merged into `4.x` on
2025-01-11. The CV-MATCHING reference already stated this; the two references
now agree.

## Applied corrections

`vault/50-calibration-geometrie/references/51-ransac-homographie.md`, revision
9 → 10: both implementation bullets rewritten as above, and the closing
provenance line extended.

## Sources

Implementation sources, read on GitHub raw: `modules/calib3d/src/fundam.cpp`
at tags 4.13.0 (L355–L450), 4.12.0 and 4.11.0 (searched for the mask
initialization, the post-processing condition and the "find new inliers"
block), and the GitHub API record of pull request 26742 (title, merge date and
base branch). Context7 is unavailable in this session.

## Checks and limitations

Vault, catalogue, learning-path, unit-test and inventory checks are recorded
in the [overview](00-bilan.md). No OpenCV build was executed for this
correction. The subagent writing CV-MATCHING-005 ran a synthetic check with a
locally installed OpenCV 4.11.0, but not on this behaviour.
