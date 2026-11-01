---
id: CV-CORRELATION
type: methode
domaine: d11
poles: ["C", "D", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-SOT", "CV-FILTRES"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MOSSE and KCF — tracking with correlation filters

## Prerequisites and competencies

**Required prerequisites**: [CV-SOT](113-tracking-monoobjet.md), [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md). **Target competencies**: explain the loop of a tracking filter; distinguish MOSSE and KCF; interpret a PSR; look for contamination of the model; define an honest comparison of trackers. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Track an initialized target in an ROI, based on its appearance and local search. Inputs: initial image, target box and following frames; output: position or box and possible response score. This single-object tracking does not automatically create trackss for all objects and does not guarantee re-identification after prolonged disappearance.

## Intuition and mechanism

A filter learns to produce a target-centered peak and a weaker response around it. MOSSE adapts a linear filter from transformed examples and accepted frames; KCF exploits a kernel regression on the cyclic offsets of the patch. The circulant structure is diagonalized to Fourier, which avoids solving a large dense regression. To follow up: extract patch → calculate response → locate peak → check trust → update under conditions. A update on the wrong target reinforces the drift.

## Mathematics and conventions

A simplified lens is $\min_h\sum_i\|h\star x_i-y_i\|^2+\lambda\|h\|^2$, where $x_i$ represents the features of the patch, $h$ the filter, $\star$ the circular correlation and $y_i$ a synthetic, often Gaussian target response. $\lambda\ge0$ regularizes the filter; these scores are arbitrary units, not calibrated probabilities. For MOSSE, $\mathrm{PSR}=(r_{max}-\mu_{horspic})/\sigma_{horspic}$ compares the maximum to the mean and standard deviation of the out-of-peak response bottom. Define this neighborhood and process a zero standard deviation. The historical threshold of a paper is not valid for any implementation.

## Parameters, cost and limitations

The search window limits the recoverable movement. Patch size, features, kernel, regularization, and learning rate change accuracy, memory, and computation. FFTs typically cost $O(n\log n)$ for $n$ samples per channel, but the entire pipeline and cores need to be measured. A Hann window limits edge discontinuities without removing the bias of cyclic shifts. Long-term scale or search extensions are variants to name; a basic KCF is not automatically scale-invariant.

## Evaluation and controlled variation

Proposed baseline: fixed appearance after initialization; variation: update online at fixed rate. Measure center error, overlap/success, target loss, and recovery time, with explicit reset protocol. Introduce an identical occlusion in both tests to test for model contamination. Analytical example: peak 0,8, average out of peak 0,2 and standard deviation 0,1 give PSR=6; this score is not a probability of 60% nor a universal threshold of success.

## Diagnosis and alternatives

If the box leaves on the bottom after a occlusion, check the update during ambiguous frames, search size, and concurrent peaks. Freezing the model, declaring the loss, or restarting a detector may be preferable to always issuing a box. For a big change of appearance or disappearance, compare a Siamese tracker or a pipeline detector+association. The proposals are reasonings of the project; no tracker or video benchmark executed for this reference note.

## Guided reasoning and proposed checks

These constructed cases develop circulating, window and risk of contamination of the model. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-CORRELATION-001

**Question of work**: How does a correlation filter initialized from a box track the target in the next frame?

**Reference Response**: Extract a search region and its features, correlate with the model, locate the peak, check reliability and then adapt the model only according to the chosen policy. The answer is a location peak, not a semantic class.

**Interpretation of the answer**: Each candidate move in the search region receives a model-like score. The peak locates the preferred hypothesis, but its contrast and the presence of competitors must be examined before an update. The search area already expresses a hypothesis about possible movement.

**Constructed example**: A target moving beyond this area can leave the background with the best available peak. Learning then this background transforms a loss of location into a persistent drift of the model. Define a loss and recovery policy, then test it on big moves and occlusions. Correlation speed is useful only if the research and update assumptions are suitable as needed.

### Case linked to CV-CORRELATION-005

**Question of work**: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?

**Reference Response**: Initialization and reset protocol, sequences, losses, overlap and center error, as well as full latency. A restart after error changes the evaluated task.

**Why Resets Change the Task**: A reset provides the tracker with a new location after a failure. A system without this help must find the target or remain lost. The two protocols therefore do not expose the model to the same accumulation of errors or the same amount of external information.

**Proposed comparison**: keep sequences, initialization, presence rule and loss criterion. Report failures and recovery periods in addition to location measurements. An average calculated only on successful frames can favor a method that abandons difficult cases. For a product, include the cost and time of the actual recovery procedure, whether automatic or human. Scores remain interpretable only with this evaluation contract.

**Documentary reference for this pass**: [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf), §§3 – 4, filter and tracking. The other developments are in the [flashcards](../114-mosse-kcf.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-CORRELATION-001

**Situation**: How does a correlation filter initialized from a box track the target in the next frame?

**From the pic to the image**: The answer is calculated in the coordinates of the patch or its features. Converting the maximum offset to the image requires the origin of the crop, its resizing, and any stride. A circular correlation convention also requires interpreting near-edge indices as appropriate signed offsets. An error here can produce a jump despite a correctly calculated peak. Check a known synthetic translation and return to the coordinate frame image before setting the trust. The possible subpixel location refines the peak estimation; it does not guarantee equivalent physical accuracy on real images.

### CV-CORRELATION-002

**Situation**: What do cyclic shifts and kernels give KCF compared with a linear filter such as MOSSE?

**Structured regression**: a regularized linear regression solves $\min_w\|Xw-y\|^2+\lambda\|w\|^2$. If the lines of $X$ are the cyclic shifts of the same signal, the circulant structure makes it possible to diagonalize the corresponding operations by Fourier transform. In a kernel regression, we work on a matrix of similarities whose structure must remain compatible. This explains the efficiency without assimilating a core to a deep network. The regularization parameter stabilizes learning according to the feature scale; it does not compensate for a target missing from the patch or an artificial edge hypothesis ill-suited to the scene.

### CV-CORRELATION-003

**Situation**: A response has a peak of 0.8, an off-peak mean of 0.2 and an off-peak standard deviation of 0.1. What is the PSR, and what does it mean?

**Effect of a distractor**: If a second peak enters the area used to calculate average and standard deviation off peak, it can change the PSR of the first, even if its height remains the same. The size of the excluded area and the edges of the patch therefore participate in the definition of the score. A positive affine transformation $r'=ar+b$, with the same support and $a>0$, ideally retains the PSR, because numerator and standard deviation are multiplied by $a$. On the other hand, clipping, quantifying or changing the medium can break this invariance. The score is therefore comparable only with an identical calculation procedure and a threshold validated in its context.

### CV-CORRELATION-004

**Situation**: A correlation-filter tracker works before an occlusion, then persistently tracks the background. Which update error should be tested?

**Separate research and learning**: Freeze updates retains a target model, but does not automatically change the region being crawled. After a long occlusion or a large shift, the target may return elsewhere and remain untraceable despite an intact model. Compare two separate interventions: freezing the model with unchanged search, then expanded search policy or detection with the same model. Measure false returns on distractors and recovery times, without using the true position to silently reset. This ablation distinguishes contamination, loss of spatial coverage and appearance ambiguity, which can produce a similar final box on the bottom.

### CV-CORRELATION-005

**Situation**: Two trackers obtain similar scores, but one is reinitialized after each failure. What must be specified for a fair comparison?

**Measure of success**: A curve can report, for each $\tau$ threshold, the proportion of frames where the IoU of the target exceeds $\tau$, under an announced presence policy. The area under this curve describes something other than the accuracy of the center at a fixed pixel threshold. Two boxes of the same center but of very different sizes can have a good center error and a bad IoU. The resets still change which periods are evaluated and what information is provided. Publishing the rules with the curve and the losses allows to compare the compromises without retaining only the frames where the tracker has succeeded.

**Passages consulted for these developments**: [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf), §3.1 – 3.2, edges and learning; mathematical complements and built protocols; [Henriques et al., KCF](https://arxiv.org/html/1404.7584v1), §IV, regression and circulant structure; project deductions.

## Sources and flashcards

- [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
- [Henriques et al., KCF, §§4 – 5, circulant structure and kernels](https://arxiv.org/pdf/1404.7584).
- [Related flashcards](../114-mosse-kcf.md): CV-CORRELATION-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
