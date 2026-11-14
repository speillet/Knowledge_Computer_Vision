# Flashcards — DeepSORT, ByteTrack and multi-object association

reference note: [[110-tracking-association/references/112-deepsort-bytetrack|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-ASSOCIATION-001

Objective: Identify the addition of DeepSORT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-001
Question: What does DeepSORT add to the association reasoning of a simple geometry-based SORT tracker?
Reponse: **Expected answer**: Appearance (ReID) descriptors, a motion gate and a matching cascade, in addition to SORT's motion prediction.

**Further explanation**: An embedding removes neither bad detections nor ambiguity and must be validated in the target domain.

**Reasoning about association**: Two nearby boxes can be geometrically similar while belonging to different people. An appearance distance adds an observation that can distinguish them; motion and gating restrict the plausible candidates. The cascade orders these decisions as the method specifies, instead of turning the filter into identity recognition.

**Example of a limit**: If the crops are small, occluded or outside the ReID training domain, their embeddings can become weakly discriminative. Increasing their weight can then worsen the assignment. Check the distances of true and false pairs in the target domain, then compare motion alone, appearance alone and their combination with the detector fixed. The cost fusion must have an interpretation and a protocol; a small cosine distance is not automatically a calibrated probability of being the same person, nor a guarantee after a long disappearance.

**Two cost geometries**: In measurement space, $d_M^2=(z-\hat z)^TS^{-1}(z-\hat z)$ accounts for the predicted covariance $S$; for unit-norm embeddings, $d_C=1-a^Tb$ describes the angular deviation. The first is unitless after normalization, but has neither the distribution nor the threshold of the second. A large motion uncertainty widens the plausible positions; it does not make appearance more discriminative. The cascade also orders the priority of tracks according to their history. Checking costs, admissibility constraints and the order of stages separately shows what the combination actually contributes.

**An older covariance can make motion distance smaller**: An old uncorrected track may have large predicted covariance, giving a small Mahalanobis distance to many detections despite weak identity evidence. Appearance and the cascade alter how those candidates compete with recently observed tracks. A small normalized motion residual is therefore not equivalent to a close or trustworthy physical match. Evaluate crossings and long occlusions separately, with descriptor domain and crop quality held fixed.

**Blocking errors**: Presenting any appearance similarity as the true identity.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [Wojke et al. 2017, DeepSORT, §2.2 eqs. 1–6 and §2.3 matching cascade](https://arxiv.org/abs/1703.07402); [deep_sort tracker.py at f08cf1d, _match L93–L131](https://github.com/nwojke/deep_sort/blob/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab/deep_sort/tracker.py#L93-L131). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-ASSOCIATION-001 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-002

Objective: Understand ByteTrack's use of low scores. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-002
Question: Does ByteTrack create a track for every low-score box?
Reponse: **Expected answer**: No: it first associates high-score boxes, then tries to recover low-score observations for the remaining tracks; unmatched low-score boxes are discarded as background.

**Further explanation**: Check the version and the life cycle; keeping low-score observations does not mean accepting every false positive. In the official code a new track also needs a score at least 0.1 above the high-score threshold.

**Why keep some low-score boxes**: A partially occluded target can remain visible while receiving a low detector score. Deleting these observations systematically breaks a track that its history could have extended. The second association recovers this information for the tracks that are still candidates.

**Product trade-off**: A low-score box can also be a false positive. Linking it to an existing track under given rules is not the same decision as creating a new identity without history. Trace the two steps and the thresholds in the version used. In a constructed test, vary the score of a real occluded box with a fixed location, then introduce false boxes. Measure continuity and false tracks together. The method's title does not mean that every box, whatever its score and context, becomes a new track.

**Two uses of the score**: A threshold can decide that an observation is reliable enough to start an identity, while less confident observations may extend an already constrained track. These decisions do not have the same false-positive cost. If a filter between the detector and the tracker removes every low-score box, the second association no longer has the data it is meant to exploit. Keep the thresholds of the whole chain in the contract, including NMS and top-k. Varying only the score of a real box, without changing its geometry, shows the transitions between priority association, recovery and rejection.

**Birth and continuation use different evidence**: A weak box consistent with an existing predicted trajectory has temporal support that the same isolated weak box lacks. ByteTrack uses that distinction to recover some observations without starting an identity from every low-confidence detection. A proposed ablation keeps the detector and first-stage matches fixed, then measures recovered true continuations and false continuations from the second stage. The phrase "every detection box" is not a guarantee that all low scores are retained.

**Blocking errors**: Equating the second association with mass creation of tracks from low-score boxes.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [Zhang et al. 2022, ByteTrack, §3 and Algorithm 1](https://arxiv.org/abs/2110.06864); [ByteTrack byte_tracker.py at d1bf019, score split, second association and track creation, L177–L268](https://github.com/ifzhang/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py#L177-L268). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-ASSOCIATION-002 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-003

Objective: Check ReID transfer. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-003
Question: A pretrained pedestrian DeepSORT model swaps the IDs of identical industrial parts. Which assumption should be checked?
Reponse: **Expected answer**: The discriminative power and training domain of the embeddings, as well as crop quality and the physical ambiguity of the parts.

**Further explanation**: Compare motion alone, appearance alone and their combination on annotated sequences; in principle, no appearance information distinguishes two visually identical objects.

**Two possible ambiguities**: An embedding can transfer poorly from a pedestrian domain to parts, but the parts can also be truly indistinguishable in the image. In the second case, changing the network does not create missing visual information. Motion, frame rate or a distinctive marker may be needed to reduce the ambiguity.

**Constructed investigation**: Keep the detections fixed and compare the distance distributions for same and different parts, with their crops. Check resolution, normalization and occlusion, then compare associations without appearance and with several weights. Examine crossing sequences rather than an average embedding score. A gain on isolated images does not prove identity continuity during a contact or an occlusion. Where observations are missing, report the uncertainty instead of presenting the ID as certain.

**Separability test**: Build positive pairs of the same part at several times and negative pairs of different parts under comparable conditions. Examine their distance distributions and overlapping cases, especially after occlusion. If they overlap strongly, no ReID threshold can remove every false match while keeping every true one. A gallery contaminated by a bad crop can also keep a track permanently close to a distractor. Then check the update policy of the embeddings, not just their weight in the cost. Motion or marking can provide additional, truly observable information.

**Some identities are visually unobservable**: If two parts are truly indistinguishable in the available crops, no appearance distance can recover their identity through an unobserved exchange on appearance alone. Motion constraints, process order or an additional marker may supply evidence if the application permits it. Distinguish this ambiguity from domain shift of a pedestrian-trained embedding using controlled same-part/different-part pairs. Retraining cannot be assumed to create a cue absent from the sensor data.

**Blocking errors**: Blindly increasing the ReID weight.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [Wojke et al. 2017, DeepSORT, §2.2 appearance threshold tuned on separate data and §2.4 pedestrian re-identification training data](https://arxiv.org/abs/1703.07402). The transfer diagnosis is a project construction.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-ASSOCIATION-003 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-004

Objective: separate detector and association. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-ASSOCIATION-004
Question: How can two trackers be compared without confounding association quality with a different detector?
Reponse: **Expected answer**: Fix the same detections or explicitly report the two variations; keep sequences, thresholds and time protocol.

**Further explanation**: Measure track quality and total cost; detector AP and identity scores answer two different questions.

**Proposed causal ablation**: Use a timestamped detection file shared by both trackers, with the same boxes, scores and classes. The differences in tracks then come from their temporal stages and parameters, within the limits of this control. To compare complete systems, also measure each detector with its own tracker.

**Example of a confounding factor**: A detector that finds a person after occlusion can improve the identity score without any change in the association. Conversely, a better association can be masked by many missing boxes. Report detection quality, identity errors, fragmentations, cost and the birth and loss rules. Keep a split by sequence and settings frozen before the test. A fair comparison does not necessarily require a single detector for every use, but it requires stating precisely which component changed and what can be attributed to it.

**Minimal factorial design**: Compare associations A and B on the same detector D1, then repeat on D2 to study their interaction. The four systems show whether an association gain depends on more complete boxes or on differently distributed scores. Keep validation settings separate from the final evaluation. Report loss and recovery events, because an average can hide that a method wins only on sequences without occlusion. The shared detection file must keep timestamps and frame order, including empty frames; removing them changes the temporal problem instead of only controlling the upstream stage.

**Association changes can interact with score calibration**: Fixing detections must include coordinates, scores, timestamps, classes and ordering, since two-stage association and track creation may use the scores differently. An association method that improves with one detector's score distribution may not improve identically with another. Compare a factorial detector/association design when that interaction matters, and include full latency. A fixed detection count alone does not establish a controlled association comparison.

**Blocking errors**: Attributing any final gain to the tracker without controlling the upstream stages.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Full reference]]; [Bewley et al. 2016, SORT, §3.1 and Table 1, effect of the detector](https://arxiv.org/abs/1602.00763); [Zhang et al. 2022, ByteTrack, §4.2, association methods compared on the same detections](https://arxiv.org/abs/2110.06864). The comparison protocol is a project proposal.
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-ASSOCIATION-004 provenance::agent pole::C pole::D pole::E
END
