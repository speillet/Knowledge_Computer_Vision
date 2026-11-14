# Review — Farnebäck — dense optical flow through polynomial expansion — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The original paper, unreachable in earlier passes (DiVA timeout, then proxy refusal in
this pass), was read in full from the author's copy at Linköping University. The
general flow problem, Lucas–Kanade and RAFT stay in
[CV-FLOT](../../../vault/100-mouvement-video/references/101-flot-optique.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FARNEBACK-001 | Quadratic expansion, coefficient change under translation, aggregation, multi-scale refinement, $2Ad=b_1-b_2$: confirmed (Farnebäck §2, §3 eqs. 2–8, §3.2 eq. 13, §3.5). Source line carried a malformed label ("project-specific quadratic derivations, original PDF inaccessible by timeout") on an OpenCV link: imprecise citation. "symmetrical", "Displacement 2D", "informational curvature", "Growing the window" | Algorithm: the mechanism that distinguishes this method from LK and descriptor matching | 3 expected criteria; 374 → 370 lexical words | Wording aligned with the reference appendix | Minor | Language fixes; Source line cites §2, §3, §3.2, §3.5 of the paper |
| CV-FARNEBACK-002 | $d=(2,-1)^T$ px from $2Ad=b_1-b_2$: confirmed by recomputation (checks/103-farneback.py, check 2); uniqueness "unless the whole neighborhood is exposed to the aperture problem" (§3.2). Blocking error said "Invert any array" (*tableau* for matrix), "residual weak and well-identified displacement" | Reasoning: solving the local constraint and its conditioning | 2 expected criteria; 380 → 371 lexical words | "In the front" → "In the question" in the card and the appendix | Minor | Language fixes; Source line given exact sections |
| CV-FARNEBACK-003 | OpenCV convention $\texttt{prev}(y,x)\sim\texttt{next}(y+\texttt{flow}[1],x+\texttt{flow}[0])$: confirmed (tracking.hpp L215–L217); $(100,-50)$ px/s recomputed (check 11). "The front convention" (*convention avant*, forward convention), "line" for row, "**check**" | Practice: array order versus component order, time base | 3 expected criteria; 299 → 307 lexical words | Objective line "units of the stream" (*flot*, flow; protected field, see below) | Minor | Language fixes; Source line cites the header lines |
| CV-FARNEBACK-004 | Backward flow must be sampled at $x+F(x)$: correct derivation; consistent with Farnebäck §3.4 (second expansion compared at the displaced position) and OpenCV's backward-check sample. "a field output" (*sortie de champ*), "dial a $F_{12}$ move", "fall from 14 to 10" | Diagnosis: round-trip test and its limits | 2 expected criteria; 408 → 406 lexical words | Wording aligned with the reference appendix | Minor | Language fixes; Source line given exact passages |
| CV-FARNEBACK-005 | Coarse scales capture larger motion with lower accuracy (§3.5) and smooth discontinuities (§4); vectors rescaled when propagated (`optflowgf.cpp` L1163–L1167): confirmed. "0,75 px" decimal comma; "bottom" for background (*fond*); "Experience built" (*expérience*, experiment); "catchable amplitude" | Evaluation: separate metrics for background, small objects and boundaries | 2 expected criteria; 385 → 395 lexical words | Expected answer English obscured the criteria | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line cites §3.5, §4 and the code |

Expected-answer change (CV-FARNEBACK-005, meaning-restoring language fix): "The
displacement is reduced to coarse levels, but the reduction can make small structures
disappear and mix boundaries. Evaluate both catchable amplitude, error of small objects
and limits of movement." → "The displacement shrinks at coarse levels, but
downsampling can make small structures disappear and mix motion boundaries. Evaluate
the capturable amplitude, the error on small objects and the motion boundaries
together."

Protected field not edited: `Objective:` of CV-FARNEBACK-003, "read the coordinate
frame and the units of the stream" → proposed "read the coordinate frame and the units
of the flow". No question is defective.

## Reference findings

Claims of revision 6 checked against their passages:

- Polynomial model, translation identities and $2Ad=b_1-b_2$: confirmed (§3, eqs. 2–8);
  the units statement is consistent.
- "Expansion and aggregation windows regulate noise resistance and smoothing of
  movement boundaries": confirmed by the OpenCV header (`winsize`, `poly_n`,
  L198–L203) and §4.
- "Pyramid levels ... extend the range ..., small structures can disappear": consistent
  with §3.5 (larger displacements at lower accuracy).
- "API OpenCV checked with Context7": unsupported in this pass (Context7 unavailable,
  no recorded query); replaced by claims read in the 4.13.0 source.
- No scientific error was found in revision 6. The body was shallow (one paragraph per
  section; no paper passage beyond §§2–3) and contained mistranslations: "Question of
  work", "Reference Response", "check" as a label, "Experience built", "Compromise of
  scale", "front convention", "field output", "dial a move", "0,75 px".

New claims verified for revision 7 (main ones): motivation from helicopter imagery
(§1); certainty and applicability, separable implementation (§2); eqs. 9–14 including
the residual $e(\mathbf x)$ as reversed confidence and uniqueness unless the whole
neighborhood has the aperture problem (§3.1–3.2); parametric models eqs. 15–20 (§3.3);
a priori displacement rounded to integers, eqs. 21–23 (§3.4); iterative and
multi-scale schemes (§3.5); Yosemite protocol, $39\times39$ Gaussian $w$ with
$\sigma=6$, $11\times11$ applicability with $\sigma=1.5$, sky excluded, Table 1 results
and the stated main weakness (§4).

Disagreements between paper, documentation and implementation, recorded in the note
(FR-036):

| Aspect | Paper or documentation | OpenCV 4.13.0 code |
| --- | --- | --- |
| A priori displacement | Rounded to integers (§3.4) | Bilinear sampling at the non-integer position; rounded variant disabled (`optflowgf.cpp` L240–L277) |
| Window solve | Exact inverse of $\sum wA^TA$ (eq. 13) | $1/(\det G+10^{-3})$ (L391, L564): weak curvature shrinks vectors towards zero |
| Applicability size | Paper: $11\times11$, $\sigma=1.5$ (§4); header: `poly_n` is the "size of the pixel neighborhood" | Support of $2\,\texttt{poly\_n}+1$ taps (L60–L80, L116–L203); `poly_n=5` gives the paper's 11 taps |
| Border handling | Zero certainty outside the image and reduced weight near the border (§2, §4) | Fixed 5-pixel weight band (L220–L221, L292–L302); a sample outside the image uses the first frame's curvature with zero linear terms (L278–L284) |
| Confidence | $e(\mathbf x)$ (§3.2) | Not returned |
| Pyramid | Coarser scale via larger applicability and/or low-pass, subsampling between scales (§3.5) | Full-resolution image blurred with $\sigma=(1/s-1)/2$ and resized at each level; levels capped at 32 px (L1107, L1127–L1143) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 462 → 3,450. Tables, the
pseudocode and the Mermaid diagram account for about a quarter of the tokens. The general
flow problem and metrics are linked to CV-FLOT rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Two-frame motivation (§1); OpenCV input/output contract with types, flow convention, warm start, missing confidence; units of coefficients; pipeline roles |
| Intuition | Shallow | Developed | Slope-change mechanism with a 1-D constructed example; aperture in polynomial form; Mermaid diagram of the OpenCV data flow |
| Prerequisites | Developed (two links) | Developed | CV-FILTRES and CV-CORNERS added |
| Assumptions | Shallow | Developed | Local quadratic model, identical polynomials up to displacement (§3.4), slowly varying field (§4), offset/gain behavior, observability (§3.2), border, occlusion and thin objects |
| Procedure | Shallow | Developed | Pseudocode with eqs. 21–22 and 13; purpose of each step; parametric models; rounding versus bilinear sampling |
| Mathematics | Developed (core identity) | Developed | Full eqs. 2–14 and 21–23 with units; residual $e$; OpenCV's determinant term and its shrinkage derivation; worked examples A, B, C and C bis |
| Parameters | Shallow | Developed | Six-parameter table with header text, paper values, sample and class defaults, code behavior (32 px cap, full-resolution pre-blur, `poly_n` half-width, Gaussian window sigma); four-step tuning approach |
| Properties | Absent | Developed | Exactness and its limits, offset invariance and gain sensitivity, dimensionality, smoothness, density versus validity, two-frame trade-off |
| Cost and implementation | Shallow | Developed | Linear cost drivers per stage; OpenCV 4.13 contracts read in code (assertions, propagation, border weights, iterations); execution status |
| Evaluation | Shallow (one protocol sentence) | Developed | Paper protocol and Table 1 results with their metric; proposed baseline and `levels` variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (LK, DIS, RAFT, parametric models, ECC); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/103-farneback.py`](checks/103-farneback.py) (13 assertions): eqs. 4–8 on a 2-D
quadratic and the card's $(2,-1)$ px, exact 11-tap expansion of a quadratic, offset
invariance and gain bias (0.727 and 1.091 px), 1-D single-step and iterated estimates
(1.650→1.500, 2.965→2.602, 1.821→4.398, 3.316→8.000, and −6.799 px for a 10 px shift),
OpenCV level cap (640×480 keeps 3 coarser levels) and per-level sigmas, determinant-term
shrinkage (9%, 62%, 98%), and the card arithmetic of CV-FARNEBACK-003 to 005.

## Applied corrections

- [Reference](../../../vault/100-mouvement-video/references/103-farneback.md),
  revision 6 → 7: body rewritten and deepened as above; unsupported Context7 claim
  removed; mistranslations fixed in the body and appendices ("Question of work" →
  "Working question", "Reference Response" → "Reference answer", "Example of limit" →
  "Example of a limit", "Compromise of scale" → "Scale trade-off", "Experience built" →
  "Constructed experiment", "Documentary reference" → "Source consulted", "Development
  of translation" → "Expanding the translation", "Directional Sensitivity" →
  "Directional sensitivity", "Transport relationship ... front convention" → "Transport
  relation ... forward convention", "dial a $F_{12}$ move" → "Composing a displacement
  $F_{12}$", "0,75 px" → "0.75 px", "In the front" → "In the question"); the appendix
  "Reference answer" of CV-FARNEBACK-005 follows the corrected expected answer; the
  appendices' source lines now name the paper sections rechecked in this pass, keeping
  the record that the PDF had timed out earlier. Sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and per-card headings kept.
- [Cards](../../../vault/100-mouvement-video/103-farneback.md): CV-FARNEBACK-005
  expected answer corrected as quoted above; further explanations and blocking errors of
  all five cards aligned word for word with the corrected appendix paragraphs, plus
  "symmetrical quadratic matrix ... Displacement 2D" → "symmetric matrix of quadratic
  coefficients ... 2D displacement", "Calculation interpreted" → "Interpreted
  calculation", "Unfavourable case ... residual weak" → "Unfavorable case ... a small
  residual", "Invert any array" → "Inverting a matrix", "Do not reverse the line/column
  components" → "Do not confuse the row/column order of array access with the component
  order", "a field output" → "an exit from the field of view", "fall from 14 to 10" →
  "bring 14 back to 10", "Read (4,-2) as (line,column)" → "Reading (4,-2) as (row,
  column)". Source lines now cite Farnebäck §§2–4 sections, the OpenCV header lines and
  code lines. IDs, questions, objectives, families, tags and target deck unchanged.

No other vault file repeats a Farnebäck claim (`rg -i farneb` outside the topic and the
progress log returns nothing).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FARNEBACK-01 | CV-FARNEBACK | OpenCV's Farnebäck returns near-zero vectors on a low-contrast wall while the camera pans: explain the mechanism and give the discriminating check | Density without validity is tested only for occlusion; the implementation's shrinkage of weakly constrained vectors is untested | Diagnosis; Failure modes, worked example C bis | 1 card, 3 criteria (aperture or weak curvature; $10^{-3}$ determinant term pulls towards zero; check $\det G$ or a synthetic translation) | [Farnebäck 2003, §3.2](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf); [optflowgf.cpp L391](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/optflowgf.cpp#L391) |
| P-CV-FARNEBACK-02 | CV-FARNEBACK | Why does an intensity offset between frames leave the Farnebäck estimate unchanged while a gain change biases it in a signal-dependent way? | No card trains the photometric assumption of the polynomial constraint | Reasoning; Assumptions, worked example B | 1 card, 3 criteria ($c$ absorbs the offset; gain scales $A_2$ and $b_2$; bias depends on $A^{-1}b_1$) | [Farnebäck 2003, §3 eqs. 4–6 and §3.1 eqs. 9–11](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf) |

## Sources

Scientific source, opened at the passages listed:

- Farnebäck, Two-Frame Motion Estimation Based on Polynomial Expansion, SCIA 2003,
  [author's copy](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf)
  (text extracted with `pdftotext`): abstract, §1, §2, §3 and §§3.1–3.5, §4 and Table 1.

Implementation sources (official code at tag 4.13.0):

- [`opencv/modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): L55–L61, L188–L229, L549–L585, L652–L767.
- [`opencv/modules/video/src/optflowgf.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/optflowgf.cpp): L57–L311, L314–L416, L560–L568, L585–L642, L1098–L1203.
- [`opencv/samples/python/opt_flow.py`](https://github.com/opencv/opencv/blob/4.13.0/samples/python/opt_flow.py): L51–L57, L76.
- [`opencv/doc/tutorials/others/optical_flow.markdown`](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown): dense optical flow section.

Failed accesses and limits:

- `https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf` (the link cited by
  earlier passes): HTTP 503 from the proxy with `curl`, refused with WebFetch; the
  author's copy of the same SCIA paper was used and the DiVA link is kept as an
  alternative in the note.
- docs.opencv.org returned HTTP 403; API claims rely on the 4.13.0 sources.
- Barron et al.'s definition of the angular error (cited by the paper as [8]) was not
  opened; the note gives the paper's description of the metric only.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC, caused only by other agents' files in progress (`130-evaluation-fiabilite/references/132-tracking-trajectoires.md`, `40-features-matching/references/45-recalage-ecc.md`); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/103-farneback.py` | 13 checks passed |
| `git diff --check -- vault/100-mouvement-video/` | No whitespace error |
| `inventaire_cartes.py vault/100-mouvement-video/103-farneback.md` | 5 cards, 370, 371, 307, 406 and 395 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 6` → `7`; H1 and per-card headings unchanged; `$$` and fences balanced |

No optical flow was computed; the 1-D experiments are constructed arithmetic in Python,
and the proposed baseline and variation are protocols, not results. The Mermaid
diagram and tables were not rendered in Obsidian, and AnkiDroid rendering is
unverified. This is agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-FARNEBACK
revision 7, CV-FARNEBACK-001 to 005, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-FARNEBACK-01, P-CV-FARNEBACK-02).
