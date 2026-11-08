---
id: CV-SOT
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# Single-object tracking: correlation, Siamese networks and MeanShift

## Problem, data and assumptions

Track an initialized target in a sequence, without assuming a multi-object detector or a global identity. Inputs: initial target and frames; output: location of this target with confidence/visibility according to method.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

MeanShift looks for a local-looking distribution mode; CamShift adapts its window to its design. Correlation filters and Siamese networks compare target model and search area. In variants that update their target model, such as KCF, update, and local search create an adaptation/drift tradeoff. SiamFC original instead retains its appearance template during tracking (§4); this update is not universal.

## Mathematics, conventions and units

A high correlation response is a relative score between template and search, not a probability of identity. The maximum observable displacement depends on the search region and cadence. Without discriminating observation after occlusion, identity can remain ambiguous.

## Parameters and properties

Search size, scale, frequency of update, trust and loss policy. A update on a distractor can contaminate the model. Presence detection and location must be distinguished.

## Cost and implementation

Template, research and multiscale calculation dominate. No single-object tracker executed; families are compared at contract level, with no universal FPS.

## Evaluation and controlled variation

Baseline with single target and separate perturbations: occlusion, distractor, field output. Measure accuracy, robustness, loss, and reset policy rather than only successful frames.

## Failure modes and diagnosis

Progressive drift: inspect what is embedded in the template and the actual presence of the target. A high score on a distractor is not evidence of persistence.

## Alternatives and applications

+ combination detector if multiple targets and I/Os are expected; point tracking if the useful output is a point. Define the contract before the model family.

## Guided reasoning and proposed checks

These built cases develop local research, adaptation and identity after occlusion. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-SOT-001

**Question of work**: Why does an initialized single-object tracker not directly replace multi-object tracking of every person in a scene?

**Reference Response**: It starts from a provided target and must relocate it; MOT also manages multiple detections, association, creations and disappearances.

**Difference of problem**: A target provided in the first frame gives the tracker initialization information that a multi-object system must often discover. The MOT must also decide which objects enter or exit, prevent several tracks from representing the same object, and maintain identities despite interactions.

**Constructed example**: Launching a single-object tracker on a person does not automatically identify a second person who enters later. Launching multiple instances can help locate initialized targets, but does not solve their identity collisions, creations, and duplicate removal alone. Set the entries and expected events before choosing architecture. Metrics must also reflect this contract: accuracy conditioned to a favorable manual initialization is not directly comparable to an evaluation where all targets must be discovered automatically.

### Case linked to CV-SOT-002

**Question of work**: During occlusion, a distractor replaces the target in the tracker's template. Which mechanism can reinforce this error?

**Reference Response**: The update of the model on a poorly associated observation can strengthen the distractor and increase drift.

**Drift Loop**: The model learns the appearance of the region he believes to be the target. If the localization becomes false and then serves as a new supervision, the error is integrated into the model; the following frames can then favor the distractor even more. A faster adaptation sometimes strengthens this loop instead of correcting it.

**check**: Record the crops used for the update, answers and loss decisions. Compare a freeze policy under uncertainty to the initial policy, with the same sequences and initialization. Also check the return of the target after occlusion. The gel may protect the model but does not guarantee re-detection if the target exits the search region. This mechanism is for variants that update their template; it should not be assigned indiscriminately to any Siamese tracker or to any fixed template.

**Documentary reference for this pass**: [KCF](https://arxiv.org/pdf/1404.7584), correlation model, circulating offsets and tracking. The other developments are in the [flashcards](../113-tracking-monoobjet.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-SOT-001

**Situation**: Why does an initialized single-object tracker not directly replace multi-object tracking of every person in a scene?

**Multi-tracking and exclusivity**: Multiple independent single-object trackers can converge on the same distractor, each satisfying its own local maximum. They do not necessarily have a common constraint preventing two IDs from representing the same object. A MOT must also define what new observations create a track and how to avoid duplicates. Launching N copies of an initialized tracker is therefore a possible brick, not a complete resolution of these decisions. In a constructed trial, crossing two similar targets and then introducing a third uninitialized target reveals both association ambiguity, exclusivity and birth management.

### CV-SOT-002

**Situation**: During occlusion, a distractor replaces the target in the tracker's template. Which mechanism can reinforce this error?

**Memory of an update**: For an interpolated model $m_t=(1-\eta)m_{t-1}+\eta\hat m_t$, the contribution of an erroneous observation then persists with a $\eta(1-\eta)^k$ factor after $k$ correct updates, in this simplified scheme. A large $\eta$ adapts quickly but integrates more the first error; a small $\eta$ protects better and follows less quickly a legitimate change. This formula describes an interpolation model, not all tracker variants. Examining regions that are actually learned and freezing rules can test for contamination; a fixed template can still be wrong on a distractor without following that wrong learning loop.

**Passages consulted for these developments**: [Bertinetto et al, SiamFC](https://arxiv.org/html/1606.09549v2), §4, unupdated template and confusions; interpolation and built multi-target cases.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-SOT-001 — Independent target searches can collapse to one distractor

Two initialized single-object trackers can both choose the same nearby person because neither enforces a shared one-to-one assignment. Running one tracker per initial person also leaves the problem of new arrivals and departures unspecified. A project MOT design must add those lifecycle and exclusivity rules where required. A strong single-target success score evaluates localization under its initialization protocol, not complete multi-object identity management.

### CV-SOT-002 — Freezing adaptation preserves the model, not visibility

Suspending template updates during a suspected occlusion can prevent contamination, but the target can still move outside the local search region. A recovery policy must then decide how to expand search or re-detect without accepting a distractor. Compare fixed-template and adaptive-template variants on the same occlusion sequences, recording false reacquisition and recovery time. A high similarity to an already contaminated template is circular evidence for continuing adaptation.

Consulted foundations: [SiamFC](https://arxiv.org/html/1606.09549v2): §4 initialized target matching and tracking protocol; [KCF](https://arxiv.org/html/1404.7584v1): tracking pipeline and online model interpolation.

## Sources and flashcards

- [KCF, model tracking and interpolation pipeline](https://arxiv.org/abs/1404.7584): Example of online update, separate from SiamFC's fixed template.

- [OpenCV, Meanshift/Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [SiamFC, method](https://arxiv.org/abs/1606.09549).
- [Related flashcards](../113-tracking-monoobjet.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
