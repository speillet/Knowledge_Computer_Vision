---
id: CV-OPENVOC
type: methode
domaine: d08
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-CLIP", "CV-DETECTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Open-vocabulary detection and grounding

## Problem, data and assumptions

Locate regions related to an evolving text or vocabulary. Distinguish image – text classification, open-vocabulary detection and grounding repository. Inputs: image plus candidates/prompt; outputs: boxes or regions with scores according to the model.

## Prerequisites and competencies

**Required prerequisites**: [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md); [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Methods such as OWL-ViT and Grounding DINO link visual representations and language to produce regions. Textual vocabulary does not replace an annotation protocol, negatives, or a rejection policy.

## Mathematics, conventions and units

A region – text similarity and a threshold lead to a sub-set of candidates. The normalization of scores depends on the model; it does not certify presence, calibration or absence of object outside vocabulary.

## Parameters and properties

Version, prompt, tokenization, resolution and thresholds. Testing synonyms, close objects, negatives, and absent classes; “open” does not mean unlimited taxonomy understood perfectly.

## Cost and implementation

Text/image encoding, number of candidates, and postprocessing count. No model executed and no monthly update gain announced as measured.

## Evaluation and controlled variation

Baseline: Closed detector retrained versus text approach on new products separated from the setting. Measure AP/recall, rejects and cost of updates; freeze formulations before testing.

## Failure modes and diagnosis

False positives on broad descriptions: analyze text ambiguity and taxonomy. A high score is not proof of exact grounding.

## Alternatives and applications

Combine known detector, embeddings and targeted annotations according to novelty frequency and error tolerance. A VLM generation is not a box-rated detection.

## Guided reasoning and proposed checks

These constructed cases develop variable vocabulary, protocol and localized output. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-OPENVOC-001

**Question of work**: Why can CLIP classification of an image not directly replace an open-vocabulary detector?

**Reference Response**: Image ranking is about the global image; detection must also locate instances with a suitable output protocol.

**Decomposition of the output**: A global image – text similarity may indicate that a content is compatible with a description. A detector must also propose positions and distinguish several occurrences, with their classes or relationships to the text. A score on the entire image does not determine these boxes or their number.

**Constructed example**: A scene with two cups and a plate may well match the “cup” text without providing the location of each cup. The detection assessment should check instances, coordinates, and objects that are missed, including when the prompt is missing from the image. A referential grounding can require yet another output, such as "the cup to the left of the plate". Define annotations, negatives, thresholds and metrics according to this contract. The language expands the interface of the candidates; it does not dispense with checking the spatial accuracy and confusions of the domain.

### Case linked to CV-OPENVOC-003

**Question of work**: A broad prompt produces boxes on related objects outside the target category. What should be tested?

**Reference Response**: Class definition, formulations/negatives and region score on validation; inspect confusions and annotations.

**Why the text may be at issue**: A general description can correspond to several visual categories that industrial taxonomy separates. A model can therefore return a region plausible for current language but incorrect for need. A single threshold does not necessarily resolve this ambiguity.

**Survey built**: Record target and excluded classes, compare more accurate formulations and close negatives on validation, and then inspect regions and annotations. Separate lack of localization and confusion of vocabulary. Also assess the absence of a target, because choosing the best candidate does not prove its presence. A new formulation must be frozen before the final test. If the domain does not provide a visible discriminating index, a better prompt may be insufficient; the interface must then allow denial or verification rather than guaranteeing an exact category.

**Documentary reference for this pass**: [Grounding DINO](https://arxiv.org/html/2303.05499v4), open-set method and protocol. The other developments are in the [flashcards](../83-detection-open-vocabulary.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-OPENVOC-001

**Situation**: Why can CLIP classification of an image not directly replace an open-vocabulary detector?

**Where the text intervenes**: In Grounding DINO described by the cited article, textual representations can guide the selection of queries and participate in decoding regions. The interface is therefore not limited to classifying a global vector after the fact. For a map of outputs, check what each score represents: token, expression or aggregated category according to the implementation. Two occurrences of the same word in an image still require two distinct regions. A test built with an object, two objects and no object, with fixed prompt, allows to check cardinality and location without confusing the best linguistic compatibility with a certain presence.

### CV-OPENVOC-002

**Situation**: Track A — design: a product catalogue changes every month. How should a retrained closed-set detector be compared with an open-vocabulary detector?

**Time division of the test**: simulate several updates to the catalog: set to an initial version, freeze the system, then introduce reserved products and close negatives. Measure the annotation and maintenance gain per cycle, as well as errors on old and new objects. The cost of a textual method includes the definition of categories and the validation of prompts; that of the closed includes collection, training and new validation. If one product is visually indistinguishable from another in the available image, no formulation is sufficient to guarantee the distinction. This protocol evaluates a capacity for evolution, rather than a single favorable photograph of the catalog.

### CV-OPENVOC-003

**Situation**: A broad prompt produces boxes on related objects outside the target category. What should be tested?

**Separate vocabulary and location**: For each false positive, compare first the proposed region to the visible object, then the category of this object to the business definition. A correct box on a semantically neighboring object is a different problem than a box placed between multiple objects. Adding precise formulations can move scores from an entire distribution: re-evaluate recall and rejection, without assuming an invariant threshold to prompt. Record the exact expressions, their tokenization if it affects the interpretation of scores and the rules of grouping into labels. These elements are part of the decision-making model and must be versioned with the checkpoint.

**Passages consulted for these developments**: [Liu et al., Grounding DINO](https://arxiv.org/html/2303.05499v4), §3.2 – 3.3, text-guided selection and decoding; project testing.

## Sources and flashcards

- [OWL-ViT, method](https://arxiv.org/abs/2205.06230).
- [Grounding DINO, method](https://arxiv.org/abs/2303.05499).
- [Related flashcards](../83-detection-open-vocabulary.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
