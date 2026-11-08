---
id: CV-REPRESENTATIONS
type: comparaison
domaine: d07
poles: [A, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 7
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Visual representations, ViT, Swin, ConvNeXt and DINOv2

## Problem, data and assumptions

Choose a representation for classification, retrieval or dense task. Inputs: pre-processed images and possible supervision; outputs: features, not necessarily classes adapted to the product. The reference note compares families; it does not deepen each cited architecture.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

HOG encodes gradients; CNN/ResNet/ConvNeXt exploits a convolutional structure. ViT deals with patch tokens; Swin organizes local attention and hierarchy. DINOv2 learns features that can be transferred by self-supervision; a suitable head and protocol remain necessary.

## Mathematics, conventions and units

For multiple H,W side of patch P, a ViT has $N=HW/P^2$ image tokens. The dense global attention has a quadratic term in N; at fixed P, doubling the two dimensions multiplies N by four and this term by sixteen. A cosine similarity compares normalized vectors; this is not automatically a probability.

## Parameters and properties

Resolution, preprocessing, global tokens/denses, selected layer, normalization and adaptation strategy. Linear probing, complete fine-tuning and LoRA/adapters change the learned parameters and data needs. MAE is pretrained by masked reconstruction, not by a final segmentation head.

## Cost and implementation

Compare memory, pre/postprocessing, and head cost; a frozen backbone can remain expensive in inference. No drive/checkpoint executed or CNN/transformer universal rating announced.

## Evaluation and controlled variation

Baseline: features frozen and small head, then controlled adaptation. Use the same splits, labels and budget; measure by class, size and domain. Vary resolution separately from the training recipe.

## Failure modes and diagnosis

Good results on random validation but bad new site: inspect scene leak, pre-processing and domain. DINOv2 and DINO detector are not the same method.

## Alternatives and applications

Choose robustness and cost useful to the product, not just popularity of the backbone. Self-supervised features can be reused by segmentation or anomalies.

## Guided reasoning and proposed checks

These constructed cases develop architecture bias, scale and transfer protocol. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-REPRESENTATIONS-001

**Question of work**: In a ViT with fixed patch size and dense global attention, how does doubling image width and height change the number of image tokens, excluding the class token, and the associated quadratic term?

**Reference Response**: Tokens ×4; quadratic term ×16, in this cost model.

**derivation of cost**: with fixed $P$ side patches and compatible dimensions, $N=HW/P^2$. Double $H$ and $W$ multiplies the number of patches by four. A global matrix of interactions between tokens then has sixteen times as many pairs. This count concerns the term of attention considered, not all operations of the network.

**Proposed practical consequence**: Before increasing resolution for small faults, estimate activation memory and test full latency. Projections, convolutions, kernels and bandwidth constraints do not necessarily follow this same factor. A batch reduction or other representation can change the compromise. Also check if the information of the defect exists in the initial acquisition: enlarging an image without additional detail does not bring the same observations as a capture actually better resolved. Measures on the target material therefore complement the cost model.

### Case linked to CV-REPRESENTATIONS-005

**Question of work**: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?

**Reference Response**: Color order, normalization, range, interpolation, crop and resolution actually received.

**Interface Trap**: Two chargers can produce visually similar images while differing in channel order or pixel center processing. Repeated or omitted normalization can also strongly alter the received tensor. The backbone sees only these values, not the pipeline intent.

**Proposed Reproducible Investigation**: use an identical cookie file, save known shapes, types, ranges and pixels after each step, and then compare the input tensors. Repeat the extraction with the same weights and parameters. If the features change before any scene variation, first look for this deterministic difference. Once the contract is restored, evaluate the new domain on a reserved set. A fine-tuning launched too early can partially absorb a pre-processing bug, make regression less visible and complicate reproducibility without having addressed its cause.

**Documentary reference for this pass**: [ViT](https://arxiv.org/html/2010.11929v2), §3, representation by patches. The other developments are in the [flashcards](../71-representations-transfert.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-REPRESENTATIONS-001

**Situation**: In a ViT with fixed patch size and dense global attention, how does doubling image width and height change the number of image tokens, excluding the class token, and the associated quadratic term?

**Example of dimensions**: a $224\times224$ image with $16\times16$ patches gives 196 image tokens; at $448\times448$, it gives 784. One attention per head typically calculates $QK^T$ of size $N\times N$, then a combination of values. The interaction term is of order $N^2d$, while the projections and the MLP introduce order terms $Nd^2$ for a width $d$. Depending on the plan, these contributions and memory access do not dominate in the same way. Memory-saving implementations can avoid storing the entire matrix without necessarily removing quadratic counting from calculated interactions.

### CV-REPRESENTATIONS-002

**Situation**: Do Swin and ConvNeXt replace CNNs with the same global attention mechanism?

**Counting by windows**: If a window contains $M^2$ tokens and the image contains $N$ tokens, the internal interactions total about $(N/M^2)(M^2)^2=NM^2$, instead of $N^2$ for global attention, fixed width. This simplification assumes a fixed window size and ignores projections, MLP, padding, and hierarchical merge. The staggered windows allow successive blocks to communicate previously separated regions. The information field is therefore built over layers; a local layer does not instantly access the entire image. Comparing this organization to convolutions requires also examining resolution, number of channels and dense task head.

### CV-REPRESENTATIONS-003

**Situation**: What is missing between DINOv2 features and an industrial defect detector ready for evaluation?

**From the token to the default zone**: Selecting local features retains a grid of patches, while a global vector aggregates the image. Interpolation of the grid to the original resolution increases the number of pixels of the score, without creating in itself a location accuracy absent from the features. Define how a patch covers the part and what defect size it should distinguish. A constructed baseline can freeze the extractor, index the nominal patches and use their distance as a score, before comparing to a supervised head. Keeping part masks, alignment, and aggregation policy allows errors to be attributed to the representation choice rather than to an implicit interface.

### CV-REPRESENTATIONS-004

**Situation**: Which tradeoffs distinguish linear probing, full fine-tuning and LoRA/adapters for visual transfer learning?

**Parametrisation LoRA**: For a layer $W\in\mathbb R^{d\times k}$, replace the complete update with $\Delta W=BA$, with $B\in\mathbb R^{d\times r}$ and $A\in\mathbb R^{r\times k}$, causes $r(d+k)$ parameters instead of $dk$, out of bias and other modules. Rank $r$ constrains the space of updates and is a compromise to validate. When the adaptation is linear and compatible with weight representation, one can form $W'=W+BA$ for inference; this differs from a non-linear adaptation kept in the computation path. The small number of parameters learned does not therefore, by itself, describe the graph actually deployed.

### CV-REPRESENTATIONS-005

**Situation**: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?

**Pretreatment Invariant**: If the model waits for $z_c=(x_c/255-\mu_c)/\sigma_c$, giving it $x_c\in[0,255]$ directly before subtraction changes the scale by a factor close to 255, without being a variation of physical domain. Testing an artificial image with each channel is constant and different makes it possible to detect permutation RGB/BGR and repeated normalization. For a dense task, also check the transformation of labels and coordinates by crop, resize and padding. An identical input image is only a sufficient witness if all stochastic steps are neutralized and if weight, mode of evaluation and numerical precision are also fixed.

**Passages consulted for these developments** : [ViT](https://arxiv.org/html/2010.11929v2), §3.1, patch sequence; project counts and tests; [Liu et al., Swin](https://arxiv.org/html/2103.14030v2), §3.2, equations 1–2, windows and offset; counting explained by the project; [Oquab et al., DINOv2](https://arxiv.org/html/2304.07193v2), §7.4, patch tokens, flashcard low resolution and interpolation; proposed inspection baseline; [Hu et al., LoRA](https://arxiv.org/html/2106.09685v2), §4.1, parameterization W+BA and linear fusion.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-REPRESENTATIONS-001 — Quadratic attention is only one runtime term

For token count $N$ and embedding width $d$, dense attention includes an $N^2d$ interaction term while projections and feed-forward blocks have terms proportional to $Nd^2$. Quadrupling tokens multiplies those terms by sixteen and four, respectively, before implementation effects. This explains why the front's sixteenfold statement applies to the quadratic term rather than guaranteeing sixteenfold wall time or memory. Measure the actual inference path at the intended batch size.

### CV-REPRESENTATIONS-002 — Local windows exchange information across layers

Nonoverlapping attention windows alone would isolate neighboring regions at each layer. Shifting their partition allows later blocks to connect tokens previously separated by a boundary, while the hierarchy changes spatial resolution. This is a mechanism for extending context without one global attention matrix at every block. ConvNeXt instead uses convolutional operations; comparing the two requires matching the downstream output scale, feature budget and deployment measurements.

### CV-REPRESENTATIONS-003 — Upsampling cannot recreate missing defect evidence

If a thin scratch is smaller than the feature grid support and has been suppressed by acquisition or feature extraction, interpolating its anomaly map to full image size does not restore the original detail. Evaluate critical defect sizes in original pixels and physical units. A proposed baseline compares multiple input resolutions or local crops under the same decision protocol, including processing cost and false alarms from texture.

### CV-REPRESENTATIONS-004 — Trainable-parameter count is not total training memory

Freezing most weights can reduce optimizer state and gradient storage, but backpropagation through selected layers can still require substantial intermediate activations. A linear probe on cached frozen features has a different cost profile from adapters or LoRA trained through a live backbone. Compare peak memory, training time and validation quality for the actual configuration. A smaller trainable update constrains adaptation; it does not guarantee robustness on a small dataset.

### CV-REPRESENTATIONS-005 — Compare tensors before comparing predictions

A proposed loader regression check uses the same encoded image and records decoded channels, resize/crop coordinates and the normalized tensor from both paths. Compare elementwise differences at each stage before running the backbone. This locates an interface discrepancy even when final predictions differ unpredictably. Include color-chart and high-frequency patterns because ordinary photos may hide channel permutations or interpolation changes. Do not infer preprocessing equivalence from matching tensor dimensions.

Consulted foundations: [ViT](https://arxiv.org/html/2010.11929v2): §3.1 image patches and token sequence; [Swin](https://arxiv.org/html/2103.14030v2): §3.2 local windows and shifted connections; [DINOv2](https://arxiv.org/html/2304.07193v2): §7 downstream dense evaluation and representation use.

## Sources and flashcards

- [Hu et al., LoRA, summary and principle of frozen parameters](https://arxiv.org/abs/2106.09685)
- [Houlsby et al., adaptors, summary](https://arxiv.org/abs/1902.00751)
- [He et al., MAE, summary](https://arxiv.org/abs/2111.06377)
- [Dalal – Triggs, HOG, summary](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)

- [ViT, §§3 – 4](https://arxiv.org/abs/2010.11929).
- [Swin, §3](https://arxiv.org/abs/2103.14030).
- [ConvNeXt, §2](https://arxiv.org/abs/2201.03545).
- [DINOv2, method and transfer](https://arxiv.org/abs/2304.07193).
- [Related flashcards](../71-representations-transfert.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
