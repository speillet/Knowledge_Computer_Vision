# Flashcards — Visual representations, ViT, Swin, ConvNeXt and DINOv2

reference note: [[70-reconnaissance-representations/references/71-representations-transfert|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-REPRESENTATIONS-001

Objective: Estimate the cost of tokens. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-001
Question: In a ViT with fixed patch size and dense global attention, how does doubling image width and height change the number of image tokens, excluding the class token, and the associated quadratic term?
Reponse: **Expected answer**: Tokens ×4; quadratic term ×16, in this cost model.

**Further explanation**: This is not an exact prediction of total time: kernels, memory and the other blocks also count.

**Derivation of the cost**: With fixed patches of side $P$ and compatible dimensions, $N=HW/P^2$. Doubling $H$ and $W$ multiplies the number of patches by four. A global matrix of interactions between tokens then has sixteen times as many pairs. This count concerns the attention term considered, not all operations of the network.

**Proposed practical consequence**: Before increasing resolution for small defects, estimate activation memory and test end-to-end latency. Projections, convolutions, kernels and bandwidth constraints do not necessarily follow the same factor. A smaller batch or another representation can change the tradeoff. Also check whether the defect information exists in the original acquisition: enlarging an image without additional detail does not bring the same observations as a capture that is actually better resolved. Measurements on the target hardware therefore complement the cost model.

**Example of dimensions**: A $224\times224$ image with $16\times16$ patches gives 196 image tokens; at $448\times448$, it gives 784. Attention typically computes, per head, $QK^T$ of size $N\times N$, then a combination of values. The interaction term is of order $N^2d$, while the projections and the MLP introduce terms of order $Nd^2$ for a width $d$. Depending on the regime, these contributions and memory access do not dominate in the same way. Memory-saving implementations can avoid storing the entire matrix without removing the quadratic count of computed interactions.

**Quadratic attention is only one runtime term**: For token count $N$ and embedding width $d$, dense attention includes an $N^2d$ interaction term while projections and feed-forward blocks have terms proportional to $Nd^2$. Quadrupling tokens multiplies those terms by sixteen and four, respectively, before implementation effects. This explains why the front's sixteenfold statement applies to the quadratic term rather than guaranteeing sixteenfold wall time or memory. Measure the actual inference path at the intended batch size.

**Blocking errors**: Announcing a guaranteed ×16 latency for the whole transformer.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]] ; [Dosovitskiy et al., ViT, §3.1, patch tokens](https://arxiv.org/html/2010.11929v2) ; [Liu et al., Swin, §3.2, eq. 1, quadratic term of global attention](https://arxiv.org/html/2103.14030v2). Cost counts: project deduction.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-REPRESENTATIONS-001 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-002

Objective: Situate Swin and ConvNeXt. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-002
Question: Do Swin and ConvNeXt replace CNNs with the same global attention mechanism?
Reponse: **Expected answer**: No: Swin uses a hierarchy of shifted local windows; ConvNeXt remains a modernized ConvNet.

**Further explanation**: Separate structure and training recipe, then compare on the same target protocol.

**What is being compared**: An architecture describes operations and their connections; a training recipe describes the data, objectives and settings used to learn them. An improvement observed when both change cannot automatically be attributed to a single architectural mechanism.

**Constructed comparison**: For a dense task, examine feature resolution, hierarchy and head cost, then compare on the same splits and inference constraints. Window attention restricts interactions to a local window at each level, while shifts and hierarchy organize the exchange of information. A ConvNet can modernize its design without becoming a global-attention model. The correct reasoning links receptive field, scale, memory and protocol to the task, rather than ranking all methods under a supposedly superior label. The named methods are identified here; each would require a dedicated reference note for complete mastery.

**Counting by windows**: If a window contains $M^2$ tokens and the image contains $N$ tokens, the interactions inside windows total about $(N/M^2)(M^2)^2=NM^2$, instead of $N^2$ for global attention, at fixed width. This simplification assumes a fixed window size and ignores projections, MLP, padding and hierarchical merging. Shifted windows let successive blocks connect previously separated regions. The receptive field is therefore built over layers; a local layer does not access the entire image at once. Comparing this organization to convolutions also requires examining resolution, number of channels and the dense-task head.

**Local windows exchange information across layers**: Nonoverlapping attention windows alone would isolate neighboring regions at each layer. Shifting their partition allows later blocks to connect tokens previously separated by a boundary, while the hierarchy changes spatial resolution. This is a mechanism for extending context without one global attention matrix at every block. ConvNeXt instead uses convolutional operations; comparing the two requires matching the downstream output scale, feature budget and deployment measurements.

**Blocking errors**: Calling ConvNeXt a transformer, or saying that every Swin layer performs global attention.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]] ; [Liu et al., Swin, §3.1 and §3.2, eqs. 1–2, shifted windows](https://arxiv.org/html/2103.14030v2) ; [Liu et al., ConvNeXt, §2 and Fig. 2, modernization without attention; §2.1, training recipe](https://arxiv.org/html/2201.03545). Window counting: project deduction.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-REPRESENTATIONS-002 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-003

Objective: Use self-supervised features. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-003
Question: What is missing between DINOv2 features and an industrial defect detector ready for evaluation?
Reponse: **Expected answer**: Define output, head or decision strategy, data, thresholds and product validation protocol.

**Further explanation**: Transferable features are not automatically a semantic taxonomy or a calibrated score on the new domain.

**Transition from representation to decision**: A feature describes the image according to the pretraining; the product must still define the defect, its location and the behavior when no known example fits. A supervised head, a nominal comparison or a search for neighbors pose different problems and data needs.

**Proposed baseline**: Fix the extraction and preprocessing, choose a simple rule, then measure missed defects and false rejections by part type. Then compare a controlled adaptation on the same held-out data. An excellent average transfer to a benchmark does not establish the separability of the small defects of the new camera. Examine feature scale, nominal coverage, and thresholds before making the system more complex. Representation is a useful resource; the evaluation should focus on the outputs actually consumed by the inspection, with a policy for uncertain cases.

**From tokens to the defect region**: Selecting local features keeps a grid of patches, while a global vector aggregates the image. Interpolating the grid to the original resolution increases the number of pixels of the score, without creating a localization accuracy absent from the features. Define how a patch covers the part and what defect size it must distinguish. A constructed baseline can freeze the extractor, index the nominal patches and use their distance as a score, before comparing with a supervised head. Keeping part masks, alignment and the aggregation policy allows errors to be attributed to the representation choice rather than to an implicit interface.

**Upsampling cannot recreate missing defect evidence**: If a thin scratch is smaller than the feature grid support and has been suppressed by acquisition or feature extraction, interpolating its anomaly map to full image size does not restore the original detail. Evaluate critical defect sizes in original pixels and physical units. A proposed baseline compares multiple input resolutions or local crops under the same decision protocol, including processing cost and false alarms from texture.

**Blocking errors**: Presenting feature extraction alone as a complete supervised solution.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]] ; [Oquab et al., DINOv2, §1, frozen features; §7.4, linear head on patch tokens and upsampled low-resolution logits](https://arxiv.org/html/2304.07193v2). Inspection baseline: project proposal.
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-REPRESENTATIONS-003 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-004

Objective: Choose an adaptation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-004
Question: Which tradeoffs distinguish linear probing, full fine-tuning and LoRA/adapters for visual transfer learning?
Reponse: **Expected answer**: They train a head, the whole model or a smaller parametrized part, respectively; training costs and flexibility differ.

**Further explanation**: Measure generalization, data needs and final cost; few learned parameters do not guarantee faster inference.

**Reasoning about resources**: Freezing the backbone reduces the number of gradients and modified parameters, but its features must still be computed for each new image. Adaptive modules can reduce the cost of learning or storing variants without removing the backbone from the inference.

**Proposed comparison**: Keep the data and target output fixed, then compare a single head, partial adaptation and full fine-tuning on generalization, training memory and final cost. Also report the cost of activations and how the adapted parameters are integrated into the deployed model. A small number of trained parameters can be useful for several product variants; it does not prove better accuracy with little data or a speedup on every runtime. Full fine-tuning is not uniformly better either: when pretrained features are good and the shift is large, it averaged 2% higher in-distribution but 7% lower out-of-distribution accuracy than linear probing on ten shift benchmarks, and linear probing then fine-tuning (LP-FT) reduced that loss. The choice therefore depends on the capacity required by the domain change and on the resources actually constrained.

**LoRA parametrization**: For a layer $W\in\mathbb R^{d\times k}$, replacing the full update with $\Delta W=BA$, with $B\in\mathbb R^{d\times r}$ and $A\in\mathbb R^{r\times k}$, trains $r(d+k)$ parameters instead of $dk$, excluding biases and other modules. The rank $r$ constrains the space of updates and is a tradeoff to validate. When the adaptation is linear and compatible with the weight representation, one can form $W'=W+BA$ for inference; this differs from a nonlinear adaptation kept in the computation path. The small number of learned parameters therefore does not, by itself, describe the graph actually deployed.

**Trainable-parameter count is not total training memory**: Freezing most weights can reduce optimizer state and gradient storage, but backpropagation through selected layers can still require substantial intermediate activations. A linear probe on cached frozen features has a different cost profile from adapters or LoRA trained through a live backbone. Compare peak memory, training time and validation quality for the actual configuration. A smaller trainable update constrains adaptation; it does not guarantee robustness on a small dataset.

**Blocking errors**: Equating a small number of trained parameters with low latency.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]] ; [Hu et al., LoRA, §3 adapter latency and §4.1 low-rank update and merging](https://arxiv.org/html/2106.09685v2) ; [Houlsby et al., adapters, §2.1](https://arxiv.org/html/1902.00751) ; [Kumar et al., LP versus FT and LP-FT, abstract and §4](https://arxiv.org/html/2202.10054). The adaptation principle is transposed to vision without reusing the NLP gains; memory reasoning: project deduction.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-REPRESENTATIONS-004 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-005

Objective: Check a backbone's preprocessing. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-005
Question: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?
Reponse: **Expected answer**: Color order, normalization, range, interpolation, crop and resolution actually received.

**Further explanation**: Compare an identical image in both pipelines before attributing the deviation to the data or the architecture.

**Interface trap**: Two loaders can produce visually similar images while differing in channel order or in how pixel centers are handled. Repeated or omitted normalization can also strongly alter the received tensor. The backbone sees only these values, not the intent of the pipeline.

**Proposed reproducible investigation**: Use an identical reference file, save the shapes, types, ranges and selected pixels after each step, and then compare the input tensors. Repeat the extraction with the same weights and parameters. If the features change before any scene variation, first look for this deterministic difference. Once the contract is restored, evaluate the new domain on a held-out set. A fine-tuning run launched too early can partially absorb a preprocessing bug, make the regression less visible and complicate reproducibility without addressing its cause.

**Preprocessing invariant**: If the model expects $z_c=(x_c/255-\mu_c)/\sigma_c$, giving it $x_c\in[0,255]$ directly before subtraction changes the scale by a factor close to 255, without any change of physical domain. Testing a synthetic image in which each channel is constant with a distinct value detects an RGB/BGR permutation and repeated normalization. For a dense task, also check how crop, resize and padding transform labels and coordinates. An identical input image is a sufficient control only if all stochastic steps are disabled and the weights, evaluation mode and numerical precision are also fixed.

**Compare tensors before comparing predictions**: A proposed loader regression check uses the same encoded image and records decoded channels, resize/crop coordinates and the normalized tensor from both paths. Compare elementwise differences at each stage before running the backbone. This locates an interface discrepancy even when final predictions differ unpredictably. Include color-chart and high-frequency patterns because ordinary photos may hide channel permutations or interpolation changes. Do not infer preprocessing equivalence from matching tensor dimensions.

**Blocking errors**: Changing the training without checking the input contract.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]] ; [torchvision v0.20.0, ImageClassification preset, L38–L64](https://github.com/pytorch/vision/blob/v0.20.0/torchvision/transforms/_presets.py#L38-L64) ; [DINOv2 evaluation transform at commit 7764ea0, L76–L91](https://github.com/facebookresearch/dinov2/blob/7764ea0f912e53c92e82eb78a2a1631e92725fc8/dinov2/data/transforms.py#L76-L91). Preprocessing check: project proposal.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-REPRESENTATIONS-005 provenance::agent pole::A pole::D pole::E
END
