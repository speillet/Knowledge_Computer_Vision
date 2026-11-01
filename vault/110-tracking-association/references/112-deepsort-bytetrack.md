---
id: CV-ASSOCIATION
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-SORT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# DeepSORT, ByteTrack and multi-object association

## Problem, data and assumptions

Improve the association beyond SORT under occlusions, variable scores and appearance. Inputs: detections, timestamps, possibly embeddings and history; output: tracks with IDs according to life cycle. The quality of the detector remains crucial.

## Prerequisites and competencies

**Required prerequisites**: [CV-SORT](111-sort.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

DeepSORT combines movement, gating Mahalanobis, appearance distance and association cascade. ByteTrack first associates high score detections, then weak ones to the remaining tracks according to the method; weak ones not associated do not indiscriminately create new tracks.

## Mathematics, conventions and units

A cosine appearance distance can write $1-a^Tb$ for unit vectors. It is not the same measure as the IoU or the residual Mahalanobis of movement. Mixing their thresholds without normalization/protocol is not a justified fusion of probabilities.

## Parameters and properties

High/low thresholds, gating, appearance memory, confirmation and duration of loss. The original ReID pedestrian can transfer incorrectly to identical parts. The 3D tracking, for example AB3DMOT, additionally requires a contract of coordinate frame/box and 3D movement, not a simple renaming of the 2D tracker.

## Cost and implementation

Embeddings add extraction and memory; detector, NMS, association and transfers must be counted. No trackers executed or purported score improvements.

## Evaluation and controlled variation

Baseline SORT with fixed detector; vary occlusion and calibration of scores separately. Measure ID switches, fragments and association metrics, with split by sequence and frozen parameters.

## Failure modes and diagnosis

Traded IDs despite appearance: check ReID domains, crops, normalization and association. False tracks: inspect creation and thresholds; do not lower all thresholds without frame traces per frame.

## Alternatives and applications

Associate movement and appearance according to ambiguities; compensate ego-motion if necessary. Single object trackers and ReID alone fulfill separate contracts.

## Guided reasoning and proposed checks

These constructed cases develop gating, appearance and association of low scores. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-ASSOCIATION-001

**Question of work**: What does DeepSORT add to the association reasoning of a simple geometry-based SORT tracker?

**Reference Response**: Appearance/ReID and gating/cascade strategies, in addition to movement, according to its design.

**Reasoning for Association**: Two nearby boxes can look similar geometrically while belonging to different people. An apparent distance adds an observation that can distinguish them; movement and gating restrict plausible candidates. The cascade organizes these decisions according to the method, instead of turning the filter into identity recognition.

**Example of limit**: If the crops are small, hidden or out of the ReID training area, their embeddings can become low discriminants. Increasing their weight can then worsen the affectation. check distances from true and false pairs in the target range, then compare movement alone, appearance alone and fixed detector combination. The cost merger must have an interpretation and a protocol; a cosine proximity is not automatically a calibrated probability of being the same person, nor a guarantee after a long disappearance.

### Case linked to CV-ASSOCIATION-004

**Question of work**: How can two trackers be compared without confounding association quality with a different detector?

**Reference Response**: Fix the same detections or explicitly report the two variations; keep sequences, thresholds and time protocol.

**Proposed causal ablation**: Use a timestamped detection file common to both trackers, with the same boxes, scores, and classes. The differences of tracks then come from their temporal stages and their parameters, within the limits of this check. To compare the complete systems, then also measure each detector with its tracker.

**Example of a confusing factor**: A detector that finds a person after occlusion can improve the identity score without changing the association. Conversely, a better association can be masked by many missing boxes. Report quality of detection, identity errors, fragments, cost and birth/loss rules. Keep one split per sequence and settings frozen on the test. A fair comparison does not necessarily require a single detector for all uses, but requires to say precisely which component has changed and what can be attributed to it.

**Documentary reference for this pass**: [ByteTrack](https://arxiv.org/html/2110.06864v3), second association algorithm. The other developments are in the [flashcards](../112-deepsort-bytetrack.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-ASSOCIATION-001

**Situation**: What does DeepSORT add to the association reasoning of a simple geometry-based SORT tracker?

**Two cost geometries**: in the measurement space, $d_M^2=(z-\hat z)^TS^{-1}(z-\hat z)$ takes into account the predicted covariance $S$; for unitary embeddings, $d_C=1-a^Tb$ describes the angular deviation. The first is without unit after normalization, but does not have the same distribution or the same threshold as the second. High motion uncertainty widens plausible positions; it does not make appearance more discriminating. The waterfall also organizes the priority of the tracks according to their history. Checking costs, eligibility constraints and sequence of steps separately helps to understand what the combination actually brings.

### CV-ASSOCIATION-002

**Situation**: Does ByteTrack create a track for every low-score box?

**Two uses of score**: A threshold can be used to decide that an observation is reliable enough to initiate an identity, while allowing less confident observations to extend an already constrained track. These decisions do not have the same false positive cost. If a filter upstream of the detector removes all weak boxes, the second association no longer has the data it is supposed to exploit. So keep the contract thresholds of the entire chain, including NMS and top-k. Testing a real box whose score varies only allows to observe the transitions between priority association, recovery and rejection, without changing its geometry.

### CV-ASSOCIATION-003

**Situation**: A pretrained pedestrian DeepSORT model swaps the IDs of identical industrial parts. Which assumption should be checked?

**Test of Separability**: build positive pairs of the same piece at several moments and negative pairs of different pieces under comparable conditions. Examine their distance distributions and overlap cases, especially after occlusion. If they overlap strongly, a threshold ReID cannot simultaneously eliminate all false matches and keep all true ones. A gallery contaminated by a bad crop can also make a track permanently close to a distractor. Then check the policy of update of the embeddings, and not just their weight in the cost. Movement or marking can provide additional information that is truly observable.

### CV-ASSOCIATION-004

**Situation**: How can two trackers be compared without confounding association quality with a different detector?

**Plan factoriel minimal**: compare association A and B on the same detector D1, then repeat on D2 if we want to study their interaction. The four systems reveal whether an association gain depends on more complete boxes or differently distributed scores. Keep the validation settings separate from the final evaluation. Report loss and recovery events, because an average can hide that a method wins only on sequences without occlusion. The shared detection file must keep timestamps and frame order, including empty frames; removing them changes the time problem instead of only check upstream.

**Passages consulted for these developments**: [Wojke et al., DeepSORT](https://arxiv.org/html/1703.07402v1), §2.2, equations 1 – 4 and gating; §2.4, descriptor; [Zhang et al., ByteTrack](https://arxiv.org/html/2110.06864v3), §3, two associations and creation; built protocols; [Bewley et al., SORT](https://arxiv.org/html/1602.00763v2), §3, estimation, association and cycle; state calculations, timelines and project protocols.

## Sources and flashcards

- [SORT, §3.1 and table 1](https://arxiv.org/abs/1602.00763): effect of the detector change, motivation for the upstream check.

- [DeepSORT, §§2.1 – 2.3](https://arxiv.org/abs/1703.07402).
- [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864).
- [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
- [Related flashcards](../112-deepsort-bytetrack.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
