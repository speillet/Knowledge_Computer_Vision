# Review — Rectified stereo, SGM and depth — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for dense rectified stereo with SGM and OpenCV's
`StereoSGBM`. Epipolar geometry stays in
[CV-EPIPOLAIRE](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md)
and rig calibration in
[CV-MULTICALIB](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | $Z=fB/d=10$ m: recomputed; principal-point offset term and Q: confirmed by OpenCV 4.13.0 `calib3d.hpp` L2058–L2085 (Q gives $Z/W=fT_x/(c_{x1}-c_{x2}-d)$). "rectified image/reprojection matrix torque" mistranslated *couple* (pair); "main abscissa" (principal-point abscissa); "even focal length" (*même*: same); "hidden region" | Reasoning: compute rectified depth with its assumptions | 1 expected criterion; 305 → 316 lexical words | Matches worked example A | Minor | Language fixes; Source line moved to versioned header lines |
| CV-STEREO-002 | $\sigma_Z\approx fB\sigma_d/d^2$, 0.25 m and 1 m, 80–133.3 m: recomputed. "drifting $Z=fB/d$" mistranslated *dériver* (differentiate); decimal commas "0,5 px", "0,25 m"; "overlaying" (*recouvrement*: overlap); "depth inverse representation" | Reasoning: why error grows with range | 1 expected criterion; 351 → 351 lexical words | Matches worked example B | Minor | Language fixes; Source line given sections |
| CV-STEREO-003 | Four fractional bits, value $=16d$, invalid $(\text{minDisparity}-1)\times16$, `reprojectImageTo3D` assumes no fractional bits: confirmed (`calib3d.hpp` L3502–L3512, L3060–L3064; `stereosgbm.cpp` L507). "basic units" (*unités de baseline*: baseline units), "digital conversion" | Diagnosis: decode a fixed-point output contract | 3 expected criteria; 275 → 282 lexical words | Matches the Procedure section | Minor | Language fixes; Source line given exact lines |
| CV-STEREO-004 | Rectification does not resolve texture, repetition or occlusion; left–right check: confirmed by Hirschmüller §2.2–§2.3 (eq. 15) and OpenCV's check (`stereosgbm.cpp` L945–L960). "What the correction changes" (*rectification*); "a positive straight disparity" mistranslated *droite* (right disparity), which made the left–right check unreadable; "changes in sum" | Comparison: rectification geometry versus matching evidence | 2 expected criteria; 350 → 370 lexical words | Consistent with Properties and the failure table | Minor | Meaning-restoring language fixes; Source line given sections and lines |

No expected answer changed.

## Reference findings

Claims of revision 6 checked against their passages:

- $Z=fB/d$, $\sigma_Z\approx fB\sigma_d/d^2$, use of Q, fixed-point disparity stored ×16:
  confirmed (OpenCV `calib3d.hpp` L2058–L2085, L3060–L3097, L3502–L3512).
- "SGBM from OpenCV is a variant … not all the details of the original article":
  confirmed and made precise (5 directions by default, blocks, Birchfield–Tomasi instead of
  mutual information, pre- and post-processing, L3671–L3688).
- "B=0,2 m": decimal comma fixed.
- No scientific error found. Language defects: "research" (search), "main points"
  (principal points), "Overall Depths ×16", "Question of work", "Reference Response",
  "Documentary reference", "built-in uncertainty derivations".

New claims verified for revision 7 (main ones):

- Hirschmüller 2008: energy eq. 11 with $P_1$, $P_2\ge P_1$ and gradient-adapted $P_2$;
  NP-completeness of 2-D minimization and streaking of 1-D DP; path recursion eqs. 12–13;
  at least 8, preferably 16 paths, eq. 14; 11-bit costs, $S\le16(C_{\max}+P_2)$, 16-bit
  $W\times H\times D$ arrays, $O(WHD)$; parabolic subpixel "theoretically justified only
  for … SSD"; 3×3 median filter; consistency check eq. 15 enforcing uniqueness; no
  visibility or ordering constraint in paths (§2.2, §2.3); Middlebury thresholds 1 and
  0.5 px on non-occluded pixels (§3.1).
- Scharstein and Szeliski 2002: four building blocks (§3); RMS and bad-pixel metrics with
  $\delta_d=1.0$ (§5.1).
- Menze and Geiger 2015: outlier if error exceeds 3 px and 5% of the true value (§5).
- OpenCV 4.13.0: `stereoRectify` flags, `alpha`, default `CALIB_ZERO_DISPARITY`, P1/P2/Q;
  `reprojectImageTo3D` frame, scaling and `handleMissingValues` ($Z=10000$);
  `StereoMatcher` fixed point; `StereoSGBM` description, modes and parameter advice;
  `stereosgbm.cpp`: 8-bit input, `CV_16S` output, fallbacks $P_1=2$, $P_2=\max(5,P_1+1)$,
  invalid value, uniqueness test, parabolic step, left–right check, unconditional 3×3
  median, speckle filter.

Documentation and code disagreement recorded in the note (FR-036): the header says that a
non-positive `disp12MaxDiff` disables the left–right check (`calib3d.hpp` L3730–L3731),
whereas `computeDisparitySGBM` replaces it by 1 and still runs the check
(`stereosgbm.cpp` L499, L945–L960). Not verified for `MODE_SGBM_3WAY` and `MODE_HH4`
beyond the shared fallback lines (L1229–L1238).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 365 → 2,615.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task; inputs (8-bit pair, calibration, rectification, range); fixed-point output and invalid value; 3D frame and units; depth versus distance; pipeline role |
| Intuition | Shallow (merged) | Developed | 1-D search, inverse depth law, SGM idea; constructed numbers; Mermaid processing diagram |
| Prerequisites | Developed (1 link) | Developed | Added CV-MULTICALIB, CV-ZHANG, CV-FISHEYE, CV-FILTRES, CV-MATCHING with the reason for each |
| Assumptions | Shallow | Developed | Rectification, synchronization, photometric consistency, texture along rows, range, no ordering constraint; degenerate cases |
| Procedure | Shallow | Developed | Offline and per-frame pseudocode; purpose of rectification flags, masking, division by 16 and Q |
| Mathematics | Developed (formula) | Developed | Offset-aware depth formula; Q and its depth; SGM energy, path recursion, sum, subpixel, consistency check; uncertainty and quantization |
| Parameters | Shallow (list) | Developed | Nine-row `StereoSGBM`/`stereoRectify` table with the doc–code disagreement; worked example C; four-step tuning approach |
| Properties | Shallow | Developed | Approximate global energy, linear complexity, discontinuities, uniqueness versus correctness, subpixel bias, implementation differences |
| Cost and implementation | Shallow | Developed | $O(WHD)$; storage and 11-bit bound; worked example D; four OpenCV 4.13 contracts; execution status |
| Evaluation | Shallow | Developed | Taxonomy metrics, Middlebury and KITTI protocols; baseline `MODE_SGBM` and controlled variation `MODE_HH` with confound; measurement limits |
| Failure modes and diagnosis | Shallow (three sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Block matching, baseline choice, active depth, learned stereo (not reviewed), monocular; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/61-stereo-profondeur.py`](checks/61-stereo-profondeur.py) (14 assertions): depths
10 and 20 m; Q reproduces 10 m and gives 12.5 m with a 4 px principal-point offset;
fixed-point 320 → 20 px and the 16× error; invalid values −16 and −272; $\sigma_Z$ 0.25 and
1 m; 80–133.3 m interval; 0.78 m quantum at 50 m; `numDisparities` 144 for 1.5 m; 235.9 MB
per cost array; 16-bit bound; suggested penalties; KITTI outlier rule; 11.18 m distance.

## Applied corrections

- [Reference](../../../vault/60-vision-3d/references/61-stereo-profondeur.md),
  revision 6 → 7: body rewritten and deepened as above; decimal comma fixed; appendix
  language fixed identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "derivation of units" → "Units in the
  derivation", "Example of check" → "Example check", "Construction of triangles" →
  "Similar-triangle construction", "What the correction changes" → "What rectification
  changes", "Bidirectional verification built" → "Constructed left–right check");
  sources split; closing provenance line replaced. Front matter unchanged except
  `revision`; H1 and per-card headings kept.
- [Cards](../../../vault/60-vision-3d/61-stereo-profondeur.md): explanation and
  blocking-error fixes listed in the findings table, applied word for word in the
  reference appendices, plus "Representation Trap" → "Representation trap", "Analytical
  Sensitivity" → "Analytical sensitivity", "Assume constant depth noise for any distance"
  → "Assuming constant depth noise at every distance", "Reproject fixed integers as
  ordinary pixels of disparity" → "Reprojecting fixed-point integers as ordinary disparity
  pixels", "Deduct a reliable depth from the only horizontality" → "Inferring a reliable
  depth from the horizontality … alone". Source lines now cite versioned OpenCV lines,
  Hirschmüller and Scharstein–Szeliski sections. Questions, IDs, objectives, families,
  tags and target deck unchanged.

`rg` over `vault/` for "disparit" and "fB/d": CV-EPIPOLAIRE-004 and the CV-HOMOGRAPHIE
parallax case state the same law consistently. Language note for the coordinator
(another subject, not edited): CV-EPIPOLAIRE cards and reference use "reverse depth" and
"posing $\rho=1/Z$" for *inverse depth* and *setting* (`vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md` L98).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-STEREO-01 | CV-STEREO | Explain what $P_1$ and $P_2$ penalize in SGM, why $P_2\ge P_1$, and the visible effect of raising $P_2$ | The SGM mechanism is named but untested; carries forward the unregistered 2026-10-20 idea "Explain the penalties SGM P1/P2" | Algorithm; Mathematics and Parameters | 1 card, 3 criteria | [Hirschmüller 2008 §2.2, eqs. 11–13](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf); [OpenCV 4.13.0 `calib3d.hpp` L3723–L3729](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp) |
| P-CV-STEREO-02 | CV-STEREO | Size `minDisparity` and `numDisparities` from the nearest and farthest depths a task needs | Range sizing and its memory and time cost are untested | Practice; Parameters, worked example C | 1 card, 3 criteria ($d_{\max}=fB/Z_{\min}$; multiple of 16; linear cost in $D$) | [OpenCV 4.13.0 `calib3d.hpp` L3717–L3720](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); [Hirschmüller §2.2](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf) |

## Sources

Scientific sources, opened at the passages listed (text extracted with `pdftotext`):

- Hirschmüller, [TPAMI 2008 PDF (cvlibs mirror)](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Hirschmueller2008PAMI.pdf): §2.2, §2.3, §2.4, §3.1.
- Scharstein and Szeliski, [IJCV 2002 PDF](https://vision.middlebury.edu/stereo/taxonomy-IJCV.pdf): §3 introduction, §5.1.
- Menze and Geiger, [CVPR 2015 PDF](https://openaccess.thecvf.com/content_cvpr_2015/papers/Menze_Object_Scene_Flow_2015_CVPR_paper.pdf): §5 evaluation protocol.

Implementation sources (official code at tag 4.13.0):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L2030–L2130, L3060–L3097, L3499–L3530, L3671–L3756.
- [`stereosgbm.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/stereosgbm.cpp): L67–L122, L490–L510, L905–L960, L1229–L1238, L2208–L2232.

Failed accesses and limits:

- docs.opencv.org returned HTTP 403; the rendered pages remain cited as consulted in
  earlier passes. Context7 was not available.
- Not reviewed: learned stereo networks and KITTI's current online leaderboard rules
  beyond the 2015 paper.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | First run: ECHEC caused by another agent's in-progress file (`130-evaluation-fiabilite/references/134-metriques-applications.md`); rerun after that fix: OK, 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/61-stereo-profondeur.py` | 14 checks passed |
| `git diff --check -- vault/60-vision-3d/61-stereo-profondeur.md vault/60-vision-3d/references/61-stereo-profondeur.md` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/60-vision-3d/61-stereo-profondeur.md` | 4 cards, 316, 351, 282 and 370 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 0 errors; no expected answer changed; front matter identical except `revision: 6` → `7` |
| Local link and anchor check over `vault/60-vision-3d` | 121 local links, 0 errors |

No stereo matcher or OpenCV call was executed; the baseline and variation are protocols.
Mermaid and tables were not rendered in Obsidian; AnkiDroid rendering is unverified. This
is agent self-review without independent validation. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-STEREO revision
7, CV-STEREO-001 to 004, language corrections above, Agent Claude Code self-review, to
republish with `paquet-anki`) and the proposal register (P-CV-STEREO-01,
P-CV-STEREO-02).
