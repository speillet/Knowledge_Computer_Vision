# Review — Open-vocabulary detection and grounding — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 7 to revision 8. Highest severity per card before correction: 0 blocking,
0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

Revision 7 had a body of 280 words with one or two sentences per contract section and
no equation, procedure, parameter value, protocol or source split. The deepened note
covers detector-level open vocabulary (ViLD, OWL-ViT, GLIP, Grounding DINO) and the
LVIS protocol. Image-level text scoring stays in
[CV-CLIP](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md)
and generative models in
[CV-VLM](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md), both
linked rather than restated.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OPENVOC-001 | Image-level similarity does not give instances or boxes: consistent with OWL-ViT §3.1 (per-token boxes and queries) and Grounding DINO §3.2–§3.3. Expected answer said "Image ranking" for image classification; "the prompt is missing from the image", "referential grounding", "allows to check"; source pointed to "§3.1: adaptation to location" on the abstract page | Comparison: image classification versus detection contract | 2 criteria; 371 → 370 words | Aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; OWL-ViT source given as HTML v2 §3.1 |
| CV-OPENVOC-002 | Catalogue comparison protocol: project design, consistent with the reference's controlled variation and with worked example B (argmax relabelling). "Reserve new products unknown to the setting", "useful point of operation", "Time division of the test", "favorable photograph" | Design: choose and validate a system for a changing catalogue | 3 criteria; 383 → 379 words | Aligned with the appendix | Minor | Language fixes in explanation, blocking errors and grading criteria |
| CV-OPENVOC-003 | Broad prompts cause semantically related boxes; separate localization from vocabulary: consistent with GLIP §5.2 (prompt wording changes AP50) and the official Grounding DINO thresholds. "Survey built", "denial", "invariant threshold to prompt", "decision-making model" | Diagnosis: vocabulary versus localization | 1 criterion list; 353 → 351 words | Aligned with the appendix | Minor | Language fixes; official code added to the source line |

Expected-answer change (CV-OPENVOC-001, meaning-restoring language fix): "Image
ranking is about the global image; detection must also locate instances with a
suitable output protocol." → "Image classification scores the whole image; detection
must also locate instances, with a suitable output protocol."

## Reference findings

Claims of revision 7 checked: OWL-ViT and Grounding DINO "link visual representations
and language to produce regions" (confirmed, OWL-ViT §3.1, Grounding DINO §3); score
normalization is model-specific and does not certify presence (consistent with both
post-processing codes, which threshold uncalibrated sigmoid scores). No scientific
error was found; the body was shallow and contained mistranslations ("grounding
repository", "monthly update gain", "box-rated detection", "Question of work",
"Reference Response", "Survey built", "Time division of the test").

New claims verified for revision 8 (main ones): ViLD base/novel split (866/337 LVIS,
48/17 COCO), ViLD-text eq. 2 with background embedding, crop ensembling and the
~2-point AR drop of base-only proposals on novel categories; OWL-ViT no-fusion
architecture, per-token boxes biased to patch centres, 576 tokens at B/32 and 768 px,
focal sigmoid loss with federated negatives and ≥50 pseudo-negatives, removal of rare
LVIS boxes, 1203 queries with seven templates, Table 1 values, deduplication, GFLOPs
comparison; GLIP eqs. 1–3, token expansion, mean token probability, equivalence of
detection and grounding, deep fusion, "stingray" prompt example; Grounding DINO
feature enhancer, Algorithm 1 (900 queries), cross-modality decoder, sub-sentence
masks, loss and matching weights, 256 tokens, Objects365 overlap with COCO, 52.5 AP
with O365/OI/GoldG, ODinW 26.1, Table 14 efficiency; LVIS federated positive and
negative sets, non-exhaustive flags and hierarchy rule.

Disagreements between implementations, recorded in the note (FR-036):

| Aspect | Official Grounding DINO (commit 856dde2) | transformers v5.23.0 |
| --- | --- | --- |
| Box threshold default | 0.35 in `predict_with_caption` and the README demo | 0.25 in `post_process_grounded_object_detection` |
| Label | Decoded tokens above `text_threshold`, then substring mapping to classes in `predict_with_classes` | Decoded tokens above `text_threshold`; no class mapping |
| OWL-ViT label | — | Argmax over queries, then sigmoid, threshold 0.1, no NMS (paper: one probability per query and object) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 280 → 4,360, of which about 620 are table cells
and 110 pseudocode and Mermaid lines.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Three task variants, input vocabularies and caption limits, preprocessing contracts, output formats and post-processed labels, pipeline roles, versioning of the vocabulary |
| Intuition | Shallow | Developed | Text embeddings replacing the classifier matrix (ViLD, OWL-ViT, GLIP), localization transfer, late versus deep fusion, constructed warehouse illustration, Mermaid data flow |
| Prerequisites | Developed (two links) | Developed | CV-IOU-AP, CV-NMS, CV-FIABILITE, CV-VLM links and target competencies |
| Assumptions | Absent | Developed | Visual grounding of names, distinguishability, localization transfer, meaning of "zero-shot", score comparability, capacity; degenerate cases |
| Procedure | Shallow | Developed | Inference and evaluation pseudocode with purpose of each step; ViLD, OWL-ViT, GLIP and Grounding DINO recipes |
| Mathematics | Shallow (one sentence) | Developed | ViLD eq. 2, GLIP grounding scores and token expansion, Grounding DINO query selection; worked examples A (token aggregation and label mapping), B (argmax relabelling), C (LVIS federated counting), D (capacity and caption chunking) |
| Parameters | Shallow (list) | Developed | Seven-row table with source values and interactions; five-step tuning approach |
| Properties | Absent | Developed | Interface versus accuracy, empirical results under protocols, late versus deep fusion coupling, calibration, detection-grounding equivalence |
| Cost and implementation | Shallow | Developed | Cost drivers for both fusion types with reported GFLOPs and FPS; official Grounding DINO and transformers contracts with line numbers; execution status |
| Evaluation | Shallow (one baseline sentence) | Developed | Protocol table (LVIS OVD, LVIS zero-shot, COCO OVD, COCO transfer, REC); baseline and vocabulary-addition variation with confounds; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Seven-row Symptom / Causes / Check / Remedy table |
| Alternatives and sources | Shallow | Developed | Five conditional choices; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/83-detection-open-vocabulary.py`](checks/83-detection-open-vocabulary.py)
(9 assertions): GLIP mean versus Grounding DINO max token score (0.40 versus 0.60),
partial-phrase label at `text_threshold` 0.25, substring-mapping failures and order
dependence, OWL-ViT argmax relabelling (0.881 → 0.909 with the "bolt" sigmoid
unchanged), LVIS federated counts (2 TP, 2 FP, 3 ignored), token counts per ViT
configuration (576, 2304, 3600) and the 10-chunk lower bound for 1203 names under 256
tokens.

## Applied corrections

- [Reference](../../../vault/80-detection-pose/references/83-detection-open-vocabulary.md),
  revision 7 → 8: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Documentary reference" → "Source consulted",
  "Survey built" → "Constructed investigation", "Time division of the test" →
  "Splitting the test over time", "Separate vocabulary and location" → "Separate
  vocabulary from localization"); sources split; closing provenance line replaced.
  Front matter unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/80-detection-pose/83-detection-open-vocabulary.md): the
  expected-answer fix above; 18 exact replacements in explanations, blocking errors,
  grading criteria and two Source lines. Questions, IDs, objectives, families, tags,
  target deck and the `## CV-OPENVOC-002` heading (link target) unchanged.

No other vault file repeats a claim corrected here.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-OPENVOC-01 | CV-OPENVOC | Given detections of one category on images of its positive set (exhaustive or not), its negative set and other images, count true positives, false positives and ignored detections under LVIS rules, and explain the consequence for open-vocabulary outputs | No evaluation card; the federated protocol behind most open-vocabulary results is untested | Evaluation; worked example C | 1 card, 3 criteria | [LVIS §2.2–§2.3](https://arxiv.org/html/1908.03195v2); [ViLD §4.1](https://arxiv.org/html/2104.13921v3) |
| P-CV-OPENVOC-02 | CV-OPENVOC | From per-token probabilities and the box and text thresholds, derive a grounding detector's box score, label and mapped class, and name the failure when only part of a phrase passes the text threshold | The output contract (token scores to category id) is untested, although it causes silent label errors | Practice or reasoning; worked example A | 1 card, 3 criteria | [GLIP §3.1](https://arxiv.org/html/2112.03857v2); [Grounding DINO code, `inference.py` L53–L97, L264–L273](https://github.com/IDEA-Research/GroundingDINO/blob/856dde20aee659246248e20734ef9ba5214f5e44/groundingdino/util/inference.py#L53-L97) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed (arXiv HTML converted to text):

- Minderer et al., OWL-ViT, [arXiv HTML v2](https://arxiv.org/html/2205.06230v2): §3,
  §3.1, §3.2, §4.1, §4.2, §4.3 (Table 1 and text).
- Liu et al., Grounding DINO, [arXiv HTML v4](https://arxiv.org/html/2303.05499v4):
  abstract, §3, §3.1–§3.5 (Algorithm 1), §4.1, §4.2 (Table 2 rows and footnote 4),
  App. A, App. I (Table 14).
- Li et al., GLIP, [arXiv HTML v2](https://arxiv.org/html/2112.03857v2): §3.1 (eqs.
  1–3 and footnotes), §3.2 (eqs. 4–5 opening), §4.1 sentence on supervised COCO, §5.2
  (manual prompt tuning).
- Gu et al., ViLD, [arXiv HTML v3](https://arxiv.org/html/2104.13921v3): abstract, §1,
  §3.2, §3.3 (eq. 2), §4.1, §4.2.
- Gupta et al., LVIS, [arXiv HTML v2](https://arxiv.org/html/1908.03195v2): §2.2, §2.3.

Implementation sources (read as raw files):

- [IDEA-Research/GroundingDINO, commit 856dde2](https://github.com/IDEA-Research/GroundingDINO/tree/856dde20aee659246248e20734ef9ba5214f5e44):
  `groundingdino/util/inference.py` L22–L26, L37–L48, L53–L97, L150–L273;
  `groundingdino/util/utils.py` L599–L610 (`get_phrases_from_posmap`); README
  L99–L106, L231–L241.
- [transformers v5.23.0](https://github.com/huggingface/transformers/tree/v5.23.0/src/transformers/models):
  `grounding_dino/processing_grounding_dino.py` L130–L212;
  `owlvit/image_processing_owlvit.py` L102–L114, L126–L177.

Failed accesses and limits:

- Context7 was not available in this session; official code at a commit or release
  tag replaced it.
- The LVIS v1 frequency bins (rare, common, frequent) are cited through ViLD §4.1; the
  LVIS paper version read (v2, 2019) does not define them.
- Grounding DINO's FPS figures are cited without hardware because the appendix passage
  does not state it.
- OVR-CNN (Zareian et al. 2021), which introduced the open-vocabulary detection
  setting, was downloaded but not used for any claim.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/83-detection-open-vocabulary.py` | 9 checks passed |
| `git diff --check -- vault/80-detection-pose/ docs/revues/2026-11-14-reference-depth/checks/83-detection-open-vocabulary.py` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/80-detection-pose/83-detection-open-vocabulary.md` | 3 cards, 351 to 379 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` and fences balanced; every appendix paragraph identical to its card paragraph; local links resolve |

No open-vocabulary model was run; the controlled variation is a protocol, not a
result. The Mermaid diagram and tables were not rendered in Obsidian, and AnkiDroid
rendering is unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-OPENVOC revision 8, CV-OPENVOC-001 expected-answer fix and language fixes in all
three cards, Agent Claude Code self-review, to republish with `paquet-anki`) and the
proposal register (P-CV-OPENVOC-01, P-CV-OPENVOC-02).
