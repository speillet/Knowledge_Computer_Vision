# Flashcards — Single-object tracking: correlation, Siamese networks and MeanShift

reference note: [[110-tracking-association/references/113-tracking-monoobjet|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-SOT-001

Objective: distinguish SOT and MOT. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SOT-001
Question: Why does an initialized single-object tracker not directly replace multi-object tracking of every person in a scene?
Reponse: **Expected answer**: It starts from a provided target and must relocate it; MOT also manages multiple detections, association, creations and disappearances.

**Further explanation**: Entries and ratings differ, although some matching components may be shared.

**Difference of problem**: A target provided in the first frame gives the tracker initialization information that a multi-object system must often discover. The MOT must also decide which objects enter or exit, prevent several tracks from representing the same object, and maintain identities despite interactions.

**Constructed example**: Launching a single-object tracker on a person does not automatically identify a second person who enters later. Launching multiple instances can help locate initialized targets, but does not solve their identity collisions, creations, and duplicate removal alone. Set the entries and expected events before choosing architecture. Metrics must also reflect this contract: accuracy conditioned to a favorable manual initialization is not directly comparable to an evaluation where all targets must be discovered automatically.

**Multi-tracking and exclusivity**: Multiple independent single-object trackers can converge on the same distractor, each satisfying its own local maximum. They do not necessarily have a common constraint preventing two IDs from representing the same object. A MOT must also define what new observations create a track and how to avoid duplicates. Launching N copies of an initialized tracker is therefore a possible brick, not a complete resolution of these decisions. In a constructed trial, crossing two similar targets and then introducing a third uninitialized target reveals both association ambiguity, exclusivity and birth management.

**Blocking errors**: Assume that following a box resolves the management of all identities.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Full reference]]; [SiamFC, introduction and §4: initialized target](https://arxiv.org/abs/1606.09549); [SORT, §3: multi-object life cycle](https://arxiv.org/abs/1602.00763); [Bertinetto et al., SiamFC, §4, unupdated template and confusions; interpolation and built multi-target cases](https://arxiv.org/html/1606.09549v2), see 2026-10-30.
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-SOT-001 provenance::agent pole::C pole::D pole::E
END

## CV-SOT-002

Objective: understand a template drift. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SOT-002
Question: During occlusion, a distractor replaces the target in the tracker's template. Which mechanism can reinforce this error?
Reponse: **Expected answer**: The update of the model on a poorly associated observation can strengthen the distractor and increase drift.

**Further explanation**: Test freeze under uncertainty, loss policy and reset on reserved sequences.

**Drift Loop**: The model learns the appearance of the region he believes to be the target. If the localization becomes false and then serves as a new supervision, the error is integrated into the model; the following frames can then favor the distractor even more. A faster adaptation sometimes strengthens this loop instead of correcting it.

**check**: Record the crops used for the update, answers and loss decisions. Compare a freeze policy under uncertainty to the initial policy, with the same sequences and initialization. Also check the return of the target after occlusion. The gel may protect the model but does not guarantee re-detection if the target exits the search region. This mechanism is for variants that update their template; it should not be assigned indiscriminately to any Siamese tracker or to any fixed template.

**Memory of an update**: For an interpolated model $m_t=(1-\eta)m_{t-1}+\eta\hat m_t$, the contribution of an erroneous observation then persists with a $\eta(1-\eta)^k$ factor after $k$ correct updates, in this simplified scheme. A large $\eta$ adapts quickly but integrates more the first error; a small $\eta$ protects better and follows less quickly a legitimate change. This formula describes an interpolation model, not all tracker variants. Examining regions that are actually learned and freezing rules can test for contamination; a fixed template can still be wrong on a distractor without following that wrong learning loop.

**Blocking errors**: Interpret each update as an automatic model enhancement.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Full reference]]; Deduction on an erroneous update of the model, for example the [KCF pipeline with interpolation](https://arxiv.org/abs/1404.7584); [SiamFC §4](https://arxiv.org/abs/1606.09549) keeps its template fixed and does not illustrate this mechanism; [Bertinetto et al., SiamFC, §4, unupdated template and confusions; interpolation and built multi-target cases](https://arxiv.org/html/1606.09549v2), consulted the 2026-10-30.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-SOT-002 provenance::agent pole::C pole::D pole::E
END
