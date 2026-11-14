# Flashcards — Open-vocabulary detection and grounding

reference note: [[80-detection-pose/references/83-detection-open-vocabulary|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-OPENVOC-001

Objective: separate the multimodal outputs. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-001
Question: Why can CLIP classification of an image not directly replace an open-vocabulary detector?
Reponse: **Expected answer**: Image classification scores the whole image; detection must also locate instances, with a suitable output protocol.

**Further explanation**: An image can contain multiple objects and candidates; grounding, classification, and generation do not all share the same metrics.

**Decomposition of the output**: A global image–text similarity may indicate that the content is compatible with a description. A detector must also propose positions and distinguish several occurrences, with their classes or their relation to the text. A score on the entire image does not determine these boxes or their number.

**Constructed example**: A scene with two cups and a plate may well match the text "cup" without giving the location of each cup. The detection evaluation should check instances, coordinates and missed objects, including when the prompted object is absent from the image. Referring-expression grounding can require yet another output, such as "the cup to the left of the plate". Define annotations, negatives, thresholds and metrics according to this contract. Language widens the set of candidate labels; it does not remove the need to check spatial accuracy and domain confusions.

**Where the text intervenes**: In Grounding DINO as described in the cited paper, text representations can guide the selection of queries and take part in decoding regions. The interface is therefore not limited to classifying a global vector after the fact. For each output, check what its score represents: a token, an expression or an aggregated category, depending on the implementation. Two occurrences of the same word in an image still require two distinct regions. A constructed test with one object, two objects and no object, with a fixed prompt, checks cardinality and localization without confusing the best linguistic match with a certain presence.

**Region grounding needs a localization evaluation**: A global image embedding can identify that an image resembles a text description while giving no location or count of the matching objects. Cropping every possible region would add a proposal/search problem with its own cost and evaluation. Compare instance recall, localization and absent-category behavior when evaluating open-vocabulary detection, rather than transferring a global zero-shot classification accuracy directly to the detection task.

**Blocking errors**: Treating an image–text score as a correctly localized box.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; [OWL-ViT, §3.1: per-token boxes and text queries](https://arxiv.org/html/2205.06230v2); [Grounding DINO, §§3.2 – 3.3](https://arxiv.org/abs/2303.05499); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-OPENVOC-001 provenance::agent pole::A pole::D
END

## CV-OPENVOC-002

Objective: Choose a system for an evolving catalog. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-002
Question: Track A — design: a product catalogue changes every month. How should a retrained closed-set detector be compared with an open-vocabulary detector?
Reponse: **Expected answer**: Define novelties, acceptable errors and annotation budget; compare the two on old / new products with negatives, fixed thresholds and maintenance cost.

**Further explanation**: Measure localization, rejection and latency; a hybrid approach may be warranted. The prompt alone does not guarantee that a new product is recognized.

**Proposed action**: Compare the cost of annotation and retraining with that of adjusting formulations, analyzing new false positives and maintaining the vocabulary. A changing catalogue may favour a text interface, but a visually very specific category may remain difficult to describe or recognize without targeted data.

**Transfer test**: Hold out new products not used for tuning, add close categories and images without any target, then measure localization and rejection at the operating point. Also keep old products to detect regressions. The choice can be hybrid, with a specialized detector for frequent products and another procedure for new ones. The comparison should state the available data and human interventions, rather than using a selected demonstration as proof of easy maintenance.

**Splitting the test over time**: Simulate several catalogue updates: fix an initial version, freeze the system, then introduce held-out products and close negatives. Measure the annotation and maintenance effort per cycle, as well as errors on old and new objects. The cost of a text-based method includes defining categories and validating prompts; that of the closed-set detector includes collection, training and new validation. If one product is visually indistinguishable from another in the available image, no formulation can guarantee the distinction. This protocol evaluates a capacity to evolve, rather than a single favourable snapshot of the catalogue.

**Vocabulary updates need backward-compatibility evidence**: A new product description can compete with old descriptions and change old-category decisions even without retraining the image encoder. A proposed monthly protocol freezes a reference set of old products, adds new products and near negatives, then measures both acquisition cost and regression on the old set. Include threshold/prompt maintenance and inference cost. An unchanged checkpoint does not imply an unchanged end-to-end classifier or detector.

**Blocking errors**: Choosing from a favourable demonstration without absent classes or a protocol.

**Grading criteria for this case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limits of the conclusion. Constructed case, without field observation.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; Project-designed case and protocol; Reference architectures: [OWL-ViT, §3](https://arxiv.org/abs/2205.06230) and [Grounding DINO, §3](https://arxiv.org/abs/2303.05499); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::conception cv_id::CV-OPENVOC-002 provenance::agent pole::A pole::D cas_pole::A::conception
END

## CV-OPENVOC-003

Objective: Check the specificity of the text. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-003
Question: A broad prompt produces boxes on related objects outside the target category. What should be tested?
Reponse: **Expected answer**: Class definition, formulations/negatives and region score on validation; inspect confusions and annotations.

**Further explanation**: Evaluate rejection rather than assuming that one threshold transfers to all descriptions.

**Why the text may be at issue**: A general description can correspond to several visual categories that an industrial taxonomy separates. A model can therefore return a region that is plausible in everyday language but wrong for the need. A single threshold does not necessarily resolve this ambiguity.

**Constructed investigation**: Record target and excluded classes, compare more precise formulations and close negatives on validation, then inspect regions and annotations. Separate localization failures from vocabulary confusion. Also assess the absence of a target, because choosing the best candidate does not prove its presence. A new formulation must be frozen before the final test. If the domain offers no visible discriminating cue, a better prompt may be insufficient; the interface must then allow rejection or verification rather than guaranteeing an exact category.

**Separate vocabulary from localization**: For each false positive, first compare the proposed region with the visible object, then the category of this object with the business definition. A correct box on a semantically neighbouring object is a different problem from a box placed across several objects. Adding more precise formulations can shift the whole score distribution: re-evaluate recall and rejection, without assuming a prompt-invariant threshold. Record the exact expressions, their tokenization if it affects how scores are read, and the rules that group tokens into labels. These elements are part of the decision model and must be versioned with the checkpoint.

**A broad phrase can be semantically correct but operationally wrong**: If the requested target is a specific fastener and the prompt describes generic metal parts, boxes on related tools may match the language while violating the product category. Audit whether localization is correct before changing the text. Then compare narrower descriptions and controlled near negatives on validation. A higher text-region score alone cannot decide a category boundary that the task specification has not defined.

**Blocking errors**: Concluding that an open-vocabulary model knows the business taxonomy without supervision.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; Diagnosis proposed by the project from the textual conditioning; [Grounding DINO, §§3.2 – 3.3](https://arxiv.org/abs/2303.05499); [official Grounding DINO code, commit 856dde2, util/inference.py L53–L97: box and text thresholds](https://github.com/IDEA-Research/GroundingDINO/blob/856dde20aee659246248e20734ef9ba5214f5e44/groundingdino/util/inference.py#L53-L97); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-OPENVOC-003 provenance::agent pole::A pole::D
END
