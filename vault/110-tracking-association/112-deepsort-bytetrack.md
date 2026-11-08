# Flashcards — DeepSORT, ByteTrack and multi-object association

reference note: [[110-tracking-association/references/112-deepsort-bytetrack|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-ASSOCIATION-001

Objective: Identify the addition of DeepSORT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-001
Question: What does DeepSORT add to the association reasoning of a simple geometry-based SORT tracker?
Reponse: **Expected answer**: Appearance/ReID and gating/cascade strategies, in addition to movement, according to its design.

**Further explanation**: An embedding does not eliminate bad detection or ambiguity and must be validated in the target domain.

**Reasoning for Association**: Two nearby boxes can look similar geometrically while belonging to different people. An apparent distance adds an observation that can distinguish them; movement and gating restrict plausible candidates. The cascade organizes these decisions according to the method, instead of turning the filter into identity recognition.

**Example of limit**: If the crops are small, hidden or out of the ReID training area, their embeddings can become low discriminants. Increasing their weight can then worsen the affectation. check distances from true and false pairs in the target range, then compare movement alone, appearance alone and fixed detector combination. The cost merger must have an interpretation and a protocol; a cosine proximity is not automatically a calibrated probability of being the same person, nor a guarantee after a long disappearance.

**Two cost geometries**: in the measurement space, $d_M^2=(z-\hat z)^TS^{-1}(z-\hat z)$ takes into account the predicted covariance $S$; for unitary embeddings, $d_C=1-a^Tb$ describes the angular deviation. The first is without unit after normalization, but does not have the same distribution or the same threshold as the second. High motion uncertainty widens plausible positions; it does not make appearance more discriminating. The waterfall also organizes the priority of the tracks according to their history. Checking costs, eligibility constraints and sequence of steps separately helps to understand what the combination actually brings.

**An older covariance can make motion distance smaller**: An old uncorrected track may have large predicted covariance, giving a small Mahalanobis distance to many detections despite weak identity evidence. Appearance and the cascade alter how those candidates compete with recently observed tracks. A small normalized motion residual is therefore not equivalent to a close or trustworthy physical match. Evaluate crossings and long occlusions separately, with descriptor domain and crop quality held fixed.

**Blocking errors**: Present any proximity of appearance as true identity.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [DeepSORT, §§2.1 – 2.3: Mahalanobis, appearance and waterfall](https://arxiv.org/abs/1703.07402); [Wojke et al., DeepSORT, §2.2, equations 1 – 4 and gating; §2.4, descriptor](https://arxiv.org/html/1703.07402v1), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-ASSOCIATION-001 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-002

Objective: understand the use of low scores ByteTrack. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-002
Question: Does ByteTrack create a track for every low-score box?
Reponse: **Expected answer**: No: it first exploits high scores, then tries to recover weak observations for the remaining tracks; the weak not associated are rejected according to the pipeline.

**Further explanation**: Check version and life cycle; keeping weak observations is not accepting indiscriminately all false positives.

**Why keep some boxes weak**: A partially obscured target can remain visible while achieving a low detector score. Systematically deleting these observations cuts a track that could have been extended thanks to its history. The second association seeks to retrieve this information among the tracks still candidates.

**Product Compromise**: A weak box can also be a false positive. Linking it to an existing track under given rules is not the same decision as creating a new identity without a history. Trace the two steps and thresholds in the version used. In a built test, vary the score of a real hidden box, with fixed location, and then introduce false boxes. Measure continuity and false tracks together. The title of the method does not mean that any box, regardless of its score and context, becomes a new track.

**Two uses of score**: A threshold can be used to decide that an observation is reliable enough to initiate an identity, while allowing less confident observations to extend an already constrained track. These decisions do not have the same false positive cost. If a filter upstream of the detector removes all weak boxes, the second association no longer has the data it is supposed to exploit. So keep the contract thresholds of the entire chain, including NMS and top-k. Testing a real box whose score varies only allows to observe the transitions between priority association, recovery and rejection, without changing its geometry.

**Birth and continuation use different evidence**: A weak box consistent with an existing predicted trajectory has temporal support that the same isolated weak box lacks. ByteTrack uses that distinction to recover some observations without starting an identity from every low-confidence detection. A proposed ablation keeps the detector and first-stage matches fixed, then measures recovered true continuations and false continuations from the second stage. The phrase every detection is not a guarantee that all low scores are retained.

**Blocking errors**: Assimilate the second association to a massive creation of weak tracks.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [ByteTrack, §3 Algorithm 1: two associations and creation from the remaining high scores](https://arxiv.org/abs/2110.06864); [Zhang et al., ByteTrack, §3, two associations and creation; built protocols](https://arxiv.org/html/2110.06864v3), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-ASSOCIATION-002 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-003

Objective: check the transfer ReID. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-003
Question: A pretrained pedestrian DeepSORT model swaps the IDs of identical industrial parts. Which assumption should be checked?
Reponse: **Expected answer**: Discrimination and the field of embeddings, as well as the quality of the crops and physical ambiguities of the parts.

**Further explanation**: Compare movement alone, appearance and combination on annotated sequences; no information on appearance distinguishes two visually identical objects in principle.

**Two possible ambiguities**: embedding can transfer from a pedestrian domain to parts incorrectly, but parts can also be truly indistinguishable in the image. In the second case, changing the network does not create missing visual information. Movement, cadence, or a distinctive marker may be necessary to reduce ambiguity.

**Survey built**: preserve detections and compare distributions of distances for the same and different parts, with their crops. Check for resolution, normalization, and occlusion, and then compare associations without appearance and with multiple weights. Examine crossover sequences rather than an average embedding score. A gain on isolated images does not prove identity continuity during a contact or a occlusion. If there are no observations, report uncertainty instead of presenting the ID as certain.

**Test of Separability**: build positive pairs of the same piece at several moments and negative pairs of different pieces under comparable conditions. Examine their distance distributions and overlap cases, especially after occlusion. If they overlap strongly, a threshold ReID cannot simultaneously eliminate all false matches and keep all true ones. A gallery contaminated by a bad crop can also make a track permanently close to a distractor. Then check the policy of update of the embeddings, and not just their weight in the cost. Movement or marking can provide additional information that is truly observable.

**Some identities are visually unobservable**: If two parts are truly indistinguishable in the available crops, no appearance distance can recover their identity through an unobserved exchange on appearance alone. Motion constraints, process order or an additional marker may supply evidence if the application permits it. Distinguish this ambiguity from domain shift of a pedestrian-trained embedding using controlled same-part/different-part pairs. Retraining cannot be assumed to create a cue absent from the sensor data.

**Blocking errors**: Blindly increase the weight ReID.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; Transfer diagnosis built by the project; [DeepSORT, §2.4: pedestrian appearance model](https://arxiv.org/abs/1703.07402); [Wojke et al., DeepSORT, §2.2, equations 1 – 4 and gating; §2.4, descriptor](https://arxiv.org/html/1703.07402v1), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-ASSOCIATION-003 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-004

Objective: separate detector and association. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-004
Question: How can two trackers be compared without confounding association quality with a different detector?
Reponse: **Expected answer**: Fix the same detections or explicitly report the two variations; keep sequences, thresholds and time protocol.

**Further explanation**: Measure tracks quality and total cost; AP detector and identity score answer two questions.

**Proposed causal ablation**: Use a timestamped detection file common to both trackers, with the same boxes, scores, and classes. The differences of tracks then come from their temporal stages and their parameters, within the limits of this check. To compare the complete systems, then also measure each detector with its tracker.

**Example of a confusing factor**: A detector that finds a person after occlusion can improve the identity score without changing the association. Conversely, a better association can be masked by many missing boxes. Report quality of detection, identity errors, fragments, cost and birth/loss rules. Keep one split per sequence and settings frozen on the test. A fair comparison does not necessarily require a single detector for all uses, but requires to say precisely which component has changed and what can be attributed to it.

**Plan factoriel minimal**: compare association A and B on the same detector D1, then repeat on D2 if we want to study their interaction. The four systems reveal whether an association gain depends on more complete boxes or differently distributed scores. Keep the validation settings separate from the final evaluation. Report loss and recovery events, because an average can hide that a method wins only on sequences without occlusion. The shared detection file must keep timestamps and frame order, including empty frames; removing them changes the time problem instead of only check upstream.

**Association changes can interact with score calibration**: Fixing detections must include coordinates, scores, timestamps, classes and ordering, since two-stage association and track creation may use the scores differently. An association method that improves with one detector's score distribution may not improve identically with another. Compare a factorial detector/association design when that interaction matters, and include full latency. A fixed detection count alone does not establish a controlled association comparison.

**Blocking errors**: Assign any final gain to the tracker without check upstream.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; Comparison protocol proposed by the project; [SORT, §3.1 and table 1: effect of the detector](https://arxiv.org/abs/1602.00763); [Bewley et al., SORT, §3, estimation, association and cycle; state calculations, timelines and project protocols](https://arxiv.org/html/1602.00763v2), see the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-ASSOCIATION-004 provenance::agent pole::C pole::D pole::E
END
