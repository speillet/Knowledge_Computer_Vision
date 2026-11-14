# Review — GrabCut, regions and appearance models — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 4 to revision 5. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for GrabCut and seeded graph cut. Unsupervised region
methods (Felzenszwalb–Huttenlocher, SLIC) are treated as alternatives only; inventory
items APP-080 (superpixels) and APP-081 (region growing) remain open.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-GRABCUT-001 | Alternation of GMM estimation and min-cut labeling: confirmed (Rother et al. §3.2, Fig. 3); exact sub-problem but no joint optimum: confirmed (Boykov & Jolly Theorem 1; Rother §3.2 "local minimum"). Expected answer said "appearance patterns" for appearance models; explanation said "bottom" for background, "business truth", "warranty" for guarantee | Algorithm: the two-step structure and what each step guarantees | 2 expected criteria; 283 → 288 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections and code lines |
| CV-GRABCUT-002 | Definite background labels cannot be undone by iterations: confirmed (Rother §3.3 "guaranteed not to be retracted"; OpenCV updates only probable states, grabcut.cpp L526–L543; hard weight $9\gamma$ exceeds any n-link sum, worked example B). Expected answer said "safe background" and "useful region"; explanation "attached to the bottom", "digital failure" | Diagnosis: separate a wrong hard constraint from a weak appearance model | 2 expected criteria; 286 → 288 lexical words | Wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact passages |
| CV-GRABCUT-003 | Interaction effort belongs in the comparison: consistent with Rother §5 (interaction counts, unequal-input error rates). Expected answer said "a quick fix can require a lot of corrections" for a method that is fast per call; "reserved images", "balance sheet" | Comparison: evaluate interactive methods by quality against effort | 3 expected criteria; 288 → 300 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given §5 |

Expected-answer changes (meaning-restoring language fixes):

- CV-GRABCUT-001: "Estimate the background/object appearance patterns and then
  optimize the labels via graph cut in the defined energy." → "Estimate the background
  and foreground appearance models, then optimize the labels by graph cut on the defined
  energy."
- CV-GRABCUT-002: "The initial zone and the safe background labels: a useful region can
  be made impossible by constraint." → "The initial rectangle and the definite
  background labels: a needed part of the object can be made impossible by a hard
  constraint."
- CV-GRABCUT-003: "Labels added by the user can provide the missing information; a quick
  fix can require a lot of corrections." → "Labels added by the user can provide the
  missing information; a method that is fast per call can still require many
  corrections."

Defective objective (header invariant, not edited): CV-GRABCUT-002 "check is an
initialization constraint" is a mistranslation; proposed wording "Check whether an
initialization constraint causes the truncation".

## Reference findings

Claims of revision 4 checked against their passages:

- Alternation of Gaussian-mixture estimation and graph-cut optimization: confirmed
  (Rother §3.2, Fig. 3).
- Schematic energy $E(L)=\sum U+\lambda\sum V$ with "$\lambda$ settles a compromise":
  imprecise. In GrabCut the smoothness weight is $\gamma=50$ and the data term has unit
  weight (eqs. 2, 7, 11); OpenCV's variable `lambda` is the hard-constraint weight
  $9\gamma$, not a trade-off; Boykov and Jolly's $\lambda$ weighs the region term. The
  note now separates the three.
- "Graph memory and iterations depend on the resolution": confirmed and made precise
  (graph over the whole image, grabcut.cpp L463–L521).
- No scientific error was found. The body held one to three sentences per section, with
  mistranslations: "safe/probable labels" and "some/probable" (definite/probable), "the
  bottom" (background), "business mask", "Question of work", "Reference Response",
  "material results".

New claims verified for revision 5 (main ones):

- Rother et al.: Fig. 1 caption and §1.2 (rectangle interaction, transparency not dealt
  with); §2.1 eqs. 2–6 ($\beta$, $\gamma=50$ tuned on 15 images, 8-connectivity, Ising
  prior when $\beta=0$); §3.1 eqs. 7–11, $K=5$, footnote 1 (hard assignment instead of
  EM); §3.2 (monotonic decrease, local minimum, automatic termination); Fig. 3 (steps,
  user editing); Fig. 4 (12 iterations); §3.3 (firm $T_B$ only); §5 (three failure cases,
  0.9 s and 0.12 s timings, 20-task and 50-image comparisons).
- Boykov and Jolly: edge-weight table, $K=1+\max_p\sum_q B_{\{p,q\}}$, Lemma 1,
  Theorem 1, non-negativity requirement and constant shift (footnote 2), regional terms
  as negative log-likelihoods (§4).
- Boykov and Kolmogorov: two search trees, orphans, $O(mn^2|C|)$ worst case, practical
  speed on vision graphs (§3).
- Felzenszwalb and Huttenlocher: eqs. 1–5, $k$ as a scale of observation, $O(m\log m)$
  (§4.1), grid-graph setup (§5).
- Achanta et al.: SLIC $O(N)$ with $2S\times2S$ search (Fig. 2, Algorithm 1), $m\in[1,40]$
  (§III-B).
- OpenCV 4.13.0 grabcut.cpp, gcgraph.hpp, kmeans.cpp, imgproc.hpp and tutorial source.

Disagreements between paper and implementation, recorded in the note (FR-036):

| Aspect | Rother et al. 2004 | OpenCV 4.13.0 |
| --- | --- | --- |
| Component assignment (step 1) | $k_n=\arg\min D_n$, including $-\log\pi$ (eq. 9, Fig. 3) | Highest component density without the mixture weight (grabcut.cpp L121–L152) |
| Stopping | Until $E$ stops decreasing (§3.2) | Exactly `iterCount` iterations (L589–L596); the tutorial's "until the classification converges" does not match the code |
| Border matting | Part of the system (§4) | Not implemented |
| Hard constraints | Infinite cost in the trimap model; firm $T_B$ (§3.3) | t-link weight $9\gamma=450$, sufficient by worked example B, plus probable-only update |
| Initialization | Background and foreground GMMs from the two sets | k-means++ with 10 iterations, seeded from the global RNG (L368–L413; kmeans.cpp L287) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 292 → 3,895. About 2,980
of these are prose; the rest are tables, pseudocode and the Mermaid diagram.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task as stated by the paper; OpenCV data contract (types, mask states, rectangle frame, model arrays, modes); hard segmentation only; pipeline roles |
| Intuition | Shallow | Developed | Plain mechanism; constructed mug illustration; Mermaid diagram of the OpenCV loop with user editing |
| Prerequisites | Shallow (conventions only) | Developed | Links to CV-ACQUISITION, CV-FILTRES, CV-WATERSHED, CV-IOU-AP, CV-METRIQUES-APPLIQUEES, CV-SAM |
| Assumptions | Shallow | Developed | Colour separability, representative background, object inside the rectangle, edges at boundaries, compactness, opacity; observability; empty classes, singular covariances, constant image |
| Procedure | Shallow | Developed | Pseudocode with purposes; incomplete labelling and hard assignment justified from the paper |
| Mathematics | Shallow (schematic energy) | Developed | Eqs. 7–11 and 5 with units; graph construction, $K$ and Theorem 1; alternation and convergence; worked examples A (contrast normalization), B (hard-constraint weight) and C (thin structures) |
| Parameters | Shallow (list) | Developed | Eight-row table including fixed OpenCV constants; four-step tuning approach |
| Properties | Absent | Developed | Exact sub-problem versus local joint minimum; implementation deviation; hard labels; invariances; boundary bias; randomness |
| Cost and implementation | Shallow | Developed | Per-iteration costs, BK max-flow, whole-image graph, 2004 timing; OpenCV 4.13 contracts; execution status |
| Evaluation | Shallow | Developed | Quality-against-effort protocol, published results with their protocol, baseline and margin variation with a confound, measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (seeded graph cut, watershed, F-H, SLIC, promptable models, matting); industrial uses labelled as project reasoning; scientific and implementation sources |

Constructed examples are recomputed by
[`checks/92-grabcut-regions.py`](checks/92-grabcut-regions.py) (11 assertions):
n-link weights 50, 30.33, 18.39, 6.77; invariance of the contrast term to colour scaling;
neighbour-pair count $4WH-3W-3H+2$ and edge count; maximum n-link sum 341.42 below
$9\gamma=450$ and above $K-1$; boundary cost per pixel 120.71 and 16.34, strand cost
241.42; log-likelihood ratio 8 and the contrast threshold $\rho\approx6.82$; 65 model
values.

## Applied corrections

- [Reference](../../../vault/90-segmentation/references/92-grabcut-regions.md),
  revision 4 → 5: body rewritten and deepened as above; mistranslations fixed in the
  appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "Example of limit" → "Example of a limitation", "Proposed
  Protocol" → "Proposed protocol", "Energy and Cut" → "Energy and cut", "Hard Constraint
  and Preference" → "Hard constraint and preference", "Quality curve – interaction" →
  "Quality–interaction curve", "appearance patterns" → "appearance models", "the bottom"
  → "the background", "safe labels" → "definite labels", "warranty" → "guarantee",
  "reserved images" → "held-out images", "balance sheet" → "results"); trailing section
  renamed "Sources" and split into scientific and implementation sources; closing
  provenance line replaced. Front matter unchanged except `revision`; H1 and per-card
  headings unchanged.
- [Cards](../../../vault/90-segmentation/92-grabcut-regions.md): expected answers of all
  three cards corrected as quoted above. Further explanations and blocking errors
  received the same language fixes as the reference appendices, plus "Verification
  built" → "Constructed check", "digital failure" → "numerical failure", "Assume that
  convergence must cancel out" → "Assuming that convergence will undo". Source lines now
  cite Rother et al. §3.1–§3.3 and §5, Boykov and Jolly Theorem 1 and OpenCV code lines.
  Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for GrabCut and
graph cut).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-GRABCUT-01 | CV-GRABCUT | Explain why GrabCut removes a thin, weakly contrasted foreground structure (boundary cost per unit length against per-pixel colour evidence) and name two remedies | The boundary-length bias is a frequent real failure (the tutorial's lost hair) and no card trains it | Reasoning; worked example C | 1 card, 3 criteria | [Rother et al. 2004, eqs. 9 and 11, §5](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/08/siggraph04-grabcut.pdf); derivation is a project construction |

## Sources

Scientific sources, opened at the passages listed (PDF text extracted with `pdftotext`):

- Rother, Kolmogorov and Blake 2004, [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/08/siggraph04-grabcut.pdf): abstract, Fig. 1, §1.2, §2.1, §3.1–§3.3, Figs. 3–4, §4 opening, §5.
- Boykov and Jolly 2001, [ICCV PDF](https://www.csd.uwo.ca/~yboykov/Papers/iccv01.pdf): §1–§3, §4 opening.
- Boykov and Kolmogorov 2004, [TPAMI PDF](https://www.csd.uwo.ca/~yboykov/Papers/pami04.pdf): §3 opening and overview, section list, §4.4 heading and setup.
- Felzenszwalb and Huttenlocher 2004, [IJCV PDF](https://www.cs.cornell.edu/~dph/papers/seg-ijcv.pdf): §3, §4 (Theorems 1–3 statements), §4.1, §5 opening.
- Achanta et al. 2012, [EPFL preprint](https://infoscience.epfl.ch/record/177415/files/Superpixel_PAMI2011-2.pdf): Fig. 2 caption, Algorithm 1, §III-B.

Implementation sources (tag 4.13.0, fetched from `raw.githubusercontent.com`):

- [`grabcut.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/grabcut.cpp): complete.
- [`gcgraph.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc/detail/gcgraph.hpp): L48–L200.
- [`kmeans.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/core/src/kmeans.cpp): L95, L280–L345.
- [`imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L351–L371, L3555–L3575.
- [GrabCut tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_grabcut/py_grabcut.markdown): complete.

Failed accesses and limits:

- docs.opencv.org/4.13.0 GrabCut tutorial: HTTP 403; the tutorial source was read. The
  rendered link is retained as not re-read.
- Kolmogorov and Zabih 2004 (graph-representable energies) and Ruzon and Tomasi 2000
  were not opened; no claim of the note rests on them.
- The definition behind Rother et al.'s "error rates" on the 50-image database is not
  stated in the passage read; the numbers are quoted with that limit.
- Context7 was not available in this session; official versioned code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | No error in this subject's files; the run reported ECHEC because of other agents' in-progress files (`130-evaluation-fiabilite/references/132-tracking-trajectoires.md`, `40-features-matching/references/45-recalage-ecc.md`) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/92-grabcut-regions.py` | 11 checks passed |
| `git diff --check -- vault/90-segmentation/92-grabcut-regions.md vault/90-segmentation/references/92-grabcut-regions.md` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/90-segmentation/92-grabcut-regions.md` | 3 cards, 288 to 300 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card header, block, ID, question, tags and deck lines identical; front matter identical except `revision: 4` → `5`; H1 and per-card headings unchanged; `$$` balanced; card paragraphs repeated in the appendices identical |

No OpenCV call and no image experiment was executed; the baseline and variation are
protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering is unverified. This is agent self-review, without independent
scientific validation or measurement of learner proficiency. Export status: **to
republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-GRABCUT
revision 5, CV-GRABCUT-001 to 003, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-GRABCUT-01).
