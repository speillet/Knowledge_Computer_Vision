# Review — CLIP, SigLIP and text-based recognition — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for contrastive image–text embeddings and their use
for zero-shot classification and retrieval. Region-level grounding stays in
[CV-OPENVOC](../../../vault/80-detection-pose/references/83-detection-open-vocabulary.md)
and generative vision–language models in
[CV-VLM](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md).
Inventory item APP-060 (SigLIP detailed loss) names this note as its introduction; the
loss is now given with its initialization and implementation, which does not close the
item. The French pre-migration text resolved the meaning of the mistranslations below.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | Zero-shot classification by text prototypes and a decision rule: confirmed; CLIP describes it as logistic regression with L2-normalized inputs and weights, no bias, temperature scaling, the text encoder acting as a hypernetwork (CLIP §3.1.2). "Correct piece / striped piece" mistranslated *pièce correcte / rayée* (good / scratched part); "research" (*retrieval*); "standard embeddings" (*normalized*); "legend generator" (*caption*) | Understanding: the vocabulary is the classifier | 2 expected criteria; 361 → 353 lexical words | Wording aligned with the reference appendices | Minor | Language fixes; Source line given CLIP §3.1.2, §3.1.4 and §6 |
| CV-CLIP-002 | Softmax over candidates is relative; $\log19\approx2.944$ gives 0.95 and a tied third candidate gives 19/39: recomputed (checks/72-clip-siglip.py). French decimal commas "2,94", "0,95", "0,487" | Reasoning: reject a misleading probability | 2 expected criteria; 367 → 366 | Decimal points restored identically in the card and the reference appendix | Minor | Expected-answer language fix; decimals; language fixes; Source line given CLIP §3.1.2 |
| CV-CLIP-003 | Softmax over the batch versus per-pair sigmoid with learned temperature and bias: confirmed (CLIP §2.3; SigLIP §3.2, Algorithm 1). "This lens change" mistranslated *changement d'objectif* (change of objective), "lot" (*batch*). Missing condition for the calibration point: SigLIP's bias, initialized at $-10$, encodes the training imbalance between one positive and the batch's negatives (SigLIP §3.2) | Comparison: what each objective trains scores to mean | 2 expected criteria; 352 → 398 | Sentence added to "Effect on evaluation", a card-only paragraph | Minor | Expected-answer language fix; sourced sentence added; Source line given CLIP §2.3 and SigLIP §3.2 |
| CV-CLIP-004 | Prompts selected on test leak information: consistent with CLIP's own caveat that repeatedly querying validation sets is "unrealistic for true zero-shot scenarios" (§6) and its near-duplicate analysis (§5) | Evaluation: protocol for text-defined classifiers | 3 expected criteria; 363 → 364 | Wording aligned with the reference appendices | Minor | Expected-answer language fix; language fixes ("reserved image", "field", "Proposed Protocol"); Source line given CLIP §3.1.4, §5, §6 |

Expected-answer changes (language, no change of criteria):

- CV-CLIP-002: "It normalizes scores between these candidates; the set may not contain
  any good descriptions and the model may be out of domain." → "It normalizes scores
  among these candidates; the set may contain no correct description and the model
  may be out of its domain."
- CV-CLIP-003: "SigLIP uses a loss sigmoid on pairs rather than a global softmax
  normalization of the batch like CLIP." → "SigLIP uses a sigmoid loss on individual
  pairs rather than a softmax normalization over the whole batch as in CLIP."
- CV-CLIP-004: "… measure errors and rejections on separate test by scene/domain." →
  "… measure errors and rejections on a separate test set split by scene or domain."

Card header defect (not edited; `Objective` lines are protected): CV-CLIP-003 has the
French objective "distinguer objectifs contrastifs". Proposed wording:
"Objective: distinguish contrastive objectives." The `Objective` line belongs to the
card header, which this pass must not change.

## Reference findings

Claims of revision 7 checked against their passages:

- "CLIP brings the positive pairs closer together and compares the candidates by a
  contrastive objective": confirmed (CLIP §2.3).
- "SigLIP uses a sigmoid objective in pairs with temperature/learned bias": confirmed
  (SigLIP §3.2, Algorithm 1).
- Similarity with an inverse temperature: confirmed (CLIP §2.3, §3.1.2).
- "Encode/index texts can be depreciated": mistranslation of *amortized*; corrected.
- "A contrast encoder alone does not generate a textual explanation": consistent with
  the method; kept as a contract statement.

No scientific error was found in revision 7. Other language defects: "standardization"
(*normalization*), "facing text classification", "Single".

New claims verified for revision 8 (main ones):

- CLIP: 400M pairs (§2.2); symmetric cross-entropy over the $N\times N$ matrix and
  log-parameterized temperature (§2.3); initialization at 0.07, clipping at 100, batch
  32,768 (§2.5); zero-shot classifier as logistic regression and text encoder as
  hypernetwork (§3.1.2); polysemy ("construction cranes and cranes that fly"), "A photo
  of a {label}." +1.3%, 80-prompt embedding-space ensemble +3.5%, almost 5% together
  (§3.1.4); near-duplicate detector (§5); validation-set use, fine-grained, counting,
  MNIST 88% (§6).
- SigLIP: loss with $z_{ij}=\pm1$ divided by the batch size, $t=\exp(t')$, imbalance at
  initialization, $t'=\log10$, $b=-10$ (§3.2, Algorithm 1); chunked implementation
  (§3.3); better than softmax below 16k batch, 32k sufficient (abstract, §1).

Implementation facts recorded in the note (FR-036): OpenCLIP v3.3.0 returns
unnormalized features from `encode_image` and `encode_text` by default, normalizes
inside `get_logits`, uses OpenAI normalization statistics distinct from ImageNet's,
and its `SigLipLoss` divides by the batch size as the paper does.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 314 → 3,174.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Tasks; preprocessing and tokenizer contract with versioned defaults; embedding and logit outputs; zero-shot as a text-generated classifier; pipeline role |
| Intuition | Shallow | Developed | Batch-matching versus pair-matching questions; constructed conveyor illustration; Mermaid decision flow |
| Prerequisites | Shallow (one link) | Developed | Links to CV-REPRESENTATIONS, CV-FLANN, CV-FIABILITE, CV-OPENVOC, CV-OCR, CV-ANOMALIES |
| Assumptions | Absent (merged with problem) | Developed | Closed candidate set; language and polysemy; pretraining domain and reported weaknesses; global embedding; meaning of softmax and sigmoid scores |
| Procedure | Shallow | Developed | Offline, online and evaluation pseudocode with purposes; CLIP versus SigLIP table |
| Mathematics | Shallow (one formula) | Developed | Similarity and temperature; both losses; worked examples A (scale), B (candidate set), C (SigLIP prior), D (prompt ensembling); calibration definition |
| Parameters | Shallow (list) | Developed | Seven-row parameter table with source values; tuning approach |
| Properties | Shallow | Developed | Zero-shot assumptions and the authors' validation caveat; relative scores; sigmoid and calibration; known weaknesses; global versus local |
| Cost and implementation | Shallow | Developed | Text and image cost; retrieval index size; training memory; OpenCLIP v3.3.0 contract; execution status |
| Evaluation | Shallow | Developed | Metrics including false acceptance and prompt disagreement; overlap analysis; published results with protocol; proposed baseline and vocabulary variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (closed classifier, CLIP-style, SigLIP-style, open-vocabulary detection, OCR, anomaly detection); industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/72-clip-siglip.py`](checks/72-clip-siglip.py) (9 assertions): softmax 0.953 at
logit scale 100 versus 0.574 at 10 for a 0.03 cosine gap; scale 14.3 at temperature
0.07; 0.95 from a $\log19$ gap for any offset and 19/39 with a tied third candidate;
SigLIP initial scores 0.5, 0.0067 and $4.5\times10^{-5}$ and the $3.05\times10^{-5}$
positive rate of a 32k batch; norm 0.866 of an averaged pair of prompt embeddings;
512,000 versus 40.96 million multiply-adds; 1.02 GB and 2.05 GB indexes.

## Applied corrections

- [Reference](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md),
  revision 7 → 8: body rewritten and deepened as above; mistranslations fixed in the
  appendices, identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Decision-making mechanism" →
  "Decision mechanism", "correct piece / striped piece" → "good part / scratched
  part", "research" → "retrieval", "standard embeddings" → "normalized embeddings",
  "Algebraic counter-example" → "Algebraic counterexample", decimal commas, "a lot" →
  "a batch", "reserved image" → "held-out image", "field" → "domain", "Documentary
  reference" → "Documentation consulted"); sources split; closing provenance line
  replaced. Front matter unchanged except `revision` (type `methode` kept); H1,
  per-card headings and appendix headings kept.
- [Cards](../../../vault/70-reconnaissance-representations/72-clip-siglip.md): three
  expected answers given language fixes (quoted above); one sourced sentence added
  to CV-CLIP-003; language fixes in all further explanations and blocking errors;
  Source lines cleaned of "see the 2026-10-30" fragments and given sections relevant
  to each card. Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for `SigLIP`,
`temperature`, `calibrated probab`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). No CV-CLIP proposal is registered yet; the 2026-10-20 proposal
"Effect of an additional candidate on softmax" was implemented in CV-CLIP-002's
explanation and is not repeated.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-CLIP-01 | CV-CLIP | Diagnose a zero-shot classifier that labels empty or unsupported images with high confidence: name the discriminating checks (raw cosine and margin, added background class, logit scale) and a validated rejection | Diagnosis family absent; rejection design is only implied | Diagnosis; Failure modes and diagnosis | 1 card, 3 criteria | [CLIP §3.1.2 and §6](https://arxiv.org/html/2103.00020v1) |
| P-CV-CLIP-02 | CV-CLIP | State the preprocessing and embedding contract of a CLIP checkpoint: its own normalization statistics and tokenizer, and L2 normalization before cosine scoring | Practice family absent; library defaults silently break similarity | Practice; Cost and implementation (OpenCLIP contract) | 1 card, 3 criteria | [OpenCLIP v3.3.0 `model.py` L326–L354](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/model.py#L326-L354) |

## Sources

Scientific sources, opened at the passages listed:

- Radford et al., CLIP, [arXiv HTML 2103.00020v1](https://arxiv.org/html/2103.00020v1):
  §2.2, §2.3, §2.5, §3.1.2, §3.1.4, §5, §6.
- Zhai et al., SigLIP, [arXiv PDF 2303.15343v4](https://arxiv.org/pdf/2303.15343v4) (text
  extracted with `pdftotext`; the HTML version returned an empty page): abstract, §1,
  §3.2, Algorithm 1, §3.3.

Implementation sources (official code at tag v3.3.0):

- [`src/open_clip/model.py`](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/model.py) L274–L302, L326–L354;
  [`transform.py`](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/transform.py) L18–L25;
  [`constants.py`](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/constants.py) L1–L4;
  [`factory.py`](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/factory.py) L829;
  [`loss.py`](https://github.com/mlfoundations/open_clip/blob/v3.3.0/src/open_clip/loss.py) L104–L153, L330–L380;
  model configurations `ViT-B-32.json` and `ViT-B-16-SigLIP.json`.

Failed accesses and limits:

- The SigLIP arXiv HTML page was empty; the PDF was used.
- The preprocessing attached to each pretrained SigLIP tag in OpenCLIP (`pretrained.py`)
  was not read; the note only states that `create_model_and_transforms` returns the
  checkpoint's preprocessing.
- Context7 was not available in this session; versioned OpenCLIP code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/72-clip-siglip.py` | 9 checks passed |
| `git diff --check` on the subject's files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/70-reconnaissance-representations/72-clip-siglip.md` | 4 cards, 353–398 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 7` → `8`; H1 and the 10 per-card headings unchanged; `$$` balanced |

No model was run; the proposed baseline and variation are protocols, not results.
AnkiDroid rendering of the corrected cards and Obsidian rendering of the Mermaid
diagram are unverified. This is agent self-review, without independent scientific
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-CLIP revision 8, CV-CLIP-001 to CV-CLIP-004, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`), the proposal register
(P-CV-CLIP-01, P-CV-CLIP-02) and the CV-CLIP-003 objective wording.
