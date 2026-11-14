# Review — Semantic, instance and panoptic segmentation — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the comparison and protocol note of the topic. U-Net, DeepLab, Mask
R-CNN and nnU-Net are described at the depth a choice of output needs; inventory items
APP-075 to APP-078 remain open for dedicated notes. Pending proposal
P-CV-SEGMENTATION-01 (worked PQ card) is unchanged; the reference body now contains a
worked PQ example that such a card could use.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Semantic, instance and panoptic contracts: confirmed (Kirillov et al. §3: per-pixel $(l_i,z_i)$, stuff ids irrelevant, no overlap by construction, strict generalization of the semantic format). "Overlay policy" for overlap policy; "Assimilate" | Comparison: choose the output a deliverable needs | 3 expected criteria; 357 → 356 lexical words | Wording aligned with the reference appendices | Minor | Language fixes; Source line given Kirillov §3 and Mask2Former §3.1 |
| CV-SEGMENTATION-002 | A semantic loss cannot choose between instance partitions with the same union: confirmed as a deduction from the per-pixel loss; U-Net's separation borders confirm the remedy (§1, §3). "Instance header" for instance head, "border index" for boundary cue, "task interface defect", "Deduct" | Diagnosis: a task-definition failure mistaken for a capacity failure | 2 expected criteria; 270 → 279 lexical words | Wording aligned with the reference appendix | Minor | Language fixes; Source line given U-Net §1 and §3 |
| CV-SEGMENTATION-003 | Discrete labels must not be interpolated as intensities; logits interpolation then argmax does not commute with argmax then interpolation: confirmed as deductions. Expected answer said "discreet labels"; "dense increase" and "an increase" for augmentation, "does not switch" for does not commute, "witness" for test case, "**check**" | Practice: label-preserving augmentation and tiling | 2 expected criteria; 371 → 382 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given Kirillov §3 and torchvision code |
| CV-SEGMENTATION-004 | Mean Dice depends on aggregation, empty-mask conventions and size: confirmed by construction (worked example B) and by Cordts et al. §3.1 (dataset-level IoU biased toward large instances). Expected answer said "borders"; French decimal comma "0,5 mm"; "a overlap", "announce cases" | Evaluation: limits of an overlap score for a medical deliverable | 3 expected criteria; 374 → 371 lexical words | Wording aligned with the reference appendices | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line given Cordts et al. §3.1 |

Expected-answer changes (meaning-restoring language fixes):

- CV-SEGMENTATION-003: "... the interpolation of the mask must preserve the discreet
  labels according to the contract." → "... the interpolation of the mask must preserve
  the discrete labels according to the contract."
- CV-SEGMENTATION-004: "... external validation, borders, rare cases, physical units and
  intended use provide further evidence." → "... external validation, boundaries, rare
  cases, physical units and intended use provide further evidence."

Defective objectives (header invariants, not edited), with proposed wording:
CV-SEGMENTATION-002 "Detecting a bad job definition" → "Detect a badly defined task";
CV-SEGMENTATION-003 "Propagating a dense increase" → "Propagate a geometric augmentation
to dense labels".

## Reference findings

Claims of revision 7 checked against their passages:

- PQ "combines instance overlap and recognition in a matching protocol": confirmed and
  made explicit (Kirillov §4.1–§4.2: IoU > 0.5 matching, PQ = SQ × RQ).
- Class IoU TP/(TP+FP+FN) and Dice 2TP/(2TP+FP+FN): confirmed (Long et al. §5; identity
  with IoU derived and recomputed).
- "DeepLab exploits dilated convolutions and context", "Mask R-CNN combines detection
  and mask by instance", "U-Net exploits encoder–decoder and resolution links",
  "nnU-Net automates pipeline choices": confirmed (Chen et al. §3.1; He et al. §3;
  Ronneberger et al. §2; Isensee et al. abstract).
- No scientific error was found. The body held one to three sentences per section, with
  mistranslations: "accounting object masks" (countable), "panoptical", "vacuum
  convention" (empty-mask convention), "consistent image–mask increases"
  (augmentations), "No workouts performed" (no training run), "Question of work",
  "Reference Response", "witness", "does not switch".

New claims verified for revision 8 (main ones):

- Kirillov et al.: §2 amodal exclusion, §3 format and relations, §4.1 Theorem 1 and
  proof, §4.2 PQ, SQ, RQ, class averaging, equal weight of segments, void and group
  labels, §7 NMS-like overlap resolution, things over stuff, G-RMI small-patch example.
- Long et al.: stride 32, FCN-16s +3.0 mean IU to 62.4, FCN-8s 62.7 (Table 2), four
  metrics (§5).
- Ronneberger et al.: unpadded convolutions and 572→388 tiles, overlap-tile with
  mirroring, even sizes for pooling, weight map eq. 2 with $w_0=10$ and $\sigma\approx5$ px.
- Chen et al. (DeepLabv3+): eq. 1, output stride 32/16/8, decoder ×4 then ×4, 89.0% and
  82.1% test results, trimap gains largest for narrow bands (§4.4), Table 5 costs.
- He et al. (Mask R-CNN): $Km^2$ output, per-class sigmoid, loss on the class's mask only,
  RoIAlign without quantization, relative 10–50% mask gain, about 200 ms per frame,
  28×28 masks, resize and 0.5 threshold.
- Cheng et al. 2022 (Mask2Former): $N$ masks and labels, masked attention eq. 2,
  post-processing, $\mathrm{mIoU_{pan}}$, Table 1 FLOPs and fps with measurement
  conditions, abstract results.
- Cheng et al. 2021 (Boundary IoU): eq. 1, quadratic interior against linear boundary
  growth, $d$ = 2% of the diagonal (COCO, ADE20k) and 0.5% (Cityscapes), expert agreement.
- Cordts et al.: void excluded from training and evaluation (§2.2); IoU accumulated over
  the whole test set and biased toward large instances; iIoU weighting (§3.1).
- torchvision v0.24.0 `MaskRCNN` input/output contract and resize defaults; segmentation
  heads' bilinear upsampling with `align_corners=False`.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 316 → 3,595. About 2,780
of these are prose; the rest are tables, pseudocode and the Mermaid diagram. As a
comparison and protocol note it exceeds 3,000 tokens because it covers three output
contracts and five metrics.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Panoptic format from the paper; output table (representation, overlap, confidence, metric); void, crowd, amodal and frame conventions; deliverable-to-output mapping |
| Intuition | Shallow | Developed | Plain contrast of the three outputs; constructed pallet illustration; Mermaid diagram of conversions between outputs |
| Prerequisites | Shallow (conventions only) | Developed | Links to CV-IOU-AP, CV-DETECTEURS, CV-NMS, CV-REPRESENTATIONS, CV-FIABILITE, CV-METRIQUES-APPLIQUEES, CV-WATERSHED, CV-GRABCUT, CV-SAM |
| Assumptions | Shallow | Developed | Taxonomy, visible separation (U-Net separation borders), resolution, annotation ambiguity; observability of occlusion and identity; empty classes, overlapping predictions, group regions |
| Procedure | Shallow | Developed | How FCN, DeepLabv3+, U-Net, Mask R-CNN and Mask2Former produce their outputs; pseudocode of the NMS-like instance-to-panoptic conversion with purposes |
| Mathematics | Shallow | Developed | Confusion-matrix metrics, dataset-level versus per-image aggregation, iIoU, Dice–IoU identity, PQ with Theorem 1, Boundary IoU, atrous convolution and output stride; worked examples A (PQ), B (aggregation, Dice) and C (Mask IoU against Boundary IoU) |
| Parameters | Shallow (list) | Developed | Eight-row table with source values; tuning approach anchored on the evaluation protocol |
| Properties | Shallow | Developed | Format relations, unique matching, what each metric rewards (G-RMI example), equivariance, effect of resampling conventions (RoIAlign) |
| Cost and implementation | Shallow | Developed | Logit memory, output-stride cost, instance-head output and speed, Mask2Former FLOPs and fps with conditions, U-Net tiling; torchvision 0.24.0 contracts; execution status |
| Evaluation | Shallow | Developed | Protocol table by deliverable; published results with their protocols; baseline and output-stride variation with a confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices among outputs, universal models, nnU-Net, classical and promptable alternatives; industrial uses labelled as project reasoning; scientific and implementation sources |

Constructed examples are recomputed by
[`checks/93-semantique-instances-panoptique.py`](checks/93-semantique-instances-panoptique.py)
(14 assertions): PQ example (SQ 0.75, RQ 0.571, PQ 0.429, RQ = F1, class mean 0.689) and
the Theorem 1 inequality on samples; aggregation (0.891 against 0.45) and Dice–IoU
identity; Mask IoU 0.9025 and 0.9801 against Boundary IoU $(d-\delta)/(d+\delta)=0.875$;
$d$ for a 640×480 image; logit memory 159.4 MB; OS 8 cost ratio 3.54 for +0.47 mIoU;
stride and mask-cell sizes.

## Applied corrections

- [Reference](../../../vault/90-segmentation/references/93-semantique-instances-panoptique.md),
  revision 7 → 8: body rewritten and deepened as above; mistranslations fixed in the
  appendices ("Question of work" → "Working question", "Reference Response" →
  "Reference answer", "overlay policy" → "overlap policy", "Test of information" →
  "Information test", "border index" → "boundary cue", "instance header" → "instance
  head", "Transforming the adapted representation" → "Transforming the appropriate
  representation", "an increase" → "an augmentation", "does not switch" → "does not
  commute", "witness" → "test case", "0,5 mm" → "0.5 mm", "a overlap" → "an overlap");
  trailing section renamed "Sources" and split into scientific and implementation
  sources; closing provenance line replaced. Front matter unchanged except `revision`;
  H1 and per-card headings unchanged.
- [Cards](../../../vault/90-segmentation/93-semantique-instances-panoptique.md): expected
  answers of CV-SEGMENTATION-003 and 004 corrected as quoted above. Further explanations
  and blocking errors received the same language fixes as the appendices, plus
  "mergers/separations" → "merges and splits", "single components" → "connected
  components", "does not automatically set the count" → "does not automatically fix the
  count", "**Two Types of Values**" → "**Two types of values**", "**check**" →
  "**Discriminating check**", "For the tile, check also returns the crop" → "For tiling,
  also check how each crop is placed back", "smooth class IDs as intensities" →
  "interpolating class IDs as intensities". Source lines now cite exact sections and
  replace the garbled Mask2Former label. Questions, IDs, objectives, families, tags and
  target deck unchanged.

No other vault file contradicts a claim of this note (`rg` over `vault/` for panoptic,
PQ, Dice, mIoU, Mask R-CNN and Boundary IoU; CV-METRIQUES-APPLIQUEES states the same
Dice–IoU identity).

## Proposals

P-CV-SEGMENTATION-01 (worked PQ card) remains pending and is not duplicated. To register
as `pending` in the [proposal register](../propositions.md) (not edited by this subject
run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-SEGMENTATION-02 | CV-SEGMENTATION | Explain why the same predictions give a high dataset-level IoU and a low per-image mean, and which aggregation a small-structure requirement needs | Aggregation level is the most frequent cause of incomparable segmentation scores; card 004 mentions it only qualitatively | Evaluation; worked example B | 1 card, 3 criteria | [Cordts et al. 2016, §3.1](https://arxiv.org/abs/1604.01685); [Long et al. 2015, §5](https://arxiv.org/abs/1411.4038) |
| P-CV-SEGMENTATION-03 | CV-SEGMENTATION | Convert overlapping instance predictions into a panoptic output (score sort, surviving fraction, things over stuff) and state what the conversion can discard | No card trains the instance-to-panoptic contract, a frequent integration step | Algorithm; Procedure | 1 card, 3 criteria | [Kirillov et al. 2019, §7](https://arxiv.org/abs/1801.00868) |

## Sources

Scientific sources, opened at the passages listed (PDF text extracted with `pdftotext`,
arXiv PDFs):

- Kirillov et al., [arXiv 1801.00868](https://arxiv.org/abs/1801.00868): §2, §3, §4.1–§4.3, §5, §7.
- Long, Shelhamer and Darrell, [arXiv 1411.4038](https://arxiv.org/abs/1411.4038): abstract, §3.3, §4.1–§4.3, §5 "Metrics", Table 2.
- Ronneberger, Fischer and Brox, [arXiv 1505.04597](https://arxiv.org/abs/1505.04597): §1, §2, §3, Figs. 1–3.
- Chen et al. (DeepLabv3+), [arXiv 1802.02611](https://arxiv.org/abs/1802.02611): abstract, §3.1, §4.4, Table 5.
- He et al. (Mask R-CNN), [arXiv 1703.06870](https://arxiv.org/abs/1703.06870): §1, §3, Fig. 4, "Inference".
- Cheng et al. (Mask2Former), [arXiv 2112.01527](https://arxiv.org/abs/2112.01527): abstract, §3.1–§3.2, §4 opening, §4.1, Table 1.
- Cheng et al. (Boundary IoU), [arXiv 2103.16562](https://arxiv.org/abs/2103.16562): §1, §4.1, §5, §6 settings.
- Cordts et al. (Cityscapes), [arXiv 1604.01685](https://arxiv.org/abs/1604.01685): §2.2, §3.1.
- Isensee et al. (nnU-Net), [arXiv 1904.08128 abstract page](https://arxiv.org/abs/1904.08128).

Implementation sources:

- [torchvision v0.24.0 `mask_rcnn.py`](https://github.com/pytorch/vision/blob/v0.24.0/torchvision/models/detection/mask_rcnn.py): L1–L240.
- [torchvision v0.24.0 `segmentation/_utils.py`](https://github.com/pytorch/vision/blob/v0.24.0/torchvision/models/segmentation/_utils.py): complete.

Failed accesses and limits:

- nature.com (nnU-Net and Reinke et al.) redirected to an authentication page; nnU-Net
  was read through its arXiv abstract. Reinke et al. was not re-read: its citations in
  cards 002 and 004 rely on the earlier passes (2026-10-20 report) and no new claim of
  this pass rests on it.
- The Cityscapes image resolution was not confirmed in the passages read; the logit
  memory example is stated for a 2048×1024 image without attributing that size to the
  dataset.
- Context7 was not available in this session; torchvision was read at a release tag.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | No error in this subject's files; ECHEC caused by another agent's in-progress file (`130-evaluation-fiabilite/references/133-donnees-generalisation.md`) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/93-semantique-instances-panoptique.py` | 14 checks passed |
| `git diff --check -- vault/90-segmentation/93-semantique-instances-panoptique.md vault/90-segmentation/references/93-semantique-instances-panoptique.md` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/90-segmentation/93-semantique-instances-panoptique.md` | 4 cards, 279 to 382 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card header, block, ID, question, tags and deck lines identical; front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced; card paragraphs repeated in the appendices identical |

No model was trained or run; the baseline and variation are protocols, not results.
The Mermaid diagram and tables were not rendered in Obsidian, and AnkiDroid rendering is
unverified. This is agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-SEGMENTATION
revision 8, CV-SEGMENTATION-001 to 004, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-SEGMENTATION-02, P-CV-SEGMENTATION-03).
