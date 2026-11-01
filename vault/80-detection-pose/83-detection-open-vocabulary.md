# Flashcards — Open-vocabulary detection and grounding

reference note: [[80-detection-pose/references/83-detection-open-vocabulary|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-OPENVOC-001

Objective: separate the multimodal outputs. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-001
Question: Why can CLIP classification of an image not directly replace an open-vocabulary detector?
Reponse: **Expected answer**: Image ranking is about the global image; detection must also locate instances with a suitable output protocol.

**Further explanation**: An image can contain multiple objects and candidates; grounding, classification, and generation do not all share the same metrics.

**Decomposition of the output**: A global image – text similarity may indicate that a content is compatible with a description. A detector must also propose positions and distinguish several occurrences, with their classes or relationships to the text. A score on the entire image does not determine these boxes or their number.

**Constructed example**: A scene with two cups and a plate may well match the “cup” text without providing the location of each cup. The detection assessment should check instances, coordinates, and objects that are missed, including when the prompt is missing from the image. A referential grounding can require yet another output, such as "the cup to the left of the plate". Define annotations, negatives, thresholds and metrics according to this contract. The language expands the interface of the candidates; it does not dispense with checking the spatial accuracy and confusions of the domain.

**Where the text intervenes**: In Grounding DINO described by the cited article, textual representations can guide the selection of queries and participate in decoding regions. The interface is therefore not limited to classifying a global vector after the fact. For a map of outputs, check what each score represents: token, expression or aggregated category according to the implementation. Two occurrences of the same word in an image still require two distinct regions. A test built with an object, two objects and no object, with fixed prompt, allows to check cardinality and location without confusing the best linguistic compatibility with a certain presence.

**Blocking errors**: Take an image – text score for a properly localized box.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; [OWL-ViT, §3.1: adaptation to location](https://arxiv.org/abs/2205.06230); [Grounding DINO, §§3.2 – 3.3](https://arxiv.org/abs/2303.05499); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-OPENVOC-001 provenance::agent pole::A pole::D
END

## CV-OPENVOC-002

Objective: choose a system with a scalable catalog. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-002
Question: Track A — design: a product catalogue changes every month. How should a retrained closed-set detector be compared with an open-vocabulary detector?
Reponse: **Expected answer**: Define novelties, acceptable errors and annotation budget; compare the two on old / new products with negatives, fixed thresholds and maintenance cost.

**Further explanation**: Measure location, rejection, and latency; a hybrid approach may be warranted. The prompt alone does not guarantee the recognition of a novelty.

**Proposed action**: compare the cost of annotations and retraining to that of adjusting formulations, analyzing new false positives and maintaining vocabulary. A changing catalog may favor a textual interface, but a visually very specific category may remain difficult to describe or recognize without targeted data.

**Transfer test**: Reserve new products unknown to the setting, add close categories and targetless images, and then measure location and rejection at the useful point of operation. Also keep old products to detect regression. The choice can be hybrid, with a specialized detector for the frequent and another procedure for the novelties. The comparison should announce the availability of data and human interventions, rather than using a selected demonstration as proof of easy maintenance.

**Time division of the test**: simulate several updates to the catalog: set to an initial version, freeze the system, then introduce reserved products and close negatives. Measure the annotation and maintenance gain per cycle, as well as errors on old and new objects. The cost of a textual method includes the definition of categories and the validation of prompts; that of the closed includes collection, training and new validation. If one product is visually indistinguishable from another in the available image, no formulation is sufficient to guarantee the distinction. This protocol evaluates a capacity for evolution, rather than a single favorable photograph of the catalog.

**Blocking errors**: Choose on a favorable demonstration without absent classes or protocol.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; Project-designed case and protocol; Reference architectures: [OWL-ViT, §3](https://arxiv.org/abs/2205.06230) and [Grounding DINO, §3](https://arxiv.org/abs/2303.05499); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), see 2026-10-30.
Tags: cv::pilote cv::d08 famille::conception cv_id::CV-OPENVOC-002 provenance::agent pole::A pole::D cas_pole::A::conception
END

## CV-OPENVOC-003

Objective: Check the specificity of the text. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-OPENVOC-003
Question: A broad prompt produces boxes on related objects outside the target category. What should be tested?
Reponse: **Expected answer**: Class definition, formulations/negatives and region score on validation; inspect confusions and annotations.

**Further explanation**: Evaluate a rejection rather than assuming the threshold transferable to all descriptions.

**Why the text may be at issue**: A general description can correspond to several visual categories that industrial taxonomy separates. A model can therefore return a region plausible for current language but incorrect for need. A single threshold does not necessarily resolve this ambiguity.

**Survey built**: Record target and excluded classes, compare more accurate formulations and close negatives on validation, and then inspect regions and annotations. Separate lack of localization and confusion of vocabulary. Also assess the absence of a target, because choosing the best candidate does not prove its presence. A new formulation must be frozen before the final test. If the domain does not provide a visible discriminating index, a better prompt may be insufficient; the interface must then allow denial or verification rather than guaranteeing an exact category.

**Separate vocabulary and location**: For each false positive, compare first the proposed region to the visible object, then the category of this object to the business definition. A correct box on a semantically neighboring object is a different problem than a box placed between multiple objects. Adding precise formulations can move scores from an entire distribution: re-evaluate recall and rejection, without assuming an invariant threshold to prompt. Record the exact expressions, their tokenization if it affects the interpretation of scores and the rules of grouping into labels. These elements are part of the decision-making model and must be versioned with the checkpoint.

**Blocking errors**: Conclude that an open-vocabulary model knows the business taxonomy without supervision.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Full reference]]; Diagnosis proposed by the project from the textual packaging; [Grounding DINO, §§3.2 – 3.3](https://arxiv.org/abs/2303.05499); [Liu et al., Grounding DINO, §3.2 – 3.3, text-guided selection and decoding; project testing](https://arxiv.org/html/2303.05499v4), consulted the 2026-10-30.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-OPENVOC-003 provenance::agent pole::A pole::D
END
