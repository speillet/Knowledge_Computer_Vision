# Review — MeanShift and CamShift — tracking an appearance distribution — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

Every card and the reference cited only the OpenCV MeanShift/CamShift tutorial, which
returned HTTP 403 in this pass and does not cover the kernel-based formulation. The
note and cards now rely on the kernel-based tracking paper, Bradski's CAMSHIFT patent
and the OpenCV 4.13.0 sources.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MEANSHIFT-001 | Centroid step and undefined centroid at zero mass: confirmed (OpenCV `camshift.cpp` L83–L90; Comaniciu et al. eq. 13). Missing condition: OpenCV stops silently on zero mass and keeps the window (L86–L87), so the caller must test $M_{00}$. "digital output", "advertised search" mistranslated | Algorithm: one iteration and its degenerate case | 2 criteria; 385 → 417 words | Aligned with the reference appendix | Minor | Condition added to the further explanation; language fixes; Source replaced |
| CV-MEANSHIFT-002 | MeanShift keeps a fixed window, CamShift adapts size and orientation from moments: confirmed (`tracking.hpp` L88–L107; `camshift.cpp` L144–L181). "The timings of the distribution" mistranslated *moments*; "pose 3D", "dispersion 2D" word order | Comparison: fixed versus adaptive window | 2 criteria; 388 → 433 words | Aligned | Minor | Language fixes; OpenCV ±2σ box convention added; Source replaced |
| CV-MEANSHIFT-003 | Same-colour parts are indistinguishable to a histogram and more iterations converge on the current basin: consistent with the unique-maximum assumption (Comaniciu et al. §4.2). Expected answer said "pieces" and "target/bottom separation" (background) | Diagnosis: model ambiguity versus iteration budget | 3 criteria; 378 → 384 words | Aligned | Important (meaning-altering term in the expected answer) | Expected answer fixed; language fixes; Source replaced |
| CV-MEANSHIFT-004 | One-factor ablation of adaptation and histogram: project protocol, consistent with the sources. "make the shade little informative" (hue), "Experience built" (constructed experiment), "reserved data" (held-out) | Evaluation: attributable comparison | 2 criteria; 299 → 302 words | Aligned | Minor | Language fixes; Source replaced |

Expected-answer change (CV-MEANSHIFT-003, meaning-restoring language fix): "The
histogram model does not necessarily distinguish the two pieces. More iterations may
converge more towards the wrong concentration. Inspect the backprojection, ROI, and
target/bottom separation before setting the stop." → "The histogram model does not
necessarily distinguish the two parts. More iterations may converge more firmly on the
wrong concentration. Inspect the backprojection, the ROI and the target/background
separation before tuning the stopping criterion."

## Reference findings

Revision 6 claims checked: the centroid formula and the 13 px example are correct; "in
the usual MeanShift tracker, the window size remains fixed" is confirmed for OpenCV
(`tracking.hpp` L88–L107), whereas the kernel-based tracker adapts its bandwidth
(Comaniciu et al. §4.3). The revision-6 body did not distinguish the kernel-based
tracker from back-projection tracking, and had mistranslations ("pose 3D", "the
choice of stimulus", "Analytical example of the project").

New verified content: Comaniciu et al. eqs. 2–7, 8–11, 12–14, the 1-pixel and
$N_{\max}=20$ stopping rule with about 4 iterations, the basin of attraction, the
unique-maximum assumption, saddle points, the 0.1% non-increase observation, the
$\pm10\%$ scale search with smoothing 0.1, the cost model (24× fewer operations for a
$50\times50$ target), 150 frames/s on a 1 GHz PC, and RGB $16^3$ bins. OpenCV 4.13.0:
integer shifts and the rounded $\epsilon^2$ test, window clipping, silent stop on zero
mass, CamShift's 10-pixel margin, $4\sqrt{\lambda}$ box size, angle in $[0,180)$
degrees, next window = box extent + 2 px, empty `RotatedRect` on zero mass;
`calcBackProject` contract; the sample's mask ($S\ge60$, $V\ge32$), 16 hue bins and
stopping criteria (10 iterations, 1 px).

Source disagreement recorded (FR-036): Bradski's patent sizes the window from the
square root of the zeroth moment, whereas OpenCV 4.13 sizes the box from the second
moments ($4\sqrt{\lambda}$) and the next window from the box extent.

## Reference depth

Body word counts (whitespace tokens, front matter excluded, H1 included, before the
first per-card appendix): 424 → 2,859.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Two formulations; HSV and back-projection data contract with value ranges; outputs of both OpenCV functions and of the kernel tracker; pipeline role |
| Intuition | Shallow | Developed | Voting weights, $\sqrt{q_u/p_u}$ interpretation, constructed centroid illustration |
| Prerequisites | Developed (two links) | Developed | Link to CV-MORPHO for moments and components |
| Assumptions | Shallow | Developed | Basin of attraction, unique maximum, reliable hue (patent thresholds), small appearance change, no layout; zero mass, round blob, empty bins, saddle points |
| Procedure | Shallow | Developed | OpenCV CamShift pipeline and kernel-tracker algorithm in pseudocode, purpose of each step |
| Mathematics | Shallow | Developed | Back-projection centroid with OpenCV's integer test; eqs. 2, 4, 6–7, 10–11, 13; CamShift moment formulas; worked Bhattacharyya example and CamShift box and growth example |
| Parameters | Shallow | Developed | Seven-row table with source values; tuning approach |
| Properties | Shallow | Developed | Local optimum, invariances, convergence observation, geometry of the box, no identity |
| Cost and implementation | Shallow | Developed | Cost model and reported speed; OpenCV `meanShift`, `CamShift`, `calcBackProject` contracts; execution status |
| Evaluation | Shallow | Developed | MeanShift baseline and CamShift as the single controlled variation, measurements, limits |
| Failure modes and diagnosis | Shallow | Developed | Six-row symptom table |
| Alternatives and sources | Shallow | Developed | Conditional choices, industrial uses labelled as project reasoning, scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/115-meanshift-camshift.py`](checks/115-meanshift-camshift.py) (7 checks):
centroid 13 px and its behaviour under scaling (13) and offset (12.67); CamShift box
$46.2\times23.1$ px for a uniform $40\times20$ px blob; window growth 40 → 71.3 →
107.4 → 149.1 → 197.2 px on a uniform field; equal eigenvalues for a disc;
Bhattacharyya coefficient 0.816, distance 0.429 and weights 1.581 / 1 / 1 / 0.

## Applied corrections

- [Reference](../../../vault/110-tracking-association/references/115-meanshift-camshift.md),
  revision 6 → 7: body rewritten as above; appendix language fixes identical to the
  card fixes ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "Experience built" → "Constructed experiment", "digital output"
  → "numerical output", "advertised search" → "declared search policy", "reserved
  data" → "held-out data", eigenvalue and 2-D/3-D wording); tutorial links replaced by
  OpenCV 4.13.0 source links; sources split; closing line replaced.
- [Cards](../../../vault/110-tracking-association/115-meanshift-camshift.md): expected
  answer of 003 as quoted above; one implementation condition added to the further
  explanations of 001 (silent zero-mass stop) and 002 ($\pm2\sigma$ box); language
  fixes in all four cards, including blocking errors ("Assimilate convergence of
  MeanShift and good identity" → "Equating MeanShift convergence with correct
  identity", "Confound box oriented 2D and orientation 3D" → "Confusing a 2-D oriented
  box with a 3-D orientation"); all Source lines replaced by verifiable sections.
  IDs, questions, objectives, families, tags and deck unchanged.

No other subject's card repeats a corrected claim.

## Proposals

To register as `pending` (register not edited in this pass):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-MEANSHIFT-01 | CV-MEANSHIFT | Explain why OpenCV's CamShift window can grow frame after frame over a same-colour background, with the $4\sqrt{\lambda}$ box and the 10 px margin | The mechanism of window blooming is described in no card; it turns a parameter-free method into a predictable failure | Reasoning; Mathematics example B | 1 card, 3 criteria | [OpenCV 4.13.0 camshift.cpp L115–L203](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L115-L203) |
| P-CV-MEANSHIFT-02 | CV-MEANSHIFT | Distinguish the kernel-based tracker (Bhattacharyya similarity, weights $\sqrt{q_u/p_u}$) from back-projection tracking, and state what each weight rewards | No card tests the original mean-shift tracking criterion; cards cover only the back-projection centroid | Understanding; Mathematics | 1 card, 3 criteria | [Comaniciu et al. 2003, §§3–4, eqs. 7, 10, 13](https://www.cs.ucf.edu/courses/cap6412/2003/Kernel-based%20object%20tracking.pdf) |

No defective question was found.

## Sources

Scientific sources (texts extracted locally):

- Comaniciu, Ramesh and Meer 2003, [Kernel-based object tracking](https://www.cs.ucf.edu/courses/cap6412/2003/Kernel-based%20object%20tracking.pdf), course-hosted copy of the TPAMI paper: §2.1–2.3, §3, §4.1–4.4, §5 (Football sequence and settings).
- Comaniciu, Ramesh and Meer 2000, [CVPR paper](https://comaniciu.net/Papers/MsTracking.pdf): downloaded; only identified as the preliminary version, no claim relies on it.
- Bradski, [US patent 6,394,557 B2](https://patents.google.com/patent/US6394557B2/en), read through WebFetch (summarized extraction, partly garbled equations): window size proportional to the square root of the zeroth moment, steps of the method, saturation and value thresholds 20 and 15 as examples.

Implementation sources (OpenCV at tag 4.13.0):
[`modules/video/src/camshift.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/camshift.cpp#L44-L218),
[`modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp#L64-L107),
[`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L3322-L3360),
[`samples/python/camshift.py`](https://github.com/opencv/opencv/blob/4.13.0/samples/python/camshift.py#L82-L102).

Not verifiable: Bradski, Intel Technology Journal Q2 1998 (wisc.edu copy returns 404,
no archived snapshot); the OpenCV MeanShift tutorial on docs.opencv.org (HTTP 403).
The patent's exact equation constants (the factor applied to $\sqrt{M_{00}}$) were not
read reliably and are not stated in the note. Context7 unavailable.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | Fails only on `40-features-matching/references/46-harris-shi-tomasi.md` (another subject in progress): `missing local link … $$E(d)=\sum_p`; no error in the files of this subject |
| `python3 scripts/learning_path.py` | OK, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/115-meanshift-camshift.py` | 7 checks passed |
| `git diff --check -- vault/110-tracking-association/` | No whitespace error |
| Inventory of the card file | 4 cards, 417 / 433 / 384 / 302 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical (33); front matter identical except `revision`; H1 and `### CV-…` headings unchanged; `$` balanced |

No tracker was executed. Obsidian and AnkiDroid rendering are unverified. Agent
self-review, without independent validation or measured learner proficiency. Export
status: **to republish with `paquet-anki`**.

For the coordinator: `Suivi-pilote.md` entry — 2026-11-14, CV-MEANSHIFT revision 7,
cards 001–004, corrections above, Agent Claude Code self-review, to republish with
`paquet-anki`; proposals P-CV-MEANSHIFT-01 and -02.
