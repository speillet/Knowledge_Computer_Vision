# Review — VLMs, grounding and the vision–action boundary — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The French text before the English migration (`git show b7142bb^:<path>`) was used to
restore the meaning of ambiguous translations ("commande" → control, "conditions de
rejet" → rejection conditions, "sorties temporelles" → temporal outputs).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VLM-001 | CLIP scores pairs, a VLM generates conditioned tokens, a VLA outputs actions: confirmed (CLIP §2.3; LLaVA §4.1–4.2; OpenVLA §3.2; RT-2 §3.2). OpenVLA cited only by its project page. "validated order policy" mistranslated *control policy* | Comparison of output contracts | 3 criteria; 359 → 362 words | Aligned with the reference appendix | Minor | Language fixes; Source given paper sections |
| CV-VLM-002 | Q-Former bridges a frozen image encoder and a frozen LLM with 32 learned queries and two-stage pre-training: confirmed (BLIP-2 §§3.1–3.3). Expected answer omitted "frozen" and its word order made "pre-trained by a learned representation" ambiguous. "Goulot" left untranslated | Understanding of a connector | 2 criteria; 291 → 301 words | Aligned | Important (expected answer imprecise on the central condition) | Expected answer corrected; language fixes; Source fixed |
| CV-VLM-003 | Sampling $T/\Delta$, retrieval recall, baselines: project protocol consistent with Flamingo §2.1 (1 frame/s sampling, 64 visual tokens). "time outputs", "discharge conditions", "fluidity", "Choice of exit" mistranslated | Design of a video index | 3 criteria; 389 → 394 words | Aligned | Minor | Expected-answer term restored ("temporal outputs"); language fixes; Source given a section |
| CV-VLM-004 | Matched negatives, one intervention at a time, coverage versus error: consistent with POPE §5.1 and LLaVA's hallucination limitation. "Survey", "Anchor tests built", "structured visual string", "phrase fluid" mistranslated | Diagnosis of hallucination versus missing observation | 3 criteria; 377 → 379 words | Aligned | Minor | Language fixes; POPE added to the Source |

Expected-answer changes:

- CV-VLM-002 (sourced correction, BLIP-2 §3: "Q-Former as the trainable module to
  bridge the gap between a frozen image encoder and a frozen LLM"): "Connect a visual
  encoder and a language model pre-trained by a learned representation and adapted
  training." → "Connect a frozen pre-trained image encoder and a frozen pre-trained
  language model through a learned intermediate representation (learned queries) and
  an adapted two-stage training."
- CV-VLM-003 (meaning-restoring language fix, French "sorties temporelles"): "time
  outputs" → "temporal outputs".

The objective line of CV-VLM-004 ("Distinct hallucination and insufficient
observation") is ungrammatical; objectives are protected, so it is reported, not
edited. Proposed: "Distinguish hallucination from insufficient observation."

## Reference findings

Revision 6 claims checked: BLIP-2's Q-Former, LLaVA's connector with instruction
tuning, Flamingo's interleaved inputs and the VLA action interface are confirmed.
Imprecisions: "LLaVA combines connector and tuning instruction according to version"
(instruction tuning), "Vary quickly and negative controlled" (prompt and controlled
negatives), "research or sampling strategy" (search), "drive" (training). The
revision-6 body had no data contract (resolution, coordinates, sampling), no
hallucination metrics and no grounding protocol.

New verified content: CLIP's $N\times N$ contrastive objective; BLIP-2's
$32\times768$ queries against $257\times1024$ features, 188M parameters, three
objectives and soft visual prompts; LLaVA eqs. 1 and 3, 595K stage-1 pairs, frozen
encoder, "bag of patches" example and hallucination limitation; Flamingo's 64-token
resampler, 1 frame/s video sampling, $\tanh(\alpha)$ gating with $\alpha=0$ at
initialization, per-image attention masking; Florence-2's 1,000 location bins and
region formats, 384 and 768 px training resolutions; RT-2's 256 uniform bins and
8-integer actions; OpenVLA's 256 bins between the 1st and 99th percentiles; $\pi_0$'s
$H=50$ chunks, flow matching and up to 50 Hz; CHAIR definitions and the beam-size
observation with its condition; POPE's sampling strategies, 1:1 balance, metrics and
yes ratio.

## Reference depth

Body word counts (whitespace tokens, front matter excluded, H1 included, before the
first per-card appendix): 351 → 2,663.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Four-interface table with inputs, outputs and what each can support; resolution, coordinate, sampling and action-space contract; project definition of grounding; pipeline role |
| Intuition | Shallow | Developed | Connector designs and what passes to the LLM; language-prior illustration from LLaVA's limitations |
| Prerequisites | Shallow (two links) | Developed | Links to CV-OPENVOC, CV-SAM, CV-IOU-AP |
| Assumptions | Absent | Developed | Resolution, bottleneck, domain, temporal coverage, prompt and decoding, action space; degenerate cases |
| Procedure | Shallow | Developed | Seven-step evaluation-centred procedure with purposes |
| Mathematics | Shallow | Developed | CLIP objective, LLaVA eqs. 1 and 3, BLIP-2 bottleneck, Flamingo gating and masking, location and action tokens, CHAIR and POPE; worked examples A–D |
| Parameters | Shallow (list) | Developed | Parameter table with effects and sourced decoding observation; tuning approach |
| Properties | Shallow | Developed | No grounding guarantee, frozen components, quantized structured outputs, image-causal attention, VLA outputs |
| Cost and implementation | Shallow | Developed | Cost drivers with variables, parameter counts, execution status; no library API claimed |
| Evaluation | Shallow | Developed | Protocols; baseline VLM against a detector pipeline with resolution as the controlled variation; reading and limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Six-row symptom table |
| Alternatives and sources | Shallow | Developed | Conditional choices, industrial uses labelled as project reasoning, sources split |

Constructed examples are recomputed by
[`checks/121-vlm-grounding.py`](checks/121-vlm-grounding.py) (9 checks): 257 tokens
for ViT-L/14 at 224 px, 10.7× compression by the Q-Former, 250 px per patch for a
4000 px image; 28,800 frames and about 7.4 million visual tokens for 8 h at 1 frame/s,
sampling probability $d/\Delta=0.4$; 4 px location bins, 0.39 mm action bins, 1 s
action chunk; always-"yes" model at accuracy 0.5 and F1 0.667.

## Applied corrections

- [Reference](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md),
  revision 6 → 7: body rewritten; appendix language fixes identical to the card
  fixes ("Question of work" → "Working question", "Reference Response" → "Reference
  answer", "bricks" → "building blocks", "Discriminant Ablation" → "Discriminating
  ablation", "Criterion of correction" → "Correction criterion", "Goulot of
  representation" → "Representation bottleneck", "Anchor tests built" →
  "Constructed grounding tests", "reserved events" → "held-out events", "drive" →
  "training"); sources split; closing line replaced.
- [Cards](../../../vault/120-generatif-multimodal/121-vlm-grounding.md): expected
  answers of 002 and 003 as quoted above; language fixes in all four cards including
  blocking errors and the "Grading criteria for the case" rubric; Source lines given
  paper sections. IDs, questions, objectives, families, tags, deck and the `## CV-VLM-003`
  and `## CV-VLM-004` anchors unchanged.

No other subject's card repeats a corrected claim.

## Proposals

To register as `pending` (register not edited in this pass):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-VLM-01 | CV-VLM | Explain why a hallucination probe must report the yes ratio and use popular and adversarial negatives, with the always-"yes" baseline | No evaluation card; a single accuracy or F1 hides a yes bias | Evaluation | 1 card, 3 criteria | [POPE §5.1](https://arxiv.org/html/2305.10355v3) |
| P-CV-VLM-02 | CV-VLM | Compute how many original pixels a VLM patch covers after resizing, and decide whether a small defect is observable before blaming the model | Resolution loss is the most frequent small-object failure and is untested | Reasoning | 1 card, 3 criteria | [BLIP-2 §3.1](https://arxiv.org/html/2301.12597v3); [Florence-2 §6.1](https://arxiv.org/html/2311.06242v1) |

No defective question was found.

## Sources

Scientific sources, read in arXiv HTML (converted locally) or PDF: CLIP §2.3 (PDF
v1); BLIP-2 §1, §3.1–3.3 (HTML v3); LLaVA §4.1–4.2, §5.1 limitations, hallucination
paragraph (HTML v2); Flamingo §2.1–2.3 and Appendix A.1.3 (HTML v2); Florence-2 §3,
§6.1 (HTML v1); RT-2 §3.2 (HTML v1); OpenVLA §1, §3.2 (HTML v3); $\pi_0$ §I, §IV
(HTML v1); CHAIR §2.1, §2.3, §3.2, §3.3 (HTML v2); POPE §5.1 (HTML v3). French
pre-migration card text from commit `b7142bb^`.

Implementation sources: none used; no library API is claimed. The OpenVLA project
page is retained but was not re-read. Context7 unavailable.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/121-vlm-grounding.py` | 9 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| Inventory of the card file | 4 cards, 362 / 301 / 394 / 379 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical (33); front matter identical except `revision`; H1 and `### CV-…` headings unchanged; `$` balanced |

No model was executed; the baseline and variation are proposed. Obsidian and
AnkiDroid rendering are unverified. Agent self-review, without independent
validation or measured learner proficiency. Export status: **to republish with
`paquet-anki`**.

For the coordinator: `Suivi-pilote.md` entry — 2026-11-14, CV-VLM revision 7, cards
001–004, corrections above, Agent Claude Code self-review, to republish with
`paquet-anki`; proposals P-CV-VLM-01 and -02.
