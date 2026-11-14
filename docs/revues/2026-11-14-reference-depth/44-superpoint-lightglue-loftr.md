# Review — SuperPoint, LightGlue and LoFTR — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the pipeline note for learned matching. It now carries the three
mechanisms (SuperPoint, LightGlue with SuperGlue as contrast, LoFTR) at the depth
needed to configure and diagnose them, the coordinate contract between stages, and
the protocols behind published numbers. Classical matching, robust estimation and
dense alignment are linked to their own references rather than restated.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Two heads on a shared encoder: confirmed (SuperPoint §3). "Homographic adaptation *matches* predictions of transformed views": imprecise, eq. 10 *averages* the unwarped detector responses over $N_h$ homographies (§5.1). LightGlue "shares features": mistranslation of *takes*. Partial assignment with unmatched points: confirmed (SuperGlue §3; LightGlue §3.2). Source line cited "bracket-to-fine" | Understanding: separates detector/descriptor, matcher and estimator roles | 2 expected criteria; 345 → 349 lexical words | ID, question, tags unchanged; explanation aligned with the reference appendix | Minor | Corrected the adaptation sentence; language fixes; Source line given exact sections and the SuperGlue/LightGlue passages |
| CV-MATCH-APPRIS-002 | Coarse matches with threshold and mutual nearest neighbour, refinement in a $5\times5$ window: confirmed (LoFTR §3.3, §3.4, §3.6; fine_matching.py). Expected answer "neither a guaranteed flow anywhere nor a complete time tracker" obscured the meaning ("everywhere", "temporal"). "Occulted", "quantifies", "digital location resolution", "Coarse at the end" | Comparison: detector-free versus dense flow and tracking | 2 expected criteria; 353 → 367 lexical words | Wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line now cites LoFTR §3.3–§3.6 and the official refinement code |
| CV-MATCH-APPRIS-003 | Equal dimensions do not guarantee compatibility: confirmed in code, `forward` only asserts the descriptor dimension (lightglue.py v0.2 L498–L499); SIFT weights additionally expect scales and orientations (L344–L366); positions are normalized by the image size (L25–L36). Expected answer "Expected weights and distributions are associated with a representation" was unclear; "excluding distribution" inverted the meaning (a *different* distribution); "**check**" label | Practice: keep extractor, weights and metadata consistent | 2 expected criteria; 360 → 371 lexical words | Aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given code lines |
| CV-MATCH-APPRIS-004 | Same pairs, resolution and geometric validation: confirmed as protocol requirements. Missing condition: the LightGlue authors tune the robust threshold per matcher (+7% AUC@5° for SuperGlue from tuning alone, App. C.5) and time matching only, excluding extraction and robust estimation (App. D). "Alignment group", "interim accounts", "comparison built", "reserved pairs" obscured the meaning | Evaluation: build a comparable baseline | 3 expected criteria; 360 → 460 lexical words | Aligned with the reference evaluation section | Minor | Language fixes; one paragraph added on estimator threshold and timing scope; Source line given exact sections |
| CV-MATCH-APPRIS-005 | Round trip $(100,60)\to(70,40)\to(100,60)$ and $H_{orig}=B^{-1}H_{net}A$: recomputed (checks 1–4). The official wrapper already undoes its own resize with a pixel-centre rule (utils.py L137–L147), so the residual risk lies in the caller's padding and crops. "Pretreatment", "paged image", "resetting the scale", "digital round trip" | Diagnosis: coordinate contract before blaming the matcher | 2 expected criteria; 366 → 362 lexical words. The front names "padding", which hints at the answer (see Proposals) | Aligned with the reference appendix | Minor | Language fixes; Source line now cites the wrapper and LoFTR scaling code |

Expected-answer changes (meaning-restoring language fixes):

- CV-MATCH-APPRIS-002: "No: it produces coarse-to-fine matches without explicit sparse
  detector; it is neither a guaranteed flow anywhere nor a complete time tracker." →
  "No: it produces coarse-to-fine matches without an explicit sparse detector; it is
  neither a flow guaranteed everywhere nor a complete temporal tracker."
- CV-MATCH-APPRIS-003: "Expected weights and distributions are associated with a
  representation; equal dimensions do not guarantee compatibility." → "The learned
  weights, and the input distributions they expect, are tied to one representation;
  equal dimensions do not guarantee compatibility."

## Reference findings

Claims of revision 7 checked against their passages:

- SuperPoint learns detection and description with homographic adaptation: confirmed
  (§3, §5); the adaptation supervises the detector, while descriptors are trained on
  homography-warped pairs with a hinge loss (§3.4).
- LightGlue uses context between features and adapts its computation: confirmed
  (§3.1, §3.3).
- LoFTR matches coarse-to-fine without a detector: confirmed (§3). "Bracket-to-fine"
  was a mistranslation of *coarse-to-fine*.
- "Do not compare weights or licenses as if they were a single product": now
  supported by the LightGlue README (Apache-2.0 for LightGlue; restrictive licence for
  SuperPoint, including weights and inference file).
- No scientific error in revision 7; the body held one to three sentences per section,
  with mistranslations ("bracket-to-fine", "official deposit", "calculation adaptation",
  "Question of work", "Reference Response", "built-in cases", "material results",
  "plane" for planar, "paged" for padded, "pretreatment").

New claims verified for revision 8 (main ones):

- SuperPoint: $H/8\times W/8$ cells, 65-channel detector head with dustbin, bicubic
  descriptor sampling and L2 normalization, hinge loss with 8 px positive radius,
  $m_p=1$, $m_n=0.2$, $\lambda_d=250$, $\lambda=10^{-4}$, $D=256$; eq. 10 and $N_h=100$
  with the 0.67 / +21% / +22% repeatability figures; training at $240\times320$; failure
  under extreme in-plane rotation (Fig. 8); 11.15 ms + 1.5 ms ≈ 13 ms on a Titan X;
  HPatches Table 4 (0.310/0.684/0.829 versus SIFT 0.424/0.676/0.759; MLE 1.158 versus
  0.833 px) under the §7.3 protocol.
- SuperGlue: partial-assignment constraints, dustbins, $T=100$ Sinkhorn iterations,
  9 layers, threshold 0.2, 69 ms on a GTX 1080 (§3, §3.2, §4).
- LightGlue: eqs. 2–10 and 12–13, $L=9$, $d=256$, $\alpha=0.95$, $\beta=0.01$, $\tau=0.1$,
  relative-only positions in self-attention and none in cross-attention, dustbin
  entanglement (§3.5), HPatches and MegaDepth protocols (§5.1–§5.2), Tables 1, 2 and 5,
  α ablation (App. C), timing scope and RTX 3080 (App. D), threshold tuning (+7%).
- LoFTR: 1/8 and 1/2 resolutions, linear attention with $\mathrm{elu}+1$, positional
  encoding added once, dual-softmax, $\theta_c=0.2$, $N_c=4$, $N_f=1$, $w=5$,
  inverse-variance fine loss, 116/130 ms on an RTX 2080 Ti, HPatches protocol and
  Table 1 (§3.1–§3.6, §4.1–§4.2).

Paper–implementation and cross-paper observations (FR-036):

| Aspect | Paper | Implementation or other paper |
| --- | --- | --- |
| LightGlue positions | Normalized to $[-1,1]$ keeping the aspect ratio (App. C) | Without `image_size`, normalized by the keypoint extent (lightglue.py L25–L36) |
| LightGlue point pruning | Active when the exit criterion is not met (§3.3) | Active on CUDA only above 1,024 keypoints (1,536 with FlashAttention), always on CPU, off under compilation (L332–L337, L544; README) |
| LoFTR refinement | Expectation in a $w\times w$ window (§3.4) | Only the image-B point moves; image-A points stay on the coarse lattice (fine_matching.py L63–L73) |
| LoFTR on HPatches | AUC@3/5/10 px 65.9/75.6/84.6, OpenCV RANSAC, short side 480 (LoFTR Table 1) | AUC@1/5 px 41.5/78.8 with tuned MAGSAC (LightGlue Table 1): same method and data, different protocol |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 328 → 5,708. The length comes from three
mechanisms plus SuperGlue as contrast, a cross-paper protocol comparison and the
implementation contracts of two repositories; classical matching, robust estimation
and dense alignment stay in their own notes.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task and correspondence definition; stage contract table with shapes, outputs and frames; who undoes preprocessing in each wrapper; pipeline roles and downstream frame requirements |
| Intuition | Shallow | Developed | One mechanism per component with sourced quotes; constructed warehouse illustration; Mermaid data-flow diagram with coordinate frames |
| Prerequisites | Shallow (three links) | Developed | Links to CV-MATCHING, CV-FLANN, CV-HOMOGRAPHIE, CV-EPIPOLAIRE, CV-BA, CV-ECC, CV-FLOT by mechanism |
| Assumptions | Shallow | Developed | Partial assignment, single geometric relation, training distributions, grids, positional metadata; degenerate and unobservable cases |
| Procedure | Shallow | Developed | Pseudocode for sparse and dense paths with purpose of each step; four-way comparison table (NN, SuperGlue, LightGlue, LoFTR) |
| Mathematics | Shallow (no equation) | Developed | SuperPoint heads, losses and eq. 10; SuperGlue contrast; LightGlue eqs. 3–10, 12–13 and normalization; LoFTR dual-softmax, MNN selection and refinement; worked examples A–D |
| Parameters | Shallow | Developed | Parameter table with paper and code values; tuning approach in four steps |
| Properties | Shallow | Developed | Learned invariances, one-to-one without correctness, uncalibrated scores, localization limits, detector-free versus dense, adaptivity effect, domain evidence |
| Cost and implementation | Shallow | Developed | Cost drivers with variables and reported timings with hardware; LightGlue v0.2 and LoFTR contracts with line numbers; licences; execution status |
| Evaluation | Shallow | Developed | Four-protocol table; cross-paper non-comparability; DLT dependence on precision; baseline and matcher-only variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices among SIFT/ORB, SuperPoint+LightGlue, LoFTR, ECC and optical flow; industrial uses labelled as project reasoning; sources split into scientific and implementation |

Constructed examples are recomputed by
[`checks/44-superpoint-lightglue-loftr.py`](checks/44-superpoint-lightglue-loftr.py)
(17 checks): preprocessing round trip and wrong inversion order, composition
$B^{-1}H_{net}A$, the 1,024 px resize and pixel-centre rule (0.4375 px and 1.5 px
shifts), normalization by the image size versus the keypoint extent (factor 1.918),
LightGlue thresholds $\lambda_0=0.9$, $\lambda_8=0.8029$ and $\beta=0.01$, the
cross-attention cost ($1.07\times10^9$ MACs; 0.49 after 30% pruning), the LoFTR grid
(4,800 cells, 4,256 after border removal, ±4 px refinement bound), the SuperPoint grid
(1,228,800 descriptor floats) and the ordering of the Table 4 values.

## Applied corrections

- [Reference](../../../vault/40-features-matching/references/44-superpoint-lightglue-loftr.md),
  revision 7 → 8: body rewritten and deepened as above. Appendix language fixes, each
  applied identically to the matching card text: "built-in cases" → "constructed
  cases", "Question of work" → "Working question", "Reference Response" → "Reference
  answer", "Example of a pipeline built" → "Constructed pipeline example", "plane" →
  "planar", "paged image" → "padded image", "official deposit" → "official
  repository", "Why these bricks" → "Why these components", "matches predictions of
  transformed views" → "aggregates the detector's predictions over randomly warped
  views", "Coarse at the end" → "Coarse to fine", "quantifies" → "quantizes", "digital
  location resolution" → "numerical resolution of a location", "excluding distribution"
  → "with a different distribution", "assign the change" → "attribute the change",
  "alignment group" → "the transformation group used to align estimated and reference
  poses", "pretreatment" → "preprocessing", "bracket-to-fine" → "coarse-to-fine",
  "calculation adaptation" → "adaptive computation". Sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and all per-card headings unchanged.
- [Cards](../../../vault/40-features-matching/44-superpoint-lightglue-loftr.md):
  expected answers of CV-MATCH-APPRIS-002 and -003 as quoted above. Language fixes in
  further explanations and blocking errors of all five cards ("Reading architecture",
  "Example of limit", "occulted", "Network trust is decision data … not a correct path
  certificate" → "The network's confidence is decision evidence … not a certificate of
  a correct trajectory", "**check**" → "**Discriminating check**", "Connecting an
  unknown representation eventually respects" → "Plugging in an unknown
  representation may respect", "The interim accounts do not therefore indicate only a
  progress produced" → "Intermediate counts therefore do not by themselves indicate
  progress on the product", "Comparison built" → "Constructed comparison", "reserved
  pairs" → "held-out pairs", "Assimilate detector-free to dense…" → "Equating
  detector-free with dense, hole-free and error-free", "Deduct compatibility of only
  the number of components" → "Inferring compatibility from the number of components
  alone"). CV-MATCH-APPRIS-004 gained one paragraph on per-matcher threshold tuning and
  timing scope (LightGlue App. C.5, App. D). All five Source lines now cite exact
  sections or code lines; "bracket-to-fine" removed. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file mentions SuperPoint, LightGlue, SuperGlue or LoFTR outside the
inventory and progress tables (`rg` over `vault/`), so no other card repeats a corrected
claim.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run; the register is a shared file). P-CV-MATCH-APPRIS-01 carries forward
the 2026-10-20 proposal "Explain early exit and pruning LightGlue", which was never
registered.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-MATCH-APPRIS-01 | CV-MATCH-APPRIS | Reconstruct LightGlue's adaptive depth and width: exit when a fraction $\alpha$ of points is confident above a decaying $\lambda_\ell$, prune points confident and unmatchable ($\sigma<\beta$), and state what this does to latency tails and accuracy | No algorithm card; the cost mechanism appears only in explanations | Algorithm; Mathematics and Parameters | 1 card, 3 criteria | [LightGlue §3.3, App. C eqs. 12–13, Table 5](https://arxiv.org/abs/2306.13643) |
| P-CV-MATCH-APPRIS-02 | CV-MATCH-APPRIS | From SuperPoint's HPatches results at $\varepsilon=1,3,5$ px against SIFT (and LoFTR's ±4 px refinement bound), decide whether a learned front end suits a 1-pixel registration tolerance and name the discriminating test | No card links match quantity to localization precision, a key decision for calibration and registration | Reasoning; Mathematics worked example D, Alternatives | 1 card, 3 criteria | [SuperPoint §7.3, Table 4](https://arxiv.org/abs/1712.07629); [LoFTR §3.4](https://arxiv.org/abs/2104.00680) |

Question proposal (not applied; questions are verbatim invariants): the front of
CV-MATCH-APPRIS-005 names "padding", which points to the coordinate-conversion answer.
Proposed wording: "After a change in image preprocessing, matches look correct when
drawn on the network inputs, but the homography estimated in the original images is
biased. What should be tested first?"

## Sources

Scientific sources (arXiv PDFs downloaded and extracted with `pdftotext`):

- DeTone, Malisiewicz and Rabinovich, SuperPoint, [arXiv 1712.07629](https://arxiv.org/abs/1712.07629):
  §3.1–§3.4 (eqs. 1–6, footnotes 1–2), §4, §5.1–§5.3 (eq. 10), §6, §7.1–§7.3,
  Table 4, Fig. 8 caption, App. A (eq. 15).
- Sarlin et al., SuperGlue, [arXiv 1911.11763](https://arxiv.org/abs/1911.11763): §3
  motivation, keypoint encoder and partial assignment, §3.2 dustbin and Sinkhorn, §4
  architecture details and test-time threshold.
- Lindenberger, Sarlin and Pollefeys, LightGlue, [arXiv 2306.13643](https://arxiv.org/abs/2306.13643):
  §3 to §3.5 (eqs. 2–11), §4, §5.1–§5.4 with Tables 1, 2 and 5 and Fig. 7, App. C
  (positional encoding, exit criterion and pruning eqs. 12–13, Table 11 discussion,
  C.2, C.5 threshold tuning), App. D (timings).
- Sun et al., LoFTR, [arXiv 2104.00680](https://arxiv.org/abs/2104.00680): §3.1–§3.6,
  Fig. 2 caption, §4.1 with Table 1, §4.2 datasets and Table 3, §4.3 (InLoc remark).

Implementation sources:

- [cvg/LightGlue at tag v0.2](https://github.com/cvg/LightGlue/tree/v0.2) (commit
  edb2b83; the default branch head on 2026-11-14 was 5a650c4, not used):
  `lightglue/lightglue.py` L20–L40, L280–L372, L440–L655; `lightglue/superpoint.py`
  L52–L120, L150–L200; `lightglue/utils.py` L10–L36, L131–L147; `README.md` usage,
  "Advanced configuration", benchmark notes, License.
- [zju3dv/LoFTR at commit df7ca80](https://github.com/zju3dv/LoFTR/tree/df7ca80f917334b94cfbe32cc2901e09a80e70a8):
  `src/loftr/utils/cvpr_ds_config.py`; `src/loftr/utils/coarse_matching.py` L1–L30,
  L170–L260; `src/loftr/utils/fine_matching.py` L20–L75; `README.md` (optimal-transport
  code and licence).

Failed accesses and limits:

- Context7 was not available in this session (see the scope record); the official
  repositories at a fixed tag or commit replaced it.
- The arXiv HTML endpoint of LoFTR cited in the 2026-10-30 appendix was not retried;
  the PDF was used. The appendix link is kept as a historical record.
- Not verified: rendering of LightGlue's README benchmark plots (images), the
  SuperPoint licence text itself (only the LightGlue README statement about it), and
  any OpenCV contrib implementation of these models.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC, caused only by `40-features-matching/references/46-harris-shi-tomasi.md` (another subject, edited concurrently); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/44-superpoint-lightglue-loftr.py` | 17 checks passed |
| `git diff --check -- vault/40-features-matching/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/40-features-matching/44-superpoint-lightglue-loftr.md` | 5 cards, 349–460 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 41 protected card lines identical; reference front matter identical except `revision: 7` → `8`; H1 and 10 per-card headings unchanged; `$`, `$$` and code fences balanced |

No model, checkpoint or OpenCV call was executed; timings and accuracies are the
authors' reported values under their protocols, and the proposed baseline is a
protocol, not a result. Mermaid and tables were not rendered in Obsidian; AnkiDroid
rendering is unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-MATCH-APPRIS revision 8, CV-MATCH-APPRIS-001 to -005, corrections listed above,
Agent Claude Code self-review, to republish with `paquet-anki`) and the proposal
register (P-CV-MATCH-APPRIS-01, P-CV-MATCH-APPRIS-02).
