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

**Further explanation**: Neither targets nor metrics are interchangeable. Name the version and access to the future.

**Contracts to distinguish**: A point path answers “where is this observation over time?” A music video label answers “what action characterizes this excerpt?”. A time interval adds a start and end estimate. One output may be correct for one of these contracts and insufficient for another.

**Constructed example**: recognizing that a person sits in a clip does not necessarily provide the instant of contact with the chair. Following a garment point also does not automatically provide the action class. Define the useful output before choosing architecture and metric: point error, visibility, classification, or time boundaries. Specify the frames accessible to the model and the decision time. A performance obtained with the full clip does not validate an alarm to be triggered before the end of the event.

**Axis of annotations**: A point path can be represented by $(x_t,y_t,v_t)$, where $v_t$ describes a visibility according to the protocol. A clip label is a category associated with a window; a time location provides at least one category and an interval $[t_d,t_f]$. Cutting a long video into tagged clips can give rough time cues, but does not automatically create precise boundaries. To compare systems, keep timestamps and match rules with actual events. A point followed on a person is neither a complete identity of the person nor an annotation of action without an additional definition.

**Blocking errors**: Deducing the boundaries of an action from a single music video label.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [CoTracker, §3: trajectories and visibility](https://arxiv.org/abs/2307.07635); [TimeSformer, summary](https://arxiv.org/abs/2102.05095); label/interval distinction: project contract.
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-VIDEO-001 provenance::agent pole::D
END

## CV-VIDEO-002

Objective: Test the loss of short events. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-002
Question: A video is summarized with one frame per second. Why can detection of a 100 ms event not be guaranteed?
Reponse: **Expected answer**: The event can occur entirely between two sampled frames.

**Further explanation**: Test phases, cadence and windows with reference; the model cannot observe information never sampled directly.

**Exemple temporel**: if the observations are taken at the instants 0 s and 1 s, an event present only from 0,35 to 0,45 s does not appear in any frame retained. It may eventually leave clues before or after, but that would be another hypothesis than direct observation of the event.

**Proposed design**: Set the minimum useful event duration and delay tolerance, and then compare multiple sampling phases, not just a favorable video. Check if a cadence increase, window, or event trigger provides the necessary information. Memory and cost increase with processed observations. A more powerful time model can exploit the available data; it does not guarantee to reconstruct an invisible event without additional assumptions. The protocol must therefore separate observed event, inferred event and missed event.

**Sampling phase**: In a constructed model where an event of duration $d<\Delta$ begins with a uniform phase with respect to a grid of steps $\Delta$, and where an instantaneous capture is sufficient, the probability that at least one sample falls into the event is $d/\Delta$. For 100 ms and a step of 1 s, it is 0,1 under these assumptions. This is not a predicted performance of a real model: exposure, visibility, and persistent clues change the problem. The calculation shows, however, why varying the phase is essential and why a demonstration where the event falls exactly on a frame does not validate a guaranteed recall.

**Blocking errors**: Assuming that a larger model guarantees the recall of any short event.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; Time counter-example built in the reference note: event between two sampled moments; [CoTracker, §3](https://arxiv.org/abs/2307.07635) for the context of discrete video inputs, without attribution of the counter-example to this article.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-VIDEO-002 provenance::agent pole::D
END

## CV-VIDEO-003

Objective: check causation and delay. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-003
Question: A point tracker uses a window containing future frames. Can its output be compared directly with a zero-delay causal model?
Reponse: **Expected answer**: Not without specifying the available information and the time to exit.

**Further explanation**: Evaluate same window, timestamps, visibility policy and decision time.

**Fairness of comparison**: A future frame can help solve a occlusion or an ambiguous movement. This information does not yet exist for a system that needs to respond immediately. An offline or windowed method can therefore accomplish a more informed task, at the cost of a delay.

**Protocol built**: For each output, note the instant of the estimated point, the last frame consumed and the instant of availability. Compare accuracy and delay with an identical policy of observations, or explicitly present the difference as a compromise. Include window wait, transfer, and calculation in latency. The term online can mean progressive processing of a stream without meaning zero delay. A good trajectory calculated after the event is not equivalent to a location early enough to drive another module. This distinction also applies to VIO valuations, smoothing and stock detection.

**Minimum time for context**: if an estimate for $t$ uses a frame at $t+h$, its availability cannot precede $t+h$, even before transfer and calculation. A latency measurement limited to the network pass would therefore omit at least this context delay. With sliding windows, specify which exits are temporary and which are revised afterwards. Evaluating the first decision and the final trajectory separately makes the comparison readable. A method can remain useful in line with an accepted deadline; the word causal, on the other hand, requires that each decision at the time in question uses only the observations already available according to the announced contract.

**Blocking errors**: Confound online word and lack of latency or future in any implementation.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; [CoTracker, §3: sliding windows](https://arxiv.org/abs/2307.07635); [CoTracker3, introduction : variantes online/offline](https://arxiv.org/abs/2410.11831); latency comparison proposed by the project.
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-VIDEO-003 provenance::agent pole::D
END

## CV-VIDEO-004

Objective: check the use of the time order. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-VIDEO-004
Question: A video classifier still recognizes an action after the frames are shuffled. What should be tested before claiming it understands temporal dynamics?
Reponse: **Expected answer**: Compare to an image/context baseline, check labels and actions that actually require order.

**Further explanation**: The scene or object may be sufficient for the score; use cases where the order distinguishes two events.

**Alternative Hypothesis**: The presence of a tool, a decor or a characteristic posture can be enough to predict the label of the clip. Frame swapping preserves many of these clues. A high accuracy does not, therefore, alone allow to attribute the decision to the temporal order.

**Proposed ablation**: Compare the model to an aggregation of image predictions, and then select cases where the same visual states in a different order correspond to different events. check sampling, labels, background and leakage between neighboring clips. If the performance remains the same on tasks that are really sensitive to order, look at the information used. A fall after permutation sustains a temporal dependence, but does not prove any form of causal understanding. Reasoning must remain tied to the tasks and controls performed, not just in the name of the architecture.

**Permutation and reverse order**: An average $z=L^{-1}\sum_t f(I_t)$ aggregation is mathematically invariant to permutation; a good score obtained in this way can come from visual states or context, without encoding their order. Building pairs like take/pose an object, with close states but a different order, tests another property. check also that permutation does not create an unusual artifact that would cause the model to fall for the wrong reason. Comparing inversion, permutation and cadence by changing only one factor helps to support the use of time without assimilating any temporal sensitivity to a complete understanding of the scene.

**Blocking errors**: Deduct a temporal understanding of a global accuracy alone.
Source: [[100-mouvement-video/references/102-points-actions-video|Full reference]]; Controlled test proposed by the project; [TimeSformer, summary and architecture](https://arxiv.org/abs/2102.05095) for the temporal attention mechanism.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-VIDEO-004 provenance::agent pole::D
END
