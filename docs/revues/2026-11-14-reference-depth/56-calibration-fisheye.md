# Review — Fisheye calibration — angular projection and off-center validation — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for angular (Kannala–Brandt) calibration as
implemented by OpenCV 4.13 `fisheye`, and for the rectification contract. General
target-based calibration stays in
[CV-ZHANG](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FISHEYE-001 | Zero coefficients give $r_d=\theta$ (equidistance), not $\tan\theta$: confirmed by OpenCV 4.13.0 `calib3d.hpp` L509–L536 and by Kannala and Brandt eqs. 1 and 3; 314 versus 520 px at 60° recomputed. "Why the center is cheating", "**check**", "Local development", "reverse", "we do not" | Reasoning: a coefficient vector has meaning only with its model | 2 expected criteria; 378 → 371 lexical words | Matches worked example A of the reference | Minor | Language fixes; Source line given exact lines and sections |
| CV-FISHEYE-002 | Sensitivity $\partial\theta_d/\partial k_j=\theta^{2j+1}$: confirmed from the model; whole-field coverage and reduced models against over-fitting: Kannala and Brandt §II-B and §V-B. Expected answer "Reserve poses and regions" (held out); "main center" mistranslated *centre principal* (principal point); French heading "Acquisition construite" left untranslated; "spot detection" | Design: plan informative and measurable peripheral views | 3 expected criteria; 377 → 377 lexical words | Matches worked example B | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given sections |
| CV-FISHEYE-003 | Mean residual dominated by densely sampled regions: arithmetic recomputed (0.66 px); ring-wise analysis is a project protocol consistent with Kannala and Brandt's residual maps (Fig. 5). Expected answer "the metric errors of the target use" mistranslated *usage visé* (intended use); "reserved observations"; "by crown, with headcount"; "location bias" for localization bias | Diagnosis: locate a model defect hidden by a global RMS | 3 expected criteria; 374 → 381 lexical words | Consistent with Evaluation and Failure modes | Minor | Meaning-restoring fix of the expected answer; language fixes |
| CV-FISHEYE-004 | Inverse map through $(K_{\mathrm{new}}R)^{-1}$: confirmed by `fisheye.cpp` L579–L615. "Radius of exit" and "gives a radius $q'$" mistranslated *rayon* (ray), which made the construction read as a radius; "reassemble a pixel to a radius" (back-project a pixel to a ray); "main center"; "This transformation is usually unrefined" (obscure) | Practice: carry the rectified contract downstream | 2 expected criteria; 311 → 314 lexical words | Matches the Mathematics section | Minor | Language fixes restoring "ray"; Source line moved to versioned code |
| CV-FISHEYE-005 | `balance` interpolates $f_{\mathrm{new}}$ between $f_{\max}$ and $f_{\min}$ from four undistorted edge midpoints and never changes $K$, $D$: confirmed by `fisheye.cpp` L655–L724. "Interpretation of Compromise", "set number of pixels", "cover, metric" | Evaluation: separate output geometry from calibration quality | 2 expected criteria; 363 → 423 lexical words | Matches worked example C | Minor | Language fixes; one sourced paragraph "What `balance` computes" added because the card's objective is to interpret this parameter and the mechanism was absent |

Expected-answer changes (meaning-restoring language fixes):

- CV-FISHEYE-002: "Reserve poses and regions for validation." → "Hold out poses and regions
  for validation."
- CV-FISHEYE-003: "Map the residuals according to radius, position and pose on reserved
  observations; inspect the points of calibration target at the edges and check the
  projection model. Then compare the metric errors of the target use." → "Map the
  residuals by radius, position and pose on held-out observations; inspect the
  calibration-target points at the edges and check the projection model. Then compare
  the metric errors for the intended use."

## Reference findings

Claims of revision 6 checked against their passages:

- Model equations, units and $r_d=\theta$ for zero coefficients: confirmed (`calib3d.hpp`
  L509–L536).
- "The four fisheye coefficients are not the first four Brown–Conrady coefficients":
  confirmed (OpenCV's $k_1$ multiplies $\theta^3$ inside an angular model; Kannala and
  Brandt eq. 6 with the first coefficient absorbed in the focal length).
- `balance` "exchanges conserved field and borders, without improving the physical
  parameters": confirmed and made precise (`fisheye.cpp` L655–L724).
- "At $\theta=60°$, a focal length of 300 px gives 314,16 px against 519,62 px":
  correct values, French decimal commas fixed (314.16 and 519.62).
- No scientific error found. Language defects: "pose $a=X/Z$" (*posons*, let),
  "reserved" for held-out, "out-of-the-way views", "low medium RMS", "main center",
  "radius" for ray, untranslated "Acquisition construite", "Question of work",
  "Reference Response", "**check**".

New claims verified for revision 7 (main ones):

- Kannala and Brandt: projection families eqs. 1–5; generic model eq. 6 with five terms;
  monotonicity and inversion (§II-A); asymmetric terms eqs. 8–10 and reduced models
  against over-fitting when control points do not cover the image (§II-B); pinhole
  singularity at $\pi/2$ (§III); circle-centroid bias (§IV-B); single-view calibration
  possible but whole-field coverage needed, Table III RMS values and held-out image
  (§V-B).
- Usenko, Demmel and Cremers: motivation for wide fields (§1); KB 6/KB 8 with
  $\operatorname{atan2}(r,z)$, iterative unprojection, singularity at $z=0$ of the
  pinhole-based implementation in OpenCV and Kalibr (§2.4); closed-form double-sphere
  inverse (§3); Huber-weighted Gauss–Newton calibration with AprilTag grid (§4); KB 8
  best on most of 16 sequences, double sphere within 1%; timing on a Xeon E5-1620
  (§5, Tables 1–2).
- OpenCV 4.13.0 `fisheye.cpp`: projection with $\theta=\arctan r$ and $z$ near 0 set to 1
  (L129–L138); Newton inversion, clipping of $\theta_d$ to $\pi/2$ with the comment "only
  valid up to 180 FOV", sentinel $(-10^6,-10^6)$ (L441–L519); inverse map through
  $(PR)^{-1}$ and $w\le0$ handling (L579–L615); `balance` rule (L655–L724);
  initialization $f=\max(w,h)/2$, principal point $(w/2-0.5,h/2-0.5)$, smoothing 0.4,
  condition threshold $10^6$ (L764–L786, L1500–L1501).

Documentation and code disagreement recorded in the note (FR-036): the header says that
with `CALIB_FIX_FOCAL_LENGTH` the focal length "is the $\max(width,height)/\pi$ or the
provided $f_x$, $f_y$" (`calib3d.hpp` L4239–L4240), whereas `calibrate` initializes it to
$\max(w,h)/2$ without a guess (`fisheye.cpp` L785).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 500 → 3,132.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task and reason (KB §III); inputs and outputs with units; raw versus rectified contracts; field-of-view limit of the implementation; pipeline roles |
| Intuition | Absent (merged in mathematics) | Developed | Angle compression; worked example A (five projection families at 60° and 90°); Mermaid data flow |
| Prerequisites | Developed (2 links) | Developed | Added CV-BA, CV-STEREO, CV-MULTICALIB with the reason for each |
| Assumptions | Shallow | Developed | Central radially symmetric model, monotonicity, $z>0$, target and circle-centroid bias; observability; degenerate cases |
| Procedure | Absent | Developed | Eight-step calibration and rectification procedure with OpenCV initialization and condition check; purpose of each step |
| Mathematics | Developed (model only) | Developed | Relation to Kannala–Brandt and atan2 variants; Newton inversion; rectification map; sampling density; worked examples B (sensitivity) and C (`balance`) |
| Parameters | Shallow | Developed | Nine-row table of flags, criteria, `balance`, `fov_scale`, map type, with the documentation–code disagreement; four-step tuning approach |
| Properties | Absent | Developed | Model family, domain, iterative inversion, no information from rectification, published accuracy with setups |
| Cost and implementation | Shallow | Developed | Cost drivers; published timing with hardware; map memory; six OpenCV 4.13 contracts; execution status |
| Evaluation | Shallow | Developed | Metrics; baseline (pinhole rational) and controlled variation (fisheye) with expected effect and confound; measurement limits |
| Failure modes and diagnosis | Shallow | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Pinhole plus distortion, full KB, unified/double-sphere models, ray-based processing; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/56-calibration-fisheye.py`](checks/56-calibration-fisheye.py) (13 assertions):
60° radii (314.16 versus 519.62 px); small-angle gap $\theta^2/3$; five projection families
at 60° and 90°; $k_4$ sensitivity (2.6e-6, 0.05 and 25.8 px); `balance` example
($f_{\min}=191.5$, $f_{\max}=336.1$, 263.8 px at 0.5, centre sampling 2.61× and 1.49×
coarser, 4.7× edge stretch); corner beyond 90° (91.7°); fold of $\theta_d$ at 104.6° for
$k_1=-0.1$; Newton inversion within 1e-10; 9.83 MB of float maps; RMS 0.66 px.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/56-calibration-fisheye.md),
  revision 6 → 7: body rewritten and deepened as above; decimal commas fixed; appendix
  language fixed identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Why the center is cheating" → "Why the
  centre misleads", "**check**" → "**Discriminating check**", "Interpretation of
  Compromise" → "Interpreting the trade-off", "Documentary reference" → "Source consulted",
  "Local development" → "Series expansion", "Pixel Error and Angular Error" → "Pixel error
  and angular error", "Radius of exit" → "Output ray", "Density of information" →
  "Information density"); sources split; closing provenance line replaced keeping the
  drafting date 2026-10-24. Front matter unchanged except `revision`; H1 and per-card
  headings kept.
- [Cards](../../../vault/50-calibration-geometrie/56-calibration-fisheye.md): the two
  expected-answer fixes above; the explanation and blocking-error fixes listed in the
  findings table and applied word for word in the reference appendices; CV-FISHEYE-005
  received the paragraph "What `balance` computes" (sourced to `fisheye.cpp` L655–L724).
  Source lines now cite the 4.13.0 header and source with lines and Kannala and Brandt
  sections. Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a corrected claim (`rg -i "fisheye|fish-eye"` over `vault/`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FISHEYE-01 | CV-FISHEYE | Explain why OpenCV's `fisheye` model cannot represent rays at or beyond 90° and name a model that can | The validity domain of the implementation is untested and silently bounds 180°+ lenses | Comparison; Problem and Properties | 1 card, 3 criteria ($\theta=\arctan(r)$ with $z>0$; clipping in `undistortPoints`; atan2-based KB or double sphere) | [Usenko et al. §2.4 and §3](https://arxiv.org/abs/1807.08957); [OpenCV 4.13.0 `fisheye.cpp` L129–L138, L443–L446](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fisheye.cpp) |
| P-CV-FISHEYE-02 | CV-FISHEYE | Diagnose a systematic offset with a circle-grid target under strong distortion | Feature bias of circle centroids is untested | Diagnosis; Assumptions and Failure modes | 1 card, 2 criteria (centroid of the projected circle is not the projected centre; remedy) | [Kannala and Brandt §IV-B](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf) |

## Sources

Scientific sources, opened at the passages listed:

- Kannala and Brandt, [author PDF](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf)
  (text extracted with `pdftotext`): §II-A, §II-B, §III, §IV-B, §V-B with Table III.
- Usenko, Demmel and Cremers, [arXiv 1807.08957 PDF](https://arxiv.org/pdf/1807.08957):
  §1, §2.4, §3, §4, §5 with Tables 1–3.

Implementation sources (official code at tag 4.13.0):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L509–L536, L4052–L4098, L4128–L4160, L4192–L4245.
- [`fisheye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/fisheye.cpp): L120–L145, L425–L520, L560–L615, L655–L724, L740–L830, L1490–L1501.

Failed accesses and limits:

- docs.opencv.org returned HTTP 403; the rendered fisheye page is kept as consulted in
  earlier passes. Context7 was not available.
- Not reviewed: Scaramuzza's omnidirectional model and OpenCV's contrib `omnidir`
  module; named in the note as not reviewed.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors (minimum 260 lexical words, set by a card outside this subject) |
| `python3 docs/revues/2026-11-14-reference-depth/checks/56-calibration-fisheye.py` | 13 checks passed |
| `git diff --check -- vault/50-calibration-geometrie/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/56-calibration-fisheye.md` | 5 cards, 371, 377, 381, 314 and 423 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 0 errors; 2 expected answers changed as recorded; front matter identical except `revision: 6` → `7` |
| Local link and anchor check over `vault/50-calibration-geometrie` | 139 local links, 0 errors |

No calibration, OpenCV call or rectification was executed; the baseline and variation are
protocols. Mermaid and tables were not rendered in Obsidian; AnkiDroid rendering is
unverified. This is agent self-review without independent validation. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-FISHEYE
revision 7, CV-FISHEYE-001 to 005, corrections above, Agent Claude Code self-review, to
republish with `paquet-anki`) and the proposal register (P-CV-FISHEYE-01,
P-CV-FISHEYE-02).
