# Review — Visual representations, ViT, Swin, ConvNeXt and DINOv2 — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the comparison note for visual representations and their
adaptation. Text-aligned embeddings stay in
[CV-CLIP](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md)
and feature-based anomaly detection in
[CV-ANOMALIES](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md).
Inventory item APP-059 (LoRA and visual adapters) names this note as its introduction;
the mechanism is now developed at comparison depth, which does not close the item.
The French pre-migration text (`git show b7142bb^:…`) was used to resolve the
mistranslations listed below.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | $N=HW/P^2$ and ×4 tokens, ×16 attention term: confirmed (ViT §3.1; Swin §3.2 eq. 1 for the quadratic term). Blocking error "to transform everything" mistranslated *pour tout transformer* (for the whole transformer); "small faults", "target material" (hardware) | Reasoning: token and attention scaling with resolution | 2 expected criteria; 345 → 352 lexical words | Wording aligned with the reference appendices | Minor | Language fixes; Source line given ViT §3.1 and Swin §3.2 |
| CV-REPRESENTATIONS-002 | Swin's shifted local windows and hierarchy, ConvNeXt as a ConvNet modernized "without introducing any attention-based modules": confirmed (Swin §3.1–§3.2; ConvNeXt §2, Fig. 2); recipe versus architecture supported by ConvNeXt §2.1 (76.1% → 78.8% from the recipe alone). Expected answer "offset local window hierarchy" blurred *shifted windows*; blocking error unintelligible | Comparison: attention organization versus convolution | 2 expected criteria; 345 → 348 | Source line cited ViT and DINOv2 for a Swin/ConvNeXt claim | Minor | Expected-answer language fix; blocking error rewritten from the French; Source line replaced |
| CV-REPRESENTATIONS-003 | Frozen DINOv2 features still need a head and a decision protocol; linear dense probes upsample a low-resolution logit map: confirmed (DINOv2 §1, §7.4). "From the token to the default zone" mistranslated *défaut* (defect); "flashcard low resolution" (*low-resolution map*) in the Source line | Understanding: from features to an evaluable inspection system | 2 expected criteria; 357 → 358 | Wording aligned with the reference appendices | Minor | Language fixes; Source line given DINOv2 §1 and §7.4 |
| CV-REPRESENTATIONS-004 | LoRA $\Delta W=BA$, $r(d+k)$ parameters, mergeable without latency unlike adapters: confirmed (LoRA §3, §4.1). Expected answer "They drive a head … or a smaller set-up" mistranslated *entraînent* (train) and *partie paramétrée plus réduite*. Missing limitation for the comparison objective: full fine-tuning can underperform linear probing out of distribution, and LP-FT mitigates it (Kumar et al., abstract, §4) | Comparison: adaptation scope under data, memory and deployment constraints | 3 expected criteria; 364 → 417 | One sentence with the Kumar et al. averages added to "Proposed comparison" (a card-only paragraph) | Minor | Meaning-restoring fix of the expected answer; sourced sentence added; language fixes; Source line given LoRA, Houlsby §2.1, Kumar et al. |
| CV-REPRESENTATIONS-005 | Loader contract (order, range, normalization, interpolation, crop): consistent with torchvision 0.20's `ImageClassification` and DINOv2's evaluation transform (bilinear versus bicubic). "Cookie file" mistranslated *fichier témoin* (reference file); "chargers" (loaders), "strings" (pipelines), "witness" (control), "drive" (training) | Diagnosis: input-contract regression before retraining | 2 expected criteria; 343 → 346 | Source line cited the DINOv2 abstract only | Minor | Language fixes; Source line given the torchvision and DINOv2 transform code at a version |

Expected-answer changes (no change of criteria):

- CV-REPRESENTATIONS-002 (language): "No: Swin uses an offset local window
  hierarchy; ConvNeXt remains a modernized ConvNet." → "No: Swin uses a hierarchy of
  shifted local windows; ConvNeXt remains a modernized ConvNet."
- CV-REPRESENTATIONS-004 (meaning-restoring, from the French original): "They drive a
  head, the whole model or a smaller set-up, respectively; learning costs and
  flexibility differ." → "They train a head, the whole model or a smaller
  parametrized part, respectively; training costs and flexibility differ."

## Reference findings

Claims of revision 7 checked against their passages:

- $N=HW/P^2$ and the quadratic attention term: confirmed (ViT §3.1; Swin §3.2).
- "MAE is pretrained by masked reconstruction, not by a final segmentation head":
  confirmed (MAE §1, Fig. 1).
- "DINOv2 learns features that can be transferred by self-supervision; a suitable
  head and protocol remain necessary": confirmed (DINOv2 §1, §7.4).
- "DINOv2 and DINO detector are not the same method": kept as a naming note; no
  source was opened for the detector.

No scientific error was found in revision 7. Its body held one to three sentences
per section and contained mistranslations: "No drive/checkpoint executed"
(*training*), "For multiple H,W side of patch P", "global tokens/denses".

New claims verified for revision 8 (main ones):

- ViT: patches, class token, learned 1D positions, weaker inductive bias, "large scale
  training trumps inductive bias", fine-tuning at higher resolution with 2D
  interpolation of position embeddings (§1, §3.1, §3.2).
- Swin: 4×4 patches, patch merging, eqs. 1–2, $M=7$, shifted windows (§3.1, §3.2).
- ConvNeXt: modernization without attention (§2, Fig. 2), recipe effect 76.1% →
  78.8% (§2.1), stage ratio and patchify stem (§2.2), 82.0% versus Swin-T 81.3%.
- DINOv2: frozen features (§1), LVD-142M curation (§3), 518-pixel final phase (§4),
  resolution cost about 3× at 416 pixels (§6.6), linear and "+ms" dense evaluation,
  frozen ViT-Adapter result 60.2 mIoU, 28 hours on 16 V100 (§7.4).
- MAE: 75% masking, encoder on visible patches (§1, Fig. 1); linear probing and
  fine-tuning "largely uncorrelated", 73.5% → 81.0% when tuning one block (§4.3).
- Kumar et al.: +2% ID, −7% OOD for fine-tuning versus linear probing; LP-FT +1% ID,
  +10% OOD over fine-tuning, on ten shift datasets (abstract, §4.1, §4.2).
- LoRA: $W_0+BA$, initialization, $\alpha/r$, merging, adapter latency (§3, §4.1);
  Houlsby adapters with skip connection and near-identity initialization (§2.1).
- HOG default detector settings (Dalal and Triggs §6).

Implementation facts recorded in the note (FR-036): torchvision 0.20's preset uses
bilinear resizing and its `convert_image_dtype` leaves float tensors unscaled, so a
float image in $[0,255]$ reaches normalization without division (project deduction
from the code); DINOv2's evaluation transform uses bicubic resizing; torchvision's
ViT asserts its exact training size; DINOv2 interpolates position encodings but
asserts sides divisible by 14.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 337 → 3,683. The note
compares six families and four adaptation protocols; architecture details beyond
what a choice needs are linked to the primary papers.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Input contract with versioned presets; global, dense and multi-scale output contracts with shapes; pipeline role |
| Intuition | Shallow | Developed | Structure each family imposes (HOG, CNN, ViT, Swin, ConvNeXt, self-supervision); constructed scratch-footprint illustration |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-SIFT, CV-ACQUISITION, CV-ANOMALIES, CV-CLIP, CV-SEGMENTATION, CV-DETECTEURS, CV-FIABILITE, CV-QUANT |
| Assumptions | Shallow (one sentence) | Developed | Pretraining domain; patch and stride geometry; resolution changes and position embeddings; linear separability; feature distortion under shift; degenerate inputs |
| Procedure | Shallow | Developed | Seven-step protocol with purposes; family comparison table |
| Mathematics | Shallow (one formula) | Developed | Token and attention terms; Swin eqs. 1–2; worked examples A (tokens and defect footprint) and B (window versus global cost); MAE encoder cost; LoRA; normalization and channel-swap signatures; HOG size; cosine similarity |
| Parameters | Shallow (list) | Developed | Seven-row parameter table with source values; tuning approach |
| Properties | Absent (merged with parameters) | Developed | Inductive bias and scale; linear-cost limits; architecture versus recipe; frozen-feature evidence and its limits; uncalibrated similarities; naming |
| Cost and implementation | Shallow | Developed | Inference, training and pretraining cost drivers; torchvision 0.20 and DINOv2 contracts; execution status |
| Evaluation | Shallow | Developed | Protocols and what each measures; published results with protocol; proposed baseline and resolution variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices from HOG to full fine-tuning and text-aligned embeddings; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/71-representations-transfert.py`](checks/71-representations-transfert.py)
(12 assertions): 196 → 784 tokens and ×16; 256 and 1,369 tokens for /14 at 224 and
518 pixels; 128-pixel patch footprint, 0.16 patch side and 2.4% area for a 20-pixel
scratch, 1.4 patches and 100 tiles at native resolution; Swin attention ratios 64 and
256 and a 13.8× total at $C=96$; MAE 49 visible tokens; LoRA 12,288 versus 589,824
parameters; normalization 0.074 versus 556.8 and the 255× slope; channel-swap
signature; HOG 3,780 dimensions.

## Applied corrections

- [Reference](../../../vault/70-reconnaissance-representations/references/71-representations-transfert.md),
  revision 7 → 8: body rewritten and deepened as above; mistranslations fixed in the
  appendices, identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "derivation of cost" → "Derivation of
  the cost", "Interface Trap" → "Interface trap", "cookie file" → "reference file",
  "chargers" → "loaders", "From the token to the default zone" → "From tokens to the
  defect region", "Parametrisation LoRA" → "LoRA parametrization", "Pretreatment
  Invariant" → "Preprocessing invariant", "witness" → "control", "staggered windows"
  → "shifted windows", "flashcard low resolution and interpolation" →
  "low-resolution logit map and upsampling"); sources split; closing provenance line
  replaced. Front matter unchanged except `revision`; H1, per-card headings and
  appendix headings kept.
- [Cards](../../../vault/70-reconnaissance-representations/71-representations-transfert.md):
  two expected answers fixed (quoted above); one sourced sentence added to
  CV-REPRESENTATIONS-004; language fixes in all further explanations and blocking
  errors; Source lines replaced by sections relevant to each card, without math in
  link labels. Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for `LoRA`,
`LP-FT`, `linear prob`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). No CV-REPRESENTATIONS proposal is registered yet; the 2026-10-20
report holds an unregistered proposal "Interpret dense tokens and global tokens",
which P-CV-REPRESENTATIONS-01 takes up with a quantitative criterion.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-REPRESENTATIONS-01 | CV-REPRESENTATIONS | Compute the footprint of one patch in original pixels after resizing, compare it with a defect size, and decide between resizing, tiling or a finer-stride backbone | Practice family absent; resolution versus patch geometry is untested (revives the 2026-10-20 dense-versus-global proposal) | Practice; Mathematics, worked example A | 1 card, 3 criteria | [ViT §3.1](https://arxiv.org/html/2010.11929v2); [DINOv2 §7.4](https://arxiv.org/html/2304.07193v2) |
| P-CV-REPRESENTATIONS-02 | CV-REPRESENTATIONS | Explain why a linear-probe score and a fine-tuning score can rank two backbones differently, and why fine-tuning can lose out of distribution | Evaluation family absent; protocol choice is untested | Evaluation; Evaluation and controlled variation | 1 card, 3 criteria | [MAE §4.3](https://arxiv.org/html/2111.06377); [Kumar et al., abstract and §4](https://arxiv.org/html/2202.10054) |

## Sources

Scientific sources, opened at the passages listed (arXiv HTML unless stated):

- ViT [2010.11929v2](https://arxiv.org/html/2010.11929v2): §1, §3.1, §3.2.
- Swin [2103.14030v2](https://arxiv.org/html/2103.14030v2): §3.1, §3.2.
- ConvNeXt [2201.03545](https://arxiv.org/html/2201.03545): §2, §2.1, §2.2, §2.5, final micro-design result.
- DINOv2 [2304.07193v2](https://arxiv.org/html/2304.07193v2): §1, §3, §4, §6.6, §7.4.
- MAE [2111.06377](https://arxiv.org/html/2111.06377): §1, Fig. 1, §4.3.
- Kumar et al. [2202.10054](https://arxiv.org/html/2202.10054): abstract, §4.1, §4.2 headings.
- LoRA [2106.09685v2](https://arxiv.org/html/2106.09685v2): §3, §4.1.
- Houlsby et al. [1902.00751](https://arxiv.org/html/1902.00751): §2.1.
- Dalal and Triggs, [HOG PDF](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf) (text extracted with `pdftotext`): §6.

Implementation sources:

- torchvision v0.20.0: [`transforms/_presets.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/transforms/_presets.py) L38–L64; [`transforms/_functional_tensor.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/transforms/_functional_tensor.py) L66–L74; [`models/vision_transformer.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/models/vision_transformer.py) L180, L214–L221, L266–L273, L351–L357, L789–L801.
- DINOv2 at commit [`7764ea0`](https://github.com/facebookresearch/dinov2/tree/7764ea0f912e53c92e82eb78a2a1631e92725fc8): `hub/backbones.py` L33–L34, L114–L172; `models/vision_transformer.py` L182–L205, L257–L272, L301–L330; `layers/patch_embed.py` L72–L73; `data/transforms.py` L42–L43, L76–L91.

Failed accesses and limits:

- The DINOv2 repository has no release tag; a commit of `main` was pinned instead.
- Not opened: the DINO detector paper, "Vision Transformers Need Registers" (register
  tokens are only named, from the code), PointNet-style or other backbones.
- Context7 was not available in this session; versioned code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/71-representations-transfert.py` | 12 checks passed |
| `git diff --check` on the subject's files | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/70-reconnaissance-representations/71-representations-transfert.md` | 5 cards, 346–417 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 7` → `8`; H1 and the 12 per-card headings unchanged; `$$` balanced |

No model, loader or training run was executed; the proposed baseline and variation
are protocols, not results. AnkiDroid rendering of the corrected cards and Obsidian
rendering of the tables are unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export
status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-REPRESENTATIONS revision 8, CV-REPRESENTATIONS-001 to -005, corrections listed
above, Agent Claude Code self-review, to republish with `paquet-anki`) and the
proposal register (P-CV-REPRESENTATIONS-01, P-CV-REPRESENTATIONS-02).
