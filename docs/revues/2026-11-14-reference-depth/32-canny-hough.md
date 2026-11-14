# Review — Canny and Hough: edges, lines and segments — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for the edge-then-vote route to lines. Derivative
kernels stay in
[CV-FILTRES](../../../vault/30-traitement-image/references/31-filtrage-gradients.md);
robust fitting in
[CV-HOMOGRAPHIE](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md).
The reference's sources section is now headed "## Sources" (its former heading
"Sources and flashcards" was not a link target; the `#sources` links of the progress
log point to the 2026-11-08 report, not to this note).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CANNY-HOUGH-001 | Hysteresis keeps weak pixels connected to strong seeds: confirmed for OpenCV ("the smallest value … is used for edge linking. The largest value is used to find initial segments of strong edges", imgproc.hpp L1903–L1907) and by the toy chain of worked example A; Canny's own hysteresis section not accessible (abstract only). Expected answer "related to strong ones" (*reliées* = connected); "certain small portions" (*faibles* = weak), "strong primer", "hysteresis as a journey", "the direction of the thresholds" (*sens* = meaning) | Algorithm: two-threshold linking and its failure modes | 1 criterion; 374 → 377 lexical words | Consistent with reference worked example A | Minor | Meaning-restoring fix of the expected answer; language fixes; Source replaced by `imgproc.hpp` and the Canny abstract |
| CV-CANNY-HOUGH-002 | Normal parameterization, signed $\rho$, uniqueness for $\theta\in[0,\pi)$: confirmed (Duda and Hart §2); OpenCV origin at the top-left corner and "0 ~ vertical line" (L2174–L2206); 8.7 px at 500 px and 120 px after the crop offset recomputed. Expected answer "the angle of normal", "convention announced"; "Couples", "leverage", "8,7 px" | Reasoning: read line parameters in a coordinate frame | 2 criteria; 417 → 421 lexical words | Consistent with reference mathematics | Minor | Language fix of the expected answer; language fixes; Source cites Duda and Hart and the OpenCV output contract |
| CV-CANNY-HOUGH-003 | An accumulator peak defines an infinite line; Duda and Hart note that collinear points are found "without regard to contiguity" (§4); `HoughLinesP` returns end points (L2208–L2238). Expected answer began "Sets a straight line" (*Elle paramètre une droite* = it parameterizes an infinite line); "extending a straight out of support", "direction of the right" (*droite* = line), "Find a Finished Support" | Comparison: line model versus observed segment | 1 criterion; 370 → 374 lexical words | Consistent with the reference segment-support construction | Minor | Meaning-restoring fix of the expected answer; language fixes; Source cites Duda and Hart §4 |
| CV-CANNY-HOUGH-004 | Texture votes and false lines when thresholds are lowered: consistent with Duda and Hart §4 ("meaningless groups of colinear points"); the normal-consistency check is a project proposal. Expected answer "Inspect map Canny"; "business lines/constraints/edge" (*métier*), "Overlapping the lines … to the image", "on her support points" | Diagnosis: separate texture support from structure | 1 criterion; 371 → 371 lexical words | Consistent with the reference evaluation protocol | Minor | Language fix of the expected answer; language fixes; Source cites Duda and Hart §4 |

Expected-answer changes (meaning-restoring language fixes, checked against the
pre-migration French text `git show b7142bb^:vault/30-traitement-image/32-canny-hough.md`):

- CV-CANNY-HOUGH-001: "… when they are related to strong ones according to
  hysteresis." → "… when they are connected to strong ones according to hysteresis."
- CV-CANNY-HOUGH-002: "… $\theta$ is the angle of normal in radians, according to the
  convention announced." → "… $\theta$ is the angle of the line's normal in radians,
  according to the stated convention."
- CV-CANNY-HOUGH-003: "Sets a straight line; support limits must be estimated
  separately or with a segment variant like HoughLinesP." → "It parameterizes an
  infinite line; the limits of its support must be estimated separately or with a
  segment variant such as HoughLinesP."
- CV-CANNY-HOUGH-004: "Inspect map Canny, angular distribution, useful region and
  spatial support of candidates." → "Inspect the Canny edge map, the angular
  distribution, the useful region and the spatial support of candidates."

Defective protected field (not edited; objective lines are invariants):
CV-CANNY-HOUGH-003 objective "Distinguish between right and segment." (*droite* =
straight line). Proposed: "Distinguish an infinite line from a segment." No defective
question was found.

## Reference findings

Claims of revision 7 checked:

- $\rho=x\cos\theta+y\sin\theta$ with $\rho$ in pixels and $\theta$ in radians:
  confirmed (Duda and Hart §2; OpenCV `HoughLines`).
- "Do not promise a Gaussian smoothing 5×5 internal to each Canny API": confirmed and
  sharpened: OpenCV 4.13 `Canny` computes Sobel derivatives with `BORDER_REPLICATE`
  and performs no Gaussian smoothing (canny.cpp L368–L377); the tutorial's smoothing
  step is a pipeline step, not part of the function.
- "Its norm L1 or L2 is not the same score": confirmed; L1 is OpenCV's default, and
  with L2 the thresholds are squared internally.
- "A probabilistic variant reduces labor under its assumptions": confirmed in the code
  (random order, points of accepted segments removed from the accumulator).
- No scientific error found. The body was shallow (326 words) and contained
  mistranslations: "a straight line is not a segment" (kept, meaningful), "his
  assumptions", "business geometric constraint", "check first outlines", "Question of
  work", "Reference Response", "Describe hysteresis as a journey", "Find a Finished
  Support", "Differentiating Vote and Adjustment Error".

New claims verified for revision 8 (main ones):

- Duda and Hart 1972: normal parameterization and its uniqueness (§2, eq. 1,
  properties 1–4); accumulator over $0\le\theta<\pi$, $-R\le\rho\le R$, cost $n d_1$
  versus $n(n-1)/2$ (§3); example with 20° bins and the missed line, sensitivity to
  quantization, collinearity "without regard to contiguity", false line when the
  threshold drops from 35 to 24 (§4); circles as cones in $(a,b,c)$ (§5).
- Canny 1986: abstract only (three criteria, detection–localization trade-off, edges
  at maxima of gradient magnitude of a Gaussian-smoothed image).
- OpenCV 4.13.0: `Canny` contract and threshold roles; `CV_8U` input; aperture odd 3–7
  or Scharr; aperture 7 divides thresholds and gradients by 16; thresholds swapped if
  needed and squared with L2; `TG22 = 13573`; `HoughLines` output convention, strict
  `> threshold`, 4-neighbour local maxima, $\rho\in[-(W+H),W+H]$; `HoughLinesP`
  algorithm and fixed random seed.

Paper versus implementation (FR-036): the `HoughLinesP` documentation states that
lines need "enough votes (> threshold)", whereas the code rejects a candidate only
when `max_val < threshold`, i.e. it accepts a peak equal to the threshold
(hough.cpp L603–L605); and its minimum-length test uses the larger of $|\Delta x|$ and
$|\Delta y|$, not the Euclidean length (L673–L674). Both are recorded in the note.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 326 → 3,175. About
600 tokens are tables, the pseudocode and the Mermaid diagram. The length comes from
two algorithms (Canny, Hough) and the segment step that joins them to measurements.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Inputs and outputs of Canny, standard and probabilistic Hough with types; OpenCV origin and angle conventions; pipeline role upstream and downstream |
| Intuition | Shallow | Developed | Canny criteria, suppression, hysteresis, voting as concurrent curves, votes versus segments; constructed carton illustration; Mermaid pipeline |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-ACQUISITION, CV-HOMOGRAPHIE, CV-MORPHO |
| Assumptions | Absent (merged) | Developed | Edge model and scale, photometric edges, straightness and distortion, contiguity, quantization; observability and degenerate cases |
| Procedure | Shallow | Developed | Pseudocode for Canny, voting and support checking with the purpose of each step |
| Mathematics | Shallow | Developed | Norms and direction; OpenCV suppression constant; thresholds in DN; normal parameterization and cost; $\rho$ sensitivity; change of origin and scale; segment support; worked examples A (hysteresis) and B (accumulator size) |
| Parameters | Shallow (list) | Developed | Nine-row table with units and a tuning approach |
| Properties | Shallow | Developed | Model-relative optimality, hysteresis as connectivity, robustness and blindness of voting, counts versus probabilities, frame dependence, extension to curves |
| Cost and implementation | Shallow | Developed | Cost drivers; OpenCV 4.13 contracts with code-level details and the documentation/code disagreement; execution status |
| Evaluation | Shallow | Developed | Edge and line metrics; proposed normal-consistency variation at equal recall with a confound; limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (Canny, standard and probabilistic Hough, robust fit, segment detector, priors); industrial uses labelled as project reasoning; sources split into scientific and implementation sources under a "Sources" heading |

Constructed examples are recomputed by
[`checks/32-canny-hough.py`](checks/32-canny-hough.py) (17 checks): hysteresis on two
chains, strength versus connectivity, single-threshold alternatives and a bridge;
Sobel response $4h$ to a step and thresholds 100/200 as 25/50 DN; L1 versus L2 on a
diagonal; `TG22`; threshold squaring; 8.7 px angular error; $(\rho,\theta)$ versus
$(-\rho,\theta+\pi)$; crop offset 120 px; axis cases; 180 × 4001 accumulator and
2.9 MB; 9 million votes; segment splitting at gaps; the `HoughLinesP` length test on a
diagonal.

## Applied corrections

- [Reference](../../../vault/30-traitement-image/references/32-canny-hough.md),
  revision 7 → 8: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Describe hysteresis as a journey" → "Describe
  hysteresis as a graph traversal", "Find a Finished Support" → "Find a finite
  support", "Differentiating Vote and Adjustment Error" → "Distinguishing votes from
  fitting error", "8,7 px" → "8.7 px"); sources split into scientific and
  implementation sources under "## Sources"; closing provenance line replaced. Front
  matter unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/30-traitement-image/32-canny-hough.md): four expected answers
  fixed as quoted above. Other language fixes: "Removing non-maxima thins the answers"
  → "Non-maximum suppression thins the responses"; "certain small portions" → "weak
  portions"; "without a strong primer" → "has no strong seed"; "Browse their
  neighbors … This diagram … a long, small portion" → "Visit their neighbors … This
  scheme … a long, weak portion"; "digital depth" → "bit depth"; "the direction of the
  thresholds" → "the meaning of the thresholds"; "vote for several couples" → "votes
  for several pairs"; "grows with distance at the origin" → "grows with the distance
  from the origin along the line"; "At a leverage of 500 px" → "At a lever arm of
  500 px"; "extending a straight out of support" → "extending a line beyond its
  support"; "the direction of the right" → "the direction of the line"; "without
  check of image and uncertainty" → "without checking the image and the uncertainty";
  "business lines/constraints/edge" → "task-relevant lines", "the task's geometric
  constraints", "task-relevant edge"; "Overlapping the lines … to the image" →
  "Overlay the lines … on the image"; "on her support points" → "of its support
  points"; blocking errors turned into gerunds. Source lines: unreachable tutorials
  replaced by Duda and Hart, the Canny abstract and versioned OpenCV headers.
  Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`HoughLines`, `hysteresis`, `Canny`); CV-FILTRES and CV-CORNERS use gradient
conventions consistent with this note.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run).

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-CANNY-HOUGH-01 | CV-CANNY-HOUGH | Convert Canny thresholds into edge contrast: for a 3×3 Sobel and the L1 norm, which step heights do thresholds 100 and 200 select, and what changes with L2, aperture 7 or a prior blur | Thresholds are tuned blindly; no card links them to image units and implementation scaling | Practice (absent family); Mathematics | 1 card, 3 criteria | [OpenCV 4.13.0 canny.cpp L368–L377, L785–L816](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/canny.cpp#L762-L832); [imgproc.hpp Sobel](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1765-L1810) |

## Sources

Scientific sources:

- Duda and Hart 1972, read in the scanned journal copy at
  [cse.unr.edu](https://www.cse.unr.edu/~bebis/CS474/Handouts/HoughTransformPaper.pdf)
  (DOI 10.1145/361237.361242, confirmed through Crossref): §2, §3, §4 and §5.
- Canny 1986: abstract only, through a bibliographic record
  ([Magdeburg bibliography entry](https://isgwww.cs.uni-magdeburg.de/~stefans/npr/entry-Canny-1986-ACA.html));
  DOI 10.1109/TPAMI.1986.4767851 confirmed through Crossref.

Implementation sources (OpenCV at tag 4.13.0):

- [`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L1903–L1942, L2174–L2238.
- [`modules/imgproc/src/canny.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/canny.cpp): L360–L380, L530–L620, L762–L832.
- [`modules/imgproc/src/hough.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/hough.cpp): L70–L110, L119–L235, L489–L735.

Failed accesses and limits:

- Canny 1986 full text: the Clemson course copy failed TLS verification (curl and
  WebFetch); no other open copy was found. Claims about Canny's hysteresis section,
  recommended threshold ratios or noise-based threshold selection are therefore not
  made; hysteresis is described from OpenCV's documentation and code.
- Matas, Galambos and Kittler 2000 (progressive probabilistic Hough): not consulted;
  the note describes the OpenCV implementation only.
- docs.opencv.org Canny and Hough tutorials: HTTP 403, retained as not re-read.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/32-canny-hough.py` | 17 checks passed |
| `git diff --check -- vault/30-traitement-image/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/30-traitement-image/32-canny-hough.md` | 4 cards, 377, 421, 374 and 371 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; a "## Sources" heading present |
| Local links and anchors under `vault/30-traitement-image` and `vault/01-Parcours` | 0 errors |

No edge detector, Hough transform or image experiment was executed; the proposed
baseline and variation are protocols, not results. The Mermaid diagram and tables were
not rendered in Obsidian, and AnkiDroid rendering of the corrected cards is unverified.
This is agent self-review, without independent scientific validation or measurement
of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-CANNY-HOUGH revision 8, CV-CANNY-HOUGH-001 to -004, corrections listed above, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-CANNY-HOUGH-01).
