---
id: CV-VIDEO
type: comparaison
domaine: d10
poles: [D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 9
prerequis: ["CV-FLOT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Point tracking, actions and video understanding

This comparison note separates three video tasks that are often confused because
they consume the same frames: tracking arbitrary points over time (TAP), classifying
a trimmed clip, and localizing actions in time within an untrimmed video. It fixes
their output contracts, their sampling and causality assumptions and their protocols,
then compares representative methods. Two-frame motion is in
[CV-FLOT](101-flot-optique.md); box tracking of one object is in
[CV-SOT](../../110-tracking-association/references/113-tracking-monoobjet.md) and
of many objects in [CV-SORT](../../110-tracking-association/references/111-sort.md);
the timing contract of a deployed video pipeline is in
[CV-PIPELINE](../../140-ingenierie-systemes/references/141-contrats-profiling-video.md).

## Problem and data contract

| Task | Input | Output | Typical protocol |
| --- | --- | --- | --- |
| Point tracking (TAP) | Video $(I_t)_{t=1}^T$ and query points $(t_q,x_q,y_q)$ in pixel and frame coordinates | Per query and frame, a position $(x_t,y_t)$ and an occlusion flag; positions during occlusion "typically assumed to be meaningless" | TAP-Vid: OA, $<\delta^x_{avg}$, AJ at $256\times256$ [TAP-Vid, §3, §4.3] |
| Clip classification | A trimmed clip, sampled into a few frames or tubelets | One label (or scores) per clip | Kinetics: about 10 s clips, top-1/top-5 [Kinetics, §2] |
| Temporal action localization (TAL) | An untrimmed video, often as clip features $x_1..x_T$ | A set of instances $(s_i,e_i,a_i)$: onset, offset, label | mAP at temporal IoU thresholds [ActionFormer, §3, §4] |

**Coordinate and time conventions.** TAP positions are in pixels of the evaluated
frame; TAP-Vid resizes every video to $256\times256$ whatever its aspect ratio, so its
pixel thresholds are anisotropic in the source frame (worked example A). CoTracker
assumes that each point is visible at its query frame and outputs tracks only for
$t\ge t_i$ [CoTracker, §3]. Clip labels refer to a window whose duration depends on the
sampling recipe; TAL boundaries are times or feature indices that must be converted
back to timestamps. In every case the time base is the acquisition timestamp of each
frame, not the frame index ([CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md)).

**Access to the future.** The contracts differ in which frames may inform an output at
time $t$. TAP-Vid's "first" protocol queries a point at its first visible frame and
expects causal tracking forward; the "strided" protocol queries every five frames and
tracks in both directions [CoTracker, §4]. Offline trackers, clip classifiers and most
TAL methods see the whole clip or video.

**Role in a pipeline.** Point tracks feed motion analysis, deformation measurement,
robotics and correspondence for 3D; clip labels feed indexing and coarse event
recognition; TAL feeds event logs and alarms with start and end times. A downstream
alarm needs a decision time and a latency budget that the benchmark protocol rarely
states.

## Intuition

A point tracker answers "where is this physical surface point in every frame, and can
I see it?"; it knows nothing about objects or actions. A clip classifier answers "what
is happening in this excerpt?"; it may answer correctly from a single frame if the
scene gives the action away. A temporal localizer answers "when does each action
start and stop?"; it must place boundaries, which a clip label cannot provide.

*Illustration (constructed).* A worker picks up a part, inspects it and puts it down.
A point tracker follows a mark on the part through the hand occlusion; a clip
classifier labels the excerpt "inspecting part", possibly from the background alone;
a temporal localizer outputs "pick up 2.0–3.1 s, inspect 3.1–7.5 s, put down
7.5–8.2 s". Swapping "pick up" and "put down" requires temporal order; recognizing
"inspecting" may not.

## Prerequisites and competencies

**Required prerequisites**: [CV-FLOT](101-flot-optique.md). Useful background:
transformer and ViT tokenization ([CV-REPRESENTATIONS](../../70-reconnaissance-representations/references/71-representations-transfert.md));
IoU and average precision, whose 1-D versions TAL uses
([CV-IOU-AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md));
data splits and leakage between clips of one video
([CV-FIABILITE](../../130-evaluation-fiabilite/references/133-donnees-generalisation.md));
latency and timing contracts ([CV-PIPELINE](../../140-ingenierie-systemes/references/141-contrats-profiling-video.md)).
**Target competencies**: choose the output contract that a use case needs; reason about
sampling and short events; separate causal, windowed and offline protocols; read TAP-Vid,
Kinetics and TAL metrics; diagnose a model that ignores time.

## Assumptions, observability and degenerate cases

- **Sampling.** An event shorter than the sampling step can fall between samples; under
  a uniform phase and instantaneous capture, it is sampled with probability
  $d/\Delta$ (worked example B). Real models sample sparsely: SlowFast's Slow pathway
  processes "only one out of $\tau$ frames", about 2 frames per second for $\tau=16$ at
  30 frames/s [SlowFast, §3.1]; TimeSformer samples 8 frames "at a rate of 1/32"
  [TimeSformer, §4].
- **Point identity.** TAP assumes a physical surface point that stays the same; it is
  undefined for fluids, reflections and points that change appearance completely.
  Positions during occlusion are not evaluated in TAP-Vid [§3].
- **Label completeness.** Kinetics clips "do not have complete (exhaustive) annotation":
  a clip can contain several actions but appears under one class, which is why the
  authors find top-5 "more suitable than top-1" [Kinetics, §2]. A clip label also says
  nothing about where in the clip the action occurs.
- **Temporal evidence.** Many clip labels can be predicted from scene and objects. The
  I3D authors initialize 3D networks so that a "boring" video of a repeated image gives
  the same output as the image classifier [I3D, §2.4], which shows how much a video model
  can rely on appearance. TimeSformer reports that space-only attention degrades
  "especially on benchmarks where strong temporal modeling is necessary" [§3].
- **Domain.** TAP models are mostly trained on synthetic Kubric sequences; TAP-Vid warns
  that Kubric performance "may not correlate very well" with other datasets [§4.3].
  CoTracker3 fine-tunes on 15k unlabelled real videos with pseudo-labels from teacher
  trackers [CoTracker3, abstract, §3.1].

Degenerate cases: a query point that is occluded at its query frame (excluded by
CoTracker's definition); a clip with no action or several; an action longer than the
model's window, whose boundaries no single window sees.

## Procedure

### Point tracking with a windowed transformer (CoTracker family)

```text
features <- CNN(I_t) for every frame, at 1/4 resolution          # CoTracker Sec. 3.1
tracks   <- query positions copied to all frames; visibility <- 1
for each window of T frames, stepping by T/2:                    # Sec. 3.3
    initialize the overlap from the previous window's estimates
    repeat M times:                                               # iterative refinement
        tokens <- correlation features around current tracks + track embeddings
        tokens <- transformer(attention over time and across tracks or proxy tokens)
        tracks += delta ; update visibility (and confidence in CoTracker3)
emit tracks and visibility for the frames the window completes
```

*Purpose.* Correlations around the current estimate localize the point; attention over
time smooths and bridges occlusions; attention across tracks lets points share motion
("joint tracking"), which the authors find improves accuracy "especially when points are
occluded" [CoTracker, §1]; support points add context [§3.4]; overlapping windows make
the model recurrent, so arbitrarily long videos can be processed [§3.3]. TAPIR instead
matches each frame independently, then refines with local correlations [TAPIR,
abstract]. CoTracker3 offers an online variant (sliding windows, forward only) and an
offline variant (the whole video as one window, forward and backward) with the same
architecture [CoTracker3, §3].

### Clip classification

Sample a clip (for example $T$ frames with stride $\tau$), apply a spatio-temporal
network, and average scores over several temporal clips and spatial crops at test time.
SlowFast uses 10 clips × 3 crops, "30 views" [SlowFast, §4]; TimeSformer a single middle
clip × 3 crops [TimeSformer, §4]; I3D trains on 64-frame snippets and tests on whole
videos, "averaging predictions temporally" [I3D, §2.4].

### Temporal action localization

Extract clip features along the video (for example two-stream I3D features), predict for
every time step an action score and the distances to onset and offset, decode candidate
intervals and suppress duplicates with Soft-NMS [ActionFormer, §3, §3.4].

## Mathematics, conventions and units

**TAP-Vid metrics** [§4.3]. For a threshold $\delta$ in pixels at $256\times256$:
$<\delta^x$ is the fraction of ground-truth-visible frames whose prediction is within
$\delta$; occlusion accuracy (OA) is the per-frame accuracy of the occlusion flag;
Jaccard at $\delta$ is $TP/(TP+FP+FN)$, where a TP is a predicted-visible point within
$\delta$ of a visible ground truth, an FP a predicted-visible point whose ground truth is
occluded or farther than $\delta$, and an FN a visible ground truth predicted occluded or
farther than $\delta$. $<\delta^x_{avg}$ and AJ average over $\delta\in\{1,2,4,8,16\}$.

**Window coverage.** $L$ frames sampled every $k$ frames at frame rate $f$ span
$(L-1)k/f$ seconds from first to last sample, with sampling step $\Delta=k/f$; state
which convention a "clip duration" uses.

**Short events.** With a sampling step $\Delta$, an event of duration $d<\Delta$ with a
uniformly distributed phase and an instantaneous capture is sampled with probability
$d/\Delta$; for $d\ge\Delta$ at least one sample always falls inside.

**Temporal IoU and TAL mAP.** For intervals $[s,e]$ and $[\hat s,\hat e]$,
$\mathrm{tIoU}=|[s,e]\cap[\hat s,\hat e]|/|[s,e]\cup[\hat s,\hat e]|$, "the 1D Jaccard
index"; mAP averages AP over classes at a tIoU threshold, and average mAP over
thresholds, $[0.3{:}0.1{:}0.7]$ on THUMOS14 and $[0.5{:}0.05{:}0.95]$ on ActivityNet-1.3
[ActionFormer, §4].

**Order invariance.** A mean of per-frame predictions $z=L^{-1}\sum_tf(I_t)$ is invariant
to any permutation of the frames; it cannot distinguish an action from its reversal.

**CoTracker windows** [§3.3]: a video of $T'$ frames is split into
$J=\lceil 2T'/T-1\rceil$ windows of length $T$ overlapping by $T/2$; training sums a
discounted track loss over windows and refinement steps with $\gamma=0.8$ (eq. 2).

### Worked example A: TAP-Vid metrics on one track

Constructed example, recomputed by checks/102-points-actions-video.py. Over 10 frames
the point is visible on frames 1–8; the tracker predicts it visible on 1–9, within $\delta$
on 1–6 and too far on 7–8. Then $TP=6$, $FP=3$ (two far points and frame 9),
$FN=2$: Jaccard $6/11=0.545$, $<\delta=6/8=0.75$, OA $=0.9$. A far prediction counts as
both FP and FN, so AJ punishes confident wrong positions more than declaring the point
occluded. For a $1920\times1080$ source, the 1 px threshold at $256\times256$ is 7.5 px
horizontally and 4.2 px vertically, and 16 px becomes 120 by 67.5 px.

### Worked example B: what sparse sampling can see

Constructed example, recomputed by checks/102-points-actions-video.py, at 30 frames/s.

| Sampling | Step $\Delta$ | First-to-last span | P(sample inside a 100 ms event) |
| --- | --- | --- | --- |
| One frame per second (card CV-VIDEO-002) | 1 s | — | 0.10 |
| TimeSformer default, 8 frames at 1/32 | 1.067 s | 7.47 s | 0.094 |
| SlowFast 4×16, Slow pathway | 0.533 s | 2.13 s (64 raw frames) | 0.19 |
| SlowFast 4×16, Fast pathway ($\alpha=8$) | 66.7 ms | 2.13 s | 1 |

The Fast pathway exists precisely to keep "a fine representation along the temporal
dimension" [SlowFast, §3.2]; the table shows what the sparse pathways alone can observe.
These are sampling probabilities, not detection rates.

### Worked example C: waiting time of windowed point tracking

Constructed from CoTracker3 §3 (windows advance by $T'/2$) and the official online
predictor (window 16, step 8), recomputed by checks/102-points-actions-video.py. In steady
state a frame waits 0–7 frames for its first estimate and 8–15 frames for the revision
by the next overlapping window: up to 233 ms and 500 ms at 30 frames/s, before any
computation. Five future frames, as in card CV-VIDEO-003, impose at least 167 ms.

## Parameters and tuning

| Parameter | Values in the sources | Effect | What to watch |
| --- | --- | --- | --- |
| Point-tracker window $T$ and step | CoTracker: $T=8$, overlap $T/2$ [§3.3, §4]; CoTracker3 online predictor: 16 and 8; offline predictor window 60 (predictor.py L14–L35, L212–L225) | Temporal context versus waiting time | Revised outputs; occlusions longer than a window rely on recurrence [§3.3] |
| Support points | Global or local grids of extra tracked points [CoTracker, §3.4]; predictor adds a $6\times6$ support grid (predictor.py L24) | Context for single queries | Configurations "can lead to small differences in performance" [§3.4] |
| Visibility threshold | Offline predictor: visibility > 0.9 (L170); online predictor: visibility × confidence > 0.6 (L298–L299) | Trade-off between OA and AJ | Thresholds are implementation choices; recalibrate on in-domain data |
| Input resolution | TAP-Vid evaluates at $256\times256$ [§3, §4.3]; CoTracker resizes to the model resolution and rescales coordinates with $(W-1)/(w-1)$ (predictor.py L113–L126, L186–L188) | Sub-pixel accuracy and speed | Aspect-ratio distortion; align-corners convention when mapping back |
| Clip sampling ($T$, $\tau$, $\alpha$) | SlowFast $\tau=16$, $\alpha=8$, $\beta=1/8$ [§3.1–3.2]; TimeSformer 8 frames at 1/32 [§4]; I3D 64 frames at 25 frames/s [§2.4] | Temporal coverage versus resolution | Short events (example B); compare models at equal views |
| Test-time views | 30 views for SlowFast; 3 for TimeSformer [§4 of each] | Accuracy versus inference cost | Report FLOPs per view and number of views [SlowFast, §4] |
| TAL thresholds | tIoU ranges $[0.3{:}0.1{:}0.7]$ and $[0.5{:}0.05{:}0.95]$ [ActionFormer, §4] | Strictness of boundary evaluation | A single tIoU hides boundary quality |

VideoMAE's pre-training masks "90% to 95%" of space-time cubes with tube masking, a choice
motivated by temporal redundancy and leakage between neighboring frames [VideoMAE,
abstract, §1]; it is a self-supervised pre-training recipe, after which a downstream task
and its protocol must still be defined.

**Tuning approach (project method).** Start from the output contract and the decision
deadline. For TAP, measure displacement per frame and occlusion durations on in-domain
video, then sweep window and visibility threshold against OA and AJ on a small annotated
set. For classification and TAL, measure the duration distribution of the events of
interest and choose a sampling step well below the shortest event that must be seen;
evaluate at fixed views and report the cost.

## Properties and limits of guarantees

- **TAP outputs are local.** A track says where a surface point goes, not which object
  it belongs to or what the object does.
- **Joint tracking helps occlusions empirically**, not by guarantee [CoTracker, §1, §4.2].
- **Online is not zero-delay.** CoTracker is "an online algorithm that operates causally
  on short windows" [abstract], but an output waits for its window (example C); offline
  variants track occluded points better at the cost of memory-bound length [CoTracker3,
  §3].
- **Classifier invariances.** Averaging frame predictions is order-invariant; 3D
  convolutions and temporal attention can use order but are not forced to.
- **Benchmark scores are protocol-bound.** TAP-Vid "first" and "strided" results differ;
  Kinetics top-1 is affected by non-exhaustive labels; TAL mAP depends on the tIoU range.

## Cost and implementation

- **Point tracking**: per window, CNN features for $T$ frames plus $M$ transformer
  iterations over $N$ tracks × $T$ frames; attention across tracks grows with $N^2$, which
  CoTracker replaces by cross-attention to a small number of proxy tokens, allowing
  "70k points" on one GPU at inference [abstract, §1].
- **Clip models**: cost per view times the number of views; for TimeSformer's default clip,
  joint space-time attention compares 2.46 M token pairs per layer and head against
  0.32 M for divided attention (worked check in checks/102-points-actions-video.py, class
  token ignored); SlowFast's Fast pathway takes "∼20% of the total computation" [§3.2].
- **TAL**: ActionFormer runs on precomputed clip features (two-stream I3D on THUMOS14)
  [§4.1], so the cost of extracting features over the whole video must be counted
  separately from the localizer.

**Implementation contract (co-tracker, commit 82e02e8).** `CoTrackerPredictor` takes
`queries` of shape $(B,N,3)$ in $(t,x,y)$ frame index and pixel coordinates, or a
`grid_size`, and returns tracks and boolean visibilities in input pixels;
`backward_tracking=True` also tracks backwards from the query frame
(predictor.py L36–L68, L161–L209). `CoTrackerOnlinePredictor` is initialized with
`is_first_step=True` and then fed successive chunks (L212–L300). The code was read, not
executed; no model was run for this note.

## Evaluation and controlled variation

**Protocols.**

- *TAP-Vid*: Kinetics (1,189 videos, 26.3 points per video), DAVIS (30 videos, 21.7 points),
  synthetic Kubric and RGB-Stacking, all evaluated at $256\times256$ [Table 1, §3.1]; the
  authors advise training on Kubric, validating on DAVIS and not tuning on held-out sets
  [§4.3]. Published example: CoTracker3 online, trained on Kubric plus 15k real videos,
  reports AJ 63.8 and OA 90.2 on TAP-Vid-DAVIS in the "first" mode [CoTracker3, Table 1].
- *Kinetics*: 400 classes, 400–1150 clips per class, each about 10 s and from a unique
  YouTube video; train/val/test with 250–1000/50/100 clips per class [§2].
- *TAL*: THUMOS14 has 413 untrimmed videos of 20 classes, the 200 validation videos are used
  for training and the 213 test videos for evaluation [ActionFormer, §4.1]; ActionFormer
  reports 71.0% mAP at tIoU 0.5 there [abstract].

Worked check (constructed, recomputed by checks/102-points-actions-video.py): ground truth
2.0–6.0 s and prediction 3.0–6.5 s give tIoU 0.667, a true positive at thresholds 0.3–0.6
and a false positive at 0.7.

**Proposed baseline and controlled variation (not executed).**

- **Question**: does a clip classifier use temporal order on the target task?
- **Data**: in-domain clips including order-sensitive pairs (pick up / put down, open /
  close) and order-insensitive classes, split by source video.
- **Baseline**: the classifier on clips in natural order, with fixed sampling and views;
  plus a frame-averaging image model on the same frames.
- **Controlled variation**: reverse the frame order of every test clip; nothing else
  changes.
- **Measurements**: accuracy on order-sensitive pairs and on the other classes, separately;
  the frame-averaging model as a reference that cannot change under reversal.
- **Expected effect (hypothesis)**: a model that uses order loses accuracy on
  order-sensitive pairs only; a model that matches the frame-averaging baseline does not
  use order.
- **Confound**: reversal may create unnatural motion (objects falling upwards) that degrades
  scores for reasons other than order; compare with a permutation within short segments.

**Measurement limits.** Small TAP benchmarks (30 DAVIS videos); synthetic training domains;
non-exhaustive clip labels; TAL results depend on the feature extractor, which "some of
our baselines" did not share [ActionFormer, §4]; benchmark protocols do not measure decision
latency.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| High clip accuracy but alarms fire at the wrong time | A clip label has no boundaries | Output type: one label per clip versus intervals | Use TAL or an event detector with timestamps |
| Short events missed regardless of model | Event shorter than the sampling step | Event durations versus $\Delta$; vary the sampling phase | Denser sampling, a fast pathway, or an event trigger |
| Model accuracy unchanged under reversal or shuffling | Prediction driven by scene or objects | Compare with the frame-averaging baseline on order-sensitive pairs | Order-sensitive data, temporal augmentations, or a pipeline with explicit state |
| Point tracks jump to a similar texture after occlusion | Appearance ambiguity; occlusion longer than the context | Visibility and confidence around the jump; track length versus window | Offline variant, support points, or reject tracks after long occlusion |
| Track positions reported during occlusion are used downstream | Positions during occlusion are not evaluated or reliable | Visibility flags and threshold | Gate on visibility; treat occluded positions as missing |
| Online tracker "slower than measured" in the system | Window waiting time excluded from latency | Timestamp of the last frame consumed versus output time | Report total delay; shorter windows if the deadline requires |
| Validation score much higher than field score | Clips of the same video in train and test; synthetic-to-real gap | Split by source video; evaluate on in-domain annotated clips | Re-split; fine-tune on in-domain data |

## Alternatives and applications

Conditional choices:

- **Prefer point tracking** when the deliverable is the motion of surface points
  (deformation, robot manipulation, 3D correspondence); prefer an online tracker when a
  bounded delay matters and an offline one for analysis of recorded video.
- **Prefer optical flow** ([CV-FLOT](101-flot-optique.md)) when only two-frame motion is
  needed, and **box tracking** ([CV-SOT](../../110-tracking-association/references/113-tracking-monoobjet.md),
  [CV-SORT](../../110-tracking-association/references/111-sort.md)) when objects, not
  points, carry identity.
- **Prefer clip classification** for indexing trimmed clips; **prefer TAL** when start and
  end times are part of the requirement.
- **Prefer a detection, tracking and rules pipeline** for well-defined industrial events
  (a part crossing a line, a door left open): its states are inspectable and its latency is
  explicit; video models fit events that are hard to specify by rules.

Industrial uses (project reasoning, not published results): tracking points on a deforming
part during a press operation; logging operator steps with start and end times; retrieving
clips of a defect type from recorded production video.

## Guided reasoning and proposed checks

These constructed cases develop point trajectories, visibility and the time horizon. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-VIDEO-001

**Working question**: How do CoTracker, video classification and temporal action localization differ?

**Reference answer**: CoTracker tracks points with visibility; classification labels a clip; localization also estimates time intervals.

**Contracts to distinguish**: A point track answers "where is this observation over time?" A clip label answers "what action characterizes this excerpt?". A time interval adds a start and end estimate. One output may be correct for one of these contracts and insufficient for another.

**Constructed example**: Recognizing that a person sits down in a clip does not necessarily give the instant of contact with the chair. Tracking a point on a garment does not automatically give the action class either. Define the useful output before choosing the architecture and the metric: point error, visibility, classification or time boundaries. Specify the frames available to the model and the decision time. A performance obtained with the full clip does not validate an alarm that must fire before the end of the event.

### Case linked to CV-VIDEO-004

**Working question**: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?

**Reference answer**: Compare to an image/context baseline, check labels and actions that actually require order.

**Alternative hypothesis**: The presence of a tool, a setting or a characteristic posture can be enough to predict the clip label. Shuffling frames preserves many of these cues. A high accuracy alone therefore does not allow attributing the decision to temporal order.

**Proposed ablation**: Compare the model with an aggregation of image predictions, then select cases where the same visual states in a different order correspond to different events. Check sampling, labels, background and leakage between neighboring clips. If the performance stays the same on tasks that really depend on order, examine which information is used. A drop after permutation supports a temporal dependence, but does not prove any form of causal understanding. The reasoning must stay tied to the tasks and controls performed, not to the name of the architecture.

**Source consulted for this pass**: [CoTracker3](https://arxiv.org/abs/2410.11831), abstract, point tracking task. The remaining developments are in the [flashcards](../102-points-actions-video.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-VIDEO-001

**Situation**: How do CoTracker, video classification and temporal action localization differ?

**Annotation axes**: A point track can be represented by $(x_t,y_t,v_t)$, where $v_t$ describes visibility under the protocol. A clip label is a category associated with a window; temporal localization provides at least one category and an interval $[t_d,t_f]$. Cutting a long video into labeled clips can give rough temporal cues, but does not automatically create precise boundaries. To compare systems, keep the timestamps and the rules for matching predictions with actual events. A point tracked on a person is neither a complete identity of that person nor an action annotation without an additional definition.

### CV-VIDEO-002

**Situation**: A video is summarized with one frame per second. Why can detection of a 100 ms event not be guaranteed?

**Sampling phase**: In a constructed model where an event of duration $d<\Delta$ starts at a uniformly distributed phase with respect to a sampling grid of step $\Delta$, and where an instantaneous capture is sufficient, the probability that at least one sample falls inside the event is $d/\Delta$. For 100 ms and a step of 1 s, it is 0.1 under these assumptions. This is not a predicted performance of a real model: exposure, visibility and persistent cues change the problem. The calculation shows, however, why varying the phase is essential and why a demonstration where the event falls exactly on a frame does not validate guaranteed recall.

### CV-VIDEO-003

**Situation**: A point tracker uses a window containing future frames. Can its output be compared directly with a zero-delay causal model?

**Minimum delay for context**: If an estimate for $t$ uses a frame at $t+h$, it cannot be available before $t+h$, even before transfer and computation. A latency measurement limited to the network pass would therefore omit at least this context delay. With sliding windows, specify which outputs are provisional and which are revised afterwards. Evaluating the first decision and the final trajectory separately makes the comparison readable. A method can remain useful online within an accepted delay; the word causal, however, requires that each decision at a given time uses only the observations already available under the stated contract.

### CV-VIDEO-004

**Situation**: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?

**Permutation and reverse order**: An average aggregation $z=L^{-1}\sum_t f(I_t)$ is mathematically invariant to permutation; a good score obtained this way can come from visual states or context without encoding their order. Building pairs such as picking up and putting down an object, with similar states in a different order, tests another property. Also check that permutation does not create an unusual artifact that makes the score drop for the wrong reason. Comparing reversal, permutation and frame rate while changing only one factor helps to establish the use of time, without equating any temporal sensitivity with a complete understanding of the scene.

**Passages consulted for these developments**: algebraic complements and protocols constructed by the project; the earlier references of the subject remain below, without a new full validation of their claims in that pass.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-VIDEO-001 — Point identity is additional information across time

A collection of independent per-frame point detections does not establish which observation belongs to the same physical point. Conversely, a continuous point track does not by itself assign an action label or its start/end times. Build evaluation around the output actually needed: visibility-aware trajectories, clip class or temporal intervals. Combining these modules is a system decision and requires checking their spatial and temporal interfaces.

### CV-VIDEO-003 — Future context imposes a latency floor

At 30 frames/s, using five future frames imposes at least about 167 ms of waiting before computation and transfer. The model may be appropriate for retrospective analysis but incompatible with a tighter online decision budget. A proposed comparison reports quality versus total output delay under a common information window, including whether later frames revise earlier outputs. Timing only the network call omits the cost of waiting for its input.

### CV-VIDEO-004 — Order sensitivity should match the task labels

Opening and closing a door can share many static frames while differing in order; recognizing a sport from a field may require much less temporal evidence. A proposed controlled set includes reverse-order pairs with changed labels and static-context baselines. Shuffle invariance alone is not proof of failure on an order-insensitive task, but a high shuffled score cannot establish that the model learned the dynamics needed for an order-sensitive decision.

Consulted foundations: [CoTracker3](https://arxiv.org/html/2410.11831v1): point-track/visibility outputs, online and offline protocols.

## Sources and flashcards

### Scientific sources

- [Doersch et al. 2022, TAP-Vid](https://arxiv.org/abs/2211.03726) (v2 PDF): §3 problem formulation and Table 1, §3.1, §4.3 metrics and validation advice.
- [Karaev et al. 2024, CoTracker](https://arxiv.org/abs/2307.07635) (v3 PDF): abstract, §1, §3 task definition, §3.3 windowed inference and eq. 2, §3.4 support points, §4 benchmarks, "first" and "strided" protocols, implementation details, Table 1 caption.
- [Karaev et al. 2024, CoTracker3](https://arxiv.org/abs/2410.11831) (v1 PDF): abstract, §3.1 pseudo-labelling, §3 online and offline models, §4 evaluation protocol, Table 1.
- [Doersch et al. 2023, TAPIR](https://arxiv.org/abs/2306.08637): abstract (matching and refinement stages).
- [Carreira and Zisserman 2017, I3D](https://arxiv.org/abs/1705.07750): §2.4 inflation, boring-video fixed point, 64-frame snippets, two streams.
- [Kay et al. 2017, Kinetics](https://arxiv.org/abs/1705.06950): §2 statistics and non-exhaustive annotation.
- [Feichtenhofer et al. 2019, SlowFast](https://arxiv.org/abs/1812.03982): §3.1–3.2 ($\tau$, $\alpha$, $\beta$, cost share), §4 inference views.
- [Bertasius et al. 2021, TimeSformer](https://arxiv.org/abs/2102.05095): §3 divided space-time attention, §4 clip sampling and inference.
- [Tong et al. 2022, VideoMAE](https://arxiv.org/abs/2203.12602): abstract and §1, tube masking at 90–95%.
- [Arnab et al. 2021, ViViT](https://arxiv.org/abs/2103.15691): uniform frame sampling and tubelet embedding (§3.2, Figs. 2–3).
- [Zhang et al. 2022, ActionFormer](https://arxiv.org/abs/2202.07925): §3 task formulation, §4 tIoU and mAP, §4.1 THUMOS14.

### Implementation sources

- [facebookresearch/co-tracker at commit 82e02e8, `cotracker/predictor.py`](https://github.com/facebookresearch/co-tracker/blob/82e02e8029753ad4ef13cf06be7f4fc5facdda4d/cotracker/predictor.py): offline predictor (L14–L209), online predictor (L212–L300).

### Related flashcards and references

- [Flashcards](../102-points-actions-video.md): CV-VIDEO-001 (output contracts), CV-VIDEO-002 (short events), CV-VIDEO-003 (future frames and delay), CV-VIDEO-004 (use of temporal order).
- [CV-FLOT](101-flot-optique.md), [CV-SOT](../../110-tracking-association/references/113-tracking-monoobjet.md), [CV-PIPELINE](../../140-ingenierie-systemes/references/141-contrats-profiling-video.md), [CV-METRIQUES-TEMPS](../../130-evaluation-fiabilite/references/132-tracking-trajectoires.md).

Drafted by agent, 2026-10-18. Revision 9, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/102-points-actions-video.md).
