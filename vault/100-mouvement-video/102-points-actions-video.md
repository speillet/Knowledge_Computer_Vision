# Flashcards — Point tracking, actions and video understanding

reference note: [[100-mouvement-video/references/102-points-actions-video|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-VIDEO-001

Objective: Choose the right video output. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-001
Question: How do CoTracker, video classification and temporal action localization differ?
Reponse: **Expected answer**: CoTracker tracks points with visibility; classification labels a clip; localization also estimates time intervals.

**Further explanation**: Neither the targets nor the metrics are interchangeable. Name the model version and its access to future frames.

**Contracts to distinguish**: A point track answers "where is this observation over time?" A clip label answers "what action characterizes this excerpt?". A time interval adds a start and end estimate. One output may be correct for one of these contracts and insufficient for another.

**Constructed example**: Recognizing that a person sits down in a clip does not necessarily give the instant of contact with the chair. Tracking a point on a garment does not automatically give the action class either. Define the useful output before choosing the architecture and the metric: point error, visibility, classification or time boundaries. Specify the frames available to the model and the decision time. A performance obtained with the full clip does not validate an alarm that must fire before the end of the event.

**Annotation axes**: A point track can be represented by $(x_t,y_t,v_t)$, where $v_t$ describes visibility under the protocol. A clip label is a category associated with a window; temporal localization provides at least one category and an interval $[t_d,t_f]$. Cutting a long video into labeled clips can give rough temporal cues, but does not automatically create precise boundaries. To compare systems, keep the timestamps and the rules for matching predictions with actual events. A point tracked on a person is neither a complete identity of that person nor an action annotation without an additional definition.

**Point identity is additional information across time**: A collection of independent per-frame point detections does not establish which observation belongs to the same physical point. Conversely, a continuous point track does not by itself assign an action label or its start/end times. Build evaluation around the output actually needed: visibility-aware trajectories, clip class or temporal intervals. Combining these modules is a system decision and requires checking their spatial and temporal interfaces.

**Blocking errors**: Deducing the boundaries of an action from a single clip label.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [Doersch et al. 2022, TAP-Vid, §3 task formulation and §4.3 metrics](https://arxiv.org/abs/2211.03726); [Karaev et al. 2024, CoTracker, §3 tracks and visibility](https://arxiv.org/abs/2307.07635); [Zhang et al. 2022, ActionFormer, §3 onset, offset and label](https://arxiv.org/abs/2202.07925). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-VIDEO-001 provenance::agent pole::D
END

## CV-VIDEO-002

Objective: Test the loss of short events. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-002
Question: A video is summarized with one frame per second. Why can detection of a 100 ms event not be guaranteed?
Reponse: **Expected answer**: The event can occur entirely between two sampled frames.

**Further explanation**: Test sampling phases, frame rates and windows against a reference; the model cannot observe information that was never sampled.

**Temporal example**: If the observations are taken at 0 s and 1 s, an event present only from 0.35 to 0.45 s appears in no retained frame. It may leave cues before or after, but using them is a different hypothesis from a direct observation of the event.

**Proposed design**: Set the minimum useful event duration and the delay tolerance, then compare several sampling phases, not just one favorable video. Check whether a higher frame rate, a window or an event trigger provides the necessary information. Memory and cost grow with the number of processed observations. A more powerful temporal model can exploit the available data; it cannot reconstruct an unseen event without additional assumptions. The protocol must therefore separate observed, inferred and missed events.

**Sampling phase**: In a constructed model where an event of duration $d<\Delta$ starts at a uniformly distributed phase with respect to a sampling grid of step $\Delta$, and where an instantaneous capture is sufficient, the probability that at least one sample falls inside the event is $d/\Delta$. For 100 ms and a step of 1 s, it is 0.1 under these assumptions. This is not a predicted performance of a real model: exposure, visibility and persistent cues change the problem. The calculation shows, however, why varying the phase is essential and why a demonstration where the event falls exactly on a frame does not validate guaranteed recall.

**Published video models sample sparsely too** (same model, recomputed in the check script of this pass): at 30 frames/s, TimeSformer's default clip of 8 frames "sampled at a rate of 1/32" [§4] has a step of 1.067 s and samples a 100 ms event with probability 0.094. SlowFast's Slow pathway keeps "one out of $\tau$ frames" with $\tau=16$ [§3.1], a 0.533 s step and a probability of 0.19. Its Fast pathway, $\alpha=8$ times denser [§3.2], steps every 66.7 ms and always catches the event. The sampling step decides what a model can see, not its size or its name.

**Persistence rules and averaged summaries** (constructed): an event of duration $d$ receives either $\lfloor d/\Delta\rfloor$ or $\lceil d/\Delta\rceil$ samples, the larger number with probability equal to the fractional part of $d/\Delta$. At 25 frames/s, a 100 ms event gets 2 or 3 frames with equal probability, so a rule that requires 3 consecutive detections misses it half the time, even with a perfect detector. A summary that averages each second instead of picking one frame always keeps a trace, but at $d/\Delta=10\%$ of its contrast: a 50 grey-level flash becomes 5 grey levels, possibly below the noise. Decimation loses the event with probability 0.9; averaging dilutes it tenfold.

**Blocking errors**: Assuming that a larger model guarantees the recall of any short event.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [Bertasius et al. 2021, TimeSformer, §4: 8 frames sampled at a rate of 1/32](https://arxiv.org/abs/2102.05095); [Feichtenhofer et al. 2019, SlowFast, §3.1 temporal stride of the Slow pathway, §3.2 Fast pathway with $\alpha=8$](https://arxiv.org/abs/1812.03982). The counter-example, the $d/\Delta$ model, the sample counts and the averaging case are project constructions.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-VIDEO-002 provenance::agent pole::D
END

## CV-VIDEO-003

Objective: Check causality and delay. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-003
Question: A point tracker uses a window containing future frames. Can its output be compared directly with a zero-delay causal model?
Reponse: **Expected answer**: Not without specifying the available information and the output time.

**Further explanation**: Evaluate with the same window, timestamps, visibility policy and decision time.

**Fairness of comparison**: A future frame can help resolve an occlusion or an ambiguous motion. This information does not yet exist for a system that must respond immediately. An offline or windowed method therefore solves a better-informed task, at the cost of a delay.

**Constructed protocol**: For each output, record the time of the estimated point, the last frame consumed and the time the output becomes available. Compare accuracy and delay under an identical observation policy, or present the difference explicitly as a trade-off. Include the window wait, transfer and computation in the latency. The term online can mean progressive processing of a stream without meaning zero delay. A good trajectory computed after the event is not equivalent to a localization early enough to drive another module. The same distinction applies to VIO estimates, smoothing and action detection.

**Minimum delay for context**: If an estimate for $t$ uses a frame at $t+h$, it cannot be available before $t+h$, even before transfer and computation. A latency measurement limited to the network pass would therefore omit at least this context delay. With sliding windows, specify which outputs are provisional and which are revised afterwards. Evaluating the first decision and the final trajectory separately makes the comparison readable. A method can remain useful online within an accepted delay; the word causal, however, requires that each decision at a given time uses only the observations already available under the stated contract.

**Future context imposes a latency floor**: At 30 frames/s, using five future frames imposes at least about 167 ms of waiting before computation and transfer. The model may be appropriate for retrospective analysis but incompatible with a tighter online decision budget. A proposed comparison reports quality versus total output delay under a common information window, including whether later frames revise earlier outputs. Timing only the network call omits the cost of waiting for its input.

**Blocking errors**: Equating the word online with zero latency and no use of future frames in every implementation.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [Karaev et al. 2024, CoTracker, abstract and §3.3 windowed inference](https://arxiv.org/abs/2307.07635); [Karaev et al. 2024, CoTracker3, §3 online and offline variants](https://arxiv.org/abs/2410.11831). The latency comparison is a project protocol; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-VIDEO-003 provenance::agent pole::D
END

## CV-VIDEO-004

Objective: Check the use of temporal order. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-004
Question: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?
Reponse: **Expected answer**: Compare to an image/context baseline, check labels and actions that actually require order.

**Further explanation**: The scene or an object may be enough for the score; use cases where the order distinguishes two events.

**Alternative hypothesis**: The presence of a tool, a setting or a characteristic posture can be enough to predict the clip label. Shuffling frames preserves many of these cues. A high accuracy alone therefore does not allow attributing the decision to temporal order.

**Proposed ablation**: Compare the model with an aggregation of image predictions, then select cases where the same visual states in a different order correspond to different events. Check sampling, labels, background and leakage between neighboring clips. If the performance stays the same on tasks that really depend on order, examine which information is used. A drop after permutation supports a temporal dependence, but does not prove any form of causal understanding. The reasoning must stay tied to the tasks and controls performed, not to the name of the architecture.

**Permutation and reverse order**: An average aggregation $z=L^{-1}\sum_t f(I_t)$ is mathematically invariant to permutation; a good score obtained this way can come from visual states or context without encoding their order. Building pairs such as picking up and putting down an object, with similar states in a different order, tests another property. Also check that permutation does not create an unusual artifact that makes the score drop for the wrong reason. Comparing reversal, permutation and frame rate while changing only one factor helps to establish the use of time, without equating any temporal sensitivity with a complete understanding of the scene.

**Order sensitivity should match the task labels**: Opening and closing a door can share many static frames while differing in order; recognizing a sport from a field may require much less temporal evidence. A proposed controlled set includes reverse-order pairs with changed labels and static-context baselines. Shuffle invariance alone is not proof of failure on an order-insensitive task, but a high shuffled score cannot establish that the model learned the dynamics needed for an order-sensitive decision.

**Blocking errors**: Inferring temporal understanding from global accuracy alone.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [Bertasius et al. 2021, TimeSformer, §3: space-only attention degrades where strong temporal modeling is necessary](https://arxiv.org/abs/2102.05095); [Carreira and Zisserman 2017, I3D, §2.4 boring-video fixed point](https://arxiv.org/abs/1705.07750). The controlled test is a project proposal.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-VIDEO-004 provenance::agent pole::D
END
