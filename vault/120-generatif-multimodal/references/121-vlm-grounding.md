---
id: CV-VLM
type: comparaison
domaine: d12
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 8
prerequis: ["CV-CLIP", "CV-VIDEO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VLMs, grounding and the vision–action boundary

This comparison note separates three interfaces that are often confused: embedding
models that score image–text pairs, generative vision-language models (VLMs) that
produce text or structured tokens conditioned on images, and vision-language-action
models (VLAs) that output robot actions. It focuses on what each output can prove
about the image and how to test it. Robotic control itself is out of scope.

## Problem and data contract

| Interface | Example | Input | Output | What the output can support |
| --- | --- | --- | --- | --- |
| Embedding | CLIP | Image; candidate texts | Cosine similarity per pair | Ranking or retrieval among candidates |
| Generative VLM | BLIP-2, LLaVA, Flamingo | Image(s) or video frames; prompt | Token sequence | A claim to verify; not a measurement |
| Structured VLM | Florence-2 | Image; task prompt | Text with location tokens | Boxes, quadrilaterals or polygons in quantized image coordinates |
| VLA | RT-2, OpenVLA, $\pi_0$ | Image(s), instruction, sometimes robot state | Discrete action tokens or continuous action chunks | An action in a normalized robot action space |

**Data contract.** Every model resizes or tiles the image to its encoder's input:
CLIP ViT-L/14 sees $224\times224$ pixels as $16\times16$ patches, Florence-2 was
pre-trained at $384\times384$ then tuned at $768\times768$ [Florence-2, §6.1]. A box
emitted as text is expressed in the coordinates of that processed image, quantized
into 1,000 bins per axis for Florence-2 [§3], and must be mapped back to the original
frame. For video, a model sees sampled frames: Flamingo samples at 1 frame/s during
training and encodes frames independently before adding learned temporal embeddings
[Flamingo, §2.1]. For actions, the units and ranges are those of the training robots'
normalized action space.

**Grounding, as used here.** A claim is grounded when the visual input supports it
and, if the claim is spatial or temporal, when its box, mask or interval matches an
annotation under a stated overlap rule (project definition; overlap metrics are in
[CV-IOU-AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md)).

**Pipeline role.** Open-vocabulary description, visual question answering in an
inspection report, candidate generation for video retrieval, and annotation
assistance. A VLM does not replace a detector whose recall and precision are measured
on the target defects.

## Intuition

The connector decides what the language model can see.

- **BLIP-2** keeps the image encoder and the LLM frozen and trains a Q-Former: 32
  learned queries of dimension 768 cross-attend to the image features and are the
  only path to the LLM, an information bottleneck trained to keep text-relevant
  content [BLIP-2, §3.1, §3.3].
- **LLaVA** projects every grid feature of a CLIP ViT-L/14 encoder into the LLM's
  word-embedding space with a trainable matrix [LLaVA, §4.1, eq. 1].
- **Flamingo** compresses each image or video into 64 visual tokens with a Perceiver
  Resampler and inserts gated cross-attention layers between frozen LM layers
  [Flamingo, §2.1–2.2].
- **Florence-2** uses one sequence-to-sequence model for captioning, detection,
  grounding and segmentation, writing regions as location tokens [Florence-2, §3].

Why answers can be fluent and wrong: the language model has a strong prior on what
usually co-occurs. LLaVA's authors report that it answered "yes" when asked whether
strawberry-flavoured yogurt was present in a fridge containing yogurt and
strawberries, and describe the model as sometimes perceiving the image "as a bag of
patches" [LLaVA, §5.1, Limitations]. Object-hallucination studies measure this
effect: CHAIR compares captioning errors with a text-only language model's
predictions [CHAIR, §2.3, §3.3], and POPE probes absent objects that frequently
co-occur with the present ones [POPE, §5.1].

## Prerequisites and competencies

**Required prerequisites**: [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md);
[CV-VIDEO](../../100-mouvement-video/references/102-points-actions-video.md). Useful:
[CV-OPENVOC](../../80-detection-pose/references/83-detection-open-vocabulary.md) for
box-level grounding by detectors, [CV-SAM](../../90-segmentation/references/94-sam-sam2.md)
for prompted masks, [CV-IOU-AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md)
for overlap metrics. **Target competencies**: explain the mechanism, compare under
constraints, interpret a measurement and diagnose a failure. Not all variants
mentioned are detailed.

## Assumptions, observability and degenerate cases

- **Resolution.** The detail must survive resizing into the encoder's patches; a
  small defect in a large image can occupy a fraction of one patch (example A).
- **Bottleneck capacity.** A fixed number of visual tokens (32 for BLIP-2, 64 for
  Flamingo) must carry every detail the question needs.
- **Domain.** Pre-training on web image–text pairs gives no guarantee on industrial
  close-ups, thermal or X-ray images.
- **Temporal coverage.** Events shorter than the sampling step can fall between
  samples (example B); no model recovers an unsampled frame.
- **Fixed prompt and decoding.** Results depend on wording and decoding settings;
  POPE was designed partly because caption-based hallucination scores were sensitive
  to instructions and caption length [POPE, §5.1].
- **Action space (VLA).** Actions are defined relative to the training robots'
  embodiment, normalization and control rate.

Degenerate cases: questions about absent objects (the model may answer "yes" by
prior), counting beyond a few instances, small text, and answers that are
syntactically valid but refer to coordinates of the resized image.

## Procedure

```text
1. Output contract   : text claim, structured box, interval, or action; units and frame
2. Interface choice  : embedding scoring | generative VLM | structured VLM | VLA
3. Preprocessing     : resolution, tiling or crop; frame sampling step for video
4. Fixed inference   : checkpoint, prompt template, decoding (greedy, beam, temperature)
5. Grounding tests   : present/absent probes with matched negatives; box or interval overlap
6. Baseline          : explicit pipeline (detector, tracker, rules) on the same annotations
7. Report            : accuracy and grounding metrics, yes-ratio, coverage, latency, cost
```

Purpose. Step 1 decides which evidence is acceptable: a sentence cannot be scored
with IoU, and a box cannot be validated by its fluency. Step 3 often explains small-
object failures before any model change. Step 4 freezes the factors that move
hallucination rates. Step 5 separates "said something present" from "said something
true". Step 6 tells whether the VLM adds value over a controllable pipeline.

## Mathematics, conventions and units

**Contrastive embedding (CLIP).** For a batch of $N$ image–text pairs, CLIP maximizes
the cosine similarity of the $N$ true pairs and minimizes it for the $N^2-N$ others,
with a symmetric cross-entropy over the similarity matrix [CLIP, §2.3]. Its output is
a similarity score, meaningful only relative to the candidate set.

**Autoregressive generation.** LLaVA trains on
$p(\mathbf X_a\mid\mathbf X_v,\mathbf X_{\text{instruct}})=\prod_{i=1}^{L}p_\theta(x_i\mid\mathbf X_v,\mathbf X_{\text{instruct},<i},\mathbf X_{a,<i})$,
where $\mathbf X_v$ is the image, $\mathbf X_{\text{instruct}}$ the instruction and
$x_i$ the answer tokens [LLaVA, eq. 3]. The visual tokens are
$\mathbf H_v=\mathbf W\mathbf Z_v$ with $\mathbf Z_v=g(\mathbf X_v)$ the CLIP grid
features [eq. 1]. Stage 1 trains only $\mathbf W$ on 595K filtered image–caption
pairs; stage 2 trains $\mathbf W$ and the LLM with the image encoder frozen [§4.2].
A high likelihood measures agreement with the training distribution of text, not the
truth of each visual claim.

**BLIP-2 bottleneck.** The query output $Z$ is $32\times768$, much smaller than the
$257\times1024$ ViT-L/14 features; the queries are trained with image–text
contrastive, image-grounded generation and image–text matching objectives, then a
fully connected layer projects $Z$ into the LLM's embedding dimension as soft visual
prompts [§3.1–3.3].

The three stage-1 objectives share the queries and differ by their self-attention
mask [§3.2]. Contrastive learning uses a unimodal mask (queries and text cannot see each
other; the image–text similarity is the highest of the 32 query–text similarities);
image-grounded generation uses a multimodal causal mask in which text tokens attend to
all queries and to earlier text, while the queries cannot see the text, so "the
information required for generating the text must be first extracted by the queries";
matching uses a bidirectional mask and averages 32 per-query logits. Stage 2 uses the
language-modeling loss for decoder LLMs (OPT) and a prefix language-modeling loss for
encoder–decoder LLMs (FlanT5) [§3.3]. Without stage 1, the Q-Former bridges the gap by
generative learning alone, "similar to the Perceiver Resampler in Flamingo"; zero-shot
VQA is substantially lower, and OPT "suffers from catastrophic forgetting where
performance drastically degrades as training proceeds" [§4.1, Fig. 5]. *Size check
(constructed, recomputed by the 2026-11-16 check script; CV-VLM-002):* the LLM receives
32 prefix tokens whatever the image, against 256 for a per-patch projection of the same
ViT-L/14 at 224 px.

**Flamingo gating.** Each new cross-attention layer's output is multiplied by
$\tanh(\alpha)$, with a layer-specific scalar $\alpha$ initialized to 0, so the
conditioned model starts exactly as the frozen LM [§2.2]; at a text token, the model
cross-attends only to the visual tokens of the image that appeared just before it
[§2.3].

**Location and action tokens.** Florence-2 represents a box as four location tokens
$(x_0,y_0,x_1,y_1)$, the top-left and bottom-right corners, each one of 1,000 bins
[§3]. RT-2 discretizes each continuous action dimension uniformly into 256 bins and
writes an action as 8 integers (termination, 6-DoF position and rotation
displacement, gripper extension) [RT-2, §3.2]. OpenVLA uses 256 bins spread between
the 1st and 99th percentiles of each dimension in the training data, to ignore
outliers [OpenVLA, §3.2]. $\pi_0$ instead predicts continuous chunks
$\mathbf A_t=[\mathbf a_t,\dots,\mathbf a_{t+H-1}]$ with $H=50$ using flow matching
and a separate action expert, and reports control at up to 50 Hz [$\pi_0$, §I, §IV].

**Hallucination metrics.** For captions over the 80 COCO object classes,
$\mathrm{CHAIR}_i$ is the fraction of mentioned objects that are hallucinated and
$\mathrm{CHAIR}_s$ the fraction of sentences that contain one [CHAIR, §2.1]. POPE asks
"Is there a/an ⟨object⟩ in the image?" for present objects and for absent objects
sampled randomly, by dataset frequency (popular) or by co-occurrence with present
objects (adversarial), with a 1:1 balance, and reports accuracy, precision, recall,
F1 and the proportion of "yes" answers [POPE, §5.1].

*Worked examples (constructed, recomputed by checks/121-vlm-grounding.py).*

- A. ViT-L/14 at 224 px gives $16\times16=256$ patches plus one class token, the 257
  of BLIP-2; the Q-Former output holds about 10.7 times fewer values. A 4000 px wide
  image resized to 224 px puts 250 original pixels in one patch width, so a 20 px
  defect covers 0.08 of a patch.
- B. Indexing 8 h of video at one frame per second gives 28,800 frames, or about
  7.4 million visual tokens at 256 tokens per frame. With a random sampling phase, an
  event of duration $d$ shorter than the step $\Delta$ is sampled with probability
  $d/\Delta$: 0.4 for a 2 s event at a 5 s step.
- C. With 1,000 location bins over a 4000 px wide image, a bin is 4 px and rounding
  costs up to 2 px per coordinate. With 256 action bins over a ±5 cm range, a bin is
  about 0.39 mm. A 50-action chunk at 50 Hz covers 1 s.
- D. With 1:1 balance, a model that always answers "yes" scores accuracy 0.5,
  precision 0.5, recall 1.0 and F1 0.667 when "yes" is the positive class; the yes
  ratio of 1.0 exposes it.

## Parameters and tuning

| Parameter | Effect | What to watch |
| --- | --- | --- |
| Input resolution, tiling or crop | Pixels per visual token; small-detail visibility | Latency grows with tokens; crops can remove context |
| Number of visual tokens (connector) | Information passed to the LLM | Fixed by the architecture for BLIP-2 and Flamingo |
| Prompt and output template | Answer style, refusal rate, parseability | Tune on validation, never on the test set |
| Decoding (greedy, beam, temperature) | Diversity and hallucination rate | In captioning, beam search generally reduced CHAIR, but for one model trained with a self-critical loss beam 5 gave 12.2 / 8.4 ($\mathrm{CHAIR}_s$ / $\mathrm{CHAIR}_i$) against 10.8 / 8.1 at beam 1 [CHAIR, §3.2] |
| Video sampling step $\Delta$ | Cost against coverage of short events | Example B |
| Checkpoint and version | Every behaviour above | Record exactly; results do not transfer across versions |
| Action discretization (VLA) | Action resolution and range | Bins set from training quantiles clip rarer large actions |

Tuning approach (project method): freeze the checkpoint and decoding; sweep
resolution or tiling first on a validation set with matched negatives; then adjust the
prompt template for parseability and refusal behaviour; report the yes ratio and the
coverage (fraction answered) next to accuracy at every step.

## Properties and limits of guarantees

- **No grounding guarantee.** Training objectives reward likely text; the LLaVA
  authors list hallucination as a limitation [LLaVA, Limitations]. Grounding is a
  property to measure on the target data.
- **Frozen components.** BLIP-2 and Flamingo keep the LLM frozen, and LLaVA keeps the
  vision encoder frozen [BLIP-2, §3; Flamingo, §2.2; LLaVA, §4.2]: the visual features
  are not adapted to a new domain unless the user fine-tunes them.
- **Structured outputs are quantized claims.** A location token box is a generated
  claim with 1,000-bin resolution in the processed image, not a calibrated detection
  with a score threshold.
- **Image-causal attention.** Flamingo attends directly to one image at a time but
  keeps earlier images through the LM's self-attention, which is how it generalizes
  to more images than seen in training [§2.3].
- **VLA outputs.** A valid action string or chunk is a command in a learned action
  space; its safety and success require closed-loop evaluation on the robot, which
  these notes do not establish.

## Cost and implementation

Cost drivers: image encoding (resolution and number of images or frames), the number
of visual tokens entering the LLM (all grid tokens for LLaVA, 32 for BLIP-2, 64 per
image for Flamingo), the LLM size, and the number of generated tokens. For video
indexing, cost is roughly proportional to $T/\Delta$ times the per-frame cost
(example B). Q-Former contains 188M parameters [BLIP-2, §3.1]; OpenVLA has 7B
parameters [OpenVLA, §1]. No model was executed for this note and no throughput is
claimed; library versions and APIs are not covered here.

## Evaluation and controlled variation

**Protocols.** Object hallucination: POPE (binary probes with random, popular and
adversarial negatives, F1 and yes ratio) and CHAIR (mentioned objects against COCO
annotations). Spatial grounding: IoU of generated boxes or masks against annotations.
Temporal grounding: overlap of retrieved intervals with annotated events, including
missed short events. Baseline: an explicit detection, tracking and rules pipeline on
the same annotations.

**Proposed baseline and controlled variation (not executed).**

- *Data*: held-out industrial images with per-object presence labels, boxes for
  defects, and matched negatives (same scene, defect absent).
- *Baseline*: the VLM with its default preprocessing, a fixed prompt and greedy
  decoding, scored with POPE-style probes (popular and adversarial negatives built
  from the defect vocabulary) and, if it emits boxes, IoU; the detector pipeline is
  scored on the same set.
- *Controlled variation*: crop or tile the region of interest so that the defect
  receives about four times more pixels per visual token; prompt, decoding and
  checkpoint unchanged.
- *Measurements*: F1, yes ratio, recall on small defects, box IoU, refusals, latency.
- *Reading*: a gain in recall on small defects with a stable yes ratio points to a
  resolution limit; a gain obtained only by more "yes" answers is not better
  grounding.

**Measurement limits.** Probe questions test presence, not attributes or relations;
CHAIR depends on a fixed object vocabulary and synonym lists; results depend on the
checkpoint, prompt and decoding and do not transfer across versions.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Describes an object that is absent | Co-occurrence prior of the language model | POPE-style probes with adversarial negatives; yes ratio | Matched-negative evaluation, refusal policy, explicit detector for critical objects |
| Misses small defects | Resolution lost in resizing or the token bottleneck | Same question on a crop of the region | Tiling or crops, higher-resolution model, dedicated detector |
| Answers change with wording | Prompt sensitivity | Paraphrase set on validation | Fixed template, report variance across paraphrases |
| Box offset or scaled | Coordinates of the resized or padded image; quantization | Map a known synthetic box through the pipeline | Correct the mapping; account for bin width (example C) |
| Short events missing from a video index | Sampling step longer than events | Recall per event duration | Smaller step on candidate intervals, motion-triggered sampling |
| Fewer hallucinations but fewer correct answers | Model or prompt refuses more | Coverage and error rate among answered items | Report both; tune refusal on validation |

## Alternatives and applications

- Prefer an explicit detection, tracking and rules pipeline when events are defined
  in advance and each decision must be inspectable and measured.
- Prefer an embedding model for retrieval and ranking among known candidates, and an
  open-vocabulary detector ([CV-OPENVOC](../../80-detection-pose/references/83-detection-open-vocabulary.md))
  when the output must be boxes with scores.
- Prefer a generative VLM for open-ended descriptions or questions not anticipated
  by the pipeline, with grounding measured; prefer a structured VLM when a single
  model must emit captions and regions.
- Treat VLAs as a different problem: a robot policy whose evaluation is closed-loop.

Industrial uses (project reasoning): draft inspection reports where every claim is
checked against a detector or a human; video retrieval in which a cheap detector
proposes intervals and a VLM describes them, with the recall of the first stage
measured; annotation assistance with human correction.

## Guided reasoning and proposed checks

These constructed cases develop the connector, visual grounding and tests of image dependence. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-VLM-001

**Working question**: How do CLIP used for image–text comparison, a generative VLM and a VLA differ?

**Reference answer**: CLIP compares image-text representations; a VLM generates outputs conditioned by vision/language; a VLA produces an action interface according to its design.

**Define the interface**: Comparing embeddings is used to rank or search among candidates; generating text produces a conditioned sequence; producing actions engages another representation and another evaluation environment. An architecture can share building blocks without these contracts becoming interchangeable.

**Constructed example**: “A part is present” may be a plausible description, but does not provide a validated box or a properly referenced robotic control. For an application, specify output format, validity time and expected reference, and then measure omissions and false assertions. If actions are studied, distinguish between knowledge of the interface and validation of a closed-loop policy. The course here covers perception and its limits; the move to control is not inferred from a convincing verbal response or a high generation score. The evidence must match what the system actually promises.

### Case linked to CV-VLM-004

**Working question**: Track D — diagnosis: a VLM describes absent objects in industrial images. Which investigation leads to a verifiable correction?

**Reference answer**: Check image actually received, resolution/prompt, distribution, negatives and reference; classify hallucinations and omissions then test one intervention at a time.

**Discriminating ablation**: Keep the image and reference labels, change only the wording on validation data, and then compare with a structured vision pipeline. Also test images without the target object and variations in resolution. This helps distinguish badly transmitted information from a tendency to complete a familiar scene linguistically.

**Correction criterion**: Seek a measured decrease in false assertions without silently increasing omissions. A cautionary instruction can change the style of responses without making their content more accurate. Keep the refusal policy, the inputs actually processed and the checkpoint, to reproduce errors. Any improvement remains tied to the protocol; no prompt here is a general guarantee of removing hallucinations on all new products.

**Source consulted for this pass**: [BLIP-2](https://arxiv.org/html/2301.12597v3), §3, visual connector and training. The remaining developments are in the [flashcards](../121-vlm-grounding.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-VLM-001

**Situation**: How do CLIP used for image–text comparison, a generative VLM and a VLA differ?

**Optimized quantity**: an autoregressive generator models $p(y\mid I,q)=\prod_kp(y_k\mid y_{<k},I,q)$ for an image $I$, a question $q$ and tokens $y_k$. A probable sequence under this model is not automatically a true visual proposition. A syntactically valid JSON format can also contain a false box or object. The evaluation must therefore separate respect for the schema, accuracy of the facts and spatial or temporal grounding. For an action output, also specify the method-specific units, coordinate frames and execution contract; the plausibility of tokens does not validate a physical action.

### CV-VLM-002

**Situation**: Which problem does BLIP-2's Q-Former address in its original architecture?

**Representation bottleneck**: Learned queries query the features of the visual encoder by cross attention and produce an intermediate representation for the language model. They are not the free questions typed by the user. Limiting the number of vectors transmitted can reduce the cost of the interface while constraining the information available on small details. A frozen encoder and a frozen LLM can be linked by learned parameters without updating all their weights. The mechanism of the bridge and the learning protocol must therefore be described separately from the final behavior, which remains to be measured on the visual observations of the task.

### CV-VLM-003

**Situation**: Track D — design: index hours of video for event retrieval. How should a general-purpose VLM be compared with detection, tracking and rules?

**Cost of indexing**: with a video of duration $T$ and a sampling step $\Delta$, the number of frames retained is of the order of $T/\Delta$. The cost includes decoding, visual encoding, building windows, and generating or indexing outputs. Reducing this number can make short events disappear; increasing the context can add cost and delay without restoring a frame never observed. A hybrid pipeline can first propose intervals and then describe them, but it is necessary to measure the recall of this preselection: an excluded event will never reach the VLM. Evaluate each step and the final index on the same held-out events.

### CV-VLM-004

**Situation**: Track D — diagnosis: a VLM describes absent objects in industrial images. Which investigation leads to a verifiable correction?

**Constructed grounding tests**: Use a positive image, a comparable negative image and, if feasible, a variation where only the target object changes. Check whether the assertions actually follow this variation and whether the correction increases refusals rather than accuracy. A decrease in the number of false assertions obtained by never responding is not the same result as better recognition; report the coverage of responses and the risk of error among responses issued. These tests must respect the distribution of the images, because artificial masking can introduce an artifact. Outputs must remain connected to the exact version of the input and prompt used.

**Passages consulted for these developments**: [Li et al., BLIP-2](https://arxiv.org/html/2301.12597v2), §3.1, learned queries and cross attention; the probabilistic formulation and the constructed tests are project reasoning.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-VLM-001 — An action interface needs a state and timing contract

A VLA output can encode commands in a learned action representation, but the controller still needs units, reference frames, frequency and validity limits. A plausible language description does not establish an executable command, and a valid command schema does not prove that the visual state was estimated correctly. Compare models at their declared outputs and evaluate any conversion into physical actions separately. No robotic execution is established by these notes.

### CV-VLM-003 — Retrieval needs both event coverage and verification

A proposed video index can use a cheap first stage to retrieve candidate intervals and a more expensive model to verify them. Measure missed events introduced by the retrieval stage separately from false descriptions introduced by verification. Include short events and temporally similar negatives, and account for sampling, decoding and prompt cost. An accurate verifier cannot recover an event never presented in its sampled candidate frames.

### CV-VLM-004 — A counterfactual image pair can test visual dependence

Construct paired inputs differing in one controlled object while keeping prompt and scene context fixed. Check whether the answer changes with the image and whether absence is acknowledged on a negative image. Preserve the actual decoded inputs and generation settings. This proposed diagnostic helps identify context-driven responses, but passing a few pairs does not certify grounding across the deployment distribution or eliminate hallucinations globally.

Consulted foundations: [BLIP-2](https://arxiv.org/html/2301.12597v2): §3 Q-Former learned queries and frozen encoder/language-model bridge; [LLaVA](https://arxiv.org/html/2304.08485v2): §4 visual instruction tuning and limitations.

## Sources and flashcards

### Scientific sources

- [Radford et al. 2021, CLIP](https://arxiv.org/abs/2103.00020): §2.3, contrastive objective over $N\times N$ pairs.
- [Li et al. 2023, BLIP-2](https://arxiv.org/html/2301.12597v3): §1, §3.1 (Q-Former, 32 × 768 queries, 188M parameters), §3.2 (three objectives and their attention masks), §3.3 (projection, soft visual prompts, LM and prefix-LM losses), §4.1 and Fig. 5 (effect of the representation-learning stage).
- [Liu et al. 2023, LLaVA](https://arxiv.org/html/2304.08485v2): §4.1 eq. 1, §4.2 eq. 3 and two-stage training, §5.1 limitations, hallucination paragraph.
- [Alayrac et al. 2022, Flamingo](https://arxiv.org/html/2204.14198v2): §2.1 Perceiver Resampler and video sampling, §2.2 tanh gating, §2.3 per-image attention masking.
- [Xiao et al. 2023, Florence-2](https://arxiv.org/html/2311.06242v1): §3 location tokens and region formats, §6.1 training resolutions.
- [Brohan et al. 2023, RT-2](https://arxiv.org/html/2307.15818v1): §3.2 action tokens.
- [Kim et al. 2024, OpenVLA](https://arxiv.org/html/2406.09246v3): §1, §3.2 action discretization.
- [Black et al. 2024, $\pi_0$](https://arxiv.org/html/2410.24164v1): §I and §IV, flow matching, action chunks, control rate.
- [Rohrbach et al. 2018, CHAIR](https://arxiv.org/html/1809.02156v2): §2.1 metric definitions, §2.3 language consistency, §3.2 beam-size observation, §3.3 causes.
- [Li et al. 2023, POPE](https://arxiv.org/html/2305.10355v3): §5.1 probing protocol and metrics.

### Implementation sources

No library API is described in this note. The [OpenVLA project page](https://openvla.github.io/) is retained as the official release page; it was not re-read in this pass.

### Related flashcards and references

- [Flashcards](../121-vlm-grounding.md): CV-VLM-001 to 004.
- [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md), [CV-OPENVOC](../../80-detection-pose/references/83-detection-open-vocabulary.md), [CV-VIDEO](../../100-mouvement-video/references/102-points-actions-video.md).

Drafted by agent, 2026-10-18. Revision 7, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/121-vlm-grounding.md).
Revision 8, 2026-11-16: BLIP-2 attention masks, stage-2 losses and the stage-1 ablation added while
deepening CV-VLM-002, by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-16-card-depth/121-vlm-grounding.md).
