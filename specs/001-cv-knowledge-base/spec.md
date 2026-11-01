# Specification: Computer Vision Senior Knowledge Base

**Branch of work**: `feat/obsidian-pilot` **Establishment**: 2026-10-18 **Editorial review**: 6, pole review and thematic coverage the 2026-10-18 **Status**: framing in implementation; editorial and application validation followed separately **Perimeter Spec Kit**: `specs/001-cv-knowledge-base`

**Demande**: build a vault Obsidian and flashcards exportable to Anki, largely covering classical and modern computer vision, to progress towards a senior generalist profile in industry.

**Confirmed Public**: CV engineer for five years, comfortable in ML/DL, experienced in semantic segmentation. Priority gaps: classic methods, specific vision techniques, matching, calibration/registration, tracking and detection.

**Confirmed Choices**: reference notes complete related to several detailed flashcards; prose in English, English technical terms and preserved original names; explained equations, pseudocode, code and illustrations useful for understanding. The detailed priorities and the pilot remain editorial proposals.

**Start-up decisions, 2026-10-18**: The user requests to start the implementation. The first batch follows the seven initial topics proposed; the confirmed revision client is **AnkiDroid on Android**. The export format remains experimental during this batch, without early technical or pedagogical validation. The initial flashcards are written by an agent, provenance displayed.

**Confirmed Organization**: a directory by theme, inspired by the Knowledge_AI_Engineering repository specified by the user. The flashcards and their reference reference notess are grouped in this theme; the navigation and the subdecks Anki follow this organization.

**Business units, 2026-10-18**: The user requests to cover six clusters related to business families, from A (Image Understanding) to F (Vision Systems & Deployment), described in [cartographie](curriculum.md). Decisions: the poles form an overlay of the existing domains, which remain the organization of the vault; the V0 wave remains devoted to the shortcomings expressed (first); the specs are enriched first and the carry-over in the vault follows by tasks.

The [Relevance Review](review.md) describes the shortcomings of the first version, the corrections and the decisions still open. The width of the catalogue, the quality of the explanations and the transfer in situation are evaluated separately.

## User scenarios and validation

### Course 1 –  Understanding a method (P1)

I want to start from the solved problem to understand how it works, assumptions, parameters and limits, and then find the sources to deepen.

**Justification**: fill the gaps in the vision, building on the ML/DL bases acquired.

**Independent validation**: re-read a reference note of the driver with its flashcards according to the [Pedagogical Contract](learning-design.md), without waiting for the complete catalog.

**Scenarios of acceptance** :

1. By opening a reference note, I find problem, inputs/outputs, hypotheses, steps, parameters, limits, alternatives and primary sources.
2. For each equation, the symbols, conventions and conditions of validity are defined, with the relevant dimensions and units.
3. For a code snippet, I know if it is illustrative or executed and what algorithmic explanation it materializes.

### Course 2 –  Choosing and diagnosing (P1)

I want to compare approaches and reason about the failures of a pipeline under industrial conditions: imperfect data, occlusions, movement, resource constraints and measurement requirements.

**Justification**: develop a technical judgement applicable to projects.

**Independent validation**: treat a comparison case and a diagnostic case, regardless of the Anki export.

**Scenarios of acceptance** :

1. For two methods meeting the same need, I find hypotheses, compromise, criteria of choice and conditions of evaluation.
2. When faced with a symptom, the response distinguishes between possible causes, observations to be collected, discriminating checks and diagnostic limitations.
3. A metric is explained with its protocol and the flaws it can mask.
4. Faced with a different context from the corrected examples, I can propose a method or a diagnosis from the relevant hypotheses and observations.

### 3 –  Review in Obsidian and Anki (Priority P1)

I want to revise contextualized questions to the developed answers, and then return to the reference reference note to deepen or correct the content.

**Justification**: combining pedagogical richness and recall practice.

**Independent validation**: Export a representative set to a trial deck, then edit and export that set again.

**Scenarios of acceptance** :

1. In Anki, the question is understandable without opening the reference note and the correction criteria allow to evaluate my answer.
2. Paragraphs, lists, formulas, images and code remain readable after export, without missing essential information.
3. To unchanged note template, edit a response updates the expected note, without duplicates or loss of the associated revision history.
4. An unmodified export retains the expected number of notes and flashcards.
5. The expected answer and blocking errors allow to correct my reminder, even if the back has optional further study.
6. The revision time and the projected daily load are known before generalizing the format of the flashcards.

### Track 4 –  Navigate and track coverage (P2)

I want to find a notion by problem, method, domain or prerequisite, and identify absent or incomplete subjects.

**Justification**: make visible the gaps and skills actually covered.

**Independent validation**: review the mapping before writing all reference notess.

**Scenarios of acceptance** :

1. Each domain has an inventory whose editorial states are visible.
2. A transverse method has a canonical reference note connected from the domains concerned.
3. An ML/DL prerequisite is bound or recalled when it serves a vision specificity.

### 5 –  Correct and enrich (P2 priority)

I want to add a variant, correct a formula and refresh a source while maintaining the consistency of existing reference notes and flashcards.

**Justification**: avoid that a scientific correction leaves contradictory flashcards.

**Independent validation**: Simulate a fix on a driver topic.

**Scenarios of acceptance** :

1. A correction makes it possible to identify the flashcards concerned.
2. Affirmations that depend on an experiment or version retain their context.
3. A change of format or export is checked on the driver before generalization.

### Course 6 –  Preparing for a business unit (P2)

I want to see, for a targeted family of trades, the areas and subjects to work, their target depth and condition, and then train myself on specific cases of this trade.

**Justification**: connect the general coverage to the expectations of the targeted positions, without duplicating the reference notes.

**Independent validation**: examine the framing of a pole in mapping before writing its reference notes.

**Scenarios of acceptance** :

1. For a cluster, I find perimeter, indicative professions, mobilized domains, key entries and further study, each with its host domain.
2. A subject serving several poles, such as CLIP for A and D, has only one canonical reference note, connected from each of them.
3. The advancement of a pole distinguishes entries inventoried, written and proofread, without inferring my mastery or my aptitude for a position.
4. Each cluster offers a case of design and a case of diagnosis specific to its trades, correctable with explicit criteria.

### Cas limites

- coordinate frame, ambiguous unit, transformation or coordinate convention.
- Method valid in a particular case or subject to degeneration.
- Score published without clearly identified protocol or variant.
- Conflicting sources, unavailable or obsolete.
- flashcard mixing several independent issues and difficult to correct.
- Formula or media operating in the vault but not in the exported deck.
- Note template or different field names depending on the installation of Anki.
- Copy of a flashcard accidentally keeping the identifier of another note.
- Note moved source side or deleted destination side.
- Plugin not available in the current catalog.
- Deleted or modified in Anki not reflected in the source.
- Knowledge recited correctly but not transferred to a new problem.
- Confusion between camera calibration and calibration of a model's scores.
- Image transformation not reflected on boxes, masks or camera settings.
- Comparison using future data, test-set thresholds, or uncounted pre/post-processing costs.
- reference note reported being replayed despite an unresolved central source discrepancy.
- Cited source that does not really support the claim, especially after an agent-assisted writing.
- Rendered correct on Anki Desktop but degraded on the client used to review.
- Subject serving several poles, written twice divergently.
- Business title whose content varies by company or sector.
- Fast-moving models and tools (VLM, VLA, inference runtimes) quoted without date or version.

## Exigences

### Functional requirements

- **FR-001**: the database MUST target the confirmed profile; general ML/DL knowledge serves as acquired prerequisites and contextualized reminders.
- **FR-002**: All learning prose MUST be in English, following the learner’s request of 2026-10-31. Retain original method names, useful acronyms, equations and compatibility identifiers; use consistent computer vision terminology.
- **FR-003**: Coverage MUST include all domains of the [cartographie](curriculum.md), with explicit states and expandable inventory.
- **FR-004**: The inventory MUST distinguish problem, family, method, variant, and evaluation protocol.
- **FR-005**: Each topic MUST indicate the necessary prerequisites and related notions, distinguishing mandatory dependencies and thematic links, with links to fill a gap.
- **FR-006**: A validated reference note MUST comply with [Pedagogical Contract](learning-design.md), with justification for non-applicable entries.
- **FR-007**: Each equation MUST explain symbols, conventions, conditions of application and relevant dimensions/units.
- **FR-008**: code and pseudocode MUST serve an identified explanation and be distinguished; a library call alone is not sufficient to explain the method.
- **FR-009**: Any executable example MUST specify dependencies, entries, and expected result, and be executed in the specified environment. An unexecuted example must be reported.
- **FR-010**: the visuals MUST have an explanatory function, a legend and a provenance; the conditions of reuse must be kept.
- **FR-011**: The properties of a method MUST distinguish between guarantee, approximation, hypothesis, and empirical result, with their limitations.
- **FR-012**: Each validated reference note MUST cite at least one relevant primary source; central assertions must be traceable to their source.
- **FR-013**: Scores and costs dependent on a protocol, hardware, or variant MUST specify these conditions; information that may evolve must have a verification date and a version if relevant.
- **FR-014**: The flashcards MUST cover the relevant families defined in the “flashcards Families” section of [Pedagogical Contract](learning-design.md). A non-applicable family must be justified during the review.
- **FR-015**: each flashcard MUST define a recall objective and correction criteria distinguishing expected answer, optional further explanation and blocking errors; its response remains developed without a ceiling of length. Since the request of the 2026-10-24, all the versoes must be long and explanatory: mechanism, example or reasoning followed and useful limits. The editorial threshold is described in the pedagogical contract; the expected answer remains the rule of correction of the reminder.
- **FR-016**: Each flashcard MUST be connected to a canonical reference note and remain understandable in its autonomous revision context.
- **FR-017**: Reference reference note and flashcards MUST have separate roles; no uniform number of flashcards per method is imposed.
- **FR-018**: Priority areas MUST include cases of choice or diagnosis under industrial constraints, with an evaluable justification.
- **FR-019**: metrics MUST be related to their task and protocol; comparisons must explain their limits of comparability.
- **FR-020**: Educational identifiers MUST be stable and separate from synchronization identities; reference note/flashcard/export relationships are traceable.
- **FR-021**: export MUST preserve developed prose, useful formulas, media and readable code snippets.
- **FR-022**: creation, update and repeated export MUST be checked without duplicate or loss of history to unchanged note template.
- **FR-023**: Remove, move, rename, and source/destination conflicts MUST have documented and tested behavior before generalization.
- **FR-024**: source files MUST remain searchable and versionable regardless of export; the vault is the canonical educational source.
- **FR-025**: Navigation MUST allow search by domain, problem, method and prerequisites, beyond the deck organization.
- **FR-026**: Editorial statements MUST distinguish inventoried subject, reference note written, reference note reread, flashcards written and verified export; they are separate from the personal level of mastery of the learner. To allow this separate tracking, the exported flashcards MUST carry their domain and their family.
- **FR-027**: the distinctions calibration/pose/registration, flow/tracking/reidentification and detector/descriptor/matcher/geometric validation MUST be explicit in the subjects concerned.
- **FR-028**: Large-scale production MUST be preceded by a driver validating the teaching contract, its contrasting cases and export capabilities. The preparatory editorial work remains possible during the choice of the plugin.
- **FR-029**: The catalog MUST make visible scope, gaps and enrichment procedure; its coverage cannot be declared exhaustive by default.
- **FR-030**: Each selected method MUST have an inventory entry with target depth, intended skills, dependencies, and associated artifacts. Priority, depth, editorial status and personal mastery are distinct.
- **FR-031**: Subjects concerned MUST specify the data contract: shapes/types/beaches, color, coordinate frames, units, normalization and propagation of resolution changes, crop, padding or coordinates.
- **FR-032**: Relevant reference notes MUST relate assumptions and failures to acquisition, cadence, temporal causality and industrial constraints; an unapplicable assumption is explicitly ruled out.
- **FR-033**: Each family of the driver MUST offer a simple baseline or reference and a controlled variation, with prediction, expected or observed result and analysis. An analytical or non-executed experiment must be identified.
- **FR-034**: The pilot MUST include two separate cases of the corrected examples for each of its six families: matching, calibration/geometry, tracking, detection, classical segmentation and registration 3D. One case is about choice, the other is about diagnosis, with explicit correction criteria.
- **FR-035**: The instructional essay MUST record a first attempt and a reminder at another session on the dates chosen by the learner, the necessary ambiguities and corrections, without assuming a retention rate. The sample shall cover the six pilot families and each type of flashcard actually produced; its selection shall be recorded before observing the results. The test also measures the duration of revision by flashcard and estimates the daily load of the first production batch, without a ceiling fixed a priori.
- **FR-036**: General properties and implementation features MUST be browsed separately. An unresolved central discrepancy prevents validating the claim and the reference note concerned.
- **FR-037**: Editorial validation MUST retain date, responsibility, evidence and limitations. An auto-review must be identified; blocking errors or correction ambiguities must be resolved before publication.
- **FR-038**: each reference note and each flashcard MUST indicate its writing source: learner, agent or mixed. A central statement written by an agent is only validated after confrontation with the passage of the cited source; the presence of a reference is not enough.
- **FR-039**: The vault MUST be organized by numbered thematic directory, with section index and central summary. The flashcards of a theme and their canonical references MUST be grouped in its directory; the target deck follows the theme. Displacement MUST preserve identifiers and update links, media, and controls. A section without written content MUST display its status, without being counted as acquired coverage.
- **FR-040**: The [cartographie](curriculum.md) MUST define six business units, from A to F, each with perimeter, indicative business units, mobilized domains, key inputs and further study. Poles do not replace domains: each entry specific to a pole has a single host domain, and a subject shared between poles keeps a single canonical reference note.
- **FR-041**: Each inventory entry MUST indicate the poles it serves; reference notes and flashcards exported carry these poles as labels, in order to track progress by pole separately from personal mastery.
- **FR-042**: each cluster MUST propose at least one system design case and one diagnostic case specific to its business, with reference response and correction criteria according to the pedagogical contract.
- **FR-043**: The priorities MUST follow the principle of "base first": the wave V0 remains devoted to the shortcomings expressed; the key inputs of a newly introduced pole are aimed at V1 and operational use, the other V2. An already prioritized entry V0 retains this priority even if several poles reuse it. The coverage of a pole is measured by its artifacts and MUST NOT be presented as an aptitude for a position.

### Principal entities

- **Domain/problem**: visual need, input/output, constraints, families of methods and associated protocols.
- **Method/variant**: identified approach, assumptions, parameters, prerequisites, properties and references.
- **Reference note**: canonical explanation of a topic, flashcards related, editorial status and editorial provenance.
- **flashcard Educational**: ID, question, objective, answer, correction criteria, references, reference note parent, domain, family, poles and writing source.
- **Note / flashcard Anki**: Destination objects; a note can generate multiple flashcards depending on the model. Their identities and numbers are distinct.
- **Source**: primary reference, localization and version context if necessary.
- **Cas industriel**: scenario, constraints, hypotheses, alternatives, observations and criteria for a satisfactory response.
- **Entry of cover**: Subject, host domain, served poles, priority, prerequisites, editorial states and gaps.
- **Business Unit**: scope, indicative professions, mobilized domains, key entries and further study with their host domain, own cases and editorial advancement.
- **Target Skill/Deepness**: an observable result expected for a subject, related to his artifacts and distinct from his priority or his personal mastery.
- **Proof of review or trial**: version of content, date, responsible, criteria applied, result, limits and possible corrections.

A "validated" reference note was reviewed in accordance with the teaching contract, without blocking errors or unresolved central divergences. This status means neither validated export nor acquired personal mastery.

## Criteria for success

### Measurable results

- **SC-001**: All mapping domains have an initial inventory; each selected method entry displays depth, skills, prerequisites, states, and links to its existing artifacts. A general domain line is not enough.
- **SC-002**: 100% of the reference notes declared validated comply with the pedagogical contract and have a primary source; any heading that is not applicable is justified.
- **SC-003**: 100% of the published flashcards have a separate identifier, a parent reference note, an objective and an unambiguous correction kernel, with further study and blocking errors identified.
- **SC-004**: The proposed driver covers the initial topics and then the extensions of `curriculum.md`, including at least one reference note of metric/protocol type, and all the expected contents: prose, list, inline/block formula, image, pseudocode and code.
- **SC-005**: all [Export Pilot](research.md) scenarios have a logged result; creation, update and repetition pass without duplicates or loss of history. An essential rendering failure prevents the solution from being validated.
- **SC-006**: The six families defined in FR-034 each have a case of choice and a case of diagnosis unpublished, that is to say twelve cases. Their precise correction is appropriate to the task, assumptions/conventions, justification, discriminant verification and limits; all applicable criteria must be met to declare a successful case. The failures of the learner remain recorded.
- **SC-007**: A correction of reference note of the driver makes it possible to identify and update the flashcards concerned; no flashcard remains orphan.
- **SC-008**: The flashcards selected for the pedagogical essay have a report of first attempt and delayed recall, with results, limits and corrections; their coverage of families and types is explained, without exclusion of failures. No published flashcard retains an identified blocking defect. The revision time by flashcard and the projected daily load are logged, with the decision to retain or adjust the format of the flashcards.
- **SC-009**: Each pilot family has a documented reference and controlled variation; the evidence distinguishes prediction, observed result, analytical result, and unexecuted example.
- **SC-010**: 100% of the published reference notes and flashcards indicate their source of writing; for content written by an agent, the journal records the central statements faced with their source.
- **SC-011**: each of the six divisions has, in the cartography, its perimeter, its indicative professions, its mobilized domains, its key entries and further study with a unique host domain, as well as a design case and a diagnostic case with reference answers, hypotheses, discriminating verifications and correction criteria; the only statements are not enough to satisfy this criterion.
- **SC-012**: No subject shared between poles has two canonical reference notess; the editorial advancement of each pole is available in vault, distinct from personal mastery.
- **SC-013**: each of the fourteen domains has effective reference notes and flashcards for the entries retained in the cover lot. The matrix distinguishes this thematic coverage, the detailed processing of each algorithm, the variants only introduced and the subjects remaining to be written. None of these states are equivalent to export validation or professional competence.

## Assumptions and Open Decisions

- The areas of cartography reflect the ambition of broad coverage; specializations and variants will be enriched by inventory.
- The six poles and their trade titles come from the request of the user of the 2026-10-18. The titles are indicative: their content varies between companies.
- For pole C, the trajectory planning and the check are out of scope; only the perception that feeds them is covered.
- The technical pilot remains a validation sample. The current application authorizes the editorial preparation of the fourteen domains and six poles before its completion; the contents keep their written status and their temporary export format. Large-scale automated adoption and dissemination remains subject to testing, including history and mobile rendering.
- Priorities, depth levels, two-stage driver and transfer protocol are offered from the expressed gaps; they do not reduce the final coverage and remain adjustable after proofreading.
- No total volume of flashcards, schedule or daily revision time has been imposed by the user. The driver measures the load instead of limiting it.
- The distribution of the wording between the learner and an agent is not fixed. Proposal: the agent writes, the learner confronts the central statements to the sources and at least rephrases the objective and the core of each flashcard. FR-038 only requires the traceability of this choice.
- Scope proposal: 001 covers the framework, the contract and the pilot. The production of the catalog will then be done in batches, with their own spec or a cover follow-up in the vault; this cutting remains to be decided.
- The name of the forgotten plugin remains uncertain. The candidate and its limitations are described in [The search for interoperability](research.md).
- Plugin, final syntax, note templates, and deletion policy will be set during design after a driver in a test deck.
- The Spec Kit constitution is still an unratified model; its examples do not become rules of the project by this draft. Candidate principles to be moved after ratification: language (FR-002), status of properties and traceability of sources (FR-011, FR-012, FR-036), canonical vault (FR-024), separation of editorial states and mastery (FR-026).
- The destination of `to-spec` is not chosen. This local draft uses Spec Kit and does not publish any issue.
- This phase includes the writing of missing content by theme, at the request of the user. It excludes installation in personal applications, a custom synchronizer and a new ML/DL general curriculum. Plan B `.apkg` is implemented in the 2026-10-24 batch for direct import on Android, in accordance with [Export Contract](../../docs/export-apkg.md). The evidence for the Anki engine remains distinct from mobile validation.
- The flashcards support the skills referred to; a number of flashcards or their memorization cannot alone certify senior status.
