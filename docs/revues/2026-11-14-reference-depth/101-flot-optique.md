# Review — Optical flow: Lucas–Kanade, Farnebäck and RAFT — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 5 to revision 6. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for two-frame flow. It now develops pyramidal
Lucas–Kanade (LK) and RAFT; Farnebäck's mechanism stays in
[CV-FARNEBACK](../../../vault/100-mouvement-video/references/103-farneback.md) and is
only compared here, and multi-frame point tracking stays in
[CV-VIDEO](../../../vault/100-mouvement-video/references/102-points-actions-video.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | One scalar constraint cannot fix two unknowns; an edge leaves the tangential component free: confirmed (Bouguet §2.3, $G$ invertible only with gradients in both directions; Lucas and Kanade §4.5). Source line cited RAFT §§3.1–3.3, which does not support this card: imprecise citation. Expected answer "without assumptions/neighboring" was incomplete English | Reasoning: aperture problem as a rank condition, needed for point selection and diagnosis | 2 expected criteria; 345 → 338 lexical words | ID, question, tags unchanged; wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |
| CV-FLOT-002 | 4 px over 20 ms = 200 px/s, 40 ms = 100 px/s, 50 ms = 80 px/s: confirmed by recomputation (checks/101-flot-optique.py, check 15). Mistranslations obscured meaning: "the stream" (*le flot*, the flow), "the second string" (*la seconde chaîne*, a second pipeline), "eventually doubles" (*éventuellement*, can double), "to pass in m/s, it takes" | Practice: unit and grid discipline before any speed claim | 2 expected criteria; 360 → 366 lexical words | Objective line "respect the temporal unity" should read "time unit" (protected field, see below) | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |
| CV-FLOT-003 | Correlations encode compatibility, updates refine: confirmed (RAFT §3.2 eq. 1, §3.3 eqs. 3–6). "all-peer" for *all-pairs*, "recurring" for *recurrent*, "occlusionss" | Comparison: separates the matching evidence from the iterative estimator, and both from identity | 2 expected criteria; 349 → 351 lexical words | Objective line is in French ("situer RAFT"; protected field, see below) | Minor | Language fixes; Source line cites RAFT §§3.2–3.3, §4.3 and `corr.py` |
| CV-FLOT-004 | A vector in an occluded region is an inference, not an observation: consistent with Sintel's unmatched-pixel evaluation (Butler et al. §4, about 8.5% of pixels) and OpenCV's sample, which ignores `status` and applies a 1 px backward check (`lk_track.py` L56–L59). "**check**" label, "field exit", "digital residual" (*numérique*, numerical), "trust policy", "reserved data" | Diagnosis: validity of dense output under occlusion | 2 expected criteria; 278 → 273 lexical words | Objective "process a occlusion" ungrammatical (protected field) | Minor | Language fixes; Source line given exact passages |

Expected-answer changes (meaning-restoring language fixes):

- CV-FLOT-001: "An equation does not constrain two unknowns without
  assumptions/neighboring; an edge can keep a tangential ambiguity." → "One equation
  cannot constrain two unknowns without extra assumptions or neighboring pixels; along
  an edge, the tangential component remains ambiguous."
- CV-FLOT-002: "No: it takes the time interval, for example 4 px at 20 ms gives
  200 px/s in this model." → "No: the time interval between the two frames is needed;
  for example, 4 px over 20 ms gives 200 px/s in this model."

Protected fields not edited (to decide by the coordinator): the `Objective:` lines of
CV-FLOT-002 ("respect the temporal unity" → proposed "respect the time unit"),
CV-FLOT-003 ("situer RAFT" → proposed "situate RAFT among flow estimators") and
CV-FLOT-004 ("process a occlusion" → proposed "interpret a vector under occlusion").
No question is defective.

## Reference findings

Claims of revision 5 checked against their passages:

- Linearized constraint $I_xu+I_yv+I_t\approx0$ and the LK least-squares system:
  confirmed (OpenCV 4.13.0 tutorial source; Bouguet eqs. 13–25; Lucas and Kanade
  §4.5).
- "The local system requires gradients in several directions": confirmed (Bouguet
  §2.3: invertible $G$ "is equivalent to saying that the image ... contains gradient
  information in both x and y directions").
- RAFT all-pairs volume, recurrent updates, no long-term identity: confirmed (RAFT
  §§3.2–3.3); the memory cost statement was qualitative and is now quantified.
- `status=1` does not prove a physical match: confirmed and made precise from
  `lkpyramid.cpp` (status tests bounds and conditioning only, at level 0).
- No scientific error was found in revision 5. Its body was shallow (one to three
  sentences per section, no source passage for LK) and contained mistranslations:
  "all-peer correlations", "recurring updates", "Constantity of intensity",
  "Question of work", "Reference Response", "**check**", "field exit", "digital
  residual", "reserved data".

New claims verified for revision 6 (main ones):

- Lucas and Kanade 1981: exhaustive search $O(M^2N^2)$ (§3); linearization and
  weighting $w(x)=1/|G'(x)-F'(x)|$, Newton–Raphson iteration (§4.1, eqs. 1–7); least
  squares (§4.2, eq. 9); convergence for misregistrations up to half a wavelength, and
  the smoothing trade-off (§4.3); five accumulated products in 2-D (§4.5); affine
  extension (§4.6).
- Bouguet: coordinates and window (§1), pyramid and propagation eqs. 5–10 with gain
  $2^{L_m+1}-1$ (§2.2), constant $G$ from the first image, stop at 0.03 px or 20
  iterations, about 5 on average (§2.3), bilinear sub-pixel sampling (§2.5), border band
  (§2.6), lost features and drift (§2.7), selection by minimum eigenvalue (§3).
- Baker and Matthews: Gauss–Newton derivation (§2.2), $O(n^2N+n^3)$ per iteration
  (§2.4), constant Hessian motivating the inverse compositional algorithm (§3.2).
- RAFT: 1/8-resolution features with $D=256$ (§3.1), eq. 1, 4-level pooled pyramid,
  lookup radius and 256 px range, $O(N^2)$ versus $O(NM)$, 17% of inference time at
  $1088\times1920$ (§3.2), ConvGRU eqs. 3–6, warm start, convex upsampling (§3.3), loss
  eq. 7 with $\gamma=0.8$ (§3.4), 12 training updates and 32/24 evaluation updates (§4),
  Table 1 results, Table 2 ablations, no divergence at 200 updates (§4.3), timing
  hardware (§4.4).
- MPI-Sintel: EPE and the Middlebury comparison (§1), $1024\times436$ rendering (§3),
  Clean/Final passes and unmatched pixels (§4), evaluation bands (§6).
- KITTI 2015: outlier rule (3 px and 5%), valid-pixel evaluation, bg/fg/bg+fg (§5).

Disagreements between paper and implementation, recorded in the note (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| RAFT lookup grid | L1 ball $\|\mathbf{dx}\|_1\le r$ (eq. 2): 41 points for $r=4$ | Square $(2r+1)^2$ grid: 81 points (`corr.py` L37–L43) |
| RAFT correlation | Plain dot product (eq. 1) | Divided by $\sqrt D$ (`corr.py` L60) |
| RAFT flow definition | Text maps pixels "in $I_2$ ... in $I_2$" (typo) | Flow on the $I_1$ grid, `coords1 - coords0` (`raft.py` L63–L70) |
| LK derivatives | Central differences; "in practice, the Sharr operator" (Bouguet §2.3) | Scharr, scaled by 32 (`lkpyramid.cpp` L59–L155) |
| LK stop rule | 0.03 px or 20 iterations (Bouguet §2.3) | Default 0.01 px or 30 iterations; count clamped to 100 (L1388–L1393) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 331 → 5,027. The note
develops two methods (LK and RAFT) and two benchmark protocols, with four worked
examples and a code-derived contract; tables, pseudocode and the Mermaid diagram account
for roughly a quarter of the tokens. Farnebäck's mechanism is linked, not restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task, sparse/dense outputs, coordinate and direction conventions, OpenCV and RAFT data contracts, photometric and timestamp contract, pipeline roles and downstream expectations |
| Intuition | Shallow | Developed | Plain mechanism of LK and RAFT; constructed brick-wall illustration; Mermaid data-flow diagram of both methods |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-CORNERS, CV-SVD, CV-ECC, CV-CAPTEURS |
| Assumptions | Shallow | Developed | Brightness constancy, small residual motion and half-wavelength range, coherent window motion, two-direction texture, visibility (Sintel 8.5% unmatched), RAFT training domain; degenerate cases |
| Procedure | Shallow | Developed | Pyramidal LK pseudocode with purpose of each step; RAFT steps; three-method comparison table |
| Mathematics | Shallow (one equation) | Developed | Units of the constraint and normal flow; LK normal equations with units; covariance $\sigma^2G^{-1}$ derivation; pyramid equations and gain; RAFT eqs. 1, 2, 7 and the ×8 scaling; worked examples A (iterations), B (periodic texture and pyramid), C (correlation volume size) |
| Parameters | Shallow (list) | Developed | Parameter table with paper values, OpenCV defaults and sample values; RAFT ablation evidence; four-step tuning approach |
| Properties | Shallow | Developed | Translation model and affine extension, photometric non-invariance (offset bias derivation), local optimum, sub-pixel accuracy, status semantics, RAFT fixed-point behavior |
| Cost and implementation | Shallow | Developed | Cost drivers with variables; OpenCV 4.13 contract of `calcOpticalFlowPyrLK` read in code (status, err, stop and oscillation rules, pyramid stop); worked example D (`minEigThreshold` units); OpenCV backward-check sample; RAFT official code contracts; execution status |
| Evaluation | Shallow | Developed | EPE and Sintel bands, KITTI outlier rule, sparse-track proxies; published results with protocol; proposed baseline and Clean→Final variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (LK, dense classical, RAFT, descriptor matching, ECC, point tracking, variational); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/101-flot-optique.py`](checks/101-flot-optique.py) (17 assertions): iterative LK
on a $7\times7$ patch (first-step errors 0.108 and 0.525 px, convergence in 3 and 4
iterations, rank-1 edge), 1-D LK on a sinusoid of wavelength 8 px (exact for 3 and 3.9 px,
aliased to $-3.9$ and $-2$ px for 4.1 and 6 px, scale-invariant ratio), pyramid gain 15
and the 150 px heuristic, RAFT padding and volume sizes (7,040 cells, 49.6 M values,
198/261 MB; 32,640 cells, 4.26 GB), lookup counts 81/41 and 256 px range, Scharr factor 32
and the meaning of `minEigThreshold` (0.1024 (grey level/px)$^2$), unit conversions and
the KITTI outlier rule.

## Applied corrections

- [Reference](../../../vault/100-mouvement-video/references/101-flot-optique.md),
  revision 5 → 6: body rewritten and deepened as above; mistranslations fixed in the
  body and appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "**check**" → "**Discriminating check**", "Example and Limit" →
  "Example and limit", "Lucas – Kanade System" → "Lucas–Kanade system", "all-peer" →
  "all-pairs", "Dimensions of Correlation" → "Dimensions of the correlation",
  "occlusionss" → "occlusions", "the second string" → "a second pipeline", "eventually
  doubles" → "can double", "residual round trip" → "Round-trip residual", "note $F_{12}$
  moving the 1 image to 2" → "let $F_{12}$ map image 1 to image 2", "digital residual" →
  "numerical residual", "reserved data" → "held-out data", "field exit" → "exit from the
  field of view"). The docs.opencv.org tutorial links (HTTP 403) were replaced by the
  tutorial's source at tag 4.13.0. Sources split into scientific and implementation
  sources; closing provenance line replaced. Front matter unchanged except `revision`;
  H1 and per-card headings kept.
- [Cards](../../../vault/100-mouvement-video/101-flot-optique.md): expected answers of
  CV-FLOT-001 and CV-FLOT-002 corrected as quoted above; further explanations and
  blocking errors of all four cards aligned word for word with the corrected appendix
  paragraphs, plus "the stream" → "the flow", "To pass in m/s, it takes a geometry and
  a scale adapted" → "Converting to m/s requires geometry and an appropriate scale",
  "Recurring updates" → "Recurrent updates", "Output is a dense movement ... of an
  object ID on any video" → "The output is a dense motion field ... of an object identity
  across a video", "Confound frame displacement and speed per second" → "Confusing the
  displacement per frame pair with a speed per second". Source lines now cite exact
  sections (Lucas and Kanade §4.1/§4.5, Bouguet §2.3, RAFT §§3.2–3.3/§4.3, Sintel §4,
  `lk_track.py` L56–L59, `corr.py`). IDs, questions, objectives, families, tags and
  target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for "all-peer",
"occlusionss", aperture and half-wavelength claims). Language-only defect seen in
another subject, not edited: "Lucas – Kanade follow-up" in
`vault/40-features-matching/46-harris-shi-tomasi.md` (CV-CORNERS).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FLOT-01 | CV-FLOT | Given a texture period, a displacement per frame and a pyramid depth, predict whether pyramidal LK recovers the motion or locks one period off, and name the discriminating check | No card trains the capture range of LK and the pyramid, nor its periodic-texture failure | Reasoning; Mathematics, worked example B | 1 card, 3 criteria (half-wavelength range; ratio unchanged by the pyramid; aliased solution $h-\lambda$) | [Lucas and Kanade 1981, §4.3](https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf); Bouguet §2.2 |
| P-CV-FLOT-02 | CV-FLOT | Compare EPE with the KITTI outlier rate (3 px and 5%) and with matched/unmatched EPE, and decide which pixels a stated protocol evaluates | No evaluation card exists for this subject; registers the unregistered 2026-10-20 idea "Distinguish EPE and validity under occlusion" | Evaluation | 1 card, 3 criteria | [Menze and Geiger 2015, §5](https://www.cvlibs.net/publications/Menze2015CVPR.pdf); Butler et al. 2012, §§4, 6 |

## Sources

Scientific sources, opened at the passages listed:

- Lucas and Kanade 1981, [CMU PDF](https://www.ri.cmu.edu/pub_files/pub3/lucas_bruce_d_1981_2/lucas_bruce_d_1981_2.pdf)
  (scanned; pages 122–124 rendered to images and read): §3, §4.1–§4.6.
- Bouguet, [pyramidal LK report](http://robots.stanford.edu/cs223b04/algo_tracking.pdf)
  (text extracted with `pdftotext`): §1, §2.1–§2.7, §3.
- Baker and Matthews, [Lucas-Kanade 20 Years On, Part 1, CMU-RI-TR-02-16](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf): §2.1, §2.2, §2.4, §3.2 opening.
- Teed and Deng, RAFT, [arXiv 2003.12039v3 PDF](https://arxiv.org/pdf/2003.12039v3): §3,
  §§3.1–3.4, §4 (implementation details, training schedule), §§4.1–4.4, Tables 1–2.
- Butler et al., [MPI-Sintel, ECCV 2012](http://files.is.tue.mpg.de/black/papers/ButlerECCV2012.pdf): §1, §3, §4, §6 table caption.
- Menze and Geiger, [KITTI 2015, CVPR](https://www.cvlibs.net/publications/Menze2015CVPR.pdf): §5 "Evaluation Protocol" and results description.

Implementation sources (official code at a tag or commit):

- [`opencv/modules/video/include/opencv2/video/tracking.hpp` at 4.13.0](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): L55–L61, L109–L229, L488–L505, L652–L767.
- [`opencv/modules/video/src/lkpyramid.cpp` at 4.13.0](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/lkpyramid.cpp): L59–L155, L187–L254, L455–L526, L680–L745, L747–L843, L1260–L1430.
- [`opencv/samples/python/lk_track.py` at 4.13.0](https://github.com/opencv/opencv/blob/4.13.0/samples/python/lk_track.py): L30–L59.
- [`opencv/doc/tutorials/others/optical_flow.markdown` at 4.13.0](https://github.com/opencv/opencv/blob/4.13.0/doc/tutorials/others/optical_flow.markdown): whole tutorial text.
- [princeton-vl/RAFT at 2888e15](https://github.com/princeton-vl/RAFT/tree/2888e15a51fa41140771d3f498ed8023cff098d1/core): `corr.py` L12–L60, `raft.py` L30–L39 and L63–L139, `utils/utils.py` L7–L24.

Failed accesses and limits:

- docs.opencv.org/4.13.0 returned HTTP 403; the tutorial and API claims rely on the
  4.13.0 sources from which that documentation is generated.
- Horn and Schunck 1981 (MIT AI Memo 572 on dspace.mit.edu) returned HTTP 429 and an
  alternative mirror returned HTML: **not verifiable**. The note mentions global
  variational methods in one qualified sentence ("not re-read in this pass") and makes
  no claim about their equations.
- Context7 was not available in this session (see the scope record); official
  versioned code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC, caused only by `40-features-matching/references/46-harris-shi-tomasi.md` (another agent's file in progress); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/101-flot-optique.py` | 17 checks passed |
| `git diff --check` on the two vault files | No whitespace error |
| `inventaire_cartes.py vault/100-mouvement-video/101-flot-optique.md` | 4 cards, 338, 366, 351 and 273 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 5` → `6`; H1 and per-card headings unchanged; `$$` and fences balanced |

No optical flow code, OpenCV call or RAFT model was executed; the constructed
examples are arithmetic recomputed in Python, and the proposed baseline and variation
are protocols, not results. The Mermaid diagram and tables were not rendered in
Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-FLOT revision 6, CV-FLOT-001 to 004, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register (P-CV-FLOT-01,
P-CV-FLOT-02).
