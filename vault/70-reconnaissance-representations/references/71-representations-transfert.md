---
id: CV-REPRESENTATIONS
type: comparaison
domaine: d07
poles: [A, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 8
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Visual representations, ViT, Swin, ConvNeXt and DINOv2

This comparison note helps choose and adapt a visual representation: a hand-designed
descriptor (HOG), a convolutional network (ResNet, ConvNeXt), a plain or hierarchical
vision transformer (ViT, Swin), or self-supervised features (MAE, DINOv2), together
with the adaptation protocol (linear probe, fine-tuning, adapters, LoRA). It focuses
on what matters when the representation feeds an inspection, retrieval or dense
task: token geometry against defect size, preprocessing contracts, global versus
dense outputs, transfer protocols and cost. Text-aligned embeddings live in
[CV-CLIP](72-clip-siglip.md) and feature-based anomaly detection in
[CV-ANOMALIES](73-patchcore-padim.md).

## Problem and data contract

**Task.** Map an image to features that a head or a decision rule can use:
classification, retrieval, detection, segmentation or anomaly scoring. The choice
covers the backbone, its pretraining, the layer and token type used, and how much of
it is adapted to the target data.

**Input contract.** A tensor $B\times3\times H\times W$ of float values produced by a
fixed chain: decode (channel order RGB or BGR), resize with a stated interpolation,
crop or pad, scale to $[0,1]$, then normalize per channel,
$z_c=(x_c/255-\mu_c)/\sigma_c$. torchvision 0.20's `ImageClassification` preset
resizes to 256 (bilinear, antialiased), center-crops, converts to float and
normalizes with $\mu=(0.485,0.456,0.406)$, $\sigma=(0.229,0.224,0.225)$
[_presets.py, L38–L64]; DINOv2's evaluation transform uses the same statistics but
bicubic resizing [dinov2 transforms.py, L42–L43, L76–L91]. A pretrained model sees
only the resulting numbers: a different interpolation, a channel swap or a missing
division by 255 is a domain shift created by the loader.

**Output contract.** Either a global vector (class token or pooled features) of
dimension $D$, or a dense grid of patch tokens of shape
$(H/P)\times(W/P)\times D$, or multi-scale feature maps (Swin, ConvNeXt) at strides 4,
8, 16 and 32. DINOv2's `forward_features` returns separate class, register and patch
tokens, and `get_intermediate_layers(..., reshape=True)` returns patch features shaped
$B\times D\times H/P\times W/P$ [dinov2 vision_transformer.py, L257–L272, L301–L330].
Coordinates of a patch map back to the image through the resize and crop, which must
be recorded to localize anything.

**Role in a pipeline.** The representation sits between acquisition
([CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md))
and a task head; downstream needs either separable global features (retrieval,
classification) or spatially faithful dense features (segmentation, anomaly maps).
Product classes, thresholds and calibrated scores are not part of the representation.

## Intuition

Every family turns pixels into features by imposing a structure. HOG histograms
gradient orientations in $8\times8$-pixel cells and normalizes them over
$16\times16$-pixel blocks, a fixed, hand-designed invariance to small shifts and
illumination [Dalal and Triggs, §6]. A CNN learns local filters with translation
equivariance and locality "baked into each layer" [Dosovitskiy et al., §3.1,
Inductive bias]. A ViT cuts the image into $P\times P$ patches and lets every token
attend to every other token, learning spatial relations from data
[Dosovitskiy et al., §3.1]. Swin restricts attention to $M\times M$ windows that shift
between consecutive blocks and merges patches to build a hierarchy
[Liu et al., §3.1–§3.2]. ConvNeXt shows that a ConvNet modernized step by step toward
Swin's design choices, "without introducing any attention-based modules", reaches
similar accuracy [Liu et al. 2022, §2, Fig. 2]. Self-supervised pretraining (MAE,
DINOv2) learns features without labels; DINOv2 aims at features usable "as they are,
i.e., without fine-tuning" [Oquab et al., §1].

*Illustration (constructed).* A 20-pixel scratch on a 2048-pixel part image,
resized to 224 pixels for a /14 backbone, covers about a sixth of one patch side
(worked example A). The global class token of a backbone trained on natural images
may not change at all; the patch token over the scratch may change slightly; a
native-resolution crop puts the scratch across more than one patch. The architecture
matters less here than the sampling geometry chosen before the backbone.

## Prerequisites and competencies

**Required prerequisites**: [vault conventions](../../01-Parcours/Pre-requis.md).
Useful background, by mechanism:

- gradients and pyramids behind HOG and CNN stems: [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md);
- local descriptors as the classical counterpart of dense features: [CV-SIFT](../../40-features-matching/references/41-sift.md);
- sampling, resolution and noise of the input: [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md);
- consumers of these features: [CV-ANOMALIES](73-patchcore-padim.md), [CV-CLIP](72-clip-siglip.md), [CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md), [CV-DETECTEURS](../../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md);
- data splits, leakage and drift: [CV-FIABILITE](../../130-evaluation-fiabilite/references/133-donnees-generalisation.md);
- deployment cost and quantization: [CV-QUANT](../../140-ingenierie-systemes/references/142-quantification-runtimes.md).

**Target competencies**: explain how each family structures an image, compute token
and attention costs and defect footprints, compare adaptation protocols under data
and deployment constraints, evaluate transfer without leakage, and diagnose loader,
resolution and domain failures.

## Assumptions, observability and degenerate cases

- **Pretraining domain.** Features are learned on a distribution (ImageNet,
  LVD-142M, web images); DINOv2 curated LVD-142M by retrieving images close to curated
  datasets [Oquab et al., §3]. Grayscale industrial images, X-ray, thermal or
  microscopy differ in statistics and in what counts as a "feature".
- **Patch and stride geometry.** Information smaller than a patch or a stride may
  survive only as a weak change of a token; DINOv2's linear segmentation produces a
  low-resolution logit map that is upsampled, which "cannot easily produce
  high-resolution segmentations" [§7.4]. Upsampling recovers no lost detail.
- **Resolution changes.** A ViT accepts other resolutions only by interpolating its
  position embeddings, which may no longer be meaningful [Dosovitskiy et al., §3.2];
  torchvision 0.20's ViT asserts the exact training size [vision_transformer.py,
  L266–L273] and provides `interpolate_embeddings` for checkpoints [L789–L801]. DINOv2
  interpolates position encodings at run time but requires sides divisible by the
  patch size [vision_transformer.py, L182–L205; patch_embed.py, L72–L73].
- **Linear separability.** A linear probe measures how linearly separable frozen
  features are; MAE's authors find linear-probing and fine-tuning results "largely
  uncorrelated" [He et al., §4.3]. Weak linear-probe accuracy does not mean weak
  features for a nonlinear head.
- **Distribution shift during adaptation.** When pretrained features are good and the
  shift is large, full fine-tuning can distort them: on ten shift benchmarks, Kumar et
  al. measured fine-tuning 2% better in distribution but 7% worse out of distribution
  than linear probing on average [Kumar et al., abstract, §4.1].
- **Degenerate cases.** Constant or near-constant inputs, heavy padding and crops
  that remove the object produce features dominated by position embeddings or
  normalization statistics, not by content (project deduction).

## Procedure

```text
1. Fix the input contract: decode order, resize (size, interpolation, antialias),
   crop or tile, scaling, normalization; log a tensor fingerprint per stage.
2. Choose the output: global token, pooled map, patch tokens, or multi-scale maps;
   map patch coordinates back to original pixels.
3. Baseline: freeze the backbone, cache features, train a linear head or a k-NN
   (or a distance-to-nominal score for anomalies).
4. Controlled adaptation, one change at a time:
   a. partial fine-tuning of the last blocks, or adapters / LoRA;
   b. LP-FT: linear probe first, then full fine-tuning from that head;
   c. full fine-tuning with the same splits and budget.
5. Resolution study: same model, several input sizes or native-resolution tiles.
6. Evaluate per class, per defect size, per site or domain, with held-out groups.
7. Deploy: measure end-to-end latency and memory, merge LoRA if linear.
```

Purpose of the steps. *Fixing the input contract* removes the most common cause of
silent degradation (CV-REPRESENTATIONS-005). *Choosing the output* decides whether
localization is possible at all. *The frozen baseline* measures what the pretrained
representation already gives, at the lowest risk of leakage and overfitting.
*Partial fine-tuning* is a middle ground: in MAE, tuning one Transformer block raised
ImageNet accuracy from 73.5% to 81.0% for ViT-L, and a few blocks approached full
fine-tuning [He et al., §4.3]. *LP-FT* addresses feature distortion: it was 1% better
in distribution and 10% better out of distribution than full fine-tuning in Kumar et
al. [abstract, §4.2]. *The resolution study* separates the effect of sampling from
that of the training recipe.

| Family | Structure imposed | Output | Scaling with image size | Typical use |
| --- | --- | --- | --- | --- |
| HOG | Fixed gradient histograms, 9 orientation bins, $8\times8$ cells, $16\times16$ blocks | Fixed-length descriptor per window | Linear | Classical detection, small data, explainability |
| CNN / ConvNeXt | Learned local filters, hierarchy, strides 4–32 | Multi-scale maps | Linear | Dense tasks, edge deployment |
| ViT | Patches, global attention, learned positions | Class token and $N=HW/P^2$ patch tokens | Attention term $\propto N^2$ | Global features, large pretraining |
| Swin | Local $M\times M$ windows, shifted, patch merging | Multi-scale maps | Linear for fixed $M$ | Dense tasks with transformer blocks |
| MAE (pretraining) | Masked-patch reconstruction | ViT features, best after fine-tuning | As ViT | Pretraining for fine-tuning |
| DINOv2 | Self-distillation, curated data, distilled smaller models | Class, register and patch tokens | As ViT | Frozen features, retrieval, dense probes |

## Mathematics, conventions and units

**Tokens.** For an image of $H\times W$ pixels and $P\times P$ patches,
$N=HW/P^2$ image tokens form the sequence, plus one class token
[Dosovitskiy et al., §3.1]. Self-attention on $N$ tokens of width $d$ has an
interaction term of order $N^2d$ and projection and MLP terms of order $Nd^2$; only the
former grows with the square of the token count.

**Window attention.** For $h\times w$ patches of $C$ channels and $M\times M$ windows,
Swin gives $\Omega(\mathrm{MSA})=4hwC^2+2(hw)^2C$ and
$\Omega(\mathrm{W\text{-}MSA})=4hwC^2+2M^2hwC$, linear in $hw$ for fixed $M$ ($M=7$ by
default), with softmax omitted [Liu et al., §3.2, eqs. 1–2]. Swin starts from
$4\times4$ patches ($H/4\times W/4$ tokens) and merges $2\times2$ neighbors at each stage
[§3.1]. Shifting the partition creates connections between neighboring windows of the
previous layer [§3.2].

*Worked example A (constructed, recomputed by checks/71-representations-transfert.py).*
ViT-B/16 has 196 tokens at 224 pixels and 784 at 448: four times more tokens and 16
times the attention term. A /14 model has 256 tokens at 224 pixels and 1,369 at the
518-pixel default of the DINOv2 hub models [dinov2 backbones.py, L33–L34]. When a
2048-pixel part image is resized to 224 pixels, one 14-pixel patch covers 128 original
pixels, and a 20-pixel scratch spans 0.16 of a patch side, about 2.4% of its area.
Tiling the image into 224-pixel crops at native resolution puts the scratch across
1.4 patches, at the cost of 100 crops.

*Worked example B (constructed, recomputed by checks/71-representations-transfert.py).*
At Swin's first stage, a 224-pixel input gives $56\times56$ tokens: the global
attention term is $hw/M^2=64$ times the windowed one, and 256 times at 448 pixels. With
$C=96$, total multiply-adds of global MSA are 13.8 times those of W-MSA, because the
$4hwC^2$ projections are shared.

**MAE.** A large random subset of patches, for example 75%, is masked; the encoder
processes only the visible patches and a lightweight decoder reconstructs the pixels
[He et al., §1, Fig. 1]. With 196 patches, the encoder sees 49 tokens: a quarter of the
per-token cost and a sixteenth of the attention term (recomputed by
checks/71-representations-transfert.py).

**Adaptation.** LoRA replaces the update of a frozen $W_0\in\mathbb R^{d\times k}$ by
$\Delta W=BA$ with $B\in\mathbb R^{d\times r}$, $A\in\mathbb R^{r\times k}$, $A$
Gaussian-initialized and $B$ zero so that training starts from the pretrained model,
and scales $\Delta Wx$ by $\alpha/r$; at deployment $W=W_0+BA$ can be merged, adding no
inference latency, unlike adapter layers [Hu et al., §4.1]. A rank-8 update of a
$768\times768$ projection trains 12,288 parameters instead of 589,824 (2.08%,
recomputed by checks/71-representations-transfert.py). Houlsby adapters insert small
bottleneck modules with a skip connection and near-identity initialization
[Houlsby et al., §2.1].

**Normalization.** With $z_c=(x_c/255-\mu_c)/\sigma_c$, feeding a float tensor in
$[0,255]$ without the division multiplies the slope $\partial z/\partial x$ by 255: a
mid-grey red value becomes about 557 instead of 0.07. torchvision 0.20's
`convert_image_dtype` returns a float tensor unchanged, so a float image in $[0,255]$
passes through `ImageClassification` unscaled; only integer inputs are rescaled
[_functional_tensor.py, L66–L74] (project deduction from the code, recomputed by
checks/71-representations-transfert.py). A constant red test image normalizes to
$(+2.25,-2.04,-1.80)$ in RGB order but $(-2.12,-2.04,+2.64)$ after a channel swap.

**HOG.** Gradient voting into 9 orientation bins over 0–180°, four $8\times8$ cells per
$16\times16$ block, block stride 8, L2-Hys normalization and a $64\times128$ window
[Dalal and Triggs, §6] give $7\times15$ blocks and a 3,780-dimensional descriptor
(recomputed by checks/71-representations-transfert.py).

**Similarity.** Retrieval compares normalized vectors with the cosine
$\cos(u,v)=u^\top v/(\lVert u\rVert\lVert v\rVert)\in[-1,1]$; its value depends on the
model and layer and is not a probability.

## Parameters and tuning

| Parameter | Values in the sources | Effect | Interactions and what to watch |
| --- | --- | --- | --- |
| Input resolution | ViT and DINOv2 evaluated at 224; DINOv2 trained at 518 for a short final phase [Oquab et al., §4]; ViT fine-tuned at higher resolution with interpolated positions [Dosovitskiy et al., §3.2] | Detail per token versus cost | Attention term $\propto N^2$; position interpolation is a shift for the model |
| Patch size $P$ | 16 (ViT-B/16), 14 (DINOv2), 4 then merging (Swin) | Spatial granularity of tokens | Defect footprint (example A) |
| Token and layer | Class token, mean of patch tokens, last layer or concatenation of the last 4 layers (DINOv2 "+ms" segmentation) [§7.4] | Global versus local information | Intermediate layers keep more spatial detail |
| Interpolation and normalization | Bilinear in torchvision presets; bicubic in DINOv2 evaluation | Input statistics | Must match the checkpoint's recipe |
| Adaptation scope | Linear head; last blocks; LoRA rank $r$ and scale $\alpha$; full fine-tuning | Capacity versus distortion and data needs | LP-FT for shifted targets; memory set by activations, not only by trainable parameters |
| Learning rate and epochs | Recipe-dependent; ConvNeXt's recipe alone took ResNet-50 from 76.1% to 78.8% [Liu et al. 2022, §2.1] | Comparability of architectures | Compare architectures under one recipe |
| Window size $M$ | Swin: 7 | Context per layer and cost | Shifted windows extend context over layers |

Tuning approach (project method). On a held-out split grouped by site, part batch or
camera: (1) verify the input contract with a fixed image; (2) run the frozen baseline
at two resolutions or with native tiles; (3) sweep the adaptation scope from linear
head to partial and full fine-tuning, with LP-FT when the domain differs; (4) only
then compare backbones under the same recipe. Watch per-defect-size recall and
false alarms, not only the mean.

## Properties and limits of guarantees

- **Inductive bias.** CNNs build in locality, two-dimensional neighborhoods and
  translation equivariance; ViT uses the 2D structure only when cutting patches and
  when adjusting position embeddings, so spatial relations must be learned
  [Dosovitskiy et al., §3.1]. Its authors report that ViT underperforms comparable
  ResNets when trained on mid-sized data and that "large scale training trumps
  inductive bias" [§1]. These are empirical findings at their scale, not guarantees
  for a small industrial dataset.
- **Linear cost of windows.** Swin's complexity is linear in image size for fixed $M$
  [Liu et al., §3.2]; this concerns the attention term, not latency on a given
  runtime.
- **Architecture versus recipe.** ConvNeXt attributes a large part of the gap between
  ConvNets and vision Transformers to training techniques and reaches 82.0% against
  Swin-T's 81.3% in the ResNet-50/Swin-T compute regime [Liu et al. 2022, §2.1, §2]:
  architecture claims need matched recipes.
- **Frozen features.** DINOv2 features are competitive without fine-tuning on many
  benchmarks [Oquab et al., §1, §7], and a frozen backbone with a ViT-Adapter and a
  Mask2Former head reached 60.2 mIoU on ADE20k [§7.4]. Benchmark transfer does not
  guarantee separability of small defects on a new camera.
- **Similarity scores** are not calibrated probabilities; thresholds belong to a
  dataset and a version of the model.
- **Naming.** DINOv2 (self-distillation features) and DINO the DETR-style detector are
  different methods with a shared name (naming note, not a source claim).

## Cost and implementation

Cost drivers, with their variables:

- **Inference**: backbone cost grows with $N$ (linearly for convolutions and windowed
  attention, with an $N^2$ term for global attention); resolution and tiling dominate
  the budget (example A). A frozen backbone still runs on every image.
- **Training**: memory is driven by activations of the layers that receive gradients,
  optimizer state and batch size; a linear probe on cached features avoids the
  backbone entirely during training, LoRA or adapters through a live backbone do not.
- **Pretraining**: DINOv2's ablation found training at 416 pixels about three times
  more expensive than at 224, and a short high-resolution phase almost as good
  [Oquab et al., §6.6].
- **Reported figures**: DINOv2's frozen segmentation pipeline trained in 28 hours on
  16 V100 GPUs [§7.4]. Such numbers depend on hardware and code; they set orders of
  magnitude only.

### torchvision 0.20 and DINOv2 contracts

Read in the torchvision v0.20.0 sources and the DINOv2 repository at commit
`7764ea0`; no code was executed for this note.

- `ImageClassification(crop_size, resize_size=256, mean, std,
  interpolation=BILINEAR, antialias=True)` resizes, center-crops, converts with
  `convert_image_dtype` and normalizes [_presets.py, L38–L64]; `ViT_B_16_Weights.IMAGENET1K_V1`
  uses it with `crop_size=224` [vision_transformer.py, L351–L357].
- `VisionTransformer` checks that height and width equal `image_size` and that
  `image_size` is divisible by the patch size; its sequence length is
  $(\text{image\_size}/P)^2+1$ [vision_transformer.py, L180, L214–L221, L266–L273].
- DINOv2 hub backbones default to `img_size=518`, `patch_size=14`, with variants with
  register tokens (`*_reg`) [backbones.py, L33–L34, L114–L172]; patch embedding
  asserts sides divisible by 14 [patch_embed.py, L72–L73]; `forward_features` returns
  `x_norm_clstoken`, `x_norm_regtokens` and `x_norm_patchtokens`
  [vision_transformer.py, L257–L272].

## Evaluation and controlled variation

**Protocols.** Linear probing on frozen features, k-NN, partial fine-tuning and full
fine-tuning answer different questions; MAE's authors argue that linear separability
"is not the sole metric for evaluating representation quality" [He et al., §4.3]. For
dense tasks, DINOv2 reports a linear layer on patch tokens and a boosted "+ms" variant
with the last four layers, 640-pixel inputs and multiscale test-time augmentation
[Oquab et al., §7.4]. Distribution shift needs an out-of-distribution test set: Kumar
et al. use ten shift benchmarks [abstract]. Industrial evaluation should group splits
by site, batch or camera ([CV-FIABILITE](../../130-evaluation-fiabilite/references/133-donnees-generalisation.md))
and report recall per defect size in physical units.

**Published results with their protocol.** Fine-tuning versus linear probing: +2%
in distribution, −7% out of distribution on average; LP-FT +1% and +10% over full
fine-tuning [Kumar et al., abstract]. MAE ViT-L: 73.5% with a linear probe, 81.0% when
tuning one block [He et al., §4.3]. ConvNeXt-T 82.0% versus Swin-T 81.3% on ImageNet-1K
at about $4.5\times10^9$ FLOPs [Liu et al. 2022, §2]. These measure different
protocols on public benchmarks.

### Proposed baseline and controlled variation (not executed)

- **Question**: does input resolution, rather than the backbone, limit the detection
  of small defects?
- **Data**: images from the target line with defect masks, split by production batch;
  defect sizes binned in millimeters.
- **Baseline**: a frozen DINOv2 ViT-S/14 at 224 pixels with the repository's evaluation
  transform, patch tokens, and a distance-to-nominal patch score (as in
  [CV-ANOMALIES](73-patchcore-padim.md)).
- **Controlled variation**: the same model, weights, score and thresholds rule, applied
  to native-resolution 224-pixel tiles of the original image.
- **Measurements**: per-size recall at a fixed false-alarm rate per part, localization
  error in millimeters, latency per part on the target hardware.
- **Expected effect (hypothesis)**: gains concentrated on defects smaller than about one
  patch at the downscaled resolution (example A), at roughly the cost multiplied by
  the number of tiles.
- **Confound**: tiles change the context seen by each token and the background
  statistics of the nominal bank; keep the nominal bank built with the same tiling.

**Measurement limits.** Public benchmark rankings rarely transfer to a single
production line; small test sets give wide confidence intervals per defect class;
leakage between near-duplicate images of the same part inflates every protocol.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Accuracy drops after a loader change | Channel order, interpolation, missing $/255$, double normalization, crop | Fingerprint tensors per stage on one image; constant-color test image (example E) | Restore the checkpoint's input contract before any retraining |
| Good on random validation, poor on a new site | Leakage of scenes or parts across splits; domain shift | Re-split by site or batch; compare frozen and fine-tuned models OOD | Grouped splits; LP-FT or frozen features; site-specific calibration |
| Small defects missed, large ones fine | Defect smaller than a patch after resizing | Recall by defect size; native-resolution tiles (example A) | Tiling, higher resolution, earlier layers, a CNN with finer stride |
| Anomaly map blurry or shifted | Upsampled low-resolution token grid; coordinate mapping through crop or pad | Overlay a synthetic marker of known position | Correct the mapping; finer grid or intermediate layers |
| Fine-tuned model worse than its linear probe out of distribution | Feature distortion during fine-tuning | Compare LP, FT and LP-FT on a shift set | LP-FT; lower learning rate on the backbone; partial fine-tuning |
| Out-of-memory with few trainable parameters | Activations of a live backbone dominate | Peak memory per configuration | Cache features; gradient checkpointing; smaller input |
| Error at a new resolution, or degraded features | Fixed `image_size` or uninterpolated position embeddings; side not divisible by $P$ | Check model assertions and position-embedding shape | Interpolate positions; pad to a multiple of $P$; evaluate the effect |
| Two backbones compared, recipe differs | Training recipe, not architecture, explains the gap | Rerun both with one recipe | Report architecture claims only under matched recipes |

## Alternatives and applications

Conditional choices:

- **Prefer HOG or other hand-designed features with a linear classifier** when data
  are scarce, the pattern is rigid (a fixed part, a known orientation) and
  explainability or very low compute matter.
- **Prefer a CNN or ConvNeXt** for dense tasks on edge hardware, when fine spatial
  strides and mature runtime support matter.
- **Prefer frozen self-supervised features (DINOv2)** with a light head or a
  nearest-neighbor rule when labels are few and the domain is not far from the
  pretraining images; validate on the target camera first.
- **Prefer partial fine-tuning, adapters or LoRA** when many variants must be stored or
  memory for full fine-tuning is lacking; merge LoRA for deployment when the update is
  linear.
- **Prefer full fine-tuning, or LP-FT**, when the target domain is far from pretraining
  and enough labeled data exist; check out-of-distribution behavior.
- **Prefer text-aligned embeddings** ([CV-CLIP](72-clip-siglip.md)) when classes must be
  named in language rather than learned from examples.

Industrial uses (project reasoning, not published results): visual inspection with
a frozen backbone and a nominal-patch bank; retrieval of similar defects or parts by
cosine similarity; site-specific classification with LoRA variants sharing one
backbone; quality monitoring of features for drift.

## Guided reasoning and proposed checks

These constructed cases develop architectural bias, scale and transfer protocol. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-REPRESENTATIONS-001

**Working question**: In a ViT with fixed patch size and dense global attention, how does doubling image width and height change the number of image tokens, excluding the class token, and the associated quadratic term?

**Reference answer**: Tokens ×4; quadratic term ×16, in this cost model.

**Derivation of the cost**: With fixed patches of side $P$ and compatible dimensions, $N=HW/P^2$. Doubling $H$ and $W$ multiplies the number of patches by four. A global matrix of interactions between tokens then has sixteen times as many pairs. This count concerns the attention term considered, not all operations of the network.

**Proposed practical consequence**: Before increasing resolution for small defects, estimate activation memory and test end-to-end latency. Projections, convolutions, kernels and bandwidth constraints do not necessarily follow the same factor. A smaller batch or another representation can change the tradeoff. Also check whether the defect information exists in the original acquisition: enlarging an image without additional detail does not bring the same observations as a capture that is actually better resolved. Measurements on the target hardware therefore complement the cost model.

### Case linked to CV-REPRESENTATIONS-005

**Working question**: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?

**Reference answer**: Color order, normalization, range, interpolation, crop and resolution actually received.

**Interface trap**: Two loaders can produce visually similar images while differing in channel order or in how pixel centers are handled. Repeated or omitted normalization can also strongly alter the received tensor. The backbone sees only these values, not the intent of the pipeline.

**Proposed reproducible investigation**: Use an identical reference file, save the shapes, types, ranges and selected pixels after each step, and then compare the input tensors. Repeat the extraction with the same weights and parameters. If the features change before any scene variation, first look for this deterministic difference. Once the contract is restored, evaluate the new domain on a held-out set. A fine-tuning run launched too early can partially absorb a preprocessing bug, make the regression less visible and complicate reproducibility without addressing its cause.

**Documentation consulted for this pass**: [ViT](https://arxiv.org/html/2010.11929v2), §3, representation by patches. The other developments are in the [flashcards](../71-representations-transfert.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-REPRESENTATIONS-001

**Situation**: In a ViT with fixed patch size and dense global attention, how does doubling image width and height change the number of image tokens, excluding the class token, and the associated quadratic term?

**Example of dimensions**: A $224\times224$ image with $16\times16$ patches gives 196 image tokens; at $448\times448$, it gives 784. Attention typically computes, per head, $QK^T$ of size $N\times N$, then a combination of values. The interaction term is of order $N^2d$, while the projections and the MLP introduce terms of order $Nd^2$ for a width $d$. Depending on the regime, these contributions and memory access do not dominate in the same way. Memory-saving implementations can avoid storing the entire matrix without removing the quadratic count of computed interactions.

### CV-REPRESENTATIONS-002

**Situation**: Do Swin and ConvNeXt replace CNNs with the same global attention mechanism?

**Counting by windows**: If a window contains $M^2$ tokens and the image contains $N$ tokens, the interactions inside windows total about $(N/M^2)(M^2)^2=NM^2$, instead of $N^2$ for global attention, at fixed width. This simplification assumes a fixed window size and ignores projections, MLP, padding and hierarchical merging. Shifted windows let successive blocks connect previously separated regions. The receptive field is therefore built over layers; a local layer does not access the entire image at once. Comparing this organization to convolutions also requires examining resolution, number of channels and the dense-task head.

### CV-REPRESENTATIONS-003

**Situation**: What is missing between DINOv2 features and an industrial defect detector ready for evaluation?

**From tokens to the defect region**: Selecting local features keeps a grid of patches, while a global vector aggregates the image. Interpolating the grid to the original resolution increases the number of pixels of the score, without creating a localization accuracy absent from the features. Define how a patch covers the part and what defect size it must distinguish. A constructed baseline can freeze the extractor, index the nominal patches and use their distance as a score, before comparing with a supervised head. Keeping part masks, alignment and the aggregation policy allows errors to be attributed to the representation choice rather than to an implicit interface.

### CV-REPRESENTATIONS-004

**Situation**: Which tradeoffs distinguish linear probing, full fine-tuning and LoRA/adapters for visual transfer learning?

**LoRA parametrization**: For a layer $W\in\mathbb R^{d\times k}$, replacing the full update with $\Delta W=BA$, with $B\in\mathbb R^{d\times r}$ and $A\in\mathbb R^{r\times k}$, trains $r(d+k)$ parameters instead of $dk$, excluding biases and other modules. The rank $r$ constrains the space of updates and is a tradeoff to validate. When the adaptation is linear and compatible with the weight representation, one can form $W'=W+BA$ for inference; this differs from a nonlinear adaptation kept in the computation path. The small number of learned parameters therefore does not, by itself, describe the graph actually deployed.

### CV-REPRESENTATIONS-005

**Situation**: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?

**Preprocessing invariant**: If the model expects $z_c=(x_c/255-\mu_c)/\sigma_c$, giving it $x_c\in[0,255]$ directly before subtraction changes the scale by a factor close to 255, without any change of physical domain. Testing a synthetic image in which each channel is constant with a distinct value detects an RGB/BGR permutation and repeated normalization. For a dense task, also check how crop, resize and padding transform labels and coordinates. An identical input image is a sufficient control only if all stochastic steps are disabled and the weights, evaluation mode and numerical precision are also fixed.

**Passages consulted for these developments**: [ViT](https://arxiv.org/html/2010.11929v2), §3.1, patch sequence; project counts and tests; [Liu et al., Swin](https://arxiv.org/html/2103.14030v2), §3.2, equations 1–2, windows and shifts; counting explained by the project; [Oquab et al., DINOv2](https://arxiv.org/html/2304.07193v2), §7.4, patch tokens, low-resolution logit map and upsampling; proposed inspection baseline; [Hu et al., LoRA](https://arxiv.org/html/2106.09685v2), §4.1, parametrization W+BA and linear merging.

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

### Scientific sources

- [Dosovitskiy et al. 2021, ViT, arXiv 2010.11929v2](https://arxiv.org/html/2010.11929v2): §1 (scale versus inductive bias), §3.1 ($N=HW/P^2$, class token, position embeddings, inductive bias), §3.2 (higher resolution, 2D interpolation of position embeddings).
- [Liu et al. 2021, Swin Transformer, arXiv 2103.14030v2](https://arxiv.org/html/2103.14030v2): §3.1 (4×4 patches, patch merging), §3.2 (eqs. 1–2, $M=7$, shifted windows).
- [Liu et al. 2022, ConvNeXt, arXiv 2201.03545](https://arxiv.org/html/2201.03545): §2 and Fig. 2 (modernization without attention), §2.1 (recipe: 76.1% to 78.8%), §2.2 (stage ratio, patchify stem), §2.5 (kernel size), final comparison with Swin-T (82.0% versus 81.3%).
- [Oquab et al. 2023, DINOv2, arXiv 2304.07193v2](https://arxiv.org/html/2304.07193v2): §1 (frozen features, distillation), §3 (LVD-142M curation), §4 (518-pixel final phase), §6.6 (resolution cost), §7.4 (linear and +ms dense evaluation, frozen ViT-Adapter result).
- [He et al. 2022, MAE, arXiv 2111.06377](https://arxiv.org/html/2111.06377): §1 and Fig. 1 (75% masking, encoder on visible patches), §4.3 (linear probing versus partial fine-tuning).
- [Kumar et al. 2022, "Fine-Tuning can Distort Pretrained Features and Underperform Out-of-Distribution", arXiv 2202.10054](https://arxiv.org/html/2202.10054): abstract, §4.1, §4.2 (LP versus FT, LP-FT).
- [Hu et al. 2022, LoRA, arXiv 2106.09685v2](https://arxiv.org/html/2106.09685v2): §3 (adapter latency), §4.1 ($W_0+BA$, initialization, $\alpha/r$, merging).
- [Houlsby et al. 2019, adapters, arXiv 1902.00751](https://arxiv.org/html/1902.00751): §2.1 (bottleneck adapters, skip connection, near-identity initialization).
- [Dalal and Triggs 2005, HOG, CVPR](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf): §6 (default detector: 9 bins, cells, blocks, L2-Hys, 64×128 window).

### Implementation sources

- [torchvision v0.20.0, `torchvision/transforms/_presets.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/transforms/_presets.py): `ImageClassification` (L38–L64).
- [torchvision v0.20.0, `torchvision/transforms/_functional_tensor.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/transforms/_functional_tensor.py): `convert_image_dtype` (L66–L74).
- [torchvision v0.20.0, `torchvision/models/vision_transformer.py`](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/models/vision_transformer.py): size checks and sequence length (L180, L214–L221, L266–L273), `ViT_B_16_Weights` (L351–L357), `interpolate_embeddings` (L789–L801).
- [DINOv2 at commit 7764ea0, `dinov2/hub/backbones.py`](https://github.com/facebookresearch/dinov2/blob/7764ea0f912e53c92e82eb78a2a1631e92725fc8/dinov2/hub/backbones.py): defaults (L33–L34), register variants (L114–L172).
- [DINOv2 at commit 7764ea0, `dinov2/models/vision_transformer.py`](https://github.com/facebookresearch/dinov2/blob/7764ea0f912e53c92e82eb78a2a1631e92725fc8/dinov2/models/vision_transformer.py): position interpolation (L182–L205), `forward_features` (L257–L272), `get_intermediate_layers` (L301–L330); [`dinov2/layers/patch_embed.py`](https://github.com/facebookresearch/dinov2/blob/7764ea0f912e53c92e82eb78a2a1631e92725fc8/dinov2/layers/patch_embed.py) (L72–L73); [`dinov2/data/transforms.py`](https://github.com/facebookresearch/dinov2/blob/7764ea0f912e53c92e82eb78a2a1631e92725fc8/dinov2/data/transforms.py) (L42–L43, L76–L91).

### Related flashcards and references

- [Flashcards](../71-representations-transfert.md): CV-REPRESENTATIONS-001 (token cost), CV-REPRESENTATIONS-002 (Swin and ConvNeXt), CV-REPRESENTATIONS-003 (from features to a defect detector), CV-REPRESENTATIONS-004 (adaptation tradeoffs), CV-REPRESENTATIONS-005 (preprocessing diagnosis).
- Related references: [CV-CLIP](72-clip-siglip.md), [CV-ANOMALIES](73-patchcore-padim.md), [CV-FIABILITE](../../130-evaluation-fiabilite/references/133-donnees-generalisation.md), [CV-QUANT](../../140-ingenierie-systemes/references/142-quantification-runtimes.md).

Drafted by agent, 2026-10-18. Revision 8, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/71-representations-transfert.md).
