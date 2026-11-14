# Review — Camera calibration with a target — Zhang’s method — 2026-11-14

## Overview

7 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 0 important, 7 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for planar-target calibration. It now follows Zhang's
report section by section (model, constraints, closed form, maximum likelihood,
distortion, degeneracies, experiments), documents where OpenCV 4.13 differs
(initialization, no skew, richer distortion, RMS denominators), and quantifies
identifiability with a noise-free reconstruction of Zhang's simulated set-up.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | Calibration estimates intrinsics, distortion and one pose per view; pose of a calibrated camera is a separate problem: confirmed (Zhang §2.1, §3.1; OpenCV header: "use solvePnP" when intrinsics are known). "Example of a string", "homograph", "What data raises what unknowns", "lifting the same unknowns" | Understanding: separates calibration, pose and registration | 3 expected criteria; 327 → 327 lexical words | Aligned with the reference appendix | Minor | Language fixes; Source line given exact passages instead of the blocked docs page |
| CV-ZHANG-002 | Projection $sx=K[R\mid t]X$ with $R$ from target to camera and $t$ in target units: confirmed (Zhang eq. 1; OpenCV `rvecs`/`tvecs` bring target coordinates into the camera frame). Expected answer "main dot" for *principal point*; "coordinate frame world/calibration target to camera" unclear; "**check**"; "normalized coordinates without unity" | Reasoning: frames and units of the projection | 3 expected criteria; 438 → 438 lexical words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given header lines |
| CV-ZHANG-003 | Two constraints per view; $n\ge3$ general, $n=2$ with zero skew; pure translation and parallel planes degenerate: confirmed (Zhang §2.3, §3.1, §4 Proposition 1) and recomputed (checks 1–5: ranks 5, 2, 2, 4 → 5). "Why guidance provides information" (*orientation*), "similar stresses" (*constraints*), "allowable", "vector product" | Reasoning: multi-view constraints and degeneracy | 3 expected criteria; 403 → 404 lexical words | Aligned with the appendix | Minor | Language fixes; Source line given equations and Proposition 1 |
| CV-ZHANG-004 | RMS measures the fit, not metric accuracy: confirmed by definition (Zhang §5.2 "root of mean squared distances, in pixels"). Missing condition: OpenCV 4.13 itself uses two denominators (`calibrateCamera` per point, `stereoCalibrate` per coordinate, calibration.cpp L621, L1155). Expected answer "reserved catches" (*held-out captures*); "Validation construite" left in French; "RMS adjustment pixel" | Evaluation: interpret a reprojection RMS | 2 expected criteria; 401 → 426 lexical words | Aligned with the reference worked example B | Minor | Meaning-restoring fix of the expected answer; one sentence on OpenCV's two conventions; Source line given code lines |
| CV-ZHANG-005 | $K'=AK$ for resize and crop, distortion unchanged: confirmed (OpenCV header: coefficients "remain the same regardless of the captured image resolution" while $f_x,f_y,c_x,c_y$ are scaled); 300 px and the order example recomputed (checks 7–8). Expected answer "main point"; "$a=0,5$"; "the new center is worth 300 px"; "focal length pixel" | Practice: propagate a pixel transform | 2 expected criteria; 397 → 402 lexical words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given header lines |
| CV-ZHANG-006 | Near-frontal views leave intrinsics poorly constrained: confirmed (Zhang §4; §5.1, 40% failures at 5°, best near 45°). Expected answer "checking free corners and parameters" mistranslated "vérifiant coins et paramètres libres" (*the corners and the free parameters*); "sub-assemblies", "Clearing mechanism", "Unleashing", "digital stability" | Diagnosis: observability of the intrinsics | 3 expected criteria; 388 → 389 lexical words | Aligned with the appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given sections and code lines |
| CV-ZHANG-007 | Industrial protocol and ray–plane intersection: consistent (project protocol; constructed 0.4 mm off-plane error, check 12). "Excluded catches", "holds" (*captures*), "plan" for plane, "radius" for ray, "dedistorted" | Design: calibration usable for metrology | 3 expected criteria; 316 → 319 lexical words | Aligned with the appendix | Minor | Language fixes; Source line given §3.4, §5.3 and header lines |

Expected-answer changes (meaning-restoring language fixes):

- CV-ZHANG-002: "$R$ transforms the coordinate frame world/calibration target to camera;
  $t$ is expressed in the coordinate frame camera and in the world points unit" → "$R$
  transforms the world (calibration target) frame into the camera frame; $t$ is expressed
  in the camera frame and in the unit of the world points"; "the main dot" → "the
  principal point".
- CV-ZHANG-004: "Validate on reserved catches and an independent measure suitable for
  use." → "Validate on held-out captures and an independent measurement suited to the use."
- CV-ZHANG-005: "transform the main point into" → "transform the principal point into".
- CV-ZHANG-006: "while checking free corners and parameters" → "while checking the
  corners and the free parameters".

## Reference findings

Claims of revision 8 checked against Zhang MSR-TR-98-71 (updated 2002):

- Model, $H\sim K[r_1\ r_2\ t]$, the two constraints, two constraints per view: confirmed
  (eqs. 1–4).
- "Three independent views are usually required; two may suffice by imposing a zero
  skew": confirmed (§3.1; the report adds the $n=1$ case).
- "Translations alone do not bring new orientation constraints": confirmed (§4, pure
  translation $R_2=R_1$; Proposition 1 for parallel planes).
- Radial model on normalized coordinates with two coefficients: confirmed (§3.3, centre
  at the principal point).
- No scientific error in revision 8. Language defects: "the dot", "main point", "plan",
  "homographs", "coins" (*corners*), "reserved catches", "Forts residuals", "drive RMS",
  "Question of work", "Reference Response", "Validation construite", and no closing
  provenance line.

New claims verified for revision 9 (main ones):

- Zhang: circular-point interpretation (§2.4); $V$ of size $2n\times6$, smallest singular
  vector (§3.1); Appendix B formulas; extrinsics and Appendix C; "algebraic distance which
  is not physically meaningful" and the ML functional with Rodrigues vectors and LM (§3.2);
  alternation versus complete ML (§3.3); six-step procedure (§3.4); LM in 3–5 iterations
  (§5); simulation set-up and results (noise 0.1–1.5 px, 100 trials, < 0.3% and about 1 px
  at 0.5 px noise; number of planes; orientation with failures at 5° and best near 45°);
  real data (640×480, 256 corners, Table 1 values, Table 2 aspect ratio
  0.99995 ± 0.00012); model imprecision (§5.3); Appendix A normalization remark; Appendix D.
- OpenCV 4.13: pinhole and distortion model, coefficient order, monotonicity warning,
  resolution statement (calib3d.hpp L56–L330); chessboard detection notes; `calibrateCamera`
  contract, flags, default criteria, initialization with principal point at the image centre
  and focal lengths by least squares, `solvePnP` poses, global LM, `patternSize` warning
  (L1606–L1743); `initIntrinsicParams2D`, RMS and standard deviations in calibration.cpp.

Paper–implementation differences (FR-036):

| Aspect | Zhang MSR-TR-98-71 | OpenCV 4.13.0 |
| --- | --- | --- |
| Initialization | Closed form for all five intrinsics from $V\mathbf b=0$ (§3.1, App. B) | Principal point fixed at $((w-1)/2,(h-1)/2)$, focal lengths by least squares from homographies, poses by `solvePnP` (calibration.cpp L61–L140; calib3d.hpp L1649–L1653, L1692–L1708) |
| Skew | Estimated ($\gamma$) | No skew parameter in the camera matrix |
| Distortion | Two radial terms (§3.3) | Up to 14 coefficients, tangential by default, enabled by flags |
| RMS | Per point, in pixels (§5.2) | Per point in `calibrateCamera`; per coordinate in `stereoCalibrate` |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 853 → 3,429.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task; OpenCV data contract (inputs, units, outputs, coefficient order, pose direction, `patternSize` convention); pipeline roles |
| Intuition | Shallow | Developed | Orthonormal axes and circular points; constructed frontal-capture illustration; Mermaid diagram of the procedure |
| Prerequisites | Shallow | Developed | Links to CV-SE3, CV-SVD, CV-BA, CV-CORNERS, PnP, fisheye, multi-sensor and hand–eye notes |
| Assumptions | Shallow | Developed | Target, camera and noise assumptions; distortion model scope; number of views; degeneracies with Proposition 1 and Appendix D; orientation results of §5.1 |
| Procedure | Shallow | Developed | Zhang's six steps with purposes; pseudocode with appendix references |
| Mathematics | Developed (model, constraints) | Developed | $V\mathbf b=0$, Appendix B and C, ML functional, Zhang versus OpenCV distortion, RMS conventions, pixel transforms; worked examples A–D |
| Parameters | Shallow | Developed | Parameter table with sources and flag effects; four-step tuning approach |
| Properties | Shallow | Developed | Statistical meaning and OpenCV standard deviations; real-data stability; model scope; units; limits of the RMS |
| Cost and implementation | Shallow | Developed | Cost drivers; OpenCV 4.13 contracts with line numbers; initialization differences; illustrative call |
| Evaluation | Shallow | Developed | Zhang's simulation and subset protocols; baseline and orientation variation with a foreshortening confound; limits |
| Failure modes and diagnosis | Three-row table | Developed | Seven-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | One sentence after the appendices | Developed | Fisheye, PnP, 3-D rig, known translation, multi-sensor and hand–eye; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/52-calibration-zhang.py`](checks/52-calibration-zhang.py) (12 checks): Zhang's
simulated camera and planes give rank 5 and exact recovery of the five intrinsics through
Appendix B; the 89.95° axis angle; rank 2 for pure translations and for parallel planes;
rank 4 for two views and 5 with the zero-skew row; per-point (0.614 px) versus
per-coordinate (0.434 px) RMS; 300 px and 299.75 px principal points after resize and crop;
140 versus 150 px for the two orders; OpenCV's initial principal point (319.5, 239.5); the
1.01% scale bias; a 13.7 px radial displacement at the image corner with Zhang's Table 1
coefficients; the 0.4 mm off-plane error.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md),
  revision 8 → 9: body rewritten and deepened as above; the trailing "Alternatives, sources
  and flashcards" section became "Sources and flashcards" (its alternatives moved into the
  body); `[opencv]` now points to the 4.13.0 header on GitHub; a closing provenance line was
  added (the file had none; drafting date 2026-10-18 from the git history). Appendix
  language fixes, applied identically to the card text: "check out of learning" →
  "validation outside the calibration data", "Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Example of a string" → "Example of a chain",
  "homograph" → "homography", "keep a part or target of check independent" → "keep an
  independent check part or target", "between holds" → "between captures", "What data
  raises what unknowns" → "Which data resolve which unknowns", "lifting" → "resolving",
  "main point" → "principal point", "Passing constraints to poses" → "From constraints to
  poses", "allowable" → "admissible", "vector product" → "cross product", "reserved" →
  "held-out", "set parameters" → "fixed parameters", "digital stability" → "numerical
  stability", "measurement on a plan" → "measurement on a plane", "radius" → "ray",
  "dedistorted" → "undistorted", "Annex C, stresses, poses and degenerations" → "Appendix C,
  constraints, poses and degeneracies". Front matter unchanged except `revision`; H1 and
  per-card headings unchanged.
- [Cards](../../../vault/50-calibration-geometrie/52-calibration-zhang.md): expected answers
  of -002, -004, -005 and -006 as quoted above; further explanations and blocking errors of
  all seven cards corrected as in the appendix, plus "Why guidance provides information" →
  "Why orientation provides information", "similar stresses" → "similar constraints",
  "Validation construite" → "Constructed validation", "The residual pixel" → "The pixel
  residual", "$a=0,5$" → "$a=0.5$", "the new center is worth 300 px" → "the new principal
  point is at 300 px", "Interface Trap" → "Interface trap", "sub-assemblies, maps by
  residuals and reserved validation" → "subsets, residual maps and held-out validation",
  "Clearing mechanism" → "Compensation mechanism", "Unleashing" → "Freeing", "excluded
  catches" → "excluded captures", blocking errors put in gerund form. CV-ZHANG-004 gained
  one sentence on OpenCV's two RMS denominators. All Source lines cite exact sections or
  code lines; the "Context7 verification" links to the blocked documentation page were
  replaced. Questions, IDs, objectives, families, tags and target deck unchanged.

`rg` over `vault/` finds the same "three views, two with zero skew" statement only in the
progress log; no other subject repeats a corrected claim.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (shared file, not
edited here). The 2026-10-20 proposal "Identify the known metric translation case"
(Appendix D) was marked as no priority at the time and is not carried forward.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ZHANG-01 | CV-ZHANG | Recognize a non-monotonic radial distortion estimate as a calibration failure, explain why it can look good near the centre, and name the check (radial factor over the image radius, peripheral held-out views) | No card trains the diagnosis of a plausible-looking but invalid distortion model | Diagnosis; Failure modes | 1 card, 3 criteria | [OpenCV 4.13.0 calib3d.hpp L262–L277](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp); [Zhang §3.3, §5.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) |

No defective question was found. Objective lines that read oddly in English ("There are
three geometric objectives.", "Spreading a pixel transformation.") are invariants and were
not edited; their French originals are "distinguer trois objectifs géométriques" and
"propager une transformation pixel".

## Sources

Scientific sources:

- Zhang, "A Flexible New Technique for Camera Calibration", MSR-TR-98-71, updated 2002,
  [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf):
  downloaded through WebFetch (direct `curl` was refused) and extracted with `pdftotext`;
  read §2.1–§2.4, §3.1–§3.4, §4, §5.1, §5.2 (Tables 1–2), §5.3, Appendices A–D.

Implementation sources (official code at tag 4.13.0):

- [`modules/calib3d/include/opencv2/calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L56–L330, L1336–L1460, L1606–L1743.
- [`modules/calib3d/src/calibration.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration.cpp): L61–L140, L166–L622, L626, L1155.

Failed accesses and limits:

- docs.opencv.org returned HTTP 403; the documentation links kept in the 2026-10-30 and
  2026-11-08 appendices were not re-read.
- The TPAMI 2000 journal version was not consulted; the technical report is its full version.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/52-calibration-zhang.py` | 12 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/52-calibration-zhang.md` | 7 cards, 319–438 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 57 protected card lines identical; front matter identical except `revision: 8` → `9`; H1 and 12 per-card headings unchanged; `$`, `$$` and fences balanced; link definitions `[zhang]` and `[opencv]` kept |

No calibration, OpenCV call or image experiment was executed; the noise-free
reconstruction in the check script is a numerical illustration, not a calibration result.
Mermaid and tables were not rendered in Obsidian; AnkiDroid rendering is unverified. This
is agent self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-ZHANG revision 9,
CV-ZHANG-001 to -007, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-ZHANG-01).
