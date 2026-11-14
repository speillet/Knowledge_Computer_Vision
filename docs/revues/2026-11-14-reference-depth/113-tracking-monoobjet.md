# Review — Single-object tracking: correlation, Siamese networks and MeanShift — 2026-11-14

## Overview

2 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 5 to revision 6. Highest severity per card before correction:
0 blocking, 0 important, 2 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the comparison and decision note of the tracking topic. Mechanism
depth for MOSSE/KCF and MeanShift/CamShift stays in
[CV-CORRELATION](../../../vault/110-tracking-association/references/114-mosse-kcf.md)
and [CV-MEANSHIFT](../../../vault/110-tracking-association/references/115-meanshift-camshift.md);
this note links to them instead of repeating their derivations. SiamFC has no
dedicated reference (inventory item APP-094 remains open), so its mechanism is
developed here at comparison depth.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | SOT starts from a given target while MOT also handles association, creation and deletion: confirmed by SiamFC §1 (target "identified solely by a rectangle in the first frame") and SORT §§3.3–3.4. Source label attributed the project's multi-target cases to SiamFC §4: imprecise citation. "Entries and ratings differ" obscured the meaning (inputs and evaluation protocols) | Comparison: separates the SOT and MOT contracts before choosing an architecture | 2 expected criteria; 264 → 271 lexical words | ID, question, tags and heading unchanged; wording aligned with the reference appendix | Minor | Language fixes in the explanation and blocking errors; Source line given exact sections and stripped of the misattribution |
| CV-SOT-002 | Update on a wrongly associated observation reinforces drift: confirmed as a mechanism of interpolating trackers (KCF §VIII-A; MOSSE §3.4, eqs. 10–12); SiamFC keeps its exemplar fixed (§2.4 "Tracking algorithm", §4.1) and is correctly given as a counterexample. Expected answer said "poorly associated" for *wrongly* associated; "gel" for freezing; "answers" for responses | Diagnosis: a senior must recognize the self-reinforcing update loop and test it | 2 expected criteria; 280 → 285 lexical words. The question front states that the distractor is already in the template, which hints at the answer (see Proposals) | ID, question, tags and heading unchanged; wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |

Expected-answer change (CV-SOT-002, meaning-restoring language fix):
"The update of the model on a poorly associated observation can strengthen the
distractor and increase drift." → "Updating the model on a wrongly associated
observation can reinforce the distractor and increase drift."

## Reference findings

Claims of revision 5 checked against their passages:

- "SiamFC original retains its appearance template during tracking (§4)":
  confirmed; the exemplar embedding "is computed once" and kept fixed because
  interpolation "does not gain much performance" (SiamFC §4.1), and the tracking
  algorithm of §2.4 does "not update a model or maintain a memory of past
  appearances".
- KCF updates its model by interpolation: confirmed (KCF §VIII-A).
- A correlation response is a relative score, not a probability: consistent with all
  sources; no source presents these scores as calibrated.
- No scientific error was found in revision 5. Its body was shallow (one to three
  sentences per section) and contained mistranslations that obscured meaning:
  "local-looking distribution mode", "adapts its window to its design" (to the
  distribution), "research" (search), "field output" (out-of-view), "I/Os" (entries
  and exits), "Question of work", "Reference Response", "gel", "**check**", "he"
  for a model, "material results" (hardware results).

New claims verified for revision 6 (main ones):

- SiamFC geometry: $127$/$255$ crops, stride 8, $6\times6$ and $22\times22$
  embeddings, $17\times17$ map upsampled to $272\times272$, context rule eq. 7,
  displacement read-out §2.1, five scales $1.025^{\{-2..2\}}$ with damping 0.35,
  86/58 frames/s on a GTX Titan X (§§2.1, 2.4, Table 1, §4.1).
- SiamFC sensitivity to "scenes with confusion" because the model is never updated
  (Fig. 6 caption); authors expect gains from model update and memory (§4.4).
- KCF: patch 2.5 times the target, cosine window, Gaussian target peaked at the
  top-left element (App. A-A); adaptation rates 0.075 raw / 0.02 HOG, $\lambda=10^{-4}$
  (Table II); no failure-detection heuristic (§VIII-A); precision metric chosen
  because overlap penalizes scale-blind trackers (§VIII-B); Table I and timing are in
  §VIII-C.
- MOSSE: preprocessing (§3.1), eq. 5, update eqs. 10–12 with $\eta=0.125$ (§3.4),
  PSR with an $11\times11$ exclusion, 20–60 normal and about 7 at occlusion or
  failure (§3.5), no scale or orientation estimate (§4.2), 669 updates/s (§4.3).
- Protocols: OTB precision, success AUC, OPE, TRE, SRE (Wu et al. §§4–5); VOT
  accuracy, robustness, re-initialization 5 frames after a zero-overlap failure,
  10-frame burn-in (Kristan et al. §3.1) and the model-free, short-term, causal
  definition (§1); LaSOT absent labels, metrics, protocols and protocol I results
  (Fan et al. §§3.3, 4.1, 4.3).

Disagreements between papers and OpenCV 4.13 implementations, recorded in the note
(FR-036):

| Aspect | Paper | OpenCV 4.13.0 |
| --- | --- | --- |
| KCF search region | 2.5 × target (KCF App. A-A) | 2 × target (`trackerKCF.cpp` L214–L218) |
| KCF scale | Not estimated in the base method | Constant box size (L363–L367) |
| KCF failure handling | No heuristic (§VIII-A) | `update` returns `false` and skips the model update when the response maximum is below `detect_thresh=0.5` (L353–L357) |
| MOSSE learning rate | $\eta=0.125$ (§3.4) | 0.2 (`mosseTracker.cpp` L32) |
| MOSSE PSR | Sidelobe excludes an $11\times11$ window; about 7 signals occlusion (§3.5) | Mean and standard deviation of the whole map, peak included; threshold 5.7 (L33, L104–L109, L203–L205) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 330 → 4,753. Of the
4,753 tokens, about 3,700 words are prose; the rest are tables, the pseudocode and
the Mermaid diagram. The length comes from comparing three families and three
benchmark protocols; method derivations were cut back to links to 114 and 115.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Model-free, short-term, causal definition (VOT §1); frame, box and crop coordinate contract; OpenCV located/not-located contract; three output cases; pipeline roles; upstream initialization sensitivity (OTB SRE) |
| Intuition | Shallow | Developed | One-line mechanism per family; constructed red-car illustration tied to SiamFC Fig. 6; Mermaid diagram of the shared per-frame loop |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-ACQUISITION, CV-IOU-AP, CV-FUSION, CV-FLOT, CV-VIDEO and to the method notes 114/115 |
| Assumptions | Shallow | Developed | Bounded motion, appearance continuity, local discriminability, presence, box representation; observability after occlusion, grid quantization, zero mass or flat response, border handling |
| Procedure | Shallow | Developed | Shared pseudocode with purpose of each step; family comparison table (model, localization, scale, update, confidence) |
| Mathematics | Shallow (no equation) | Developed | Conventions; MeanShift centroid; MOSSE closed form and update; KCF relation and FFT index conventions; SiamFC eqs. 2–7; worked examples A (capture range) and B (update memory) |
| Parameters | Shallow (list) | Developed | Cross-family parameter table with source values and OpenCV defaults; four-step tuning approach; frame-rate re-tuning |
| Properties | Shallow | Developed | Translation equivariance and cyclic-shift approximation; scale and rotation; adaptation versus drift; uncalibrated scores; SiamFC training domain |
| Cost and implementation | Shallow | Developed | Cost drivers with variables and reported speeds with hardware; constructed correlation-versus-backbone cost; OpenCV 4.13 contracts for `meanShift`, `CamShift`, `Tracker`, DNN trackers, `TrackerKCF` and legacy `TrackerMOSSE`; execution status |
| Evaluation | Shallow | Developed | OTB, VOT and LaSOT protocol table; worked example C (precision versus IoU); published results with protocol; proposed baseline and frame-subsampling variation with a confound control; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices across families, MOT, point tracking, segmentation and hybrids; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/113-tracking-monoobjet.py`](checks/113-tracking-monoobjet.py) (14 assertions):
SiamFC capture range (64 crop pixels, $s=1.27$ and 50.4 px for a 50 px target,
$128/127$ of the width for any square target, 59.6 px for an $80\times40$ target),
update memory ($1-(1-\eta)^{10}$ = 0.18, 0.54, 0.74, 0.89 and half-lives 34.3, 8.9,
5.2, 3.1 for $\eta$ = 0.02, 0.075, 0.125, 0.2; $\eta'=0.144375$), IoU of a fixed box
under a 1.5× scale change (0.444), and correlation versus first-convolution cost
(2,663,424 versus 527,215,392 multiply-accumulates).

## Applied corrections

- [Reference](../../../vault/110-tracking-association/references/113-tracking-monoobjet.md),
  revision 5 → 6: body rewritten and deepened as above; mistranslations fixed in the
  body and both appendices ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Difference of problem" → "Problem difference",
  "Drift Loop" → "Drift loop", "**check**" → "**Discriminating check**", "gel" →
  "freezing", "he believes" → "it believes", "answers" → "responses", "circulating
  offsets" → "cyclic shifts", "Memory of an update" → "Memory of one update");
  appendix source line no longer attributes the interpolation formula and the
  multi-target cases to SiamFC; sources split into scientific and implementation
  sources; closing provenance line replaced. Front matter unchanged except
  `revision`; H1, per-card headings and the `#sources-and-flashcards` heading kept.
- [Cards](../../../vault/110-tracking-association/113-tracking-monoobjet.md):
  CV-SOT-002 expected answer corrected as quoted above. Language fixes in further
  explanations and blocking errors of both cards: "Entries and ratings" → "Inputs and
  evaluation protocols", "conditioned to" → "conditioned on", "a possible brick" →
  "a possible building block", "reveals both association ambiguity, exclusivity and
  birth management" → "reveals association ambiguity, the lack of exclusivity and the
  need for birth management", "Assume that following a box resolves the management of
  all identities" → "Assuming that tracking one box solves identity management for
  every object", "Test freeze under uncertainty, loss policy and reset on reserved
  sequences" → "Test freezing under uncertainty, the loss policy and resets on
  held-out sequences", "Interpret each update as an automatic model enhancement" →
  "Treating every update as an automatic improvement of the model". Source lines
  now cite SiamFC §1/§4.1/Fig. 6, SORT §§3.3–3.4 and KCF §VIII-A, and label the
  constructed parts as project constructions. Questions, IDs, objectives, families,
  tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for SiamFC,
KCF and MOSSE parameters).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not
edited by this subject run; the register is a shared file):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SOT-01 | CV-SOT | Compute a Siamese tracker's per-frame capture range from crop size, stride and context scale, and decide whether a given target speed and frame rate are trackable | The bounded-motion assumption shared by all families is untested; no card trains crop-to-frame reasoning | Reasoning; Mathematics, worked example A | 1 card, 3 criteria (64 crop pixels; scale factor from eq. 7; division by $s$) | [SiamFC §2.1, §2.4 eq. 7, Table 1](https://arxiv.org/html/1606.09549v2) |
| P-CV-SOT-02 | CV-SOT | Choose among a correlation filter, a Siamese tracker and detection plus association under stated constraints (CPU budget, similar distractors, need for a loss signal, re-detection) and name one discriminating test | No card trains the decision that this comparison note exists for | Design; Alternatives and applications | 1 card, 3–4 criteria | [SiamFC §4.1 and Fig. 6](https://arxiv.org/html/1606.09549v2); [KCF §VIII-A](https://arxiv.org/html/1404.7584v3); [MOSSE §3.5](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) |

Question proposal (not applied; questions are verbatim invariants): the front of
CV-SOT-002 states that "a distractor replaces the target in the tracker's template",
which hints at the template-update mechanism the answer must name. Proposed wording:
"During an occlusion, an adaptive single-object tracker moves its box onto a
similar-looking object and keeps following it after the target reappears. Which
mechanism can turn this momentary error into persistent drift?"

## Sources

Scientific sources, opened at the passages listed:

- Bertinetto et al., SiamFC, [arXiv HTML v2](https://arxiv.org/html/1606.09549v2):
  §1, §2 and §2.1 (eqs. 1–2, displacement read-out), §2.2 (eqs. 3–6), §2.3, §2.4
  (eq. 7, Table 1, "Tracking algorithm"), §4.1, §4.3, §4.4 (Table 2, VOT-16
  paragraph), Fig. 2 and Fig. 6 captions.
- Henriques et al., KCF, [arXiv HTML v3](https://arxiv.org/html/1404.7584v3): §IV-A
  to §IV-E, §V-A to §V-C, §VI-A and §VI-B, §VIII-A (Algorithm 1), §VIII-B, §VIII-C
  (Table I, timing), Appendix A-A, Table II.
- Bolme et al., MOSSE, [CVPR 2010 PDF](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf)
  (text extracted with `pdftotext`): abstract, §3 introduction, §§3.1–3.5, §4.2,
  §4.3.
- Wu, Lim and Yang, OTB, [CVPR 2013](https://openaccess.thecvf.com/content_cvpr_2013/papers/Wu_Online_Object_Tracking_2013_CVPR_paper.pdf): §4 and §5 opening.
- Kristan et al., VOT methodology, [arXiv 1503.01313v3](https://arxiv.org/abs/1503.01313): §1, §3.1.
- Fan et al., LaSOT, [arXiv 1809.07845v2](https://arxiv.org/abs/1809.07845): §3.3, §3.4, §4.1, §4.3.
- Bewley et al., SORT, [arXiv 1602.00763](https://arxiv.org/abs/1602.00763): §§3.3–3.4 headings and opening (card CV-SOT-001 source).

Implementation sources (official code at tag 4.13.0):

- [`opencv/modules/video/include/opencv2/video/tracking.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp): L64–L107, L807–L833, L878–L1060.
- [`opencv_contrib/modules/tracking/include/opencv2/tracking.hpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/include/opencv2/tracking.hpp): L90–L149.
- [`opencv_contrib/modules/tracking/include/opencv2/tracking/tracking_legacy.hpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/include/opencv2/tracking/tracking_legacy.hpp): L328–L342.
- [`opencv_contrib/modules/tracking/src/trackerKCF.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/trackerKCF.cpp): L195–L225, L330–L400, L650–L690, L900–L918.
- [`opencv_contrib/modules/tracking/src/mosseTracker.cpp`](https://github.com/opencv/opencv_contrib/blob/4.13.0/modules/tracking/src/mosseTracker.cpp): L31–L33, L76–L112, L140–L230.

Failed accesses and limits:

- docs.opencv.org/4.13.0 pages (`Tracker`, `TrackerKCF`, video tracking group,
  MeanShift tutorial) returned HTTP 403 with both `curl` and WebFetch. API claims
  rely on the 4.13.0 headers and sources from which that documentation is generated.
  The tutorial link is retained in the note as not re-read in this pass.
- Context7 was not available in this session (see the scope record); official
  versioned code replaced it.
- Not re-verified in this pass: the MeanShift and CamShift mechanism papers
  (Comaniciu et al.; Bradski), whose content belongs to CV-MEANSHIFT and is only
  linked here.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/113-tracking-monoobjet.py` | 14 checks passed |
| `git diff --check -- vault/110-tracking-association/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/110-tracking-association/113-tracking-monoobjet.md` | 2 cards, 271 and 285 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 5` → `6`; H1 and per-card headings unchanged; `$$` balanced |

No tracker, OpenCV call or video experiment was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not
rendered in Obsidian, and AnkiDroid rendering of the corrected cards is unverified.
This is agent self-review, without independent scientific validation or measurement
of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-SOT revision 6, CV-SOT-001 and CV-SOT-002, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-SOT-01, P-CV-SOT-02).
