# Flashcards — CLIP, SigLIP and text-based recognition

reference note: [[70-reconnaissance-representations/references/72-clip-siglip|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-CLIP-001

Objective: interpret the zero-shot CLIP. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-001
Question: How can CLIP classify an image using classes described in text?
Reponse: **Expected answer**: Encode image and descriptions, compare in an aligned space and then apply a decision rule on these candidates.

**Further explanation**: Quality depends on prompts, vocabulary and domain; not training a new head does not mean making no assumptions.

**Decision mechanism**: Each class description defines a text candidate in the shared space. The image is compared to these candidates, then a rule chooses a candidate or rejects all of them. The vocabulary is therefore part of the definition of the classifier, even without training an additional head.

**Constructed example**: Proposing only "good part" and "scratched part" forces a comparison between these two descriptions, even if the image shows another part or an empty background. The best candidate can be the least bad. Test alternative descriptions on validation, keep negatives and define a measured rejection policy. Image–text similarity can be used for retrieval or classification by description; it does not by itself provide a generated explanation or the precise location of a scratch. The interface and metric must match the requested output.

**Decision and cost**: For normalized embeddings $v$ and $t_j$, compute $s_j=\tau v^Tt_j$ and then choose a candidate according to the fixed rule. Several prompts for the same class can be encoded and then combined in text space, with explicit renormalization; averaging embeddings and averaging probabilities are two different operations. Fixed texts can be pre-encoded, while each image still has to pass through the encoder. The number of candidates then enters the comparisons. Keeping the version of the vocabulary with the model makes results reproducible, because changing the formulations actually changes the classifier.

**The vocabulary defines the available decision**: For an image of a wrench, a candidate set containing only cat and dog still produces a winner under argmax. Adding wrench changes the decision space without changing the image embedding. A project classifier therefore needs an explicit candidate vocabulary and a policy for none-of-the-above or uncertain cases, validated on representative negatives. Text/image similarity alone does not establish that every input belongs to one candidate class.

**Blocking errors**: Presenting CLIP as a standalone caption generator.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]] ; [Radford et al., CLIP, §3.1.2 zero-shot classifier and §3.1.4 prompts and ensembling](https://arxiv.org/html/2103.00020v1) ; [Radford et al., CLIP, §6, limitations](https://arxiv.org/abs/2103.00020). Constructed cases: project deduction.
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-CLIP-001 provenance::agent pole::A pole::D
END

## CV-CLIP-002

Objective: Reject a misleading probability. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-002
Question: Why does a CLIP softmax score of 0.95 over two labels not prove that the predicted object is present?
Reponse: **Expected answer**: It normalizes scores among these candidates; the set may contain no correct description and the model may be out of its domain.

**Further explanation**: Test rejections, new candidates and calibration on representative data.

**Reading the softmax**: Normalization shares a unit mass among the candidates provided. Removing a competitor or changing the temperature changes the values without adding any evidence from the image. A very high score may therefore only indicate that the other formulations receive even lower scores.

**Constructed test**: Keep the image and add a plausible description that was absent. Observe how the ranking and values change, then compare with an annotated reference. Also include images with no correct class and out-of-domain scenes. A rejection policy must be validated on these cases, at the product's operating point. Calibration refers to the agreement between scores and error frequencies under a given protocol; it does not follow from the scores summing to one. The interpretation must therefore remain relative to the candidate set and to the observed distribution.

**Algebraic counterexample**: For two logits $a,b$, $p_1=1/(1+e^{b-a})$. A difference $a-b=\log19\simeq2.94$ is enough to give $p_1=0.95$, regardless of the absolute values of the two logits. Adding the same constant to both changes nothing. If a third candidate receives a logit equal to $a$, the probability of the first becomes $19/(19+1+19)=19/39$, approximately 0.487, without any change in the image. This constructed case isolates the effect of the candidate set; it does not predict the values of a checkpoint. A robust rejection therefore requires a protocol that includes the absences and distributions actually encountered.

**Adding a candidate changes normalized confidence**: Constructed logits for two labels are $\log19$ and zero, yielding 0.95 for the first. Adding a third label with the same top logit changes that probability to $19/39\approx0.487$, although the first label's similarity to the image is unchanged. A threshold on candidate-softmax probability therefore depends on vocabulary composition. Validate confidence or rejection under the vocabulary changes the product actually permits.

**Blocking errors**: Interpreting any normalized score as the probability that the label is true.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]] ; [Radford et al., CLIP, §3.1.2, softmax over candidate texts with temperature](https://arxiv.org/html/2103.00020v1). Algebraic counterexample: project construction.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-CLIP-002 provenance::agent pole::A pole::D
END

## CV-CLIP-003

Objective: Distinguish contrastive objectives. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-003
Question: What is the central difference between CLIP's softmax objective and the SigLIP objective?
Reponse: **Expected answer**: SigLIP uses a sigmoid loss on individual pairs rather than a softmax normalization over the whole batch as in CLIP.

**Further explanation**: This change of objective does not by itself provide operational calibration; temperature, bias and data details matter.

**Reasoning about the objective**: A softmax normalization over the batch puts candidates in competition in the denominator. A per-pair sigmoid objective treats each pair's compatibility as a separate binary decision, with its own parameters and its balance of positives and negatives. This changes what the scores are trained to represent, without removing the role of the data.

**Effect on evaluation**: Compare models on the same images, texts, absent classes and rejection criteria, logging the checkpoint and preprocessing. A change of objective does not make an output value a reliable probability on an industrial line. A function bounded between zero and one can still be miscalibrated out of distribution: SigLIP's learned bias, initialized at $-10$, absorbs the training imbalance of one positive per image against all other pairs in the batch, so a raw sigmoid score reflects that training prior rather than the deployment prior. The flashcard asks to distinguish learning mechanisms; an empirical ranking of variants would require a protocol and additional measurements, rather than a conclusion drawn from the name of the loss alone.

**Loss formulas**: With positive pairs on the diagonal of a batch, one direction of CLIP uses $-\frac1n\sum_i\log[\exp(s_{ii})/\sum_j\exp(s_{ij})]$, complemented by the text→image direction. A per-pair sigmoid form writes $\log(1+\exp(-y_{ij}s_{ij}))$ with $y_{ij}\in\{-1,+1\}$, followed by an aggregation specified by the method. Temperature and bias enter the definition of the logits; normalization conventions matter when comparing gradients and loss values. The central difference is the coupling of candidates in the denominator, not a probabilistic certification of scores after transfer.

**Pairwise loss does not imply calibrated deployment probabilities**: A sigmoid objective removes the shared softmax normalization across training pairs, but its score distribution still depends on training pair balance, bias/temperature and data distribution. Do not infer that an arbitrary sigmoid similarity is a calibrated probability that a class is physically present. Compare objectives through the task's fixed candidate and decision protocol, with held-out calibration evidence where probabilities are required.

**Blocking errors**: Deducing a reliable probability from the word sigmoid alone.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]] ; [Radford et al., CLIP, §2.3, symmetric cross-entropy](https://arxiv.org/html/2103.00020v1) ; [Zhai et al., SigLIP, §3.2 and Algorithm 1, sigmoid loss, temperature and bias](https://arxiv.org/abs/2303.15343). Calibration reasoning: project deduction.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-CLIP-003 provenance::agent pole::A pole::D
END

## CV-CLIP-004

Objective: test the sensitivity to the text. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-004
Question: How can an image–text classifier be tested without tuning prompts on the final test set?
Reponse: **Expected answer**: Create validation variants, freeze prompts and vocabulary, and then measure errors and rejections on a separate test set split by scene or domain.

**Further explanation**: Keep negatives and cases with no correct class; measure sensitivity to formulations without afterwards selecting the best test score.

**Why prompts are parameters**: Choosing a formulation by its score on the test set indirectly uses the test labels to set the system. Even without a gradient, this selection can overfit the decision to the examples that are supposed to provide an independent measurement.

**Proposed protocol**: Define a set of formulations and a combination rule on validation, freeze the vocabulary and thresholds, and open the final test only once these choices are frozen. Separate scenes or domains according to future use and document missing categories. Report errors and sensitivity to formulations without keeping only favorable cases. For a new iteration after failure analysis, prepare another independent evaluation. Good transfer practice thus keeps exploring the model separate from estimating its generalization, even when the tool is called zero-shot.

**Measurable sensitivity**: For each held-out image, keep the winning label, its margin over the second candidate and the decision changes between predefined formulations. Report the disagreement rate by class and domain, in addition to the final accuracy. An average over several prompts must be fixed before the test and its cost included in the protocol. Also keep images of the same object or sequence in the same split: several very similar views can make validation too favorable. These measures turn an impression of robustness to wording into an observable property, without selecting after the fact only the formulation that succeeds on each example.

**Prompt selection is part of model selection**: Trying many prompts and retaining the one with the best final test score leaks information from the evaluation set even if backbone weights never change. Keep prompt families, class vocabulary, ensembling and rejection thresholds within validation, then freeze them together. A proposed report includes per-class errors, unsupported-class inputs and prompt disagreement. It should also record whether the test images or near duplicates influenced any earlier selection step.

**Blocking errors**: Choosing the prompts from the final test results.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]] ; [Radford et al., CLIP, §3.1.4 prompt engineering, §5 near-duplicates, §6 validation-set use](https://arxiv.org/html/2103.00020v1). Validation protocol: project proposal.
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-CLIP-004 provenance::agent pole::A pole::D
END
