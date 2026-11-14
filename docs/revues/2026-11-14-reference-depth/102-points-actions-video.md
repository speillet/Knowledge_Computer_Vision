# Review — Point tracking, actions and video understanding — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the comparison note for three video output contracts: point tracking,
clip classification and temporal action localization. Two-frame motion stays in
[CV-FLOT](../../../vault/100-mouvement-video/references/101-flot-optique.md) and box
tracking in the tracking topic.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIDEO-001 | Points with visibility, clip labels and intervals: confirmed (TAP-Vid §3; CoTracker §3; ActionFormer §3 defines instances $(s_i,e_i,a_i)$). "A music video label" twice, in the explanation and the blocking errors, translated *clip* as a music video: this altered the meaning of the blocking error | Comparison: choosing the output contract before the model | 3 expected criteria; 345 → 351 lexical words | Wording aligned with the reference appendix | Important | Mistranslation corrected in the card and appendix; Source line cites TAP-Vid, CoTracker and ActionFormer sections |
| CV-VIDEO-002 | Event between two samples; $d/\Delta=0.1$: confirmed by recomputation (checks/102-points-actions-video.py, check 4). French label "Exemple temporel", decimal commas "0,35", "0,45", "0,1"; Source line cited CoTracker §3 "for the context of discrete video inputs", which does not support the card | Reasoning: sampling and short events | 1 expected criterion; 280 → 283 lexical words | Source now cites real sampling grids (TimeSformer §4, SlowFast §3.1) | Minor | Language fixes; Source line replaced |
| CV-VIDEO-003 | Future frames impose a delay; "online" is not zero delay: confirmed (CoTracker abstract and §3.3; CoTracker3 §3). Expected answer "the time to exit" (*temps de sortie*, output time); "stock detection" (*détection d'actions*), "VIO valuations", "exits are temporary"; French in the Source line ("variantes online/offline") | Evaluation: comparing causal, windowed and offline outputs | 2 expected criteria; 358 → 360 lexical words | Objective "check causation and delay" lowercase but protected | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given exact sections |
| CV-VIDEO-004 | Frame averaging is order-invariant; scene cues can explain shuffled accuracy: confirmed by derivation (check 12) and consistent with TimeSformer §3 and I3D §2.4. "Frame swapping ... A fall after permutation sustains", "take/pose an object" (*prendre/poser*), "Deduct a temporal understanding" | Diagnosis: whether a classifier uses order | 2 expected criteria; 367 → 362 lexical words | Wording aligned with the reference appendix | Minor | Language fixes; Source line cites TimeSformer §3 and I3D §2.4 |

Expected-answer change (CV-VIDEO-003, meaning-restoring language fix): "Not without
specifying the available information and the time to exit." → "Not without specifying the
available information and the output time."

Protected fields not edited: the `Objective:` lines of CV-VIDEO-003 ("check causation and
delay" → proposed "Check causality and delay") and CV-VIDEO-004 ("check the use of the time
order" → proposed "Check the use of temporal order"). No question is defective.

## Reference findings

Claims of revision 8 checked against their passages:

- CoTracker predicts points and visibility with joint attention; CoTracker3 has online
  (sliding windows) and offline (single window) variants: confirmed (CoTracker abstract,
  §1, §3; CoTracker3 §3). The source list said "slippery windows" for sliding windows.
- TimeSformer and ViViT apply attention to space-time patches: confirmed (TimeSformer §3;
  ViViT §3.2).
- VideoMAE pre-trains by reconstructing masked tubes and its high ratio is a method choice:
  confirmed (VideoMAE abstract and §1: "90% to 95%").
- $(L-1)/f$ span convention: correct arithmetic; extended to strided sampling.
- No scientific error was found in revision 8; the body was shallow (one to three sentences
  per section, no protocol or metric definitions) and contained mistranslations: "music
  video", "slippery windows", "stock detection", "Exemple temporel", "Question of work",
  "Reference Response", decimal commas.

New claims verified for revision 9 (main ones): TAP-Vid task, occluded positions not
evaluated, dataset table, $256\times256$ evaluation, OA, $<\delta^x_{avg}$ and AJ
definitions, validation advice (§3, §3.1, §4.3); CoTracker visibility at the query frame,
1/4-resolution features, windows $J=\lceil2T'/T-1\rceil$ with overlap $T/2$, loss eq. 2 with
$\gamma=0.8$, support points, "first" and "strided" protocols, $T=8$ in training, 70k points
(§3, §3.1, §3.3, §3.4, §4, abstract); CoTracker3 pseudo-labelling with 15k real videos
(§3.1), online and offline variants (§3), Table 1 DAVIS AJ 63.8 and OA 90.2; TAPIR's two
stages (abstract); I3D inflation, boring-video fixed point, 25 frames/s, 64-frame snippets,
whole-video testing (§2.4); Kinetics statistics and non-exhaustive labels favoring top-5
(§2); SlowFast $\tau=16$, $\alpha=8$, $\beta=1/8$, Fast pathway about 20% of computation,
30-view testing (§3.1, §3.2, §4); TimeSformer clip $8\times224\times224$ at rate 1/32, single
clip × 3 crops, degradation of space-only attention (§3, §4); ActionFormer task formulation,
Soft-NMS, tIoU and mAP ranges, THUMOS14 split and 71.0% mAP at 0.5 (§3, §3.4, §4, §4.1,
abstract).

Implementation contract read in the official co-tracker code (commit 82e02e8,
`cotracker/predictor.py`): queries in $(t,x,y)$ pixel coordinates, bilinear resizing to the
model resolution with align-corners rescaling, visibility thresholds 0.9 (offline) and 0.6
on visibility × confidence (online), online window 16 with step 8, offline default window 60.
These thresholds are implementation choices not stated in the papers (FR-036).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 321 → 3,354. The note compares
three tasks and their protocols; tables account for about a third of the tokens. Box tracking,
two-frame flow and pipeline timing are linked to their own notes.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Three-task contract table (inputs, outputs, protocol); coordinate and time conventions; access to future frames; pipeline roles |
| Intuition | Shallow | Developed | One question per task; constructed pick-inspect-place illustration |
| Prerequisites | Shallow (one link) | Developed | Links to CV-REPRESENTATIONS, CV-IOU-AP, CV-FIABILITE, CV-PIPELINE, CV-CAPTEURS |
| Assumptions | Shallow | Developed | Sampling, point identity, label completeness, temporal evidence (I3D boring video, TimeSformer), synthetic domain; degenerate cases |
| Procedure | Shallow | Developed | Windowed point-tracking pseudocode with purpose of each step; TAPIR contrast; clip classification test-time views; TAL decoding |
| Mathematics | Shallow (one formula) | Developed | TAP-Vid metrics; window span; $d/\Delta$; tIoU and mAP ranges; order invariance; CoTracker window count; worked examples A (metrics), B (sampling grids), C (windowed latency) |
| Parameters | Shallow (list) | Developed | Parameter table with paper values and code defaults (windows, support points, visibility thresholds, resolution, clip sampling, views, tIoU); VideoMAE masking; tuning approach |
| Properties | Absent | Developed | Locality of tracks, empirical status of joint tracking, online versus zero delay, classifier invariances, protocol-bound scores |
| Cost and implementation | Shallow | Developed | Cost drivers with variables (tracks × frames, proxy tokens, views, divided attention count, Fast pathway share, TAL features); co-tracker implementation contract; execution status |
| Evaluation | Shallow | Developed | TAP-Vid, Kinetics and THUMOS14 protocols with published examples; tIoU worked check; proposed baseline and reversal variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (point tracking, flow, box tracking, classification, TAL, rule pipelines); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/102-points-actions-video.py`](checks/102-points-actions-video.py) (12 assertions):
TAP-Vid metrics on one track (TP 6, FP 3, FN 2; Jaccard 0.545, $<\delta$ 0.75, OA 0.9),
anisotropic thresholds for a $1920\times1080$ source, sampling probabilities (0.1, 0.094,
0.1875, 1), SlowFast and TimeSformer spans, windowed waiting times (0–7 and 8–15 frames;
233 and 500 ms), CoTracker window counts, TimeSformer attention pairs (2.46 M versus 0.32 M),
a tIoU of 0.667 against THUMOS14 thresholds and order invariance of frame averaging.

## Applied corrections

- [Reference](../../../vault/100-mouvement-video/references/102-points-actions-video.md),
  revision 8 → 9: body rewritten and deepened as above; mistranslations fixed in the body,
  appendices and sources ("A music video label" → "A clip label", "slippery windows" →
  sliding windows, "Question of work" → "Working question", "Reference Response" → "Reference
  answer", "Alternative Hypothesis" → "Alternative hypothesis", "Axis of annotations" →
  "Annotation axes", "Minimum time for context" → "Minimum delay for context", "exits are
  temporary" → "outputs are provisional", "take/pose an object" → "picking up and putting
  down an object", "Documentary reference" → "Source consulted", "0,1" → "0.1"). Sources split
  into scientific and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and per-card headings kept.
- [Cards](../../../vault/100-mouvement-video/102-points-actions-video.md): CV-VIDEO-003
  expected answer corrected as quoted above; further explanations and blocking errors of all
  four cards aligned word for word with the corrected appendix paragraphs, plus "Exemple
  temporel ... 0,35 to 0,45 s" → "Temporal example ... 0.35 to 0.45 s", "It may eventually
  leave clues" → "It may leave cues", "Protocol built" → "Constructed protocol", "VIO
  valuations, smoothing and stock detection" → "VIO estimates, smoothing and action
  detection", "Confound online word and lack of latency" → "Equating the word online with
  zero latency", "Deduct a temporal understanding of a global accuracy alone" → "Inferring
  temporal understanding from global accuracy alone". Source lines now cite exact sections.
  IDs, questions, objectives, families, tags and target deck unchanged.

No other vault file repeats a corrected claim (`rg` over `vault/` for "music video",
"slippery", "stock detection", "Exemple temporel").

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by this
subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-VIDEO-01 | CV-VIDEO | Compute Jaccard, $<\delta$ and occlusion accuracy for a short constructed track and explain why a confident far prediction costs more in AJ than declaring the point occluded | No card trains the TAP-Vid metrics, the only protocol of the point-tracking output | Evaluation; Mathematics, worked example A | 1 card, 3 criteria (TP/FP/FN definitions; double counting of far points; resolution of the thresholds) | [Doersch et al. 2022, TAP-Vid, §4.3](https://arxiv.org/abs/2211.03726) |
| P-CV-VIDEO-02 | CV-VIDEO | Given an online point tracker with a 16-frame window advancing by 8 frames at 30 frames/s, state when a frame's first and revised estimates become available and what a latency benchmark must include | The delay of windowed online methods is tested only qualitatively (CV-VIDEO-003) | Reasoning; worked example C | 1 card, 3 criteria (0–7 frames first; 8–15 frames revision; computation added) | [CoTracker3, §3](https://arxiv.org/abs/2410.11831); [co-tracker predictor.py L212–L225](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/cotracker/predictor.py#L212-L225) |

## Sources

Scientific sources, opened at the passages listed (arXiv PDFs, text extracted with
`pdftotext`):

- TAP-Vid, [arXiv 2211.03726v2](https://arxiv.org/abs/2211.03726): §3, Table 1, §3.1, §4.3.
- CoTracker, [arXiv 2307.07635v3](https://arxiv.org/abs/2307.07635): abstract, §1, §3, §3.1, §3.3 (eq. 2), §3.4, §4 benchmarks and implementation details, Table 1 caption.
- CoTracker3, [arXiv 2410.11831v1](https://arxiv.org/abs/2410.11831): abstract, §3.1, §3 (online model), §4 evaluation protocol, Table 1.
- TAPIR, [arXiv 2306.08637v2](https://arxiv.org/abs/2306.08637): abstract.
- I3D, [arXiv 1705.07750v3](https://arxiv.org/abs/1705.07750): §2.4.
- Kinetics, [arXiv 1705.06950v1](https://arxiv.org/abs/1705.06950): §2 (statistics, non-exhaustive annotation).
- SlowFast, [arXiv 1812.03982v3](https://arxiv.org/abs/1812.03982): §3.1, §3.2, §4 (training and inference).
- TimeSformer, [arXiv 2102.05095v4](https://arxiv.org/abs/2102.05095): §3 (space-time attention schemes), §4 (setup and inference).
- VideoMAE, [arXiv 2203.12602v3](https://arxiv.org/abs/2203.12602): abstract, §1.
- ViViT, [arXiv 2103.15691v2](https://arxiv.org/abs/2103.15691): §3.2.
- ActionFormer, [arXiv 2202.07925v2](https://arxiv.org/abs/2202.07925): abstract, §3, §3.4, §4, §4.1.

Implementation source:

- [facebookresearch/co-tracker at 82e02e8, `cotracker/predictor.py`](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/cotracker/predictor.py): L14–L35, L36–L68, L110–L127, L161–L209, L212–L300.

Failed accesses and limits: no access failure for this subject. Not opened: the THUMOS14
and ActivityNet challenge documents (the TAL protocol is taken from ActionFormer §4), the
co-tracker online demo script (the chunk feeding pattern is deduced from the paper and the
predictor's `step`). Context7 was not available.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/102-points-actions-video.py` | 12 checks passed |
| `git diff --check -- vault/100-mouvement-video/` | No whitespace error |
| `inventaire_cartes.py vault/100-mouvement-video/` | 13 cards in the topic, no anomaly; CV-VIDEO 351, 283, 360 and 362 words |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 8` → `9`; H1 and per-card headings unchanged; `$$` and fences balanced |

No video model was executed; the constructed examples are arithmetic in Python, and the
proposed baseline and reversal variation are protocols, not results. AnkiDroid rendering
and Obsidian rendering of the tables are unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator: the
correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-VIDEO revision 9,
CV-VIDEO-001 to 004, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-VIDEO-01, P-CV-VIDEO-02).
