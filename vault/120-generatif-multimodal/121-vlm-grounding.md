# Flashcards — VLMs, grounding and the vision–action boundary

reference note: [[120-generatif-multimodal/references/121-vlm-grounding|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-VLM-001

Objective: Situate encoder, VLM and VLA. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-VLM-001
Question: How do CLIP used for image–text comparison, a generative VLM and a VLA differ?
Reponse: **Expected answer**: CLIP compares image-text representations; a VLM generates outputs conditioned by vision/language; a VLA produces an action interface according to its design.

**Further explanation**: Tasks, metrics and validations differ. Studying the VLA here does not include validation on a robot.

**Define the interface**: Comparing embeddings is used to rank or search among candidates; generating text produces a conditioned sequence; producing actions engages another representation and another evaluation environment. An architecture can share building blocks without these contracts becoming interchangeable.

**Constructed example**: “A part is present” may be a plausible description, but does not provide a validated box or a properly referenced robotic control. For an application, specify output format, validity time and expected reference, and then measure omissions and false assertions. If actions are studied, distinguish between knowledge of the interface and validation of a closed-loop policy. The course here covers perception and its limits; the move to control is not inferred from a convincing verbal response or a high generation score. The evidence must match what the system actually promises.

**Optimized quantity**: an autoregressive generator models $p(y\mid I,q)=\prod_kp(y_k\mid y_{<k},I,q)$ for an image $I$, a question $q$ and tokens $y_k$. A probable sequence under this model is not automatically a true visual proposition. A syntactically valid JSON format can also contain a false box or object. The evaluation must therefore separate respect for the schema, accuracy of the facts and spatial or temporal grounding. For an action output, also specify the method-specific units, coordinate frames and execution contract; the plausibility of tokens does not validate a physical action.

**An action interface needs a state and timing contract**: A VLA output can encode commands in a learned action representation, but the controller still needs units, reference frames, frequency and validity limits. A plausible language description does not establish an executable command, and a valid command schema does not prove that the visual state was estimated correctly. Compare models at their declared outputs and evaluate any conversion into physical actions separately. No robotic execution is established by these notes.

**Blocking errors**: Presenting a textual description as a validated control policy.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Full reference]]; [CLIP, §2.3: contrastive image–text objective](https://arxiv.org/abs/2103.00020); [LLaVA, §§4.1–4.2: projected visual tokens and autoregressive training](https://arxiv.org/html/2304.08485v2); [OpenVLA, §3.2: actions discretized into 256 bins and emitted as tokens](https://arxiv.org/html/2406.09246v3). Added reasoning: project deduction.
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-VLM-001 provenance::agent pole::A pole::D
END

## CV-VLM-002

Objective: Situate a visual connector. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-VLM-002
Question: Which problem does BLIP-2's Q-Former address in its original architecture?
Reponse: **Expected answer**: Connect a frozen pre-trained image encoder and a frozen pre-trained language model through a learned intermediate representation (learned queries) and an adapted two-stage training.

**Further explanation**: Do not generalize this connector to all VLM variants; it does not guarantee exact grounding on its own.

**Intuition of the connector**: The pre-trained visual encoder and language model do not automatically share an interface that carries useful information. The Q-Former learns an intermediate representation from queries and objectives adapted to connect these spaces in BLIP-2.

**What this does not demonstrate**: A trained connection can allow conditioned outputs without guaranteeing that every claimed detail is present in the image. Information can be poorly represented, poorly resolved or dominated by linguistic regularities. For a constructed diagnosis, check the received image, prompt variations and annotated negative examples, and then measure the useful outputs. Compare a specific version of the architecture rather than assume that all VLMs use the same bridge. The mechanism explains an organization of learning and transfer; it does not replace a grounding protocol on the target domain.

**Representation bottleneck**: Learned queries query the features of the visual encoder by cross attention and produce an intermediate representation for the language model. They are not the free questions typed by the user. Limiting the number of vectors transmitted can reduce the cost of the interface while constraining the information available on small details. A frozen encoder and a frozen LLM can be linked by learned parameters without updating all their weights. The mechanism of the bridge and the learning protocol must therefore be described separately from the final behavior, which remains to be measured on the visual observations of the task.

**Blocking errors**: Attributing a Q-Former to every multimodal model or equating it with a simple prompt.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Full reference]]; [Li et al., BLIP-2, §§3.1–3.3: Q-Former with 32 learned queries between a frozen image encoder and a frozen LLM, two-stage pre-training](https://arxiv.org/html/2301.12597v3). The diagnostic reasoning is a project deduction.
Tags: cv::pilote cv::d12 famille::comprehension cv_id::CV-VLM-002 provenance::agent pole::A pole::D
END

## CV-VLM-003

Objective: Design a video index. Family: design. Provenance: agent.

START
CV-Pilote
ID: CV-VLM-003
Question: Track D — design: index hours of video for event retrieval. How should a general-purpose VLM be compared with detection, tracking and rules?
Reponse: **Expected answer**: Define events, temporal outputs, cost and latency; build baselines on annotated clips, including negatives/short events; compare recall, hallucinations and full cost.

**Further explanation**: A hybrid system can be justified; document sampling, access to future frames and rejection conditions. Fluency does not measure the recall of events.

**Proposed output choice**: For a specific rule such as “object entering a zone and then exiting”, detection, tracking and temporal logic make certain hypotheses inspectable. For open descriptions, a VLM can provide different flexibility. The two options can complement each other, but the fluency of the text does not measure the recall of events.

**Comparison**: Set sampling, minimum duration of events, access to the future and an annotated interval reference. Include absences of event, close scenes and short cases entirely between two samples. Measure omissions, false assertions, temporal location, and cost of encoding/decoding on the actual volume. A better description of a selected clip does not guarantee a good indexing of several hours. The protocol must show the trade-off between coverage, cost and accuracy of the expected response.

**Cost of indexing**: with a video of duration $T$ and a sampling step $\Delta$, the number of frames retained is of the order of $T/\Delta$. The cost includes decoding, visual encoding, building windows, and generating or indexing outputs. Reducing this number can make short events disappear; increasing the context can add cost and delay without restoring a frame never observed. A hybrid pipeline can first propose intervals and then describe them, but it is necessary to measure the recall of this preselection: an excluded event will never reach the VLM. Evaluate each step and the final index on the same held-out events.

**Retrieval needs both event coverage and verification**: A proposed video index can use a cheap first stage to retrieve candidate intervals and a more expensive model to verify them. Measure missed events introduced by the retrieval stage separately from false descriptions introduced by verification. Include short events and temporally similar negatives, and account for sampling, decoding and prompt cost. An accurate verifier cannot recover an event never presented in its sampled candidate frames.

**Blocking errors**: Choosing on the basis of a few plausible descriptions without ground truth.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating verification, limit of the conclusion. Constructed case, without field observation.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Full reference]]; case and indexing protocol designed by the project; example of an image and video model: [Flamingo, §2.1: frames sampled at 1 frame/s, resampled to 64 visual tokens](https://arxiv.org/html/2204.14198v2). Added reasoning: project deduction.
Tags: cv::pilote cv::d12 famille::conception cv_id::CV-VLM-003 provenance::agent pole::A pole::D cas_pole::D::conception
END

## CV-VLM-004

Objective: Distinguish hallucination from insufficient observation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-VLM-004
Question: Track D — diagnosis: a VLM describes absent objects in industrial images. Which investigation leads to a verifiable correction?
Reponse: **Expected answer**: Check image actually received, resolution/prompt, distribution, negatives and reference; classify hallucinations and omissions then test one intervention at a time.

**Further explanation**: Compare with a structured detection or a measured rejection rule. A high text score does not prove the object; do not tune the prompt on the final test set.

**Discriminating ablation**: Keep the image and reference labels, change only the wording on validation data, and then compare with a structured vision pipeline. Also test images without the target object and variations in resolution. This helps distinguish badly transmitted information from a tendency to complete a familiar scene linguistically.

**Correction criterion**: Seek a measured decrease in false assertions without silently increasing omissions. A cautionary instruction can change the style of responses without making their content more accurate. Keep the refusal policy, the inputs actually processed and the checkpoint, to reproduce errors. Any improvement remains tied to the protocol; no prompt here is a general guarantee of removing hallucinations on all new products.

**Constructed grounding tests**: Use a positive image, a comparable negative image and, if feasible, a variation where only the target object changes. Check whether the assertions actually follow this variation and whether the correction increases refusals rather than accuracy. A decrease in the number of false assertions obtained by never responding is not the same result as better recognition; report the coverage of responses and the risk of error among responses issued. These tests must respect the distribution of the images, because artificial masking can introduce an artifact. Outputs must remain connected to the exact version of the input and prompt used.

**A counterfactual image pair can test visual dependence**: Construct paired inputs differing in one controlled object while keeping prompt and scene context fixed. Check whether the answer changes with the image and whether absence is acknowledged on a negative image. Preserve the actual decoded inputs and generation settings. This proposed diagnostic helps identify context-driven responses, but passing a few pairs does not certify grounding across the deployment distribution or eliminate hallucinations globally.

**Blocking errors**: Accepting fluent wording as visual proof or promising complete elimination by prompting.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating verification, limit of the conclusion. Constructed case, without field observation.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Full reference]]; investigation proposed by the project; [LLaVA, §§4.1–4.2 and hallucination limitation](https://arxiv.org/html/2304.08485v2); [Li et al., POPE, §5.1: present/absent object probes with random, popular and adversarial negatives and the yes ratio](https://arxiv.org/html/2305.10355v3). Added reasoning: project deduction.
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-VLM-004 provenance::agent pole::A pole::D cas_pole::D::diagnostic
END
