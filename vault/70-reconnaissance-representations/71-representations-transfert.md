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

**Further explanation**: This is not an exact prediction of total time: kernels, memory and other blocks count.

**derivation of cost**: with fixed $P$ side patches and compatible dimensions, $N=HW/P^2$. Double $H$ and $W$ multiplies the number of patches by four. A global matrix of interactions between tokens then has sixteen times as many pairs. This count concerns the term of attention considered, not all operations of the network.

**Proposed practical consequence**: Before increasing resolution for small faults, estimate activation memory and test full latency. Projections, convolutions, kernels and bandwidth constraints do not necessarily follow this same factor. A batch reduction or other representation can change the compromise. Also check if the information of the defect exists in the initial acquisition: enlarging an image without additional detail does not bring the same observations as a capture actually better resolved. Measures on the target material therefore complement the cost model.

**Example of dimensions**: a $224\times224$ image with $16\times16$ patches gives 196 image tokens; at $448\times448$, it gives 784. One attention per head typically calculates $QK^T$ of size $N\times N$, then a combination of values. The interaction term is of order $N^2d$, while the projections and the MLP introduce order terms $Nd^2$ for a width $d$. Depending on the plan, these contributions and memory access do not dominate in the same way. Memory-saving implementations can avoid storing the entire matrix without necessarily removing quadratic counting from calculated interactions.

**Blocking errors**: Announce guaranteed ×16 latency to transform everything.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]]; [ViT, §3.1](https://arxiv.org/abs/2010.11929); analytical counting of the project; [ViT, §3.1, sequence of patches; project counts and tests](https://arxiv.org/html/2010.11929v2), consult the 2026-10-30.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-REPRESENTATIONS-001 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-002

Objective: Swin and ConvNeXt. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-002
Question: Do Swin and ConvNeXt replace CNNs with the same global attention mechanism?
Reponse: **Expected answer**: No: Swin uses an offset local window hierarchy; ConvNeXt remains a modernized ConvNet.

**Further explanation**: Separate structure and training recipe, then compare on the same target protocol.

**What we compare**: An architecture describes operations and their connections; a training recipe describes the data, objectives, and settings used to learn them. An improvement observed by changing the two does not automatically relate to a single architectural mechanism.

**Example of comparison built**: For a dense task, examine feature resolution, hierarchy, and head cost, and then compare the same splits and inference constraints. Window attention limits some local interactions to one level, while shifts and hierarchy organize the exchange of information. A ConvNet can modernize its design without becoming a global attention. The correct reasoning is to link information field, scale, memory, and protocol to the task, not to classify all methods under a supposedly superior label. The named methods are identified here; each would require a dedicated reference note for its complete mastery.

**Counting by windows**: If a window contains $M^2$ tokens and the image contains $N$ tokens, the internal interactions total about $(N/M^2)(M^2)^2=NM^2$, instead of $N^2$ for global attention, fixed width. This simplification assumes a fixed window size and ignores projections, MLP, padding, and hierarchical merge. The staggered windows allow successive blocks to communicate previously separated regions. The information field is therefore built over layers; a local layer does not instantly access the entire image. Comparing this organization to convolutions requires also examining resolution, number of channels and dense task head.

**Blocking errors**: Qualify ConvNeXt to transform or each Swin layer of overall attention.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]]; [ViT, §§3 – 4](https://arxiv.org/abs/2010.11929); [Swin, §3](https://arxiv.org/abs/2103.14030); [ConvNeXt, §2](https://arxiv.org/abs/2201.03545); [DINOv2, method and transfer](https://arxiv.org/abs/2304.07193); [Liu et al., Swin, §3.2, equations 1 – 2, windows and offset; counting explained by the project](https://arxiv.org/html/2103.14030v2), see the 2026-10-30.
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

**Transition from representation to decision**: a feature describes the image according to the pretraining; the product must still define defect, location and behavior when no known example is suitable. A supervised head, a nominal comparison or a search for neighbors pose different problems and data needs.

**Proposed Baseline**: fix extraction and pre-treatment, choose a simple rule, then measure missed defects and false rejections by part type. Then compare a controlled adaptation with the same reserved data. An excellent average transfer to a benchmark does not establish the separability of the small defects of the new camera. Examine feature scale, nominal coverage, and thresholds before making the system more complex. Representation is a useful resource; the evaluation should focus on the outputs actually consumed by the inspection, with a policy for uncertain cases.

**From the token to the default zone**: Selecting local features retains a grid of patches, while a global vector aggregates the image. Interpolation of the grid to the original resolution increases the number of pixels of the score, without creating in itself a location accuracy absent from the features. Define how a patch covers the room and what defect size it should distinguish. A constructed baseline can freeze the extractor, index the nominal patches and use their distance as a score, before comparing to a supervised head. Keeping room masks, alignment, and aggregation policy allows errors to be attributed to the representation choice rather than to an implicit interface.

**Blocking errors**: Present extraction alone as a complete supervised solution.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]]; [ViT, §§3 – 4](https://arxiv.org/abs/2010.11929); [Swin, §3](https://arxiv.org/abs/2103.14030); [ConvNeXt, §2](https://arxiv.org/abs/2201.03545); [DINOv2, method and transfer](https://arxiv.org/abs/2304.07193); [Oquab et al., DINOv2, §7.4, patch tokens, flashcard low resolution and interpolation; proposed inspection baseline](https://arxiv.org/html/2304.07193v2), see the 2026-10-30.
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-REPRESENTATIONS-003 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-004

Objective: Choose an adaptation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-004
Question: Which tradeoffs distinguish linear probing, full fine-tuning and LoRA/adapters for visual transfer learning?
Reponse: **Expected answer**: They drive a head, the whole model or a smaller set-up, respectively; learning costs and flexibility differ.

**Further explanation**: Measuring generalization, necessary data and final cost; few parameters learned does not guarantee faster inference.

**Reasoning about resources**: Freezing the backbone reduces the number of gradients and modified parameters, but the calculation of its features remains necessary for each new image. Adaptive modules can reduce the cost of learning or storing variants without removing the backbone from the inference.

**Proposed comparison**: Keep data and target output, then compare a single head, partial adaptation and full adjustment on generalization, training memory and final cost. Also report the cost of activations and how the appropriate parameters are integrated into the deployed model. A small number of trained parameters can be useful for several product variants; it does not prove better accuracy with little data or acceleration on each runtime. The choice therefore depends on the capacity required for the change of domain and the resources really constrained.

**Parametrisation LoRA**: For a layer $W\in\mathbb R^{d\times k}$, replace the complete update with $\Delta W=BA$, with $B\in\mathbb R^{d\times r}$ and $A\in\mathbb R^{r\times k}$, causes $r(d+k)$ parameters instead of $dk$, out of bias and other modules. Rank $r$ constrains the space of updates and is a compromise to validate. When the adaptation is linear and compatible with weight representation, one can form $W'=W+BA$ for inference; this differs from a non-linear adaptation kept in the computation path. The small number of parameters learned does not therefore, by itself, describe the graph actually deployed.

**Blocking errors**: Assimilate low number of parameters driven and low latency.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]]; [ViT, §3.1](https://arxiv.org/abs/2010.11929); [Hu et al., LoRA, summary and principle of frozen parameters](https://arxiv.org/abs/2106.09685); [Houlsby et al., adaptors, summary](https://arxiv.org/abs/1902.00751); principle of adaptation transposed to the vision, without taking back the NLP gains; [Hu et al., LoRA, §4.1, parametrization W+BA and linear fusion](https://arxiv.org/html/2106.09685v2), consult the 2026-10-30.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-REPRESENTATIONS-004 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-005

Objective: check preprocessing a backbone. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-005
Question: A pretrained backbone degrades after the image loader is replaced. What should be checked before another fine-tuning run?
Reponse: **Expected answer**: Color order, normalization, range, interpolation, crop and resolution actually received.

**Further explanation**: Compare an identical image in both strings before assigning the deviation to the data or architecture.

**Interface Trap**: Two chargers can produce visually similar images while differing in channel order or pixel center processing. Repeated or omitted normalization can also strongly alter the received tensor. The backbone sees only these values, not the pipeline intent.

**Proposed Reproducible Investigation**: use an identical cookie file, save known shapes, types, ranges and pixels after each step, and then compare the input tensors. Repeat the extraction with the same weights and parameters. If the features change before any scene variation, first look for this deterministic difference. Once the contract is restored, evaluate the new domain on a reserved set. A fine-tuning launched too early can partially absorb a pre-processing bug, make regression less visible and complicate reproducibility without having addressed its cause.

**Pretreatment Invariant**: If the model waits for $z_c=(x_c/255-\mu_c)/\sigma_c$, giving it $x_c\in[0,255]$ directly before subtraction changes the scale by a factor close to 255, without being a variation of physical domain. Testing an artificial image with each channel is constant and different makes it possible to detect permutation RGB/BGR and repeated normalization. For a dense task, also check the transformation of labels and coordinates by crop, resize and padding. An identical input image is only a sufficient witness if all stochastic steps are neutralized and if weight, mode of evaluation and numerical precision are also fixed.

**Blocking errors**: Change the drive without check the entry contract.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Full reference]]; [DINOv2, summary and valuation by transfer](https://arxiv.org/abs/2304.07193); check of the preprocessing proposed by the project.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-REPRESENTATIONS-005 provenance::agent pole::A pole::D pole::E
END
