---
id: CV-CLIP
type: methode
domaine: d07
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-REPRESENTATIONS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# CLIP, SigLIP and text-based recognition

## Problem, data and assumptions

Link images and descriptions in a common space for retrieval or classification with vocabulary defined at the time of use. Inputs: images, text and preprocessing of the model; output: similarities or decisions under protocol. A contrast encoder alone does not generate a textual explanation.

## Prerequisites and competencies

**Required prerequisites**: [CV-REPRESENTATIONS](71-representations-transfert.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

CLIP brings the positive pairs closer together and compares the candidates by a contrasting goal. SigLIP uses a sigmoid lens in pairs with temperature/learned bias. The zero-shot constructs class descriptions and compares them to images.

## Mathematics, conventions and units

A similarity can write $s_{ij}=\tau\langle v_i/\|v_i\|,t_j/\|t_j\|\rangle$, inverse temperature $\tau$ according to convention. The softmax on a set of candidates is relative to this set. Adding a candidate changes the normalized values; these are not proof of calibrated truth probability.

## Parameters and properties

Version/checkpoint, prompts, languages, set of labels, resolution and standardization. Test synonyms and difficult negatives. Sigmoid also does not guarantee out-of-distribution calibration.

## Cost and implementation

Encode/index texts can be depreciated; images, vocabulary size, and search for neighbors come at a cost. No model executed; paper results are not valid on the target domain.

## Evaluation and controlled variation

Baseline: Closed classifier on known categories facing text classification. Vary prompts and vocabulary separately; measure errors, rejects and unrepresented classes with reference labels.

## Failure modes and diagnosis

An absent object receives a high score: check candidates, description bias and out-of-distribution; plan for a measured rejection decision, without inventing a universal threshold.

## Alternatives and applications

Closed classification if stable taxonomy and sufficient data; open-vocabulary for another compromise. Retrieval, grounding and text generation require separate outputs and evaluations.

## Guided reasoning and proposed checks

These constructed cases develop image-text contrast, candidates and domain offset. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-CLIP-001

**Question of work**: How can CLIP classify an image using classes described in text?

**Reference Response**: Encode image and descriptions, compare in an aligned space and then apply a decision rule on these candidates.

**Decision-making mechanism**: Each class description defines a textual candidate in the shared space. The image is compared to these candidates, and then a rule chooses or rejects a proposal. Vocabulary is therefore a part of the definition of the classifier, even without training an additional head.

**Constructed example**: proposing only "correct piece" and "striped piece" forces a comparison between these formulations, even if the image shows another piece or an empty background. The best candidate can be the least bad. Test alternative descriptions on validation, keep negatives and define a measured rejection policy. Image-text similarity can be used for research or classification by description; it does not by itself provide a generated explanation or the precise location of a scratch. The interface and metric must match the requested output.

### Case linked to CV-CLIP-004

**Question of work**: How can an image–text classifier be tested without tuning prompts on the final test set?

**Reference Response**: Create validation variants, freeze prompts and vocabulary, and then measure errors and rejections on separate test by scene/domain.

**Why prompts are parameters**: choosing a formulation based on its score on the test indirectly uses its labels to set the system. Even without a gradient, this selection can over-adapt the decision to the examples that are supposed to provide an independent measure.

**Proposed Protocol**: define a set of formulations and a combination rule on validation, keep the vocabulary and thresholds, and then open the final test once the choices are frozen. Separate scenes or domains according to future use and document missing categories. Report errors and sensitivity to formulations without keeping only favorable cases. For a new iteration after failure analysis, prepare another independent assessment. A good transfer practice thus retains a distinction between exploring the model and estimating its generalization, even when the tool is qualified as zero-shot.

**Documentary reference for this pass**: [CLIP](https://arxiv.org/html/2103.00020v1), §§2 – 3, learning and zero-shot evaluation. The other developments are in the [flashcards](../72-clip-siglip.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-CLIP-001

**Situation**: How can CLIP classify an image using classes described in text?

**Decision and cost**: For standard embeddings $v$ and $t_j$, calculate $s_j=\tau v^Tt_j$ and then choose a candidate according to the fixed rule. A set of prompts of the same class can be encoded and then combined in text space, with explicit normalization; averaging embeddings and averaging probabilities are two different operations. Fixed texts can be pre-encoded, while each image still has to pass through the encoder. The number of candidates is then included in the comparisons. Keeping the version of this vocabulary with the model makes the results reproducible, because changing the formulations actually changes the classifier used.

### CV-CLIP-002

**Situation**: Why does a CLIP softmax score of 0.95 over two labels not prove that the predicted object is present?

**Algebraic counter-example**: for two logs $a,b$, $p_1=1/(1+e^{b-a})$. A difference $a-b=\log19\simeq2,94$ is enough to give $p_1=0,95$, regardless of the absolute value of the two logs. Adding the same constant to the two does not change anything. If a third candidate receives a logit equal to $a$, the probability of the first becomes $19/(19+1+19)=19/39$, approximately 0,487, without any change in the image. This built case isolates the effect of the candidate set; it does not predict the values of a checkpoint. A robust rejection therefore requires a protocol including the absences and distributions actually encountered.

### CV-CLIP-003

**Situation**: What is the central difference between CLIP's softmax objective and the SigLIP objective?

**Loss formulas**: with positive pairs on the diagonal of a lot, a direction of CLIP uses $-\frac1n\sum_i\log[\exp(s_{ii})/\sum_j\exp(s_{ij})]$, supplemented by the direction text→image. A sigmoid form per pair writes $\log(1+\exp(-y_{ij}s_{ij}))$ with $y_{ij}\in\{-1,+1\}$, then an aggregation according to the method. Temperature and bias participate in the definition of logits; normalization conventions count for the comparison of gradients and loss values. The central difference is the coupling of candidates in the denominator, not a probabilistic certification of scores after transfer.

### CV-CLIP-004

**Situation**: How can an image–text classifier be tested without tuning prompts on the final test set?

**Measurable sensitivity**: For each reserved image, keep the winning label, its margin with the second candidate and the decision changes between predefined formulations. Report the rate of disagreement by class and field, in addition to the final accuracy. An average of several prompts must be set before the test and its costs incorporated into the protocol. Separate also the images of the same object or sequence between games: several very similar views can make the validation too favorable. These measures transform an impression of robustness to words into observable property, without selecting only the formulation that succeeds on each example after the fact.

**Passages consulted for these developments**: [Radford et al., CLIP](https://arxiv.org/html/2103.00020v1), §2.3, symmetrical loss; §3.1, text classification; algebraic project counterexamples; [Zhai et al., SigLIP](https://arxiv.org/pdf/2303.15343), summary, objective per pair; HTML v4 version inaccessible, use of PDF.

## Sources and flashcards

- [CLIP, §§2.3,3 and limits §6](https://arxiv.org/abs/2103.00020).
- [SigLIP, §3 and Algorithm1](https://arxiv.org/abs/2303.15343).
- [Related flashcards](../72-clip-siglip.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
