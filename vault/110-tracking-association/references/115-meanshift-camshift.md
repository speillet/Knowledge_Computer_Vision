---
id: CV-MEANSHIFT
type: methode
domaine: d11
poles: ["C", "D", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-SOT", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MeanShift and CamShift — tracking an appearance distribution

## Prerequisites and competencies

**Required prerequisites**: [CV-SOT](113-tracking-monoobjet.md), [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md). **Target competencies**: explain a MeanShift iteration; distinguish MeanShift and CamShift; diagnose a color distractor; evaluate color and adaptation separately. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Track a target initialized by a window and an appearance pattern, often a color histogram. Each frame becomes a backprojection image: the pixels receive a score according to their compatibility with the model. A high value is not a calibrated probability of identity. Same color and same object are two different notions.

## Mechanism and mathematics

MeanShift moves a window to the weighted center of mass of the local distribution, until convergence or stop. For non-negative $p(x,y)$ scores, set $M_{00}=\sum p$, $M_{10}=\sum xp$ and $M_{01}=\sum yp$ in the window: the centroid is $(M_{10}/M_{00},M_{01}/M_{00})$ if $M_{00}>0$. The coordinates are in pixels. This is a local search, not a global maximum guarantee. In the usual MeanShift tracker, the window size remains fixed. CamShift adapts the window and its orientation from the moments of distribution, then continues the follow-up. An oriented rectangle is not a pose 3D.

## Assumptions, parameters and cost

Histogram, channels, bins, initial ROI and saturation/luminance mask change the target/bottom separation. The hue is unstable on sparsely saturated pixels: a simple HSV conversion does not guarantee invariance in lighting. Budget iterations and minimal movement control the stop. A window that is too small loses the target; a window that is too large includes distractors. The cost includes color conversion, backprojection and iterations on the window. API OpenCV 4.13 checked; no video tracking performed.

## Evaluation and controlled variation

Proposed baseline: MeanShift with fixed window; variation: CamShift on a sequence where the target changes scale, with identical histogram and initialization. Measure overlap, center error, window surface and losses, including a distractor of the same color. Analytical example of the project: two masses 1 and 3 located at $x=10$ and $x=14$ have their center weighted at 13 px, not at 12. If the mass is zero, do not divide: declare an observation invalid or apply an advertised search policy.

## Diagnosis and alternatives

A window drawn by the background requires to inspect the backprojection and the histogram contrast before adding iterations. During a occlusion, a distractor can accumulate more mass than the target. CamShift can then enlarge an incorrect window; scaling is not an identity check. Compare histograms better separated, texture features, correlation filters or detector+association according to constraints. The choice of stimulus must be measured and explicit.

## Guided reasoning and proposed checks

These built cases develop backprojection, local mode and window adaptation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-MEANSHIFT-001

**Question of work**: What does one MeanShift iteration compute on a backprojection image, and what should happen if the window contains no mass?

**Reference Response**: Calculate the centroid of scores in the window, and then move the window to that center. If the total mass $M_{00}$ is zero, the centroid is indefinite: do not divide and apply an explicit loss/search policy.

**Reading moments**: The backprojection assigns a mass to each position according to its compatibility with the reference appearance. The weighted centroid gives a window shift towards this concentration. With two masses 1 and 3 placed at 10 and 14 pixels, the center is $(10+42)/4=13$ pixels: it is not the unweighted average of positions.

**Decision limit**: If the whole mass is zero, no mean position is defined by these observations. An arbitrary digital output would mask a lack of information. Report the loss or apply an advertised search, and then evaluate this policy. Even with a positive mass, a background of similar color can attract the window, so the concentration found does not verify the identity of the initialized object.

### Case linked to CV-MEANSHIFT-004

**Question of work**: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?

**Reference Response**: Keep the same histogram, frames, and initialization; compare fixed window and adaptive window on a scale change. Measure center, overlap, size, and losses, and then separately test a histogram change.

**The logic of ablation**: Changing only the window adaptation tests its effect on the location contract. Modifying the histogram at the same time changes the masses on which the displacement is calculated, which prevents assigning the improvement to a single mechanism.

**Experience built**: Use one sequence where the target gradually grows, then another where a distractor appears without scaling. Keep the same loss and reset criteria, and report errors on all frames. An adaptive window can help the first case and harm the second if the mass of the distractor distorts it. The comparison must make this compromise visible. Channels, bins and masks are parameters of the appearance model; their setting requires another ablation and reserved data.

**Documentary reference for this pass**: [OpenCV 4.13, Meanshift and Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html), histogram, backprojection and window CamShift. The other developments are in the [flashcards](../115-meanshift-camshift.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-MEANSHIFT-001

**Situation**: What does one MeanShift iteration compute on a backprojection image, and what should happen if the window contains no mass?

**Weighted iteration**: For $p(x,y)\ge0$ scores in window $W$, the current center displacement $c$ is $m(c)=\sum_Wp(x,y)(x,y)^T/\sum_Wp(x,y)-c$, in this uniform window model. A common multiplication of all scores by a positive constant does not change the centroid; adding a uniform mass can instead move it towards the geometric center of the window. This distinction explains why normalizing the histogram and changing its contrast are not always equivalent operations. The stop criterion measures a move or budget of iterations, without establishing that the found mode represents the original object.

### CV-MEANSHIFT-002

**Situation**: The target approaches the camera, but the tracking window remains too small. What does CamShift add compared with usual MeanShift?

**Moments of extent**: Around the centroid, the matrix of normalized central moments $\begin{bmatrix}\mu_{20}&\mu_{11}\\\mu_{11}&\mu_{02}\end{bmatrix}/M_{00}$ describes the dispersion 2D of the mass. Its eigenvectors give main axes; their values inform the extent according to a window conversion convention. Close values make the orientation undetermined, as for an almost circular distribution. These quantities describe the backprojection in the image plane, not the physical axes 3D of the part. A distractor can change center, orientation and size simultaneously. The appearance mask should therefore be inspected before interpreting a suitable window as a reliable geometric measurement of the target.

### CV-MEANSHIFT-003

**Situation**: CamShift jumps to another part of the same color. Why can increasing the number of iterations make the problem worse?

**Identity missing from histogram**: A histogram retains color frequency and loses much of their spatial arrangement. Two different objects can therefore produce very similar distributions, even with a high backprojection mass. An ROI containing more pixels of the desired color can attract the window without being the target. Testing a background of the same color and then a textured distractor makes it possible to verify this hypothesis. Adding a spatial descriptor or detection changes the information used and requires a new evaluation; increasing the number of iterations does not restore the spatial relationships that the histogram model has deleted.

### CV-MEANSHIFT-004

**Situation**: Which experiment distinguishes an improvement due to CamShift adaptation from one due to a new histogram?

**Two factors, four tests**: To distinguish adaptation and appearance, compare histogram H1 with fixed/adaptive window, then histogram H2 with the same two policies. Measure overlap, center error and initialization losses and identical sequences. The interaction can be important: an adaptive window benefits from a clean backprojection but encompasses more background with a poorly separated histogram. A change of binning modifies the trade-off between color discrimination and noise robustness; a low-saturation mask further changes the retained pixels. These choices must be recorded separately to make the result reproducible and attributable to the mechanism actually modified.

**Passages consulted for these developments**: [OpenCV 4.13.0, MeanShift/CamShift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html), MeanShift, centroid and backprojection; moments and factorial plan deduced by the project.

## Sources and flashcards

- [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [Related flashcards](../115-meanshift-camshift.md): CV-MEANSHIFT-001 to 004.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
