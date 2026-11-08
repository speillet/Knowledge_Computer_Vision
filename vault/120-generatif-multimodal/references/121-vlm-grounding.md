---
id: CV-VLM
type: comparaison
domaine: d12
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-CLIP", "CV-VIDEO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VLMs, grounding and the vision–action boundary

## Problem, data and assumptions

Connect visual observations and language for questions, descriptions or structured outputs. Distinguish between image – text embedding, generative VLM, and action-producing VLA. The robotic control remains outside the scope of this preparation.

## Prerequisites and competencies

**Required prerequisites**: [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md); [CV-VIDEO](../../100-mouvement-video/references/102-points-actions-video.md). **Target competencies**: explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

BLIP-2 connects visual encoder and LLM via Q-Former; LLaVA combines connector and tuning instruction according to version; Flamingo processes interwoven multimodal inputs. A textual response can rely on the language without being properly anchored in the image. Florence-2 is a multitasking input to deepen, not an interchangeable universal output.

## Mathematics, conventions and units

The input is converted into visual and textual tokens/features depending on the method; their number, resolution, and context condition the cost. Generative training optimizes an objective on the tokens; decoding then produces a sequence according to a research or sampling strategy. None of these objectives constitute proof of visual truth. A text likelihood score does not replace a box or mask annotation.

## Parameters and properties

Checkpoint, image processor, prompt, output format, possible tools and access to the future. RT-2/OpenVLA/π0 introduce an action interface; knowing this interface is not worth validating a robotic policy.

## Cost and implementation

Encoding, visual tokens, video context and decoding have separate costs. No model executed or hardware availability assumed. Variants should be named when quoting a specific connector or property.

## Evaluation and controlled variation

Baseline: pipeline detection/tracking/rules versus VLM, with same annotated tasks and reserved data. Vary quickly and negative controlled; measure hallucinations, omissions, location and cost, not just fluidity.

## Failure modes and diagnosis

Absent object description: inspect resolution, prompt, out-of-distribution and reference; test negative images and alternative formulations without selecting the best result on test.

## Alternatives and applications

An explicit pipeline can offer more controllable outputs for defined events; VLM can help with new descriptions/contexts under evaluation. Grounding must have its protocol.

## Guided reasoning and proposed checks

These constructed cases develop connector, visual anchoring and image dependency testing. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-VLM-001

**Question of work**: How do CLIP used for image–text comparison, a generative VLM and a VLA differ?

**Reference Response**: CLIP compares image-text representations; a VLM generates outputs conditioned by vision/language; a VLA produces an action interface according to its design.

**Define the interface**: Comparing embeddings is used to rank or search among candidates; generating text produces a conditioned sequence; producing actions engages another representation and another evaluation environment. An architecture can share bricks without these contracts becoming interchangeable.

**Constructed example**: “A part is present” may be a plausible description, but does not provide a validated box or a properly referenced robotic control. For an application, specify output format, validity time and expected reference, and then measure omissions and false assertions. If actions are studied, distinguish between knowledge of the interface and validation of a closed-loop policy. The course here covers perception and its limits; the move to command is not inferred from a convincing verbal response or a high generation score. The evidence must match what the system actually promises.

### Case linked to CV-VLM-004

**Question of work**: Track D — diagnosis: a VLM describes absent objects in industrial images. Which investigation leads to a verifiable correction?

**Reference Response**: Check image actually received, resolution/prompt, distribution, negatives and reference; classify hallucinations and omissions then test one intervention at a time.

**Discriminant Ablation**: Keep the image and reference labels, edit only the formulation on validation, and then compare to a structured visual string. Also test images without target object and variations in resolution. This helps distinguish mistransmitted information from a tendency to linguistically complement a familiar scene.

**Criterion of correction**: Seek a measured decrease in false assertions without silently increasing omissions. A cautionary note can change the style of responses without making their content more accurate. Keep a policy of refusal, entries actually processed and checkpoint to reproduce errors. Any improvement remains protocol related; no prompt here is a general guarantee to remove hallucinations on all new products.

**Documentary reference for this pass**: [BLIP-2](https://arxiv.org/html/2301.12597v3), §3, visual connector and drive. The other developments are in the [flashcards](../121-vlm-grounding.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-VLM-001

**Situation**: How do CLIP used for image–text comparison, a generative VLM and a VLA differ?

**Optimized quantity**: an autoregressive generation models $p(y\mid I,q)=\prod_kp(y_k\mid y_{<k},I,q)$ for a $I$ image, a $q$ question and $y_k$ tokens. A probable sequence under this model is not automatically a true visual proposition. A syntactically valid JSON format can also contain a false box or object. The evaluation must therefore separate respect for the schema, accuracy of the facts and spatial or temporal anchoring. For an action output, add more method-specific units, coordinate frames, and execution contract; the plausibility of tokens does not validate a physical action.

### CV-VLM-002

**Situation**: Which problem does BLIP-2's Q-Former address in its original architecture?

**Goulot of representation**: learned queries query the features of the visual encoder by cross attention and produce an intermediate representation for the language model. They are not the free questions typed by the user. Limiting the number of vectors transmitted can reduce the cost of the interface while constraining the information available on small details. A frozen encoder and a frozen LLM can be linked by learned parameters without updating all their weights. The mechanism of the bridge and the learning protocol must therefore be described separately from the final behavior, which remains to be measured on the visual observations of the task.

### CV-VLM-003

**Situation**: Track D — design: index hours of video for event retrieval. How should a general-purpose VLM be compared with detection, tracking and rules?

**Cost of indexing**: with a video of duration $T$ and a sampling step $\Delta$, the number of frames retained is of the order of $T/\Delta$. The cost includes decoding, visual encoding, building windows, and generating or indexing outputs. Reducing this number can make short events disappear; increasing the context can add cost and delay without restoring a frame never observed. A hybrid pipeline can first propose intervals and then describe them, but it is necessary to measure the recall of this preselection: an excluded event will never reach the VLM. Evaluate each step and the final index on the same reserved events.

### CV-VLM-004

**Situation**: Track D — diagnosis: a VLM describes absent objects in industrial images. Which investigation leads to a verifiable correction?

**Anchor tests built**: use a positive image, a comparable negative image and, if feasible, a variation where only the target object changes. Check if the assertions actually follow this variation and if the correction increases the refusal rather than the accuracy. A decrease in the number of false assertions obtained by never responding is not the same result as better recognition; report coverage of responses and risk of error among responses issued. These tests must respect the distribution of the images, because an artificial masking can introduce an artifact. Outputs must remain connected to the exact version of the input and prompt used.

**Passages consulted for these developments**: [Li et al., BLIP-2](https://arxiv.org/html/2301.12597v2), §3.1, learned queries and cross attention; probabilistic models and built tests.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-VLM-001 — An action interface needs a state and timing contract

A VLA output can encode commands in a learned action representation, but the controller still needs units, reference frames, frequency and validity limits. A plausible language description does not establish an executable command, and a valid command schema does not prove that the visual state was estimated correctly. Compare models at their declared outputs and evaluate any conversion into physical actions separately. No robotic execution is established by these notes.

### CV-VLM-002 — Learned queries are a representation bottleneck

Q-Former query vectors are learned model parameters that attend to visual features; they are not a list of user questions whose answers independently verify image facts. The representation passed to the language model is limited by the visual encoder and connector. If small text is not resolved at that input resolution, fluent downstream generation cannot guarantee its recovery. Evaluate sensitivity to crop and resolution using known text or object details.

### CV-VLM-003 — Retrieval needs both event coverage and verification

A proposed video index can use a cheap first stage to retrieve candidate intervals and a more expensive model to verify them. Measure missed events introduced by the retrieval stage separately from false descriptions introduced by verification. Include short events and temporally similar negatives, and account for sampling, decoding and prompt cost. An accurate verifier cannot recover an event never presented in its sampled candidate frames.

### CV-VLM-004 — A counterfactual image pair can test visual dependence

Construct paired inputs differing in one controlled object while keeping prompt and scene context fixed. Check whether the answer changes with the image and whether absence is acknowledged on a negative image. Preserve the actual decoded inputs and generation settings. This proposed diagnostic helps identify context-driven responses, but passing a few pairs does not certify grounding across the deployment distribution or eliminate hallucinations globally.

Consulted foundations: [BLIP-2](https://arxiv.org/html/2301.12597v2): §3 Q-Former learned queries and frozen encoder/language-model bridge; [LLaVA](https://arxiv.org/html/2304.08485v2): §4 visual instruction tuning and limitations.

## Sources and flashcards

- [Florence-2, summary](https://arxiv.org/abs/2311.06242): Prompt representation for multiple tasks.
- [RT-2, summary and fig. 1](https://arxiv.org/abs/2307.15818) and [π, summary](https://arxiv.org/abs/2410.24164): vision – language – action interface, without robotic validation of the project.

- [BLIP-2, architecture](https://arxiv.org/abs/2301.12597).
- [LLaVA original](https://arxiv.org/abs/2304.08485).
- [Flamingo](https://arxiv.org/abs/2204.14198).
- [OpenVLA, interface actions](https://openvla.github.io/).
- [Related flashcards](../121-vlm-grounding.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
