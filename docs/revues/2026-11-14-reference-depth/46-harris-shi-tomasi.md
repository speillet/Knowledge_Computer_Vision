# Review — Harris and Shi–Tomasi — local structure and trackable points — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for structure-tensor corner detectors. Segment-test
detection, ORB's use of the Harris response, scale-space detection and Lucas–Kanade
tracking are linked to their own notes ([CV-FAST-BRIEF](../../../vault/40-features-matching/references/47-fast-brief.md),
[CV-ORB](../../../vault/40-features-matching/references/42-orb.md),
[CV-SIFT](../../../vault/40-features-matching/references/41-sift.md),
[CV-FLOT](../../../vault/100-mouvement-video/references/101-flot-optique.md)) rather
than restated.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CORNERS-001 | Smallest eigenvalue decides 2-D constraint: confirmed by Shi–Tomasi ch. 4 (eq. 4.1, aperture problem) and Harris p. 149 (three cases). $\operatorname{cov}(\hat d)\propto M^{-1}$: correct project derivation under i.i.d. noise, now derived in the reference. Expected answer said "The two directions are constrained", ambiguous for *both* directions; "proper direction", "Diverting", "followability", "large axis" obscured meaning | Reasoning: links eigenvalues to trackability | 2 expected criteria; 387 → 385 lexical words | Numbers match the reference (−308.04, 336; recomputed) | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |
| CV-CORNERS-002 | Harris $\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$ and Shi–Tomasi $\min(\lambda_1,\lambda_2)$: confirmed (Harris p. 150; Shi–Tomasi eq. 4.1; OpenCV `corner.cpp` L52–L155). Contrast powers $\alpha^2$ and $\alpha^4$: confirmed from Harris p. 150 (eigenvalues scale by $p^2$). "his parameter", "coin count", "derivation Scale" | Comparison: score definitions and threshold transfer | 2 expected criteria; 372 → 372 lexical words | Consistent with reference examples A and D | Minor | Language fixes; Source line given primary passages instead of unreadable tutorials |
| CV-CORNERS-003 | Three parameters: confirmed (`imgproc.hpp` L2083–L2135; `featureselect.cpp` L382–L547). French decimal "0,1"; "bound to 10"; "An almost uniform image can have a better low score" garbled the meaning. Missing conditions the practice objective needs: maximum computed inside the mask (L415), stricter effect of the same `qualityLevel` on the Harris score, `maxCorners` documented as unlimited for `<= 0` but asserted `>= 0` (L389), strict `>` threshold, integer positions | Practice: configure a selection | 3 expected criteria; 303 → 391 lexical words | Aligned with the reference parameter table | Minor | Language fixes; one short "Implementation conditions" paragraph added; Source line given header and code lines |
| CV-CORNERS-004 | Strong local corners do not resolve global ambiguity: confirmed as a property of $M$ (Harris p. 149: shape of the autocorrelation at the origin); repeatability denominator from Schmid et al. §3.1. "inlays" (inliers), "boxes" (grid cells), "at register", "a check built" altered or obscured the meaning | Diagnosis: separates detection from association | 3 expected criteria; 385 → 387 lexical words | Consistent with the reference failure table | Minor | Language fixes; Source line given exact passages |
| CV-CORNERS-005 | Count is not a quality measure; survival, coverage and geometry needed: consistent with Shi–Tomasi ch. 5 and ch. 7 (dissimilarity monitoring, non-overlapping windows); protocol and survivor example are project constructions. Expected answer said "dots" and "add noise or redundant dots"; "the piece useful", "balance sheet", "check round trip built" | Evaluation: protocol for a tracking front end | 3 expected criteria; 372 → 378 lexical words | Consistent with the reference controlled variation | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |

Expected-answer changes (meaning-restoring language fixes):

- CV-CORNERS-001: "The two directions are constrained; the first one looks like an
  edge, even if its total gradient is stronger." → "Both directions are constrained;
  the first one behaves like an edge, even though its total gradient is stronger."
- CV-CORNERS-005: "A setting that produces more dots can add noise or redundant
  dots." → "A setting that produces more points can add noisy or redundant points."

## Reference findings

Claims of revision 6 checked against their passages:

- Tensor $M=\sum w\nabla I\nabla I^T$, $E(d)\approx d^TMd$, Harris
  $R=\det M-k\,\mathrm{tr}^2M$: confirmed (Harris 1988, pp. 149–150). The paper gives
  no value of $k$; "0.04" is OpenCV's default (`imgproc.hpp` L2127–L2130), and
  Schmid et al. used 0.06 (§2.2).
- `goodFeaturesToTrack` uses the minimum eigenvalue by default, `qualityLevel` is
  relative to the best score and `minDistance` is in pixels: confirmed
  (`imgproc.hpp` L2083–L2135; `featureselect.cpp` L409–L416, L451–L527).
- Constructed values $R_H(\mathrm{diag}(100,1))=-308.04$, $R_H(\mathrm{diag}(20,20))=336$:
  recomputed.
- The 2026-11-08 appendix cited the OpenCV *video tracking* group for the
  `goodFeaturesToTrack` contract; the function is documented in `imgproc`. Imprecise
  citation, replaced by the 4.13.0 header link.
- The former closing line stated that the OpenCV API was "verified with Context7";
  that verification is not reproducible in this session (Context7 unavailable) and
  the line was replaced as the brief requires.
- No scientific error was found. The body was shallow (one paragraph per merged
  section) and contained machine-translation defects listed below.

New claims verified for revision 7 (main ones):

- Harris: three cases and Moravec's defects (p. 149); Gaussian window and derivative
  $(-1,0,1)$ (p. 149); eigenvalues proportional to the principal curvatures and
  rotation-invariant, contrast factor $p^2$ (pp. 149–150); response signs and flat
  region by trace (pp. 150–151); 8-way local maxima (p. 151); motivation from the
  aperture problem and edge fragmentation (pp. 147–148).
- Shi–Tomasi (TR 93-1399): good feature defined by the tracker, "optimal by
  construction" (abstract, ch. 4); eq. 2.1 and its validity at surface markings
  (ch. 2); $Zd=e$, eq. 3.10 (ch. 3); eq. 4.1, noise and conditioning argument,
  threshold halfway between bounds, "not critical", confidence ellipse (ch. 4); twig
  junction and dissimilarity monitoring (ch. 5); non-overlapping $25\times25$
  windows and aliasing (ch. 7); rigidity "not a local feature" (ch. 8).
- Schmid, Mohr and Bauckhage 2000: Harris implementations, $k=0.06$, Gaussian
  $\sigma=2$, 1% threshold, 3×3 suppression, improved Harris with Gaussian
  derivatives $\sigma=1$ (§2.2); repeatability definition and $\min(n_1,n_i)$
  denominator (§3.1); 10 px mean spacing and $\varepsilon=1.5$ (§3.3); standard
  Harris worst near 45° (§3.3.1); 91%/89% under rotation (§3.3.2, Fig. 7 caption);
  54%/1% under scale changes 1.5/4.1 and "very poor" beyond 1.5 (2) (§3.3.3,
  Fig. 11 caption); information content (§4).
- OpenCV 4.13.0: input types and derivative scaling $1/(2^{k-1}\cdot b)$, ×1/2 for
  Scharr, ×1/255 for 8-bit, unnormalized box filter (`corner.cpp` L247–L254,
  L313–L314); score formulas (L52–L155); `goodFeaturesToTrack` assertions,
  `THRESH_TOZERO`, dilation, border skip, deterministic sort, grid spacing, output
  type, disabled OpenVX path (`featureselect.cpp` L55–L60, L382–L547); prefix
  property (`imgproc.hpp` L2100–L2102); `calcOpticalFlowPyrLK` defaults and
  `minEigThreshold` (`video/tracking.hpp` L134–L186).

Disagreements between documentation and implementation (FR-036):

| Aspect | Header documentation | OpenCV 4.13.0 code |
| --- | --- | --- |
| `maxCorners` | "`maxCorners <= 0` implies that no limit" (`imgproc.hpp` L2107) | `CV_Assert(... maxCorners >= 0)`: a negative value throws (`featureselect.cpp` L389) |
| Threshold equality | Corners "less than the product are rejected" (L2112–L2114) | `THRESH_TOZERO` keeps only values strictly greater (L416; `imgproc.hpp` L329) |
| Parameter name | "stronger corner at a distance less than maxDistance" (L2095–L2096) | The parameter is `minDistance`; strict `<` test (L500) |
| Harris paper vs OpenCV | Gaussian window (Harris p. 149) | Unnormalized box window of `blockSize` (`corner.cpp` L313–L314) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 497 → 4,381. The
body includes the Mermaid diagram, the pseudocode, three tables and four worked
examples; the per-card appendices were language-corrected but not extended.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task from both papers; input types, coordinate convention, intermediate maps, output types and integer positions; score units; pipeline roles; selection/tracker window mismatch and LK's own gate |
| Intuition | Shallow | Developed | Three cases from Harris; eigenvectors as change directions; constructed road-scene illustration with the sources' twig and reflection counterexamples; Mermaid data flow of `goodFeaturesToTrack` |
| Prerequisites | Shallow (two links) | Developed | Links by mechanism to CV-FILTRES, CV-SVD, CV-FLOT, CV-ACQUISITION, CV-CANNY-HOUGH, CV-HOMOGRAPHIE; competencies restated in English |
| Assumptions | Shallow (two sentences) | Developed | Translation and brightness constancy, single scale (Schmid §3.3.3), rotation and discrete masks (§3.3.1), contrast, noise floor; observability (aperture, repeated patterns); degenerate cases and border handling |
| Procedure | Shallow (one sentence) | Developed | Pseudocode faithful to OpenCV 4.13 and the purpose of each of seven steps |
| Mathematics | Shallow | Developed | Derivation of $M$ with units; eigenvalues; Harris response and its regions; Shi–Tomasi eq. 4.1 and threshold rule; worked examples A (sign and $k$), B (worst-direction error $\sigma/\sqrt{\lambda_2}$), C (OpenCV score units, localization offset), D (relative threshold under mixed contrast) |
| Parameters | Shallow | Developed | Eight-row table with source values, effects and interactions; packing limit for `minDistance`; five-step tuning approach |
| Properties | Absent (merged) | Developed | Rotation, contrast and offset, translation, scale and viewpoint with published repeatability, localization, scope of "optimal by construction", distinctiveness |
| Cost and implementation | Shallow (one sentence) | Developed | Cost per stage with named variables; OpenCV 4.13 contracts for `cornerMinEigenVal`, `cornerHarris`, `goodFeaturesToTrack`, prefix property and `calcOpticalFlowPyrLK`; execution status |
| Evaluation | Shallow | Developed | Repeatability protocol (Schmid §3.1), tracking metrics, published results with their conditions; proposed baseline and per-cell quota variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (four sentences) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow (one sentence) | Developed | Conditional choices (Shi–Tomasi, Harris, FAST, SIFT/ORB, learned matching, direct registration); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/46-harris-shi-tomasi.py`](checks/46-harris-shi-tomasi.py) (18 assertions):
card values (−308.04, 336), Harris sign boundary ($\lambda_2/\lambda_1>0.0436$ for
$k=0.04$, 0.0685 for $k=0.06$; homogeneity; $k<1/4$), worst-direction deviations
(0.1, 1.0 and 0.2236 px), OpenCV-scaled tensors of an ideal step ($A=2/3$,
$R_H=-0.0178$) and corner ($A=B=13/36$, $C=1/9$, $\lambda_2=1/4$, $R_H=0.0972$, maximum at
pixel $(0,0)$, 0.71 px offset, factors $255^2$ and $255^4$ for float input), mixed
contrast (0.0246 kept, 0.000605 rejected, 25.5 and 80.6 levels) and the packing limit
(26.6 px for 500 points in $640\times480$; 3,547 points at 10 px).

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/46-harris-shi-tomasi.md),
  revision 6 → 7: body rewritten and deepened as above. Appendix language fixes,
  applied identically to the cards: "Question of work" → "Working question",
  "Reference Response" → "Reference answer", "proper direction" → "direction",
  "Lucas – Kanade follow-up" → "Lucas–Kanade tracking", "smallest binding term" →
  "smallest eigenvalue, which is the weakest constraint", "dots" → "points",
  "the piece useful" → "the useful part of the object", "Protocol built" →
  "Constructed protocol", "space quotas" → "spatial quotas", "Diverting the local
  tensor" → "Deriving the local tensor", "large axis" → "major axis", "followability"
  → "trackability", "not two new proofs of identity of the point" → "neither is
  evidence of the point's identity", "Removing maxima and spacing remain separate
  steps of these formulas" → "Non-maximum suppression and spacing are separate
  steps, outside these formulas", "suite of filters" → "sequence of filters", "In a
  built-in case ... can get a lot" → "In a constructed case ... can reject many of
  them", "box" → "grid cell", "check round trip built" → "Constructed forward–backward
  check", "balance sheet" → "tally", "Reliable monitoring and refusal policy" →
  "Tracking reliability and the rejection policy". Appendix citation of the video
  tracking group replaced by the `imgproc.hpp` link. Sources split into scientific
  and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/46-harris-shi-tomasi.md): the two
  expected-answer changes quoted above; in further explanations and blocking errors,
  the appendix fixes plus "his parameter" → "its parameter", "no formula imposes a
  better performance on any stage" → "neither formula guarantees better performance
  at every stage", "derivation Scale" → "Scale derivation", "coin count" → "corner
  count", "0,1" → "0.1", "bound to 10" → "is 10", "An almost uniform image can have
  a better low score" → "in an almost uniform image even the best score is low",
  "space cover" → "spatial coverage", "Set each stress" → "Set each constraint",
  "raise the absolute scores" → "record the absolute scores", "inlays cover the
  surface at register" → "inliers cover the surface to be registered", "Compare period
  offset assumptions" → "Compare hypotheses shifted by one period", blocking errors
  rewritten as gerunds. CV-CORNERS-003 gains one "Implementation conditions" paragraph
  (mask maximum, Harris scaling of `qualityLevel`, `maxCorners` assertion, integer
  positions). All five Source lines now cite exact passages of Harris 1988,
  Shi–Tomasi TR 93-1399, Schmid et al. 2000 or OpenCV 4.13.0 code. Questions, IDs,
  objectives, families, tags and target deck unchanged.

`rg -n -i "harris|shi.tomasi|goodFeaturesToTrack|qualityLevel" vault/` found no other
subject repeating a claim corrected here; the CV-MATCHING and CV-ORB mentions are
consistent and belong to subjects reviewed later in this run.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-CORNERS-01 | CV-CORNERS | Given $k=0.04$, state which eigenvalue ratio separates positive from negative Harris responses and explain why a global contrast change does not move that boundary | The role of $k$ is untested; cards only use the isotropic case | Algorithm; Mathematics, worked example A | 1 card, 3 criteria (ratio equation, 0.0436, homogeneity of degree 2) | [Harris and Stephens 1988, p. 150](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf) |
| P-CV-CORNERS-02 | CV-CORNERS | Choose the selection window and score for a pyramidal Lucas–Kanade front end, and explain why Shi–Tomasi's "optimal by construction" argument needs the tracker's own window | Absent design family; selection–tracker coupling (OpenCV selects on $3\times3$, tracks $21\times21$) | Design; Problem and Properties | 1 card, 3 criteria | [Shi and Tomasi, ch. 3–4](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf); [OpenCV 4.13.0 `video/tracking.hpp` L134–L186](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp#L134-L186) |

No existing proposal in the register or in earlier reports concerns this subject.
No question was found defective.

## Sources

Scientific sources, opened at the passages listed:

- Harris and Stephens 1988, [BMVA archive PDF](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf)
  (text extracted with `pdftotext`): pp. 147–151, all sections.
- Shi and Tomasi, [Cornell TR 93-1399 PDF](https://users.cs.duke.edu/~tomasi/papers/shi/TR_93-1399_Cornell.pdf)
  (text extracted with `pdftotext`): abstract, ch. 1–5, ch. 7 opening and aliasing
  paragraph, ch. 8. The CVPR 1994 version was not opened (the Clemson mirror failed
  certificate verification); the technical report is its extended version.
- Schmid, Mohr and Bauckhage 2000, [HAL inria-00548302](https://inria.hal.science/inria-00548302v1)
  (text extracted with `pdftotext`): §2.2, §3.1, §3.3, §3.3.1–§3.3.3, §3.4, §4
  headings.

Implementation sources (official code at tag 4.13.0, fetched from
`raw.githubusercontent.com`):

- [`modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L329, L1943–L2167.
- [`modules/imgproc/src/corner.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/corner.cpp): L52–L155, L237–L321, L550–L572, L634–L654.
- [`modules/imgproc/src/featureselect.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/featureselect.cpp): L55–L60, L382–L547.
- [`modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): L134–L186.
- [`modules/core/include/opencv2/core/base.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/include/opencv2/core/base.hpp): L337–L341.

Failed accesses and limits:

- docs.opencv.org/4.13.0 tutorials (Harris, Shi–Tomasi) were not re-read (HTTP 403
  reported for this pass); the links are retained in the note as not re-read, and API
  claims rely on the 4.13.0 headers and sources.
- Context7 was not available in this session; official versioned code replaced it.
- Not verifiable here: the CVPR 1994 paper itself (see above); Kalal et al.'s
  forward–backward error, which the 2026-10-30 appendix presents as a constructed
  check without citing it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/46-harris-shi-tomasi.py` | 18 checks passed |
| `git diff --check` on the three files of this subject | No whitespace error |
| `inventaire_cartes.py vault/40-features-matching/46-harris-shi-tomasi.md` | 5 cards, 372–391 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 6` → `7`; H1 and per-card headings unchanged; `$$` balanced |

No OpenCV call or image experiment was executed; the worked examples are recomputed
analytic or simulated calculations, and the proposed baseline and variation are
protocols, not results. The Mermaid diagram, tables and equations were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-CORNERS revision 7, CV-CORNERS-001 to 005, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-CORNERS-01, P-CV-CORNERS-02).
