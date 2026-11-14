# Review — SAM, SAM 2 and prompted video segmentation — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for promptable image and video segmentation.
Inventory item APP-082 (SAM 2 video memory) is now treated at method depth in this
note; whether that closes the item is the coordinator's decision.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | Prompt-guided, class-agnostic masks: confirmed (Kirillov et al. 2023 §2–§3; `SamPredictor.predict` returns masks, quality scores and logits, no class, predictor.py L92–L135); text-to-mask is an exploratory proof of concept: confirmed (§7.5, §8). "Ambiguity of Prompt", "the same index" (prompt), "business category", "Confound" | Understanding: the output contract that decides where SAM fits in a pipeline | 2 expected criteria; 292 → 290 lexical words | Wording aligned with the reference appendices | Minor | Language fixes; Source line given exact sections and code lines |
| CV-SAM-002 | Memory and propagation: confirmed (Ravi et al. §4: memory attention, memory bank of recent and prompted frames, object pointers); confusion among similar objects: confirmed as a stated limitation (App. C). Expected answer said "time-guided masks", a mistranslation of masks propagated over time; "stored spread", "path order", "self-contained and classified MOT", "Assimilate spread of masklets" | Comparison: what memory adds over per-frame segmentation and what it does not provide | 2 expected criteria; 274 → 282 lexical words | Wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given §4 and App. C |
| CV-SAM-003 | Future-frame corrections change the task: confirmed (Ravi et al. §4: prompted frames may come "from the future"; §6.1 offline and online protocols). "Advertise", "self-deployable", "release" for output, "to $t+2$ s", "decision to $t$" | Evaluation: separate information access, interaction budget and availability time | 2 expected criteria; 357 → 364 lexical words | Wording aligned with the reference appendices | Minor | Language fixes; Source line given §4 and §6.1 |

Expected-answer change (meaning-restoring language fix):

- CV-SAM-002: "Memory and propagation of time-guided masks according to the protocol."
  → "Memory, and propagation of the prompted masks over time, according to the
  protocol." (French source: "Mémoire et propagation de masques guidées dans le temps
  selon le protocole".)

Defective objectives (header invariants, not edited), with proposed wording from the
French originals: CV-SAM-001 "Set the output to SAM" → "Define SAM's output";
CV-SAM-002 "Find SAM 2 on video" → "Position SAM 2 for video"; CV-SAM-003 "check the
future in evaluation" → "Control access to future frames in evaluation".

## Reference findings

Claims of revision 7 checked against their passages:

- Image and prompt encoders condition a mask decoder; several proposals represent
  ambiguity: confirmed (Kirillov et al. 2023 §3, App. A).
- SAM 2 adds memory and propagation with prompts and corrections: confirmed (Ravi et al.
  §3–§4, Fig. 2).
- "The text-to-mask prototype of the SAM paper is not the automatic contract of its
  standard checkpoint/API": confirmed (§7.5 modified training; predictor has no text
  input).
- "Cache of the depreciable encoder" was a mistranslation of the amortized encoder;
  "dots" (points), "pattern" (model), "spread" (propagate), "Varier" (vary), "Question of
  work", "Reference Response", "Advertise" (report), "material results" (hardware).
- No scientific error was found; the body held one to three sentences per section.

New claims verified for revision 8 (main ones):

- SAM: §2 task and valid-mask definition; §3 components, ~50 ms decoding on CPU in a
  browser, three masks, predicted IoU, focal plus Dice, 11 simulated rounds; §7.1
  single-point protocol (distance-transform centre, most confident mask, 23 datasets,
  human rating, oracle); §7.4 boxes from ViTDet; §7.5 proof of concept; §8 limitations
  (fine structures, disconnected components, crispness, not real-time with a heavy
  encoder, dedicated interactive methods better with many points, exploratory text);
  App. A (1024 input, 64×64×256 embedding, quarter-resolution masks, minimum-loss
  training, fourth output token, MSE-trained IoU head, 20:1 ratio); App. B (32×32 grid);
  Fig. 13 (91M, 308M, 636M; marginal ViT-H gain).
- SAM 2: footnote 1 (results use SAM 2.1); §3 PVS; §4 streaming encoder, memory
  attention, multiple masks and highest-IoU propagation, presence head, memory encoder,
  FIFO banks of $N$ recent and $M$ prompted frames, object pointers, future prompted
  frames, training prompts; §6.1 offline and online protocols, 3 clicks per frame, >3×
  fewer interactions; §6.2 Table 4; §6.3 58.9 against 58.1 mIoU, 6× faster; §7 43.8 and
  30.2 FPS; App. A.2 Table 9 (resolution, frames, $N=6$, 64 channels, encoder sizes);
  App. B (valid objects with boundaries); App. C limitations; App. D.1 occlusion
  embedding; App. D.3 benchmarking conditions.
- DAVIS 2017: $\mathcal J$, $\mathcal F$ and averaging over objects (§3).
- Official code: SAM predictor contract, resize, padding, mask post-processing and logit
  threshold; SAM 2 video predictor options, object-id rule, prompt encoding,
  missing-object score, propagation signature.

Disagreements and precisions between paper and implementation (FR-036):

| Aspect | Paper | Official code |
| --- | --- | --- |
| Causality | Streaming design; prompted frames may come from the future (Ravi et al. §4) | `init_state` loads a stored video; `propagate_in_video(..., reverse=False)` can run backwards (sam2_video_predictor.py L42–L52, L546–L551) |
| New objects | Not discussed | Refused after tracking starts; `reset_state` required (L145–L150) |
| Overlap between objects | Objects processed separately (App. C) | `non_overlap_masks=False` by default (L22–L39) |
| Mask output | Masks predicted at a quarter of the input (App. A) | Bilinear upsampling, crop, resize, threshold at logit 0 (sam.py L19, L133–L162) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 310 → 3,556. About 2,520
of these are prose; the rest are tables, pseudocode and the Mermaid diagram.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task definitions from both papers; code-level data contract (types, coordinates, box format, mask prompt, outputs); pipeline roles |
| Intuition | Shallow | Developed | Amortized encoder, ambiguity, memory; tire/bicycle illustration from the paper; Mermaid diagram of one SAM 2 step |
| Prerequisites | Shallow (one link) | Developed | Links to CV-GRABCUT, CV-WATERSHED, CV-SOT, CV-SORT, CV-METRIQUES-TEMPS, CV-DETECTEURS, CV-OPENVOC |
| Assumptions | Shallow | Developed | Prompt defines the target, visible boundaries, domain coverage, fine detail, video continuity; observability of identity and future prompts; absent objects, mid-video objects, multi-prompt output |
| Procedure | Shallow | Developed | Pseudocode for SAM and SAM 2 with the purpose of each step |
| Mathematics | Shallow | Developed | Minimum-loss training, meaning of the quality score, mask post-processing and threshold, $\mathcal J\&\mathcal F$; worked examples A (click and logit geometry) and B (memory span); section justified as having no closed-form model |
| Parameters | Shallow (list) | Developed | Seven-row table with source values; tuning approach |
| Properties | Shallow | Developed | No semantics, represented ambiguity, amortized speed, memory carrying errors, causality as a protocol property, SAM 2.1 version |
| Cost and implementation | Shallow | Developed | Cost drivers with reported speeds and their conditions; official predictor contracts at commits; execution status |
| Evaluation | Shallow | Developed | Protocol table (single point, offline, online, VOS); published results with protocols; baseline and online/offline variation with a confound; measurement limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (interactive segmenters, closed-set models, detector boxes, trackers, GrabCut); industrial uses labelled as project reasoning; scientific and implementation sources |

Constructed examples are recomputed by [`checks/94-sam-sam2.py`](checks/94-sam-sam2.py)
(12 assertions): 1920×1080 frame to 1024×576 plus 448 padded rows; click mapping
$(960,540)\to(512,288)$; strides 16 and 4; 7.5 original pixels per logit cell; 144 valid
logit rows; cable width in cells; memory span 0.2 s and 0.4 s; 24-click budget; 22.8 and
33.1 ms per frame; Table 9a resolution trade-off.

## Applied corrections

- [Reference](../../../vault/90-segmentation/references/94-sam-sam2.md), revision 7 → 8:
  body rewritten and deepened as above; mistranslations fixed in the appendices
  ("Question of work" → "Working question", "Reference Response" → "Reference answer",
  "Ambiguity of Prompt" → "Prompt ambiguity", "Proposed Protocol" → "Proposed protocol",
  "dot" → "point", "piece" → "part", "string" → "chain", "the same index" → "the same
  prompt", "business category" → "application category", "A stored spread" → "A
  propagation from memory", "path order" → "processing order", "Advertise" → "Report",
  "self-deployable tracker" → "deployable autonomous tracker", "release" → "output",
  "corrected to $t+2$ s" → "corrected at $t+2$ s"); trailing section renamed "Sources"
  and split into scientific and implementation sources; closing provenance line
  replaced. Front matter unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/90-segmentation/94-sam-sam2.md): expected answer of CV-SAM-002
  corrected as quoted above. Further explanations and blocking errors received the same
  language fixes as the appendices, plus "causation" → "causality", "self-contained and
  classified MOT" → "autonomous, classified multi-object tracking", "keep confusion" →
  "preserve a confusion", "births of tracks" → "track births", "delay" → "latency",
  "Confound object mask and business class" → "Confusing an object mask with an
  application class", "Assimilate spread of masklets" → "Equating masklet propagation".
  Source lines now cite exact sections and code lines instead of the garbled
  "time protocols built without execution SAM 2" label. Questions, IDs, objectives,
  families, tags and target deck unchanged.

No other vault file contradicts this note (`rg` over `vault/` for SAM, SAM 2 and Segment
Anything: CV-OPENVOC, CV-VLM and CV-SOT only link to it).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SAM-01 | CV-SAM | Diagnose a SAM 2 masklet that switches to a look-alike object after a crossing or a long occlusion: which signals to inspect (presence score, frame of the switch, memory span) and which remedies apply online versus offline | No diagnosis card exists for this subject; the failure is the main stated limitation of SAM 2 | Diagnosis; Failure modes and worked example B | 1 card, 3 criteria | [Ravi et al. 2024, §4 and App. C](https://arxiv.org/abs/2408.00714) |
| P-CV-SAM-02 | CV-SAM | Map a click and a box from an original image to SAM's resized and padded input, and state the size of one output logit cell in original pixels | The data contract (resize, padding, quarter-resolution logits) explains fine-structure losses and coordinate bugs; no practice card covers it | Practice; worked example A | 1 card, 3 criteria | [Kirillov et al. 2023, App. A](https://arxiv.org/abs/2304.02643); [segment-anything transforms.py and sam.py at dca509f](https://github.com/facebookresearch/segment-anything/blob/dca509fe793f601edb92606367a655c15ac00fdf/segment_anything/utils/transforms.py) |

## Sources

Scientific sources, opened at the passages listed (arXiv PDFs, text extracted with
`pdftotext`):

- Kirillov et al. 2023, [arXiv 2304.02643v1](https://arxiv.org/abs/2304.02643): §2, §3, §4 opening, §7.1, §7.4 heading, §7.5, §8, App. A, App. B opening, Fig. 4 and Fig. 13 captions.
- Ravi et al. 2024, [arXiv 2408.00714v2](https://arxiv.org/abs/2408.00714): footnote 1, §3, §4, §6.1–§6.3, Table 4, §7 opening, App. A.2 (Table 9), App. B, App. C, App. D.1, App. D.3.
- Pont-Tuset et al. 2017, [arXiv 1704.00675](https://arxiv.org/abs/1704.00675): §3.

Implementation sources (fetched from `raw.githubusercontent.com` at fixed commits; the
repositories have no release tag readable through the API used):

- [segment-anything `dca509f`](https://github.com/facebookresearch/segment-anything/tree/dca509fe793f601edb92606367a655c15ac00fdf): `predictor.py` L1–L170, `utils/transforms.py` L30–L102, `modeling/sam.py` L15–L175.
- [sam2 `2b90b9f`](https://github.com/facebookresearch/sam2/tree/2b90b9f5ceec907a1c18123530e92e794ad901a4) (2024-12-16): `sam2/sam2_video_predictor.py` L15–L240, L300, L430–L560, L620–L680, L780–L870.

Failed accesses and limits:

- Context7 was not available; the official repositories were read at commits instead of
  versioned documentation.
- XMem++, Cutie and RITM were not opened; they appear only as the baselines named by the
  SAM and SAM 2 papers.
- The default number $M$ of prompted-frame memories was not found in the passages read
  and is not given in the note.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/94-sam-sam2.py` | 12 checks passed |
| `git diff --check -- vault/90-segmentation/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/90-segmentation/94-sam-sam2.md` | 3 cards, 282 to 364 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card header, block, ID, question, tags and deck lines identical; front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced; card paragraphs repeated in the appendices identical |

No model was run; the baseline and variation are protocols, not results. The Mermaid
diagram and tables were not rendered in Obsidian, and AnkiDroid rendering is unverified.
This is agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-SAM revision 8,
CV-SAM-001 to 003, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-SAM-01, P-CV-SAM-02).
