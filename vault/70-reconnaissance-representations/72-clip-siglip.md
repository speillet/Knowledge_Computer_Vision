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

**Further explanation**: Quality depends on prompts, vocabulary and field; the absence of training of a new head does not imply the absence of hypotheses.

**Decision-making mechanism**: Each class description defines a textual candidate in the shared space. The image is compared to these candidates, and then a rule chooses or rejects a proposal. Vocabulary is therefore a part of the definition of the classifier, even without training an additional head.

**Constructed example**: proposing only "correct piece" and "striped piece" forces a comparison between these formulations, even if the image shows another piece or an empty background. The best candidate can be the least bad. Test alternative descriptions on validation, keep negatives and define a measured rejection policy. Image-text similarity can be used for research or classification by description; it does not by itself provide a generated explanation or the precise location of a scratch. The interface and metric must match the requested output.

**Decision and cost**: For standard embeddings $v$ and $t_j$, calculate $s_j=\tau v^Tt_j$ and then choose a candidate according to the fixed rule. A set of prompts of the same class can be encoded and then combined in text space, with explicit normalization; averaging embeddings and averaging probabilities are two different operations. Fixed texts can be pre-encoded, while each image still has to pass through the encoder. The number of candidates is then included in the comparisons. Keeping the version of this vocabulary with the model makes the results reproducible, because changing the formulations actually changes the classifier used.

**Blocking errors**: Present CLIP as a standalone legend generator.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]]; [CLIP, §§2.3,3 and limits §6](https://arxiv.org/abs/2103.00020); [SigLIP, §3 and Algorithm1](https://arxiv.org/abs/2303.15343); [Radford et al., CLIP, §2.3, symmetrical loss; §3.1, text classification; algebraic project counterexamples](https://arxiv.org/html/2103.00020v1); [Zhai et al., SigLIP, summary, objective per pair; HTML v4 version inaccessible, use of PDF](https://arxiv.org/pdf/2303.15343), see the 2026-10-30.
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-CLIP-001 provenance::agent pole::A pole::D
END

## CV-CLIP-002

Objective: Reject a misleading probability. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-002
Question: Why does a CLIP softmax score of 0.95 over two labels not prove that the predicted object is present?
Reponse: **Expected answer**: It normalizes scores between these candidates; the set may not contain any good descriptions and the model may be out of domain.

**Further explanation**: Test rejections, new candidates and calibration on representative data.

**Reading the softmax**: Normalization shares a mass between the candidates provided. Removing a competitor or changing the temperature changes the values without adding any evidence in the image. A very high score can therefore only indicate that other formulations receive even lower scores.

**Example of test built**: preserve the image and add a previously absent plausible description. Observe how the ranking and values change, then compare to an annotated reference. Also include images without good class and out-of-domain scenes. A rejection policy must be validated on these cases, at the point of operation of the product. Calibration refers to the agreement between scores and error frequencies in a given protocol; it does not derive from the sum equal to one. The interpretation must therefore remain relative to all the candidates and to the distribution observed.

**Algebraic counter-example**: for two logs $a,b$, $p_1=1/(1+e^{b-a})$. A difference $a-b=\log19\simeq2,94$ is enough to give $p_1=0,95$, regardless of the absolute value of the two logs. Adding the same constant to the two does not change anything. If a third candidate receives a logit equal to $a$, the probability of the first becomes $19/(19+1+19)=19/39$, approximately 0,487, without any change in the image. This built case isolates the effect of the candidate set; it does not predict the values of a checkpoint. A robust rejection therefore requires a protocol including the absences and distributions actually encountered.

**Blocking errors**: Interpret any normalized score as a probability of truth.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]]; [CLIP, §§2.3,3 and limits §6](https://arxiv.org/abs/2103.00020); [SigLIP, §3 and Algorithm1](https://arxiv.org/abs/2303.15343); [Radford et al., CLIP, §2.3, symmetrical loss; §3.1, text classification; algebraic project counterexamples](https://arxiv.org/html/2103.00020v1); [Zhai et al., SigLIP, summary, objective per pair; HTML v4 version inaccessible, use of PDF](https://arxiv.org/pdf/2303.15343), see the 2026-10-30.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-CLIP-002 provenance::agent pole::A pole::D
END

## CV-CLIP-003

Objective: distinguer objectifs contrastifs. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-003
Question: What is the central difference between CLIP's softmax objective and the SigLIP objective?
Reponse: **Expected answer**: SigLIP uses a loss sigmoid on pairs rather than a global softmax normalization of the batch like CLIP.

**Further explanation**: This lens change does not automatically grant operational calibration; temperature, bias and data details count.

**Reasoning about the objective**: a softmax lot normalization puts candidates in competition in the denominator. A sigmoid lens per pair treats compatibility according to another learning construct, with its parameters and positives/negatives. This changes what the scores are trained to represent, without removing the role of the data.

**Impact of evaluation**: compare models on the same images, texts, absent classes and rejection criteria, by logging checkpoint and preprocessing. A change in objective does not mean that an output value is automatically a reliable probability on an industrial line. A function bounded between zero and one can still be miscalibrated out of distribution. The flashcard asks to distinguish between learning mechanisms; an empirical ranking of variants would require a protocol and additional measures, rather than a conclusion drawn from the name of the loss alone.

**Loss formulas**: with positive pairs on the diagonal of a lot, a direction of CLIP uses $-\frac1n\sum_i\log[\exp(s_{ii})/\sum_j\exp(s_{ij})]$, supplemented by the direction text→image. A sigmoid form per pair writes $\log(1+\exp(-y_{ij}s_{ij}))$ with $y_{ij}\in\{-1,+1\}$, then an aggregation according to the method. Temperature and bias participate in the definition of logits; normalization conventions count for the comparison of gradients and loss values. The central difference is the coupling of candidates in the denominator, not a probabilistic certification of scores after transfer.

**Blocking errors**: Deducing a reliable probability of the single word sigmoid.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]]; [CLIP, §§2.3,3 and limits §6](https://arxiv.org/abs/2103.00020); [SigLIP, §3 and Algorithm1](https://arxiv.org/abs/2303.15343); [Radford et al., CLIP, §2.3, symmetrical loss; §3.1, text classification; algebraic project counterexamples](https://arxiv.org/html/2103.00020v1); [Zhai et al., SigLIP, summary, objective per pair; HTML v4 version inaccessible, use of PDF](https://arxiv.org/pdf/2303.15343), see the 2026-10-30.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-CLIP-003 provenance::agent pole::A pole::D
END

## CV-CLIP-004

Objective: test the sensitivity to the text. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-CLIP-004
Question: How can an image–text classifier be tested without tuning prompts on the final test set?
Reponse: **Expected answer**: Create validation variants, freeze prompts and vocabulary, and then measure errors and rejections on separate test by scene/domain.

**Further explanation**: Keep negatives and cases without good class; measure sensitivity to formulations without subsequently selecting the best test score.

**Why prompts are parameters**: choosing a formulation based on its score on the test indirectly uses its labels to set the system. Even without a gradient, this selection can over-adapt the decision to the examples that are supposed to provide an independent measure.

**Proposed Protocol**: define a set of formulations and a combination rule on validation, keep the vocabulary and thresholds, and then open the final test once the choices are frozen. Separate scenes or domains according to future use and document missing categories. Report errors and sensitivity to formulations without keeping only favorable cases. For a new iteration after failure analysis, prepare another independent assessment. A good transfer practice thus retains a distinction between exploring the model and estimating its generalization, even when the tool is qualified as zero-shot.

**Measurable sensitivity**: For each reserved image, keep the winning label, its margin with the second candidate and the decision changes between predefined formulations. Report the rate of disagreement by class and field, in addition to the final accuracy. An average of several prompts must be set before the test and its costs incorporated into the protocol. Separate also the images of the same object or sequence between games: several very similar views can make the validation too favorable. These measures transform an impression of robustness to words into observable property, without selecting only the formulation that succeeds on each example after the fact.

**Blocking errors**: Choose the prompts based on the final test results.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Full reference]]; [Radford et al., CLIP, §§2.3, 3.1 and limits §6](https://arxiv.org/abs/2103.00020); validation protocol proposed by the project; [Radford et al., CLIP, §2.3, symmetrical loss; §3.1, text classification; algebraic project counterexamples](https://arxiv.org/html/2103.00020v1); [Zhai et al., SigLIP, summary, objective per pair; HTML v4 version inaccessible, use of PDF](https://arxiv.org/pdf/2303.15343), consult the 2026-10-30.
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-CLIP-004 provenance::agent pole::A pole::D
END
